import { useEffect, useRef, useState } from "react";
import { conversationLabel, nativePathText } from "./presentation";
import { draftStateWords } from "./WorkflowDrafts";
import { preparedMessages, preparedMessageLimit, type PreparedMessage } from "./preparedMessages";
import { cleanTrialAnchor } from "./TrialComposer";
import { GuideResult, GuideWithheld, type GuideOutcome } from "./RunJourney";
import { acknowledgeBringBackDoubt, beginBringBack, bringBackDoubtsFor, bringBackHeld, bringBackSendBlock, doubtDestination, endBringBack, useBringBackDoubts, type BringBackDoubt } from "./bringBackDoubts";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
type Act = (command: string, args: Record<string, unknown>) => Promise<Json>;
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

/** The host's workflow name rule (workflow_workspace::valid_name). */
export const validWorkflowName = (name: string) => name.length > 0 && name.length <= 64 && name.split("-").every(part => /^[a-z0-9]+$/.test(part));
/** The host's draft folder under an opened library (workflow_drafts::DRAFTS). */
export const draftFolder = (libraryRoot: string, name: string) => `${libraryRoot.replace(/\/+$/, "")}/.chirality/workflow-drafts/${name}`;

/** The request the person may edit and send; the App never sends it. */
export function draftRequestText(folder: string, name: string): string {
  return [
    `Please turn the method we used in this conversation into a reusable workflow draft named "${name}".`,
    "",
    `Write it as the folder ${folder}/ :`,
    `- ${folder}/WORKFLOW.md starts with front matter holding only \`name: ${name}\` and a one-line \`description:\`, then the method in prose: when to use it, its steps, what it needs and what it produces.`,
    "- If it helps, add the workflow-declaration block after the prose, as your instructions describe.",
    "- Put any supporting files the method needs in the same folder.",
    "",
    "Only write inside that folder. Don't register it; I'll try and review it in the App.",
  ].join("\n");
}

/**
 * The draft list's own trial and review commands for the named draft, with the
 * guide's conversation as the authoring conversation; arguments are exactly
 * DraftRow's. Prepared trial messages open through the studio's existing,
 * source-checked Open; nothing is sent.
 */
function DraftActions({ draft, chosen, host, canAct, act, openPreparedMessage, findInHistory }: { draft: Json; chosen: Json; host: Json; canAct: boolean; act: Act; openPreparedMessage?: (item: PreparedMessage) => void; findInHistory?: (hint: string) => void }) {
  const delegationMissing = chosen?.delegation?.reading === "missing";
  const perform = (command: string, args: Record<string, unknown>) => { if (canAct) void act(command, args); };
  const performed = (command: string, args: Record<string, unknown>): Promise<unknown> => {
    if (!canAct) return Promise.resolve();
    try { return Promise.resolve(act(command, args)).catch(() => undefined); } catch { return Promise.resolve(); }
  };
  const prepared = preparedMessages(host).filter(item => item.kind !== "bring-back" && item.pending?.draftName === draft.name);
  return <div aria-label="Try or review this draft">
    {!delegationMissing && <><button disabled={!canAct || !chosen || !!draft.tryLimit} onClick={() => perform("workflow_trial_prepare", { name: draft.name, kind: "delegated", generation: chosen?.generation, threadId: chosen?.threadId })}>Try it with the agent in this conversation</button>{" "}</>}
    <button disabled={!canAct || !!draft.tryLimit} onClick={() => perform("workflow_trial_prepare", { name: draft.name, kind: "clean", generation: chosen?.generation ?? null, threadId: chosen?.threadId ?? null })}>Try it in a fresh conversation</button>{" "}
    <button disabled={!canAct || !!draft.reviewLimit} onClick={() => perform("workflow_review_draft", { name: draft.name })}>Review it for registration…</button>
    <p><small>Trying is optional and pre-fills a trial message for you to send; it is not a run or a registration. Reviewing shows exactly the listed content; only your confirmation in the App's dialog registers it.</small></p>
    {delegationMissing && <p role="note"><small>Trying with the agent isn't available in this conversation: {text(chosen.delegation.reason)}. Try it in a fresh conversation.</small></p>}
    {draft.tryLimit && <p role="note"><small>{text(draft.tryLimit)}</small></p>}
    {draft.reviewLimit && <p role="note"><small>{text(draft.reviewLimit)}</small></p>}
    {prepared.map(item => <p key={item.identity}>Trial {text(item.pending?.sequence)} is ready to send.{" "}
      {item.kind === "clean" ? <a href={`#${cleanTrialAnchor(item.pending?.reference)}`}>Read and send it in the new-trial message box</a>
        : openPreparedMessage && <button disabled={preparedMessageLimit(host, item) !== null} onClick={() => openPreparedMessage(item)}>Read and send trial {text(item.pending?.sequence)}</button>}</p>)}
    <DraftTrials draft={draft} chosen={chosen} host={host} canAct={canAct} perform={performed} openPreparedMessage={openPreparedMessage} findInHistory={findInHistory}/>
  </div>;
}

/** A conversation as a trial row carries it. A tuple `{generation, threadId}` is
 * a live source the host proved; a bare ID is a saved label and is never
 * matched against the current session. */
function ConversationRef({ host, refValue, none, findInHistory }: { host: Json; refValue: Json; none: string; findInHistory?: (hint: string) => void }) {
  // A saved bare ID is only a search hint for History: nothing is read, selected or continued here.
  if (typeof refValue === "string" && refValue) return <>a recorded conversation <small>(<code>{refValue}</code>)</small>{findInHistory && <>{" "}<button onClick={() => findInHistory(refValue)}>Look for it in History</button></>}</>;
  if (refValue && typeof refValue === "object" && typeof refValue.threadId === "string" && refValue.threadId) {
    const row = list(host?.threads).find((t: Json) => t?.threadId === refValue.threadId && same(t?.generation, refValue.generation) && same(t?.generation, host?.generation));
    return row ? <>{conversationLabel(host, row)}</> : <>a conversation that isn't loaded now</>;
  }
  return <>{none}</>;
}

const sameTarget = (a: Json, b: Json) => same([a?.generation ?? null, a?.threadId ?? null], [b?.generation ?? null, b?.threadId ?? null]);
/** This draft's own listed trials (references the host gave it). */
const ownTrials = (draft: Json): Json[] => list(draft?.trials).filter((trial: Json) => (trial?.kind === "clean" || trial?.kind === "delegated") && typeof trial?.reference === "string" && trial.reference);
/** Prepared results messages for this draft's own trials. Bring-backs are App-wide, and another library may hold a same-name draft. */
const ownResults = (draft: Json, host: Json): PreparedMessage[] => {
  const references = new Set(ownTrials(draft).map((trial: Json) => trial.reference));
  return preparedMessages(host).filter(item => item.kind === "bring-back" && references.has(item.pending?.trial) && item.pending?.draftName === draft?.name);
};
/** Doubts that still hold for this draft's trials. */
const heldDoubts = (draft: Json, doubts: BringBackDoubt[]) => ownTrials(draft).flatMap((trial: Json) =>
  bringBackDoubtsFor("trial", trial.reference, doubts).filter(doubt => !doubt.acknowledged));

/**
 * The draft's trials as the host lists them (TT-4; newest first), and bringing
 * one back to the guide's conversation with the draft list's own command and
 * arguments (TT-10/TT-11). Bringing back only pre-fills a message; it is sent
 * from the conversation, and nothing here sends, registers or checks anything.
 * A trial already prepared for this conversation opens its existing message;
 * a send the host couldn't confirm holds it until the host records it or the
 * person says they checked (bringBackDoubts).
 */
function DraftTrials({ draft, chosen, host, canAct, perform, openPreparedMessage, findInHistory }: { draft: Json; chosen: Json; host: Json; canAct: boolean; perform: (command: string, args: Record<string, unknown>) => Promise<unknown>; openPreparedMessage?: (item: PreparedMessage) => void; findInHistory?: (hint: string) => void }) {
  const doubts = useBringBackDoubts();
  const trials = ownTrials(draft);
  const feedback = ownResults(draft, host);
  // A new results message after this guide's Bring press takes the focus once
  // it is committed, so the person lands on what to do next.
  const pressed = useRef<string | null>(null);
  const seen = useRef(new Set(feedback.map(item => item.identity)));
  const buttons = useRef(new Map<string, HTMLButtonElement>());
  useEffect(() => {
    const fresh = feedback.find(item => !seen.current.has(item.identity) && item.pending?.trial === pressed.current);
    for (const item of feedback) seen.current.add(item.identity);
    if (fresh) { pressed.current = null; buttons.current.get(fresh.identity)?.focus?.(); }
  });
  if (!trials.length && !feedback.length) return null;
  const target = chosen ? { generation: chosen.generation, threadId: chosen.threadId } : null;
  const bring = (trial: Json) => {
    if (!target || !canAct) return;
    // Read at the press, not from this render: an earlier control can't lift a
    // hold. The App's dispatch guard rechecks the host's current view as well.
    if (bringBackHeld("trial", trial.reference, target)) return;
    const key = JSON.stringify(["trial", trial.reference, target]);
    if (!beginBringBack(key)) return;
    pressed.current = trial.reference;
    void perform("workflow_trial_bring_back", { reference: trial.reference, generation: target.generation, threadId: target.threadId, includeNative: false }).finally(() => endBringBack(key));
  };
  return <div aria-label="Trials of this draft">
    <h4>Trials so far</h4>
    {trials.length > 0 && <ul>{trials.map((trial: Json) => {
      const n = text(trial.sequence), brought = list(trial.broughtBack);
      const mine = bringBackDoubtsFor("trial", trial.reference, doubts);
      const held = target ? mine.find(doubt => !doubt.acknowledged && doubtDestination(doubt, target) !== "other") : undefined;
      const existing = target ? feedback.find(item => item.pending?.trial === trial.reference && sameTarget(item.pending?.target, target) && item.pending?.includeNative !== true) : undefined;
      const existingBlock = existing ? bringBackSendBlock(existing.pending, existing.pending?.target, doubts) : null;
      const limit = held ? "Check that conversation first." : trial.live ? "Bringing it back waits until no turn is live in the trial."
        : trial.sourceLimit ? COLD_TRIAL : !chosen ? "Choose the conversation where you did the work to bring it back there." : null;
      return <li key={text(trial.reference)} aria-label={`Trial ${n} of ${text(draft.name)}`}>
        <strong>Trial {n}</strong> · {trial.kind === "clean"
          ? <>in a fresh conversation (<ConversationRef host={host} refValue={trial.trialConversation} none="not started" findInHistory={findInHistory}/>)</>
          : <>with the agent in <ConversationRef host={host} refValue={trial.authoringConversation} none="no recorded conversation" findInHistory={findInHistory}/></>}{trial.time ? <> · {text(trial.time)}</> : null}
        <br/><small>{brought.length ? <>Brought back {brought.length === 1 ? "once" : `${brought.length} times`}, to {brought.map((b: Json, i: number) => <span key={i}>{i ? ", " : ""}<ConversationRef host={host} refValue={b?.to} none="a conversation not recorded"/></span>)}.</> : "Not brought back yet."}</small>
        {mine.map(doubt => <div key={doubt.preparedId} role={doubt.acknowledged ? "note" : "alert"} aria-label={`Trial ${n} results may have been sent`}>
          <p><strong>Trial {n}'s results may already have been sent</strong> to <ConversationRef host={host} refValue={doubt.target} none="its conversation"/>: the App couldn't confirm the send{feedback.some(item => item.pending?.id === doubt.preparedId) ? ". Its prepared message is still listed, but that copy is not sent again" : ", and the prepared message was withdrawn"}.{doubt.acknowledged ? " You said you checked that conversation." : " Bringing it back there again could send the transcript twice."}</p>
          {target && doubtDestination(doubt, target) === "same-id-other-source" && <p><small>Codex or the home has changed since that send. The conversation chosen now has the same ID ({text(target.threadId)}), so bringing trial {n} back to it {doubt.acknowledged ? "is allowed again" : "is held until you've checked"}. That doesn't make the earlier destination this one.</small></p>}
          {!doubt.acknowledged && <p><button disabled={!canAct} onClick={() => acknowledgeBringBackDoubt(doubt)}>I've checked — let me bring it back again</button></p>}
          <details><summary>Your message and what was reported</summary><p><small>Your message: {doubt.personText || "(empty)"}</small></p><p><small>Reported: {doubt.message}</small></p>
            <p><small>Original destination: conversation <code>{text(doubt.target.threadId)}</code> in Codex session {text(doubt.target.generation?.spawnCounter)} of the {text(doubt.source.modeHomeClass)} home.</small></p></details>
        </div>)}
        <br/>{existing && !held
          ? (existingBlock
            // The results line below already offers this held copy; the row only says where it is.
            ? <small>Its results are prepared for this conversation but held, so they aren't sent again; see below.</small>
            : <><button disabled={!openPreparedMessage || preparedMessageLimit(host, existing) !== null} onClick={() => openPreparedMessage?.(existing)}>Read and send trial {n}'s prepared results</button><small> Its results are already prepared for this conversation.</small></>)
          : <><button disabled={!canAct || limit !== null} onClick={() => bring(trial)}>{chosen ? `Bring trial ${n} back to ${conversationLabel(host, chosen)}` : `Bring trial ${n} back`}</button>{limit && <small> {limit}</small>}{limit === COLD_TRIAL && <details><summary>Why</summary><p><small>{text(trial.sourceLimit)}</small></p></details>}</>}
      </li>;
    })}</ul>}
    <div aria-live="polite">{feedback.map(item => {
      // A copy the dispatch guard holds is prepared, not ready to send (same rule as its Send).
      const block = bringBackSendBlock(item.pending, item.pending?.target, doubts);
      const n = text(item.pending?.sequence);
      return <p key={item.identity}>{block
        ? <>Trial {n}'s results are prepared in <ConversationRef host={host} refValue={item.owner} none="its conversation"/>, but sending them is held: {block}</>
        : <>Trial {n}'s results are ready to send in <ConversationRef host={host} refValue={item.owner} none="its conversation"/>.</>}{" "}
        {openPreparedMessage && <button ref={node => { if (node) buttons.current.set(item.identity, node); else buttons.current.delete(item.identity); }} disabled={preparedMessageLimit(host, item) !== null} onClick={() => openPreparedMessage(item)}>{block ? `Open trial ${n}'s prepared results to read or remove` : `Read and send trial ${n}'s results`}</button>}</p>;
    })}</div>
    <p><small>Bringing a trial back pre-fills a message with its transcript for the agent to assess against the draft; you read and send it. To include native items or choose another conversation, use the draft list in the workflow studio. When a trial went well, review the draft for registration.</small></p>
  </div>;
}

/** The registration review that belongs to this draft, by the review's own identity. */
type ReviewIdentity = { names: string[]; root: Json; origin: Json; sourceRoot: Json };
type ReviewRow = { reference: string; status: Json; identity: ReviewIdentity | null };
const DISMISSED = "native confirmation dismissed; no capture/registration";
const UNAVAILABLE = "native review/capture unavailable; original owner state retained";

/**
 * The draft's actual next step: an unconfirmed bring-back, prepared messages,
 * then the registration review's own state (never inferred from the draft
 * state alone), then the draft state.
 */
function draftStep(draft: Json, data: Json, host: Json, doubts: BringBackDoubt[], review: ReviewRow | null): { words: string; href: string; link: string } {
  if (draft?.state === "not valid" || draft?.state === "registered, unchanged since" || draft?.state === "removed") return nextFor(draft);
  const doubt = heldDoubts(draft, doubts)[0];
  if (doubt) return { words: `Check whether trial ${text(doubt.sequence)}'s results arrived in the conversation before bringing it back again.`, href: "#conversation", link: "Go to the conversation" };
  const results = ownResults(draft, host)[0];
  if (results) return bringBackSendBlock(results.pending, results.pending?.target, doubts)
    ? { words: `Trial ${text(results.pending?.sequence)}'s prepared results are held and not sent again; after reading the conversation, remove that copy and bring the trial back if you still need to.`, href: "#conversation", link: "Go to the conversation" }
    : { words: `Read and send trial ${text(results.pending?.sequence)}'s results in the conversation, then review the draft.`, href: "#conversation", link: "Go to the conversation" };
  const trial = preparedMessages(host).find(item => item.kind !== "bring-back" && item.pending?.draftName === draft?.name);
  if (trial) return { words: `Read and send trial ${text(trial.pending?.sequence)} in the conversation.`, href: trial.kind === "clean" ? `#${cleanTrialAnchor(trial.pending?.reference)}` : "#conversation", link: "Go to the trial message" };
  if (review) {
    const state = review.status?.state;
    if (review.status?.presentation && review.reference === data?.activeReview)
      return { words: "A review is open. Read it and confirm registration in the App's dialog — or close it to keep working.", href: "#workflow-reviews", link: "Open the review" };
    if (state === DISMISSED) return { words: "You cancelled the App's confirmation, so nothing was registered. To register it, look for drafts again and review it again.", href: "#workflow-reviews", link: "See the review" };
    if (state === UNAVAILABLE) return { words: `The review or its confirmation became unavailable, so registration did not complete${review.status?.limit ? ` (${text(review.status.limit)})` : ""}. The original attempt is kept: continue it from the review, or review the draft again.`, href: "#workflow-reviews", link: "Open the review" };
    if (review.status?.presentation) return { words: "That review is no longer the current one, so it can't be confirmed from here. Review the draft again.", href: "#workflow-reviews", link: "See the review" };
  }
  if (draft?.state === "under review") return { words: "A review was started, but its confirmation isn't available here now. Open the review to see its state.", href: "#workflow-reviews", link: "Open the review" };
  return nextFor(draft);
}

const EXISTING = "an existing draft continues below";
/** A saved trial whose original source isn't established (after a relaunch): the available next actions, not just the refusal. */
const COLD_TRIAL = "This saved trial can't be brought back here. Try the draft again in a fresh conversation above, or look at the earlier conversation in History.";

function nextFor(draft: Json): { words: string; href: string; link: string } {
  switch (draft?.state) {
    case "not valid": return { words: "The App can't review it yet. Ask the agent to fix the findings below, then look again.", href: "#conversation", link: "Go to the conversation" };
    case "under review": return { words: "A review is open. Read it and confirm registration in the App's dialog — or close it to keep working.", href: "#workflow-reviews", link: "Open the review" };
    case "changed since review": return { words: "The files changed after review. Review again before registering.", href: "#workflow-drafts", link: "Open the draft" };
    case "registered, unchanged since": return { words: "Registered. You can now use it from Run a workflow.", href: "#run-workflow", link: "Run a workflow" };
    case "removed": return { words: "The draft folder is gone.", href: "#workflow-drafts", link: "Open the draft list" };
    default: return { words: "Optionally try it (with the authoring agent, or in a fresh conversation), then review it for registration. Only your confirmation registers it.", href: "#workflow-drafts", link: "Try or review it" };
  }
}

const MAKE_COMMANDS = ["workflow_open_project_library", "workflow_observe_drafts", "workflow_review_draft", "workflow_trial_prepare", "workflow_trial_bring_back"];
/**
 * J2 — make a reusable workflow from work done in a conversation. The App
 * composes a request for the person to edit and send in that conversation
 * (no host command); finding the draft uses the studio's existing
 * `workflow_observe_drafts`; trial, review and registration stay in the
 * existing draft list and review, where only the person's act registers.
 */
export function MakeWorkflowGuide({ data, host, act, busy, offerComposer, openPreparedMessage, showConversation, findInHistory, outcome, viewStale = false }: {
  data: Json; host: Json; act: Act; busy: boolean; outcome?: GuideOutcome | null; viewStale?: boolean; offerComposer: (threadKey: string, text: string) => void; openPreparedMessage?: (item: PreparedMessage) => void;
  showConversation?: (threadId: string, target?: string) => void; findInHistory?: (hint: string) => void;
}) {
  // Continue <draft> moves the person to its current step once it is shown,
  // only while the same library and draft are still the ones shown.
  const revealDraft = useRef<{ library: Json; name: string } | null>(null);
  const draftStatus = useRef<HTMLParagraphElement>(null);
  const [revealRequest, setRevealRequest] = useState(0);
  const doubts = useBringBackDoubts();
  // A review names its library and workflows only while its presentation is
  // shown. Reviews are App-wide and outlive a library switch, so keep the full
  // identity it was seen with (library root, origin, source root and workflow
  // names): a later dismissed or unavailable status still belongs to its own
  // library's draft, never to a same-name draft elsewhere (this window only).
  const reviewIdentities = useRef(new Map<string, ReviewIdentity>());
  const reviews: ReviewRow[] = list(data?.reviews).filter((row: Json) => typeof row?.reference === "string").map((row: Json) => {
    const presentation = row.status?.presentation;
    const names = list(presentation?.entries).map((entry: Json) => entry?.identity?.name).filter((name: Json) => typeof name === "string");
    if (presentation && names.length && typeof presentation.library === "string")
      reviewIdentities.current.set(row.reference, { names, root: presentation.library, origin: presentation.origin ?? null, sourceRoot: presentation.source_root ?? null });
    return { reference: row.reference, status: row.status, identity: reviewIdentities.current.get(row.reference) ?? null };
  });
  const [conversation, setConversation] = useState("");
  const [name, setName] = useState("");
  const sourceCurrent = !!data?.context?.sourceRef && host?.workflowRoot?.context?.sourceRef === data.context.sourceRef && same(data.context.generation, host?.generation);
  const ready = host?.state === "ready" && host?.generationClosed !== true;
  const canAct = !busy && sourceCurrent;
  const conversations = list(host?.threads).filter((row: Json) => same(row.generation, host?.generation));
  const chosen = conversations.find((row: Json) => JSON.stringify([row.generation, row.threadId]) === conversation);
  const active = list(data?.libraries).find((library: Json) => library.reference === data?.activeLibrary);
  const root = nativePathText(active?.root);
  const drafts = list(data?.drafts?.drafts);
  const trimmed = name.trim();
  const valid = validWorkflowName(trimmed);
  const existingDraft = drafts.find((draft: Json) => draft.name === trimmed);
  const registeredSame = list(active?.registered).some((row: Json) => row.name === trimmed);
  const unfinished = drafts.filter((draft: Json) => draft.state !== "registered, unchanged since" && draft.state !== "removed");
  const blocked = !ready ? "Connect Codex first: open Connection & access and start Codex."
    : !sourceCurrent ? "The workflow view is out of date. Wait for it to refresh, or reopen the App view."
    : !active ? data?.projectLibraryAvailable === true ? "Show this project's workflows so the draft has a place to go, and to see unfinished drafts." : "Open a workflow library in the workflow studio below, or choose a project in Desktop setup."
    : !chosen ? conversations.length ? "Choose the conversation where you did the work." : "Do the work in a conversation first, then choose it here."
    : root === null ? "The opened library's folder can't be shown, so the App can't name where the draft goes."
    : !trimmed ? "Name the workflow: lowercase letters and digits, words joined by hyphens."
    : !valid ? "Use lowercase letters and digits only, words joined by single hyphens, at most 64 characters."
    : existingDraft ? EXISTING
    : registeredSame ? `A workflow named ${trimmed} is already registered in this library; a new draft with that name would be refused. Choose another name, or refine ${trimmed} from the workflow studio.`
    : null;
  const folder = root !== null && valid ? draftFolder(root, trimmed) : null;
  // An existing draft blocks a new request, but its own next step is what to do now.
  const activeRoot = nativePathText(active?.root);
  const ownReviews = existingDraft && activeRoot !== null ? reviews.filter(row => !!row.identity && row.identity.names.includes(existingDraft.name)
    && row.identity.root === activeRoot && same(row.identity.origin, active?.origin ?? null) && same(row.identity.sourceRoot, active?.sourceRoot ?? null)) : [];
  const review = ownReviews.find(row => row.reference === data?.activeReview) ?? ownReviews.at(-1) ?? null;
  const step = existingDraft ? draftStep(existingDraft, data, host, doubts, review) : null;
  const nextLine = blocked === EXISTING && step ? `${trimmed}: ${step.words}` : blocked;
  useEffect(() => {
    const wanted = revealDraft.current;
    if (!wanted || !revealRequest) return;
    revealDraft.current = null;
    if (wanted.library !== (data?.activeLibrary ?? null) || existingDraft?.name !== wanted.name || trimmed !== wanted.name) return;
    // The status region can be taller than the window: land on its first line.
    draftStatus.current?.scrollIntoView?.({ block: "start" });
    draftStatus.current?.focus?.({ preventScroll: true });
  }, [revealRequest]); // eslint-disable-line react-hooks/exhaustive-deps
  if (viewStale && !busy) return <GuideWithheld id="make-workflow" label="Make a workflow from your work" title="Make a workflow from your work" outcome={outcome} resultLabel="Make a workflow — last result" only={MAKE_COMMANDS}/>;
  return <section id="make-workflow" className="workflow-stage run-journey" aria-label="Make a workflow from your work" aria-busy={busy}>
    <h2>Make a workflow from your work</h2>
    <p className="run-journey-next" role="status" aria-live="polite"><strong>Next:</strong> {nextLine ?? "Put the request in the conversation, read it, and send it when you're happy with it."}</p>
    {!busy && <GuideResult label="Make a workflow — last result" outcome={outcome} only={MAKE_COMMANDS}/>}
    <ol className="run-journey-steps">
      <li><h3>Where you did the work</h3>
        {conversations.length ? <label>Conversation with the work <select value={conversation} disabled={!canAct} onChange={event => setConversation(event.target.value)}>
          <option value="">Choose a conversation</option>
          {conversations.map((row: Json) => { const key = JSON.stringify([row.generation, row.threadId]); return <option key={key} value={key}>{conversationLabel(host, row)}</option>; })}
        </select></label> : <p>No conversation in this session yet. <a href="#workspace-start">Start one</a> and do the work there first.</p>}
        {chosen && <details className="conversation-identity"><summary>Exact conversation ID</summary><code>{chosen.threadId}</code></details>}
      </li>
      <li><h3>Where the draft goes</h3>
        {active ? <p>{text(active.origin) || "Opened"} workflow library{root !== null ? <> in <code>{root}</code></> : ""}. Drafts are kept in its <code>.chirality/workflow-drafts</code> folder until you register them.</p>
          : data?.projectLibraryAvailable === true ? <button disabled={!canAct} onClick={() => { if (canAct) void act("workflow_open_project_library", {}); }}>Show this project's workflows</button>
          : <p>No library is open. Open one in the workflow studio below, or <a href="#desktop-setup">choose a project in Desktop setup</a>.</p>}
      </li>
      <li><h3>Name</h3>
        <label>Workflow name <input value={name} disabled={busy} onChange={event => setName(event.target.value)} spellCheck={false} autoCapitalize="off" autoCorrect="off"/></label>
        {folder && <p><small>It will be written to <code>{folder}</code>.</small></p>}
      </li>
      <li><h3>Ask the agent to write it</h3>
        <button className="setup-primary" disabled={!canAct || blocked !== null || !folder || !chosen} onClick={() => { if (canAct && blocked === null && folder && chosen) offerComposer(conversation, draftRequestText(folder, trimmed)); }}>Put the request in the conversation</button>
        <p><small>The request appears in that conversation's message box for you to edit. Nothing is sent until you press Send there.</small></p>
      </li>
      <li><h3>Find, try and register it</h3>
        <button disabled={!canAct || !active} onClick={() => { if (canAct && active) void act("workflow_observe_drafts", {}); }}>Look for drafts in this library</button>
        {typeof data?.drafts?.limit === "string" && data.drafts.limit && <p role="note">The App couldn't read this library's drafts: {data.drafts.limit}</p>}
        {existingDraft && step ? (() => { const next = step; return <div className="run-journey-state" aria-label="Draft status">
          <p ref={draftStatus} tabIndex={-1} role="status" aria-label="Draft state"><strong>{trimmed}</strong>: {draftStateWords(existingDraft.state, existingDraft.content)}.</p>
          {list(existingDraft.findings).length > 0 && <ul aria-label="What to fix">{list(existingDraft.findings).map((finding: Json) => <li key={text(finding)}>{text(finding)}</li>)}</ul>}
          <p>{next.words} {next.href === "#conversation" && showConversation && chosen
            ? <button onClick={() => showConversation(chosen.threadId)}>Show the conversation</button>
            : <a href={next.href}>{next.link}</a>}</p>
          {(existingDraft.state === "draft" || existingDraft.state === "changed since review") && <DraftActions draft={existingDraft} chosen={chosen} host={host} canAct={canAct} act={act} openPreparedMessage={openPreparedMessage} findInHistory={findInHistory}/>}
        </div>; })() : trimmed && valid && active ? <p>No draft named {trimmed} has been seen yet. After the agent writes it, look for drafts.</p> : null}
      </li>
    </ol>
    {unfinished.length > 0 && <div aria-label="Unfinished drafts">
      <h3>Unfinished drafts in this library</h3>
      <p><small>Drafts are files in the library, so they are still here after you quit and reopen the App. Their earlier conversations are in History. Reading one there only shows it; to keep working in it, press Continue there, which is a separate step.</small></p>
      <ul>{unfinished.map((draft: Json) => <li key={text(draft.name)}><strong>{text(draft.name)}</strong> — {draftStateWords(draft.state, draft.content)}{" "}
        <button disabled={busy} onClick={() => { setName(text(draft.name)); revealDraft.current = { library: data?.activeLibrary ?? null, name: text(draft.name) }; setRevealRequest(n => n + 1); }}>Continue {text(draft.name)}</button></li>)}</ul>
    </div>}
  </section>;
}
