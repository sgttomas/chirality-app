import { type MouseEvent, type ReactNode } from "react";
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
// read, or a failed read. A reading is whole only where its reader positively
// says so; each adapter names the host field that says it. Only when every
// reading is whole does the line give a definite count or the list say that
// nothing is waiting. Otherwise the line counts only what is observed now and
// says the status is incomplete, and each source not read whole is named with
// its reason and the time of its read.
//
// The list is a projection of its sources' latest readings and keeps no
// memory of entries: each reading replaces the one before. The one thing
// retained is the source's own: when a source's latest read failed, its last
// successful reading (the snapshot, packet or view the App already holds for
// it, bound to its home, generation, time and limits) is shown as one block,
// as last read at its time, not counted, its current state unknown.
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
 * listed. A register whose generation is not a generation (sameActivityGeneration)
 * gives nothing. */
function requestEntries(host: Json): WaitingEntry[] {
  if (host?.state !== "ready" || !sameActivityGeneration(host?.generation, host?.generation)) return [];
  const home = text(host?.homeRouting?.activeModeHomeClass) || null;
  const requests = hostRequests(host).filter((r: Json) => sameActivityGeneration(r?.generation, host.generation));
  return requests.filter((r: Json) => answerable(r) && r?.closedGeneration !== true).map((r: Json) => {
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

/** Requests in one home other than the active one: the host's overview gives only
 * a count per conversation there, so each such group is one entry with its count. */
function otherHomeEntries(host: Json, home: string): WaitingEntry[] {
  return list(host?.waitingRequests?.groups).filter((g: Json) => text(g?.modeHomeClass) === home && Number.isInteger(g?.count) && g.count > 0).map((g: Json) => {
    const threadId = typeof g.threadId === "string" && g.threadId ? g.threadId : null;
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

/** A run's checkpoint arrivals from its lifecycle records whose latest recorded disposition is "waiting"
 * in a run that has not ended (after a run ends an act no longer changes an arrival). Used for a hot run,
 * and for a reopened run once the host gives its lifecycle records. */
function arrivalsOf(run: Json, reference: string): WaitingEntry[] {
  const entries: WaitingEntry[] = [];
  const records = list(run?.lifecycle?.records);
  const ended = !!run?.lifecycle?.end || records.some((r: Json) => r?.kind === "run_ended");
  if (ended) return entries;
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
      key: JSON.stringify(["checkpoint-arrival", reference, arrival.recordId ?? [b.checkpoint, b.arrivalOrdinal], latest.recordId ?? changes.length]),
      source: "checkpoint-arrival", kind: "checkpoint-reached", count: 1,
      asker: { kind: "checkpoint", checkpoint: b.checkpoint, requester: request ? text(request.body?.requester?.kind) || null : null },
      responder: ACTOR[text(actor)] ?? "you",
      concerns: { kind: "run", run: reference, conversation }, integrator: "not recorded",
      group: { key: JSON.stringify(["conversation", home, conversation]), label: { kind: "conversation", threadId: conversation, home, otherHome: false } },
      asOf: null, target: { kind: "run", anchor: runEvidenceAnchor(reference) },
    });
  }
  return entries;
}

const NO_REQUESTER = "requester identity not established";
const NO_EXAMINER = "examiner not established";
const AWAITING_REVIEW = "awaiting review";

/** Returns awaiting review in the fleet packet's return-review queues. */
function returnEntries(fleet: Json, readAt: number | null): WaitingEntry[] {
  const entries: WaitingEntry[] = [];
  for (const view of list(fleet?.workspace?.undertakings)) {
    for (const row of list(view?.queue)) {
      if (typeof row?.returnRef !== "string" || row?.state !== AWAITING_REVIEW) continue;
      const undertaking = text(view.undertaking), item = text(row.item);
      entries.push({
        key: JSON.stringify(["return-review", undertaking, row.returnRef, row.state]),
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
  return entries;
}

const PENDING = (state: Json) => text(state).startsWith("pending");
const DECIDED = "decided";

/** Decision packages pending the person's decision. */
function decisionEntries(decisions: Json, readAt: number | null): WaitingEntry[] {
  return list(decisions?.rows).filter((row: Json) => typeof row?.package === "string" && PENDING(row.state)).map((row: Json) => ({
    key: JSON.stringify(["decision-package", row.package, row.requestSources ?? null, row.state]),
    source: "decision-package", kind: "decision", count: 1,
    asker: { kind: "requested-by", who: typeof row.requestedBy === "string" && row.requestedBy && row.requestedBy !== NO_REQUESTER ? row.requestedBy : null }, responder: "you",
    concerns: { kind: "decision-package", package: row.package }, integrator: "not recorded",
    group: { key: "none", label: { kind: "none" } }, asOf: readAt, target: { kind: "decision", anchor: decisionPackageAnchor(row.package) },
  } satisfies WaitingEntry));
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

/** A source's last successful reading, kept by the source itself (the status snapshot, fleet packet or
 * decision view the App holds), shown only when the source's latest read failed: one block, as it was,
 * not counted. It is bound to the home, generation, time and limits of the read that gave it. */
export type LastRead = {
  state: "whole" | "limited";
  /** When the read that gave it was started (ms since the epoch). */
  at: number | null;
  entries: WaitingEntry[];
  limits: string[];
  /** The home it was read in, where the source belongs to one. */
  home: string | null;
  /** The Codex generation it was read from, where that applies. */
  generation: Json;
  /** For the active home's requests: the waiting overview of that same read. */
  overview: Json;
};

export type SourceReading = {
  /** The source's identity: "requests:‹home›" (or "requests" before any home is known), "other-homes", "home:‹class›",
   * "hot-runs", "run:‹reference›", "reopened", "reopened-run:‹run›", "returns" or "decisions". */
  key: string;
  /** The source in the App's words. */
  name: string;
  state: ReadingState;
  /** When the read that gave this state was started (for a failed reading, the failed read), or null where none has been. */
  at: number | null;
  /** The entries observed in this reading; none unless it is whole or limited. */
  entries: WaitingEntry[];
  /** For a limited reading, what its reader said it could not read. */
  limits: string[];
  /** The App's sentence for a reading that is not whole. */
  note: string | null;
  /** For a failed reading: the source's last successful reading, or null where there is none. */
  lastRead: LastRead | null;
  /** For the active home's requests read whole: the waiting overview of the same read. */
  overview: Json;
};

type Scope = { home: string | null; generation: Json };
type Found = { evidence: Omit<ReadEvidence, "call">; entries: WaitingEntry[]; overview?: Json };
const nothing = (): Found => ({ evidence: { read: false, affirmedWhole: false, limits: [] }, entries: [] });

function finish(key: string, name: string, scope: Scope, call: ReadEvidence["call"], found: Found, notes: { limited: string; notRead: string; failed: string }, at: number | null, retainedAt: number | null): SourceReading {
  const state = decideReading({ call, ...found.evidence });
  // What the read the App still holds was, before the later read failed: only a whole or limited one is shown.
  const held = state === "failed" ? decideReading({ call: "answered", ...found.evidence }) : null;
  const lastRead: LastRead | null = held === "whole" || held === "limited"
    ? { state: held, at: retainedAt, entries: found.entries, limits: found.evidence.limits, home: scope.home, generation: scope.generation, overview: found.overview ?? null } : null;
  const observed = state === "whole" || state === "limited";
  return {
    key, name, state, at,
    entries: observed ? found.entries : [],
    limits: state === "limited" ? found.evidence.limits : [],
    note: state === "whole" ? null : state === "limited" ? notes.limited : state === "failed" ? notes.failed : notes.notRead,
    lastRead, overview: observed ? found.overview ?? null : null,
  };
}

const REOPENED_RUN_NOT_READ = "reopened-run-not-read";
const RUN_STATE_ENDED = "ended";
const RUN_STATE_NOT_STARTED = "start not confirmed in record";
const statusFailed = (name: string) => `${name} could not be read at the last attempt: the App's last read of its own status failed.`;

/** The readings carried by one host status read: requests in the active home, the hot runs and each of
 * them, the overview of other homes and each of them, and the census of runs reopened after a restart
 * and each of those. */
function hostReadings(host: Json, call: ReadEvidence["call"], at: number | null, retainedAt: number | null): SourceReading[] {
  const out: SourceReading[] = [];
  const active = text(host?.homeRouting?.activeModeHomeClass);
  const hostScope: Scope = { home: active || null, generation: host?.generation ?? null };
  const push = (key: string, name: string, found: Found, limited: string, notRead: string, scope: Scope = hostScope) =>
    out.push(finish(key, name, scope, call, found, { limited, notRead, failed: statusFailed(name) }, at, retainedAt));
  // Requests in the active home. The host gives the home's whole request register (serverRequests, the
  // register snapshot of native_requests.rs) whenever its Codex is ready with a generation: `state: "ready"`
  // with a generation of the generation's shape (sameActivityGeneration) and a `serverRequests` array is the
  // positive word. Any other state is not read. The source is the register of that home: its identity names it.
  const running = host?.state === "ready" && sameActivityGeneration(host?.generation, host?.generation) && Array.isArray(host?.serverRequests);
  const requestsName = active ? `Requests from Codex in the ${active} home` : "Requests from Codex in the active home";
  push(active ? `requests:${active}` : "requests", requestsName,
    { evidence: { read: running, affirmedWhole: running, limits: [] }, entries: requestEntries(host), overview: host?.waitingRequests ?? null },
    "", !host ? `${requestsName} have not been read yet.` : host?.state === "ready" ? `${requestsName} are not read: the App's status gave no register with a generation it can use.` : `${requestsName} are not read while Codex is not running.`);
  // Hot runs. The workflow root's `runs` is the host's table of every run in this process
  // (runtime_session.rs `snapshot`): an array there is the positive word that the table was read.
  const root = host?.workflowRoot;
  const runs = Array.isArray(root?.runs) ? root.runs : null;
  push("hot-runs", "Workflow runs", { evidence: { read: !!runs, affirmedWhole: !!runs, limits: [] }, entries: [] }, "", "Workflow runs have not been read yet.");
  for (const run of runs ?? []) {
    const reference = text(run?.reference);
    // A run's own records are whole when the host gives its `lifecycle.records` array (lifecycle_view: every
    // entry the run holds in this process). A run whose lock is busy comes as the placeholder
    // {reference, state: "original run operation pending"} with no lifecycle: that is not read.
    const records = Array.isArray(run?.lifecycle?.records);
    push(`run:${reference}`, `The run ${reference}`, records ? { evidence: { read: true, affirmedWhole: true, limits: [] }, entries: arrivalsOf(run, reference) } : nothing(),
      "", `The run ${reference} could not be read just now (an operation on it was in progress), so whether one of its checkpoints waits for your act is not known.`,
      { home: text(run?.home) || null, generation: run?.generation ?? null });
  }
  // Other homes. waiting_requests.rs `overview` lists every configured home in `sources`, each with the
  // `state` of its register: the overview is read when `sources` is an array naming the active home, and
  // a home's count is whole only where its source says `state: "ready"`.
  const sources = Array.isArray(host?.waitingRequests?.sources) ? host.waitingRequests.sources : null;
  const overview = !!sources && sources.some((s: Json) => text(s?.modeHomeClass) === active);
  push("other-homes", "Requests in other homes", { evidence: { read: overview, affirmedWhole: overview, limits: [] }, entries: [] }, "", "Requests in other homes have not been read.");
  for (const source of overview ? sources! : []) {
    const home = text(source?.modeHomeClass);
    if (home === active) continue;
    const ready = source?.state === "ready";
    push(`home:${home}`, `Requests in the ${home || "unreported"} home`, { evidence: { read: ready, affirmedWhole: ready, limits: [] }, entries: otherHomeEntries(host, home) },
      "", `Requests in the ${home || "unreported"} home are not read (${text(source?.state) || "state not reported"}).`, { home: home || null, generation: null });
  }
  // Runs reopened after the App restarted (record_supply.rs `RunsReading::view`, with the
  // `historyNotices` read_reopened_history attaches). The census is read when `reopened` holds a `runs`
  // array; it is whole only when its `limits` and `historyNotices` are both present and empty. Until the
  // person reopens recorded runs the host gives `reopened: null`: not read.
  const reopened = root?.reopened;
  const census = !!reopened && typeof reopened === "object" && Array.isArray(reopened.runs);
  const censusWhole = census && Array.isArray(reopened.limits) && Array.isArray(reopened.historyNotices);
  push("reopened", "Runs recorded before the App restarted", { evidence: { read: census, affirmedWhole: censusWhole, limits: census ? [...list(reopened.limits), ...list(reopened.historyNotices)].map(text) : [] }, entries: [] },
    "Runs recorded before the App restarted were read with limits: some may not be shown, and whether one of their checkpoints waits for your act is not known.",
    "Runs recorded before the App restarted have not been read, so whether one of their checkpoints waits for your act is not known. Reopen recorded workflow runs reads them.");
  for (const row of census ? reopened.runs : []) {
    const reference = text(row?.reference ?? row?.run);
    if ((runs ?? []).some((live: Json) => live?.reference === reference)) continue;   // a hot run's own reading covers it
    let found: Found;
    if (Array.isArray(row?.lifecycle?.records)) {
      // The shape the coming host read gives a reopened run: reference, lifecycle {state, end, records}
      // and limits. Its records are whole when `limits` is present and empty.
      found = { evidence: { read: true, affirmedWhole: Array.isArray(row?.limits), limits: list(row?.limits).map(text) }, entries: arrivalsOf(row, reference) };
    } else if (row?.state === RUN_STATE_ENDED || row?.state === RUN_STATE_NOT_STARTED) {
      // An end recorded in the run's records, or a complete record set with no run_opened
      // (RecordedLifecycle::StartNotConfirmed is given only for a complete set): nothing of it can wait.
      found = { evidence: { read: true, affirmedWhole: true, limits: [] }, entries: [] };
    } else {
      // Still open, or a lifecycle the records do not establish ("unknown"), or a state the App does not
      // know: its checkpoints are not read.
      found = nothing();
    }
    push(`reopened-run:${reference}`, `The run ${reference}, reopened after the App restarted`, found,
      "A run reopened after the App restarted was read with limits, so more of its checkpoints may be waiting.", REOPENED_RUN_NOT_READ);
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
  const found: Found = read ? { evidence: { read, affirmedWhole, limits: list(packet.limits).map((l: Json) => text(l?.reason ?? l)) }, entries: returnEntries(packet, retainedAt ?? at) } : nothing();
  return finish("returns", "Returns", { home: null, generation: null }, call, found,
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
  const found: Found = read ? { evidence: { read, affirmedWhole, limits: [...list(view.limits).map(text), ...list(view.historyNotices).map(text), ...list(view.unresolvedRecords).map(() => "unresolved record"), ...unsettled] }, entries: decisionEntries(view, retainedAt ?? at) } : nothing();
  return finish("decisions", "Decisions", { home: null, generation: null }, call, found,
    { limited: "Decisions were read with limits, so more may be waiting.", notRead: "Decisions have not been read yet.", failed: "Decisions could not be read at the last attempt." }, at, retainedAt);
}

export type WaitingSources = {
  /** The status snapshot shown (the last read that succeeded), the start time of the read that gave it, and whether a later status read failed (and when it started). */
  host: Json; hostReadAt?: number | null; hostFailure?: string | null; hostFailedAt?: number | null;
  /** The last good fleet packet, when its read started, and whether a later read failed. */
  fleet?: Json; fleetReadAt?: number | null; fleetFailure?: string | null; fleetFailedAt?: number | null;
  /** The last good decision view, when its read started, and whether a later read failed. */
  decisions?: Json; decisionsReadAt?: number | null; decisionsFailure?: string | null; decisionsFailedAt?: number | null;
};

const callOf = (value: Json, failure: string | null): ReadEvidence["call"] => failure ? "rejected" : value ? "answered" : "not-made";

/** Every source's reading. A pure function of what the App holds now: nothing from an earlier render is kept. */
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

// ---- What the list shows: the readings now, and nothing else ----

/** One row naming a source not read whole: its reading (null for the aggregated note on reopened runs) and the App's sentence. */
export type CoverageRow = { reading: SourceReading | null; note: string };
export type WaitingView = {
  readings: SourceReading[];
  /** Entries observed now, in a reading that answered: only these are counted. */
  observed: WaitingEntry[];
  /** Every source read whole: the only state in which the count is definite and "nothing is waiting" may be said. */
  complete: boolean;
  /** Each source not read whole, in source order. */
  coverage: CoverageRow[];
  /** The App's sentences of those rows. */
  notes: string[];
  /** The failed readings whose source keeps a last successful reading with something in it, each shown as one block. */
  lastReads: SourceReading[];
};

/** What one set of readings shows. Nothing is carried from an earlier set. */
export function waitingView(readings: SourceReading[]): WaitingView {
  const observed = readings.filter(r => r.state === "whole" || r.state === "limited").flatMap(r => r.entries);
  const coverage: CoverageRow[] = [];
  let reopenedUnread = 0;
  for (const reading of readings) {
    if (reading.state === "whole" || !reading.note) continue;
    if (reading.note === REOPENED_RUN_NOT_READ) { reopenedUnread++; continue; }
    coverage.push({ reading, note: reading.note });
  }
  // A run reopened after the App restarted is read from the project records, which the host gives without its
  // checkpoints: whether one of its arrivals waits for the person's act is not shown anywhere in the App yet.
  if (reopenedUnread > 0) coverage.push({ reading: null, note: `${reopenedUnread} run${reopenedUnread === 1 ? "" : "s"} reopened after the App restarted ${reopenedUnread === 1 ? "is" : "are"} not known to have ended: the App does not show their checkpoints, so whether one waits for your act is not shown here or anywhere else in the App yet.` });
  const complete = readings.every(r => r.state === "whole");
  return { readings, observed, complete, coverage, notes: coverage.map(row => row.note), lastReads: readings.filter(r => r.state === "failed" && r.lastRead && r.lastRead.entries.length > 0) };
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
/** The one line. With every source read whole, the definite count of what is waiting and how many of
 * those are requests from Codex. Otherwise only what is observed now, and that the status is incomplete:
 * a failed source's last successful reading is never counted. */
export function waitingLine(observed: WaitingEntry[], complete: boolean): string {
  const requests = waitingRequestCount(observed);
  const part = requests > 0 ? ` (${requests} request${requests === 1 ? "" : "s"} from Codex)` : "";
  return complete ? `Waiting on you: ${waitingTotal(observed)}${part}` : `Waiting on you: ${waitingTotal(observed)} observed now${part}; status incomplete`;
}

const pad = (n: number) => String(n).padStart(2, "0");
/** "‹time›" in local hours, minutes and seconds. */
export const clockWords = (at: number) => { const d = new Date(at); return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; };
/** "as of ‹time›" in local hours, minutes and seconds. */
export const asOfWords = (at: number) => `as of ${clockWords(at)}`;

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

/** What acting from an entry in a last-read block meets at its source today: whether the source checks
 * the record is still waiting before it accepts an answer (an entry there may be out of date). */
export const LAST_READ_OFFER: Record<WaitingEntry["source"], string> = {
  "supplier-request": "Its request card takes an answer only while the request is still outstanding.",
  "waiting-overview": "Opening checks that home again and shows its request cards as they are now.",
  "checkpoint-arrival": "It may already be settled: the checkpoint act there does not yet refuse an arrival that is no longer waiting.",
  "decision-package": "It may already be decided: the decision there does not yet refuse a package that is no longer pending.",
  "return-review": "Returns have no review control in the App yet: it shows the return's record.",
};

/** One entry: what waits, who asks, who must respond, what it concerns, who integrates, and the way to its
 * control. An entry of a failed source's last successful reading says when it was read, that its current
 * state is unknown, and what its source checks before taking an answer; its link never says it is still open. */
export function WaitingEntryRow({ entry, go, lastRead }: { entry: WaitingEntry; go: (entry: WaitingEntry) => void; lastRead?: { at: number | null } }) {
  const href = entry.target.kind === "request" ? entry.target.anchor ? `#${entry.target.anchor}` : "#other-requests" : `#${entry.target.anchor}`;
  const open = (event: MouseEvent<HTMLAnchorElement>) => { event.preventDefault?.(); event.stopPropagation?.(); go(entry); };
  const parts: ReactNode[] = [
    <strong key="what">{lastRead ? `as last read: ${WAITING_WORDS[entry.kind]}` : WAITING_WORDS[entry.kind]}{entry.count > 1 ? ` (${entry.count})` : ""}</strong>,
    <span key="asks"><Asker asker={entry.asker} /></span>,
    <span key="responds"><Responder responder={entry.responder} /></span>,
    <span key="concerns">Concerns: <Concerns concerns={entry.concerns} /></span>,
    <span key="integrates">Who integrates the result: {entry.integrator}</span>,
  ];
  if (lastRead) parts.push(<small key="last-read">{lastRead.at === null ? "As last read" : `As last read at ${clockWords(lastRead.at)}`}; current state unknown. {LAST_READ_OFFER[entry.source]}</small>);
  else if (entry.asOf !== null) parts.push(<small key="as-of">{asOfWords(entry.asOf)}</small>);
  return <div className="waiting-on-you-entry" data-waiting-key={entry.key} data-waiting-source={entry.source} data-waiting-last-read={lastRead ? "true" : undefined}>
    {parts.flatMap((part, i) => i === 0 ? [part] : [<span key={`sep${i}`} aria-hidden="true"> · </span>, part])}
    {" "}<a href={href} onClick={open}>Go to it</a>
  </div>;
}

/** What a reader said it could not read, boxed: the words come from records, not from the App. */
function Limits({ limits }: { limits: string[] }) {
  if (limits.length === 0) return null;
  return <>{" "}What its reader said it could not read: {limits.map((limit, i) => <span key={i}>{i > 0 ? "; " : ""}<AgentText value={limit} source="file" label="Limit:" name="What the reader could not read, as it reported it, not the App's words" /></span>)}.</>;
}

/** The time of a source's read, and what its state means for what the list shows of it. */
function ReadTime({ reading }: { reading: SourceReading }) {
  const when = reading.at === null ? null : clockWords(reading.at);
  if (reading.state === "limited") return <>Read {when ? `at ${when}` : "earlier"} with limits: this reading may omit waiting items; what it shows is counted as observed now.<Limits limits={reading.limits} /></>;
  if (reading.state === "not-read") return <>{when ? `Checked at ${when}.` : "No read of it has been made yet."}</>;
  const last = reading.lastRead;
  const lastWhen = last?.at === null || last?.at === undefined ? "earlier" : `at ${clockWords(last.at)}`;
  return <>The read {when ? `started at ${when} ` : ""}failed. {!last ? "There is no earlier successful reading of it to show."
    : last.entries.length > 0 ? `Its last successful reading, ${lastWhen}, is shown below as it was then, not counted; its current state is unknown.`
    : `Its last successful reading, ${lastWhen}, showed nothing waiting; its current state is unknown.`}
    {last && last.limits.length > 0 && <> That reading had limits and may have omitted waiting items.<Limits limits={last.limits} /></>}
    {last && last.state === "limited" && last.limits.length === 0 && <> That reading was not whole and may have omitted waiting items.</>}</>;
}

/** The nested overview of requests from Codex by home, governed by the reading of the active home's
 * requests: drawn as now from a whole reading; from a failed read, the last successful reading's
 * overview, presented throughout as last read; otherwise withheld, with the reason. */
function RequestsOverview({ reading, view, busy, open }: { reading: SourceReading | undefined; view: Json; busy: boolean; open: (group: WaitingRequestGroup) => void }) {
  if (reading && (reading.state === "whole" || reading.state === "limited")) return <WaitingRequestsIndicator overview={reading.overview} view={view} busy={busy} open={open} />;
  if (reading?.state === "failed" && reading.lastRead) return <WaitingRequestsIndicator overview={reading.lastRead.overview} view={view} busy={busy} open={open}
    lastRead={reading.lastRead.at === null ? "an earlier read" : clockWords(reading.lastRead.at)} />;
  return <p className="waiting-requests-withheld">The overview of requests from Codex by home is not shown: {reading?.note ? reading.note.charAt(0).toLowerCase() + reading.note.slice(1) : "requests from Codex have not been read."}</p>;
}

/** The place: one line, "Waiting on you: N", that opens to the list. It shows the readings it is given and
 * keeps nothing from an earlier render. */
export function WaitingOnYou({ readings, view, busy = false, openGroup, go, onOpen }: {
  readings: SourceReading[]; view?: Json; busy?: boolean; openGroup: (group: WaitingRequestGroup) => void; go: (entry: WaitingEntry) => void;
  /** Called each time the person opens the list: the App reads the return-review queue then. */
  onOpen?: () => void;
}) {
  const { observed, complete, coverage, lastReads } = waitingView(readings);
  return <section className="waiting-on-you" aria-label="Waiting on you">
    <details id="waiting-on-you" onToggle={event => { if ((event.currentTarget as HTMLDetailsElement).open) onOpen?.(); }}>
      <summary><span role="status" aria-live="polite">{waitingLine(observed, complete)}</span></summary>
      <div className="waiting-on-you-list">
        {complete ? observed.length === 0 && <p>Nothing recorded is waiting on you.</p>
          : <p>{observed.length === 0 ? "Nothing is observed waiting on you now, but the status is incomplete:" : "The status is incomplete:"}</p>}
        {coverage.length > 0 && <div className="waiting-on-you-coverage" role="group" aria-label="What this list could not read whole">
          {coverage.map(({ reading, note }, i) => <p key={reading?.key ?? `note${i}`} data-waiting-source-key={reading?.key} data-waiting-state={reading?.state}>{note}{reading && <> <small><ReadTime reading={reading} /></small></>}</p>)}
        </div>}
        {waitingGroups(observed).map(({ group, entries }) => <div key={group.key} className="waiting-on-you-group" role="group" aria-label="Entries of one conversation or assignment">
          <p className="waiting-on-you-group-label"><GroupLabel group={group} /></p>
          {entries.map(entry => <WaitingEntryRow key={entry.key} entry={entry} go={go} />)}
        </div>)}
        {lastReads.map(reading => <div key={reading.key} className="waiting-on-you-last-read" role="group" aria-label="As last read, not counted" data-waiting-source-key={reading.key}>
          <p>{reading.name}, as last read{reading.lastRead!.at === null ? "" : ` at ${clockWords(reading.lastRead!.at)}`}; its current state is unknown, and nothing here is counted above.{reading.lastRead!.state === "limited" && " That reading had limits and may have omitted waiting items."}</p>
          {reading.lastRead!.entries.map(entry => <WaitingEntryRow key={entry.key} entry={entry} go={go} lastRead={{ at: reading.lastRead!.at }} />)}
        </div>)}
        <RequestsOverview reading={readings.find(r => r.key === "requests" || r.key.startsWith("requests:"))} view={view} busy={busy} open={openGroup} />
        <p><small>Each source shows what its latest reading observed, and the next reading replaces it: nothing is kept from one reading to the next, so an item a limited reading showed can drop from view when the next reading does not hold it, and after a change of home the requests of the home left are shown only as that home's overview reads them. When a source's latest read failed, its last successful reading is shown apart, as last read at its time, not counted, its current state unknown. Each item also has its own place in the App, which reads its source itself: a request from Codex on its request card, beside its conversation or under the requests outside the selected conversation (in another home, once that home is opened); a checkpoint arrival of a run in this session in that run's panel in the workflow studio; a return in the fleet records panel; a decision package in the decision packages view. A run reopened after the App restarted does not show its checkpoints anywhere in the App yet. Returns and decisions are read again every 15 seconds, and returns each time you open this list. Nothing here answers, dismisses or settles anything; Go to it opens the existing control or record. A question or tool permission already answered is refused there. A decision package and a checkpoint act are checked there against the current content of what they concern, but an earlier decision or act does not stop another being recorded, and neither yet refuses an item that is no longer waiting. Returns have no review control in the App yet: Go to it shows the return's record. A return whose examiner is an agent is not a demand on you, but the records do not yet say whether the examiner is a person or an agent, so every return waiting for review is listed.</small></p>
      </div>
    </details>
  </section>;
}
