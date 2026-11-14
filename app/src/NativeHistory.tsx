import { NativeItemCard } from "./NativeActivity";
import { AgentText, SuppliedId, Word, Num, isoSeconds } from "./AgentText";
import { ITEM_KIND, ITEMS_VIEW, TURN_STATUS } from "./nativeWords";
import { useEffect, useRef, useState } from "react";
import { invoke } from "./hostReads";

type Json = any;
const list = (value: Json): Json[] => Array.isArray(value) ? value : [];
const object = (value: Json) => value !== null && typeof value === "object" && !Array.isArray(value);
const text = (value: Json): string => value === undefined ? "not reported" : value === null ? "null (as supplied)" : typeof value === "string" ? value : JSON.stringify(value);
const nonempty = (value: Json): value is string => typeof value === "string" && value.length > 0;
const positive = (value: Json) => Number.isSafeInteger(value) && value > 0;

function generationValid(value: Json): boolean {
  return object(value) && Object.keys(value).length === 3 && nonempty(value.appSession) && nonempty(value.home) && positive(value.spawnCounter);
}
function sameGeneration(a: Json, b: Json): boolean {
  return generationValid(a) && generationValid(b) && a.appSession === b.appSession && a.home === b.home && a.spawnCounter === b.spawnCounter;
}

export type HistoryPageBinding = {
  accepted: boolean; notice: string; page: Json; rawPage: Json; query: Json; resolution: Json;
  home: Json; generation: Json; epoch: Json; threadId: Json;
};

// The current stream resolution identifies an accepted page. Mutable UI intent
// and the accumulated live native_items projection do not: both can describe a
// different read. Pending/error resolutions deliberately withhold readable old
// rows and their cursors; the unchanged raw page remains available below.
export function historyPageBinding(host: Json, kind: "turns" | "items"): HistoryPageBinding {
  const history = host?.nativeHistory, selected = history?.selected;
  const stream = kind === "items" ? "item-pages" : "turn-pages";
  const method = kind === "items" ? "thread/items/list" : "thread/turns/list";
  const resolution = selected?.streamResolutions?.[stream];
  const query = resolution?.query;
  const rawPage = selected?.[kind === "items" ? "itemsPage" : "turnsPage"];
  const base = { accepted: false, page: null, rawPage, query, resolution, home: history?.home, generation: history?.generation, epoch: history?.selectionEpoch, threadId: selected?.threadId };
  if (!selected) return { ...base, notice: "Select a stored conversation to read its history." };
  if (host?.state !== "ready" || history?.state !== "history-receiving" || !sameGeneration(host?.generation, history?.generation) || history.home !== history.generation?.home) {
    return { ...base, notice: "The history source is unavailable or has changed. Readable pages and paging are withheld; any retained native JSON is prior read evidence." };
  }
  if (resolution?.outcome === "pending") return { ...base, notice: "The requested page is pending. Any retained native JSON belongs to a prior read; readable rows and paging wait for the matched response." };
  if (selected?.errorsByStream?.[stream] != null || (resolution && resolution.outcome !== "native-result-observed")) {
    return { ...base, notice: "The requested page is unavailable. Any retained native JSON belongs to a prior read; it is not relabelled as the requested page. No automatic retry." };
  }
  if (rawPage == null) return { ...base, notice: "This page has not been read." };
  if (!positive(history.selectionEpoch) || !nonempty(selected.threadId) || !positive(resolution?.revision)
    || !positive(query?.factory_id) || !positive(query?.query_id) || query?.method !== method
    || query?.home !== history.home || !sameGeneration(query?.generation, history.generation)
    || query?.params?.threadId !== selected.threadId || !["asc", "desc"].includes(query?.params?.sortDirection)
    || (query.params.cursor !== undefined && !nonempty(query.params.cursor))
    || (kind === "items" && !nonempty(query.params.turnId))) {
    return { ...base, notice: "The retained page's accepted source identity is not established for this selection. Readable rows and paging are withheld; inspect the native JSON and stream evidence." };
  }
  if (!object(rawPage) || !Array.isArray(rawPage.data)) return { ...base, notice: "The retained page is malformed. Readable rows and paging are withheld; its native JSON remains available." };
  return { ...base, accepted: true, page: rawPage, notice: "Latest accepted page for this selection. Native statuses describe the read; current execution status is not established." };
}

export function HistoryPageSource({ binding }: { binding: HistoryPageBinding }) {
  const q = binding.query;
  return <>
    <p role="status">{binding.notice}</p>
    {binding.accepted && <p><small>Source home <SuppliedId value={binding.home} label="Home:" name="Home, as recorded; the App does not vouch for its words" /> · conversation <SuppliedId value={binding.threadId} label="Conversation:" name="Conversation identity as Codex reported it, not the App's words" />{q.params.turnId && <> · turn <SuppliedId value={q.params.turnId} label="Turn:" name="Turn identity as Codex reported it, not the App's words" /></>}<br />
      {q.params.sortDirection === "desc" ? "Newest first" : "Oldest first"} · {q.params.cursor === undefined ? "first page request" : "cursor page request"}.<br />
      Only this received page is shown. An exhausted cursor ends this paging direction; it does not establish a complete conversation or current descendant status.</small></p>}
  </>;
}

function RawPage({ binding, kind }: { binding: HistoryPageBinding; kind: string }) {
  return <>
    <details><summary>Original native {kind} page{!binding.accepted && binding.rawPage != null ? " (retained prior read; source not established for current request)" : ""}</summary><AgentText block value={JSON.stringify(binding.rawPage ?? { state: "not read" }, null, 2)} source="codex" label="Codex sent (native JSON):" /></details>
    <details><summary>Current {kind} stream source evidence</summary><AgentText block value={JSON.stringify({ home: binding.home, generation: binding.generation, selectionEpoch: binding.epoch, threadId: binding.threadId, resolution: binding.resolution }, null, 2)} source="codex" label="The App's record of this read, with Codex's identities (JSON):" name="The App's record of this read, holding identities Codex reported" /></details>
  </>;
}

const snippet = (value: Json) => {
  const source = typeof value === "string" ? value : "";
  return source.length > 320 ? `${source.slice(0, 320)}… (preview)` : source;
};
function preview(item: Json): string {
  if (item?.type === "userMessage") return snippet(list(item.content).filter(part => part?.type === "text" && typeof part.text === "string").map(part => part.text).join("\n"));
  return item?.type === "agentMessage" || item?.type === "plan" ? snippet(item.text) : "";
}
/** A native time in seconds: in ISO 8601 when it is a valid time, else boxed as Codex sent it. */
function NativeTime({ value }: { value: Json }) {
  if (value === null) return <>null (as supplied)</>;
  const time = isoSeconds(value);
  return time !== null ? <>{time}</> : <AgentText value={value} source="codex" label="Codex sent:" name="A value Codex sent where a time was expected, not the App's words" />;
}

export function StoredTurnPage({ binding, canRead, readItems }: { binding: HistoryPageBinding; canRead: boolean; readItems: (turnId: string) => void }) {
  return <div aria-label="Stored native turn page">
    <HistoryPageSource binding={binding} />
    {binding.accepted && binding.page.data.length === 0 && <p>Native returned an empty turn page. This does not establish that the conversation has no other turns.</p>}
    {binding.accepted && binding.page.data.map((turn: Json, index: number) => {
      const valid = object(turn) && nonempty(turn.id);
      const items = list(turn?.items);
      const user = items.find(item => item?.type === "userMessage");
      const response = [...items].reverse().find(item => item?.type === "agentMessage" || item?.type === "plan");
      return <article key={index} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
        <p><b>Turn <SuppliedId value={turn?.id} label="Turn:" name="Turn identity as Codex reported it, not the App's words" /></b> · native status <Word value={turn?.status} words={TURN_STATUS} name="A turn status Codex sent that the App does not recognise, not the App's words" />{turn?.status === "inProgress" && " (in progress at the read; current outcome unknown)"}{turn?.status === "interrupted" && " (cause not established by this page)"}</p>
        <div><small>Items view: {turn?.itemsView === undefined ? "full (native default)" : turn.itemsView === null ? "null (as supplied)" : <Word value={turn.itemsView} words={ITEMS_VIEW} />} · {Array.isArray(turn?.items) ? `${items.length} embedded items` : "items malformed or not reported"}. {turn?.itemsView === "notLoaded" ? "Items have not been loaded in this summary." : turn?.itemsView === "summary" ? "Summary items can omit substantive activity; read the item page." : "Embedded items are not rendered as the selected item page."}</small></div>
        {turn?.startedAt !== undefined && <div><small>Native start: <NativeTime value={turn.startedAt} /></small></div>}
        {turn?.completedAt !== undefined && <div><small>Native end: <NativeTime value={turn.completedAt} /></small></div>}
        {turn?.durationMs !== undefined && <div><small>Native duration ms: <Num value={turn.durationMs} /></small></div>}
        {preview(user) && <div>Input preview:<AgentText block value={preview(user)} source="person" /></div>}
        {preview(response) && <div>{response.type === "plan" ? "Plan" : "Agent"} preview:<AgentText block value={preview(response)} source="agent" /></div>}
        {items.length > 0 && <div><small>Embedded native kinds: {items.map((item, i) => <span key={i}>{i > 0 ? ", " : ""}<Word value={item?.type} words={ITEM_KIND} name="An item kind Codex sent that the App does not recognise, not the App's words" /></span>)}.</small></div>}
        {turn?.error != null && <p>Codex reported a turn error: <AgentText value={text(turn.error?.message ?? turn.error)} source="codex" label="Error:" name="Turn error as Codex reported it, not the App's words" /></p>}
        <p><small>Checklist updates: not recoverable from native history.</small></p>
        {valid ? <button disabled={!canRead} onClick={() => readItems(turn.id)}>Read items for this turn</button> : <p>Malformed native turn identity; an item read cannot be targeted.</p>}
        <details><summary>Native turn summary</summary><AgentText block value={JSON.stringify(turn, null, 2)} source="codex" label="Codex sent (native JSON):" /></details>
      </article>;
    })}
    <RawPage binding={binding} kind="turn" />
  </div>;
}

export function StoredItemPage({ binding }: { binding: HistoryPageBinding }) {
  return <div aria-label="Stored native item page">
    <HistoryPageSource binding={binding} />
    {binding.accepted && <>
      <p><small>Read-only native history. Tool success does not establish checking, acceptance, approval or reliance. Parent completion does not establish descendant return, review or integration. Checklist updates are not kept in Codex history; not recoverable after restart or relaunch. Recovered plans have no live revision number.</small></p>
      {binding.page.data.length === 0 && <p>Native returned an empty item page for turn <SuppliedId value={binding.query.params.turnId} label="Turn:" name="Turn identity as Codex reported it, not the App's words" />. Other pages or unrecorded activity are not established by this result.</p>}
      {binding.page.data.map((entry: Json, index: number) => {
        const native = entry?.item;
        const valid = object(entry) && entry.turnId === binding.query.params.turnId && object(native) && nonempty(native.id) && nonempty(native.type);
        return <article key={index}>
          {valid ? <NativeItemCard history row={{ threadId: binding.threadId, turnId: entry.turnId, native }} /> : <p>This native entry has a malformed item or mismatched turn identity. Its readable body is withheld; the source follows unchanged.</p>}
          <details><summary>Native page entry {index + 1} (including timing fields)</summary><AgentText block value={JSON.stringify(entry, null, 2)} source="codex" label="Codex sent (native JSON):" /></details>
        </article>;
      })}
    </>}
    <RawPage binding={binding} kind="item" />
  </div>;
}

/** The prior-work reader belongs to an exact admitted resume, independently
 * of the stored-history browser. Its disposable pages never hydrate live rows. */
export function continuationContextBinding(host: Json, thread: Json): { accepted: boolean; context: Json; notice: string; scope: string | null } {
  const base = { accepted: false, context: null, scope: null };
  if (thread?.nativeResumeObserved !== true || !nonempty(thread?.resumeRequestRef)) return { ...base, notice: "No admitted continuation context." };
  const matches = list(host?.continuationContexts).filter(context => context?.home === thread.generation?.home
    && sameGeneration(context.generation, thread.generation) && context.threadId === thread.threadId && context.resumeRequestRef === thread.resumeRequestRef);
  if (matches.length !== 1) return { ...base, notice: "Prior work is unavailable: a unique context for this admitted resume has not been received. No automatic retry." };
  const context = matches[0];
  const unavailable = { ...base, context, notice: "The prior-work source is unavailable or has changed. Readable pages and controls are withheld; retained source evidence is a prior read." };
  if (host?.state !== "ready" || !sameGeneration(host.generation, thread.generation) || context.sourceCurrent !== true
    || !positive(context.revision) || !positive(context.admissionSelectionEpoch)
    || context.partial !== true || context.fullHistoryRebuilt !== false || context.durableNativeData !== false
    || context.pageLimits?.turns !== 20 || context.pageLimits?.items !== 50
    || context.history?.home !== context.home || !sameGeneration(context.history?.generation, context.generation)
    || context.history?.selected?.threadId !== context.threadId
    || !["queued", "reading", "partial", "empty", "unavailable"].includes(context.state)) return unavailable;
  const scope = JSON.stringify([context.generation, context.home, context.threadId, context.resumeRequestRef, context.admissionSelectionEpoch]);
  return { accepted: true, context, scope, notice: context.state === "queued" || context.state === "reading"
    ? "Prior work is loading. The conversation is open; this read does not send a message."
    : context.state === "unavailable" ? "Some prior work could not be read. Any readable page below is a separately matched partial snapshot. No automatic retry."
    : context.state === "empty" ? "The bounded read returned an empty page. Other pages or unrecorded work are not established."
    : "Prior work: bounded partial snapshot from this admitted conversation." };
}

export function continuationPageBinding(host: Json, thread: Json, kind: "turns" | "items"): HistoryPageBinding {
  const owner = continuationContextBinding(host, thread);
  const binding = historyPageBinding({ state: host?.state, generation: host?.generation, nativeHistory: owner.context?.history }, kind);
  if (!owner.accepted) return { ...binding, accepted: false, page: null, notice: owner.notice };
  if (binding.accepted && (binding.query?.params?.limit !== owner.context.pageLimits[kind] || binding.page.data.length > owner.context.pageLimits[kind])) {
    return { ...binding, accepted: false, page: null, notice: "The bounded prior-work query limit is not established. Readable rows and paging are withheld." };
  }
  if (binding.accepted && !list(owner.context.receipts).some(receipt => receipt?.sourceCurrent === true
    && receipt.home === owner.context.home && sameGeneration(receipt.generation, owner.context.generation)
    && nonempty(receipt.requestRef) && receipt.requestIdentity != null && receipt.writeResult === "written" && receipt.outcome === "response-observed-result"
    && positive(receipt.receiptPosition)
    && JSON.stringify(receipt.query) === JSON.stringify(binding.query))) {
    return { ...binding, accepted: false, page: null, notice: "The prior-work page has no matching accepted native read receipt. Readable rows and paging are withheld." };
  }
  return binding;
}

export function ContinuationContext({ host, thread }: { host: Json; thread: Json }) {
  const owner = continuationContextBinding(host, thread);
  const context = owner.context;
  const turns = continuationPageBinding(host, thread, "turns"), items = continuationPageBinding(host, thread, "items");
  const [attempt, setAttempt] = useState<Json>(null);
  const serial = useRef(0);
  const latest = useRef(owner);
  latest.current = owner;
  useEffect(() => () => { serial.current++; }, []);
  if (thread?.nativeResumeObserved !== true || !nonempty(thread?.resumeRequestRef)) return null;
  const pending = owner.accepted && attempt?.scope === owner.scope && attempt?.revision === context.revision && ["requesting", "queued"].includes(attempt.state);
  const failure = owner.accepted && attempt?.scope === owner.scope && attempt?.revision === context.revision && attempt.state === "failed" ? attempt.error : null;
  const reading = context?.state === "queued" || context?.state === "reading";
  const canRead = owner.accepted && !pending && !reading;
  const action = async (kind: string, cursor: string | null = null, direction = "desc", turnId: string | null = null) => {
    if (!canRead) return;
    const token = ++serial.current, scope = owner.scope, revision = context.revision;
    setAttempt({ scope, revision, state: "requesting" });
    try {
      await invoke("continuation_context_action", { generation: context.generation, threadId: context.threadId, resumeRequestRef: context.resumeRequestRef, revision, action: kind, cursor, direction, turnId });
      if (serial.current === token && latest.current.scope === scope && latest.current.context?.revision === revision) setAttempt({ scope, revision, state: "queued" });
    } catch (error) {
      if (serial.current === token && latest.current.scope === scope && latest.current.context?.revision === revision) setAttempt({ scope, revision, state: "failed", error: String(error) });
    }
  };
  const paging = (kind: "turns" | "items", binding: HistoryPageBinding) => { const kindWords = kind === "turns" ? "turns" : "items"; return binding.accepted && <p>
    {nonempty(binding.page.nextCursor) && <button disabled={!canRead} onClick={() => { void action(kind, binding.page.nextCursor, binding.query.params.sortDirection, kind === "items" ? binding.query.params.turnId : null); }}>Read more {kindWords}</button>}{" "}
    {nonempty(binding.page.backwardsCursor) && <button disabled={!canRead} onClick={() => { void action(kind, binding.page.backwardsCursor, binding.query.params.sortDirection === "desc" ? "asc" : "desc", kind === "items" ? binding.query.params.turnId : null); }}>Read previous {kindWords} page</button>}
    <small> {binding.page.nextCursor === null ? "This paging direction is exhausted; this is not a complete conversation." : binding.page.nextCursor === undefined ? "Next cursor not reported." : "More may be read explicitly."}</small>
  </p>; };
  return <section aria-label="Prior work in continued conversation">
    <h3>Prior work</h3>
    <p role="status">{owner.notice}</p>
    <p><small>Transient, read-only context; at most 20 turn summaries and 50 items in each page. This is not a complete transcript or a rebuild of live state. Native statuses describe the read. Original role, CCE authority, pending requests and checklist revisions are not restored by these pages.</small></p>
    {pending && <p role="status">Prior-work read requested; waiting for the current host context.</p>}
    {failure && <p role="alert">Prior-work read request failed: <AgentText value={failure} source="codex" label="Reported:" name="What the failed request reported, not the App's words" />. No resume or message was retried.</p>}
    {owner.accepted && <>
      <p><small>Source home <SuppliedId value={context.home} label="Home:" name="Home, as recorded; the App does not vouch for its words" /> · conversation <SuppliedId value={context.threadId} label="Conversation:" name="Conversation identity as Codex reported it, not the App's words" /> · admitted resume <SuppliedId value={context.resumeRequestRef} label="Resume:" name="Resume reference, as recorded; the App does not vouch for its words" />.</small></p>
      {context.error != null && <p role="alert">Prior-work read: <AgentText value={text(context.error)} source="codex" label="Reported:" name="What the prior-work read reported, not the App's words" /></p>}
      {context.state === "unavailable" && <button disabled={!canRead} onClick={() => { void action("retry"); }}>Retry prior-work read</button>}
      <h4>Prior turn summaries</h4>{paging("turns", turns)}
      <StoredTurnPage binding={turns} canRead={canRead} readItems={turnId => { void action("items", null, "desc", turnId); }} />
      <h4>Prior messages and work</h4>{paging("items", items)}
      <StoredItemPage binding={items} />
    </>}
    {context && <details><summary>Prior-work source and read evidence</summary><AgentText block value={JSON.stringify(context, null, 2)} source="codex" label="The read, with the pages Codex sent (JSON):" name="Prior-work read with Codex's pages, not the App's words" /></details>}
  </section>;
}
