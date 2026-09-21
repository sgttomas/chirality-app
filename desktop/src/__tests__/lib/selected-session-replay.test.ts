import { describe, expect, it } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import type { SessionEventsReplay } from '../../lib/harness/client';
import {
  buildSelectedSessionReplayProjection,
  canContinueRecordedConversation,
  createSelectedSessionReplayLoader
} from '../../lib/woven-dialogue/selected-session-replay';

function session(sessionId: string): SessionRecord {
  return {
    sessionId,
    projectRoot: '/repo/project',
    persona: 'WORKING_ITEMS',
    mode: 'governed',
    createdAt: '2026-07-23T00:00:00.000Z',
    updatedAt: '2026-07-23T00:00:00.000Z'
  };
}

function messageEvent(sessionId: string, index: number): HarnessEvent {
  return {
    schemaVersion: 1,
    eventId: `event-${index}`,
    sessionId,
    turnId: 'turn-1',
    timestamp: `2026-07-23T00:00:${String(index).padStart(2, '0')}.000Z`,
    type: 'message.completed',
    data: {
      role: index % 2 === 0 ? 'assistant' : 'user',
      text: `message-${index}`
    }
  };
}

function replay(
  sessionId: string,
  events: HarnessEvent[],
  overrides: Partial<SessionEventsReplay> = {}
): SessionEventsReplay {
  return {
    events,
    malformedLineCount: 0,
    summary: {
      eventCount: events.length,
      malformedLineCount: 0,
      eventTypeCounts: {
        'message.completed': events.length
      },
      firstTimestamp: events[0]?.timestamp,
      lastTimestamp: events.at(-1)?.timestamp
    },
    session: session(sessionId),
    instructionHistory: [],
    instructionBases: [],
    ...overrides
  };
}

describe('selected-session replay projection', () => {
  it('bounds copied transcript data and exposes rendered versus available counts', () => {
    const events = Array.from({ length: 5 }, (_, index) =>
      messageEvent('selected', index + 1)
    );
    const projection = buildSelectedSessionReplayProjection(
      'selected',
      replay('selected', events),
      {
        observedAt: '2026-07-23T01:00:00.000Z',
        maxItems: 2,
        currency: 'CURRENT'
      }
    );

    expect(projection.disclosure).toBe('BOUNDED');
    expect(projection.bounded).toEqual({ rendered: 2, available: 5 });
    expect(projection.transcript.items.map(({ text }) => text)).toEqual([
      'message-4',
      'message-5'
    ]);
    expect(projection.sourceEventCount).toBe(5);
    expect(projection.renderedItemCount).toBe(2);
  });

  it('discloses malformed, stale, empty, and evidence-only snapshots honestly', () => {
    const malformed = buildSelectedSessionReplayProjection(
      'selected',
      replay('selected', [messageEvent('selected', 1)], {
        malformedLineCount: 2
      }),
      { observedAt: '2026-07-23T01:00:00.000Z' }
    );
    expect(malformed.disclosure).toBe('MALFORMED');
    expect(malformed.diagnostics.map(({ code }) => code)).toContain(
      'MALFORMED_REPLAY_RECORDS'
    );

    const stale = buildSelectedSessionReplayProjection(
      'selected',
      replay('selected', [messageEvent('selected', 1)]),
      {
        observedAt: '2026-07-23T01:00:00.000Z',
        stale: true,
        currency: 'CURRENT'
      }
    );
    expect(stale).toMatchObject({ disclosure: 'STALE', currency: 'STALE' });

    const empty = buildSelectedSessionReplayProjection(
      'selected',
      replay('selected', []),
      { observedAt: '2026-07-23T01:00:00.000Z' }
    );
    expect(empty.disclosure).toBe('EMPTY');

    const evidenceOnlyEvent: HarnessEvent = {
      ...messageEvent('selected', 1),
      eventId: 'coordination-only',
      type: 'coordination.notice',
      data: { noticeId: 'notice-1' }
    };
    const evidenceOnly = buildSelectedSessionReplayProjection(
      'selected',
      replay('selected', [evidenceOnlyEvent]),
      { observedAt: '2026-07-23T01:00:00.000Z' }
    );
    expect(evidenceOnly.disclosure).toBe('EVIDENCE_ONLY');
  });

  it('fails closed when replay metadata or events identify another session', () => {
    const projection = buildSelectedSessionReplayProjection(
      'selected',
      replay('other', [messageEvent('other', 1)]),
      {
        observedAt: '2026-07-23T01:00:00.000Z',
        currency: 'CURRENT'
      }
    );

    expect(projection).toMatchObject({
      selectedSessionId: 'selected',
      disclosure: 'CONFLICTING',
      currency: 'CONFLICTING'
    });
    expect(projection.diagnostics.map(({ code }) => code)).toEqual(
      expect.arrayContaining([
        'REPLAY_SESSION_ID_CONFLICT',
        'REPLAY_EVENT_SESSION_ID_CONFLICT',
        'REPLAY_FOREIGN_CONTENT_SUPPRESSED'
      ])
    );
    expect(projection.transcript.items).toEqual([]);
  });
});

describe('selected-session replay loader', () => {
  it('publishes loading and prevents a late prior response from replacing selection', async () => {
    const resolvers = new Map<string, (value: SessionEventsReplay) => void>();
    const loader = createSelectedSessionReplayLoader(
      (sessionId) =>
        new Promise<SessionEventsReplay>((resolve) => {
          resolvers.set(sessionId, resolve);
        })
    );
    const observed: string[] = [];
    loader.subscribe((state) => {
      observed.push(
        state.status === 'READY'
          ? `READY:${state.projection.selectedSessionId}`
          : state.status === 'IDLE'
            ? 'IDLE'
            : `${state.status}:${state.selectedSessionId}`
      );
    });

    const first = loader.load('first', {
      observedAt: '2026-07-23T01:00:00.000Z'
    });
    const second = loader.load('second', {
      observedAt: '2026-07-23T01:00:01.000Z'
    });

    resolvers.get('first')?.(replay('first', [messageEvent('first', 1)]));
    await expect(first).resolves.toMatchObject({ applied: false });
    expect(loader.getState()).toEqual({
      status: 'LOADING',
      selectedSessionId: 'second'
    });

    resolvers.get('second')?.(replay('second', [messageEvent('second', 1)]));
    await expect(second).resolves.toMatchObject({ applied: true });
    expect(loader.getState()).toMatchObject({
      status: 'READY',
      projection: { selectedSessionId: 'second' }
    });
    expect(observed).toEqual([
      'LOADING:first',
      'LOADING:second',
      'READY:second'
    ]);
  });

  it('reports only the current request as unavailable and cancellation returns to idle', async () => {
    const loader = createSelectedSessionReplayLoader(async () => {
      throw new Error('canonical replay unavailable');
    });

    await expect(
      loader.load('missing', {
        observedAt: '2026-07-23T01:00:00.000Z'
      })
    ).resolves.toMatchObject({ applied: true });
    expect(loader.getState()).toEqual({
      status: 'UNAVAILABLE',
      selectedSessionId: 'missing',
      message: 'canonical replay unavailable'
    });

    loader.cancel();
    expect(loader.getState()).toEqual({ status: 'IDLE' });
  });
});


it('opens only complete, current, same-project idle conversation snapshots directly', () => {
  const projection = buildSelectedSessionReplayProjection('selected', replay('selected', []), { observedAt: '2026-09-11' });
  projection.session!.continuation = { schemaVersion: 'chirality.session/v3', projectRoot: '/repo/project', roleId: 'HELP_HUMAN', mode: 'governed', interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: 'basis' };
  expect(canContinueRecordedConversation(projection, '/repo/project', false)).toBe(true);
  expect(canContinueRecordedConversation(projection, '/other', false)).toBe(false);
  expect(canContinueRecordedConversation(projection, '/repo/project', true)).toBe(false);
  for (const disclosure of ['CONFLICTING', 'STALE', 'MALFORMED', 'BOUNDED'] as const) {
    expect(canContinueRecordedConversation({ ...projection, disclosure }, '/repo/project', false)).toBe(false);
  }
});
