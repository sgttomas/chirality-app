import { useState } from "react";
type Json = any;

// Readable presentation of the host's native view (DEL-01-03 §5–§7; messages
// and reasoning are the DEL-01-04 conversation part of the same timeline).
// Every row keeps the native item unchanged beside its display reading (TR-1);
// nothing here infers checking, acceptance, approval, return or reliance.

export type ActivityTurn = { turnId: string; native: Json | null; items: Json[]; checklists: Json[] };
export type ActivityModel = { threadId: string; turns: ActivityTurn[]; goal: Json | null; checklistGaps: Json[]; children: Json[]; parent: Json | null };

const order = (row: Json) => (typeof row?.observedOrder === "number" ? row.observedOrder : Number.MAX_SAFE_INTEGER);

export function activityThreads(view: Json): string[] {
  const seen: string[] = [];
  for (const row of [...(view?.items ?? [])].sort((a, b) => order(a) - order(b))) if (row?.threadId && !seen.includes(row.threadId)) seen.push(row.threadId);
  for (const turn of view?.turns ?? []) if (turn?.threadId && !seen.includes(turn.threadId)) seen.push(turn.threadId);
  return seen;
}

export function activityModel(view: Json, threadId: string): ActivityModel {
  const turns = new Map<string, ActivityTurn>();
  const turnFor = (turnId: string) => {
    if (!turns.has(turnId)) turns.set(turnId, { turnId, native: null, items: [], checklists: [] });
    return turns.get(turnId)!;
  };
  for (const row of view?.items ?? []) if (row?.threadId === threadId) turnFor(row.turnId).items.push(row);
  for (const turn of view?.turnRecords ?? []) if (turn?.threadId === threadId && turn.native?.id) turnFor(turn.native.id).native = turn.native;
  for (const revision of view?.revisions ?? []) if (revision?.kind === "checklist" && revision.threadId === threadId) turnFor(revision.turnId).checklists.push(revision);
  const list = Array.from(turns.values());
  for (const turn of list) {
    turn.items.sort((a, b) => order(a) - order(b));
    turn.checklists.sort((a, b) => (a.ordinal ?? 0) - (b.ordinal ?? 0));
  }
  const firstSeen = (turn: ActivityTurn) => Math.min(...turn.items.map(order), Number.MAX_SAFE_INTEGER);
  const started = (turn: ActivityTurn) => (typeof turn.native?.startedAt === "number" ? turn.native.startedAt : null);
  list.sort((a, b) => {
    const sa = started(a), sb = started(b);
    if (sa !== null && sb !== null && sa !== sb) return sa - sb;
    return firstSeen(a) - firstSeen(b);
  });
  return {
    threadId,
    turns: list,
    goal: view?.goals?.[threadId] ?? null,
    checklistGaps: (view?.checklistGaps ?? []).filter((gap: Json) => gap?.threadId === threadId),
    children: (view?.descendants ?? []).filter((child: Json) => child?.parentThreadId === threadId),
    parent: (view?.descendants ?? []).find((child: Json) => child?.threadId === threadId) ?? null,
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
  return NATIVE_STATE_LABEL[state] ?? state;
}

const KNOWN = new Set(["userMessage", "agentMessage", "reasoning", "plan", "commandExecution", "fileChange", "mcpToolCall", "dynamicToolCall", "functionCallOutput", "collabAgentToolCall", "subAgentActivity", "webSearch", "imageView", "imageGeneration", "enteredReviewMode", "exitedReviewMode", "contextCompaction", "sleep", "hookPrompt"]);

const pre = { whiteSpace: "pre-wrap" as const, overflowWrap: "anywhere" as const, margin: "4px 0" };
const card = { borderLeft: "3px solid #999", padding: "2px 8px", margin: "6px 0" };

function Raw({ value, label = "Native item" }: { value: Json; label?: string }) {
  return <details><summary>{label}</summary><pre style={pre}>{JSON.stringify(value, null, 2)}</pre></details>;
}
function Shown({ label, value }: { label: string; value: Json }) {
  if (value === undefined) return null;
  return <div>{label}: {value === null ? <i>null (as supplied)</i> : typeof value === "string" ? value : JSON.stringify(value)}</div>;
}
function LongText({ text, label }: { text: string | null | undefined; label: string }) {
  if (text === null || text === undefined) return <div>{label}: <i>not supplied by Codex</i></div>;
  if (text.length <= 2000) return <div>{label}:<pre style={pre}>{text}</pre></div>;
  return <details><summary>{label} ({text.length} characters)</summary><pre style={pre}>{text}</pre></details>;
}
function StateLine({ row }: { row: Json }) {
  const native = row.native ?? {};
  return <div>
    <b>{displayStateText(row)}</b>
    {" · native status "}{native.status === undefined ? <i>none in this item kind</i> : String(native.status)}
    {row.standing === "recovered-from-supplier" && " · read from Codex history"}
    {row.observationEnded && " · observation ended"}
    {row.endReason && ` · ${row.endReason}`}
    {row.displayState === "waiting-on-request" && " · answer it on its request card under Native requests; this row offers no answer"}
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

function messageText(content: Json): string {
  return (Array.isArray(content) ? content : []).map((part: Json) => part?.type === "text" ? part.text : `[${part?.type ?? "input"} ${JSON.stringify(part)}]`).join("\n");
}

function ItemBody({ row, plans }: { row: Json; plans: Json[] }) {
  const n = row.native ?? {};
  switch (n.type) {
    case "userMessage":
      return <div><b>User message</b> (text Codex recorded as input; not an act)<pre style={pre}>{messageText(n.content)}</pre></div>;
    case "agentMessage":
      return <div><b>Agent</b>{n.phase ? ` · ${n.phase === "final_answer" ? "final answer" : n.phase}` : ""}{row.displayState === "in-progress" && " · in progress"}
        <pre style={pre}>{n.text ?? ""}</pre></div>;
    case "reasoning":
      return <div><i>Reasoning summary</i>{(n.summary ?? []).length === 0 ? <i> (none supplied)</i> : <pre style={pre}>{(n.summary ?? []).join("\n\n")}</pre>}</div>;
    case "plan": {
      const revision = plans.find(r => r.itemId === n.id && r.turnId === row.turnId);
      const text = row.displayState === "in-progress" && n.text === undefined ? row.preview : n.text;
      return <div><b>Plan</b>{revision ? ` · revision ${revision.ordinal} in this conversation` : ""}{row.previewStanding && row.displayState === "in-progress" ? ` · ${row.previewStanding}` : ""}
        <StateLine row={row} /><pre style={pre}>{text ?? ""}</pre></div>;
    }
    case "commandExecution": {
      const startSource = row.startNative?.source;
      return <div><b>Command</b> <code>{n.command}</code><StateLine row={row} />
        <Shown label="cwd" value={n.cwd} />
        <div>source: {startSource !== undefined && startSource !== n.source ? `${String(startSource)} at start, ${String(n.source)} at completion` : String(n.source ?? "not supplied")}{n.source === "userShell" && " (the App's call at the person's direction)"}</div>
        <Shown label="exit code" value={n.exitCode} /><Shown label="duration ms" value={n.durationMs} />
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : <LongText label="output" text={n.aggregatedOutput} />}</div>;
    }
    case "fileChange":
      return <div><b>File change</b><StateLine row={row} />
        {(n.changes ?? []).map((change: Json, i: number) => <details key={i}><summary>{change.kind?.type ?? "change"} {change.path}{change.kind?.move_path ? ` → ${change.kind.move_path}` : ""}</summary><pre style={pre}>{change.diff}</pre></details>)}</div>;
    case "mcpToolCall":
      return <div><b>MCP tool</b> {n.server} / {n.tool}<StateLine row={row} />
        <Shown label="arguments" value={n.arguments} /><Shown label="read-only hint" value={n.readOnlyHint} /><Shown label="duration ms" value={n.durationMs} />
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : <>{n.error && <div>error: {n.error.message}</div>}{n.result && <Raw label="result" value={n.result} />}</>}</div>;
    case "dynamicToolCall":
      return <div><b>App tool</b> {n.namespace ? `${n.namespace} / ` : ""}{n.tool}<StateLine row={row} />
        <Shown label="arguments" value={n.arguments} /><Shown label="success" value={n.success} />
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : n.contentItems && <Raw label="content items" value={n.contentItems} />}</div>;
    case "functionCallOutput":
      return <div><b>Function output</b> {n.namespace ? `${n.namespace} / ` : ""}{n.name}<StateLine row={row} />{typeof n.output === "string" ? <LongText label="output" text={n.output} /> : <Raw label="output" value={n.output} />}</div>;
    case "collabAgentToolCall":
      return <div><b>Delegation</b> {String(n.tool)}<StateLine row={row} />
        <div>from {n.senderThreadId} to {(n.receiverThreadIds ?? []).join(", ") || "no receivers reported"}</div>
        <Shown label="requested model" value={n.model} /><Shown label="effort" value={n.reasoningEffort} />
        {n.prompt && <LongText label="prompt" text={n.prompt} />}
        {Object.entries(n.agentsStates ?? {}).map(([id, state]: [string, Json]) => <div key={id}>agent {id}: Codex status {state?.status}{state?.message ? ` — ${state.message}` : ""}</div>)}</div>;
    case "subAgentActivity":
      return <div><b>Subagent activity</b> {n.kind} · {n.agentPath} ({n.agentThreadId})<StateLine row={row} /></div>;
    case "webSearch":
      return <div><b>Web search</b> {n.query}<StateLine row={row} /></div>;
    case "contextCompaction":
      return <div><i>Context compacted</i></div>;
    default:
      if (!KNOWN.has(n.type)) return <div><b>unfamiliar item <code>{String(n.type)}</code></b><StateLine row={row} /></div>;
      return <div><b>{n.type}</b><StateLine row={row} /></div>;
  }
}

function Checklist({ revisions }: { revisions: Json[] }) {
  const latest = revisions[revisions.length - 1];
  return <div style={card}>
    <b>Checklist</b> · revision {latest.ordinal} of {revisions.length} observed live (Codex does not keep checklist updates in its history){latest.afterTurnEnd && " · received after the turn ended"}
    {latest.content?.explanation && <p>{latest.content.explanation}</p>}
    <ol>{(latest.content?.steps ?? []).map((step: Json, i: number) => <li key={i}>[{step.status}] {step.step}</li>)}</ol>
    {revisions.length > 1 && <details><summary>Earlier revisions</summary>{revisions.slice(0, -1).map(r => <div key={r.revisionId}>revision {r.ordinal}{r.unchangedFromPrevious ? " (unchanged)" : ""}: {(r.content?.steps ?? []).map((s: Json) => `[${s.status}] ${s.step}`).join("; ")}</div>)}</details>}
  </div>;
}

function Child({ child }: { child: Json }) {
  const status = child.lastObservedStatus;
  return <li>
    {child.threadId} · last observed Codex status {status?.status ?? "not reported"}{status?.message ? ` — ${status.message}` : ""}
    {" "}(source {child.statusSource ?? child.parentSource}){child.observationEnded && " · observation ended"} · guidance {child.guidance === "not-known" ? "not known" : child.guidance}
    {" "}· return, review and integration not inferred
  </li>;
}

export function NativeActivityView({ view, threadId }: { view: Json; threadId: string | null | undefined }) {
  const [shown, setShown] = useState<string>("");
  if (!threadId) return <p>Select a conversation to see its activity.</p>;
  const children = activityModel(view, threadId).children;
  const target = shown && children.some((c: Json) => c.threadId === shown) ? shown : threadId;
  const model = activityModel(view, target);
  const plans = (view?.revisions ?? []).filter((r: Json) => r.kind === "plan-item" && r.threadId === target);
  return <div aria-label="Native activity">
    <h3>Activity</h3>
    <p>Codex types {plans[0]?.typesPin ?? "0.160.0"} · supplier standing {String(view?.supplierStanding ?? "not established")}. {(view?.limits ?? []).join(" ")}</p>
    {children.length > 0 && <label>Show <select value={target} onChange={e => setShown(e.target.value === threadId ? "" : e.target.value)}>
      <option value={threadId}>this conversation</option>
      {children.map((c: Json) => <option key={c.threadId} value={c.threadId}>descendant {c.threadId}</option>)}
    </select></label>}
    {model.parent && <p>Descendant of {model.parent.parentThreadId} ({model.parent.parentSource}).</p>}
    {model.goal && <p>Goal ({model.goal.source}): {model.goal.native === null ? "cleared" : typeof model.goal.native?.objective === "string" ? model.goal.native.objective : JSON.stringify(model.goal.native)}</p>}
    {model.checklistGaps.map((gap, i) => <p key={i}>Checklist for turn {gap.turnId}: {gap.reason}</p>)}
    {model.turns.length === 0 && <p>No activity observed for this conversation yet. Stored history appears after it is read.</p>}
    {model.turns.map(turn => <section key={turn.turnId} style={{ borderTop: "1px solid #ccc", marginTop: 8 }}>
      <div><small>Turn {turn.turnId} · {turn.native ? `native status ${turn.native.status}` : "turn status not observed"}{turn.native?.durationMs != null && ` · ${turn.native.durationMs} ms`}</small></div>
      {turn.native?.error?.message && <p role="alert">Turn error: {turn.native.error.message}</p>}
      {turn.items.map(row => <div key={row.native?.id} style={card}>
        <ItemBody row={row} plans={plans} />
        <Raw value={row.native} />
      </div>)}
      {turn.checklists.length > 0 && <Checklist revisions={turn.checklists} />}
    </section>)}
    {model.children.length > 0 && <><h4>Descendants</h4><p>A completed turn here says nothing about these descendants.</p><ul>{model.children.map((c: Json) => <Child key={c.threadId} child={c} />)}</ul></>}
  </div>;
}
