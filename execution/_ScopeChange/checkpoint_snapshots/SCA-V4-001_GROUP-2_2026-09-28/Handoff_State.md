# Group-2 handoff — SCA-V4-001

**Decision.** Checkpoint group 2 is accepted, as recorded in `DECISION.md`
and `ACCEPTED_MANIFEST.csv` (owner act 2026-09-28, DECISION-7: "accept the
remaining items as recommended"), on the packet revision 2.

**Authoritative register.** `SCA-V4-001_2026-09-28_2155/Amendment_Actions.csv`,
SHA-256 `069645d979efa1e0a20f50194acca08afa8715ce647f36ad507c5bf2b76f14d2`
(47 rows). `Intake_Actions.csv` is group-1 evidence only.

**Next owning stage.** Checkpoint-group-3 preparation from this snapshot
(`ACCEPTED_GROUP2_DECISION_SNAPSHOT`), candidate path
`execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/`, posture
`FIRST_AMENDMENT`:
1. Apply BASIS_AMENDMENT Parts A and B and the B7 mirrors to the candidate,
   every replacement matching exactly once, except the acceptance-conditional
   A07, A17a–c and D-15.
2. Recompute `Consolidated_Coverage.csv` (B8).
3. Generate the candidate `Supersession_Map.csv` with
   `tools/coordination/accumulate_supersession_map.py` (no prior map).
4. Run `audit-decomp` read-only over PKG-01, 02, 03, 04, 05, 08, 09 and
   compare with the pre-change baseline; classify findings as
   `EXPECTED_CONSEQUENCE` or new.
5. Check DAG-001 currency (`shasum -a 256 -c _DAG/DAG-001/SOURCE_MANIFEST.sha256`).
6. Dispatch an independent review, then write the candidate `RUN_SUMMARY.md`
   and `Handoff_State.md` with the exact acceptance-conditional edit list, and
   present group 3.

**Status of later stages.**

| Stage | State |
|---|---|
| Exact amendment and propagation decision | Accepted (this snapshot) |
| Candidate poststate | Not started at this record |
| Acceptance-conditional edits (A07, A17a–c, D-15) | Wait for group 3 |
| ScopeOfWork REVISE (16) | Wait for group 3 (`project-setup` INCREMENTAL → `scope-of-work` REVISE) |
| Current basis | `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; `_LATEST.md` absent |
| Pointer posture for group 3 | `FIRST_AMENDMENT` |

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
- A07, A17a–c and D-15;
- `_LATEST.md` and any accepted `SCA-*` snapshot;
- any `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_DAG` or
  `_STATUS.md` change;
- DAG-002 (checkpoint C).

Reopen only on a material departure from the accepted exact amendment or
register.
