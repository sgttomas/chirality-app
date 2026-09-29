# RUN_SUMMARY — APP_V4_SCA_V4_001_POSTACCEPT

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json`
`overall_status`. `closure_readiness` is WARN.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, as the scope-change post-acceptance audit (H-5) |
| Executor | node AK2, a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-09-29T13:35:41Z |
| Subject | commit `3d006a909`, plus the uncommitted post-acceptance edits: H-1…H-4, the finalized snapshot and `_ScopeChange/_LATEST.md` |
| Variant / scope | SOFTWARE; PKG-01, 02, 03, 04, 05, 08, 09 (30 deliverables), identical to BASELINE and POSTCHANGE |
| Findings | 0 BLOCKER, 38 WARNING, 94 INFO, 0 EXPECTED_CONSEQUENCE. POSTCHANGE: 0 / 38 / 94 / 0. BASELINE: 0 / 2 / 126 / 0 |
| Check 10 | `active_snapshot_status` PASS; `handoff_state_status` PASS |
| Coverage | Forward, reverse, context fidelity and objective coverage 100 %; artifact presence 11.22 % (unchanged) |

## Differences from POSTCHANGE, one line each (detail: `COMPARISON.md`)

- **The Change Register part of COV-131 is closed:** "Decision Log" binds at
  rank exact (H-3, D-15). COV-131 remains a WARNING only for the pre-existing
  heading bindings of Ledger, Objectives, Partitions and Production Units.
- COV-122 and COV-127 were rehashed (H-4, H-3).
- Check 10 now runs and passes, because `_LATEST.md` exists.
- Still open: COV-119/120 (`Coverage_Telemetry.json`, `STALE_REBUILD_REQUIRED`
  per DECISION-8). Also open are the 37 lifecycle WARNINGs (DECISION-6).

`AuditState` is WARNINGS and `AdjustedAuditState` is WARNINGS
(COMPARISON §4). DAG-001 currency is in
`_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/DAG_CURRENCY.txt`
(130/130 OK).

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `Brief.md` | `f434d62e91e17cfe52f3981c85885c9126d50ad592c40708adc9cab70d312265` |
| `QA_Report.md` | `45a15dab46be189dff6b40fd4238245e372a00fe8b214f3063697dcde19ea18c` |
| `Decision_Log.md` | `d5094e771bcaba973d57e3ffc10c92f8826892e15feca39614a2079735c7f0ee` |
| `COMPARISON.md` | `f01cbb82410cd594421629b12c21676c6974c7b760e4723033e67fd392cbe57d` |
| `Decomp_Coverage_IssueLog.csv` | `ecaea862342528a653c1bfe0c1b3e9fbc14fd6698ed29cfd75d5ab9cadcbe45d` |
| `Decomp_Coverage_Matrix.csv` | `32ec176d9e3a0a169a3651875679a79639f92aa9bfc683add5dd8c3f98eac500` |
| `coverage_summary.json` | `a8d3d45b03fcc17dd01bc5ee066874675fab89fa23feb594da7dede217ab53c6` |
| `structure.json` | `e296b2e5be58a8ab1177bc8161b4798a21ceb94f195504b6989a81ff10a51a47` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `013a0d73ace71f1f30c85248781061135b6859416078a152841eeaed3ebea238` |

`structure.json` records absolute local paths, as in BASELINE. The run moved
no pointer; `_ScopeChange/_LATEST.md` was created by the finalization step
before this audit.
