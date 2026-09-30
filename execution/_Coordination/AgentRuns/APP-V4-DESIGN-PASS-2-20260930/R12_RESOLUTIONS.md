# R12 rulings — for Wave B (design development)

Integrator: HELP_HUMAN. Inputs: the surveys' section 8 items left for Wave B,
DECISION-K1 and its Part 2 (matters the integrator takes, not objected to),
the carries from R10, R11 and V17b. R1–R11 stand. Labels as in R9.

## R12-1 What Wave B produces — INTEGRATION

LOOP_INIT asks, for work toward 60%, for interfaces, states, data, operating
sequences, failure behaviour and verification. Wave B adds, per exchanged
contribution:

- **Data:** a PROPOSED schema for each format the files define only as
  element meanings, written as JSON Schema (draft 2020-12) in the Design
  folder that owns the format, beside the Design file, with an example
  instance that validates. Names are Chirality's own; no wire field of a host
  or supplier is selected.
- **States:** one transition table per stateful thing the file owns.
- **Sequences:** the operating sequence for each exchange, with the failure
  behaviour at each step: what fails, who reports it, what record is left,
  what happens next.
- **Verification:** each designed case says what it needs to run (test
  double, fixture, candidate) and, where a local prototype exists, whether it
  ran and what it produced.

Every new structure is PROPOSED unless an accepted text or ruling decides it.
The file's version steps once for Wave B (v0.7 → v0.8; v0.5 → v0.6; GUIDE
v0.4 → v0.5).

## R12-2 Shared parts — INTEGRATION (DECISION-K1 Part 2)

Placement (OI-013, OI-014) stays open for the phase review. Each format is
therefore written as a schema plus conformance fixtures (valid and invalid
instances), which every placement option needs. No file chooses library,
local implementation or service.

## R12-3 Local prototypes — INTEGRATION (DECISION-K1 K1-6)

A prototype is a small script that renders, parses or validates a format, or
simulates a host or supplier, run with the tools already on this machine
(Python 3 standard library; `node` if present). It lives in the owning
deliverable's `Design/prototype/` folder with a README stating what it shows
and that it is not product code. No package is installed. Its output is
recorded as observed, with the command and the date.

## R12-4 The external seam — INTEGRATION (DECISION-K1 Part 2)

The design is developed for both native paths: an MCP server's tools and a
command-line tool that Codex runs. ADAPTER maps each path's observed items to
record elements. One simulated host, specified once in C, offers both paths
and is cited by C, P, ADAPTER and XT.

## R12-5 Workflow registration is a recorded human act — INTEGRATION (DECISION-K1 Part 2)

It is added to ACT's act table as A15 "register workflow revision" (subject:
a workflow revision; content: the revision identity and the draft it derives
from; purpose: make it available in the project), with an RS record kind.
DEL-02-02 AC-006 is its source. A checkpoint may not require A15 in this
increment (no workflow declares one; recorded as a possible extension).

## R12-6 The first connected operation: an option sheet — INTEGRATION (DECISION-K1 Part 2)

CA gains a table that sets each step of the designed activity against what
SWBPIPE's answers say exists (data, not commitments), with columns: step;
SWBPIPE today; examinable against SWBPIPE now (yes/no, why); examinable on the
simulated host (yes/no). It selects nothing (OI-021 stays open) and claims no
join.

## R12-7 LOOP's open rulings — DERIVED / INTEGRATION

- **N-OPEN-1 (DERIVED).** Under the amended V4-HOST-01 and V4-HOST-02 the
  model service the person selected is allowed whether it is local or cloud.
  "User-controlled local endpoint" is therefore a class label in the
  destination record (local or cloud), not a gate. MS-11 is released.
- **T-OPEN-1 / MC-8 (INTEGRATION).** LOOP adopts P §3.1 rule 5 for a
  response with several tool calls of which one is malformed: the valid
  calls are handled on their own; the malformed one gets its own refusal
  result. Both stay PROPOSED until the fixture basis is observed.

## R12-8 The model interface for LOOP's fixtures — INTEGRATION (DECISION-K1 Part 2 and K1-6)

LOOP names a published Chat Completions reference as its **fixture basis**,
labelled "fixture basis, not a product selection" (DEL-05-01 REQ-002 forbids
selecting a product protocol version before its basis exists). The four
open representation points (fragmented tool calls, finish reasons, several
calls per response, "no arguments") are written from that reference, with
its URL and retrieval date. Where a local OpenAI-compatible server is later
observed (OBS-1), the observation is recorded beside them.

## R12-9 The two ADAPTER evidence limits (R10-6) and the host read without workspace identity (R10-5)

Decided in Wave B by nodes B4 and B3 respectively, each returning a ruling
proposal with both passages; the integrator rules in R13 before the second
review.

## R12-10 Carries into Wave B

- V17b m-1 and RS R15 / PANEL §3.8: every place that says a refused or
  declined destination request is **recorded** is labelled PROPOSED (V4-HI-70
  and V4-ARC-12 record destinations contacted; V4-EXM-23 reports a decline to
  the agent). Node B5.
- V17b m-2: LOOP LP-5's A8 mapping labelled DERIVED, as ACT AP-12. Node B5.
- V17-B n-5: EXEC says recording is observation and not a reaction to the
  arrival. Node B2.
- A3 carry: a declaration element for taking up SP-6F. Node B1.
- R10-8: WD's element designating a message as a declared output. Node B1;
  EXEC uses it in B2.
- R11-9: a current-phase case where an earlier act does not count (content no
  longer current, or another kind). Node B2 writes the case; B7 cites it in
  CA W14-05.
- V17-A N-4: one wording of "prior act not counted" across the files. Node B4
  fixes it in RS and records it; B8 follows in GUIDE; other files follow in
  their Wave B nodes.
