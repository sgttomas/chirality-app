import { useState } from "react";
import { nativePathText } from "./presentation";
import { draftStateWords } from "./WorkflowDrafts";
import { preparedMessages, preparedMessageLimit, type PreparedMessage } from "./preparedMessages";

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
function DraftActions({ draft, chosen, host, canAct, act, openPreparedMessage }: { draft: Json; chosen: Json; host: Json; canAct: boolean; act: Act; openPreparedMessage?: (item: PreparedMessage) => void }) {
  const delegationMissing = chosen?.delegation?.reading === "missing";
  const perform = (command: string, args: Record<string, unknown>) => { if (canAct) void act(command, args); };
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
      {item.kind === "clean" ? <a href="#conversation">Read and send it in the new-trial message box</a>
        : openPreparedMessage && <button disabled={preparedMessageLimit(host, item) !== null} onClick={() => openPreparedMessage(item)}>Read and send trial {text(item.pending?.sequence)}</button>}</p>)}
  </div>;
}

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

/**
 * J2 — make a reusable workflow from work done in a conversation. The App
 * composes a request for the person to edit and send in that conversation
 * (no host command); finding the draft uses the studio's existing
 * `workflow_observe_drafts`; trial, review and registration stay in the
 * existing draft list and review, where only the person's act registers.
 */
export function MakeWorkflowGuide({ data, host, act, busy, offerComposer, openPreparedMessage, showConversation }: {
  data: Json; host: Json; act: Act; busy: boolean; offerComposer: (threadKey: string, text: string) => void; openPreparedMessage?: (item: PreparedMessage) => void;
  showConversation?: (threadId: string, target?: string) => void;
}) {
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
    : existingDraft ? `A draft named ${trimmed} already exists. Continue it below instead of asking for a new one.`
    : registeredSame ? `A workflow named ${trimmed} is already registered in this library; a new draft with that name would be refused. Choose another name, or refine ${trimmed} from the workflow studio.`
    : null;
  const folder = root !== null && valid ? draftFolder(root, trimmed) : null;
  return <section id="make-workflow" className="workflow-stage run-journey" aria-label="Make a workflow from your work" aria-busy={busy}>
    <h2>Make a workflow from your work</h2>
    <p className="run-journey-next" role="status" aria-live="polite"><strong>Next:</strong> {blocked ?? "Put the request in the conversation, read it, and send it when you're happy with it."}</p>
    <ol className="run-journey-steps">
      <li><h3>Where you did the work</h3>
        {conversations.length ? <label>Conversation with the work <select value={conversation} disabled={!canAct} onChange={event => setConversation(event.target.value)}>
          <option value="">Choose a conversation</option>
          {conversations.map((row: Json) => { const key = JSON.stringify([row.generation, row.threadId]); return <option key={key} value={key}>{row.preview ? `${text(row.preview).slice(0, 48)} · ` : ""}{row.model ?? "model not reported"} · {row.threadId}</option>; })}
        </select></label> : <p>No conversation in this session yet. <a href="#workspace-start">Start one</a> and do the work there first.</p>}
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
        {existingDraft ? (() => { const next = nextFor(existingDraft); return <div className="run-journey-state" aria-label="Draft status">
          <p role="status"><strong>{trimmed}</strong>: {draftStateWords(existingDraft.state, existingDraft.content)}.</p>
          {list(existingDraft.findings).length > 0 && <ul aria-label="What to fix">{list(existingDraft.findings).map((finding: Json) => <li key={text(finding)}>{text(finding)}</li>)}</ul>}
          <p>{next.words} {next.href === "#conversation" && showConversation && chosen
            ? <button onClick={() => showConversation(chosen.threadId)}>Show the conversation</button>
            : <a href={next.href}>{next.link}</a>}</p>
          {(existingDraft.state === "draft" || existingDraft.state === "changed since review") && <DraftActions draft={existingDraft} chosen={chosen} host={host} canAct={canAct} act={act} openPreparedMessage={openPreparedMessage}/>}
        </div>; })() : trimmed && valid && active ? <p>No draft named {trimmed} has been seen yet. After the agent writes it, look for drafts.</p> : null}
      </li>
    </ol>
    {unfinished.length > 0 && <div aria-label="Unfinished drafts">
      <h3>Unfinished drafts in this library</h3>
      <p><small>Drafts are files in the library, so they are still here after you quit and reopen the App. Their earlier conversations are in History; reading one there doesn't continue it.</small></p>
      <ul>{unfinished.map((draft: Json) => <li key={text(draft.name)}><strong>{text(draft.name)}</strong> — {draftStateWords(draft.state, draft.content)}{" "}
        <button disabled={busy} onClick={() => setName(text(draft.name))}>Continue {text(draft.name)}</button></li>)}</ul>
    </div>}
  </section>;
}
