# Run summary — SCA-V4-003 (CANDIDATE, before group 3)

- **Amendment:** SCA-V4-003, the contract proposals of App v4 design passes 2
  and 3 (variant `SOFTWARE`, posture `ACCEPTED_PREDECESSOR`; predecessor
  SCA-V4-002). Run: APP-V4-SCA003-20261002.
- **Owner acts** (`AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md`):
  the directions "Proceed as recommended." and "yes, run the closeout.";
  DECISION-1, groups 1–2, "accept the remaining items as recommended"
  (2026-10-03). Group 3 is not yet presented.
- **Decision snapshots:** `checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/`
  (`3e747b7685`) and `…_GROUP-2_2026-10-03/` (`ec267bdb9f`).
- **Pointer:** `_ScopeChange/_LATEST.md` still names SCA-V4-002 (unchanged).
- **Independent review:** not yet run (written before it; see
  `Handoff_State.md`).

## What changed in the candidate

- `_Decomposition/Open_Issues.csv`: OI-009 `Status` `RESOLVED_BY_OWNER_DECISION`
  and `Consequence` (B-02, Q-10 option B); OI-018 `Consequence` pointer
  (B-03, Q-11). Result sha256 `9c2d916c…515d`, the packet's stated hash;
  OPEN 23 → 22.
- `Supersession_Delta.csv` (D-021) and `Supersession_Map.csv` (30 rows).
- The SCA-V4-002 effective-state note (C-02).

Held for group 3: B-01 (Decision Log entry) and C-01 (`_LATEST.md`). After
acceptance: the 19 ScopeOfWork REVISEs, the 20-register UPDATE and DAG-004.

## Checks

- The post-change audit-decomp over PKG-01, 02, 03, 04, 05, 09 and 10 used a
  byte-identical script (`AgentRuns/APP-V4-SCA003-20261002/POSTCHANGE/`).
  - Result: 0 BLOCKER, 52 WARNING, 77 INFO; baseline 0 / 35 / 93.
  - Every difference is attributed: 16 re-graded by the Q-13 act; COV-129
    `EXPECTED_CONSEQUENCE` (this folder before its records); COV-116 and
    COV-121 are B-02/B-03.
  - The GUIDE change at `a68a9e06e2` has no effect.
- DAG-003: 130/130 OK.
- All 42 register targets equal their blobs at `ec267bdb9f` except
  `Open_Issues.csv`; the 19 ScopeOfWork files equal the SOW_REVISIONS prior
  hashes.

| Field | Value |
|---|---|
| `DecompositionTruthState` | `INCOMPLETE` |
| `DerivativePackageState` | `INCOMPLETE` |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `FROZEN` |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | `WARNINGS` |
| `AdjustedAuditState` | `WARNINGS` |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

**Expected closure verdict at group 3:** `OPEN_PENDING_DERIVATIVE_CLOSURE`.

## Records (sha256)

| File | sha256 |
|---|---|
| `Decision_Log.md` | `f85710600c158a5b2834356d4d6f572385b4353597adb53ff1cc5d26b1576379` |
| `Handoff_State.md` | `1f8f6e0ad58b169b29f0ab35aceb64b84e5405de9f44261f1c1837014f820df6` |

## Repository-change evidence (for the responsible current role)

- **Modified:** `execution/_Decomposition/Open_Issues.csv`.
- **Added:**
  - `execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/` (13 files);
  - `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_20261004T002903Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`;
  - `execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/Application/`
    (scripts, logs, DAG currency, target hashes);
  - `…/POSTCHANGE/` (audit outputs and comparison).
- **Suggested commit message:**
  `scope-change(app-v4): SCA-V4-003 groups 1-2 applied as candidate; C-02; post-change audit`
