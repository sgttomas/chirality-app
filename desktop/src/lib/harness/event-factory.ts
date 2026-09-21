import { randomUUID } from 'node:crypto';
import type { HarnessEvent, HarnessEventType } from '@chirality/runtime-contracts/event-schema';

export function createHarnessEvent(input: {
  sessionId: string;
  type: HarnessEventType;
  data?: Record<string, unknown>;
  turnId?: string;
  parentEventId?: string;
}): HarnessEvent {
  return {
    schemaVersion: 1,
    eventId: `evt_${randomUUID()}`,
    sessionId: input.sessionId,
    turnId: input.turnId,
    parentEventId: input.parentEventId,
    timestamp: new Date().toISOString(),
    type: input.type,
    data: input.data ?? {}
  };
}
