import { useCallback, useEffect, useRef, useState } from "react";
import { invoke as platformInvoke, type InvokeArgs, type InvokeOptions } from "@tauri-apps/api/core";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

/** The host's status command. Its reads are numbered; it never marks a press. */
const STATUS = "host_status";

/**
 * What this module establishes about a command, stated as far as it holds:
 *
 * After a command whose own effect could change what the guides show settles,
 * both guides are withheld until a status read started after it has been
 * applied. One exception: while a press made in the workflow panel is still
 * in progress, the steps from before it stay on screen with every control
 * disabled, the panel announced as busy and the press's result not yet said;
 * once that press is no longer in progress, whichever way its refresh ended,
 * the rule applies. A command issued outside the panel withholds at once. If
 * the refresh after a press neither resolves nor rejects, the earlier steps
 * stay on screen, disabled and marked busy, for as long as it hangs.
 *
 * What the host learns by itself is not a command's effect: a notification
 * from Codex, a turn ending, or a reply write that finished and that the host
 * reconciles the next time anything observes it, the status read included.
 * The view follows those at the next status read that succeeds and is
 * applied, as it always has. The App starts one every POLL_MS, which is a
 * schedule and not a bound: a read that fails leaves the previous view in
 * place, and the guides then say that their last read failed.
 *
 * So every command marks when it settles, except the ones below. They are the
 * commands the web view issues by itself (on a timer, or from an effect that
 * re-runs with nothing pressed), where marking would withhold the guides with
 * nobody having done anything. Each is recorded with its host function's own
 * effect, read from the host's code. A command a person presses is never
 * listed, whatever it does: it marks, which costs one status read. A command
 * added later marks until someone reads its host function and lists it.
 */
export const POLL_MS = 1000;
export const SELF_ISSUED_QUIET: Readonly<Record<string, string>> = {
  checkpoint_native_waiting_ui: "the waiting-navigation registry only, which neither guide shows",
  claim_native_waiting_intent: "claim ownership in the waiting-navigation registry; reconciliation only",
  decision_view: "reads the decision projection; where the records store was not opened at startup, opening it can create the store's folder and store.json; neither guide shows either",
  finish_native_waiting_intent: "the waiting-navigation registry only, which neither guide shows",
  host_observe: "queues an observer reconstruction kept apart from live activity; reconciliation only",
  native_confirmation_content: "none",
  workflow_review_digest: "none",
};

const settleListeners = new Set<() => void>();

/**
 * The web view's command function: the platform's, and when a command other
 * than the status read or one listed above settles, either way, every mounted
 * status holder is told. The telling is attached before the caller's own
 * continuation, so a status read the caller starts afterwards is numbered
 * after the mark.
 */
export function invoke<T = Json>(command: string, args?: InvokeArgs, options?: InvokeOptions): Promise<T> {
  const pending = platformInvoke<T>(command, args, options);
  if (command !== STATUS && !Object.hasOwn(SELF_ISSUED_QUIET, command)) {
    const settled = () => { for (const tell of [...settleListeners]) tell(); };
    pending.then(settled, settled);
  }
  return pending;
}

/** One read of the host's status: its place in the order reads were started, and the reply. */
export type HostRead = { index: number; snapshot: Json };

/** What a view needs to say whether the status it shows was read after the last command settled. */
export type HostReads = {
  /** How many status reads have been started so far. A read started later has a larger index. */
  started: () => number;
  /** The index of the read whose reply is the status now shown; 0 before any. */
  applied: number;
  /** How many status reads had been started when the last marking command settled; null before any. */
  settledAt: number | null;
  /** The message of a status read that failed, while no read started after it has been applied. */
  failure: string | null;
};

type Shown = { host: Json; applied: number; settledAt: number | null; failed: { index: number; message: string } | null };

/**
 * The host's status as the web view holds it, with its reads in order.
 *
 * Every status read is numbered when it starts: the caller starts the read and
 * hands its pending reply to `readHost` in the same statement, as
 * `readHost(invoke("host_status"))`. A reply is applied only
 * if its read started after the one whose reply is shown. So the view never
 * applies an older read over a newer one, whatever order the replies arrive
 * in. That is all the numbering establishes: it does not say a reply is
 * complete, or that nothing changed in the host after it was read.
 *
 * It also holds when the last command that may change the host settled (see
 * `invoke`), as the number of reads started by then.
 */
export function useOrderedHost(): { host: Json; hostReads: HostReads; readHost: (reply: Promise<Json>) => Promise<HostRead>; applyHost: (read: HostRead) => boolean } {
  const [shown, setShown] = useState<Shown>({ host: null, applied: 0, settledAt: null, failed: null });
  const order = useRef({ started: 0, applied: 0 });
  useEffect(() => {
    const tell = () => { const settledAt = order.current.started; setShown(old => ({ ...old, settledAt })); };
    settleListeners.add(tell);
    return () => { settleListeners.delete(tell); };
  }, []);
  const readHost = useCallback(async (reply: Promise<Json>): Promise<HostRead> => {
    // Numbered before the first await, so in the order the reads were started.
    const index = ++order.current.started;
    try { return { index, snapshot: await reply }; }
    catch (error) {
      setShown(old => (old.failed && old.failed.index > index ? old : { ...old, failed: { index, message: String(error) } }));
      throw error;
    }
  }, []);
  const applyHost = useCallback((read: HostRead): boolean => {
    if (read.index <= order.current.applied) return false;
    order.current.applied = read.index;
    setShown(old => ({ ...old, host: read.snapshot, applied: read.index }));
    return true;
  }, []);
  const started = useCallback(() => order.current.started, []);
  const failure = shown.failed && shown.failed.index > shown.applied ? shown.failed.message : null;
  return { host: shown.host, hostReads: { started, applied: shown.applied, settledAt: shown.settledAt, failure }, readHost, applyHost };
}

/**
 * Whether the status shown may be from before the last command that could
 * change the host: true until a read that started after that command settled
 * has been applied.
 */
export function shownBeforePress(reads: HostReads | undefined): boolean {
  return !!reads && reads.settledAt !== null && reads.applied <= reads.settledAt;
}
