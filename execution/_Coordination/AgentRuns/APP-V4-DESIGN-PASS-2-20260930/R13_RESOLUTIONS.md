# R13 rulings — questions returned by Wave B

Integrator: HELP_HUMAN. Inputs: `WAVE_B/B3.md`, `B4.md`, `B5.md` and the
R12-9 items. R1–R12 stand. Labels as in R9.

## R13-1 A host read without workspace identity or generation (R10-5; R12-9) — INTEGRATION

B3's option B. Such a read is citable only when the host declares that it
supplies no workspace identity or generation (in its C basis profile, or in a
documented host statement). The read then carries the evidence limit "basis
lineage not supplied", and comparisons across lineages read *unknown
(incomparable)*. A read that simply omits an element the host does supply
stays *basis incomplete* (C §5.2 rule 1). ADAPTER RD-2 and C §5.2 are
reworded to say this, and R8-12 item 6's whole-model identity reading sits
inside it.

## R13-2 The two ADAPTER evidence limits (R10-6; R12-9) — INTEGRATION

B4's recommendation. RS R11 adds both as limits the writer records:
"resubmission without prior observation" on the resubmission's operation
entry, and "App-restart interruption" on relaunch. The RS schema adds both
labels. Deriving them at read time is not adopted, because ADAPTER, XT and
CA expect a recorded limit.

## R13-3 The stateless-MCP evidence rule (B5; LOOP G-15) — INTEGRATION

Accepted as B5 wrote it: the server's discovery lists revision 2026-07-28;
the host sends it only per-request metadata and never `initialize`; no
session identifier appears. The record carries "stateless revision declared,
not verified". Verification beyond this is not claimed.

## R13-4 RS format version — INTEGRATION

RS format 0.1 is a PROPOSED draft with no consumer outside this design set.
B5's destination additions and R13-2's labels are made to 0.1 in place, with
a change row. A version step begins when a consumer relies on the format.

## R13-5 A turn while a destination request is pending — INTEGRATION

The call that needs the destination waits for the person's answer; that wait
is the grant being sought (V4-HOST-02: "when the agent asks during its
work"), not a checkpoint hold, so DECISION-4 does not bear on it. The loop
may continue other work in the turn; the person may end the turn, and the
request then closes "unanswered at end". LOOP §5.3 states this.

## R13-6 OBS-1 findings — DERIVED (observation, not qualification)

The files take OBS-1's dated observations as observations at pin 0.158.0,
LM Studio 0.4.16, on one local model:

- With a Responses provider, Codex offered the MCP test tool as a
  `namespace` tool; LM Studio ignored that tool type, so no MCP tool call
  could be made on the local route. HOSTING and ADAPTER record this as an
  observed limit of that route (not of MCP generally), and the design
  consequence: at this pin, an App user on that local route cannot use a
  host's MCP tools. EXEC's "OBS-1 pending" cells for the MCP path stay
  pending with this reason.
- LOOP §4.1's OBS-1 column takes the four Chat Completions points observed
  directly on the local server (Part C).
- ADAPTER takes Part D's per-thread MCP configuration observation (OC-3 (b)).
- HOSTING records the supplier's start-up traffic (chatgpt.com remote
  control, a refused plugins request, the github.com plugin sync) with
  analytics disabled and no sign-in, against U-18 and the start-up-fetch
  item deferred to the phase review.
- OBS-1b's command-line observations are applied the same way when they
  arrive.
