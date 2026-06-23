import { describe, it, expect } from 'vitest';
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
import { writeFile, readFile } from '@horus/tools';

describe('filesystem tools', () => {
  it('writes and reads file', () => { const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(),'horus-fs-')), 'a.txt'); const w = writeFile({ path: file, content: 'hello' }); expect(w.ok).toBe(true); expect(readFile({ path: file }).data).toBe('hello'); });
});
