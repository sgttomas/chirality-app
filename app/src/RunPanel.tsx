import { useState } from "react";
import { ConversationSelect, conversationKey, findConversation } from "./TrialComposer";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// The run panel's readable parts (DEL-01-04 NIR §9 PD-1…PD-7, placing
// DEL-04-02 AS §4 OV-1…OV-7, §8 and §9 DS-1…DS-6, with DEL-02-03 SD-1…SD-6).
// The declared part is the selected revision's own declaration as the host
// read it; checkpoints are plan guidance in this phase; standing facets come
// only from the run record. Nothing here holds, blocks or pauses a run,
// infers checking, acceptance or reliance, or reacts to an arrival.

const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);
const names = (value: Json): string => list(value).map(text).join(", ");
// Declared text is shown as written; only a closing full stop is added where it has none.
const sentence = (value: string): string => /[.!?]$/.test(value.trim()) ? value.trim() : `${value.trim()}.`;

// DS-1 / AP-1: one label per act kind.
export const ACT_LABEL: Record<string, string> = { A4: "mark checked", A5: "accept", A6: "approve", A7: "rely", A10: "reject", A12: "set grant", A15: "register workflow revision" };
export const actLabel = (act: Json) => ACT_LABEL[text(act)] ?? `act ${text(act)} (not a checkpoint act)`;

const READING: Record<string, string> = { recognized: "", declared_empty: "declared empty", undeclared: "not declared", not_established: "not established", invalid: "invalid" };
const SUBJECT: Record<string, string> = {
  change_items_of_named_proposal: "the change items of a named proposal",
  named_output: "a named output",
  objects_named_output_concerns: "the objects a named output concerns",
  objects_changed_by_named_outcome: "the objects changed by a named outcome",
  targets_of_held_call: "the targets of the call it comes before",
  grant_setting: "a grant setting",
};
const INPUT_KIND: Record<string, string> = { host_read: "read from the host", file_supplied: "a file you supply", person_supplied: "you supply it", workflow_output: "another workflow's output" };
const TOOL_CLASS: Record<string, string> = { host_operation: "host operation", harness_capability: "Codex capability" };
const OUTPUT_FORM: Record<string, string> = { host_change: "a change in the host", file: "a file", message: "a message", workflow_input: "an input to another workflow", human_act_standing: "the standing of a human act" };
const EVIDENCE_KIND: Record<string, string> = {
  host_receipt_reference: "host receipt reference", read_basis_reference: "read basis reference", evaluated_basis: "evaluated basis",
  host_result_reference: "host result reference", examination_reference: "examination reference", human_act_record_reference: "human-act record reference", run_record_reference: "run record reference",
};
// SD-3: where the act is performed. The App never opens it because of an arrival (PD-5).
const SURFACE: Record<string, string> = {
  host_act_facility: "in the host's own view",
  app_act_control: "with the App act control, which you open yourself; nothing opens because the work reached the checkpoint",
  grant_control: "with the grant control",
};
const ACTOR: Record<string, string> = { the_person: "you", the_accountable_professional: "the accountable professional" };

function reachedWhen(rw: Json): string {
  switch (rw?.kind) {
    case "before_dispatch": return `before ${text(rw.tool)} is dispatched`;
    case "output_produced": return `when ${text(rw.output)} is produced`;
    case "host_outcome": return `when ${names(rw.tools)} report ${text(rw.outcome)}`;
    default: return `not established (${text(rw)})`;
  }
}
function decisionPath(p: Json): string {
  switch (p?.path) {
    case "stop": return "stop";
    case "return_to_stage": return `return to ${text(p.stage)}`;
    case "proceed_on_branch": return `proceed: ${text(p.branch)}`;
    default: return text(p);
  }
}
const readingNote = (element: Json) => {
  const words = READING[text(element?.reading)] ?? text(element?.reading);
  const findings = list(element?.findings).map(text);
  return words || findings.length ? <small> · {words || "finding"}{findings.length ? `: ${findings.join("; ")}` : ""}</small> : null;
};

// SD-2: an arrival's disposition as a record label, never a run state.
const DISPOSITION: Record<string, string> = {
  "not reached": "not reached",
  waiting: "reached; act not yet recorded",
  performed: "performed",
  "resolved negatively": "resolved negatively",
  lapsed: "lapsed",
  unknown: "unknown",
};
export const arrivalLabel = (disposition: Json) => DISPOSITION[text(disposition)] ?? `not a recorded disposition (${text(disposition)})`;

/** The run record's entry kinds, as the run view reports them. */
const recordKinds = (run: Json): string[] => list(run?.lifecycle?.records).map((r: Json) => text(r?.kind));
const records = (run: Json): Json[] => list(run?.lifecycle?.records);
const sameArrival = (a: Json, checkpoint: string, ordinal: Json) => text(a?.checkpoint) === checkpoint && a?.arrivalOrdinal === ordinal;
const TIME_SOURCE: Record<string, string> = { supplier_item_time: "time Codex gave for the item", app_observation_time: "time the App observed it" };
// An entry not yet in the run record says so; one written late carries its CE-19
// limit (`writtenLate` on the live run, or the limit entry read from the record).
const writtenNote = (r: Json, all: Json[]): string => r?.written === false ? `Not yet written to the run record: ${text(r.limit) || "the write did not complete"}.`
  : r?.writtenLate === true || all.some((e: Json) => e?.kind === "evidence_limit" && e?.body?.label === "record write failed" && e?.body?.subjectRef === r?.recordId) ? "Written late; the run record carries a “record write failed” limit for it." : "";
const line = (key: string, body: Json) => <span key={key}><br /><small>{body}</small></span>;

/** EXEC CE-3 / SD-2: one recorded arrival with its latest disposition, read from
 * the run record. Information only: nothing waits on it and nothing is sent. */
export function ArrivalRecord({ arrival, all }: { arrival: Json; all: Json[] }) {
  const b = arrival?.body ?? {};
  const name = text(b.checkpoint);
  const related = (kind: string) => all.filter((e: Json) => e?.kind === kind && sameArrival(e?.body?.arrival, name, b.arrivalOrdinal));
  const changes = related("disposition_change");
  const latest = changes.length ? changes[changes.length - 1].body?.disposition : undefined;
  const time = b.event?.evidencedTime;
  const note = writtenNote(arrival, all);
  return <li>
    Arrival {text(b.arrivalOrdinal)}: {latest === undefined ? "disposition not recorded" : arrivalLabel(latest)}. Observed {text(b.event?.ref)}{time ? ` at ${text(time.value)} (${TIME_SOURCE[text(time.source)] ?? text(time.source)})` : ""}.
    {list(b.referents).map((r: Json, i: number) => line(`r${i}`, `Subject: ${text(r?.subject)}; content ${r?.content?.notObtainable ? `not obtainable: ${text(r.content.reason)}` : `${text(r?.content?.method)} ${text(r?.content?.value).slice(0, 12)}`}.`))}
    {line("q", `Request for the act: ${b.requestObservation?.state === "not yet observed" ? "no request from the agent observed" : text(b.requestObservation?.state)}.`)}
    {related("continued_past").map((c: Json, i: number) => line(`c${i}`, `The agent went on with ${text(c.body?.actionRef)} with no act recorded against this arrival. This is a record, not a finding against the agent.`))}
    {related("run_resumed").map((c: Json, i: number) => line(`s${i}`, `After the act the run went on with ${text(c.body?.firstActionRef)}.`))}
    {list(b.limits).map((l: Json, i: number) => line(`l${i}`, `Limit: ${text(l)}`))}
    {note && line("w", note)}
  </li>;
}

/** OV-1, SD-1, PD-1, PD-7: one declared checkpoint as plan guidance, with
 * what the run record holds about it. */
export function CheckpointGuidance({ element, run }: { element: Json; run?: Json }) {
  const v = element?.value ?? {};
  const invalid = element?.reading === "invalid";
  const all = run ? records(run) : [];
  const name = text(v.name);
  const listing = all.find((r: Json) => r?.kind === "checkpoint_listed" && text(r?.body?.checkpoint) === name);
  const arrivals = all.filter((r: Json) => r?.kind === "checkpoint_arrival" && text(r?.body?.checkpoint) === name);
  const unread = all.filter((r: Json) => r?.kind === "checkpoint_arrival" && typeof r?.body?.checkpoint !== "string").length;
  const evaluability = listing?.body?.evaluability;
  return <li>
    <b>{text(v.name) || "(unnamed checkpoint)"}</b>: {actLabel(v.required_act)} by {ACTOR[text(v.actor)] ?? text(v.actor)} on {SUBJECT[text(v.subject?.class)] ?? text(v.subject?.class)}{v.subject?.output ? ` (${text(v.subject.output)})` : ""}, {reachedWhen(v.reached_when)}.
    {invalid && <> <b>Declaration finding: invalid</b> ({list(element.findings).map(text).join("; ")}). It is listed as written and treated as nothing more.</>}
    {!invalid && readingNote(element)}
    <br /><small>Purpose: {sentence(text(v.purpose) || "not stated")} Scope: {sentence(text(v.scope) || "not stated")}{v.position ? ` In the method: ${sentence(text(v.position))}` : ""}</small>
    <br /><small>Where the act is performed: {SURFACE[text(v.expected_act_evidence?.capturing_surface)] ?? "not stated"}{v.expected_act_evidence?.description ? ` (${text(v.expected_act_evidence.description)})` : ""}.</small>
    {v.held_actions && <><br /><small>Declared held actions ({v.held_actions.form === "host_operations_only" ? `host operations ${names(v.held_actions.tools)}` : list(v.held_actions.steps).map((s: Json) => `${text(s.step)}${s.app_side ? " (App side)" : ""}`).join("; ")}): plan guidance in this phase; nothing is stopped.</small></>}
    {(v.on_negative_decision || v.on_mixed_decision || v.on_subject_absent) && <><br /><small>{v.on_negative_decision ? `If declined: ${decisionPath(v.on_negative_decision)}. ` : ""}{v.on_mixed_decision ? `If mixed: ${decisionPath(v.on_mixed_decision)}. ` : ""}{v.on_subject_absent ? `If the subject is absent: ${decisionPath(v.on_subject_absent)}.` : ""}</small></>}
    {v.governed !== undefined && <><br /><small>{v.governed === "yes" ? "Declared governed. In this phase that changes nothing: the checkpoint is plan guidance (OV-7)." : `Governed value not recognized (${text(v.governed)}); preserved and reported (FB-19).`}</small></>}
    <br /><small>The agent asks you for the act when its work reaches this point; the act is recorded only when you perform it.</small>
    {run && line("record", `Run record: ${!listing ? (invalid ? "not listed: the run record lists only the checkpoints the App recognizes (CE-1)." : "this checkpoint is missing in record (no checkpoint_listed entry for it); it is shown here from the declaration.")
      : evaluability?.status === "not evaluable" ? `listed. The App does not record arrivals for it: ${text(evaluability?.reason)}`
      : `listed. The App records an arrival only from what it observes in the conversation: ${text(evaluability?.reason)}`}${listing && writtenNote(listing, all) ? ` ${writtenNote(listing, all)}` : ""}`)}
    {run && listing && (arrivals.length
      ? <ul aria-label={`Recorded arrivals of ${name}`}>{arrivals.map((a: Json, i: number) => <ArrivalRecord key={i} arrival={a} all={all} />)}</ul>
      : line("none", `No arrival recorded in this run.${unread ? ` ${unread} arrival entr${unread === 1 ? "y" : "ies"} could not be read, so this may be incomplete.` : ""}`))}
  </li>;
}

/** AS §8: separate facets, each no stronger than the record. Values are the
 * record's; with no record of the output every facet says so. */
export type Facets = { temporal: string; hostChecks: string; limitations: string; humanActs: string; examination: string; evidence: string; route: string };
// Kinds known to say nothing about an output's standing. Any other kind,
// including one this view has never seen, makes the facets unknown.
export const OUTPUT_NEUTRAL_KINDS = ["run_opened", "supplied_guidance", "compatibility_report_ref", "run_ended", "checkpoint_listed"];
// Checkpoint entries whose bodies this view reads (EXEC CE-3, CE-12): an arrival,
// its "waiting" disposition and a continuation record no act, check or result,
// so they leave the facets as they are; an arrival bound to an output adds an
// evidence note. The same kinds without a readable body, or with another
// disposition, read as unknown like any other entry.
const readCheckpointEntry = (r: Json): boolean => {
  const b = r?.body;
  switch (r?.kind) {
    case "checkpoint_arrival": return typeof b?.checkpoint === "string" && b?.event?.source === "native_item";
    case "disposition_change": return b?.disposition === "waiting";
    case "continued_past": return typeof b?.arrival?.checkpoint === "string";
    default: return false;
  }
};
// An arrival whose bound subject is this output: what the record observed, and no more.
function arrivalEvidence(output: Json, run: Json): string | undefined {
  const name = text(output?.name);
  const bound = records(run).filter((r: Json) => r?.kind === "checkpoint_arrival" && list(r?.body?.referents).some((x: Json) => text(x?.subject).startsWith(`output ${name}:`)));
  if (!name || !bound.length) return undefined;
  return `observed in the conversation only: ${bound.map((r: Json) => `${text(r.body.event?.ref)} (arrival of ${text(r.body.checkpoint)})`).join("; ")}. That marks where the agent put the output; it does not show that its content meets the declaration`;
}
export function outputStanding(output: Json, run: Json): Facets {
  const unread = Array.from(new Set(records(run).filter((r: Json) => !OUTPUT_NEUTRAL_KINDS.includes(text(r?.kind)) && !readCheckpointEntry(r)).map((r: Json) => text(r?.kind))));
  if (unread.length) {
    const unknown = `unknown: the run record holds ${unread.join(", ")} entries whose bodies this view does not read, so their relation to ${text(output?.name)} is not shown`;
    return { temporal: unknown, hostChecks: unknown, limitations: unknown, humanActs: unknown, examination: unknown, evidence: `unknown (record entries not read by this view)`, route: unknown };
  }
  return {
    temporal: "unknown: no result for this output is recorded",
    hostChecks: "none reported",
    limitations: "none reported",
    humanActs: "none recorded in this run (acts on App files are in their own act log)",
    examination: "none recorded",
    evidence: arrivalEvidence(output, run) ?? `missing: no record of ${text(output?.name) || "this output"} in the run record`,
    route: "not recorded",
  };
}
export function StandingFacets({ facets }: { facets: Facets }) {
  return <ul aria-label="Standing facets">
    <li>Current or historical: {facets.temporal}</li>
    <li>Host checks: {facets.hostChecks}</li>
    <li>Known limitations: {facets.limitations}</li>
    <li>Human acts: {facets.humanActs}</li>
    <li>Agent examination: {facets.examination}</li>
    <li>Evidence: {facets.evidence}</li>
    <li>Route and outcome: {facets.route}</li>
  </ul>;
}

/** The declared part, readable (WD §4; OV-1). `run` adds the record's view. */
export function DeclaredPart({ declaration, run }: { declaration: Json; run?: Json }) {
  if (!declaration) return <p>Declared part: not supplied by the host.</p>;
  if (declaration.unavailable) return <p role="note">Declared part could not be read: {text(declaration.unavailable)}</p>;
  const elements = (category: string): Json[] => list(declaration.elements?.[category]);
  const category = (key: string, title: string, render: (element: Json, index: number) => Json) => {
    const reading = text(declaration.categories?.[key]);
    const rows = elements(key);
    return <div key={key}>
      <h4>{title}</h4>
      {rows.length === 0 ? <p>{reading === "declared_empty" ? "Declared empty." : reading === "undeclared" || !reading ? "Not declared." : `Not established (${READING[reading] ?? reading}).`}</p> : <ul>{rows.map(render)}</ul>}
    </div>;
  };
  const raw = declaration.raw ?? {};
  return <div aria-label="Declared part">
    {declaration.reading === "undeclared" && <p>This workflow declares no requirements part; its text is the whole method.</p>}
    {declaration.reading === "not_established" && <p role="note">The declared part is not established: {list(declaration.findings).map(text).join("; ")}. It is shown as far as it was read.</p>}
    {declaration.reading === "recognized" && list(declaration.findings).length > 0 && <p><small>Findings: {list(declaration.findings).map(text).join("; ")}</small></p>}
    {category("expected_inputs", "Inputs", (e, i) => <li key={i}><b>{text(e.value?.name)}</b> ({e.value?.necessity === "optional" ? "optional" : "required"}; {INPUT_KIND[text(e.value?.kind)] ?? text(e.value?.kind)}{e.value?.read_through ? ` through ${text(e.value.read_through)}` : ""}): {text(e.value?.meaning)}{e.value?.basis_requirement ? ` Basis: ${text(e.value.basis_requirement)}` : ""}{e.value?.absence_effect ? ` If absent: ${text(e.value.absence_effect)}` : ""}{readingNote(e)}</li>)}
    {category("required_tools", "Tools", (e, i) => <li key={i}><b>{text(e.value?.name)}</b> ({e.value?.necessity === "optional" ? "optional" : "required"} {TOOL_CLASS[text(e.value?.class)] ?? text(e.value?.class)}{e.value?.operation ? ` ${text(e.value.operation)}` : ""}{e.value?.capability ? ` ${text(e.value.capability)}` : ""}{list(e.value?.versions).length ? `, versions ${names(e.value.versions)}` : ""}): {text(e.value?.purpose)}{e.value?.fallback ? ` Fallback: ${text(e.value.fallback)}` : ""}{readingNote(e)}</li>)}
    {category("checkpoints", "Checkpoints (plan guidance)", (e, i) => <CheckpointGuidance key={i} element={e} run={run} />)}
    {category("returned_outputs", "Outputs", (e, i) => <li key={i}><b>{text(e.value?.name)}</b> ({OUTPUT_FORM[text(e.value?.form)] ?? text(e.value?.form)}{e.value?.path ? ` at ${text(e.value.path)}` : ""}{e.value?.designating_line ? `, first line “${text(e.value.designating_line)}”` : ""}; to {text(e.value?.destination)}): {text(e.value?.meaning)}{readingNote(e)}
      <br /><small>Declared promise, not a standing: {names(e.value?.promised_standing) || "none"}.{e.value?.gating_checkpoint ? ` Declared with checkpoint ${text(e.value.gating_checkpoint)}.` : ""}</small>
      {run && <StandingFacets facets={outputStanding(e.value, run)} />}</li>)}
    {category("returned_evidence", "Evidence returned", (e, i) => <li key={i}><b>{text(e.value?.name)}</b> ({EVIDENCE_KIND[text(e.value?.kind)] ?? text(e.value?.kind)}, for {names(e.value?.supports)}): {text(e.value?.meaning)}{readingNote(e)}</li>)}
    <p>Written for roles: {raw.compatible_roles === undefined ? "not stated (any role)" : names(raw.compatible_roles) || "none established"}. Tool ceiling: {raw.tool_restriction === undefined ? "none declared" : names(raw.tool_restriction?.capabilities) || "no capabilities"}.</p>
    <details><summary>Declared part as the host read it (JSON)</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(declaration, null, 2)}</pre></details>
  </div>;
}

const OUTCOME: Record<string, string> = {
  present: "present",
  present_currently_unavailable: "present, currently unavailable",
  missing: "missing",
  version_mismatch: "version differs",
  not_exposed_on_this_surface: "not exposed on this surface",
  channel_not_enabled: "channel not enabled",
  not_established: "not established",
};
const CHECK: Record<string, string> = { compatible: "passes", unsupported: "does not pass", not_established: "not established" };
export const roleWords = (role: Json): string => role?.standing === "app-observed" ? (role.role ? text(role.role) : "no role") : `not established (${text(role?.reason) || "no original App binding"})`;

/** DEL-02-03 CK-1…CK-3, advisory (CC-3). U-R10: a role outside the written-for
 * roles is shown with the role in force and the way to work in another role. */
export function CompatibilityAdvisory({ entry }: { entry: Json }) {
  const p = entry?.preparation;
  if (!p) return <li>{text(entry?.occasionLabel)}: no evaluation{entry?.limit ? ` (${text(entry.limit)})` : ""}. This check is advisory and never decides whether the run starts.</li>;
  const declared = p.declaration?.raw?.compatible_roles;
  const role = p.role;
  const inForce = role?.standing === "app-observed" ? (role.role ?? null) : undefined;
  const mismatch = Array.isArray(declared) && inForce !== undefined && !declared.includes(inForce);
  return <li>
    {text(entry.occasionLabel)}: requirement check {CHECK[text(p.check?.result)] ?? text(p.check?.result)} ({text(entry.statement)}){entry.notCurrent ? "; evaluated on an earlier basis, so it is not current" : ""}. Advisory: it never decides whether the run starts.
    <ul>
      {list(p.requirements).map((r: Json, i: number) => <li key={i}>{text(r.name)}: {OUTCOME[text(r.outcome)] ?? text(r.outcome)}{r.reason ? `: ${text(r.reason)}` : ""}{r.fallback ? ` · fallback: ${text(r.fallback)}` : ""}</li>)}
      <li>Role in force: {roleWords(role)}, fixed for the conversation's life.</li>
      {mismatch && <li role="note">The workflow is written for {names(declared)}; this conversation has {inForce ?? "no role"}. The check does not pass for the role. You may still start or continue the run. To work in one of those roles, use Continue as on the conversation: that starts a new conversation and leaves this one as it is.</li>}
      {list(p.check?.findings).filter((f: Json) => !(mismatch && /written for/.test(text(f)))).map((f: Json, i: number) => <li key={`f${i}`}>Finding: {text(f)}</li>)}
    </ul>
    <small>Publication: {text(entry.publication?.state) || "not published"}; {text(entry.r14)}</small>
  </li>;
}

/** EXEC A-12 / CE-19: run record entries the App could not write yet. They are
 * kept in this App process, in order, and written when writing works again,
 * each followed by a "record write failed" limit. Nothing is written elsewhere. */
export function RecordWriteNotice({ run }: { run: Json }) {
  const pending = records(run).filter((r: Json) => r?.written === false);
  if (!pending.length) return null;
  const limits = Array.from(new Set(pending.map((r: Json) => text(r?.limit)).filter(Boolean)));
  return <p role="alert">{pending.length} run record entr{pending.length === 1 ? "y is" : "ies are"} not yet written ({pending.map((r: Json) => text(r?.kind)).join(", ")}){limits.length ? `: ${limits.join("; ")}` : ""}. They are kept in this App process only, in order, and are written to this run's record when writing works again, each followed by a “record write failed” limit. If the App quits first they are lost.</p>;
}

export type RunBringBackAct = (command: string, args: Record<string, unknown>) => Promise<unknown>;

/** WR TT-10, TT-11: "Bring a real run back to authoring", at the person's
 * press only. The host reads the run's turns and pre-fills the transcript,
 * unsent, in the conversation the person chose. */
export function RunBringBackView({ run, conversations, target, setTarget, includeNative, setIncludeNative, busy, act }: {
  run: Json; conversations: Json[]; target: string; setTarget: (key: string) => void; includeNative: boolean; setIncludeNative: (on: boolean) => void; busy: boolean; act: RunBringBackAct;
}) {
  const chosen = list(conversations).find((c: Json) => conversationKey(c) === target) ?? null;
  return <div aria-label="Bring a real run back">
    <ConversationSelect label="Bring back to" conversations={conversations} value={target} setValue={setTarget} disabled={busy} />{" "}
    <label><input type="checkbox" checked={includeNative} disabled={busy} onChange={e => setIncludeNative(e.target.checked)} /> include native items</label>{" "}
    <button disabled={busy || !chosen} onClick={() => { void act("workflow_run_bring_back", { runRef: run?.reference, generation: chosen?.generation, threadId: chosen?.threadId, includeNative }); }}>Bring a real run back to authoring</button>
    <p><small>Pre-fills a transcript of this run, read from Codex history, in the chosen conversation's composer; nothing is sent until you send it there. For revising the workflow after real use.</small></p>
  </div>;
}

/** TT-10's default target for bringing a run back: the host's
 * `runBringBackDefaults` entry for this run (the authoring conversation of the
 * latest trial of a draft of the run's slot), or none. */
export const runBringBackDefault = (workflowRoot: Json, runRef: Json): string | null => {
  const entry = list(workflowRoot?.runBringBackDefaults).find((d: Json) => d?.run === runRef);
  return entry?.threadId ? text(entry.threadId) : null;
};

/** The person's pick wins; until then the target is the host's default
 * conversation when it is a started conversation here, else none. */
export function RunBringBack({ run, conversations, defaultThread = null, busy, act }: { run: Json; conversations: Json[]; defaultThread?: string | null; busy: boolean; act: RunBringBackAct }) {
  const [picked, setPicked] = useState<string | null>(null);
  const [includeNative, setIncludeNative] = useState(false);
  const target = picked ?? conversationKey(findConversation(conversations, defaultThread));
  return <RunBringBackView run={run} conversations={conversations} target={target} setTarget={setPicked} includeNative={includeNative} setIncludeNative={setIncludeNative} busy={busy} act={act} />;
}

/** PD-1, PD-3, PD-7 for one run, from the run view the host reports. */
export function RunPanel({ run, conversations, bringBackDefault = null, busy = false, act }: { run: Json; conversations?: Json[]; bringBackDefault?: string | null; busy?: boolean; act?: RunBringBackAct }) {
  const compatibility = list(run?.compatibility);
  const declaration = compatibility.find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration;
  const workflow = run?.workflow ?? {};
  return <div aria-label="Run panel">
    <p>Workflow {text(workflow.name)} ({text(workflow.origin)}), revision {text(workflow.revision).slice(0, 12)} · conversation {text(run?.conversation)} · run {text(run?.lifecycle?.state)}{run?.lifecycle?.follows ? ` · follows ${text(run.lifecycle.follows)}` : ""}{run?.lifecycle?.end ? ` · ended: ${text(run.lifecycle.end.cause)}` : ""}.</p>
    <p><small>Run record entries: {recordKinds(run).length ? recordKinds(run).join(", ") : "none written yet"}. What the record does not hold is shown as not recorded.</small></p>
    <RecordWriteNotice run={run} />
    <h4>Declared part of {text(workflow.name) || "this workflow"}</h4>
    {declaration ? <DeclaredPart declaration={declaration} run={run} /> : <p>The declared part was not evaluated for this run, so it is not shown here.</p>}
    <h4>Compatibility (advisory)</h4>
    {compatibility.length ? <ul>{compatibility.map((c: Json, i: number) => <CompatibilityAdvisory key={i} entry={c} />)}</ul> : <p>No compatibility evaluation for this run.</p>}
    {act && <RunBringBack run={run} conversations={conversations ?? []} defaultThread={bringBackDefault} busy={busy} act={act} />}
  </div>;
}

/** The selected workflow before a run (CK-1): its identity and declared part. */
export function SelectedWorkflow({ selection }: { selection: Json }) {
  if (!selection || selection.state === "not-selected") return <p>No workflow selected.</p>;
  const id = selection.identity ?? {};
  return <div aria-label="Selected workflow">
    <p>Selected: <b>{text(id.name)}</b> ({text(id.origin)}), revision {text(id.revision).slice(0, 12)} · {text(selection.standing)} · {selection.runnable ? "can be run" : `not runnable: ${text(selection.runLimit)}`}{selection.currentLimit ? ` · current limit: ${text(selection.currentLimit)}` : ""}.</p>
    <DeclaredPart declaration={selection.declaration} />
  </div>;
}
