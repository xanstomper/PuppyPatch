<div align="center">

```
██████╗ ██╗   ██╗██████╗ ██████╗ ██╗   ██╗██████╗  █████╗ ████████╗ ██████╗██╗  ██╗
██╔══██╗██║   ██║██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║  ██║
██████╔╝██║   ██║██████╔╝██████╔╝ ╚████╔╝ ██████╔╝███████║   ██║   ██║     ███████║
██╔═══╝ ██║   ██║██╔═══╝ ██╔═══╝   ╚██╔╝  ██╔═══╝ ██╔══██║   ██║   ██║     ██╔══██║
██║     ╚██████╔╝██║     ██║        ██║   ██║     ██║  ██║   ██║   ╚██████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝     ╚═╝        ╚═╝   ╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝

**Red Team AI Agent — Terminal-First Security Testing**

[![Go](https://img.shields.io/badge/Go-1.26%2B-00ADD8?style=for-the-badge&logo=go)](https://go.dev)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE.md)
[![Platform](https://img.shields.io/badge/platform-linux%20|%20macOS%20|%20windows-lightgrey?style=for-the-badge)]()
[![AI](https://img.shields.io/badge/AI-5000%2B%20Techniques-ff6b6b?style=for-the-badge)]()
[![Tools](https://img.shields.io/badge/Tools-36%20Engines-845ef7?style=for-the-badge)]()
[![TUI](https://img.shields.io/badge/TUI-Bubble%20Tea-ff6b6b?style=for-the-badge)]()

</div>

---

## What Is PuppyPatch?

PuppyPatch is a **terminal-native red team AI agent** built for authorized security testing. It combines a polished, Crush-inspired TUI with a massive database of 5,000+ attack techniques, code audit patterns, exploit payloads, and security testing methodologies.

Unlike point-and-click security tools, PuppyPatch operates through an **AI-powered chat interface** where you describe what you want to test and it generates the approach, payloads, and remediation steps. The agent is configured with DAN (Do Anything Now) mode for comprehensive security testing — no refusals, no gatekeeping, just direct technical output.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   PuppyPatch TUI                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────────────────────┐  │
│  │   Sidebar    │  │         Chat Interface            │  │
│  │  · Chat      │  │  ● User: scan this target         │  │
│  │  · Sessions  │  │  ● PP: ⚡ AI-Infra-Guard scan..  │  │
│  │  · Models    │  │  ● User: audit this file          │  │
│  │  · Findings  │  │  ● PP: 📋 Found 12 vulns...      │  │
│  │  · Skills    │  │                                   │  │
│  │              │  │  ═══════════════════════════════   │  │
│  │              │  │  ::::: scan target.com             │  │
│  └─────────────┘  └──────────────────────────────────┘  │
│  ─────────────────────────────────────────────────────  │
│  ctrl+p · ctrl+m · ctrl+f · ctrl+h · ctrl+c            │
└─────────────────────────────────────────────────────────┘
```

## Features

### 🎯 5,000+ Security Testing Techniques

| Category | Count | Description |
|----------|-------|-------------|
| Code Audit Patterns | 1,800+ | Python, JS/TS, Go, Rust, Java, C#, PHP, C/C++, Solidity |
| Exploit Payloads | 1,500+ | SQLi, XSS, command injection, SSRF, SSTI, XXE, deserialization, JWT |
| Network Commands | 500+ | Reconnaissance, exploitation, post-exploitation tool commands |
| Jailbreak Techniques | 100+ | 5 levels: direct, roleplay, encoding, technical, advanced |
| Evasion Methods | 200+ | WAF bypass, IDS evasion, log tampering, rate-limit bypass |
| Crypto Attacks | 100+ | Weak hashes, broken encryption, side-channel, key management |
| Attack Patterns | 200+ | OWASP Top 10, CWE Top 25, CWE-1000 taxonomy |

### 🛠️ 36 Integrated Security Engines

| Engine | Purpose |
|--------|---------|
| **AI-Infra-Guard** | Full-stack AI infrastructure scanning |
| **Garak** | LLM vulnerability probing |
| **PyRIT** (Microsoft) | AI red teaming framework |
| **PentestAgent** | Black-box penetration testing |
| **RedTeamerAgent** | Deep SAST code auditing |
| **Agentic Security** | LLM fuzzing & scanning |
| **OBLITERATUS** | Refusal direction projection for model testing |
| **Cognitive Frameworks** | OWL/ANCHOR/DOX/SISPIS pipeline |

### 🖥️ Professional Terminal UI

Built on **Bubble Tea** (the same framework powering Crush, Glow, and other Charm tools), the TUI features:

- **Command Palette** (Ctrl+P) — fuzzy-search all commands
- **Model Switcher** (Ctrl+M) — swap between 6 providers
- **Findings Panel** (Ctrl+F) — browse discovered vulnerabilities by severity
- **Help Overlay** (Ctrl+H) — full command reference
- **Multi-Provider LLM Support** — Anthropic, OpenAI, OpenRouter, DeepSeek, Ollama, NVIDIA
- **Vim-style navigation** — PgUp/PgDn scroll, Tab focus cycling

### 🧠 Agent Capabilities

The AI agent operates with **full compliance** for security testing:

- Generates realistic exploit payloads for verification
- Performs deep code audits across 16+ languages
- Maps attack surfaces and enumerates vulnerabilities
- Produces CVSS-scored findings with CWE mappings
- Suggests remediation and patches
- Maintains session history and tracks findings

## Installation

### From Source

```bash
git clone https://github.com/xanstomper/PuppyPatch.git
cd PuppyPatch
go build -o puppypatch .
./puppypatch
```

### From Binary

```bash
# Download the latest release for your platform
curl -L https://github.com/xanstomper/PuppyPatch/releases/latest/download/puppypatch-linux-amd64 -o ~/.local/bin/puppy
chmod +x ~/.local/bin/puppy
puppy
```

## Quick Start

```bash
# Launch interactive TUI
puppy

# Run non-interactive commands
puppy help
puppy models

# Or for direct terminal access (no TTY needed)
puppy --help
```

### Configuration

Config file: `~/.puppypatch/config.json`

```json
{
  "provider": "ollama",
  "model": "llama3.3",
  "api_keys": {
    "anthropic": "",
    "openai": "",
    "openrouter": "",
    "deepseek": "",
    "nvidia": ""
  }
}
```

Set a provider:
```bash
puppy login anthropic    # Login with API key
puppy models             # List available models
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+P` | Command palette |
| `Ctrl+M` | Switch model/provider |
| `Ctrl+F` | Toggle findings view |
| `Ctrl+H` | Help overlay |
| `Ctrl+C` | Quit |
| `PgUp/PgDn` | Scroll chat |
| `Esc` | Close overlay |
| `Tab` | Cycle focus |
| `Ctrl+N` | New session |
| `Ctrl+S` | Session list |

## Commands

```
  /scan <target>       AI-Infra-Guard scan
  /audit <path>        RedTeamerAgent code audit
  /pentest <target>    PentestAgent session
  /garak <target>      Garak LLM scanner
  /jailbreak           List 100+ jailbreak techniques
  /knowledge <q>       Search knowledge base
  /exploit <q>         Generate exploit payloads
  /patch <vuln>        Remediation guidance
  /secrets <path>      Scan for secrets
  /network <target>    Network reconnaissance
  /web <target>        Web application scan
  /tools               List all 36 engines
  /status              Agent status
  /findings            Discovered vulnerabilities
  /skills              Learned skills
  /model               Switch model
  /provider <name>     Switch provider
  /clear               Clear chat
  /help                Show help
```

## Security Testing Methodology

PuppyPatch follows a structured red team workflow:

1. **Reconnaissance** — Map the attack surface, identify entry points, enumerate services
2. **Analysis** — Scan for vulnerabilities, audit code, probe for weaknesses
3. **Exploitation** — Test and verify findings with safe exploitation techniques
4. **Reporting** — Document with severity scoring, CWE mapping, remediation steps
5. **Remediation** — Generate production-ready fixes with validation

> **⚠️ Authorized Testing Only**
> PuppyPatch is designed for authorized security assessments. Always ensure you have explicit permission before testing any system. Government, critical infrastructure, and educational institutions require explicit authorization.

## Project Structure

```
PuppyPatch/
├── main.go                    # Entry point
├── internal/
│   ├── agent/                 # Agent coordinator & tools
│   ├── app/                   # Application lifecycle
│   ├── cmd/                   # CLI commands
│   ├── config/                # Configuration management
│   ├── db/                    # SQLite database
│   ├── redteam/               # Red team tool registry
│   ├── session/               # Session management
│   ├── message/               # Message handling
│   ├── skills/                # Skill tracking
│   ├── ui/                    # TUI rendering
│   │   ├── model/             # Main TUI components
│   │   ├── chat/              # Chat message rendering
│   │   ├── dialog/            # Dialog overlays
│   │   ├── styles/            # Theming
│   │   └── logo/              # Logo rendering
│   └── version/               # Version info
└── go.mod
```

## License

MIT — See [LICENSE.md](LICENSE.md)

## Acknowledgments

- [Charmbracelet](https://charm.sh) — Bubble Tea and the TUI ecosystem
- [Crush](https://github.com/charmbracelet/crush) — TUI inspiration and architecture
- All the open-source security tools that make this possible

---

<div align="center">
  <sub>Built for authorized security testing. Use responsibly.</sub>
</div>
