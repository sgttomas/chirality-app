import type { DependencyRegisterRow } from '../dependencies/schema';
import type { LifecycleState, ParsedStatusDocument } from '../lifecycle/status-parser';

const BLOCKING_DEPENDENCY_TYPES = new Set(['PREREQUISITE', 'CONSTRAINT']);
const NON_BLOCKING_SATISFACTION = new Set(['SATISFIED', 'WAIVED', 'NOT_APPLICABLE']);
const BLOCKER_SUBSET_DEPENDENCY_CLASS = 'EXECUTION';
const BLOCKER_SUBSET_TARGET_TYPE = 'DELIVERABLE';
const HUMAN_GATE_TARGETS = new Set(['CHECKING', 'ISSUED']);
const LIFECYCLE_TRANSITION_AGENTS = new Set(['CHANGE', 'WORKING_ITEMS']);

const NEXT_LIFECYCLE_TARGETS: Record<LifecycleState, LifecycleState[]> = {
  OPEN: ['INITIALIZED'],
  INITIALIZED: ['SEMANTIC_READY', 'IN_PROGRESS'],
  SEMANTIC_READY: ['IN_PROGRESS'],
  IN_PROGRESS: ['CHECKING'],
  CHECKING: ['ISSUED'],
  ISSUED: []
};

type WorkspaceErrorPayload = {
  error?: {
    type?: string;
    message?: string;
    details?: unknown;
  };
};

export class WorkspaceApiClientError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details?: unknown;

  constructor(status: number, code: string, message: string, details?: unknown) {
    super(message);
    this.name = 'WorkspaceApiClientError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

async function readJson<T>(response: Response): Promise<T | undefined> {
  try {
    return (await response.json()) as T;
  } catch {
    return undefined;
  }
}

async function requestWorkspaceApi<T>(
  input: RequestInfo | URL,
  init: RequestInit,
  fallbackMessage: string
): Promise<T> {
  const response = await fetch(input, init);
  const payload = await readJson<T & WorkspaceErrorPayload>(response);

  if (!response.ok) {
    const type = payload?.error?.type ?? 'WORKSPACE_API_ERROR';
    const message = payload?.error?.message ?? fallbackMessage;
    throw new WorkspaceApiClientError(response.status, type, message, payload?.error?.details);
  }

  if (!payload) {
    throw new WorkspaceApiClientError(
      response.status,
      'INVALID_RESPONSE',
      'Workspace API returned an empty response body'
    );
  }

  return payload as T;
}

export interface DeliverableStatusSnapshot {
  projectRoot: string;
  deliverablePath: string;
  statusFilePath: string;
  status: ParsedStatusDocument;
}

export interface DeliverableStatusTransitionResult extends DeliverableStatusSnapshot {
  transition: {
    from: string;
    to: string;
    actor: string;
  };
}

export interface DeliverableDependenciesSnapshot {
  projectRoot: string;
  deliverablePath: string;
  dependenciesFilePath: string;
  dependenciesSummaryPath?: string;
  registerPresent: boolean;
  secondarySummaryPresent: boolean;
  headers: string[];
  rows: DependencyRegisterRow[];
  warnings: string[];
}

export interface DeliverableStatusTransitionInput {
  projectRoot: string;
  deliverablePath: string;
  targetState: string;
  actor: string;
  date?: string;
  metadata?: Record<string, string>;
  approvalSha?: string;
}

export interface DependencyRowSummary {
  totalRows: number;
  activeRows: number;
  activeUpstreamBlockerCandidates: number;
  bySatisfaction: Record<string, number>;
}

export function workspaceApiErrorMessage(error: unknown): string {
  if (error instanceof WorkspaceApiClientError) {
    return `${error.code}: ${error.message}`;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'Unexpected workspace API failure';
}

export function currentIsoDate(now = new Date()): string {
  return now.toISOString().slice(0, 10);
}

export function nextLifecycleTargets(currentState: LifecycleState): LifecycleState[] {
  return NEXT_LIFECYCLE_TARGETS[currentState] ?? [];
}

export function requiresApprovalShaForTarget(targetState: string | undefined): boolean {
  return HUMAN_GATE_TARGETS.has((targetState ?? '').trim().toUpperCase());
}

export function canAgentTransitionLifecycle(agent: string | undefined): boolean {
  return LIFECYCLE_TRANSITION_AGENTS.has((agent ?? '').trim().toUpperCase());
}

function hasUnresolvedAssumptionGate(notes: string | undefined): boolean {
  const normalizedNotes = (notes ?? '').trim().toUpperCase();
  if (!normalizedNotes.includes('ASSUMPTION')) {
    return false;
  }

  return !normalizedNotes.includes('RESOLVED') && !normalizedNotes.includes('CLOSED');
}

export function isExecutionBlockerSubsetRow(row: DependencyRegisterRow): boolean {
  const normalizedClass = (row.DependencyClass ?? '').trim().toUpperCase();
  const normalizedStatus = (row.Status ?? '').trim().toUpperCase();
  const normalizedDirection = (row.Direction ?? '').trim().toUpperCase();
  const normalizedType = (row.DependencyType ?? '').trim().toUpperCase();
  const normalizedTargetType = (row.TargetType ?? '').trim().toUpperCase();
  const normalizedSatisfaction = (row.SatisfactionStatus ?? 'TBD').trim().toUpperCase() || 'TBD';

  if (normalizedClass !== BLOCKER_SUBSET_DEPENDENCY_CLASS) {
    return false;
  }
  if (normalizedStatus !== 'ACTIVE') {
    return false;
  }
  if (normalizedDirection !== 'UPSTREAM') {
    return false;
  }
  if (!BLOCKING_DEPENDENCY_TYPES.has(normalizedType)) {
    return false;
  }
  if (normalizedTargetType !== BLOCKER_SUBSET_TARGET_TYPE) {
    return false;
  }
  if (NON_BLOCKING_SATISFACTION.has(normalizedSatisfaction)) {
    return false;
  }

  return !hasUnresolvedAssumptionGate(row.Notes);
}

export function summarizeDependencyRows(rows: DependencyRegisterRow[]): DependencyRowSummary {
  const bySatisfaction: Record<string, number> = {};
  let activeRows = 0;
  let activeUpstreamBlockerCandidates = 0;

  for (const row of rows) {
    const normalizedStatus = (row.Status ?? '').trim().toUpperCase();
    const normalizedSatisfaction = (row.SatisfactionStatus ?? 'TBD').trim().toUpperCase() || 'TBD';

    bySatisfaction[normalizedSatisfaction] = (bySatisfaction[normalizedSatisfaction] ?? 0) + 1;

    if (normalizedStatus === 'ACTIVE') {
      activeRows += 1;
    }

    if (isExecutionBlockerSubsetRow(row)) {
      activeUpstreamBlockerCandidates += 1;
    }
  }

  return {
    totalRows: rows.length,
    activeRows,
    activeUpstreamBlockerCandidates,
    bySatisfaction
  };
}

export async function fetchDeliverableStatus(
  projectRoot: string,
  deliverablePath: string
): Promise<DeliverableStatusSnapshot> {
  const query = new URLSearchParams({ projectRoot, deliverablePath });
  return requestWorkspaceApi<DeliverableStatusSnapshot>(
    `/api/working-root/deliverable/status?${query.toString()}`,
    { method: 'GET' },
    'Unable to read deliverable lifecycle status'
  );
}

export async function transitionDeliverableStatus(
  input: DeliverableStatusTransitionInput
): Promise<DeliverableStatusTransitionResult> {
  return requestWorkspaceApi<DeliverableStatusTransitionResult>(
    '/api/working-root/deliverable/status/transition',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(input)
    },
    'Unable to apply lifecycle transition'
  );
}

export async function fetchDeliverableDependencies(
  projectRoot: string,
  deliverablePath: string
): Promise<DeliverableDependenciesSnapshot> {
  const query = new URLSearchParams({ projectRoot, deliverablePath });
  return requestWorkspaceApi<DeliverableDependenciesSnapshot>(
    `/api/working-root/deliverable/dependencies?${query.toString()}`,
    { method: 'GET' },
    'Unable to read deliverable dependency register'
  );
}
