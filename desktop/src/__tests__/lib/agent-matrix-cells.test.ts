import { describe, expect, it } from 'vitest';
import { CHIRALITY_ROLES } from '@chirality/runtime-contracts/v3';
import { DIRECT_ENTRY_ROLE_IDS, isRoleSelectionBlocked } from '../../lib/portal/agent-matrix-cells';

describe('retired matrix compatibility', () => {
  it('derives exactly the three direct-entry choices from the shared role registry', () => {
    expect(DIRECT_ENTRY_ROLE_IDS).toEqual(['HELP_HUMAN', 'HELPS_HUMANS', 'WORKING_ITEMS']);
    expect(CHIRALITY_ROLES.find(role => role.defaultForNewChat)?.id).toBe('HELP_HUMAN');
    expect(CHIRALITY_ROLES.find(role => role.id === 'TASK')?.directEntry).toBe(false);
  });

  it('blocks role selection at an active execution boundary', () => {
    expect(isRoleSelectionBlocked(false)).toBe(false);
    expect(isRoleSelectionBlocked(true)).toBe(true);
  });
});
