import { conversationLabel, nativePathText } from "./presentation";
import { hostRequests, requestThread } from "./RequestCards";
import { chatWorkflow } from "./workflowSelection";
import { appProjectFolder } from "./WorkflowContext";
import { useState } from "react";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
type Act = (command: string, args: Record<string, unknown>) => Promise<Json>;
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);
const starts = (value: Json, prefix: string) => typeof value === "string" && value.startsWith(prefix);
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

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
    const waiting = hostRequests(host).filter((request: Json) => requestThread(request) === run.conversation && request.state === "outstanding").length;
    if (waiting > 0) return { tone: "waiting", title: "Waiting for your answer", detail: `Codex is asking ${waiting === 1 ? "a question or approval" : `${waiting} questions or approvals`} in the conversation. Nothing continues until you answer there.` };
    const thread = list(host?.threads).find((row: Json) => row.threadId === run.conversation && same(row.generation, host?.generation));
    if (thread?.status?.type === "active") return { tone: "working", title: "Working", detail: "Codex is working on this run. Follow its progress in the conversation." };
    if (thread?.status?.type === "systemError") return { tone: "failed", title: "Codex reported an error", detail: "The conversation reported a system error. The run is still open; read the conversation, then continue or end the run." };
    return { tone: "idle", title: "Open — Codex is not working right now", detail: "The run stays open until you end it. Reply in the conversation to continue, or end the run when you are done." };
  }
  if (run?.source) return { tone: "working", title: "Starting", detail: "The starting message was sent. The run opens when Codex begins it." };
  if (status.sent === false && status.limit) return { tone: "failed", title: "Not started", detail: `${text(status.state)}: ${text(status.limit)}` };
  return { tone: "idle", title: "Ready to start", detail: "The run is prepared and has not been sent. Start it when your inputs are ready." };
}

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
export function RunWorkflowGuide({ data, host, thread, chooseThread, act, busy, text: personText, setText, outcome, showConversation }: {
  data: Json; host: Json; thread: string; chooseThread: (thread: string) => void; act: Act; busy: boolean;
  text: string; setText: (text: string) => void; outcome?: { command: string; message: string } | null;
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
  const registered = list(active?.registered);
  const listing = active?.entryListing;
  const listed = listing?.state === "observed" && listing.libraryRef === active?.reference ? list(listing.entries) : [];
  const unregistered = listed.filter((entry: Json) => entry.reviewable === true && typeof entry.reference === "string");
  const selection = thread ? chatWorkflow(data, data?.context?.sourceRef, thread) : undefined;
  const chosen = selection && selection.state !== "not-selected" ? selection : null;
  const chosenSequence = chosen ? registered.find((row: Json) => row.name === chosen.identity?.name && row.revision === chosen.identity?.revision)?.sequence : undefined;
  const runs = list(data?.runs).filter((run: Json) => run.conversation === thread && run.home === host?.generation?.home);
  const latest = runs.at(-1);
  const prepared = latest && !latest.source && starts(latest?.lifecycle?.state, "prepared") ? latest : null;
  const reading = latest ? runReading(latest, host) : null;
  // An open run, or one sent and not yet opened, is ended or followed from the studio, not re-prepared here.
  const unresolvedStart = !!latest && starts(latest.lifecycle?.state, "start not confirmed") && !startRefused(latest);
  const finishedOffer = latest && starts(latest.lifecycle?.state, "open") ? list(data?.offers).find((offer: Json) => offer?.finished?.run === latest.reference) : undefined;
  const inProgress = !!latest && (starts(latest.lifecycle?.state, "open") || (!!latest.source && starts(latest.lifecycle?.state, "prepared")));
  const declaration = list(latest?.compatibility).find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration ?? chosen?.declaration;
  const inputs = declaredRows(declaration, "expected_inputs");
  const outputs = declaredRows(declaration, "returned_outputs");
  const pendingReview = list(data?.reviews).some((review: Json) => review.reference === data?.activeReview && review.status?.presentation);
  const bundled = list(data?.productionCatalog?.entries);
  const step = !ready ? "Connect Codex first: open Connection & access and start Codex."
    : !sourceCurrent ? "The workflow view is out of date. Wait for it to refresh, or reopen the App view."
    : !active ? projectAvailable ? "Show this project's workflows to begin." : "No project folder is set. Choose one in Desktop setup; it applies the next time you open the App."
    : !thread ? conversations.length ? "Choose the conversation that will run the workflow." : "Start a conversation first, then choose it here."
    : !chosen ? registered.some((row: Json) => row.selectable === true) || bundled.some((entry: Json) => entry.runnable === true) ? "Choose a workflow to use." : "No workflow here is ready to use yet. Review one below, or open another library in the workflow studio."
    : chosen.runnable !== true ? `${text(chosen.identity?.name)} can't run: ${text(chosen.runLimit)}`
    : unresolvedStart && checkedRun !== latest.reference ? "Read the conversation: the last start's outcome is unknown and it may have run."
    : !latest || starts(latest.lifecycle?.state, "ended") || starts(latest.lifecycle?.state, "start not confirmed") ? "Describe what the workflow should work on, then prepare the run."
    : prepared ? "Check your inputs, then start the run." : reading?.title ?? "";
  return <section id="run-workflow" className="workflow-stage run-journey" aria-label="Run a workflow" aria-busy={busy}>
    <h2>Run a workflow</h2>
    <p className="run-journey-next" role="status" aria-live="polite"><strong>Next:</strong> {step}</p>
    <ol className="run-journey-steps">
      <li><h3>Project</h3>
        <p>Project folder: {projectFolder !== null ? <code>{projectFolder}</code> : "not established for this App window."}</p>
        {active ? <p>Using the {text(active.origin) || "opened"} workflow library{libraryFolder ? <> in <code>{libraryFolder}</code></> : ""}.</p>
          : <p>{projectAvailable ? "This App has a project folder. Its workflows are kept in its .chirality folder." : "No project folder is set for this App yet."}</p>}
        {projectAvailable ? <button disabled={!canAct || !ready} onClick={() => perform("workflow_open_project_library", {})}>{active ? "Reload this project's workflows" : "Show this project's workflows"}</button>
          : <p><a href="#desktop-setup">Choose a project in Desktop setup</a> — the choice applies when you next open the App. Or open any workflow library from the workflow studio below.</p>}
      </li>
      <li><h3>Conversation</h3>
        {conversations.length ? <label>Conversation to run it in <select value={thread} disabled={!canAct} onChange={event => chooseThread(event.target.value)}>
          <option value="">Choose a conversation</option>
          {conversations.map((row: Json) => <option key={row.threadId} value={row.threadId}>{conversationLabel(host, row)}</option>)}
        </select></label> : <p>No conversation in this session yet. <a href="#workspace-start">Start a new conversation</a>, then choose it here.</p>}
        {thread && <details className="conversation-identity"><summary>Exact conversation ID</summary><code>{thread}</code></details>}
        <p><small>The workflow runs inside this conversation; you answer its questions there.</small></p>
      </li>
      <li><h3>Workflow</h3>
        {chosen && <p aria-label="Workflow chosen for this run"><strong>{text(chosen.identity?.name)}</strong> — {text(chosen.identity?.origin)} library, {chosenSequence !== undefined ? `revision ${text(chosenSequence)} ` : ""}<code title={text(chosen.identity?.revision)}>{text(chosen.identity?.revision).slice(0, 12)}…</code>. {chosen.runnable === true ? "Ready to run." : `Can't run: ${text(chosen.runLimit)}`}</p>}
        {active && registered.length > 0 && <ul aria-label="Workflows ready to use">{registered.map((row: Json) => <li key={`${row.name}@${row.revision}`}>
          <strong>{text(row.name)}</strong> · revision {text(row.sequence)}{chosen && chosen.identity?.name === row.name && chosen.identity?.revision === row.revision ? <> — chosen</> : row.selectable === true
            ? <> <button disabled={!canAct || !thread} onClick={() => perform("workflow_select_listed", { libraryRef: active.reference, name: row.name, revision: row.revision })}>Use {text(row.name)}</button></>
            : <> — {text(row.label)}</>}
        </li>)}</ul>}
        {active && !Array.isArray(active.registered) && active.registered?.limit && <p role="note">This library's list of approved workflows can't be read: {text(active.registered.limit)}</p>}
        {active && registered.length === 0 && Array.isArray(active.registered) && <p>No workflow in this library has been approved for use yet.</p>}
        {active && unregistered.length > 0 && <div aria-label="Workflows that need a first review">
          <p>These workflows are in the folder but haven't been approved for use here. Read one once and confirm it in the App's confirmation dialog; after that it is listed above. Nothing runs during the review.</p>
          <ul>{unregistered.map((entry: Json) => <li key={entry.reference}><strong>{text(entry.name)}</strong>{" "}
            <button disabled={!canAct} onClick={() => perform("workflow_review_library_entries", { libraryRef: active.reference, listingRef: listing.reference, entryRefs: [entry.reference] })}>Review {text(entry.name)} for first use…</button></li>)}</ul>
        </div>}
        {pendingReview && <p role="note">A review is open. <a href="#workflow-reviews">Read it and confirm</a> to approve the workflow for use.</p>}
        {active && <button disabled={!canAct} onClick={() => perform("workflow_library_entries_refresh", { libraryRef: active.reference })}>Look for other workflows in this library</button>}
        {bundled.map((entry: Json) => entry.runnable === true
          ? <p key={entry.name}>Included with the App: <strong>{text(entry.name)}</strong>{entry.revision ? <> (<code>{text(entry.revision).slice(0, 12)}…</code>)</> : ""}.{" "}
            <button disabled={!canAct || !thread} onClick={() => perform("workflow_select_production_bundle", { name: entry.name })}>Use {text(entry.name)} (included with the App)</button></p>
          : <div key={entry.name} role="note"><p>Included with the App: <strong>{text(entry.name)}</strong>. This build can't run it directly; you can inspect it in the workflow studio.</p>
            <details><summary>Why</summary><p>{text(entry.runLimit) || text(data?.productionCatalog?.standing) || "The App reports it as not runnable."}</p></details></div>)}
      </li>
      <li><h3>Inputs</h3>
        {inputs.length > 0 ? <ul aria-label="What this workflow needs">{inputs.map((input: Json, index: number) => <li key={index}>
          <strong>{text(input.name)}</strong> ({input.necessity === "optional" ? "optional" : "required"}; {INPUT_KIND[text(input.kind)] ?? text(input.kind)}): {text(input.meaning)}{input.absence_effect ? ` If you leave it out: ${text(input.absence_effect)}` : ""}</li>)}</ul>
          : chosen ? <p>This workflow doesn't list required inputs. Describe what it should work on.</p> : <p>Choose a workflow to see what it needs.</p>}
        <label>What should the workflow work on? <textarea value={personText} onChange={event => setText(event.target.value)} disabled={busy} rows={3}/></label>
        <p><small>Name any files in the project folder that it should use. This text goes with the workflow's own instructions in one starting message.</small></p>
      </li>
      <li><h3>Start</h3>
        {!prepared ? <>{unresolvedStart && <p><label><input type="checkbox" checked={checkedRun === latest.reference} disabled={!canAct} onChange={event => setCheckedRun(event.target.checked ? latest.reference : null)}/> I read the conversation and want to prepare a new run anyway</label>
            <small>The earlier start may have run; a new run sends the workflow again.</small></p>}
          <button className="setup-primary" disabled={!canAct || !ready || !thread || chosen?.runnable !== true || inProgress || (unresolvedStart && checkedRun !== latest.reference)}
          onClick={() => { if (!unresolvedStart || checkedRun === latest.reference) perform("workflow_prepare_run", { generation: host.generation, threadId: thread, personText }); }}>Prepare this run</button></>
          : <><p>Prepared {text(prepared.workflow?.name)} with your text. Nothing has been sent yet.</p>
            <button className="setup-primary" disabled={!canAct || !ready} onClick={() => perform("workflow_send_run", { runRef: prepared.reference })}>Start the run</button></>}
        <p><small>Preparing composes the starting message from the chosen revision; nothing is sent. Starting records the run and sends that message once — if recording fails, nothing is sent.</small></p>
      </li>
      <li><h3>Progress</h3>
        {reading ? <div className={`run-journey-state run-journey-${reading.tone}`} aria-label="Run progress">
          <p role="status"><strong>{reading.title}.</strong> {reading.detail}</p>
          {(starts(latest.lifecycle?.state, "open") || reading.tone === "uncertain") && <p>{showConversation
            ? <button onClick={() => showConversation(latest.conversation, reading.tone === "waiting" ? "conversation-requests" : "conversation")}>{reading.tone === "waiting" ? "Answer in the conversation" : "Show the conversation"}</button>
            : <a href="#conversation">Go to the conversation</a>}</p>}
          {finishedOffer && <p aria-label="Agent finished report"><strong>The agent wrote “{text(finishedOffer.finished.statement)}”.</strong> This is the agent's statement.{" "}
            <button disabled={!canAct} onClick={() => perform("workflow_end_run", { runRef: latest.reference, finishedReport: finishedOffer.message })}>End as completed, on the agent's report</button></p>}
          {starts(latest.lifecycle?.state, "open") && <p><button disabled={!canAct} onClick={() => perform("workflow_end_run", { runRef: latest.reference, finishedReport: null })}>End this run</button>{" "}
            <small>Ending here records that you ended it — not that it completed. To stop only Codex's current step, use Stop in the conversation; the run stays open.</small></p>}
        </div> : <p>No run in this conversation yet.</p>}
        {outcome?.message && <p role="status" aria-label="Run a workflow — last result">{outcome.message}</p>}
      </li>
      <li><h3>Results</h3>
        {outputs.length > 0 ? <ul aria-label="Where the results go">{outputs.map((output: Json, index: number) => <li key={index}>
          <strong>{text(output.name)}</strong>{output.path ? <> — declared path <code>{text(output.path)}</code></> : ""}{output.meaning ? `: ${text(output.meaning)}` : ""}</li>)}</ul>
          : <p>{chosen ? "This workflow doesn't declare where its results go; the agent reports them in the conversation." : "Choose a workflow to see what it produces."}</p>}
        <p><small>These are what the workflow declares it produces; the App hasn't checked that any of them exist. {projectFolder !== null ? <>A relative declared path is the workflow's own wording; the App doesn't establish whether it is inside the project folder <code>{projectFolder}</code>.</> : "The project folder is not established for this App window."} Files Codex actually changed are listed in the conversation's activity.</small></p>
      </li>
    </ol>
  </section>;
}
