import { useState } from "react";
import { ModelProviderFields, RoleChoice, type SendState, type StartChoice } from "./ConversationRoles";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Trial and bring-back composers (DEL-02-02 WR §4.2 TT-3a, TT-3b, TT-10; §6
// SQ-DT, SQ-FT, SQ-BB). Under the owner's OI-008 ruling the Rust host composes
// the trial text and the transcript, pre-fills them and sends them; this view
// shows what the host pre-filled and calls a host send command only when the
// person presses Send. Nothing here sends, starts or records on its own.
//
// Each composer is a hookless view (testable by walking its element tree) and
// a thin stateful wrapper holding the person's edits.

export type TrialAct = (command: string, args: Record<string, unknown>) => Promise<unknown>;
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);

/** A conversation as the panel keys it: the generation and thread ID. */
export const conversationKey = (conversation: Json): string => conversation ? JSON.stringify([conversation.generation, conversation.threadId]) : "";
/** Only a complete native tuple can supply an implicit conversation default. */
export function conversationReference(ref: Json): Json | null {
  const g = ref?.generation;
  return typeof ref === "object" && typeof ref?.threadId === "string" && !!ref.threadId &&
    typeof g?.appSession === "string" && !!g.appSession && typeof g?.home === "string" && !!g.home &&
    Number.isSafeInteger(g?.spawnCounter) && g.spawnCounter > 0 ? { generation: g, threadId: ref.threadId } : null;
}
/** A saved bare ID is a label, even when only one loaded conversation has it. */
export function findConversation(conversations: Json[], ref: Json): Json | null {
  const source = conversationReference(ref);
  if (!source) return null;
  const matches = list(conversations).filter((c: Json) => c?.threadId === source.threadId &&
    c.generation?.appSession === source.generation.appSession && c.generation?.home === source.generation.home && c.generation?.spawnCounter === source.generation.spawnCounter);
  return matches.length === 1 ? matches[0] : null;
}
export const conversationName = (ref: Json): string => text(typeof ref === "string" ? ref : ref?.threadId) || "not reported";

/** A select over this App's started conversations. */
export function ConversationSelect({ label, conversations, value, setValue, disabled, none = "No conversation chosen" }: { label: string; conversations: Json[]; value: string; setValue: (key: string) => void; disabled?: boolean; none?: string }) {
  return <label>{label} <select value={value} disabled={disabled} onChange={e => setValue(e.target.value)}>
    <option value="">{none}</option>
    {list(conversations).map((c: Json) => <option key={conversationKey(c)} value={conversationKey(c)}>{text(c.threadId)} · {text(c.model) || "model not reported"} via {text(c.modelProvider) || "provider not reported"}</option>)}
  </select></label>;
}

/** The host's error message as given: Tauri rejects with the host's string,
 * or with a send refusal `{message, prefillKept}`. */
export const hostMessage = (error: unknown): string => {
  if (error instanceof Error) return error.message;
  const refusal = error as Json;
  if (refusal && typeof refusal === "object" && typeof refusal.message === "string") return refusal.message;
  return text(error);
};
/** Whether the host said the refused message is still pre-filled (its
 * `prefillKept` flag); anything else, including a plain string, is "no". */
export const prefillKept = (error: unknown): boolean => {
  const refusal = error as Json;
  return !!refusal && typeof refusal === "object" && !(error instanceof Error) && refusal.prefillKept === true;
};

/** Calls a host command for the person's press and turns the outcome into a
 * send state: "sent" only when the host resolved with a result, worded by
 * `sentWords` from that result; a refusal or error keeps the host's message
 * as given. */
export function pressSend(act: TrialAct, command: string, args: Record<string, unknown>, setOutcome: (outcome: SendState) => void, sentWords: (result: Json) => string): void {
  setOutcome({ state: "sending" });
  let call: Promise<unknown>;
  try { call = Promise.resolve(act(command, args)); } catch (error) { call = Promise.reject(error); }
  void call.then(
    result => setOutcome(result === undefined ? { state: "failed", failure: "The host did not report the send's outcome; see the App message." } : { state: "sent", detail: sentWords(result) }),
    error => setOutcome({ state: "failed", failure: hostMessage(error), prefillKept: prefillKept(error) }));
}

/** Success words for each trial send (WR SQ-DT DT-4, SQ-FT FT-4, SQ-BB BB-5). */
export const delegatedSentWords = (threadId: Json) => `Sent to conversation ${text(threadId)}; the trial link was written on Codex's acknowledgment`;
export const cleanSentWords = (threadId: Json) => `Sent in the new trial conversation ${text(threadId)}`;
export const bringBackSentWords = (threadId: Json) => `Transcript sent to conversation ${text(threadId)}`;

/** A trial or bring-back send's outcome in its own words. A failure shows the
 * host's message as given; "You can send it again" is added only when the
 * host's refusal carries `prefillKept: true` (the message is still pre-filled),
 * never from the message's wording. */
export function TrialSendOutcome({ outcome }: { outcome: SendState }) {
  if (outcome.state === "sending") return <p role="status"><small>Sending; waiting for Codex's acknowledgment.</small></p>;
  if (outcome.state === "sent") return <p role="status"><small>{text(outcome.detail)}.</small></p>;
  if (outcome.state === "failed") {
    const failure = text(outcome.failure);
    return <p role="alert"><small>{failure}{outcome.prefillKept === true ? " You can send it again." : ""}</small></p>;
  }
  return null;
}

/** TT-3a: the trial text as its own element. Openable and removable; never edited in place. */
export function TrialCard({ pending, busy, act }: { pending: Json; busy: boolean; act: TrialAct }) {
  return <div aria-label="Trial text" style={{ border: "1px dashed #888", padding: 6, margin: "6px 0" }}>
    <p><b>{text(pending?.card)}</b></p>
    <details><summary>Open the trial text ({text(pending?.bytes)} bytes; identity {text(pending?.textIdentity?.value ?? pending?.textIdentity).slice(0, 12)})</summary><pre style={{ whiteSpace: "pre-wrap" }}>{text(pending?.text)}</pre></details>
    <p><small>Not editable here: to change it, change the draft and Try again. Removing it cancels the trial; nothing is recorded.</small>{" "}
      <button disabled={busy} onClick={() => { void Promise.resolve(act("workflow_trial_cancel", { reference: pending?.reference })).catch(() => undefined); }}>Remove</button></p>
  </div>;
}

function PendingNotes({ pending }: { pending: Json }) {
  return <>
    {pending?.authoringLimit && <p role="note">{text(pending.authoringLimit)}</p>}
    {pending?.delegation && pending.delegation.reading !== "present" && <p role="note">Delegation {text(pending.delegation.reading)}: {text(pending.delegation.reason)}</p>}
    {pending?.runInForce && <p role="note">{text(pending.runInForce)}</p>}
    {pending?.draftChanged && <p role="note">{text(pending.draftChanged)}</p>}
    {pending?.limit && <p role="note">{text(pending.limit)}</p>}
    <p><small>Proposed work folder: <code>{text(pending?.workFolder)}</code> (the App enforces nothing). A trial is not a workflow run, registration, checking or acceptance.</small></p>
  </>;
}

/** TT-3a, SQ-DT DT-3/DT-4: the delegated trial pre-filled in the authoring conversation. */
export function DelegatedTrialComposerView({ pending, conversations, message, setMessage, target, setTarget, outcome, setOutcome, busy, ready, act }: {
  pending: Json; conversations: Json[]; message: string; setMessage: (m: string) => void; target: string; setTarget: (key: string) => void;
  outcome: SendState; setOutcome: (o: SendState) => void; busy: boolean; ready: boolean; act: TrialAct;
}) {
  const chosen = list(conversations).find((c: Json) => conversationKey(c) === target) ?? null;
  const sent = outcome.state === "sending" || outcome.state === "sent";
  return <section aria-label="Trial composer" style={{ border: "1px solid #888", padding: 8, margin: "8px 0" }}>
    <h3>Trial {text(pending?.sequence)} of draft {text(pending?.draftName)} — pre-filled, not sent</h3>
    <label>Your message (editable; not sent) <textarea value={message} disabled={busy || sent} onChange={e => setMessage(e.target.value)} rows={6} style={{ display: "block", width: "100%" }} /></label>
    <TrialCard pending={pending} busy={busy || sent} act={act} />
    <PendingNotes pending={pending} />
    <p><ConversationSelect label="Send to" conversations={conversations} value={target} setValue={setTarget} disabled={busy || sent} />{" "}
      <button disabled={busy || !ready || !chosen || sent} onClick={() => pressSend(act, "workflow_trial_send", { reference: pending?.reference, generation: chosen?.generation, threadId: chosen?.threadId, personText: message }, setOutcome, () => delegatedSentWords(chosen?.threadId))}>Send</button></p>
    <TrialSendOutcome outcome={outcome} />
  </section>;
}

export function DelegatedTrialComposer({ pending, conversations, busy, ready, act }: { pending: Json; conversations: Json[]; busy: boolean; ready: boolean; act: TrialAct }) {
  const [message, setMessage] = useState<string>(text(pending?.message));
  const [target, setTarget] = useState<string>(conversationKey(findConversation(conversations, pending?.authoring)));
  const [outcome, setOutcome] = useState<SendState>({ state: "unsent" });
  return <DelegatedTrialComposerView pending={pending} conversations={conversations} message={message} setMessage={setMessage} target={target} setTarget={setTarget} outcome={outcome} setOutcome={setOutcome} busy={busy} ready={ready} act={act} />;
}

export type CleanChoice = StartChoice & { role: string; roleTouched: boolean };

/** TT-3b, SQ-FT FT-3/FT-4: a new trial conversation, like Continue as but
 * without a handoff turn. Its role and model are the person's; it starts and
 * the trial message is sent only when the person presses Send. */
export function CleanTrialPanelView({ pending, roleSet, limits, entries, modeHomeClass, choice, setChoice, message, setMessage, outcome, setOutcome, busy, ready, act }: {
  pending: Json; roleSet: Json; limits: Json; entries: { value: string; label: string }[]; modeHomeClass: Json;
  choice: CleanChoice; setChoice: (c: CleanChoice) => void; message: string; setMessage: (m: string) => void;
  outcome: SendState; setOutcome: (o: SendState) => void; busy: boolean; ready: boolean; act: TrialAct;
}) {
  const started = pending?.cleanConversation && pending?.state === "started; trial message not sent" ? pending.cleanConversation : null;
  const sent = outcome.state === "sending" || outcome.state === "sent";
  const noModel = !choice.model.trim() || !choice.modelProvider.trim();
  return <section aria-label="New trial conversation" style={{ border: "1px solid #888", padding: 8, margin: "8px 0" }}>
    <h3>New trial conversation: trial {text(pending?.sequence)} of draft {text(pending?.draftName)}</h3>
    <p><small>Optional: a clean trial is shown, not required. It is a new conversation with the role and model you choose and nothing but the trial text and your inputs.</small></p>
    <TrialCard pending={pending} busy={busy || sent} act={act} />
    <label>Inputs for this trial (editable; not sent) <textarea value={message} disabled={busy || sent} onChange={e => setMessage(e.target.value)} rows={4} style={{ display: "block", width: "100%" }} /></label>
    <PendingNotes pending={pending} />
    {started ? <div>
      <p>Trial conversation {conversationName(started)} started; the trial message was not sent. Send sends it to that conversation.</p>
      <button disabled={busy || !ready || sent} onClick={() => pressSend(act, "workflow_trial_send", { reference: pending?.reference, generation: started.generation, threadId: started.threadId, personText: message }, setOutcome, () => cleanSentWords(started.threadId))}>Send</button>
    </div> : <div>
      <RoleChoice group={`clean-trial-role:${text(pending?.reference)}`} roleSet={roleSet} limits={limits} role={choice.role} preselected={!choice.roleTouched && !!choice.role && choice.role === roleSet?.defaultRole}
        setRole={role => setChoice({ ...choice, role, roleTouched: true })} />
      <p>The new conversation starts with no model selected; choose one.</p>
      <ModelProviderFields model={choice.model} modelProvider={choice.modelProvider}
        setModel={model => setChoice({ ...choice, model })} setModelProvider={modelProvider => setChoice({ ...choice, modelProvider })} />{" "}
      <label>Access entry <select value={choice.entryId} onChange={e => setChoice({ ...choice, entryId: e.target.value })}><option value="">No entry selected</option>{entries.map(e => <option key={e.value} value={e.value}>{e.label}</option>)}</select></label>
      <p><button disabled={busy || !ready || noModel || !choice.entryId || sent} onClick={() => pressSend(act, "workflow_trial_start_clean", { reference: pending?.reference, model: choice.model, modelProvider: choice.modelProvider, entryId: choice.entryId, modeHomeClass, role: choice.role === "" ? null : choice.role, personText: message }, setOutcome, result => cleanSentWords(result?.thread?.threadId ?? result?.conversation?.threadId ?? "not named by the host"))}>Send</button>
        <small> Starts the new conversation, then sends the trial text and your inputs once.</small></p>
      {noModel && <p><small>Not started — no model selected.</small></p>}
    </div>}
    <TrialSendOutcome outcome={outcome} />
  </section>;
}

export function CleanTrialPanel({ pending, roleSet, limits, entries, modeHomeClass, busy, ready, act }: { pending: Json; roleSet: Json; limits: Json; entries: { value: string; label: string }[]; modeHomeClass: Json; busy: boolean; ready: boolean; act: TrialAct }) {
  const [choice, setChoice] = useState<CleanChoice>({ model: "", modelProvider: "", entryId: "", role: roleSet?.available ? text(roleSet.defaultRole) : "", roleTouched: false });
  const [message, setMessage] = useState<string>(text(pending?.message));
  const [outcome, setOutcome] = useState<SendState>({ state: "unsent" });
  return <CleanTrialPanelView pending={pending} roleSet={roleSet} limits={limits} entries={entries} modeHomeClass={modeHomeClass} choice={choice} setChoice={setChoice}
    message={message} setMessage={setMessage} outcome={outcome} setOutcome={setOutcome} busy={busy} ready={ready} act={act} />;
}

/** The bring-back composer's title: a trial by its sequence and draft, as
 * elsewhere (never its internal reference); a run by its reference. */
export function bringBackTitle(pending: Json): string {
  if (!pending?.trial) return `Bring run ${text(pending?.run)} back`;
  const n = pending.sequence === null || pending.sequence === undefined ? "" : ` ${text(pending.sequence)}`;
  const draft = text(pending.draftName) ? ` of draft ${text(pending.draftName)}` : "";
  return `Bring trial${n}${draft} back`;
}

/** TT-10, SQ-BB BB-4/BB-5: a transcript pre-filled in the target conversation. */
export function BringBackComposerView({ pending, conversations, prompt, setPrompt, target, setTarget, outcome, setOutcome, busy, ready, act }: {
  pending: Json; conversations: Json[]; prompt: string; setPrompt: (p: string) => void; target: string; setTarget: (key: string) => void;
  outcome: SendState; setOutcome: (o: SendState) => void; busy: boolean; ready: boolean; act: TrialAct;
}) {
  const chosen = list(conversations).find((c: Json) => conversationKey(c) === target) ?? null;
  const sent = outcome.state === "sending" || outcome.state === "sent";
  const shortenings = list(pending?.shortenings);
  return <section aria-label="Bring back composer" style={{ border: "1px solid #888", padding: 8, margin: "8px 0" }}>
    <h3>{bringBackTitle(pending)} — pre-filled, not sent</h3>
    <label>Your message (editable; not sent) <textarea value={prompt} disabled={busy || sent} onChange={e => setPrompt(e.target.value)} rows={4} style={{ display: "block", width: "100%" }} /></label>
    <div aria-label="Transcript" style={{ border: "1px dashed #888", padding: 6, margin: "6px 0" }}>
      <p><b>{text(pending?.card)}</b></p>
      <details><summary>Open the transcript ({text(pending?.bytes)} bytes{pending?.includeNative ? "; native items included" : ""})</summary><pre style={{ whiteSpace: "pre-wrap" }}>{text(pending?.transcript)}</pre></details>
      {pending?.source?.standing && <p><small>{text(pending.source.standing)}</small></p>}
      {list(pending?.source?.limits).length > 0 && <ul aria-label="History source limits">{list(pending.source.limits).map((limit, i) => <li key={i}><small>{text(limit)}</small></li>)}</ul>}
      {shortenings.length > 0 && <ul aria-label="Shortenings">{shortenings.map((s: Json, i: number) => <li key={i}><small>{text(s)}</small></li>)}</ul>}
      <p><small>Read from Codex history; a record of that conversation, it instructs nothing. Not editable here.</small>{" "}
        <button disabled={busy || sent} onClick={() => { void Promise.resolve(act("workflow_bring_back_cancel", { id: pending?.id })).catch(() => undefined); }}>Remove</button></p>
    </div>
    <p><ConversationSelect label="Send to" conversations={conversations} value={target} setValue={setTarget} disabled={busy || sent} />{" "}
      <button disabled={busy || !ready || !chosen || sent} onClick={() => pressSend(act, "workflow_bring_back_send", { id: pending?.id, generation: chosen?.generation, threadId: chosen?.threadId, personText: prompt }, setOutcome, () => bringBackSentWords(chosen?.threadId))}>Send</button></p>
    <TrialSendOutcome outcome={outcome} />
  </section>;
}

export function BringBackComposer({ pending, conversations, busy, ready, act }: { pending: Json; conversations: Json[]; busy: boolean; ready: boolean; act: TrialAct }) {
  const [prompt, setPrompt] = useState<string>(text(pending?.prompt));
  const [target, setTarget] = useState<string>(conversationKey(findConversation(conversations, pending?.target)));
  const [outcome, setOutcome] = useState<SendState>({ state: "unsent" });
  return <BringBackComposerView pending={pending} conversations={conversations} prompt={prompt} setPrompt={setPrompt} target={target} setTarget={setTarget} outcome={outcome} setOutcome={setOutcome} busy={busy} ready={ready} act={act} />;
}

/** Which pending composers belong in the selected conversation's panel. */
export function composersFor(workflowRoot: Json, selected: Json): { delegated: Json[]; clean: Json[]; bringBacks: Json[] } {
  const same = (ref: Json) => !!findConversation(selected ? [selected] : [], ref);
  const pending = list(workflowRoot?.pendingTrials);
  return {
    delegated: pending.filter((p: Json) => p?.kind === "delegated" && same(p.authoring)),
    clean: pending.filter((p: Json) => p?.kind === "clean"),
    bringBacks: list(workflowRoot?.pendingBringBacks).filter((b: Json) => same(b?.target)),
  };
}
