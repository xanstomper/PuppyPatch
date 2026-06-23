import { describe, it, expect, vi } from 'vitest';
import { providerFromRef, parseModelRef } from '@horus/models';

describe('mock model boundary', () => {
  it('uses mock mode by default', async () => { vi.stubEnv('HORUS_MOCK_MODEL', undefined); const p = providerFromRef(parseModelRef('openai:gpt-4o-mini')); expect(p.status().mode).toBe('mock'); expect(await p.call('hello')).toContain('Mock model response'); });
  it('falls back to mock when real mode lacks credentials', async () => { vi.stubEnv('HORUS_MOCK_MODEL', '0'); vi.stubEnv('OPENAI_API_KEY', ''); const p = providerFromRef(parseModelRef('openai:gpt-4o-mini')); expect(p.status().mode).toBe('mock'); expect(p.status().warning).toContain('Missing'); });
});
