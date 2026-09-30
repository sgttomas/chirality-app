# RUN_SUMMARY — APP_V4_SCA_V4_002_POSTCHANGE

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json` `overall_status`. `closure_readiness` is WARN.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, as the scope-change post-change audit (method, group-3 preparation step 5) for SCA-V4-002 |
| Executor | node AK1, a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-09-30T01:10:07Z |
| Subject | the working tree at `39c97257b` plus the uncommitted SCA-V4-002 candidate application (10 files; `COMPARISON.md` §1) |
| Expected source | `_ScopeChange/SCA-V4-001_2026-09-28_2155/` (via `_ScopeChange/_LATEST.md`, unchanged) over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` |
| Variant / scope | SOFTWARE. **PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables), the baseline's scope |
| Script | `audit_checks.py` byte-identical to `BASELINE/audit_checks.py`; `inventory.json` byte-identical to the baseline's |
| Findings | 0 BLOCKER, 39 WARNING (38 pre-existing + COV-139), 101 INFO, 0 EXPECTED_CONSEQUENCE. Baseline: 0 / 38 / 101 / 0 |
| Coverage | Forward, reverse, context fidelity and objective coverage 100 %; artifact presence 10.78 %. All unchanged |
| Check 10 | `active_snapshot_status` PASS; `handoff_state_status` PASS; COV-140 INFO (the registered parser; carried, was COV-139) |
| Comparison | `COMPARISON.md` attributes every difference from the baseline |

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `COMPARISON.md` | `a5cc059a5cee8a32c60b50db65efba3f583b0a1b7116742590455c84da5e7d37` |
| `Decomp_Coverage_IssueLog.csv` | `4f104b602fa6855491ba650c01e0bcc5d74f5864fb481d3a1fd6ff928db79492` |
| `Decomp_Coverage_Matrix.csv` | `ab799df150ecd9988919f3cb2f89afff6d0e130455cb51db5adb32823850431f` |
| `coverage_summary.json` | `ba6a393b162ed20f6556877df00a14e9ebebcdebaefe60c96f15c19c44ed8fc1` |
| `structure.json` | `064a165079de417e1ca5b2471c3ef07171cd9a9bdd5ebac94b3355235de826d7` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `ea6c2be722f5e1abb5abeef2844455755ba4b9588172e464678b8e09edf1d30b` |
| `INPUT_MANIFEST.sha256` | `971f03905b05e1934212adbfdf25a3a863075af49b647118927f0cc72566f91d` |
