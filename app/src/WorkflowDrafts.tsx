type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// The workflow draft list (DEL-02-02 WR §5.1, §6 SQ-D, §4.2 TT-3/TT-4; DEL-01-04
// NIR §7 display words, PL-5). Under the owner's OI-008 ruling for the draft
// workspace, the Rust host observes drafts, computes their content identity and
// hygiene, and keeps trial pointers; this element only lists and presents what
// the host reports and names a draft back to the host by its listed name.

export type DraftAct = (command: string, args: Record<string, unknown>) => Promise<unknown>;
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);
const short = (value: Json): string => text(value).slice(0, 12);

/** NIR §7 DR: the words for each WR §5.1 state the workspace reports. */
export function draftStateWords(state: string, content?: Json): string {
  switch (state) {
    case "draft": return "draft — not registered";
    case "not valid": return "draft — not valid for registration";
    case "under review": return `under review (reviewed content ${short(content?.value)})`;
    case "changed since review": return "changed since review — review again before registering";
    case "registered, unchanged since": return "registered, unchanged since — the files still equal the revision this App recorded at registration";
    case "removed": return "removed";
    default: return `state reported as “${state}”`;
  }
}

/** WR D-3: where the last change was observed; never who did the work. */
export function attributionWords(attribution: Json): string {
  switch (attribution?.kind) {
    case "app action": return "written by this App (Refine or Create draft)";
    case "file change item": return `last change seen in Codex file-change item ${text(attribution.item)} (conversation ${text(attribution.thread)})`;
    case "not observed": return "not observed";
    default: return "not observed";
  }
}

function TrialPointer({ pointer }: { pointer: Json }) {
  return <li>Tried in conversation {text(pointer.conversation)} at {text(pointer.time)} with content {short(pointer.content?.value)} ({text(pointer.contentNow)}). {text(pointer.standing)}.</li>;
}

export function DraftRow({ draft, attachments, busy, act }: { draft: Json; attachments: Json; busy: boolean; act: DraftAct }) {
  const listed = attachments?.ownerRef && typeof attachments?.listRevision === "number";
  return <article aria-label={`Draft ${text(draft.name)}`} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
    <h4>{text(draft.name)} · {draftStateWords(draft.state, draft.content)}</h4>
    <p>Content {draft.content?.value ? `${short(draft.content.value)} (${text(draft.content.method)})` : `not established: ${text(draft.content?.not_established)}`}{draft.fileCount !== undefined && draft.fileCount !== null ? ` · ${text(draft.fileCount)} files` : ""}. Attribution: {attributionWords(draft.attribution)}.</p>
    {(draft.findings ?? []).length > 0 && <ul aria-label="Hygiene findings">{draft.findings.map((f: Json) => <li key={text(f)}>{text(f)}</li>)}</ul>}
    <p>{draft.base ? `App-recorded base: ${text(draft.base.name)} revision ${short(draft.base.revision)} (${text(draft.base.origin)} library).` : text(draft.baseLimit)}</p>
    {draft.slot?.identicalTo !== undefined && draft.slot?.identicalTo !== null && <p>Same bytes as registered revision {text(draft.slot.identicalTo)} of this library.</p>}
    <p><small>{text(draft.standing)}</small></p>
    <button disabled={busy || !!draft.tryLimit || !listed} onClick={() => { void act("workflow_try_draft", { ownerRef: attachments.ownerRef, listRevision: attachments.listRevision, name: draft.name }); }}>Try in a conversation</button>
    <small> Adds the draft’s files to “Selected text attachments” and sends nothing. You choose an ordinary conversation and send; the message is yours — not a workflow run, not registration. It opens no conversation itself, and non-text files are not attached (pending owner decision, WR U-WR-24).</small>
    {draft.tryLimit && <p role="note">{text(draft.tryLimit)}</p>}
    <div><button disabled={busy || !!draft.reviewLimit} onClick={() => { void act("workflow_review_draft", { name: draft.name }); }}>Review for registration…</button>
      <small> Opens the review of exactly the listed content. Registering is your separate A15 act through the native confirmation.</small></div>
    {draft.reviewLimit && <p role="note">{text(draft.reviewLimit)}</p>}
    {(draft.trials ?? []).length > 0 && <ul aria-label="Trial pointers">{draft.trials.map((p: Json) => <TrialPointer key={`${text(p.conversation)}@${text(p.time)}`} pointer={p} />)}</ul>}
  </article>;
}

export function WorkflowDraftsView({ data, attachments, workspace, pointerLimits, busy, act }: { data: Json; attachments: Json; workspace: boolean; pointerLimits?: Json; busy: boolean; act: DraftAct }) {
  const drafts: Json[] = data?.drafts ?? [];
  const transitions: Json[] = data?.transitions ?? [];
  // Problems the host could not resolve are shown, never hidden (damaged trial
  // pointers, transitions that did not conform to the WR schema).
  const limits: string[] = [...(pointerLimits ?? []), ...(data?.transitionLimits ?? [])].map(text);
  return <section aria-label="Workflow drafts">
    <h3>Workflow drafts</h3>
    <p>Drafts are folders under <code>.chirality/workflow-drafts/</code> of the open library. A draft has no workflow identity: trying it is an ordinary conversation, and only a registered revision runs.</p>
    <button disabled={busy || !workspace} onClick={() => { void act("workflow_open_project_library", {}); }}>Open this App project’s workflow library</button>{" "}
    <button disabled={busy || !data} onClick={() => { void act("workflow_observe_drafts", {}); }}>Refresh draft list</button>
    {!workspace && <p role="note">No explicit App project is configured; open a library with the folder picker below.</p>}
    {!data && <p>Open a library to list its drafts.</p>}
    {data?.state && <p>{text(data.state)}</p>}
    {data?.observedAt && <p>Listed at {text(data.observedAt)}. {text(data.standing)}.</p>}
    {data?.limit && <p role="note">{text(data.limit)}</p>}
    {limits.length > 0 && <ul role="alert" aria-label="Draft workspace limits">{limits.map(l => <li key={l}>{l}</li>)}</ul>}
    {data && !data.state && drafts.length === 0 && !data.limit && <p>No drafts in this library.</p>}
    {drafts.map(draft => <DraftRow key={text(draft.name)} draft={draft} attachments={attachments} busy={busy} act={act} />)}
    {transitions.length > 0 && <details><summary>Observed draft changes in this App session ({transitions.length})</summary><ul>{transitions.map((t, i) =>
      <li key={i}>{text(t.time)} · {text(t.draft?.name)}: {text(t.event)} ({text(t.from)} → {text(t.to)}); attribution {attributionWords(t.attribution)}</li>)}</ul></details>}
  </section>;
}
