import type { ReactNode } from "react";
import { SuppliedId } from "./AgentText";
import { StopLabel } from "./NativeActivity";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Start, Stop and Restart Codex (DEL-01-04 §5.2; DEL-01-02 C-12, DEF-5a).
// Stop and Restart always ask first in the host's native question, which lists
// the live work in force; there is no way to stop Codex from here without it.
// A stop is the person's operational choice, not a recorded act. Turn labels
// come from the App's stop-request records (REC SR) or the host's outcome
// (TO-4 "interrupted by Stop Codex"), never from an interrupt acknowledgment.

const text = (v: unknown) => (v === null || v === undefined ? "" : typeof v === "string" ? v : JSON.stringify(v));
const list = (v: unknown): Json[] => (Array.isArray(v) ? v : []);

/** The App-owned home (REC H-acct / H-key) for an ACCESS home class. */
export const appHome = (cls: unknown): string | undefined => (cls === "account" ? "H-acct" : cls === "api-key" ? "H-key" : cls === "local-provider" ? "H-omlx" : undefined);

/** The App's stop label for a turn. First the newest stop-request record
 *  (REC SR, read back from the App ledger after a relaunch) for the turn in
 *  the given App-owned home; then the newest Stop Codex outcome of this App
 *  process that stopped Codex and names it. A refused stop gives no label
 *  (the turn kept running). The ledger is App-wide, so rows of another home
 *  are not matched. Generations are not matched: a turn read from history
 *  may come from an earlier generation. */
export function stopLabel(stops: Json, threadId: string | null | undefined, turnId: string | null | undefined, requests?: Json, home?: string): Json | null {
  if (!threadId || !turnId) return null;
  const recorded = list(requests?.records).filter((r: Json) => r?.threadId === threadId && r?.turnId === turnId && (!home || r?.home === home));
  if (recorded.length) return recorded[recorded.length - 1];
  const outcomes = list(stops?.outcomes).filter((o: Json) => o?.state === "stopped");
  for (let i = outcomes.length - 1; i >= 0; i--) {
    const turn = list(outcomes[i]?.turns).find((t: Json) => t?.threadId === threadId && t?.turnId === turnId && typeof t?.label === "string");
    if (turn) return turn;
  }
  return null;
}

const CAUSE: Record<string, string> = { "person-interrupt": "your interrupt", "codex-stop": "Stop or Restart Codex", quit: "quitting the App" };

/** REC SR: the stop requests the App recorded, this session's and earlier
 *  sessions' (from the App ledger), each with its label or reading. */
export function StopRequests({ requests }: { requests: Json }) {
  const rows = list(requests?.records);
  const limits = list(requests?.limits);
  if (!rows.length && !limits.length) return null;
  return <details aria-label="Recorded stop requests">
    <summary>Recorded stop requests ({rows.length})</summary>
    <ul>
      {rows.map((r: Json) => <li key={text(r.stopRequestId)}>
        Conversation {text(r.threadId)} · turn {text(r.turnId)} · {CAUSE[text(r.cause)] ?? text(r.cause)} at {text(r.requestedAt)}{r.earlierSession ? " (earlier App session)" : r.sourceSessionEnd === "not-established" ? " (another App session; its end is not established)" : ""}: {r.label ? <b>{text(r.label)}</b> : null}{r.label && r.labelDerived ? " (derived; not written)" : ""}{r.label ? ". " : ""}{text(r.reading)}{r.codexReported ? ` Codex reported: ${text(r.codexReported)}.` : ""}
        <br /><small>Record: {text(r.persistence)}.</small>
      </li>)}
      {limits.map((l: Json, i: number) => <li key={`limit${i}`}>Limit: {text(l)}</li>)}
    </ul>
    <p><small>{text(requests?.standing)}</small></p>
  </details>;
}

/** A stopped turn with no Stop Codex label: Codex was stopped, but the turn's
 *  interrupt was not written (not sent, or its write's outcome unknown) and
 *  Codex reported no end. The absent label then says nothing by itself; the
 *  turn's reading (process, turn status and interrupt kept apart), or else its
 *  stop-request record's reading, says what happened. Only a refused stop
 *  reads as Codex not stopped. */
export function noLabelReading(t: Json, outcome: Json): string {
  if (outcome?.state !== "stopped") return "no Stop Codex label (Codex was not stopped)";
  return text(t?.reading) || text(t?.stopRequest?.reading) || "no Stop Codex label; no reading was reported for this turn";
}

export function StopOutcome({ outcome }: { outcome: Json }) {
  const turns = list(outcome?.turns);
  const runs = list(outcome?.runsInForce?.rows);
  return <div role="status" aria-label="Stop Codex outcome" style={{ border: "1px solid #bbb", padding: 8, margin: "8px 0" }}>
    <p><b>{text(outcome?.action) || "Stop Codex"}</b> confirmed by you at {text(outcome?.confirmedAt) || "time not reported"} · home {text(outcome?.modeHomeClass) || "not reported"} · {outcome?.state === "stopped" ? "Codex stopped" : `Codex not stopped: ${text(outcome?.stop?.reading) || "reason not reported"}`}.</p>
    {turns.length === 0 ? <p>No live turn was observed, so no interrupt was sent.</p> : <ul>
      {turns.map((t: Json) => <li key={`${text(t.threadId)}/${text(t.turnId)}`}>
        Conversation {text(t.threadId)} · turn {text(t.turnId)}: {t.label ? <b>{text(t.label)}</b> : noLabelReading(t, outcome)}
        {t.codexReported ? ` · Codex reported: ${text(t.codexReported)}` : outcome?.state === "stopped" ? " · Codex reported no end before the stop" : " · Codex reported no end"}
        {" "}· interrupt request: {text(t.interruptRequest?.reading) || text(t.interruptRequest?.state)}
        {t.interruptRequest && <> · stop-request record: {t.stopRequest ? text(t.stopRequest.persistence) : "not recorded"}</>}
      </li>)}
    </ul>}
    {outcome?.outstandingRequests?.count > 0 && <p>{outcome.outstandingRequests.count} waiting request(s): {text(outcome.outstandingRequests.reading)}</p>}
    {runs.length > 0 && <p>Workflow runs in force at the stop: {runs.map((r: Json) => `${text(r?.workflow?.name) || "workflow"} (run ${text(r?.run)})`).join(", ")}. {text(outcome?.runsInForce?.reading)}</p>}
    {outcome?.historyNote && <p>{text(outcome.historyNote)}</p>}
    {outcome?.codexStopRecord && <p>Stop Codex record: {text(outcome.codexStopRecord.reading) || text(outcome.codexStopRecord.state)}.</p>}
    {outcome?.start && <p>{outcome.start.state === "started" ? "Codex started again in a new process." : `Codex was not started again: ${text(outcome.start.reading)}`} {text(outcome?.conversations)}</p>}
    <p><small>{text(outcome?.records)}</small></p>
  </div>;
}

export function CodexProcessControls({ host, busy, act }: { host: Json; busy: boolean; act: (command: string, args: Record<string, unknown>) => void }) {
  const state = host?.state;
  const running = !!host?.generation && !["absent", "stopped", "refused", "stopping"].includes(state);
  const stops = host?.codexStops;
  const outcomes = list(stops?.outcomes);
  const latest = outcomes[outcomes.length - 1];
  return <div aria-label="Codex process">
    <p>
      <button disabled={busy} onClick={() => act("host_start", { modeHomeClass: host?.homeRouting?.activeModeHomeClass })}>Start Codex</button>{" "}
      <button disabled={busy || !running} onClick={() => act("codex_stop", { generation: host?.generation, restart: false })}>Stop Codex…</button>{" "}
      <button disabled={busy || !running} onClick={() => act("codex_stop", { generation: host?.generation, restart: true })}>Restart Codex…</button>
    </p>
    <p>Stop Codex and Restart Codex ask first. A native question lists the live turns, waiting requests, delegated agents and workflow runs in force, and waits for your answer with no time limit. <b>Keep Codex running</b> (the default) and Cancel change nothing. If you confirm, the App stops sending new turns to this Codex process and checks the list again; if it changed, you are asked again. It then asks Codex to interrupt each live turn, waits up to {text(stops?.stopWaitLimitSeconds) || "10"} s for those turns to end, and stops Codex. Waiting requests are not answered, and no workflow run ends. Restart then starts Codex again; it continues no conversation until you choose <b>Continue selected conversation</b>.</p>
    <p>Stopping Codex is your operational choice, not a recorded act. {text(stops?.records)}</p>
    {latest && <StopOutcome outcome={latest} />}
    <StopRequests requests={host?.stopRequests} />
  </div>;
}

// Turns a stop interrupted, where the person reads the conversation
// (DEL-01-02 REQ-005, AC-006). Everything here comes from the stop-request
// records above (REC SR), read back after a relaunch: a turn is called
// interrupted only where its record's label says so, a derived label keeps its
// reading, and a request that was not sent or whose write outcome is unknown
// is shown by its own reading, never as an interrupt that reached Codex. An
// absent record is not evidence that nothing was interrupted.

/** The two labels a confirmed quit gives a turn it interrupted (stop_records.rs label). */
export const QUIT_INTERRUPTED = "interrupted by quit";
export const QUIT_NOT_OBSERVED = "interrupted by quit (final status not observed)";

/** What a stop label says of the turn's end: interrupted, completed, failed or
 *  unknown; null for a value that is not one of the App's labels. */
export function labelOutcome(label: unknown): "interrupted" | "completed" | "failed" | "unknown" | null {
  if (typeof label !== "string") return null;
  if (label.endsWith("(final status not observed)") || label.startsWith("outcome unknown")) return "unknown";
  if (label.startsWith("interrupted by ")) return "interrupted";
  if (label.startsWith("completed (")) return "completed";
  if (label.startsWith("failed (")) return "failed";
  return null;
}

/** The recorded stop requests for one conversation in one App-owned home, in request order. */
export function stopRequestsFor(requests: Json, threadId: string | null | undefined, home?: string): Json[] {
  if (!threadId) return [];
  return list(requests?.records).filter((r: Json) => r?.threadId === threadId && (!home || r?.home === home));
}

/** The stop requests of the App's most recent quit of an earlier session
 *  whose end is established: those of the earlier App session with the newest
 *  quit request. With `home`, only that App-owned home's rows. */
export function lastQuitRecords(requests: Json, home?: string): Json[] {
  const quit = list(requests?.records).filter((r: Json) => r?.cause === "quit" && r?.earlierSession === true);
  if (!quit.length) return [];
  const newest = quit.reduce((a: Json, b: Json) => (text(b.requestedAt) > text(a.requestedAt) ? b : a));
  return quit.filter((r: Json) => r.appSession === newest.appSession && (!home || r.home === home));
}

const count = (n: number, one: string, many: string) => (n === 1 ? `1 ${one}` : `${n} ${many}`);
const isQuitInterrupt = (r: Json) => r?.label === QUIT_INTERRUPTED || r?.label === QUIT_NOT_OBSERVED;
const NOT_SHOWN = "An interrupted turn is not a workflow run's end. Requests Codex was waiting on you for when the App quit or Codex was stopped were not answered, and this App session cannot answer them. Nothing here says what became of agents the conversation delegated work to.";
const ABSENCE = "Some stop records carry limits (listed under Codex process, Recorded stop requests). A turn with no record here is not shown to have run to its end.";

/** On one conversation: the turns its stop records name, each with its label
 *  or reading, and an offer to continue it by the existing Continue (thread
 *  resume, admitted only on a matching resume response). */
export function ConversationStops({ records, limited, onContinue, canContinue }: { records: Json[]; limited?: boolean; onContinue?: () => void; canContinue?: boolean }) {
  const rows = list(records);
  if (!rows.length) return null;
  const quit = rows.filter((r: Json) => r?.cause === "quit");
  const observed = quit.filter((r: Json) => r.label === QUIT_INTERRUPTED);
  const notObserved = quit.filter((r: Json) => r.label === QUIT_NOT_OBSERVED);
  const others = rows.filter((r: Json) => !isQuitInterrupt(r));
  const stopping = rows.some((r: Json) => r?.cause === "quit" || r?.cause === "codex-stop");
  const turn = (r: Json) => <li key={text(r.stopRequestId)}>Turn <SuppliedId value={r.turnId} label="Turn:" name="Turn identity as Codex reported it, not the App's words" />{" "}
    <small>({CAUSE[text(r.cause)] ?? text(r.cause)}, requested {text(r.requestedAt)})</small>
    <StopLabel stop={r} /></li>;
  return <div role="note" aria-label="Stopped turns in this conversation" style={{ border: "1px solid #bbb", padding: 8, margin: "8px 0" }}>
    {observed.length > 0 && <p><b>{observed.length === 1 ? "A turn of this conversation was" : `${observed.length} turns of this conversation were`} interrupted when you quit the App.</b> Codex reported {observed.length === 1 ? "it" : "them"} interrupted.</p>}
    {notObserved.length > 0 && <p><b>{notObserved.length === 1 ? "A turn of this conversation was" : `${notObserved.length} turns of this conversation were`} under way when you quit the App.</b> The App asked Codex to interrupt {notObserved.length === 1 ? "it" : "them"}; no final status was recorded for {notObserved.length === 1 ? "it" : "them"}, so the App labels {notObserved.length === 1 ? "it" : "them"} “{QUIT_NOT_OBSERVED}”. Codex's own status, where its history reports one, is shown with the turn.</p>}
    {(observed.length > 0 || notObserved.length > 0) && <ul>{[...observed, ...notObserved].map(turn)}</ul>}
    {others.length > 0 && <>
      <p>{observed.length + notObserved.length > 0 ? "Other stop requests recorded for this conversation" : "Stop requests recorded for this conversation"}; each says what its record establishes:</p>
      <ul>{others.map(turn)}</ul>
    </>}
    {stopping && <p><small>{NOT_SHOWN}</small></p>}
    {limited && <p><small>{ABSENCE}</small></p>}
    {onContinue && <p><button disabled={!canContinue} onClick={onContinue}>Continue this conversation</button>{" "}
      <small>Continue asks Codex to open this conversation again and waits for its answer before you can send in it. The App does not send the interrupted turn's message again; nothing is sent until you write and send a message.</small></p>}
  </div>;
}

/** The App's most recent quit of an earlier session, said without a press:
 *  the conversations of this home whose turns it interrupted. `name` shows a
 *  conversation (its supplied title and identity); `select`, where given,
 *  chooses it for inspection (no read, no Continue). */
export function LastQuitNotice({ requests, home, name, select, selected, canSelect, received, open, dismiss }: {
  requests: Json; home?: string; name: (threadId: string) => ReactNode;
  select?: (threadId: string) => void; selected?: string | null; canSelect?: boolean; received?: (threadId: string) => boolean;
  open?: ReactNode; dismiss?: () => void;
}) {
  const all = lastQuitRecords(requests);
  const rows = lastQuitRecords(requests, home);
  if (!all.length) return null;
  const interrupted = rows.filter(isQuitInterrupt);
  const others = rows.filter((r: Json) => !isQuitInterrupt(r));
  const elsewhere = home ? all.filter((r: Json) => r.home !== home).length : 0;
  const threads: string[] = [];
  for (const r of interrupted) if (!threads.includes(text(r.threadId))) threads.push(text(r.threadId));
  const at = all.reduce((a: Json, b: Json) => (text(b.requestedAt) > text(a.requestedAt) ? b : a)).requestedAt;
  return <div role="note" aria-label="Work interrupted when the App was last quit" style={{ border: "1px solid #bbb", padding: 8, margin: "8px 0" }}>
    <p><b>When you last quit the App with work under way (stop requests recorded {text(at)}), {threads.length
      ? `the App asked Codex to interrupt ${count(interrupted.length, "turn", "turns")} in ${count(threads.length, "conversation", "conversations")} of this Codex home.`
      : rows.length ? "the App recorded stop requests for the turns under way in this Codex home." : "the App recorded stop requests in another Codex home."}</b></p>
    {threads.length > 0 && <ul>{threads.map(thread => {
      const turns = interrupted.filter((r: Json) => text(r.threadId) === thread);
      const here = received ? received(thread) : true;
      return <li key={thread}>{name(thread)} · {turns.map((r: Json, i: number) => <span key={text(r.stopRequestId)}>{i > 0 ? "; " : ""}{text(r.label)}{r.labelDerived ? " (derived; not written)" : ""}</span>)}
        {select && (selected === thread ? <small> (selected)</small> : here
          ? <>{" "}<button disabled={!canSelect} onClick={() => select(thread)}>Select this conversation</button></>
          : <small> Not among the received conversations; read another page of stored conversations to find it.</small>)}
      </li>;
    })}</ul>}
    {others.length > 0 && <p>For {count(others.length, "other turn", "other turns")} under way then, the record does not establish that the interrupt ended {others.length === 1 ? "it" : "them"}; the conversation shows what each record says.</p>}
    {elsewhere > 0 && <p>{count(elsewhere, "more stop request", "more stop requests")} from that quit {elsewhere === 1 ? "is" : "are"} recorded in another Codex home; choose that home under Connection &amp; access to see {elsewhere === 1 ? "it" : "them"}.</p>}
    <p>{select ? "Select a conversation to see its interrupted turns and to continue it." : "Open History and select the conversation to see its interrupted turns and to continue it."} Nothing is continued or sent until you choose Continue. {open}</p>
    {list(requests?.limits).length > 0 && <p><small>{ABSENCE}</small></p>}
    {dismiss && <p><button onClick={dismiss}>Hide this notice</button> <small>It stays hidden until the App is next started or another stop is recorded; History still shows it.</small></p>}
  </div>;
}
