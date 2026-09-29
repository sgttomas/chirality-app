# RUN_SUMMARY — APP_V4_SCA_V4_001_POSTCHANGE

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json` `overall_status`. `closure_readiness` is WARN.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, as the scope-change group-3 post-change audit |
| Executor | node AK1, a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-09-29T04:02:46Z |
| Subject | commit `f4ba34c2c` plus the uncommitted SCA-V4-001 candidate edits (15 files); A07, A17a–c, D-15 not applied |
| Variant / scope | SOFTWARE; PKG-01, 02, 03, 04, 05, 08, 09 (30 deliverables), identical to BASELINE |
| Findings | 0 BLOCKER, 38 WARNING, 94 INFO, 0 EXPECTED_CONSEQUENCE (BASELINE: 0 / 2 / 126 / 0) |
| Coverage | Forward, reverse, context fidelity and objective coverage 100 %; artifact presence 11.22 % (unchanged) |
| DAG-001 currency | `shasum -a 256 -c _DAG/DAG-001/SOURCE_MANIFEST.sha256`: 130/130 OK, exit 0 (`DAG_CURRENCY.txt`) |

## Differences from BASELINE, in one line each (detail: `COMPARISON.md`)

- 37 Check-6 INFO → WARNING: the 14 IN_PROGRESS units (DECISION-6, commit `67a2fac4b`), not the amendment.
- Closed: the stale "no production folders" WARNING (D-16).
- 5 new INFO: five decomposition files now differ from GROUP3 canonical (the candidate edits); two existing ones rehashed.
- Two Check-6 artifact texts changed (D-10b, D-11d).
- Still open as the packet expected to close: the Change Register binding (D-15 acceptance-conditional) and
  COV-119/120 (`Coverage_Telemetry.json` not rewritten; the packet names no writer inside the exact write boundary).

`AuditState` WARNINGS; `AdjustedAuditState` WARNINGS (COMPARISON §3).

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `Brief.md` | `d9f0ed9b7204e647ae8487a5fbd2dd08f4ee57008a6dfdea7d14a33b9c3bdf5f` |
| `QA_Report.md` | `206c15cbd1fccf5a553045d5bcc322245546ae5c9a16dcf68af87bce02c2c687` |
| `Decision_Log.md` | `b7d9b8cb34b31282f3a7bed1aad0cf53008f58bb7830684d4430b08813d138e1` |
| `Decomp_Coverage_Report.md` | `00f39caf76ee8ea68b976c29c1dc96d73510052a8e079a953ca97492b7a18514` |
| `COMPARISON.md` | `25d6dbef6aaea3d5dccd4de7475f97ad8322d7a4b9938649fe4f02ea4178ec3b` |
| `Decomp_Coverage_IssueLog.csv` | `ed5b8e765449124df6b9687bacbe4cbe09449847740716b3b2be55cd34652893` |
| `Decomp_Coverage_Matrix.csv` | `32ec176d9e3a0a169a3651875679a79639f92aa9bfc683add5dd8c3f98eac500` |
| `coverage_summary.json` | `4b6d9622c3beb32cf838e8c811f3d5d74b0ce9b5bac11a91116a0e165d899ca7` |
| `structure.json` | `790bc6ab11772612ee965fe47eb4131d423257ee56b92eb4bce6d7427d6fc86f` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `8dedc11daea28662ec2cec5a90b445b02307b7057b91eeea2e042829a5efe04e` |
| `projections.py` | `83f767308047be682f32ee3334355bd6e50c75ecbc0639877b31a8aff7e88f13` |
| `projections.json` | `bf16258fac8344dace7c55e99dc51e4422df800393d914bacb06f37bbc0fa35b` |
| `DAG_CURRENCY.txt` | `8c93ecdd10b1b403e3e0b9ec84c9c9b37649aae9c40dc5b6123a6b8615518a0c` |

`structure.json` records absolute local paths, as in BASELINE. No pointer was moved.
