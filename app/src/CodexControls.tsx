import type { ReactNode } from "react";
import { AgentText, SuppliedId, Word } from "./AgentText";
import { TURN_STATUS } from "./nativeWords";

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
export const appHome = (cls: unknown): string | undefined => (cls === "account" ? "H-acct" : cls === "api-key" ? "H-key" : undefined);

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

// Stop requests where the person reads the conversation (DEL-01-02 REQ-005,
// AC-006). Everything here comes from the stop-request records above (REC SR)
// and, for the session before this one, from its start and end records as the
// host carries them. A view says no more than a record establishes:
// - a stop request is associated only in the home bound to the History source
//   it is shown with; where that home is not known, nothing is associated;
// - a turn's end is said only as Codex reported it in the record; the App's
//   label is shown as the App's label, with its reading, and is never read as
//   a cause, an order of events or a Codex status;
// - a request without a confirmed write keeps its reading;
// - a quit is spoken of only where the previous session's recorded end is
//   that quit, and only for the requests its end record names;
// - an interrupt request answers no Codex request, and an absent record is not
//   evidence that nothing was interrupted.

/** The App's stop labels (stop_records.rs label), as the App's words. */
const STOP_LABELS: Record<string, string> = {
  "interrupted by the person": "interrupted by the person",
  "completed (stop requested)": "completed (stop requested)",
  "failed (stop requested)": "failed (stop requested)",
  "outcome unknown (stop requested)": "outcome unknown (stop requested)",
  "interrupted by quit": "interrupted by quit",
  "completed (quit requested)": "completed (quit requested)",
  "failed (quit requested)": "failed (quit requested)",
  "interrupted by quit (final status not observed)": "interrupted by quit (final status not observed)",
  "interrupted by Stop Codex": "interrupted by Stop Codex",
  "completed (Stop Codex requested)": "completed (Stop Codex requested)",
  "failed (Stop Codex requested)": "failed (Stop Codex requested)",
  "interrupted by Stop Codex (final status not observed)": "interrupted by Stop Codex (final status not observed)",
};
const RECORDED = { label: "The stop's label, as recorded; the App does not vouch for its words", reading: "The stop request's reading, as recorded; the App does not vouch for its words",
  persistence: "Where the stop is recorded, as recorded; the App does not vouch for its words", requested: "When the stop was requested, as recorded; the App does not vouch for its words" } as const;
const TURN_ID = "Turn identity as Codex reported it, not the App's words";

/** A final turn status as Codex reported it in a stop record, or null. */
export const reportedFinal = (value: unknown): "completed" | "interrupted" | "failed" | null =>
  value === "completed" || value === "interrupted" || value === "failed" ? value : null;

/** The App-owned home of an ACCESS home class for the stored views (the host's
 *  stop_records::home_class). The live view keeps appHome above. */
const storedHome = (cls: unknown): string | undefined => (cls === "account" ? "H-acct" : cls === "api-key" ? "H-key" : cls === "local-provider" ? "H-omlx" : undefined);

const sameGeneration = (a: Json, b: Json) => !!a && !!b && typeof a.appSession === "string" && a.appSession === b.appSession
  && typeof a.home === "string" && a.home === b.home && Number.isSafeInteger(a.spawnCounter) && a.spawnCounter === b.spawnCounter;

/** The App-owned home (H-acct, H-key, H-omlx) of one Codex generation: the
 *  home routing entry holding exactly that generation. Undefined unless
 *  exactly one entry does: an unknown home is never a wildcard. */
export function homeOfGeneration(host: Json, generation: Json): string | undefined {
  const holding = list(host?.homeRouting?.entries).filter((entry: Json) => sameGeneration(entry?.generation, generation));
  return holding.length === 1 ? storedHome(holding[0]?.modeHomeClass) : undefined;
}

/** The App-owned home of a History source: only where its home and its
 *  generation's home agree (as the stored page requires), then the home of
 *  that generation. */
export function historyHome(host: Json, history: Json): string | undefined {
  return typeof history?.home === "string" && history.home === history?.generation?.home ? homeOfGeneration(host, history.generation) : undefined;
}

/** The stop record for a stored turn, matched in its owning App-owned home on
 *  both paths: the newest stop-request record of that home, else the newest
 *  Stop Codex outcome of this App process that stopped Codex in that home and
 *  names the turn. No home, no match. */
export function storedStopLabel(stops: Json, threadId: string | null | undefined, turnId: string | null | undefined, requests: Json, home: string | undefined): Json | null {
  if (!home || !threadId || !turnId) return null;
  const recorded = list(requests?.records).filter((r: Json) => r?.threadId === threadId && r?.turnId === turnId && r?.home === home);
  if (recorded.length) return recorded[recorded.length - 1];
  const outcomes = list(stops?.outcomes).filter((o: Json) => o?.state === "stopped" && storedHome(o?.modeHomeClass) === home);
  for (let i = outcomes.length - 1; i >= 0; i--) {
    const turn = list(outcomes[i]?.turns).find((t: Json) => t?.threadId === threadId && t?.turnId === turnId && typeof t?.label === "string");
    if (turn) return turn;
  }
  return null;
}

/** The recorded stop requests for one conversation in its App-owned home, in
 *  request order. No home, none. */
export function stopRequestsFor(requests: Json, threadId: string | null | undefined, home: string | undefined): Json[] {
  if (!threadId || !home) return [];
  return list(requests?.records).filter((r: Json) => r?.threadId === threadId && r?.home === home);
}

/** A row that may carry the added Continue offer: a labelled stop-request
 *  record of an earlier App session whose end is established. */
export const continueEligible = (r: Json) => !!r?.stopRequestId && typeof r?.label === "string" && r.label in STOP_LABELS && r.earlierSession === true;

/** What one stop-request row establishes of its turn's end, in the App's words. */
function RowOutcome({ row }: { row: Json }) {
  if (typeof row?.label !== "string") return <>Stop request, no outcome label.</>;
  const reported = row.codexReported;
  const kind = row.cause === "quit" ? "The App recorded a quit stop request for this turn." : row.cause === "codex-stop" ? "The App recorded a Stop Codex stop request for this turn."
    : row.cause === "person-interrupt" ? "The App recorded an interrupt request for this turn." : "The App recorded a stop request for this turn.";
  return <>{row.cause === "quit" && reported === "interrupted" ? <>The App recorded a quit stop request for this turn. Codex reported it interrupted.</>
    : reported === null || reported === undefined ? <>{kind} The final outcome is unknown to the App.</>
    : <>Codex reported the turn <Word value={reported} words={TURN_STATUS} label="Recorded:" name="A turn status as recorded; the App does not vouch for its words" />.</>}
    {" "}App label: <b><Word value={row.label} words={STOP_LABELS} label="Recorded:" name={RECORDED.label} /></b>{row.labelDerived ? " (derived; not written)" : ""}.</>;
}

const count = (n: number, one: string, many: string) => (n === 1 ? `1 ${one}` : `${n} ${many}`);
const BOUNDS = "An interrupted turn is not a workflow run's end. An interrupt request does not answer a Codex request. Nothing here says what became of agents the conversation delegated work to.";
const ABSENCE = "The App's reading of stop records has limits. See Recorded stop requests under Codex process. A turn with no record here is not shown to have run to its end.";

/** On one conversation: the stop requests its records name, each with what
 *  its record establishes, and, where a row qualifies, an offer to continue
 *  it by the existing Continue (thread resume, admitted only on a matching
 *  resume response). `records` are this conversation's in its own home. */
export function ConversationStops({ records, limited, onContinue, canContinue }: { records: Json[]; limited?: boolean; onContinue?: () => void; canContinue?: boolean }) {
  const rows = list(records);
  if (!rows.length) return null;
  const offer = onContinue && rows.some(continueEligible);
  return <div role="note" aria-label="Stop requests recorded for this conversation" style={{ border: "1px solid #bbb", padding: 8, margin: "8px 0" }}>
    <p>Stop requests the App recorded for this conversation, each with what its record establishes:</p>
    <ul>{rows.map((r: Json) => <li key={text(r.stopRequestId)}>
      Turn <SuppliedId value={r.turnId} label="Turn:" name={TURN_ID} />{" "}
      <small>({CAUSE[text(r.cause)] ?? text(r.cause)}, requested <AgentText value={text(r.requestedAt)} source="record" label="Requested:" name={RECORDED.requested} />{r.earlierSession ? ", earlier App session" : ""})</small>: <RowOutcome row={r} />{" "}
      <AgentText value={text(r.reading)} source="codex" label="Reading:" name={RECORDED.reading} />{" "}
      <small>Record: <AgentText value={text(r.persistence)} source="codex" label="Record:" name={RECORDED.persistence} />.</small>
    </li>)}</ul>
    <p><small>Read turns asks Codex for a page of stored turns. {BOUNDS}</small></p>
    {limited && <p><small>{ABSENCE}</small></p>}
    {offer && <p><button disabled={!canContinue} onClick={onContinue}>Continue this conversation</button> <small>Continue asks Codex to reopen this conversation. It opens after a matching resume is confirmed. Continue sends no conversation message.</small></p>}
  </div>;
}

/** The quit stop requests of the App session this one followed, from the
 *  host's `previousSession`. None when the host names no previous session. */
export function previousQuitRecords(requests: Json): Json[] {
  const previous = requests?.previousSession;
  if (typeof previous !== "string" || !previous) return [];
  return list(requests?.records).filter((r: Json) => r?.cause === "quit" && r?.earlierSession === true && r?.appSession === previous);
}

/** How the previous session's end is recorded, where the notice does not
 *  speak of a quit: `held` is the quit's request list where it is held. */
function endWords(end: unknown, held: Json[] | null): string {
  if (end === "quit-with-live-work" || end === "clean") {
    return held ? "That session's recorded quit names none of these requests." : "The App recorded the session's end as a quit. The held records do not supply its request list.";
  }
  if (end === "system-terminated") return "That session's end is recorded as ended by the system.";
  if (end === "ended-without-record") return "That session's end was not recorded.";
  return "How that session ended is not recorded here.";
}

/** The previous App session's quit stop requests, said without a press. A
 *  quit is spoken of only where that session's recorded end is the quit and
 *  only for the requests its end record names. Rows of the bound History home
 *  (`home`) are listed by conversation where they carry a label; rows
 *  elsewhere are counted only. `name` shows a conversation; `received` says
 *  whether the bound received list holds it. Selection is History's own. */
export function PreviousQuitNotice({ requests, home, name, received, inHistory, open, hide }: {
  requests: Json; home: string | undefined; name: (threadId: string) => ReactNode; received: (threadId: string) => boolean;
  inHistory?: boolean; open?: ReactNode; hide?: () => void;
}) {
  const all = previousQuitRecords(requests);
  if (!all.length) return null;
  const held = Array.isArray(requests?.previousSessionQuitStops) ? list(requests.previousSessionQuitStops) : null;
  const quitEnd = ["quit-with-live-work", "clean"].includes(requests?.previousSessionEnd);
  const named = quitEnd && held ? all.filter((r: Json) => held.includes(r.stopRequestId)) : [];
  const quit = named.length > 0;
  const shown = quit ? named : all;
  const inHome = (r: Json) => !!home && r.home === home;
  const here = shown.filter(inHome);
  const elsewhere = home ? shown.length - here.length : 0;
  const listed = here.filter(continueEligible);
  const unconfirmed = here.filter((r: Json) => !listed.includes(r) && r.send !== "sent").length;
  const written = here.filter((r: Json) => r.send === "sent").length;
  const absent = quit ? all.filter((r: Json) => !named.includes(r) && inHome(r)).length : 0;
  const threads: string[] = [];
  for (const r of listed) if (!threads.includes(text(r.threadId))) threads.push(text(r.threadId));
  return <div role="note" aria-label={quit ? "Stop requests of the App's last quit" : "Stop requests from the previous App session"} style={{ border: "1px solid #bbb", padding: 8, margin: "8px 0" }}>
    <p><b>{quit ? "The App quit. Its end record names stop requests for turns the App had observed live." : "The previous App session recorded quit stop requests."}</b>
      {quit ? "" : ` ${endWords(requests?.previousSessionEnd, held)}`}
      {home ? ` ${quit ? "For that quit, " : "In this Codex home, "}${written === 0 ? "no interrupt request is recorded as written to Codex" : `${count(written, "interrupt request was", "interrupt requests were")} written to Codex`}${quit ? " in this Codex home" : ""}.` : ""}</p>
    {threads.length > 0 && <ul>{threads.map(thread => <li key={thread}>{name(thread)}
      <ul>{listed.filter((r: Json) => text(r.threadId) === thread).map((r: Json) => <li key={text(r.stopRequestId)}>Turn <SuppliedId value={r.turnId} label="Turn:" name={TURN_ID} />: <RowOutcome row={r} /></li>)}</ul>
      {!received(thread) && <small>This conversation is missing from the received list.</small>}
    </li>)}</ul>}
    {unconfirmed > 0 && <p>For {count(unconfirmed, "other stop request", "other stop requests")} in this Codex home, the App has no confirmed write to Codex.</p>}
    {absent > 0 && <p>{count(absent, "quit stop request", "quit stop requests")} in this Codex home {absent === 1 ? "is" : "are"} absent from the recorded quit's list.</p>}
    {!home && <p>Which Codex home is in view is not established, so no conversation is listed.</p>}
    {elsewhere > 0 && <p>{count(elsewhere, "stop request", "stop requests")} {elsewhere === 1 ? "is" : "are"} recorded outside this Codex home.</p>}
    {inHistory && threads.some(received) && <p>Select an available conversation to inspect its stop requests. Continue is a separate choice.</p>}
    <p>This notice resumes no conversation and sends no conversation message.</p>
    {open && <p>{open}</p>}
    {list(requests?.limits).length > 0 && <p><small>{ABSENCE}</small></p>}
    {hide && <p><button onClick={hide}>Hide this notice</button> <small>Hidden in this window until it reloads. The History notice is still available.</small></p>}
  </div>;
}
