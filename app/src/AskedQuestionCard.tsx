import { createContext, useContext, useState } from "react";
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
/** What is established about it: waiting on the person; a message from the person follows it; a later question of
 * the agent's in the same conversation is the one waiting; or the conversation's later messages are not read. */
export type AskedStanding = "waiting" | "followed" | "superseded" | "not-read";
/** Why the card cannot send now, in the App's words (ASKED_UNAVAILABLE). */
export type AskedUnavailable = "not-connected" | "busy" | "unconfirmed" | "other-conversation" | "no-send" | "nothing-to-send";
/** What the conversation's send path reported: sent, not sent for a reason the App names, or a failure as reported. */
export type AskedSendResult = { sent: true } | { sent: false; unavailable: AskedUnavailable } | { sent: false; reported: string };
export type AskedSend = (threadId: string, text: string) => Promise<AskedSendResult>;

export const ASKED_UNAVAILABLE = {
  "not-connected": "Connect to Codex before sending. Your answers stay here.",
  busy: "An operation is pending. Sending is paused until its result is received. Your answers stay here.",
  unconfirmed: "An earlier message to this conversation wasn't confirmed and may have been sent. Read the conversation, then confirm below the message box before sending again. Your answers stay here.",
  "other-conversation": "Open this conversation to send your answer there. Your answers stay here.",
  "no-send": "Answers can be sent from the conversation's own view.",
  "nothing-to-send": "Answer at least one question to send.",
} as const;
const STANDING_WORDS = {
  waiting: "The agent asked this and went on: its turn did not wait for you. Your answer is sent as your next message in this conversation.",
  "not-read": "The agent asked this and went on: its turn did not wait for you. Your answer is sent as your next message in this conversation.",
  followed: "The agent asked this and went on: its turn did not wait for you.",
  superseded: "The agent asked this and went on: its turn did not wait for you.",
} as const;

/** Each question's answer as the person gave it: the option chosen (by index), or the text typed. */
export type AskedAnswers = { chosen: Readonly<Partial<Record<number, number | null>>>; typed: Readonly<Partial<Record<number, string | null>>> };

/** The answer to one question, or null where it is unanswered. Typed text that is not only white space is the
 * answer, exactly as typed; otherwise a chosen option's text, exactly as the agent gave it. */
function answerFor(question: AskedQuestionText, chosen: number | null | undefined, typed: string | null | undefined): string | null {
  if (typeof typed === "string" && typed.trim() !== "") return typed;
  const options = Array.isArray(question.options) ? question.options : [];
  if (typeof chosen === "number" && Number.isInteger(chosen) && chosen >= 0 && chosen < options.length && typeof options[chosen] === "string") return options[chosen];
  return null;
}

/** The exact text sent as the person's message: for each answered question, its title on one line and the answer on
 * the next; questions separated by a blank line; unanswered questions left out. Empty when none is answered. */
export function askedQuestionReply(questions: readonly AskedQuestionText[], answers: AskedAnswers): string {
  // A question without a title as text is never sent: nothing the App cannot quote exactly goes into the message.
  return (Array.isArray(questions) ? questions : []).flatMap((question, i) => {
    if (typeof question?.title !== "string") return [];
    const answer = answerFor(question, answers.chosen[i], answers.typed[i]);
    return answer === null ? [] : [`${question.title}\n${answer}`];
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

/** The standing of one question item, read from a home's native view snapshot (its askedQuestions). A view whose
 * observation has ended is not a current reading: the conversation's later messages are then not read. */
export function askedStanding(view: Json, entry: Pick<AskedQuestionEntry, "threadId" | "turnId" | "itemId">): AskedStanding {
  const asked = view?.askedQuestions;
  if (!view || view.observationEnded === true || !Array.isArray(asked?.read) || !asked.read.includes(entry.threadId)) return "not-read";
  const waiting = (Array.isArray(asked.waiting) ? asked.waiting : []).find((w: Json) => w?.threadId === entry.threadId);
  if (!waiting) return "followed";
  return waiting.turnId === entry.turnId && waiting.itemId === entry.itemId ? "waiting" : "superseded";
}

export function AskedQuestionCard({ entry, standing, send, pending, unavailable }: { entry: AskedQuestionEntry; standing: AskedStanding; send?: AskedSend; pending: boolean; unavailable: AskedUnavailable | null }) {
  // What the person types and which offered option they chose, kept apart per question (by its place): an option's
  // text is the agent's and never enters a field the person types in.
  const [chosen, setChosen] = useState<Record<number, number>>({});
  const [typed, setTyped] = useState<Record<number, string>>({});
  const [sending, setSending] = useState(false);
  const [outcome, setOutcome] = useState<AskedSendResult | null>(null);
  const answering = standing === "waiting" || standing === "not-read";
  const questions: AskedQuestionText[] = Array.isArray(entry?.questions) ? entry.questions : [];
  const reply = askedQuestionReply(questions, { chosen, typed });
  const blocked: AskedUnavailable | null = !send ? "no-send" : unavailable;
  const choose = (i: number, option: number) => { setChosen(c => ({ ...c, [i]: option })); setTyped(t => { const next = { ...t }; delete next[i]; return next; }); setOutcome(null); };
  const clear = (i: number) => { setChosen(c => { const next = { ...c }; delete next[i]; return next; }); setTyped(t => { const next = { ...t }; delete next[i]; return next; }); setOutcome(null); };
  const press = async () => {
    // The text sent is exactly the preview shown with this press.
    const text = reply;
    if (!send || !text || sending || pending || blocked) return;
    setSending(true); setOutcome(null);
    let result: AskedSendResult;
    try { result = await send(entry?.threadId, text); }
    catch (error) { result = { sent: false, reported: error instanceof Error ? error.message : String(error) }; }
    setOutcome(result);
    // A failed send keeps every answer; a sent one leaves the fields empty.
    if (result.sent) { setChosen({}); setTyped({}); }
    setSending(false);
  };
  return <div className="asked-question-card" aria-label="The agent's question">
    <p><b>Question from the agent</b> · <Word value={standing} words={STANDING_WORDS} source="record" label="Recorded:" name="A standing the App does not recognise" /></p>
    {standing === "followed" && <p>A message from you follows this question.</p>}
    {standing === "superseded" && <p>The agent asked a later question in this conversation; that one is the question waiting.</p>}
    {standing === "not-read" && <p>Chirality has not read this conversation's later messages, so it cannot say whether you replied.</p>}
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
    {answering && <>
      {reply !== "" && <div><p>This is sent as your message, exactly:</p><AgentText block value={reply} source="record" label="Your message, as it will be sent:" name="The message the App will send for you: the agent's questions and your answers" /></div>}
      <button className="setup-primary" disabled={reply === "" || sending || pending || !!blocked} onClick={() => { void press(); }}>Send answers</button>
      {blocked && <p><Word value={blocked} words={ASKED_UNAVAILABLE} source="record" label="Recorded:" name="A reason the App does not recognise" /></p>}
      {sending && <p role="status">Sending your answers as your message.</p>}
      {outcome?.sent === true && <p role="status">Sent as your message in this conversation. The agent's reply, if any, appears in the conversation.</p>}
      {outcome && outcome.sent === false && "unavailable" in outcome && <p role="alert">Not sent. <Word value={outcome.unavailable} words={ASKED_UNAVAILABLE} source="record" label="Recorded:" name="A reason the App does not recognise" /></p>}
      {outcome && outcome.sent === false && "reported" in outcome && <p role="alert">The App couldn't confirm the send; it may or may not have been sent. Your answers stay here. <AgentText value={outcome.reported} source="record" label="Reported:" name="What the send reported, not the App's words" /></p>}
    </>}
  </div>;
}

/** What the conversation's view hands every card it draws: the native view snapshot, the send path, and whether a
 * send is pending or unavailable. Absent outside a conversation's own view, where nothing is sent from a card. */
export type AskedQuestionHost = { view: Json; send: AskedSend; pending: boolean; unavailable: AskedUnavailable | null };
export const AskedQuestionContext = createContext<AskedQuestionHost | null>(null);

/** The card at an agent message that carries questions with delivery "async"; nothing for any other item. */
export function AskedQuestionMount({ row }: { row: Json }) {
  const host = useContext(AskedQuestionContext);
  const n = row?.native;
  if (n?.type !== "agentMessage" || n.delivery !== "async" || !Array.isArray(n.questions) || n.questions.length === 0) return null;
  const questions = askedQuestionsOf(n.questions);
  if (!questions || typeof row.threadId !== "string" || typeof row.turnId !== "string" || typeof n.id !== "string") return <p>This message carries questions the App cannot read; Codex's item is shown as sent.</p>;
  const entry: AskedQuestionEntry = { threadId: row.threadId, turnId: row.turnId, itemId: n.id, questions };
  return <AskedQuestionCard key={JSON.stringify([row.threadId, row.turnId, n.id])} entry={entry} standing={askedStanding(host?.view, entry)}
    send={host?.send} pending={host?.pending ?? false} unavailable={host ? host.unavailable : "no-send"} />;
}
