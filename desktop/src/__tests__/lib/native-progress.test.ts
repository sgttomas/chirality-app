import { describe, it, expect } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { deriveNativeProgress } from '../../lib/shell/native-progress';
import { deriveSubagentActivity } from '../../lib/shell/harness-event-views';
import { deriveTurnActivityFromEvents } from '../../lib/shell/turn-activity';
const e = (id: string, method: string, params: Record<string, unknown>): HarnessEvent => ({ schemaVersion: 1, eventId: id, sessionId: 'session', turnId: 'runtime-parent', timestamp: '2026-09-12T00:00:00Z', type: 'codex.notification', data: { method, params, codex: { providerThreadId: 'parent', providerTurnId: 'parent-turn' } } });
const scope = { threadId: 'parent', turnId: 'native-turn' };
describe('native progress replay', () => {
  it('replaces the checklist, keeps empty revisions and isolates actual child turn identity', () => {
    const events = [e('1', 'turn/plan/updated', { ...scope, plan: [{ step: 'Read', status: 'pending' }] }),
      e('2', 'turn/plan/updated', { ...scope, plan: [{ step: 'Read', status: 'completed' }, { step: 'Write', status: 'inProgress' }] }),
      e('3', 'turn/plan/updated', { threadId: 'child', turnId: 'child-turn', plan: [] })];
    expect(deriveNativeProgress(events).checklists).toMatchObject([{ steps: [{ status: 'completed' }, { status: 'inProgress' }] }, { steps: [] }]);
    expect(deriveTurnActivityFromEvents(events)).toEqual(deriveTurnActivityFromEvents(JSON.parse(JSON.stringify(events))));
  });
  it('reconciles indexed summaries and excludes hidden reasoning content', () => {
    const events = [e('1', 'item/reasoning/summaryTextDelta', { ...scope, itemId: 'r', summaryIndex: 0, delta: 'Checking' }),
      e('2', 'item/reasoning/summaryTextDelta', { ...scope, itemId: 'r', summaryIndex: 0, delta: ' the file' }),
      e('3', 'item/completed', { ...scope, item: { id: 'r', type: 'reasoning', summary: ['Checked the file'], content: ['Never display this'] } })];
    expect(deriveNativeProgress(events).summaries.map(row => row.text)).toEqual(['Checked the file']);
    expect(JSON.stringify(deriveTurnActivityFromEvents(events))).not.toContain('Never display this');
  });
  it('does not mistake completed spawn calls or the parent completion for child completion', () => {
    const events = [e('1', 'item/completed', { ...scope, item: { id: 'spawn', type: 'collabAgentToolCall', status: 'completed', receiverThreadIds: ['child-a', 'child-b'], prompt: 'Review the patch', agentsStates: { 'child-a': { status: 'running' }, 'child-b': { status: 'pendingInit' } } } }),
      e('2', 'turn/completed', { threadId: 'parent', turn: { id: 'native-turn', status: 'completed' } }),
      e('3', 'item/completed', { threadId: 'child-a', turnId: 'child-turn', item: { type: 'agentMessage', id: 'answer', text: 'Found one issue.' } }),
      e('4', 'turn/completed', { threadId: 'child-a', turn: { id: 'child-turn', status: 'failed' } })];
    expect(deriveSubagentActivity(events)).toMatchObject([{ status: 'failed', description: 'Review the patch', summary: 'Found one issue.' }, { status: 'waiting' }]);
  });
});
it('records the explicit child observation boundary without declaring the task completed', () => {
  const events = [e('spawn', 'item/completed', { ...scope, item: { type: 'collabAgentToolCall', receiverThreadIds: ['child'], agentsStates: { child: { status: 'running' } } } }),
    e('limit', 'chirality/nativeChildren/observationEnded', { ...scope, agentThreadIds: ['child'], reason: 'parentTurnEnded', message: 'Later child activity is not recorded here.' })];
  expect(deriveSubagentActivity(events)[0]).toMatchObject({ status: 'running', observationEnded: 'Later child activity is not recorded here.' });
  expect(deriveTurnActivityFromEvents(events).running).toBe(0);
});

const activity = (eventId: string, id: string, kind: string, phase = 'completed', child = 'child'): HarnessEvent => e(eventId, `item/${phase}`, { ...scope, item: { type: 'subAgentActivity', id, kind, agentThreadId: child, agentPath: `/root/${child}` } });
it('merges stock v2 raw and retained lifecycle pairs by actual child identity', () => {
  const start = activity('a1', 'a', 'started', 'started');
  const retained = { ...start, eventId: 'old', type: 'subagent.progress', data: { taskId: 'a', agentThreadId: 'child', kind: 'started', agentPath: '/root/child', phase: 'completed', codex: start.data } } as HarnessEvent;
  const events = [start, activity('a2', 'a', 'started'), retained,
    e('wait', 'item/completed', { ...scope, item: { type: 'collabAgentToolCall', receiverThreadIds: [], agentsStates: {}, status: 'completed' } }),
    activity('b1', 'b', 'completed', 'started'), activity('b2', 'b', 'completed')];
  const rows = deriveSubagentActivity(events);
  expect(rows).toHaveLength(1);
  expect(rows[0]).toMatchObject({ key: 'native:session:child', nativeThreadId: 'child', agentPath: '/root/child', status: 'completed', eventCount: 2 });
  expect(rows[0].summary).toBeUndefined(); expect(rows[0].agentRole).toBeUndefined();
  expect(deriveSubagentActivity(JSON.parse(JSON.stringify(events)))).toEqual(rows);
});
it('keeps interaction unknown, interruption explicit and missing completion nonterminal', () => {
  const events = [activity('a', 'a', 'interacted'), activity('b', 'b', 'started', 'completed', 'second'),
    e('end', 'chirality/nativeChildren/observationEnded', { agentThreadIds: ['second'] })];
  expect(deriveSubagentActivity(events)).toMatchObject([{ status: 'unknown' }, { status: 'running', observationEnded: expect.any(String) }]);
  expect(deriveSubagentActivity([...events, activity('c', 'c', 'interrupted')])[0].status).toBe('interrupted');
});
it('merges actual child thread metadata and messages without inventing a Runtime session', () => {
  const rows = deriveSubagentActivity([activity('a', 'a', 'started'),
    e('thread', 'thread/started', { thread: { id: 'child', parentThreadId: 'parent', agentNickname: 'Checker', agentRole: 'reviewer' } }),
    e('msg', 'item/completed', { threadId: 'child', item: { type: 'agentMessage', text: 'Observed result' } })]);
  expect(rows).toHaveLength(1);
  expect(rows[0]).toMatchObject({ agentName: 'Checker', agentRole: 'reviewer', parentThreadId: 'parent', summary: 'Observed result', status: 'running' });
});

it('normalizes retained-only top-level and nested stock activity without a legacy row', () => {
  const raw = activity('raw', 'a', 'started');
  const nested = { ...raw, type: 'subagent.progress', data: { taskId: 'a', codex: raw.data } } as HarnessEvent;
  const top = { ...raw, eventId: 'top', type: 'subagent.progress', data: { taskId: 'b', agentThreadId: 'child', agentPath: '/root/child', kind: 'completed', phase: 'started' } } as HarnessEvent;
  expect(deriveSubagentActivity([nested, top])).toMatchObject([{ key: 'native:session:child', status: 'completed', agentPath: '/root/child', eventCount: 2 }]);
  expect(deriveSubagentActivity([nested, top])).toHaveLength(1);
});
