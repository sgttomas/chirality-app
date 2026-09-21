import { describe, expect, it } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import type { TranscriptItem } from '@chirality/runtime-contracts/transcript-replay';
import { deriveTurnActivityFromEvents, deriveTurnActivityFromTranscript, summarizeTurnActivity } from '../../lib/shell/turn-activity';

const event = (type: HarnessEvent['type'], data: Record<string, unknown>, turnId: string | undefined, at: number, eventId = `${type}-${at}`): HarnessEvent =>
  ({ schemaVersion: 1, eventId, sessionId: 's1', ...(turnId ? { turnId } : {}), timestamp: new Date(1_700_000_000_000 + at).toISOString(), type, data });

describe('deriveTurnActivityFromEvents', () => {
  it('scopes rows to the named turn, keeps observation order, and reports running and failed counts', () => {
    const events = [
      event('tool.started', { toolUseId: 'a', toolName: 'commandExecution', summary: 'npm test\nsecond line' }, 't1', 10),
      event('codex.notification', { method: 'item/completed', params: { item: { type: 'reasoning', summary: [{ type: 'summary_text', text: 'Considering the test layout' }] } } }, 't1', 20),
      event('tool.completed', { toolUseId: 'a', toolName: 'commandExecution' }, 't1', 30),
      event('tool.started', { toolUseId: 'b', toolName: 'fileChange', summary: 'src/x.ts' }, 't1', 40),
      event('tool.failed', { toolUseId: 'b', toolName: 'fileChange' }, 't1', 50),
      event('tool.started', { toolUseId: 'c', toolName: 'commandExecution' }, 't1', 60),
      event('tool.started', { toolUseId: 'z', toolName: 'commandExecution', summary: 'other turn' }, 't2', 70)
    ];
    const activity = deriveTurnActivityFromEvents(events, 't1');
    expect(activity.items.map(item => [item.kind, item.status, item.title, item.detail])).toEqual([
      ['tool', 'completed', 'Command finished', 'npm test'],
      ['reasoning', 'completed', 'Reasoning summary', 'Considering the test layout'],
      ['tool', 'failed', 'File change failed or declined', 'src/x.ts'],
      ['tool', 'running', 'Running command', undefined]
    ]);
    expect(activity.running).toBe(1);
    expect(activity.failed).toBe(1);
    expect(summarizeTurnActivity(activity, true)).toBe('Running command · 4 actions · 1 failed');
    expect(summarizeTurnActivity(activity, false)).toBe('Turn details · 4 actions · 1 failed');
    // Unscoped: the whole buffer is the turn (the panel clears it at send).
    expect(deriveTurnActivityFromEvents(events).items).toHaveLength(5);
    expect(deriveTurnActivityFromEvents([], 't1').items).toEqual([]);
    expect(summarizeTurnActivity(deriveTurnActivityFromEvents([]), true)).toBe('Working');
  });

  it('ignores reasoning items without text rather than inventing a summary', () => {
    const events = [event('codex.notification', { method: 'item/completed', params: { item: { type: 'reasoning', summary: [] } } }, 't1', 1)];
    expect(deriveTurnActivityFromEvents(events, 't1').items).toEqual([]);
  });
});

describe('deriveTurnActivityFromTranscript', () => {
  it('maps recorded tool items of one turn to the same fixed sentences', () => {
    const items: TranscriptItem[] = [
      { key: 'k1', kind: 'tool', status: 'completed', title: 'commandExecution', timestamp: '2026-09-12T00:00:01.000Z', eventId: 'e1', eventType: 'tool.completed', turnId: 't1', toolName: 'commandExecution', summary: 'ls' },
      { key: 'k2', kind: 'tool', status: 'failed', title: 'Read failed', timestamp: '2026-09-12T00:00:02.000Z', eventId: 'e2', eventType: 'tool.failed', turnId: 't1', toolName: 'read_file' },
      { key: 'k3', kind: 'tool', status: 'completed', title: 'x', timestamp: '2026-09-12T00:00:03.000Z', eventId: 'e3', eventType: 'tool.completed', turnId: 't2', toolName: 'commandExecution' },
      { key: 'k4', kind: 'message', role: 'assistant', status: 'completed', title: 'reply', timestamp: '2026-09-12T00:00:04.000Z', eventId: 'e4', eventType: 'message.completed', turnId: 't1', text: 'hi' }
    ];
    const activity = deriveTurnActivityFromTranscript(items, 't1');
    expect(activity.items.map(item => [item.status, item.title, item.detail])).toEqual([
      ['completed', 'Command finished', 'ls'],
      ['failed', 'Failed to read file', 'Read failed']
    ]);
    expect(deriveTurnActivityFromTranscript(items, undefined).items).toEqual([]);
  });
});

it('keeps raw shell details out of compact progress and in expanded activity', () => {
  const activity = deriveTurnActivityFromEvents([{ schemaVersion: 1, eventId: 'shell', sessionId: 's', turnId: 't', timestamp: '2026-09-12T00:00:00Z', type: 'tool.started', data: { toolUseId: 'shell', toolName: 'commandExecution', summary: '/bin/zsh -lc cat /private/full/path' } }]);
  expect(summarizeTurnActivity(activity, true)).toBe('Running command · 1 action');
  expect(activity.items[0].detail).toContain('/bin/zsh -lc cat /private/full/path');
});
