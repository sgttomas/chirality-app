# Post-acceptance audit vs post-change audit — SCA-V4-002 accepted

**Run.** `APP_V4_SCA_V4_002_POSTACCEPT`, 2026-09-30T02:17:43Z, by node AK2
(Type 2 TASK, Claude Code subagent; no delegation) of run
`APP-V4-SCA002-20260929`. Read-only `audit-decomp` over the same scope as
the baseline and the post-change audit: **PKG-01, 02, 03, 04, 05, 09, 10**
(32 deliverables). Subject: the working tree at `851ec3d88` plus the
uncommitted group-3 application (H-1, H-2, the accepted-snapshot records
and the group-3 decision snapshot; §1). Writes: this folder only.

**Method and tools.** `audit_checks.py` here is `BASELINE/audit_checks.py`
(sha256 `ea6c2be7…d30b`, byte-identical to POSTCHANGE's) with two
documented changes and no check, rule, severity or ordering changed:
- **(f)** the active amendment is resolved from `_ScopeChange/_LATEST.md`
  (the `Latest:` target, cross-checked against the `**Active snapshot:**`
  line) instead of the hard-coded SCA-V4-001 path. It is used in the Check 9
  INFO on `_Decomposition/_LATEST.md`, in the registered-parser comparison
  and in the summary's expected-source fields. SCA-V4-001 stays the
  attribution basis for the working-vs-GROUP3 INFO rows and the parity basis;
- **(g)** Check 10's one-active-snapshot reading ignores the
  `**Accepted predecessor:**` field line of the SPEC §11.2 pointer form
  (BASIS_AMENDMENT C-01). That line names the predecessor as accepted, not
  active; the rule (exactly one active snapshot) is unchanged.

**Disclosure: the unchanged base script.** Run against the same state (to
scratch, not kept), `BASELINE/audit_checks.py` reports 1 BLOCKER, 38 WARNING,
101 INFO: its `names` heuristic reads the predecessor path on the
`**Accepted predecessor:**` line as a second active snapshot ("_LATEST.md
names amendment snapshot folders ['SCA-V4-001_2026-09-28_2155',
'SCA-V4-002_2026-09-29_1901']"), and its registered-parser INFO compares the
parser's target (`SCA-V4-002_2026-09-29_1901`) with the hard-coded SCA-V4-001
folder, so it still fires with the description "the pointer has no
'Latest:' line", which is no longer true. Both are limits of the script
written for the `FIRST_AMENDMENT` posture, not findings against the applied
state: the pointer names exactly one active snapshot (`Latest:` and
`**Active snapshot:**` agree), and the registered parser resolves it. The
accepted C-01 text is not edited. A tool improvement is outside this
amendment.

`inventory.json` is byte-identical to the baseline's and POSTCHANGE's.
`tools/evaluation/audit_structure.py` was run the same way (41/41 PASS, all
`SOW_V1`; INITIALIZED 27, IN_PROGRESS 14; `structure.json` differs only in
its recorded inventory path and timestamp).

**Result.** 0 BLOCKER, **38 WARNING**, **100 INFO**, 0 EXPECTED_CONSEQUENCE
(POSTCHANGE: 0 / 39 / 101 / 0; BASELINE: 0 / 38 / 101 / 0).
`overall_status` WARNINGS; `closure_readiness` WARN. Coverage figures are
unchanged: forward 100 % (packages and deliverables), reverse 100 %, context
fidelity 100 %, objective coverage 100 %, artifact presence 10.78 %.
Topology unchanged: 11 / 41 / 10 / 262. `Decomp_Coverage_Matrix.csv` is
**byte-identical** to POSTCHANGE's and the baseline's. Check 10:
`active_snapshot_status` PASS, `handoff_state_status` PASS, active snapshot
`execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`, no missing artifact, no
incomplete residue (SCA-V4-001's folder is complete); the registered parser
returns `SCA-V4-002_2026-09-29_1901` with `pointer_matches_active` True.

## 1. Input differences (INPUT_MANIFEST.sha256, 187 files)

Of the 170 files POSTCHANGE hashed, **2 changed**; 17 were added to the
manifest (the active snapshot's 13 required artifacts, the group-3 decision
folder's 3 files and `BASIS_AMENDMENT.md`), none of which POSTCHANGE hashed.

| File | POSTCHANGE | POSTACCEPT | Cause |
|---|---|---|---|
| `_Decomposition/SOFTWARE_DECOMP.md` | `7434058164…` | `ea3388bcb0…` | H-1 (B-04, the SCA-V4-002 Decision Log entry) |
| `_ScopeChange/_LATEST.md` | `a9a7cdc8c5…` | `2b7938bc82…` | H-2 (C-01, the pointer move in SPEC §11.2 form) |

All 128 scoped deliverable files (`ScopeOfWork.md`, `Dependencies.csv`,
`_CONTEXT.md`, `_STATUS.md`), the other 16 `_Decomposition` files, the four
basis documents, the three decomposition pointers, the 13 SCA-V4-001
snapshot files, the SCA-V4-001 group-3 folder and `IMPACT_ASSESSMENT.md`
are unchanged.

## 2. Issue-log differences (140 → 138 rows)

Matched on (check, severity, entity type, entity ID, description). No
matched row is renumbered.

| Issue | Change | Attribution |
|---|---|---|
| COV-127 (Check 9 INFO, `_Decomposition/_LATEST.md`) | wording: the active amendment named is now `SCA-V4-002_2026-09-29_1901` (was `SCA-V4-001_2026-09-28_2155`) | script change (f); the pointer move (H-2). The finding itself (ASC-ISS-006; `_LATEST_ACCEPTED.md` still names GROUP3 alone) is carried until B-06a is applied with the REVISEs |
| COV-133 (Check 9 INFO, `SOFTWARE_DECOMP.md`) | working hash `7434058164` → `ea3388bcb0` | H-1. The attribution text still says "named in 1 row(s) of the accepted SCA-V4-001 Amendment_Actions.csv AffectedFiles", which is true; the file is also register row 13 of SCA-V4-002 |
| COV-139 (Check 10 WARNING, `SCA-V4-002_2026-09-29_1901`, "Historical snapshot residue") | **removed** | the candidate folder now holds `Handoff_State.md` and `RUN_SUMMARY.md` and is the active snapshot; the `EXPECTED_CONSEQUENCE` classification at group 3 is closed |
| COV-140 (Check 10 INFO, `_LATEST.md`, registered pointer parser) | **removed** | H-2: the pointer carries `Latest:` and the parser resolves it to the active snapshot (V13 F2 closed) |

The 38 WARNINGs are those of the baseline: 37 lifecycle WARNINGs (Check 6;
DECISION-6) and COV-137 (Check 9b heading bindings for Ledger, Objectives,
Partitions and Production Units; the Change Register part binds "Decision
Log" at rank exact, as since SCA-V4-001).

## 3. Summary-field differences (coverage_summary.json)

| Field | POSTCHANGE | POSTACCEPT | Cause |
|---|---|---|---|
| `issues_warning` / `issues_info` | 39 / 101 | 38 / 100 | COV-139 and COV-140 removed |
| `expected_source_snapshot`, `extensions.expected_source.active_amendment` | SCA-V4-001 | SCA-V4-002 | (f); the pointer move |
| `extensions.expected_source.predecessor_parity_amendment` | absent | SCA-V4-001 | (f) labels the parity basis explicitly |
| `extensions.expected_source.files_equal` | 14 of 22 | 12 of 22 | `SOFTWARE_DECOMP.md` (H-1) and `_ScopeChange/_LATEST.md` (H-2) now differ from the SCA-V4-001 accepted poststate, in addition to the eight SCA-V4-002 register targets applied in the candidate |
| `extensions.registered_pointer_parser` | `target: None`, `pointer_matches_active: False` | `target: SCA-V4-002_2026-09-29_1901`, `pointer_matches_active: True` | H-2 |
| `extensions.active_snapshot_check` | active SCA-V4-001; `other_sca_folders` [SCA-V4-002]; `incomplete_residue` [SCA-V4-002] | active SCA-V4-002; `other_sca_folders` [SCA-V4-001]; `incomplete_residue` [] | H-2; the accepted-snapshot records |
| `extensions.working_vs_group3_differences` | `SOFTWARE_DECOMP.md` at `7434058164…` | `SOFTWARE_DECOMP.md` at `ea3388bcb0…` | H-1 |
| `run_label`, `timestamp`, `expected_handoff_phase`, `decomposition_revision` | POSTCHANGE values | this run's values (`POST_ACCEPTANCE`; `851ec3d88`) | run identity |

Every other summary field is equal.

## 4. Findings that bear on the propagation

- COV-127 closes only with B-06a (`_LATEST_ACCEPTED.md`), timed with the
  SoW REVISEs.
- No finding concerns the nine `ScopeOfWork.md` files; the REVISEs have not
  run at this audit.
