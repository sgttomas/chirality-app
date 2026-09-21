import { HarnessError } from '@chirality/runtime-contracts/errors';
import { CHIRALITY_ROLES } from '@chirality/runtime-contracts/v3';
import type { AgentClass } from './agent-instruction';

/** Legacy route shape retained while renderer callers move to RolesResponse. */
export type AgentRosterEntry = {
  name: string;
  type: number | undefined;
  class: AgentClass | undefined;
};

export const UNTYPED_PERSONA = 'UNTYPED';
export const GENERALIST_AGENT2_PERSONA = 'GENERALIST_AGENT2';

/** Production discovery is Runtime-owned; this is the legacy projection only. */
export async function listAgentRoster(_instructionRootOverride?: string): Promise<AgentRosterEntry[]> {
  return CHIRALITY_ROLES.map((role) => ({ name: role.id, type: role.agentType, class: undefined }));
}

export function isDirectChatPersona(entry: AgentRosterEntry): boolean {
  return CHIRALITY_ROLES.some((role) => role.id === entry.name && role.directEntry);
}

export function selectDirectChatPersonas(roster: readonly AgentRosterEntry[]): AgentRosterEntry[] {
  return roster.filter(isDirectChatPersona);
}

export async function assertDirectChatPersona(persona: string, _instructionRootOverride?: string): Promise<void> {
  const normalized = persona.trim().toUpperCase();
  if (normalized === UNTYPED_PERSONA) return;
  const role = CHIRALITY_ROLES.find((candidate) => candidate.id === normalized);
  if (!role?.directEntry) {
    throw new HarnessError('INVALID_REQUEST', 400, `Role '${persona}' is not available for direct chat.`, {
      persona,
      roleId: role?.id,
      agentType: role?.agentType
    });
  }
}
