import { checkpointStore, loadConfig } from '@horus/core';
import { ModelRouter, providerFromRef } from '@horus/models';
export type SlashResult = { kind: 'message'|'diff'|'undo'|'status'|'model'|'mcp'; text: string };
export function parseSlashCommand(input: string): { command: string; args: string[] } | undefined {
  if (!input.startsWith('/')) return undefined;
  const [command, ...args] = input.trim().split(/\s+/);
  return { command, args };
}
export function runSlashCommand(input: string, gitStatus = 'unknown'): SlashResult {
  const parsed = parseSlashCommand(input);
  if (!parsed) return { kind: 'message', text: 'not a slash command' };
  const cfg = loadConfig();
  if (parsed.command === '/doctor') return { kind: 'message', text: 'doctor: environment ok' };
  if (parsed.command === '/model') { const provider = providerFromRef(new ModelRouter(cfg.model).route()); const s = provider.status(); return { kind: 'model', text: `model=${cfg.model} mode=${s.mode}${s.warning ? ` warning=${s.warning}` : ''}` }; }
  if (parsed.command === '/status') return { kind: 'status', text: `runtime=phase1-core-mvp git=${gitStatus || 'unknown'} mcp=placeholder` };
  if (parsed.command === '/diff') return { kind: 'diff', text: checkpointStore.diffLastPatch() || 'diff: none' };
  if (parsed.command === '/undo') { try { const cp = checkpointStore.undoLastPatch(); return { kind: 'undo', text: `undo: restored ${cp.file}` }; } catch (e) { return { kind: 'undo', text: `undo: ${(e as Error).message}` }; } }
  if (parsed.command === '/mcp') return { kind: 'mcp', text: 'MCP integration is placeholder-only in Phase 1 and planned for Phase 2.' };
  if (parsed.command === '/help') return { kind: 'message', text: '/doctor /model /status /diff /undo /mcp /help /new /reset' };
  if (parsed.command === '/new' || parsed.command === '/reset') return { kind: 'message', text: `${parsed.command}: session reset` };
  return { kind: 'message', text: `unknown command: ${parsed.command}` };
}
