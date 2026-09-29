# Decomposition coverage report — post-change audit of the SCA-V4-001 candidate

**Run:** `APP_V4_SCA_V4_001_POSTCHANGE`, 2026-09-29T04:02:46Z. Subject: `f4ba34c2c` plus the uncommitted SCA-V4-001
candidate (groups 1–2 accepted; A07, A17a–c and D-15 not applied). Variant SOFTWARE.

**Scope:** PKG-01, 02, 03, 04, 05, 08 and 09 (30 deliverables), as in BASELINE. Repository: 11 packages, 41
deliverables, 10 objectives, 262 ledger rows.

**Overall status: WARNINGS. Closure readiness: WARN.** 0 BLOCKER, 38 WARNING, 94 INFO, 0 EXPECTED_CONSEQUENCE.

Derivative evidence for scope-change group-3 preparation; not decomposition truth. The TASK moves no pointer. The
comparison with BASELINE, with the cause of every difference, is in [COMPARISON.md](COMPARISON.md).

## Summary of the 12 checks

| # | Check | Verdict | Key result |
|---|---|---|---|
| 1 | Forward coverage: Packages | PASS | 7/7 |
| 2 | Forward coverage: Deliverables | PASS | 30/30 (41/41 repository-wide), all in `1_Working` |
| 3 | Reverse coverage: Folders | PASS | 100 % |
| 4 | ID consistency | PASS | COV-001 INFO: the DEL-01-05 folder label (unchanged) |
| 5 | Context fidelity | PASS | 30/30 MATCH, including the four `_CONTEXT.md` files the candidate edited (DEL-02-03, 05-01, 05-02, 09-07). INFO: `PackageID` listed twice in each (COV-002…031) |
| 6 | Artifact presence | WARN | 11/98 (11.22 %), unchanged. 37 absences are WARNING because 14 units are IN_PROGRESS (DECISION-6); 50 remain INFO |
| 7 | Objective mapping | PASS | 10/10 objectives supported; registers and telemetry objective counts agree; integrity PASS |
| 8 | Ledger integrity | PASS | 262 rows (234 IN / 15 OUT / 13 TBD); mappings unchanged by the amendment |
| 9 | Derivative package parity | SKIPPED | Not variant-owned. Other observations below (0 WARNING, 12 INFO) |
| 9b | Package-shape conformance | WARN | COV-131: no heading binds; the Change Register stays unbound until D-15 (acceptance-conditional) |
| 10 | Active snapshot and handoff state | SKIPPED | `_ScopeChange/_LATEST.md` absent (FIRST_AMENDMENT) |
| 11 | Lifecycle distribution | INFO | Scoped: INITIALIZED 16, IN_PROGRESS 14. All: INITIALIZED 27, IN_PROGRESS 14 |
| 12 | Comparison mode | done | Against `APP_V4_SCA_V4_001_PRECHANGE`: [COMPARISON.md](COMPARISON.md) |

## Other derivative-currency observations (Check 9)

| Issue | Severity | Surface | Observation |
|---|---|---|---|
| COV-119 | INFO | `Coverage_Telemetry.json` | Open-issue counts stale (pre-existing; not rewritten, COMPARISON D11) |
| COV-120 | INFO | `Coverage_Telemetry.json` | Candidate-era standing and "no folders or SoWs" check (pre-existing) |
| COV-121 | INFO | `_Decomposition/_LATEST.md` | Reads `Latest: (none)` (pre-existing; BASELINE COV-122) |
| COV-122, 123, 126, 128, 129 | INFO | `Consolidated_Coverage.csv`, `Deliverables.csv`, `Packages.csv`, `ScopeLedger.csv`, `Vocabulary_Map.csv` | Differ from GROUP3 canonical: SCA-V4-001 candidate edits |
| COV-124, 125, 127 | INFO | `External_Dependencies.csv`, `Open_Issues.csv`, `SOFTWARE_DECOMP.md` | Differ from GROUP3 canonical (pre-existing; the last two rehashed by D-14a/b and D-16) |
| COV-130 | INFO | `Objectives.csv` | Frozen "final Group3 acceptance remains pending" label (pre-existing) |

The BASELINE WARNING on the stale "no production folders" sentence is closed by D-16. The main-document package summary
table agrees with the registers on all 11 rows.

## What to fix for a cleaner rerun (not in this TASK's authority)

- After group-3 acceptance: apply D-15 (closes the Change Register part of COV-131), A07 and A17a–c, then recompute
  `Consolidated_Coverage.csv` again.
- Decide the `Coverage_Telemetry.json` rewrite (COV-119/120): writer, and the `standing`, `Revision` and `Date` values.
- Anticipated artifacts of the 14 IN_PROGRESS units are produced by their own production work (Check 6).
