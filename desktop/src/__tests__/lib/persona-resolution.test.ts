import { describe, expect, it } from 'vitest';
import { DEFAULT_PERSONA, PERSONA_ALIASES, resolvePersona } from '../../lib/shell/persona-resolution';

describe('resolvePersona', () => {
  it('defaults new chats to HELP_HUMAN', () => {
    expect([null, undefined, '', '   '].map(resolvePersona)).toEqual(Array(4).fill('HELP_HUMAN'));
    expect(DEFAULT_PERSONA).toBe('HELP_HUMAN');
  });

  it('accepts exactly the three direct-entry roles', () => {
    expect(resolvePersona('help_human')).toBe('HELP_HUMAN');
    expect(resolvePersona(' helps_humans ')).toBe('HELPS_HUMANS');
    expect(resolvePersona('working_items')).toBe('WORKING_ITEMS');
    expect(resolvePersona('TASK')).toBe('HELP_HUMAN');
  });

  it('keeps bounded legacy display aliases without reviving retired roles', () => {
    expect(PERSONA_ALIASES).toEqual({ HELP: 'HELP_HUMAN', AGENTS: 'HELPS_HUMANS' });
    expect(resolvePersona('ORCHESTRATE')).toBe('HELP_HUMAN');
    expect(resolvePersona('RESEARCH')).toBe('HELP_HUMAN');
    expect(resolvePersona('CHANGE')).toBe('HELP_HUMAN');
  });
});
