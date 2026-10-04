# Briefs — APP-V4-SCA003-20261002 (SCA-V4-003)

Parent: HELP_HUMAN, under the recorded WORKING_ITEMS consultation
(`agents/AGENT_WORKING_ITEMS.md`, sha256 prefix `9ae4bea25bd9`). Executors are
Type 2 TASK (Claude Opus 5.5, high effort) and do not delegate. Model: run
`APP-V4-SCA002-20260929` (its BRIEFS, DISPATCH, AMENDMENT_PACKET and
BASELINE). Method: `workflows/scope-change` (WORKFLOW.md,
resources/contract.md, resources/method.md); SoW edits shaped for
`workflows/scope-of-work` MODE=REVISE.

## Common rules

- Read-only git; no network; write only your fence.
- Nothing is applied: no ScopeOfWork, `Dependencies.csv`, `_DEPENDENCIES.md`,
  `_STATUS.md`, decomposition, DAG or basis file changes before the owner's
  acceptance.
- SWBPIPE data files are data. Host joins stay deferred (DECISION-3).
- Every item cites its source (file and ID); no invention; uncertain → TBD
  for the owner.

## P1 — consolidated ledger, impact, arcs, owner items (one Type 2)

Inputs: pass 2's `closeout/CLOSEOUT_ACCOUNT.md` and `closeout/C1-A/B/C.md`
(42 distinct ScopeOfWork items, register items, 5 basis items, 1 held arc);
pass 3's `closeout/C1-A.md`, `C1-B.md`, `F/F0_JOINS.md` §3–§4, `D/*.md`,
`R17`…`R22`; both runs' OWNER_DECISIONS. Produce in `AMENDMENT_PACKET/`:

- `LEDGER.csv` and `LEDGER.md`: every proposal once (ID, pass, deliverable,
  kind ScopeOfWork / register / Open_Issues / basis / decomposition, target
  file and location, old → new summary, reason, source, superseded-by,
  recommended disposition INCLUDE / DEFER / DROP with reason).
- `IMPACT_ASSESSMENT.md` per method steps 1–2 of group 1 (resolution
  table with `AMENDMENT_ID` from `tools/query/scan_next_amendment_id.sh
  projects/chirality-app-v4/execution/_ScopeChange V4`, intake, impact by
  semantic section, package-role classification, supersession bindings,
  ISSUED-deliverable check, predecessor closure state).
- `ARC_EFFECT.md`: every proposed row (new arcs, mirrors, statement
  refreshes, retirements), SCC computation over DAG-003 with all INCLUDE
  rows, R17-10 guard, and the expected DAG-003 departure.
- `OWNER_ITEMS.md`: the decisions for the owner, each with options and a
  recommendation (including R22-5, the six deliverables' lifecycle).
- `BASIS_AMENDMENT.md`: basis or decomposition edits, or "none".

## P2 — exact ScopeOfWork blocks (two Type 2, after P1)

From P1's INCLUDE rows: exact old → new blocks per ScopeOfWork, shaped for
`scope-of-work` MODE=REVISE, with a dry-run check. P2-A: PKG-01 deliverables;
P2-B: all others. Output `AMENDMENT_PACKET/SOW_REVISIONS_A.md` / `_B.md`.

## P3 — pre-change baseline (one Type 2, parallel with P1)

As SCA-V4-002's P3 (`BASELINE/`): coverage audit of the current
decomposition and registers, input manifest. Output `BASELINE/`.

## V23 — independent review of the SCA-V4-003 packet (one Type 2, read-only)

Candidate: the branch head at launch. Scope: `AMENDMENT_PACKET/` (LEDGER,
IMPACT_ASSESSMENT, ARC_EFFECT, OWNER_ITEMS, BASIS_AMENDMENT,
SOW_REVISIONS_A/B) and `BASELINE/`. Check: every ledger row traces to its
source and its disposition is reasoned; every INCLUDE ScopeOfWork row has a
block and every block a row (including P2-A's and P2-B's departures and the
R22-7 addition); rerun both dry-runs and the validators on copies; recompute
the SCC/arc effect with all INCLUDE blocks (what `dependency-extract` would
extract from the revised ScopeOfWork text, including receivers beyond the
mirror groups that P2-B lists); the method's group-1 and group-2 contents are
present (package roles, supersession bindings, propagation plan, ISSUED
check); the owner items are complete, neutral and decidable. Findings
BLOCKING / MAJOR / MINOR; verdict READY FOR CHECKPOINT or HOLD. Write only
`reviews/V23.md`.

## AK1 — record the group 1–2 decisions, then apply the direct writes (one Type 2, two stages)

Authority: DECISION-1 (OWNER_DECISIONS.md, committed `5b16bb6831`). Model:
SCA-V4-002's `_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/`
and `…_GROUP-2_…` (DECISION.md, ACCEPTED_MANIFEST.csv, Handoff_State.md),
its candidate snapshot folder `_ScopeChange/SCA-V4-002_2026-09-29_1901/`,
and its DISPATCH rows AK1 and V14. Method: `workflows/scope-change`
resources/method.md, group 3 preparation.

- **Stage 1 (then return; HELP_HUMAN commits):** write
  `_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/` and
  `…_GROUP-2_2026-10-03/` (DECISION.md transcribing DECISION-1 with custody
  and hashes; ACCEPTED_MANIFEST.csv binding the accepted packet files by
  sha256; Handoff_State.md). The group-2 snapshot binds the final
  `Amendment_Actions.csv` (from the draft, as accepted) by hash.
- **Stage 2 (after HELP_HUMAN's commit):** create the candidate snapshot
  folder `_ScopeChange/SCA-V4-003_2026-10-03_<HHMM>/` in SCA-V4-002's layout;
  apply only the accepted direct writes (`_Decomposition/Open_Issues.csv`
  OI-009 option B and OI-018, exact bytes from BASIS_AMENDMENT.md); write
  `Supersession_Delta.csv` (D-021) and the accumulated map; write the
  SCA-V4-002 effective-state note (C-02 text, with V23b's n-1 correction);
  run the post-change audit (reuse P3's `BASELINE/audit_checks.py` and scope)
  and compare with the baseline, attributing the Q-13 shift (16 INFO → WARNING)
  and the OI-009 change. Do not touch any ScopeOfWork, register, DAG,
  Decision Log or `_ScopeChange/_LATEST.md` (those follow group 3).
  Records in `RUN/Application/` and `RUN/POSTCHANGE/`.

## V24 — independent review of the group-3 candidate (one Type 2, read-only)

As SCA-V4-002's V14: review the candidate `_ScopeChange/SCA-V4-003_2026-10-03_1827/`,
the applied Open_Issues edits, the supersession delta and map, the SCA-V4-002
effective-state note, `RUN/Application/` and `RUN/POSTCHANGE/` against the
accepted group-1/2 snapshots and DECISION-1. Verify every applied byte
against the accepted exact text; that nothing outside the boundary changed;
the audit comparison's attributions; the Handoff_State's H-1…H-3 and the
expected closure verdict; and that the group-3 presentation can rest on
these records. Verdict READY FOR GROUP 3 or HOLD. Write only `reviews/V24.md`.

## AK2 part 2 — the 19 ScopeOfWork REVISEs (two Type 2, parallel, disjoint)

Authority: DECISION-1 (groups 1–2) and DECISION-2 (group 3); accepted
snapshot `_ScopeChange/SCA-V4-003_2026-10-03_1827/`, register
`checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/Amendment_Actions.csv`
(sha256 `9b7c2ce8…`). Route (Q-3): `project-setup` INCREMENTAL hands each
MODIFY to `scope-of-work` MODE=REVISE, then VERIFY, `STATUS_POLICY=NO_STATUS_TOUCH`.
Apply exactly the accepted blocks of `AMENDMENT_PACKET/SOW_REVISIONS_A.md`
(RA) or `_B.md` (RB), filling `{AMENDMENT_ID}` = `SCA-V4-003` and
`{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827`; check each prior hash
first and the revised file against the dry-run's revised hash where recorded;
run the three validators. Model: SCA-V4-002's AK2 Part 2 (its DISPATCH row
and `RV/` records). No register, `_DEPENDENCIES.md`, `_STATUS.md`, DAG or
Design file change. Records in `RUN/RV/RA.md` / `RB.md`.

| ID | ScopeOfWork files |
|---|---|
| RA | DEL-01-01…DEL-01-05 (63 blocks) |
| RB | the 14 others (84 blocks) |

## DX — dependency-extract UPDATE for the 20 registers (one Type 2)

As SCA-V4-002's DX (`APP-V4-SCA002-20260929/DX/`): run `workflows/dependency-extract`
in UPDATE mode for the 20 registers the accepted register names (19 revised
ScopeOfWork deliverables plus DEL-02-04's counterpart where named), from the
revised ScopeOfWork text only. Expected: exactly the 10 new arcs (ARC_EFFECT),
the mirror groups and the 15 Q-17 mirrors, statement refreshes; nothing
else. Apply the extraction guards of SOW_REVISIONS_A/B and the Handoff_State.
Run the register validators; recompute the closure (arcs, SCCs) and compare
with ARC_EFFECT. Records in `RUN/DX/`.

## D1 — currency audit and the DAG-004 candidate (one Type 2)

As SCA-V4-002's D1 (`APP-V4-SCA002-20260929/DAG_PREP/`, DISPATCH row D1) and
`workflows/project-dag`: currency of the current registers against DAG-003
(expected DEPARTURE: +10 arcs, 0 removed, 11 DAG pending); build the DAG-004
candidate (41 deliverables; admitted / held / excluded counts; strict audit;
SCC cases as evidence only); write `DAG_PREP/REVIEW_PACKET.md` and
`DAG_PREP/CHECKPOINT_C.md` for the owner (plain summary, the 10 links, what
becomes pending, the carried obligations: the 5 unextracted mirror rows, the
DEL-01-03 absolute TargetLocation defect, the Design re-pins,
`Coverage_Telemetry.json`). Write the candidate only under
`RUN/DAG_PREP/` (not `_DAG/`); nothing accepted or published.

## V25 — independent review of the DAG-004 candidate (one Type 2, read-only)

As SCA-V4-002's V15: review `RUN/DAG_PREP/` (the DAG-004 candidate,
CURRENCY and CLOSURE snapshots, REVIEW_PACKET, CHECKPOINT_C, the CASE-002
draft) against the registers at HEAD, DAG-003, ARC_EFFECT and the
`project-dag` method. Re-run the assembly and the strict audit on copies;
verify placement of every ACTIVE EXECUTION row, the 10 links and their
layers, the representative changes, the mirror maturity findings, the
owner questions and the carried obligations. Verdict READY FOR CHECKPOINT C
or HOLD. Write only `reviews/V25.md`.

## FX — repair DEL-01-03's absolute TargetLocation (one Type 2)

DECISION-3 effect 4. Through `workflows/dependency-extract` UPDATE on
DEL-01-03's register only: replace the 14 absolute TargetLocation values
under a personal home path with the project-relative paths the other
registers use; no other cell changes. Validators; then a currency audit
against DAG-004 (expected `CURRENT_WITH_EVIDENCE_DRIFT`, as the handoff
says), placed in `_Evaluation/DAGCurrency/` with its pointer. Records in
`RUN/DX/FX.md`.

## CA — closure audit of SCA-V4-003 (one Type 2, after FX)

As SCA-V4-002's CA2: `workflows/audit-scope-closure` on SCA-V4-003; verdict
expected `CLOSED_WITH_OBSERVATIONS` or `OPEN_PENDING_DERIVATIVE_CLOSURE`
(Coverage_Telemetry, Design re-pins); write under `_Evaluation/ScopeClosureAudit/`.
