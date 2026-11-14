import { AgentText, type AgentTextSource, plainId, SuppliedId, Word, wordOf } from "./AgentText";

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Run offers beneath an agent message (DEL-01-04 NIR §5.7 RN-3…RN-7; DEL-02-02
// WR §16.5 PR-1…PR-5, FN-1…FN-3). The host reads the two exact line forms from
// messages it observed and supplies these offers; this element only presents
// them. A line is the agent's statement: nothing ends, is selected or starts
// until the person presses a button, and the host re-reads the message then.
//
// This is a guarded view (tests/support/presentation-guard.mjs): every value
// in an offer reaches the page through an approved presentation. The agent's
// statement and proposal, the host's notice, a library folder and the
// compatibility report's texts are boxed; a workflow name stands in the App's
// words, and in a button, only when it meets the App's own name rule, and is
// otherwise boxed beside; a run reference is shown as an identifier or boxed;
// the host's fixed vocabularies are the App's words only for a value the App
// recognises. A button carries only the App's words.

export type RunAct = (command: string, args: Record<string, unknown>) => Promise<unknown>;
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const box = { border: "1px dashed #777", padding: "4px 8px", margin: "4px 0 8px 16px" };

/** A workflow name the App's own rule admits (`workflow_workspace::valid_name`): lowercase letters, digits and
 * single hyphens, at most 64 characters. */
const SAFE_WORKFLOW_NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;
/** A workflow name in the App's words when it meets that rule; null otherwise, and the name is then shown boxed. */
const workflowName = (value: Json): string | null => typeof value === "string" && value.length <= 64 && SAFE_WORKFLOW_NAME.test(value) ? plainId(value) : null;

/** A recorded value shown as text the App did not write; "not recorded" when there is none. */
function Boxed({ value, label, name, source = "codex" }: { value: Json; label: string; name: string; source?: AgentTextSource }) {
  if (value === undefined || value === null || value === "") return <i>not recorded</i>;
  return <AgentText value={value} source={source} label={label} name={name} />;
}
/** A workflow name the App's rule does not admit, boxed beside the App's words that stand for it. */
function NameBeside({ value }: { value: Json }) {
  if (workflowName(value) !== null || value === undefined || value === null || value === "") return null;
  return <> <AgentText value={value} source="file" label="Workflow:" name="Workflow name as recorded, not the App's words" /></>;
}
/** A revision: its first twelve characters in the App's words when it is hexadecimal, else boxed whole. */
function Revision({ value }: { value: Json }) {
  const short = typeof value === "string" && /^[0-9a-f]+$/i.test(value) ? plainId(value.slice(0, 12)) : null;
  if (short !== null) return <>{short}</>;
  return <Boxed value={value} label="Revision:" name="Workflow revision as recorded, not the App's words" />;
}

// The host's words for a run's end (runtime_session.rs offers: "completed", or "ended to start ‹name›").
const END_CAUSE = { completed: "completed" } as const;
function EndCause({ cause }: { cause: Json }) {
  const word = wordOf(END_CAUSE, cause);
  if (word !== null) return <>“{word}”</>;
  const successor = typeof cause === "string" && cause.startsWith("ended to start ") ? workflowName(cause.slice("ended to start ".length)) : null;
  if (successor !== null) return <>“ended to start {successor}”</>;
  return <Boxed value={cause} label="Cause:" name="Why the run ends, as recorded; the App does not vouch for its words" />;
}

// The host's fixed words for a resolved proposal and a workflow's origin.
const STANDING = { "registered — selectable in this App session": "registered — selectable in this App session" } as const;
const ORIGIN = { project: "project", bundled: "bundled", local: "local" } as const;
// DEL-02-03 CK-1…CK-3 words, as RunPanel's CompatibilityAdvisory gives them.
const OUTCOME = {
  present: "present",
  present_currently_unavailable: "present, currently unavailable",
  missing: "missing",
  version_mismatch: "version differs",
  not_exposed_on_this_surface: "not exposed on this surface",
  channel_not_enabled: "channel not enabled",
  not_established: "not established",
} as const;
const CHECK = { compatible: "passes", unsupported: "does not pass", not_established: "not established" } as const;
const PUBLICATION = { "not published": "not published" } as const;
const REPORT = "Part of the compatibility report, as recorded; the App does not vouch for its words";
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);

/** One evaluation-basis field: its value boxed, or "not supplied". */
function Basis({ value }: { value: Json }) {
  if (value === undefined || value === null || value === "") return <>not supplied</>;
  return <AgentText value={value} source="codex" label="Recorded:" name={REPORT} />;
}

/** DEL-02-03 CK-1…CK-3, advisory (CC-3), for the proposed workflow. U-R10: a role outside the written-for roles is
 * shown with the role in force and the way to work in another role. The same content as RunPanel's
 * CompatibilityAdvisory, with every reported value boxed. */
function Compatibility({ entry }: { entry: Json }) {
  const p = entry?.preparation;
  if (!p) return <li>{entry?.occasionLabel ? <Boxed value={entry.occasionLabel} label="Occasion:" name={REPORT} /> : "Compatibility"}: no evaluation{entry?.limit ? <> (<Boxed value={entry.limit} label="Limit:" name={REPORT} />)</> : ""}. Evaluation basis not supplied. This check is advisory and never decides whether the run starts.</li>;
  const declared = p.declaration?.raw?.compatible_roles;
  const role = p.role;
  const inForce = role?.standing === "app-observed" ? (role.role ?? null) : undefined;
  const mismatch = Array.isArray(declared) && inForce !== undefined && !declared.includes(inForce);
  return <li>
    <Boxed value={entry.occasionLabel} label="Occasion:" name={REPORT} />: requirement check <Word value={p.check?.result} words={CHECK} label="Result:" name={REPORT} /> (<Boxed value={entry.statement} label="Statement:" name={REPORT} />){entry.notCurrent ? "; evaluated on an earlier basis, so it is not current" : ""}. Advisory: it never decides whether the run starts.
    <ul>
      {list(p.requirements).map((r: Json, i: number) => <li key={i}><Boxed value={r?.name} label="Requirement:" name={REPORT} />: <Word value={r?.outcome} words={OUTCOME} label="Outcome:" name={REPORT} />{r?.reason ? <>: <Boxed value={r.reason} label="Reason:" name={REPORT} /></> : ""} · purpose: {r?.purpose ? <Boxed value={r.purpose} label="Purpose:" name={REPORT} /> : "not supplied"}{r?.fallback ? <> · fallback: <Boxed value={r.fallback} label="Fallback:" name={REPORT} /></> : ""}</li>)}
      <li>Role in force: {role?.standing === "app-observed" ? role.role ? <Boxed value={role.role} label="Role:" name={REPORT} /> : "no role" : <>not established ({role?.reason ? <Boxed value={role.reason} label="Reason:" name={REPORT} /> : "no original App binding"})</>}, fixed for the conversation's life.</li>
      {mismatch && <li role="note">The workflow is written for {list(declared).map((n: Json, i: number) => <span key={i}>{i ? ", " : ""}<Boxed value={n} label="Role:" name={REPORT} /></span>)}; this conversation has {inForce ? <Boxed value={inForce} label="Role:" name={REPORT} /> : "no role"}. The check does not pass for the role. You may still start or continue the run. To work in one of those roles, use Continue as on the conversation: that starts a new conversation and leaves this one as it is.</li>}
      {list(p.check?.findings).filter((f: Json) => !(mismatch && /written for/.test(text(f)))).map((f: Json, i: number) => <li key={`f${i}`}>Finding: <Boxed value={f} label="Finding:" name={REPORT} /></li>)}
      <li>Evaluation basis: surface <Basis value={p.basis?.surface} />; acting pin <Basis value={p.basis?.acting_pin} />; catalog edition <Basis value={p.basis?.catalog_edition} />; environment observation <Basis value={p.basis?.environment_observation} />; evaluated at <Basis value={p.evaluated_at} />.</li>
      <li>Evaluation context: conversation <Basis value={p.basis?.conversation} />; home <Basis value={p.basis?.home} />; generation <Basis value={p.basis?.generation} />.</li>
      <li>Environment inventory source: <Basis value={entry.inventoryOrigin?.kind} />{entry.inventoryOrigin?.source ? <> · <Boxed value={entry.inventoryOrigin.source} label="Source:" name={REPORT} /></> : ""}.</li>
      {list(entry.publication?.factsNotSupplied).map((limit: Json, i: number) => <li key={`publication${i}`}>Report publication limit: <Boxed value={limit} label="Limit:" name={REPORT} /></li>)}
    </ul>
    <small>Publication: {entry.publication?.state ? <Word value={entry.publication.state} words={PUBLICATION} label="Publication:" name={REPORT} /> : "not published"}; <Boxed value={entry.r14} label="Report:" name={REPORT} /></small>
  </li>;
}

const RUN = { label: "Run:", name: "Run reference, as recorded; the App does not vouch for its words" } as const;
export function RunOffer({ offer, generation, ready, busy, act }: { offer: Json; generation: Json; ready: boolean; busy: boolean; act: RunAct }) {
  const finished = offer?.finished;
  const proposal = offer?.proposal;
  const workflow = proposal?.resolution?.workflow;
  const during = proposal?.runInForce;
  const notice = proposal?.resolution?.notice;
  if (!finished && !proposal) return null;
  return <div role="group" aria-label="Workflow run offer" style={box}>
    {finished && <p><AgentText value={finished.statement} label="The agent wrote:" name="The agent's statement in its message, not the App's words" /> This is the agent’s statement; run <SuppliedId value={finished.run} label={RUN.label} name={RUN.name} /> stays in force until you end it.</p>}
    {finished && <button disabled={busy} onClick={() => { void act("workflow_end_run", { runRef: finished.run, finishedReport: offer.message }); }}>End run</button>}
    {finished && <small> Ending here records that you ended the run, with cause “completed” as the agent stated. It does not check or take the work as done.</small>}
    {proposal && <p>The agent proposed a next workflow: <AgentText value={proposal.proposed} label="Next workflow:" name="The workflow the agent's message proposes, as it wrote it; not the App's words" />. Nothing is selected or started unless you choose it.</p>}
    {proposal && !workflow && <p role="note">{notice === undefined || notice === null || notice === "" ? "The proposal names no single registered workflow." : <AgentText value={notice} source="codex" label="Recorded:" name="Why no start is offered, as recorded, with the proposed name; the App does not vouch for its words" />} No start is offered.</p>}
    {proposal && workflow && <ul aria-label="Proposed workflow compatibility"><Compatibility entry={proposal.compatibility} /></ul>}
    {proposal && workflow && !during && <><button disabled={busy || !ready} onClick={() => { void act("workflow_start_proposed", { generation, message: offer.message, runRef: null, personText: "", proposalContext: proposal.context }); }}>Start {workflowName(workflow.name) ?? "the proposed workflow"} (proposed by the agent)</button><NameBeside value={workflow.name} /></>}
    {proposal && workflow && during && <>
      <button disabled={busy || !ready} onClick={() => { void act("workflow_start_proposed", { generation, message: offer.message, runRef: during.run, personText: "", proposalContext: proposal.context }); }}>End {workflowName(during.workflow) ?? "the current run"} and start {workflowName(workflow.name) ?? "the proposed workflow"}</button><NameBeside value={during.workflow} /><NameBeside value={workflow.name} />
      <small> One step, your choice: run <SuppliedId value={during.run} label={RUN.label} name={RUN.name} /> ends with cause <EndCause cause={during.endCause} />, then {workflowName(workflow.name) ?? "the proposed workflow"} starts in this conversation.</small>
    </>}
    {proposal && workflow && <p><small>Proposed workflow: <Word value={workflow.origin} words={ORIGIN} label="Origin:" name="The workflow's origin, as recorded; the App does not vouch for its words" /> library <Boxed value={workflow.source_root} source="file" label="Library:" name="The library's folder, as recorded; the App does not vouch for its words" />, revision <Revision value={workflow.revision} /> (<Word value={proposal.resolution?.standing} words={STANDING} label="Standing:" name="The proposal's standing, as recorded; the App does not vouch for its words" />).</small></p>}
  </div>;
}
