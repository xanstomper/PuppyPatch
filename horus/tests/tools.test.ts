import { describe, it, expect } from 'vitest';
import { createMvpToolRegistry } from '@horus/tools';

describe('tool registry', () => {
  it('registers core tools', () => { const names = createMvpToolRegistry().list().map(t => t.name); expect(names).toContain('read_file'); expect(names).toContain('undo_last_patch'); });
});
