import { createContext, useContext, useLayoutEffect, useRef, useState } from "react";
import { AgentText, Word, numberWords } from "./AgentText";
import { EXACT_TEXT } from "./exactText";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// The agent's question that does not wait (Codex's request_user_input_async):
// it arrives as an agent message carrying questions, the turn goes on, and
// nothing waits on an answer. The person's answer is their ordinary next
// message in that conversation, sent through the conversation's own send path
// and only on their press. Every title and option is the agent's text and is
// drawn through AgentText; every control carries the App's words.

/** One question as the agent gave it: a title, and options or none. */
export type AskedQuestionText = { title: string; options?: string[] | null };
/** The question item: its conversation, turn and item, and its questions. */
export type AskedQuestionEntry = { threadId: string; turnId: string; itemId: string; questions: AskedQuestionText[] };
/** What is established about it: waiting on the person (it is the conversation's waiting entry); a message from the
 * person follows it (the reading names this item as one the App observed a message from the person after); another
 * question of the agent's in the same conversation is the waiting entry (whether a message from the person follows this
 * one is not established); the conversation is read and nothing waits there, but the reading does not name this item as
 * followed (whether a message from the person follows it is not established); or the conversation's later messages are
 * not read. */
export type AskedStanding = "waiting" | "followed" | "another" | "not-established" | "not-read";
/** Why the card cannot send now, in the App's words (ASKED_UNAVAILABLE). */
export type AskedUnavailable = "not-connected" | "busy" | "unconfirmed" | "other-conversation" | "no-send" | "nothing-to-send" | "stale";
/** What the conversation's send path reported: sent, not sent for a reason the App names, or a failure as reported. */
export type AskedSendResult = { sent: true } | { sent: false; unavailable: AskedUnavailable } | { sent: false; reported: string };
/** The conversation view a card was drawn in, as the send path captured it then (opaque to the card): a press sends
 * only while it is still the view shown. */
export type AskedBinding = { owner: string; epoch: number; attempts: number };
export type AskedSend = (threadId: string, text: string, binding: AskedBinding | null) => Promise<AskedSendResult>;

export const ASKED_UNAVAILABLE = {
  "not-connected": "Connect to Codex before sending. Your answers stay here.",
  busy: "An operation is pending. Sending is paused until its result is received. Your answers stay here.",
  unconfirmed: "An earlier message to this conversation wasn't confirmed and may have been sent. Read the conversation, then confirm below the message box before sending again. Your answers stay here.",
  "other-conversation": "Open this conversation to send your answer there. Your answers stay here.",
  "no-send": "Answers can be sent from the conversation's own view.",
  "nothing-to-send": "Answer at least one question to send.",
  stale: "That press belonged to an earlier view of the conversation or to earlier answers. Check your answers, then press Send answers again. Your answers stay here.",
} as const;
const STANDING_WORDS = {
  waiting: "The agent asked this and went on: its turn did not wait for you. Your answer is sent as your next message in this conversation.",
  "not-read": "The agent asked this and went on: its turn did not wait for you. Your answer is sent as your next message in this conversation.",
  followed: "The agent asked this and went on: its turn did not wait for you.",
  another: "The agent asked this and went on: its turn did not wait for you.",
  "not-established": "The agent asked this and went on: its turn did not wait for you.",
} as const;
const DELEGATED = "This question was asked in a delegated agent's conversation. Chirality sends no answer there; the agent you are talking with can relay it.";

/** Each question's answer as the person gave it: the option chosen (by index), or the text typed. */
export type AskedAnswers = { chosen: Readonly<Partial<Record<number, number | null>>>; typed: Readonly<Partial<Record<number, string | null>>> };

/** The answer to one question, or null where it is unanswered. Typed text that is not only white space is the
 * answer, exactly as typed; otherwise a chosen option (its place and text, exactly as the agent gave it). */
function answerFor(question: AskedQuestionText, chosen: number | null | undefined, typed: string | null | undefined): { typed: string } | { option: number; text: string } | null {
  if (typeof typed === "string" && typed.trim() !== "") return { typed };
  const options = Array.isArray(question.options) ? question.options : [];
  if (typeof chosen === "number" && Number.isInteger(chosen) && chosen >= 0 && chosen < options.length && typeof options[chosen] === "string") return { option: chosen, text: options[chosen] };
  return null;
}

/** The exact text sent as the person's message. For each answered question: the line `You asked: ` and its title
 * quoted as a JSON string; then either `I choose your option N: ` and the option's text quoted the same way, or
 * `My answer: ` and the person's text, exactly as typed, quoted the same way on the same line. Questions are separated
 * by one blank line; unanswered questions are left out. Quoting keeps every line break, carriage return and quote of
 * the agent's text and of the person's inside one line, so neither can read as another line of the message (a second
 * answer, or a question the App quoted). Empty when none is answered. */
export function askedQuestionReply(questions: readonly AskedQuestionText[], answers: AskedAnswers): string {
  // A question without a title as text is never sent: nothing the App cannot quote exactly goes into the message.
  return (Array.isArray(questions) ? questions : []).flatMap((question, i) => {
    if (typeof question?.title !== "string") return [];
    const answer = answerFor(question, answers.chosen[i], answers.typed[i]);
    if (answer === null) return [];
    const asked = `You asked: ${JSON.stringify(question.title)}`;
    return ["typed" in answer ? `${asked}\nMy answer: ${JSON.stringify(answer.typed)}` : `${asked}\nI choose your option ${answer.option + 1}: ${JSON.stringify(answer.text)}`];
  }).join("\n\n");
}

/** The questions of an item, where each has the pinned shape (a title, and options as text or absent); else null. */
export function askedQuestionsOf(value: Json): AskedQuestionText[] | null {
  if (!Array.isArray(value) || value.length === 0) return null;
  const out: AskedQuestionText[] = [];
  for (const q of value) {
    if (!q || typeof q !== "object" || Array.isArray(q) || typeof q.title !== "string") return null;
    if (Object.keys(q).some(k => k !== "title" && k !== "options")) return null;
    if (q.options !== undefined && q.options !== null && !(Array.isArray(q.options) && q.options.every((o: Json) => typeof o === "string"))) return null;
    out.push({ title: q.title, options: q.options ?? null });
  }
  return out;
}

const sameItem = (a: Json, entry: Pick<AskedQuestionEntry, "threadId" | "turnId" | "itemId">) =>
  a?.threadId === entry.threadId && a?.turnId === entry.turnId && a?.itemId === entry.itemId;

/** The standing of one question item, read from a home's native view snapshot (its askedQuestions). A view whose
 * observation has ended is not a current reading: the conversation's later messages are then not read. A message
 * from the person follows the item only where `askedQuestions.followed` names that item (the one question, per read
 * conversation with no waiting question, that the App observed a message from the person after); a missing or
 * malformed `followed` names nothing. */
export function askedStanding(view: Json, entry: Pick<AskedQuestionEntry, "threadId" | "turnId" | "itemId">): AskedStanding {
  const asked = view?.askedQuestions;
  if (!view || view.observationEnded === true || !Array.isArray(asked?.read) || !asked.read.includes(entry.threadId)) return "not-read";
  const waiting = (Array.isArray(asked.waiting) ? asked.waiting : []).find((w: Json) => w?.threadId === entry.threadId);
  if (waiting) return sameItem(waiting, entry) ? "waiting" : "another";
  return Array.isArray(asked.followed) && asked.followed.some((f: Json) => sameItem(f, entry)) ? "followed" : "not-established";
}

const delegatedSource = (source: Json) => !!source && typeof source === "object" && !Array.isArray(source) && Object.hasOwn(source, "subAgent");

/** Whether a conversation is part of the agent's question that does not wait: an admitted top-level conversation of
 * the status's current generation. Its row is in the status's conversations (`threads`, which must be a list) with
 * that generation, and no sign the status gives marks it as a delegated agent's: no row for it names a parent or a
 * delegated agent's source (`threadSource.subAgent`), and the native view does not list it among descendants. The one
 * rule for coverage, the list's entries, the card's answer control and the send. */
export function askedAdmittedTopLevel(status: Json, threadId: unknown): boolean {
  if (typeof threadId !== "string" || threadId === "" || !Array.isArray(status?.threads)) return false;
  const generation = JSON.stringify(status?.generation);
  const rows: Json[] = status.threads.filter((t: Json) => t?.threadId === threadId);
  if (!rows.some((t: Json) => JSON.stringify(t?.generation) === generation)) return false;
  if (rows.some((t: Json) => (typeof t?.parentThreadId === "string" && t.parentThreadId !== "") || delegatedSource(t?.threadSource))) return false;
  const descendants: Json[] = Array.isArray(status?.nativeView?.descendants) ? status.nativeView.descendants : [];
  return !descendants.some((d: Json) => d?.threadId === threadId);
}

export function AskedQuestionCard({ entry, standing, send, binding = null, pending, unavailable, delegated = false }: { entry: AskedQuestionEntry; standing: AskedStanding; send?: AskedSend; binding?: AskedBinding | null; pending: boolean; unavailable: AskedUnavailable | null; delegated?: boolean }) {
  // What the person types and which offered option they chose, kept apart per question (by its place): an option's
  // text is the agent's and never enters a field the person types in.
  const [chosen, setChosen] = useState<Record<number, number>>({});
  const [typed, setTyped] = useState<Record<number, string>>({});
  const [sending, setSending] = useState(false);
  const [outcome, setOutcome] = useState<AskedSendResult | null>(null);
  // A question in a delegated agent's conversation is shown for information only: nothing is sent there from here.
  // Answer fields are drawn only where an answer can go: in the conversation's own view, which hands the card its send.
  // Anywhere else (a stored item page in History) the card says where answers are sent from and draws no field.
  const offersAnswer = !delegated && (standing === "waiting" || standing === "not-read");
  const answering = offersAnswer && !!send;
  const questions: AskedQuestionText[] = Array.isArray(entry?.questions) ? entry.questions : [];
  const reply = askedQuestionReply(questions, { chosen, typed });
  // The text of the committed drawing (set at commit, below). A press drawn with other answers (a handler kept from an
  // earlier drawing) sends nothing; a drawing that was made and not committed changes nothing for the button shown.
  const current = useRef(reply);
  const blocked: AskedUnavailable | null = !send ? "no-send" : unavailable;
  // A press belongs to one committed control that offers Send, once. Each drawing makes its own binding; the commit of
  // a drawing that offers Send makes that binding the live one, and any other commit, or unmounting, leaves none live.
  // A press acts only while its binding is live, and uses it before it sends: a handler kept from another drawing, from
  // a card whose standing no longer offers an answer, from a card no longer mounted, or from a press already made,
  // sends nothing. A later drawing that offers Send has a fresh binding, so the person can press again after a failure.
  const offered = answering && !!send && reply !== "" && !sending && !pending && !blocked;
  const livePress = useRef<{ used: boolean } | null>(null);
  const answeringNow = useRef(false);
  const pressBinding = { used: false };
  useLayoutEffect(() => {
    livePress.current = offered ? pressBinding : null;
    current.current = reply;
    answeringNow.current = answering;
    return () => { livePress.current = null; answeringNow.current = false; };
  });
  const choose = (i: number, option: number) => { setChosen(c => ({ ...c, [i]: option })); setTyped(t => { const next = { ...t }; delete next[i]; return next; }); setOutcome(null); };
  const clear = (i: number) => { setChosen(c => { const next = { ...c }; delete next[i]; return next; }); setTyped(t => { const next = { ...t }; delete next[i]; return next; }); setOutcome(null); };
  const press = async () => {
    if (pressBinding.used) return;
    // The text sent is exactly the preview shown with this press.
    const text = reply;
    if (livePress.current !== pressBinding || text !== current.current) {
      // Said only where the card still offers answering; a card that no longer does says nothing of an old press.
      if (answeringNow.current) setOutcome({ sent: false, unavailable: "stale" });
      return;
    }
    if (!send || !text || sending || pending || blocked) return;
    pressBinding.used = true; livePress.current = null;
    setSending(true); setOutcome(null);
    let result: AskedSendResult;
    try { result = await send(entry?.threadId, text, binding); }
    catch (error) { result = { sent: false, reported: error instanceof Error ? error.message : String(error) }; }
    setOutcome(result);
    // A failed send keeps every answer; a sent one leaves the fields empty.
    if (result.sent) { setChosen({}); setTyped({}); }
    setSending(false);
  };
  return <div className="asked-question-card" aria-label="The agent's question">
    {delegated ? <p><b>Question from the agent</b> · {DELEGATED}</p> : <>
      <p><b>Question from the agent</b> · <Word value={standing} words={STANDING_WORDS} source="record" label="Recorded:" name="A standing the App does not recognise" /></p>
      {standing === "followed" && <p>A message from you follows this question.</p>}
      {standing === "another" && <p>Chirality cannot establish whether a message from you follows this question. Another question the agent asked in this conversation is the one listed under "Waiting on you".</p>}
      {standing === "not-established" && <p>Chirality cannot establish whether a message from you follows this question.</p>}
      {standing === "not-read" && <p>Chirality has not read this conversation's later messages, so it cannot say whether you replied.</p>}
    </>}
    {questions.map((question, i) => {
      const options: Json[] = Array.isArray(question?.options) ? question.options : [];
      return <div key={i}>
        <p>Question {i + 1}: <AgentText value={question?.title} label={`Question ${i + 1}:`} /></p>
        {answering ? <>
          {/* The option's text is the agent's: the button carries the App's words and the text stands beside it. */}
          {options.map((option, k) => <div key={k}><button disabled={sending} onClick={() => choose(i, k)}>Choose option {k + 1}</button>{" "}<AgentText value={option} label={`Option ${k + 1}:`} /></div>)}
          <label>Your own answer <textarea {...EXACT_TEXT} rows={2} disabled={sending} value={typed[i] ?? ""} onChange={e => { const value = e.target.value; setTyped(t => ({ ...t, [i]: value })); setChosen(c => { const next = { ...c }; delete next[i]; return next; }); setOutcome(null); }} /></label>
          <button disabled={sending} onClick={() => clear(i)}>Leave unanswered</button>
          <p>Selected: {(typed[i] ?? "").trim() !== "" ? "your own answer, in the field above" : chosen[i] !== undefined ? <>{`option ${numberWords((chosen[i] ?? 0) + 1) ?? ""} `}<AgentText value={options[chosen[i] ?? 0]} label="Its text:" /></> : "—"}</p>
        </> : options.map((option, k) => <div key={k}>Option {k + 1}: <AgentText value={option} label={`Option ${k + 1}:`} /></div>)}
      </div>;
    })}
    {offersAnswer && !send && <p><Word value="no-send" words={ASKED_UNAVAILABLE} source="record" label="Recorded:" name="A reason the App does not recognise" /></p>}
    {answering && <>
      {reply !== "" && <div><p>This is sent as your message, exactly:</p><AgentText block exactLineEnds value={reply} source="record" label="Your message, as it will be sent:" name="The message the App will send for you: the agent's questions and your answers" /></div>}
      <button className="setup-primary" disabled={reply === "" || sending || pending || !!blocked} onClick={() => { void press(); }}>Send answers</button>
      {blocked && <p><Word value={blocked} words={ASKED_UNAVAILABLE} source="record" label="Recorded:" name="A reason the App does not recognise" /></p>}
      {sending && <p role="status">Sending your answers as your message.</p>}
      {outcome?.sent === true && <p role="status">Sent as your message in this conversation. The agent's reply, if any, appears in the conversation.</p>}
      {outcome && outcome.sent === false && "unavailable" in outcome && <p role="alert">Not sent. <Word value={outcome.unavailable} words={ASKED_UNAVAILABLE} source="record" label="Recorded:" name="A reason the App does not recognise" /></p>}
      {outcome && outcome.sent === false && "reported" in outcome && <p role="alert">The App couldn't confirm the send; it may or may not have been sent. Your answers stay here. <AgentText value={outcome.reported} source="record" label="Reported:" name="What the send reported, not the App's words" /></p>}
    </>}
  </div>;
}

/** What the conversation's view hands every card it draws: the native view snapshot, the host status it came with (for
 * askedAdmittedTopLevel), the conversation shown, the send path with the view it is bound to now, and whether a send is
 * pending or unavailable. Absent outside a conversation's own view, where nothing is sent from a card. */
export type AskedQuestionHost = { view: Json; status: Json; threadId: string | null; send: AskedSend; binding: AskedBinding | null; pending: boolean; unavailable: AskedUnavailable | null };
export const AskedQuestionContext = createContext<AskedQuestionHost | null>(null);

/** The card at a completed agent message that carries questions with delivery "async"; nothing for any other item.
 * At an item of another conversation than the one shown (a delegated agent's), or of one that is not an admitted
 * top-level conversation (askedAdmittedTopLevel), the card is information only. */
export function AskedQuestionMount({ row }: { row: Json }) {
  const host = useContext(AskedQuestionContext);
  const n = row?.native;
  if (row?.displayState !== "completed" || n?.type !== "agentMessage" || n.delivery !== "async" || !Array.isArray(n.questions) || n.questions.length === 0) return null;
  const questions = askedQuestionsOf(n.questions);
  if (!questions || typeof row.threadId !== "string" || typeof row.turnId !== "string" || typeof n.id !== "string") return <p>This message carries questions the App cannot read; Codex's item is shown as sent.</p>;
  const entry: AskedQuestionEntry = { threadId: row.threadId, turnId: row.turnId, itemId: n.id, questions };
  const delegated = !!host && typeof host.threadId === "string" && (row.threadId !== host.threadId || !askedAdmittedTopLevel(host.status, row.threadId));
  return <AskedQuestionCard key={JSON.stringify([row.threadId, row.turnId, n.id])} entry={entry} standing={askedStanding(host?.view, entry)} delegated={delegated}
    send={host?.send} binding={host?.binding ?? null} pending={host?.pending ?? false} unavailable={host ? host.unavailable : "no-send"} />;
}
