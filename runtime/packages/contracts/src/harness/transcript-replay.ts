import type { HarnessEvent, HarnessEventType } from './event-schema.js';
import type { SessionRecord } from './types.js';

type JsonRecord = Record<string, unknown>;

export type TranscriptMessageRole = 'user' | 'assistant';
export type TranscriptItemKind = 'message' | 'tool' | 'terminal' | 'diagnostic';
export type TranscriptItemStatus =
  | 'accepted'
  | 'queued'
  | 'started'
  | 'completed'
  | 'failed'
  | 'cancelled'
  | 'interrupted'
  | 'diagnostic';

export type TranscriptArtifactLink = {
  artifactPath?: string;
  artifactRelativePath?: string;
  sha256?: string;
  toolName?: string;
  turnId?: string;
  retentionPolicy?: string;
  redacted?: boolean;
  truncated?: boolean;
  artifactByteLength?: number;
};

export type TranscriptItem = {
  key: string;
  kind: TranscriptItemKind;
  role?: TranscriptMessageRole;
  status: TranscriptItemStatus;
  title: string;
  timestamp: string;
  eventId: string;
  eventType: HarnessEventType;
  turnId?: string;
  text?: string;
  /** Native message identity and supplier phase; null means unknown. */
  nativeItemId?: string;
  providerThreadId?: string;
  phase?: "commentary" | "final_answer" | null;
  attachments?: string[];
  summary?: string;
  /** Recorded terminal cause; distinct from presentation status. */
  terminalReason?: string;
  toolName?: string;
  artifact?: TranscriptArtifactLink;
};

export type TranscriptSdkLinkage = {
  engineSessionId?: string;
  claudeSessionId?: string;
  sdkSessionId?: string;
  sdkTranscriptPath?: string;
  sdkSessionStoreKey?: string;
  sdkConfigDir?: string;
  sdkSettingSources?: string[];
  sdkPackageVersion?: string;
  sdkClaudeCodeVersion?: string;
  model?: string;
};

export type TranscriptView = {
  sessionId?: string;
  itemCount: number;
  items: TranscriptItem[];
  terminalStatus?: Extract<TranscriptItemStatus, 'completed' | 'failed' | 'cancelled' | 'interrupted'>;
  sdkLinkage?: TranscriptSdkLinkage;
};

function isRecord(value: unknown): value is JsonRecord {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function readString(value: unknown): string | undefined {
  return typeof value === 'string' && value.length > 0 ? value : undefined;
}

function readNumber(value: unknown): number | undefined {
  return typeof value === 'number' && Number.isFinite(value) ? value : undefined;
}

function readBoolean(value: unknown): boolean | undefined {
  return typeof value === 'boolean' ? value : undefined;
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

function turnKey(event: HarnessEvent): string {
  return (
    event.turnId ??
    readString(event.data.turnId) ??
    readString(event.data.parentToolUseId) ??
    event.sessionId
  );
}

function messageRole(event: HarnessEvent): TranscriptMessageRole {
  return readString(event.data.role) === 'assistant' ? 'assistant' : 'user';
}

function messageStatus(type: HarnessEventType): TranscriptItemStatus {
  switch (type) {
    case 'message.queued':
      return 'queued';
    case 'message.started':
      return 'started';
    case 'message.completed':
      return 'completed';
    default:
      return 'accepted';
  }
}

function terminalStatus(
  type: HarnessEventType
): TranscriptView['terminalStatus'] | undefined {
  switch (type) {
    case 'turn.completed':
      return 'completed';
    case 'turn.failed':
      return 'failed';
    case 'turn.cancelled':
      return 'cancelled';
    case 'turn.interrupted':
      return 'interrupted';
    default:
      return undefined;
  }
}

function artifactLink(data: JsonRecord): TranscriptArtifactLink | undefined {
  const artifactMetadata = data.artifactMetadata;
  if (!isRecord(artifactMetadata)) {
    return undefined;
  }
  const artifact: TranscriptArtifactLink = {
    artifactPath: readString(artifactMetadata.artifactPath),
    artifactRelativePath: readString(artifactMetadata.artifactRelativePath),
    sha256: readString(artifactMetadata.sha256),
    toolName: readString(artifactMetadata.toolName),
    turnId: readString(artifactMetadata.turnId),
    retentionPolicy: readString(artifactMetadata.retentionPolicy),
    redacted: readBoolean(artifactMetadata.redacted),
    truncated: readBoolean(artifactMetadata.truncated),
    artifactByteLength: readNumber(artifactMetadata.artifactByteLength)
  };
  return Object.values(artifact).some((value) => value !== undefined) ? artifact : undefined;
}

function summarizeToolResult(data: JsonRecord): string | undefined {
  const resultMetadata = data.resultMetadata;
  if (!isRecord(resultMetadata)) {
    return undefined;
  }

  const parts: string[] = [];
  const contentItemCount = readNumber(resultMetadata.contentItemCount);
  if (contentItemCount !== undefined) {
    parts.push(`${contentItemCount} content item${contentItemCount === 1 ? '' : 's'}`);
  }
  const contentTypes = readStringArray(resultMetadata.contentTypes);
  if (contentTypes.length > 0) {
    parts.push(contentTypes.join(', '));
  }
  const byteLength = readNumber(resultMetadata.resultByteLength);
  if (byteLength !== undefined) {
    parts.push(`${byteLength} bytes`);
  }
  if (readBoolean(resultMetadata.outputPersisted)) {
    parts.push('artifact saved');
  }

  return parts.length > 0 ? parts.join(' / ') : undefined;
}

function terminalSummary(event: HarnessEvent): string | undefined {
  const data = event.data;
  const error = readString(data.error);
  if (error) {
    return error;
  }
  const errors = readStringArray(data.errors);
  if (errors.length > 0) {
    return errors.join('; ');
  }
  return (
    readString(data.stopReason) ??
    readString(data.terminalReason) ??
    readString(data.subtype) ??
    undefined
  );
}

function deriveSdkLinkage(session?: SessionRecord): TranscriptSdkLinkage | undefined {
  if (!session) {
    return undefined;
  }

  const linkage: TranscriptSdkLinkage = {
    engineSessionId: session.engineSessionId,
    claudeSessionId: session.claudeSessionId,
    sdkSessionId: session.sdkSessionId,
    sdkTranscriptPath: session.sdkTranscriptPath,
    sdkSessionStoreKey: session.sdkSessionStoreKey,
    sdkConfigDir: session.sdkConfigDir,
    sdkSettingSources: session.sdkSettingSources,
    sdkPackageVersion: session.sdkPackageVersion,
    sdkClaudeCodeVersion: session.sdkClaudeCodeVersion,
    model: session.model
  };

  return Object.values(linkage).some((value) => value !== undefined) ? linkage : undefined;
}

function completedAssistantKeys(events: readonly HarnessEvent[]): Set<string> {
  const keys = new Set<string>();
  for (const event of events) {
    if (event.type === 'message.completed' && messageRole(event) === 'assistant') {
      keys.add(turnKey(event));
    }
  }
  return keys;
}

function nativeMessage(event: HarnessEvent): { params: JsonRecord; item: JsonRecord; key: string; method: string } | undefined {
  if (event.type !== 'codex.notification') return undefined;
  const params = isRecord(event.data.params) ? event.data.params : {};
  const codex = isRecord(event.data.codex) ? event.data.codex : {};
  if (codex.isPrimaryThread === false || (codex.isPrimaryThread !== true && params.threadId !== codex.providerThreadId)) return undefined;
  const item = isRecord(params.item) ? params.item : {};
  const method = String(event.data.method);
  if (method !== 'item/agentMessage/delta' && !(['item/started', 'item/completed'].includes(method) && item.type === 'agentMessage')) return undefined;
  const itemId = readString(params.itemId) ?? readString(item.id);
  const threadId = readString(params.threadId);
  const turnId = readString(params.turnId);
  if (!itemId || !threadId || !turnId) return undefined;
  return { params, item, method, key: JSON.stringify([event.sessionId, threadId, turnId, itemId]) };
}

export function deriveTranscriptView(
  events: readonly HarnessEvent[],
  session?: SessionRecord
): TranscriptView {
  const items: TranscriptItem[] = [];
  const nativeTurns = new Set(events.filter(event => nativeMessage(event)).map(turnKey));
  const nativeItems = new Map<string, TranscriptItem>();
  const steerItems = new Map<string, TranscriptItem>();
  const seenNativeEvents = new Set<string>();
  const bootTurns = new Set(events.filter(event => event.type === "turn.accepted" && event.data.boot === true).map(turnKey));
  const assistantCompletionKeys = completedAssistantKeys(events);
  // Older adapters also emitted a user message event. Prefer that record to
  // avoid duplicating the same accepted input during mixed-version replay.
  const explicitUserTurns = new Set(events.filter(event =>
    ['message.accepted', 'message.queued', 'message.started', 'message.completed'].includes(event.type) &&
    messageRole(event) === 'user' && Boolean(readString(event.data.text) ?? readString(event.data.message))
  ).map(turnKey));
  const acceptedAttachments = new Map(events.filter(event => event.type === 'turn.accepted')
    .map(event => [turnKey(event), readStringArray(event.data.attachments)]));
  const deltaItems = new Map<string, TranscriptItem>();
  let currentTerminalStatus: TranscriptView['terminalStatus'];

  for (const event of events) {
    const data = event.data;
    if (bootTurns.has(turnKey(event))) continue;
    const native = nativeMessage(event);
    if (native) {
      if (seenNativeEvents.has(event.eventId)) continue;
      seenNativeEvents.add(event.eventId);
      let row = nativeItems.get(native.key);
      if (!row) {
        row = { key: `native:${native.key}`, kind: 'message', role: 'assistant', status: 'started', title: 'Assistant',
          timestamp: event.timestamp, eventId: event.eventId, eventType: event.type, turnId: event.turnId,
          nativeItemId: readString(native.params.itemId) ?? readString(native.item.id), providerThreadId: String(native.params.threadId), phase: null, text: '' };
        nativeItems.set(native.key, row);
        items.push(row);
      }
      if (native.method === 'item/agentMessage/delta') {
        if (row.status !== 'completed' && typeof native.params.delta === 'string') row.text = (row.text ?? '') + native.params.delta;
      } else {
        // Completed text is the full authoritative snapshot, not an append.
        if (typeof native.item.text === 'string' && (native.method === 'item/completed' || row.status !== 'completed')) row.text = native.item.text;
        if ((native.method === 'item/completed' || row.status !== 'completed') && (native.item.phase === 'commentary' || native.item.phase === 'final_answer' || native.item.phase === null)) row.phase = native.item.phase;
        if (native.method === 'item/completed') row.status = 'completed';
      }
      row.eventId = event.eventId;
      continue;
    }
    if (event.type === 'codex.steer') {
      const operationId = readString(data.operationId);
      if (!operationId) continue;
      const key = JSON.stringify([event.sessionId, operationId]);
      let row = steerItems.get(key);
      if (!row) {
        row = { key: `steer:${key}`, kind: 'message', role: 'user', status: 'queued', title: 'User', timestamp: event.timestamp,
          eventId: event.eventId, eventType: event.type, turnId: event.turnId, text: readString(data.text) };
        steerItems.set(key, row); items.push(row);
      }
      row.status = data.status === 'accepted' ? 'accepted' : data.status === 'rejected' ? 'failed' : 'queued';
      row.summary = data.status === 'unknown' ? 'Delivery unconfirmed' : readString(data.message);
      continue;
    }
    if (nativeTurns.has(turnKey(event)) && (event.type === 'message.delta' ||
      (['message.accepted', 'message.started', 'message.completed'].includes(event.type) && messageRole(event) === 'assistant'))) continue;


    if (event.type === 'turn.accepted' && !explicitUserTurns.has(turnKey(event))) {
      const text = readString(data.message) ?? readString(data.text);
      const attachments = readStringArray(data.attachments);
      // Missing historical input is absence of evidence, never invented prose.
      if (text || attachments.length) items.push({
        key: event.eventId, kind: 'message', role: 'user', status: 'accepted',
        title: 'User', timestamp: event.timestamp, eventId: event.eventId,
        eventType: event.type, turnId: event.turnId, text,
        ...(attachments.length ? { attachments } : {})
      });
      continue;
    }

    if (
      event.type === 'message.accepted' ||
      event.type === 'message.queued' ||
      event.type === 'message.started' ||
      event.type === 'message.completed'
    ) {
      const role = messageRole(event);
      const text = readString(data.text) ?? readString(data.message);
      items.push({
        key: event.eventId,
        kind: 'message',
        role,
        status: messageStatus(event.type),
        title: role === 'assistant' ? 'Assistant' : 'User',
        timestamp: event.timestamp,
        eventId: event.eventId,
        eventType: event.type,
        turnId: event.turnId,
        text,
        ...(role === 'user' ? { attachments: readStringArray(data.attachments).length
          ? readStringArray(data.attachments) : acceptedAttachments.get(turnKey(event)) ?? [] } : {}),
        summary: text ? undefined : event.type
      });
      continue;
    }

    if (event.type === 'message.delta') {
      if (assistantCompletionKeys.has(turnKey(event))) {
        continue;
      }
      const text = readString(data.text);
      if (!text) {
        continue;
      }
      const key = `assistant-delta:${turnKey(event)}`;
      const existing = deltaItems.get(key);
      if (existing) {
        existing.text = `${existing.text ?? ''}${text}`;
        existing.eventId = event.eventId;
        existing.timestamp = event.timestamp;
      } else {
        const item: TranscriptItem = {
          key,
          kind: 'message',
          role: 'assistant',
          status: 'started',
          title: 'Assistant',
          timestamp: event.timestamp,
          eventId: event.eventId,
          eventType: event.type,
          turnId: event.turnId,
          text
        };
        deltaItems.set(key, item);
        items.push(item);
      }
      continue;
    }

    if (event.type === 'tool.completed' || event.type === 'tool.failed') {
      const toolName = readString(data.toolName) ?? readString(data.adapterToolName) ?? 'tool';
      const artifact = artifactLink(data);
      items.push({
        key: event.eventId,
        kind: 'tool',
        status: event.type === 'tool.failed' ? 'failed' : 'completed',
        title: toolName,
        timestamp: event.timestamp,
        eventId: event.eventId,
        eventType: event.type,
        turnId: event.turnId,
        toolName,
        summary: readString(data.summary) ?? summarizeToolResult(data),
        artifact
      });
      continue;
    }

    const status = terminalStatus(event.type);
    if (status) {
      currentTerminalStatus = status;
      items.push({
        key: event.eventId,
        kind: 'terminal',
        status,
        title: `Turn ${status}`,
        timestamp: event.timestamp,
        eventId: event.eventId,
        eventType: event.type,
        turnId: event.turnId,
        summary: terminalSummary(event),
        ...(readString(data.reason) ? { terminalReason: readString(data.reason) } : {})
      });
      continue;
    }

    if (event.type === 'runtime.mirror.error') {
      items.push({
        key: event.eventId,
        kind: 'diagnostic',
        status: 'diagnostic',
        title: 'Replay diagnostic',
        timestamp: event.timestamp,
        eventId: event.eventId,
        eventType: event.type,
        turnId: event.turnId,
        summary: readString(data.error) ?? readString(data.message) ?? event.type
      });
    }
  }

  return {
    sessionId: session?.sessionId ?? events[0]?.sessionId,
    itemCount: items.length,
    items,
    terminalStatus: currentTerminalStatus,
    sdkLinkage: deriveSdkLinkage(session)
  };
}
