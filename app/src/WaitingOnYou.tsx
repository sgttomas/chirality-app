import type { MouseEvent, ReactNode } from "react";
import { AgentText } from "./AgentText";
import { AskedBy, WaitingRequestsIndicator, answerable, hostRequests, requestAsker, requestThread, type RequestAsker, type WaitingRequestGroup } from "./RequestCards";
import { requestAnchorId, sameActivityGeneration } from "./NativeActivity";
import { runEvidenceAnchor } from "./RunJourney";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// "Waiting on you" (DEL-01-04): one place, under the sticky navigation and
// seen on every view, listing what waits on the person. It is a view, not a
// queue. Each entry is one source's own record, read from that source and
// keyed by its identity and revision: a supplier request in the host's
// register, a checkpoint arrival in a run record, a return in the fleet
// packet's review queue, or a decision package in the decision view. The list
// settles nothing and hides nothing: an entry leaves only when its source
// records the answer, and "Go to it" opens the source's own control, which
// refuses a stale answer. Related obligations stay separate entries. The words
// never say "held".

export type WaitingKind =
  | "question"
  | "tool-permission"
  | "pause"
  // Named for a checkpoint arrival that is a completed turn. The checkpoint
  // recorder records arrivals only from a completed agent message, a completed
  // file change or the start of a capability's item, so nothing selects it yet.
  | "turn-completed"
  | "return"
  | "decision"
  | "requests-in-another-home"
  // A point that waits on the person through an App-supplied tool call can wait
  // with no time limit, and its end is known only from the turn's end. If
  // Codex stops with it outstanding it is not raised again. Nothing feeds this
  // state yet: no source records such a call, and none is made up here.
  | "app-call-unanswered-at-codex-stop";

/** What is waiting, in the App's words. */
export const WAITING_WORDS: Record<WaitingKind, string> = {
  question: "a question is waiting",
  "tool-permission": "a tool permission is waiting",
  pause: "the agent was asked to pause",
  "turn-completed": "a turn completed",
  return: "a return is waiting for review",
  decision: "a decision is waiting",
  "requests-in-another-home": "questions or tool permissions are waiting in another home",
  "app-call-unanswered-at-codex-stop": "the call was not answered before Codex stopped; it will not be asked again",
};

/** Who asks, as each source records it. Agent-supplied values are drawn through AgentText. */
export type WaitingAsker =
  | { kind: "request"; asker: RequestAsker }
  | { kind: "returned-by"; who: string }
  | { kind: "requested-by"; who: string | null }
  | { kind: "checkpoint"; checkpoint: string; requester: string | null };

/** What the entry concerns. */
export type WaitingConcern =
  | { kind: "conversation"; threadId: string | null; home: string | null }
  | { kind: "run"; run: string; conversation: string | null }
  | { kind: "assignment"; undertaking: string; item: string }
  | { kind: "decision-package"; package: string };

/** Where "Go to it" leads: always the source's existing control or record. */
export type WaitingTarget =
  | { kind: "request"; group: WaitingRequestGroup; anchor: string | null }
  | { kind: "run"; anchor: string }
  | { kind: "return"; anchor: string }
  | { kind: "decision"; anchor: string };

export type WaitingGroup = { key: string; label: { kind: "conversation"; threadId: string | null; home: string | null; otherHome: boolean } | { kind: "assignment"; undertaking: string; item: string } | { kind: "none" } };

export type WaitingEntry = {
  /** The source record's identity and revision. */
  key: string;
  source: "supplier-request" | "checkpoint-arrival" | "return-review" | "decision-package" | "waiting-overview";
  kind: WaitingKind;
  /** 1 for a record; a group's count for requests read only as a count in another home. */
  count: number;
  asker: WaitingAsker;
  /** Who must respond. */
  responder: string;
  concerns: WaitingConcern;
  /** No source records who integrates the result. */
  integrator: "not recorded";
  group: WaitingGroup;
  /** When the source was read, for a source that can be stale between reads (ms since the epoch). */
  asOf: number | null;
  target: WaitingTarget;
};

/** How often the decision packages are read again while the App is open
 * (Journeys' own number: frequent enough that an entry appears soon, light
 * enough for a file read). The return-review queue is read when the list is
 * opened. The host status read that carries requests and run records keeps its
 * own POLL_MS. */
export const WAITING_SOURCE_POLL_MS = 15_000;

const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const hex = (value: string): string => Array.from(value, c => c.charCodeAt(0).toString(16).padStart(4, "0")).join("");
export const returnReviewAnchor = (returnRef: string) => `return-review-${hex(returnRef)}`;
export const decisionPackageAnchor = (pkg: string) => `decision-package-${hex(pkg)}`;

const QUESTIONS = ["item/tool/requestUserInput", "mcpServer/elicitation/request"];
const TOOL_PERMISSIONS = ["item/commandExecution/requestApproval", "item/fileChange/requestApproval", "item/permissions/requestApproval", "execCommandApproval", "applyPatchApproval"];
const sameJson = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

/** The conversation a thread belongs to: the top of its delegation chain in the
 * host's view of the same Codex process, else the thread itself. */
function rootConversation(threadId: string | null, generation: Json, view: Json): string | null {
  if (!threadId || !sameActivityGeneration(generation, view?.generation)) return threadId;
  const nodes = list(view?.descendants);
  let current = threadId;
  const seen = new Set<string>();
  for (;;) {
    if (seen.has(current)) return current;
    seen.add(current);
    const node = nodes.find((n: Json) => n?.threadId === current);
    if (!node || typeof node.parentThreadId !== "string" || !node.parentThreadId) return current;
    current = node.parentThreadId;
  }
}

/** The person's answerable requests in the active home's current register:
 * the same records the host counts for the waiting overview. A request the
 * App answers by rule, or one not offered for the person's answer, is not
 * listed. */
function requestEntries(host: Json): WaitingEntry[] {
  if (host?.state !== "ready" || !host?.generation) return [];
  const home = text(host?.homeRouting?.activeModeHomeClass) || null;
  return hostRequests(host).filter((r: Json) => answerable(r) && sameJson(r?.generation, host.generation) && r?.closedGeneration !== true).map((r: Json) => {
    const threadId = requestThread(r);
    const root = rootConversation(threadId, r.generation, host?.nativeView);
    const method = text(r?.method);
    return {
      key: JSON.stringify(["supplier-request", r.generation, r.requestIdentity, r.state, r.replyWriteResult ?? null]),
      source: "supplier-request", kind: QUESTIONS.includes(method) ? "question" : TOOL_PERMISSIONS.includes(method) ? "tool-permission" : "question",
      count: 1, asker: { kind: "request", asker: requestAsker(threadId, r.generation, host?.nativeView) }, responder: "you",
      concerns: { kind: "conversation", threadId, home }, integrator: "not recorded",
      group: { key: JSON.stringify(["conversation", home, root]), label: { kind: "conversation", threadId: root, home, otherHome: false } },
      asOf: null,
      target: { kind: "request", group: { modeHomeClass: home ?? "", generation: r.generation, threadId, count: 1 }, anchor: requestAnchorId(r.generation, r.requestIdentity) },
    } satisfies WaitingEntry;
  });
}

/** Requests in homes other than the active one: the host's overview gives only
 * a count per conversation there, so each such group is one entry with its count. */
function otherHomeEntries(host: Json): WaitingEntry[] {
  const active = text(host?.homeRouting?.activeModeHomeClass);
  return list(host?.waitingRequests?.groups).filter((g: Json) => text(g?.modeHomeClass) !== active && Number.isInteger(g?.count) && g.count > 0).map((g: Json) => {
    const threadId = typeof g.threadId === "string" && g.threadId ? g.threadId : null;
    const home = text(g.modeHomeClass);
    return {
      key: JSON.stringify(["waiting-overview", home, g.generation, threadId, g.count]),
      source: "waiting-overview", kind: "requests-in-another-home", count: g.count,
      asker: { kind: "request", asker: requestAsker(threadId, g.generation, host?.nativeView) }, responder: "you",
      concerns: { kind: "conversation", threadId, home }, integrator: "not recorded",
      group: { key: JSON.stringify(["conversation", home, threadId]), label: { kind: "conversation", threadId, home, otherHome: true } },
      asOf: null, target: { kind: "request", group: { modeHomeClass: home, generation: g.generation, threadId, count: g.count }, anchor: null },
    } satisfies WaitingEntry;
  });
}

const sameArrival = (a: Json, checkpoint: string, ordinal: Json) => text(a?.checkpoint) === checkpoint && a?.arrivalOrdinal === ordinal;
const ACTOR: Record<string, string> = { the_person: "you", the_accountable_professional: "the accountable professional" };

/** Checkpoint arrivals whose latest recorded disposition is "waiting", in runs
 * that have not ended (after a run ends an act no longer changes an arrival). */
function arrivalEntries(host: Json): WaitingEntry[] {
  const entries: WaitingEntry[] = [];
  for (const run of list(host?.workflowRoot?.runs)) {
    const records = list(run?.lifecycle?.records);
    if (run?.lifecycle?.end || records.some((r: Json) => r?.kind === "run_ended")) continue;
    const declaration = list(run?.compatibility).find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration;
    const declared = list(declaration?.elements?.checkpoints);
    const conversation = typeof run?.conversation === "string" && run.conversation ? run.conversation : null;
    const home = text(run?.home) || null;
    for (const arrival of records.filter((r: Json) => r?.kind === "checkpoint_arrival" && typeof r?.body?.checkpoint === "string")) {
      const b = arrival.body;
      const changes = records.filter((r: Json) => r?.kind === "disposition_change" && sameArrival(r?.body?.arrival, b.checkpoint, b.arrivalOrdinal));
      const latest = changes[changes.length - 1];
      if (latest?.body?.disposition !== "waiting") continue;
      const request = records.filter((r: Json) => r?.kind === "act_request" && sameArrival(r?.body?.arrival, b.checkpoint, b.arrivalOrdinal)).pop();
      const actor = declared.find((e: Json) => text(e?.value?.name) === b.checkpoint)?.value?.actor;
      entries.push({
        key: JSON.stringify(["checkpoint-arrival", run.reference, arrival.recordId ?? [b.checkpoint, b.arrivalOrdinal], latest.recordId ?? changes.length]),
        source: "checkpoint-arrival", kind: "pause", count: 1,
        asker: { kind: "checkpoint", checkpoint: b.checkpoint, requester: request ? text(request.body?.requester?.kind) || null : null },
        responder: ACTOR[text(actor)] ?? "you",
        concerns: { kind: "run", run: text(run.reference), conversation }, integrator: "not recorded",
        group: { key: JSON.stringify(["conversation", home, conversation]), label: { kind: "conversation", threadId: conversation, home, otherHome: false } },
        asOf: null, target: { kind: "run", anchor: runEvidenceAnchor(run.reference) },
      });
    }
  }
  return entries;
}

/** Returns awaiting review in the fleet packet's return-review queues. */
function returnEntries(fleet: Json, readAt: number | null): WaitingEntry[] {
  const entries: WaitingEntry[] = [];
  for (const view of list(fleet?.workspace?.undertakings)) {
    for (const row of list(view?.queue)) {
      if (row?.state !== "awaiting review" || typeof row?.returnRef !== "string") continue;
      const undertaking = text(view.undertaking), item = text(row.item);
      entries.push({
        key: JSON.stringify(["return-review", undertaking, row.returnRef, row.state]),
        source: "return-review", kind: "return", count: 1, asker: { kind: "returned-by", who: text(row.returnedBy) }, responder: "you",
        concerns: { kind: "assignment", undertaking, item }, integrator: "not recorded",
        group: { key: JSON.stringify(["assignment", undertaking, item]), label: { kind: "assignment", undertaking, item } },
        asOf: readAt, target: { kind: "return", anchor: returnReviewAnchor(row.returnRef) },
      });
    }
  }
  return entries;
}

const NO_REQUESTER = "requester identity not established";

/** Decision packages pending the person's decision. */
function decisionEntries(decisions: Json, readAt: number | null): WaitingEntry[] {
  return list(decisions?.rows).filter((row: Json) => typeof row?.package === "string" && text(row?.state).startsWith("pending")).map((row: Json) => ({
    key: JSON.stringify(["decision-package", row.package, row.requestSources ?? null, row.state]),
    source: "decision-package", kind: "decision", count: 1,
    asker: { kind: "requested-by", who: typeof row.requestedBy === "string" && row.requestedBy && row.requestedBy !== NO_REQUESTER ? row.requestedBy : null }, responder: "you",
    concerns: { kind: "decision-package", package: row.package }, integrator: "not recorded",
    group: { key: "none", label: { kind: "none" } }, asOf: readAt, target: { kind: "decision", anchor: decisionPackageAnchor(row.package) },
  } satisfies WaitingEntry));
}

export type WaitingSources = { host: Json; fleet?: Json; fleetReadAt?: number | null; decisions?: Json; decisionsReadAt?: number | null };

/** Every entry waiting on the person, one per source record, in source order. */
export function waitingEntries({ host, fleet = null, fleetReadAt = null, decisions = null, decisionsReadAt = null }: WaitingSources): WaitingEntry[] {
  return [...requestEntries(host), ...arrivalEntries(host), ...otherHomeEntries(host), ...returnEntries(fleet, fleetReadAt), ...decisionEntries(decisions, decisionsReadAt)];
}

/** The entries grouped by assignment where one exists, otherwise by conversation, in first-seen order. */
export function waitingGroups(entries: WaitingEntry[]): { group: WaitingGroup; entries: WaitingEntry[] }[] {
  const groups: { group: WaitingGroup; entries: WaitingEntry[] }[] = [];
  for (const entry of entries) {
    const found = groups.find(g => g.group.key === entry.group.key);
    if (found) found.entries.push(entry); else groups.push({ group: entry.group, entries: [entry] });
  }
  return groups;
}

export const waitingTotal = (entries: WaitingEntry[]) => entries.reduce((sum, entry) => sum + entry.count, 0);
/** How many of them are requests from Codex, in every home: a part of the same count, never a second one. */
export const waitingRequestCount = (entries: WaitingEntry[]) => waitingTotal(entries.filter(entry => entry.source === "supplier-request" || entry.source === "waiting-overview"));
/** The one line: everything waiting, and how many of those are requests from Codex. */
export function waitingLine(entries: WaitingEntry[]): string {
  const requests = waitingRequestCount(entries);
  return `Waiting on you: ${waitingTotal(entries)}${requests > 0 ? ` (${requests} request${requests === 1 ? "" : "s"} from Codex)` : ""}`;
}

const pad = (n: number) => String(n).padStart(2, "0");
/** "as of ‹time›" in local hours, minutes and seconds. */
export const asOfWords = (at: number) => { const d = new Date(at); return `as of ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; };

function GroupLabel({ group }: { group: WaitingGroup }) {
  const label = group.label;
  if (label.kind === "none") return <>No conversation or assignment recorded</>;
  if (label.kind === "assignment") return <>Assignment: undertaking <AgentText value={label.undertaking} label="Undertaking:" name="Undertaking as recorded, not the App's words" />, item <AgentText value={label.item} label="Item:" name="Work item as recorded, not the App's words" /></>;
  const where = label.otherHome ? ` in the ${label.home ?? "unreported"} home` : "";
  return label.threadId ? <>Conversation <code>{label.threadId}</code>{where}</> : <>No conversation named{where}</>;
}

function Asker({ asker }: { asker: WaitingAsker }) {
  switch (asker.kind) {
    case "request": return <AskedBy asker={asker.asker} />;
    case "returned-by": return <>Returned by <AgentText value={asker.who} label="Returned by:" name="Who returned it, as recorded, not the App's words" /></>;
    case "requested-by": return asker.who === null ? <>Requested by: not established</> : <>Requested by <AgentText value={asker.who} label="Requested by:" name="Who requested the decision, as the package records it, not the App's words" /></>;
    case "checkpoint": return <>Asked at the workflow's checkpoint <AgentText value={asker.checkpoint} label="Checkpoint:" name="Checkpoint name as declared, not the App's words" />{asker.requester ? <>; a request for the act was observed from <AgentText value={asker.requester} label="Requester:" name="Requester as recorded, not the App's words" /></> : null}</>;
  }
}

function Concerns({ concerns }: { concerns: WaitingConcern }) {
  switch (concerns.kind) {
    case "conversation": return concerns.threadId ? <>the conversation <code>{concerns.threadId}</code></> : <>no conversation named</>;
    case "run": return <>the run <code>{concerns.run}</code>{concerns.conversation ? <> in the conversation <code>{concerns.conversation}</code></> : null}</>;
    case "assignment": return <>undertaking <AgentText value={concerns.undertaking} label="Undertaking:" name="Undertaking as recorded, not the App's words" />, item <AgentText value={concerns.item} label="Item:" name="Work item as recorded, not the App's words" /></>;
    case "decision-package": return <>the decision package <AgentText value={concerns.package} label="Package:" name="Decision package name as recorded, not the App's words" /></>;
  }
}

/** One entry: what waits, who asks, who must respond, what it concerns, who integrates, and the way to its control. */
export function WaitingEntryRow({ entry, go }: { entry: WaitingEntry; go: (entry: WaitingEntry) => void }) {
  const href = entry.target.kind === "request" ? entry.target.anchor ? `#${entry.target.anchor}` : "#other-requests" : `#${entry.target.anchor}`;
  const open = (event: MouseEvent<HTMLAnchorElement>) => { event.preventDefault?.(); event.stopPropagation?.(); go(entry); };
  const parts: ReactNode[] = [
    <strong key="what">{WAITING_WORDS[entry.kind]}{entry.count > 1 ? ` (${entry.count})` : ""}</strong>,
    <span key="asks"><Asker asker={entry.asker} /></span>,
    <span key="responds">Who must respond: {entry.responder}</span>,
    <span key="concerns">Concerns: <Concerns concerns={entry.concerns} /></span>,
    <span key="integrates">Who integrates the result: {entry.integrator}</span>,
  ];
  if (entry.asOf !== null) parts.push(<small key="as-of">{asOfWords(entry.asOf)}</small>);
  return <div className="waiting-on-you-entry" data-waiting-key={entry.key} data-waiting-source={entry.source}>
    {parts.flatMap((part, i) => i === 0 ? [part] : [<span key={`sep${i}`} aria-hidden="true"> · </span>, part])}
    {" "}<a href={href} onClick={open}>Go to it</a>
  </div>;
}

/** The place: one line, "Waiting on you: N", that opens to the list. */
export function WaitingOnYou({ entries, overview, view, busy = false, openGroup, go, onOpen, fleetFailure = null }: {
  entries: WaitingEntry[]; overview: Json; view?: Json; busy?: boolean; openGroup: (group: WaitingRequestGroup) => void; go: (entry: WaitingEntry) => void;
  /** Called each time the person opens the list: the App reads the return-review queue then. */
  onOpen?: () => void;
  /** The last read of the return-review queue on opening failed; returns shown are as of the earlier read. */
  fleetFailure?: string | null;
}) {
  const total = waitingTotal(entries);
  return <section className="waiting-on-you" aria-label="Waiting on you">
    <details id="waiting-on-you" onToggle={event => { if ((event.currentTarget as HTMLDetailsElement).open) onOpen?.(); }}>
      <summary><span role="status" aria-live="polite">{waitingLine(entries)}</span></summary>
      <div className="waiting-on-you-list">
        {total === 0 && <p>Nothing recorded is waiting on you.</p>}
        {waitingGroups(entries).map(({ group, entries }) => <div key={group.key} className="waiting-on-you-group" role="group" aria-label="Entries of one conversation or assignment">
          <p className="waiting-on-you-group-label"><GroupLabel group={group} /></p>
          {entries.map(entry => <WaitingEntryRow key={entry.key} entry={entry} go={go} />)}
        </div>)}
        {fleetFailure && <p role="note">Returns could not be read when this list was opened; returns shown are as of the earlier read.</p>}
        <WaitingRequestsIndicator overview={overview} view={view} busy={busy} open={openGroup} />
        <p><small>Each entry is its source's own record and leaves when that source records the answer. Returns are read each time you open this list. Nothing here answers, dismisses or settles anything; Go to it opens the existing control, which checks that the record is still current. Returns have no review control in the App yet: Go to it shows the return's record.</small></p>
      </div>
    </details>
  </section>;
}
