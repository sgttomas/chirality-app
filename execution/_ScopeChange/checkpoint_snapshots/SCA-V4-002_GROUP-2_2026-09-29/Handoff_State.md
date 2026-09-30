# Group-2 handoff — SCA-V4-002

**Decision.** Checkpoint group 2 is accepted, as recorded in `DECISION.md`
and `ACCEPTED_MANIFEST.csv` (owner act 2026-09-29, DECISION-2: "accept the
remaining items as recommended"), on the packet revision 2.

**Authoritative register.** `SCA-V4-002_2026-09-29_1901/Amendment_Actions.csv`,
SHA-256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`
(16 rows). `Intake_Actions.csv` is group-1 evidence only.

**Next owning stage.** Checkpoint-group-3 preparation from this snapshot
(`ACCEPTED_GROUP2_DECISION_SNAPSHOT`), candidate path
`execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/`, posture
`ACCEPTED_PREDECESSOR` (`ACCEPTED_PREDECESSOR_SNAPSHOT` =
`execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/`):
1. Apply A-01, B-02, B-05a, B-05b, B-06b and B-06c to the candidate, every
   replacement matching exactly once.
2. Recompute the 31 HOST_INTEGRATION rows of `Consolidated_Coverage.csv`
   (B-01).
3. Generate the candidate `Supersession_Map.csv` with
   `tools/coordination/accumulate_supersession_map.py`, with SCA-V4-001's
   `Supersession_Map.csv` (sha256 `e8e43320…a801`) as the prior map.
4. Run `audit-decomp` read-only over PKG-01, 02, 03, 04, 05, 09, 10 and
   compare with the pre-change baseline; classify findings as
   `EXPECTED_CONSEQUENCE` or new.
5. Check DAG-002 currency (`shasum -a 256 -c _DAG/DAG-002/SOURCE_MANIFEST.sha256`).
6. Dispatch an independent review, then write the candidate `RUN_SUMMARY.md`
   and `Handoff_State.md` with the exact acceptance-conditional edit list and
   a "carried from predecessor" section, and present group 3.

**Status of later stages.**

| Stage | State |
|---|---|
| Exact amendment and propagation decision | Accepted (this snapshot) |
| SCA-V4-001 effective-state record (C-02) | Written after the group-1 snapshot |
| Candidate poststate | Not started at this record |
| Acceptance-conditional edits (B-04, C-01) | Wait for group 3 |
| B-06a (`_LATEST_ACCEPTED.md`) | Waits for group 3; applied with the SoW REVISEs |
| ScopeOfWork REVISE (9) | Wait for group 3 (`project-setup` INCREMENTAL → `scope-of-work` REVISE) |
| Current basis | GROUP3 as amended by SCA-V4-001; `_ScopeChange/_LATEST.md` names `SCA-V4-001_2026-09-28_2155` |
| Pointer posture for group 3 | `ACCEPTED_PREDECESSOR` |

**State fields (at this record).**

| Field | Value |
|---|---|
| `DecompositionTruthState` | `NOT_STARTED` |
| `DerivativePackageState` | `INCOMPLETE` |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `FROZEN` |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | `NOT_RUN` (post-change) |
| `AdjustedAuditState` | `NOT_RUN` |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

**Remains unauthorized until group 3:**
- B-04, C-01 and B-06a;
- moving `_LATEST.md`, and any accepted-state marker on the SCA-V4-002
  folder;
- any `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_DAG`,
  `_STATUS.md` or `Coverage_Telemetry.json` change;
- DAG-003.

**Commit sequence (Q-14).** This snapshot and the files it binds are to be
committed before the application. AK1 has read-only git and makes no commit;
the coordinating session commits.

Reopen only on a material departure from the accepted exact amendment or
register.
