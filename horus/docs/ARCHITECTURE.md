# Architecture

Phase 1 architecture:
- Commander CLI launches React Ink.
- Ink UI subscribes to typed runtime events.
- Single-agent runtime uses mock-first model adapter, project instructions, and safe tools.
- Tools are Zod-validated and return structured results.
- File edits go through checkpoint/diff/undo.
- MCP is a placeholder event/panel/command only.
