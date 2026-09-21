import { nativeNotification, record } from './native-progress';
import type { HarnessEvent, HarnessEventType } from '@chirality/runtime-contracts/event-schema';

/**
 * Pure derivations over the bridged `harness:event` stream. These power the
 * Tools and Subagents views of the workspace sidebar. They are intentionally
 * DOM-free and side-effect-free so they can be unit-tested in the node test
 * environment, and so the live stream and the persisted replay log derive to
 * the same rows ("replay is free" — see DESIGN §4).
 */

export type ToolActivityStatus = 'queued' | 'permission' | 'running' | 'completed' | 'failed';

export type ToolActivityRow = {
  /** Stable grouping key for the tool invocation. */
  key: string;
  /** For Codex items this is the item type (`commandExecution`, `fileChange`, `mcpToolCall`, ...). */
  toolName: string;
  status: ToolActivityStatus;
  /** Short human summary carried by the Codex adapter (command line, file list, tool name). */
  summary?: string;
  source?: string;
  surface?: string;
  /** Redacted safe path fields surfaced from the tool input metadata. */
  pathFields: Record<string, string>;
  /** Latest harness event type observed for this invocation. */
  lastEventType: HarnessEventType;
  timestamp: string;
  eventCount: number;
};

export type SubagentActivityStatus = 'running' | 'completed' | 'failed' | 'waiting' | 'interrupted' | 'unknown';

export type SubagentActivityRow = {
  key: string;
  agentName: string;
  status: SubagentActivityStatus;
  description?: string;
  summary?: string;
  lastToolName?: string;
  outputArtifactPath?: string;
  observationEnded?: string;
  nativeThreadId?: string;
  parentThreadId?: string;
  agentPath?: string;
  agentRole?: string;
  lastEventType: HarnessEventType;
  timestamp: string;
  eventCount: number;
};

export type PermissionRequestStatus = 'pending' | 'allowed' | 'denied';

export type PermissionRequestRow = {
  key: string;
  /**
   * The session that owns this gated call, captured from the event so the
   * approval can be posted even if the operator has since navigated away and the
   * UI's notion of the "active" session has changed (DESIGN §5.3 item b).
   */
  sessionId: string;
  toolName: string;
  reason: string;
  status: PermissionRequestStatus;
  mode?: string;
  /** Codex server request id and method when the approval came from the App Server. */
  requestId?: string;
  method?: string;
  /** Who resolved it: the user, the recorded policy, or the Runtime (turn ended). */
  decidedBy?: string;
  pathFields: Record<string, string>;
  timestamp: string;
};

export type ServerRequestStatus = 'pending' | 'answered' | 'cancelled' | 'unsupported' | 'failed';

/** One Codex server request that is not an approval (`codex.request`), with its resolution. */
export type ServerRequestRow = {
  key: string;
  sessionId: string;
  requestId: string;
  method: string;
  /** Adapter classification: `userInput`, `elicitation`, `dynamicToolCall`, or another method. */
  kind: string;
  /** Raw upstream `params`, preserved for faithful rendering and inspection. */
  request: unknown;
  status: ServerRequestStatus;
  decision?: unknown;
  decidedBy?: string;
  timestamp: string;
};

export type UserInputQuestion = {
  id: string;
  header: string;
  question: string;
  options: readonly { label: string; description: string }[];
  isOther: boolean;
  isSecret: boolean;
};

export type CodexNotificationRow = {
  key: string;
  sessionId: string;
  method: string;
  /** Raw upstream `params`, shown collapsed. */
  params: unknown;
  /** `thinking` for a completed reasoning item; `notification` otherwise. */
  kind: 'thinking' | 'notification';
  /** Reasoning text for a thinking row. */
  text?: string;
  timestamp: string;
};

const TOOL_STATUS_BY_TYPE: Partial<Record<HarnessEventType, ToolActivityStatus>> = {
  'tool.queued': 'queued',
  'tool.permission': 'permission',
  'tool.started': 'running',
  'tool.progress': 'running',
  'tool.completed': 'completed',
  'tool.failed': 'failed'
};

const SUBAGENT_STATUS_BY_TYPE: Partial<Record<HarnessEventType, SubagentActivityStatus>> = {
  'subagent.started': 'running',
  'subagent.progress': 'running',
  'subagent.completed': 'completed',
  'subagent.failed': 'failed'
};

function readString(value: unknown): string | undefined {
  return typeof value === 'string' && value.length > 0 ? value : undefined;
}

function readStringRecord(value: unknown): Record<string, string> {
  if (!value || typeof value !== 'object') {
    return {};
  }
  const result: Record<string, string> = {};
  for (const [fieldName, fieldValue] of Object.entries(value as Record<string, unknown>)) {
    const text = readString(fieldValue);
    if (text) {
      result[fieldName] = text;
    }
  }
  return result;
}

function readStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }
  return value.flatMap((item) => {
    const text = readString(item);
    return text ? [text] : [];
  });
}

function markRowCompletion(
  rows: Map<string, ToolActivityRow>,
  key: string,
  status: ToolActivityStatus,
  event: HarnessEvent
): boolean {
  const target = rows.get(key);
  if (!target) {
    return false;
  }
  // Map.set on an existing key updates the value in place (insertion order kept).
  rows.set(key, {
    ...target,
    status,
    lastEventType: event.type,
    timestamp: event.timestamp,
    eventCount: target.eventCount + 1
  });
  return true;
}

/**
 * Collapse the ordered tool.* lifecycle events into one row per tool
 * invocation, keyed by `toolUseId`, in first-seen order. The row reflects the
 * latest observed status; identifying fields (name, source, path metadata) are
 * filled from whichever lifecycle event carried them.
 *
 * The SDK's `tool_use_summary` message emits a `tool.completed` event that has
 * no id of its own — only `precedingToolUseIds`. Such an event completes the
 * tools it follows rather than starting a row of its own, so it is folded onto
 * the referenced rows and never produces an orphan "tool" entry.
 */
export function deriveToolActivity(events: readonly HarnessEvent[]): ToolActivityRow[] {
  const rows = new Map<string, ToolActivityRow>();

  for (const event of events) {
    const status = TOOL_STATUS_BY_TYPE[event.type];
    if (!status) {
      continue;
    }

    const data = event.data ?? {};
    const toolUseId = readString(data.toolUseId) ?? readString(data.adapterToolUseId);

    if (!toolUseId && Array.isArray(data.precedingToolUseIds)) {
      // Summary-style completion: apply the status to each preceding row.
      for (const ref of readStringArray(data.precedingToolUseIds)) {
        markRowCompletion(rows, ref, status, event);
      }
      continue;
    }

    const key = toolUseId ?? event.eventId;
    const existing = rows.get(key);

    const inputMetadata = data.inputMetadata;
    const incomingPathFields =
      inputMetadata && typeof inputMetadata === 'object'
        ? readStringRecord((inputMetadata as Record<string, unknown>).pathFields)
        : {};

    // Map.set keeps the existing key's position, so rows stay in first-seen order.
    rows.set(key, {
      key,
      toolName:
        readString(data.toolName) ??
        readString(data.adapterToolName) ??
        existing?.toolName ??
        'tool',
      status,
      summary: readString(data.summary) ?? existing?.summary,
      source: readString(data.source) ?? existing?.source,
      surface: readString(data.surface) ?? existing?.surface,
      pathFields: {
        ...(existing?.pathFields ?? {}),
        ...incomingPathFields
      },
      lastEventType: event.type,
      timestamp: event.timestamp,
      eventCount: (existing?.eventCount ?? 0) + 1
    });
  }

  return [...rows.values()];
}

function readNestedPathFields(data: Record<string, unknown>): Record<string, string> {
  // Path metadata lives at data.safeMetadata.inputMetadata.pathFields.
  const safeMetadata = data.safeMetadata;
  if (!safeMetadata || typeof safeMetadata !== 'object') {
    return {};
  }
  const inputMetadata = (safeMetadata as Record<string, unknown>).inputMetadata;
  if (!inputMetadata || typeof inputMetadata !== 'object') {
    return {};
  }
  return readStringRecord((inputMetadata as Record<string, unknown>).pathFields);
}

const PERMISSION_STATUS_BY_BEHAVIOR: Record<string, PermissionRequestStatus> = {
  ask: 'pending',
  allow: 'allowed',
  deny: 'denied'
};

/**
 * Collapse `tool.permission` events into one row per gated tool call, in
 * first-seen order. Only calls that entered the `ask` (pending) state are
 * surfaced — straight policy allows/denies are not operator-actionable. The
 * status reflects the latest behavior, so an `ask` followed by the operator's
 * `allow`/`deny` resolves the same row.
 */
export function derivePermissionRequests(events: readonly HarnessEvent[]): PermissionRequestRow[] {
  const rows = new Map<string, PermissionRequestRow>();

  for (const event of events) {
    if (event.type !== 'tool.permission') {
      continue;
    }

    const data = event.data ?? {};
    const behavior = readString(data.behavior);
    const status = behavior ? PERMISSION_STATUS_BY_BEHAVIOR[behavior] : undefined;
    if (!status) {
      continue;
    }

    const key =
      readString(data.toolUseId) ??
      readString(data.adapterToolUseId) ??
      readString(data.decisionId) ??
      event.eventId;
    const existing = rows.get(key);

    // Surface a row only once it has entered (or is entering) the pending state.
    if (!existing && status !== 'pending') {
      continue;
    }

    const pathFields = readNestedPathFields(data);

    rows.set(key, {
      key,
      sessionId: event.sessionId,
      toolName: readString(data.toolName) ?? existing?.toolName ?? 'tool',
      reason: readString(data.reason) ?? existing?.reason ?? '',
      status,
      mode: readString(data.mode) ?? existing?.mode,
      requestId: readString(data.requestId) ?? existing?.requestId,
      method: readString(data.method) ?? existing?.method,
      decidedBy: readString(data.decidedBy) ?? existing?.decidedBy,
      pathFields:
        Object.keys(pathFields).length > 0 ? pathFields : (existing?.pathFields ?? {}),
      timestamp: event.timestamp
    });
  }

  return [...rows.values()];
}

const SERVER_REQUEST_OUTCOMES: Record<string, ServerRequestStatus> = {
  answered: 'answered',
  cancelled: 'cancelled',
  unsupported: 'unsupported',
  failed: 'failed'
};

function readRecord(value: unknown): Record<string, unknown> | undefined {
  return value && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined;
}

/** Best-effort classification when the adapter did not label the request. */
const APPROVAL_REQUEST_METHODS = new Set([
  'item/commandExecution/requestApproval', 'item/fileChange/requestApproval', 'item/permissions/requestApproval',
  'execCommandApproval', 'applyPatchApproval'
]);

export function classifyServerRequestMethod(method: string): string {
  if (APPROVAL_REQUEST_METHODS.has(method)) return 'approval';
  if (method === 'item/tool/requestUserInput') return 'userInput';
  if (method === 'mcpServer/elicitation/request') return 'elicitation';
  if (method === 'item/tool/call') return 'dynamicToolCall';
  return method;
}

/**
 * Collapse `codex.request` and `codex.request.resolved` events into one row per
 * Codex server request, in first-seen order. Approval requests are carried by
 * `tool.permission` instead and never appear here.
 */
export function deriveServerRequests(events: readonly HarnessEvent[]): ServerRequestRow[] {
  const rows = new Map<string, ServerRequestRow>();
  for (const event of events) {
    if (event.type !== 'codex.request' && event.type !== 'codex.request.resolved') continue;
    const data = event.data ?? {};
    const requestId = readString(data.requestId);
    if (!requestId) continue;
    const method = readString(data.method) ?? '';
    const key = `${event.sessionId}:${requestId}`;
    const existing = rows.get(key);
    if (event.type === 'codex.request') {
      rows.set(key, {
        key,
        sessionId: event.sessionId,
        requestId,
        method: method || existing?.method || '',
        kind: readString(data.kind) ?? existing?.kind ?? classifyServerRequestMethod(method),
        request: data.request ?? existing?.request,
        status: existing?.status ?? 'pending',
        ...(existing?.decision !== undefined ? { decision: existing.decision } : {}),
        ...(existing?.decidedBy ? { decidedBy: existing.decidedBy } : {}),
        timestamp: existing?.timestamp ?? event.timestamp
      });
      continue;
    }
    const outcome = readString(data.outcome);
    const status: ServerRequestStatus = (outcome ? SERVER_REQUEST_OUTCOMES[outcome] : undefined) ?? 'answered';
    if (!existing) {
      // A resolution for an approval (carried by tool.permission) or for a request
      // whose `codex.request` was never persisted: nothing to surface as a card.
      continue;
    }
    rows.set(key, {
      ...existing,
      status,
      ...(data.decision !== undefined ? { decision: data.decision } : {}),
      ...(readString(data.decidedBy) ? { decidedBy: readString(data.decidedBy) } : {}),
      timestamp: event.timestamp
    });
  }
  return [...rows.values()];
}

/** Requests the user can still answer: pending, of an answerable kind, and only while the turn is live. */
export function selectPendingServerRequests(events: readonly HarnessEvent[], active: boolean): ServerRequestRow[] {
  if (!active) return [];
  return deriveServerRequests(events).filter(
    (row) => row.status === 'pending' && (row.kind === 'userInput' || row.kind === 'elicitation')
  );
}

/** Questions of an `item/tool/requestUserInput` request, read from its raw params. */
export function readUserInputQuestions(request: unknown): UserInputQuestion[] {
  const params = readRecord(request);
  const questions = Array.isArray(params?.questions) ? params.questions : [];
  return questions.flatMap((entry): UserInputQuestion[] => {
    const question = readRecord(entry);
    const id = readString(question?.id);
    if (!question || !id) return [];
    const options = Array.isArray(question.options)
      ? question.options.flatMap((option): { label: string; description: string }[] => {
          const record = readRecord(option);
          const label = readString(record?.label);
          return label ? [{ label, description: readString(record?.description) ?? '' }] : [];
        })
      : [];
    return [{
      id,
      header: readString(question.header) ?? id,
      question: readString(question.question) ?? '',
      options,
      isOther: question.isOther === true,
      isSecret: question.isSecret === true
    }];
  });
}

/** Message text of an `mcpServer/elicitation/request`, read from its raw params. */
export function readElicitationMessage(request: unknown): string {
  const params = readRecord(request);
  return readString(params?.message) ?? '';
}

function reasoningText(item: Record<string, unknown>): string | undefined {
  const direct = readString(item.summary);
  if (direct) return direct;
  for (const field of ['summary']) {
    const value = item[field];
    if (Array.isArray(value)) {
      const parts = value.flatMap((part) => {
        const text = readString(part) ?? readString(readRecord(part)?.text);
        return text ? [text] : [];
      });
      if (parts.length > 0) return parts.join('\n');
    }
  }
  return undefined;
}

/**
 * Every `codex.notification` in order: a completed reasoning item becomes a
 * "Thinking" row carrying its text; anything else becomes a generic card with
 * the upstream method and its raw params for inspection.
 */
export function deriveCodexNotifications(events: readonly HarnessEvent[]): CodexNotificationRow[] {
  const rows: CodexNotificationRow[] = [];
  for (const event of events) {
    if (event.type !== 'codex.notification') continue;
    const data = event.data ?? {};
    const method = readString(data.method) ?? 'notification';
    const params = data.params ?? data.codex;
    const item = readRecord(readRecord(params)?.item);
    if (method === 'item/completed' && item && item.type === 'reasoning') {
      rows.push({ key: event.eventId, sessionId: event.sessionId, method, params, kind: 'thinking', text: reasoningText(item) ?? '', timestamp: event.timestamp });
      continue;
    }
    rows.push({ key: event.eventId, sessionId: event.sessionId, method, params, kind: 'notification', timestamp: event.timestamp });
  }
  return rows;
}

/**
 * Select the operator-actionable permission requests for the approval cards: the
 * gated calls still awaiting a decision, but only while a turn is live (`active`).
 * Once the turn ends the broker has auto-denied every still-pending request, so a
 * leftover `pending` row is no longer actionable and must not be surfaced
 * (DESIGN §5.3 item a). Pure so both branches are unit-testable without the React
 * wrapper or a DOM.
 */
export function selectPendingPermissionRequests(
  events: readonly HarnessEvent[],
  active: boolean
): PermissionRequestRow[] {
  if (!active) {
    return [];
  }
  return derivePermissionRequests(events).filter((row) => row.status === 'pending');
}

/**
 * Collapse legacy task lifecycle and native child evidence into one row per run.
 * Native rows use session + actual thread identity; stock activity item IDs only
 * deduplicate lifecycle pairs. Legacy events remain keyed by taskId.
 * Collapse the ordered subagent.* lifecycle events into one row per child run,
 * in first-seen order. Keyed by `taskId` — the SDK mapper sets `taskId` on
 * every subagent.* event, whereas `childRunId` is only present when a child-run
 * record was built (e.g. a `task_updated` completion with no output file omits
 * it). Keying on `taskId` keeps the completion collapsing onto the running row
 * instead of forking an orphan.
 */
export function deriveSubagentActivity(events: readonly HarnessEvent[]): SubagentActivityRow[] {
  const rows = new Map<string, SubagentActivityRow>();

  for (const event of events) {
    const status = SUBAGENT_STATUS_BY_TYPE[event.type];
    if (!status) {
      continue;
    }

    const data = event.data ?? {};
    // Retained stock-v2 activity uses item IDs, not legacy task identities.
    if (event.type === 'subagent.progress' && (readString(data.agentThreadId) || record(record(record(data.codex).params).item).type === 'subAgentActivity')) continue;
    const key =
      readString(data.taskId) ??
      readString(data.childRunId) ??
      readString(data.toolUseId) ??
      event.eventId;
    const existing = rows.get(key);

    // Map.set keeps the existing key's position, so rows stay in first-seen order.
    rows.set(key, {
      key,
      agentName:
        readString(data.agentName) ??
        readString(data.subagentType) ??
        existing?.agentName ??
        'subagent',
      status,
      description: readString(data.description) ?? existing?.description,
      summary: readString(data.summary) ?? existing?.summary,
      lastToolName: readString(data.lastToolName) ?? existing?.lastToolName,
      outputArtifactPath: readString(data.outputArtifactPath) ?? existing?.outputArtifactPath,
      lastEventType: event.type,
      timestamp: event.timestamp,
      eventCount: (existing?.eventCount ?? 0) + 1
    });
  }

  // Native collaboration calls describe receivers, not assignment completion.
  const nativeStatus = (value: unknown): SubagentActivityStatus => {
    const status = typeof value === 'string' ? value : record(value).type;
    return status === 'completed' ? 'completed' : status === 'errored' || status === 'failed' || status === 'systemError' ? 'failed'
      : status === 'interrupted' ? 'interrupted' : status === 'running' || status === 'active' ? 'running'
      : status === 'pendingInit' ? 'waiting' : 'unknown';
  };
  const update = (event: HarnessEvent, id: string, patch: Partial<SubagentActivityRow>) => {
    const key = `native:${event.sessionId}:${id}`;
    const old = rows.get(key);
    rows.set(key, { key, nativeThreadId: id, agentName: old?.agentName ?? 'subagent', status: old?.status ?? 'unknown',
      ...old, ...patch, lastEventType: event.type, timestamp: event.timestamp, eventCount: (old?.eventCount ?? 0) + 1 });
  };
  const seenEvents = new Set<string>();
  const seenActivities = new Set<string>();
  for (const event of events) {
    if (seenEvents.has(event.eventId)) continue;
    seenEvents.add(event.eventId);
    const data = event.data ?? {};
    const retained = event.type === 'subagent.progress' ? record(record(data.codex).params) : undefined;
    const retainedItem: Record<string, unknown> = { ...record(retained?.item) };
    if (retained && readString(data.agentThreadId)) {
      Object.assign(retainedItem, { type: 'subAgentActivity', agentThreadId: data.agentThreadId,
        kind: data.kind ?? retainedItem.kind, agentPath: data.agentPath ?? retainedItem.agentPath,
        id: data.taskId ?? retainedItem.id });
    }
    const n = nativeNotification(event) ?? (retained ? {
      method: readString(record(data.codex).method), params: retained,
      threadId: readString(retained.threadId), item: retainedItem
    } : undefined);
    if (!n) continue;
    if (n.item.type === 'subAgentActivity') {
      const id = readString(n.item.agentThreadId);
      if (!id) continue;
      const itemId = readString(n.item.id);
      const pairKey = `${event.sessionId}:${id}:${itemId ?? event.eventId}`;
      if (seenActivities.has(pairKey)) continue;
      seenActivities.add(pairKey);
      const kind = readString(n.item.kind);
      // Outer item/completed merely closes the activity report, not child work.
      const status = kind === 'started' ? 'running' : kind === 'completed' ? 'completed' : kind === 'interrupted' ? 'interrupted' : undefined;
      update(event, id, { ...(status ? { status } : {}), ...(readString(n.item.agentPath) ? { agentPath: readString(n.item.agentPath) } : {}) });
      continue;
    }
    if (n.method === 'chirality/nativeChildren/observationEnded') {
      for (const id of readStringArray(n.params.agentThreadIds)) update(event, id, { observationEnded: readString(n.params.message) ?? 'Observation ended with the parent turn. Later child activity is not recorded here.' });
    }
    if (n.item.type === 'collabAgentToolCall') {
      const states = record(n.item.agentsStates);
      const receivers = new Set([...readStringArray(n.item.receiverThreadIds), ...Object.keys(states)]);
      for (const id of receivers) {
        const state = record(states[id]);
        update(event, id, { ...(state.status ? { status: nativeStatus(state.status) } : {}),
          ...(readString(n.item.prompt) ? { description: readString(n.item.prompt) } : {}),
          ...(readString(state.message) ? { summary: readString(state.message) } : {}) });
      }
    }
    const thread = record(n.params.thread);
    if (n.method === 'thread/started' && n.threadId && readString(thread.parentThreadId)) {
      update(event, n.threadId, { ...(readString(thread.agentNickname) ? { agentName: readString(thread.agentNickname) } : {}), parentThreadId: readString(thread.parentThreadId), agentRole: readString(thread.agentRole), ...(readString(thread.agentPath) ? { agentPath: readString(thread.agentPath) } : {}), ...(thread.status ? { status: nativeStatus(thread.status) } : {}) });
    }
    if (!n.threadId || !rows.has(`native:${event.sessionId}:${n.threadId}`)) continue;
    if (n.method === 'thread/status/changed') {
      const status = record(n.params.status);
      update(event, n.threadId, { status: Array.isArray(status.activeFlags) && status.activeFlags.length ? 'waiting' : nativeStatus(n.params.status) });
    }
    if (n.method === 'turn/started') update(event, n.threadId, { status: 'running' });
    if (n.method === 'turn/completed') update(event, n.threadId, { status: nativeStatus(record(n.params.turn).status) });
    if (n.method === 'item/completed' && n.item.type === 'agentMessage' && readString(n.item.text)) update(event, n.threadId, { summary: readString(n.item.text) });
  }
  return [...rows.values()];
}
