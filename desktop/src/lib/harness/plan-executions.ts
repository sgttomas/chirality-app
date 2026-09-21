import type { TurnOutcome } from '../shell/turn-phase';

/**
 * Local record of plan executions: which plan revision was sent for
 * execution, in which turn, and how that turn ended. The Runtime records the
 * plan revisions and the turns; it has no notion of "this turn executed
 * revision N", so the App keeps that link per session in local storage,
 * alongside the chat drafts. Records are append-only per attempt; a revision
 * that was never sent has no record and reads as "Not executed".
 */
export const PLAN_EXECUTION_STORAGE_PREFIX = 'chirality.planExecutions.v1';
const MAX_RECORDS = 200;

export type PlanExecutionStatus = 'running' | TurnOutcome;

export type PlanExecutionRecord = {
  revision: number;
  /** 1-based attempt number for that revision. */
  attempt: number;
  startedAt: string;
  status: PlanExecutionStatus;
  /** Identity allocated before submission; absent only on legacy local records. */
  turnId?: string;
  endedAt?: string;
};

export function buildPlanExecutionStorageKey(sessionId: string): string {
  return `${PLAN_EXECUTION_STORAGE_PREFIX}:${sessionId}`;
}

const STATUSES: ReadonlySet<string> = new Set(['running', 'completed', 'interrupted', 'failed', 'unknown']);

export function sanitizePlanExecutionRecords(value: unknown): PlanExecutionRecord[] {
  if (!Array.isArray(value)) return [];
  const records: PlanExecutionRecord[] = [];
  for (const entry of value) {
    if (!entry || typeof entry !== 'object') continue;
    const record = entry as Record<string, unknown>;
    if (typeof record.revision !== 'number' || !Number.isInteger(record.revision) || record.revision < 1) continue;
    if (typeof record.attempt !== 'number' || !Number.isInteger(record.attempt) || record.attempt < 1) continue;
    if (typeof record.startedAt !== 'string' || !record.startedAt) continue;
    if (typeof record.status !== 'string' || !STATUSES.has(record.status)) continue;
    records.push({
      revision: record.revision, attempt: record.attempt, startedAt: record.startedAt, status: record.status as PlanExecutionStatus,
      ...(typeof record.turnId === 'string' && record.turnId ? { turnId: record.turnId } : {}),
      ...(typeof record.endedAt === 'string' && record.endedAt ? { endedAt: record.endedAt } : {})
    });
    if (records.length >= MAX_RECORDS) break;
  }
  return records;
}

export function readPlanExecutionRecords(storage: Pick<Storage, 'getItem'>, sessionId: string): PlanExecutionRecord[] {
  try {
    const raw = storage.getItem(buildPlanExecutionStorageKey(sessionId));
    return raw ? sanitizePlanExecutionRecords(JSON.parse(raw)) : [];
  } catch {
    return [];
  }
}

export function writePlanExecutionRecords(storage: Pick<Storage, 'setItem' | 'removeItem'>, sessionId: string, records: readonly PlanExecutionRecord[]): void {
  try {
    if (records.length === 0) storage.removeItem(buildPlanExecutionStorageKey(sessionId));
    else storage.setItem(buildPlanExecutionStorageKey(sessionId), JSON.stringify(records.slice(-MAX_RECORDS)));
  } catch {
    // Execution records are a local convenience; the Runtime log stays authoritative.
  }
}

/** Start attempt N for a revision: one more than the attempts already recorded for it. */
export function beginPlanExecution(records: readonly PlanExecutionRecord[], revision: number, startedAt: string, turnId?: string): PlanExecutionRecord[] {
  const attempt = records.filter(record => record.revision === revision).length + 1;
  return [...records, { revision, attempt, startedAt, status: 'running', ...(turnId ? { turnId } : {}) }];
}

/** The most recent running record (at most one turn runs per session). */
export function runningPlanExecution(records: readonly PlanExecutionRecord[]): PlanExecutionRecord | undefined {
  return [...records].reverse().find(record => record.status === 'running');
}

export function settlePlanExecution(records: readonly PlanExecutionRecord[], target: { revision: number; attempt: number }, patch: { status: TurnOutcome; endedAt: string; turnId?: string }): PlanExecutionRecord[] {
  return records.map(record => record.revision === target.revision && record.attempt === target.attempt
    ? { ...record, status: patch.status, endedAt: patch.endedAt, ...(patch.turnId ? { turnId: patch.turnId } : {}) }
    : record);
}

export function attachPlanExecutionTurn(records: readonly PlanExecutionRecord[], target: { revision: number; attempt: number }, turnId: string): PlanExecutionRecord[] {
  return records.map(record => record.revision === target.revision && record.attempt === target.attempt && record.turnId !== turnId ? { ...record, turnId } : record);
}

/** Per-revision summary for the Plan tab: the latest attempt decides the label. */
export function latestPlanExecution(records: readonly PlanExecutionRecord[], revision: number): PlanExecutionRecord | undefined {
  return [...records].reverse().find(record => record.revision === revision);
}

/**
 * The marker line the composer carries when a plan revision is prepared for
 * execution. A submitted message still carrying it is that revision's
 * execution attempt; an edited message without it is an ordinary turn.
 */
export function planExecutionMarker(revision: number): string {
  return `--- plan revision ${revision} ---`;
}

export function detectPlanExecution(text: string, prepared: { revision: number } | null): number | null {
  if (!prepared) return null;
  return text.includes(planExecutionMarker(prepared.revision)) ? prepared.revision : null;
}
