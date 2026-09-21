import type { ChiralityRoleName } from '@chirality/runtime-contracts/v3';

export const DEFAULT_PERSONA: ChiralityRoleName = 'HELP_HUMAN';

/** Legacy route aliases that still resolve to a live direct-entry role. */
export const PERSONA_ALIASES: Readonly<Record<string, ChiralityRoleName>> = {
  HELP: 'HELP_HUMAN',
  AGENTS: 'HELPS_HUMANS'
};

const DIRECT_ENTRY_ROLES = new Set<ChiralityRoleName>([
  'HELP_HUMAN',
  'HELPS_HUMANS',
  'WORKING_ITEMS'
]);

/**
 * Route compatibility is deliberately bounded to the four-role registry.
 * Historical session personas remain replay metadata; they are not accepted
 * as new execution roles.
 */
export function resolvePersona(rawAgent: string | null | undefined): ChiralityRoleName {
  const normalized = rawAgent?.trim().toUpperCase();
  if (!normalized) return DEFAULT_PERSONA;
  const alias = PERSONA_ALIASES[normalized];
  if (alias) return alias;
  return DIRECT_ENTRY_ROLES.has(normalized as ChiralityRoleName)
    ? normalized as ChiralityRoleName
    : DEFAULT_PERSONA;
}
