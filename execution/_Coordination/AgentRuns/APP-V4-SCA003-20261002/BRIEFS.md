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
