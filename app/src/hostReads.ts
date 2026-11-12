import { useCallback, useEffect, useRef, useState } from "react";
import { invoke as platformInvoke, type InvokeArgs, type InvokeOptions } from "@tauri-apps/api/core";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

/** The host's status command. Its reads are numbered; it never marks a press. */
const STATUS = "host_status";

/**
 * The commands the web view issues that only read: closed, and tested as
 * closed. A command not listed here is taken to be able to change what the
 * host would report, so a command added later marks until someone lists it.
 * Listing a command that changes host state would let a view from before it
 * be shown as current; leaving a read off the list only withholds the guides
 * until the next status read.
 */
export const READ_COMMANDS: readonly string[] = [
  "collaboration_modes_read",
  "decision_view",
  "native_confirmation_content",
  "read_available_models",
  "read_configured_providers",
  "read_connector_routes",
  "read_effective_access_settings",
  "read_fleet_records",
  "read_home_access",
  "read_recovery_custody",
  "read_recovery_request_history",
  "role_supply_history",
  "workflow_review_digest",
];

const settleListeners = new Set<() => void>();

/**
 * The web view's command function: the platform's, and when a command other
 * than the status read or a listed read settles, either way, every mounted
 * status holder is told. The telling is attached before the caller's own
 * continuation, so a status read the caller starts afterwards is numbered
 * after the mark.
 */
export function invoke<T = Json>(command: string, args?: InvokeArgs, options?: InvokeOptions): Promise<T> {
  const pending = platformInvoke<T>(command, args, options);
  if (command !== STATUS && !READ_COMMANDS.includes(command)) {
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
