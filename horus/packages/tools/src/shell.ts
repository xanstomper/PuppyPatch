import { execa } from 'execa';
import { z } from 'zod';
import { classifyCommandRisk, eventBus, redactSecrets } from '@horus/core';

export const RunCommandInput = z.object({ command: z.string(), cwd: z.string().default('.') });
export async function runCommand(input: z.infer<typeof RunCommandInput>) {
  const risk = classifyCommandRisk(input.command);
  if (risk === 'destructive') return { ok: false, error: 'approval required for destructive command', code: 'APPROVAL_REQUIRED' };
  eventBus.emitEvent({ type: 'shell', action: 'start', command: input.command });
  const result = await execa(input.command, { cwd: input.cwd, shell: true, reject: false });
  if (result.stdout) eventBus.emitEvent({ type: 'shell', action: 'stdout', command: input.command, content: redactSecrets(result.stdout) });
  if (result.stderr) eventBus.emitEvent({ type: 'shell', action: 'stderr', command: input.command, content: redactSecrets(result.stderr) });
  eventBus.emitEvent({ type: 'shell', action: 'exit', command: input.command, exitCode: result.exitCode });
  return { ok: result.exitCode === 0, data: { stdout: redactSecrets(result.stdout), stderr: redactSecrets(result.stderr), exitCode: result.exitCode, risk } };
}
