import { AgentText, idWords, wordOf } from "./AgentText";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// The points recorded in one conversation (DEL-02-03 REQ-008). The host joins
// each pointer kept with the conversation to its record in the App's records
// store and hands the terms only when that record is found once, whole and
// matching its digest; otherwise it hands "terms not read" with why. This view
// shows what took effect and nothing more: the terms the agent supplied are
// always marked as the agent's text, never a heading, control or label; the
// App's own sentences say what recording a point does not do.

const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);

/** The App's words for the closed values of version 1 of the point tool. */
const KIND = { checkpoint: "Checkpoint", review: "Review", decision: "Decision", input: "Input", "sign-off": "Sign-off" } as const;
const PAUSE = {
  "asks the agent to pause": "The point asks the agent to pause.",
  "does not ask the agent to pause": "The point does not ask the agent to pause.",
} as const;
const PAUSE_SET_BY = { "the person": "Set by the person.", "the agent": "Set by the agent." } as const;
const REQUESTED = { "the person": "Placed at the person's request.", "the agent itself": "Placed by the agent of its own accord." } as const;
const RESERVED = {
  "marking work checked": "marking work checked",
  "accepting a proposal": "accepting a proposal",
  "engineering approval": "engineering approval",
  "professional reliance": "professional reliance",
  "changing the autonomy grant": "changing the autonomy grant",
  "enabling external-agent access": "enabling external-agent access",
} as const;
const OFFER = {
  "offered at start in this App session": "The App offered its point tool when this conversation started.",
  "offered when this conversation started, restored after the App restarted": "The App offered its point tool when this conversation started; that offer was restored after the App restarted.",
} as const;

/** The supplied text fields of a point, with the App's name for each. */
const TEXT_FIELDS: [string, string][] = [
  ["label", "Label"],
  ["whenItArises", "When it arises"],
  ["whoMustRespond", "Who must respond"],
  ["responseRequested", "Response requested"],
  ["resolvedWhen", "Resolved when"],
  ["whoIntegrates", "Who integrates"],
  ["agentStatement", "The agent's statement"],
];

export const NONE_RECORDED = "No point has been recorded in this conversation.";
export const NOT_READ_WHOLE = "The App could not read this conversation's points whole.";
export const NOT_OFFERED = "This conversation was not offered the App's point tool in this App session.";
export const PAUSE_IS_COOPERATION = "Whether the agent pauses is its own cooperation: the App holds nothing for this point and has not seen whether the agent paused.";
export const INTEGRATOR_UNKNOWN = "The App does not know whether they accepted this or did it.";
export const RESERVED_ACT = "That act is made only at a declared checkpoint, through the App's act control. Recording this point performed no act and offers none.";
export const RECORDING_ONLY = "A recorded point is the agent's record of where a response is wanted. The App has not told anyone about it and is not waiting on it.";

function runWords(run: Json): string {
  if (run?.state === "in run") return `Placed during run ${idWords(run.run)}.`;
  if (run?.state === "no run") return "Placed when no run was open in this conversation in this App session.";
  return "Whether a run was open when it was placed is not established.";
}

function placerWords(placer: Json): string {
  const start = placer?.observed?.turnStart;
  return start ? "Placed by this conversation's agent, in a turn the App started at your press." : "Placed by this conversation's agent; the App did not see this turn start at your press.";
}

function Terms({ terms }: { terms: Json }) {
  if (terms?.state !== "read") return <p>Terms not read. <AgentText value={terms?.reason ?? "no reason was given"} source="record" label="Why:" name="Why the App could not read this point's terms" /></p>;
  const a = terms.arguments ?? {};
  const kind = wordOf(KIND, a.kind);
  const pause = wordOf(PAUSE, a.pause);
  const pauseBy = wordOf(PAUSE_SET_BY, a.pauseSetBy);
  const requested = wordOf(REQUESTED, a.placedOnRequestOf);
  const reserved = wordOf(RESERVED, a.reservedAct);
  return <div>
    <p>Kind: {kind ?? "not recorded"}.</p>
    <dl>
      {TEXT_FIELDS.map(([key, name]) => <div key={key}><dt>{name}</dt><dd>{a[key] === undefined ? "not recorded" : <AgentText value={a[key]} source="agent" />}</dd></div>)}
      <div><dt>Concerns</dt><dd>{a.concerns === undefined ? "not recorded" : <>
        {a.concerns.content === undefined ? "Content not recorded." : <AgentText value={a.concerns.content} source="agent" label="Content:" />}{" "}
        {a.concerns.revision === undefined ? "Revision not recorded." : <AgentText value={a.concerns.revision} source="agent" label="Revision:" />}
      </>}</dd></div>
    </dl>
    {pause && <p>{pause} {pauseBy ?? ""} {PAUSE_IS_COOPERATION}</p>}
    {a.whoIntegrates !== undefined && <p>Who integrates is as named when the point was placed. {INTEGRATOR_UNKNOWN}</p>}
    {reserved && <p>The point names a reserved act: {reserved}. {RESERVED_ACT}</p>}
    <p>{requested ?? "Whose request it was placed at is not recorded."}</p>
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
      <p>Point {i + 1}, reference {idWords(p.point)}. {runWords(p.run)} {placerWords(p.placer)}</p>
      <Terms terms={p.terms} />
    </article>)}
    {refused.length > 0 && <div><p>Calls the App refused; these are not points:</p><ul>{refused.map((r: Json, i: number) => <li key={i}><AgentText value={r?.reason} source="record" label="Refused:" name="Why the App refused this point call" /></li>)}</ul></div>}
  </section>;
}
