import { choiceLabels, idWords, numberWords, safeName } from "./AgentText";
import { threadChoices } from "./presentation";
import { chatWorkflow, workflowAssurance, workflowContext } from "./workflowSelection";
import { WorkflowTextControl, useWorkflowTexts, type WorkflowTexts } from "./WorkflowText";
import { LibraryPathsBesideWorkflow, RoleBesideWorkflow, includedEntryOf, includedSections, librarySourceWords, matchesSearch } from "./IncludedWorkflows";
import { RequirementCheck } from "./RequirementCheck";
import { GuideResult, VIEW_NOT_REFRESHED, registeredRevisionAnchor, type GuideOutcome } from "./RunJourney";
import { useState } from "react";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
type Act = (command: string, args: Record<string, unknown>) => Promise<Json>;
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => (typeof value === "string" ? value : "");
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

/** The two commands the tab issues, both the Run guide's own, through the same `act`. */
export const LIBRARY_COMMANDS = ["workflow_select_production_bundle", "workflow_select_listed"];

/**
 * Why choosing is not possible now, in the Run guide's words for each condition, or null when it is. Choosing needs
 * what the guide's choose needs: no press in progress, the shown workflow source current, and a conversation chosen.
 */
export function chooseBlock({ busy, sourceCurrent, thread, conversations }: { busy: boolean; sourceCurrent: boolean; thread: string; conversations: number }): "busy" | "stale" | "no-conversation" | "no-conversations" | null {
  if (!sourceCurrent) return "stale";
  if (busy) return "busy";
  if (!thread) return conversations ? "no-conversation" : "no-conversations";
  return null;
}

/** The control that chooses a workflow: 3.0.1's toggle. The App has no command that clears a conversation's choice, so
 * a chosen card shows the pressed state and offers no Remove. */
function ChooseToggle({ chosen, disabled, choose }: { chosen: boolean; disabled: boolean; choose: () => void }) {
  if (chosen) return <button type="button" aria-pressed="true" disabled>Chosen</button>;
  return <button type="button" aria-pressed="false" disabled={disabled} onClick={choose}>Use in message</button>;
}

/** Inspect: the workflow's own text, read through the App's present read and shown in the card as that read shows it. */
function InspectToggle({ shown, disabled, read, hide }: { shown: boolean; disabled: boolean; read: () => void; hide: () => void }) {
  return <button type="button" aria-expanded={shown} disabled={disabled && !shown} onClick={shown ? hide : read}>Inspect</button>;
}

/**
 * The right panel's Workflows tab, in 3.0.1's form: a search, the workflows included with the App in the Library's
 * own groups, and this project's workflows, each a card with Inspect and the toggle that chooses it for the
 * conversation chosen under Run a workflow. It reads the same host state the Run guide reads, so the two agree on what
 * is chosen, and it issues only the guide's own choosing commands under the guide's conditions.
 */
export function WorkflowLibrary({ data, host, thread, act, busy, outcome, viewStale = false, readFailure = null }: {
  data: Json; host: Json; thread: string; act: Act; busy: boolean; outcome?: GuideOutcome | null; viewStale?: boolean; readFailure?: string | null;
}) {
  const [search, setSearch] = useState("");
  const texts = useWorkflowTexts();
  const sourceCurrent = !!data?.context?.sourceRef && host?.workflowRoot?.context?.sourceRef === data.context.sourceRef && same(data.context.generation, host?.generation);
  const conversations = list(host?.threads).filter((row: Json) => same(row.generation, host?.generation));
  const block = chooseBlock({ busy, sourceCurrent, thread, conversations: conversations.length });
  const canAct = !busy && sourceCurrent;
  const perform = (command: string, args: Record<string, unknown>) => { if (block === null) void act(command, args); };
  const catalog = data?.productionCatalog;
  const entries = list(catalog?.entries);
  const from = librarySourceWords(catalog?.source);
  const selection = thread ? chatWorkflow(data, data?.context?.sourceRef, thread) : undefined;
  const chosen = selection && selection.state !== "not-selected" ? selection : null;
  // As the Run guide's list: an included entry is chosen only when the selection is that entry by its whole identity
  // and the host admits it to run; a registered row when the selection has its name and revision.
  const chosenEntry = chosen?.runnable === true ? includedEntryOf(catalog, chosen) : undefined;
  const conversationAt = conversations.findIndex((row: Json) => row.threadId === thread);
  const conversationLabel = conversationAt >= 0 ? choiceLabels(threadChoices(conversations, (row: Json) => row.threadId))[conversationAt] : "";

  if (viewStale && !busy) return <section className="method-library" aria-label="Workflows">
    <p className="method-library-note" role="status">{VIEW_NOT_REFRESHED}</p>
    {readFailure && <p role="alert">The last read failed: {readFailure}</p>}
    <GuideResult label="Workflows — last result" outcome={outcome} only={LIBRARY_COMMANDS} stepsShown={false}/>
  </section>;

  const searching = search.trim() !== "";
  const found = entries.filter(entry => matchesSearch(entry, search));
  const sections = includedSections(found);
  const includedSlot = (entry: Json) => `library:included:${text(entry?.name)}`;
  const chosenSlot = `library:chosen:${text(data?.context?.sourceRef)}:${thread}`;
  const holds = (entry: Json) => texts.of(includedSlot(entry), entry?.identity) !== undefined;

  // This project: the opened library's registered workflows and the ones in its folder awaiting a first review.
  const libraries = list(data?.libraries);
  const active = libraries.find((library: Json) => library.reference === data?.activeLibrary);
  const projectAvailable = data?.projectLibraryAvailable === true;
  const registered = list(active?.registered);
  const listing = active?.entryListing;
  const listed = listing?.state === "observed" && listing.libraryRef === active?.reference ? list(listing.entries) : [];
  const unregistered = listed.filter((entry: Json) => entry.reviewable === true && typeof entry.reference === "string");
  const sameName = (name: Json) => registered.filter((row: Json) => row.name === name).length > 1;
  const wordsMatch = (name: Json) => matchesSearch({ name }, search);
  const shownRegistered = registered.filter((row: Json) => wordsMatch(row.name));
  const shownUnregistered = unregistered.filter((entry: Json) => wordsMatch(entry.name));
  const pendingReview = list(data?.reviews).some((review: Json) => review.reference === data?.activeReview && review.status?.presentation);
  const libraryWords = `${text(active?.origin) || "opened"} workflow library`;

  const chosenExtras = <>
    {chosen && <RoleBesideWorkflow entry={includedEntryOf(catalog, chosen)} conversation={conversations.find((row: Json) => row.threadId === thread)}/>}
    {chosen && chosen.identity?.origin !== "bundled" && <p role="note" aria-label="Approval evidence">{workflowAssurance(chosen.assurance)}</p>}
    {chosen && <RequirementCheck selection={chosen}/>}
  </>;
  const chosenLimit = chosen?.runnable === true ? chosen?.currentLimit : chosen?.runLimit;
  const newer = chosen?.newerRevision;

  const includedCard = (entry: Json) => {
    const name = text(entry?.name);
    const shownName = text(entry?.navigation?.displayName) || name;
    const isChosen = chosenEntry === entry;
    const textShown = holds(entry);
    const roles = list(entry?.roles).filter((role: Json) => typeof role === "string");
    const runnable = entry?.runnable === true;
    return <li key={name} className="method-card" aria-label={`Included workflow ${safeName(entry?.name)}`} data-chosen={isChosen ? "true" : undefined}>
      <div className="method-card-heading"><strong>{shownName}</strong>{shownName !== name && <code className="method-card-identifier" title="Workflow identifier">{name}</code>}</div>
      {entry?.description ? <p>{text(entry.description)}</p> : null}
      <p className="method-card-meta"><small>{from || "Included with the App"}</small></p>
      {entry?.runnable === false && <p className="method-card-limit" role="note">Can't be used in this App: {text(entry.runLimit) || text(catalog?.standing) || "the App reports it as not runnable"}.</p>}
      {entry?.runnable !== true && entry?.runnable !== false && <p className="method-card-limit" role="note">The App hasn't reported whether this workflow can be used here.</p>}
      <div className="method-card-actions">
        <InspectToggle shown={textShown} disabled={!canAct} hide={() => texts.hide(includedSlot(entry))}
          read={() => texts.read(includedSlot(entry), entry?.identity, { kind: "included", name: entry?.name, revision: entry?.identity?.revision }, workflowContext(data, host, ""))}/>
        <ChooseToggle chosen={isChosen} disabled={block !== null || !runnable} choose={() => perform("workflow_select_production_bundle", { name: entry.name })}/>
      </div>
      {textShown && <IncludedText entry={entry} slot={includedSlot(entry)} source={from} texts={texts} disabled={!canAct} data={data} host={host}/>}
      <details className="method-card-details"><summary>Details</summary>
        <p>Revision <code title={idWords(entry?.revision)}>{text(entry?.revision).slice(0, 12)}…</code></p>
        {roles.length > 0 && <p>The Library lists it for these roles: {roles.join(", ")}.</p>}
        {entry?.compatibility === "legacy" && <p>The Library marks it as legacy.</p>}
        {isChosen && chosenExtras}
        <LibraryPathsBesideWorkflow entry={entry} source={catalog?.source}/>
      </details>
    </li>;
  };

  const registeredCard = (row: Json) => {
    const isChosen = !!chosen && chosen.identity?.name === row.name && chosen.identity?.revision === row.revision;
    const name = text(row.name);
    return <li key={`${name}@${text(row.revision)}`} className="method-card" aria-label={`Project workflow ${safeName(row.name)}`} data-chosen={isChosen ? "true" : undefined}>
      <div className="method-card-heading"><strong>{name}</strong></div>
      <p className="method-card-meta"><small>{libraryWords} · revision {numberWords(row.sequence) ?? ""}{sameName(row.name) ? " · another revision has the same name" : ""}</small></p>
      {row.selectable !== true && <p className="method-card-limit" role="note">{text(row.label)}.{" "}
        <a href={`#${registeredRevisionAnchor(active.reference, row.name, row.revision)}`}>{row.reconfirm === true ? `Re-confirm ${safeName(row.name)} in the workflow studio` : "See this revision in the workflow studio"}</a></p>}
      <div className="method-card-actions">
        {isChosen && <InspectToggle shown={texts.of(chosenSlot, chosen.identity) !== undefined} disabled={!canAct} hide={() => texts.hide(chosenSlot)}
          read={() => texts.read(chosenSlot, chosen.identity, { kind: "selection", revision: chosen.identity?.revision }, workflowContext(data, host, thread))}/>}
        <ChooseToggle chosen={isChosen} disabled={block !== null || row.selectable !== true} choose={() => perform("workflow_select_listed", { libraryRef: active.reference, name: row.name, revision: row.revision })}/>
      </div>
      {isChosen && texts.of(chosenSlot, chosen.identity) !== undefined && <WorkflowTextControl slot={chosenSlot} identity={chosen.identity} source={libraryWords} texts={texts} disabled={!canAct}
        target={{ kind: "selection", revision: chosen.identity?.revision }} context={() => workflowContext(data, host, thread)}/>}
      <details className="method-card-details"><summary>Details</summary>
        <p>Revision {numberWords(row.sequence) ?? ""} <code title={idWords(row.revision)}>{text(row.revision).slice(0, 12)}…</code>{row.selectable === true ? <> · {text(row.label)}</> : null}</p>
        {row.reconfirm === true && <p>Refine it into a draft, then review that draft and confirm in the App's dialog. Nothing is chosen or run until you do.</p>}
        {isChosen && chosenExtras}
      </details>
    </li>;
  };

  const unregisteredCard = (entry: Json) => <li key={entry.reference} className="method-card" aria-label={`Project workflow ${safeName(entry.name)}`}>
    <div className="method-card-heading"><strong>{text(entry.name)}</strong></div>
    <p className="method-card-meta"><small>{libraryWords}</small></p>
    <p className="method-card-limit" role="note">In the folder but not yet approved for use here. <a href="#run-workflow">Review it under Run a workflow</a></p>
  </li>;

  const projectNote = !active
    ? projectAvailable
      ? <p className="method-library-note">This App has a project folder. Its workflows are kept in its .chirality folder. <a href="#run-workflow">Show them under Run a workflow</a></p>
      : <p className="method-library-note">No project folder is set for this App yet. <a href="#desktop-setup">Choose a project in Desktop setup</a> — the choice applies when you next open the App.</p>
    : registered.length === 0 && unregistered.length === 0 && Array.isArray(active.registered) ? <p className="method-library-note">No workflow in this library has been approved for use yet.</p> : null;

  return <section className="method-library" aria-label="Workflows" aria-busy={busy}>
    <input type="search" className="method-library-search" value={search} onChange={event => setSearch(event.target.value)} placeholder="Search workflows" aria-label="Search workflows"
      spellCheck={false} autoCapitalize="off" autoCorrect="off"/>
    {block === "stale" && <p className="method-library-note" role="note">The workflow view is out of date. Wait for it to refresh, or reopen the App view.</p>}
    {block === "no-conversation" && <p className="method-library-note" role="note">Choose the conversation that will run the workflow, under <a href="#run-workflow">Run a workflow</a>.</p>}
    {block === "no-conversations" && <p className="method-library-note" role="note">No conversation in this session yet. <a href="#workspace-start">Start a new conversation</a>, then choose it under Run a workflow.</p>}
    {thread && conversationLabel && <p className="method-library-note">For {conversationLabel}, chosen under <a href="#run-workflow">Run a workflow</a>.</p>}
    {chosen && !(chosen.runnable === true && !chosen.currentLimit) && <p className="method-library-note" role="note">{text(chosen.identity?.name)} can't run: {text(chosenLimit)}</p>}
    {chosen && newer && !newer.limit && <p className="method-library-note" role="note">A newer revision of {text(chosen.identity?.name)} is registered ({text(newer.notice)}). This conversation keeps using the chosen one until you choose the newer one under <a href="#run-workflow">Run a workflow</a>.</p>}
    {chosen && newer?.limit && chosen.identity?.origin !== "bundled" && <p className="method-library-note" role="note">Newer revisions of {text(chosen.identity?.name)} can't be checked: {text(newer.limit)}</p>}
    {readFailure && <p role="alert">The App's last read of its state failed ({readFailure}). What is shown here was read before that.</p>}
    {!busy && <GuideResult label="Workflows — last result" outcome={outcome} only={LIBRARY_COMMANDS}/>}
    {searching && <p className="method-library-note" role="status">{found.length + shownRegistered.length + shownUnregistered.length === 0 ? "No workflow matches. Try fewer or other words." : `${numberWords(found.length + shownRegistered.length + shownUnregistered.length)} match.`}</p>}

    <section className="method-library-group" aria-labelledby="method-group-included">
      <h3 id="method-group-included">Included with Chirality</h3>
      {catalog?.limit && <p role="note">The included workflows can't be read: {text(catalog.limit)}</p>}
      {sections.map((section, index) => <details key={section.key} className="method-library-subgroup"
        open={searching || index === 0 || section.entries.some(entry => entry === chosenEntry) || section.entries.some(holds) ? true : undefined}>
        <summary><h4>{section.label}</h4><span className="method-library-count">{numberWords(section.entries.length)}</span></summary>
        <ul className="method-library-list">{section.entries.map(includedCard)}</ul>
      </details>)}
    </section>

    <section className="method-library-group" aria-labelledby="method-group-project">
      <h3 id="method-group-project">This project</h3>
      {projectNote}
      {active && !Array.isArray(active.registered) && active.registered?.limit && <p role="note">This library's list of approved workflows can't be read: {text(active.registered.limit)}</p>}
      {active && listing?.libraryRef === active.reference && listing?.state === "unavailable" && <p role="note">The App couldn't look in this library's folder for other workflows{list(listing.limits).length ? `: ${list(listing.limits).map(text).join("; ")}` : "."}</p>}
      {pendingReview && <p role="note">A review is open. <a href="#workflow-reviews">Read it and confirm</a> to approve the workflow for use.</p>}
      {(shownRegistered.length > 0 || shownUnregistered.length > 0) && <ul className="method-library-list">
        {shownRegistered.map(registeredCard)}
        {shownUnregistered.map(unregisteredCard)}
      </ul>}
    </section>
  </section>;
}

/** An included workflow's text, held for its card. Its words and marking are the present read's own. */
function IncludedText({ entry, slot, source, texts, disabled, data, host }: { entry: Json; slot: string; source: string; texts: WorkflowTexts; disabled: boolean; data: Json; host: Json }) {
  return <WorkflowTextControl slot={slot} identity={entry?.identity} source={`included with the App${source ? `, from ${source}` : ""}`} texts={texts} disabled={disabled}
    target={{ kind: "included", name: entry?.name, revision: entry?.identity?.revision }} context={() => workflowContext(data, host, "")}/>;
}
