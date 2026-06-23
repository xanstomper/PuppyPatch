# PuppyPatch — Red Team AI Agent Framework

## Structure

```
puppypatch/
├── agent/          # RedShark — Core Go red team agent (scope gate, evidence chain, tool registry, uncensored prompts)
├── platform/       # Python orchestration platform (cognitive pipeline, MCP bridge, memory, skills)
├── brain/          # Knowledge base (findings, skills, sessions, security research)
├── pentestagent/   # Crew AI pentesting agent (playbooks, MCP, RAG, container runtimes)
├── redamon/        # Reconnaissance orchestrator (GH secrets, GVM, Nuclei, trufflehog, graph DB)
├── pyrit/          # PyRIT red teaming framework docs
├── patches/        # Security patches for AI tooling packages
├── redteamer/      # Universal Vulnerability Detection Engine (CWE/OWASP coverage)
├── PUPPYPATCH.md   # Universal injection prompt — paste into any AI agent
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── SECURITY.md
```

## Ownership

This repo is the monolithic PuppyPatch red team AI agent framework. All subdirectories are part of the same project. The core agent (RedShark) is in `agent/` — a Go binary with compiled scope-gated execution, evidence chaining, and uncensored system prompts. Everything else supports, extends, or documents the red team toolchain and knowledge base.

## How It Works

- **Refusal is compiled, not prompted** — the scope gate in `agent/internal/scope/` enforces the Rules of Engagement in Go code, not LLM instructions
- **Uncensored by architecture** — the LLM never moralizes or self-restricts; it only reports gate refusals
- **Evidence-chained** — every action logs target, technique, timestamp, output, and hash
- **Universal injection** — `PUPPYPATCH.md` transforms any AI agent into a red team operator
