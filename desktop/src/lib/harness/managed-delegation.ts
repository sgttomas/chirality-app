import { createHash, randomUUID } from 'node:crypto';
import { mkdir, readFile, readdir, rename, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import type { EngineSelection, SessionRecord } from '@chirality/runtime-contracts/types';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { getHarnessToolDescriptor } from '@chirality/runtime-contracts/tool-descriptor';
import {
  parseAgentClass,
  parseAgentType,
  parseCommaSeparatedList,
  parseFrontmatter,
  readAgentInstruction
} from './agent-instruction';
import { appendHarnessEvent } from './session-events';
import { createHarnessEvent } from './event-factory';
import { getPermissionEventChannel } from './permission-event-channel';
import { GENERALIST_AGENT2_PERSONA } from './agent-roster';

export const MANAGED_DELEGATION_POLICY_VERSION = 'managed-delegation.v3.atomic-coordination';
export const ORCHESTRATION_RECORD_SCHEMA_VERSION = 'chirality-agent-runs/v2';

export type AgentType = 0 | 1 | 2;
export type ChildKind = 'named' | 'task' | 'generalist';
export type OrchestrationPosture =
  | 'TERMINAL_FAN_OUT_IN'
  | 'SUPERVISED_MANY_TO_MANY'
  | 'MIXED';
export type SelectionAuthority = 'HUMAN' | 'AGENT_0' | 'AGENT_1';
export type ClaimStatus = 'PROVISIONAL' | 'VALIDATED' | 'ACCEPTED' | 'DISPUTED';
export type CoordinationDisposition =
  | 'RECORD'
  | 'RELAY'
  | 'AMEND'
  | 'HOLD'
  | 'REPLAN'
  | 'ESCALATE'
  | 'ROUTE';
export type UpdateAcknowledgment =
  | 'INCORPORATED'
  | 'NO_EFFECT'
  | 'BLOCKED'
  | 'CONFLICT'
  | 'HUMAN_DECISION_REQUIRED';
export type AmendmentCategory =
  | 'INFORMATION'
  | 'CONTEXT'
  | 'SEQUENCING'
  | 'SCOPE'
  | 'RISK'
  | 'AUTHORITY'
  | 'SHARED_WRITE'
  | 'ACCEPTANCE';

export type DelegateAgentInput = {
  executionRoot: string;
  runId: string;
  planVersion: string;
  selectionAuthority: SelectionAuthority;
  posture: OrchestrationPosture;
  acceptedBasis: string[];
  workGraph?: Record<string, unknown>;
  childKind: ChildKind;
  agentName?: string;
  purpose: string;
  brief: string;
  declaredContext: string[];
  tools: string[];
  engineSelection?: EngineSelection;
  writeTargets: string[];
  dependencies: string[];
  acceptedPredecessors?: string[];
  expectedOutput: string;
  acceptanceCriteria: string[];
  requiredReturnMarkers: string[];
  executionMode?: 'WAIT' | 'BACKGROUND';
  contextSealed: boolean;
  pipelineRunApproved: boolean;
  approvalRef: string;
};

export type ManagedChildLaunch = {
  parent: SessionRecord;
  childPersona: string;
  childKind: ChildKind;
  childAgentType: AgentType;
  childInstanceId: string;
  runId: string;
  brief: string;
  declaredContext: string[];
  tools: string[];
  engineSelection?: EngineSelection;
  writeTargets: string[];
  instructionContent?: string;
  instructionPath?: string;
  instructionHash?: string;
  briefHash: string;
  requiredReturnMarkers: string[];
  approvalRef: string;
  executionMode: 'WAIT' | 'BACKGROUND';
};

export type ManagedChildReturn = {
  sessionId: string;
  status: 'RUNNING' | 'COMPLETED' | 'FAILED' | 'BLOCKED';
  output: string;
  outputArtifact?: string;
};

export type ManagedChildLauncher = (input: ManagedChildLaunch) => Promise<ManagedChildReturn>;
export type ManagedParentBinder = (parent: SessionRecord) => Promise<SessionRecord>;

type ResolvedChild = {
  persona: string;
  agentType: AgentType;
  instructionContent?: string;
  instructionPath?: string;
  instructionHash?: string;
};

function sha256(value: string): string {
  return createHash('sha256').update(value).digest('hex');
}

function safeSegment(value: string, field: string): string {
  if (!/^[A-Za-z0-9._-]+$/.test(value) || value === '.' || value === '..') {
    throw new HarnessError('INVALID_REQUEST', 400, `${field} contains unsafe characters`);
  }
  return value;
}

function requireNonEmpty(value: string, field: string): string {
  const normalized = value.trim();
  if (!normalized) {
    throw new HarnessError('INVALID_REQUEST', 400, `${field} must be non-empty`);
  }
  return normalized;
}

function assertWorkGraph(workGraph: Record<string, unknown>, field = 'workGraph'): void {
  const requiredArrays = [
    'nodes',
    'edges',
    'concurrencyEligibility',
    'expectedReturns',
    'fanInGates',
    'humanDecisionPoints'
  ];
  const missing = requiredArrays.filter((key) => !Array.isArray(workGraph[key]));
  if (missing.length > 0) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      `${field} must declare array field(s): ${missing.join(', ')}`
    );
  }
}

export function assertValidManagedChildReturn(output: string, requiredMarkers: readonly string[]): void {
  if (!output.trim()) {
    throw new HarnessError('INVALID_REQUEST', 409, 'Completed child return is empty');
  }
  const missing = requiredMarkers.filter((marker) => !output.includes(marker));
  if (missing.length > 0) {
    throw new HarnessError(
      'INVALID_REQUEST',
      409,
      `Completed child return is schema-invalid; missing marker(s): ${missing.join(', ')}`
    );
  }
}

function contained(root: string, candidate: string, field: string): string {
  const resolved = path.resolve(root, candidate);
  const normalizedRoot = path.resolve(root);
  if (resolved !== normalizedRoot && !resolved.startsWith(`${normalizedRoot}${path.sep}`)) {
    throw new HarnessError('INVALID_REQUEST', 400, `${field} escapes the project root`);
  }
  return resolved;
}

function pathsOverlap(left: string, right: string): boolean {
  const a = path.resolve(left);
  const b = path.resolve(right);
  return a === b || a.startsWith(`${b}${path.sep}`) || b.startsWith(`${a}${path.sep}`);
}

function canonicalToolNames(tools: readonly string[]): Set<string> {
  return new Set(tools.map((tool) => getHarnessToolDescriptor(tool)?.name ?? tool));
}

function assertChildToolPolicy(
  parentTools: readonly string[],
  childTools: readonly string[],
  instructionContent?: string
): void {
  const declared = instructionContent
    ? parseCommaSeparatedList(parseFrontmatter(instructionContent).tools)
    : [...parentTools];
  const allowed = canonicalToolNames(declared);
  const excess = [...canonicalToolNames(childTools)].filter((tool) => !allowed.has(tool));
  if (excess.length > 0) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      `Child tools exceed the declared child policy: ${excess.join(', ')}`
    );
  }
}

function assertBoundedEngineSelection(input: {
  selection?: EngineSelection;
  selectionAuthority: SelectionAuthority;
  child: ResolvedChild;
  tools: readonly string[];
  writeTargets: readonly string[];
}): void {
  if (!input.selection) return;

  const selection = input.selection;
  if (
    selection.adapterId !== 'pi' ||
    selection.providerId !== 'omlx' ||
    !selection.model.trim()
  ) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'This milestone permits only adapterId pi with providerId omlx and an exact non-empty model ID'
    );
  }
  if (!['HUMAN', 'AGENT_0', 'AGENT_1'].includes(input.selectionAuthority)) {
    throw new HarnessError('INVALID_REQUEST', 403, 'Engine selection authority is not permitted');
  }
  if (input.child.agentType !== 2) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Pi/oMLX is permitted only for a managed Agent 2 child');
  }
  if (input.writeTargets.length > 0) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Pi/oMLX children may not declare write targets');
  }
  if (input.tools.length !== 1) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Pi/oMLX children require exactly one declared read-only tool');
  }
  const descriptor = getHarnessToolDescriptor(input.tools[0]);
  if (
    !descriptor ||
    input.tools[0] !== 'read_file' ||
    descriptor.name !== 'read_file' ||
    descriptor.permissions.length !== 1 ||
    descriptor.permissions[0] !== 'read'
  ) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'Pi/oMLX children require the exact Chirality read_file tool in this milestone'
    );
  }
}

async function resolveChild(
  parentPersona: string,
  input: DelegateAgentInput
): Promise<{ parentType: AgentType; child: ResolvedChild }> {
  const parentInstruction = await readAgentInstruction(parentPersona);
  const parentType = parseAgentType(parentInstruction.content);
  if (parentType !== 0 && parentType !== 1 && parentType !== 2) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Parent agent type is missing or invalid');
  }
  if (parentType === 2) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Agent 2 may not delegate');
  }
  const frontmatter = parseFrontmatter(parentInstruction.content);
  const allowlist = parseCommaSeparatedList(frontmatter.subagents);

  if (input.childKind === 'generalist') {
    if (frontmatter.allow_generalist_agent2 !== true) {
      throw new HarnessError('INVALID_REQUEST', 400, 'Ephemeral generalist Agent 2 is not allowed');
    }
    return { parentType, child: { persona: GENERALIST_AGENT2_PERSONA, agentType: 2 } };
  }

  const agentName = input.childKind === 'task' ? input.agentName?.trim() || 'TASK' : requireNonEmpty(input.agentName ?? '', 'agentName');
  if (!allowlist.includes(agentName)) {
    throw new HarnessError('INVALID_REQUEST', 400, `${agentName} is not allowlisted by ${parentPersona}`);
  }
  const instruction = await readAgentInstruction(agentName, parentInstruction.instructionRoot);
  const childType = parseAgentType(instruction.content);
  const childClass = parseAgentClass(instruction.content);
  if (childType !== 0 && childType !== 1 && childType !== 2) {
    throw new HarnessError('INVALID_REQUEST', 400, `${agentName} has no valid agent type`);
  }
  if (
    parentType === 0 &&
    !(
      (input.childKind === 'named' && childType === 1) ||
      (input.childKind === 'task' && agentName === 'TASK' && childType === 2 && childClass === 'TASK')
    )
  ) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'Agent 0 may delegate only to named Agent 1 roles or the TASK Agent 2 declaring AGENT_CLASS=TASK'
    );
  }
  if (parentType === 1 && childType !== 2) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Agent 1 may delegate only to Agent 2');
  }
  if (input.childKind === 'task' && childType !== 2) {
    throw new HarnessError('INVALID_REQUEST', 400, 'TASK child must be Agent 2');
  }
  if (childType === 2 && agentName !== 'TASK') {
    const approvalRef = parseFrontmatter(instruction.content).dedicated_agent2_approval;
    if (typeof approvalRef !== 'string' || !/^D-GOV-\d+$/.test(approvalRef)) {
      throw new HarnessError('INVALID_REQUEST', 409, `${agentName} has no dedicated Agent 2 approval reference`);
    }
    const repoRoot = path.dirname(path.dirname(instruction.path));
    const decisionsRoot = path.join(repoRoot, 'docs', 'governance_harness', '_DECISIONS');
    const matches = (await readdir(decisionsRoot)).filter((name) => name.startsWith(`${approvalRef}_`) && name.endsWith('.md'));
    if (matches.length !== 1) {
      throw new HarnessError('INVALID_REQUEST', 409, `${approvalRef} does not resolve to one decision record`);
    }
    const decision = await readFile(path.join(decisionsRoot, matches[0]), 'utf8');
    if (!/^Status:\s+RULED\s*$/m.test(decision)) {
      throw new HarnessError('INVALID_REQUEST', 409, `${agentName} dedicated Agent 2 approval is not RULED`);
    }
    if (!new RegExp(`^\\|\\s*${agentName}\\s*\\|`, 'm').test(decision)) {
      throw new HarnessError('INVALID_REQUEST', 409, `${approvalRef} does not approve role ${agentName}`);
    }
  }
  return {
    parentType,
    child: {
      persona: agentName,
      agentType: childType,
      instructionContent: instruction.content,
      instructionPath: instruction.path,
      instructionHash: sha256(instruction.content)
    }
  };
}

function renderPlan(input: DelegateAgentInput, parent: SessionRecord): string {
  const graph = input.workGraph ?? {};
  return [
    '# Orchestration Plan',
    '',
    `- Schema: ${ORCHESTRATION_RECORD_SCHEMA_VERSION}`,
    `- RunID: ${input.runId}`,
    `- PlanVersion: ${input.planVersion}`,
    `- SelectionAuthority: ${input.selectionAuthority}`,
    `- Posture: ${input.posture}`,
    `- ParentSession: ${parent.sessionId}`,
    `- ParentRole: ${parent.persona}`,
    `- AcceptedBasis: ${input.acceptedBasis.join('; ')}`,
    `- ConcurrencyEligibility: ${JSON.stringify(graph.concurrencyEligibility ?? [])}`,
    `- ExpectedReturns: ${JSON.stringify(graph.expectedReturns ?? [])}`,
    `- FanInGates: ${JSON.stringify(graph.fanInGates ?? [])}`,
    `- HumanDecisionPoints: ${JSON.stringify(graph.humanDecisionPoints ?? [])}`,
    ''
  ].join('\n');
}

function renderBrief(
  input: DelegateAgentInput,
  instanceId: string,
  parent: SessionRecord,
  declaredContext: readonly string[],
  writeTargets: readonly string[]
): string {
  return [
    '# Launch Brief',
    '',
    `RunID: ${input.runId}`,
    `PlanVersion: ${input.planVersion}`,
    `ParentSessionID: ${parent.sessionId}`,
    `ParentRole: ${parent.persona}`,
    `ChildInstanceID: ${instanceId}`,
    `ChildKind: ${input.childKind}`,
    `Purpose: ${input.purpose}`,
    `ScopePath: ${writeTargets[0] ?? declaredContext[0] ?? parent.projectRoot}`,
    `AcceptedBasis: ${input.acceptedBasis.join('; ')}`,
    `DeclaredContext: ${declaredContext.join('; ') || 'none'}`,
    `AllowedTools: ${input.tools.join(', ')}`,
    `EngineSelection: ${input.engineSelection ? JSON.stringify(input.engineSelection) : 'inherited/default'}`,
    `AllowedWriteTargets: ${writeTargets.join('; ') || 'none'}`,
    `Dependencies: ${input.dependencies.join(', ') || 'none'}`,
    `AcceptedPredecessors: ${(input.acceptedPredecessors ?? []).join(', ') || 'none'}`,
    `ExpectedOutput: ${input.expectedOutput}`,
    `AcceptanceCriteria: ${input.acceptanceCriteria.join('; ')}`,
    `RequiredReturnMarkers: ${input.requiredReturnMarkers.join('; ')}`,
    `ApprovalRef: ${input.approvalRef}`,
    '',
    input.childKind === 'generalist'
      ? 'Ephemeral Agent 2 contract: follow the Agent 2 base contract in AGENTS.md. This brief is the complete purpose-specific instruction; no dedicated role is implied.'
      : '',
    '',
    input.brief,
    ''
  ].join('\n');
}

async function writeNew(filePath: string, content: string): Promise<void> {
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, content, { encoding: 'utf8', flag: 'wx' });
}

/**
 * Replace a file's contents atomically: write to a uniquely-named temp file in
 * the SAME directory, then rename(2) over the target. rename is atomic on POSIX,
 * so a concurrent reader of `filePath` always observes either the prior complete
 * contents or the new complete contents — never the empty/partial state that a
 * plain truncate-then-write (`writeFile`) exposes mid-transition. Used for every
 * in-place STATUS.json overwrite so sibling overlap scans cannot read a torn record.
 */
async function writeAtomic(filePath: string, content: string): Promise<void> {
  const dir = path.dirname(filePath);
  await mkdir(dir, { recursive: true });
  const tempPath = path.join(dir, `.${path.basename(filePath)}.${randomUUID()}.tmp`);
  try {
    await writeFile(tempPath, content, { encoding: 'utf8', flag: 'wx' });
    await rename(tempPath, filePath);
  } catch (error) {
    await rm(tempPath, { force: true });
    throw error;
  }
}

async function readJson(filePath: string): Promise<Record<string, unknown>> {
  return JSON.parse(await readFile(filePath, 'utf8')) as Record<string, unknown>;
}

export async function refreshOrchestrationHandoff(runRoot: string): Promise<void> {
  const instancesRoot = path.join(runRoot, 'instances');
  let entries: string[] = [];
  try {
    entries = (await readdir(instancesRoot)).sort();
  } catch {
    return;
  }
  const rows: string[] = [];
  const statuses: string[] = [];
  for (const instanceId of entries) {
    try {
      const status = await readJson(path.join(instancesRoot, instanceId, 'STATUS.json'));
      statuses.push(String(status.status ?? 'UNKNOWN'));
      rows.push(`| ${instanceId} | ${String(status.childRole ?? '')} | ${String(status.status ?? 'UNKNOWN')} | ${String(status.outputArtifact ?? '') || '—'} |`);
    } catch {
      statuses.push('INVALID_STATUS');
      rows.push(`| ${instanceId} | — | INVALID_STATUS | — |`);
    }
  }
  const open = statuses.some((status) => status !== 'COMPLETED');
  const content = [
    '# Agent Run Handoff State',
    '',
    `- Schema: ${ORCHESTRATION_RECORD_SCHEMA_VERSION}`,
    `- ClosureVerdict: ${open ? 'OPEN' : 'TERMINAL_RETURNS_RECORDED'}`,
    `- UpdatedAt: ${new Date().toISOString()}`,
    '',
    '| Instance | Role | Status | Output |',
    '|---|---|---|---|',
    ...rows,
    ''
  ].join('\n');
  await writeFile(path.join(runRoot, 'HANDOFF_STATE.md'), content, 'utf8');
}

async function assertNoActiveWriteOverlap(
  runRoot: string,
  instanceId: string,
  writeTargets: string[],
  dependencies: string[]
): Promise<void> {
  const instancesRoot = path.join(runRoot, 'instances');
  let entries: string[] = [];
  try {
    entries = await readdir(instancesRoot);
  } catch {
    return;
  }
  for (const siblingId of entries) {
    if (siblingId === instanceId) continue;
    try {
      const status = await readJson(path.join(instancesRoot, siblingId, 'STATUS.json'));
      if (!['LAUNCHED', 'RUNNING'].includes(String(status.status))) continue;
      const siblingTargets = Array.isArray(status.writeTargets)
        ? status.writeTargets.filter((item): item is string => typeof item === 'string')
        : [];
      const overlap = writeTargets.some((target) => siblingTargets.some((other) => pathsOverlap(target, other)));
      if (overlap && !dependencies.includes(siblingId)) {
        throw new HarnessError(
          'INVALID_REQUEST',
          409,
          `Concurrent write overlap with active sibling ${siblingId}`
        );
      }
    } catch (error) {
      if (error instanceof HarnessError) throw error;
      throw new HarnessError(
        'INVALID_REQUEST',
        409,
        `Cannot prove write disjointness because sibling ${siblingId} has an invalid status record`
      );
    }
  }
}

async function withRunLaunchLock<T>(runRoot: string, operation: () => Promise<T>): Promise<T> {
  await mkdir(runRoot, { recursive: true });
  const lockPath = path.join(runRoot, '.launch-lock');
  const deadline = Date.now() + 10_000;
  while (true) {
    try {
      await mkdir(lockPath);
      break;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'EEXIST') throw error;
      if (Date.now() >= deadline) {
        throw new HarnessError('INVALID_REQUEST', 409, 'Timed out waiting for orchestration launch lock');
      }
      await new Promise((resolve) => setTimeout(resolve, 10));
    }
  }
  try {
    return await operation();
  } finally {
    await rm(lockPath, { recursive: true, force: true });
  }
}

async function assertAcceptedPredecessors(
  runRoot: string,
  dependencies: string[],
  acceptedPredecessors: string[]
): Promise<void> {
  for (const dependency of dependencies) {
    if (!acceptedPredecessors.includes(dependency)) {
      throw new HarnessError('INVALID_REQUEST', 409, `Dependency ${dependency} has no manager acceptance`);
    }
    const instanceRoot = path.join(runRoot, 'instances', safeSegment(dependency, 'dependency'));
    const status = await readJson(path.join(instanceRoot, 'STATUS.json'));
    if (status.schema !== ORCHESTRATION_RECORD_SCHEMA_VERSION || status.status !== 'COMPLETED') {
      throw new HarnessError('INVALID_REQUEST', 409, `Dependency ${dependency} has no valid completed return`);
    }
    const returned = await readFile(path.join(instanceRoot, 'RETURN.md'), 'utf8');
    const requiredMarkers = Array.isArray(status.requiredReturnMarkers)
      ? status.requiredReturnMarkers.filter((marker): marker is string => typeof marker === 'string')
      : [];
    assertValidManagedChildReturn(returned, requiredMarkers);
  }
}

export class ManagedDelegationService {
  constructor(
    private readonly launchChild: ManagedChildLauncher,
    private readonly bindValidatedParent?: ManagedParentBinder
  ) {}

  async delegate(parent: SessionRecord, parentTools: readonly string[], input: DelegateAgentInput) {
    if (!input.contextSealed || !input.pipelineRunApproved || !input.approvalRef?.trim()) {
      throw new HarnessError('INVALID_REQUEST', 400, 'Delegation requires seal, run approval, and approvalRef');
    }
    if (
      !Array.isArray(input.requiredReturnMarkers) ||
      input.requiredReturnMarkers.length === 0 ||
      input.requiredReturnMarkers.some((marker) => !marker.trim())
    ) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        'Delegation requires at least one non-empty return-schema marker'
      );
    }
    requireNonEmpty(input.purpose, 'purpose');
    requireNonEmpty(input.brief, 'brief');
    requireNonEmpty(input.expectedOutput, 'expectedOutput');
    if (
      input.acceptanceCriteria.length === 0 ||
      input.acceptanceCriteria.some((criterion) => !criterion.trim())
    ) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        'Delegation requires at least one non-empty acceptance criterion'
      );
    }
    const { parentType, child } = await resolveChild(parent.persona, input);
    if (parent.orchestrationRunId && parent.orchestrationRunId !== input.runId) {
      throw new HarnessError('INVALID_REQUEST', 409, 'Managed child must remain in the parent orchestration run');
    }
    assertChildToolPolicy(parentTools, input.tools, child.instructionContent);
    const declaredContext = input.declaredContext.map((target) =>
      contained(parent.projectRoot, target, 'declaredContext')
    );
    const writeTargets = input.writeTargets.map((target) =>
      contained(parent.projectRoot, target, 'writeTarget')
    );
    assertBoundedEngineSelection({
      selection: input.engineSelection,
      selectionAuthority: input.selectionAuthority,
      child,
      tools: input.tools,
      writeTargets
    });
    const descriptors = input.tools
      .map((toolName) => getHarnessToolDescriptor(toolName))
      .filter((descriptor) => descriptor !== undefined);
    if (
      descriptors.some((descriptor) => descriptor.permissions.includes('read')) &&
      declaredContext.length === 0
    ) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        'Managed read tools require at least one declared context path'
      );
    }
    if (
      descriptors.some((descriptor) =>
        descriptor.permissions.includes('workspace-write') ||
        descriptor.permissions.includes('shell')
      ) &&
      writeTargets.length === 0
    ) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        'Managed write or shell tools require at least one declared write target'
      );
    }
    if (canonicalToolNames(input.tools).has('shell')) {
      const projectRoot = path.resolve(parent.projectRoot);
      const fullRead = declaredContext.some((target) => target === projectRoot);
      const fullWrite = writeTargets.some((target) => target === projectRoot);
      if (!fullRead || !fullWrite) {
        throw new HarnessError(
          'INVALID_REQUEST',
          400,
          'Managed Bash requires declared read and write scope over the project root; use bounded file tools or a deterministic registered tool for narrower children'
        );
      }
    }
    const executionRoot = contained(parent.projectRoot, input.executionRoot, 'executionRoot');
    const runId = safeSegment(input.runId, 'runId');
    const instanceId = `inst_${randomUUID()}`;
    const runRoot = path.join(executionRoot, '_Coordination', 'AgentRuns', runId);
    const planPath = path.join(runRoot, 'ORCHESTRATION_PLAN.md');
    const graphPath = path.join(runRoot, 'WORK_GRAPH.json');
    let initialPlan: string | undefined;
    try {
      initialPlan = await readFile(planPath, 'utf8');
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error;
    }
    if (initialPlan !== undefined) {
      if (!initialPlan.includes(`PlanVersion: ${input.planVersion}`)) {
        const version = safeSegment(input.planVersion, 'planVersion');
        let versionedPlan: string;
        try {
          versionedPlan = await readFile(
            path.join(runRoot, 'plans', version, 'ORCHESTRATION_PLAN.md'),
            'utf8'
          );
        } catch {
          throw new HarnessError('INVALID_REQUEST', 409, 'Plan version does not match the persisted run');
        }
        if (!versionedPlan.includes(`PlanVersion: ${input.planVersion}`)) {
          throw new HarnessError('INVALID_REQUEST', 409, 'Plan version does not match the persisted run');
        }
      }
      if (input.workGraph) {
        throw new HarnessError(
          'INVALID_REQUEST',
          409,
          'Existing runs accept work-graph changes only through a versioned REPLAN disposition'
        );
      }
    } else {
      if (!input.workGraph) {
        throw new HarnessError('INVALID_REQUEST', 400, 'First dispatch requires workGraph');
      }
      assertWorkGraph(input.workGraph);
      await writeNew(planPath, renderPlan(input, parent));
      await writeNew(graphPath, `${JSON.stringify({ schema: ORCHESTRATION_RECORD_SCHEMA_VERSION, ...input.workGraph }, null, 2)}\n`);
      const versionRoot = path.join(runRoot, 'plans', safeSegment(input.planVersion, 'planVersion'));
      await writeNew(path.join(versionRoot, 'ORCHESTRATION_PLAN.md'), renderPlan(input, parent));
      await writeNew(path.join(versionRoot, 'WORK_GRAPH.json'), `${JSON.stringify({ schema: ORCHESTRATION_RECORD_SCHEMA_VERSION, ...input.workGraph }, null, 2)}\n`);
    }
    const brief = renderBrief(input, instanceId, parent, declaredContext, writeTargets);
    const briefHash = sha256(brief);
    const instanceRoot = path.join(runRoot, 'instances', instanceId);
    const baseStatus = {
      schema: ORCHESTRATION_RECORD_SCHEMA_VERSION,
      policyVersion: MANAGED_DELEGATION_POLICY_VERSION,
      runId,
      planVersion: input.planVersion,
      instanceId,
      parentSessionId: parent.sessionId,
      parentRole: parent.persona,
      parentAgentType: parentType,
      childKind: input.childKind,
      childRole: child.persona,
      childAgentType: child.agentType,
      instructionPath: child.instructionPath,
      instructionHash: child.instructionHash,
      briefHash,
      declaredContext,
      tools: input.tools,
      engineSelection: input.engineSelection,
      writeTargets,
      outputArtifact: null,
      requiredReturnMarkers: input.requiredReturnMarkers
    };
    await withRunLaunchLock(runRoot, async () => {
      await assertAcceptedPredecessors(runRoot, input.dependencies, input.acceptedPredecessors ?? []);
      await assertNoActiveWriteOverlap(runRoot, instanceId, writeTargets, input.dependencies);
      await writeNew(path.join(instanceRoot, 'LAUNCH_BRIEF.md'), brief);
      await writeNew(path.join(instanceRoot, 'STATUS.json'), `${JSON.stringify({ ...baseStatus, status: 'LAUNCHED' }, null, 2)}\n`);
      await writeAtomic(path.join(instanceRoot, 'STATUS.json'), `${JSON.stringify({ ...baseStatus, status: 'RUNNING' }, null, 2)}\n`);
    });
    try {
      const parentForRun: SessionRecord = {
        ...parent,
        orchestrationRunId: runId,
        executionRoot,
        planVersion: input.planVersion
      };
      const launchParent = this.bindValidatedParent
        ? await this.bindValidatedParent(parentForRun)
        : parentForRun;
      const returned = await this.launchChild({
        parent: launchParent,
        childPersona: child.persona,
        childKind: input.childKind,
        childAgentType: child.agentType,
        childInstanceId: instanceId,
        runId,
        brief,
        declaredContext,
        tools: input.tools,
        engineSelection: input.engineSelection,
        writeTargets,
        instructionContent: child.instructionContent,
        instructionPath: child.instructionPath,
        instructionHash: child.instructionHash,
        briefHash,
        requiredReturnMarkers: input.requiredReturnMarkers,
        approvalRef: input.approvalRef,
        executionMode: input.executionMode ?? 'WAIT'
      });
      if (returned.status === 'COMPLETED') {
        assertValidManagedChildReturn(returned.output, input.requiredReturnMarkers);
      }
      if (returned.status !== 'RUNNING') {
        await writeNew(path.join(instanceRoot, 'RETURN.md'), returned.output.endsWith('\n') ? returned.output : `${returned.output}\n`);
      }
      await writeAtomic(path.join(instanceRoot, 'STATUS.json'), `${JSON.stringify({ ...baseStatus, childSessionId: returned.sessionId, status: returned.status, outputArtifact: returned.status === 'RUNNING' ? null : returned.outputArtifact ?? path.join(instanceRoot, 'RETURN.md') }, null, 2)}\n`);
      await refreshOrchestrationHandoff(runRoot);
      return { runId, instanceId, ...returned, instructionHash: child.instructionHash, briefHash };
    } catch (error) {
      const message = error instanceof Error ? error.message : 'managed child failed';
      await writeAtomic(path.join(instanceRoot, 'STATUS.json'), `${JSON.stringify({ ...baseStatus, status: 'FAILED', error: message }, null, 2)}\n`);
      await refreshOrchestrationHandoff(runRoot);
      throw error;
    }
  }
}

export function coordinationRunRoot(session: SessionRecord): string {
  if (!session.orchestrationRunId) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Session is not attached to an orchestration run');
  }
  const executionRoot = contained(session.projectRoot, session.executionRoot ?? 'execution', 'executionRoot');
  return path.join(executionRoot, '_Coordination', 'AgentRuns', safeSegment(session.orchestrationRunId, 'runId'));
}

async function assertManagedChildSession(
  session: SessionRecord
): Promise<{ parentSessionId: string; agentInstanceId: string }> {
  if (!session.parentSessionId || !session.agentInstanceId) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Only a managed child may use this channel');
  }
  const status = await readJson(
    path.join(
      coordinationRunRoot(session),
      'instances',
      safeSegment(session.agentInstanceId, 'agentInstanceId'),
      'STATUS.json'
    )
  );
  if (
    status.childSessionId !== session.sessionId ||
    status.parentSessionId !== session.parentSessionId
  ) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'Session is not the recorded direct child for this orchestration instance'
    );
  }
  return {
    parentSessionId: session.parentSessionId,
    agentInstanceId: session.agentInstanceId
  };
}

export async function reportCoordinationNotice(session: SessionRecord, input: {
  noticeType: string;
  claimStatus: ClaimStatus;
  summary: string;
  evidenceRefs: string[];
  affectedScopes: string[];
  requestedAction: string;
  blocking: boolean;
  humanDecisionRequired: boolean;
  acceptedBasisRef: string;
  validationRef?: string;
  humanAcceptanceRef?: string;
}) {
  if (input.claimStatus === 'VALIDATED' && !input.validationRef?.trim()) {
    throw new HarnessError('INVALID_REQUEST', 400, 'VALIDATED notice requires validationRef');
  }
  if (input.claimStatus === 'ACCEPTED' && !input.humanAcceptanceRef?.trim()) {
    throw new HarnessError('INVALID_REQUEST', 400, 'ACCEPTED notice requires humanAcceptanceRef');
  }
  const { parentSessionId, agentInstanceId } = await assertManagedChildSession(session);
  const noticeId = `notice_${randomUUID()}`;
  const record = { schema: ORCHESTRATION_RECORD_SCHEMA_VERSION, noticeId, runId: session.orchestrationRunId, senderInstanceId: agentInstanceId, senderSessionId: session.sessionId, parentSessionId, ...input, createdAt: new Date().toISOString() };
  await writeNew(path.join(coordinationRunRoot(session), 'notices', `${noticeId}.json`), `${JSON.stringify(record, null, 2)}\n`);
  const event = createHarnessEvent({ sessionId: parentSessionId, type: 'coordination.notice', data: record });
  await appendHarnessEvent(event);
  getPermissionEventChannel().publish(parentSessionId, event);
  return record;
}

export async function sendAgentUpdate(parent: SessionRecord, input: {
  childInstanceId: string;
  noticeId?: string;
  disposition: CoordinationDisposition;
  summary: string;
  claimStatus: ClaimStatus;
  evidenceRefs: string[];
  consequential: boolean;
  humanRulingRef?: string;
  amendment?: string;
  planVersion?: string;
  selectionAuthority?: SelectionAuthority;
  posture?: OrchestrationPosture;
  acceptedBasis?: string[];
  workGraph?: Record<string, unknown>;
  validationRef?: string;
  humanAcceptanceRef?: string;
  amendmentCategories?: AmendmentCategory[];
  amendmentVersion?: string;
}) {
  const runRoot = coordinationRunRoot(parent);
  const childStatus = await readJson(path.join(runRoot, 'instances', safeSegment(input.childInstanceId, 'childInstanceId'), 'STATUS.json'));
  if (childStatus.parentSessionId !== parent.sessionId) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Updates may be sent only to a direct child');
  }
  if (childStatus.status !== 'RUNNING') {
    throw new HarnessError('INVALID_REQUEST', 409, 'Updates may be sent only to an active child');
  }
  const categoricalHumanTriggers = new Set<AmendmentCategory>([
    'SCOPE', 'RISK', 'AUTHORITY', 'SHARED_WRITE', 'ACCEPTANCE'
  ]);
  if (
    (input.disposition === 'AMEND' || input.disposition === 'REPLAN') &&
    (!input.amendmentCategories || input.amendmentCategories.length === 0)
  ) {
    throw new HarnessError('INVALID_REQUEST', 400, 'AMEND and REPLAN require amendmentCategories');
  }
  if (input.amendment && !input.amendmentVersion?.trim() && !input.planVersion?.trim()) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Versioned amendment requires amendmentVersion or planVersion');
  }
  const categoryRequiresHuman = input.amendmentCategories?.some((category) =>
    categoricalHumanTriggers.has(category)
  ) ?? false;
  if ((input.consequential || categoryRequiresHuman) && !input.humanRulingRef?.trim()) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Consequential amendment requires humanRulingRef');
  }
  if (input.claimStatus === 'VALIDATED' && !input.validationRef?.trim()) {
    throw new HarnessError('INVALID_REQUEST', 400, 'VALIDATED update requires validationRef');
  }
  if (input.claimStatus === 'ACCEPTED' && !input.humanAcceptanceRef?.trim()) {
    throw new HarnessError('INVALID_REQUEST', 400, 'ACCEPTED update requires humanAcceptanceRef');
  }
  if (input.disposition === 'RELAY' && !input.noticeId) {
    throw new HarnessError('INVALID_REQUEST', 400, 'RELAY requires noticeId');
  }
  let sourceNotice: Record<string, unknown> | undefined;
  if (input.noticeId) {
    sourceNotice = await readJson(
      path.join(runRoot, 'notices', `${safeSegment(input.noticeId, 'noticeId')}.json`)
    );
    if (
      input.disposition === 'RELAY' &&
      sourceNotice.claimStatus !== input.claimStatus
    ) {
      throw new HarnessError(
        'INVALID_REQUEST',
        409,
        'Informational relay must preserve the source notice claim status'
      );
    }
  }
  if (input.disposition === 'REPLAN') {
    if (
      !input.planVersion?.trim() ||
      !input.selectionAuthority ||
      !input.posture ||
      !input.acceptedBasis ||
      !input.workGraph ||
      !input.amendment?.trim()
    ) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        'REPLAN requires planVersion, selectionAuthority, posture, acceptedBasis, workGraph, and amendment'
      );
    }
    assertWorkGraph(input.workGraph, 'REPLAN workGraph');
    const planVersion = safeSegment(input.planVersion, 'planVersion');
    const versionRoot = path.join(runRoot, 'plans', planVersion);
    const plan = [
      '# Orchestration Plan',
      '',
      `- Schema: ${ORCHESTRATION_RECORD_SCHEMA_VERSION}`,
      `- RunID: ${parent.orchestrationRunId}`,
      `- PlanVersion: ${input.planVersion}`,
      `- SelectionAuthority: ${input.selectionAuthority}`,
      `- Posture: ${input.posture}`,
      `- ParentSession: ${parent.sessionId}`,
      `- ParentRole: ${parent.persona}`,
      `- AcceptedBasis: ${input.acceptedBasis.join('; ')}`,
      `- ConcurrencyEligibility: ${JSON.stringify(input.workGraph.concurrencyEligibility)}`,
      `- ExpectedReturns: ${JSON.stringify(input.workGraph.expectedReturns)}`,
      `- FanInGates: ${JSON.stringify(input.workGraph.fanInGates)}`,
      `- HumanDecisionPoints: ${JSON.stringify(input.workGraph.humanDecisionPoints)}`,
      ''
    ].join('\n');
    await writeNew(path.join(versionRoot, 'ORCHESTRATION_PLAN.md'), plan);
    await writeNew(
      path.join(versionRoot, 'WORK_GRAPH.json'),
      `${JSON.stringify({ schema: ORCHESTRATION_RECORD_SCHEMA_VERSION, ...input.workGraph }, null, 2)}\n`
    );
  } else if (input.workGraph || input.planVersion) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'Plan versions and work graphs may be changed only by a REPLAN disposition'
    );
  }
  const updateId = `update_${randomUUID()}`;
  const record = { schema: ORCHESTRATION_RECORD_SCHEMA_VERSION, updateId, runId: parent.orchestrationRunId, parentSessionId: parent.sessionId, sourceNoticeClaimStatus: sourceNotice?.claimStatus, ...input, createdAt: new Date().toISOString() };
  await writeNew(path.join(runRoot, 'updates', `${updateId}.json`), `${JSON.stringify(record, null, 2)}\n`);
  if (input.noticeId) {
    await writeNew(path.join(runRoot, 'dispositions', `${safeSegment(input.noticeId, 'noticeId')}.json`), `${JSON.stringify(record, null, 2)}\n`);
  }
  if (input.amendment) {
    const amendmentVersion = safeSegment(
      input.amendmentVersion ?? input.planVersion ?? '',
      'amendmentVersion'
    );
    await writeNew(path.join(runRoot, 'amendments', input.childInstanceId, `${amendmentVersion}.md`), `${input.amendment.trim()}\n`);
  }
  const childSessionId = typeof childStatus.childSessionId === 'string' ? childStatus.childSessionId : undefined;
  if (childSessionId) {
    const event = createHarnessEvent({ sessionId: childSessionId, type: 'coordination.update', data: record });
    await appendHarnessEvent(event);
    getPermissionEventChannel().publish(childSessionId, event);
  }
  return record;
}

export async function acknowledgeAgentUpdate(session: SessionRecord, input: {
  updateId: string;
  acknowledgment: UpdateAcknowledgment;
  summary?: string;
}) {
  const { parentSessionId, agentInstanceId } = await assertManagedChildSession(session);
  const runRoot = coordinationRunRoot(session);
  const update = await readJson(path.join(runRoot, 'updates', `${safeSegment(input.updateId, 'updateId')}.json`));
  if (update.childInstanceId !== agentInstanceId || update.parentSessionId !== parentSessionId) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Update is not addressed to this child');
  }
  const record = { schema: ORCHESTRATION_RECORD_SCHEMA_VERSION, childInstanceId: agentInstanceId, childSessionId: session.sessionId, ...input, acknowledgedAt: new Date().toISOString() };
  await writeNew(path.join(runRoot, 'acknowledgments', `${input.updateId}.json`), `${JSON.stringify(record, null, 2)}\n`);
  const event = createHarnessEvent({ sessionId: parentSessionId, type: 'coordination.acknowledged', data: record });
  await appendHarnessEvent(event);
  getPermissionEventChannel().publish(parentSessionId, event);
  return record;
}
