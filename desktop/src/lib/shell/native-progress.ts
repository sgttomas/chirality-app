import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';

export const record = (value: unknown): Record<string, unknown> => value && typeof value === 'object' && !Array.isArray(value) ? value as Record<string, unknown> : {};
const text = (value: unknown): string | undefined => typeof value === 'string' ? value : undefined;
export type NativeChecklist = { key: string; explanation?: string; steps: { step: string; status: 'pending' | 'inProgress' | 'completed' }[] };
export type NativeSummary = { key: string; text: string; timestamp: string; completed: boolean };

/** Native identity always comes from params, never the parent Runtime routing envelope. */
export function nativeNotification(event: HarnessEvent) {
  if (event.type !== 'codex.notification') return undefined;
  const data = event.data ?? {};
  const params = record(data.params);
  const thread = record(params.thread);
  const turn = record(params.turn);
  const threadId = text(params.threadId) ?? text(thread.id);
  const turnId = text(params.turnId) ?? text(turn.id);
  return { method: text(data.method), params, threadId, turnId, item: record(params.item) };
}

export function deriveNativeProgress(events: readonly HarnessEvent[]): { checklists: NativeChecklist[]; summaries: NativeSummary[] } {
  const plans = new Map<string, NativeChecklist>();
  const summaries = new Map<string, NativeSummary>();
  const seen = new Set<string>();
  for (const event of events) {
    if (seen.has(event.eventId)) continue;
    seen.add(event.eventId);
    const n = nativeNotification(event);
    if (!n?.threadId || !n.turnId) continue;
    const scope = `${event.sessionId}:${n.threadId}:${n.turnId}`;
    if (n.method === 'turn/plan/updated' && Array.isArray(n.params.plan)) {
      plans.set(scope, { key: scope, explanation: text(n.params.explanation), steps: n.params.plan.flatMap(value => {
        const row = record(value);
        return typeof row.step === 'string' && ['pending', 'inProgress', 'completed'].includes(String(row.status))
          ? [{ step: row.step, status: row.status as 'pending' | 'inProgress' | 'completed' }] : [];
      }) });
    }
    const id = text(n.params.itemId) ?? text(n.item.id);
    if (!id) continue;
    const base = `${scope}:${id}`;
    if (n.method === 'item/reasoning/summaryTextDelta' && typeof n.params.delta === 'string') {
      const key = `${base}:${n.params.summaryIndex ?? 0}`;
      const old = summaries.get(key);
      if (!old?.completed) summaries.set(key, { key, text: (old?.text ?? '') + n.params.delta, timestamp: event.timestamp, completed: false });
    }
    if (n.method === 'item/completed' && n.item.type === 'reasoning' && Array.isArray(n.item.summary)) {
      for (const key of summaries.keys()) if (key.startsWith(`${base}:`)) summaries.delete(key);
      n.item.summary.forEach((value, index) => {
        if (typeof value === 'string') {
          const key = `${base}:${index}`;
          summaries.set(key, { key, text: value, timestamp: event.timestamp, completed: true });
        }
      });
    }
  }
  return { checklists: [...plans.values()], summaries: [...summaries.values()] };
}
