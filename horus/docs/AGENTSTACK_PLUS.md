# AgentStack++ Project Generation

Horus now includes a TypeScript-first project generation layer that exceeds simple scaffolding without becoming low-code magic.

## Commands
- `horus init <name> --template <template>`
- `horus generate agent <name>`
- `horus generate task <name>`
- `horus generate tool <name>`
- `horus tools list/search/add/remove/inspect/test/publish`
- `horus config validate/doctor/explain/print`
- `horus dev/build/package/deploy`

## Generated Project Contents
Generated projects include TypeScript config, package.json, source folders, agent/task/tool definitions, MCP/model/memory/permission/eval configs, tests, evals, docs, HORUS.md, CI, Dockerfile, docker-compose, .env.example.

## SDK
`defineAgent`, `defineTask`, `defineTool`, and `runTask` provide a type-safe project API for engineers.

FINAL LOCK: Horus must include AgentStack-level project generation, templates, agent/task/tool scaffolding, provider flexibility, framework-agnostic tooling, observability, and clean developer onboarding, but implemented 100x stronger with TypeScript, React Ink, MCP-native tools, memory, skills, evals, deployment, security gates, and production-grade multi-agent orchestration.
