import { describe, it, expect } from 'vitest';
import { classifyCommandRisk, redactSecrets } from '@horus/core';

describe('risk classifier', () => {
  it('blocks destructive commands', () => { expect(classifyCommandRisk('git push origin main')).toBe('destructive'); });
  it('redacts secrets', () => { expect(redactSecrets('sk-abcdefghijklmnopqrstuvwxyz')).toContain('[REDACTED]'); });
});
