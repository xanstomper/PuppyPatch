import fs from 'node:fs';
import path from 'node:path';
import { z } from 'zod';
import { checkpointStore, eventBus, isProtectedFile } from '@horus/core';

export const ReadFileInput = z.object({ path: z.string() });
export const WriteFileInput = z.object({ path: z.string(), content: z.string() });
export const ListFilesInput = z.object({ path: z.string().default('.') });

export function readFile(input: z.infer<typeof ReadFileInput>) { return { ok: true, data: fs.readFileSync(input.path, 'utf8') }; }
export function listFiles(input: z.infer<typeof ListFilesInput>) { return { ok: true, data: fs.readdirSync(input.path) }; }
export function writeFile(input: z.infer<typeof WriteFileInput>) {
  if (isProtectedFile(input.path)) return { ok: false, error: `protected file: ${input.path}`, code: 'PROTECTED_FILE' };
  const cp = checkpointStore.snapshot(input.path, 'before write_file');
  fs.mkdirSync(path.dirname(input.path), { recursive: true });
  fs.writeFileSync(input.path, input.content);
  checkpointStore.recordAfter(cp.id);
  eventBus.emitEvent({ type: 'file', action: 'checkpoint', path: input.path, content: cp.id });
  eventBus.emitEvent({ type: 'file', action: 'write', path: input.path });
  return { ok: true, data: { path: input.path, checkpointId: cp.id } };
}
