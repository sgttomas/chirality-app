# RUN_SUMMARY — APP_V4_SCA_V4_002_PRECHANGE

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json` `overall_status`. `closure_readiness` is WARN.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, as the scope-change pre-change baseline (method step 5) for SCA-V4-002 |
| Executor | node P3, a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-09-30T00:52:43Z |
| Subject | commit `f05bd1bbd`. The working decomposition equals the SCA-V4-001 accepted poststate (22/22 files) |
| Expected source | `_ScopeChange/SCA-V4-001_2026-09-28_2155/` (via `_ScopeChange/_LATEST.md`) over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` |
| Variant / scope | SOFTWARE. **PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables), derived from the proposed register (PKG-05 because of row 16). The post-change audit must reuse this scope |
| Findings | 0 BLOCKER, 38 WARNING, 101 INFO, 0 EXPECTED_CONSEQUENCE. POSTACCEPT (SCA-V4-001; different scope): 0 / 38 / 94 / 0 |
| Coverage | Forward (packages and deliverables), reverse, context fidelity and objective coverage are 100 %. Artifact presence is 10.78 % |
| Check 10 | `active_snapshot_status` PASS; `handoff_state_status` PASS. COV-139 INFO: the registered parser returns `None` (V13 F2) |
| Reuse | Not admissible: the scoped SoWs changed after POSTACCEPT, and CA1 is not an audit-decomp run (Decision_Log D-4) |

Findings that bear on SCA-V4-002 are listed in `Decomp_Coverage_Report.md`, "Findings that bear on SCA-V4-002", in
this order:
- PKG-05 is missing from IMPACT_ASSESSMENT §4;
- row 14 must keep the `_CONTEXT.md` mirror exact;
- COV-139 and COV-127 confirm items 5a and Q-12;
- the carried items are pre-existing.

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `Brief.md` | `c1de3c49ba2eba000e2041a17f68c31b31147b8e4b3e39de49670e4ffb370f8c` |
| `QA_Report.md` | `60945bc412f4a29d6ea27501d34478a07138228e221f23e395048ef8894aa099` |
| `Decision_Log.md` | `cd23e057d19837b8944fee22c39f93508a04489dd2f2107edc571feec34dc7d7` |
| `Decomp_Coverage_Report.md` | `724e595df77a45a637029f92b880307dc649ff00abadbfc4049f88f60405c4a9` |
| `Decomp_Coverage_IssueLog.csv` | `d7149634d4b6721c6d50abf586a00528162756d6eeb7d2d92f61a2b5249d65de` |
| `Decomp_Coverage_Matrix.csv` | `ab799df150ecd9988919f3cb2f89afff6d0e130455cb51db5adb32823850431f` |
| `coverage_summary.json` | `f89010ea5f0e12b4b3c79a693abb825fe4996cdf317c982086f39d04c6cb0edb` |
| `structure.json` | `faa8ba65fc3a72630362918144ef0dd55cc536dcba5141c55530439c2c6a6f02` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `ea6c2be722f5e1abb5abeef2844455755ba4b9588172e464678b8e09edf1d30b` |
| `INPUT_MANIFEST.sha256` | `957a120bea4a039bfe3f260a5c3b1deb827b96e21efa5d628043756821379aed` |

`structure.json` records absolute local paths, as the earlier runs did. The run moved no pointer.
