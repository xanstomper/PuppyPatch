import { describe, it, expect } from 'vitest';
import { HorusEventBus } from '@horus/core';

describe('event bus', () => {
  it('emits typed events', () => { const bus = new HorusEventBus(); let seen = false; bus.onEvent(e => { seen = e.type === 'task'; }); bus.emitEvent({ type: 'task', action: 'new', content: 'x' }); expect(seen).toBe(true); });
});
