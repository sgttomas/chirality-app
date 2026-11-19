// The workflow picked for the next message, and the press that starts a run with it (owner's first journey: pick a
// workflow in the Workflows tab, write what it should work on, press once). The pick is the renderer's alone: the host
// keeps a workflow selection only for a conversation that exists and has no command that clears one, so nothing is
// sent or stored when a workflow is picked or removed. The press issues the Run guide's own commands, in its order and
// under its guards (RunJourney.tsx RunWorkflowGuide), each awaited once and none retried.
import { safeName } from "./AgentText";
import { chatWorkflow, workflowArguments, workflowAssurance } from "./workflowSelection";
import { LibraryPathsBesideWorkflow, RoleBesideWorkflow, includedEntryOf, librarySourceWords } from "./IncludedWorkflows";
import { RequirementCheck, toolReading } from "./RequirementCheck";
import { INPUT_KIND, declaredRows, guideResultWords, orderRuns, runReading, startRefused } from "./RunJourney";
import { hostMessage } from "./TrialComposer";

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

export function pickIncluded(entry: Json, catalog: Json, host: Json): WorkflowPick {
  return { kind: "included", name: text(entry?.name), revision: text(entry?.revision), title: text(entry?.navigation?.displayName) || text(entry?.name),
    from: librarySourceWords(catalog?.source) || "Included with the App", scope: pickScope(host) };
}
export function pickListed(row: Json, library: Json, host: Json): WorkflowPick {
  return { kind: "listed", name: text(row?.name), revision: text(row?.revision), libraryRef: text(library?.reference), sequence: Number.isSafeInteger(row?.sequence) ? row.sequence : undefined,
    label: text(row?.label), title: text(row?.name), from: `${text(library?.origin) || "opened"} workflow library`, scope: pickScope(host) };
}
/** Whether a card is the picked workflow. */
export const isIncludedPick = (pick: WorkflowPick | null | undefined, entry: Json) => !!pick && pick.kind === "included" && pick.name === entry?.name && pick.revision === entry?.revision;
export const isListedPick = (pick: WorkflowPick | null | undefined, row: Json, library: Json) => !!pick && pick.kind === "listed" && pick.libraryRef === library?.reference && pick.name === row?.name && pick.revision === row?.revision;

/** Why the picked workflow cannot be used now, in the card's words, from what the catalogue or the library listing says
 * before any selection; null when nothing there stops it. */
export function pickLimit(pick: WorkflowPick, host: Json): string | null {
  const root = host?.workflowRoot;
  if (pick.kind === "included") {
    const catalog = root?.productionCatalog;
    const entry = list(catalog?.entries).find((row: Json) => row?.name === pick.name);
    if (!entry || entry.revision !== pick.revision) return "It is no longer listed among the included workflows as it was when you picked it. Pick it again under Workflows.";
    if (entry.runnable === false) return `Can't be used in this App: ${text(entry.runLimit) || text(catalog?.standing) || "the App reports it as not runnable"}.`;
    if (entry.runnable !== true) return "The App hasn't reported whether this workflow can be used here.";
    return null;
  }
  const library = list(root?.libraries).find((row: Json) => row?.reference === pick.libraryRef);
  const row = list(library?.registered).find((entry: Json) => entry?.name === pick.name && entry?.revision === pick.revision);
  if (!library || root?.activeLibrary !== pick.libraryRef || !row) return "It is no longer listed in the opened workflow library. Pick it again under Workflows.";
  if (row.selectable !== true) return `${text(row.label) || "It can't be chosen now"}.`;
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

/**
 * What the Run guide holds about a conversation's runs that decides whether a run may start there (RunWorkflowGuide:
 * runs of the exact current generation, home and thread; the latest by preparationOrder; a start whose outcome is
 * unknown; a run open or sent and not yet confirmed).
 */
export function conversationRuns(host: Json, thread: string) {
  const runs = list(host?.workflowRoot?.runs).filter((run: Json) => run.conversation === thread && run.home === host?.generation?.home && same(run.generation, host?.generation));
  const order = orderRuns(runs);
  const latest = order.unordered.length === 0 ? order.ordered[0] : runs.length === 1 ? runs[0] : undefined;
  const unresolved = (latest ? [latest] : runs).filter((run: Json) => starts(run.lifecycle?.state, "start not confirmed") && !startRefused(run));
  const inProgress = (latest ? [latest] : runs).some((run: Json) => starts(run.lifecycle?.state, "open") || (!!run.source && starts(run.lifecycle?.state, "prepared")));
  return { latest, unresolvedStart: unresolved.length > 0, holdKey: unresolved.map((run: Json) => text(run.reference)).join("\n"), inProgress };
}

/** The declared part of a selection as the Run guide reads it. */
const declarationOf = (selection: Json) => selection?.compatibility?.preparation?.declaration ?? selection?.declaration;

/** The required-tool check in one short line: what is available and what is missing, by name (DEL-02-03 REQ-001). */
export function toolsLine(selection: Json): { words: string; missing: string[] } {
  const preparation = selection?.compatibility?.preparation;
  const declaration = declarationOf(selection);
  const category = declaration?.categories?.required_tools;
  if (!declaration || declaration.reading === "undeclared" || category === "undeclared" || category === undefined && declaration.reading === "recognized")
    return { words: "Required tools: not declared, so the App can't check them.", missing: [] };
  if (declaration.reading !== "recognized" || category !== "recognized" && category !== "declared_empty") return { words: "Required tools: the App couldn't read them.", missing: [] };
  if (category === "declared_empty") return { words: "Required tools: it declares none.", missing: [] };
  const rows = list(preparation?.requirements);
  const required = list(declaration?.elements?.required_tools).map((element: Json, index: number) => ({ tool: element?.value ?? {}, row: preparation ? rows[index] : undefined }))
    .filter(t => t.tool.necessity !== "optional").map(t => ({ name: text(t.tool.name) || "Unnamed tool", state: toolReading(t.tool, t.row).state }));
  if (!preparation) return { words: "Required tools: not checked for this conversation.", missing: [] };
  const available = required.filter(t => t.state === "available").length, unknown = required.filter(t => t.state === "unknown").length;
  const missing = required.filter(t => t.state === "missing").map(t => t.name);
  if (!required.length) return { words: "Required tools: none required.", missing: [] };
  if (!missing.length && !unknown) return { words: `Required tools: ${available === 1 ? "the one it needs is" : `all ${available} are`} available.`, missing: [] };
  const parts = [`${available} available`, ...(unknown ? [`${unknown} couldn't be checked`] : [])];
  return { words: `Required tools: ${parts.join("; ")}${missing.length ? "; missing:" : "."}`, missing };
}

// ---- The press: the steps, in the Run guide's order, through its commands ----

/** What a start of a new conversation came to (App.tsx StartOutcome). */
type StartOutcome = { opened: string } | { failed: string } | { notConfirmed: true };
export type PickRun = {
  pick: WorkflowPick;
  text: string;
  /** The conversation shown, or null in a new chat (steps 1 and 2 run first). */
  thread: string | null;
  /** The view the person pressed on. */
  host: Json;
  /** Step 1: the new chat's present start (App.tsx startConversation). */
  start: () => Promise<StartOutcome | null>;
  /** A host command; rejects with the host's message. */
  act: (command: string, args: Record<string, unknown>) => Promise<Json>;
  /** A read of host_status, applied to the view; rejects when it fails. */
  read: () => Promise<Json>;
  /** Says which step is under way. */
  step: (words: string) => void;
  /** Runs this composer prepared and has not sent, by conversation, with the text each was prepared with. */
  prepared: Map<string, { reference: string; text: string }>;
  /** Runs this composer asked the host to send: never asked again. */
  attempted: Set<string>;
  /** The runs whose start of unknown outcome the person said they read (the guide's acknowledgement), or null. */
  acknowledged: string | null;
  /** Between host_status reads (step 2). */
  pause?: (ms: number) => Promise<void>;
};
export type PickRunOutcome =
  | { state: "started" }
  | { state: "nothing" }
  /** Stopped after the workflow was chosen, to show what it needs before anything is sent; Start run goes on from step 5. */
  | { state: "review"; opened?: string }
  | { state: "stopped"; words: string; opened?: string };

/** The step words shown while the press runs. */
export const PICK_STEPS = { start: "Starting the conversation…", choose: "Choosing the workflow…", prepare: "Preparing the run…", send: "Starting the run…" } as const;
const NOTHING_SENT = "Nothing was sent.";
/** The host's refusals a person can meet here before anything was done, in short words (the guide's REFUSAL_WORDS
 * name the same exact replies); any other reply is shown as the host gave it. */
const REASON_WORDS: Record<string, string> = {
  "Native history context is busy; refresh the workflow choice": "the App was busy reading conversation history",
  "Workflow App home source changed; refresh the displayed choice": "the App's view was out of date",
  "Workflow native generation changed; refresh the displayed choice": "the App's view was out of date",
  "Native history selection changed; refresh the displayed workflow choice": "the App's view was out of date",
  "The displayed workflow choice changed; refresh before selecting, inspecting or preparing": "the App's view was out of date",
  "Workflow source or chat changed; refresh the displayed choice before acting": "the conversation is no longer current in this view",
};
export function reasonWords(error: unknown): string {
  const reply = hostMessage(error).replace(/^Error: /, "").trim();
  return (Object.hasOwn(REASON_WORDS, reply) ? REASON_WORDS[reply] : reply || "the App gave no reason").replace(/[.\s]+$/, "");
}
/** Codex or the workflow source changed under the press: the steps stop where they are. */
const CHANGED = "Codex or the workflow source changed, so the App stopped";

/**
 * One press: (1) start the conversation and (2) read the status until its row appears, in a new chat; (3) choose the
 * workflow for it unless it already is, and (4) read the status for the selection; (5) prepare the run with the
 * person's text and (6) send it. A step whose outcome the App holds is not repeated: a press after a failure goes on
 * from the first step not done, and a run this composer asked the host to send is never asked again.
 */
export async function runPickedWorkflow(run: PickRun): Promise<PickRunOutcome> {
  const { pick, text: personText } = run;
  let host = run.host, thread = run.thread;
  const scope = pick.scope;
  if (pickScope(host) !== scope) return { state: "stopped", words: `${CHANGED}. Pick the workflow again. ${NOTHING_SENT}` };
  let opened: string | undefined;
  const stop = (words: string): PickRunOutcome => ({ state: "stopped", words, ...(opened ? { opened } : {}) });
  const changed = () => stop(opened ? `The conversation started, but ${CHANGED} there. ${NOTHING_SENT}` : `${CHANGED}. ${NOTHING_SENT}`);
  if (!thread) {
    run.step(PICK_STEPS.start);
    const outcome = await run.start();
    if (!outcome) return { state: "nothing" };
    if ("failed" in outcome) return stop(`Couldn't start the conversation: ${reasonWords(outcome.failed)}. ${NOTHING_SENT}`);
    let key: Json = null;
    if ("opened" in outcome) { try { key = JSON.parse(outcome.opened); } catch { key = null; } }
    if (!Array.isArray(key) || typeof key[1] !== "string") return stop("The App couldn't confirm the conversation started; it may exist. The workflow wasn't sent.");
    opened = (outcome as { opened: string }).opened;
    thread = key[1];
    // Step 2: the new conversation's row, which the selection's context names.
    let seen: Json = null;
    for (let attempt = 0; attempt < 4 && !seen; attempt++) {
      if (attempt) await (run.pause ?? (ms => new Promise<void>(resolve => setTimeout(resolve, ms))))(250);
      try { host = await run.read(); } catch { host = null; }
      seen = list(host?.threads).find((row: Json) => row.threadId === thread && same(row.generation, host?.generation));
    }
    if (!seen) return stop(`The conversation started, but the App couldn't read it back, so the workflow wasn't chosen. ${NOTHING_SENT}`);
    if (pickScope(host) !== scope) return changed();
  }
  const conversation = thread as string;
  if (run.thread) {
    // An open conversation: its runs as the host holds them now, not as the view last drew them, under the guide's two
    // conditions (no run of it still open or sent and unconfirmed; a start of unknown outcome only once acknowledged).
    try { host = await run.read(); } catch { return stop(`The App couldn't read its state, so it didn't start the run. ${NOTHING_SENT}`); }
    if (pickScope(host) !== scope) return changed();
    const runs = conversationRuns(host, conversation);
    if (runs.inProgress) return stop(`A workflow run is still open in this conversation. End it under Run a workflow before starting another. ${NOTHING_SENT}`);
    if (runs.unresolvedStart && run.acknowledged !== runs.holdKey) return stop(`Read the conversation: a start here has an unknown outcome and may have run. ${NOTHING_SENT}`);
  }
  const name = pick.title;
  // Steps 3 and 4: the selection, unless the conversation already has exactly this workflow chosen.
  let selection = pickedSelection(host, conversation, pick);
  let chose = false;
  if (!selection) {
    const notChosen = (reason: string) => stop(opened ? `The conversation started, but the workflow wasn't chosen: ${reason}. ${NOTHING_SENT}` : `The workflow wasn't chosen for this conversation: ${reason}. ${NOTHING_SENT}`);
    const [command, args]: [string, Record<string, unknown>] = pick.kind === "included" ? ["workflow_select_production_bundle", { name: pick.name }]
      : ["workflow_select_listed", { libraryRef: pick.libraryRef, name: pick.name, revision: pick.revision }];
    let request: Record<string, unknown>;
    try { request = workflowArguments(command, args, host?.workflowRoot, host, conversation); } catch (error) { return notChosen(reasonWords(error)); }
    run.step(PICK_STEPS.choose);
    let refused: unknown = null;
    try { await run.act(command, request); } catch (error) { refused = error ?? "the App gave no reason"; }
    chose = true;
    try { host = await run.read(); } catch { return stop(`${opened ? "The conversation started, but the" : "The"} App couldn't read whether the workflow was chosen. ${NOTHING_SENT}`); }
    if (pickScope(host) !== scope) return changed();
    selection = pickedSelection(host, conversation, pick);
    if (refused !== null && !selection) return notChosen(reasonWords(refused));
    if (!selection) return notChosen("the App doesn't show it chosen for the conversation");
  }
  // The guide's condition to prepare: the selection runnable and with no current limit, in the host's words.
  const limit = selection.runnable === true ? selection.currentLimit : selection.runLimit;
  if (selection.runnable !== true || selection.currentLimit) return stop(`${name} can't run: ${text(limit) || "the App reports it as not runnable"}. ${NOTHING_SENT}`);
  // Release target criterion 1: before the run the App says which declared required tools are available and which are
  // missing. The check is the host's, for this conversation, and exists only once the workflow is chosen for it.
  if (chose) return { state: "review", ...(opened ? { opened } : {}) };
  // Step 5: prepare, unless this composer prepared a run here with this same text that is still prepared and unsent.
  const kept = run.prepared.get(conversation);
  const keptRun = kept && kept.text === personText && !run.attempted.has(kept.reference)
    ? list(host?.workflowRoot?.runs).find((row: Json) => row.reference === kept.reference && !row.source && starts(row.lifecycle?.state, "prepared") && !(row.status?.sent === false && row.status?.limit)) : undefined;
  let reference: string = keptRun ? kept!.reference : "";
  if (!keptRun) {
    run.prepared.delete(conversation);
    const notPrepared = (reason: string) => stop(`${opened ? "The conversation started and the workflow was chosen, but the" : "The"} run wasn't prepared: ${reason}. ${NOTHING_SENT}`);
    let request: Record<string, unknown>;
    try { request = workflowArguments("workflow_prepare_run", { generation: host.generation, threadId: conversation, personText }, host?.workflowRoot, host, conversation); }
    catch (error) { return notPrepared(reasonWords(error)); }
    run.step(PICK_STEPS.prepare);
    try { reference = text((await run.act("workflow_prepare_run", request))?.reference); } catch (error) { return notPrepared(reasonWords(error)); }
    if (!reference) return notPrepared("the App didn't report the prepared run");
    run.prepared.set(conversation, { reference, text: personText });
    try { host = await run.read(); } catch { return stop(`The run was prepared, but the App couldn't read its state afterwards, so it wasn't started. ${NOTHING_SENT}`); }
    if (pickScope(host) !== scope) return changed();
  }
  const prepared = list(host?.workflowRoot?.runs).find((row: Json) => row.reference === reference);
  if (!prepared) return stop(`The run was prepared, but the App can't see it now, so it wasn't started. ${NOTHING_SENT}`);
  // The guide's Start is not offered for a prepared run whose records the App may not save.
  if (prepared.publication?.admissionRefusal) return stop(`The run was prepared, but its records can't be saved: ${reasonWords(prepared.publication.admissionRefusal)}. It wasn't started. ${NOTHING_SENT}`);
  // Step 6: send, once.
  if (run.attempted.has(reference)) return stop(`This run was already sent once, so the App won't send it again. Read the conversation.`);
  run.step(PICK_STEPS.send);
  run.attempted.add(reference);
  run.prepared.delete(conversation);
  let sendError: unknown = null;
  try { await run.act("workflow_send_run", { runRef: reference }); } catch (error) { sendError = error ?? "the App gave no reason"; }
  let after: Json = null;
  try { after = await run.read(); } catch { after = null; }
  const sent = list(after?.workflowRoot?.runs).find((row: Json) => row.reference === reference);
  if (!sent) {
    // What happened is not read: the present result of the press, and no second send.
    const said = guideResultWords({ command: "workflow_send_run", message: sendError === null ? "" : hostMessage(sendError), failed: sendError !== null, settled: true }, false);
    return stop(`${said?.words ?? "Start requested."} The App couldn't read the run's state afterwards and won't send it again; read the conversation.`);
  }
  const reading = runReading(sent, after);
  if (reading.tone === "failed" || reading.tone === "uncertain") return stop(`${reading.title}. ${reading.detail}`);
  if (sent.source || starts(sent.lifecycle?.state, "open")) return { state: "started" };
  // Still prepared and not sent: the host refused before sending. It may be started again.
  run.attempted.delete(reference);
  run.prepared.set(conversation, { reference, text: personText });
  return stop(`The run wasn't started: ${sendError === null ? "the App didn't report why" : reasonWords(sendError)}. ${NOTHING_SENT}`);
}

// ---- What the person sees beside the chip ----

/** The chip, and beside it what the App holds about the picked workflow for the conversation the press would use. */
export function PickChip({ pick, host, thread, disabled, remove }: { pick: WorkflowPick; host: Json; thread: string; disabled: boolean; remove: () => void }) {
  const root = host?.workflowRoot;
  const selection = thread ? pickedSelection(host, thread, pick) : undefined;
  const revision = pick.kind === "listed" && pick.sequence !== undefined ? `revision ${pick.sequence}` : null;
  const entry = pick.kind === "included" ? list(root?.productionCatalog?.entries).find((row: Json) => row?.name === pick.name && row?.revision === pick.revision) : undefined;
  const tools = selection ? toolsLine(selection) : null;
  const declaration = selection ? declarationOf(selection) : undefined;
  const inputs = declaredRows(declaration, "expected_inputs");
  const conversation = list(host?.threads).find((row: Json) => row.threadId === thread && same(row.generation, host?.generation));
  const newer = selection?.newerRevision;
  return <div className="v4-pick" aria-label="Workflow for this message">
    <ul className="method-chip-list" aria-label="Workflow picked">
      {/* The chip names the workflow and its source (and a registered revision's number); the revision digest is
          whole under Details. */}
      <li className="method-chip"><span>{pick.title}</span><small>{pick.from}{revision ? ` · ${revision}` : null}</small>
        <button type="button" aria-label={`Remove ${safeName(pick.name)}`} title="Remove" disabled={disabled} onClick={remove}>×</button></li>
    </ul>
    {tools ? <p className="v4-pick-note">{tools.words}{tools.missing.map((tool, index) => <span key={index}>{index ? "," : ""} <strong>{tool}</strong></span>)}{tools.missing.length ? "." : ""}
      {inputs.length > 0 && <> It asks for: {inputs.map((input: Json, index: number) => <span key={index}>{index ? ", " : ""}<strong>{text(input.name)}</strong>{input.necessity === "optional" ? " (optional)" : ""}</span>)}.</>}</p>
      : <p className="v4-pick-note">Press Start run to see the tools it needs. Nothing is sent until you press again.</p>}
    <details className="v4-pick-details"><summary>Details</summary>
      {inputs.length > 0 && <ul aria-label="What this workflow needs">{inputs.map((input: Json, index: number) => <li key={index}>
        <strong>{text(input.name)}</strong> ({input.necessity === "optional" ? "optional" : "required"}; {INPUT_KIND[text(input.kind)] ?? text(input.kind)}): {text(input.meaning)}{input.absence_effect ? ` If you leave it out: ${text(input.absence_effect)}` : ""}</li>)}</ul>}
      {selection && !inputs.length && <p>This workflow doesn't list required inputs. Describe what it should work on.</p>}
      {selection && <RequirementCheck selection={selection}/>}
      {selection && <RoleBesideWorkflow entry={includedEntryOf(root?.productionCatalog, selection)} conversation={conversation}/>}
      {selection && selection.identity?.origin !== "bundled" && <p role="note" aria-label="Approval evidence">{workflowAssurance(selection.assurance)}</p>}
      {!selection && pick.kind === "listed" && pick.label && <p>{pick.label}.</p>}
      {selection && newer && !newer.limit && <p role="note">A newer revision of <strong>{text(selection.identity?.name)}</strong> is registered ({text(newer.notice)}). This conversation keeps using the one shown above until you choose the newer one.</p>}
      {entry && <LibraryPathsBesideWorkflow entry={entry} source={root?.productionCatalog?.source}/>}
      <p>Revision <code>{pick.revision}</code></p>
    </details>
  </div>;
}
