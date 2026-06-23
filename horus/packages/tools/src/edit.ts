import { z } from 'zod';
import { checkpointStore, eventBus } from '@horus/core';
import { writeFile, WriteFileInput } from './filesystem.js';
export const PatchFileInput = WriteFileInput.extend({ note: z.string().default('patch_file') });
export function patchFile(input: z.infer<typeof PatchFileInput>) { return writeFile({ path: input.path, content: input.content }); }
export function createCheckpoint(input: { path: string; note?: string }) { const cp = checkpointStore.snapshot(input.path, input.note); eventBus.emitEvent({ type: 'file', action: 'checkpoint', path: input.path, content: cp.id }); return { ok: true, data: cp }; }
export function restoreCheckpoint(input: { id: string }) { const cp = checkpointStore.restoreCheckpoint(input.id); eventBus.emitEvent({ type: 'file', action: 'restore', path: cp.file }); return { ok: true, data: cp }; }
export function undoLastPatch() { const cp = checkpointStore.undoLastPatch(); eventBus.emitEvent({ type: 'file', action: 'undo', path: cp.file }); return { ok: true, data: cp }; }
export function diffLastPatch() { const diff = checkpointStore.diffLastPatch(); eventBus.emitEvent({ type: 'file', action: 'diff', diff }); return { ok: true, data: diff }; }
