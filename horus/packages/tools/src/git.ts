import { execa } from 'execa';
import { z } from 'zod';
import { eventBus } from '@horus/core';
export const GitInput = z.object({ cwd: z.string().default('.') });
export async function gitStatus(input: z.infer<typeof GitInput>) { const r = await execa('git', ['status','--short'], { cwd: input.cwd, reject: false }); eventBus.emitEvent({ type: 'git', action: 'status', content: r.stdout }); return { ok: r.exitCode === 0, data: r.stdout }; }
export async function gitDiff(input: z.infer<typeof GitInput>) { const r = await execa('git', ['diff'], { cwd: input.cwd, reject: false }); eventBus.emitEvent({ type: 'git', action: 'diff', content: r.stdout }); return { ok: r.exitCode === 0, data: r.stdout }; }
