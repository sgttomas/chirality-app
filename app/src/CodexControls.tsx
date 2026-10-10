type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Start, Stop and Restart Codex (DEL-01-04 §5.2; DEL-01-02 C-12, DEF-5a).
// Stop and Restart always ask first in the host's native question, which lists
// the live work in force; there is no way to stop Codex from here without it.
// A stop is the person's operational choice, not a recorded act. Turn labels
// come from the App's stop-request records (REC SR) or the host's outcome
// (TO-4 "interrupted by Stop Codex"), never from an interrupt acknowledgment.

const text = (v: unknown) => (v === null || v === undefined ? "" : typeof v === "string" ? v : JSON.stringify(v));
const list = (v: unknown): Json[] => (Array.isArray(v) ? v : []);

/** The App's stop label for a turn. First the newest stop-request record
 *  (REC SR, read back from the App ledger after a relaunch) for the turn; then
 *  the newest Stop Codex outcome of this App process that stopped Codex and
 *  names it. A refused stop gives no label (the turn kept running). */
export function stopLabel(stops: Json, threadId: string | null | undefined, turnId: string | null | undefined, requests?: Json): Json | null {
  if (!threadId || !turnId) return null;
  const recorded = list(requests?.records).filter((r: Json) => r?.threadId === threadId && r?.turnId === turnId);
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
        Conversation {text(r.threadId)} · turn {text(r.turnId)} · {CAUSE[text(r.cause)] ?? text(r.cause)} at {text(r.requestedAt)}{r.earlierSession ? " (earlier App session)" : ""}: {r.label ? <b>{text(r.label)}</b> : null}{r.label ? ". " : ""}{text(r.reading)}{r.codexReported ? ` Codex reported: ${text(r.codexReported)}.` : ""}
        <br /><small>Record: {text(r.persistence)}.</small>
      </li>)}
      {limits.map((l: Json, i: number) => <li key={`limit${i}`}>Limit: {text(l)}</li>)}
    </ul>
    <p><small>{text(requests?.standing)}</small></p>
  </details>;
}

export function StopOutcome({ outcome }: { outcome: Json }) {
  const turns = list(outcome?.turns);
  const runs = list(outcome?.runsInForce?.rows);
  return <div role="status" aria-label="Stop Codex outcome" style={{ border: "1px solid #bbb", padding: 8, margin: "8px 0" }}>
    <p><b>{text(outcome?.action) || "Stop Codex"}</b> confirmed by you at {text(outcome?.confirmedAt) || "time not reported"} · home {text(outcome?.modeHomeClass) || "not reported"} · {outcome?.state === "stopped" ? "Codex stopped" : `Codex not stopped: ${text(outcome?.stop?.reading) || "reason not reported"}`}.</p>
    {turns.length === 0 ? <p>No live turn was observed, so no interrupt was sent.</p> : <ul>
      {turns.map((t: Json) => <li key={`${text(t.threadId)}/${text(t.turnId)}`}>
        Conversation {text(t.threadId)} · turn {text(t.turnId)}: {t.label ? <b>{text(t.label)}</b> : "no Stop Codex label (Codex was not stopped)"}
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
