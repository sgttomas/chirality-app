import { describe, expect, it } from 'vitest';
import {
  attachPlanExecutionTurn, beginPlanExecution, buildPlanExecutionStorageKey, detectPlanExecution, latestPlanExecution,
  planExecutionMarker, readPlanExecutionRecords, runningPlanExecution, sanitizePlanExecutionRecords, settlePlanExecution, writePlanExecutionRecords
} from '../../lib/harness/plan-executions';

describe('plan execution records', () => {
  it('numbers attempts per revision, settles the running record, and reports the latest attempt per revision', () => {
    let records = beginPlanExecution([], 1, '2026-09-12T10:00:00Z');
    expect(records).toEqual([{ revision: 1, attempt: 1, startedAt: '2026-09-12T10:00:00Z', status: 'running' }]);
    expect(runningPlanExecution(records)).toMatchObject({ revision: 1, attempt: 1 });
    records = attachPlanExecutionTurn(records, { revision: 1, attempt: 1 }, 'turn-1');
    records = settlePlanExecution(records, { revision: 1, attempt: 1 }, { status: 'interrupted', endedAt: '2026-09-12T10:01:00Z' });
    expect(runningPlanExecution(records)).toBeUndefined();
    records = beginPlanExecution(records, 1, '2026-09-12T10:02:00Z');
    expect(records.at(-1)).toMatchObject({ revision: 1, attempt: 2, status: 'running' });
    records = settlePlanExecution(records, { revision: 1, attempt: 2 }, { status: 'completed', endedAt: '2026-09-12T10:03:00Z', turnId: 'turn-2' });
    expect(latestPlanExecution(records, 1)).toMatchObject({ attempt: 2, status: 'completed', turnId: 'turn-2' });
    expect(latestPlanExecution(records, 2)).toBeUndefined();
  });

  it('recognises an execution only while the prepared marker survives in the sent text', () => {
    expect(detectPlanExecution(`Execute the plan.\n\n${planExecutionMarker(3)}\nsteps`, { revision: 3 })).toBe(3);
    expect(detectPlanExecution('Actually, something else', { revision: 3 })).toBeNull();
    expect(detectPlanExecution(planExecutionMarker(3), null)).toBeNull();
  });

  it('reads, sanitises, and writes records per session and removes an empty list', () => {
    const store = new Map<string, string>();
    const storage = { getItem: (key: string) => store.get(key) ?? null, setItem: (key: string, value: string) => { store.set(key, value); }, removeItem: (key: string) => { store.delete(key); } };
    writePlanExecutionRecords(storage, 'sess', [{ revision: 2, attempt: 1, startedAt: 's', status: 'unknown' }]);
    expect(store.has(buildPlanExecutionStorageKey('sess'))).toBe(true);
    expect(readPlanExecutionRecords(storage, 'sess')).toEqual([{ revision: 2, attempt: 1, startedAt: 's', status: 'unknown' }]);
    expect(sanitizePlanExecutionRecords([{ revision: 0, attempt: 1, startedAt: 's', status: 'running' }, { revision: 1, attempt: 1, startedAt: 's', status: 'done' }, 'x', { revision: 1, attempt: 1, startedAt: 's', status: 'failed', turnId: 't', endedAt: 'e' }]))
      .toEqual([{ revision: 1, attempt: 1, startedAt: 's', status: 'failed', turnId: 't', endedAt: 'e' }]);
    writePlanExecutionRecords(storage, 'sess', []);
    expect(store.has(buildPlanExecutionStorageKey('sess'))).toBe(false);
    expect(readPlanExecutionRecords({ getItem: () => '{not json' }, 'sess')).toEqual([]);
  });
});

it('stores the preallocated identity in the initial running attempt before any observed result', () => {
  const store = new Map<string, string>();
  const storage = { getItem: (key: string) => store.get(key) ?? null, setItem: (key: string, value: string) => { store.set(key, value); }, removeItem: (key: string) => { store.delete(key); } };
  const started = beginPlanExecution([], 2, '2026-09-12T00:00:00Z', 'submitted-turn');
  writePlanExecutionRecords(storage, 'session', started);
  expect(readPlanExecutionRecords(storage, 'session')).toEqual([{ revision: 2, attempt: 1, startedAt: '2026-09-12T00:00:00Z', status: 'running', turnId: 'submitted-turn' }]);
});
