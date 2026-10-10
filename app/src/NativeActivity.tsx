import { Component, useState, type ReactNode } from "react";
type Json = any;

// Readable presentation of the host's native view (DEL-01-03 §5–§7; messages
// and reasoning are the DEL-01-04 conversation part of the same timeline).
// Every row keeps the native item unchanged beside its display reading (TR-1);
// nothing here infers checking, acceptance, approval, return or reliance.

export type ActivityTurn = { turnId: string; native: Json | null; items: Json[]; checklists: Json[] };
export type ActivityModel = { threadId: string; turns: ActivityTurn[]; goal: Json | null; checklistGaps: Json[]; children: Json[]; subtree: Json[]; parent: Json | null };

// Native collections are read through list() so an off-schema value (an object
// or string where Codex documents an array) shows nothing instead of throwing.
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);

// NIR §4.7 / NPTD TR-6 item anchors: a request card and its activity row link to
// each other by these element ids. The key is a short hash of the native
// identity, so any id characters are safe in a fragment.
function anchorKey(parts: Json[]): string {
  const source = JSON.stringify(parts) ?? "";
  let hash = 0x811c9dc5;
  for (let i = 0; i < source.length; i++) { hash ^= source.charCodeAt(i); hash = Math.imul(hash, 0x01000193) >>> 0; }
  return `${hash.toString(36)}-${source.length.toString(36)}`;
}
export const itemAnchorId = (threadId: Json, turnId: Json, itemId: Json) => `item-${anchorKey([threadId, turnId, itemId])}`;
export const requestAnchorId = (generation: Json, requestIdentity: Json) => `request-${anchorKey([generation, requestIdentity])}`;
const order = (row: Json) => (typeof row?.observedOrder === "number" ? row.observedOrder : Number.MAX_SAFE_INTEGER);

function descendantsOf(view: Json, root: string): Json[] {
  const all: Json[] = list(view?.descendants), found: Json[] = [], queue = [root];
  while (queue.length) {
    const parent = queue.shift();
    for (const child of all) if (child?.parentThreadId === parent && child.threadId !== root && !found.includes(child)) { found.push(child); queue.push(child.threadId); }
  }
  return found;
}

export function activityModel(view: Json, threadId: string): ActivityModel {
  const turns = new Map<string, ActivityTurn>();
  const turnFor = (turnId: string) => {
    if (!turns.has(turnId)) turns.set(turnId, { turnId, native: null, items: [], checklists: [] });
    return turns.get(turnId)!;
  };
  for (const row of list(view?.items)) if (row?.threadId === threadId) turnFor(row.turnId).items.push(row);
  // turnRecords associates each native turn with its thread; the turn itself stays in `turns`.
  for (const record of list(view?.turnRecords)) if (record?.threadId === threadId && record.turnId) turnFor(record.turnId).native = list(view?.turns).find((turn: Json) => turn?.id === record.turnId) ?? null;
  for (const revision of list(view?.revisions)) if (revision?.kind === "checklist" && revision.threadId === threadId) turnFor(revision.turnId).checklists.push(revision);
  const collected = Array.from(turns.values());
  for (const turn of collected) {
    turn.items.sort((a, b) => order(a) - order(b));
    turn.checklists.sort((a, b) => (a.ordinal ?? 0) - (b.ordinal ?? 0));
  }
  const firstSeen = (turn: ActivityTurn) => Math.min(...turn.items.map(order), Number.MAX_SAFE_INTEGER);
  const started = (turn: ActivityTurn) => (typeof turn.native?.startedAt === "number" ? turn.native.startedAt : null);
  // Turns with a native start time keep that order. A turn without one goes
  // after every turn this App received before it.
  const ordered = collected.filter(t => started(t) !== null).sort((a, b) => started(a)! - started(b)! || firstSeen(a) - firstSeen(b));
  for (const turn of collected.filter(t => started(t) === null).sort((a, b) => firstSeen(a) - firstSeen(b))) {
    let at = 0;
    ordered.forEach((other, index) => { if (firstSeen(other) <= firstSeen(turn)) at = index + 1; });
    ordered.splice(at, 0, turn);
  }
  return {
    threadId,
    turns: ordered,
    goal: view?.goals?.[threadId] ?? null,
    checklistGaps: list(view?.checklistGaps).filter((gap: Json) => gap?.threadId === threadId),
    children: list(view?.descendants).filter((child: Json) => child?.parentThreadId === threadId),
    subtree: descendantsOf(view, threadId),
    parent: list(view?.descendants).find((child: Json) => child?.threadId === threadId) ?? null,
  };
}

const NATIVE_STATE_LABEL: Record<string, string> = {
  "in-progress": "in progress",
  "waiting-on-request": "waiting on a request",
  "not-completed": "not completed (turn ended)",
  unknown: "unknown — no completion observed",
};
export function displayStateText(row: Json): string {
  const state = row?.displayState ?? "unknown";
  return typeof state === "string" && Object.prototype.hasOwnProperty.call(NATIVE_STATE_LABEL, state) ? NATIVE_STATE_LABEL[state] : text(state);
}

const KNOWN = new Set(["userMessage", "agentMessage", "reasoning", "plan", "commandExecution", "fileChange", "mcpToolCall", "dynamicToolCall", "functionCallOutput", "collabAgentToolCall", "subAgentActivity", "webSearch", "imageView", "imageGeneration", "enteredReviewMode", "exitedReviewMode", "contextCompaction", "sleep", "hookPrompt"]);

const pre = { whiteSpace: "pre-wrap" as const, overflowWrap: "anywhere" as const, margin: "4px 0" };
const card = { borderLeft: "3px solid #999", padding: "2px 8px", margin: "6px 0" };

function json(value: Json): string {
  try { return JSON.stringify(value, null, 2) ?? String(value); } catch { return String(value); }
}
function Raw({ value, label = "Native item" }: { value: Json; label?: string }) {
  return <details><summary>{label}</summary><pre style={pre}>{json(value)}</pre></details>;
}
// Native fields are interpolated through text() so an off-schema value from a
// different supplier shows as JSON instead of breaking the whole view.
function text(value: Json): string {
  return value === null || value === undefined ? "" : typeof value === "string" ? value : typeof value === "number" || typeof value === "boolean" ? String(value) : JSON.stringify(value);
}
function Shown({ label, value }: { label: string; value: Json }) {
  if (value === undefined) return null;
  return <div>{label}: {value === null ? <i>null (as supplied)</i> : typeof value === "string" ? value : JSON.stringify(value)}</div>;
}
function LongText({ text: value, label }: { text: Json; label: string }) {
  if (value === null || value === undefined) return <div>{label}: <i>not supplied by Codex</i></div>;
  const shown = text(value);
  if (shown.length <= 2000) return <div>{label}:<pre style={pre}>{shown}</pre></div>;
  return <details><summary>{label} ({shown.length} characters)</summary><pre style={pre}>{shown}</pre></details>;
}
function StateLine({ row }: { row: Json }) {
  const native = row.native ?? {};
  return <div>
    <b>{displayStateText(row)}</b>
    {" · native status "}{native.status === undefined ? <i>none in this item kind</i> : text(native.status)}
    {row.standing === "recovered-from-supplier" && " · read from Codex history"}
    {row.observationEnded && " · observation ended"}
    {row.endReason && ` · ${text(row.endReason)}`}
    {row.previewStanding && row.displayState !== "completed" && ` · ${text(row.previewStanding)}`}
    {row.requestRef && <>{" · "}<a href={`#${requestAnchorId(row.requestRef.generation, row.requestRef.requestIdentity)}`}>{row.displayState === "waiting-on-request" ? "answer it on its request card" : "its request card"}</a>{row.displayState === "waiting-on-request" && "; this row offers no answer"}</>}
    {row.settlementOrigin && ` · request settled by ${JSON.stringify(row.settlementOrigin)}`}
  </div>;
}

// TR-4: a completed row whose result elements are all null is "result not supplied".
export function resultNotSupplied(row: Json): boolean {
  const n = row?.native ?? {};
  if (row?.displayState !== "completed") return false;
  switch (n.type) {
    case "commandExecution": return n.aggregatedOutput == null && n.exitCode == null;
    case "mcpToolCall": return n.result == null && n.error == null;
    case "dynamicToolCall": return n.contentItems == null && n.success == null;
    default: return false;
  }
}

// Text streamed by Codex deltas before completion; the completed native item
// replaces it (the host drops the preview at completion). An interrupted or
// unknown item keeps its partial text, labelled by its state.
function streamed(row: Json): string | null {
  return row?.displayState !== "completed" && typeof row?.preview === "string" ? row.preview : null;
}
// Messages and reasoning show their state only when it is not "completed", so
// an interrupted or unknown message never reads as finished.
function Unfinished({ row }: { row: Json }) {
  if (row?.displayState === "completed") return null;
  return <StateLine row={row} />;
}

function messageText(content: Json): string {
  return (Array.isArray(content) ? content : []).map((part: Json) => part?.type === "text" ? text(part.text) : `[${text(part?.type ?? "input")} ${JSON.stringify(part)}]`).join("\n");
}
// RN-1: in the start turn of a run the App recorded, the run-start text the App
// wrote (WR-FRAME-1, its first line App-written) is folded and openable; the rest
// of the message, and any other message, shows as received.
const RUN_TEXT = /^\[Chirality\] (Workflow run start:|Previous workflow run ended:)/;
function UserMessage({ content, fold }: { content: Json; fold: boolean }) {
  const parts = Array.isArray(content) ? content : [];
  const folded = parts.filter((part: Json) => fold && part?.type === "text" && typeof part.text === "string" && RUN_TEXT.test(part.text));
  const rest = parts.filter((part: Json) => !folded.includes(part));
  return <>
    {folded.map((part: Json, i: number) => <details key={i}><summary>Workflow run text the App supplied ({part.text.length} characters)</summary><pre style={pre}>{part.text}</pre></details>)}
    {(rest.length > 0 || folded.length === 0) && <pre style={pre}>{messageText(rest)}</pre>}
  </>;
}

function ItemBody({ row, plans, runStart = false }: { row: Json; plans: Json[]; runStart?: boolean }) {
  const n = row.native ?? {};
  switch (n.type) {
    case "userMessage":
      return <div><b>User message</b> (text Codex recorded as input; not an act)<Unfinished row={row} /><UserMessage content={n.content} fold={runStart} /></div>;
    case "agentMessage":
      return <div><b>Agent</b>{n.phase ? ` · ${n.phase === "final_answer" ? "final answer" : text(n.phase)}` : ""}<Unfinished row={row} />
        <pre style={pre}>{streamed(row) ?? text(n.text)}</pre></div>;
    case "reasoning": {
      const summary: Json[] = Array.isArray(row.summaryPreview) && row.displayState !== "completed" ? row.summaryPreview : list(n.summary);
      return <div><i>Reasoning summary</i><Unfinished row={row} />{summary.length === 0 ? <i> (none supplied{row.displayState === "completed" ? "" : " so far"})</i> : <pre style={pre}>{summary.map(text).join("\n\n")}</pre>}</div>;
    }
    case "plan": {
      // An ordinal counts revisions in the order this App received them, so it
      // reads as a revision number only for live-observed plans; recovered
      // ones follow the order history pages were read.
      const revision = plans.find(r => r?.itemId === n.id && r?.turnId === row.turnId);
      // The state line already says "read from Codex history" for a recovered row.
      const where = revision?.standing === "live-observed" ? ` · revision ${text(revision.ordinal)} in this conversation`
        : revision?.standing === "recovered-from-supplier" && row.standing !== "recovered-from-supplier" ? " · revision read from Codex history" : "";
      return <div><b>Plan</b>{where}
        <StateLine row={row} /><pre style={pre}>{streamed(row) ?? text(n.text)}</pre></div>;
    }
    case "commandExecution": {
      const startSource = row.startNative?.source;
      return <div><b>Command</b> <code>{text(n.command)}</code><StateLine row={row} />
        <Shown label="cwd" value={n.cwd} />
        <div>source: {startSource !== undefined && startSource !== n.source ? `${text(startSource)} at start, ${text(n.source)} at completion` : text(n.source ?? "not supplied")}{n.source === "userShell" && " (the App's call at the person's direction)"}</div>
        <Shown label="exit code" value={n.exitCode} /><Shown label="duration ms" value={n.durationMs} />
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : <LongText label={streamed(row) !== null ? "output so far" : "output"} text={streamed(row) ?? n.aggregatedOutput} />}</div>;
    }
    case "fileChange":
      return <div><b>File change</b><StateLine row={row} />
        {list(n.changes).map((change: Json, i: number) => <details key={i}><summary>{text(change?.kind?.type) || "change"} {text(change?.path)}{change?.kind?.move_path ? ` → ${text(change.kind.move_path)}` : ""}</summary><pre style={pre}>{text(change?.diff)}</pre></details>)}</div>;
    case "mcpToolCall":
      return <div><b>MCP tool</b> {text(n.server)} / {text(n.tool)}<StateLine row={row} />
        <Shown label="arguments" value={n.arguments} /><Shown label="read-only hint" value={n.readOnlyHint} /><Shown label="duration ms" value={n.durationMs} />
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : <>{n.error && <div>error: {text(n.error.message)}</div>}{n.result && <Raw label="result" value={n.result} />}</>}</div>;
    case "dynamicToolCall":
      return <div><b>App tool</b> {n.namespace ? `${text(n.namespace)} / ` : ""}{text(n.tool)}<StateLine row={row} />
        <Shown label="arguments" value={n.arguments} /><Shown label="success" value={n.success} />
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : n.contentItems && <Raw label="content items" value={n.contentItems} />}</div>;
    case "functionCallOutput":
      return <div><b>Function output</b> {n.namespace ? `${text(n.namespace)} / ` : ""}{text(n.name)}<StateLine row={row} />{typeof n.output === "string" ? <LongText label="output" text={n.output} /> : <Raw label="output" value={n.output} />}</div>;
    case "collabAgentToolCall":
      return <div><b>Delegation</b> {text(n.tool)}<StateLine row={row} />
        <div>from {text(n.senderThreadId)} to {list(n.receiverThreadIds).map(text).join(", ") || "no receivers reported"}</div>
        <Shown label="requested model" value={n.model} /><Shown label="effort" value={n.reasoningEffort} />
        {n.prompt && <LongText label="prompt" text={n.prompt} />}
        {Object.entries(n.agentsStates && typeof n.agentsStates === "object" && !Array.isArray(n.agentsStates) ? n.agentsStates : {}).map(([id, state]: [string, Json]) => <div key={id}>agent {id}: Codex status {text(state?.status)}{state?.message ? ` — ${text(state.message)}` : ""}</div>)}</div>;
    case "subAgentActivity":
      return <div><b>Subagent activity</b> {text(n.kind)} · {text(n.agentPath)} ({text(n.agentThreadId)})<StateLine row={row} /></div>;
    case "webSearch":
      return <div><b>Web search</b> {text(n.query)}<StateLine row={row} /></div>;
    case "contextCompaction":
      return <div><i>Context compacted</i><Unfinished row={row} /></div>;
    default:
      if (!KNOWN.has(n.type)) return <div><b>unfamiliar item <code>{text(n.type) || "with no type"}</code></b><StateLine row={row} /></div>;
      return <div><b>{text(n.type)}</b><StateLine row={row} /></div>;
  }
}

function Checklist({ revisions }: { revisions: Json[] }) {
  const latest = revisions[revisions.length - 1];
  return <div style={card}>
    <b>Checklist</b> · revision {text(latest.ordinal)} of {revisions.length} observed live (Codex does not keep checklist updates in its history){latest.afterTurnEnd && " · received after the turn ended"}
    {latest.content?.explanation && <p>{text(latest.content.explanation)}</p>}
    <ol>{list(latest.content?.steps).map((step: Json, i: number) => <li key={i}>[{text(step?.status)}] {text(step?.step)}</li>)}</ol>
    {revisions.length > 1 && <details><summary>Earlier revisions</summary>{revisions.slice(0, -1).map((r, i) => <div key={i}>revision {text(r?.ordinal)}{r?.unchangedFromPrevious ? " (unchanged)" : ""}: {list(r?.content?.steps).map((s: Json) => `[${text(s?.status)}] ${text(s?.step)}`).join("; ")}</div>)}</details>}
  </div>;
}

function Child({ child }: { child: Json }) {
  const reported = child.lastObservedStatus;
  const status = reported && typeof reported === "object" ? reported : { status: reported };
  return <>
    {text(child.threadId)} · last observed Codex status {text(status.status) || "not reported"}{status.message ? ` — ${text(status.message)}` : ""}
    {child.statusSource ? ` (status source ${text(child.statusSource)})` : ""} · parent from {text(child.parentSource)}
    {child.nativeThread?.agentRole != null && ` · role ${text(child.nativeThread.agentRole)} (as Codex reports)`}{child.nativeThread?.agentNickname != null && ` · nickname ${text(child.nativeThread.agentNickname)}`}
    {child.observationEnded && " · observation ended"} · guidance {child.guidance === "not-known" ? "not known" : text(child.guidance)}
    {" "}· return, review and integration not inferred
  </>;
}

// One unreadable row falls back to its raw JSON instead of unmounting the App:
// an item shows its native item unchanged; a checklist or descendant shows the
// App's entry that carries the native content. The fallback resets when the
// host supplies a new row (`row`, compared by identity or value).
type BoundaryProps = { value: Json; row?: Json; label: string; children?: ReactNode };
export class RowBoundary extends Component<BoundaryProps, { failed: boolean; row: Json }> {
  constructor(props: BoundaryProps) {
    super(props);
    this.state = { failed: false, row: props.row ?? props.value };
  }
  static getDerivedStateFromProps(props: BoundaryProps, state: { row: Json }) {
    const row = props.row ?? props.value;
    return row !== state.row ? { failed: false, row } : null;
  }
  static getDerivedStateFromError() {
    return { failed: true };
  }
  render() {
    if (!this.state.failed) return this.props.children;
    const what = this.props.label === "native item" ? "the native JSON follows unchanged" : "its JSON entry follows unchanged";
    return <div style={card}><i>This {this.props.label} could not be shown readably; {what}.</i><pre style={pre}>{json(this.props.value)}</pre></div>;
  }
}

// RN-1: run start and end markers from the App's own run records (display only).
// A marker shows what the App recorded; it never comes from message text.
const marker = { borderTop: "2px dashed #777", borderBottom: "2px dashed #777", padding: "2px 8px", margin: "6px 0", fontSize: "0.9em" };
const runOpened = (run: Json) => typeof run?.lifecycle?.state === "string" && /^(open|ended)/.test(run.lifecycle.state);
function runName(run: Json): string {
  return `${text(run?.workflow?.name) || "workflow"} ${text(run?.workflow?.revision).slice(0, 12)}`.trim();
}
export function RunStartMarker({ run }: { run: Json }) {
  return <div role="note" style={marker}>Workflow run started: <b>{runName(run)}</b> (run {text(run?.reference)}), as the App recorded it. The workflow text it supplied is folded in the user message of this turn.</div>;
}
export function RunEndMarker({ run }: { run: Json }) {
  const cause = text(run?.lifecycle?.end?.cause) || "cause not recorded";
  return <div role="note" style={marker}>Run ended: <b>{cause}</b> ({runName(run)}, run {text(run?.reference)}){run?.finishedReport ? "; you ended it on the agent's “Workflow finished” statement" : ""}. You ended it; this marker checks nothing and does not take the work as done.</div>;
}

// TO-4 / RECOVERY §3.4: the App's own label for a turn it was asked to stop,
// beside Codex's reported status (Codex cannot say who interrupted). A REC SR
// row carries its own reading and where it is recorded.
export function StopLabel({ stop }: { stop: Json | null }) {
  if (!stop) return null;
  if (stop.stopRequestId) return <p role="note">{stop.label ? <>App label: <b>{text(stop.label)}</b>{stop.labelDerived ? " (derived; not written)" : ""}. </> : "Stop request: "}{text(stop.reading)}{stop.codexReported ? ` Codex reported: ${text(stop.codexReported)}.` : ""}{stop.earlierSession ? " From an earlier App session." : ""} Codex's own status is shown beside it. <small>Record: {text(stop.persistence)}.</small></p>;
  return <p role="note">App label: <b>{text(stop.label)}</b> ({stop.codexReported ? `Codex reported at the stop: ${text(stop.codexReported)}` : "Codex reported no end before the stop"}). Codex's own status is shown beside it.</p>;
}

export function NativeActivityView({ view, threadId, offers, renderOffer, runs, stopLabelFor }: { view: Json; threadId: string | null | undefined; offers?: Json[]; renderOffer?: (offer: Json) => ReactNode; runs?: Json[]; stopLabelFor?: (threadId: string, turnId: string) => Json | null }) {
  const [shown, setShown] = useState<string>("");
  if (!threadId) return <p>Select a conversation to see its activity.</p>;
  const descendants = activityModel(view, threadId).subtree;
  const target = shown && descendants.some((c: Json) => c.threadId === shown) ? shown : threadId;
  const model = activityModel(view, target);
  const plans = list(view?.revisions).filter((r: Json) => r?.kind === "plan-item" && r.threadId === target);
  // Markers and offers belong to the selected conversation itself, not to a descendant.
  const ownRuns = target === threadId ? list(runs).filter((run: Json) => run?.conversation === target && runOpened(run)) : [];
  const shownTurns = new Set(model.turns.map(turn => turn.turnId));
  const unplaced = ownRuns.filter((run: Json) => !shownTurns.has(run.turn) || (run.lifecycle?.end && !shownTurns.has(run.endedAfterTurn)));
  const offersFor = (row: Json) => target === threadId && renderOffer ? list(offers).filter((offer: Json) => offer?.message?.threadId === row.threadId && offer?.message?.turnId === row.turnId && offer?.message?.itemId === row.native?.id) : [];
  return <div aria-label="Native activity">
    <h3>Activity</h3>
    <p>Codex types {text(view?.typesPin) || "not reported"} · supplier standing {String(view?.supplierStanding ?? "not established")}. {list(view?.limits).map(text).join(" ")}</p>
    {descendants.length > 0 && <label>Show <select value={target} onChange={e => setShown(e.target.value === threadId ? "" : e.target.value)}>
      <option value={threadId}>this conversation</option>
      {descendants.map((c: Json) => <option key={text(c.threadId)} value={text(c.threadId)}>descendant {text(c.threadId)}{c.parentThreadId !== threadId ? ` (of ${text(c.parentThreadId)})` : ""}</option>)}
    </select></label>}
    {model.parent && <p>Descendant of {text(model.parent.parentThreadId)} ({text(model.parent.parentSource)}).</p>}
    {model.goal && <p>Goal ({text(model.goal.source)}): {model.goal.native === null ? "cleared" : typeof model.goal.native?.objective === "string" ? model.goal.native.objective : JSON.stringify(model.goal.native)}</p>}
    {model.checklistGaps.map((gap, i) => <p key={i}>Checklist for turn {text(gap.turnId)}: {text(gap.reason)}</p>)}
    {unplaced.length > 0 && <div><small>Workflow runs in this conversation whose position this view cannot show:</small>
      {unplaced.map((run: Json) => <div key={text(run.reference)}>{!shownTurns.has(run.turn) && <RunStartMarker run={run} />}{run.lifecycle?.end && !shownTurns.has(run.endedAfterTurn) && <RunEndMarker run={run} />}</div>)}</div>}
    {model.turns.length === 0 && <p>No activity observed for this conversation in the current Codex generation. This view shows what the App received live in this generation and what it has read from Codex history; earlier generations' observations remain under the native JSON below.</p>}
    {model.turns.map(turn => <section key={text(turn.turnId)} style={{ borderTop: "1px solid #ccc", marginTop: 8 }}>
      {ownRuns.filter((run: Json) => run.turn === turn.turnId).map((run: Json) => <RunStartMarker key={text(run.reference)} run={run} />)}
      <div><small>Turn {text(turn.turnId)} · {turn.native ? `native status ${text(turn.native.status)}` : "turn status not observed"}{turn.native?.durationMs != null && ` · ${text(turn.native.durationMs)} ms`}</small></div>
      <StopLabel stop={stopLabelFor?.(target, text(turn.turnId)) ?? null} />
      {turn.native?.error?.message && <p role="alert">Turn error: {text(turn.native.error.message)}</p>}
      {turn.items.map((row, i) => <RowBoundary key={text(row.native?.id) || `row-${i}`} value={row.native} row={row} label="native item"><div style={card} id={itemAnchorId(row.threadId, row.turnId, row.native?.id)}>
        <ItemBody row={row} plans={plans} runStart={ownRuns.some((run: Json) => run.turn === row.turnId)} />
        <Raw value={row.native} />
      </div>{offersFor(row).map((offer: Json, k: number) => <div key={k}>{renderOffer?.(offer)}</div>)}</RowBoundary>)}
      {turn.checklists.length > 0 && <RowBoundary value={turn.checklists} row={`${turn.checklists.length}:${text(turn.checklists[turn.checklists.length - 1]?.revisionId)}`} label="checklist"><Checklist revisions={turn.checklists} /></RowBoundary>}
      {ownRuns.filter((run: Json) => run.lifecycle?.end && run.endedAfterTurn === turn.turnId).map((run: Json) => <RunEndMarker key={text(run.reference)} run={run} />)}
    </section>)}
    {model.children.length > 0 && <><h4>Descendants</h4><p>A completed turn here says nothing about these descendants.</p><ul>{model.children.map((c: Json, i: number) => <li key={text(c?.threadId) || `child-${i}`}><RowBoundary value={c} label="descendant"><Child child={c} /></RowBoundary></li>)}</ul></>}
  </div>;
}
