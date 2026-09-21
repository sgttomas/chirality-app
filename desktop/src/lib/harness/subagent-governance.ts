import {
  asNonEmptyString,
  parseAgentClass,
  parseAgentType,
  parseCommaSeparatedList,
  parseFrontmatter,
  readAgentInstruction,
  tryReadAgentInstruction
} from './agent-instruction';
import { createHash } from 'node:crypto';
import { GENERALIST_AGENT2_PERSONA, UNTYPED_PERSONA } from './agent-roster';

export type GovernanceGateId =
  | 'ENVIRONMENT'
  | 'PERSONA_ALLOWLIST'
  | 'METADATA_PRESENCE'
  | 'CONTEXT_SEALED'
  | 'PIPELINE_RUN_APPROVED'
  | 'APPROVAL_REF'
  | 'INTERNAL_ERROR'
  | 'ALLOW';

export type SubagentGovernanceDecision = {
  allowed: boolean;
  gate: GovernanceGateId;
  reason: string;
  evaluationMs: number;
  allowlistedSubagents: string[];
  delegatedSubagents: string[];
  delegatedAgentInstructions?: Record<string, {
    path: string;
    content: string;
    sha256: string;
    agentType: 1 | 2;
  }>;
  approvalRef?: string;
  approvedBy?: string;
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function normalizeSubagentList(rawSubagents: unknown): string[] {
  const parsed = parseCommaSeparatedList(rawSubagents);
  const unique = new Set<string>();

  for (const candidate of parsed) {
    const normalized = candidate.trim();
    if (normalized.length > 0) {
      unique.add(normalized);
    }
  }

  return [...unique];
}

function deny(
  gate: Exclude<GovernanceGateId, 'ALLOW'>,
  reason: string,
  allowlistedSubagents: string[],
  evaluationMs: number
): SubagentGovernanceDecision {
  return {
    allowed: false,
    gate,
    reason,
    evaluationMs,
    allowlistedSubagents,
    delegatedSubagents: [],
    delegatedAgentInstructions: {}
  };
}

function logDecision(persona: string, decision: SubagentGovernanceDecision): void {
  const evaluationPart = ` evaluationMs=${decision.evaluationMs.toFixed(3)}`;
  if (decision.allowed) {
    const subagentSummary =
      decision.delegatedSubagents.length > 0 ? decision.delegatedSubagents.join(',') : 'none';
    const approvedByPart = decision.approvedBy ? ` approvedBy=${decision.approvedBy}` : '';
    console.info(
      `[harness/subagent-governance] ALLOW persona=${persona} gate=${decision.gate}${evaluationPart} delegated=${subagentSummary} approvalRef=${decision.approvalRef ?? ''}${approvedByPart}`
    );
    return;
  }

  console.info(
    `[harness/subagent-governance] DENY persona=${persona} gate=${decision.gate}${evaluationPart} reason=${decision.reason}`
  );
}

function parseSlowWarningThresholdMs(env: NodeJS.ProcessEnv): number | undefined {
  const raw = asNonEmptyString(env.CHIRALITY_SUBAGENT_GOVERNANCE_WARN_MS);
  if (!raw) {
    return undefined;
  }

  const parsed = Number(raw);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return undefined;
  }

  return parsed;
}

function maybeWarnOnSlowEvaluation(
  persona: string,
  decision: SubagentGovernanceDecision,
  env: NodeJS.ProcessEnv
): void {
  const thresholdMs = parseSlowWarningThresholdMs(env);
  if (!thresholdMs || decision.evaluationMs <= thresholdMs) {
    return;
  }

  console.warn(
    `[harness/subagent-governance] SLOW_EVALUATION persona=${persona} gate=${decision.gate} evaluationMs=${decision.evaluationMs.toFixed(3)} thresholdMs=${thresholdMs.toFixed(3)}`
  );
}

function elapsedMs(startNs: bigint): number {
  return Number(process.hrtime.bigint() - startNs) / 1_000_000;
}

function finalizeDecision(
  persona: string,
  decision: SubagentGovernanceDecision,
  env: NodeJS.ProcessEnv
): SubagentGovernanceDecision {
  logDecision(persona, decision);
  maybeWarnOnSlowEvaluation(persona, decision, env);
  return decision;
}

function formatAgentType(agentType: number | undefined): string {
  if (typeof agentType === 'number') {
    return `TYPE ${agentType}`;
  }
  return 'missing';
}

async function resolveDelegatedSubagents(
  subagents: string[],
  instructionRoot: string,
  parentType: 0 | 1
): Promise<{ names: string[]; instructions: NonNullable<SubagentGovernanceDecision['delegatedAgentInstructions']> }> {
  const delegated: string[] = [];
  const instructions: NonNullable<SubagentGovernanceDecision['delegatedAgentInstructions']> = {};

  for (const subagentName of subagents) {
    const instruction = await tryReadAgentInstruction(subagentName, instructionRoot);
    if (!instruction) {
      console.error(
        `[harness/subagent-governance] Candidate subagent rejected: ${subagentName} instruction file not found.`
      );
      continue;
    }

    const agentType = parseAgentType(instruction.content);
    const agentClass = parseAgentClass(instruction.content);
    const allowedType =
      parentType === 0
        ? agentType === 1 ||
          (subagentName === 'TASK' && agentType === 2 && agentClass === 'TASK')
        : agentType === 2;
    if (!allowedType) {
      const expected = parentType === 0 ? 'TYPE 1 or TASK Agent 2' : 'TYPE 2';
      console.error(
        `[harness/subagent-governance] Candidate subagent rejected: ${subagentName} declares AGENT_TYPE=${formatAgentType(
          agentType
        )}; expected ${expected}.`
      );
      continue;
    }

    if (parentType === 1 && agentClass !== 'TASK') {
      const renderedClass = agentClass ?? 'missing';
      console.warn(
        `[harness/subagent-governance] Candidate subagent warning: ${subagentName} declares AGENT_CLASS=${renderedClass}; TASK is preferred.`
      );
    }

    const delegatedAgentType: 1 | 2 = agentType === 1 ? 1 : 2;
    delegated.push(subagentName);
    instructions[subagentName] = {
      path: instruction.path,
      content: instruction.content,
      sha256: createHash('sha256').update(instruction.content).digest('hex'),
      agentType: delegatedAgentType
    };
  }

  return { names: delegated, instructions };
}

export async function evaluateSubagentGovernance(
  persona: string,
  subagentGovernance: unknown,
  env: NodeJS.ProcessEnv = process.env
): Promise<SubagentGovernanceDecision> {
  const startNs = process.hrtime.bigint();
  let allowlistedSubagents: string[] = [];

  try {
    if ([UNTYPED_PERSONA, GENERALIST_AGENT2_PERSONA].includes(persona.trim().toUpperCase())) {
      const denied = deny(
        'PERSONA_ALLOWLIST',
        'Untyped sessions and ephemeral Agent 2 instances may not delegate.',
        [],
        elapsedMs(startNs)
      );
      return finalizeDecision(persona, denied, env);
    }
    const personaInstruction = await readAgentInstruction(persona);
    const frontmatter = parseFrontmatter(personaInstruction.content, {
      warnPrefix: '[harness/subagent-governance]'
    });
    allowlistedSubagents = normalizeSubagentList(frontmatter.subagents);
    const parentType = parseAgentType(personaInstruction.content);
    if (parentType !== 0 && parentType !== 1) {
      const denied = deny(
        'PERSONA_ALLOWLIST',
        'Only Agent 0 and Agent 1 may delegate.',
        allowlistedSubagents,
        elapsedMs(startNs)
      );
      return finalizeDecision(persona, denied, env);
    }

    if (env.CHIRALITY_ENABLE_SUBAGENTS !== 'true') {
      const denied = deny(
        'ENVIRONMENT',
        'CHIRALITY_ENABLE_SUBAGENTS is not set to "true".',
        allowlistedSubagents,
        elapsedMs(startNs)
      );
      return finalizeDecision(persona, denied, env);
    }

    if (allowlistedSubagents.length === 0) {
      const denied = deny(
        'PERSONA_ALLOWLIST',
        'Active persona is not allowlisted for subagents.',
        allowlistedSubagents,
        elapsedMs(startNs)
      );
      return finalizeDecision(persona, denied, env);
    }

    if (!isRecord(subagentGovernance)) {
      const denied = deny(
        'METADATA_PRESENCE',
        'opts.subagentGovernance is missing or invalid.',
        allowlistedSubagents,
        elapsedMs(startNs)
      );
      return finalizeDecision(persona, denied, env);
    }

    if (subagentGovernance.contextSealed !== true) {
      const denied = deny(
        'CONTEXT_SEALED',
        'contextSealed must be strictly true.',
        allowlistedSubagents,
        elapsedMs(startNs)
      );
      return finalizeDecision(persona, denied, env);
    }

    if (subagentGovernance.pipelineRunApproved !== true) {
      const denied = deny(
        'PIPELINE_RUN_APPROVED',
        'pipelineRunApproved must be strictly true.',
        allowlistedSubagents,
        elapsedMs(startNs)
      );
      return finalizeDecision(persona, denied, env);
    }

    const approvalRef = asNonEmptyString(subagentGovernance.approvalRef);
    if (!approvalRef) {
      const denied = deny(
        'APPROVAL_REF',
        'approvalRef must be a non-empty string.',
        allowlistedSubagents,
        elapsedMs(startNs)
      );
      return finalizeDecision(persona, denied, env);
    }

    const approvedBy = asNonEmptyString(subagentGovernance.approvedBy);
    const delegated = await resolveDelegatedSubagents(
      allowlistedSubagents,
      personaInstruction.instructionRoot,
      parentType
    );
    const allowed: SubagentGovernanceDecision = {
      allowed: true,
      gate: 'ALLOW',
      reason: 'All delegation governance gates passed.',
      evaluationMs: elapsedMs(startNs),
      allowlistedSubagents,
      delegatedSubagents: delegated.names,
      delegatedAgentInstructions: delegated.instructions,
      approvalRef,
      approvedBy
    };

    return finalizeDecision(persona, allowed, env);
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown gate evaluation failure.';
    const denied = deny('INTERNAL_ERROR', message, allowlistedSubagents, elapsedMs(startNs));
    console.error(
      `[harness/subagent-governance] INTERNAL_ERROR persona=${persona} gate=INTERNAL_ERROR reason=${message}`
    );
    return finalizeDecision(persona, denied, env);
  }
}
