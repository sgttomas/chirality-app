# Run summary — SCA-V4-002 (ACCEPTED, active snapshot)

- **Amendment:** SCA-V4-002, the App v4 follow-on alignment (variant
  `SOFTWARE`, posture `ACCEPTED_PREDECESSOR`; predecessor SCA-V4-001). Run:
  APP-V4-SCA002-20260929.
- **Owner acts** (all in
  `AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md`):
  - the direction to start: "Proposal accepted.  Proceed accordingly.";
  - DECISION-2: groups 1–2, "accept the remaining items as recommended";
  - DECISION-3, 2026-09-29: group 3, "Accept (Recommended)".
- **Decision snapshots:**
  - `checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/`;
  - `…_GROUP-2_2026-09-29/`;
  - `…_GROUP-3_2026-09-29/`.
- **Active pointer:** `_ScopeChange/_LATEST.md` names this folder
  (`Latest: SCA-V4-002_2026-09-29_1901`).

The candidate version of this file, as presented at group 3, is sha256
`f259c9b901dade4e8791d0bbaa1d6e945c1b71ef9e18d6bb54c7d6cd90ef1108`
(at `ffdb56e1a`).

## What changed

The amendment makes 16 `MODIFY` actions, with no structural change:
- the HOST_INTEGRATION line break (A-01) and the 31-row recompute (B-01);
- the OI-012 pointer (B-02);
- the DEL-04-01 description qualifier and its mirror (B-05);
- the reading-rule notes on `_Decomposition/_LATEST.md` and five
  `_CONTEXT.md` lines (B-06b, B-06c);
- the supersession delta answering ASC-ISS-001 (17 DL rows + D-014) and the
  accumulated map (29 rows);
- the SCA-V4-001 effective-state record (C-02).

After acceptance, H-1 (B-04, the Decision Log entry) was applied with
`{ACCEPT_DATE}` = 2026-09-29 and `{AMENDMENT_SNAPSHOT}` =
`SCA-V4-002_2026-09-29_1901`; H-2 (C-01) rewrote `_ScopeChange/_LATEST.md`
in SPEC §11.2 form; H-3 confirmed that the Decision Log entry shifts no
`Consolidated_Coverage.csv` row. `Handoff_State.md` gives the paths and
hashes.

Still to come through propagation (authorized by DECISION-3): the 9 SoW
REVISEs (`NO_STATUS_TOUCH`) with B-06a, the register refresh, the currency
audit and the DAG-003 candidate for checkpoint C.

## Checks

- **Before acceptance:**
  - the baseline and post-change audit-decomp over seven packages (PKG-01,
    02, 03, 04, 05, 09, 10), with every difference attributed;
  - DAG-002 at 130/130;
  - independent review V14: READY FOR GROUP 3.
- **After acceptance (H-4),** in
  `_PostAcceptanceValidation/SCA-V4-002_20260930T021014Z/`:
  - the applied bytes equal the listed edits;
  - the registered pointer parser resolves `_LATEST.md`;
  - the audit-decomp rerun in `POSTACCEPT/` finds 0 BLOCKER and 38 WARNING;
    COV-139 is absent; the registered-parser INFO is absent;
  - Check 10 (active snapshot) passes;
  - DAG-002 is at 130/130 OK.

| Field | Value |
|---|---|
| `DecompositionTruthState` | `COMPLETE` |
| `DerivativePackageState` | `INCOMPLETE` |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `IN_PROGRESS` |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | `WARNINGS` |
| `AdjustedAuditState` | `WARNINGS` |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`

## Open downstream work (not executed by the scope-change)

- the 9 SoW REVISEs (`scope-of-work` MODE=REVISE, `NO_STATUS_TOUCH`), with
  B-06a;
- the dependency-register UPDATE;
- the DAG-002 departure and the DAG-003 candidate (owner checkpoint C);
- `Coverage_Telemetry.json` (`STALE_REBUILD_REQUIRED`, owned by the
  decomposition owner; carried);
- the 17 design re-pins (carried);
- `audit-scope-closure` for SCA-V4-002, superseding the SCA-V4-001 CA1
  snapshot (ASC-ISS-001 closed by this acceptance).

See `Handoff_State.md`.

## Repository-change evidence (for the responsible current role)

- **Modified:**
  - `execution/_Decomposition/SOFTWARE_DECOMP.md` (H-1);
  - `execution/_ScopeChange/_LATEST.md` (H-2);
  - this folder's `Handoff_State.md`, `RUN_SUMMARY.md` and `Decision_Log.md`.
- **Added:**
  - `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/`;
  - `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_20260930T021014Z/`;
  - `execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/POSTACCEPT/`.
- **Suggested commit message:**
  `docs(app-v4): SCA-V4-002 group 3 accepted (DECISION-3) — H-1…H-4, accepted snapshot, _LATEST.md`
