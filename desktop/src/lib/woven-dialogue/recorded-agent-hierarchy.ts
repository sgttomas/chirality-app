import type {
  OperatorSessionProjection,
  ProjectionCurrency,
  ProjectionDiagnostic,
  RecordedAgentHierarchy
} from './contracts';

const CURRENCIES = new Set<ProjectionCurrency>([
  'CURRENT',
  'STALE',
  'CONFLICTING',
  'UNKNOWN'
]);
const ROLES = new Set<NonNullable<OperatorSessionProjection['role']>>([
  'agent0',
  'agent1',
  'agent2'
]);
const RUNTIME_STATUSES = new Set<
  NonNullable<OperatorSessionProjection['runtimeStatus']>
>(['idle', 'running', 'completed', 'failed', 'interrupted']);

export type RecordedSessionEvidence = {
  sessionId: unknown;
  sourceReference: unknown;
  observedAt: unknown;
  currency?: unknown;
  persona?: unknown;
  role?: unknown;
  status?: unknown;
  engineSelection?: {
    adapterId?: unknown;
    providerId?: unknown;
    model?: unknown;
  };
  residencyEpoch?: unknown;
  parentSessionId?: unknown;
  outputArtifact?: unknown;
  approvalRef?: unknown;
};

function nonEmptyString(value: unknown): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const normalized = value.trim();
  return normalized.length > 0 ? normalized : undefined;
}

function currencyFromEvidence(
  value: unknown,
  diagnostics: ProjectionDiagnostic[],
  sourceReference?: string
): ProjectionCurrency {
  if (typeof value === 'string' && CURRENCIES.has(value as ProjectionCurrency)) {
    return value as ProjectionCurrency;
  }
  if (value !== undefined) {
    diagnostics.push({
      code: 'INVALID_CURRENCY',
      message: 'Recorded currency is outside the admitted projection vocabulary.',
      sourceReference
    });
  }
  return 'UNKNOWN';
}

function optionalRecordedValue(
  value: unknown,
  field: string,
  diagnostics: ProjectionDiagnostic[],
  sourceReference?: string
): string | undefined {
  const recorded = nonEmptyString(value);
  if (value !== undefined && recorded === undefined) {
    diagnostics.push({
      code: `INVALID_${field.toUpperCase()}`,
      message: `${field} was present but was not a non-empty recorded string.`,
      sourceReference
    });
  }
  return recorded;
}

function optionalRole(
  value: unknown,
  diagnostics: ProjectionDiagnostic[],
  sourceReference?: string
): OperatorSessionProjection['role'] {
  if (value === undefined) {
    return undefined;
  }
  if (typeof value === 'string' && ROLES.has(value as NonNullable<OperatorSessionProjection['role']>)) {
    return value as NonNullable<OperatorSessionProjection['role']>;
  }
  diagnostics.push({
    code: 'INVALID_ROLE',
    message: 'Recorded role is outside the admitted agent0/agent1/agent2 vocabulary.',
    sourceReference
  });
  return undefined;
}

function optionalRuntimeStatus(
  value: unknown,
  diagnostics: ProjectionDiagnostic[],
  sourceReference?: string
): OperatorSessionProjection['runtimeStatus'] {
  if (value === undefined) {
    return undefined;
  }
  if (
    typeof value === 'string' &&
    RUNTIME_STATUSES.has(value as NonNullable<OperatorSessionProjection['runtimeStatus']>)
  ) {
    return value as NonNullable<OperatorSessionProjection['runtimeStatus']>;
  }
  diagnostics.push({
    code: 'INVALID_RUNTIME_STATUS',
    message: 'Recorded runtime status is outside the admitted runtime vocabulary.',
    sourceReference
  });
  return undefined;
}

export function buildRecordedAgentHierarchy(
  evidence: readonly RecordedSessionEvidence[]
): RecordedAgentHierarchy {
  const hierarchyDiagnostics: ProjectionDiagnostic[] = [];
  const bySessionId = new Map<string, RecordedSessionEvidence>();
  const conflictingSessionIds = new Set<string>();

  for (const candidate of evidence) {
    const sessionId = nonEmptyString(candidate.sessionId);
    const sourceReference = nonEmptyString(candidate.sourceReference);
    if (!sessionId) {
      hierarchyDiagnostics.push({
        code: 'INVALID_SESSION_ID',
        message: 'Session evidence without a non-empty sessionId cannot enter the hierarchy.',
        sourceReference
      });
      continue;
    }
    if (bySessionId.has(sessionId)) {
      conflictingSessionIds.add(sessionId);
      hierarchyDiagnostics.push({
        code: 'DUPLICATE_SESSION_ID',
        message: `Multiple admitted records claim sessionId ${sessionId}; the first record is retained and marked conflicting.`,
        sourceReference
      });
      continue;
    }
    bySessionId.set(sessionId, candidate);
  }

  const admittedSessionIds = new Set(bySessionId.keys());
  const projections: OperatorSessionProjection[] = [];

  for (const sessionId of [...bySessionId.keys()].sort()) {
    const candidate = bySessionId.get(sessionId)!;
    const diagnostics: ProjectionDiagnostic[] = [];
    const sourceReference =
      optionalRecordedValue(
        candidate.sourceReference,
        'source reference',
        diagnostics
      ) ?? 'SOURCE_NOT_RECORDED';
    const observedAt =
      optionalRecordedValue(candidate.observedAt, 'observed at', diagnostics, sourceReference) ??
      'OBSERVATION_TIME_NOT_RECORDED';
    const recordedParentSessionId = nonEmptyString(candidate.parentSessionId);
    const parentAvailable = recordedParentSessionId
      ? admittedSessionIds.has(recordedParentSessionId)
      : false;

    if (candidate.parentSessionId !== undefined && !recordedParentSessionId) {
      diagnostics.push({
        code: 'INVALID_PARENT_SESSION_ID',
        message: 'parentSessionId was present but was not a non-empty recorded identifier.',
        sourceReference
      });
    } else if (recordedParentSessionId && !parentAvailable) {
      diagnostics.push({
        code: 'PARENT_SESSION_UNAVAILABLE',
        message: `Recorded parent ${recordedParentSessionId} is not present in the admitted session set.`,
        sourceReference
      });
    } else if (recordedParentSessionId === sessionId) {
      diagnostics.push({
        code: 'SELF_PARENT_REFERENCE',
        message: `Session ${sessionId} records itself as its parent.`,
        sourceReference
      });
    }

    const projection: OperatorSessionProjection = {
      projectionId: `recorded-session:${sessionId}`,
      sourceReference,
      sessionId,
      observedAt,
      currency: conflictingSessionIds.has(sessionId)
        ? 'CONFLICTING'
        : currencyFromEvidence(candidate.currency, diagnostics, sourceReference),
      parentage: recordedParentSessionId
        ? {
            state: 'RECORDED',
            parentSessionId: recordedParentSessionId,
            parentAvailable
          }
        : {
            state: 'NOT_RECORDED'
          },
      diagnostics
    };

    const persona = optionalRecordedValue(
      candidate.persona,
      'persona',
      diagnostics,
      sourceReference
    );
    const role = optionalRole(candidate.role, diagnostics, sourceReference);
    const runtimeStatus = optionalRuntimeStatus(
      candidate.status,
      diagnostics,
      sourceReference
    );
    const adapterId = optionalRecordedValue(
      candidate.engineSelection?.adapterId,
      'adapter id',
      diagnostics,
      sourceReference
    );
    const providerId = optionalRecordedValue(
      candidate.engineSelection?.providerId,
      'provider id',
      diagnostics,
      sourceReference
    );
    const model = optionalRecordedValue(
      candidate.engineSelection?.model,
      'model',
      diagnostics,
      sourceReference
    );
    const residencyEpoch = optionalRecordedValue(
      candidate.residencyEpoch,
      'residency epoch',
      diagnostics,
      sourceReference
    );
    const outputArtifactReference = optionalRecordedValue(
      candidate.outputArtifact,
      'output artifact',
      diagnostics,
      sourceReference
    );
    const approvalEvidenceReference = optionalRecordedValue(
      candidate.approvalRef,
      'approval reference',
      diagnostics,
      sourceReference
    );

    if (persona) projection.persona = persona;
    if (role) projection.role = role;
    if (runtimeStatus) projection.runtimeStatus = runtimeStatus;
    if (adapterId) projection.adapterId = adapterId;
    if (providerId) projection.providerId = providerId;
    if (model) projection.model = model;
    if (residencyEpoch) projection.residencyEpoch = residencyEpoch;
    if (outputArtifactReference) {
      projection.outputArtifactReference = outputArtifactReference;
    }
    if (approvalEvidenceReference) {
      projection.approvalEvidenceReference = approvalEvidenceReference;
    }

    projections.push(projection);
  }

  const roots: OperatorSessionProjection[] = [];
  const children = new Map<string, OperatorSessionProjection[]>();
  const unresolvedParentSessionIds = new Set<string>();

  for (const projection of projections) {
    if (projection.parentage.state === 'NOT_RECORDED') {
      roots.push(projection);
      continue;
    }

    const parentSessionId = projection.parentage.parentSessionId;
    const siblings = children.get(parentSessionId) ?? [];
    siblings.push(projection);
    children.set(parentSessionId, siblings);
    if (!projection.parentage.parentAvailable) {
      unresolvedParentSessionIds.add(parentSessionId);
    }
  }

  const childrenByParentSessionId = Object.fromEntries(
    [...children.entries()]
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([parentSessionId, childProjections]) => [
        parentSessionId,
        [...childProjections].sort((left, right) =>
          left.sessionId.localeCompare(right.sessionId)
        )
      ])
  );
  const reachableSessionIds = new Set<string>();
  const pending = [...roots];
  while (pending.length > 0) {
    const current = pending.pop();
    if (!current || reachableSessionIds.has(current.sessionId)) {
      continue;
    }
    reachableSessionIds.add(current.sessionId);
    pending.push(...(childrenByParentSessionId[current.sessionId] ?? []));
  }
  const detached = projections.filter(
    (projection) => !reachableSessionIds.has(projection.sessionId)
  );

  return {
    roots,
    detached,
    childrenByParentSessionId,
    unresolvedParentSessionIds: [...unresolvedParentSessionIds].sort(),
    diagnostics: hierarchyDiagnostics
  };
}
