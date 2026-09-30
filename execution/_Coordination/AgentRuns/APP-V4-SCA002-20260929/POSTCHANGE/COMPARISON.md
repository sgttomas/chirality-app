# Post-change audit vs pre-change baseline — SCA-V4-002 candidate

**Run.** `APP_V4_SCA_V4_002_POSTCHANGE`, 2026-09-30T01:10:07Z, by node AK1
(Type 2 TASK, Claude Code subagent; no delegation) of run
`APP-V4-SCA002-20260929`. Read-only `audit-decomp` over the same scope as
the baseline: **PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables). Subject:
the working tree at `39c97257b` plus the uncommitted SCA-V4-002 candidate
application (the 10 files listed in §1). Writes: this folder only.

**Method and tools.** `audit_checks.py` here is **byte-identical** to
`BASELINE/audit_checks.py` (sha256 `ea6c2be7…d30b`): no check, rule,
severity, wording or ordering changed. `inventory.json` is byte-identical to
the baseline's. `tools/evaluation/audit_structure.py` was run the same way
(41/41 PASS, all `SOW_V1`; INITIALIZED 27, IN_PROGRESS 14; `structure.json`
differs from the baseline's only in its recorded inventory path and
timestamp).

**Result.** 0 BLOCKER, **39 WARNING** (38 + 1), 101 INFO, 0
EXPECTED_CONSEQUENCE. `overall_status` WARNINGS; `closure_readiness` WARN.
Coverage figures are unchanged: forward 100 % (packages and deliverables),
reverse 100 %, **context fidelity 100 %**, objective coverage 100 %,
artifact presence 10.78 %. Topology unchanged: 11 / 41 / 10 / 262. Open
issues unchanged: 23 OPEN. `Decomp_Coverage_Matrix.csv` is **byte-identical**
to the baseline's.

## 1. Input differences (INPUT_MANIFEST.sha256, 170 files)

Ten files differ from the baseline manifest. Every one is a target of the
accepted SCA-V4-002 register, applied in the candidate:

| File | Baseline | Post-change | Register row / edit |
|---|---|---|---|
| `docs/HOST_INTEGRATION.md` | `6c6854f9…` | `d4331c39…` | 10 / A-01 (the packet's stated result hash) |
| `_Decomposition/Consolidated_Coverage.csv` | `4eee4bcb…` | `36677365…` | 11 / B-01 (31 rows) |
| `_Decomposition/Open_Issues.csv` | `f6b92362…` | `a1178218…` | 12 / B-02 |
| `_Decomposition/Deliverables.csv` | `2480cbef…` | `552df060…` | 14 / B-05a |
| DEL-04-01 `_CONTEXT.md` | `3f981bd6…` | `2a01a70b…` | 14, 16 / B-05b, B-06c |
| `_Decomposition/_LATEST.md` | `8eb05194…` | `b1b8410b…` | 15 / B-06b |
| DEL-02-03 `_CONTEXT.md` | `d8cfefa0…` | `41d4a224…` | 16 / B-06c |
| DEL-05-01 `_CONTEXT.md` | `58f0bc84…` | `8977ff6b…` | 16 / B-06c |
| DEL-05-02 `_CONTEXT.md` | `e889d2b7…` | `32012929…` | 16 / B-06c |
| DEL-09-07 `_CONTEXT.md` | `8f7927ff…` | `3c424e4e…` | 16 / B-06c |

The other 160 audited files are unchanged, including `SOFTWARE_DECOMP.md`
(B-04 held), `checkpoint_snapshots/_LATEST_ACCEPTED.md` (B-06a held),
`_ScopeChange/_LATEST.md` (C-01 held), every `ScopeOfWork.md`,
`Dependencies.csv` and `_STATUS.md`, and `Coverage_Telemetry.json`.

## 2. Issue-log differences (`Decomp_Coverage_IssueLog.csv`)

Baseline: 139 issues. Post-change: 140. Every difference is listed.

| Post-change ID | Baseline ID | Check | Severity | What differs | Attribution |
|---|---|---|---|---|---|
| COV-127 | COV-127 | 9 | INFO | The quoted `_Decomposition/_LATEST.md` text now includes the B-06b reading-rule sentence. The rest of the description (that `_LATEST_ACCEPTED.md` names GROUP3 alone) is still true, because B-06a is held for the SoW REVISE stage | Direct effect of B-06b (row 15). The `_LATEST_ACCEPTED.md` half closes when B-06a is applied after group 3 |
| COV-128 | COV-128 | 9 | INFO | Working `Consolidated_Coverage.csv` hash `4eee4bcb…` → `36677365…` against the frozen GROUP3 | B-01 (row 11). The row is still attributed to SCA-V4-001's `AffectedFiles`, as the script derives it; SCA-V4-002 also names the file |
| COV-129 | COV-129 | 9 | INFO | Working `Deliverables.csv` hash `2480cbef…` → `552df060…` | B-05a (row 14); same note |
| COV-131 | COV-131 | 9 | INFO | Working `Open_Issues.csv` hash `f6b92362…` → `a1178218…` | B-02 (row 12); same note |
| **COV-139** | — | 10 | **WARNING** | **New.** "Historical snapshot residue is incomplete but not active truth" for `_ScopeChange/SCA-V4-002_2026-09-29_1901`. The script treats every `SCA-*` folder other than the active one as historical residue and checks it for the 13 required artifacts | **Caused by the candidate folder, not by an applied edit.** The folder is SCA-V4-002's in-preparation candidate (posture `ACCEPTED_PREDECESSOR`; `SCA-V4-002_GROUP-2_AUTHORIZED.md`), not historical residue. At the audit it lacked `Post_Change_Coverage.json`, `Decision_Log.md`, `Handoff_State.md` and `RUN_SUMMARY.md`. The first two were written after this run (this audit's `coverage_summary.json` is the copy). `Handoff_State.md` and `RUN_SUMMARY.md` are written at the end of group-3 preparation, after the independent review (method step 5–7; IMPACT_ASSESSMENT §7 step 3). The finding closes then. Recommended classification for the group-3 package: `EXPECTED_CONSEQUENCE` of the accepted sequencing (IMPACT_ASSESSMENT §7, accepted at group 2), not a defect; the script's label "historical residue" is a wording limit of the unchanged script. The classification is for the group-3 preparer and reviewer, not fixed here |
| COV-140 | COV-139 | 10 | INFO | Same finding, renumbered by one: the registered pointer parser returns `None` for `_ScopeChange/_LATEST.md` (V13 F2) | Pre-existing, carried. It closes at C-01 (group 3), as the baseline predicted |

Every other issue (COV-001…COV-126, COV-130, COV-132…COV-138) is
byte-identical to the baseline. In particular:
- **Check 5 (context fidelity):** no new finding. DEL-04-01's `_CONTEXT.md`
  `- **Description:**` bullet changed byte-consistently with
  `Deliverables.csv` (B-05a/b), as baseline finding 3 required; Check 5 is
  MATCH for all 32 scoped deliverables. The B-06c sentences sit on the
  non-bullet `Accepted basis:` line and add no compared field.
- **Check 6:** the 37 lifecycle WARNINGs and the artifact-presence INFOs are
  unchanged (DECISION-6; not this amendment).
- **Check 9:** COV-125/126 (`Coverage_Telemetry.json` stale; ASC-ISS-004)
  and COV-130, COV-132…COV-136 are unchanged. The telemetry finding gains no
  new delta from this amendment: the OPEN count stays 23 (Q-5 option A).
- **Check 9b (COV-137):** the heading bindings are unchanged; the Change
  Register still binds at rank exact to `## Decision Log`.
- **Check 10 (active snapshot):** `active_snapshot_status` PASS,
  `handoff_state_status` PASS. The active snapshot is still
  `SCA-V4-001_2026-09-28_2155`, as the posture requires.
- **Check 11 (COV-138):** unchanged.

## 3. `coverage_summary.json` differences

| Field | Baseline | Post-change | Attribution |
|---|---|---|---|
| `run_label`, `timestamp`, `expected_handoff_phase`, `decomposition_revision` | baseline values | this run's values | run identity |
| `issues_warning` | 38 | 39 | COV-139 (§2) |
| `extensions.expected_source.files_equal` | 22 of 22 | **14 of 22** | The eight unequal files are exactly the SCA-V4-002 targets that the parity set covers: `HOST_INTEGRATION.md`, `Consolidated_Coverage.csv`, `Deliverables.csv`, `Open_Issues.csv`, and the `_CONTEXT.md` of DEL-02-03, DEL-05-01, DEL-05-02 and DEL-09-07. The parity basis is the SCA-V4-001 accepted poststate; the candidate is meant to differ from it in these files. (DEL-04-01 `_CONTEXT.md` and `_Decomposition/_LATEST.md` are not in the parity set.) |
| `extensions.working_vs_group3_differences` | seven files | the same seven files; three hashes changed | `Consolidated_Coverage.csv`, `Deliverables.csv`, `Open_Issues.csv` (§1). No file newly differs from GROUP3 |
| `extensions.active_snapshot_check.other_sca_folders`, `.incomplete_residue` | `[]`, `[]` | `["SCA-V4-002_2026-09-29_1901"]` both | The candidate folder (§2, COV-139) |

Every other field, including `scope_check` (the seven packages equal the
register's packages), `registered_pointer_parser` (`None`, unchanged),
`section_binding`, `objective_rows` and `sow_frontmatter`, is identical.

## 4. What the comparison establishes

- The intended candidate edits occurred, and only they: the ten changed
  inputs are the register's candidate-stage targets (rows 10, 11, 12, 14, 15
  in part, 16). The held edits (B-04, B-06a, C-01) left their targets
  unchanged.
- No coverage regression: every coverage figure is unchanged; no orphan, no
  parentless deliverable or ledger row; topology unchanged.
- No new Check 5 finding: the DEL-04-01 mirror is exact.
- The one new WARNING is the candidate folder's own incompleteness during
  preparation, not an applied-edit defect (§2).
- Raw `AuditState`: `WARNINGS`. `AdjustedAuditState` if COV-139 is
  classified `EXPECTED_CONSEQUENCE` by the group-3 preparer: `WARNINGS`
  (the 38 pre-existing WARNINGs remain). The classification table for the
  group-3 package is §2.
