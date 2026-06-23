# Horus by Aporia — Phase 1 Core MVP

Horus Phase 1 is a TypeScript-first React Ink terminal coding-agent foundation. It is intentionally small and reliable.

## Install
```bash
pnpm install
```

## Run
```bash
pnpm horus
pnpm horus doctor
pnpm horus model list
pnpm horus model set openrouter:anthropic/claude-sonnet-4.5
```

## Validate
```bash
pnpm build
pnpm test
```

## What Phase 1 includes
- TypeScript monorepo
- `horus` CLI entrypoint
- React Ink black terminal UI
- typed event bus
- slash command parser
- prompt input
- transcript pane
- right sidebar
- mock model adapter by default
- model router skeleton
- file tools
- shell tool
- git status/diff tools
- checkpoint/diff/undo
- safety/risk classifier
- config loader
- `HORUS.md` project-instruction loader
- basic single-agent coding loop
- tests

## Phase 1 slash commands
- `/doctor`
- `/model`
- `/status`
- `/diff`
- `/undo`
- `/mcp`
- `/help`
- `/new`
- `/reset`

## Mock model behavior
Horus runs offline by default. The model adapter uses mock responses unless:

```bash
HORUS_MOCK_MODEL=0
```

is set and provider credentials/config are valid. If credentials are missing, Horus falls back to mock mode and emits a clear warning.

## MCP Phase 1 rule
MCP is placeholder-only in Phase 1:
- TUI MCP status panel
- MCP event type placeholder
- `/mcp` command says integration is planned for Phase 2

No real MCP tool calling exists in Phase 1.

## Intentionally deferred
- No swarm mode
- No 60-agent orchestration
- No Hermes++ memory/skills loop
- No autonomous skill creation
- No AgentStack++ project generation
- No template engine
- No gateway
- No dashboard
- No messaging integrations
- No cloud backends
- No scheduled automations
- No trajectory export/training
- No benchmark suite beyond MVP tests
- No full MCP implementation
- No Claude Code/OpenCode parity claim

## Checkpoint / undo
`write_file` and `patch_file` snapshot the original file before editing. `/diff` shows the latest patch diff. `/undo` restores the latest checkpoint.
