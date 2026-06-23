import { describe, it, expect } from 'vitest';
import { loadConfig } from '@horus/core';

describe('config loading', () => {
  it('loads defaults', () => { expect(loadConfig('__missing__.json').model).toContain(':'); });
});
