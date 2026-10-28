import { useState } from "react";
import { ConversationSelect, conversationKey, conversationReference, findConversation } from "./TrialComposer";
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
const ACT_RELATION: Record<string, string> = { "after arrival": "after the arrival", "earlier act": "before the arrival, on content still current (an earlier act counts)" };
// EXEC CE-10 / SD-2 (RC-8): what a recorded lapse observation says, and no more.
const LAPSE_STATE: Record<string, string> = {
  lapsed: "the file's content changed",
  "lapsed (subject absent)": "the file is absent",
  "matches c0 again after observed lapse": "the file matches the content acted on again, after the observed lapse",
  "unknown (incomparable)": "lapse unknown: the content identities are not comparable",
  "unknown (unavailable)": "lapse unknown: the file could not be read",
};
const lapseLine = (b: Json, pending = false): string => {
  const lapsed = b?.state === "lapsed" || b?.state === "lapsed (subject absent)";
  const label = !lapsed ? "" : b?.when === "after run end" ? ` Act lapsed at ${text(b?.time)} after run end; ${pending ? "the arrival’s pending label is lapsed" : "the arrival is recorded as lapsed"}.` : b?.when === "after resume" ? ` Act lapsed at ${text(b?.time)}; the arrival stays performed.` : ` Lapsed at ${text(b?.time)}; the arrival is recorded as waiting again.`;
  return `Lapse observed for ${text(b?.act?.actKind)} ${text(b?.act?.recordId)} at ${text(b?.time)} (${text(b?.when)}): ${LAPSE_STATE[text(b?.state)] ?? text(b?.state)}.${label} Nothing is asked or stopped because of it.`;
};
const line = (key: string, body: Json) => <span key={key}><br /><small>{body}</small></span>;
export type OpenArrivalFileAct = (runRef: string, arrivalRecordId: string) => Promise<void>;

/** EXEC CE-3 / SD-2: one recorded arrival with its latest disposition, read from
 * the run record. Information only: nothing waits on it and nothing is sent. */
export function ArrivalRecord({ arrival, all, runRef, fileActEntry, openFileAct, busy = false }: {
  arrival: Json; all: Json[]; runRef?: string; fileActEntry?: Json; openFileAct?: OpenArrivalFileAct; busy?: boolean;
}) {
  const b = arrival?.body ?? {};
  const name = text(b.checkpoint);
  const related = (kind: string) => all.filter((e: Json) => e?.kind === kind && sameArrival(e?.body?.arrival, name, b.arrivalOrdinal));
  const postEnd = related("act_after_run_end");
  // CE-16 persists only a coordinate. A corrected/nonunique arrival does not
  // prove that coordinate still denotes this subject; raw history stays visible.
  const coordinateArrivals = all.filter((e: Json) => e?.kind === "checkpoint_arrival" && text(e?.body?.checkpoint) === name && e?.body?.arrivalOrdinal === b.arrivalOrdinal);
  const postEndBound = coordinateArrivals.length === 1 && !arrival?.corrects && !arrival?.afterRunEndRelationLimit;
  const endAt = all.findIndex((e: Json) => e?.kind === "run_ended");
  const afterEnd = (e: Json) => endAt >= 0 && all.indexOf(e) > endAt;
  const changes = related("disposition_change").filter((e: Json) => postEndBound || !afterEnd(e));
  const requests = related("act_request");
  const latest = changes.length ? changes[changes.length - 1].body?.disposition : undefined;
  const time = b.event?.evidencedTime;
  const note = writtenNote(arrival, all);
  const candidate = fileActEntry?.state === "candidate" && !!runRef && typeof arrival?.recordId === "string" && !!arrival.recordId;
  const fileActReason = text(fileActEntry?.reason) || (runRef ? "No current file-act entry was supplied by the host for this arrival." : "Historical or reopened arrival: no current owned file-act entry is available.");
  return <li>
    Arrival {text(b.arrivalOrdinal)}: {latest === undefined ? "disposition not recorded" : arrivalLabel(latest)}. Observed {text(b.event?.ref)}{time ? ` at ${text(time.value)} (${TIME_SOURCE[text(time.source)] ?? text(time.source)})` : ""}.
    {list(b.referents).map((r: Json, i: number) => line(`r${i}`, `Subject: ${text(r?.subject)}; content ${r?.content?.notObtainable ? `not obtainable: ${text(r.content.reason)}` : `${text(r?.content?.method)} ${text(r?.content?.value).slice(0, 12)}`}.`))}
    {requests.length
      ? requests.map((r: Json, i: number) => line(`q${i}`, `Request for the act observed: ${text(r.body?.form)} from ${text(r.body?.requester?.kind)}; act kind ${text(r.body?.actKind)}. A request is not the act.`))
      : line("q", `Request for the act: ${b.requestObservation?.state === "not yet observed" ? "no request from the agent observed" : text(b.requestObservation?.state)}.`)}
    {related("act_counted").map((c: Json, i: number) => line(`a${i}`, `Act counted: ${text(c.body?.act?.actKind)} ${text(c.body?.act?.recordId)}, captured ${text(c.body?.act?.capturedAt)} in the App act control, ${ACT_RELATION[text(c.body?.relation)] ?? text(c.body?.relation)}.`))}
    {!postEndBound && (postEnd.length>0 || related("act_lapsed").some((e: Json) => e.body?.when === "after run end")) && line("end-limit", `Post-end subject association not established for this arrival: ${text(arrival?.afterRunEndRelationLimit) || "corrected or ambiguous arrival coordinate"}. The observation remains in the recorded history.`)}
    {(postEndBound ? postEnd : []).map((c: Json, i: number) => line(`end${i}`, `After run end: ${text(c.body?.act?.actKind)} ${text(c.body?.act?.recordId)}, captured ${text(c.body?.act?.capturedAt)} in the App act control. The ended arrival disposition is unchanged. ${writtenNote(c, all)}`))}
    {related("act_not_counted").map((c: Json, i: number) => line(`n${i}`, `Act not counted: ${text(c.body?.act?.actKind)} ${text(c.body?.act?.recordId)}, captured ${text(c.body?.act?.capturedAt)}: ${text(c.body?.reason)}${c.body?.capturedBeforeArrival === true ? " (prior act not counted)" : ""}.`))}
    {related("arrival_declined").map((c: Json, i: number) => line(`d${i}`, `Declined by the person (${text(c.body?.declinedEventRef)}).`))}
    {related("continued_past").map((c: Json, i: number) => line(`c${i}`, `The agent went on with ${text(c.body?.actionRef)} with no act recorded against this arrival. This is a record, not a finding against the agent.`))}
    {related("run_resumed").map((c: Json, i: number) => line(`s${i}`, `After the act the run went on with ${text(c.body?.firstActionRef)}.`))}
    {related("act_lapsed").filter((c: Json) => postEndBound || c.body?.when !== "after run end").map((c: Json, i: number) => line(`x${i}`, `${lapseLine(c.body, c.written === false)} ${writtenNote(c, all)}`))}
    {list(b.limits).map((l: Json, i: number) => line(`l${i}`, `Limit: ${text(l)}`))}
    {note && line("w", note)}
    {candidate ? <p>
      <button disabled={busy || !openFileAct} onClick={() => openFileAct?.(runRef!, arrival.recordId)}>Review file for this arrival…</button>{" "}
      {fileActReason} The host rechecks the original source and current file when you click. Review opens a frozen offer; a separate native confirmation is required for an act.
      {!openFileAct && " File review is unavailable in this view."}
    </p> : <p role="note">Arrival file review unavailable: {fileActReason}</p>}
  </li>;
}

/** OV-1, SD-1, PD-1, PD-7: one declared checkpoint as plan guidance, with
 * what the run record holds about it. */
export function CheckpointGuidance({ element, run, openFileAct, busy = false }: { element: Json; run?: Json; openFileAct?: OpenArrivalFileAct; busy?: boolean }) {
  const v = element?.value ?? {};
  const invalid = element?.reading === "invalid";
  const all = run ? records(run) : [];
  const name = text(v.name);
  const listing = all.find((r: Json) => r?.kind === "checkpoint_listed" && text(r?.body?.checkpoint) === name);
  const arrivals = all.filter((r: Json) => r?.kind === "checkpoint_arrival" && text(r?.body?.checkpoint) === name);
  const unread = all.filter((r: Json) => r?.kind === "checkpoint_arrival" && typeof r?.body?.checkpoint !== "string").length;
  const evaluability = listing?.body?.evaluability;
  const findings = all.filter((r: Json) => r?.kind === "declaration_finding" && text(r?.body?.checkpoint) === name);
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
    {run && line("record", `Run record: ${!listing ? (findings.length ? `not listed: reported as a declaration finding (${findings.map((f: Json) => `${text(f.body?.finding)}, ${text(f.body?.code)}`).join("; ")}); no arrival is recorded for it (CE-2).` : invalid ? "not listed: the run record lists only the checkpoints the App recognizes (CE-1)." : "this checkpoint is missing in record (no checkpoint_listed entry for it); it is shown here from the declaration.")
      : evaluability?.status === "not evaluable" ? `listed. The App does not record arrivals for it: ${text(evaluability?.reason)}`
      : `listed. The App records an arrival only from what it observes in the conversation: ${text(evaluability?.reason)}`}${listing && writtenNote(listing, all) ? ` ${writtenNote(listing, all)}` : ""}`)}
    {run && listing && (arrivals.length
      ? <ul aria-label={`Recorded arrivals of ${name}`}>{arrivals.map((a: Json, i: number) => <ArrivalRecord key={i} arrival={a} all={all} runRef={run?.reference} fileActEntry={run?.fileActEntries?.[a.recordId]} openFileAct={openFileAct} busy={busy} />)}</ul>
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
// evidence note. The act entries at an arrival (CE-5, CE-6, CE-8, CE-10, CE-11
// and every CE-18 label) are read into the human-act facet only. The same kinds
// without a readable body read as unknown like any other entry; so do
// observation losses and recoveries, whose effect on a facet AS §8 does not map.
const readCheckpointEntry = (r: Json): boolean => {
  const b = r?.body;
  switch (r?.kind) {
    case "checkpoint_arrival": return typeof b?.checkpoint === "string" && b?.event?.source === "native_item";
    case "disposition_change": return b?.disposition === "waiting" || readActEntry(r);
    case "continued_past": return typeof b?.arrival?.checkpoint === "string";
    // RE-2: this is a later act observation, with no ended-run facet change.
    case "act_after_run_end": return str(b?.arrival?.checkpoint) && Number.isInteger(b?.arrival?.arrivalOrdinal) && b.arrival.arrivalOrdinal >= 1 && ["A4", "A6", "A7"].includes(b?.act?.actKind) && str(b?.act?.recordId) && str(b?.act?.capturedAt) && b?.act?.capturingSurface === "app_act_control";
    default: return readActEntry(r);
  }
};
// RS R13 tool-permission settlements feed no facet: AS §8 names no source for
// them, RS §8's record-out does not carry them to AS, and an A14 settlement is
// never an act (AS §2 "never shown as a grant or an act; recorded only in RS
// R13"; DS-3; RS HA-1). A readable one leaves every facet as it is.
// RS R11 "lost acknowledgement" is a record-out evidence limit, which AS §8
// assigns to Evidence completeness only: it adds an *unknown* note there and
// leaves the other facets as they are. Other limits are not read here.
const SETTLED_BY = ["the person via interaction", "the user's Codex mode", "App named-rule decline", "explicit error", "the supplier", "none — ended unanswered"];
const SETTLEMENTS = ["answered", "declined", "errored", "resolved by supplier", "ended unanswered (process exit)"];
const settlementEntry = (r: Json): boolean => r?.kind === "tool_permission_settlement" && str(r?.body?.request) && SETTLED_BY.includes(r?.body?.settledBy) && SETTLEMENTS.includes(r?.body?.settlement);
// RS R5 `model_turn` (the model and destination per turn) feeds no facet either:
// AS §2 and §3.2 place the destination in DEL-03-03's channel status, "not here".
const modelTurnEntry = (r: Json): boolean => r?.kind === "model_turn" && typeof r?.body?.requested === "string" && typeof r?.body?.effective === "string"
  && ((Number.isInteger(r?.body?.turn) && r.body.turn >= 1) || r?.body?.scope === "thread");
const lostAcknowledgement = (r: Json): boolean => r?.kind === "evidence_limit" && r?.body?.label === "lost acknowledgement" && str(r?.body?.subjectRef);
// AS §8 "Human acts" (source: the record): the checkpoint entries about acts at an
// arrival, which this view reads into that facet only. They say nothing about the
// other facets (no result, host check, limitation, examination or route).
const ACT_ENTRY_KINDS = ["act_counted", "act_not_counted", "act_lapsed", "arrival_declined", "run_resumed"];
const DISPOSITIONS = ["waiting", "performed", "resolved negatively", "lapsed", "not reached", "unknown"];
// Each kind's required body fields (EXEC `checkpoint-record-entries.schema.json`
// $defs); a body missing one is unreadable and makes every facet unknown.
const str = (v: Json) => typeof v === "string" && v.length > 0;
const actRef = (a: Json) => str(a?.recordId) && str(a?.actKind) && str(a?.capturedAt) && str(a?.capturingSurface);
const READABLE: Record<string, (b: Json) => boolean> = {
  act_counted: b => actRef(b?.act) && ["after arrival", "earlier act"].includes(b?.relation) && Array.isArray(b?.referents),
  act_not_counted: b => actRef(b?.act) && str(b?.reason) && typeof b?.capturedBeforeArrival === "boolean",
  act_lapsed: b => actRef(b?.act) && str(b?.state) && Array.isArray(b?.referents) && b?.c0 !== null && typeof b?.c0 === "object" && b?.c1 !== undefined && b?.c1 !== null && str(b?.time),
  arrival_declined: b => str(b?.declinedEventRef),
  run_resumed: b => str(b?.firstActionRef) && str(b?.time),
  disposition_change: b => DISPOSITIONS.includes(text(b?.disposition))
    && (b?.performanceOrdinal === undefined || (Number.isInteger(b.performanceOrdinal) && b.performanceOrdinal >= 1))
    && (b?.answeredBy === undefined || (Array.isArray(b.answeredBy) && b.answeredBy.every(str)))
    && (b?.annotations === undefined || Array.isArray(b.annotations)),
};
const readActEntry = (r: Json): boolean => typeof r?.body?.arrival?.checkpoint === "string" && Number.isInteger(r?.body?.arrival?.arrivalOrdinal)
  && (r?.kind === "disposition_change" || ACT_ENTRY_KINDS.includes(text(r?.kind))) && READABLE[text(r?.kind)](r.body);
const LAPSE_FACET: Record<string, string> = {
  lapsed: "lapsed",
  "lapsed (subject absent)": "lapsed (subject absent)",
  "matches c0 again after observed lapse": "matches c₀ again after observed lapse",
  "unknown (incomparable)": "unknown (incomparable)",
  "unknown (unavailable)": "unknown (unavailable)",
};
const actCited = (act: Json) => `${text(act?.actKind)} ${text(act?.recordId)}, captured ${text(act?.capturedAt)}`;
// AS §8 Human acts for an output that names its gating checkpoint (WD §4.4;
// AS OV-5): read from the record's entries for that checkpoint's latest
// arrival only, never computed from files (R8-4). Lapse states are the
// recorder's own act_lapsed observations; with none, no lapse is recorded,
// which is not "not lapsed" (AS §8: not yet evaluated is never shown as not lapsed).
function gatedHumanActs(gate: string, all: Json[]): string {
  const arrivals = all.filter((r: Json) => r?.kind === "checkpoint_arrival" && text(r?.body?.checkpoint) === gate);
  if (!arrivals.length) return `none recorded in this run: checkpoint ${gate}, which gates this output, has no recorded arrival`;
  const ordinal = Math.max(...arrivals.map((r: Json) => Number(r?.body?.arrivalOrdinal) || 0));
  const at = (r: Json) => text(r?.body?.arrival?.checkpoint) === gate && r?.body?.arrival?.arrivalOrdinal === ordinal;
  const of = (kind: string) => all.filter((r: Json) => r?.kind === kind && at(r));
  const coordinate = arrivals.filter((r: Json) => r?.body?.arrivalOrdinal === ordinal);
  if ((coordinate.length !== 1 || coordinate[0]?.corrects || coordinate[0]?.afterRunEndRelationLimit)
      && of("act_lapsed").some((r: Json) => r.body?.when === "after run end")) {
    return `unknown: checkpoint ${gate}, arrival ${ordinal} has no established post-end subject association (${text(coordinate[0]?.afterRunEndRelationLimit) || "corrected or ambiguous arrival coordinate"}); the original lapse remains in recorded history`;
  }
  const labels = of("disposition_change");
  const latest = labels.length ? labels[labels.length - 1].body : undefined;
  const where = `checkpoint ${gate}, arrival ${ordinal}`;
  const notCounted = of("act_not_counted").map((r: Json) => `${actCited(r.body?.act)}: ${r.body?.capturedBeforeArrival === true ? "prior act not counted" : "act not counted"} — ${text(r.body?.reason)}`);
  const also = notCounted.length ? ` Not counted: ${notCounted.join("; ")}.` : "";
  const disposition = text(latest?.disposition);
  if (!latest) return `unknown: ${where} has no recorded disposition`;
  if (disposition === "unknown") return `unknown: ${where} is recorded unknown`;
  if (disposition === "resolved negatively") {
    const declined = of("arrival_declined").map((r: Json) => text(r.body?.declinedEventRef));
    return `${where}: resolved negatively — declined (${declined.join(", ") || "the declining record is not named"}); no act counts for it.${also}`;
  }
  // The latest performance and the acts that answer it.
  const performances = labels.filter((b: Json) => b?.body?.disposition === "performed" && typeof b?.body?.performanceOrdinal === "number");
  const top = performances.length ? Math.max(...performances.map((b: Json) => b.body.performanceOrdinal)) : 0;
  const performance = performances.find((b: Json) => b.body.performanceOrdinal === top)?.body;
  if (!performance) {
    if (disposition === "waiting") return `${where}: reached; no act recorded for it.${also}`;
    return `unknown: ${where} is recorded ${disposition} with no recorded performance`;
  }
  const counted = of("act_counted");
  // PH-4 / RC-2: never *performed* without the act: every act the label cites
  // needs its act_counted entry at this arrival.
  const answeredBy = list(performance.answeredBy);
  const missing = answeredBy.filter((id: Json) => !counted.some((r: Json) => r.body?.act?.recordId === id));
  if (!answeredBy.length) return `unknown: ${where} is labelled performed but the label names no act`;
  if (missing.length) return `unknown: ${where} is labelled performed but no act_counted entry at this arrival cites ${missing.map(text).join(", ")}`;
  const acts = answeredBy.map((id: Json) => {
    const c = counted.find((r: Json) => r.body?.act?.recordId === id);
    const cited = actCited(c.body.act);
    const earlier = c?.body?.relation === "earlier act" ? ` — by earlier act ${text(id)} at ${text(c.body.act.capturedAt)}` : "";
    const observations = of("act_lapsed").filter((r: Json) => r.body?.act?.recordId === id);
    const last = observations.length ? observations[observations.length - 1].body : undefined;
    const state = !last ? "lapse: not yet evaluated (no lapse observation recorded; not shown as not lapsed)"
      : LAPSE_FACET[text(last.state)] === undefined ? `lapse: unknown (state ${text(last.state)} not read by this view)`
      : `lapse: ${LAPSE_FACET[text(last.state)]} (observed ${text(last.time)}${last.state === "lapsed" || last.state === "lapsed (subject absent)" || last.state === "matches c0 again after observed lapse" ? `; c₀ ${text(last.c0?.method)} ${text(last.c0?.value).slice(0, 12)}` : ""})`;
    return `${cited}${earlier}; ${state}`;
  });
  const answered = acts.length > 1 ? `answered by ${acts.length} acts: ` : "";
  const now = disposition === "performed" ? "performed" : disposition === "waiting" ? "reached again; the act on its current content is not yet recorded" : `recorded ${disposition}`;
  return `${where}: ${now} (performance ${top}); ${answered}${acts.join(" | ")}. Actor, recorder and recording mode are in the act record, not in the run record.${also}`;
}
// An arrival whose bound subject is this output: what the record observed, and no more.
function arrivalEvidence(output: Json, run: Json): string | undefined {
  const name = text(output?.name);
  const bound = records(run).filter((r: Json) => r?.kind === "checkpoint_arrival" && list(r?.body?.referents).some((x: Json) => text(x?.subject).startsWith(`output ${name}:`)));
  if (!name || !bound.length) return undefined;
  return `observed in the conversation only: ${bound.map((r: Json) => `${text(r.body.event?.ref)} (arrival of ${text(r.body.checkpoint)})`).join("; ")}. That marks where the agent put the output; it does not show that its content meets the declaration`;
}
export function outputStanding(output: Json, run: Json): Facets {
  const unread = Array.from(new Set(records(run).filter((r: Json) => !OUTPUT_NEUTRAL_KINDS.includes(text(r?.kind)) && !readCheckpointEntry(r) && !settlementEntry(r) && !modelTurnEntry(r) && !lostAcknowledgement(r)).map((r: Json) => text(r?.kind))));
  if (unread.length) {
    const unknown = `unknown: the run record holds ${unread.join(", ")} entries whose bodies this view does not read, so their relation to ${text(output?.name)} is not shown`;
    return { temporal: unknown, hostChecks: unknown, limitations: unknown, humanActs: unknown, examination: unknown, evidence: `unknown (record entries not read by this view)`, route: unknown };
  }
  const all = records(run);
  const gate = text(output?.gating_checkpoint);
  // With no gating checkpoint declared, acts recorded at an arrival bound to this
  // output are not this output's declared act standing: unknown, never "none".
  const name = text(output?.name);
  const boundActs = all.filter((r: Json) => readActEntry(r) && !(r?.kind === "disposition_change" && r?.body?.disposition === "waiting"))
    .filter((r: Json) => all.some((a: Json) => a?.kind === "checkpoint_arrival" && text(a?.body?.checkpoint) === text(r?.body?.arrival?.checkpoint)
      && a?.body?.arrivalOrdinal === r?.body?.arrival?.arrivalOrdinal && list(a?.body?.referents).some((x: Json) => text(x?.subject).startsWith(`output ${name}:`))));
  const humanActs = gate ? gatedHumanActs(gate, all)
    : boundActs.length ? `unknown: acts are recorded at an arrival bound to ${name}, which declares no gating checkpoint, so they are not shown as its standing`
    : all.some((a: Json) => a?.kind === "checkpoint_arrival" && list(a?.body?.referents).some((x: Json) => text(x?.subject).startsWith(`output ${name}:`)))
      ? "none recorded in this run (acts on App files are in their own act log)"
      : "none recorded for this output (acts on App files are in their own act log)";
  return {
    temporal: "unknown: no result for this output is recorded",
    hostChecks: "none reported",
    limitations: "none reported",
    humanActs,
    examination: "none recorded",
    evidence: [arrivalEvidence(output, run) ?? `missing: no record of ${text(output?.name) || "this output"} in the run record`,
      ...all.filter(lostAcknowledgement).map((r: Json) => `unknown (unobserved outcome, observer: the App): Codex's acknowledgement of a reply written to ${text(r.body.subjectRef)} was not observed (lost acknowledgement); its relation to ${name || "this output"} is not recorded`)].join("; "),
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
export function DeclaredPart({ declaration, run, openFileAct, busy = false }: { declaration: Json; run?: Json; openFileAct?: OpenArrivalFileAct; busy?: boolean }) {
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
    {category("checkpoints", "Checkpoints (plan guidance)", (e, i) => <CheckpointGuidance key={i} element={e} run={run} openFileAct={openFileAct} busy={busy} />)}
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
  if (!p) return <li>{text(entry?.occasionLabel) || "Compatibility"}: no evaluation{entry?.limit ? ` (${text(entry.limit)})` : ""}. Evaluation basis not supplied. This check is advisory and never decides whether the run starts.</li>;
  const declared = p.declaration?.raw?.compatible_roles;
  const role = p.role;
  const inForce = role?.standing === "app-observed" ? (role.role ?? null) : undefined;
  const mismatch = Array.isArray(declared) && inForce !== undefined && !declared.includes(inForce);
  return <li>
    {text(entry.occasionLabel)}: requirement check {CHECK[text(p.check?.result)] ?? text(p.check?.result)} ({text(entry.statement)}){entry.notCurrent ? "; evaluated on an earlier basis, so it is not current" : ""}. Advisory: it never decides whether the run starts.
    <ul>
      {list(p.requirements).map((r: Json, i: number) => <li key={i}>{text(r.name)}: {OUTCOME[text(r.outcome)] ?? text(r.outcome)}{r.reason ? `: ${text(r.reason)}` : ""} · purpose: {text(r.purpose) || "not supplied"}{r.fallback ? ` · fallback: ${text(r.fallback)}` : ""}</li>)}
      <li>Role in force: {roleWords(role)}, fixed for the conversation's life.</li>
      {mismatch && <li role="note">The workflow is written for {names(declared)}; this conversation has {inForce ?? "no role"}. The check does not pass for the role. You may still start or continue the run. To work in one of those roles, use Continue as on the conversation: that starts a new conversation and leaves this one as it is.</li>}
      {list(p.check?.findings).filter((f: Json) => !(mismatch && /written for/.test(text(f)))).map((f: Json, i: number) => <li key={`f${i}`}>Finding: {text(f)}</li>)}
      <li>Evaluation basis: surface {text(p.basis?.surface) || "not supplied"}; acting pin {text(p.basis?.acting_pin) || "not supplied"}; catalog edition {text(p.basis?.catalog_edition) || "not supplied"}; environment observation {text(p.basis?.environment_observation) || "not supplied"}; evaluated at {text(p.evaluated_at) || "not supplied"}.</li>
      <li>Evaluation context: conversation {text(p.basis?.conversation) || "not supplied"}; home {text(p.basis?.home) || "not supplied"}; generation {text(p.basis?.generation) || "not supplied"}.</li>
      <li>Environment inventory source: {text(entry.inventoryOrigin?.kind) || "not supplied"}{entry.inventoryOrigin?.source ? ` · ${text(entry.inventoryOrigin.source)}` : ""}.</li>
      {list(entry.publication?.factsNotSupplied).map((limit: Json, i: number) => <li key={`publication${i}`}>Report publication limit: {text(limit)}</li>)}
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

const unsavedRunAssociation = (run: Json): boolean => !!run?.turn && run?.runTag?.persistence === "memory-only";
export const hasUnsavedHistoryReference = (run: Json): boolean => unsavedRunAssociation(run) || list(run?.learningPointers).some(pointer => pointer?.persistence === "memory-only");
export function HistoryReferenceNotice({ pointers, run }: { pointers: Json; run?: Json }) {
  const unsaved = list(pointers).filter(pointer => pointer?.persistence === "memory-only");
  if (unsavedRunAssociation(run)) unsaved.push({ purpose: "run association" });
  return <>{unsaved.map((pointer, i) => <p key={i} role="note">
    History reference could not be saved{pointer.purpose ? ` (${text(pointer.purpose)})` : ""}.
    {" "}It is kept in this App session only. Retry saving records; the message will not be sent again.
  </p>)}</>;
}

export type RunBringBackAct = (command: string, args: Record<string, unknown>) => Promise<unknown>;

/** Historical projections identify evidence, never a live run owner. */
export const isRecordedRun = (run: Json): boolean => !!run?.run && !run?.reference;
/** A local host source reading offers a request, not validated history. The
 * host checks records and native history only when the person requests them. */
export function runLearningLimit(run: Json, action: "bringBack" | "compare"): string | null {
  const offer = run?.learning?.[action];
  if (offer?.offered === false) return text(offer.reason) || "The recorded run's source is unavailable.";
  if (isRecordedRun(run) && offer?.offered !== true) return "Reopen the recorded runs to establish whether this history source is available.";
  return null;
}

/** WR TT-10, TT-11: "Bring a real run back to authoring", at the person's
 * press only. The host reads the run's turns and pre-fills the transcript,
 * unsent, in the conversation the person chose. */
export function RunBringBackView({ run, conversations, target, setTarget, includeNative, setIncludeNative, busy, act }: {
  run: Json; conversations: Json[]; target: string; setTarget: (key: string) => void; includeNative: boolean; setIncludeNative: (on: boolean) => void; busy: boolean; act: RunBringBackAct;
}) {
  const chosen = list(conversations).find((c: Json) => conversationKey(c) === target) ?? null;
  const limit = runLearningLimit(run, "bringBack");
  return <div aria-label="Bring a real run back">
    <ConversationSelect label="Bring back to" conversations={conversations} value={target} setValue={setTarget} disabled={busy} />{" "}
    <label><input type="checkbox" checked={includeNative} disabled={busy} onChange={e => setIncludeNative(e.target.checked)} /> include native items</label>{" "}
    <button disabled={busy || !chosen || !!limit} onClick={() => { void act("workflow_run_bring_back", { runRef: run?.reference ?? run?.run, generation: chosen?.generation, threadId: chosen?.threadId, includeNative }); }}>Bring a real run back to authoring</button>
    {isRecordedRun(run) && <p><small>Recorded evidence (unsigned). {text(run?.learning?.standing) || "Current execution and original supply are not established here."}</small></p>}
    {isRecordedRun(run) && !limit && <p><small>The recorded history is checked when you request the transcript.</small></p>}
    {limit && <p role="note">Bring back is unavailable: {limit}</p>}
    <p><small>Pre-fills a transcript of this run, read from Codex history, in the chosen conversation's composer; nothing is sent until you send it there. For revising the workflow after real use.</small></p>
  </div>;
}

/** TT-10's default target for bringing a run back: the host's
 * `runBringBackDefaults` entry for this run (the authoring conversation of the
 * latest trial of a draft of the run's slot), or none. */
export const runBringBackDefault = (workflowRoot: Json, runRef: Json): Json | null => {
  const entry = list(workflowRoot?.runBringBackDefaults).find((d: Json) => d?.run === runRef);
  return conversationReference(entry?.authoring);
};

/** The person's pick wins; until then the target is the host's default
 * conversation when it is a started conversation here, else none. */
export function RunBringBack({ run, conversations, defaultThread = null, busy, act }: { run: Json; conversations: Json[]; defaultThread?: Json; busy: boolean; act: RunBringBackAct }) {
  const [picked, setPicked] = useState<string | null>(null);
  const [includeNative, setIncludeNative] = useState(false);
  const target = picked ?? conversationKey(findConversation(conversations, defaultThread));
  return <>
    {picked === null && !findConversation(conversations, defaultThread) && <p role="note"><small>Original authoring source unavailable or not selected; choose a current target explicitly.</small></p>}
    <RunBringBackView run={run} conversations={conversations} target={target} setTarget={setPicked} includeNative={includeNative} setIncludeNative={setIncludeNative} busy={busy} act={act} />
  </>;
}

/** PD-1, PD-3, PD-7 for one run, from the run view the host reports. */
export function RunPanel({ run, conversations, bringBackDefault = null, busy = false, act, openFileAct }: { run: Json; conversations?: Json[]; bringBackDefault?: Json; busy?: boolean; act?: RunBringBackAct; openFileAct?: OpenArrivalFileAct }) {
  const compatibility = list(run?.compatibility);
  const declaration = compatibility.find((c: Json) => c?.preparation?.declaration)?.preparation?.declaration;
  const workflow = run?.workflow ?? {};
  return <div aria-label="Run panel">
    <p>Workflow {text(workflow.name)} ({text(workflow.origin)}), revision {text(workflow.revision).slice(0, 12)} · conversation {text(run?.conversation)} · run {text(run?.lifecycle?.state)}{run?.lifecycle?.follows ? ` · follows ${text(run.lifecycle.follows)}` : ""}{run?.lifecycle?.end ? ` · ended: ${text(run.lifecycle.end.cause)}` : ""}.</p>
    <p><small>Run record entries: {recordKinds(run).length ? recordKinds(run).join(", ") : "none written yet"}. What the record does not hold is shown as not recorded.</small></p>
    <RecordWriteNotice run={run} />
    <HistoryReferenceNotice pointers={run?.learningPointers} run={run} />
    <h4>Declared part of {text(workflow.name) || "this workflow"}</h4>
    {declaration ? <DeclaredPart declaration={declaration} run={run} openFileAct={openFileAct} busy={busy} /> : <p>The declared part was not evaluated for this run, so it is not shown here.</p>}
    <h4>Compatibility (advisory)</h4>
    {compatibility.length ? <ul>{compatibility.map((c: Json, i: number) => <CompatibilityAdvisory key={i} entry={c} />)}</ul> : <p>No compatibility evaluation for this run.</p>}
    {act && <RunBringBack run={run} conversations={conversations ?? []} defaultThread={bringBackDefault} busy={busy} act={act} />}
  </div>;
}

/** The selected workflow before a run (CK-1): its identity and declared part. */
export function SelectedWorkflow({ selection, inspection = false }: { selection: Json; inspection?: boolean }) {
  if (!selection || selection.state === "not-selected") return <p>{inspection ? "No workflow content inspected." : "No workflow selected."}</p>;
  const id = selection.identity ?? {};
  return <div aria-label={inspection ? "Inspected workflow content" : "Selected workflow"}>
    <p>{inspection ? "Inspected:" : "Selected:"} <b>{text(id.name)}</b> ({text(id.origin)}), revision {text(id.revision).slice(0, 12)} · {text(selection.standing)} · {selection.runnable ? "can be run" : `not runnable: ${text(selection.runLimit)}`}{selection.currentLimit ? ` · current limit: ${text(selection.currentLimit)}` : ""}.</p>
    <DeclaredPart declaration={selection.declaration} />
  </div>;
}
