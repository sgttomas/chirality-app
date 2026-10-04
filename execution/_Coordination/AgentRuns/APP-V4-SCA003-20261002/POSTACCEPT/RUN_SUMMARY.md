# RUN_SUMMARY — APP_V4_SCA_V4_003_POSTACCEPT

**RUN_STATUS = WARNINGS.** This equals `coverage_summary.json` `overall_status`.

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-decomp`, as the SCA-V4-003 post-acceptance validation audit (H-3) |
| Executor | node AK2 (part 1), a Type 2 TASK (Claude Code subagent); no delegation |
| Timestamp (UTC) | 2026-10-04T01:00:17Z |
| Subject | the working tree at `84b520742d` plus the uncommitted F-1, H-1, H-2, F-3 and F-4 edits |
| Expected source | `_ScopeChange/SCA-V4-003_2026-10-03_1827/` (named by `_ScopeChange/_LATEST.md` after H-2) |
| Scope | SOFTWARE; PKG-01, 02, 03, 04, 05, 09, 10 (32 deliverables) |
| Script | `audit_checks.py` byte-identical to `BASELINE/audit_checks.py` |
| Findings | 0 BLOCKER, 51 WARNING, 77 INFO, 0 EXPECTED_CONSEQUENCE |
| Check 10 | PASS / PASS; active snapshot SCA-V4-003; registered parser match True |
| Comparison | `COMPARISON.md`: IssueLog and Matrix byte-identical to the simulation; against POSTCHANGE, COV-129 is absent and COV-123 carries the H-1 hash |

## Snapshot files (sha256; this file is not self-listed)

| File | sha256 |
|---|---|
| `COMPARISON.md` | `54d00949539b05287abab95441438a21f15fd6e89db248f1a00ffdbded4171c6` |
| `Decomp_Coverage_IssueLog.csv` | `fd1f4b5bcb31908966d0b1c6914b6db93e5de4241fe7b1894f47a1549d3b9f0d` |
| `Decomp_Coverage_Matrix.csv` | `7ac1635384e25fbda7f1dee9198c78be00c643b5931ce354a21081da6a29a7e6` |
| `coverage_summary.json` | `bc7d36bdd888306a27f753363b02704bf5a03f917f7330500633784ba5182e99` |
| `structure.json` | `c2efe7deaf3169d0bf9dee25289307b0d795d97491ccd0dc7ff35e18aa701544` |
| `inventory.json` | `e9088c41301596aaed3d9ddde8033544543186b4ad175b6202294713a0499014` |
| `audit_checks.py` | `8c3bef0676f826692d82261742488dd45148fdb5bb718a9dd9c39e7b903eb0d3` |
| `INPUT_MANIFEST.sha256` | `b19473f8383225dd238dd243782249ab7deb5b946022328c011aff0573fe5757` |
