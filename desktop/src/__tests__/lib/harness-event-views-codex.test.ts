import { describe, expect, it } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import {
  deriveCodexNotifications,
  derivePermissionRequests,
  deriveServerRequests,
  deriveToolActivity,
  readElicitationMessage,
  readUserInputQuestions,
  selectPendingPermissionRequests,
  selectPendingServerRequests
} from '../../lib/shell/harness-event-views';

let counter = 0;
function event(type: HarnessEvent['type'], data: Record<string, unknown>, timestamp = '2026-09-12T00:00:00.000Z'): HarnessEvent {
  counter += 1;
  return { schemaVersion: 1, eventId: `evt-${counter}`, sessionId: 's1', turnId: 't1', timestamp, type, data } as HarnessEvent;
}

const questions = [
  { id: 'colour', header: 'Colour', question: 'Which colour?', options: [{ label: 'Red', description: 'warm' }, { label: 'Blue' }], isOther: true },
  { id: 'token', header: 'Token', question: 'Paste the token', isSecret: true }
];

describe('Codex server requests (codex.request / codex.request.resolved)', () => {
  it('surfaces a user-input request as pending and clears it on resolution with the decision', () => {
    const events = [
      event('codex.request', { requestId: 'req-1', method: 'item/tool/requestUserInput', kind: 'userInput', request: { questions } }),
      event('codex.request', { requestId: 'req-2', method: 'mcpServer/elicitation/request', request: { message: 'Allow the server to read config?' } })
    ];
    const pending = selectPendingServerRequests(events, true);
    expect(pending.map((row) => [row.requestId, row.kind, row.status])).toEqual([['req-1', 'userInput', 'pending'], ['req-2', 'elicitation', 'pending']]);
    expect(readUserInputQuestions(pending[0].request)).toEqual([
      { id: 'colour', header: 'Colour', question: 'Which colour?', options: [{ label: 'Red', description: 'warm' }, { label: 'Blue', description: '' }], isOther: true, isSecret: false },
      { id: 'token', header: 'Token', question: 'Paste the token', options: [], isOther: false, isSecret: true }
    ]);
    expect(readElicitationMessage(pending[1].request)).toBe('Allow the server to read config?');

    const resolved = [...events, event('codex.request.resolved', { requestId: 'req-1', method: 'item/tool/requestUserInput', outcome: 'answered', decision: { colour: { answers: ['Red'] } }, decidedBy: 'user' })];
    expect(selectPendingServerRequests(resolved, true).map((row) => row.requestId)).toEqual(['req-2']);
    const all = deriveServerRequests(resolved);
    expect(all.find((row) => row.requestId === 'req-1')).toMatchObject({ status: 'answered', decidedBy: 'user', decision: { colour: { answers: ['Red'] } } });
    // A finished turn has nothing answerable left.
    expect(selectPendingServerRequests(resolved, false)).toEqual([]);
  });

  it('never surfaces a card for a resolution without its request, or for non-answerable kinds', () => {
    const events = [
      event('codex.request.resolved', { requestId: 'orphan', method: 'item/tool/requestUserInput', outcome: 'cancelled' }),
      event('codex.request', { requestId: 'tool-call', method: 'item/tool/call', request: {} })
    ];
    expect(deriveServerRequests(events).map((row) => row.requestId)).toEqual(['tool-call']);
    expect(selectPendingServerRequests(events, true)).toEqual([]);
  });
});

describe('Codex approvals mapped to permission cards', () => {
  it('keeps the request id and Codex method on the pending row and follows the resolution', () => {
    const events = [
      event('tool.permission', { behavior: 'ask', toolUseId: 'item-1', toolName: 'commandExecution', reason: 'Run: npm test', requestId: 'req-9', method: 'item/commandExecution/requestApproval', request: { command: ['npm', 'test'] } })
    ];
    const pending = selectPendingPermissionRequests(events, true);
    expect(pending).toHaveLength(1);
    expect(pending[0]).toMatchObject({ key: 'item-1', toolName: 'commandExecution', requestId: 'req-9', method: 'item/commandExecution/requestApproval', status: 'pending' });

    const allowed = [...events, event('tool.permission', { behavior: 'allow', toolUseId: 'item-1', toolName: 'commandExecution', decidedBy: 'user' })];
    expect(selectPendingPermissionRequests(allowed, true)).toEqual([]);
    expect(derivePermissionRequests(allowed)[0]).toMatchObject({ status: 'allowed', decidedBy: 'user', requestId: 'req-9' });
    expect(selectPendingPermissionRequests(events, false)).toEqual([]);
  });
});

describe('Codex notifications and tool rows', () => {
  it('turns a completed reasoning item into a Thinking line and keeps every other notification inspectable', () => {
    const events = [
      event('codex.notification', { method: 'item/completed', params: { item: { type: 'reasoning', id: 'r1', summary: [{ text: 'Weighing the options' }] } } }),
      event('codex.notification', { method: 'thread/tokenUsage/updated', params: { total: 120 } })
    ];
    const rows = deriveCodexNotifications(events);
    expect(rows.map((row) => [row.kind, row.method])).toEqual([['thinking', 'item/completed'], ['notification', 'thread/tokenUsage/updated']]);
    expect(rows[0].text).toBe('Weighing the options');
    expect(rows[1].params).toEqual({ total: 120 });
  });

  it('shows Codex item types as tool rows carrying the raw params and summary', () => {
    const events = [
      event('tool.started', { toolUseId: 'item-2', toolName: 'commandExecution', summary: 'npm test', codex: { command: ['npm', 'test'] } }),
      event('tool.completed', { toolUseId: 'item-2', toolName: 'commandExecution', summary: 'npm test (exit 0)' })
    ];
    const rows = deriveToolActivity(events);
    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({ toolName: 'commandExecution', status: 'completed', summary: 'npm test (exit 0)' });
  });
});
