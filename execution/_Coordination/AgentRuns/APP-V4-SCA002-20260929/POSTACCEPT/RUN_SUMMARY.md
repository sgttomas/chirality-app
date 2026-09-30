# RUN_SUMMARY — APP_V4_SCA_V4_002_POSTACCEPT

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json` `overall_status`. `closure_readiness` is WARN.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, as the scope-change post-acceptance audit (method, "After acceptance": rerun `audit-decomp` against the applied state; H-4) for SCA-V4-002 |
| Executor | node AK2, a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-09-30T02:17:43Z |
| Subject | the working tree at `851ec3d88` plus the uncommitted group-3 application: H-1 (`SOFTWARE_DECOMP.md`), H-2 (`_ScopeChange/_LATEST.md`), the finalized accepted-snapshot records and the group-3 decision snapshot (`COMPARISON.md` §1) |
| Expected source | `_ScopeChange/SCA-V4-002_2026-09-29_1901/` (via `_ScopeChange/_LATEST.md`, `Latest: SCA-V4-002_2026-09-29_1901`) over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` |
| Variant / scope | SOFTWARE. **PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables), the baseline's and POSTCHANGE's scope |
| Script | `audit_checks.py` = `BASELINE/audit_checks.py` with the documented changes (f) and (g) only (the active amendment resolved from the pointer; the `**Accepted predecessor:**` line excluded from the one-snapshot reading); `inventory.json` byte-identical to the baseline's. The unchanged base script's result on the same state is disclosed in `COMPARISON.md` |
| Findings | 0 BLOCKER, 38 WARNING, 100 INFO, 0 EXPECTED_CONSEQUENCE. POSTCHANGE: 0 / 39 / 101 / 0. **COV-139 absent** (the accepted snapshot holds every required artifact); **the registered-parser INFO absent** (the pointer resolves) |
| Coverage | Forward, reverse, context fidelity and objective coverage 100 %; artifact presence 10.78 %. All unchanged |
| Check 10 | `active_snapshot_status` PASS; `handoff_state_status` PASS; active snapshot `SCA-V4-002_2026-09-29_1901`; no incomplete residue; state fields and closure verdict as in the accepted `Handoff_State.md`; registered parser target `SCA-V4-002_2026-09-29_1901`, `pointer_matches_active` True |
| Comparison | `COMPARISON.md` attributes every difference from POSTCHANGE (2 changed inputs; COV-127 and COV-133 wording; COV-139 and COV-140 removed) |

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `COMPARISON.md` | `02d327308d0f1193f020542c099f7bc36179d9374b4b898559f3d481a245a30a` |
| `Decomp_Coverage_IssueLog.csv` | `44697dc6cc7674c5bc7595c55f369e89b88c072f33d2e7efd9c72beb35407116` |
| `Decomp_Coverage_Matrix.csv` | `ab799df150ecd9988919f3cb2f89afff6d0e130455cb51db5adb32823850431f` |
| `coverage_summary.json` | `20a81fcb72a6cef6024b64d203e5e480eb3a0e9f36a8a4bbf536bd266acd5a78` |
| `structure.json` | `97cf39dad55a31abdf44992ab24c303596663726e8862b7929fc7c9943f908f8` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `86c2b41f4aa2739e85381c4cc4c7a97f003811d47edda573c2c9d8df28d205e0` |
| `INPUT_MANIFEST.sha256` | `2324caa14f7d1e1fea592de7cb6834c69f01ae5855398c4ab84f106a9281172b` |
