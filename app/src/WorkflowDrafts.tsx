import { useState } from "react";
import { ConversationSelect, conversationKey, conversationName, findConversation } from "./TrialComposer";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// The workflow draft list and its trials (DEL-02-02 WR §5.1, §5.5, §6 SQ-D,
// SQ-DT, SQ-FT, SQ-BB, §4.2 TT-3…TT-13; DEL-01-04 NIR §7 display words, PL-5).
// Under the owner's OI-008 ruling the Rust host observes drafts, composes trial
// texts, takes snapshots, keeps trial links and sends; this element lists and
// presents what the host reports and, on the person's press only, names a
// draft or a trial back to the host. Every help action here is a button
// (TT-11); nothing runs on its own, and nothing here scores or judges a trial.

export type DraftAct = (command: string, args: Record<string, unknown>) => Promise<unknown>;
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
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

/** TT-9: the three fidelity readings, in the design's words. */
export function fidelityWords(fidelity: Json, kind?: string): string {
  switch (fidelity?.state) {
    case "verbatim": return `workflow given verbatim${fidelity.header_present === true ? " (trial header present)" : fidelity.header_present === false ? " (trial header not present)" : ""}`;
    case "differs": return `${kind === "clean" ? "the trial conversation's input" : "the sub-agent's input"} differs from the run text${fidelity.difference ? `: ${text(fidelity.difference)}` : ""}`;
    default: return "not checked";
  }
}

/** A Compare side as the host takes it. */
export const trialSide = (reference: Json) => JSON.stringify({ trial: text(reference) });
export const runSide = (reference: Json) => JSON.stringify({ run: text(reference) });

/** The drafts view's own state: the person's choices, nothing of the host's. */
export type DraftsState = { authoring: string; chosen: string[]; compared: Json | null; compareError: string; bbTarget: Record<string, string>; bbNative: Record<string, boolean> };
export const initialDraftsState: DraftsState = { authoring: "", chosen: [], compared: null, compareError: "", bbTarget: {}, bbNative: {} };
type Update = (patch: Partial<DraftsState>) => void;

function SubAgent({ trial, busy, act }: { trial: Json; busy: boolean; act: DraftAct }) {
  const sub = trial.subAgent;
  if (!sub) return <>sub-agent not linked</>;
  return <>
    {sub.state === "linked" ? <>sub-agent {text(sub.thread)}{sub.linkedBy ? ` (linked ${text(sub.linkedBy)})` : ""}{" "}
      <button disabled={busy} onClick={() => { void act("workflow_trial_unlink", { reference: trial.reference, childThread: sub.thread }); }}>Unlink</button></> : "sub-agent not linked"}
    {list(sub.alsoGiven).length > 0 && <> · also given this trial's workflow: {list(sub.alsoGiven).map(text).join(", ")}</>}
    {list(sub.unread).map((child: Json) => <span key={text(child)}> · sub-agent {text(child)} started in the trial turn (input not read){" "}
      <button disabled={busy} onClick={() => { void act("workflow_trial_link", { reference: trial.reference, childThread: child }); }}>Link as trial {text(trial.sequence)}</button></span>)}
  </>;
}

/** TT-4: one listed trial, with its help actions (TT-11). */
export function TrialRow({ trial, conversations, busy, act, state, update }: { trial: Json; conversations: Json[]; busy: boolean; act: DraftAct; state: DraftsState; update: Update }) {
  if (trial?.kind === "earlier attachment trial") return <li>Earlier attachment trial · content {short(trial.content?.value)} ({text(trial.version)}) · conversation {conversationName(trial.conversation)} · {text(trial.time)}</li>;
  const reference = text(trial.reference);
  const side = trialSide(reference);
  const ticked = state.chosen.includes(side);
  const defaultTarget = conversationKey(findConversation(conversations, trial.authoringConversation));
  const target = state.bbTarget[reference] ?? defaultTarget;
  const chosen = list(conversations).find((c: Json) => conversationKey(c) === target) ?? null;
  const includeNative = state.bbNative[reference] ?? false;
  const fidelity = trial.fidelity ?? {};
  return <li aria-label={`Trial ${text(trial.sequence)}`}>
    <label><input type="checkbox" checked={ticked} disabled={busy} onChange={() => update({ chosen: ticked ? state.chosen.filter(c => c !== side) : [...state.chosen, side] })} /> Compare</label>{" "}
    <b>Trial {text(trial.sequence)}</b> · {trial.kind === "clean" ? "clean (fresh conversation)" : "delegated (with the authoring agent)"} · {text(trial.time)}
    <div><small>Content {short(trial.content?.value)} ({trial.version === "current" ? "current version" : "earlier version"}) · authoring conversation {conversationName(trial.authoringConversation)} · {trial.kind === "clean"
      ? <>trial conversation {trial.trialConversation ? conversationName(trial.trialConversation) : "not started"}</>
      : <SubAgent trial={trial} busy={busy} act={act} />}</small></div>
    <div><small>Fidelity: {fidelityWords(fidelity, trial.kind)}{list(fidelity.limits).length ? ` (${list(fidelity.limits).map(text).join("; ")})` : ""}. Snapshot: {text(trial.snapshot?.reading) || "not read"}.
      {trial.filesOutsideWorkFolder ? ` ${text(trial.filesOutsideWorkFolder.reading)}.` : ""} Work folder <code>{text(trial.workFolder)}</code>.</small></div>
    <div><small>{list(trial.broughtBack).length ? `Brought back: ${list(trial.broughtBack).map((b: Json) => `${text(b.time)} to ${conversationName(b.to)}`).join("; ")}.` : "Not brought back."} {text(trial.standing)}</small></div>
    <div>
      <button disabled={busy} onClick={() => { void act("workflow_trial_again", { reference }); }}>Try again</button>{" "}
      <button disabled={busy} onClick={() => { void act("workflow_trial_read", { reference }); }}>Read again</button>{" "}
      <ConversationSelect label="Bring back to" conversations={conversations} value={target} setValue={key => update({ bbTarget: { ...state.bbTarget, [reference]: key } })} disabled={busy} />{" "}
      <label><input type="checkbox" checked={includeNative} disabled={busy} onChange={e => update({ bbNative: { ...state.bbNative, [reference]: e.target.checked } })} /> include native items</label>{" "}
      <button disabled={busy || !!trial.live || !chosen} onClick={() => { void act("workflow_trial_bring_back", { reference, generation: chosen?.generation, threadId: chosen?.threadId, includeNative }); }}>Bring trial back</button>
      {trial.live && <small> Bring trial back waits until no turn is live.</small>}
    </div>
  </li>;
}

export function DraftRow({ draft, authoring, conversations = [], pending = [], busy, act, state = initialDraftsState, update = () => undefined }: { draft: Json; authoring: Json | null; conversations?: Json[]; pending?: Json[]; busy: boolean; act: DraftAct; state?: DraftsState; update?: Update }) {
  const trials = list(draft.trials);
  const mine = list(pending).filter((p: Json) => p?.draftName === draft.name);
  return <article aria-label={`Draft ${text(draft.name)}`} style={{ borderTop: "1px solid #ccc", paddingTop: 8 }}>
    <h4>{text(draft.name)} · {draftStateWords(draft.state, draft.content)}</h4>
    <p>Content {draft.content?.value ? `${short(draft.content.value)} (${text(draft.content.method)})` : `not established: ${text(draft.content?.not_established)}`}{draft.fileCount !== undefined && draft.fileCount !== null ? ` · ${text(draft.fileCount)} files` : ""}. Attribution: {attributionWords(draft.attribution)}.</p>
    {(draft.findings ?? []).length > 0 && <ul aria-label="Hygiene findings">{draft.findings.map((f: Json) => <li key={text(f)}>{text(f)}</li>)}</ul>}
    <p>{draft.base ? `App-recorded base: ${text(draft.base.name)} revision ${short(draft.base.revision)} (${text(draft.base.origin)} library).` : text(draft.baseLimit)}</p>
    {draft.slot?.identicalTo !== undefined && draft.slot?.identicalTo !== null && <p>Same bytes as registered revision {text(draft.slot.identicalTo)} of this library.</p>}
    <p><small>{text(draft.standing)}</small></p>
    <div>
      <button disabled={busy || !!draft.tryLimit || !authoring} onClick={() => { void act("workflow_trial_prepare", { name: draft.name, kind: "delegated", generation: authoring?.generation, threadId: authoring?.threadId }); }}>Try with the authoring agent</button>{" "}
      <button disabled={busy || !!draft.tryLimit} onClick={() => { void act("workflow_trial_prepare", { name: draft.name, kind: "clean", generation: authoring?.generation ?? null, threadId: authoring?.threadId ?? null }); }}>Try in a fresh conversation</button>
      <p><small>Either pre-fills a trial message for you to read and send; nothing is sent until you press Send. A trial is not a workflow run, registration, checking or acceptance. The fresh-conversation trial is optional.</small></p>
      {!authoring && !draft.tryLimit && <p role="note"><small>Choose an authoring conversation above to try with the authoring agent, or try in a fresh conversation.</small></p>}
    </div>
    {draft.tryLimit && <p role="note">{text(draft.tryLimit)}</p>}
    {mine.map((p: Json) => <p key={text(p.reference)}><small>Trial {text(p.sequence)} ({text(p.kind)}) is pre-filled, not sent: {text(p.state)}. Send or remove it in the conversation panel.</small></p>)}
    <div><button disabled={busy || !!draft.reviewLimit} onClick={() => { void act("workflow_review_draft", { name: draft.name }); }}>Review for registration…</button>
      <small> Opens the review of exactly the listed content. Registering is your separate A15 act through the native confirmation.</small></div>
    {draft.reviewLimit && <p role="note">{text(draft.reviewLimit)}</p>}
    {trials.length > 0 && <ul aria-label="Trials">{trials.map((t: Json, i: number) => <TrialRow key={text(t.reference) || `${text(t.time)}:${i}`} trial={t} conversations={conversations} busy={busy} act={act} state={state} update={update} />)}</ul>}
  </article>;
}

/** TT-11 Compare: the host's side-by-side reading and version difference. It scores and judges nothing. */
export function CompareResult({ result }: { result: Json }) {
  if (!result) return null;
  const sides = [result.left, result.right];
  const row = (label: string, read: (s: Json) => Json) => <tr><th scope="row">{label}</th>{sides.map((s, i) => <td key={i}>{text(read(s ?? {}))}</td>)}</tr>;
  const difference = result.difference ?? {};
  return <div aria-label="Compare result">
    <table><tbody>
      {row("Side", s => s.label)}{row("Kind", s => s.kind)}{row("Version", s => s.version)}{row("Conversation", s => conversationName(s.conversation))}{row("Snapshot", s => s.snapshot?.reading ?? s.snapshot)}
      {row("Turns", s => s.summary?.turns)}{row("Endings", s => list(s.summary?.endings).map(text).join(", "))}
      {row("Commands run", s => s.summary?.commands?.run)}{row("Commands failed", s => s.summary?.commands?.failed)}{row("Commands", s => list(s.summary?.commands?.list).map(text).join("; "))}
      {row("File changes reported", s => Array.isArray(s.summary?.fileChanges) ? s.summary.fileChanges.map(text).join(", ") : s.summary?.fileChanges)}
      {row("Final agent message", s => s.summary?.finalAgentMessage)}{row("Limits", s => list(s.summary?.limits).map(text).join("; "))}
    </tbody></table>
    <h5>Version difference</h5>
    {difference.limit ? <p role="note">{text(difference.limit)}</p> : <>
      {list(difference.files).length === 0 && <p>No file differs.</p>}
      <ul>{list(difference.files).map((f: Json) => <li key={text(f.path)}>{text(f.path)}: {text(f.change)}{f.before || f.after ? ` (${short(f.before?.digest ?? f.before) || "absent"} → ${short(f.after?.digest ?? f.after) || "absent"})` : ""}{f.limit ? ` · ${text(f.limit)}` : ""}
        {(f.text || f.lines) && <pre style={{ whiteSpace: "pre-wrap" }}>{f.text ? text(f.text) : Array.isArray(f.lines) ? f.lines.map(text).join("\n") : text(f.lines)}</pre>}</li>)}</ul>
      {difference.unchanged !== undefined && <p><small>Unchanged files: {text(difference.unchanged)}.</small></p>}
      {difference.standing && <p><small>{text(difference.standing)}</small></p>}
    </>}
    <p><small>{text(result.standing) || "Shown side by side; nothing is scored or judged."}</small></p>
  </div>;
}

/** The hookless body of the drafts view: everything shown, every press. */
export function WorkflowDraftsList({ data, workspace, pointerLimits, conversations = [], runs = [], pending = [], busy, act, state, update }: { data: Json; workspace: boolean; pointerLimits?: Json; conversations?: Json[]; runs?: Json[]; pending?: Json[]; busy: boolean; act: DraftAct; state: DraftsState; update: Update }) {
  const drafts: Json[] = data?.drafts ?? [];
  const transitions: Json[] = data?.transitions ?? [];
  // Problems the host could not resolve are shown, never hidden (damaged trial
  // pointers, transitions that did not conform to the WR schema).
  const limits: string[] = [...(pointerLimits ?? []), ...(data?.transitionLimits ?? [])].map(text);
  const authoring = list(conversations).find((c: Json) => conversationKey(c) === state.authoring) ?? null;
  const runRefs: string[] = Array.from(new Set(list(runs).map((r: Json) => text(r?.reference ?? r?.run)).filter(Boolean)));
  const anyTrials = drafts.some(d => list(d.trials).some((t: Json) => t?.reference));
  const sides = state.chosen;
  const compare = () => {
    if (sides.length !== 2) return;
    update({ compareError: "" });
    void Promise.resolve(act("workflow_trial_compare", { left: JSON.parse(sides[0]), right: JSON.parse(sides[1]) })).then(
      result => update(result === undefined ? { compared: null, compareError: "Compare did not complete; see the message below." } : { compared: result }),
      error => update({ compared: null, compareError: String(error) }));
  };
  return <section aria-label="Workflow drafts">
    <h3>Workflow drafts</h3>
    <p>Drafts are folders under <code>.chirality/workflow-drafts/</code> of the open library. A draft has no workflow identity: a trial mirrors a run of its content but is never a run, and only a registered revision runs.</p>
    <button disabled={busy || !workspace} onClick={() => { void act("workflow_open_project_library", {}); }}>Open this App project’s workflow library</button>{" "}
    <button disabled={busy || !data} onClick={() => { void act("workflow_observe_drafts", {}); }}>Refresh draft list</button>
    <p><ConversationSelect label="Authoring conversation" conversations={conversations} value={state.authoring} setValue={authoring => update({ authoring })} disabled={busy} none="None chosen" />
      <small> The conversation that tries a draft with its agent, and the default place a trial is brought back to.</small></p>
    {!workspace && <p role="note">No explicit App project is configured; open a library with the folder picker below.</p>}
    {!data && <p>Open a library to list its drafts.</p>}
    {data?.state && <p>{text(data.state)}</p>}
    {data?.observedAt && <p>Listed at {text(data.observedAt)}. {text(data.standing)}.</p>}
    {data?.limit && <p role="note">{text(data.limit)}</p>}
    {limits.length > 0 && <ul role="alert" aria-label="Draft workspace limits">{limits.map(l => <li key={l}>{l}</li>)}</ul>}
    {data && !data.state && drafts.length === 0 && !data.limit && <p>No drafts in this library.</p>}
    {drafts.map(draft => <DraftRow key={text(draft.name)} draft={draft} authoring={authoring} conversations={conversations} pending={pending} busy={busy} act={act} state={state} update={update} />)}
    {(anyTrials || sides.length > 0) && <div aria-label="Compare trials">
      <h4>Compare</h4>
      <p><small>Tick two trials, or one trial and a run, then Compare. It shows them side by side with the difference between their versions; it scores and judges nothing.</small></p>
      {runRefs.length > 0 && <p>{runRefs.map(ref => { const side = runSide(ref); const ticked = sides.includes(side);
        return <label key={ref}><input type="checkbox" checked={ticked} disabled={busy} onChange={() => update({ chosen: ticked ? sides.filter(c => c !== side) : [...sides, side] })} /> run {ref} </label>; })}</p>}
      <button disabled={busy || sides.length !== 2} onClick={compare}>Compare</button>
      {sides.length > 2 && <small> Tick exactly two.</small>}
      {state.compareError && <p role="alert">{state.compareError}</p>}
      <CompareResult result={state.compared} />
    </div>}
    {transitions.length > 0 && <details><summary>Observed draft changes in this App session ({transitions.length})</summary><ul>{transitions.map((t, i) =>
      <li key={i}>{text(t.time)} · {text(t.draft?.name)}: {text(t.event)} ({text(t.from)} → {text(t.to)}); attribution {attributionWords(t.attribution)}</li>)}</ul></details>}
  </section>;
}

export function WorkflowDraftsView(props: { data: Json; workspace: boolean; pointerLimits?: Json; conversations?: Json[]; runs?: Json[]; pending?: Json[]; busy: boolean; act: DraftAct }) {
  const [state, setState] = useState<DraftsState>(initialDraftsState);
  return <WorkflowDraftsList {...props} state={state} update={patch => setState(s => ({ ...s, ...patch }))} />;
}

/** TT-13: the review's last clean trial line. Information only: it gates
 * nothing, and the registration offer beside it is unchanged. */
export function LastCleanTrialLine({ line, busy, act }: { line: Json; busy: boolean; act: DraftAct }) {
  if (!line) return null;
  const words = text(line.reading) || (line.state === "none" ? "Last clean trial: none" : `Last clean trial: ${text(line.state)}`);
  return <p aria-label="Last clean trial"><small>{words}. Information only: a clean trial is optional and gates nothing.</small>{" "}
    <button disabled={busy || !line.draftName} onClick={() => { void act("workflow_trial_prepare", { name: line.draftName, kind: "clean", generation: null, threadId: null }); }}>Try in a fresh conversation</button></p>;
}
