import { AgentText, idWords, wordOf } from "./AgentText";
import { hostRequests, requestThread } from "./RequestCards";
import { activityModel, errorWords } from "./NativeActivity";
import { type ReactNode } from "react";

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
    {result.detail && <details><summary>What the App reported</summary><AgentText block value={result.detail} source="record" /></details>}</div>;
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
      return { tone: "uncertain", title: "Open in an earlier Codex session", detail: "This run was recorded open in a Codex session that isn't the current one, so the App can't see what it is doing now. Find its conversation in History, under More." };
    const waiting = hostRequests(host).filter((request: Json) => requestThread(request) === run.conversation && request.state === "outstanding" && (request.generation === undefined || same(request.generation, run.generation))).length;
    if (waiting > 0) return { tone: "waiting", title: "Waiting for your answer", detail: `Codex is asking ${waiting === 1 ? "a question or approval" : `${waiting} questions or approvals`} in the conversation. Answer it there.` };
    const thread = list(host?.threads).find((row: Json) => row.threadId === run.conversation && same(row.generation, host?.generation));
    // The status is Codex's own last report for this conversation, and each
    // reading says that report and nothing that would follow from it: an
    // idle conversation says nothing of agents it delegated to, a waiting
    // flag is Codex's word before any request has reached the App, and the
    // end of the App's observation is not a claim about Codex's process. A
    // status never reported, or not one the App can read, says nothing.
    if (host?.generationClosed === true || thread?.statusObservationEnded === true) return { tone: "uncertain", title: "Open — the App is no longer receiving from Codex", detail: "The App is no longer receiving from the Codex process this run was in, so what the run was doing is not known. Start Codex again under Connection and access, then continue the conversation or end the run." };
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

/**
 * What the App holds about the agents a conversation delegated work to (the host's `nativeView.descendants`, the
 * whole subtree under the conversation), each read on its own:
 *   - active: Codex's status row for that agent's own conversation (`threads`, this Codex session, observation not
 *     ended) is "active"; or, with no such row, the delegating item's last report of it
 *     (`lastObservedStatus.status` from `collabAgentToolCall.agentsStates`, observation not ended) is "running" or
 *     "pendingInit", which is what the host itself counts as an observed active child (runtime_session.rs);
 *   - idle: its own status row is "idle", and no delegating item's report says it is running or starting;
 *   - unreadable: anything else (no row and no running report, a row that is neither active nor idle, a row and a
 *     report that disagree, an observation that ended).
 * `viewReadable` is false where the App holds no native view of this Codex session to read descendants from: then it
 * cannot tell whether the conversation delegated anything.
 */
export type DelegatedReading = { viewReadable: boolean; active: number; idle: number; unreadable: number };
export function delegatedReading(conversation: Json, host: Json): DelegatedReading {
  const view = host?.nativeView;
  if (!view || !same(view.generation, host?.generation) || host?.nativeViewObservationEnded === true || view.observationEnded === true)
    return { viewReadable: false, active: 0, idle: 0, unreadable: 0 };
  const reading = { viewReadable: true, active: 0, idle: 0, unreadable: 0 };
  for (const child of activityModel(view, text(conversation)).subtree) {
    const row = list(host?.threads).find((t: Json) => t?.threadId === child?.threadId && same(t?.generation, host?.generation) && t?.statusObservationEnded !== true);
    const reported = child?.lastObservedStatus;
    const reportedStatus = reported && typeof reported === "object" ? reported.status : reported;
    const reportedRunning = child?.observationEnded !== true && (reportedStatus === "running" || reportedStatus === "pendingInit");
    if (row?.status?.type === "active" || (!row && reportedRunning)) reading.active += 1;
    else if (row?.status?.type === "idle" && !reportedRunning) reading.idle += 1;
    else reading.unreadable += 1;
  }
  return reading;
}

/** The actions a run's state offers in the Run tab, each the present guide's own act or navigation. */
export type RunWordAction = "answer" | "show" | "reply" | "end" | "end-completed";
/** The mark beside a state's word: one shape for each, so the state never rests on colour alone. */
export type RunMark = "you" | "move" | "work" | "said" | "ended" | "quiet" | "unknown" | "failed";
/** A run's state in a word, one short sentence, and what it offers. */
export type RunWord = { word: string; sentence: string; mark: RunMark; actions: RunWordAction[] };
/** Said where a conversation has several runs and the App cannot tell which is latest. */
export const ORDER_UNKNOWN_WORD: RunWord = { word: "Order unknown", sentence: "This conversation has several runs, and the App can't tell which is the latest. Each is under Details.", mark: "unknown", actions: [] };

/**
 * The Run tab's and the status strip's shorter reading of a run: over exactly the conditions `runReading` decides,
 * in the same order, never saying more than its branch establishes. `finishedOffer` is the host's finished offer for
 * this run, as the guide finds it. Where a run is open in this Codex session and Codex reports its conversation idle,
 * the agents it delegated to are read too (delegatedReading), since an idle conversation says nothing of them.
 */
export function runWord(run: Json, host: Json, finishedOffer?: Json): RunWord {
  const lifecycle = text(run?.lifecycle?.state);
  const status = run?.status ?? {};
  if (starts(lifecycle, "ended")) {
    const cause = text(run.lifecycle?.end?.cause);
    if (cause === "completed") return { word: "Ended", sentence: "You ended it as completed, on the agent's report.", mark: "ended", actions: [] };
    if (cause === "ended by the person") return { word: "Ended", sentence: "You ended it.", mark: "ended", actions: [] };
    if (starts(cause, "ended to start ")) return { word: "Ended", sentence: "It ended so that another workflow could start.", mark: "ended", actions: [] };
    return { word: "Ended", sentence: "The run ended. Its recorded cause is under Details.", mark: "ended", actions: [] };
  }
  if (starts(lifecycle, "start not confirmed")) {
    if (startRefused(run)) return { word: "Start refused", sentence: "Codex refused the starting message, so this workflow did not run.", mark: "failed", actions: [] };
    return { word: "Start unknown", sentence: "The App can't tell whether Codex received the starting message. It may have run, and the App will not resend it. Read the conversation first.", mark: "unknown", actions: ["show"] };
  }
  if (starts(lifecycle, "open")) {
    // As runReading: a run recorded open in an earlier Codex session is never read against this session's activity.
    if (!same(run?.generation, host?.generation) || run?.home !== host?.generation?.home)
      return { word: "Earlier session", sentence: "Open in a Codex session that isn't the current one, so the App can't see what it is doing. Find its conversation in History, under More.", mark: "unknown", actions: [] };
    const offered: RunWordAction[] = finishedOffer ? ["end-completed", "end"] : ["end"];
    const waiting = hostRequests(host).filter((request: Json) => requestThread(request) === run.conversation && request.state === "outstanding" && (request.generation === undefined || same(request.generation, run.generation))).length;
    if (waiting > 0) return { word: "Needs answer", sentence: waiting === 1 ? "Codex is asking a question or approval in the conversation." : `Codex is asking ${waiting} questions or approvals in the conversation.`, mark: "you", actions: ["answer", ...offered] };
    const thread = list(host?.threads).find((row: Json) => row.threadId === run.conversation && same(row.generation, host?.generation));
    if (host?.generationClosed === true || thread?.statusObservationEnded === true)
      return { word: "Not receiving", sentence: "The App is no longer receiving from Codex for this run, so what it was doing is not known.", mark: "unknown", actions: ["show", ...offered] };
    if (thread?.status?.type === "active") {
      const flags = list(thread.status.activeFlags);
      if (flags.includes("waitingOnApproval") || flags.includes("waitingOnUserInput"))
        return { word: "Waiting", sentence: "Codex reports it is waiting for an approval or your answer. The request shows in the conversation once the App receives it.", mark: "you", actions: ["show", ...offered] };
      return { word: "Working", sentence: "Codex reports this conversation active.", mark: "work", actions: ["show", ...offered] };
    }
    if (thread?.status?.type === "systemError") return { word: "Error", sentence: "Codex reported a system error. The run is still open; read the conversation first.", mark: "failed", actions: ["show", ...offered] };
    if (thread?.status?.type === "idle") {
      const delegated = delegatedReading(run.conversation, host);
      if (delegated.active > 0) return { word: "Working", sentence: "The agent's turn has ended, and an agent it delegated work to is reported active.", mark: "work", actions: ["show", ...offered] };
      const unseen = !delegated.viewReadable || delegated.unreadable > 0;
      if (finishedOffer) return { word: "Agent says finished", sentence: `That is the agent's word. Ending the run is yours.${unseen ? " The App can't see whether agents it delegated to are still working." : ""}`, mark: "said", actions: offered };
      if (unseen) return { word: "Turn ended", sentence: delegated.viewReadable ? "The agent's turn has ended. The App can't see whether the agents it delegated to are still working." : "The agent's turn has ended. The App can't see whether it delegated work to other agents.", mark: "unknown", actions: ["reply", ...offered] };
      return { word: "Your move", sentence: "The agent's turn has ended. The run is open.", mark: "move", actions: ["reply", ...offered] };
    }
    return { word: "State unknown", sentence: "The App can't tell what Codex is doing in this conversation. Read it before deciding what to do.", mark: "unknown", actions: ["show", ...offered] };
  }
  if (run?.source) return { word: "Starting", sentence: "The App has issued the starting message and is waiting for Codex's reply.", mark: "work", actions: [] };
  if (status.sent === false && status.limit) return { word: "Not started", sentence: `${NOT_SENT[text(status.state)] ? "Nothing was sent." : "The App reports this run was not sent."} Details say why.`, mark: "failed", actions: [] };
  return { word: "Not started", sentence: "The run is prepared. Nothing has been sent.", mark: "quiet", actions: [] };
}

/**
 * The run of one conversation, as the Run guide chooses it: this conversation's runs in the exact current Codex
 * session and home, the latest by the host's `preparationOrder` (or the only one), none where several runs' order is
 * unknown; the host's finished offer for the latest open run; and its state in a word. One function, so the Run tab
 * and the status strip never disagree.
 */
export function conversationRun(data: Json, host: Json, thread: string) {
  const runs = thread ? list(data?.runs).filter((run: Json) => run.conversation === thread && run.home === host?.generation?.home && same(run.generation, host?.generation)) : [];
  const order = orderRuns(runs);
  const latest: Json = order.unordered.length === 0 ? order.ordered[0] : runs.length === 1 ? runs[0] : undefined;
  const orderUnknown = !latest && runs.length > 1;
  const finishedOffer: Json = latest && starts(latest.lifecycle?.state, "open") ? list(data?.offers).find((offer: Json) => offer?.finished?.run === latest.reference) : undefined;
  const word: RunWord | null = latest ? runWord(latest, host, finishedOffer) : orderUnknown ? ORDER_UNKNOWN_WORD : null;
  return { runs, latest, orderUnknown, finishedOffer, word };
}
/** What the status strip names for a conversation's run: the workflow's name and the Run tab's word; null with no run. */
export function stripRun(data: Json, host: Json, thread: string): { name: string; word: string; mark: RunMark } | null {
  const { latest, word } = conversationRun(data, host, thread);
  if (!word) return null;
  return { name: latest ? text(latest.workflow?.name) || "Workflow run" : "Workflow runs", word: word.word, mark: word.mark };
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
 * host keeps the latest of them only. `turnStatus` is the status the App
 * holds for that turn from Codex's reports (not always the last one received:
 * the host keeps a reported end over a later stale report of progress), or
 * null where it holds none or cannot tie one to this conversation's turn.
 * Empty for a run that is not open in the exact current source.
 */
export function runTurnNotices(run: Json, host: Json): HeldTurnNotice[] {
  if (!starts(text(run?.lifecycle?.state), "open") || !same(run?.generation, host?.generation) || run?.home !== host?.generation?.home) return [];
  if (host?.generationClosed === true) return [];
  const view = host?.nativeView, conversation = run.conversation;
  const turnOf = (entry: Json): string | null => (typeof entry?.turnId === "string" && entry.turnId ? entry.turnId : null);
  const mine = list(view?.turnErrors).filter((entry: Json) => entry?.threadId === conversation && turnOf(entry) && same(entry.generation, run.generation));
  // The host reports a turn's row with the turn's id only, and which conversation holds a turn of that id in a
  // separate list. So a row is this conversation's turn only where exactly one record names that id, it is this
  // conversation's, and exactly one row has the id. Where another conversation also holds a turn of that id, the
  // App cannot tell the rows apart and says no status. The two lists are not paired by position: nothing declares it.
  const heldStatus = (id: string): string | null => {
    const records = list(view?.turnRecords).filter((record: Json) => turnOf(record) === id);
    const rows = list(view?.turns).filter((row: Json) => row?.id === id);
    if (records.length !== 1 || records[0].threadId !== conversation || rows.length !== 1) return null;
    return typeof rows[0].status === "string" && rows[0].status ? rows[0].status : null;
  };
  const received = (entry: Json) => (typeof entry?.observedOrder === "number" ? entry.observedOrder : -1);
  const said: HeldTurnNotice[] = [];
  for (const id of new Set<string>(mine.map((entry: Json) => entry.turnId))) {
    const ofTurn = mine.filter((entry: Json) => entry.turnId === id);
    const notice = ofTurn.reduce((best: Json, entry: Json) => (received(entry) >= received(best) ? entry : best));
    if (notice.laterFrameForTurn === true || notice.observationEnded === true) continue;
    said.push({ turnId: id, words: errorWords(notice.error), turnStatus: heldStatus(id),
      count: typeof notice.ordinalInTurn === "number" ? notice.ordinalInTurn : ofTurn.length,
      retry: notice.willRetry === true ? "Codex said it will retry." : notice.willRetry === false ? "Codex said it will not retry." : "Codex did not say whether it will retry." });
  }
  return said;
}
const TURN_STATUS_WORDS: Record<string, string> = { inProgress: "in progress", completed: "completed", failed: "failed", interrupted: "interrupted" };
/** What the App holds of the notice's own turn, in Codex's terms; nothing where it holds no status. */
export const turnStatusWords = (status: string | null): string => (status === null ? "" : `The App holds Codex's report of that turn as ${TURN_STATUS_WORDS[status] ?? `“${status}”`}.`);

export function declaredRows(declaration: Json, key: string): Json[] {
  return list(declaration?.elements?.[key]).map((element: Json) => element?.value ?? {});
}
export const INPUT_KIND: Record<string, string> = { host_read: "read by Codex from the project", file_supplied: "a file you name", person_supplied: "you describe it", workflow_output: "another workflow's result" };

/** One run of the open conversation under the Run tab's Details (only runs of the exact current source are listed there). */
export function RunResult({ run, host, showConversation }: { run: Json; host: Json; showConversation?: (threadId: string, target?: string) => void }) {
  const reading = runReading(run, host);
  const outputs = declaredRows(list(run?.compatibility).find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration, "returned_outputs");
  return <li aria-label={`Run ${idWords(run.reference)}`}>
    <strong>{text(run.workflow?.name) || "Workflow run"}</strong>{run.workflow?.revision ? <> (<code title={idWords(run.workflow.revision)}>{text(run.workflow.revision).slice(0, 12)}…</code>)</> : null} · {reading.title}.
    {outputs.length > 0 && <> It declares: {outputs.map((output: Json, index: number) => <span key={index}>{index ? "; " : ""}<strong>{text(output.name)}</strong>{output.path ? <> (<code>{text(output.path)}</code>)</> : null}</span>)}.</>}
    <br/><small>The agent reports its results in the conversation; the App hasn't checked them.</small>{" "}
    {showConversation ? <button onClick={() => showConversation(run.conversation)}>Show the conversation</button> : <a href="#conversation">Go to the conversation</a>}{" "}
    <a href={`#${runEvidenceAnchor(run.reference)}`}>Open this run's recorded evidence (in the workflow studio, under More › Make a workflow)</a>
  </li>;
}

/** Said in a view while no status read started after the last command that may change the host has been applied. */
export const VIEW_NOT_REFRESHED = "What this view showed may be from before the App's last operation finished. The App is not showing its steps until it has read its state again after that; it reads again by itself.";
/** The guide's words: its title (and accessible name), its result's label and its section's id. */
const GUIDE_TITLE = { make: "Make a workflow from your work" } as const;
const GUIDE_RESULT_LABEL = { make: "Make a workflow — last result" } as const;
const GUIDE_ID = { make: "make-workflow" } as const;
/**
 * A guide while what it holds may be from before the last press: its heading,
 * that statement and the press's own result, and none of its steps. Nothing
 * cached is shown as current and no control is offered.
 */
export function GuideWithheld({ guide, outcome, only, readFailure, children }: { guide: keyof typeof GUIDE_TITLE; outcome?: GuideOutcome | null; only: string[]; readFailure?: string | null; children?: ReactNode }) {
  return <section id={GUIDE_ID[guide]} className="workflow-stage run-journey" aria-label={wordOf(GUIDE_TITLE, guide) ?? ""}>
    <h2>{wordOf(GUIDE_TITLE, guide)}</h2>
    <p className="run-journey-next" role="status" aria-live="polite"><strong>Next:</strong> {VIEW_NOT_REFRESHED}</p>
    {readFailure && <p role="alert">The last read failed: {readFailure}</p>}
    <GuideResult label={wordOf(GUIDE_RESULT_LABEL, guide) ?? ""} outcome={outcome} only={only} stepsShown={false}/>
    {children}
  </section>;
}
