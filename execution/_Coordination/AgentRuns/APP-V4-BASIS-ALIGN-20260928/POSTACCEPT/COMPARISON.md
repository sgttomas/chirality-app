# Pre/post comparison — SCA-V4-001 after acceptance (node AK2)

This file compares `POSTACCEPT/coverage_summary.json` and its issue log with:
- `POSTCHANGE/coverage_summary.json` (sha256 `4b6d9622…9ca7`), the audited
  candidate the owner accepted;
- `BASELINE/coverage_summary.json` (sha256 `d8ac5c4d…20f9`), the pre-change
  state.

All three runs use the same seven packages and the same `inventory.json`
(`e9088c41…`). The check script is the same except for two documented
additions in POSTACCEPT (see `QA_Report.md`).

A control run of the POSTACCEPT script on an extract of `230bf1e64` gives an
issue log and matrix byte-identical to POSTCHANGE's (sha256 `ed5b8e76…2893`
and `32ec176d…c500`). So the additions change nothing when the Change
Register is unbound and `_LATEST.md` is absent.

## 1. Headline

| Measure | BASELINE | POSTCHANGE | POSTACCEPT |
|---|---|---|---|
| BLOCKER / WARNING / INFO / EXPECTED_CONSEQUENCE | 0 / 2 / 126 / 0 | 0 / 38 / 94 / 0 | 0 / 38 / 94 / 0 |
| Total findings | 128 | 132 | 132 |
| `overall_status` / `closure_readiness` | WARNINGS / WARN | WARNINGS / WARN | WARNINGS / WARN |
| Change Register (scope-change, SOFTWARE) binding | unbound | unbound | **"Decision Log", rank exact** |
| `active_snapshot_status` / `handoff_state_status` (Check 10) | SKIPPED / SKIPPED | SKIPPED / SKIPPED | **PASS / PASS** |
| Lifecycle (scoped) | INITIALIZED 30 | INITIALIZED 16, IN_PROGRESS 14 | INITIALIZED 16, IN_PROGRESS 14 |
| `extensions.working_vs_group3_differences` | 3 files | 8 files | 8 files |

These are unchanged from POSTCHANGE:
- the issue IDs;
- partitions 7/7 and production units 30/30;
- reverse coverage, context fidelity and objective coverage at 100 %;
- artifact presence at 11.22 % (11/98);
- `package_shape_conformance` WARN and `objective_evidence_integrity` PASS;
- `repository_topology` 11 / 41 / 10 / 262 / 262;
- the 30 scoped `ScopeOfWork.md` hashes and frontmatter;
- `open_issue_status_counts`;
- the 30 context matches (all MATCH);
- `Decomp_Coverage_Matrix.csv`, byte for byte.

## 2. Every difference from POSTCHANGE and its cause

| # | POSTCHANGE | POSTACCEPT | Cause |
|---|---|---|---|
| P1 | COV-131 (Check 9b) WARNING. No heading hit for "Ledger, Objectives, Partitions, Production Units, **Change Register (scope-change, SOFTWARE)**"; the Change Register is "UNRESOLVED" | COV-131 WARNING. No heading hit for "Ledger, Objectives, Partitions, Production Units"; the Change Register "binds: 'Decision Log' at rank exact to '## Decision Log'" | H-3 (D-15) added `## Decision Log`. **The Change Register part of COV-131 is closed.** The finding remains a WARNING for the four pre-existing heading bindings, which the registers resolve through `Companion_Inventory.csv` (BASELINE COV-127; IMPACT_ASSESSMENT §9 "pre-existing"). This matches `POSTCHANGE/projections.json`. The clause "binds: …" comes from POSTACCEPT addition (a) |
| P2 | COV-122 INFO: `Consolidated_Coverage.csv` `a988f5a6…` differs from GROUP3 | COV-122 INFO: now `4eee4bcb…` | H-4, the second B8 recompute |
| P3 | COV-127 INFO: `SOFTWARE_DECOMP.md` `98e8bc4b…` differs from GROUP3 | COV-127 INFO: now `74340581…` | H-3 (D-15) |
| P4 | `section_binding` for the Change Register: `Decision Log` rank null | `Decision Log` rank exact, hit "Decision Log" | H-3 |
| P5 | `active_snapshot_status` SKIPPED; `handoff_state_status` SKIPPED | PASS; PASS. `extensions.active_snapshot_check`: `_LATEST.md` names exactly one snapshot, `SCA-V4-001_2026-09-28_2155/`. All 13 required artifacts are present. The eight state fields are admissible and consistent across `Handoff_State.md` and `RUN_SUMMARY.md`. The verdict is `OPEN_PENDING_DERIVATIVE_CLOSURE` with stale derivatives recorded, and there is no other `SCA-*` folder | `_LATEST.md` now exists (method "After acceptance"). Check 10 runs by POSTACCEPT addition (b). A negative test in scratch, on the `230bf1e64` extract with the same `_LATEST.md`, raised 10 BLOCKERs because the snapshot had no `Handoff_State.md` or `RUN_SUMMARY.md` at that commit |
| P6 | run label, timestamp, revision, handoff phase | new values | Run metadata |

The basis documents changed by H-1 and H-2 (PRD, ARCHITECTURE,
HOST_INTEGRATION, EXAMINATION) are not audit-decomp inputs apart from the
Consolidated_Coverage recompute. So they produce no finding difference.

**Still open, as expected:**
- COV-119 and COV-120 (INFO, `Coverage_Telemetry.json`). They are recorded
  as `STALE_REBUILD_REQUIRED`, owned by the decomposition owner, per
  DECISION-8 answer 2 ("Record as stale, fix later (Recommended)"). The file
  is not written under SCA-V4-001.
- The 37 Check-6 lifecycle WARNINGs (DECISION-6; not caused by this
  amendment).

## 3. Relation to BASELINE

BASELINE → POSTACCEPT is the sum of three sets of differences:
- POSTCHANGE `COMPARISON.md` D1–D9;
- P1–P6 above;
- the remaining differences, D10 and D11.

Those two differences resolve as follows:
- **D10, the Change Register part of BASELINE COV-127, is now closed (P1).**
- D11 (COV-119/120) stays open, as recorded above.

Overall, BASELINE COV-121 closed (D-16), the Change Register binding closed
(D-15), and no finding was added apart from the five Check-9 INFOs of the
edited registers (D6).

## 4. Classification (post-acceptance)

| Finding(s) | Severity | Classification | Basis |
|---|---|---|---|
| 37 Check-6 WARNINGs | WARNING | Not an SCA-V4-001 effect (DECISION-6 lifecycle; the artifacts are not yet produced) | POSTCHANGE control run |
| COV-131 (Check 9b) | WARNING | Pre-existing: Ledger, Objectives, Partitions and Production Units bind through `Companion_Inventory.csv`, not by heading. The Change Register part is closed | BASELINE COV-127; IMPACT_ASSESSMENT §9 |
| COV-119, COV-120 | INFO | Pre-existing; `STALE_REBUILD_REQUIRED` (DECISION-8) | — |
| COV-122, 123, 126, 128, 129 and COV-125, 127 | INFO | Intended consequence of the accepted edits (H-3 and H-4 now included) | Register rows 18–31 |
| Check 10 | — | PASS | P5 |

- `AuditState` (raw): **WARNINGS** (0 BLOCKER, 38 WARNING).
- `AdjustedAuditState`: **WARNINGS**. No finding is now classified
  `EXPECTED_CONSEQUENCE`: the one that was, the Change Register part of
  COV-131, is closed.
- There is no new orphan, parentless deliverable or ledger row, and no ID,
  mapping, count or objective change. There is no BLOCKER.
