import { EventEmitter } from 'node:events';
import type { HorusEvent } from './types.js';

export class HorusEventBus extends EventEmitter {
  emitEvent(event: HorusEvent) { return this.emit('event', event); }
  onEvent(handler: (event: HorusEvent) => void) { this.on('event', handler); return () => this.off('event', handler); }
}
export const eventBus = new HorusEventBus();
