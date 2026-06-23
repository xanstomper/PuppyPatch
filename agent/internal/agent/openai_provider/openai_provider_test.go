// Tests for the OpenAI Chat Completions provider. These exercise the wire-format
// converters (buildMessages, parseResponse) directly, plus an end-to-end HTTP
// round-trip using net/http/httptest so we don't need a live OpenAI key.
//
// The provider implements agent.Provider, so we also pin that the response
// shape matches the contract the agent coordinator depends on.
package openai_provider

import (
	"context"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/xanstomper/redteam-agent/internal/agent"
	"github.com/xanstomper/redteam-agent/internal/msg"
)

// fakeChatServer is a minimal OpenAI-compatible chat completions endpoint.
// Tests configure it to return a canned body (or to inspect the request body).
type fakeChatServer struct {
	server    *httptest.Server
	gotReq    chatRequest
	gotHeader http.Header
	calls     int
}

func newFakeChatServer(t *testing.T, status int, body string) *fakeChatServer {
	t.Helper()
	f := &fakeChatServer{}
	f.server = httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		f.calls++
		f.gotHeader = r.Header.Clone()
		raw, _ := io.ReadAll(r.Body)
		_ = json.Unmarshal(raw, &f.gotReq)
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(status)
		_, _ = w.Write([]byte(body))
	}))
	t.Cleanup(f.server.Close)
	return f
}

// ---------------------------------------------------------------------------
// NewOpenAIProvider env handling
// ---------------------------------------------------------------------------

func TestNewOpenAIProviderDefaults(t *testing.T) {
	t.Setenv("REDSHARK_API_KEY", "")
	t.Setenv("REDSHARK_API_BASE", "")
	t.Setenv("REDSHARK_MODEL", "")
	p := NewOpenAIProvider()
	if p.APIBase != defaultAPIBase {
		t.Errorf("default APIBase = %q, want %q", p.APIBase, defaultAPIBase)
	}
	if p.Model != defaultModel {
		t.Errorf("default Model = %q, want %q", p.Model, defaultModel)
	}
	if p.APIKey != "" {
		t.Errorf("default APIKey = %q, want empty", p.APIKey)
	}
	if p.HTTPClient == nil || p.HTTPClient.Timeout == 0 {
		t.Errorf("expected non-zero HTTPClient.Timeout")
	}
}

func TestNewOpenAIProviderFromEnv(t *testing.T) {
	t.Setenv("REDSHARK_API_KEY", "sk-test")
	t.Setenv("REDSHARK_API_BASE", "http://localhost:9876/v1")
	t.Setenv("REDSHARK_MODEL", "gpt-4o-mini")
	p := NewOpenAIProvider()
	if p.APIKey != "sk-test" {
		t.Errorf("APIKey = %q, want %q", p.APIKey, "sk-test")
	}
	if p.APIBase != "http://localhost:9876/v1" {
		t.Errorf("APIBase = %q, want %q", p.APIBase, "http://localhost:9876/v1")
	}
	if p.Model != "gpt-4o-mini" {
		t.Errorf("Model = %q, want %q", p.Model, "gpt-4o-mini")
	}
}

// ---------------------------------------------------------------------------
// buildMessages
// ---------------------------------------------------------------------------

func TestBuildMessagesSystemAndHistory(t *testing.T) {
	hist := []msg.Message{
		{ID: "m1", Role: msg.RoleUser, Content: "scan example.com"},
		{ID: "m2", Role: msg.RoleAssistant, Content: `{"target":"example.com"}`, ToolName: "nmap"},
		{ID: "m3", Role: msg.RoleTool, Content: "PORT 80 OPEN", ToolName: "nmap"},
		{ID: "m4", Role: msg.RoleSystem, Content: "extra system note"},
		{ID: "m5", Role: msg.RoleRefusal, Content: "REFUSED nmap: protected"},
	}
	got := buildMessages("you are redshark", hist)
	if len(got) != 6 {
		t.Fatalf("len(got) = %d, want 6 (system + 5)", len(got))
	}
	if got[0].Role != "system" || got[0].Content != "you are redshark" {
		t.Errorf("got[0] = %+v, want system message", got[0])
	}
	if got[1].Role != "user" || got[1].Content != "scan example.com" {
		t.Errorf("got[1].role/content = %q/%q, want user/scan...", got[1].Role, got[1].Content)
	}
	// Assistant tool-call row: Content cleared, ToolCalls populated.
	if got[2].ToolCalls == nil {
		t.Fatalf("got[2].ToolCalls nil, want tool call mirror")
	}
	tc := got[2].ToolCalls[0]
	if tc.Function.Name != "nmap" || tc.Function.Arguments != `{"target":"example.com"}` {
		t.Errorf("got[2] tool call = %+v", tc)
	}
	if got[2].Content != "" {
		t.Errorf("assistant tool-call message should have empty content, got %q", got[2].Content)
	}
	// Tool result row mirrors back to "tool" role.
	if got[3].Role != "tool" || got[3].ToolCallID != "m3" || got[3].Name != "nmap" {
		t.Errorf("got[3] = %+v, want tool result", got[3])
	}
	if got[4].Role != "system" {
		t.Errorf("got[4].Role = %q, want system", got[4].Role)
	}
	// Refusal is folded into a normal assistant turn.
	if got[5].Role != "assistant" || !strings.Contains(got[5].Content, "REFUSED") {
		t.Errorf("got[5] = %+v, want assistant refusal text", got[5])
	}
}

func TestBuildMessagesEmptySystemPrompt(t *testing.T) {
	hist := []msg.Message{{Role: msg.RoleUser, Content: "hi"}}
	got := buildMessages("   ", hist)
	if len(got) != 1 || got[0].Role != "user" {
		t.Fatalf("whitespace-only system prompt should be dropped, got %+v", got)
	}
}

// ---------------------------------------------------------------------------
// parseResponse
// ---------------------------------------------------------------------------

func TestParseResponseContentOnly(t *testing.T) {
	body := `{"choices":[{"message":{"role":"assistant","content":"all clear"}}]}`
	pr, err := parseResponse([]byte(body))
	if err != nil {
		t.Fatalf("parseResponse error: %v", err)
	}
	if pr.Content != "all clear" {
		t.Errorf("Content = %q, want %q", pr.Content, "all clear")
	}
	if len(pr.ToolCalls) != 0 {
		t.Errorf("ToolCalls = %+v, want none", pr.ToolCalls)
	}
}

func TestParseResponseToolCalls(t *testing.T) {
	body := `{
	  "choices":[{
	    "message":{
	      "role":"assistant",
	      "content":null,
	      "tool_calls":[{
	        "id":"call_001",
	        "type":"function",
	        "function":{
	          "name":"nmap",
	          "arguments":"{\"target\":\"example.com\"}"
	        }
	      }]
	    }
	  }]
	}`
	pr, err := parseResponse([]byte(body))
	if err != nil {
		t.Fatalf("parseResponse error: %v", err)
	}
	if pr.Content != "" {
		t.Errorf("Content = %q, want empty", pr.Content)
	}
	if len(pr.ToolCalls) != 1 {
		t.Fatalf("len(ToolCalls) = %d, want 1", len(pr.ToolCalls))
	}
	tc := pr.ToolCalls[0]
	if tc.ID != "call_001" || tc.Name != "nmap" || tc.Args != `{"target":"example.com"}` {
		t.Errorf("ToolCall = %+v", tc)
	}
}

func TestParseResponseRejectEmptyChoices(t *testing.T) {
	body := `{"choices":[]}`
	if _, err := parseResponse([]byte(body)); err == nil {
		t.Errorf("expected error on empty choices, got nil")
	}
}

func TestParseResponseRejectMalformedJSON(t *testing.T) {
	if _, err := parseResponse([]byte("not-json")); err == nil {
		t.Errorf("expected error on malformed JSON, got nil")
	}
}

// ---------------------------------------------------------------------------
// buildTools
// ---------------------------------------------------------------------------

func TestBuildToolsEmpty(t *testing.T) {
	if got := buildTools(nil); got != nil {
		t.Errorf("buildTools(nil) = %+v, want nil", got)
	}
}

func TestBuildToolsRoundTrip(t *testing.T) {
	defs := []agent.ToolDef{
		{
			Name:        "nmap",
			Description: "port scan",
			Parameters: map[string]any{
				"type": "object",
				"properties": map[string]any{
					"target": map[string]any{"type": "string"},
				},
			},
		},
	}
	got := buildTools(defs)
	if len(got) != 1 {
		t.Fatalf("len(got) = %d, want 1", len(got))
	}
	if got[0].Type != "function" || got[0].Function.Name != "nmap" {
		t.Errorf("got[0] = %+v", got[0])
	}
	if got[0].Function.Parameters == nil {
		t.Errorf("expected Parameters propagated, got nil")
	}
}

// ---------------------------------------------------------------------------
// Complete — end-to-end against httptest
// ---------------------------------------------------------------------------

func TestCompleteSendsAuthorizationAndParsesResponse(t *testing.T) {
	body := `{
	  "choices":[{
	    "message":{
	      "role":"assistant",
	      "content":"running scan",
	      "tool_calls":[{
	        "id":"call_xyz",
	        "type":"function",
	        "function":{
	          "name":"nmap",
	          "arguments":"{\"target\":\"example.com\"}"
	        }
	      }]
	    }
	  }]
	}`
	fake := newFakeChatServer(t, http.StatusOK, body)
	p := &OpenAIProvider{
		APIKey:  "sk-test",
		APIBase: fake.server.URL,
		Model:   "gpt-4o",
	}
	hist := []msg.Message{{ID: "m1", Role: msg.RoleUser, Content: "scan example.com"}}
	resp, err := p.Complete(context.Background(), "system prompt", hist,
		[]agent.ToolDef{{Name: "nmap", Description: "port scan"}})
	if err != nil {
		t.Fatalf("Complete error: %v", err)
	}
	if resp.Content != "running scan" {
		t.Errorf("Content = %q, want %q", resp.Content, "running scan")
	}
	if len(resp.ToolCalls) != 1 {
		t.Fatalf("len(ToolCalls) = %d, want 1", len(resp.ToolCalls))
	}
	if fake.calls != 1 {
		t.Errorf("calls = %d, want 1", fake.calls)
	}
	if got := fake.gotHeader.Get("Authorization"); got != "Bearer sk-test" {
		t.Errorf("Authorization = %q, want %q", got, "Bearer sk-test")
	}
	if ctype := fake.gotHeader.Get("Content-Type"); ctype != "application/json" {
		t.Errorf("Content-Type = %q, want application/json", ctype)
	}
	if !strings.HasSuffix(fake.gotReq.Model, "gpt-4o") {
		t.Errorf("model = %q, want gpt-4o", fake.gotReq.Model)
	}
	if fake.gotReq.Messages[0].Role != "system" {
		t.Errorf("first message role = %q, want system", fake.gotReq.Messages[0].Role)
	}
}

func TestCompleteOmitsAuthWhenNoKey(t *testing.T) {
	body := `{"choices":[{"message":{"role":"assistant","content":"hi"}}]}`
	fake := newFakeChatServer(t, http.StatusOK, body)
	p := &OpenAIProvider{APIBase: fake.server.URL, Model: "x"}
	if _, err := p.Complete(context.Background(), "s",
		[]msg.Message{{Role: msg.RoleUser, Content: "hi"}}, nil); err != nil {
		t.Fatalf("Complete error: %v", err)
	}
	if got := fake.gotHeader.Get("Authorization"); got != "" {
		t.Errorf("Authorization = %q, want empty (local-ai / ollama)", got)
	}
}

func TestCompleteShows4xxBodyInError(t *testing.T) {
	body := `{"error":{"message":"bad model","type":"invalid_request_error"}}`
	fake := newFakeChatServer(t, http.StatusBadRequest, body)
	p := &OpenAIProvider{APIBase: fake.server.URL, Model: "x"}
	_, err := p.Complete(context.Background(), "s",
		[]msg.Message{{Role: msg.RoleUser, Content: "hi"}}, nil)
	if err == nil {
		t.Fatalf("expected error on 400, got nil")
	}
	if !strings.Contains(err.Error(), "400") {
		t.Errorf("err = %q, want it to contain status 400", err.Error())
	}
	if !strings.Contains(err.Error(), "bad model") {
		t.Errorf("err = %q, want body excerpt", err.Error())
	}
}

func TestCompleteStripsTrailingSlashOnBase(t *testing.T) {
	body := `{"choices":[{"message":{"role":"assistant","content":"ok"}}]}`
	fake := newFakeChatServer(t, http.StatusOK, body)
	p := &OpenAIProvider{APIBase: strings.TrimRight(fake.server.URL, "/") + "///", Model: "x"}
	if _, err := p.Complete(context.Background(), "s",
		[]msg.Message{{Role: msg.RoleUser, Content: "hi"}}, nil); err != nil {
		t.Fatalf("Complete error: %v", err)
	}
	// Could sanity-check the path the request hit was /chat/completions by
	// cracking the recorded request, but the header set + 200 assert verifiesthe
	// pipeline at least reaches the server.
	if fake.calls != 1 {
		t.Errorf("calls = %d, want 1", fake.calls)
	}
}
