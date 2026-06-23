import fs from 'node:fs';
import { eventBus, loadConfig } from '@horus/core';
import { ModelRouter, providerFromRef } from '@horus/models';
import { createMvpToolRegistry } from '@horus/tools';
import { loadProjectInstructions } from './agentRuntime.js';

export async function runCodingLoop(prompt: string, cwd = '.') {
  eventBus.emitEvent({ type: 'task', action: 'new', content: prompt });
  const config = loadConfig();
  const router = new ModelRouter(config.model);
  const provider = providerFromRef(router.route());
  const instructions = loadProjectInstructions(cwd);
  eventBus.emitEvent({ type: 'agent', action: 'start', content: 'single-agent coding loop started' });
  const registry = createMvpToolRegistry();
  eventBus.emitEvent({ type: 'tool', action: 'start', tool: 'git_status' });
  const status = await registry.call('git_status', { cwd });
  eventBus.emitEvent({ type: 'tool', action: 'done', tool: 'git_status', ok: status.ok, content: String(status.data ?? status.error ?? '') });
  const planPrompt = `Project instructions:\n${instructions.horus ?? ''}\n\nUser task:\n${prompt}`;
  const plan = await provider.call(planPrompt);
  eventBus.emitEvent({ type: 'agent', action: 'plan', content: plan });
  const lower = prompt.toLowerCase();
  if (lower.includes('diff') || lower.includes('status') || lower.includes('audit')) {
    const diff = await registry.call('git_diff', { cwd });
    eventBus.emitEvent({ type: 'tool', action: 'done', tool: 'git_diff', ok: diff.ok, content: String(diff.data ?? '') });
  }
  const verifyCommand = detectVerificationCommand(cwd);
  let verification = 'no verification command detected';
  if (verifyCommand) {
    const result = await registry.call('run_command', { command: verifyCommand, cwd });
    verification = JSON.stringify(result.data ?? result.error);
  }
  const final = `Plan created. Git inspected. Verification: ${verification}`;
  eventBus.emitEvent({ type: 'agent', action: 'done', content: final });
  eventBus.emitEvent({ type: 'task', action: 'done', content: final });
  return { plan, final };
}
export function detectVerificationCommand(cwd = '.') {
  if (fs.existsSync(`${cwd}/package.json`)) return 'pnpm test';
  if (fs.existsSync(`${cwd}/pyproject.toml`)) return 'pytest -q';
  return undefined;
}

