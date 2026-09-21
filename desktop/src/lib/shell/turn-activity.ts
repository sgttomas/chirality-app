import { deriveNativeProgress, nativeNotification, type NativeChecklist } from './native-progress';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import type { TranscriptItem } from '@chirality/runtime-contracts/transcript-replay';
import { actionSentence, taskSentence } from './activity-sentences';
import { deriveCodexNotifications, deriveSubagentActivity, deriveToolActivity, type ToolActivityStatus } from './harness-event-views';

/**
 * The compact activity a turn shows in the conversation: tool use, subagent
 * tasks and completed reasoning summaries, in observation order. Pure and
 * DOM-free so the live stream and a resumed transcript derive to the same
 * rows. Reasoning rows carry only the summary text Codex published as a
 * completed reasoning item; nothing here claims access to full internal
 * reasoning.
 */
export type TurnActivityKind = 'tool' | 'subagent' | 'reasoning';
export type TurnActivityStatus = ToolActivityStatus | 'waiting' | 'interrupted' | 'unknown';

export type TurnActivityItem = {
  key: string;
  kind: TurnActivityKind;
  status: TurnActivityStatus;
  /** Fixed sentence for the row (never a generated narrative). */
  title: string;
  /** Recorded summary carried by the adapter (command line, file list, reasoning summary). */
  detail?: string;
  timestamp: string;
};

export type TurnActivity = {
  items: TurnActivityItem[];
  checklists?: NativeChecklist[];
  running: number;
  failed: number;
  pendingApproval: number;
};

const EMPTY: TurnActivity = { items: [], running: 0, failed: 0, pendingApproval: 0 };

function finish(items: TurnActivityItem[], order?: Map<string, number>): TurnActivity {
  if (items.length === 0) return EMPTY;
  // Rows read in the order the reader first saw them, like the Activity view;
  // a row's own timestamp is its latest event, which would reorder as tools finish.
  if (order) items.sort((left, right) => (order.get(left.key) ?? Number.MAX_SAFE_INTEGER) - (order.get(right.key) ?? Number.MAX_SAFE_INTEGER));
  else items.sort((left, right) => left.timestamp.localeCompare(right.timestamp));
  return {
    items,
    running: items.filter(item => item.status === 'running' || item.status === 'queued').length,
    failed: items.filter(item => item.status === 'failed').length,
    pendingApproval: items.filter(item => item.status === 'permission').length
  };
}

function clip(text: string | undefined, limit = 240): string | undefined {
  if (!text) return undefined;
  const line = text.trim().split('\n').find(candidate => candidate.trim()) ?? '';
  return line.length > limit ? `${line.slice(0, limit - 1)}…` : line || undefined;
}

/**
 * Activity for one turn from the bridged event stream. With a `turnId` only
 * that turn's events count; without one the whole buffer is the turn (the
 * panel clears the buffer when it starts a turn, so this is the streaming case
 * before the Runtime has named the turn).
 */
export function deriveTurnActivityFromEvents(events: readonly HarnessEvent[], turnId?: string): TurnActivity {
  const scoped = turnId ? events.filter(event => event.turnId === turnId) : events;
  if (scoped.length === 0) return EMPTY;
  const order = new Map<string, number>();
  scoped.forEach((event, index) => {
    const data = event.data ?? {};
    const text = (value: unknown): string | undefined => typeof value === 'string' && value ? value : undefined;
    const keys = event.type.startsWith('tool.') ? [`tool:${text(data.toolUseId) ?? text(data.adapterToolUseId) ?? event.eventId}`]
      : event.type.startsWith('subagent.') ? [`subagent:${text(data.taskId) ?? text(data.childRunId) ?? text(data.toolUseId) ?? event.eventId}`]
      : event.type === 'codex.notification' ? [`reasoning:${event.eventId}`] : [];
    for (const key of keys) if (!order.has(key)) order.set(key, index);
  });
  const items: TurnActivityItem[] = [];
  for (const row of deriveToolActivity(scoped)) {
    items.push({ key: `tool:${row.key}`, kind: 'tool', status: row.status, title: actionSentence(row), detail: clip(row.summary), timestamp: row.timestamp });
  }
  for (const row of deriveSubagentActivity(scoped)) {
    items.push({ key: `subagent:${row.key}`, kind: 'subagent', status: row.observationEnded ? 'unknown' : row.status, title: `${taskSentence(row)}${row.observationEnded ? ' (last observed)' : ''}`, detail: [row.description, row.summary, row.observationEnded].filter(Boolean).join('\n\n') || undefined, timestamp: row.timestamp });
  }
  // Retained older streams may omit native IDs; their supplied summaries stay readable.
  for (const row of deriveCodexNotifications(scoped.filter(event => { const n = nativeNotification(event); return !n?.threadId || !n.turnId; }))) {
    if (row.kind === 'thinking' && row.text?.trim()) items.push({ key: `reasoning:${row.key}`, kind: 'reasoning', status: 'completed', title: 'Reasoning summary', detail: row.text, timestamp: row.timestamp });
  }
  const native = deriveNativeProgress(scoped);
  for (const row of native.summaries) {
    if (!row.text.trim()) continue;
    items.push({ key: `reasoning:${row.key}`, kind: 'reasoning', status: row.completed ? 'completed' : 'running', title: 'Reasoning summary', detail: row.text, timestamp: row.timestamp });
  }
  return { ...finish(items, order), checklists: native.checklists };

}

const TRANSCRIPT_STATUS: Partial<Record<TranscriptItem['status'], ToolActivityStatus>> = {
  accepted: 'queued', queued: 'queued', started: 'running', completed: 'completed', failed: 'failed', cancelled: 'failed', interrupted: 'failed'
};

/** Activity for one recorded turn from the transcript projection's tool items. */
export function deriveTurnActivityFromTranscript(items: readonly TranscriptItem[], turnId: string | undefined): TurnActivity {
  if (!turnId) return EMPTY;
  const rows: TurnActivityItem[] = [];
  for (const item of items) {
    if (item.kind !== 'tool' || item.turnId !== turnId) continue;
    const status = TRANSCRIPT_STATUS[item.status] ?? 'completed';
    rows.push({ key: `transcript:${item.key}`, kind: 'tool', status, title: actionSentence({ toolName: item.toolName ?? 'tool', status }), detail: clip(item.summary ?? (item.title !== item.toolName ? item.title : undefined)), timestamp: item.timestamp });
  }
  return finish(rows);
}

/** One line for the collapsed disclosure. Counts describe observed rows, never complete work. */
export function summarizeTurnActivity(activity: TurnActivity, running: boolean): string {
  const count = activity.items.length;
  const actions = `${count} ${count === 1 ? 'action' : 'actions'}`;
  const failed = activity.failed ? ` · ${activity.failed} failed` : '';
  if (running) {
    const latest = [...activity.items].reverse().find(item => item.status === 'running' || item.status === 'permission') ?? activity.items.at(-1);
    const lead = latest?.title ?? 'Working';
    return count ? `${lead} · ${actions}${failed}` : 'Working';
  }
  return `Turn details · ${actions}${failed}`;
}
