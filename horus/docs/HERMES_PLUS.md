# Horus Hermes++ Capability Map

Horus is TypeScript-first and React Ink terminal-native. This document tracks concrete Hermes-level capability parity without pretending unfinished adapters are complete.

## Implemented Foundations
- Typed event bus driving UI/runtime.
- Layered SQLite + FTS memory with inspect/edit/delete/hybrid search primitives.
- User profile store with confidence/source/sensitive flags.
- Advanced skill schema with version, confidence, anti-patterns, recovery, eval hooks.
- Tool registry with 70+ schema/safety/permission-defined tools and adapter-ready entries.
- Provider routing primitives and OpenAI-compatible endpoint client.
- MCP registry/client/permission gates.
- Backend manager covering local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox, Kubernetes, GitHub Actions, custom.
- Automation spec/store.
- Gateway platform abstraction.
- RPC server skeleton with bearer-token auth and tool listing.
- Trajectory store/export/compression and eval runner baseline.
- Observability JSONL observer and metrics counters.

## Adapter-Ready, Not Overclaimed
Some tools are registered with safe adapter-ready handlers until provider credentials, real cloud backends, or external APIs are configured. Horus exposes this status explicitly.

## Safety
Permission tiers, command risk classifier, redaction, approval queue, safety levels on every tool, dry-run defaults.

FINAL LOCK: Horus must include Hermes-level self-improvement, memory, skills, gateway, scheduling, terminal backends, and trajectory generation, but implemented 100x stronger with TypeScript, React Ink, MCP-native tools, provider routing, safety gates, evals, observability, and a larger tool library.
