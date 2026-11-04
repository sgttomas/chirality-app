import { useSyncExternalStore } from "react";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

/**
 * Bring-back sends the host could not confirm (any refusal without
 * `prefillKept: true`: an unknown outcome, a transcript sent without its
 * observation written, a lost pre-fill). The host withdraws the pre-fill, so
 * its composer and outcome would vanish; this keeps them for the life of this
 * App window (not across relaunch, and not native or global deduplication).
 *
 * While a doubt is held, every preparation and send of the same trial or run
 * to the same recorded conversation ID is refused at dispatch (`bringBackRefusal`), so no
 * control, earlier or current, can repeat it. Only the person's explicit
 * acknowledgement lifts it: no existing record correlates a later brought-back
 * row with this original request and full target, so none is taken as
 * evidence. Acknowledging starts nothing, and the original outcome stays
 * shown. The host's message is kept as given and never parsed.
 *
 * The hold follows the original conversation ID across a Codex restart or home
 * change: a source change never resolves or erases it. Matching an ID only
 * blocks a blind retry; it never makes the old destination the current one.
 * A different, explicitly chosen conversation ID is not held.
 */
export type BringBackDoubt = {
  kind: "trial" | "run"; ref: string; sequence: Json; draftName: Json; preparedId: string;
  source: { sourceRef: Json; modeHomeClass: Json; generation: Json };
  target: { generation: Json; threadId: Json }; personText: string; message: string; acknowledged: boolean;
};
let doubts: BringBackDoubt[] = [];
const listeners = new Set<() => void>();
const emit = () => { for (const listener of listeners) listener(); };
const sameTarget = (a: Json, b: Json) => JSON.stringify([a?.generation ?? null, a?.threadId ?? null]) === JSON.stringify([b?.generation ?? null, b?.threadId ?? null]);
/** The hold's match: the recorded conversation ID, in any generation or home. */
const sameConversationId = (a: Json, b: Json) => typeof a?.threadId === "string" && !!a.threadId && a.threadId === b?.threadId;

export function noteBringBackDoubt(doubt: BringBackDoubt): void {
  // Every original attempt is kept; a later one never replaces an earlier outcome.
  doubts = [...doubts.filter(row => !(row.kind === doubt.kind && row.ref === doubt.ref && row.preparedId === doubt.preparedId && sameTarget(row.target, doubt.target))), doubt];
  emit();
}
/** Where the original send went, compared with a conversation shown now. */
export function doubtDestination(doubt: BringBackDoubt, current: Json): "same" | "same-id-other-source" | "other" {
  if (!sameConversationId(doubt.target, current)) return "other";
  return sameTarget(doubt.target, current) ? "same" : "same-id-other-source";
}
export function acknowledgeBringBackDoubt(doubt: BringBackDoubt): void {
  doubts = doubts.map(row => row === doubt ? { ...row, acknowledged: true } : row);
  emit();
}
/** The doubts for one trial or run (to any conversation), newest last. */
export function bringBackDoubtsFor(kind: "trial" | "run", ref: string, list = doubts): BringBackDoubt[] {
  return list.filter(row => row.kind === kind && row.ref === ref);
}
/** Whether bringing `ref` back to `target` must be refused now, read at the press. */
export function bringBackHeld(kind: "trial" | "run", ref: string, target: Json): BringBackDoubt | null {
  return doubts.find(row => row.kind === kind && row.ref === ref && sameConversationId(row.target, target) && !row.acknowledged) ?? null;
}
export function useBringBackDoubts(): BringBackDoubt[] {
  return useSyncExternalStore(listener => { listeners.add(listener); return () => { listeners.delete(listener); }; }, () => doubts, () => doubts);
}
/** The App window's end (and test isolation). */
export function resetBringBackDoubts(): void { doubts = []; emit(); }

/**
 * The dispatch guard for every bring-back preparation and send, read against
 * the host's CURRENT view at the call (not a rendered control): a held doubt
 * for the same trial or run and conversation refuses both; an identical
 * prepared message (same trial or run, conversation and options) refuses a
 * new preparation; a send of the same trial or run to the same conversation
 * already in flight refuses another. Returns the refusal, or null.
 */
export function bringBackRefusal(command: string, args: Record<string, unknown>, host: Json): string | null {
  const pending: Json[] = Array.isArray(host?.workflowRoot?.pendingBringBacks) ? host.workflowRoot.pendingBringBacks : [];
  const target = { generation: args.generation ?? null, threadId: args.threadId ?? null };
  if (command === "workflow_trial_bring_back" || command === "workflow_run_bring_back") {
    const kind = command === "workflow_trial_bring_back" ? "trial" : "run";
    const ref = String((kind === "trial" ? args.reference : args.runRef) ?? "");
    if (bringBackHeld(kind, ref, target)) return "Not prepared: an earlier send of these results to that conversation wasn't confirmed and may have arrived. Check the conversation, then confirm you checked.";
    if (pending.some(row => (kind === "trial" ? row?.trial : row?.run) === ref && sameTarget(row?.target, target) && !!row?.includeNative === !!args.includeNative))
      return "Not prepared again: these results are already prepared for that conversation. Read and send them there.";
    return null;
  }
  if (command === "workflow_bring_back_send") {
    // A retained Send of a message whose send was unconfirmed (and withdrawn) is never repeated.
    if (doubts.some(doubt => doubt.preparedId === String(args.id))) return "Not sent: this message's earlier send wasn't confirmed and may have arrived; it was withdrawn and is not sent again.";
    const row = pending.find(entry => entry?.id === args.id);
    const kind = typeof row?.trial === "string" && row.trial ? "trial" : typeof row?.run === "string" && row.run ? "run" : null;
    if (!kind) return null;
    const ref = kind === "trial" ? row.trial : row.run;
    if (bringBackHeld(kind, ref, target)) return "Not sent: an earlier send of these results to this conversation wasn't confirmed and may have arrived. Read the conversation, then confirm you checked.";
    if (inFlight.has(sendKey(kind, ref, target))) return "Not sent: these results are being sent to this conversation now.";
    return null;
  }
  return null;
}
/** One send of a trial's or run's results to one conversation ID at a time. */
export const sendKey = (kind: "trial" | "run", ref: string, target: Json) => JSON.stringify(["send", kind, ref, target?.threadId ?? null]);

/** A synchronous guard for one press until its command settles. */
const inFlight = new Set<string>();
export function beginBringBack(key: string): boolean { if (inFlight.has(key)) return false; inFlight.add(key); return true; }
export function endBringBack(key: string): void { inFlight.delete(key); }
