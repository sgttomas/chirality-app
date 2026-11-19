import { idWords, numberWords, safeName } from "./AgentText";
import { workflowContext } from "./workflowSelection";
import { WorkflowTextControl, useWorkflowTexts, type WorkflowTexts } from "./WorkflowText";
import { LibraryPathsBesideWorkflow, includedSections, librarySourceWords, matchesSearch } from "./IncludedWorkflows";
import { VIEW_NOT_REFRESHED, registeredRevisionAnchor } from "./RunJourney";
import { Supplied, isIncludedPick, isListedPick, pickIncluded, pickListed, type WorkflowPick } from "./WorkflowPick";
import { useState } from "react";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => (typeof value === "string" ? value : "");
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

/** The control that picks a workflow for the next message: 3.0.1's toggle. Picking is the renderer's alone (the pick is
 * held until the composer's Start run), so a picked card offers Remove, which sends nothing either. */
function PickToggle({ picked, disabled, pick, remove }: { picked: boolean; disabled: boolean; pick: () => void; remove: () => void }) {
  if (picked) return <button type="button" aria-pressed="true" onClick={remove}>Remove</button>;
  return <button type="button" aria-pressed="false" disabled={disabled} onClick={pick}>Use in message</button>;
}

/** Inspect: the workflow's own text, read through the App's present read and shown in the card as that read shows it. */
function InspectToggle({ shown, disabled, read, hide }: { shown: boolean; disabled: boolean; read: () => void; hide: () => void }) {
  return <button type="button" aria-expanded={shown} disabled={disabled && !shown} onClick={shown ? hide : read}>Inspect</button>;
}

/**
 * The right panel's Workflows tab, in 3.0.1's form: a search, the workflows included with the App in the Library's
 * own groups, and this project's workflows, each a card with Inspect and the toggle that picks it for the next
 * message. A pick needs no conversation: the composer's Start run chooses it for the conversation it starts or is in.
 * The tab issues no host command of its own besides Inspect's read.
 */
export function WorkflowLibrary({ data, host, busy, pick = null, setPick, viewStale = false, readFailure = null }: {
  data: Json; host: Json; busy: boolean; pick?: WorkflowPick | null; setPick?: (pick: WorkflowPick | null) => void; viewStale?: boolean; readFailure?: string | null;
}) {
  const [search, setSearch] = useState("");
  const texts = useWorkflowTexts();
  const sourceCurrent = !!data?.context?.sourceRef && host?.workflowRoot?.context?.sourceRef === data.context.sourceRef && same(data.context.generation, host?.generation);
  const canAct = !busy && sourceCurrent;
  // Picking is offered while the shown source is the host's; it waits for nothing else, since it sends nothing.
  const canPick = sourceCurrent && !!setPick;
  const catalog = data?.productionCatalog;
  const entries = list(catalog?.entries);
  const from = librarySourceWords(catalog?.source);

  if (viewStale && !busy) return <section className="method-library" aria-label="Workflows">
    <p className="method-library-note" role="status">{VIEW_NOT_REFRESHED}</p>
    {readFailure && <p role="alert">The last read failed: {readFailure}</p>}
  </section>;

  const searching = search.trim() !== "";
  const found = entries.filter(entry => matchesSearch(entry, search));
  const sections = includedSections(found);
  const includedSlot = (entry: Json) => `library:included:${text(entry?.name)}`;
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
  const remove = () => setPick?.(null);

  const includedCard = (entry: Json) => {
    const name = text(entry?.name);
    const shownName = text(entry?.navigation?.displayName) || name;
    const isChosen = isIncludedPick(pick, entry);
    const textShown = holds(entry);
    const roles = list(entry?.roles).filter((role: Json) => typeof role === "string");
    const runnable = entry?.runnable === true;
    return <li key={name} className="method-card" aria-label={`Included workflow ${safeName(entry?.name)}`} data-chosen={isChosen ? "true" : undefined}>
      <div className="method-card-heading"><strong><Supplied value={shownName} of="title"/></strong>{shownName !== name && <code className="method-card-identifier" title="Workflow identifier"><Supplied value={name} of="name"/></code>}</div>
      {entry?.description ? <p><Supplied value={text(entry.description)} of="description"/></p> : null}
      <p className="method-card-meta"><small>{from || "Included with the App"}</small></p>
      {entry?.runnable === false && <p className="method-card-limit" role="note">Can't be used in this App: {text(entry.runLimit) || text(catalog?.standing) ? <Supplied value={text(entry.runLimit) || text(catalog?.standing)} of="reason"/> : "the App reports it as not runnable"}.</p>}
      {entry?.runnable !== true && entry?.runnable !== false && <p className="method-card-limit" role="note">The App hasn't reported whether this workflow can be used here.</p>}
      <div className="method-card-actions">
        <InspectToggle shown={textShown} disabled={!canAct} hide={() => texts.hide(includedSlot(entry))}
          read={() => texts.read(includedSlot(entry), entry?.identity, { kind: "included", name: entry?.name, revision: entry?.identity?.revision }, workflowContext(data, host, ""))}/>
        <PickToggle picked={isChosen} disabled={!canPick || !runnable} pick={() => setPick?.(pickIncluded(entry, catalog, host))} remove={remove}/>
      </div>
      {textShown && <IncludedText entry={entry} slot={includedSlot(entry)} source={from} texts={texts} disabled={!canAct} data={data} host={host}/>}
      <details className="method-card-details"><summary>Details</summary>
        <p>Revision <code title={idWords(entry?.revision)}>{text(entry?.revision).slice(0, 12)}…</code></p>
        {roles.length > 0 && <p>The Library lists it for these roles: <Supplied value={roles.join(", ")} of="roles"/>.</p>}
        {entry?.compatibility === "legacy" && <p>The Library marks it as legacy.</p>}
        <LibraryPathsBesideWorkflow entry={entry} source={catalog?.source}/>
      </details>
    </li>;
  };

  const registeredCard = (row: Json) => {
    const isChosen = isListedPick(pick, row, active);
    const name = text(row.name);
    return <li key={`${name}@${text(row.revision)}`} className="method-card" aria-label={`Project workflow ${safeName(row.name)}`} data-chosen={isChosen ? "true" : undefined}>
      <div className="method-card-heading"><strong><Supplied value={name} of="name"/></strong></div>
      <p className="method-card-meta"><small>{libraryWords} · revision {numberWords(row.sequence) ?? ""}{sameName(row.name) ? " · another revision has the same name" : ""}</small></p>
      {row.selectable !== true && <p className="method-card-limit" role="note"><Supplied value={text(row.label)} of="reason"/>.{" "}
        <a href={`#${registeredRevisionAnchor(active.reference, row.name, row.revision)}`}>{row.reconfirm === true ? "Re-confirm it in the workflow studio" : "See this revision in the workflow studio"}</a></p>}
      <div className="method-card-actions">
        <PickToggle picked={isChosen} disabled={!canPick || row.selectable !== true} pick={() => setPick?.(pickListed(row, active, host))} remove={remove}/>
      </div>
      <details className="method-card-details"><summary>Details</summary>
        <p>Revision {numberWords(row.sequence) ?? ""} <code title={idWords(row.revision)}>{idWords(row.revision).slice(0, 12)}…</code>{row.selectable === true ? <> · <Supplied value={text(row.label)} of="reason"/></> : null}</p>
        {row.reconfirm === true && <p>Refine it into a draft, then review that draft and confirm in the App's dialog. Nothing is chosen or run until you do.</p>}
      </details>
    </li>;
  };

  const unregisteredCard = (entry: Json) => <li key={entry.reference} className="method-card" aria-label={`Project workflow ${safeName(entry.name)}`}>
    <div className="method-card-heading"><strong><Supplied value={text(entry.name)} of="name"/></strong></div>
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
    {!sourceCurrent && <p className="method-library-note" role="note">The workflow view is out of date. Wait for it to refresh, or reopen the App view.</p>}
    {readFailure && <p role="alert">The App's last read of its state failed ({readFailure}). What is shown here was read before that.</p>}
    {searching && <p className="method-library-note" role="status">{found.length + shownRegistered.length + shownUnregistered.length === 0 ? "No workflow matches. Try fewer or other words." : `${numberWords(found.length + shownRegistered.length + shownUnregistered.length)} match.`}</p>}

    <section className="method-library-group" aria-labelledby="method-group-included">
      <h3 id="method-group-included">Included with Chirality</h3>
      {catalog?.limit && <p role="note">The included workflows can't be read: {text(catalog.limit)}</p>}
      {sections.map((section, index) => <details key={section.key} className="method-library-subgroup"
        open={searching || index === 0 || section.entries.some(entry => isIncludedPick(pick, entry)) || section.entries.some(holds) ? true : undefined}>
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
