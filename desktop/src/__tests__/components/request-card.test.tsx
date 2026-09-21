import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { CodexNotificationList } from '../../components/woven-dialogue/activity-shelf';
import { RequestCards } from '../../components/shell/request-card';
import type { CodexNotificationRow, ServerRequestRow } from '../../lib/shell/harness-event-views';

/**
 * Codex server requests other than approvals (`item/tool/requestUserInput`,
 * `mcpServer/elicitation/request`) are answered from a card that posts the
 * answer through the App session request route. The card is presentational:
 * it disappears when the follow-up `codex.request.resolved` event removes the
 * row from the derived list, and a failed post keeps it with the reason.
 */

function row(overrides: Partial<ServerRequestRow> = {}): ServerRequestRow {
  return {
    key: 'req-1', sessionId: 's1', requestId: 'req-1', method: 'item/tool/requestUserInput', kind: 'userInput', status: 'pending',
    request: { questions: [
      { id: 'colour', header: 'Colour', question: 'Which colour?', options: [{ label: 'Red', description: 'warm' }, { label: 'Blue' }], isOther: true },
      { id: 'reason', header: 'Reason', question: 'Why?' }
    ] },
    timestamp: '2026-09-12T00:00:00.000Z',
    ...overrides
  };
}

let tree: ReactTestRenderer | undefined;
afterEach(() => { if (tree) act(() => tree!.unmount()); tree = undefined; });

const button = (label: string) => tree!.root.findAllByType('button').find((node) => node.children.join('') === label)!;

describe('RequestCards', () => {
  it('renders nothing without pending requests and hides requests shown elsewhere', () => {
    expect(renderToStaticMarkup(<RequestCards sessionId="s1" requests={[]} />)).toBe('');
    expect(renderToStaticMarkup(<RequestCards sessionId="s1" requests={[row()]} suppressedRequestIds={new Set(['req-1'])} />)).toBe('');
  });

  it('answers every user-input question by id and sends nothing until all are answered', async () => {
    const answer = vi.fn(async () => ({ sent: true as const }));
    await act(async () => { tree = create(<RequestCards sessionId="s1" requests={[row()]} answer={answer} />); });
    expect(button('Send answers').props.disabled).toBe(true);
    const radios = tree!.root.findAll((node) => node.type === 'input' && node.props.type === 'radio');
    expect(radios.map((node) => node.props.value)).toEqual(['Red', 'Blue']);
    await act(async () => radios[0].props.onChange());
    expect(button('Send answers').props.disabled).toBe(true);
    const free = tree!.root.findAll((node) => node.type === 'input' && node.props.type === 'text');
    // The "Other" field for the first question plus the free-text second question.
    expect(free).toHaveLength(2);
    await act(async () => free[1].props.onChange({ target: { value: 'because' } }));
    expect(button('Send answers').props.disabled).toBe(false);
    await act(async () => tree!.root.findByType('form').props.onSubmit({ preventDefault: vi.fn() }));
    expect(answer).toHaveBeenCalledWith({ sessionId: 's1', requestId: 'req-1', answer: { kind: 'userInput', answers: { colour: { answers: ['Red'] }, reason: { answers: ['because'] } } } });
    expect(button('Sending answers...').props.disabled).toBe(true);
  });

  it('accepts or declines an elicitation and keeps the card with the reason when the post fails', async () => {
    const answer = vi.fn().mockRejectedValueOnce(new Error('Runtime refused the answer')).mockResolvedValue({ sent: true });
    const elicitation = row({ key: 'req-2', requestId: 'req-2', method: 'mcpServer/elicitation/request', kind: 'elicitation', request: { message: 'Allow config read?' } });
    await act(async () => { tree = create(<RequestCards sessionId="s1" requests={[elicitation]} answer={answer} />); });
    expect(JSON.stringify(tree!.toJSON())).toContain('Allow config read?');
    await act(async () => button('Decline').props.onClick());
    expect(answer).toHaveBeenLastCalledWith({ sessionId: 's1', requestId: 'req-2', answer: { kind: 'elicitation', action: 'decline' } });
    expect(JSON.stringify(tree!.toJSON())).toContain('Runtime refused the answer');
    expect(button('Accept').props.disabled).toBe(false);
    await act(async () => button('Accept').props.onClick());
    expect(answer).toHaveBeenLastCalledWith({ sessionId: 's1', requestId: 'req-2', answer: { kind: 'elicitation', action: 'accept' } });
    expect(JSON.stringify(tree!.toJSON())).not.toContain('Runtime refused the answer');
    // Resolution arrives as an event: the row leaves the list and the card with it.
    await act(async () => tree!.update(<RequestCards sessionId="s1" requests={[]} answer={answer} />));
    expect(tree!.toJSON()).toBeNull();
  });
});

describe('CodexNotificationList', () => {
  it('renders Thinking lines as text and other notifications as method plus collapsed JSON', () => {
    const rows: CodexNotificationRow[] = [
      { key: 'n1', sessionId: 's1', method: 'item/completed', kind: 'thinking', text: 'Weighing the options', params: { item: { type: 'reasoning' } }, timestamp: '2026-09-12T00:00:00.000Z' },
      { key: 'n2', sessionId: 's1', method: 'thread/tokenUsage/updated', kind: 'notification', params: { total: 120 }, timestamp: '2026-09-12T00:00:01.000Z' }
    ];
    const html = renderToStaticMarkup(<CodexNotificationList rows={rows} emptyMessage="No Codex notifications yet." />);
    expect(html).toContain('Thinking');
    expect(html).toContain('Weighing the options');
    expect(html).toContain('thread/tokenUsage/updated');
    expect(html).toContain('<details');
    expect(html).toContain('&quot;total&quot;: 120');
    expect(renderToStaticMarkup(<CodexNotificationList rows={[]} emptyMessage="No Codex notifications yet." />)).toContain('No Codex notifications yet.');
  });
});

it.each([
  ['item/commandExecution/requestApproval', ['accept', 'acceptForSession', 'decline'], true],
  ['item/fileChange/requestApproval', ['accept', 'acceptForSession', 'decline'], true],
  ['item/commandExecution/requestApproval', ['accept', 'decline'], false],
  ['item/fileChange/requestApproval', undefined, false],
  ['item/permissions/requestApproval', undefined, true],
  ['execCommandApproval', undefined, false],
] as const)('offers session approval only for supported native scope: %s %j', async (method, availableDecisions, offered) => {
  const answer = vi.fn(async () => ({ sent: true as const }));
  const request = row({ method, kind: 'approval', request: { reason: 'Read the requested child folder', permissions: { fileSystem: { read: ['/project/child'] } }, availableDecisions } });
  await act(async () => { tree = create(<RequestCards sessionId="s1" requests={[request]} answer={answer} />); });
  expect(Boolean(button('Allow for this session'))).toBe(offered);
  expect(button('Approve').props.disabled).toBe(false); expect(button('Deny').props.disabled).toBe(false);
  if (offered) {
    await act(async () => button('Allow for this session').props.onClick());
    expect(answer).toHaveBeenCalledWith({ sessionId: 's1', requestId: 'req-1', answer: { kind: 'approval', verdict: 'allowForSession' } });
    expect(request.request).toMatchObject({ permissions: { fileSystem: { read: ['/project/child'] } } });
  }
});
