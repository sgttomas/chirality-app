# Run summary — SCA-V4-001 (ACCEPTED, active snapshot)

- **Amendment:** SCA-V4-001, the first App v4 scope-change (variant
  `SOFTWARE`, posture `FIRST_AMENDMENT`). Run: APP-V4-BASIS-ALIGN-20260928.
- **Owner acts** (all in
  `AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`):
  - DECISION-6: lifecycle; the arc set.
  - DECISION-7: groups 1–2, "accept the remaining items as recommended".
  - DECISION-8, 2026-09-29: group 3, "Accept (Recommended)". The telemetry
    answer was "Record as stale, fix later (Recommended)". The "local-first"
    answer was "Small follow-on amendment (Recommended)".
- **Decision snapshots:**
  - `checkpoint_snapshots/SCA-V4-001_GROUP-1_2026-09-28/`;
  - `…_GROUP-2_2026-09-28/`;
  - `…_GROUP-3_2026-09-29/`.
- **Active pointer:** `_ScopeChange/_LATEST.md` names this folder.

The candidate version of this file, as presented at group 3, is sha256
`bdcd5ac4f8ddd95488e318b925b7270c56c6e3f736114928898b6e9c22d9efd5`
(at `9ae24fc0f`).

## What changed

The amendment makes 47 `MODIFY` actions, with no structural change:
- the phased checkpoint (V4-WF-05 and related);
- model access with no default (V4-HOST-01, V4-ARC-11);
- the DECISION-5 network destinations (V4-HOST-02, V4-ARC-12);
- host-agent destinations in the run record (V4-HI-70);
- "local-first" amended (PRD §1.1, PKG-05);
- the matching decomposition rows and `_CONTEXT.md` mirrors.

After acceptance, H-1 (A07), H-2 (A17a–c) and H-3 (D-15, the new
`## Decision Log` Change Register) were applied with `{ACCEPT_DATE}` =
2026-09-29. H-4 was the second `Consolidated_Coverage.csv` recompute.
`Handoff_State.md` gives the paths and hashes.

## Checks

- **Before acceptance:**
  - the baseline and post-change audit-decomp over seven packages, with every
    difference attributed;
  - DAG-001 at 130/130;
  - independent review V11: READY FOR GROUP 3.
- **After acceptance (H-5),** in
  `_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/`:
  - the applied bytes equal the listed edits;
  - the audit-decomp rerun in `POSTACCEPT/` finds 0 BLOCKER, 38 WARNING and
    94 INFO;
  - the Change Register part of COV-131 is closed ("Decision Log" binds at
    rank exact);
  - Check 10 (active snapshot) passes;
  - DAG-001 is at 130/130 OK.

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

- the 16 SoW REVISEs (`project-setup` INCREMENTAL → `scope-of-work`
  MODE=REVISE);
- the dependency-register rows;
- the DAG-001 departure and the DAG-002 candidate (owner checkpoint C);
- `Coverage_Telemetry.json` (`STALE_REBUILD_REQUIRED`, owned by the
  decomposition owner);
- the design re-pins;
- `audit-scope-closure`;
- SCA-V4-002, for DEL-10-03 REQ-005.

See `Handoff_State.md`.

## Repository-change evidence (for the responsible current role)

- **Modified:**
  - `projects/chirality-app-v4/docs/PRD.md`, `ARCHITECTURE.md`,
    `HOST_INTEGRATION.md`, `EXAMINATION.md`;
  - `execution/_Decomposition/SOFTWARE_DECOMP.md`,
    `Consolidated_Coverage.csv`;
  - this folder's `Handoff_State.md`, `RUN_SUMMARY.md` and `Decision_Log.md`.
- **Added:**
  - `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/`;
  - `execution/_ScopeChange/_LATEST.md`;
  - `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/`;
  - `execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/POSTACCEPT/`.
- **Suggested commit message:**
  `docs(app-v4): SCA-V4-001 group 3 accepted (DECISION-8) — H-1…H-5, accepted snapshot, _LATEST.md`
