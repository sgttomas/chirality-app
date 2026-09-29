# RUN_SUMMARY — APP_V4_SCA_V4_001_PRECHANGE

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json` `overall_status`. `closure_readiness` is WARN.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, used as the scope-change method step 5 pre-change baseline |
| Executor | node P3, a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-09-29T02:30:11Z |
| Basis commit | `306291bddde7862e2a4a14856e325dcf8bf5e2cd` |
| Variant | SOFTWARE |
| Scope | PKG-01, 02, 03, 04, 05, 08 and 09, holding 30 deliverables. The repository holds 11 packages, 41 deliverables, 10 objectives and 262 ledger rows |
| Expected source snapshot | `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` |
| Findings | 0 BLOCKER, 2 WARNING (COV-121, COV-127), 126 INFO, 0 EXPECTED_CONSEQUENCE |
| Coverage | All of these are 100 %: forward packages 7/7, forward deliverables 30/30, reverse, context fidelity and objectives. Artifact presence is 11.22 % (heuristic; all units INITIALIZED) |

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `Brief.md` | `48cbb9da95cbb6214adda503043a32ec5b4369a06921a58ba0cac2ea8c186eac` |
| `Decision_Log.md` | `483b44704df2b694850d82c816fe421f4b2d9a82c9e7783b3c1275e57ed612ac` |
| `QA_Report.md` | `78bb31c131b55124e18bc5df11292add387deb10da167145a7493975ee52f796` |
| `Decomp_Coverage_Report.md` | `38696458a4bce75499869a2a6f5dda5da9e8a3d6b33c39713b483fae08f07ea6` |
| `Decomp_Coverage_IssueLog.csv` | `2976264d5ed2c7a3835bfa417293b845f0b7835c924c8e1f843caf6544e7c05d` |
| `Decomp_Coverage_Matrix.csv` | `75a34e18f046248aba8de60b2268115d41f817d95287866e777a18e687e228b7` |
| `coverage_summary.json` | `d8ac5c4d35012d6a6fb6a3ef2c509caba08a616c8e14a5601bff2a83ee9620f9` |
| `structure.json` | `6f66116ca7139d6ee98723043e1c8dfc8048801bc7cc96a2993f86ba7d4ce7ac` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `08d350b537d357b6ca2ca3f01f1c2db39fcfe14badd94f3bdf9db210cedbd296` |

## Top issues

1. **COV-127, WARNING (9b).** The scope-change Change Register ("Decision Log" or "Revision History") does not bind to
   any heading of `SOFTWARE_DECOMP.md`. U-3 is not confirmed. A30 needs a declared binding.
2. **COV-121, WARNING (9).** The "Checkpoint and next stage" section of `SOFTWARE_DECOMP.md` still says no folders or SoWs
   exist.
3. **COV-119 and COV-120, INFO (9).** `Coverage_Telemetry.json` is candidate-era and stale on open-issue counts. A
   recompute is already planned.
4. **COV-122 to COV-126, INFO (9).** They cover the `_LATEST.md` pointer, the three files that differ from GROUP3, and the
   frozen label in `Objectives.csv`.

## Recommended next action

The integrator stores `BASELINE/coverage_summary.json` as the pre-change baseline, as `Pre_Change_Coverage.json` when
it transcribes the `_ScopeChange` snapshot. Before K1 it resolves the Change Register binding for A30 (COV-127). It
runs the post-change audit with the same seven-package scope.

No pointer was moved. The TASK has no such authority, and `_LATEST.md` belongs to the manager.
