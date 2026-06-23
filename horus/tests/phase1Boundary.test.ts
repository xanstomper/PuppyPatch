import { describe, it, expect } from 'vitest';
import fs from 'node:fs';

describe('phase 1 docs boundary', () => {
  it('README declares deferred features', () => { const readme = fs.readFileSync('README.md','utf8'); expect(readme).toContain('No swarm mode'); expect(readme).toContain('MCP is placeholder-only'); });
});
