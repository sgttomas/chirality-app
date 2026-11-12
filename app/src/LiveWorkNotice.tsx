import { hostRequests, requestThread } from "./RequestCards";
import { conversationLabel } from "./presentation";
type Json = any;

// What is running now, and what an earlier App session left running, said
// once under the connection line so it is seen from every view (DEL-01-02:
// after a window is lost or the App is relaunched the person sees the actual
// state). Every word comes from the host's own fields: the status Codex last
// reported for a conversation, the host's turn and request registers, and
// `host.interruptedWork`. Nothing here resumes, sends or settles anything.

const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

/**
 * One conversation's state in a few words, or "" when it is idle or not
 * known. A stopped Codex establishes nothing, so it reads "".
 */
export function conversationStateWords(host: Json, thread: Json): string {
  if (!host || host.state !== "ready" || host.generationClosed === true || !same(thread?.generation, host.generation)) return "";
  const waiting = hostRequests(host).some((request: Json) => request?.state === "outstanding" && requestThread(request) === thread.threadId && (request.generation === undefined || same(request.generation, host.generation)));
  if (waiting) return "waiting for your answer";
  if (thread.statusObservationEnded === true) return "";
  const status = thread.status?.type;
  // Once Codex has reported a status for the conversation, that is the reading.
  if (thread.statusSource) {
    if (status === "active") return list(thread.status.activeFlags).some((flag: Json) => flag === "waitingOnApproval" || flag === "waitingOnUserInput") ? "waiting for your answer" : "working";
    if (status === "systemError") return "Codex reported a system error";
    return "";
  }
  // Before any status report: a turn the host saw start and has not seen end.
  const live = list(host.conversationTurns).some((turn: Json) => turn?.threadId === thread.threadId && same(turn.generation, host.generation)
    && turn.nativeTurn?.status === "inProgress" && turn.terminalEventObserved !== true && turn.observationEnded !== true);
  return live || status === "active" ? "working" : status === "systemError" ? "Codex reported a system error" : "";
}

const END: Record<string, string> = {
  "ended-without-record": "the App ended without a normal quit",
  "system-terminated": "the system ended the App",
  "quit-with-live-work": "you quit the App while it was in progress",
};

/** What Codex's history said of one turn an earlier App session left live, or that it is not known. */
export function interruptedTurnWords(turn: Json): string {
  const status = typeof turn?.codexStatus === "string" ? turn.codexStatus : "";
  if (turn?.reading === "read" && status === "inProgress") return "Codex's history still lists that turn as in progress; whether it finished is unknown.";
  if (turn?.reading === "read" && status) return `Codex's history now reports that turn as ${status}.`;
  if (turn?.reading === "not-in-history") return "That turn is not in Codex's history; what became of it is unknown.";
  if (turn?.reading === "not-read-yet") return "The App has not read it back from Codex yet.";
  if (turn?.reading === "unavailable") return `The App could not read it back from Codex${typeof turn.reason === "string" && turn.reason ? ` (${turn.reason})` : ""}; what became of it is unknown.`;
  return "What became of it is not established.";
}

/** The note for one turn of the shown conversation that an earlier App session left live, or null. */
export function interruptedTurnNote(host: Json, threadId: string, turnId: string): string | null {
  for (const conversation of list(host?.interruptedWork?.conversations)) {
    if (conversation?.threadId !== threadId) continue;
    const turn = list(conversation.turns).find((entry: Json) => entry?.turnId === turnId);
    if (turn) return `This turn was in progress when the App last ran${END[conversation.priorSessionEnd] ? `; ${END[conversation.priorSessionEnd]}` : ""}. ${interruptedTurnWords(turn)} Nothing was resumed or resent.`;
  }
  return null;
}

export function LiveWorkNotice({ host, showConversation, findInHistory }: { host: Json; showConversation?: (threadId: string) => void; findInHistory?: (hint: string) => void }) {
  const current = list(host?.threads).filter((thread: Json) => same(thread?.generation, host?.generation));
  const live = current.map((thread: Json) => ({ thread, words: conversationStateWords(host, thread) })).filter(row => row.words);
  const interrupted = list(host?.interruptedWork?.conversations);
  if (live.length === 0 && interrupted.length === 0) return null;
  return <section aria-label="Work in progress and interrupted work" role="status">
    {live.length > 0 && <ul aria-label="Conversations with work in progress">{live.map(({ thread, words }) => <li key={String(thread.threadId)}>
      <strong>{conversationLabel(host, thread)}</strong> is {words}.{" "}
      {showConversation && <button onClick={() => showConversation(thread.threadId)}>Show it</button>}
    </li>)}</ul>}
    {interrupted.length > 0 && <ul aria-label="Conversations interrupted when the App last ran">{interrupted.map((conversation: Json) => {
      const loaded = current.find((thread: Json) => thread.threadId === conversation.threadId);
      const turns = list(conversation.turns);
      return <li key={String(conversation.threadId)}>
        When the App last ran, {loaded ? <strong>{conversationLabel(host, loaded)}</strong> : <>a conversation (<code>{String(conversation.threadId)}</code>)</>} had {turns.length === 1 ? "a turn" : `${turns.length} turns`} in progress{END[conversation.priorSessionEnd] ? `; ${END[conversation.priorSessionEnd]}` : ""}.{" "}
        {turns.map((turn: Json, index: number) => <span key={index}>{interruptedTurnWords(turn)} </span>)}
        Nothing was resumed or resent.{" "}
        {loaded ? showConversation && <button onClick={() => showConversation(conversation.threadId)}>Show it</button>
          : findInHistory && <button onClick={() => findInHistory(String(conversation.threadId))}>Find it in History to continue it</button>}
      </li>;
    })}</ul>}
  </section>;
}
