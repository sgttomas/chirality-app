import type { HarnessEvent, HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import { redactJsonLike } from './run-logger';
import type { UIEvent } from '@chirality/runtime-contracts/types';

/**
 * The keystone bridge: forward rich HarnessEvents to the live browser stream as a
 * provider-neutral `harness:event` UIEvent, so the live loop, subagent view, and
 * tool-usage view can render the harness's real event vocabulary — the same shape
 * persisted to events.jsonl (live == replay).
 *
 * High-frequency events already covered by the thin public UIEvents are skipped:
 *  - `model.delta` / `message.delta`: per-token assistant text (covered by `chat:delta`).
 *  - `adapter.initialized`: provider boot metadata (covered by `session:init`).
 *
 * The forwarded payload is redacted with the same helper used for persistence, so
 * configured API keys never reach the browser even though provider metadata is
 * allowed in payloads (RuntimeEngineContract.providerMetadataAllowed).
 */
export const HARNESS_EVENT_STREAM_SKIP: ReadonlySet<HarnessEventType> = new Set<HarnessEventType>([
  'model.delta',
  'message.delta',
  'adapter.initialized'
]);

export function harnessEventToUiEvent(event: HarnessEvent): UIEvent | null {
  if (HARNESS_EVENT_STREAM_SKIP.has(event.type)) {
    return null;
  }

  return {
    type: 'harness:event',
    data: redactJsonLike(event)
  };
}
