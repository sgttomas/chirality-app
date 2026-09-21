import type { SessionRecord } from '@chirality/runtime-contracts/types';
import {
  deriveTranscriptView,
  type TranscriptView
} from '@chirality/runtime-contracts/transcript-replay';
import {
  replaySessionEvents,
  type SessionEventsReplay
} from '../harness/client';
import type {
  ProjectionCurrency,
  ProjectionDiagnostic,
  ReplayDisclosure,
  SelectedSessionReplayProjection,
  SelectedSessionReplayState
} from './contracts';
import { projectOperatorSession } from './operator-projection';

export const DEFAULT_REPLAY_ITEM_LIMIT = 500;

export type SelectedSessionReplayOptions = {
  observedAt: string;
  maxItems?: number;
  currency?: ProjectionCurrency;
  stale?: boolean;
  availableSessionIds?: ReadonlySet<string>;
};

export type ReplayFetcher = (
  sessionId: string,
  signal: AbortSignal
) => Promise<SessionEventsReplay>;

export type ReplayLoadResult = {
  applied: boolean;
  state: SelectedSessionReplayState;
};

export type SelectedSessionReplayLoader = {
  getState(): SelectedSessionReplayState;
  subscribe(listener: (state: SelectedSessionReplayState) => void): () => void;
  load(sessionId: string, options: SelectedSessionReplayOptions): Promise<ReplayLoadResult>;
  cancel(): void;
  dispose(): void;
};

export function canContinueRecordedConversation(projection: SelectedSessionReplayProjection, projectRoot: string | null, liveTurnActive: boolean): boolean {
  return !liveTurnActive && Boolean(projection.session?.continuation) &&
    projection.session?.continuation?.projectRoot === projectRoot &&
    !['CONFLICTING', 'STALE', 'MALFORMED', 'BOUNDED'].includes(projection.disclosure);
}

function positiveLimit(value: number | undefined): number {
  if (value === undefined) {
    return DEFAULT_REPLAY_ITEM_LIMIT;
  }
  if (!Number.isFinite(value) || value < 1) {
    throw new Error('Replay item limit must be a positive finite number');
  }
  return Math.floor(value);
}

function boundedTranscript(transcript: TranscriptView, limit: number): TranscriptView {
  if (transcript.items.length <= limit) {
    return {
      ...transcript,
      items: [...transcript.items]
    };
  }

  const items = transcript.items.slice(transcript.items.length - limit);
  return {
    ...transcript,
    itemCount: items.length,
    items
  };
}

function conflictDiagnostics(
  selectedSessionId: string,
  replay: SessionEventsReplay
): ProjectionDiagnostic[] {
  const diagnostics: ProjectionDiagnostic[] = [];
  const sourceReference = `session:${selectedSessionId}/events`;

  if (replay.session && replay.session.sessionId !== selectedSessionId) {
    diagnostics.push({
      code: 'REPLAY_SESSION_ID_CONFLICT',
      message: `Replay metadata identifies ${replay.session.sessionId}, not the selected session.`,
      sourceReference
    });
  }

  const conflictingEvent = replay.events.find(
    (event) => event.sessionId !== selectedSessionId
  );
  if (conflictingEvent) {
    diagnostics.push({
      code: 'REPLAY_EVENT_SESSION_ID_CONFLICT',
      message: `Event ${conflictingEvent.eventId} belongs to a different session.`,
      sourceReference
    });
  }

  if (
    replay.transcript?.sessionId &&
    replay.transcript.sessionId !== selectedSessionId
  ) {
    diagnostics.push({
      code: 'REPLAY_TRANSCRIPT_SESSION_ID_CONFLICT',
      message: `Transcript identifies ${replay.transcript.sessionId}, not the selected session.`,
      sourceReference
    });
  }

  return diagnostics;
}

function disclosureFor(input: {
  conflict: boolean;
  stale: boolean;
  malformedLineCount: number;
  bounded: boolean;
  hasSession: boolean;
  sourceEventCount: number;
  sourceItemCount: number;
}): ReplayDisclosure {
  if (input.conflict) return 'CONFLICTING';
  if (input.stale) return 'STALE';
  if (input.malformedLineCount > 0) return 'MALFORMED';
  if (input.bounded) return 'BOUNDED';
  if (!input.hasSession) return 'EVIDENCE_ONLY';
  if (input.sourceItemCount === 0 && input.sourceEventCount === 0) return 'EMPTY';
  if (input.sourceItemCount === 0) return 'EVIDENCE_ONLY';
  return 'READY_SNAPSHOT';
}

/**
 * Rebuild a selected-session replay view from one GET response. The returned
 * object owns copied/bounded transcript data and never reads or writes the
 * primary dialogue's live event buffer.
 */
export function buildSelectedSessionReplayProjection(
  selectedSessionId: string,
  replay: SessionEventsReplay,
  options: SelectedSessionReplayOptions
): SelectedSessionReplayProjection {
  const limit = positiveLimit(options.maxItems);
  const diagnostics = conflictDiagnostics(selectedSessionId, replay);
  const identityConflict = diagnostics.some((diagnostic) =>
    diagnostic.code.endsWith('_CONFLICT')
  );
  const admittedEvents = identityConflict
    ? replay.events.filter((event) => event.sessionId === selectedSessionId)
    : replay.events;
  const sourceTranscript = identityConflict
    ? deriveTranscriptView(admittedEvents)
    : replay.transcript ?? deriveTranscriptView(replay.events, replay.session);
  const transcript = boundedTranscript(sourceTranscript, limit);
  const sourceItemCount = sourceTranscript.items.length;
  const bounded = sourceItemCount > transcript.items.length;
  const malformedLineCount = Math.max(0, replay.malformedLineCount);
  const canonicalSession =
    replay.session?.sessionId === selectedSessionId ? replay.session : undefined;

  if (!canonicalSession) {
    diagnostics.push({
      code: 'REPLAY_SESSION_METADATA_UNAVAILABLE',
      message: 'Canonical session metadata was not included with this replay.',
      sourceReference: `session:${selectedSessionId}/events`
    });
  }
  if (malformedLineCount > 0) {
    diagnostics.push({
      code: 'MALFORMED_REPLAY_RECORDS',
      message: `${malformedLineCount} malformed replay record${
        malformedLineCount === 1 ? ' was' : 's were'
      } skipped.`,
      sourceReference: `session:${selectedSessionId}/events`
    });
  }
  if (bounded) {
    diagnostics.push({
      code: 'REPLAY_RENDER_BOUNDED',
      message: `Showing ${transcript.items.length} of ${sourceItemCount} transcript items.`,
      sourceReference: `session:${selectedSessionId}/events`
    });
  }
  if (options.stale) {
    diagnostics.push({
      code: 'REPLAY_STALE',
      message: 'A newer canonical session observation exists; this replay is stale.',
      sourceReference: `session:${selectedSessionId}/events`
    });
  }

  if (identityConflict) {
    diagnostics.push({
      code: 'REPLAY_FOREIGN_CONTENT_SUPPRESSED',
      message:
        'Transcript metadata or events identified another session; foreign content was suppressed.',
      sourceReference: `session:${selectedSessionId}/events`
    });
  }
  const conflict = identityConflict;
  const disclosure = disclosureFor({
    conflict,
    stale: options.stale === true,
    malformedLineCount,
    bounded,
    hasSession: Boolean(canonicalSession),
    sourceEventCount: replay.events.length,
    sourceItemCount
  });
  const currency: ProjectionCurrency =
    disclosure === 'CONFLICTING'
      ? 'CONFLICTING'
      : disclosure === 'STALE'
        ? 'STALE'
        : options.currency ?? 'UNKNOWN';

  const availableSessionIds =
    options.availableSessionIds ??
    new Set(canonicalSession ? [canonicalSession.sessionId] : []);
  const session = canonicalSession
    ? projectOperatorSession(canonicalSession, availableSessionIds, {
        observedAt: options.observedAt,
        currencyBySessionId: {
          [canonicalSession.sessionId]: currency
        }
      })
    : undefined;

  return {
    selectedSessionId,
    sourceReference: `session:${selectedSessionId}/events`,
    observedAt: options.observedAt,
    disclosure,
    currency,
    ...(session ? { session } : {}),
    transcript,
    events: admittedEvents,
    instructionHistory: [...replay.instructionHistory],
    instructionBases: [...replay.instructionBases],
    malformedLineCount,
    sourceEventCount: replay.events.length,
    renderedItemCount: transcript.items.length,
    ...(bounded
      ? {
          bounded: {
            rendered: transcript.items.length,
            available: sourceItemCount
          }
        }
      : {}),
    diagnostics
  };
}

function errorMessage(error: unknown): string {
  return error instanceof Error && error.message.trim().length > 0
    ? error.message
    : 'Selected-session replay is unavailable.';
}

/**
 * Request-versioned GET loader. Starting or cancelling a later request makes
 * every earlier response ineligible to update state, even when the underlying
 * fetch implementation cannot abort in flight.
 */
export function createSelectedSessionReplayLoader(
  fetchReplay: ReplayFetcher = (sessionId) => replaySessionEvents(sessionId)
): SelectedSessionReplayLoader {
  let state: SelectedSessionReplayState = { status: 'IDLE' };
  let generation = 0;
  let activeController: AbortController | undefined;
  const listeners = new Set<(next: SelectedSessionReplayState) => void>();

  const publish = (next: SelectedSessionReplayState): void => {
    state = next;
    for (const listener of listeners) {
      listener(next);
    }
  };

  const cancel = (): void => {
    generation += 1;
    activeController?.abort();
    activeController = undefined;
    publish({ status: 'IDLE' });
  };

  return {
    getState: () => state,
    subscribe(listener) {
      listeners.add(listener);
      return () => {
        listeners.delete(listener);
      };
    },
    async load(sessionId, options) {
      const requestGeneration = generation + 1;
      generation = requestGeneration;
      activeController?.abort();
      const controller = new AbortController();
      activeController = controller;
      publish({ status: 'LOADING', selectedSessionId: sessionId });

      try {
        const replay = await fetchReplay(sessionId, controller.signal);
        if (generation !== requestGeneration || controller.signal.aborted) {
          return { applied: false, state };
        }
        const projection = buildSelectedSessionReplayProjection(
          sessionId,
          replay,
          options
        );
        activeController = undefined;
        publish({ status: 'READY', projection });
        return { applied: true, state };
      } catch (error) {
        if (generation !== requestGeneration || controller.signal.aborted) {
          return { applied: false, state };
        }
        activeController = undefined;
        publish({
          status: 'UNAVAILABLE',
          selectedSessionId: sessionId,
          message: errorMessage(error)
        });
        return { applied: true, state };
      }
    },
    cancel,
    dispose() {
      cancel();
      listeners.clear();
    }
  };
}
