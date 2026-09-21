import { isSessionBootConfirmed } from '../harness/session-boot-readiness';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import type {
  OperatorSessionProjection,
  ProjectionCurrency,
  ProjectionDiagnostic
} from './contracts';
import type { ChiralityRoleName, QualifiedMethodReference } from '@chirality/runtime-contracts/v3';

type SessionSource = SessionRecord & Record<string, unknown>;

export type OperatorProjectionOptions = {
  observedAt: string;
  currencyBySessionId?: Readonly<Record<string, ProjectionCurrency>>;
};

export type OperatorProjectionResult = {
  sessions: OperatorSessionProjection[];
  diagnostics: ProjectionDiagnostic[];
};

const RUNTIME_STATUSES = new Set([
  'idle',
  'running',
  'completed',
  'failed',
  'interrupted'
] as const);

function readString(value: unknown): string | undefined {
  return typeof value === 'string' && value.trim().length > 0 ? value : undefined;
}

const ROLE_IDS = new Set<ChiralityRoleName>(['HELP_HUMAN', 'HELPS_HUMANS', 'WORKING_ITEMS', 'TASK']);
const DIRECT_ENTRY_ROLE_IDS = new Set<ChiralityRoleName>(['HELP_HUMAN', 'HELPS_HUMANS', 'WORKING_ITEMS']);
const INTERACTION_MODES = new Set(['chat', 'native-plan'] as const);
const PERMISSION_MODES = new Set(['readOnly', 'ask', 'workspaceWrite', 'bypass'] as const);

function readMethods(value: unknown): QualifiedMethodReference[] | undefined {
  if (!Array.isArray(value)) return undefined;
  const methods: QualifiedMethodReference[] = [];
  for (const entry of value) {
    if (!entry || typeof entry !== 'object') return undefined;
    const item = entry as Record<string, unknown>;
    if ((item.kind !== 'skill' && item.kind !== 'workflow') ||
      (item.source !== 'project' && item.source !== 'user' && item.source !== 'bundled') ||
      !readString(item.name) || !readString(item.sourceRootId)) return undefined;
    methods.push({ kind: item.kind, source: item.source, name: item.name as string, sourceRootId: item.sourceRootId as string });
  }
  return methods;
}

function recordedRole(
  source: SessionSource,
  diagnostics: ProjectionDiagnostic[],
  sourceReference: string
): OperatorSessionProjection['role'] {
  const explicitRole =
    source.role === 'agent0' || source.role === 'agent1' || source.role === 'agent2'
      ? source.role
      : undefined;
  const agentTypeRole =
    source.agentType === 0
      ? 'agent0'
      : source.agentType === 1
        ? 'agent1'
        : source.agentType === 2
          ? 'agent2'
          : undefined;

  if (explicitRole && agentTypeRole && explicitRole !== agentTypeRole) {
    diagnostics.push({
      code: 'CONFLICTING_RECORDED_ROLE',
      message: 'Recorded role and agentType disagree; role is not projected.',
      sourceReference
    });
    return undefined;
  }

  return explicitRole ?? agentTypeRole;
}

function runtimeStatus(source: SessionSource): OperatorSessionProjection['runtimeStatus'] {
  return typeof source.status === 'string' &&
    RUNTIME_STATUSES.has(
      source.status as NonNullable<OperatorSessionProjection['runtimeStatus']>
    )
    ? (source.status as OperatorSessionProjection['runtimeStatus'])
    : undefined;
}

function projectionSignature(source: SessionSource): string {
  return JSON.stringify({
    sessionId: source.sessionId,
    parentSessionId: source.parentSessionId,
    role: source.role,
    agentType: source.agentType,
    status: source.status,
    engineSelection: source.engineSelection,
    model: source.model,
    reasoningEffort: source.reasoningEffort,
    residencyEpoch: source.residencyEpoch,
    schemaVersion: source.schemaVersion,
    roleId: source.roleId,
    interactionMode: source.interactionMode,
    permissionMode: source.permissionMode,
    selectedMethods: source.selectedMethods,
    methodSelectionRevision: source.methodSelectionRevision,
    instructionBasisId: source.instructionBasisId,
    outputArtifact: source.outputArtifact,
    approvalRef: source.approvalRef
  });
}

function projectOne(
  session: SessionRecord,
  availableSessionIds: ReadonlySet<string>,
  options: OperatorProjectionOptions,
  conflictDiagnostic?: ProjectionDiagnostic
): OperatorSessionProjection {
  const source = session as unknown as SessionSource;
  const sourceReference = `session:${session.sessionId}`;
  const diagnostics: ProjectionDiagnostic[] = [];
  if (conflictDiagnostic) {
    diagnostics.push(conflictDiagnostic);
  }

  const role = recordedRole(source, diagnostics, sourceReference);
  const parentSessionId = readString(source.parentSessionId);
  const engineSelection =
    source.engineSelection && typeof source.engineSelection === 'object'
      ? source.engineSelection
      : undefined;
  const selectedCurrency = options.currencyBySessionId?.[session.sessionId] ?? 'UNKNOWN';
  const hasConflict =
    Boolean(conflictDiagnostic) ||
    diagnostics.some((diagnostic) => diagnostic.code.startsWith('CONFLICTING_'));
  const persona = readString(source.persona);
  const status = runtimeStatus(source);
  const adapterId = readString(engineSelection?.adapterId);
  const providerId = readString(engineSelection?.providerId);
  const model = readString(engineSelection?.model) ?? readString(source.model);
  const reasoningEffort = readString(source.reasoningEffort);
  const residencyEpoch = readString(source.residencyEpoch);
  const outputArtifactReference = readString(source.outputArtifact);
  const approvalEvidenceReference = readString(source.approvalRef);
  const roleId = typeof source.roleId === 'string' && ROLE_IDS.has(source.roleId as ChiralityRoleName)
    ? source.roleId as ChiralityRoleName : undefined;
  const interactionMode = typeof source.interactionMode === 'string' && INTERACTION_MODES.has(source.interactionMode as 'chat' | 'native-plan')
    ? source.interactionMode as 'chat' | 'native-plan' : undefined;
  const permissionMode = typeof source.permissionMode === 'string' && PERMISSION_MODES.has(source.permissionMode as 'readOnly' | 'ask' | 'workspaceWrite' | 'bypass')
    ? source.permissionMode as 'readOnly' | 'ask' | 'workspaceWrite' | 'bypass' : undefined;
  const selectedMethods = readMethods(source.selectedMethods);
  const instructionBasisId = readString(source.instructionBasisId);
  const methodSelectionRevision = typeof source.methodSelectionRevision === 'number' && Number.isSafeInteger(source.methodSelectionRevision) && source.methodSelectionRevision >= 0
    ? source.methodSelectionRevision : undefined;
  const expectedRole = roleId === 'HELP_HUMAN' ? 'agent0' : roleId === 'TASK' ? 'agent2' : roleId ? 'agent1' : undefined;
  // A running session is continuable too: the Runtime owns its turn, and the
  // chat panel re-attaches to it on resume (Working, Stop available) instead of
  // sending anything. Refusing it would strand a chat reopened during work in
  // the read-only lens.
  const continuation = source.schemaVersion === 'chirality.session/v3' && roleId && DIRECT_ENTRY_ROLE_IDS.has(roleId) && interactionMode && permissionMode && selectedMethods &&
    instructionBasisId && methodSelectionRevision !== undefined && status && role === expectedRole
    ? { schemaVersion: 'chirality.session/v3' as const, projectRoot: session.projectRoot, roleId,
        mode: session.mode, interactionMode, permissionMode, selectedMethods, methodSelectionRevision, instructionBasisId }
    : undefined;

  return {
    projectionId: `operator-session:${session.sessionId}`,
    sourceReference,
    sessionId: session.sessionId,
    observedAt: options.observedAt,
    currency: hasConflict ? 'CONFLICTING' : selectedCurrency,
    ...(persona ? { persona } : {}),
    ...(role ? { role } : {}),
    ...(status ? { runtimeStatus: status } : {}),
    ...(adapterId ? { adapterId } : {}),
    ...(providerId ? { providerId } : {}),
    ...(model ? { model } : {}),
    ...(reasoningEffort ? { reasoningEffort } : {}),
    ...(residencyEpoch ? { residencyEpoch } : {}),
    parentage: parentSessionId
      ? {
          state: 'RECORDED',
          parentSessionId,
          parentAvailable: availableSessionIds.has(parentSessionId)
        }
      : { state: 'NOT_RECORDED' },
    ...(outputArtifactReference ? { outputArtifactReference } : {}),
    ...(approvalEvidenceReference ? { approvalEvidenceReference } : {}),
    ...(continuation ? { continuation } : {}),
    ...(source.schemaVersion === 'chirality.session/v3' ? { bootstrapConfirmed: isSessionBootConfirmed(source) } : {}),
    diagnostics
  };
}

/**
 * Build a disposable, provider-neutral view over exact canonical session
 * fields. No relationship, role, model, status, approval, or currency is
 * derived from persona, prose, timestamp order, or visual placement.
 */
export function buildOperatorSessionProjection(
  sourceSessions: readonly SessionRecord[],
  options: OperatorProjectionOptions
): OperatorProjectionResult {
  const grouped = new Map<string, SessionRecord[]>();
  for (const session of sourceSessions) {
    const records = grouped.get(session.sessionId) ?? [];
    records.push(session);
    grouped.set(session.sessionId, records);
  }

  const availableSessionIds = new Set(grouped.keys());
  const diagnostics: ProjectionDiagnostic[] = [];
  const sessions: OperatorSessionProjection[] = [];

  for (const [sessionId, records] of grouped) {
    const first = records[0];
    if (!first) {
      continue;
    }
    const conflicting =
      new Set(
        records.map((record) =>
          projectionSignature(record as unknown as SessionSource)
        )
      ).size > 1;
    const conflictDiagnostic = conflicting
      ? {
          code: 'CONFLICTING_SESSION_RECORDS',
          message: `Canonical sources disagree for session ${sessionId}; the first record is shown without resolving the conflict.`,
          sourceReference: `session:${sessionId}`
        }
      : undefined;

    if (conflictDiagnostic) {
      diagnostics.push(conflictDiagnostic);
    }
    sessions.push(projectOne(first, availableSessionIds, options, conflictDiagnostic));
  }

  return { sessions, diagnostics };
}

export function projectOperatorSession(
  session: SessionRecord,
  availableSessionIds: ReadonlySet<string>,
  options: OperatorProjectionOptions
): OperatorSessionProjection {
  return projectOne(session, availableSessionIds, options);
}
