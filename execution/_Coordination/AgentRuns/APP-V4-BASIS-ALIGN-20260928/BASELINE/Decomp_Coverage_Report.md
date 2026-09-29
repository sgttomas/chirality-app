# Decomposition coverage report — pre-change baseline for SCA-V4-001 (proposed)

**Run:** `APP_V4_SCA_V4_001_PRECHANGE`, 2026-09-29T02:30:11Z, basis commit `306291bdd`. The variant is SOFTWARE.

**Subject:** the working package in `projects/chirality-app-v4/execution/_Decomposition/`, with its deliverable folders.
The expected source snapshot is `checkpoint_snapshots/GROUP3-20260928T001055Z`, resolved via `_LATEST_ACCEPTED.md`.

**Scope:** PKG-01, 02, 03, 04, 05, 08 and 09, which hold 30 deliverables. The whole repository holds 11 packages, 41
deliverables, 10 objectives and 262 ledger rows.

**Overall status: WARNINGS. Closure readiness: WARN.** There are 0 BLOCKER, 2 WARNING, 126 INFO and 0
EXPECTED_CONSEQUENCE findings.

This is derivative evidence for the scope-change pre-change comparison (method step 5). It is not decomposition truth.
The TASK moves no pointer.

## Summary of the 12 checks

| # | Check | Verdict | Key result |
|---|---|---|---|
| 1 | Forward coverage: Packages | PASS | 7/7 declared packages have folders; all 11 exist repository-wide |
| 2 | Forward coverage: Deliverables | PASS | 30/30 scoped (41/41 repository-wide) have exactly one folder, in `1_Working` |
| 3 | Reverse coverage: Folders | PASS | No undeclared DEL or PKG folder; reverse coverage is 100 % |
| 4 | ID consistency | PASS | All IDs and parent packages match; one INFO label difference: DEL-01-05 folder uses `OAuth-sign-in` for `OAuth/sign-in` |
| 5 | Context fidelity | PASS | 30/30 `_CONTEXT.md` MATCH on the 15 compared fields. SoW frontmatter identity, scope refs and objective refs match the registers. INFO: every `_CONTEXT.md` lists `PackageID` twice, with identical values |
| 6 | Artifact presence | PASS (INFO only) | All SOW_V1 and valid. Heuristic artifact presence is 11/98 (11.22 %). All 30 units are INITIALIZED, so the 87 absences are INFO |
| 7 | Objective mapping | PASS | 10/10 objectives have active support. `Objectives.csv` MappedDeliverables and ScopeItemIDs agree with `Deliverables.csv` and the ledger `ObjectiveIDs` for all 10. Telemetry objective counts agree. Objective-evidence integrity: PASS |
| 8 | Ledger integrity | PASS | 262 rows (234 IN / 15 OUT / 13 TBD). Every IN row maps to existing deliverables, reciprocal with `CoversScopeItems`. No OUT/TBD row carries a mapping. 0 rows without an objective |
| 9 | Derivative package parity | SKIPPED | Not variant-owned for SOFTWARE. Other derivative-currency observations are listed below (1 WARNING, 7 INFO) |
| 9b | Package-shape conformance | WARN | Companion inventory is present and complete. Heading binding is unresolved (COV-127) |
| 10 | Active snapshot and handoff state | SKIPPED | `execution/_ScopeChange/_LATEST.md` is absent (FIRST_AMENDMENT posture) |
| 11 | Lifecycle distribution | INFO | Scoped: INITIALIZED 30. Repository-wide: INITIALIZED 41 |
| 12 | Comparison mode | not requested | This run is the "pre" side for the later post-change comparison |

## Key figures (`coverage_summary.json`)

| Measure | Value |
|---|---|
| Partitions (packages) declared / found | 7 / 7 (100 %) |
| Production units declared / found | 30 / 30 (100 %) |
| Reverse coverage | 100 % |
| Context fidelity | 100 % |
| Artifact presence (heuristic) | 11.22 % |
| Objective coverage | 100 % |
| Deliverables without an objective mapping | 0 |
| IN ledger rows without an objective mapping | 0 (178 scoped; 234 repository-wide) |
| Scoped ledger rows | 178 IN / 14 OUT / 7 TBD |
| Lifecycle | INITIALIZED 30 (41 repository-wide) |

## Findings that bear on the amendment

1. **COV-127 · WARNING · Check 9b: the Change Register binding is unresolved (answers U-3).** The audit-decomp Variant
   Section Binding was applied to the `##` headings of `SOFTWARE_DECOMP.md`. The SOFTWARE Change Register targets
   "Decision Log" and "Revision History" get no exact, prefix or substring hit, so U-3 is **not confirmed**.
   - "Artifact coverage and decision/change log" does contain "decision/change log", but not "decision log".
   - Only the PROJECT-form target "Change Log" hits that heading, by substring.
   - The scope-change contract says to "stop and report an unresolved binding rather than resolving by position". A30
     (`SOFTWARE_DECOMP.md#change-log`) therefore needs a declared basis before checkpoint group 1. Two options:
     - an explicit, recorded binding accepted with the packet, or
     - a heading that binds, for example a `## Decision Log` section added by A30 itself.
   - The anchor `#change-log` does not match the GitHub slug of the actual heading
     (`#artifact-coverage-and-decisionchange-log`).
   - The same heading test also finds no Scope Ledger, Objectives, Packages or Deliverables section. Those semantics bind
     only through `Companion_Inventory.csv` to the registers, which the method admits (step 0.2). That is sufficient for
     this audit, but the main document itself is not self-binding.
2. **COV-121 · WARNING · Check 9 derivative currency: the main document contradicts itself.** Its "Checkpoint and next
   stage" section still says "No production Package/Deliverable folders or local ScopeOfWork contracts have been
   created".
   - Its own status line says local contract definition is underway.
   - 41 deliverable folders, each with a `ScopeOfWork.md`, exist.
   - A30 edits this document. The group-2 amendment text should correct or supersede this sentence, or state why it
     remains.
3. **COV-119 and COV-120 · INFO: `Coverage_Telemetry.json` is the frozen Group3 copy.**
   - Its `standing` is still `GROUPS1_2_ACCEPTED_GROUP3_CANDIDATE`, and its check `no_production_folders_or_SoWs_created`
     is still `true`.
   - It reports `ActiveOpenIssueCount` 24 with resolved IDs OI-015 and OI-025. The working `Open_Issues.csv` has 23 OPEN,
     and OI-017 is `RESOLVED_FOR_CURRENT_DEFINITION_RUN`.
   - IMPACT_ASSESSMENT §8 already plans a RECOMPUTE by the post-change baseline. The post-change comparison should treat
     these as pre-existing, not as amendment effects.
4. **COV-123 to COV-125 · INFO.** The working `SOFTWARE_DECOMP.md`, `Open_Issues.csv` and `External_Dependencies.csv`
   differ from GROUP3 canonical. The differences are standing and receiving-currency updates from `ddd721a90` and carry
   no change to scope, structure or mapping. They are the reason reuse of the GROUP3 audit was inadmissible, and this
   baseline records their current hashes.
5. **Scope note.** O-20 scopes the baseline to PKG-02, 03, 04, 05, 08 and 09. Action A41 modifies DEL-01-01, which is in
   PKG-01, so this run adds PKG-01 (Decision_Log D-3). The post-change audit should use the same seven-package scope so
   the comparison is like for like.
6. **Structural facts the amendment relies on.** The IMPACT_ASSESSMENT §4 validation claims hold at `306291bdd`:
   - The 16 amended deliverables and the ledger rows SOW-015, 016, 017, 052, 137, 138, 201 and 202 exist.
   - All eight rows are IN, homed PKG-05 ×5, PKG-02 ×1 and PKG-09 ×2.
   - OBJ-003 and OBJ-005 each have active support: 5 and 10 deliverables.
   - No unit is RETIRED or ISSUED.

## Other derivative-currency observations (Check 9, all variants)

| Issue | Severity | Surface | Observation |
|---|---|---|---|
| COV-119 | INFO | `Coverage_Telemetry.json` | Open-issue counts are stale against the working `Open_Issues.csv` (see finding 3) |
| COV-120 | INFO | `Coverage_Telemetry.json` | Candidate-era standing and "no folders or SoWs" check |
| COV-121 | WARNING | `SOFTWARE_DECOMP.md` | Stale "no folders or SoWs" sentence (see finding 2) |
| COV-122 | INFO | `_Decomposition/_LATEST.md` | Reads `Latest: (none)`. The accepted basis resolves through `checkpoint_snapshots/_LATEST_ACCEPTED.md` |
| COV-123 to 125 | INFO | three working files | Differ from GROUP3 canonical (later standing updates) |
| COV-126 | INFO | `Objectives.csv` | All 10 Notes keep the frozen label "final Group3 acceptance remains pending" |

The main-document package summary table ("Accepted flat work domains") agrees with the registers on all 11 rows:
deliverable counts and IN/OUT/TBD counts.

## Informational items

- **Check 4 (COV-001).** The DEL-01-05 folder label substitutes `-` for `/` in the name. This is a filesystem constraint;
  the ID matches.
- **Check 5 (COV-002 to COV-031).** Each scoped `_CONTEXT.md` repeats `- **PackageID:**` under the Identity heading, with
  identical values. The same pattern holds for all 41 units.
- **Check 6 (87 rows).** Anticipated artifacts are not yet present. This is expected at INITIALIZED, and product
  implementation has not begun.
- **COV-128.** `audit_structure.py` reports the workspace tool roots `_Aggregation`, `_Estimates` and `_Reconciliation`
  as absent. This is outside the 12 checks.

## What to fix for a cleaner rerun (not in this TASK's authority)

- Resolve the Change Register binding for A30, either by a recorded explicit binding or by a heading that binds (COV-127).
- Correct the stale sentence in `SOFTWARE_DECOMP.md` as part of the A30 edit (COV-121).
- Recompute `Coverage_Telemetry.json` at the post-change baseline, as IMPACT_ASSESSMENT §8 already plans (COV-119/120).
- Optionally, update `_Decomposition/_LATEST.md` or document that `checkpoint_snapshots/_LATEST_ACCEPTED.md` is the
  pointer of record (COV-122).
