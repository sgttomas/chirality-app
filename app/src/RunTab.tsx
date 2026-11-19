import { idWords } from "./AgentText";
import { revealWorkspaceTarget } from "./DailyWorkspace";
import { includedEntryOf, librarySourceWords } from "./IncludedWorkflows";
import { GuideResult, RunResult, VIEW_NOT_REFRESHED, conversationRun, orderRuns, runEvidenceAnchor, runReading, runTurnNotices, turnStatusWords,
  type GuideOutcome, type RunWordAction } from "./RunJourney";
import { appProjectFolder } from "./WorkflowContext";
import { chatWorkflow } from "./workflowSelection";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
type Act = (command: string, args: Record<string, unknown>) => Promise<Json>;
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);
const starts = (value: Json, prefix: string) => typeof value === "string" && value.startsWith(prefix);
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

/** The one command the tab issues: the end of a run as the former Run a workflow guide issued it, through the same `act`. */
export const RUN_TAB_COMMANDS = ["workflow_end_run"];
/** The tab's empty states. */
export const NO_CONVERSATION = "Open or start a conversation to see its run.";
export const NO_RUN = "No workflow run in this conversation.";
/** A workflow chosen for the conversation and no run of it: the conversation's own words (App.tsx), after the name. */
export const CHOSEN_NO_RUN = " is chosen for this conversation. No run has been started.";

/** Where a run's workflow comes from, in the guide's words: an included workflow by its whole identity as the run's
 * text records it, else a bundled copy, else the library it came from. */
export function runSourceWords(run: Json, catalog: Json): string {
  const identity = run?.runText?.workflow;
  const from = librarySourceWords(catalog?.source);
  if (identity && includedEntryOf(catalog, { identity })) return `Included with the App${from ? `, from ${from}` : ""}`;
  const origin = text(run?.workflow?.origin);
  if (origin === "bundled") return "A bundled copy";
  return origin ? `${origin.charAt(0).toUpperCase()}${origin.slice(1)} library` : "Where it comes from is not recorded";
}

/** A file change Codex reported as completed in this conversation (the host's native view of this Codex session). */
type ReportedFile = { path: string; kind: string };
const CHANGE_WORDS: Record<string, string> = { add: "new file", delete: "deleted", update: "changed" };
/**
 * The files Codex reported changing in a conversation: each completed `fileChange` item's paths, from the native view
 * of the current Codex session, the last report of each path kept. A declined, failed or unfinished change is not a
 * change, and a command or tool that wrote a file reports none, so this is never every file changed.
 */
export function reportedFiles(host: Json, conversation: string): ReportedFile[] {
  const view = host?.nativeView;
  if (!conversation || !view || !same(view.generation, host?.generation)) return [];
  const byPath = new Map<string, ReportedFile>();
  const rows = list(view.items).filter((row: Json) => row?.threadId === conversation && row?.native?.type === "fileChange" && row?.displayState === "completed")
    .sort((a: Json, b: Json) => (a?.observedOrder ?? 0) - (b?.observedOrder ?? 0));
  for (const row of rows) for (const change of list(row.native.changes)) {
    const path = typeof change?.kind?.move_path === "string" && change.kind.move_path ? change.kind.move_path : change?.path;
    if (typeof path !== "string" || !path) continue;
    const kind = change?.kind?.move_path ? "moved" : CHANGE_WORDS[text(change?.kind?.type)] ?? "changed";
    // A file the agent added and then changed is still one it reported adding.
    const earlier = byPath.get(path)?.kind;
    byPath.delete(path);
    byPath.set(path, { path, kind: earlier === "new file" && kind === "changed" ? earlier : kind });
  }
  return [...byPath.values()];
}
/** A reported path's name and its folder, the folder relative to the project folder where it is inside it. */
function pathParts(path: string, project: string | null): { name: string; folder: string } {
  const inside = project && path.startsWith(`${project.replace(/\/$/, "")}/`) ? path.slice(project.replace(/\/$/, "").length + 1) : path;
  const at = inside.lastIndexOf("/");
  return at < 0 ? { name: inside, folder: "" } : { name: inside.slice(at + 1), folder: inside.slice(0, at + 1) };
}

function declaredOutputs(run: Json, chosen: Json): Json[] {
  const declaration = list(run?.compatibility).find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration
    // The chosen workflow's declaration speaks for the run only where it is the run's own workflow and revision.
    ?? (chosen && chosen.identity?.name === run?.workflow?.name && chosen.identity?.revision === run?.workflow?.revision ? chosen.declaration : undefined);
  return list(declaration?.elements?.returned_outputs).map((element: Json) => element?.value ?? {});
}

/**
 * The right panel's Run tab: the run of the conversation open in the centre, and nothing more. Its state in a word
 * (runWord, over runReading's conditions), the next action, its results, what workflow it is, and the present detail
 * behind one disclosure. Its acts are the Run guide's workflow_end_run under the guide's conditions.
 */
export function RunTab({ data, host, thread, act, busy, outcome, showConversation, viewStale = false, readFailure = null }: {
  data: Json; host: Json; thread: string; act: Act; busy: boolean; outcome?: GuideOutcome | null; viewStale?: boolean; readFailure?: string | null;
  showConversation?: (threadId: string, target?: string) => void;
}) {
  if (!thread) return <section className="v4-runview run-tab" aria-label="Run"><p className="run-tab-empty">{NO_CONVERSATION}</p></section>;
  if (viewStale && !busy) return <section className="v4-runview run-tab" aria-label="Run">
    <p className="run-tab-empty" role="status">{VIEW_NOT_REFRESHED}</p>
    {readFailure && <p role="alert">The last read failed: {readFailure}</p>}
    <GuideResult label="Run — last result" outcome={outcome} only={RUN_TAB_COMMANDS} stepsShown={false}/>
  </section>;

  const { runs, latest, orderUnknown, finishedOffer, word } = conversationRun(data, host, thread);
  const failure = readFailure && <p role="alert" aria-label="Last status read failed">The App's last read of its state failed ({readFailure}). What is shown here was read before that.</p>;
  if (!word) {
    // As the conversation says it: a workflow chosen for it, and no run of this conversation recorded at all.
    const held = chatWorkflow(data, data?.context?.sourceRef, thread);
    const chosenName = held && held.state !== "not-selected" && typeof held.identity?.name === "string" && held.identity.name
      && !list(data?.runs).some((run: Json) => run.conversation === thread) ? held.identity.name : null;
    return <section className="v4-runview run-tab" aria-label="Run">
      {failure}
      {chosenName ? <p className="run-tab-chosen" role="note" aria-label="Workflow chosen, not started"><strong>{chosenName}</strong>{CHOSEN_NO_RUN}</p>
        : <><p className="run-tab-empty">{NO_RUN}</p>
          <p><button type="button" className="v4-plain run-tab-choose" onClick={() => revealWorkspaceTarget("view-library", true)}>Choose a workflow</button></p></>}
    </section>;
  }

  // As the guide: never while busy, never while the shown workflow source or Codex session differs from the host's.
  const sourceCurrent = !!data?.context?.sourceRef && host?.workflowRoot?.context?.sourceRef === data.context.sourceRef && same(data.context.generation, host?.generation);
  const canAct = !busy && sourceCurrent;
  const end = (finishedReport: Json) => { if (canAct && latest) void act("workflow_end_run", { runRef: latest.reference, finishedReport }); };
  const reading = latest ? runReading(latest, host) : null;
  const turnNotices = latest ? runTurnNotices(latest, host) : [];
  const catalog = data?.productionCatalog;
  const selection = chatWorkflow(data, data?.context?.sourceRef, thread);
  const chosen = selection && selection.state !== "not-selected" ? selection : null;
  const outputs = latest ? declaredOutputs(latest, chosen) : [];
  const projectFolder = appProjectFolder(host);
  const files = latest ? reportedFiles(host, thread) : [];
  const name = latest ? text(latest.workflow?.name) || "Workflow run" : "Workflow runs";
  const source = latest ? runSourceWords(latest, catalog) : "";
  const open = !!latest && starts(latest.lifecycle?.state, "open");
  const go = (target: string) => showConversation?.(thread, target);
  const control = (action: RunWordAction) => {
    if (action === "end") return <button key={action} type="button" className="v4-plain" disabled={!canAct} onClick={() => end(null)}>End run</button>;
    if (action === "end-completed") return <button key={action} type="button" className="v4-primary" disabled={!canAct} onClick={() => end(finishedOffer?.message)}>End run as completed</button>;
    if (!showConversation) return <a key={action} href="#conversation">Go to the conversation</a>;
    if (action === "answer") return <button key={action} type="button" className="v4-primary" onClick={() => go("conversation-requests")}>Answer in the conversation</button>;
    if (action === "reply") return <button key={action} type="button" className="v4-primary" onClick={() => go("conversation")}>Reply</button>;
    return <button key={action} type="button" className="v4-plain" onClick={() => go("conversation")}>Show the conversation</button>;
  };
  // Runs of this conversation other than the one read above, in the guide's Results wording (a prepared, unsent one is not a run yet).
  const sent = (run: Json) => !(starts(run?.lifecycle?.state, "prepared") && !run.source);
  const others = orderRuns(runs.filter(run => run !== latest && sent(run)));

  return <section className="v4-runview run-tab" aria-label="Run" aria-busy={busy}>
    <div className="v4-runview-head">
      <p className="v4-runview-title">{name}</p>
      {source && <p className="v4-runview-on">{source}</p>}
    </div>
    <div className={`v4-next v4-next--${word.mark}`} aria-label="Run state">
      <div role="status" aria-live="polite">
        <span className="v4-next-state"><span className={`v4-dot v4-dot--${word.mark}`} aria-hidden="true"/>{word.word}</span>
        {finishedOffer && <p className="run-tab-said" aria-label="Agent finished report">The agent wrote <q>{text(finishedOffer.finished?.statement)}</q></p>}
        <p>{word.sentence}</p>
        {finishedOffer && word.word !== "Agent says finished" && <p>That is the agent's word. Ending the run is yours.</p>}
      </div>
      {word.actions.length > 0 && <div className="v4-next-actions">{word.actions.map(control)}</div>}
    </div>
    {/* Held notices, each with its turn, in the guide's words: outside the state above, since they are not a reading of the run. */}
    {turnNotices.length > 0 && <div className="run-tab-notices" role="note" aria-label="Error notices the App holds for this conversation">
      {turnNotices.map(notice => <p key={notice.turnId}>The App holds an error notice from Codex for turn <code>{notice.turnId}</code> of this conversation{notice.count > 1 ? `; it is the latest of ${notice.count} for that turn` : ""}: <q>{notice.words}</q> {notice.retry}{notice.turnStatus !== null ? ` ${turnStatusWords(notice.turnStatus)}` : ""}</p>)}
      <p>The conversation's activity shows each notice the App has kept, with its turn.</p>
    </div>}
    {!busy && <GuideResult label="Run — last result" outcome={outcome} only={RUN_TAB_COMMANDS} stepsShown={false}/>}
    {failure}
    {latest && <div className="run-tab-results">
      <h3>Results</h3>
      {outputs.length > 0 ? <ul className="run-tab-declared" aria-label="What the workflow declares it produces">{outputs.map((output: Json, index: number) =>
        <li key={index}><strong>{text(output.name)}</strong>{output.path ? <> <code>{text(output.path)}</code></> : null}</li>)}</ul> : null}
      <p className="v4-unchecked">{outputs.length > 0 ? "Declared by the workflow; the App hasn't checked that any exist." : "This workflow doesn't declare what it produces."} The agent reports its results in the conversation.</p>
      {files.length > 0 && <div className="run-tab-files" aria-label="Files the agent reported changing">
        <p className="run-tab-count">{files.length === 1 ? "1 file" : `${files.length} files`} changed in this conversation</p>
        <ul>{files.map(file => { const parts = pathParts(file.path, projectFolder); return <li key={file.path} className="v4-file">
          <span className="v4-file-glyph" aria-hidden="true"/><span className="v4-file-name"><b>{parts.name}</b><span>{parts.folder ? `${parts.folder} · ` : ""}{file.kind}</span></span></li>; })}</ul>
        <p className="v4-unchecked">Reported by the agent. The App hasn't checked it.</p>
      </div>}
    </div>}
    {latest && <dl className="v4-facts">
      <dt>Workflow</dt><dd>{name}{latest.workflow?.revision ? <> <small>· revision <code title={idWords(latest.workflow.revision)}>{text(latest.workflow.revision).slice(0, 12)}…</code></small></> : null}</dd>
    </dl>}
    <details className="run-tab-details">
      <summary>Details</summary>
      {reading && <p aria-label="Run progress"><strong>{reading.title}.</strong> {reading.detail}</p>}
      {orderUnknown && <p>This conversation has several runs, and the App can't tell which one is the latest.</p>}
      {open && <p><small>Ending here records that you ended it — not that it completed. To stop only Codex's current step, use Stop in the conversation; the run stays open.</small></p>}
      {/* Each declared output with its meaning, in the guide's words (the list above gives the name and path only). */}
      {outputs.some((output: Json) => output.meaning) && <ul aria-label="Where the results go">{outputs.map((output: Json, index: number) => <li key={index}>
        <strong>{text(output.name)}</strong>{output.path ? <> — declared path <code>{text(output.path)}</code></> : ""}{output.meaning ? `: ${text(output.meaning)}` : ""}</li>)}</ul>}
      {latest && <p><small>These are what the workflow declares it produces; the App hasn't checked that any of them exist. {projectFolder !== null ? <>A relative declared path is the workflow's own wording; the App doesn't establish whether it is inside the project folder <code>{projectFolder}</code>.</> : "The App has not reported a matching project folder; the library location alone does not establish output locations."} The conversation's activity shows file changes reported by Codex; it does not establish every file changed by commands or tools.</small></p>}
      {(others.ordered.length + others.unordered.length) > 0 && <ul aria-label="Runs in this conversation">
        {others.ordered.map((run: Json) => <RunResult key={text(run.reference)} run={run} host={host} showConversation={showConversation}/>)}
        {others.unordered.length > 0 && <li><small>{others.ordered.length ? "These runs' order isn't known:" : others.unordered.length > 1 ? "The App doesn't know these runs' order:" : ""}</small></li>}
        {others.unordered.map((run: Json) => <RunResult key={text(run.reference)} run={run} host={host} showConversation={showConversation}/>)}
      </ul>}
      {latest && <p><a href={`#${runEvidenceAnchor(latest.reference)}`}>Open this run's recorded evidence (in the workflow studio, under More › Make a workflow)</a></p>}
    </details>
  </section>;
}
