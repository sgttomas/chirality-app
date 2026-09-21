import { describe, expect, it } from 'vitest';
import {
  assertDirectChatPersona,
  listAgentRoster,
  selectDirectChatPersonas
} from '../../lib/harness/agent-roster';

describe('legacy role projection', () => {
  it('projects only the four v3 roles without inspecting an instruction directory', async () => {
    const roster = await listAgentRoster('/path/that/does/not/exist');
    expect(roster.map((entry) => [entry.name, entry.type])).toEqual([
      ['HELP_HUMAN', 0],
      ['HELPS_HUMANS', 1],
      ['WORKING_ITEMS', 1],
      ['TASK', 2]
    ]);
  });

  it('offers the three direct roles and rejects TASK direct entry', async () => {
    const direct = selectDirectChatPersonas(await listAgentRoster());
    expect(direct.map((entry) => entry.name)).toEqual([
      'HELP_HUMAN',
      'HELPS_HUMANS',
      'WORKING_ITEMS'
    ]);
    await expect(assertDirectChatPersona('TASK')).rejects.toMatchObject({ type: 'INVALID_REQUEST' });
  });
});
