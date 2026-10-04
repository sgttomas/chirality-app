# Run summary — SCA-V4-003 (CANDIDATE, before group 3)

- **Amendment:** SCA-V4-003, the contract proposals of App v4 design passes 2
  and 3. Variant `SOFTWARE`; posture `ACCEPTED_PREDECESSOR`; predecessor
  SCA-V4-002. Run: APP-V4-SCA003-20261002.
- **Owner acts** (`AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md`):
  - the directions "Proceed as recommended." and "yes, run the closeout.";
  - DECISION-1, groups 1–2, "accept the remaining items as recommended"
    (2026-10-03).
- Group 3 is not yet presented.
- **Decision snapshots:** `checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/`
  (`3e747b7685`) and `…_GROUP-2_2026-10-03/` (`ec267bdb9f`).
- **Pointer:** `_ScopeChange/_LATEST.md` still names SCA-V4-002 (unchanged).
- **Candidate:** committed at `fa16393978`.
- **Independent review:** `AgentRuns/APP-V4-SCA003-20261002/reviews/V24.md`
  (`64a01f0c4c`), READY FOR GROUP 3 after M-1, with no blocking finding.
  This revision (node AK1-R) makes the M-1 fix and the minors m-1, m-2, m-3,
  m-5 and m-6; see `Handoff_State.md`.

**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE` (proposed, for the owner's acceptance at group 3)

## What changed in the candidate

- `_Decomposition/Open_Issues.csv` (result sha256 `9c2d916c…515d`, the
  packet's stated hash; OPEN 23 → 22):
  - OI-009 `Status` `RESOLVED_BY_OWNER_DECISION` and `Consequence` (B-02, Q-10
    option B);
  - OI-018 `Consequence` pointer (B-03, Q-11).
- `Supersession_Delta.csv` (D-021) and `Supersession_Map.csv` (30 rows).
- The SCA-V4-002 effective-state note (C-02).

Held for group 3: B-01 (Decision Log entry) and C-01 (`_LATEST.md`), with the
finalization F-1 to F-4 and the validation H-3. `Handoff_State.md` lists each
edit exactly. After acceptance: the 19 ScopeOfWork REVISEs, the 20-register
UPDATE and DAG-004.

## Checks

- **Post-change audit-decomp** (`AgentRuns/APP-V4-SCA003-20261002/POSTCHANGE/`):
  PKG-01, 02, 03, 04, 05, 09 and 10, with a byte-identical script.
  - Result: 0 BLOCKER, 52 WARNING, 77 INFO; the baseline was 0 / 35 / 93.
  - 16 findings were re-graded by the Q-13 act (pre-existing, kept in the
    adjusted state).
  - COV-129 is `EXPECTED_CONSEQUENCE` and is closed at `fa16393978`
    (0 / 51 / 77 there).
  - COV-116 and COV-121 are the effects of B-02 and B-03.
  - The GUIDE change at `a68a9e06e2` has no effect.
  - V24 reproduced these results.
- **DAG-003:** 130/130 OK.
- **Register targets:** all 42 equal their blobs at `ec267bdb9f` except
  `Open_Issues.csv`. The 19 ScopeOfWork files equal the SOW_REVISIONS prior
  hashes.
- **Simulated post-acceptance audit:** H-1 and H-2 applied to a scratch copy
  of this revised candidate. Recorded in
  `AgentRuns/APP-V4-SCA003-20261002/Application/SIMULATED_POSTACCEPT.md`.

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

## Artifact hashes

All 13 required artifacts, including this file, are listed in
`AgentRuns/APP-V4-SCA003-20261002/Application/CANDIDATE_ARTIFACTS.sha256`.
The convention: no candidate file lists its own hash or another candidate
record's; that file is written last.

## Repository-change evidence (for the responsible current role)

**Already committed:**
- `fa16393978` holds:
  - `execution/_Decomposition/Open_Issues.csv`;
  - the candidate folder `execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/`
    (13 files);
  - the C-02 note
    `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_20261004T002903Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`;
  - `RUN/Application/` and `RUN/POSTCHANGE/`.
- `64a01f0c4c` holds V24.

**This revision (AK1-R, uncommitted at writing):**
- **Modified:** this folder's `Handoff_State.md`, `RUN_SUMMARY.md` and
  `Decision_Log.md` (one note).
- **Added:** `RUN/Application/simulate_postaccept.py`,
  `simulated_postaccept.json`, `SIMULATED_POSTACCEPT.md` and
  `CANDIDATE_ARTIFACTS.sha256`.
- **Suggested commit message:**
  `docs(app-v4): SCA-V4-003 candidate records revised for group 3 (V24 M-1, minors)`
