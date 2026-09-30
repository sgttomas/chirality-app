# SCA-V4-002 checkpoint group 3 — accepted audited poststate

Recorded 2026-09-29 by node AK2, a Type 2 TASK (Claude Code subagent; no
delegation) dispatched by the coordinating session of run
`APP-V4-SCA002-20260929`, which presented checkpoint B (K2) to the owner.
This record transcribes the owner's act as it is recorded in the run's
`OWNER_DECISIONS.md`. It is not a new request for the same decision, and it
claims no inspection the owner did not perform.

## Custody of the act

| Item | Value |
|---|---|
| Record | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md`, section "Checkpoint B: SCA-V4-002 group 3 (owner, exact, 2026-09-29), DECISION-3" |
| Record sha256 at transcription | `f2dda563beaadc737c73d897d6801a78332e5a722334dd8ef6d26c0dd0c38ef3`. The working-tree file and the blob at `851ec3d88` give the same hash |
| Commit that added DECISION-3 | `851ec3d88bb090f0bc63ad7075b1668ad65afb39` ("docs(app-v4): SCA-V4-002 checkpoint B — group 3 accepted (DECISION-3)", 2026-09-29 20:01:45 -0600). It changes only that file (25 insertions) |
| Channel | As the record states, this is the owner's answer to a structured question in the active chat, transcribed by the recorder. AK2 did not observe the chat and relies on that record |
| Earlier acts in this amendment | The direction to start ("Proposal accepted.  Proceed accordingly.") and DECISION-2 (groups 1 and 2, "accept the remaining items as recommended"), recorded in `../SCA-V4-002_GROUP-1_2026-09-29/` and `../SCA-V4-002_GROUP-2_2026-09-29/` |

## What the owner had in front of them

As recorded in DECISION-3 "Custody":
- the candidate `_ScopeChange/SCA-V4-002_2026-09-29_1901/`, applied at
  `70376aff2`;
- its `Handoff_State.md` and `RUN_SUMMARY.md` at `ffdb56e1a`;
- review V14, with the verdict READY FOR GROUP 3;
- the six-versus-seven-package audit scope (V14 R-3), disclosed in the
  question.

The commit `ffdb56e1a` → `851ec3d88` changes only `OWNER_DECISIONS.md`, so
every presented file has its presented bytes at `851ec3d88`.
`ACCEPTED_MANIFEST.csv` binds those bytes.

The presented `Handoff_State.md` (sha256 `c522d3fe…362b`) contains:
- the exact acceptance-conditional list H-1…H-4 with the slots filled at
  acceptance;
- the propagation table for the accepted route (Q-3) and the closure verdict
  `OPEN_PENDING_DERIVATIVE_CLOSURE`;
- the COV-139 classification (`EXPECTED_CONSEQUENCE`) with the 16-artifact
  list;
- the dispositions carried from V14 (R-1…R-4, O-5);
- the "carried from the predecessor" section.

The presented `RUN_SUMMARY.md` is sha256 `f259c9b9…1108`.

## The owner's act (verbatim)

| Question presented | Owner's answer (exact label) |
|---|---|
| Checkpoint B (scope-change group 3 for SCA-V4-002): accept the applied, audited result? | "Accept (Recommended)" |

No correction or exception was recorded.

## Interpretation (recording role's reading, not owner text)

| Item | Effect |
|---|---|
| Audited poststate | The candidate at `70376aff2`, with its records at `ffdb56e1a`, is accepted as presented. That covers A-01, B-01, B-02, B-05a, B-05b, B-06b, B-06c, the supersession delta and accumulated map, and the post-change audit. So are its closure verdict `OPEN_PENDING_DERIVATIVE_CLOSURE` and its explicitly open downstream obligations |
| Acceptance-conditional list | H-1 (B-04) is applied exactly from `BASIS_AMENDMENT.md` (sha256 `091871fd…4238`) with `{ACCEPT_DATE}` = `2026-09-29` (DECISION-3 "Effects") and `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901`; the five clause slots are all filled because the owner declined no item (Q-6, Q-7, Q-10 option (a), Q-11, Q-12 option (a)); Q-5 option A adds nothing. H-2 (C-01) rewrites `_ScopeChange/_LATEST.md` in SPEC §11.2 form from the Part C text, naming SCA-V4-001 as the predecessor and the C-02 record at its committed path `_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/` (V14 R-1). H-3 is the `Consolidated_Coverage.csv` recompute check for rows H-1 shifts. H-4 is the post-acceptance record under `_ScopeChange/_PostAcceptanceValidation/`, with an audit-decomp rerun over the seven packages (PKG-01, 02, 03, 04, 05, 09, 10) |
| Accepted amendment snapshot | The candidate folder `_ScopeChange/SCA-V4-002_2026-09-29_1901/`, in the contract's form `SCA-{NNN}_{YYYY-MM-DD}_{HHMM}`, is finalized as the immutable accepted snapshot. `_ScopeChange/_LATEST.md` is moved to it. Its group-1 and group-2 bound files are not rewritten. Only its unbound status records are updated after this act: `Handoff_State.md`, `RUN_SUMMARY.md` and `Decision_Log.md` |
| Supersession | The 18 `Supersession_Delta.csv` bindings (17 `DL-SCA-V4-001-…` rows and D-014) take effect when `_LATEST.md` names this snapshot, through the accumulated `Supersession_Map.csv` (29 rows) |
| ASC-ISS-001 | Closes on this acceptance (DECISION-3 "Effects"), to be confirmed by a superseding `audit-scope-closure` snapshot for SCA-V4-001 |
| COV-139 | `EXPECTED_CONSEQUENCE` of the accepted sequence, as presented; the H-4 rerun confirms it absent once the candidate holds its records |
| R-3 (six versus seven packages) | Disclosed in the question; the seven-package scope is the accepted audit scope, and no packet byte is edited |
| Reopening | No affected deliverable is `ISSUED` or `CHECKING` (five IN_PROGRESS, four INITIALIZED among the nine). This acceptance authorizes no `ISSUED → IN_PROGRESS` reopening, and no `write_status.sh --amendment` path arises. `ScopeChanging` `YES` on register row 1 (DEL-10-03) records a scope-changing text edit to an INITIALIZED deliverable, not a reopening |

## What this acceptance authorizes and does not authorize

It authorizes:
- this decision folder;
- H-1…H-3 exactly as listed, and the H-4 post-acceptance record;
- finalizing `SCA-V4-002_2026-09-29_1901/` as the accepted snapshot, and
  moving `_ScopeChange/_LATEST.md` to it;
- the propagation recorded in DECISION-3 "Effects", each step through its
  owning workflow and its own brief, in this order:
  1. the 9 `scope-of-work` MODE=REVISE runs (`STATUS_POLICY`
     `NO_STATUS_TOUCH`), one deliverable per brief, each closing with
     MODE=VERIFY, with B-06a applied alongside them;
  2. the dependency-register refresh (`dependency-extract` UPDATE);
  3. the `project-dag` currency audit and the DAG-003 candidate, for owner
     checkpoint C.

It does not authorize:
- any edit not on the acceptance-conditional list;
- any `Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG/` write under this
  acceptance (the register UPDATE and DAG-003 have their own briefs);
- any write to `Coverage_Telemetry.json`;
- any `_STATUS.md` or lifecycle change;
- acceptance of DAG-003, which is owner checkpoint C;
- any release, publication or reliance claim.

The standing Git authorization governs commits and merges. This TASK makes
none.

## Basis

- Accepted group-1 snapshot `checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/`
  (`DECISION.md` `5e7a321e849d9add0ccc87d01b976919ac6b6f0c45f2bd03f6b14e4bc0b43688`,
  `ACCEPTED_MANIFEST.csv` `e8e51b24b855341a2cfa06059b3f808c5a6c9f6b6afcc5c52d58390b20e86df4`).
- Accepted group-2 snapshot `checkpoint_snapshots/SCA-V4-002_GROUP-2_2026-09-29/`
  (`DECISION.md` `094aec9d3b8a302385dd9338ce873240cd66f9be7a778207a6c3961657b71fa0`,
  `ACCEPTED_MANIFEST.csv` `fd851925d2ccb73d8b5eb0cf9f225747b8a03d2fc0e197b538dec542c5e9a2ad`).
  It binds the register `Amendment_Actions.csv` at
  `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`, which is
  unchanged.
- Pointer posture `ACCEPTED_PREDECESSOR`. `_ScopeChange/_LATEST.md` (sha256
  `a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d`) names
  the accepted predecessor `SCA-V4-001_2026-09-28_2155` before this act.
- Evidence base: commit `851ec3d88`, working tree clean.
