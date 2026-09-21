import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { act, create } from 'react-test-renderer';
import { describe, expect, it, vi } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { ActivityStrip, derivePrimaryTurnActivity } from '../../components/woven-dialogue/activity-shelf';

function event(type: HarnessEvent['type'], second: number, sessionId = 'primary', turnId: string | undefined = 'turn', data = {}): HarnessEvent {
  return { schemaVersion: 1, eventId: `${sessionId}-${type}-${second}`, sessionId, turnId, timestamp: `2026-09-07T00:00:${String(second).padStart(2, '0')}.000Z`, type, data };
}
const completed = () => [event('turn.started', 0), event('tool.started', 1, 'primary', 'turn', { toolUseId: 'tool-a' }), event('turn.completed', 3)];

describe('primary ActivityStrip projection', () => {
  it('offers an accessible public issue link without sending current activity or session details', () => {
    let tree!: ReturnType<typeof create>;
    act(() => { tree = create(<ActivityStrip primarySessionId="private-session" events={completed()} running onOpenDetails={() => {}} />); });
    const link = tree.root.findByType('a');
    expect(link.children.join('')).toBe('Report issue');
    expect(link.props.href).toBe('https://github.com/sgttomas/chirality-app/issues/new/choose');
    expect(link.props.target).toBe('_blank');
    expect(link.props.rel.split(' ')).toEqual(expect.arrayContaining(['noopener', 'noreferrer']));
    expect(link.props['aria-hidden']).not.toBe(true);
    expect(link.props.tabIndex).not.toBe(-1);
    act(() => tree.unmount());
  });

  it.each([42, {}, [], null, true, '   '])('renders unavailable for malformed turn identity %j without throwing', turnId => {
    const malformed = { ...event('turn.started', 5), turnId } as unknown as HarnessEvent;
    expect(derivePrimaryTurnActivity([...completed(), malformed], 'primary')).toBeNull();
    const html = renderToStaticMarkup(<ActivityStrip primarySessionId="primary" events={[...completed(), malformed]} running={false} onOpenDetails={() => {}} />);
    expect(html).not.toContain('Primary turn activity unavailable');
    expect(html).not.toContain('Turn duration unavailable');
    expect(html).not.toContain('Last turn:');
    expect(html).not.toContain('1 actions');
  });
  it.each([42, {}, null])('does not apply string operations to malformed primary identity %j', identity => {
    const html = renderToStaticMarkup(<ActivityStrip primarySessionId={identity as unknown as string} events={completed()} running={false} onOpenDetails={() => {}} />);
    expect(html).not.toContain('Primary turn activity unavailable');
  });
  it('ignores later other-session work even when turn and tool identities collide', () => {
    const primary = completed();
    const other = [event('turn.started', 4, 'other'), event('tool.started', 5, 'other', 'turn', { toolUseId: 'tool-a' }), event('turn.completed', 9, 'other')];
    expect(derivePrimaryTurnActivity([...primary, ...other], 'primary')).toEqual({ actions: 1, children: 0, elapsed: 3000 });
  });
  it('keeps child counts observed and scoped to the primary turn', () => {
    const events = [event('turn.started', 0), event('subagent.started', 1, 'primary', 'turn', { taskId: 'child' }), event('subagent.completed', 2, 'primary', 'turn', { taskId: 'child' }), event('subagent.started', 3, 'other', 'turn', { taskId: 'other-child' }), event('turn.completed', 4)];
    expect(derivePrimaryTurnActivity(events, 'primary')).toEqual({ actions: 0, children: 1, elapsed: 4000 });
  });
  it('counts only the newest primary turn using existing invocation derivation', () => {
    const events = [...completed(), event('turn.started', 4, 'primary', 'next'), event('tool.started', 5, 'primary', 'next', { toolUseId: 'tool-a' }), event('tool.completed', 6, 'primary', 'next', { toolUseId: 'tool-a' }), event('turn.completed', 8, 'primary', 'next')];
    expect(derivePrimaryTurnActivity(events, 'primary')).toEqual({ actions: 1, children: 0, elapsed: 4000 });
  });
  it.each([undefined, '', 'missing'])('cannot infer primary identity %s from buffered sessions', id => {
    expect(derivePrimaryTurnActivity(completed(), id)).toBeNull();
  });
  it.each([
    ['start truncated', [event('tool.started', 1), event('turn.completed', 3)]],
    ['latest start truncated', [...completed(), event('turn.completed', 9, 'primary', 'next')]],
    ['missing turn id', [{ ...event('turn.started', 4), turnId: undefined }]],
    ['later missing turn id', [...completed(), { ...event('turn.started', 4), turnId: undefined }]],
    ['bad start timestamp', [{ ...event('turn.started', 0), timestamp: 'invalid' }, event('turn.completed', 3)]],
    ['bad end timestamp', [event('turn.started', 0), { ...event('turn.completed', 3), timestamp: 'invalid' }]],
    ['end predates start', [event('turn.started', 4), event('turn.completed', 3)]],
    ['out of order boundaries', [event('turn.completed', 3), event('turn.started', 0)]],
    ['reused same-session turn id', [...completed(), event('turn.started', 4), event('turn.completed', 5)]],
    ['late previous end after newer start', [event('turn.started', 0), event('turn.started', 2, 'primary', 'next'), event('turn.completed', 3)]],
    ['conflicting ends', [...completed(), event('turn.failed', 4)]]
  ] as const)('keeps %s unknown', (_label, events) => {
    expect(derivePrimaryTurnActivity(events, 'primary')).toBeNull();
  });
  it('does not use an unrelated last event as an end and never ticks elapsed time', () => {
    const events = [event('turn.started', 0), event('tool.started', 1, 'primary', 'turn', { toolUseId: 'a' }), event('turn.completed', 9, 'other')];
    expect(derivePrimaryTurnActivity(events, 'primary')).toEqual({ actions: 1, children: 0, elapsed: undefined });
    const html = renderToStaticMarkup(<ActivityStrip primarySessionId="primary" events={events} running onOpenDetails={() => {}} />);
    expect(html).toContain('Working'); expect(html).toContain('1 actions · 0 children observed');
    expect(html).not.toContain('Turn duration unavailable'); expect(html).not.toContain('Last turn:');
  });
  it.each(['turn.completed', 'turn.failed', 'turn.interrupted'] as const)('uses only the matching %s observation for elapsed', end => {
    expect(derivePrimaryTurnActivity([event('turn.started', 1), event(end, 4)], 'primary')?.elapsed).toBe(3000);
  });
  it('does not label a completed previous turn current when streaming starts before events arrive', () => {
    const html = renderToStaticMarkup(<ActivityStrip primarySessionId="primary" events={completed()} running onOpenDetails={() => {}} />);
    expect(html).toContain('Working'); expect(html).not.toContain('Primary turn activity unavailable');
    expect(html).not.toContain('1 actions'); expect(html).not.toContain('Last turn:');
  });
  it('preserves reconnect content, live region and Details callback without changing primary identity', () => {
    const details = vi.fn(); let tree!: ReturnType<typeof create>;
    act(() => { tree = create(<ActivityStrip primarySessionId="primary" events={completed()} running={false} reconnectControl={<button aria-label="Reconnect">Reconnect</button>} onOpenDetails={details} />); });
    expect(tree.root.findByProps({ role: 'status' }).children.join('')).toContain('Last turn: 3.0 s');
    expect(tree.root.findByProps({ 'aria-label': 'Reconnect' })).toBeTruthy();
    act(() => tree.root.findAllByType('button').find(node => node.children.join('') === 'Details ›')!.props.onClick());
    expect(details).toHaveBeenCalledTimes(1);
    act(() => tree.unmount());
  });
});

describe('ActivityStrip turn phase', () => {
  it.each([
    ['preparing', 'Preparing'], ['working', 'Working'], ['waiting', 'Waiting for you'], ['reconnecting', 'Reconnecting'], ['stopping', 'Stopping']
  ] as const)('labels the %s phase from the chat panel rather than the streaming flag alone', (phase, label) => {
    const html = renderToStaticMarkup(<ActivityStrip primarySessionId="primary" events={[]} running phase={phase} onOpenDetails={() => {}} />);
    expect(html).toContain(`data-turn-phase="${phase}"`);
    expect(html).toContain(`<span role="status">${label}`);
  });
  it('falls back to Working and Idle from the streaming flag without a phase', () => {
    expect(renderToStaticMarkup(<ActivityStrip primarySessionId="primary" events={[]} running onOpenDetails={() => {}} />)).toContain('data-turn-phase="working"');
    expect(renderToStaticMarkup(<ActivityStrip primarySessionId="primary" events={[]} running={false} onOpenDetails={() => {}} />)).toContain('data-turn-phase="idle"');
  });
});
