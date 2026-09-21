import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';

/**
 * Keep only the last `max` events (dropping the oldest), preserving order.
 *
 * Shared by the live-event buffer's append path and the hydrate-on-open path
 * (D-APP-22) so both honor the same `MAX_LIVE_HARNESS_EVENTS` bound. Hydrate
 * REPLACES the buffer with the (bounded) replayed events rather than appending,
 * so events already streamed live in the same turn are never double-counted.
 */
export function boundHarnessEventBuffer(
  events: readonly HarnessEvent[],
  max: number
): HarnessEvent[] {
  if (events.length <= max) {
    return [...events];
  }
  return events.slice(events.length - max);
}
