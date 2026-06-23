package redteam

type Tool struct {
	Name        string
	Description string
	Category    string
}

func AllTools() []Tool {
	return []Tool{
		{Name: "scan", Description: "AI-Infra-Guard scan", Category: "redteam"},
		{Name: "audit", Description: "RedTeamerAgent audit", Category: "redteam"},
		{Name: "pentest", Description: "PentestAgent session", Category: "redteam"},
		{Name: "garak", Description: "Garak LLM scanner", Category: "redteam"},
		{Name: "pyrit", Description: "PyRIT framework", Category: "redteam"},
		{Name: "agentic_sec", Description: "Agentic Security scanner", Category: "redteam"},
		{Name: "jailbreak", Description: "Jailbreak techniques", Category: "attack"},
		{Name: "exploit", Description: "Exploit generation", Category: "attack"},
		{Name: "injection", Description: "Prompt injection", Category: "attack"},
		{Name: "leak", Description: "Prompt leakage", Category: "attack"},
		{Name: "evasion", Description: "Evasion techniques", Category: "attack"},
		{Name: "network_scan", Description: "Network recon", Category: "scanning"},
		{Name: "web_scan", Description: "Web app scan", Category: "scanning"},
		{Name: "secrets_scan", Description: "Secrets detection", Category: "scanning"},
		{Name: "dep_check", Description: "Dependency check", Category: "scanning"},
		{Name: "code_analysis", Description: "Code analysis", Category: "analysis"},
		{Name: "fuzzing", Description: "Fuzz testing", Category: "testing"},
		{Name: "knowledge", Description: "Knowledge base query", Category: "knowledge"},
		{Name: "cwe_lookup", Description: "CWE taxonomy lookup", Category: "knowledge"},
		{Name: "owasp_lookup", Description: "OWASP LLM lookup", Category: "knowledge"},
		{Name: "attack_lib", Description: "Attack pattern library", Category: "knowledge"},
		{Name: "patch", Description: "Generate patch", Category: "remediation"},
		{Name: "fix", Description: "Auto-fix vulns", Category: "remediation"},
		{Name: "remediate", Description: "Remediation workflow", Category: "remediation"},
		{Name: "redshark_agent", Description: "RedShark agent spawning", Category: "agent"},
		{Name: "redshark_skill", Description: "RedShark skill management", Category: "agent"},
		{Name: "redshark_mcp", Description: "RedShark MCP integration", Category: "agent"},
		{Name: "hermes_agent", Description: "Hermes multi-agent", Category: "agent"},
		{Name: "multi_agent", Description: "Multi-agent coordination", Category: "agent"},
		{Name: "owl_reason", Description: "OWL cognitive reasoning", Category: "cognitive"},
		{Name: "obliteratus", Description: "OBLITERATUS abliteration", Category: "cognitive"},
		{Name: "shell", Description: "Shell execution", Category: "utility"},
		{Name: "python", Description: "Python execution", Category: "utility"},
		{Name: "help", Description: "Tool help", Category: "utility"},
		{Name: "status", Description: "Agent status", Category: "utility"},
	}
}

func AllToolNames() []string {
	tools := AllTools()
	names := make([]string, len(tools))
	for i, t := range tools {
		names[i] = t.Name
	}
	return names
}

func ToolByName(name string) *Tool {
	for _, t := range AllTools() {
		if t.Name == name {
			return &t
		}
	}
	return nil
}
