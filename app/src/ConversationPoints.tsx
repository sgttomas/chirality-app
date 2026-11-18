import { AgentText, idWords, wordOf } from "./AgentText";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// The points recorded in one conversation (DEL-02-03 REQ-008). The host joins
// each pointer kept with the conversation to its record in the App's records
// store and hands the record's terms, run reading and observation only when
// that record is sound and joins; otherwise it hands "terms not read" with
// why. Every term the agent supplied, its closed values included, is shown as
// the agent's statement in a marked box, never as the App's word, a heading,
// a control or a label. The App speaks in its own voice only of what it
// observed itself: whether this turn was started at the person's press, the
// run reading, and what recording a point does not do.

const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);

const OFFER = {
  "offered at start in this App session": "The App offered its point tool when this conversation started.",
  "offered when this conversation started; restored when it was resumed": "The App offered its point tool when this conversation started; that offer was restored when the conversation was resumed in this App session.",
} as const;

/** Every term of version 1 of the point tool, with the App's name for it. */
const TERMS: [string[], string][] = [
  [["version"], "Tool version"],
  [["operation"], "Operation"],
  [["label"], "Label"],
  [["kind"], "Kind"],
  [["whenItArises"], "When it arises"],
  [["pause"], "Pause"],
  [["pauseSetBy"], "Pause set by"],
  [["whoMustRespond"], "Who must respond"],
  [["responseRequested"], "Response requested"],
  [["resolvedWhen"], "Resolved when"],
  [["concerns", "content"], "Concerns: content"],
  [["concerns", "revision"], "Concerns: revision"],
  [["whoIntegrates"], "Who integrates"],
  [["reservedAct"], "Reserved act"],
  [["placedOnRequestOf"], "Placed on request of"],
  [["agentStatement"], "The agent's statement"],
];
const at = (value: Json, path: string[]): Json => path.reduce((v, k) => (v && typeof v === "object" ? v[k] : undefined), value);

export const NONE_RECORDED = "No point has been recorded in this conversation.";
export const NOT_READ_WHOLE = "The App could not read this conversation's points whole.";
export const NOT_OFFERED = "This conversation was not offered the App's point tool in this App session.";
export const NOT_STATED = "not stated";
export const TERMS_ARE_THE_AGENTS = "The terms below are the agent's statements as it supplied them; the App has not checked any of them.";
export const PAUSE_IS_COOPERATION = "Whether the agent pauses is its own cooperation: the App holds nothing for this point and has not seen whether the agent paused.";
export const INTEGRATOR_UNKNOWN = "The App does not know whether whoever the agent named as integrating accepted this or did it.";
export const RESERVED_ACT = "A reserved act is made only at a declared checkpoint, through the App's act control. Recording this point performed no act and offers none.";
export const RECORDING_ONLY = "A recorded point is the agent's record of where a response is wanted. The App has not told anyone about it and is not waiting on it.";
export const DELEGATION_NOT_ESTABLISHED = "Whether a delegation covers this placement is not established.";

/** The App's own observation of how the turn that placed the point started. */
const TURN_START = {
  "person-press": "The App observed that the turn in which the agent placed this point was started at your press.",
  "app-not-person": "The App observed that the turn in which the agent placed this point was not started at your press.",
  "not-observed": "The App did not observe how the turn in which the agent placed this point started.",
} as const;
/** Why the App could not establish whether a run was open. */
const RUN_NOT_ESTABLISHED = {
  "start-sent-not-yet-open": "Whether a run was open when it was placed is not established: the App had sent a run's start in this conversation and had not yet seen that run open.",
  "resumed-earlier-run-unknown": "Whether a run was open when it was placed is not established: this conversation was resumed, and the App cannot tell whether a run of an earlier App session was still open in it.",
} as const;

function runWords(run: Json): string {
  if (run?.state === "in run") return `Placed during run ${idWords(run.run)}.`;
  if (run?.state === "no run") return "Placed when no run was open in this conversation in this App session.";
  return wordOf(RUN_NOT_ESTABLISHED, run?.reason) ?? "Whether a run was open when it was placed is not established.";
}

function observedWords(observed: Json): string {
  return `${wordOf(TURN_START, observed?.turnStart) ?? "The App did not observe how the turn in which this point was placed started."} ${DELEGATION_NOT_ESTABLISHED}`;
}

function Terms({ terms }: { terms: Json }) {
  if (terms?.state !== "read") return <p>Terms not read. <AgentText value={terms?.reason ?? "no reason was given"} source="record" label="Why:" name="Why the App could not read this point's terms" /></p>;
  const a = terms.arguments ?? {};
  return <div>
    <p>{TERMS_ARE_THE_AGENTS}</p>
    <dl>
      {TERMS.map(([path, name]) => { const value = at(a, path); return <div key={path.join(".")}><dt>{name}</dt><dd>{value === undefined ? NOT_STATED : <AgentText value={value} source="agent" />}</dd></div>; })}
    </dl>
    {a.pause !== undefined && <p>{PAUSE_IS_COOPERATION}</p>}
    {a.whoIntegrates !== undefined && <p>{INTEGRATOR_UNKNOWN}</p>}
    {a.reservedAct !== undefined && <p>{RESERVED_ACT}</p>}
  </div>;
}

/** The points of the selected conversation, as the host's `points` reading hands them. */
export function ConversationPoints({ points, generation, threadId }: { points: Json; generation: Json; threadId: Json }) {
  const row = list(points).find((p: Json) => JSON.stringify(p?.generation) === JSON.stringify(generation) && p?.threadId === threadId);
  if (!row) return null;
  const shown = list(row.points);
  const refused = list(row.refused);
  const whole = row.reading?.whole === true;
  const offered = wordOf(OFFER, row.offer?.state);
  return <section aria-label="Points recorded in this conversation">
    <h3>Points recorded in this conversation</h3>
    <p>{offered ?? NOT_OFFERED}</p>
    {!whole && <div><p>{NOT_READ_WHOLE}</p><ul>{list(row.reading?.reasons).map((r: Json, i: number) => <li key={i}><AgentText value={r} source="record" label="Why:" name="Why the App could not read this conversation's points whole" /></li>)}</ul></div>}
    {whole && offered && shown.length === 0 && <p>{NONE_RECORDED}</p>}
    {shown.length > 0 && <p>{RECORDING_ONLY}</p>}
    {shown.map((p: Json, i: number) => <article key={i} aria-label={`Point ${i + 1}`}>
      <p>Point {i + 1}, reference {idWords(p.point)}.{p.terms?.state === "read" && <> {runWords(p.run)} {observedWords(p.observed)}</>}</p>
      {typeof p.formatVersion === "string" && <p>This record is of a newer format version, {idWords(p.formatVersion)}; the App read it as far as it knows that format.</p>}
      <Terms terms={p.terms} />
    </article>)}
    {refused.length > 0 && <div><p>Calls the App refused; these are not points:</p><ul>{refused.map((r: Json, i: number) => <li key={i}><AgentText value={r?.reason} source="record" label="Refused:" name="Why the App refused this point call" /></li>)}</ul></div>}
  </section>;
}
