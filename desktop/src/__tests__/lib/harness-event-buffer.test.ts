import { describe, expect, it } from 'vitest';
import type { HarnessEvent, HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import { boundHarnessEventBuffer } from '../../lib/shell/harness-event-buffer';
import { deriveToolActivity } from '../../lib/shell/harness-event-views';

let counter = 0;
function event(type: HarnessEventType, data: Record<string, unknown>): HarnessEvent {
  counter += 1;
  return {
    schemaVersion: 1,
    eventId: `evt_${counter}`,
    sessionId: 'sess_test',
    timestamp: `2026-06-18T00:00:0${counter % 10}.000Z`,
    type,
    data
  };
}

describe('boundHarnessEventBuffer', () => {
  it('returns a copy unchanged when under the bound', () => {
    const events = [event('tool.started', { toolUseId: 't1', toolName: 'Read' })];
    const bounded = boundHarnessEventBuffer(events, 10);
    expect(bounded).toEqual(events);
    expect(bounded).not.toBe(events);
  });

  it('drops the oldest events when over the bound, preserving order', () => {
    const events = Array.from({ length: 5 }, (_, index) =>
      event('tool.started', { toolUseId: `t${index}`, toolName: 'Read' })
    );
    const bounded = boundHarnessEventBuffer(events, 3);
    expect(bounded).toHaveLength(3);
    expect(bounded.map((entry) => entry.data.toolUseId)).toEqual(['t2', 't3', 't4']);
  });

  it('handles empty input', () => {
    expect(boundHarnessEventBuffer([], 10)).toEqual([]);
  });
});

describe('hydrate/derive parity (live == replay, D-APP-22)', () => {
  it('produces identical buffers and derived rows for live-append vs hydrate', () => {
    const events = [
      event('tool.queued', { toolUseId: 't1', toolName: 'Read', source: 'model' }),
      event('tool.started', { toolUseId: 't1', toolName: 'Read', source: 'adapter' }),
      event('tool.completed', { toolUseId: 't1', toolName: 'Read' }),
      event('tool.queued', { toolUseId: 't2', toolName: 'Bash', source: 'model' }),
      event('tool.failed', { toolUseId: 't2', toolName: 'Bash' })
    ];

    // Live: append one at a time through the same bound helper the provider uses.
    let live: HarnessEvent[] = [];
    for (const next of events) {
      live = boundHarnessEventBuffer([...live, next], 2000);
    }
    // Replay/hydrate: seed the whole array at once.
    const replay = boundHarnessEventBuffer(events, 2000);

    expect(replay).toEqual(live);
    expect(deriveToolActivity(replay)).toEqual(deriveToolActivity(live));
    expect(deriveToolActivity(replay).map((row) => row.key)).toEqual(['t1', 't2']);
  });

  it('stays identical even when both paths truncate to the bound', () => {
    const events = Array.from({ length: 10 }, (_, index) =>
      event('tool.completed', { toolUseId: `t${index}`, toolName: 'Read' })
    );

    let live: HarnessEvent[] = [];
    for (const next of events) {
      live = boundHarnessEventBuffer([...live, next], 4);
    }
    const replay = boundHarnessEventBuffer(events, 4);

    expect(replay).toEqual(live);
    expect(deriveToolActivity(replay)).toEqual(deriveToolActivity(live));
  });
});
