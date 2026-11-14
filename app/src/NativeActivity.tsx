import { Component, useEffect, useImperativeHandle, useRef, useState, type ReactNode, type Ref } from "react";
import { AgentText, type AgentTextSource, plainId, SuppliedId, Word, Num, Flag, wordOf, numberWords } from "./AgentText";
import { RunOffer, type RunAct } from "./RunOffers";
import { AGENT_STATUS, AGENT_TOOL, CHANGE_KIND, CHILD_STATUS, COMMAND_SOURCE, ITEM_KIND, ITEM_STATUS, MESSAGE_PHASE, REASONING_EFFORT, STEP_STATUS, SUBAGENT_ACTIVITY, TURN_STATUS } from "./nativeWords";
type Json = any;

// Readable presentation of the host's native view (DEL-01-03 §5–§7; messages
// and reasoning are the DEL-01-04 conversation part of the same timeline).
// Every row keeps the native item unchanged beside its display reading (TR-1);
// nothing here infers checking, acceptance, approval, return or reliance.
// Every value the agent, its tools or Codex supplies is shown through
// AgentText, so nothing in the stream that the App did not draw from a host
// record can read as the App's own words or as a request card. The App's own
// labels (item kinds, statuses) stay outside the box.

export type ActivityTurn = { turnId: string; native: Json | null; items: Json[]; checklists: Json[]; errors: Json[]; unreadableErrors: Json[] };
export type ActivityModel = { threadId: string; turns: ActivityTurn[]; goal: Json | null; checklistGaps: Json[]; children: Json[]; subtree: Json[]; parent: Json | null };
export type ActivityLocation = { generation: Json; rootThreadId: string; threadId: string; turnId: string; itemId: string };
export type ActivityReveal = { location: ActivityLocation; isCurrent: () => boolean };
export type NativeActivityHandle = { reveal: (navigation: ActivityReveal) => void };

export function sameActivityGeneration(a: Json, b: Json): boolean {
  const valid = (g: Json) => g && typeof g === "object" && Object.keys(g).length === 3
    && typeof g.appSession === "string" && !!g.appSession && typeof g.home === "string" && !!g.home
    && Number.isSafeInteger(g.spawnCounter) && g.spawnCounter > 0;
  return !!valid(a) && !!valid(b) && a.appSession === b.appSession && a.home === b.home && a.spawnCounter === b.spawnCounter;
}

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
    if (!turns.has(turnId)) turns.set(turnId, { turnId, native: null, items: [], checklists: [], errors: [], unreadableErrors: [] });
    return turns.get(turnId)!;
  };
  for (const row of list(view?.items)) if (row?.threadId === threadId) turnFor(row.turnId).items.push(row);
  // turnRecords associates each native turn with its thread; the turn itself stays in `turns`.
  for (const record of list(view?.turnRecords)) if (record?.threadId === threadId && record.turnId) turnFor(record.turnId).native = list(view?.turns).find((turn: Json) => turn?.id === record.turnId) ?? null;
  for (const revision of list(view?.revisions)) if (revision?.kind === "checklist" && revision.threadId === threadId) turnFor(revision.turnId).checklists.push(revision);
  // The supplier's error notices for a turn, in the order received. A turn
  // known only by such a notice is still shown, so the notice is not lost.
  for (const error of list(view?.turnErrors)) if (error?.threadId === threadId && typeof error.turnId === "string" && error.turnId) turnFor(error.turnId).errors.push(error);
  for (const error of list(view?.unreadableTurnErrors)) if (error?.threadId === threadId && typeof error.turnId === "string" && error.turnId) turnFor(error.turnId).unreadableErrors.push(error);
  const collected = Array.from(turns.values());
  for (const turn of collected) {
    turn.errors.sort((a, b) => (a.receiptPosition ?? 0) - (b.receiptPosition ?? 0));
    turn.items.sort((a, b) => order(a) - order(b));
    turn.checklists.sort((a, b) => (a.ordinal ?? 0) - (b.ordinal ?? 0));
  }
  // An error notice has its place in the same receiving order as the items.
  // The host keeps only a turn's newest notices, so each carries the order
  // of the turn's first one: the turn's place does not move as old ones go.
  const noticeOrder = (entry: Json) => (typeof entry?.turnFirstObservedOrder === "number" ? entry.turnFirstObservedOrder : order(entry));
  const firstSeen = (turn: ActivityTurn) => Math.min(...turn.items.map(order), ...turn.errors.map(noticeOrder), ...turn.unreadableErrors.map(noticeOrder), Number.MAX_SAFE_INTEGER);
  const started = (turn: ActivityTurn) => (typeof turn.native?.startedAt === "number" ? turn.native.startedAt : null);
  // Turns with a native start time keep that order. A turn without one goes
  // after every turn this App received before it.
  const ordered = collected.filter(t => started(t) !== null).sort((a, b) => started(a)! - started(b)! || firstSeen(a) - firstSeen(b));
  for (const turn of collected.filter(t => started(t) === null).sort((a, b) => firstSeen(a) - firstSeen(b))) {
    let at = 0;
    ordered.forEach((other, index) => { if (firstSeen(other) <= firstSeen(turn)) at = index + 1; });
    ordered.splice(at, 0, turn);
  }
  const subtree = descendantsOf(view, threadId);
  return {
    threadId,
    turns: ordered,
    goal: view?.goals?.[threadId] ?? null,
    checklistGaps: list(view?.checklistGaps).filter((gap: Json) => gap?.threadId === threadId),
    children: list(view?.descendants).filter((child: Json) => child?.parentThreadId === threadId),
    subtree,
    // A node naming one of this conversation's own descendants as its parent
    // is an inverted inference (trial witness 2026-10-10 (c)); never shown.
    // In a cycle the host has not yet corrected, the child's real line is
    // hidden too (DEL-01-03 NPTD §7.2, limit (c)).
    parent: list(view?.descendants).find((child: Json) => child?.threadId === threadId && !subtree.some((d: Json) => d?.threadId === child?.parentThreadId)) ?? null,
  };
}

// The host's display state for a row: its own states, and a completed item's native status copied in.
const NATIVE_STATE_LABEL = {
  "in-progress": "in progress",
  "waiting-on-request": "waiting on a request",
  "not-completed": "not completed (turn ended)",
  unknown: "unknown — no completion observed",
  completed: "completed",
  failed: "failed",
  declined: "declined",
  interrupted: "interrupted",
} as const;
export function displayStateText(row: Json): string {
  return wordOf(NATIVE_STATE_LABEL, row?.displayState ?? "unknown") ?? "a state the App does not recognise";
}
// The host's own sentences for why a row ended and what a preview stands for.
const END_REASON = { "turn ended without item completion": "turn ended without item completion", "in progress at the read": "in progress at the read" } as const;
const PREVIEW_STANDING = { "in progress; may differ from completed plan": "in progress; may differ from completed plan", "streamed so far; may differ from the completed item": "streamed so far; may differ from the completed item" } as const;
const PARENT_SOURCE = { "collabAgentToolCall.senderThreadId": "the delegating item's sender", "not-confirmed": "not confirmed", "subAgentActivity containing thread (inference)": "the thread holding its sub-agent activity (inferred)" } as const;

const KNOWN = new Set(["userMessage", "agentMessage", "reasoning", "plan", "commandExecution", "fileChange", "mcpToolCall", "dynamicToolCall", "functionCallOutput", "collabAgentToolCall", "subAgentActivity", "webSearch", "imageView", "imageGeneration", "enteredReviewMode", "exitedReviewMode", "contextCompaction", "sleep", "hookPrompt"]);

const pre = { whiteSpace: "pre-wrap" as const, overflowWrap: "anywhere" as const, margin: "4px 0" };
const card = { borderLeft: "3px solid #999", padding: "2px 8px", margin: "6px 0" };

function json(value: Json): string {
  try { return JSON.stringify(value, null, 2) ?? String(value); } catch { return String(value); }
}
// Native JSON as Codex sent it: it holds the agent's text, so it is shown as text the App did not write.
const NATIVE_JSON = "Native JSON as Codex sent it, which holds the agent's text, not the App's words";
function NativeJson({ value }: { value: Json }) {
  return <AgentText block value={json(value)} source="codex" label="As Codex sent it:" name={NATIVE_JSON} />;
}
function Raw({ value, label = "Native item" }: { value: Json; label?: string }) {
  return <details><summary>{label}</summary><NativeJson value={value} /></details>;
}
/** A Codex-supplied identifier in the App's words: as written when it is a plain identifier, else boxed as Codex's text. */
function Id({ value }: { value: Json }) {
  const id = plainId(value);
  return id !== null ? <>{id}</> : value === null || value === undefined || value === "" ? <>not reported</> : <AgentText value={text(value)} source="codex" label="Identity:" name="Identity as Codex reported it, not the App's words" />;
}
/** The same for a control's own words, which cannot hold a box. */
const idWords = (value: Json) => plainId(value) ?? "with an identity that is not a plain identifier";
// Native fields are interpolated through text() so an off-schema value from a
// different supplier shows as JSON instead of breaking the whole view.
function text(value: Json): string {
  return value === null || value === undefined ? "" : typeof value === "string" ? value : typeof value === "number" || typeof value === "boolean" ? String(value) : JSON.stringify(value);
}
// A field whose value is a number, a flag or Codex's own vocabulary: the App's words only for a value it checks.
function ShownNumber({ label, value }: { label: string; value: Json }) {
  if (value === undefined) return null;
  return <div>{label}: {value === null ? <i>null (as supplied)</i> : <Num value={value} />}</div>;
}
function ShownFlag({ label, value }: { label: string; value: Json }) {
  if (value === undefined) return null;
  return <div>{label}: {value === null ? <i>null (as supplied)</i> : <Flag value={value} yes="true" no="false" />}</div>;
}
function ShownEffort({ value }: { value: Json }) {
  if (value === undefined) return null;
  return <div>effort: {value === null ? <i>null (as supplied)</i> : <Word value={value} words={REASONING_EFFORT} />}</div>;
}
// A field whose value the agent (or its tool) supplied.
function Supplied({ label, value, source = "agent" }: { label: string; value: Json; source?: AgentTextSource }) {
  if (value === undefined) return null;
  return <div>{label}: {value === null ? <i>null (as supplied)</i> : <AgentText value={text(value)} source={source} />}</div>;
}
function LongText({ text: value, label, source = "tool" }: { text: Json; label: string; source?: AgentTextSource }) {
  if (value === null || value === undefined) return <div>{label}: <i>not supplied by Codex</i></div>;
  const shown = text(value);
  if (shown.length <= 2000) return <div>{label}:<AgentText block value={shown} source={source} /></div>;
  return <details><summary>{label} ({numberWords(shown.length)} characters)</summary><AgentText block value={shown} source={source} /></details>;
}
function StateLine({ row }: { row: Json }) {
  const native = row.native ?? {};
  return <div>
    <b><Word value={row?.displayState ?? "unknown"} words={NATIVE_STATE_LABEL} label="Recorded:" source="codex" name="A state the App does not recognise, as the host recorded it, not the App's words" /></b>
    {" · native status "}{native.status === undefined ? <i>none in this item kind</i> : native.status === null ? <i>null (as supplied)</i> : <Word value={native.status} words={ITEM_STATUS} name="An item status Codex sent that the App does not recognise, not the App's words" />}
    {row.standing === "recovered-from-supplier" && " · read from Codex history"}
    {row.historyRead && " · status at the read; current outcome not established"}
    {row.observationEnded && " · observation ended"}
    {row.endReason && <> · <Word value={row.endReason} words={END_REASON} label="Recorded:" name="Why the row ended, as recorded; the App does not vouch for its words" /></>}
    {row.previewStanding && row.displayState !== "completed" && <> · <Word value={row.previewStanding} words={PREVIEW_STANDING} label="Recorded:" name="What the preview stands for, as recorded; the App does not vouch for its words" /></>}
    {row.requestRef && <>{" · "}<a href={`#${requestAnchorId(row.requestRef.generation, row.requestRef.requestIdentity)}`}>{row.displayState === "waiting-on-request" ? "answer it on its request card" : "its request card"}</a>{row.displayState === "waiting-on-request" && "; this row offers no answer"}</>}
    {row.settlementOrigin && <> · request settled by <AgentText value={JSON.stringify(row.settlementOrigin)} source="codex" label="Settlement:" name="The request's settlement, as recorded; the App does not vouch for its words" /></>}
  </div>;
}

// A disposable native page is a snapshot, not an observation of a live item or
// request. Only documented terminal statuses imply a terminal reading. In
// particular imageGeneration accepts arbitrary status strings in the native
// schema; an unfamiliar status must remain unknown. The documented no-status
// kinds are complete items when returned in history, as in native_items.rs.
const NO_STATUS = new Set(["userMessage", "hookPrompt", "agentMessage", "functionCallOutput", "plan", "reasoning", "subAgentActivity", "webSearch", "imageView", "sleep", "enteredReviewMode", "exitedReviewMode", "contextCompaction"]);
const TERMINAL = new Set(["completed", "failed", "declined", "interrupted"]);
export function historyItemRow(native: Json, threadId: string, turnId: string): Json {
  const status = native?.status;
  const completed = status === undefined && NO_STATUS.has(native?.type);
  return { native, threadId, turnId, standing: "recovered-from-supplier", historyRead: true,
    displayState: completed ? "completed" : TERMINAL.has(status) ? status : "unknown",
    ...(status === "inProgress" ? { endReason: "in progress at the read" } : {}),
  };
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
    {folded.map((part: Json, i: number) => <details key={i}><summary>Workflow run text the App supplied ({numberWords(part.text.length)} characters)</summary><AgentText block value={part.text} source="file" label="The run text, with the workflow's files as the App read them:" name="Workflow run text from the workflow's files, not the App's words" /></details>)}
    {(rest.length > 0 || folded.length === 0) && <AgentText block value={messageText(rest)} source="person" />}
  </>;
}

// Native tool text stays readable without loading referenced media or opening
// links. Other result blocks remain available as their unchanged native JSON.
function ToolContent({ content }: { content: Json }) {
  if (!Array.isArray(content)) return null;
  return <>{content.map((part: Json, i: number) => {
    const value = part?.type === "text" || part?.type === "inputText" ? part.text
      : part?.type === "resource" ? part.resource?.text : undefined;
    return value !== undefined ? <LongText key={i} label="result text" text={value} /> : <Raw key={i} label={`result content ${i + 1}`} value={part} />;
  })}</>;
}

function ItemBody({ row, plans, runStart = false }: { row: Json; plans: Json[]; runStart?: boolean }) {
  const n = row.native ?? {};
  switch (n.type) {
    case "userMessage":
      return <div><b>User message</b> (text Codex recorded as input; not an act)<Unfinished row={row} /><UserMessage content={n.content} fold={runStart} /></div>;
    case "agentMessage":
      return <div><b>Agent</b>{n.phase ? <> · <Word value={n.phase} words={MESSAGE_PHASE} /></> : ""}<Unfinished row={row} />
        <AgentText block value={streamed(row) ?? text(n.text)} /></div>;
    case "reasoning": {
      const summary: Json[] = Array.isArray(row.summaryPreview) && row.displayState !== "completed" ? row.summaryPreview : list(n.summary);
      return <details><summary>Reasoning summary{row.displayState === "completed" ? "" : " (not finished; its state is shown inside)"}</summary><Unfinished row={row} />{summary.length === 0 ? <i> (none supplied{row.displayState === "completed" ? "" : " so far"})</i> : <AgentText block value={summary.map(text).join("\n\n")} />}</details>;
    }
    case "plan": {
      // An ordinal counts revisions in the order this App received them, so it
      // reads as a revision number only for live-observed plans; recovered
      // ones follow the order history pages were read.
      const revision = plans.find(r => r?.itemId === n.id && r?.turnId === row.turnId);
      // The state line already says "read from Codex history" for a recovered row.
      const where = revision?.standing === "live-observed" ? ` · revision ${numberWords(revision.ordinal) ?? "not numbered"} in this conversation`
        : revision?.standing === "recovered-from-supplier" && row.standing !== "recovered-from-supplier" ? " · revision read from Codex history" : "";
      return <div><b>Plan</b>{where}
        <StateLine row={row} /><AgentText block value={streamed(row) ?? text(n.text)} /></div>;
    }
    case "commandExecution": {
      const startSource = row.startNative?.source;
      return <div><b>Command</b><StateLine row={row} />
        {typeof n.exitCode === "number" && n.exitCode !== 0 && <p role="status">Command exited with code {numberWords(n.exitCode)}.</p>}
        <div>Command: <AgentText value={text(n.command)} /></div>
        <details><summary>Command details</summary>
        <Supplied label="cwd" value={n.cwd} />
        <div>source: {startSource !== undefined && startSource !== n.source ? <><Word value={startSource} words={COMMAND_SOURCE} /> at start, <Word value={n.source} words={COMMAND_SOURCE} /> at completion</> : n.source === undefined || n.source === null ? "not supplied" : <Word value={n.source} words={COMMAND_SOURCE} />}{n.source === "userShell" && " (the App's call at the person's direction)"}</div>
        <ShownNumber label="exit code" value={n.exitCode} /><ShownNumber label="duration ms" value={n.durationMs} /></details>
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : <details><summary>Command output{streamed(row) !== null ? " so far" : ""}</summary><LongText label={streamed(row) !== null ? "output so far" : "output"} text={streamed(row) ?? n.aggregatedOutput} /></details>}</div>;
    }
    case "fileChange":
      return <div><b>File change</b><StateLine row={row} />
        {list(n.changes).map((change: Json, i: number) => <div key={i}>
          <div>{change?.kind?.type ? <Word value={change.kind.type} words={CHANGE_KIND} /> : "change"} <AgentText value={text(change?.path)} label="Path:" />{change?.kind?.move_path ? <>, moved to <AgentText value={text(change.kind.move_path)} label="Path:" /></> : ""}</div>
          <details><summary>Change {i + 1} (diff)</summary><AgentText block value={text(change?.diff)} label="The agent's change (diff):" /></details></div>)}</div>;
    case "mcpToolCall":
      return <div><b>MCP tool</b> <AgentText value={text(n.server)} label="Server:" source="tool" name="MCP server name as Codex reports it, not the App's words" /> / <AgentText value={text(n.tool)} label="Tool:" source="tool" name="MCP tool name as Codex reports it, not the App's words" /><StateLine row={row} />
        <Supplied label="arguments" value={n.arguments} /><ShownFlag label="read-only hint" value={n.readOnlyHint} /><ShownNumber label="duration ms" value={n.durationMs} />
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : <>{n.error && <LongText label="error" text={n.error.message ?? n.error} />}{n.result != null && <><ToolContent content={n.result.content} /><Raw label="result" value={n.result} /></>}</>}</div>;
    case "dynamicToolCall":
      return <div><b>App tool</b> <AgentText value={`${n.namespace ? `${text(n.namespace)} / ` : ""}${text(n.tool)}`} label="Name:" source="tool" name="Tool name as Codex reports it, not the App's words" /><StateLine row={row} />
        <Supplied label="arguments" value={n.arguments} /><ShownFlag label="success" value={n.success} />
        {resultNotSupplied(row) ? <div>result not supplied by Codex</div> : n.contentItems != null && <><ToolContent content={n.contentItems} /><Raw label="content items" value={n.contentItems} /></>}</div>;
    case "functionCallOutput":
      return <div><b>Function output</b> <AgentText value={`${n.namespace ? `${text(n.namespace)} / ` : ""}${text(n.name)}`} label="Name:" source="tool" name="Function name as Codex reports it, not the App's words" /><StateLine row={row} />{typeof n.output === "string" ? <LongText label="output" text={n.output} /> : <Raw label="output" value={n.output} />}</div>;
    case "collabAgentToolCall":
      return <div><b>Delegation</b> <Word value={n.tool} words={AGENT_TOOL} /><StateLine row={row} />
        <div>from <Id value={n.senderThreadId} /> to {list(n.receiverThreadIds).length ? list(n.receiverThreadIds).map((r: Json, i: number) => <span key={i}>{i ? ", " : ""}<Id value={r} /></span>) : "no receivers reported"}</div>
        <Supplied label="requested model" value={n.model} /><ShownEffort value={n.reasoningEffort} />
        {n.prompt && <LongText label="prompt" text={n.prompt} source="agent" />}
        {Object.entries(n.agentsStates && typeof n.agentsStates === "object" && !Array.isArray(n.agentsStates) ? n.agentsStates : {}).map(([id, state]: [string, Json]) => <div key={id}>agent <Id value={id} />: Codex status <Word value={state?.status} words={AGENT_STATUS} />{state?.message ? <> — <AgentText value={text(state.message)} /></> : ""}</div>)}</div>;
    case "subAgentActivity":
      return <div><b>Subagent activity</b> <Word value={n.kind} words={SUBAGENT_ACTIVITY} /> · <AgentText value={text(n.agentPath)} label="Agent path:" /> (<Id value={n.agentThreadId} />)<StateLine row={row} /></div>;
    case "webSearch":
      return <div><b>Web search</b> <AgentText value={text(n.query)} label="Query:" /><StateLine row={row} /></div>;
    case "contextCompaction":
      return <div><i>Context compacted</i><Unfinished row={row} /></div>;
    default:
      if (!KNOWN.has(n.type)) return <div><b>unfamiliar item</b> {n.type === undefined || n.type === null || n.type === "" ? "with no type" : <AgentText value={n.type} source="codex" label="Type:" name="An item type Codex sent that the App does not recognise, not the App's words" />}<StateLine row={row} /></div>;
      return <div><b><Word value={n.type} words={ITEM_KIND} /></b><StateLine row={row} /></div>;
  }
}

function Checklist({ revisions }: { revisions: Json[] }) {
  const latest = revisions[revisions.length - 1];
  return <div style={card}>
    <b>Checklist</b> · revision <Num value={latest.ordinal} /> of {numberWords(revisions.length)} observed live (Codex does not keep checklist updates in its history){latest.afterTurnEnd && " · received after the turn ended"}
    {latest.content?.explanation && <AgentText block value={text(latest.content.explanation)} />}
    <ol>{list(latest.content?.steps).map((step: Json, i: number) => <li key={i}>[<Word value={step?.status} words={STEP_STATUS} />] <AgentText value={text(step?.step)} label="Step:" /></li>)}</ol>
    {revisions.length > 1 && <details><summary>Earlier revisions</summary>{revisions.slice(0, -1).map((r, i) => <div key={i}>revision <Num value={r?.ordinal} />{r?.unchangedFromPrevious ? " (unchanged)" : ""}: {list(r?.content?.steps).map((s: Json, k: number) => <span key={k}>{k > 0 && "; "}[<Word value={s?.status} words={STEP_STATUS} />] <AgentText value={text(s?.step)} label="Step:" /></span>)}</div>)}</details>}
  </div>;
}

function Child({ child, trialLabel }: { child: Json; trialLabel?: Json }) {
  const reported = child.lastObservedStatus;
  const status = reported && typeof reported === "object" ? reported : { status: reported };
  return <>
    {trialLabel ? <><AgentText value={trialLabel} source="codex" label="Trial:" name="The trial's label, as recorded; the App does not vouch for its words" /> · </> : null}
    <Id value={child.threadId} /> · last observed Codex status {status.status === undefined || status.status === null || status.status === "" ? "not reported" : <Word value={status.status} words={CHILD_STATUS} />}{status.message ? <> — <AgentText value={text(status.message)} /></> : ""}
    {child.statusSource ? <> (status source <AgentText value={text(child.statusSource)} source="codex" label="Status source:" name="Where the status was read, as recorded; the App does not vouch for its words" />)</> : ""} · parent from <Word value={child.parentSource} words={PARENT_SOURCE} label="Recorded:" name="Where the parent was read, as recorded; the App does not vouch for its words" />
    {child.nativeThread?.agentRole != null && <> · role <AgentText value={text(child.nativeThread.agentRole)} label="Role:" name="Agent role as Codex reports it, not the App's words" /> (as Codex reports)</>}{child.nativeThread?.agentNickname != null && <> · nickname <AgentText value={text(child.nativeThread.agentNickname)} label="Name:" name="Agent nickname as Codex reports it, not the App's words" /></>}
    {child.observationEnded && " · observation ended"} · guidance {child.guidance === "not-known" ? "not known" : <AgentText value={text(child.guidance)} source="codex" label="Guidance:" name="The descendant's guidance reading, as recorded; the App does not vouch for its words" />}
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
    const kind = this.props.label === "native item" ? "native item" : this.props.label === "checklist" ? "checklist" : this.props.label === "descendant" ? "descendant" : "entry";
    return <div style={card}><i>This {kind} could not be shown readably; {what}.</i><NativeJson value={this.props.value} /></div>;
  }
}

// Shared native body and raw item. History deliberately takes only the native
// item and its source identities: live previews, request links, revisions,
// run markers and item anchors cannot leak into the read-only page.
export function NativeItemCard({ row, plans = [], runStart = false, history = false, children, after }: { row: Json; plans?: Json[]; runStart?: boolean; history?: boolean; children?: ReactNode; after?: ReactNode }) {
  const shown = history ? historyItemRow(row?.native, row?.threadId, row?.turnId) : row;
  return <RowBoundary value={shown.native} row={row} label="native item"><div style={card} {...(!history ? { id: itemAnchorId(shown.threadId, shown.turnId, shown.native?.id) } : {})}>
    {history && <div><small>Native item <SuppliedId value={shown.native?.id} label="Item:" name="Item identity as Codex reported it, not the App's words" /> · <Word value={shown.native?.type} words={ITEM_KIND} /> · read from Codex history</small></div>}
    <ItemBody row={shown} plans={history ? [] : plans} runStart={!history && runStart} />
    {!history && children}
    <Raw value={shown.native} />
  </div>{!history && after}</RowBoundary>;
}

// RN-1: run start and end markers from the App's own run records (display only).
// A marker shows what the App recorded; it never comes from message text.
const marker = { borderTop: "2px dashed #777", borderBottom: "2px dashed #777", padding: "2px 8px", margin: "6px 0", fontSize: "0.9em" };
const runOpened = (run: Json) => typeof run?.lifecycle?.state === "string" && /^(open|ended)/.test(run.lifecycle.state);
function runName(run: Json): string {
  return `${text(run?.workflow?.name) || "workflow"} ${text(run?.workflow?.revision).slice(0, 12)}`.trim();
}
/** A run's workflow name and revision in the App's words when the name meets the App's own rule and the revision is
 * hexadecimal, else boxed as recorded. */
function RunName({ run }: { run: Json }) {
  const name = text(run?.workflow?.name), revision = text(run?.workflow?.revision).slice(0, 12);
  if ((!name || (name.length <= 64 && SAFE_WORKFLOW_NAME.test(name))) && /^[0-9a-f]*$/i.test(revision))
    return <b>{name ? plainId(name) : "workflow"}{revision ? <> {plainId(revision)}</> : null}</b>;
  return <AgentText value={runName(run)} source="codex" label="Workflow name:" name="Workflow name as recorded, not the App's words" />;
}
// NPTD §5.7 (R19-2): the run in force at a turn, from the App's run markers
// only: a run whose start turn is shown at or before the turn, and whose end,
// if recorded, is after that turn or at its end. A run whose end turn this view
// cannot place is in force only at its start turn. With two in force the later
// start is the one in force. Nothing is inferred about which run caused an item.
export function runInForce(runs: Json[], turnIds: string[], turnId: string): Json | null {
  const at = turnIds.indexOf(turnId);
  if (at < 0) return null;
  let found: Json | null = null;
  let foundStart = -1;
  for (const run of runs) {
    const start = turnIds.indexOf(text(run?.turn));
    if (start < 0 || start > at) continue;
    if (run?.lifecycle?.end) {
      const end = turnIds.indexOf(text(run?.endedAfterTurn));
      if (end < 0 ? start !== at : end < at) continue;
    }
    if (start >= foundStart) { found = run; foundStart = start; }
  }
  return found;
}
// The plan revision or tool row label (NPTD §5.7): "during the run of ‹workflow›
// ‹revision›". Messages, reasoning and compaction are conversation, not plan or
// tool rows, and carry none.
const UNLABELLED = new Set(["userMessage", "agentMessage", "reasoning", "contextCompaction"]);
/** A workflow name the App's own rule admits (`workflow_workspace::valid_name`): lowercase letters,
 * digits and single hyphens, at most 64 characters. A name outside it may come from a file an agent
 * wrote, so it is drawn as text the App did not write, never inside the App's sentence. */
const SAFE_WORKFLOW_NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;
export function RunLabel({ run }: { run: Json | null }) {
  if (!run) return null;
  return <div><small>During the run of <RunName run={run} />, as the App's run markers place this turn.</small></div>;
}
const RUN_ID = { label: "Run:", name: "Run reference, as recorded; the App does not vouch for its words" } as const;
export function RunStartMarker({ run }: { run: Json }) {
  return <div role="note" style={marker}>Workflow run started: <RunName run={run} /> (run <SuppliedId value={run?.reference} label={RUN_ID.label} name={RUN_ID.name} />), as the App recorded it. The workflow text it supplied is folded in the user message of this turn.</div>;
}
// The host's run-end causes (runtime_session.rs run_end_cause): its own words, or "ended to start ‹name›" with a
// name the App's rule admits. Anything else is boxed.
const RUN_END_CAUSE = { "ended by the person": "ended by the person", completed: "completed", invalid: "invalid" } as const;
function RunEndCause({ cause }: { cause: Json }) {
  if (cause === undefined || cause === null || cause === "") return <b>cause not recorded</b>;
  const word = wordOf(RUN_END_CAUSE, cause);
  if (word !== null) return <b>{word}</b>;
  const successor = typeof cause === "string" && cause.startsWith("ended to start ") ? cause.slice("ended to start ".length) : null;
  if (successor !== null && successor.length <= 64 && SAFE_WORKFLOW_NAME.test(successor)) return <b>ended to start {plainId(successor)}</b>;
  return <AgentText value={cause} source="codex" label="Cause:" name="Why the run ended, as recorded; the App does not vouch for its words" />;
}
export function RunEndMarker({ run }: { run: Json }) {
  return <div role="note" style={marker}>Run ended: <RunEndCause cause={run?.lifecycle?.end?.cause} /> (<RunName run={run} />, run <SuppliedId value={run?.reference} label={RUN_ID.label} name={RUN_ID.name} />){run?.finishedReport ? "; you ended it on the agent's “Workflow finished” statement" : ""}. You ended it; this marker checks nothing and does not take the work as done.</div>;
}

// TO-4 / RECOVERY §3.4: the App's own label for a turn it was asked to stop,
// beside Codex's reported status (Codex cannot say who interrupted). A REC SR
// row carries its own reading and where it is recorded.
// The App's own labels for a stopped turn (stop_records.rs label, codex_stop.rs outcome_label).
const STOP_LABEL = {
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
} as const;
const STOP_WORDS = { label: "The stop's label, as recorded; the App does not vouch for its words", reading: "The stop request's reading, as recorded; the App does not vouch for its words", persistence: "Where the stop is recorded, as recorded; the App does not vouch for its words" } as const;
export function StopLabel({ stop }: { stop: Json | null }) {
  if (!stop) return null;
  if (stop.stopRequestId) return <p role="note">{stop.label ? <>App label: <b><Word value={stop.label} words={STOP_LABEL} label="Recorded:" name={STOP_WORDS.label} /></b>{stop.labelDerived ? " (derived; not written)" : ""}. </> : "Stop request: "}<AgentText value={text(stop.reading)} source="codex" label="Reading:" name={STOP_WORDS.reading} />{stop.codexReported ? <> Codex reported: <Word value={stop.codexReported} words={TURN_STATUS} />.</> : ""}{stop.earlierSession ? " From an earlier App session." : ""} Codex's own status is shown beside it. <small>Record: <AgentText value={text(stop.persistence)} source="codex" label="Record:" name={STOP_WORDS.persistence} />.</small></p>;
  return <p role="note">App label: <b><Word value={stop.label} words={STOP_LABEL} label="Recorded:" name={STOP_WORDS.label} /></b> ({stop.codexReported ? <>Codex reported at the stop: <Word value={stop.codexReported} words={TURN_STATUS} /></> : "Codex reported no end before the stop"}). Codex's own status is shown beside it.</p>;
}

// NPTD §7.1: the delegation view by the host's reading for this conversation.
// Present: the view is shown, with "none observed" when empty. Missing: the
// view is absent and one line says why. Not established: shown only when
// delegation items arrive. Items that arrive are always shown (the list
// below), whatever the reading.
const DELEGATION_REASON = "Why delegation is not available, as recorded; the App does not vouch for its words";
export function DelegationLine({ delegation, descendants }: { delegation: Json; descendants: number }) {
  const at = delegation?.readAt ? <> (read <AgentText value={text(delegation.readAt)} source="codex" label="Read at:" name="When the delegation reading was taken, as recorded; the App does not vouch for its words" />)</> : "";
  if (delegation?.reading === "present") return descendants > 0 ? null : <p><small>Delegation available{at}; no descendants observed.</small></p>;
  if (delegation?.reading === "missing") return <p role="note"><small>Delegation not available: <AgentText value={text(delegation.reason)} source="codex" label="Reason:" name={DELEGATION_REASON} />{at}.{descendants > 0 ? " Descendants that arrived anyway are shown below." : ""}</small></p>;
  if (descendants > 0 && delegation?.reading === "not established") return <p><small>Delegation availability not established: <AgentText value={text(delegation.reason)} source="codex" label="Reason:" name={DELEGATION_REASON} />.</small></p>;
  return null;
}

/**
 * A turn's status for its heading. A turn last seen in progress is not in
 * progress once Codex has stopped: its outcome was not observed.
 */
export const turnStatusWords = (native: Json | null, observationEnded: boolean) => !native ? "status unknown"
  : native.status === "inProgress" && observationEnded ? "in progress when last observed; the App is no longer receiving from that Codex process, so its outcome is unknown"
  : wordOf(TURN_STATUS, native.status) ?? "a status the App does not recognise (shown under Turn source and timing)";

/** One error notice in the supplier's own words: its message, then its details where it sent any. */
/** A Codex error in Codex's own words: its message and, where given, its additional details. */
export const errorWords = (error: Json) => `${text(error?.message)}${typeof error?.additionalDetails === "string" && error.additionalDetails ? ` — ${error.additionalDetails}` : ""}`;

/**
 * The supplier's `error` notifications for one turn, as received. The words
 * are Codex's; the App adds only what it received and when: whether Codex
 * said it will retry, and whether a later frame that itself names the turn
 * (an item, a delta, the turn's end, or a frame named error it could not
 * read) arrived after the latest notice. A frame tied to the turn only
 * through a request or a reply is not counted, and the sentences say so. Nothing here says the turn failed, recovered or
 * is still trying, or that Codex's process has ended.
 */
export function TurnErrors({ errors, unreadable, turn }: { errors: Json[]; unreadable?: Json[]; turn: Json | null }) {
  const unread = list(unreadable);
  if (errors.length === 0 && unread.length === 0) return null;
  // What the host knows of a frame it could not read is its kind, where it
  // was received, and how many there were; never a meaning or a retry state.
  const lastUnread = unread[unread.length - 1];
  const unreadCount = typeof lastUnread?.ordinalInTurn === "number" ? lastUnread.ordinalInTurn : unread.length;
  const requests = unread.filter((entry: Json) => entry?.kind === "server-request-named-error").length;
  const refused = unread.length > 0 && <p role="status">
    Codex sent {unreadCount === 1 ? "a frame" : `${numberWords(unreadCount)} frames`} named <code>error</code> for this turn that the App could not read as the error notice its Codex version defines, so {unreadCount === 1 ? "its" : "their"} meaning and retry state are not established.
    {requests > 0 && ` ${requests === unread.length && unreadCount === unread.length ? (requests === 1 ? "It was" : "They were") : `${requests} of those kept ${requests === 1 ? "was" : "were"}`} ${requests === 1 ? "a request from Codex and not a notice" : "requests from Codex and not notices"}.`}
    {unreadCount > unread.length && ` The App kept the latest ${unread.length}.`}
    {" "}Received at position {unread.map((entry: Json, i: number) => <span key={i}>{i > 0 ? ", " : ""}<Num value={entry?.receiptPosition} /></span>)}; the original {unread.length === 1 ? "envelope is" : "envelopes are"} under Host diagnostics only while the host's journal still holds {unread.length === 1 ? "it" : "them"}.
  </p>;
  // With nothing readable, no error notice was established: the group is not labelled as one.
  if (errors.length === 0) return <div aria-label="Frames named error that the App could not read">{refused}</div>;
  const latest = errors[errors.length - 1];
  const received = typeof latest?.ordinalInTurn === "number" ? latest.ordinalInTurn : errors.length;
  const retry = latest?.willRetry === true ? "Codex said it will retry." : latest?.willRetry === false ? "Codex said it will not retry." : "Codex did not say whether it will retry.";
  const since = latest?.laterFrameForTurn === true ? "The App has since received a later event naming this turn."
    : latest?.observationEnded === true ? "The App stopped receiving from that Codex process before any later event naming this turn."
    : turn?.status === "inProgress" || turn === null ? "No later event naming this turn has reached the App." : "";
  return <div role={latest?.willRetry === false ? "alert" : "status"} aria-label="Errors Codex reported in this turn">
    <p>Codex reported an error in this turn{received > 1 ? ` ${numberWords(received)} times; the latest` : ""}: <AgentText value={errorWords(latest?.error)} source="codex" /> {retry}{since && ` ${since}`}</p>
    <details><summary>{errors.length === 1 ? "The error notice, with its whole error object" : `The ${numberWords(errors.length)} error notices in the order received, each with its whole error object`}</summary>
      {received > errors.length && <p><small>{numberWords(received - errors.length)} earlier {received - errors.length === 1 ? "notice is" : "notices are"} no longer kept.</small></p>}
      <ol>{errors.map((entry: Json, i: number) => <li key={i} value={typeof entry?.ordinalInTurn === "number" ? entry.ordinalInTurn : i + 1}>
        <AgentText value={errorWords(entry?.error)} source="codex" /> · {entry?.willRetry === true ? "will retry" : entry?.willRetry === false ? "will not retry" : "retry not stated"}
        <small> · received at position <Num value={entry?.receiptPosition} /></small>
        <NativeJson value={entry?.error} />
      </li>)}</ol>
    </details>
    {refused}
  </div>;
}

// RN-3…RN-7: the run offers beneath an agent message are drawn by RunOffer (a guarded view) with what the App
// supplies for its buttons; the activity takes no other renderer for them.
export type OfferControls = { generation: Json; ready: boolean; busy: boolean; act: RunAct };
export function NativeActivityView({ view, threadId, offers, offerControls, runs, stopLabelFor, trialTurns, trialChildren, delegation, navigationRef }: { view: Json; threadId: string | null | undefined; offers?: Json[]; offerControls?: OfferControls; runs?: Json[]; stopLabelFor?: (threadId: string, turnId: string) => Json | null; trialTurns?: Json[]; trialChildren?: Json[]; delegation?: Json; navigationRef?: Ref<NativeActivityHandle> }) {
  const [shown, setShown] = useState<string>("");
  const [pending, setPending] = useState<(ActivityReveal & { revision: number }) | null>(null);
  const revision = useRef(0);
  const container = useRef<HTMLDivElement>(null);
  const received = (location: ActivityLocation) => threadId === location.rootThreadId
    && sameActivityGeneration(view?.generation, location.generation) && view?.home === location.generation.home
    && (location.threadId === threadId || activityModel(view, threadId).subtree.some(child => child.threadId === location.threadId))
    && list(view?.items).some(row => row?.threadId === location.threadId && row?.turnId === location.turnId && row?.native?.id === location.itemId);
  useImperativeHandle(navigationRef, () => ({ reveal: navigation => {
    if (!navigation.isCurrent() || !received(navigation.location)) return;
    setShown(navigation.location.threadId === threadId ? "" : navigation.location.threadId);
    setPending({ ...navigation, revision: ++revision.current });
  } }));
  useEffect(() => {
    if (!pending) return;
    if (pending.revision !== revision.current || !pending.isCurrent() || !received(pending.location)) {
      setPending(null);
      if (pending.revision === revision.current) setShown("");
      return;
    }
    const target = shown || threadId;
    if (target !== pending.location.threadId) { setPending(null); return; }
    const { threadId: thread, turnId: turn, itemId: item } = pending.location;
    // Source/intent checks establish the destination. DOM lookup only scrolls
    // the already-rendered row inside this activity view, never supplies custody.
    const element = container.current?.querySelector<HTMLElement>(`#${itemAnchorId(thread, turn, item)}`);
    setPending(null);
    if (element && pending.revision === revision.current && pending.isCurrent()) element.scrollIntoView({ block: "center" });
  });
  // WR TT-2, TT-4: the host's trial labels (worded by the host) on the turn
  // that carried a trial message and on a linked sub-agent's row. Display only.
  const turnLabel = (thread: string, turn: string) => list(trialTurns).find((t: Json) => t?.threadId === thread && t?.turnId === turn)?.label;
  const childLabel = (thread: Json) => list(trialChildren).find((t: Json) => t?.threadId === thread)?.label;
  if (!threadId) return <p>Select a conversation to see its activity.</p>;
  const descendants = activityModel(view, threadId).subtree;
  const target = shown && descendants.some((c: Json) => c.threadId === shown) ? shown : threadId;
  const model = activityModel(view, target);
  const plans = list(view?.revisions).filter((r: Json) => r?.kind === "plan-item" && r.threadId === target);
  // Markers and offers belong to the selected conversation itself, not to a descendant.
  const ownRuns = target === threadId ? list(runs).filter((run: Json) => run?.conversation === target && runOpened(run)) : [];
  const shownTurns = new Set(model.turns.map(turn => turn.turnId));
  const turnIds = model.turns.map(turn => text(turn.turnId));
  const unplaced = ownRuns.filter((run: Json) => !shownTurns.has(run.turn) || (run.lifecycle?.end && !shownTurns.has(run.endedAfterTurn)));
  const offersFor = (row: Json) => target === threadId && offerControls ? list(offers).filter((offer: Json) => offer?.message?.threadId === row.threadId && offer?.message?.turnId === row.turnId && offer?.message?.itemId === row.native?.id) : [];
  return <div ref={container} aria-label="Native activity">
    <h3>Activity</h3>
    <details><summary>Activity source and limits</summary><p>Codex types {view?.typesPin ? <SuppliedId value={view.typesPin} label="Types:" name="The pinned Codex types, as recorded; the App does not vouch for its words" /> : "not reported"} · supplier standing {view?.supplierStanding === undefined || view?.supplierStanding === null ? "not established" : <AgentText value={text(view.supplierStanding)} source="codex" label="Standing:" name="The supplier's standing, as recorded; the App does not vouch for its words" />}.</p>{list(view?.limits).length > 0 && <AgentText block value={list(view?.limits).map(text).join("\n")} source="codex" label="Limits:" name="The activity view's limits, as recorded; the App does not vouch for its words" />}</details>
    {descendants.length > 0 && <label>Show <select value={target} onChange={e => {
      revision.current++; setPending(null);
      setShown(e.target.value === threadId ? "" : e.target.value);
    }}>
      <option value={threadId}>this conversation</option>
      {descendants.map((c: Json) => <option key={text(c.threadId)} value={text(c.threadId)}>descendant {idWords(c.threadId)}{c.parentThreadId !== threadId ? ` (of ${idWords(c.parentThreadId)})` : ""}</option>)}
    </select></label>}
    {model.parent && <p>Descendant of <Id value={model.parent.parentThreadId} /> (<Word value={model.parent.parentSource} words={PARENT_SOURCE} label="Recorded:" name="Where the parent was read, as recorded; the App does not vouch for its words" />).</p>}
    {model.goal && <p>Goal (<AgentText value={text(model.goal.source)} source="codex" label="Source:" name="Where the goal was read, as recorded; the App does not vouch for its words" />): {model.goal.native === null ? "cleared" : <AgentText value={typeof model.goal.native?.objective === "string" ? model.goal.native.objective : JSON.stringify(model.goal.native)} source="codex" />}</p>}
    {model.checklistGaps.map((gap, i) => <p key={i}>Checklist for turn <SuppliedId value={gap.turnId} label="Turn:" name="Turn identity as Codex reported it, not the App's words" />: <AgentText value={text(gap.reason)} source="codex" label="Reason:" name="Why the checklist is missing, as recorded; the App does not vouch for its words" /></p>)}
    {unplaced.length > 0 && <div><small>Workflow runs in this conversation whose position this view cannot show:</small>
      {unplaced.map((run: Json) => <div key={text(run.reference)}>{!shownTurns.has(run.turn) && <RunStartMarker run={run} />}{run.lifecycle?.end && !shownTurns.has(run.endedAfterTurn) && <RunEndMarker run={run} />}</div>)}</div>}
    {model.turns.length === 0 && <p>No activity observed for this conversation in the current Codex generation. This view shows what the App received live in this generation and what it has read from Codex history; earlier generations' observations remain under the native JSON below.</p>}
    {model.turns.map((turn, index) => <section key={text(turn.turnId)} aria-label={`Conversation turn ${index + 1}`} style={{ borderTop: "1px solid #ccc", marginTop: 8 }}>
      {ownRuns.filter((run: Json) => run.turn === turn.turnId).map((run: Json) => <RunStartMarker key={text(run.reference)} run={run} />)}
      <h4>{`Turn ${index + 1}`} · {turnStatusWords(turn.native, view?.observationEnded === true)}</h4>
      <details><summary>Turn source and timing</summary><small>Turn <SuppliedId value={turn.turnId} label="Turn:" name="Turn identity as Codex reported it, not the App's words" /> · {turn.native ? <>native status <Word value={turn.native.status} words={TURN_STATUS} name="A turn status Codex sent that the App does not recognise, not the App's words" /></> : "turn status not observed"}{turn.native?.durationMs != null && <> · <Num value={turn.native.durationMs} /> ms</>}</small></details>
      {turnLabel(target, turn.turnId) && <p role="note"><small><AgentText value={text(turnLabel(target, turn.turnId))} source="codex" label="Trial:" name="The trial's label for this turn, as recorded; the App does not vouch for its words" /></small></p>}
      <StopLabel stop={stopLabelFor?.(target, text(turn.turnId)) ?? null} />
      {turn.native?.error?.message && <p role="alert">Turn error: <AgentText value={text(turn.native.error.message)} source="codex" /></p>}
      <TurnErrors errors={turn.errors} unreadable={turn.unreadableErrors} turn={turn.native} />
      {turn.items.map((row, i) => <NativeItemCard key={text(row.native?.id) || `row-${i}`} row={row} plans={plans} runStart={ownRuns.some((run: Json) => run.turn === row.turnId)} after={offersFor(row).map((offer: Json, k: number) => <div key={k}>{offerControls && <RunOffer offer={offer} generation={offerControls.generation} ready={offerControls.ready} busy={offerControls.busy} act={offerControls.act} />}</div>)}>
        {!UNLABELLED.has(text(row.native?.type)) && <RunLabel run={runInForce(ownRuns, turnIds, text(turn.turnId))} />}
      </NativeItemCard>)}
      {turn.checklists.length > 0 && <RowBoundary value={turn.checklists} row={`${turn.checklists.length}:${text(turn.checklists[turn.checklists.length - 1]?.revisionId)}`} label="checklist"><Checklist revisions={turn.checklists} /><RunLabel run={runInForce(ownRuns, turnIds, text(turn.turnId))} /></RowBoundary>}
      {ownRuns.filter((run: Json) => run.lifecycle?.end && run.endedAfterTurn === turn.turnId).map((run: Json) => <RunEndMarker key={text(run.reference)} run={run} />)}
    </section>)}
    <DelegationLine delegation={target === threadId ? delegation : null} descendants={model.children.length} />
    {model.children.length > 0 && <><h4>Descendants</h4><p>A completed turn here says nothing about these descendants.</p><ul>{model.children.map((c: Json, i: number) => <li key={text(c?.threadId) || `child-${i}`}><RowBoundary value={c} label="descendant"><Child child={c} trialLabel={childLabel(c?.threadId)} /></RowBoundary></li>)}</ul></>}
  </div>;
}
