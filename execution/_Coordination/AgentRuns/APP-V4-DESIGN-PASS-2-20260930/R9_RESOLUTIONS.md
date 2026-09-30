# R9 rulings — alignment wave (Wave A) of the second design pass

Integrator: HELP_HUMAN. Inputs: the six survey reports in [SURVEY/](SURVEY/)
(S1-A…S1-F). R1–R8 stand except where amended here. Standing labels as
before: SETTLED (an owner decision or accepted text decides it), DERIVED,
INTEGRATION (the integrator's reading; the owner may revisit it), PROPOSED.

Wave A brings every Design file onto the amended basis and the revised
ScopeOfWork contracts. It adds no new design content; that is Wave B.

## R9-1 Checkpoints: the amended wording, and who requests — wording SETTLED; the requester is INTEGRATION

**The text to use (SETTLED: PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as
amended by SCA-V4-001; DEL-02-03 REQ-002 and AC-002 as revised).** Quote the
current texts. Where a file summarizes them, use this summary:

> When a run reaches a declared checkpoint, the required human act is
> requested, and it is recorded as done only when the person performs it,
> whatever the autonomy setting. Holding the run at the checkpoint until the
> act is performed is phased to the governance layer: in the current phase a
> checkpoint is plan guidance that the person and the agents manage, and
> neither the App nor a host's embedded loop enforces a hold, blocks a run,
> or reports a workflow unsupported because a hold cannot be enforced. The
> reserved acts (V4-HI-30) still bind.

Consequences for wording:

- Drop "first half / second half" of V4-WF-05, and every "flagged for the
  next accepted-basis update" marker on these texts. Cite the amended text.
- **In force in every phase:** the act is requested; it is recorded as done
  only when the person performs it; the reserved acts bind.
- **Phased to the governance layer:** holding the run until the act.
- V4-HI-42 is no longer described as "guidance in Phase 1" or as "declared
  checkpoints override autonomy". Its request clause and its record clause
  are in force; only the hold is phased.

**Who requests, in the current phase (INTEGRATION; a reading of DECISION-4's
exact text, put to the owner for confirmation in this run's decision
package).** The owner's words: "I don't want checkpoints in workflows to be
programmed into the app to respond in a certain manner. … I want the human
and agent to work out the plan and any pause or hold point or gate are the
agents to manage their own behaviour accordingly."

- The **agent carrying out the workflow** asks the person for the act when
  its work reaches the checkpoint. It does so because the declared checkpoint
  is part of the plan it was given.
- The **product's part** is: (i) to give the agent the declared checkpoint
  with the workflow; (ii) to offer the person the means to perform the act;
  (iii) to record what it observes — the checkpoint's identity, the request
  where it can be identified, and the act only when the person performs it.
  REQ-002 requires that history "preserve the checkpoint's identity and
  actual disposition", so recording is required where the arrival is
  observed, not optional. A record never says *performed* without the act.
- Neither the App nor a host's embedded loop issues the request in the
  agent's place, pauses the run, or otherwise reacts to the arrival.
- How an App run observes an arrival and a request, and what the record then
  holds, is defined in EXEC in Wave B. Wave A states this ruling and points
  there; it does not invent the mechanism.

## R9-2 R8-11 item 2 and R8-12 item 2, restated against the amended text — DERIVED

- **R8-11 item 2** now reads: D2's "no autonomy grant widens past a reserved
  act" binds. For a declared checkpoint, V4-HI-42's request clause and record
  clause are in force whatever the autonomy setting; whether the run goes on
  before the act is for the person and the agents in the current phase, and
  the host's own treatment of its operations decides what the host does.
- **Corrected by [R10-1](R10_RESOLUTIONS.md):** the bullet below is wrong
  for this case and is kept only as the record of what was ruled. The
  checkpoint is *not reached*, and nothing is requested.
- **R8-12 item 2** (FX-C9 / PC-24) now reads: when the active grant lets the
  host apply directly, no proposal arises and the host may apply. If the
  workflow declares a checkpoint there, its act is still requested, no act is
  recorded by reason of the direct application, and the checkpoint's
  disposition stays *act not performed* unless the person performs it. "No A5
  is required" is replaced by "no A5 is forced, and none is recorded".

## R9-3 Terms — INTEGRATION

The accepted texts say "the current phase" and "the governance phase" (or
"governance layer"). Use those. On first use in a file write "the current
phase (Phase 1)"; afterwards either form may stand where it already does.

## R9-4 Standing labels after the amendments — DERIVED

- A reading that is now in the accepted basis or a revised ScopeOfWork is
  cited to that text and loses its INTEGRATION or "addition" label (for
  example RS R15 and D16 against V4-HI-70 and V4-HOST-02; V4-HOST-01 and
  V4-ARC-11 on model options).
- A reading the owner confirmed in an amendment checkpoint (the OWNER_ITEMS
  of SCA-V4-001 and SCA-V4-002, accepted "as recommended") is labelled
  SETTLED with that citation. The executor cites the item; it does not
  upgrade a label without one.
- PROPOSED items stay PROPOSED.

## R9-5 Pins — INTEGRATION

Each header pins:

- the four basis docs by current sha256, naming SCA-V4-001 and SCA-V4-002;
- the deliverable's current `ScopeOfWork.md` sha256 and the amendment(s) that
  revised it;
- `_DAG/_LATEST.md` → DAG-003 where the file cites the graph;
- rulings: R1–R8 by file, R8 at its current sha256, and this file;
- the SWBPIPE answers at `afb6e063…` wherever they are cited;
- sibling Design files **by version label and section only**. Sibling byte
  hashes live in GUIDE's input table alone, which is re-pinned last.

History lines ("Changes from …", predecessor hashes) are true records and are
not rewritten. Mistyped abbreviations found by the surveys are corrected.

## R9-6 Receivers and interface tables follow the live registers — DERIVED

- Each file's Receivers line and its receiver or interface table is rebuilt
  from the ACTIVE rows of its own `Dependencies.csv` and of its consumers'
  registers, including consumers outside the 14 and the arcs N-18, N-21,
  N-24 and X-1.
- Wave A defines no new contribution. Where a register names a contribution
  the supplier's file does not yet contain, the row says so plainly ("named
  by DEP-…; not yet defined here") and the executor returns it as a Wave B
  item.

## R9-7 The evidence route from DEL-01-01 to DEL-04-03 — DERIVED

DEL-04-03's ScopeOfWork (CLM-004) and RS R13 take supplier evidence from
DEL-01-01 directly. HOSTING §6.4, S-7 and §8.2 are reworded to match: the
evidence is supplied to DEL-04-03; DEL-01-02's custody of in-flight requests
is a separate contribution of a deliverable outside this increment. If
DEL-01-01's own ScopeOfWork says otherwise, the executor stops and returns
the texts instead.

## R9-8 Rulings and review items already made, now applied

- R8-12 item 5 in P (the two evidence-limit labels), and the same two labels
  listed in RS R11.
- V10b S-2 at ADAPTER.
- V6 m-3, m-5, m-6 and m-7; V9 N-7.
- Findings and UNRESOLVED rows that a record has since closed (the surveys'
  NOW items marked "closed by record") are closed with the citation.

## R9-9 Disagreements with no deciding text — procedure

Where two files disagree and no ruling, ScopeOfWork text or owner decision
decides, the executor does not choose. It leaves both texts, and returns the
disagreement as an R10 candidate with the two passages and the options.

## R9-10 What Wave A leaves alone

- No ScopeOfWork, register, `_STATUS.md`, decomposition, scope-change, DAG
  or basis-doc edit. A need for one is returned as a proposed item for a
  later amendment.
- `RELAY_QUESTIONS_SWBPIPE.md`: metadata only. §0–§3, the relayed body, stay
  byte-identical; the executor proves it by hashing that span before and
  after. It stays RELAY-v0.3.
- `PIN_SPIKE_0.158.0.md`: no edit. It is a dated observation record.
- `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md`: SWBPIPE's files; never
  edited.
- The governance-phase definitions are retained as they are, relabelled only
  where R9-1 requires.

## R9-11 Versions

Wave A edits are one version step per file, recorded in a new "Changes from
…" table with R9 item IDs:

| File | From | To |
|---|---|---|
| ACT, AS, RS, C, P, WD, WD-EX, LOOP, PANEL, HOSTING | v0.6 | v0.7 |
| EXEC | v0.4 | v0.5 |
| ADAPTER, CA, XT | v0.4 | v0.5 |
| GUIDE | v0.3 | v0.4 |
| RELAY | v0.3 | v0.3 (metadata only) |
| PIN_SPIKE | v0.1 | unchanged |

All files stay DRAFT: unsupplied, unimplemented and not accepted.
