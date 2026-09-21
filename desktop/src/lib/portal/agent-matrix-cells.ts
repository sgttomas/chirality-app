import { CHIRALITY_ROLES, type ChiralityRoleName } from '@chirality/runtime-contracts/v3';

/** Compatibility module for the retired matrix route. */
export const DIRECT_ENTRY_ROLE_IDS: readonly ChiralityRoleName[] = CHIRALITY_ROLES
  .filter(role => role.directEntry)
  .map(role => role.id);

export function isRoleSelectionBlocked(streaming: boolean): boolean {
  return streaming;
}
