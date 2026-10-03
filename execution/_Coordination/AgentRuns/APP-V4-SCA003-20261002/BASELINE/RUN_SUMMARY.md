# RUN_SUMMARY — APP_V4_SCA_V4_003_PRECHANGE

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json` `overall_status`. `closure_readiness` is WARN.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, as the scope-change pre-change baseline (method step 5) for SCA-V4-003 |
| Executor | node P3, a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-10-03T02:46:41Z |
| Subject | commit `897a107cc` (unchanged audited inputs at `f47ca8f6b`, where HEAD moved during the run). The working state equals the SCA-V4-002 accepted poststate with its propagation: 148/148 files |
| Expected source | `_ScopeChange/SCA-V4-002_2026-09-29_1901/` (via `_ScopeChange/_LATEST.md`; predecessor SCA-V4-001) over `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; DAG-003 source bytes |
| Variant / scope | SOFTWARE. **PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables). Covers the six packages the SCA-V4-003 proposal records target (20 deliverables); PKG-10 kept for comparability. The post-change audit must reuse this scope |
| Findings | 0 BLOCKER, 35 WARNING, 93 INFO, 0 EXPECTED_CONSEQUENCE. SCA-V4-002 POSTACCEPT (same scope): 0 / 38 / 100 / 0 |
| Coverage | Forward (packages and deliverables), reverse, context fidelity and objective coverage 100 %. Artifact presence 19.61 % (heuristic; was 10.78 %) |
| Check 10 | `active_snapshot_status` PASS; `handoff_state_status` PASS; active SCA-V4-002; no residue; registered parser resolves the pointer |
| Reuse | Not admissible: 21 inputs changed since POSTACCEPT, and Design files changed Check 6 inputs (Decision_Log D-4) |

**Differences from the SCA-V4-002 post-acceptance audit** (`COMPARISON.md`): 3 WARNING and 6 INFO Check 6 absences
cleared, because Design documents and prototypes from design passes 2 and 3 now satisfy the fuzzy file-name rule
(heuristic, not production); COV-127 (ASC-ISS-006) closed by B-06a; five Check 9 INFO rows reworded to cite both
accepted amendments. No new finding.

Findings that bear on SCA-V4-003 are in `Decomp_Coverage_Report.md`, "Findings that bear on SCA-V4-003", in this order:
- the proposal records' SoW and register hashes match the pre-change bytes (20/20, 20/20); the DEL-01-04
  `_STATUS.md` prefix in pass-3 C1-A is mistyped;
- R22-5 would turn 16 Check 6 INFO rows into WARNINGs in the post-change audit;
- DAG-003 binds every target file (130/130 now), so edits mean a currency check and DAG-004;
- Check 5 is MATCH for all 32; any `Deliverables.csv` edit needs its `_CONTEXT.md` mirror;
- Open_Issues edits change Check 9 wording only, unless a status changes;
- the closed and carried items.

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `Brief.md` | `1d8d207f80ba68fc082b516cabf50af95bd8b834d011bf8c7fe3748683f52bc9` |
| `QA_Report.md` | `5c32fe2774b0d02a8495f33510389f0369d70182f029c65d8213319d13283e0a` |
| `Decision_Log.md` | `7913595240f1170494b4590907c4734e44c61c8cdf998dfb5b7e9b2366f157ae` |
| `Decomp_Coverage_Report.md` | `c92c6c2c313abbca5cee6d9ce0cb4a86ec3d6b226c15caeca8c9753339603ed1` |
| `COMPARISON.md` | `29e1f46a0faee0358f61a48b03c5e59ecb4512d77e3bf164fa4297ea8cc629a2` |
| `Decomp_Coverage_IssueLog.csv` | `aca5801c0ae140ced315278606dfed788881dac0a02df3033898687c23fe1f56` |
| `Decomp_Coverage_Matrix.csv` | `2613d19a52641fbed8ab8e1fb52d981d67e670644c4abbec8647a0610a990b99` |
| `coverage_summary.json` | `99f016cc3c3d40f73822ebf625305960a7b77728d20d503195e1ab004f8de37f` |
| `structure.json` | `a5c8b01bc9d1b49b795473693efa2f7422b097f55d6c7f8c1ccbe2a1f8498139` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `8c3bef0676f826692d82261742488dd45148fdb5bb718a9dd9c39e7b903eb0d3` |
| `INPUT_MANIFEST.sha256` | `1c10e3a13bd0a41bea7bc3b5599454eec2856a1091bfcb994146cabece1714aa` |

`structure.json` records absolute local paths, as the earlier runs did. The run moved no pointer and applied nothing.
