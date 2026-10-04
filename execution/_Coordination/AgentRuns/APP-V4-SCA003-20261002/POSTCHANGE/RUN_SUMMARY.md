# RUN_SUMMARY — APP_V4_SCA_V4_003_POSTCHANGE

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json` `overall_status`. `closure_readiness` is WARN.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, as the scope-change post-change audit (method, group-3 preparation step 5) for SCA-V4-003 |
| Executor | node AK1 (stage 2), a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-10-04T00:31:55Z |
| Subject | the working tree at `ec267bdb9f` plus the uncommitted SCA-V4-003 candidate application (`COMPARISON.md` §1) |
| Expected source | `_ScopeChange/SCA-V4-002_2026-09-29_1901/` (via `_ScopeChange/_LATEST.md`, unchanged) over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` |
| Variant / scope | SOFTWARE. **PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables), the baseline's scope |
| Script | `audit_checks.py` byte-identical to `BASELINE/audit_checks.py`; `inventory.json` byte-identical to the baseline's |
| Findings | 0 BLOCKER, 52 WARNING (35 pre-existing + 16 re-graded by the Q-13 act + COV-129), 77 INFO, 0 EXPECTED_CONSEQUENCE (script). Baseline: 0 / 35 / 93 / 0 |
| Coverage | Forward, reverse, context fidelity and objective coverage 100 %; artifact presence 19.61 %. All unchanged |
| Check 10 | `active_snapshot_status` PASS; `handoff_state_status` PASS; COV-129 WARNING (the candidate folder before its records; recommended `EXPECTED_CONSEQUENCE`) |
| Comparison | `COMPARISON.md` attributes every difference from the baseline |

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `COMPARISON.md` | `97fe68b9515db0dc332b7c2147d287b9e599d3e62f719bd0ba91a5f658d78088` |
| `Decomp_Coverage_IssueLog.csv` | `042db014b3d24b8b0a92d233db2d1aee53d265bdac685980ac50c72195b6368f` |
| `Decomp_Coverage_Matrix.csv` | `7ac1635384e25fbda7f1dee9198c78be00c643b5931ce354a21081da6a29a7e6` |
| `coverage_summary.json` | `17fd4b0e8d13af9f953b81039118627fc0c3d820abd596ec282de9200911795d` |
| `structure.json` | `92cc0297c3006f6ed433453353a72f185382b08c35b6d615809a9be09f19f520` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `8c3bef0676f826692d82261742488dd45148fdb5bb718a9dd9c39e7b903eb0d3` |
| `INPUT_MANIFEST.sha256` | `b5d8e2ebd6ba0d0440ad9640248828a71647301b04ea575a3eda487c4af708c4` |

`structure.json` records absolute local paths, as the earlier runs did. The run moved no pointer and applied nothing.
