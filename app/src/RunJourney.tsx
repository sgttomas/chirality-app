import { conversationLabel, nativePathText } from "./presentation";
import { hostRequests, requestThread } from "./RequestCards";
import { errorWords } from "./NativeActivity";
import { chatWorkflow, workflowAssurance } from "./workflowSelection";
import { ProjectFolderSummary, appProjectFolder } from "./WorkflowContext";
import { IncludedWorkflows, RoleBesideWorkflow, includedEntryOf, librarySourceWords } from "./IncludedWorkflows";
import { useEffect, useRef, useState, type ReactNode } from "react";

/** What each guide command did, in the person's words. */
const ACTION_WORDS: Record<string, [string, string]> = {
  workflow_open_project_library: ["Opened this project's workflow library", "show this project's workflows"],
  workflow_library_entries_refresh: ["Looked for other workflows in this library", "look for other workflows in this library"],
  workflow_review_library_entries: ["Opened the review", "open the review"],
  workflow_select_listed: ["Chose the workflow for this conversation", "choose the workflow"],
  workflow_select_production_bundle: ["Chose the included workflow for this conversation", "choose the included workflow"],
  workflow_follow_newer_revision: ["Moved this conversation to the newer revision", "move to the newer revision"],
  workflow_prepare_run: ["Prepared the run; nothing has been sent", "prepare the run"],
  workflow_send_run: ["Start requested", "start the run"],
  workflow_end_run: ["Ending requested", "end the run"],
  workflow_observe_drafts: ["Looked for drafts in this library", "look for drafts"],
  workflow_review_draft: ["Opened the review", "open the review"],
  workflow_trial_prepare: ["Asked for the trial message. Nothing has been sent", "prepare the trial"],
  workflow_trial_bring_back: ["Asked for the trial's results as a message. Nothing has been sent", "bring the trial back"],
};
/**
 * Where a result sends the person to look, kept apart from the result itself:
 * it is said only while the guide's steps are shown. A result is also shown
 * while the steps are withheld, and must not point at what is not there.
 */
const RESULT_POINTERS: Record<string, string> = {
  workflow_send_run: "See Progress for what happened.",
  workflow_end_run: "See Progress.",
  workflow_trial_prepare: "It is listed below when it is ready to read and send.",
  workflow_trial_bring_back: "It is listed below when it is ready to read and send.",
};
/**
 * Refusals a person can meet from a guide's button, in their words. Each is
 * one exact host or App message, said only for the commands it can come from
 * before anything was done, so "nothing was done" is what was established.
 * Any other refusal is shown in the App's own words.
 */
const CHECKED_FIRST = ["workflow_open_project_library", "workflow_library_entries_refresh", "workflow_review_library_entries", "workflow_select_listed",
  "workflow_select_production_bundle", "workflow_follow_newer_revision", "workflow_prepare_run", "workflow_observe_drafts"];
const OUT_OF_DATE = "this view was out of date, so nothing was done. Press the button again.";
const REFUSAL_WORDS: { exact: string; commands: string[]; words: string }[] = [
  { exact: "Native history context is busy; refresh the workflow choice", commands: CHECKED_FIRST, words: "the App was busy reading conversation history, so nothing was done. Press the button again." },
  { exact: "Workflow App home source changed; refresh the displayed choice", commands: CHECKED_FIRST, words: OUT_OF_DATE },
  { exact: "Workflow native generation changed; refresh the displayed choice", commands: CHECKED_FIRST, words: OUT_OF_DATE },
  { exact: "Native history selection changed; refresh the displayed workflow choice", commands: CHECKED_FIRST, words: OUT_OF_DATE },
  // The App's own check before any host command is issued (workflowArguments).
  { exact: "Workflow source or chat changed; refresh the displayed choice before acting", commands: CHECKED_FIRST, words: "the conversation chosen here is no longer open in this view, so nothing was done. Choose the conversation again, then press the button again." },
];
const refusalWords = (command: string, reply: string): string | undefined => REFUSAL_WORDS.find(row => row.exact === reply && row.commands.includes(command))?.words;
/** The host's states for a prepared run it did not send, in plain words. Each state itself says nothing was sent. What to do is the host's own text. */
const NOT_SENT: Record<string, string> = {
  "WR pre-send publication failed; nothing sent": "The App couldn't finish saving the run's record.",
  "generated supporting files changed or unavailable; nothing sent": "The App couldn't verify the copy of the workflow's supporting files that this run was prepared with.",
  "selected revision source changed or unavailable; nothing sent": "The App couldn't verify the chosen workflow for this run.",
  "workflow approval changed since preparation; nothing sent": "The App couldn't apply the same workflow approval it applied when you prepared this run.",
};
export type GuideOutcome = { command: string; message: string; failed?: boolean; settled?: boolean };
/** The last guide action's result without raw host JSON; the exact reply stays under details. */
export function guideResultWords(outcome: GuideOutcome, stepsShown = true): { words: string; detail: string; failed: boolean } | null {
  // Only a settled result of a command the guides name: an unknown command's reply is never called done.
  if (!outcome?.settled || !Object.hasOwn(ACTION_WORDS, outcome.command)) return null;
  const [done, verb] = ACTION_WORDS[outcome.command];
  if (outcome.failed) {
    const reply = outcome.message.replace(/^Error: /, "");
    const plain = refusalWords(outcome.command, reply);
    if (plain) return { words: `Couldn't ${verb}: ${plain}`, detail: reply, failed: true };
    // The result points nowhere: it is also shown while the guide's steps, Progress among them, are withheld.
    return { words: `Couldn't ${verb}: ${reply}`, detail: "", failed: true };
  }
  // The included-workflow command also serves reading one with no conversation
  // (the studio's inspection): the host says which it was in `choiceChat`.
  if (outcome.command === "workflow_select_production_bundle") {
    let chat: Json;
    try { chat = JSON.parse(outcome.message)?.choiceChat; } catch { chat = undefined; }
    if (chat === null) return { words: "Opened the included workflow to read. Nothing was chosen for a conversation.", detail: outcome.message, failed: false };
    if (!chat || typeof chat !== "object") return { words: `The App accepted this.${stepsShown ? " The Workflow step shows what is chosen for the conversation." : ""}`, detail: outcome.message, failed: false };
  }
  const pointer = stepsShown ? RESULT_POINTERS[outcome.command] : undefined;
  return { words: `${done}.${pointer ? ` ${pointer}` : ""}`, detail: outcome.message, failed: false };
}
/** The last press's result, shown under a guide's Next line where the person is looking. */
export function GuideResult({ label, outcome, only, stepsShown = true }: { label: string; outcome?: GuideOutcome | null; only?: string[]; stepsShown?: boolean }) {
  // A guide that names its own commands stays silent about another view's press.
  const result = outcome && (!only || only.includes(outcome.command)) ? guideResultWords(outcome, stepsShown) : null;
  if (!result) return null;
  return <div role={result.failed ? "alert" : "status"} aria-label={label} className={`run-journey-state${result.failed ? " run-journey-failed" : ""}`}><p>{result.words}</p>
    {result.detail && <details><summary>What the App reported</summary><pre style={{ whiteSpace: "pre-wrap" }}>{result.detail}</pre></details>}</div>;
}

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
/** A run's own place in the workflow studio, so a link lands on its recorded evidence. Exact: the reference's UTF-16 code units in hex. */
const hex = (value: Json): string => Array.from(typeof value === "string" ? value : "", c => c.charCodeAt(0).toString(16).padStart(4, "0")).join("");
export const runEvidenceAnchor = (reference: Json): string => `run-evidence-${hex(reference)}`;
/** A registered revision's own row in the workflow studio (library, name and revision, each exact). */
export const registeredRevisionAnchor = (library: Json, name: Json, revision: Json): string => `registered-revision-${hex(library)}-${hex(name)}-${hex(revision)}`;
type Act = (command: string, args: Record<string, unknown>) => Promise<Json>;
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);
const starts = (value: Json, prefix: string) => typeof value === "string" && value.startsWith(prefix);
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

/** Runs of ONE home and conversation by the host's `preparationOrder` (its
 * position in that conversation's run list), highest first. Rows without it
 * stay in the host's order, unsorted, as order not known. */
export function orderRuns(runs: Json[]): { ordered: Json[]; unordered: Json[] } {
  const has = (run: Json) => Number.isInteger(run?.preparationOrder) && run.preparationOrder >= 0;
  return { ordered: runs.filter(has).sort((a, b) => b.preparationOrder - a.preparationOrder), unordered: runs.filter(run => !has(run)) };
}
/** The recorded workflow's full source identity equals the chosen one's (name, origin, source root and kind as supplied); incomplete is no match. */
const sameWorkflowFamily = (recorded: Json, chosen: Json): boolean => {
  const fields = ["name", "origin", "source_root"];
  const recordedRoot = recorded?.source_root ?? recorded?.sourceRoot, chosenRoot = chosen?.source_root ?? chosen?.sourceRoot;
  if (fields.some(key => typeof (key === "source_root" ? recordedRoot : recorded?.[key]) !== "string" || typeof (key === "source_root" ? chosenRoot : chosen?.[key]) !== "string")) return false;
  if (typeof recorded?.kind === "string" && typeof chosen?.kind === "string" && recorded.kind !== chosen.kind) return false;
  return recorded.name === chosen.name && recorded.origin === chosen.origin && recordedRoot === chosenRoot;
};
/** One reading of a run, from the host's own lifecycle/status fields. */
export type RunReading = { tone: "idle" | "working" | "waiting" | "failed" | "uncertain" | "ended" | "done"; title: string; detail: string };
/** Only Codex's definite refusal establishes that the start did not happen. */
export const startRefused = (run: Json) => starts(run?.status?.state, "native workflow-text turn/start refused by Codex");
export function runReading(run: Json, host: Json): RunReading {
  const lifecycle = text(run?.lifecycle?.state);
  const status = run?.status ?? {};
  if (starts(lifecycle, "ended")) {
    const cause = text(run.lifecycle?.end?.cause);
    if (cause === "completed") return { tone: "done", title: "Ended as completed", detail: "The agent reported the workflow finished and you ended the run on that report. The App records that report; it has not checked the work." };
    if (cause === "ended by the person") return { tone: "ended", title: "Ended by you", detail: "You ended the run without a finished report from the agent. This does not say the work is complete." };
    if (starts(cause, "ended to start ")) return { tone: "ended", title: "Ended to start another workflow", detail: `The run ended so that ${cause.slice("ended to start ".length)} could start. This does not say the work is complete.` };
    return { tone: "ended", title: "Ended", detail: `The run ended (recorded cause: ${cause || "not reported"}). This does not say the work is complete.` };
  }
  if (starts(lifecycle, "start not confirmed")) {
    if (startRefused(run)) return { tone: "failed", title: "Codex refused to start the run", detail: `Codex refused the starting message, so this workflow did not run.${status.limit ? ` Reason: ${text(status.limit)}.` : ""} You can prepare it again.` };
    return { tone: "uncertain", title: "Start not confirmed — outcome unknown", detail: `The App could not confirm whether Codex received the starting message${status.limit ? ` (${text(status.limit)})` : ""}. It may have run. The App will not resend it. Read the conversation before deciding what to do.` };
  }
  if (starts(lifecycle, "open")) {
    // Live activity belongs to this run only when the run is of the exact
    // current source (generation and home). A run recorded open in an earlier
    // Codex session keeps its lifecycle, but a same-ID thread or request now
    // is not its activity.
    if (!same(run?.generation, host?.generation) || run?.home !== host?.generation?.home)
      return { tone: "uncertain", title: "Open in an earlier Codex session", detail: "This run was recorded open in a Codex session that isn't the current one, so the App can't see what it is doing now. Find its conversation in History." };
    const waiting = hostRequests(host).filter((request: Json) => requestThread(request) === run.conversation && request.state === "outstanding" && (request.generation === undefined || same(request.generation, run.generation))).length;
    if (waiting > 0) return { tone: "waiting", title: "Waiting for your answer", detail: `Codex is asking ${waiting === 1 ? "a question or approval" : `${waiting} questions or approvals`} in the conversation. Answer it there.` };
    const thread = list(host?.threads).find((row: Json) => row.threadId === run.conversation && same(row.generation, host?.generation));
    // The status is Codex's own last report for this conversation, and each
    // reading says that report and nothing that would follow from it: an
    // idle conversation says nothing of agents it delegated to, a waiting
    // flag is Codex's word before any request has reached the App, and the
    // end of the App's observation is not a claim about Codex's process. A
    // status never reported, or not one the App can read, says nothing.
    if (host?.generationClosed === true || thread?.statusObservationEnded === true) return { tone: "uncertain", title: "Open — the App is no longer receiving from Codex", detail: "The App is no longer receiving from the Codex process this run was in, so what the run was doing is not known. Start Codex again under Connection & access, then continue the conversation or end the run." };
    if (thread?.status?.type === "active") {
      const flags = list(thread.status.activeFlags);
      if (flags.includes("waitingOnApproval") || flags.includes("waitingOnUserInput")) return { tone: "waiting", title: "Codex reports it is waiting for an approval or an answer", detail: "Codex reports this conversation is waiting for an approval or for your answer. The request appears in the conversation once the App has received it." };
      return { tone: "working", title: "Open — Codex reports this conversation active", detail: "Codex last reported this conversation as active. Follow its progress in the conversation." };
    }
    if (thread?.status?.type === "systemError") return { tone: "failed", title: "Codex reported an error", detail: "The conversation reported a system error. The run is still open; read the conversation, then continue or end the run." };
    if (thread?.status?.type === "idle") return { tone: "idle", title: "Open — Codex reports this conversation idle", detail: "Codex last reported this conversation as idle, which says nothing about agents it delegated work to. The run stays open until you end it. Reply in the conversation to continue, or end the run when you are done." };
    return { tone: "uncertain", title: "Open — what Codex is doing is not known", detail: `The App cannot establish what Codex is doing in this conversation: ${thread?.statusSource?.limit ? text(thread.statusSource.limit) : thread?.status?.type === "notLoaded" ? "Codex reports the conversation as not loaded" : "it holds no status from Codex for it that it can read"}. The run stays open; read the conversation before deciding what to do.` };
  }
  // A source means the App issued the starting message; whether Codex received it is not established until its reply.
  if (run?.source) return { tone: "working", title: "Starting", detail: "The App has issued the starting message and is waiting for Codex's reply. The run opens when Codex confirms the starting turn." };
  if (status.sent === false && status.limit) {
    const what = NOT_SENT[text(status.state)];
    return { tone: "failed", title: "Not started", detail: `${what ? `Nothing was sent. ${what}` : "The App reports that this run was not sent."}${typeof status.retry === "string" && status.retry ? ` What the App says to do: ${status.retry}.` : ""} The App reported: ${text(status.state)}: ${text(status.limit)}` };
  }
  return { tone: "idle", title: "Ready to start", detail: "The run is prepared and has not been sent. Start it when your inputs are ready." };
}

/** One turn's latest error notice, as the Run guide says it: attributed to its turn, with what the App holds of that turn. */
export type HeldTurnNotice = { turnId: string; words: string; retry: string; count: number; turnStatus: string | null };

/**
 * The error notices the App holds from Codex (the supplier's `error`
 * notification) for an open run's conversation, one for each turn that has
 * any: that turn's latest. They are said beside the run's state because a
 * conversation Codex reports active can be one that cannot reach its model.
 *
 * Each is said as a notice held for its turn, with the status the App holds
 * for that same turn, and as nothing more. Nothing here compares one turn
 * with another: not by start time, not by the order frames reached the App,
 * and there is no "latest turn" or "current turn". The App is not told which
 * turn of a conversation is current, and does not infer it.
 *
 * A turn's notice is left out only on evidence about that same turn: a later
 * frame naming it was received, or the App's receiving ended. Within one turn
 * the latest notice is the one received last, which is an order of frames
 * about the same turn.
 *
 * `count` is the number of notices the host accepted for that one turn; the
 * host keeps the latest of them only. `turnStatus` is the status Codex last
 * reported to the App for that turn, or null where the App holds none. Empty
 * for a run that is not open in the exact current source.
 */
export function runTurnNotices(run: Json, host: Json): HeldTurnNotice[] {
  if (!starts(text(run?.lifecycle?.state), "open") || !same(run?.generation, host?.generation) || run?.home !== host?.generation?.home) return [];
  if (host?.generationClosed === true) return [];
  const view = host?.nativeView, conversation = run.conversation;
  const turnOf = (entry: Json): string | null => (typeof entry?.turnId === "string" && entry.turnId ? entry.turnId : null);
  const mine = list(view?.turnErrors).filter((entry: Json) => entry?.threadId === conversation && turnOf(entry) && same(entry.generation, run.generation));
  const recorded = new Set<string>(list(view?.turnRecords).filter((record: Json) => record?.threadId === conversation).map(turnOf).filter((id): id is string => !!id));
  const received = (entry: Json) => (typeof entry?.observedOrder === "number" ? entry.observedOrder : -1);
  const said: HeldTurnNotice[] = [];
  for (const id of new Set<string>(mine.map((entry: Json) => entry.turnId))) {
    const ofTurn = mine.filter((entry: Json) => entry.turnId === id);
    const notice = ofTurn.reduce((best: Json, entry: Json) => (received(entry) >= received(best) ? entry : best));
    if (notice.laterFrameForTurn === true || notice.observationEnded === true) continue;
    const status = recorded.has(id) ? list(view?.turns).find((entry: Json) => entry?.id === id)?.status : undefined;
    said.push({ turnId: id, words: errorWords(notice.error), turnStatus: typeof status === "string" && status ? status : null,
      count: typeof notice.ordinalInTurn === "number" ? notice.ordinalInTurn : ofTurn.length,
      retry: notice.willRetry === true ? "Codex said it will retry." : notice.willRetry === false ? "Codex said it will not retry." : "Codex did not say whether it will retry." });
  }
  return said;
}
const TURN_STATUS_WORDS: Record<string, string> = { inProgress: "in progress", completed: "completed", failed: "failed", interrupted: "interrupted" };
/** What the App holds of the notice's own turn, in Codex's terms; nothing where it holds no status. */
export const turnStatusWords = (status: string | null): string => (status === null ? "" : `Codex last reported that turn to the App as ${TURN_STATUS_WORDS[status] ?? `“${status}”`}.`);

function declaredRows(declaration: Json, key: string): Json[] {
  return list(declaration?.elements?.[key]).map((element: Json) => element?.value ?? {});
}
const INPUT_KIND: Record<string, string> = { host_read: "read by Codex from the project", file_supplied: "a file you name", person_supplied: "you describe it", workflow_output: "another workflow's result" };

/**
 * J1 — use an existing workflow. A guided reading over the workflow studio's
 * own state and commands: every button calls the same host command as the
 * studio's detailed controls, through the same `act`, with no new default,
 * selection, registration or filesystem write.
 */
/** One run under Results. Navigation only for a run of the exact current source; others are read only. */
function RunResult({ run, host, loaded, showConversation }: { run: Json; host: Json; loaded: boolean; showConversation?: (threadId: string, target?: string) => void }) {
  const reading = runReading(run, host);
  const outputs = declaredRows(list(run?.compatibility).find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration, "returned_outputs");
  return <li aria-label={`Run ${text(run.reference)}`}>
    <strong>{text(run.workflow?.name) || "Workflow run"}</strong>{run.workflow?.revision ? <> (<code title={text(run.workflow.revision)}>{text(run.workflow.revision).slice(0, 12)}…</code>)</> : null} · {reading.title}.
    {outputs.length > 0 && <> It declares: {outputs.map((output: Json, index: number) => <span key={index}>{index ? "; " : ""}<strong>{text(output.name)}</strong>{output.path ? <> (<code>{text(output.path)}</code>)</> : null}</span>)}.</>}
    <br/><small>The agent reports its results in the conversation; the App hasn't checked them.</small>{" "}
    {!loaded ? <small>Its conversation isn't loaded in this Codex session; find it in History.</small>
      : showConversation ? <button onClick={() => showConversation(run.conversation)}>Show the conversation</button> : <a href="#conversation">Go to the conversation</a>}{" "}
    <a href={`#${runEvidenceAnchor(run.reference)}`}>Open this run's recorded evidence (in the workflow studio, under Make a workflow)</a>
  </li>;
}

/** Said in a guide while no status read started after the last command that may change the host has been applied. */
export const VIEW_NOT_REFRESHED = "What this view showed may be from before the App's last operation finished. The App is not showing its steps until it has read its state again after that; it reads again by itself.";
/**
 * A guide while what it holds may be from before the last press: its heading,
 * that statement and the press's own result, and none of its steps. Nothing
 * cached is shown as current and no control is offered.
 */
export function GuideWithheld({ id, label, title, outcome, resultLabel, only, readFailure, children }: { id: string; label: string; title: string; outcome?: GuideOutcome | null; resultLabel: string; only: string[]; readFailure?: string | null; children?: ReactNode }) {
  return <section id={id} className="workflow-stage run-journey" aria-label={label}>
    <h2>{title}</h2>
    <p className="run-journey-next" role="status" aria-live="polite"><strong>Next:</strong> {VIEW_NOT_REFRESHED}</p>
    {readFailure && <p role="alert">The last read failed: {readFailure}</p>}
    <GuideResult label={resultLabel} outcome={outcome} only={only} stepsShown={false}/>
    {children}
  </section>;
}
const RUN_COMMANDS = ["workflow_open_project_library", "workflow_library_entries_refresh", "workflow_review_library_entries", "workflow_select_listed", "workflow_select_production_bundle", "workflow_follow_newer_revision", "workflow_prepare_run", "workflow_send_run", "workflow_end_run"];

export function RunWorkflowGuide({ data, host, thread, chooseThread, act, busy, text: personText, setText, outcome, showConversation, viewStale = false, readFailure = null }: {
  data: Json; host: Json; thread: string; chooseThread: (thread: string) => void; act: Act; busy: boolean; viewStale?: boolean; readFailure?: string | null;
  text: string; setText: (text: string) => void; outcome?: GuideOutcome | null;
  showConversation?: (threadId: string, target?: string) => void;
}) {
  // The unknown-start acknowledgement names one run; a later run starts unacknowledged.
  const [checkedRun, setCheckedRun] = useState<string | null>(null);
  const ready = host?.state === "ready" && host?.generationClosed !== true;
  const sourceCurrent = !!data?.context?.sourceRef && host?.workflowRoot?.context?.sourceRef === data.context.sourceRef && same(data.context.generation, host?.generation);
  const conversations = list(host?.threads).filter((row: Json) => same(row.generation, host?.generation));
  const libraries = list(data?.libraries);
  const active = libraries.find((library: Json) => library.reference === data?.activeLibrary);
  const projectAvailable = data?.projectLibraryAvailable === true;
  const libraryFolder = nativePathText(active?.root);
  const projectFolder = appProjectFolder(host);
  // Every host-changing control goes through one guard: never while busy or
  // while the shown workflow source/generation differs from the host's.
  const canAct = !busy && sourceCurrent;
  const perform = (command: string, args: Record<string, unknown>) => { if (canAct) void act(command, args); };
  // After Prepare, land on Start; after Start, on Progress (not on the page).
  const startButton = useRef<HTMLButtonElement>(null);
  const progressNode = useRef<HTMLDivElement>(null);
  const [landing, setLanding] = useState<"start" | "progress" | null>(null);
  const performThen = (command: string, args: Record<string, unknown>, then: "start" | "progress") => {
    if (!canAct) return;
    void Promise.resolve(act(command, args)).then(() => setLanding(then), () => setLanding(then));
  };
  const registered = list(active?.registered);
  const listing = active?.entryListing;
  const listed = listing?.state === "observed" && listing.libraryRef === active?.reference ? list(listing.entries) : [];
  const unregistered = listed.filter((entry: Json) => entry.reviewable === true && typeof entry.reference === "string");
  const selection = thread ? chatWorkflow(data, data?.context?.sourceRef, thread) : undefined;
  const chosen = selection && selection.state !== "not-selected" ? selection : null;
  const chosenSequence = chosen ? registered.find((row: Json) => row.name === chosen.identity?.name && row.revision === chosen.identity?.revision)?.sequence : undefined;
  // This conversation's runs: the exact current generation, home and thread. A
  // run from an earlier Codex session with the same thread ID is not current.
  const runs = list(data?.runs).filter((run: Json) => run.conversation === thread && run.home === host?.generation?.home && same(run.generation, host?.generation));
  // The host's runs are an unordered map; only its preparationOrder (local to
  // one home and conversation) orders them. Without it for every run, no
  // latest run is chosen and nothing is sorted.
  const order = orderRuns(runs);
  const latest = order.unordered.length === 0 ? order.ordered[0] : runs.length === 1 ? runs[0] : undefined;
  const orderUnknown = !latest && runs.length > 1;
  const preparedUnsent = runs.filter((run: Json) => !run.source && starts(run?.lifecycle?.state, "prepared"));
  const prepared = latest ? (!latest.source && starts(latest?.lifecycle?.state, "prepared") ? latest : null) : preparedUnsent.length === 1 ? preparedUnsent[0] : null;
  const reading = latest ? runReading(latest, host) : null;
  const turnNotices = latest ? runTurnNotices(latest, host) : [];
  // An open run, or one sent and not yet opened, is ended or followed from the studio, not re-prepared here.
  const unresolved = (latest ? [latest] : runs).filter((run: Json) => starts(run.lifecycle?.state, "start not confirmed") && !startRefused(run));
  const unresolvedStart = unresolved.length > 0;
  const holdKey = unresolved.map((run: Json) => text(run.reference)).join("\n");
  const finishedOffer = latest && starts(latest.lifecycle?.state, "open") ? list(data?.offers).find((offer: Json) => offer?.finished?.run === latest.reference) : undefined;
  const inProgress = (latest ? [latest] : runs).some((run: Json) => starts(run.lifecycle?.state, "open") || (!!run.source && starts(run.lifecycle?.state, "prepared")));
  const declaration = list(latest?.compatibility).find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration ?? chosen?.declaration;
  const inputs = declaredRows(declaration, "expected_inputs");
  const outputs = declaredRows(declaration, "returned_outputs");
  const pendingReview = list(data?.reviews).some((review: Json) => review.reference === data?.activeReview && review.status?.presentation);
  const bundled = list(data?.productionCatalog?.entries);
  useEffect(() => {
    if (landing === "start" && startButton.current) { startButton.current.focus?.(); setLanding(null); }
    else if (landing === "progress" && progressNode.current) { progressNode.current.focus?.(); setLanding(null); }
  });
  // Runs that started in this conversation, newest first (a prepared, unsent one is not a run yet).
  const sent = (run: Json) => !(starts(run?.lifecycle?.state, "prepared") && !run.source);
  const resultOrder = orderRuns(runs.filter(sent));
  // Runs of this home that are not current here: another generation (even with
  // the same thread ID) or a conversation not loaded now. Read only, grouped by
  // their conversation; orders are never compared across groups.
  const loadedHere = (run: Json) => same(run.generation, host?.generation) && conversations.some((row: Json) => row.threadId === run.conversation);
  const earlier = list(data?.runs).filter((run: Json) => run.home === host?.generation?.home && sent(run) && !loadedHere(run) && (!thread || run.conversation === thread));
  const earlierGroups: { conversation: string; runs: { ordered: Json[]; unordered: Json[] } }[] = [];
  for (const run of earlier) { const key = text(run.conversation); if (!earlierGroups.some(g => g.conversation === key)) earlierGroups.push({ conversation: key, runs: orderRuns(earlier.filter((r: Json) => text(r.conversation) === key)) }); }
  const recordedRuns = chosen ? list(data?.reopened?.runs).filter((run: Json) => sameWorkflowFamily(run?.workflow, chosen.identity)
    && !list(data?.runs).some((live: Json) => live.reference === run.run)) : [];
  const sameName = (name: Json) => registered.filter((row: Json) => row.name === name).length > 1;
  const newer = chosen?.newerRevision;
  // A current limit (changed store, approval no longer admitted) blocks the run
  // even while the selection's standing admits it (WR §4.6, SL-4).
  // The Library release is named only for a selection that is a catalogue
  // entry by its whole identity; any other is described by its own source.
  const librarySource = librarySourceWords(data?.productionCatalog?.source);
  const chosenSource = !chosen ? "" : includedEntryOf(data?.productionCatalog, chosen) ? `included with the App${librarySource ? `, from ${librarySource}` : ""}`
    : chosen.identity?.origin === "bundled" ? `a bundled copy${chosen.identity?.source_root ? ` (source ${text(chosen.identity.source_root)})` : ""}`
    : `${text(chosen.identity?.origin)} library`;
  const chosenReady = chosen?.runnable === true && !chosen?.currentLimit;
  const chosenLimit = chosen?.runnable === true ? chosen?.currentLimit : chosen?.runLimit;
  const step = !ready ? "Connect Codex first: open Connection & access and start Codex."
    : !sourceCurrent ? "The workflow view is out of date. Wait for it to refresh, or reopen the App view."
    : !active ? projectAvailable ? "Show this project's workflows to begin." : "No project folder is set. Choose one in Desktop setup; it applies the next time you open the App."
    : !thread ? conversations.length ? "Choose the conversation that will run the workflow." : "Start a conversation first, then choose it here."
    : !chosen ? registered.some((row: Json) => row.selectable === true) || bundled.some((entry: Json) => entry.runnable === true) ? "Choose a workflow to use." : "No workflow here is ready to use yet. Review one below, or open another library in the workflow studio."
    : !chosenReady ? `${text(chosen.identity?.name)} can't run: ${text(chosenLimit)}`
    : unresolvedStart && checkedRun !== holdKey ? (latest ? "Read the conversation: the last start's outcome is unknown and it may have run."
      : "Read the conversation: a start here has an unknown outcome and may have run; the App can't tell which run is latest.")
    : orderUnknown && inProgress ? "A run in this conversation is still open, and the App can't tell which run is latest; follow or end it from Results or the workflow studio before preparing another."
    : !latest || starts(latest.lifecycle?.state, "ended") || starts(latest.lifecycle?.state, "start not confirmed") ? "Describe what the workflow should work on, then prepare the run."
    : prepared ? prepared.status?.sent === false && prepared.status?.limit ? "The run didn't start. Progress says why and what to do." : "Check your inputs, then start the run." : orderUnknown ? "This conversation has several runs whose order the App can't tell; see each under Results." : reading?.title ?? "";
  if (viewStale && !busy) return <GuideWithheld id="run-workflow" label="Run a workflow" title="Run a workflow" outcome={outcome} resultLabel="Run a workflow — last result" only={RUN_COMMANDS} readFailure={readFailure}>
    {thread && <p>{showConversation ? <button onClick={() => showConversation(thread)}>Show the conversation</button> : <a href="#conversation">Go to the conversation</a>}</p>}
  </GuideWithheld>;
  return <section id="run-workflow" className="workflow-stage run-journey" aria-label="Run a workflow" aria-busy={busy}>
    <h2>Run a workflow</h2>
    <p className="run-journey-next" role="status" aria-live="polite"><strong>Next:</strong> {step}</p>
    {/* While a press is still in progress its result is not said: the steps below are from before it. */}
    {!busy && <GuideResult label="Run a workflow — last result" outcome={outcome} only={RUN_COMMANDS}/>}
    {readFailure && <p role="alert" aria-label="Last status read failed">The App's last read of its state failed ({readFailure}). What is shown here was read before that.</p>}
    <ol className="run-journey-steps">
      <li aria-labelledby="run-project-heading"><h3 id="run-project-heading">Project</h3>
        <ProjectFolderSummary host={host} libraryAvailable={projectAvailable}/>
        {active ? <p>Using the {text(active.origin) || "opened"} workflow library{libraryFolder ? <> in <code>{libraryFolder}</code></> : ""}.</p>
          : <p>{projectAvailable ? "This App has a project folder. Its workflows are kept in its .chirality folder." : "No project folder is set for this App yet."}</p>}
        {projectAvailable ? <button disabled={!canAct || !ready} onClick={() => perform("workflow_open_project_library", {})}>{active ? "Reload this project's workflows" : "Show this project's workflows"}</button>
          : <p><a href="#desktop-setup">Choose a project in Desktop setup</a> — the choice applies when you next open the App. Or open any workflow library from the workflow studio below.</p>}
      </li>
      <li aria-labelledby="run-conversation-heading"><h3 id="run-conversation-heading">Conversation</h3>
        {conversations.length ? <label>Conversation to run it in <select value={thread} disabled={!canAct} onChange={event => chooseThread(event.target.value)}>
          <option value="">Choose a conversation</option>
          {conversations.map((row: Json) => <option key={row.threadId} value={row.threadId}>{conversationLabel(host, row)}</option>)}
        </select></label> : <p>No conversation in this session yet. <a href="#workspace-start">Start a new conversation</a>, then choose it here.</p>}
        {thread && <details className="conversation-identity"><summary>Exact conversation ID</summary><code>{thread}</code></details>}
        <p><small>The workflow runs inside this conversation; you answer its questions there.</small></p>
      </li>
      <li aria-labelledby="run-workflow-heading"><h3 id="run-workflow-heading">Workflow</h3>
        {chosen && <p aria-label="Workflow chosen for this run"><strong>{text(chosen.identity?.name)}</strong> — {chosenSource}, {chosenSequence !== undefined ? `revision ${text(chosenSequence)} ` : "revision "}<code title={text(chosen.identity?.revision)}>{text(chosen.identity?.revision).slice(0, 12)}…</code>. {chosenReady ? "Ready to run." : `Can't run: ${text(chosenLimit)}`}</p>}
        {chosen && <RoleBesideWorkflow entry={includedEntryOf(data?.productionCatalog, chosen)} conversation={conversations.find((row: Json) => row.threadId === thread)}/>}
        {chosen && chosen.identity?.origin !== "bundled" && <p role="note" aria-label="Approval evidence">{workflowAssurance(chosen.assurance)}</p>}
        {chosen && newer && !(newer.limit && chosen.identity?.origin === "bundled") && (newer.limit ? <p role="note">Newer revisions of {text(chosen.identity?.name)} can't be checked: {text(newer.limit)}</p>
          : <p role="note" aria-label="Newer revision for this conversation">A newer revision of <strong>{text(chosen.identity?.name)}</strong> is registered ({text(newer.notice)}). This conversation keeps using the one shown above until you choose the newer one.{" "}
            {newer.selectable === true ? <button disabled={!canAct} onClick={() => perform("workflow_follow_newer_revision", { selectionRef: chosen.reference, revision: newer.revision })}>{text(newer.offered)}</button> : <small>{text(newer.offered)}.</small>}</p>)}
        {active && registered.length > 0 && <ul aria-label="Workflows ready to use">{registered.map((row: Json) => <li key={`${row.name}@${row.revision}`}>
          <strong>{text(row.name)}</strong> · revision {text(row.sequence)}{chosen && chosen.identity?.name === row.name && chosen.identity?.revision === row.revision ? <> — chosen</> : row.selectable === true
            ? <> <button disabled={!canAct || !thread} onClick={() => perform("workflow_select_listed", { libraryRef: active.reference, name: row.name, revision: row.revision })}>Use {text(row.name)}{sameName(row.name) ? ` revision ${text(row.sequence)}` : ""}</button></>
            : <> — {text(row.label)}.{" "}
              <a href={`#${registeredRevisionAnchor(active.reference, row.name, row.revision)}`}>{row.reconfirm === true ? `Re-confirm ${text(row.name)} in the workflow studio` : "See this revision in the workflow studio"}</a>
              {row.reconfirm === true && <small> Refine it into a draft, then review that draft and confirm in the App's dialog. Nothing is chosen or run until you do.</small>}</>}
          {row.selectable === true && <small> · {text(row.label)}</small>}
        </li>)}</ul>}
        {active && !Array.isArray(active.registered) && active.registered?.limit && <p role="note">This library's list of approved workflows can't be read: {text(active.registered.limit)}</p>}
        {active && registered.length === 0 && Array.isArray(active.registered) && <p>No workflow in this library has been approved for use yet.</p>}
        {active && unregistered.length > 0 && <div aria-label="Workflows that need a first review">
          <p>These workflows are in the folder but haven't been approved for use here. Read one once and confirm it in the App's confirmation dialog; after that it is listed above. Nothing runs during the review.</p>
          <ul>{unregistered.map((entry: Json) => <li key={entry.reference}><strong>{text(entry.name)}</strong>{" "}
            <button disabled={!canAct} onClick={() => perform("workflow_review_library_entries", { libraryRef: active.reference, listingRef: listing.reference, entryRefs: [entry.reference] })}>Review {text(entry.name)} for first use…</button></li>)}</ul>
        </div>}
        {active && listing?.libraryRef === active.reference && listing?.state === "unavailable" && <p role="note">The App couldn't look in this library's folder for other workflows{list(listing.limits).length ? `: ${list(listing.limits).map(text).join("; ")}` : "."}</p>}
        {pendingReview && <p role="note">A review is open. <a href="#workflow-reviews">Read it and confirm</a> to approve the workflow for use.</p>}
        {active && <button disabled={!canAct} onClick={() => perform("workflow_library_entries_refresh", { libraryRef: active.reference })}>Look for other workflows in this library</button>}
        <IncludedWorkflows catalog={data?.productionCatalog} chosen={chosen} disabled={!canAct} needsConversation={!thread} choose={name => perform("workflow_select_production_bundle", { name })}/>
      </li>
      <li aria-labelledby="run-inputs-heading"><h3 id="run-inputs-heading">Inputs</h3>
        {inputs.length > 0 ? <ul aria-label="What this workflow needs">{inputs.map((input: Json, index: number) => <li key={index}>
          <strong>{text(input.name)}</strong> ({input.necessity === "optional" ? "optional" : "required"}; {INPUT_KIND[text(input.kind)] ?? text(input.kind)}): {text(input.meaning)}{input.absence_effect ? ` If you leave it out: ${text(input.absence_effect)}` : ""}</li>)}</ul>
          : chosen ? <p>This workflow doesn't list required inputs. Describe what it should work on.</p> : <p>Choose a workflow to see what it needs.</p>}
        <label>What should the workflow work on? <textarea value={personText} onChange={event => setText(event.target.value)} disabled={busy} rows={3}/></label>
        <p><small>Name any files in the project folder that it should use. This text goes with the workflow's own instructions in one starting message.</small></p>
      </li>
      <li aria-labelledby="run-start-heading"><h3 id="run-start-heading">Start</h3>
        {!prepared ? <>{unresolvedStart && <p><label><input type="checkbox" checked={checkedRun === holdKey} disabled={!canAct} onChange={event => setCheckedRun(event.target.checked ? holdKey : null)}/> I read the conversation and want to prepare a new run anyway</label>
            <small>The earlier start may have run; a new run sends the workflow again.</small></p>}
          <button className="setup-primary" disabled={!canAct || !ready || !thread || !chosenReady || inProgress || (unresolvedStart && checkedRun !== holdKey)}
          onClick={() => { if (!unresolvedStart || checkedRun === holdKey) performThen("workflow_prepare_run", { generation: host.generation, threadId: thread, personText }, "start"); }}>Prepare this run</button></>
          : <><p>Prepared {text(prepared.workflow?.name)} with your text. Nothing has been sent yet.</p>
            <button ref={startButton} className="setup-primary" disabled={!canAct || !ready} onClick={() => performThen("workflow_send_run", { runRef: prepared.reference }, "progress")}>Start the run</button>
            {prepared.status?.sent === false && prepared.status?.limit && <>{" "}<button disabled={!canAct || !ready || !thread || !chosenReady} onClick={() => performThen("workflow_prepare_run", { generation: host.generation, threadId: thread, personText }, "start")}>Prepare this run again</button></>}</>}
        <p><small>Preparing composes the starting message from the chosen revision; nothing is sent. Starting records the run and sends that message once — if recording fails, nothing is sent.</small></p>
      </li>
      <li aria-labelledby="run-progress-heading"><h3 id="run-progress-heading">Progress</h3>
        {reading ? <><div ref={progressNode} tabIndex={-1} className={`run-journey-state run-journey-${reading.tone}`} aria-label="Run progress">
          <p role="status"><strong>{reading.title}.</strong> {reading.detail}</p>
          {(starts(latest.lifecycle?.state, "open") || reading.tone === "uncertain") && <p>{showConversation
            ? <button onClick={() => showConversation(latest.conversation, reading.tone === "waiting" ? "conversation-requests" : "conversation")}>{reading.tone === "waiting" ? "Answer in the conversation" : "Show the conversation"}</button>
            : <a href="#conversation">Go to the conversation</a>}</p>}
          {finishedOffer && <p aria-label="Agent finished report"><strong>The agent wrote “{text(finishedOffer.finished.statement)}”.</strong> This is the agent's statement.{" "}
            <button disabled={!canAct} onClick={() => perform("workflow_end_run", { runRef: latest.reference, finishedReport: finishedOffer.message })}>End as completed, on the agent's report</button></p>}
          {starts(latest.lifecycle?.state, "open") && <p><button disabled={!canAct} onClick={() => perform("workflow_end_run", { runRef: latest.reference, finishedReport: null })}>End this run</button>{" "}
            <small>Ending here records that you ended it — not that it completed. To stop only Codex's current step, use Stop in the conversation; the run stays open.</small></p>}
        </div>
        {/* Held notices, each with its turn. Outside the state above and without its marking: they are not a reading of the run. */}
        {turnNotices.length > 0 && <div role="note" aria-label="Error notices the App holds for this conversation">
          {turnNotices.map(notice => <p key={notice.turnId}>The App holds an error notice from Codex for turn <code>{notice.turnId}</code> of this conversation{notice.count > 1 ? `; it is the latest of ${notice.count} for that turn` : ""}: <q>{notice.words}</q> {notice.retry}{notice.turnStatus !== null ? ` ${turnStatusWords(notice.turnStatus)}` : ""}</p>)}
          <p>The conversation's activity shows each notice the App has kept, with its turn.</p>
        </div>}</> : orderUnknown ? <p role="status">This conversation has several runs, and the App can't tell which one is the latest. Each is listed under Results.</p> : <p>No run in this conversation yet.</p>}
      </li>
      <li aria-labelledby="run-results-heading"><h3 id="run-results-heading">Results</h3>
        {(resultOrder.ordered.length + resultOrder.unordered.length) > 0 && <ul aria-label="Runs in this conversation">
          {resultOrder.ordered.map((run: Json) => <RunResult key={text(run.reference)} run={run} host={host} loaded showConversation={showConversation}/>)}
          {resultOrder.unordered.length > 0 && <li><small>{resultOrder.ordered.length ? "These runs' order isn't known:" : resultOrder.unordered.length > 1 ? "The App doesn't know these runs' order:" : ""}</small></li>}
          {resultOrder.unordered.map((run: Json) => <RunResult key={text(run.reference)} run={run} host={host} loaded showConversation={showConversation}/>)}
        </ul>}
        {earlierGroups.length > 0 && <div aria-label="Runs whose conversation isn't loaded">
          <p>{thread ? "Earlier runs with this conversation ID, from a Codex session that isn't loaded now:" : "Earlier runs whose conversation isn't loaded in this Codex session:"}</p>
          {earlierGroups.map(group => <div key={group.conversation}><p><small>Recorded conversation <code>{group.conversation}</code>{group.runs.unordered.length > 1 || (group.runs.unordered.length && group.runs.ordered.length) ? " (order of some runs isn't known)" : ""}</small></p>
            <ul>{[...group.runs.ordered, ...group.runs.unordered].map((run: Json) => <RunResult key={text(run.reference)} run={run} host={host} loaded={false} showConversation={showConversation}/>)}</ul></div>)}
        </div>}
        {recordedRuns.length > 0 && <div aria-label="Recorded runs of this workflow">
          <p>Recorded runs of {text(chosen?.identity?.name)} from the project's records (read only; not live in this session):</p>
          <ul>{recordedRuns.map((run: Json) => <li key={text(run.run)}>{text(run.run)}{run.workflow?.revision ? <> · revision <code title={text(run.workflow.revision)}>{text(run.workflow.revision).slice(0, 12)}…</code></> : null} · {text(run.state)} · recorded conversation <code>{text(run.conversation) || "not recorded"}</code> · {workflowAssurance(run.assurance)}</li>)}</ul>
        </div>}
        {outputs.length > 0 ? <ul aria-label="Where the results go">{outputs.map((output: Json, index: number) => <li key={index}>
          <strong>{text(output.name)}</strong>{output.path ? <> — declared path <code>{text(output.path)}</code></> : ""}{output.meaning ? `: ${text(output.meaning)}` : ""}</li>)}</ul>
          : <p>{chosen ? "This workflow doesn't declare where its results go; the agent reports them in the conversation." : "Choose a workflow to see what it produces."}</p>}
        <p><small>These are what the workflow declares it produces; the App hasn't checked that any of them exist. {projectFolder !== null ? <>A relative declared path is the workflow's own wording; the App doesn't establish whether it is inside the project folder <code>{projectFolder}</code>.</> : "The App has not reported a matching project folder; the library location alone does not establish output locations."} Files Codex actually changed are listed in the conversation's activity.</small></p>
      </li>
    </ol>
  </section>;
}
