import { useSyncExternalStore } from "react";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

/**
 * Bring-back sends the host could not confirm (any refusal without
 * `prefillKept: true`: an unknown outcome, a transcript sent without its
 * observation written, a lost pre-fill). The host withdraws the pre-fill, so
 * its composer and outcome would vanish; this keeps them for the life of this
 * App window (not across relaunch, and not native or global deduplication).
 *
 * While a doubt is held, every entry point that would bring the same trial or
 * run back to the same conversation refuses at the press. Only the host's own
 * record (a trial row's brought-back count rising) or the person's explicit
 * acknowledgement lifts it; both start nothing, and the original outcome stays
 * shown. The host's message is kept as given and never parsed.
 */
export type BringBackDoubt = {
  kind: "trial" | "run"; ref: string; sequence: Json; draftName: Json; preparedId: string;
  source: { sourceRef: Json; modeHomeClass: Json; generation: Json };
  target: { generation: Json; threadId: Json }; personText: string; message: string;
  /** The trial row's recorded bring-backs before the send. */
  brought: number; acknowledged: boolean;
};
let doubts: BringBackDoubt[] = [];
const listeners = new Set<() => void>();
const emit = () => { for (const listener of listeners) listener(); };
const sameTarget = (a: Json, b: Json) => JSON.stringify([a?.generation ?? null, a?.threadId ?? null]) === JSON.stringify([b?.generation ?? null, b?.threadId ?? null]);

export function noteBringBackDoubt(doubt: BringBackDoubt): void {
  doubts = [...doubts.filter(row => !(row.kind === doubt.kind && row.ref === doubt.ref && sameTarget(row.target, doubt.target))), doubt];
  emit();
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
export function bringBackHeld(kind: "trial" | "run", ref: string, target: Json, brought?: number): BringBackDoubt | null {
  return doubts.find(row => row.kind === kind && row.ref === ref && sameTarget(row.target, target) && !row.acknowledged
    && !(kind === "trial" && typeof brought === "number" && brought > row.brought)) ?? null;
}
/** Whether a held doubt is resolved by the host's own record. */
export const resolvedByRecord = (doubt: BringBackDoubt, brought?: number) => doubt.kind === "trial" && typeof brought === "number" && brought > doubt.brought;
export function useBringBackDoubts(): BringBackDoubt[] {
  return useSyncExternalStore(listener => { listeners.add(listener); return () => { listeners.delete(listener); }; }, () => doubts, () => doubts);
}
/** The App window's end (and test isolation). */
export function resetBringBackDoubts(): void { doubts = []; emit(); }

/** A synchronous guard for one press until its command settles. */
const inFlight = new Set<string>();
export function beginBringBack(key: string): boolean { if (inFlight.has(key)) return false; inFlight.add(key); return true; }
export function endBringBack(key: string): void { inFlight.delete(key); }
