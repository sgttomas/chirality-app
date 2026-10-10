type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Start, Stop and Restart Codex (DEL-01-04 §5.2; DEL-01-02 C-12, DEF-5a).
// Stop and Restart always ask first in the host's native question, which lists
// the live work in force; there is no way to stop Codex from here without it.
// A stop is the person's operational choice, not a recorded act. Turn labels
// come from the host's outcome (TO-4 "interrupted by Stop Codex"), never from
// an interrupt acknowledgment.

const text = (v: unknown) => (v === null || v === undefined ? "" : typeof v === "string" ? v : JSON.stringify(v));
const list = (v: unknown): Json[] => (Array.isArray(v) ? v : []);

/** The App's Stop Codex label for a turn, from the newest outcome that names it. */
export function stopLabel(stops: Json, threadId: string | null | undefined, turnId: string | null | undefined): Json | null {
  if (!threadId || !turnId) return null;
  const outcomes = list(stops?.outcomes);
  for (let i = outcomes.length - 1; i >= 0; i--) {
    const turn = list(outcomes[i]?.turns).find((t: Json) => t?.threadId === threadId && t?.turnId === turnId);
    if (turn) return turn;
  }
  return null;
}

export function StopOutcome({ outcome }: { outcome: Json }) {
  const turns = list(outcome?.turns);
  const runs = list(outcome?.runsInForce?.rows);
  return <div role="status" aria-label="Stop Codex outcome" style={{ border: "1px solid #bbb", padding: 8, margin: "8px 0" }}>
    <p><b>{text(outcome?.action) || "Stop Codex"}</b> confirmed by you at {text(outcome?.confirmedAt) || "time not reported"} · home {text(outcome?.modeHomeClass) || "not reported"} · {outcome?.state === "stopped" ? "Codex stopped" : `Codex not stopped: ${text(outcome?.stop?.reading) || "reason not reported"}`}.</p>
    {turns.length === 0 ? <p>No live turn was observed, so no interrupt was sent.</p> : <ul>
      {turns.map((t: Json) => <li key={`${text(t.threadId)}/${text(t.turnId)}`}>
        Conversation {text(t.threadId)} · turn {text(t.turnId)}: <b>{text(t.label)}</b>
        {t.codexReported ? ` · Codex reported: ${text(t.codexReported)}` : " · Codex reported no end before the stop"}
        {" "}· interrupt request: {text(t.interruptRequest?.reading) || text(t.interruptRequest?.state)}
      </li>)}
    </ul>}
    {outcome?.outstandingRequests?.count > 0 && <p>{outcome.outstandingRequests.count} waiting request(s): {text(outcome.outstandingRequests.reading)}</p>}
    {runs.length > 0 && <p>Workflow runs in force at the stop: {runs.map((r: Json) => `${text(r?.workflow?.name) || "workflow"} (run ${text(r?.run)})`).join(", ")}. {text(outcome?.runsInForce?.reading)}</p>}
    {outcome?.historyNote && <p>{text(outcome.historyNote)}</p>}
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
    <p>Stop Codex and Restart Codex ask first. A native question lists the live turns, waiting requests, delegated agents and workflow runs in force, and waits for your answer with no time limit. <b>Keep Codex running</b> (the default) and Cancel change nothing. If you confirm, the App asks Codex to interrupt each live turn, waits up to {text(stops?.stopWaitLimitSeconds) || "10"} s for those turns to end, then stops Codex. Waiting requests are not answered, and no workflow run ends. Restart then starts Codex again; it continues no conversation until you choose <b>Continue selected conversation</b>.</p>
    <p>Stopping Codex is your operational choice, not a recorded act. {text(stops?.records)}</p>
    {latest && <StopOutcome outcome={latest} />}
  </div>;
}
