import { useCallback, useRef, useState } from "react";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

/** One read of the host's status: its place in the order reads were started, and the reply. */
export type HostRead = { index: number; snapshot: Json };

/** What a view needs to say whether the status it shows was read after a press settled. */
export type HostReads = {
  /** How many status reads have been started so far. A read started later has a larger index. */
  started: () => number;
  /** The index of the read whose reply is the status now shown; 0 before any. */
  applied: number;
};

/**
 * The host's status as the web view holds it, with its reads in order.
 *
 * Every status read is numbered when it starts: the caller starts the read and
 * hands its pending reply to `readHost` in the same statement, as
 * `readHost(invoke("host_status"))`. A reply is applied only
 * if its read started after the one whose reply is shown. So the view never
 * applies an older read over a newer one, whatever order the replies arrive
 * in. That is all this establishes: it does not say a reply is complete, or
 * that nothing changed in the host after it was read.
 */
export function useOrderedHost(): { host: Json; hostReads: HostReads; readHost: (reply: Promise<Json>) => Promise<HostRead>; applyHost: (read: HostRead) => boolean } {
  const [shown, setShown] = useState<{ host: Json; applied: number }>({ host: null, applied: 0 });
  const order = useRef({ started: 0, applied: 0 });
  const readHost = useCallback(async (reply: Promise<Json>): Promise<HostRead> => {
    // Numbered before the first await, so in the order the reads were started.
    const index = ++order.current.started;
    return { index, snapshot: await reply };
  }, []);
  const applyHost = useCallback((read: HostRead): boolean => {
    if (read.index <= order.current.applied) return false;
    order.current.applied = read.index;
    setShown({ host: read.snapshot, applied: read.index });
    return true;
  }, []);
  const started = useCallback(() => order.current.started, []);
  return { host: shown.host, hostReads: { started, applied: shown.applied }, readHost, applyHost };
}

/**
 * Whether the status shown may be from before a press: true until a read that
 * started after the press settled has been applied. `settledAt` is the number
 * of reads started when the press settled; null when no press has settled.
 */
export function shownBeforePress(settledAt: number | null, reads: HostReads | undefined): boolean {
  return settledAt !== null && !!reads && reads.applied <= settledAt;
}
