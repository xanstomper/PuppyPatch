import { describe, it, expect } from 'vitest';
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
import { writeFile } from '@horus/tools';
import { checkpointStore } from '@horus/core';

describe('checkpoint undo', () => {
  it('undo restores last write', () => { const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(),'horus-cp-')), 'a.txt'); fs.writeFileSync(file, 'before'); writeFile({ path: file, content: 'after' }); expect(fs.readFileSync(file,'utf8')).toBe('after'); checkpointStore.undoLastPatch(); expect(fs.readFileSync(file,'utf8')).toBe('before'); });
});
