import { useEffect, useRef, useState, type ReactNode } from "react";
import { WorkspaceDisclosure } from "./DailyWorkspace";
import { FleetSourceRecords, FleetWorkspace, readFleetPacket, type FleetPacket } from "./FleetRecordsPanel";

type Json = any;

/** Delay between the end of one read and the start of the next while the
 * view is shown. Each read rebuilds the whole fleet folder and reads the
 * decision packages and the records store, so reads never overlap and the
 * next one waits a full interval after the last finishes. */
export const DELEGATED_WORK_REREAD_MS = 10_000;

/** One read of the two read-only host commands; nothing of its own is kept. */
export type DelegatedWorkRead = {
  reading: boolean;
  /** When the last read finished; null before the first. */
  readAt: number | null;
  fleet: FleetPacket | null; fleetError: string;
  decisions: Json; decisionError: string;
};
export const UNREAD: DelegatedWorkRead = { reading: false, readAt: null, fleet: null, fleetError: "", decisions: null, decisionError: "" };

type Timers = { set: (run: () => void, ms: number) => unknown; clear: (timer: unknown) => void };
const browserTimers: Timers = { set: (run, ms) => setTimeout(run, ms), clear: timer => clearTimeout(timer as ReturnType<typeof setTimeout>) };

/** Reads while shown: once on show, then again an interval after each read
 * ends, never two at once, and none scheduled while hidden. A read sends only
 * the two read-only commands; a failed part replaces its earlier result. */
export function createDelegatedWorkReader({ invoke, publish, intervalMs = DELEGATED_WORK_REREAD_MS, now = Date.now, timers = browserTimers }: {
  invoke: (command: string) => Promise<Json>; publish: (read: DelegatedWorkRead) => void;
  intervalMs?: number; now?: () => number; timers?: Timers;
}) {
  let shown = false, reading = false, timer: unknown = null, state = UNREAD;
  const cancel = () => { if (timer !== null) { timers.clear(timer); timer = null; } };
  const read = async () => {
    if (reading) return;
    cancel();
    reading = true; publish(state = { ...state, reading: true });
    const [fleet, decisions] = await Promise.allSettled([readFleetPacket(invoke), invoke("decision_view")]);
    reading = false;
    publish(state = {
      reading: false, readAt: now(),
      fleet: fleet.status === "fulfilled" ? fleet.value : null, fleetError: fleet.status === "rejected" ? String(fleet.reason) : "",
      decisions: decisions.status === "fulfilled" ? decisions.value : null, decisionError: decisions.status === "rejected" ? String(decisions.reason) : "",
    });
    if (shown && timer === null) timer = timers.set(() => { timer = null; void read(); }, intervalMs);
  };
  return {
    show() { if (shown) return; shown = true; void read(); },
    hide() { shown = false; cancel(); },
    readNow: () => read(),
  };
}

/** The view's reads, driven by whether it is shown. */
export function useDelegatedWork(shown: boolean, invoke: (command: string) => Promise<Json>, options: { intervalMs?: number; now?: () => number; timers?: Timers } = {}) {
  const [read, setRead] = useState<DelegatedWorkRead>(UNREAD);
  const reader = useRef<ReturnType<typeof createDelegatedWorkReader> | null>(null);
  if (!reader.current) reader.current = createDelegatedWorkReader({ ...options, invoke, publish: setRead });
  useEffect(() => {
    const current = reader.current!;
    if (shown) current.show(); else current.hide();
    return () => current.hide();
  }, [shown]);
  return { read, readNow: () => reader.current!.readNow() };
}

/** What keeps the last read from being complete, from the read's own fields. */
export function readLimits(read: DelegatedWorkRead): string[] {
  const limits: string[] = [];
  if (read.fleetError) limits.push(`the fleet records could not be read (${read.fleetError})`);
  else if (read.fleet) {
    if (read.fleet.limits.length > 0) limits.push(`${read.fleet.limits.length} part(s) of the fleet records could not be read or established; see Source records below`);
    if (!read.fleet.workspace) limits.push("the fleet records carry no derived work view");
    for (const view of read.fleet.workspace?.undertakings ?? []) {
      if (!view.graph) limits.push(`undertaking ${view.undertaking} has no current graph established`);
      else if (!view.currentGraphEstablished) limits.push(`the current graph of undertaking ${view.undertaking} is not established`);
      if (!view.queueComplete) limits.push(`the return-review queue of undertaking ${view.undertaking} is incomplete`);
    }
  }
  if (read.decisionError) limits.push(`the decision packages could not be read (${read.decisionError})`);
  else if (read.decisions?.error) limits.push(`the decision packages could not be read (${read.decisions.error})`);
  else if ((read.decisions?.limits ?? []).length > 0) limits.push(`the decision view states ${read.decisions.limits.length} limit(s); see Decision packages below`);
  return limits;
}

const time = (ms: number) => new Date(ms).toLocaleTimeString();

/** Follow delegated work: each undertaking's selected work and its return
 * queue, then the decision packages, all read from the project's files. */
export function DelegatedWorkView({ read, readNow, decisionPackages }: {
  read: DelegatedWorkRead; readNow: () => void;
  /** The existing decision packages panel, given the view's decision read. */
  decisionPackages: (view: Json) => ReactNode;
}) {
  const limits = read.readAt === null ? [] : readLimits(read);
  const failures = (read.fleetError !== "" ? 1 : 0) + (read.decisionError !== "" ? 1 : 0);
  const failed = failures > 0;
  return <section aria-label="Delegated work">
    <h2>Delegated work</h2>
    <p>Follow work handed to other agents: what each piece is waiting on, what has come back for you to examine, and the decisions prepared for you. Everything here is read from the project's files while this view is open and re-read every {DELEGATED_WORK_REREAD_MS / 1000} seconds; reading writes nothing and performs no act.</p>
    <p role="status" aria-live="polite">
      {read.readAt === null ? (read.reading ? "Reading the project's delegated work…" : "Not read yet.")
        : <>Last read at {time(read.readAt)}: {limits.length === 0 ? "complete." : <>{failures === 2 ? "failed" : failed ? "failed in part" : "incomplete"}.</>}{read.reading ? " Reading again…" : ""}</>}
    </p>
    {limits.length > 0 && <div role={failed ? "alert" : undefined}><p>This read is not complete:</p><ul>{limits.map((limit, i) => <li key={i}>{limit}</li>)}</ul></div>}
    <p><button onClick={readNow} disabled={read.reading}>{read.reading ? "Reading…" : "Read again now"}</button></p>
    {read.fleetError ? <p role="alert">Fleet read failed: {read.fleetError}. No earlier reading of the work and returns is shown.</p>
      : read.fleet?.workspace ? <FleetWorkspace workspace={read.fleet.workspace}/>
      : read.fleet ? <p>The fleet records carry no derived work view.</p> : null}
    <WorkspaceDisclosure id="delegated-decisions" title="Decision packages" description="Matters prepared for you to decide or accept, and the decisions recorded" open>
      <p>Opening the act control shows it at the top of this window. Only the confirmation the App then shows records a decision.</p>
      {decisionPackages(read.decisionError ? { error: `Decision read failed: ${read.decisionError}. No earlier reading of the decision packages is shown.` } : read.decisions)}
    </WorkspaceDisclosure>
    <WorkspaceDisclosure id="delegated-sources" title="Source records" description="Counts, store state, native conversation links, source limits and the complete fleet packet">
      {read.fleet ? <FleetSourceRecords packet={read.fleet}/> : <p>{read.fleetError ? "The last read failed; no source records are shown." : "Not read yet."}</p>}
    </WorkspaceDisclosure>
  </section>;
}

/** The act names of DEL-04-01, so a package's requested act reads in words. */
const ACT_NAMES: Record<string, string> = {
  A4: "mark checked", A5: "accept", A6: "approve (engineering approval)", A7: "rely (professional reliance)",
  A10: "reject", A12: "set grant", A13: "enable external access, or disable it", A15: "register workflow revision", A16: "decide",
};
export function actName(kind: unknown): string {
  const code = typeof kind === "string" ? kind : String(kind ?? "act not stated");
  return ACT_NAMES[code] ? `${ACT_NAMES[code]} (${code})` : code;
}
