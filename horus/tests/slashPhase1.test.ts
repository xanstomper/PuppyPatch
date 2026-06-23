import { describe, it, expect } from 'vitest';
import { parseSlashCommand, runSlashCommand } from '../apps/cli/src/tui/slash.js';

describe('phase 1 slash commands', () => {
  it('parses slash commands', () => { expect(parseSlashCommand('/doctor')?.command).toBe('/doctor'); });
  it('/mcp is placeholder only', () => { expect(runSlashCommand('/mcp').text).toContain('placeholder-only'); });
  it('/model reports mode', () => { expect(runSlashCommand('/model').text).toContain('mode=mock'); });
  it('/status reports phase1', () => { expect(runSlashCommand('/status').text).toContain('phase1-core-mvp'); });
});
