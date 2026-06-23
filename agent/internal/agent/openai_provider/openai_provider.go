// Package openai_provider implements the agent.Provider interface against the
// OpenAI Chat Completions API. Because the wire format is stable across many
// providers (OpenAI, local-ai, ollama, vllm, etc.) you only change
// REDSHARK_API_BASE to point RedShark at any compatible endpoint.
//
// Configuration is via environment variables or struct fields:
//   - REDSHARK_API_KEY  (required for cloud endpoints; blank for local)
//   - REDSHARK_API_BASE (default: https://api.openai.com/v1)
//   - REDSHARK_MODEL    (default: gpt-4o)
package openai_provider

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/xanstomper/redteam-agent/internal/agent"
	"github.com/xanstomper/redteam-agent/internal/msg"
)

const (
	defaultAPIBase = "https://api.openai.com/v1"
	defaultModel   = "gpt-4o"
	defaultTimeout = 60 * time.Second
)

// OpenAIProvider implements agent.Provider using the OpenAI Chat Completions API.
// A nil *OpenAIProvider means no live provider is configured; callers should
// fall back to the stub provider rather than hitting the network.
type OpenAIProvider struct {
	// APIKey is the bearer token. Empty is fine for local-ai / ollama.
	APIKey string
	// APIBase is the base URL (e.g. "https://api.openai.com/v1").
	APIBase string
	// Model is the model identifier.
	Model string
	// HTTPClient allows customising the HTTP client (timeouts, TLS, mocks).
	HTTPClient *http.Client
}

// NewOpenAIProvider creates a provider with defaults from environment variables.
// It returns nil when no API key and no local-compatible base URL is supplied,
// which signals to the caller that a live OpenAI/NIM backend is not configured.
func NewOpenAIProvider() *OpenAIProvider {
	base := strings.TrimSpace(os.Getenv("REDSHARK_API_BASE"))
	model := strings.TrimSpace(os.Getenv("REDSHARK_MODEL"))
	key := strings.TrimSpace(os.Getenv("REDSHARK_API_KEY"))

	if base == "" {
		base = defaultAPIBase
	}
	if model == "" {
		model = defaultModel
	}
	if key == "" && !isLocalCompatible(base) {
		return nil
	}

	return &OpenAIProvider{
		APIKey:     key,
		APIBase:    base,
		Model:      model,
		HTTPClient: &http.Client{Timeout: defaultTimeout},
	}
}

func isLocalCompatible(base string) bool {
	b := strings.ToLower(base)
	return strings.HasPrefix(b, "http://localhost") || strings.HasPrefix(b, "http://127.0.0.1") || strings.HasPrefix(b, "http://0.0.0.0")
}

// Using reports whether a live OpenAI-compatible provider is active.
func (p *OpenAIProvider) Using() bool {
	return p != nil
}

// Complete implements agent.Provider. Sends history + tools and returns the
// model response (content text and/or tool calls).
func (p *OpenAIProvider) Complete(ctx context.Context, systemPrompt string, history []msg.Message, toolDefs []agent.ToolDef) (*agent.ProviderResponse, error) {
	if p.HTTPClient == nil {
		p.HTTPClient = &http.Client{Timeout: defaultTimeout}
	}
	messages := buildMessages(systemPrompt, history)
	tools := buildTools(toolDefs)

	reqBody := chatRequest{
		Model:    p.Model,
		Messages: messages,
	}
	if len(tools) > 0 {
		reqBody.Tools = tools
	}

	body, err := json.Marshal(reqBody)
	if err != nil {
		return nil, fmt.Errorf("openai: marshal request: %w", err)
	}

	url := strings.TrimRight(p.APIBase, "/") + "/chat/completions"
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("openai: build request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")
	if p.APIKey != "" {
		req.Header.Set("Authorization", "Bearer "+p.APIKey)
	}

	resp, err := p.HTTPClient.Do(req)
	if err != nil {
		if ctx.Err() != nil {
			return nil, fmt.Errorf("openai: request cancelled: %w", ctx.Err())
		}
		return nil, fmt.Errorf("openai: http do: %w", err)
	}
	defer resp.Body.Close()

	respBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("openai: read body: %w", err)
	}

	if resp.StatusCode != http.StatusOK {
		preview := respBytes
		if len(preview) > 400 {
			preview = preview[:400]
		}
		return nil, fmt.Errorf("openai: API error %d: %s", resp.StatusCode, string(preview))
	}

	parsed, err := parseResponse(respBytes)
	if err != nil {
		return nil, fmt.Errorf("openai: parse response: %w", err)
	}
	return parsed, nil
}

// ---------------------------------------------------------------------------
// OpenAI wire types
// ---------------------------------------------------------------------------

type chatRequest struct {
	Model    string        `json:"model"`
	Messages []chatMessage `json:"messages"`
	Tools    []chatTool    `json:"tools,omitempty"`
}

type chatMessage struct {
	Role       string         `json:"role"`
	Content    string         `json:"content,omitempty"`
	ToolCalls  []chatToolCall `json:"tool_calls,omitempty"`
	ToolCallID string         `json:"tool_call_id,omitempty"`
	Name       string         `json:"name,omitempty"`
}

type chatToolCall struct {
	ID       string           `json:"id,omitempty"`
	Type     string           `json:"type"`
	Function chatFunctionCall `json:"function"`
}

type chatFunctionCall struct {
	Name      string `json:"name"`
	Arguments string `json:"arguments"`
}

type chatTool struct {
	Type     string       `json:"type"`
	Function chatFunction `json:"function"`
}

type chatFunction struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Parameters  any    `json:"parameters"`
}

type chatResponse struct {
	Choices []chatChoice `json:"choices"`
}

type chatChoice struct {
	Message chatMessage `json:"message"`
}

// ---------------------------------------------------------------------------
// Conversion helpers (exported as lowercase for testing inside the package)
// ---------------------------------------------------------------------------

// buildMessages converts the internal history into OpenAI chat messages and
// prepends a system prompt when supplied.
func buildMessages(systemPrompt string, history []msg.Message) []chatMessage {
	out := make([]chatMessage, 0, 1+len(history))

	if strings.TrimSpace(systemPrompt) != "" {
		out = append(out, chatMessage{Role: "system", Content: systemPrompt})
	}

	for _, m := range history {
		switch m.Role {
		case msg.RoleUser:
			out = append(out, chatMessage{Role: "user", Content: m.Content})
		case msg.RoleAssistant:
			cm := chatMessage{Role: "assistant", Content: m.Content}
			// An assistant message that drove a tool call carries the args
			// as Content with ToolName set. Mirror that as a tool_calls entry.
			if m.ToolName != "" {
				cm.ToolCalls = []chatToolCall{{
					ID:   m.ID,
					Type: "function",
					Function: chatFunctionCall{
						Name:      m.ToolName,
						Arguments: m.Content,
					},
				}}
				cm.Content = ""
			}
			out = append(out, cm)
		case msg.RoleTool:
			out = append(out, chatMessage{
				Role:       "tool",
				Content:    m.Content,
				ToolCallID: m.ID,
				Name:       m.ToolName,
			})
		case msg.RoleSystem:
			out = append(out, chatMessage{Role: "system", Content: m.Content})
		case msg.RoleRefusal:
			out = append(out, chatMessage{Role: "assistant", Content: m.Content})
		}
	}
	return out
}

// buildTools converts agent.ToolDef to the OpenAI function-tools wire format.
func buildTools(defs []agent.ToolDef) []chatTool {
	if len(defs) == 0 {
		return nil
	}
	out := make([]chatTool, 0, len(defs))
	for _, d := range defs {
		out = append(out, chatTool{
			Type: "function",
			Function: chatFunction{
				Name:        d.Name,
				Description: d.Description,
				Parameters:  d.Parameters,
			},
		})
	}
	return out
}

// parseResponse decodes an OpenAI chat completion into a ProviderResponse.
func parseResponse(body []byte) (*agent.ProviderResponse, error) {
	var cr chatResponse
	if err := json.Unmarshal(body, &cr); err != nil {
		return nil, fmt.Errorf("unmarshal: %w", err)
	}
	if len(cr.Choices) == 0 {
		return nil, fmt.Errorf("no choices in response")
	}
	choice := cr.Choices[0]
	pr := &agent.ProviderResponse{
		Content: choice.Message.Content,
	}
	for _, tc := range choice.Message.ToolCalls {
		pr.ToolCalls = append(pr.ToolCalls, agent.ToolCall{
			ID:   tc.ID,
			Name: tc.Function.Name,
			Args: tc.Function.Arguments,
		})
	}
	return pr, nil
}
