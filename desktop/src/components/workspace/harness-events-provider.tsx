'use client';

import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode
} from 'react';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { boundHarnessEventBuffer } from '../../lib/shell/harness-event-buffer';

/**
 * Holds the live, bridged `harness:event` stream for the active turn so that
 * the producer (the chat panel / live loop) and the consumers (the Tools and
 * Subagents sidebar views) share one source of truth. The chat panel appends
 * rich events as they arrive and clears them when a new turn starts.
 *
 * The stream is exposed through two separate contexts: a *data* context (the
 * events array, which changes on every append) and an *actions* context
 * (append/clear, whose identity is stable). The producer subscribes only to the
 * stable actions context, so appending an event does not re-render the heavy
 * chat transcript; only the data consumers (the stream views) re-render.
 */
type HarnessEventActions = {
  appendEvent: (event: HarnessEvent) => void;
  clearEvents: () => void;
  /**
   * Replace the buffer with a past session's persisted events (hydrate-on-open,
   * D-APP-22). Bounded to `MAX_LIVE_HARNESS_EVENTS`; replacing (not appending)
   * means same-turn live events are never double-counted.
   */
  hydrateEvents: (events: readonly HarnessEvent[]) => void;
  /**
   * Mark a live turn as active. Lets buffer consumers (e.g. the session list)
   * avoid replacing the buffer mid-turn — hydrating a past session while a turn
   * streams would mix two sessions' events (D-APP-22 "no same-turn mix").
   */
  setStreaming: (streaming: boolean) => void;
};

const HarnessEventsDataContext = createContext<HarnessEvent[] | null>(null);
const HarnessEventActionsContext = createContext<HarnessEventActions | null>(null);
const HarnessStreamingContext = createContext<boolean | null>(null);

/** Bound the buffer so a long-running, tool-heavy turn cannot grow without limit. */
export const MAX_LIVE_HARNESS_EVENTS = 2000;

export function HarnessEventsProvider({ children }: { children: ReactNode }): JSX.Element {
  const [events, setEvents] = useState<HarnessEvent[]>([]);
  const [streaming, setStreamingState] = useState(false);

  const appendEvent = useCallback((event: HarnessEvent) => {
    setEvents((existing) => boundHarnessEventBuffer([...existing, event], MAX_LIVE_HARNESS_EVENTS));
  }, []);

  const clearEvents = useCallback(() => {
    setEvents([]);
  }, []);

  const hydrateEvents = useCallback((incoming: readonly HarnessEvent[]) => {
    setEvents(boundHarnessEventBuffer(incoming, MAX_LIVE_HARNESS_EVENTS));
  }, []);

  const setStreaming = useCallback((value: boolean) => {
    setStreamingState(value);
  }, []);

  const actions = useMemo<HarnessEventActions>(
    () => ({ appendEvent, clearEvents, hydrateEvents, setStreaming }),
    [appendEvent, clearEvents, hydrateEvents, setStreaming]
  );

  return (
    <HarnessEventActionsContext.Provider value={actions}>
      <HarnessStreamingContext.Provider value={streaming}>
        <HarnessEventsDataContext.Provider value={events}>
          {children}
        </HarnessEventsDataContext.Provider>
      </HarnessStreamingContext.Provider>
    </HarnessEventActionsContext.Provider>
  );
}

/** Data hook for consumers that render the stream (Tools / Subagents views). */
export function useHarnessEvents(): { events: HarnessEvent[] } {
  const events = useContext(HarnessEventsDataContext);
  if (events === null) {
    throw new Error('useHarnessEvents must be used inside HarnessEventsProvider');
  }
  return { events };
}

/** Actions hook for the producer (the chat panel); stable across event appends. */
export function useHarnessEventActions(): HarnessEventActions {
  const actions = useContext(HarnessEventActionsContext);
  if (!actions) {
    throw new Error('useHarnessEventActions must be used inside HarnessEventsProvider');
  }
  return actions;
}

/** Whether a live turn is currently streaming events into the buffer. */
export function useHarnessStreaming(): boolean {
  const streaming = useContext(HarnessStreamingContext);
  if (streaming === null) {
    throw new Error('useHarnessStreaming must be used inside HarnessEventsProvider');
  }
  return streaming;
}
