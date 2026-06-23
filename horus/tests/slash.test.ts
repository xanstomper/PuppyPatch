import { describe, it, expect } from 'vitest';
import { SlashCommands } from '@horus/shared';

describe('slash commands', () => {
  it('has diff and undo', () => { expect(SlashCommands).toContain('/diff'); expect(SlashCommands).toContain('/undo'); });
});
