import fs from 'node:fs';
import path from 'node:path';
import { createPatch } from 'diff';

export type Checkpoint = { id: string; file: string; before: string; after?: string; createdAt: number; note?: string };
export class CheckpointStore {
  checkpoints: Checkpoint[] = [];
  snapshot(file: string, note?: string) {
    const before = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
    const cp: Checkpoint = { id: crypto.randomUUID(), file, before, createdAt: Date.now(), note };
    this.checkpoints.push(cp);
    return cp;
  }
  recordAfter(id: string) { const cp = this.checkpoints.find(x => x.id === id); if (cp) cp.after = fs.existsSync(cp.file) ? fs.readFileSync(cp.file, 'utf8') : ''; return cp; }
  last() { return this.checkpoints.at(-1); }
  diffLastPatch() { const cp = this.last(); if (!cp) return ''; const after = cp.after ?? (fs.existsSync(cp.file) ? fs.readFileSync(cp.file, 'utf8') : ''); return createPatch(cp.file, cp.before, after, 'before', 'after'); }
  restoreCheckpoint(id: string) { const cp = this.checkpoints.find(x => x.id === id); if (!cp) throw new Error(`Checkpoint not found: ${id}`); fs.mkdirSync(path.dirname(cp.file), { recursive: true }); fs.writeFileSync(cp.file, cp.before); return cp; }
  undoLastPatch() { const cp = this.last(); if (!cp) throw new Error('No checkpoint to undo'); return this.restoreCheckpoint(cp.id); }
}
export const checkpointStore = new CheckpointStore();
