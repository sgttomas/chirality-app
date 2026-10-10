type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

// Run offers beneath an agent message (DEL-01-04 NIR §5.7 RN-3…RN-7; DEL-02-02
// WR §16.5 PR-1…PR-5, FN-1…FN-3). The host reads the two exact line forms from
// messages it observed and supplies these offers; this element only presents
// them. A line is the agent's statement: nothing ends, is selected or starts
// until the person presses a button, and the host re-reads the message then.

export type RunAct = (command: string, args: Record<string, unknown>) => Promise<unknown>;
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);
const box = { border: "1px dashed #777", padding: "4px 8px", margin: "4px 0 8px 16px" };

export function RunOffer({ offer, generation, ready, busy, act }: { offer: Json; generation: Json; ready: boolean; busy: boolean; act: RunAct }) {
  const finished = offer?.finished;
  const proposal = offer?.proposal;
  const workflow = proposal?.resolution?.workflow;
  const during = proposal?.runInForce;
  if (!finished && !proposal) return null;
  return <div role="group" aria-label="Workflow run offer" style={box}>
    {finished && <p>The agent wrote <q>{text(finished.statement)}</q>. This is the agent’s statement; run {text(finished.run)} stays in force until you end it.</p>}
    {finished && <button disabled={busy} onClick={() => { void act("workflow_end_run", { runRef: finished.run, finishedReport: offer.message }); }}>End run</button>}
    {finished && <small> Ending here records that you ended the run, with cause “completed” as the agent stated. It does not check or take the work as done.</small>}
    {proposal && <p>The agent proposed <q>Next workflow: {text(proposal.proposed)}</q>. Nothing is selected or started unless you choose it.</p>}
    {proposal && !workflow && <p role="note">{text(proposal.resolution?.notice) || "The proposal names no single registered workflow."} No start is offered.</p>}
    {proposal && workflow && !during && <button disabled={busy || !ready} onClick={() => { void act("workflow_start_proposed", { generation, message: offer.message, runRef: null, personText: "" }); }}>Start {text(workflow.name)} (proposed by the agent)</button>}
    {proposal && workflow && during && <>
      <button disabled={busy || !ready} onClick={() => { void act("workflow_start_proposed", { generation, message: offer.message, runRef: during.run, personText: "" }); }}>End {text(during.workflow) || "the current run"} and start {text(workflow.name)}</button>
      <small> One step, your choice: run {text(during.run)} ends with cause “{text(during.endCause)}”, then {text(workflow.name)} starts in this conversation.</small>
    </>}
    {proposal && workflow && <p><small>Proposed workflow: {text(workflow.origin)} library “{text(workflow.source_root)}”, revision {text(workflow.revision).slice(0, 12)} ({text(proposal.resolution?.standing)}).</small></p>}
  </div>;
}
