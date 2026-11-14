import { useRef, type MouseEvent, type ReactNode } from "react";
import { AgentText, plainId } from "./AgentText";
import { AskedBy, WaitingRequestsIndicator, answerable, hostRequests, requestAsker, requestThread, type RequestAsker, type WaitingRequestGroup } from "./RequestCards";
import { requestAnchorId, sameActivityGeneration } from "./NativeActivity";
import { runEvidenceAnchor } from "./RunJourney";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// "Waiting on you" (DEL-01-04): one place, under the sticky navigation and
// seen on every view, listing what waits on the person. It is a view, not a
// queue. Each entry is one source's own record, read from that source and
// keyed by its identity and revision: a supplier request in the host's
// register, a checkpoint arrival in a run record, a return in the fleet
// packet's review queue, or a decision package in the decision view.
//
// Every source is held as a reading (waitingReadings), and one function,
// decideReading, says what each reading is: read whole, read with limits, not
// read, or a failed read whose last good reading is kept with its time. A
// reading is whole only where its reader positively says so; each adapter
// names the host field that says it. Only when every reading is whole does the
// line give a definite count or the list say that nothing is waiting.
// Otherwise the line counts only what is observed now and says the status is
// incomplete, and what an earlier reading showed waiting stays apart, as last
// seen at its time with its current state unknown, until its source is read
// whole again or records a disposition for that very record. Absence from a
// reading that is not whole retires nothing.
//
// The list settles nothing; "Go to it" opens the source's existing control or
// record (what each control checks is said in the list's footer). Related
// obligations stay separate entries. The words never say "held".

export type WaitingKind =
  | "question"
  | "tool-permission"
  // A checkpoint arrival whose act is not yet recorded: the run reached a
  // declared checkpoint. Nothing records that the agent was asked to pause there.
  | "checkpoint-reached"
  // Named for the point call, when one exists: a point that asked the agent to
  // pause. Nothing feeds it yet; an arrival is never said to be one.
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
  "checkpoint-reached": "a checkpoint was reached; your act is not yet recorded",
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
  /** The source record's identity without its revision: what a disposition recorded for that record settles. */
  item: string;
  source: "supplier-request" | "checkpoint-arrival" | "return-review" | "decision-package" | "waiting-overview";
  kind: WaitingKind;
  /** 1 for a record; a group's count for requests read only as a count in another home. */
  count: number;
  asker: WaitingAsker;
  /** Who must respond: the App's words, or, for a return, who prepared its brief as the record names them. */
  responder: string | { kind: "brief-preparer"; who: string | null };
  concerns: WaitingConcern;
  /** No source records who integrates the result. */
  integrator: "not recorded";
  group: WaitingGroup;
  /** When the source was read, for a source that can be stale between reads (ms since the epoch). */
  asOf: number | null;
  target: WaitingTarget;
};

/** How often the decision packages and the return-review queue are read again
 * while the App is open. The Journeys lane's own number, not a requirement:
 * frequent enough that an entry appears soon, light enough for a file read. The
 * return-review queue is also read when the list is opened. The host status
 * read that carries requests and run records keeps its own POLL_MS. */
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
 * listed. Requests in the register that are no longer outstanding are settled. */
function requestEntries(host: Json): { entries: WaitingEntry[]; settled: string[] } {
  if (host?.state !== "ready" || !host?.generation) return { entries: [], settled: [] };
  const home = text(host?.homeRouting?.activeModeHomeClass) || null;
  const requests = hostRequests(host).filter((r: Json) => sameJson(r?.generation, host.generation));
  const itemOf = (r: Json) => JSON.stringify(["supplier-request", r.generation, r.requestIdentity]);
  const settled = requests.filter((r: Json) => r?.state !== "outstanding" || r?.closedGeneration === true).map(itemOf);
  const entries = requests.filter((r: Json) => answerable(r) && r?.closedGeneration !== true).map((r: Json) => {
    const threadId = requestThread(r);
    const root = rootConversation(threadId, r.generation, host?.nativeView);
    const method = text(r?.method);
    return {
      key: JSON.stringify(["supplier-request", r.generation, r.requestIdentity, r.state, r.replyWriteResult ?? null]), item: itemOf(r),
      source: "supplier-request", kind: QUESTIONS.includes(method) ? "question" : TOOL_PERMISSIONS.includes(method) ? "tool-permission" : "question",
      count: 1, asker: { kind: "request", asker: requestAsker(threadId, r.generation, host?.nativeView) }, responder: "you",
      concerns: { kind: "conversation", threadId, home }, integrator: "not recorded",
      group: { key: JSON.stringify(["conversation", home, root]), label: { kind: "conversation", threadId: root, home, otherHome: false } },
      asOf: null,
      target: { kind: "request", group: { modeHomeClass: home ?? "", generation: r.generation, threadId, count: 1 }, anchor: requestAnchorId(r.generation, r.requestIdentity) },
    } satisfies WaitingEntry;
  });
  return { entries, settled };
}

/** Requests in one home other than the active one: the host's overview gives only
 * a count per conversation there, so each such group is one entry with its count. */
function otherHomeEntries(host: Json, home: string): WaitingEntry[] {
  return list(host?.waitingRequests?.groups).filter((g: Json) => text(g?.modeHomeClass) === home && Number.isInteger(g?.count) && g.count > 0).map((g: Json) => {
    const threadId = typeof g.threadId === "string" && g.threadId ? g.threadId : null;
    return {
      key: JSON.stringify(["waiting-overview", home, g.generation, threadId, g.count]), item: JSON.stringify(["waiting-overview", home, g.generation, threadId]),
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

/** A run's checkpoint arrivals from its lifecycle records: those whose latest recorded disposition is
 * "waiting" in a run that has not ended are entries; every other arrival is settled (after a run ends an
 * act no longer changes an arrival). Used for a hot run, and for a reopened run once the host gives its
 * lifecycle records. */
function arrivalsOf(run: Json, reference: string): { entries: WaitingEntry[]; settled: string[] } {
  const entries: WaitingEntry[] = [], settled: string[] = [];
  const records = list(run?.lifecycle?.records);
  const ended = !!run?.lifecycle?.end || records.some((r: Json) => r?.kind === "run_ended");
  const declaration = list(run?.compatibility).find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration;
  const declared = list(declaration?.elements?.checkpoints);
  const conversation = typeof run?.conversation === "string" && run.conversation ? run.conversation : null;
  const home = text(run?.home) || null;
  for (const arrival of records.filter((r: Json) => r?.kind === "checkpoint_arrival" && typeof r?.body?.checkpoint === "string")) {
    const b = arrival.body;
    const item = JSON.stringify(["checkpoint-arrival", reference, arrival.recordId ?? [b.checkpoint, b.arrivalOrdinal]]);
    const changes = records.filter((r: Json) => r?.kind === "disposition_change" && sameArrival(r?.body?.arrival, b.checkpoint, b.arrivalOrdinal));
    const latest = changes[changes.length - 1];
    if (ended || latest?.body?.disposition !== "waiting") { if (ended || latest) settled.push(item); continue; }
    const request = records.filter((r: Json) => r?.kind === "act_request" && sameArrival(r?.body?.arrival, b.checkpoint, b.arrivalOrdinal)).pop();
    const actor = declared.find((e: Json) => text(e?.value?.name) === b.checkpoint)?.value?.actor;
    entries.push({
      key: JSON.stringify(["checkpoint-arrival", reference, arrival.recordId ?? [b.checkpoint, b.arrivalOrdinal], latest.recordId ?? changes.length]), item,
      source: "checkpoint-arrival", kind: "checkpoint-reached", count: 1,
      asker: { kind: "checkpoint", checkpoint: b.checkpoint, requester: request ? text(request.body?.requester?.kind) || null : null },
      responder: ACTOR[text(actor)] ?? "you",
      concerns: { kind: "run", run: reference, conversation }, integrator: "not recorded",
      group: { key: JSON.stringify(["conversation", home, conversation]), label: { kind: "conversation", threadId: conversation, home, otherHome: false } },
      asOf: null, target: { kind: "run", anchor: runEvidenceAnchor(reference) },
    });
  }
  return { entries, settled };
}

const NO_REQUESTER = "requester identity not established";
const NO_EXAMINER = "examiner not established";
const AWAITING_REVIEW = "awaiting review";
const returnItem = (undertaking: string, returnRef: string) => JSON.stringify(["return-review", undertaking, returnRef]);

/** Returns awaiting review in the fleet packet's return-review queues; a queued return in any other state is settled. */
function returnEntries(fleet: Json, readAt: number | null): { entries: WaitingEntry[]; settled: string[] } {
  const entries: WaitingEntry[] = [], settled: string[] = [];
  for (const view of list(fleet?.workspace?.undertakings)) {
    for (const row of list(view?.queue)) {
      if (typeof row?.returnRef !== "string") continue;
      const undertaking = text(view.undertaking), item = text(row.item);
      if (row?.state !== AWAITING_REVIEW) { settled.push(returnItem(undertaking, row.returnRef)); continue; }
      entries.push({
        key: JSON.stringify(["return-review", undertaking, row.returnRef, row.state]), item: returnItem(undertaking, row.returnRef),
        source: "return-review", kind: "return", count: 1, asker: { kind: "returned-by", who: text(row.returnedBy) },
        // The queue's examiner is whoever prepared the brief, as recorded; the host drops whether that is a person
        // or an agent, so every return is listed, and none is said to be the person's unless the record says so.
        responder: { kind: "brief-preparer", who: typeof row.examines === "string" && row.examines && row.examines !== NO_EXAMINER ? row.examines.replace(/ \(prepared the brief\)$/, "") : null },
        concerns: { kind: "assignment", undertaking, item }, integrator: "not recorded",
        group: { key: JSON.stringify(["assignment", undertaking, item]), label: { kind: "assignment", undertaking, item } },
        asOf: readAt, target: { kind: "return", anchor: returnReviewAnchor(row.returnRef) },
      });
    }
  }
  return { entries, settled };
}

const PENDING = (state: Json) => text(state).startsWith("pending");
const DECIDED = "decided";

/** Decision packages pending the person's decision; a package the view shows decided is settled. */
function decisionEntries(decisions: Json, readAt: number | null): { entries: WaitingEntry[]; settled: string[] } {
  const rows = list(decisions?.rows).filter((row: Json) => typeof row?.package === "string");
  const itemOf = (row: Json) => JSON.stringify(["decision-package", row.package]);
  return {
    settled: rows.filter((row: Json) => row.state === DECIDED).map(itemOf),
    entries: rows.filter((row: Json) => PENDING(row.state)).map((row: Json) => ({
      key: JSON.stringify(["decision-package", row.package, row.requestSources ?? null, row.state]), item: itemOf(row),
      source: "decision-package", kind: "decision", count: 1,
      asker: { kind: "requested-by", who: typeof row.requestedBy === "string" && row.requestedBy && row.requestedBy !== NO_REQUESTER ? row.requestedBy : null }, responder: "you",
      concerns: { kind: "decision-package", package: row.package }, integrator: "not recorded",
      group: { key: "none", label: { kind: "none" } }, asOf: readAt, target: { kind: "decision", anchor: decisionPackageAnchor(row.package) },
    } satisfies WaitingEntry)),
  };
}

// ---- Readings: how each source was read, and the one rule that decides it ----

/** How one source was read. Only "whole" lets the list give a definite count or say that nothing is waiting. */
export type ReadingState = "whole" | "limited" | "not-read" | "failed";

/** What an adapter found in its source, for decideReading. */
export type ReadEvidence = {
  /** Whether the read that supplies the source answered, was rejected, or has not been made yet. */
  call: "answered" | "rejected" | "not-made";
  /** Whether the answer holds anything of this source: a busy placeholder, null, or a lifecycle the records do not establish holds nothing. */
  read: boolean;
  /** Whether the source's reader positively says the reading is whole, through the field its adapter names. */
  affirmedWhole: boolean;
  /** What the reader says it could not read. Any limit keeps the reading from being whole. */
  limits: string[];
};

/** The one rule for every source: a reading is whole only on its reader's positive word with no limit. A
 * rejected read is a failed reading; nothing read is not read; anything else read is read with limits. */
export function decideReading(evidence: ReadEvidence): ReadingState {
  if (evidence.call === "not-made") return "not-read";
  if (evidence.call === "rejected") return "failed";
  if (!evidence.read) return "not-read";
  return evidence.affirmedWhole && evidence.limits.length === 0 ? "whole" : "limited";
}

export type SourceReading = {
  /** The source: "requests", "other-homes", "home:‹class›", "hot-runs", "run:‹reference›", "reopened", "reopened-run:‹run›", "returns" or "decisions". */
  key: string;
  /** The reading that lists this one (a run in the hot runs, a home in the overview): when that reading is
   * whole and no longer lists this source, what this source last showed is retired. */
  parent: string | null;
  state: ReadingState;
  /** When the read that gave this reading was started (ms since the epoch), or null where none has been. */
  at: number | null;
  /** The entries observed in this reading. For a failed reading, those of the earlier reading still held, which are last seen, not observed now. */
  entries: WaitingEntry[];
  /** For a failed reading: when the earlier reading still held was started. */
  retainedAt: number | null;
  /** Records this reading itself shows settled: a fresh disposition for that very record. */
  settled: string[];
  /** The App's sentence for a reading that is not whole. */
  note: string | null;
};

type Notes = { limited: string; notRead: string; failed: string };
type Found = { evidence: Omit<ReadEvidence, "call">; entries: WaitingEntry[]; settled: string[] };
const nothing = (): Found => ({ evidence: { read: false, affirmedWhole: false, limits: [] }, entries: [], settled: [] });

function finish(key: string, parent: string | null, call: ReadEvidence["call"], found: Found, notes: Notes, at: number | null, retainedAt: number | null): SourceReading {
  const state = decideReading({ call, ...found.evidence });
  const held = state === "failed" && found.evidence.read;
  return {
    key, parent, state, at,
    entries: state === "whole" || state === "limited" || held ? found.entries : [],
    retainedAt: held ? retainedAt : null,
    settled: state === "whole" || state === "limited" ? found.settled : [],
    note: state === "whole" ? null : state === "limited" ? notes.limited : state === "failed" ? notes.failed : notes.notRead,
  };
}

const STATUS_FAILED = "The App's last read of its own status failed: requests from Codex and workflow runs are shown as last seen, and their current state is unknown.";
const REOPENED_RUN_NOT_READ = "reopened-run-not-read";
const RUN_STATE_ENDED = "ended";
const RUN_STATE_NOT_STARTED = "start not confirmed in record";

/** The readings carried by one host status read: requests in the active home, the hot runs and each of
 * them, the overview of other homes and each of them, and the census of runs reopened after a restart
 * and each of those. */
function hostReadings(host: Json, call: ReadEvidence["call"], at: number | null, retainedAt: number | null): SourceReading[] {
  const out: SourceReading[] = [];
  const failed = STATUS_FAILED;
  // Requests in the active home. The host gives the home's whole request register (serverRequests, the
  // register snapshot of native_requests.rs) whenever its Codex is ready with a generation: `state: "ready"`
  // with a `generation` and a `serverRequests` array is the positive word. Any other state is not read.
  const running = host?.state === "ready" && !!host?.generation && Array.isArray(host?.serverRequests);
  const requests = requestEntries(host);
  out.push(finish("requests", null, call, { evidence: { read: running, affirmedWhole: running, limits: [] }, ...requests },
    { limited: "", notRead: "Requests from Codex are not read while Codex is not running.", failed }, at, retainedAt));
  // Hot runs. The workflow root's `runs` is the host's table of every run in this process
  // (runtime_session.rs `snapshot`): an array there is the positive word that the table was read.
  const root = host?.workflowRoot;
  const runs = Array.isArray(root?.runs) ? root.runs : null;
  out.push(finish("hot-runs", null, call, { evidence: { read: !!runs, affirmedWhole: !!runs, limits: [] }, entries: [], settled: [] },
    { limited: "", notRead: "Workflow runs have not been read yet.", failed }, at, retainedAt));
  for (const run of runs ?? []) {
    const reference = text(run?.reference);
    // A run's own records are whole when the host gives its `lifecycle.records` array (lifecycle_view: every
    // entry the run holds in this process). A run whose lock is busy comes as the placeholder
    // {reference, state: "original run operation pending"} with no lifecycle: that is not read.
    const records = Array.isArray(run?.lifecycle?.records);
    const found = records ? { evidence: { read: true, affirmedWhole: true, limits: [] }, ...arrivalsOf(run, reference) } : nothing();
    out.push(finish(`run:${reference}`, "hot-runs", call, found,
      { limited: "", notRead: `The run ${reference} could not be read just now (an operation on it was in progress), so whether one of its checkpoints waits for your act is not known.`, failed }, at, retainedAt));
  }
  // Other homes. waiting_requests.rs `overview` lists every configured home in `sources`, each with the
  // `state` of its register: the overview is read when `sources` is an array naming the active home, and
  // a home's count is whole only where its source says `state: "ready"`.
  const active = text(host?.homeRouting?.activeModeHomeClass);
  const sources = Array.isArray(host?.waitingRequests?.sources) ? host.waitingRequests.sources : null;
  const overview = !!sources && sources.some((s: Json) => text(s?.modeHomeClass) === active);
  out.push(finish("other-homes", null, call, { evidence: { read: overview, affirmedWhole: overview, limits: [] }, entries: [], settled: [] },
    { limited: "", notRead: "Requests in other homes have not been read.", failed }, at, retainedAt));
  for (const source of overview ? sources! : []) {
    const home = text(source?.modeHomeClass);
    if (home === active) continue;
    const ready = source?.state === "ready";
    out.push(finish(`home:${home}`, "other-homes", call, { evidence: { read: ready, affirmedWhole: ready, limits: [] }, entries: otherHomeEntries(host, home), settled: [] },
      { limited: "", notRead: `Requests in the ${home || "unreported"} home are not read (${text(source?.state) || "state not reported"}).`, failed }, at, retainedAt));
  }
  // Runs reopened after the App restarted (record_supply.rs `RunsReading::view`, with the
  // `historyNotices` read_reopened_history attaches). The census is read when `reopened` holds a `runs`
  // array; it is whole only when its `limits` and `historyNotices` are both present and empty. Until the
  // person reopens recorded runs the host gives `reopened: null`: not read.
  const reopened = root?.reopened;
  const census = !!reopened && typeof reopened === "object" && Array.isArray(reopened.runs);
  const censusWhole = census && Array.isArray(reopened.limits) && Array.isArray(reopened.historyNotices);
  out.push(finish("reopened", null, call, { evidence: { read: census, affirmedWhole: censusWhole, limits: census ? [...list(reopened.limits), ...list(reopened.historyNotices)].map(text) : [] }, entries: [], settled: [] },
    { limited: "Runs recorded before the App restarted were read with limits: some may not be shown, and whether one of their checkpoints waits for your act is not known.",
      notRead: "Runs recorded before the App restarted have not been read, so whether one of their checkpoints waits for your act is not known. Reopen recorded workflow runs reads them.", failed }, at, retainedAt));
  for (const row of census ? reopened.runs : []) {
    const reference = text(row?.reference ?? row?.run);
    if ((runs ?? []).some((live: Json) => live?.reference === reference)) continue;   // a hot run's own reading covers it
    let found: Found;
    if (Array.isArray(row?.lifecycle?.records)) {
      // The shape the coming host read gives a reopened run: reference, lifecycle {state, end, records}
      // and limits. Its records are whole when `limits` is present and empty.
      found = { evidence: { read: true, affirmedWhole: Array.isArray(row?.limits), limits: list(row?.limits).map(text) }, ...arrivalsOf(row, reference) };
    } else if (row?.state === RUN_STATE_ENDED || row?.state === RUN_STATE_NOT_STARTED) {
      // An end recorded in the run's records, or a complete record set with no run_opened
      // (RecordedLifecycle::StartNotConfirmed is given only for a complete set): nothing of it can wait.
      found = { evidence: { read: true, affirmedWhole: true, limits: [] }, entries: [], settled: [] };
    } else {
      // Still open, or a lifecycle the records do not establish ("unknown"), or a state the App does not
      // know: its checkpoints are not read.
      found = nothing();
    }
    out.push(finish(`reopened-run:${reference}`, "reopened", call, found,
      { limited: "A run reopened after the App restarted was read with limits, so more of its checkpoints may be waiting.", notRead: REOPENED_RUN_NOT_READ, failed }, at, retainedAt));
  }
  return out;
}

/** The return-review queues in the fleet packet. read_fleet_records gives partial observations as values,
 * not as a rejected call: the packet is whole only when its `limits` array is empty, its project log says
 * `coordination.project.complete: true`, and every undertaking in `workspace.undertakings` says
 * `queueComplete: true` (fleet_records.rs, fleet_views.rs). */
function returnsReading(packet: Json, call: ReadEvidence["call"], at: number | null, retainedAt: number | null): SourceReading {
  const read = !!packet && typeof packet === "object";
  const undertakings = Array.isArray(packet?.workspace?.undertakings) ? packet.workspace.undertakings : null;
  const affirmedWhole = read && Array.isArray(packet.limits) && packet.coordination?.project?.complete === true
    && !!undertakings && undertakings.every((view: Json) => view?.queueComplete === true);
  const found: Found = read ? { evidence: { read, affirmedWhole, limits: list(packet.limits).map((l: Json) => text(l?.reason ?? l)) }, ...returnEntries(packet, retainedAt ?? at) } : nothing();
  return finish("returns", null, call, found,
    { limited: "Returns were read with limits, so more may be waiting for review.", notRead: "Returns have not been read yet.", failed: "Returns could not be read at the last attempt." }, at, retainedAt);
}

/** The decision view. decision_view gives partial observations as values: it is whole only when its
 * `limits`, `historyNotices` and `unresolvedRecords` arrays are all present and empty, and every row is
 * either pending or decided (a row whose standing is ambiguous or whose request identity cannot be
 * resolved may be waiting) (decision_view.rs `derive`). */
function decisionsReading(view: Json, call: ReadEvidence["call"], at: number | null, retainedAt: number | null): SourceReading {
  const read = !!view && typeof view === "object" && Array.isArray(view.rows);
  const unsettled = read ? view.rows.filter((row: Json) => !PENDING(row?.state) && row?.state !== DECIDED).map((row: Json) => `${text(row?.package)}: ${text(row?.state)}`) : [];
  const affirmedWhole = read && Array.isArray(view.limits) && Array.isArray(view.historyNotices) && Array.isArray(view.unresolvedRecords);
  const found: Found = read ? { evidence: { read, affirmedWhole, limits: [...list(view.limits).map(text), ...list(view.historyNotices).map(text), ...list(view.unresolvedRecords).map(() => "unresolved record"), ...unsettled] }, ...decisionEntries(view, retainedAt ?? at) } : nothing();
  return finish("decisions", null, call, found,
    { limited: "Decisions were read with limits, so more may be waiting.", notRead: "Decisions have not been read yet.", failed: "Decisions could not be read at the last attempt." }, at, retainedAt);
}

export type WaitingSources = {
  /** The status snapshot shown, the start time of the read that gave it, and whether a later status read failed (and when it started). */
  host: Json; hostReadAt?: number | null; hostFailure?: string | null; hostFailedAt?: number | null;
  /** The last good fleet packet, when its read started, and whether a later read failed. */
  fleet?: Json; fleetReadAt?: number | null; fleetFailure?: string | null; fleetFailedAt?: number | null;
  /** The last good decision view, when its read started, and whether a later read failed. */
  decisions?: Json; decisionsReadAt?: number | null; decisionsFailure?: string | null; decisionsFailedAt?: number | null;
};

const callOf = (value: Json, failure: string | null): ReadEvidence["call"] => failure ? "rejected" : value ? "answered" : "not-made";

/** Every source's reading. */
export function waitingReadings({ host, hostReadAt = null, hostFailure = null, hostFailedAt = null, fleet = null, fleetReadAt = null, fleetFailure = null, fleetFailedAt = null,
  decisions = null, decisionsReadAt = null, decisionsFailure = null, decisionsFailedAt = null }: WaitingSources): SourceReading[] {
  const timed = (failure: string | null, readAt: number | null, failedAt: number | null): [number | null, number | null] => failure ? [failedAt, readAt] : [readAt, null];
  return [
    ...hostReadings(host, callOf(host, hostFailure), ...timed(hostFailure, hostReadAt, hostFailedAt)),
    returnsReading(fleet, callOf(fleet, fleetFailure), ...timed(fleetFailure, fleetReadAt, fleetFailedAt)),
    decisionsReading(decisions, callOf(decisions, decisionsFailure), ...timed(decisionsFailure, decisionsReadAt, decisionsFailedAt)),
  ];
}

/** The entries observed now in every source, one per source record, in source order. */
export function waitingEntries(sources: WaitingSources): WaitingEntry[] {
  return waitingReadings(sources).filter(r => r.state === "whole" || r.state === "limited").flatMap(r => r.entries);
}

// ---- The list over time: what is observed now, and what was last seen ----

export type WaitingMemory = Record<string, { latest: SourceReading; lastWhole: { at: number | null; entries: WaitingEntry[] } | null }>;
export type LastSeen = { entry: WaitingEntry; at: number | null };
export type WaitingView = {
  readings: SourceReading[];
  /** Entries observed now, in a reading that answered: only these are counted. */
  observed: WaitingEntry[];
  /** Entries an earlier reading showed waiting whose source is not read whole now and has not recorded their disposition. */
  lastSeen: LastSeen[];
  /** Every source read whole: the only state in which the count is definite and "nothing is waiting" may be said. */
  complete: boolean;
  /** The App's sentences for what is not read whole. */
  notes: string[];
};

/** Folds the readings now into what the list remembers. A whole reading replaces what its source last
 * showed. A reading that is not whole keeps the entries the last whole reading showed, as last seen,
 * except those this reading observes now or itself shows settled; a failed reading also keeps those of
 * the earlier reading it still holds. A reading started before the one a source last took is not taken.
 * A source no longer listed is retired only where the reading that listed it is whole now. */
export function foldWaiting(memory: WaitingMemory, incoming: SourceReading[]): { memory: WaitingMemory; view: WaitingView } {
  const next: WaitingMemory = {};
  const readings = incoming.map(reading => {
    const before = memory[reading.key];
    const current = before && before.latest.at !== null && reading.at !== null && reading.at < before.latest.at ? before.latest : reading;
    next[current.key] = { latest: current, lastWhole: current.state === "whole" ? { at: current.at, entries: current.entries } : before?.lastWhole ?? null };
    return current;
  });
  const wholeNow = new Set(readings.filter(r => r.state === "whole").map(r => r.key));
  for (const [key, kept] of Object.entries(memory)) {
    if (next[key]) continue;
    if (kept.latest.parent !== null && wholeNow.has(kept.latest.parent)) continue;
    next[key] = kept;
  }
  const observed = readings.filter(r => r.state === "whole" || r.state === "limited").flatMap(r => r.entries);
  const now = new Set(observed.map(e => e.item));
  const settled = new Set(readings.flatMap(r => r.settled));
  const seen = new Map<string, LastSeen>();
  const keep = (entry: WaitingEntry, at: number | null) => {
    if (now.has(entry.item) || settled.has(entry.item)) return;
    const had = seen.get(entry.item);
    if (!had || (at ?? -Infinity) > (had.at ?? -Infinity)) seen.set(entry.item, { entry, at });
  };
  for (const [key, kept] of Object.entries(next)) {
    const current = readings.find(r => r.key === key);
    if (current?.state === "whole") continue;
    if (current?.state === "failed") for (const entry of current.entries) keep(entry, current.retainedAt);
    for (const entry of kept.lastWhole?.entries ?? []) keep(entry, kept.lastWhole!.at);
  }
  const lastSeen = [...seen.values()];
  const notes: string[] = [];
  let reopenedUnread = 0;
  for (const reading of readings) {
    if (reading.state === "whole" || !reading.note) continue;
    if (reading.note === REOPENED_RUN_NOT_READ) { reopenedUnread++; continue; }
    if (!notes.includes(reading.note)) notes.push(reading.note);
  }
  // A run reopened after the App restarted is read from the project records, which the host gives without its
  // checkpoints: whether one of its arrivals waits for the person's act is not shown anywhere in the App yet.
  if (reopenedUnread > 0) notes.push(`${reopenedUnread} run${reopenedUnread === 1 ? "" : "s"} reopened after the App restarted ${reopenedUnread === 1 ? "is" : "are"} not known to have ended: the App does not show their checkpoints, so whether one waits for your act is not shown here or anywhere else in the App yet.`);
  const complete = readings.every(r => r.state === "whole") && lastSeen.length === 0;
  return { memory: next, view: { readings, observed, lastSeen, complete, notes } };
}

/** The view of a set of readings with nothing remembered from earlier: what one render shows on its own. */
export const waitingView = (readings: SourceReading[]): WaitingView => foldWaiting({}, readings).view;

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
/** The one line. With every source read whole, the definite count of what is waiting and how many of
 * those are requests from Codex. Otherwise only what is observed now, and that the status is incomplete:
 * entries last seen earlier are never counted. */
export function waitingLine(observed: WaitingEntry[], complete: boolean): string {
  const requests = waitingRequestCount(observed);
  const part = requests > 0 ? ` (${requests} request${requests === 1 ? "" : "s"} from Codex)` : "";
  return complete ? `Waiting on you: ${waitingTotal(observed)}${part}` : `Waiting on you: ${waitingTotal(observed)} observed now${part}; status incomplete`;
}

const pad = (n: number) => String(n).padStart(2, "0");
/** "as of ‹time›" in local hours, minutes and seconds. */
export const asOfWords = (at: number) => { const d = new Date(at); return `as of ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; };

/** A conversation's identity in the App's words: as written when it is a plain identifier, else boxed as Codex's text. */
function Id({ value }: { value: string }) {
  return plainId(value) !== null ? <code>{value}</code> : <AgentText value={value} source="codex" label="Conversation:" name="Conversation identity as Codex reported it, not the App's words" />;
}

function GroupLabel({ group }: { group: WaitingGroup }) {
  const label = group.label;
  if (label.kind === "none") return <>No conversation or assignment recorded</>;
  if (label.kind === "assignment") return <>Assignment: undertaking <AgentText value={label.undertaking} label="Undertaking:" name="Undertaking as recorded, not the App's words" />, item <AgentText value={label.item} label="Item:" name="Work item as recorded, not the App's words" /></>;
  const where = label.otherHome ? ` in the ${label.home ?? "unreported"} home` : "";
  return label.threadId ? <>Conversation <Id value={label.threadId} />{where}</> : <>No conversation named{where}</>;
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
    case "conversation": return concerns.threadId ? <>the conversation <Id value={concerns.threadId} /></> : <>no conversation named</>;
    case "run": return <>the run <code>{concerns.run}</code>{concerns.conversation ? <> in the conversation <Id value={concerns.conversation} /></> : null}</>;
    case "assignment": return <>undertaking <AgentText value={concerns.undertaking} label="Undertaking:" name="Undertaking as recorded, not the App's words" />, item <AgentText value={concerns.item} label="Item:" name="Work item as recorded, not the App's words" /></>;
    case "decision-package": return <>the decision package <AgentText value={concerns.package} label="Package:" name="Decision package name as recorded, not the App's words" /></>;
  }
}

function Responder({ responder }: { responder: WaitingEntry["responder"] }) {
  if (typeof responder === "string") return <>Who must respond: {responder}</>;
  return responder.who === null ? <>Who must respond: not established</>
    : <>Who must respond: <AgentText value={responder.who} label="Examiner:" name="Who prepared the brief, as recorded, not the App's words" />, who prepared the brief, as recorded</>;
}

/** "at ‹time›" in local hours, minutes and seconds. */
const clockWords = (at: number) => { const d = new Date(at); return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; };

/** One entry: what waits, who asks, who must respond, what it concerns, who integrates, and the way to its
 * control. An entry last seen in an earlier reading says when, that its current state is unknown, and its
 * link does not say it is still open. */
export function WaitingEntryRow({ entry, go, lastSeen }: { entry: WaitingEntry; go: (entry: WaitingEntry) => void; lastSeen?: { at: number | null } }) {
  const href = entry.target.kind === "request" ? entry.target.anchor ? `#${entry.target.anchor}` : "#other-requests" : `#${entry.target.anchor}`;
  const open = (event: MouseEvent<HTMLAnchorElement>) => { event.preventDefault?.(); event.stopPropagation?.(); go(entry); };
  const parts: ReactNode[] = [
    <strong key="what">{WAITING_WORDS[entry.kind]}{entry.count > 1 ? ` (${entry.count})` : ""}</strong>,
    <span key="asks"><Asker asker={entry.asker} /></span>,
    <span key="responds"><Responder responder={entry.responder} /></span>,
    <span key="concerns">Concerns: <Concerns concerns={entry.concerns} /></span>,
    <span key="integrates">Who integrates the result: {entry.integrator}</span>,
  ];
  if (lastSeen) parts.push(<small key="last-seen">{lastSeen.at === null ? "Last seen waiting earlier" : `Last seen waiting at ${clockWords(lastSeen.at)}`}; current state unknown.</small>);
  else if (entry.asOf !== null) parts.push(<small key="as-of">{asOfWords(entry.asOf)}</small>);
  return <div className="waiting-on-you-entry" data-waiting-key={entry.key} data-waiting-source={entry.source} data-waiting-last-seen={lastSeen ? "true" : undefined}>
    {parts.flatMap((part, i) => i === 0 ? [part] : [<span key={`sep${i}`} aria-hidden="true"> · </span>, part])}
    {" "}<a href={href} onClick={open}>{lastSeen ? "Go to it (it may already be settled)" : "Go to it"}</a>
  </div>;
}

/** The place: one line, "Waiting on you: N", that opens to the list. It folds each set of readings into
 * what it remembers, so an entry an earlier reading showed stays, as last seen, while its source is not read whole. */
export function WaitingOnYou({ readings, overview, view, busy = false, openGroup, go, onOpen }: {
  readings: SourceReading[]; overview: Json; view?: Json; busy?: boolean; openGroup: (group: WaitingRequestGroup) => void; go: (entry: WaitingEntry) => void;
  /** Called each time the person opens the list: the App reads the return-review queue then. */
  onOpen?: () => void;
}) {
  const memory = useRef<WaitingMemory>({});
  const folded = foldWaiting(memory.current, readings);
  memory.current = folded.memory;
  const { observed, lastSeen, complete, notes } = folded.view;
  return <section className="waiting-on-you" aria-label="Waiting on you">
    <details id="waiting-on-you" onToggle={event => { if ((event.currentTarget as HTMLDetailsElement).open) onOpen?.(); }}>
      <summary><span role="status" aria-live="polite">{waitingLine(observed, complete)}</span></summary>
      <div className="waiting-on-you-list">
        {complete ? observed.length === 0 && <p>Nothing recorded is waiting on you.</p>
          : <p>{observed.length === 0 ? "Nothing is observed waiting on you now, but the status is incomplete:" : "The status is incomplete:"}</p>}
        {notes.length > 0 && <ul aria-label="What this list could not read whole">{notes.map((note, i) => <li key={i}>{note}</li>)}</ul>}
        {waitingGroups(observed).map(({ group, entries }) => <div key={group.key} className="waiting-on-you-group" role="group" aria-label="Entries of one conversation or assignment">
          <p className="waiting-on-you-group-label"><GroupLabel group={group} /></p>
          {entries.map(entry => <WaitingEntryRow key={entry.key} entry={entry} go={go} />)}
        </div>)}
        {lastSeen.length > 0 && <div className="waiting-on-you-last-seen" role="group" aria-label="Last seen earlier, not counted">
          <p>Last seen waiting in an earlier reading, and not counted above: each may already be settled.</p>
          {lastSeen.map(({ entry, at }) => <WaitingEntryRow key={entry.key} entry={entry} go={go} lastSeen={{ at }} />)}
        </div>}
        <WaitingRequestsIndicator overview={overview} view={view} busy={busy} open={openGroup} />
        <p><small>An entry observed now leaves when its source records the answer. An entry last seen earlier stays until its source is read whole again or records an answer for it. Returns and decisions are read again every 15 seconds, and returns each time you open this list. Nothing here answers, dismisses or settles anything; Go to it opens the existing control or record. A question or tool permission already answered is refused there. A decision package and a checkpoint act are checked there against the current content of what they concern, but an earlier decision or act does not stop another being recorded. Returns have no review control in the App yet: Go to it shows the return's record. A return whose examiner is an agent is not a demand on you, but the records do not yet say whether the examiner is a person or an agent, so every return waiting for review is listed.</small></p>
      </div>
    </details>
  </section>;
}
