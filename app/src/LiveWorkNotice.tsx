import { appHome } from "./CodexControls";
import { answerable, hostRequests, requestThread } from "./RequestCards";
import { conversationLabel } from "./presentation";
type Json = any;

// What is running now, and what the App session before this one last
// recorded as a turn in progress, said once under the connection line so it
// is seen from every view (DEL-01-02: after a window is lost or the App is
// relaunched the person sees the actual state). Every word comes from the
// host's own fields: the status Codex last reported for a conversation, the
// host's turn and request registers, and `host.interruptedWork`. Nothing here
// resumes, sends or settles anything.

const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const same = (a: Json, b: Json) => JSON.stringify(a) === JSON.stringify(b);

/** A conversation's state now, from what Codex and the host report, or "" when it is idle or not known. */
export type ConversationState = "" | "answer" | "codex-waiting" | "working" | "system-error";

export function conversationState(host: Json, thread: Json): ConversationState {
  // A stopped or replaced Codex establishes nothing.
  if (!host || host.state !== "ready" || host.generationClosed === true || !same(thread?.generation, host.generation)) return "";
  // Only a request the person can answer waits for them; a named-service call does not.
  if (hostRequests(host).some((request: Json) => answerable(request) && requestThread(request) === thread.threadId && same(request.generation, host.generation))) return "answer";
  if (thread.statusObservationEnded === true) return "";
  const status = thread.status?.type;
  // Once Codex has reported a status for the conversation, that is the reading.
  if (thread.statusSource) {
    if (status === "active") return list(thread.status.activeFlags).some((flag: Json) => flag === "waitingOnApproval" || flag === "waitingOnUserInput") ? "codex-waiting" : "working";
    return status === "systemError" ? "system-error" : "";
  }
  // Before any status report: a turn the host saw start and has not seen end.
  const live = list(host.conversationTurns).some((turn: Json) => turn?.threadId === thread.threadId && same(turn.generation, host.generation)
    && turn.nativeTurn?.status === "inProgress" && turn.terminalEventObserved !== true && turn.observationEnded !== true);
  return live || status === "active" ? "working" : status === "systemError" ? "system-error" : "";
}

const SUFFIX: Record<ConversationState, string> = {
  "": "",
  answer: "waiting for your answer",
  "codex-waiting": "Codex reports it is waiting for an approval or an answer",
  working: "working",
  "system-error": "Codex reported a system error",
};

/** The conversation selector's suffix for one conversation, or "". */
export function conversationStateWords(host: Json, thread: Json): string {
  return SUFFIX[conversationState(host, thread)];
}

/** One complete sentence for a conversation's state, naming it as `name`. */
export function conversationStateSentence(state: ConversationState, name: string): string {
  switch (state) {
    case "answer": return `${name} is waiting for your answer.`;
    case "codex-waiting": return `Codex reports ${name} is waiting for an approval or an answer; the request appears in the conversation once the App has received it.`;
    case "working": return `${name} is working.`;
    case "system-error": return `Codex reported a system error in ${name}.`;
    default: return "";
  }
}

/**
 * The home this status is established to be the status of, or null. The
 * reply names its own home (`statusHome`); that must be the active home the
 * routing reports and the App-owned home of that class, and, when a Codex
 * generation is reported, the physical home that generation runs in. Any of
 * them missing or disagreeing establishes no home.
 */
export function shownHome(host: Json): { home: string; physicalHome: string } | null {
  const named = host?.statusHome;
  if (typeof named?.modeHomeClass !== "string" || typeof named?.home !== "string" || typeof named?.physicalHome !== "string") return null;
  if (host?.homeRouting?.activeModeHomeClass !== named.modeHomeClass || appHome(named.modeHomeClass) !== named.home) return null;
  if (host?.generation != null && host.generation?.home !== named.physicalHome) return null;
  return { home: named.home, physicalHome: named.physicalHome };
}

/**
 * The entries of `interruptedWork` that are the shown home's: the reading
 * and each entry must name the App-owned home and the physical home this
 * status is established to be of. A reading of any other home, or shown
 * beside a status whose home is not established, gives nothing: no outcome
 * and no offer.
 */
export function interruptedEntries(host: Json): Json[] {
  const shown = shownHome(host);
  const work = host?.interruptedWork;
  if (!shown || work?.home !== shown.home || work?.physicalHome !== shown.physicalHome) return [];
  return list(work.conversations).filter((entry: Json) => entry?.home === shown.home && entry?.physicalHome === shown.physicalHome && typeof entry?.threadId === "string");
}

/** A conversation loaded now in this home's current generation that is the entry's conversation, or undefined. */
function loadedFor(host: Json, entry: Json): Json | undefined {
  if (host?.generation?.home !== entry.physicalHome) return undefined;
  return list(host?.threads).find((thread: Json) => same(thread?.generation, host.generation) && thread.threadId === entry.threadId);
}

const LOST: Record<string, string> = {
  "supplier-exit": "That record was made when Codex ended unexpectedly, before the App session ended.",
  "supplier-stop": "That record was made when Codex was stopped, before the App session ended.",
};
const END: Record<string, string> = {
  "ended-without-record": "No end of that App session was recorded.",
  "system-terminated": "The App recorded that the system ended it.",
  "quit-with-live-work": "The App recorded that you quit it, and that this record was made when it stopped Codex for the quit.",
};

const reported = (status: string, earlier: boolean) => status === "inProgress"
  ? `${earlier ? "An earlier read of Codex's history" : "When the App read Codex's history, it"} listed that turn as in progress${earlier ? "." : "; whether it finished is unknown."}`
  : `${earlier ? "An earlier read of Codex's history" : "When the App read Codex's history, it"} reported that turn as ${status}.`;

/** What the App's reads of Codex's history said of one turn, or that it is not known. */
export function interruptedTurnWords(turn: Json): string {
  const current = turn?.current;
  const status = typeof current?.codexStatus === "string" && current.codexStatus ? current.codexStatus : "";
  let words: string;
  if (current?.reading === "read" && status) words = reported(status, false);
  else if (current?.reading === "not-in-history") words = "When the App read Codex's history, that turn was not in it; what became of it is unknown.";
  else if (current?.reading === "not-read") words = turn?.earlier || current.attempts > 0
    ? "The latest recovery attempt has not completed a read of this turn."
    : "The App has not read that turn back from Codex.";
  else if (current?.reading === "unavailable") words = `The App could not read it back from Codex${typeof current.reason === "string" && current.reason ? ` (${current.reason})` : ""}; what became of it is unknown.`;
  else if (current?.reading === "turn-not-named") words = "The App read the conversation back from Codex, but that read did not name this turn; what became of it is unknown.";
  else words = "What became of it is not established.";
  const earlier = turn?.earlier;
  if (earlier?.reading === "read" && typeof earlier.codexStatus === "string" && earlier.codexStatus) words += ` ${reported(earlier.codexStatus, true)}`;
  else if (earlier?.reading === "not-in-history") words += " An earlier read of Codex's history did not find that turn.";
  return words;
}

/** Whether a read of Codex's history was attempted for this turn. */
const readAttempted = (turn: Json) => ["read", "not-in-history", "unavailable", "turn-not-named"].includes(turn?.current?.reading) || !!turn?.earlier;
const READ_SENT_NOTHING = "Reading it back resumed nothing and resent nothing.";

/** What is recorded of that App session and this entry's record, as sentences. */
function recordedWords(entry: Json): string {
  return [LOST[entry.lostBeforeSessionEnd], END[entry.priorSessionEnd]].filter(Boolean).join(" ");
}

/**
 * The note for one turn of the shown conversation, or null. `generation`: the
 * shown conversation's generation; only an entry of its physical home and of
 * the home this status is for is matched.
 */
export function interruptedTurnNote(host: Json, generation: Json, threadId: string, turnId: string): string | null {
  if (typeof generation?.home !== "string") return null;
  for (const entry of interruptedEntries(host)) {
    if (entry.physicalHome !== generation.home || entry.threadId !== threadId) continue;
    const turn = list(entry.turns).find((candidate: Json) => candidate?.turnId === turnId);
    if (!turn) continue;
    return ["The last thing the App recorded of this turn before the previous App session ended was that it was in progress.", recordedWords(entry), interruptedTurnWords(turn), readAttempted(turn) ? READ_SENT_NOTHING : ""].filter(Boolean).join(" ");
  }
  return null;
}

export function LiveWorkNotice({ host, showConversation, findInHistory }: { host: Json; showConversation?: (threadId: string) => void; findInHistory?: (hint: string) => void }) {
  const current = list(host?.threads).filter((thread: Json) => same(thread?.generation, host?.generation));
  const live = current.map((thread: Json) => ({ thread, state: conversationState(host, thread) })).filter(row => row.state);
  const interrupted = interruptedEntries(host);
  if (live.length === 0 && interrupted.length === 0) return null;
  return <section aria-label="Conversation status and interrupted work" role="status">
    {live.length > 0 && <ul aria-label="Conversation status">{live.map(({ thread, state }) => <li key={String(thread.threadId)}>
      {conversationStateSentence(state, conversationLabel(host, thread))}{" "}
      {showConversation && <button onClick={() => showConversation(thread.threadId)}>Show it</button>}
    </li>)}</ul>}
    {interrupted.length > 0 && <ul aria-label="Conversations the earlier App session last recorded as working">{interrupted.map((entry: Json) => {
      const loaded = loadedFor(host, entry);
      const turns = list(entry.turns);
      return <li key={JSON.stringify([entry.sourceGeneration, entry.threadId])}>
        The last thing the App recorded for {loaded ? <strong>{conversationLabel(host, loaded)}</strong> : <>a conversation (<code>{String(entry.threadId)}</code>)</>} before the previous App session ended was {turns.length === 1 ? "a turn" : `${turns.length} turns`} in progress.{" "}
        {recordedWords(entry) && <>{recordedWords(entry)} </>}
        {turns.map((turn: Json, index: number) => <span key={index}>{interruptedTurnWords(turn)} </span>)}
        {turns.some(readAttempted) && <>{READ_SENT_NOTHING} </>}
        {loaded ? showConversation && <button onClick={() => showConversation(entry.threadId)}>Show it</button>
          : findInHistory && <button onClick={() => findInHistory(String(entry.threadId))}>Find it in History</button>}
      </li>;
    })}</ul>}
  </section>;
}
