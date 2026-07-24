export const HARNESS_EVENT_TYPES = [
  'session.created',
  'session.resumed',
  'turn.accepted',
  'turn.started',
  'adapter.initialized',
  'message.accepted',
  'message.queued',
  'message.started',
  'message.delta',
  'message.completed',
  'model.request.started',
  'model.delta',
  'model.completed',
  'turn.completed',
  'turn.failed',
  'turn.cancelled',
  'turn.interrupted',
  'tool.queued',
  'tool.permission',
  'tool.started',
  'tool.progress',
  'tool.completed',
  'tool.failed',
  'hook.started',
  'hook.progress',
  'hook.completed',
  'hook.failed',
  'queue.enqueued',
  'queue.consumed',
  'queue.cleared',
  'branch.created',
  'branch.selected',
  'branch.summarized',
  'interruption.requested',
  'interruption.completed',
  'context.compaction.started',
  'context.compacted',
  'context.compaction.failed',
  'subagent.started',
  'subagent.progress',
  'subagent.completed',
  'subagent.failed',
  'coordination.notice',
  'coordination.update',
  'coordination.acknowledged',
  'runtime.mirror.error'
] as const;

export type HarnessEventType = (typeof HARNESS_EVENT_TYPES)[number];

export type HarnessEvent = {
  schemaVersion: 1;
  eventId: string;
  sessionId: string;
  turnId?: string;
  parentEventId?: string;
  timestamp: string;
  type: HarnessEventType;
  data: Record<string, unknown>;
};
