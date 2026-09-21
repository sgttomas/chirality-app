import type { AgentDefinition } from '@anthropic-ai/claude-agent-sdk';
import type { ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';
import { getCurrentTrancheDisallowedToolNames } from '@chirality/runtime-contracts/tool-descriptor';

export const SUBAGENT_BRIDGE_POLICY_VERSION = 'subagent-bridge.v4.disabled-after-managed-delegation';
export const SUBAGENT_BRIDGE_RULING_REF = 'D-APP-10 Option C';

export const SUBAGENT_EXECUTION_DENIED_REASON =
  'The legacy SDK Agent bridge is disabled; use delegate_agent so hierarchy, scopes, parentage, and returns are durably recorded.';

export const SUBAGENT_EXECUTION_ALLOWED_REASON =
  'Subagent execution is allowed by the D-APP-10 Option C executable bridge.';

export type ExecutableSubagentBridge = {
  policyVersion: typeof SUBAGENT_BRIDGE_POLICY_VERSION;
  rulingRef: typeof SUBAGENT_BRIDGE_RULING_REF;
  sessionId: string;
  delegatedSubagents: string[];
  agents: Record<string, AgentDefinition>;
};

export type SubagentPreflightDecision = {
  allowed: boolean;
  reason: string;
  safeMetadata: {
    policyVersion: typeof SUBAGENT_BRIDGE_POLICY_VERSION;
    rulingRef: typeof SUBAGENT_BRIDGE_RULING_REF;
    denyClass?: 'subagent-execution';
    allowClass?: 'subagent-execution';
    executionPosture: 'hard-denied' | 'executable';
    executableBridge: boolean;
    requestedAgent?: string;
    eligibleAgentNames: string[];
    eligibleChildDefinition: boolean;
    childToolNames: [];
    childCapabilityInheritance: false;
  };
};

function uniqueNames(names: readonly string[] | undefined): string[] {
  return Array.from(
    new Set(
      (names ?? [])
        .map((name) => name.trim())
        .filter((name) => name.length > 0)
    )
  );
}

function readStringField(input: Record<string, unknown>, fields: readonly string[]): string | undefined {
  for (const field of fields) {
    const value = input[field];
    if (typeof value === 'string' && value.trim().length > 0) {
      return value.trim();
    }
  }
  return undefined;
}

export function extractRequestedSubagentName(toolInput: Record<string, unknown>): string | undefined {
  return readStringField(toolInput, ['agent', 'agentName', 'subagent_type', 'subagentType']);
}

export function createExecutableAgentDefinition(
  agentName: string,
  instruction?: NonNullable<ResolvedOpts['delegatedAgentInstructions']>[string]
): AgentDefinition {
  const disallowedTools = getCurrentTrancheDisallowedToolNames([]);
  return {
    description: `Governed named child ${agentName}; compatibility child turn with no inherited tools.`,
    prompt: [
      'You are a governed Chirality child running through the deprecated D-APP-10 Option C SDK Agent compatibility adapter. Execute only the delegated child turn. Do not delegate, inherit parent capabilities, or claim acceptance.',
      instruction
        ? `Named instruction source: ${instruction.path}\ncontentSha256: ${instruction.sha256}\n\n${instruction.content}`
        : 'The named instruction package was unavailable. Fail closed and return that defect.'
    ].join('\n\n'),
    tools: [],
    disallowedTools,
    maxTurns: 1,
    permissionMode: 'dontAsk'
  };
}

export function createExecutableSubagentBridge(input: {
  session: SessionRecord;
  opts: ResolvedOpts;
}): ExecutableSubagentBridge | undefined {
  void input;
  return undefined;
}

export function evaluateSubagentPreflight(input: {
  toolInput: Record<string, unknown>;
  eligibleAgentNames?: readonly string[];
}): SubagentPreflightDecision {
  const eligibleAgentNames = uniqueNames(input.eligibleAgentNames);
  const requestedAgent = extractRequestedSubagentName(input.toolInput);
  const eligibleChildDefinition = false;

  return {
    allowed: eligibleChildDefinition,
    reason: SUBAGENT_EXECUTION_DENIED_REASON,
    safeMetadata: {
      policyVersion: SUBAGENT_BRIDGE_POLICY_VERSION,
      rulingRef: SUBAGENT_BRIDGE_RULING_REF,
      denyClass: eligibleChildDefinition ? undefined : 'subagent-execution',
      allowClass: undefined,
      executionPosture: 'hard-denied',
      executableBridge: false,
      requestedAgent,
      eligibleAgentNames,
      eligibleChildDefinition,
      childToolNames: [],
      childCapabilityInheritance: false
    }
  };
}
