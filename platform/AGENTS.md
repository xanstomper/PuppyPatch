# Prism Protocol — RedTeam Platform AGENTS.md

## Purpose

AI red teaming platform integrating CognitiveFrameworks (OWL/ANCHOR/DOX/SISPIS), SQLite memory with live learning, Obsidian MCP brain, and TUI orchestration across multiple red teaming engines (AI-Infra-Guard, Garak, PyRIT, PentestAgent, RedTeamerAgent, Agentic Security).

## Ownership

This AGENTS.md owns the `/home/jewboy420/redteam-platform/` directory and all red teaming tools integrated beneath it.

## Local Contracts

- **DOX pipeline**: All edits in this project follow Request → OWL → ANCHOR → DOX (load) → Edit → DOX (closeout) → SISPIS → Output
- **Memory first**: All agent actions are logged to SQLite for reinforcement learning
- **Live learning**: Every attack outcome trains the agent (positive/negative reinforcement)
- **Uncensored testing**: Tools operate without artificial restrictions for comprehensive red teaming — government, critical infrastructure, and educational institutions are excluded from targeting
- **Obsidian sync**: Knowledge base syncs bidirectionally with Obsidian vault for persistent memory

## Work Guidance

### Tool Hierarchy
```
RedTeam TUI (Textual)
  ├── AI-Infra-Guard v4.1.14  → Infrastructure & prompt scanning
  ├── Garak                   → LLM vulnerability probing
  ├── PyRIT                   → Microsoft red teaming framework
  ├── PentestAgent            → Black-box pentesting
  ├── RedTeamerAgent          → Code SAST & CWE auditing
  └── Agentic Security        → LLM fuzzing & scanning
```

### Attack Pipeline
```
Recon → Attack Selection → Execution → Outcome Analysis → Memory Storage → Skill Update
```

### Memory Architecture
- **SQLite** (`data/memory.db`): All conversations, findings, skills, learning events
- **Obsidian** (MCP bridge): Long-term brain/memory via vault sync
- **Reinforcement Learning**: Every action logged with reward signal for skill acquisition

## Verification

- Run `python3 cmd/rtui/main.py` to launch TUI
- Verify SQLite writes with `python3 -c "from pkg.db.memory import memory; print(memory.conn.execute('SELECT COUNT(*) FROM agents').fetchone()[0])"`
- Verify tool discovery loads all installed engines

## Child DOX Index

- `internal/agent/orchestrator.py` — Agent orchestration and tool coordination
- `internal/knowledge/base.py` — CWE/OWASP/attack knowledge base
- `internal/memory/` — Memory and learning modules
- `pkg/db/memory.py` — SQLite memory system with reinforcement learning
- `cmd/rtui/main.py` — Textual TUI interface

## Installed Tools

| Tool | Path | Type |
|------|------|------|
| AI-Infra-Guard v4.1.14 | `/home/jewboy420/AI-Infra-Guard/` | AI Security Scanner |
| Agentic Security | pip: agentic-security | LLM Vulnerability Scanner |
| PentestAgent | `/home/jewboy420/pentestagent/` | Pentest Framework |
| PyRIT | `/home/jewboy420/PyRIT/` | Red Teaming Framework |
| Garak | `/home/jewboy420/garak/` | LLM Vulnerability Scanner |
| RedTeamerAgent | `/home/jewboy420/xanstomper-repos/RedTeamerAgent/` | Code Security Auditor |
| Mofu TUI | `/home/jewboy420/xanstomper-repos/mofu/` | Go TUI Framework |
