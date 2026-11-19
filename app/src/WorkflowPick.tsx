// The workflow picked for the next message, and the press that starts a run with it (owner's first journey: pick a
// workflow in the Workflows tab, write what it should work on, press once). The pick is the renderer's alone: the host
// keeps a workflow selection only for a conversation that exists and has no command that clears one, so nothing is
// sent or stored when a workflow is picked or removed. The press issues the Run guide's own commands, in its order and
// under its guards (the former Run a workflow guide's, which this replaced). A command whose outcome the App could not establish is kept with
// what it was for, and is not issued again until a later read establishes its outcome or the person says to go on.
import { AgentText, idWords, safeName, wordOf } from "./AgentText";
import { chatWorkflow, workflowArguments, workflowAssurance, workflowContext } from "./workflowSelection";
import { WorkflowTextControl, useWorkflowTexts } from "./WorkflowText";
import { LibraryPathsBesideWorkflow, RoleBesideWorkflow, includedEntryOf, librarySourceWords } from "./IncludedWorkflows";
import { RequirementCheck, requirementReading, type ToolState } from "./RequirementCheck";
import { INPUT_KIND, declaredRows, guideResultWords, orderRuns, runReading, startRefused } from "./RunJourney";
import { hostMessage } from "./TrialComposer";
import { useEffect, useState } from "react";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => (typeof value === "string" ? value : "");
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);
const starts = (value: Json, prefix: string) => typeof value === "string" && value.startsWith(prefix);

/** One workflow picked in the Workflows tab, as its card shows it, and the source it was picked in. */
export type WorkflowPick = {
  kind: "included" | "listed";
  name: string;
  revision: string;
  /** The opened library a registered revision is listed in (workflow_select_listed's libraryRef). */
  libraryRef?: string;
  /** A registered revision's number in its library, as the card shows it. */
  sequence?: number;
  /** A registered revision's standing, as the library listing words it (workflow_library.rs registered_listing). */
  label?: string;
  /** The card's heading: the Library's title for an included workflow, else the name. */
  title: string;
  /** Where it comes from, in the card's words. */
  from: string;
  /** The workflow source, Codex generation and home it was picked under (pickScope). */
  scope: string;
};

/** What a pick is bound to: the host's workflow source, its Codex generation and the home in use. A change to any may
 * mean the same name no longer names the same thing, so the App drops the pick (App.tsx). */
export const pickScope = (host: Json): string => JSON.stringify([host?.workflowRoot?.context?.sourceRef ?? null, host?.generation ?? null, host?.homeRouting?.activeModeHomeClass ?? null]);
/** What one press is bound to besides its conversation: the pick's scope and the workflow library in use. */
export const pressBinding = (host: Json): string => JSON.stringify([pickScope(host), host?.workflowRoot?.activeLibrary ?? null]);
/** Two picks are the same workflow, picked in the same source. */
export const samePick = (a: WorkflowPick | null | undefined, b: WorkflowPick | null | undefined): boolean =>
  !!a && !!b && a.kind === b.kind && a.name === b.name && a.revision === b.revision && (a.libraryRef ?? null) === (b.libraryRef ?? null) && a.scope === b.scope;

export function pickIncluded(entry: Json, catalog: Json, host: Json): WorkflowPick {
  return { kind: "included", name: text(entry?.name), revision: text(entry?.revision), title: text(entry?.navigation?.displayName) || text(entry?.name),
    from: librarySourceWords(catalog?.source) || "Included with the App", scope: pickScope(host) };
}
export function pickListed(row: Json, library: Json, host: Json): WorkflowPick {
  return { kind: "listed", name: text(row?.name), revision: text(row?.revision), libraryRef: text(library?.reference), sequence: Number.isSafeInteger(row?.sequence) ? row.sequence : undefined,
    label: text(row?.label), title: text(row?.name), from: library?.origin === "project" ? "Project workflow library" : "Opened workflow library", scope: pickScope(host) };
}
/** Whether a card is the picked workflow. */
export const isIncludedPick = (pick: WorkflowPick | null | undefined, entry: Json) => !!pick && pick.kind === "included" && pick.name === entry?.name && pick.revision === entry?.revision;
export const isListedPick = (pick: WorkflowPick | null | undefined, row: Json, library: Json) => !!pick && pick.kind === "listed" && pick.libraryRef === library?.reference && pick.name === row?.name && pick.revision === row?.revision;

/** Text the App did not write (a workflow's title, description or name, a tool's or input's name, a host's reason),
 * drawn plain in the line it stands in: AgentText's named group, which says whose text it is to assistive technology
 * and shows control and direction characters as marks; its box and visible label are left out (workspace.css
 * .v4-supplied), so a card's title reads as a title. Never inside a control. */
export function Supplied({ value, of }: { value: Json; of: SuppliedKind }) {
  return <span className="v4-supplied"><AgentText value={value} source="file" label="" name={wordOf(SUPPLIED_NAMES, of) ?? "Text the App did not write"} /></span>;
}
/** Whose text a Supplied value is, in the App's words (its accessible name). */
export const SUPPLIED_NAMES = {
  title: "A workflow's own title, not the App's words",
  description: "A workflow's own description, not the App's words",
  name: "A workflow's own name, not the App's words",
  tool: "A tool as the workflow names it, not the App's words",
  input: "An input as the workflow names it, not the App's words",
  meaning: "What the workflow says of an input, not the App's words",
  reason: "What the App's host reported, not the App's words",
  roles: "Roles as the Library lists them, not the App's words",
} as const;
export type SuppliedKind = keyof typeof SUPPLIED_NAMES;

/** Why the picked workflow cannot be used now, from what the catalogue or the library listing says before any
 * selection; null when nothing there stops it. Parts: the App's words, and the host's or Library's text marked. */
export function pickLimit(pick: WorkflowPick, host: Json): Part[] | null {
  const root = host?.workflowRoot;
  if (pick.kind === "included") {
    const catalog = root?.productionCatalog;
    const entry = list(catalog?.entries).find((row: Json) => row?.name === pick.name);
    if (!entry || entry.revision !== pick.revision) return ["It is no longer listed among the included workflows as it was when you picked it. Pick it again under Workflows."];
    if (entry.runnable === false) { const why = text(entry.runLimit) || text(catalog?.standing); return why ? ["Can't be used in this App: ", reported(why), "."] : ["Can't be used in this App: the App reports it as not runnable."]; }
    if (entry.runnable !== true) return ["The App hasn't reported whether this workflow can be used here."];
    return null;
  }
  const library = list(root?.libraries).find((row: Json) => row?.reference === pick.libraryRef);
  const row = list(library?.registered).find((entry: Json) => entry?.name === pick.name && entry?.revision === pick.revision);
  if (!library || root?.activeLibrary !== pick.libraryRef || !row) return ["It is no longer listed in the opened workflow library. Pick it again under Workflows."];
  if (row.selectable !== true) return text(row.label) ? [reported(text(row.label)), "."] : ["It can't be chosen now."];
  return null;
}

/** The conversation's workflow selection when it is the picked workflow by its whole identity, else undefined. */
export function pickedSelection(host: Json, thread: string, pick: WorkflowPick): Json {
  const root = host?.workflowRoot;
  const selection = thread ? chatWorkflow(root, root?.context?.sourceRef, thread) : undefined;
  if (!selection || selection.state === "not-selected") return undefined;
  if (pick.kind === "included") {
    const entry = includedEntryOf(root?.productionCatalog, selection);
    return entry && entry.name === pick.name && entry.revision === pick.revision && selection.identity?.revision === pick.revision ? selection : undefined;
  }
  const library = list(root?.libraries).find((row: Json) => row?.reference === pick.libraryRef);
  const id = selection.identity;
  return library && id?.origin === library.origin && id?.source_root === library.sourceRoot && id?.name === pick.name && id?.revision === pick.revision ? selection : undefined;
}

/** A run row the host gave in full: its conversation, home, generation and lifecycle. A row with only a reference (the
 * host's "original run operation pending", while another operation holds the run) establishes nothing about the run. */
export const completeRun = (row: Json): boolean => !!row && typeof row.reference === "string" && typeof row.conversation === "string" && typeof row.home === "string"
  && !!row.generation && typeof row.lifecycle?.state === "string";

/**
 * What the Run guide held about a conversation's runs that decides whether a run may start there (as it read them:
 * runs of the exact current generation, home and thread; the latest by preparationOrder; a start whose outcome is
 * unknown; a run open or sent and not yet confirmed). `partial`: the host gave a row that names no conversation, which
 * may be this one's.
 */
export function conversationRuns(host: Json, thread: string) {
  const runs = list(host?.workflowRoot?.runs).filter((run: Json) => run.conversation === thread && run.home === host?.generation?.home && same(run.generation, host?.generation));
  const order = orderRuns(runs);
  const latest = order.unordered.length === 0 ? order.ordered[0] : runs.length === 1 ? runs[0] : undefined;
  const unresolved = (latest ? [latest] : runs).filter((run: Json) => starts(run.lifecycle?.state, "start not confirmed") && !startRefused(run));
  const inProgress = (latest ? [latest] : runs).some((run: Json) => starts(run.lifecycle?.state, "open") || (!!run.source && starts(run.lifecycle?.state, "prepared")));
  const partial = list(host?.workflowRoot?.runs).some((run: Json) => !completeRun(run));
  return { runs, latest, unresolvedStart: unresolved.length > 0, holdKey: unresolved.map((run: Json) => text(run.reference)).join("\n"), inProgress, partial };
}

/** A run the App established was sent, or may have been: anything but a complete prepared row with nothing sent. */
const mayHaveBeenSent = (run: Json) => !completeRun(run) || !!run.source || !starts(run.lifecycle?.state, "prepared");
/**
 * The name of the workflow chosen for a conversation, for the transcript's "chosen, not started" note, only where the
 * App establishes both: the host shows a workflow chosen for it, and no run of the conversation that was sent or may
 * have been (a prepared run never sent does not count; a row the host gave only in part, which may be this
 * conversation's, and a start this composer could not confirm, both may have been). Else null.
 */
export function chosenNotStarted(host: Json, thread: string, doubted: boolean): string | null {
  const root = host?.workflowRoot;
  const chosen = thread ? chatWorkflow(root, root?.context?.sourceRef, thread) : undefined;
  const name = chosen && chosen.state !== "not-selected" ? text(chosen.identity?.name) : "";
  if (!name || doubted || !Array.isArray(root?.runs)) return null;
  const mine = (run: Json) => !completeRun(run) || run.conversation === thread && run.home === host?.generation?.home;
  return root.runs.some((run: Json) => mine(run) && mayHaveBeenSent(run)) ? null : name;
}

/** What a read establishes about a preparation whose reply gave no run: the one new prepared run of the conversation
 * (`found`), or, with every run given in full and none new, that nothing was prepared; else nothing (`established` false). */
function preparationOutcome(host: Json, conversation: string, before: readonly string[]): { established: boolean; found?: Json } {
  const rows = list(host?.workflowRoot?.runs);
  if (!Array.isArray(host?.workflowRoot?.runs) || rows.some((r: Json) => !completeRun(r))) return { established: false };
  const fresh = rows.filter((r: Json) => r.conversation === conversation && !before.includes(r.reference));
  if (!fresh.length) return { established: true };
  return fresh.length === 1 && !fresh[0].source && starts(fresh[0].lifecycle.state, "prepared") ? { established: true, found: fresh[0] } : { established: false };
}

/** The declared part of a selection as the Run guide reads it. */
const declarationOf = (selection: Json) => selection?.compatibility?.preparation?.declaration ?? selection?.declaration;

/** The short reading shown beside a chosen workflow before its run (release criterion 1; DEL-02-03 REQ-001): each
 * declared required tool by name with its state, read with the guide's own requirementReading, and the inputs it asks
 * for. Its key is what a press compares with what it reads: a press sends only what was shown. */
export type PickReview = { words: string; tools: { name: string; state: ToolState }[]; inputs: { name: string; optional: boolean }[] };
export function pickReview(selection: Json): PickReview {
  const read = requirementReading(selection);
  const inputs = declaredRows(declarationOf(selection), "expected_inputs").map((input: Json) => ({ name: text(input.name), optional: input.necessity === "optional" }));
  if (read.kind === "undeclared") return { words: "Required tools: not declared, so the App can't check them.", tools: [], inputs };
  if (read.kind === "unreadable") return { words: "Required tools: the App couldn't read them.", tools: [], inputs };
  if (read.kind === "empty") return { words: "Required tools: it declares none.", tools: [], inputs };
  const tools = read.tools.filter(t => t.required).map(t => ({ name: text(t.tool.name), state: t.reading.state }));
  if (!tools.length) return { words: "Required tools: none required.", tools, inputs };
  if (!read.checked) return { words: "Required tools, not checked for this conversation:", tools: tools.map(t => ({ ...t, state: "unknown" as const })), inputs };
  return { words: "Required tools:", tools, inputs };
}
const TOOL_STATE_WORDS: Record<ToolState, string> = { available: "available", unavailable: "unavailable now", missing: "missing", unknown: "not established" };
export const reviewKey = (selection: Json, conversation: string): string => JSON.stringify([conversation, text(selection?.reference), selection?.identity ?? null, pickReview(selection)]);

// ---- The press: the steps, in the Run guide's order, through its commands ----

/** A piece of a line: the App's words, or text the App did not write, drawn marked (Supplied). */
export type Part = string | { supplied: string; of: SuppliedKind };
const reported = (value: string): Part => ({ supplied: value, of: "reason" });
/** A line's text, as a test or a screen reader reads it. */
export const partsText = (parts: readonly Part[]): string => parts.map(part => typeof part === "string" ? part : part.supplied).join("");
export function PartsLine({ parts }: { parts: readonly Part[] }) {
  return <>{parts.map((part, index) => typeof part === "string" ? part : <Supplied key={index} value={part.supplied} of={part.of}/>)}</>;
}

/** What a start of a new conversation came to (App.tsx StartOutcome). */
type StartOutcome = { opened: string } | { failed: string } | { notConfirmed: true };
/** A command this composer issued whose outcome the App has not established: which command, for which conversation and
 * workflow, what it was bound to, the runs the conversation had before it, and the host's reply where one came. */
export type PickDoubt = { kind: "choose" | "prepare" | "send"; conversation: string; binding: string; command: string; key: string; reference?: string; before?: string[]; reply: string;
  /** For a send: what its run was prepared for (preparationKey), so a run the host later shows not sent may be sent again. */
  prepared?: string };
/** What the composer keeps between presses, for the App session. */
export type PickMemory = {
  /** Runs this composer prepared and has not sent, by conversation, with what each was prepared for (preparationKey). */
  prepared: Map<string, { reference: string; key: string }>;
  /** Runs this composer asked the host to send: never asked again. */
  attempted: Set<string>;
  /** Commands whose outcome is not established, by conversation. */
  doubts: Map<string, PickDoubt>;
};
export const pickMemory = (): PickMemory => ({ prepared: new Map(), attempted: new Set(), doubts: new Map() });
/** What a preparation was made for: the selection and workflow, the conversation, home, Codex generation and text. */
export const preparationKey = (selection: Json, pick: WorkflowPick, conversation: string, host: Json, personText: string): string =>
  JSON.stringify([text(selection?.reference), selection?.identity ?? null, [pick.kind, pick.name, pick.revision, pick.libraryRef ?? null], conversation, host?.homeRouting?.activeModeHomeClass ?? null, host?.generation?.home ?? null, host?.generation ?? null, personText]);

/** What the composer holds back on for a conversation: the guide's unknown starts and this composer's doubts. `sent`
 * when one of them may have sent the workflow; `key` is what the person's acknowledgement names. */
export function pickHold(host: Json, thread: string, memory: PickMemory): { key: string; sent: boolean } | null {
  if (!thread) return null;
  const runs = conversationRuns(host, thread);
  const doubt = memory.doubts.get(thread);
  if (!runs.unresolvedStart && !doubt) return null;
  return { key: JSON.stringify([runs.holdKey, doubt?.key ?? null]), sent: runs.unresolvedStart || doubt?.kind === "send" };
}

export type PickRun = {
  pick: WorkflowPick;
  text: string;
  /** The conversation shown, or null in a new chat (steps 1 and 2 run first). */
  thread: string | null;
  /** The conversation's key as the App holds the person's choice ("" in a new chat). */
  threadKey: string;
  /** The view the person pressed on. */
  host: Json;
  /** The review the composer was showing when the person pressed (reviewKey), or null. */
  shown: string | null;
  /** Now: the latest status the App has accepted, the key of the conversation the person has chosen ("" for none), the pick and the draft. */
  now: () => { host: Json; thread: string; pick: WorkflowPick | null; text: string };
  /** Step 1: the new chat's present start (App.tsx startConversation). */
  start: () => Promise<StartOutcome | null>;
  /** A host command; rejects with the host's message. */
  act: (command: string, args: Record<string, unknown>) => Promise<Json>;
  /** A read of host_status, applied to the view; resolves to the latest status the App has accepted; rejects when it fails. */
  read: () => Promise<Json>;
  /** Says which step is under way. */
  step: (words: string) => void;
  memory: PickMemory;
  /** The hold (pickHold key) the person said they read, or null. */
  acknowledged: string | null;
  /** Between host_status reads (step 2). */
  pause?: (ms: number) => Promise<void>;
};
export type PickRunOutcome =
  | { state: "started" }
  | { state: "nothing" }
  /** Stopped to show what the workflow needs before anything is sent; Start run goes on from step 5. */
  | { state: "review"; opened?: string; changed?: boolean }
  /** `startUnknown`: the conversation's start was not confirmed, so one may exist; the composer starts no other until the person says. */
  | { state: "stopped"; parts: Part[]; opened?: string; startUnknown?: boolean };

/** The step words shown while the press runs. */
export const PICK_STEPS = { start: "Starting the conversation…", choose: "Choosing the workflow…", prepare: "Preparing the run…", send: "Starting the run…",
  follow: "Moving to the newer revision…", read: "Reading the App's state…" } as const;
const NOTHING_SENT = "Nothing was sent.";
/** The host's refusals a person can meet here before anything was done, in short words (the guide's REFUSAL_WORDS
 * name the same exact replies, for the commands they can come from); any other reply is the host's, shown marked. */
const REASON_WORDS: Record<string, string> = {
  "Native history context is busy; refresh the workflow choice": "the App was busy reading conversation history",
  "Workflow App home source changed; refresh the displayed choice": "the App's view was out of date",
  "Workflow native generation changed; refresh the displayed choice": "the App's view was out of date",
  "Native history selection changed; refresh the displayed workflow choice": "the App's view was out of date",
  "The displayed workflow choice changed; refresh before selecting, inspecting or preparing": "the App's view was out of date",
  "Workflow source or chat changed; refresh the displayed choice before acting": "the conversation is no longer current in this view",
};
const replyOf = (error: unknown): string => hostMessage(error).replace(/^Error: /, "").trim();
/** Whether a choice or preparation was refused before anything was done: one of the exact replies above. */
const refusedFirst = (error: unknown): boolean => Object.hasOwn(REASON_WORDS, replyOf(error));
export function reasonPart(error: unknown): Part {
  const reply = replyOf(error);
  if (Object.hasOwn(REASON_WORDS, reply)) return REASON_WORDS[reply];
  return reply ? reported(reply.replace(/[.\s]+$/, "")) : "the App gave no reason";
}
/** Codex or the workflow source changed under the press: the steps stop where they are. */
const CHANGED = "Codex or the workflow source changed, so the App stopped";
const MOVED = {
  library: "The workflow library in use changed, so the App stopped",
  conversation: "Another conversation was chosen while the App was working, so it stopped",
  pick: "Another workflow was picked while the App was working, so it stopped",
  text: "Your text changed while the App was working, so it stopped",
} as const;
/** The guide's reading of a run (runReading), with the host's reason marked where the guide's words place it. */
function readingParts(run: Json, host: Json): Part[] {
  const limit = run?.status?.limit;
  const HERE = "\u0000";
  const reading = runReading(limit ? { ...run, status: { ...run.status, limit: HERE } } : run, host);
  const [before, ...after] = `${reading.title}. ${reading.detail}`.split(HERE);
  return after.length ? [before, reported(text(limit) || JSON.stringify(limit)), after.join("")] : [before];
}
/** The words of a start the App could not confirm, as the guide says them for a start not confirmed. */
const notConfirmedWords = (host: Json) => { const reading = runReading({ lifecycle: { state: "start not confirmed" }, status: {} }, host); return `${reading.title}. ${reading.detail}`; };
let doubtSequence = 0;

/**
 * One press: (1) start the conversation and (2) read the status until its row appears, in a new chat; (3) choose the
 * workflow for it unless it already is, and (4) read the status for the selection; then stop to show what it needs,
 * unless the composer was showing exactly that when the person pressed; (5) prepare the run with the person's text and
 * (6) send it. After every await the press goes on only while the source, library, conversation, pick and text are
 * those it was pressed with. A command whose outcome is not established is kept (PickMemory.doubts): the next press
 * reads first and acts only on what the read establishes.
 */
export async function runPickedWorkflow(run: PickRun): Promise<PickRunOutcome> {
  const { pick, text: personText, memory } = run;
  const pressed = run.host;
  const scope = pick.scope, binding = pressBinding(pressed);
  let host = pressed, thread = run.thread;
  let opened: string | undefined;
  let chose = false, preparedNow = false;
  const stop = (...parts: Part[]): PickRunOutcome => ({ state: "stopped", parts, ...(opened ? { opened } : {}) });
  // What was done before the press stopped for a change: each step is said, and nothing was sent.
  const done = () => [opened ? " The conversation started." : "", chose ? " The workflow was chosen for it." : "", preparedNow ? " The run was prepared." : ""].join("");
  const moved = (): PickRunOutcome | null => {
    const now = run.now();
    const why = pickScope(now.host) !== scope ? CHANGED : pressBinding(now.host) !== binding ? MOVED.library
      : !samePick(now.pick, pick) ? MOVED.pick : now.text !== personText ? MOVED.text
      : (run.thread ? now.thread !== run.threadKey : now.thread !== "" && now.thread !== opened) ? MOVED.conversation : null;
    return why ? stop(`${why}.${done()} ${NOTHING_SENT}`) : null;
  };
  const early = moved();
  if (early) return early;
  if (!thread) {
    run.step(PICK_STEPS.start);
    const outcome = await run.start();
    if (!outcome) return { state: "nothing" };
    if ("failed" in outcome) return stop("Couldn't start the conversation: ", reasonPart(outcome.failed), `. ${NOTHING_SENT}`);
    let key: Json = null;
    if ("opened" in outcome) { try { key = JSON.parse(outcome.opened); } catch { key = null; } }
    if (!Array.isArray(key) || typeof key[1] !== "string") return { state: "stopped", parts: ["The App couldn't confirm the conversation started; it may exist. The workflow wasn't sent."], startUnknown: true };
    opened = (outcome as { opened: string }).opened;
    thread = key[1];
    // Step 2: the new conversation's row, which the selection's context names.
    let seen: Json = null;
    for (let attempt = 0; attempt < 4 && !seen; attempt++) {
      if (attempt) await (run.pause ?? (ms => new Promise<void>(resolve => setTimeout(resolve, ms))))(250);
      try { host = await run.read(); } catch { host = null; }
      const change = moved();
      if (change) return change;
      seen = list(host?.threads).find((row: Json) => row.threadId === thread && same(row.generation, host?.generation));
    }
    if (!seen) return stop(`The conversation started, but the App couldn't read it back, so the workflow wasn't chosen. ${NOTHING_SENT}`);
  } else {
    // An open conversation: its runs as the host holds them now, not as the view last drew them.
    run.step(PICK_STEPS.read);
    try { host = await run.read(); } catch { return stop(`The App couldn't read its state, so it didn't start the run. ${NOTHING_SENT}`); }
    const change = moved();
    if (change) return change;
  }
  const conversation = thread as string;
  // The guide's conditions (no run of it still open or sent and unconfirmed; a start of unknown outcome only once
  // acknowledged), and this composer's own doubts, reconciled with what this read establishes.
  const runs = conversationRuns(host, conversation);
  if (runs.inProgress) return stop(`A workflow run is still open in this conversation. End it with End run in the Run tab before starting another. ${NOTHING_SENT}`);
  const hold = pickHold(host, conversation, memory);
  const acknowledged = !!hold && run.acknowledged === hold.key;
  const doubt = memory.doubts.get(conversation);
  if (doubt && doubt.binding !== binding && !acknowledged) return stop(`An earlier step here has an outcome the App couldn't establish, under another Codex session or workflow source. Read the conversation, then confirm below to go on. ${NOTHING_SENT}`);
  if (doubt?.kind === "send") {
    const row = list(host?.workflowRoot?.runs).find((r: Json) => r.reference === doubt.reference);
    // Established only by a complete row: Codex's own refusal, or the host's own "nothing sent". Anything else (a row
    // given in part, a missing row, an outcome unknown) holds until the person says they read the conversation.
    const full = completeRun(row) && row.conversation === conversation;
    if (full && starts(row.lifecycle.state, "start not confirmed") && startRefused(row)) memory.doubts.delete(conversation);
    else if (full && starts(row.lifecycle.state, "prepared") && !row.source && row.status?.sent === false) {
      memory.doubts.delete(conversation); memory.attempted.delete(text(doubt.reference));
      if (doubt.prepared) memory.prepared.set(conversation, { reference: text(doubt.reference), key: doubt.prepared });
    } else if (!acknowledged) return stop(`${notConfirmedWords(host)} Nothing more was sent.`);
    else { memory.doubts.delete(conversation); memory.prepared.delete(conversation); }
  }
  if (runs.unresolvedStart && !acknowledged) return stop(`Read the conversation: a start here has an unknown outcome and may have run. ${NOTHING_SENT}`);
  // Steps 3 and 4: the selection, unless the conversation already has exactly this workflow chosen.
  let selection = pickedSelection(host, conversation, pick);
  if (doubt?.kind === "choose") {
    // The choice's outcome: the host's selection for the conversation, which this read gives in full or not at all.
    if (selection || Array.isArray(host?.workflowRoot?.selections) || acknowledged) memory.doubts.delete(conversation);
    else return stop(`The App couldn't establish whether the workflow was chosen, so it didn't choose it again. Press Start run to read again. ${NOTHING_SENT}`);
  }
  if (!selection) {
    const notChosen = (...reason: Part[]) => stop(opened ? "The conversation started, but the workflow wasn't chosen: " : "The workflow wasn't chosen for this conversation: ", ...reason, `. ${NOTHING_SENT}`);
    const [command, args]: [string, Record<string, unknown>] = pick.kind === "included" ? ["workflow_select_production_bundle", { name: pick.name }]
      : ["workflow_select_listed", { libraryRef: pick.libraryRef, name: pick.name, revision: pick.revision }];
    let request: Record<string, unknown>;
    try { request = workflowArguments(command, args, host?.workflowRoot, host, conversation); } catch (error) { return notChosen(reasonPart(error)); }
    run.step(PICK_STEPS.choose);
    let refused: unknown = null, reply: Json = null;
    try { reply = await run.act(command, request); } catch (error) { refused = error ?? "the App gave no reason"; }
    if (refused !== null && refusedFirst(refused)) return notChosen(reasonPart(refused));
    chose = refused === null;
    // Until a read establishes it, the choice's outcome is kept, with the host's reply.
    memory.doubts.set(conversation, { kind: "choose", conversation, binding, command, key: `choose:${++doubtSequence}`, reply: refused !== null ? replyOf(refused) : JSON.stringify(reply ?? null) });
    try { host = await run.read(); } catch { return stop(`${opened ? "The conversation started, but the" : "The"} App couldn't read whether the workflow was chosen. ${NOTHING_SENT}`); }
    const change = moved();
    if (change) return change;
    selection = pickedSelection(host, conversation, pick);
    if (!Array.isArray(host?.workflowRoot?.selections) && !selection) return stop(`${opened ? "The conversation started, but the" : "The"} App couldn't read whether the workflow was chosen. ${NOTHING_SENT}`);
    memory.doubts.delete(conversation);
    if (refused !== null && !selection) return notChosen(reasonPart(refused));
    if (!selection) return notChosen("the App doesn't show it chosen for the conversation");
    chose = true;
  }
  // The guide's condition to prepare: the selection runnable and with no current limit, in the host's words.
  const limit = selection.runnable === true ? selection.currentLimit : selection.runLimit;
  if (selection.runnable !== true || selection.currentLimit) return stop("The workflow can't run: ", text(limit) ? reported(text(limit)) : "the App reports it as not runnable", `. ${NOTHING_SENT}`);
  // Release target criterion 1: before the run the App says which declared required tools are available and which are
  // missing. A press goes on to prepare only when the composer was showing this selection with this reading when the
  // person pressed; otherwise it stops here and shows it.
  if (run.shown !== reviewKey(selection, conversation)) return { state: "review", ...(opened ? { opened } : {}), ...(run.shown && !chose ? { changed: true } : {}) };
  // Step 5: prepare, unless this composer prepared a run for exactly this and it is still prepared and unsent.
  const want = preparationKey(selection, pick, conversation, host, personText);
  if (doubt?.kind === "prepare" && memory.doubts.get(conversation) === doubt) {
    const outcome = preparationOutcome(host, conversation, doubt.before ?? []);
    if (outcome.found) {
      // Prepared. Used only for exactly what it was prepared for; otherwise left unsent, as the guide leaves one no longer wanted.
      if (want === doubt.key.slice(doubt.key.indexOf(":") + 1)) memory.prepared.set(conversation, { reference: outcome.found.reference, key: want });
      memory.doubts.delete(conversation);
    } else if (!outcome.established) {
      if (!acknowledged) return stop(`The App couldn't establish whether the run was prepared, so it didn't prepare it again. Read the Run tab, then confirm below to go on. ${NOTHING_SENT}`);
      memory.doubts.delete(conversation);
    } else memory.doubts.delete(conversation); // every row read in full, none new: nothing was prepared.
  }
  const kept = memory.prepared.get(conversation);
  let reference = kept && kept.key === want && !memory.attempted.has(kept.reference) ? kept.reference : "";
  if (kept && !reference) memory.prepared.delete(conversation); // made for something else: left unsent, as the guide leaves a prepared run no longer wanted.
  if (!reference) {
    const notPrepared = (...reason: Part[]) => stop(opened ? "The conversation started and the workflow was chosen, but the run wasn't prepared: " : "The run wasn't prepared: ", ...reason, `. ${NOTHING_SENT}`);
    let request: Record<string, unknown>;
    try { request = workflowArguments("workflow_prepare_run", { generation: host.generation, threadId: conversation, personText }, host?.workflowRoot, host, conversation); }
    catch (error) { return notPrepared(reasonPart(error)); }
    const before = list(host?.workflowRoot?.runs).map((r: Json) => text(r.reference));
    run.step(PICK_STEPS.prepare);
    let refused: unknown = null, reply: Json = null;
    try { reply = await run.act("workflow_prepare_run", request); } catch (error) { refused = error ?? "the App gave no reason"; }
    if (refused !== null && refusedFirst(refused)) return notPrepared(reasonPart(refused));
    reference = text(reply?.reference);
    if (!reference) {
      // The reply establishes nothing: kept, and the status read now. Said "wasn't prepared" only when the read shows
      // every run in full and none new; a new prepared run is the one this press made; anything else holds.
      const kept: PickDoubt = { kind: "prepare", conversation, binding, command: "workflow_prepare_run", key: `${++doubtSequence}:${want}`, before, reply: refused !== null ? replyOf(refused) : JSON.stringify(reply ?? null) };
      memory.doubts.set(conversation, kept);
      const why: Part = refused !== null ? reasonPart(refused) : "the App didn't report the prepared run";
      try { host = await run.read(); } catch { return stop("The App couldn't establish whether the run was prepared: ", why, `. ${NOTHING_SENT}`); }
      const change = moved();
      if (change) return change;
      const outcome = preparationOutcome(host, conversation, before);
      if (!outcome.established) return stop("The App couldn't establish whether the run was prepared: ", why, `. ${NOTHING_SENT}`);
      memory.doubts.delete(conversation);
      if (!outcome.found) return notPrepared(why);
      reference = text(outcome.found.reference);
      memory.prepared.set(conversation, { reference, key: want });
    } else {
    memory.prepared.set(conversation, { reference, key: want });
    try { host = await run.read(); } catch { preparedNow = true; return stop(`The run was prepared, but the App couldn't read its state afterwards, so it wasn't started. ${NOTHING_SENT}`); }
    }
    preparedNow = true;
    const change = moved();
    if (change) return change;
  }
  // The guide's Start: the conversation's latest run, prepared and unsent, given in full, whose records may be saved.
  const now = conversationRuns(host, conversation);
  const prepared = now.runs.find((row: Json) => row.reference === reference);
  if (!completeRun(prepared) || prepared.source || !starts(prepared.lifecycle.state, "prepared") || now.latest?.reference !== reference)
    return stop(`The run was prepared, but the App can't read it as ready to start now, so it wasn't started. Press Start run to read it again. ${NOTHING_SENT}`);
  if (prepared.publication?.admissionRefusal) return stop("The run was prepared, but its records can't be saved: ", reasonPart(prepared.publication.admissionRefusal), `. It wasn't started. ${NOTHING_SENT}`);
  if (memory.attempted.has(reference)) return stop("This run was already sent once, so the App won't send it again. Read the conversation.");
  // Step 6: send, once. Kept as a doubt until the host's row establishes what happened.
  run.step(PICK_STEPS.send);
  memory.attempted.add(reference);
  memory.prepared.delete(conversation);
  memory.doubts.set(conversation, { kind: "send", conversation, binding, command: "workflow_send_run", key: `send:${reference}`, reference, reply: "", prepared: want });
  let sendError: unknown = null, reply: Json = null;
  try { reply = await run.act("workflow_send_run", { runRef: reference }); } catch (error) { sendError = error ?? "the App gave no reason"; }
  const held = memory.doubts.get(conversation)!;
  held.reply = sendError !== null ? replyOf(sendError) : JSON.stringify(reply ?? null);
  let after: Json = null;
  try { after = await run.read(); } catch { after = null; }
  const sent = list(after?.workflowRoot?.runs).find((row: Json) => row.reference === reference);
  if (!after) {
    // What happened is not read: the present result of the press, and no second send.
    const said = guideResultWords({ command: "workflow_send_run", message: sendError === null ? "" : hostMessage(sendError), failed: sendError !== null, settled: true }, false);
    return stop(sendError === null ? `${said?.words ?? "Start requested."} ` : "Couldn't start the run: ", ...(sendError === null ? [] : [reasonPart(sendError), ". "]), "The App couldn't read the run's state afterwards and won't send it again; read the conversation.");
  }
  if (!completeRun(sent) || sent.conversation !== conversation) return stop(notConfirmedWords(after));
  if (starts(sent.lifecycle.state, "start not confirmed")) {
    // The guide's reading, with the host's reason marked.
    if (startRefused(sent)) memory.doubts.delete(conversation);
    return stop(...readingParts(sent, after));
  }
  if (starts(sent.lifecycle.state, "open") || sent.source && starts(sent.lifecycle.state, "prepared")) { memory.doubts.delete(conversation); return { state: "started" }; }
  if (starts(sent.lifecycle.state, "prepared") && !sent.source && sent.status?.sent === false) {
    // The host's own "nothing sent": the same prepared run may be started again.
    memory.doubts.delete(conversation);
    memory.attempted.delete(reference);
    memory.prepared.set(conversation, { reference, key: want });
    return stop("The run wasn't started: ", sendError === null ? "the App didn't report why" : reasonPart(sendError), `. ${NOTHING_SENT}`);
  }
  return stop(notConfirmedWords(after));
}

// ---- What the person sees beside the chip ----

/** What following a newer revision from the chip needs: the composer's host command (it reads the status after), a read of
 * host_status, the composer's step line, and the pick to replace with the revision followed. */
export type PickFollow = {
  act: (command: string, args: Record<string, unknown>) => Promise<Json>;
  read?: () => Promise<Json>;
  step: (words: string) => void;
  repick: (pick: WorkflowPick) => void;
};
const FOLLOW = "workflow_follow_newer_revision";

/**
 * The run guide's "follow the newer revision", at the chip: where the conversation's chosen workflow (the picked one)
 * has a newer registered revision, the guide's note, and its command with the guide's arguments under the guide's
 * conditions (not while busy, not while the shown workflow source or Codex session is not the host's; offered only
 * where the host says the newer revision is selectable). A limit on reading newer revisions is said as the guide said
 * it, except for a bundled selection, which has no library revisions to follow. Once followed, the pick becomes the
 * revision followed, so that Start run does not choose the earlier one again.
 */
type FollowResult = { words: string; failed: boolean } | null;
function NewerRevision({ pick, host, thread, selection, disabled, follow, setResult }: { pick: WorkflowPick; host: Json; thread: string; selection: Json; disabled: boolean; follow?: PickFollow;
  setResult: (result: FollowResult) => void }) {
  const root = host?.workflowRoot;
  const newer = selection?.newerRevision;
  if (!newer || newer.limit && selection.identity?.origin === "bundled") return null;
  const name = text(selection.identity?.name);
  if (newer.limit) return <p role="note">Newer revisions of <strong>{name}</strong> can't be checked: {text(newer.limit)}</p>;
  const sourceCurrent = !!root?.context?.sourceRef && same(root.context.generation, host?.generation);
  const canFollow = !disabled && sourceCurrent && !!follow;
  const said = (message: string, failed: boolean) => {
    const words = guideResultWords({ command: FOLLOW, message, failed, settled: true }, false);
    setResult(words ? { words: words.words, failed } : null);
  };
  const press = async () => {
    if (!canFollow || !follow) return;
    let request: Record<string, unknown>;
    try { request = workflowArguments(FOLLOW, { selectionRef: selection.reference, revision: newer.revision }, root, host, thread); }
    catch (error) { said(`Error: ${hostMessage(error)}`, true); return; }
    follow.step(PICK_STEPS.follow);
    let refused: unknown = null, after: Json = null;
    try {
      try { await follow.act(FOLLOW, request); } catch (error) { refused = error ?? "the App gave no reason"; }
      if (refused === null && follow.read) { try { after = await follow.read(); } catch { after = null; } }
    } finally { follow.step(""); }
    if (refused !== null) { said(`Error: ${hostMessage(refused)}`, true); return; }
    said("", false);
    if (pick.kind !== "listed") return;
    const library = list(after?.workflowRoot?.libraries).find((row: Json) => row?.reference === pick.libraryRef);
    const row = list(library?.registered).find((entry: Json) => entry?.name === pick.name && entry?.revision === newer.revision);
    follow.repick(row ? pickListed(row, library, after) : { ...pick, revision: text(newer.revision), sequence: Number.isSafeInteger(newer.sequence) ? newer.sequence : undefined, label: "", scope: pickScope(after ?? host) });
  };
  return <div role="note" aria-label="Newer revision for this conversation">
    <p>A newer revision of <strong>{name}</strong> is registered ({text(newer.notice)}). This conversation keeps the one it has until you choose the newer one.</p>
    {newer.selectable === true ? <p><button type="button" disabled={!canFollow} onClick={() => { void press(); }}>Use the newer revision</button></p> : <p><small>{text(newer.offered)}.</small></p>}
  </div>;
}

/** The chip, and beside it what the App holds about the picked workflow for the conversation the press would use. */
export function PickChip({ pick, host, thread, disabled, remove, follow }: { pick: WorkflowPick; host: Json; thread: string; disabled: boolean; remove: () => void; follow?: PickFollow }) {
  const root = host?.workflowRoot;
  // The last press of "Use the newer revision", said under the note; it stays once the note goes with the revision followed.
  const [followed, setFollowed] = useState<FollowResult>(null);
  // Another workflow picked (not the same one at the revision followed): the result was of the earlier one.
  const pickedWorkflow = JSON.stringify([pick.kind, pick.name, pick.libraryRef ?? null, thread]);
  useEffect(() => { setFollowed(null); }, [pickedWorkflow]);
  const selection = thread ? pickedSelection(host, thread, pick) : undefined;
  const revision = pick.kind === "listed" && pick.sequence !== undefined ? `revision ${pick.sequence}` : null;
  const entry = pick.kind === "included" ? list(root?.productionCatalog?.entries).find((row: Json) => row?.name === pick.name && row?.revision === pick.revision) : undefined;
  const review = selection ? pickReview(selection) : null;
  const inputs = selection ? declaredRows(declarationOf(selection), "expected_inputs") : [];
  const conversation = list(host?.threads).find((row: Json) => row.threadId === thread && same(row.generation, host?.generation));
  // The chosen workflow's own text, read as the conversation's selection (the former guide's read, under its conditions).
  const texts = useWorkflowTexts();
  const sourceCurrent = !!root?.context?.sourceRef && same(root.context.generation, host?.generation);
  const librarySource = librarySourceWords(root?.productionCatalog?.source);
  const chosenSource = !selection ? "" : includedEntryOf(root?.productionCatalog, selection) ? `included with the App${librarySource ? `, from ${librarySource}` : ""}`
    : selection.identity?.origin === "bundled" ? `a bundled copy${selection.identity?.source_root ? ` (source ${text(selection.identity.source_root)})` : ""}`
    : `${text(selection.identity?.origin)} library`;
  return <div className="v4-pick" aria-label="Workflow for this message">
    <ul className="method-chip-list" aria-label="Workflow picked">
      {/* The chip names the workflow and its source (and a registered revision's number); the revision digest is
          whole under Details. */}
      <li className="method-chip"><span><Supplied value={pick.title} of="title"/></span><small>{pick.from}{revision ? ` · ${revision}` : null}</small>
        <button type="button" aria-label="Remove the picked workflow" title="Remove" disabled={disabled} onClick={remove}>×</button></li>
    </ul>
    {review ? <p className="v4-pick-note" aria-label="What it needs">{review.words}{review.tools.map((tool, index) => <span key={index}>{index ? ", " : " "}<Supplied value={tool.name || "Unnamed tool"} of="tool"/> {TOOL_STATE_WORDS[tool.state]}</span>)}{review.tools.length ? "." : ""}
      {review.inputs.length > 0 && <> It asks for: {review.inputs.map((input, index) => <span key={index}>{index ? ", " : ""}<Supplied value={input.name} of="input"/>{input.optional ? " (optional)" : ""}</span>)}.</>}</p>
      : <p className="v4-pick-note">Press Start run to see the tools it needs. Nothing is sent until you press again.</p>}
    <details className="v4-pick-details"><summary>Details</summary>
      {inputs.length > 0 && <ul aria-label="What this workflow needs">{inputs.map((input: Json, index: number) => <li key={index}>
        <Supplied value={text(input.name)} of="input"/> ({input.necessity === "optional" ? "optional" : "required"}; {INPUT_KIND[text(input.kind)] ?? "kind not recognised"}): <Supplied value={text(input.meaning)} of="meaning"/>{input.absence_effect ? <> If you leave it out: <Supplied value={text(input.absence_effect)} of="meaning"/></> : null}</li>)}</ul>}
      {selection && !inputs.length && <p>This workflow doesn't list required inputs. Describe what it should work on.</p>}
      {selection && <WorkflowTextControl slot={`chosen:${text(root?.context?.sourceRef)}:${thread}`} identity={selection.identity} source={chosenSource} texts={texts}
        disabled={disabled || !sourceCurrent} target={{ kind: "selection", revision: selection.identity?.revision }} context={() => workflowContext(root, host, thread)}/>}
      {selection && <RequirementCheck selection={selection}/>}
      {selection && <RoleBesideWorkflow entry={includedEntryOf(root?.productionCatalog, selection)} conversation={conversation}/>}
      {selection && selection.identity?.origin !== "bundled" && <p role="note" aria-label="Approval evidence">{workflowAssurance(selection.assurance)}</p>}
      {!selection && pick.kind === "listed" && pick.label && <p><Supplied value={pick.label} of="reason"/></p>}
      {selection && <NewerRevision pick={pick} host={host} thread={thread} selection={selection} disabled={disabled} follow={follow} setResult={setFollowed}/>}
      {followed && <p role={followed.failed ? "alert" : "status"}>{followed.words}</p>}
      {entry && <LibraryPathsBesideWorkflow entry={entry} source={root?.productionCatalog?.source}/>}
      <p>Revision <code>{idWords(pick.revision)}</code></p>
    </details>
  </div>;
}
