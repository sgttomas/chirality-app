# Group-3 handoff — SCA-V4-002

**Decision.** Checkpoint group 3 is accepted, as recorded in `DECISION.md` and
`ACCEPTED_MANIFEST.csv`. The owner act is DECISION-3, 2026-09-29: "Accept
(Recommended)". The acceptance covers:
- the candidate at `70376aff2`, with `Handoff_State.md` and `RUN_SUMMARY.md`
  at `ffdb56e1a`;
- the acceptance-conditional list H-1…H-4 in that `Handoff_State.md`;
- the propagation route in that `Handoff_State.md` (Q-3).

There is no group-3 correction.

**Next steps, in order.** Each is performed exactly as listed:
1. this folder;
2. H-1 (B-04), applied from `BASIS_AMENDMENT.md` with `{ACCEPT_DATE}` =
   `2026-09-29`, `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` and
   the five clause slots filled (no item declined). The filled "old" block
   must match exactly once;
3. H-2 (C-01): `_ScopeChange/_LATEST.md` rewritten in SPEC §11.2 form from
   the Part C text, with `{AMENDMENT_ID}` = `SCA-V4-002`,
   `{CLOSURE_VERDICT}` = `OPEN_PENDING_DERIVATIVE_CLOSURE`,
   `{GROUP12_REFS}` = the actual decision folders, `{SCA001_CLOSURE}` =
   `OPEN_PENDING_DERIVATIVE_CLOSURE` per the C-02 record at
   `_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/`
   (V14 R-1: the committed folder name is used), `{ARC_LIST}` = N-18, N-21,
   N-24 and X-1, `{OPEN_LIST}` = the open items of the group-3
   Handoff_State including the SCA-V4-001 items still open, `{UTC}` = the
   H-4 record's timestamp. The registered parser must resolve it;
4. H-3, the `Consolidated_Coverage.csv` recompute check for the rows H-1
   shifts (the register carries no `SOFTWARE_DECOMP.md` row, so the check
   is expected to change no byte);
5. finalizing `SCA-V4-002_2026-09-29_1901/` as the accepted snapshot, which
   updates its `Handoff_State.md`, `RUN_SUMMARY.md` and `Decision_Log.md`.
   Its group-1 and group-2 bound files are not rewritten;
6. H-4, the append-only record
   `_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_{UTC}/`, with the
   audit-decomp rerun over PKG-01, 02, 03, 04, 05, 09 and 10 written to the
   run folder's `POSTACCEPT/`. COV-139 should be absent and the registered
   pointer-parser INFO should clear.

**Active snapshot after the pointer move.**
`execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/`. Its `Handoff_State.md`
carries:
- the post-acceptance state fields;
- the derivative-package table;
- the closure verdict;
- the dispositions carried from V14 and the items carried from the
  predecessor.

**State fields after application.**

| Field | Value |
|---|---|
| `DecompositionTruthState` | `COMPLETE` (after H-1…H-3) |
| `DerivativePackageState` | `INCOMPLETE` (Coverage_Telemetry.json `STALE_REBUILD_REQUIRED`; the 17 Design re-pins) |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `IN_PROGRESS` (propagation authorized by DECISION-3) |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | as recorded by H-4 |
| `AdjustedAuditState` | as recorded by H-4 |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`.

**ASC-ISS-001.** Closed by this acceptance: the 17 `DL-SCA-V4-001-…` rows
take effect through the accumulated `Supersession_Map.csv` when `_LATEST.md`
names the accepted snapshot. The closure is confirmed by a superseding
`audit-scope-closure` snapshot for SCA-V4-001; until that snapshot exists,
the CA1 record's `OPEN` status stands as written.

**Propagation authorized (DECISION-3 "Effects"), in order:**
1. the 9 `scope-of-work` MODE=REVISE runs for DEL-10-03, 02-01, 02-03,
   09-07, 01-04, 02-02, 03-03, 04-02 and 01-01, one deliverable per brief,
   each closing with MODE=VERIFY, with `STATUS_POLICY` `NO_STATUS_TOUCH`,
   `AMENDMENT_REF` naming SCA-V4-002, the accepted snapshot and the register
   row, `REVISION_SCOPE` from `SOW_REVISIONS.md`, and
   `PRIOR_CONTRACT_SHA256` equal to the packet's prior hash;
2. B-06a on `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`,
   applied with the REVISEs so that one DAG departure takes it up;
3. `dependency-extract` UPDATE for the revised deliverables, plus
   DEL-04-01/02/03 re-quoting (ASC-ISS-008) and DEP-09-07-016 (ASC-ISS-007);
4. `project-dag`: the DAG-002 currency audit, then TRIGGER=SUCCESSOR for the
   DAG-003 candidate, for owner checkpoint C;
5. the decomposition owner, for `Coverage_Telemetry.json` (bounded brief);
6. the App v4 design undertaking, for the 17 Design re-pins;
7. `audit-scope-closure`, as the closure check for SCA-V4-002 and as the
   superseding snapshot for SCA-V4-001.

**Still unauthorized:**
- any edit not on the acceptance-conditional list;
- `Coverage_Telemetry.json` under SCA-V4-002;
- lifecycle or `_STATUS.md` changes;
- DAG-003 acceptance;
- release.
