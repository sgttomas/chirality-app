# Post-change audit vs pre-change baseline — SCA-V4-003 candidate

**Run.** `APP_V4_SCA_V4_003_POSTCHANGE`, 2026-10-04T00:31:55Z, by node AK1
(stage 2; Type 2 TASK, Claude Code subagent; no delegation) of run
`APP-V4-SCA003-20261002`. Read-only `audit-decomp` over the baseline's scope:
**PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables). Subject: the working
tree at `ec267bdb9f` (both decision snapshots committed) plus the uncommitted
SCA-V4-003 candidate application: `_Decomposition/Open_Issues.csv` (B-02
option B, B-03), the candidate folder `_ScopeChange/SCA-V4-003_2026-10-03_1827/`
as it stood at the audit (9 files; see §1), and the SCA-V4-002
effective-state note. Writes: this folder only.

**Method and tools.**
- `audit_checks.py` is **byte-identical** to `BASELINE/audit_checks.py`
  (sha256 `8c3bef06…b0d3`); no check, rule, severity, wording or order changed.
- `inventory.json` is a byte copy of the baseline's (`e9088c41…9014`), as in
  the SCA-V4-002 POSTCHANGE run (the tool reads it as input).
- `tools/evaluation/audit_structure.py` (`d37ffbd0…ecdb3f`, unchanged) was run
  the same way: `COMPLETE`, 41/41 PASS. `structure.json` differs from the
  baseline's only in the six lifecycle values of the Q-13 act (INITIALIZED 27
  → 21, IN_PROGRESS 14 → 20) and the recorded inventory path.
- Command: `RUN_LABEL=APP_V4_SCA_V4_003_POSTCHANGE HANDOFF_PHASE=… RUN_TS=2026-10-04T00:31:55Z BASIS_COMMIT=ec267bdb9f… python3 audit_checks.py <repo> <POSTCHANGE> PKG-01,PKG-02,PKG-03,PKG-04,PKG-05,PKG-09,PKG-10`; exit 0.

**Result.** 0 BLOCKER, **52 WARNING**, **77 INFO**, 0 EXPECTED_CONSEQUENCE
(the script does not classify). Baseline: 0 / 35 / 93 / 0. `overall_status`
WARNINGS; `closure_readiness` WARN. Coverage unchanged: forward 100 %
(packages and deliverables), reverse 100 %, context fidelity 100 %,
objective coverage 100 %, artifact presence 19.61 %. Topology unchanged:
11 / 41 / 10 / 262. Check 10 `active_snapshot_status` PASS,
`handoff_state_status` PASS; the active snapshot is still SCA-V4-002.

## 1. Input differences

`shasum -a 256 -c BASELINE/INPUT_MANIFEST.sha256` at the subject: 206 of 215
OK, 9 differ.

| File | Baseline | Post-change | Attribution |
|---|---|---|---|
| `_Decomposition/Open_Issues.csv` | `a1178218…80f0` | `9c2d916c…515d` | SCA-V4-003 register rows 21, 22 (B-02 option B, B-03); the packet's stated result hash |
| Six `_STATUS.md` (DEL-01-02, 01-03, 01-04, 01-05, 02-02, 02-04) | INITIALIZED | IN_PROGRESS | The Q-13 act (DECISION-1 Q-13, a separate owner act outside the amendment), commit `baa6e618d7` |
| `RUN/BRIEFS.md`, `RUN/OWNER_DECISIONS.md` | — | — | Run records appended after the baseline (DECISION-1 at `5b16bb6831`; the AK1 brief at `7fea17baaf`); read by the script only for its scope derivation, which is unchanged (`extensions.scope_check` equal) |

`POSTCHANGE/INPUT_MANIFEST.sha256` (234 entries) is the baseline's 215 paths
rehashed at the subject, plus the 19 SCA-V4-003 files that existed at the
audit: the two `_AUTHORIZED.md` pointers, the 7 decision-snapshot files, the
9 candidate files (Amendment_Actions.csv, Amendment_Preview.md, Brief.md,
Impact_Assessment.md, Intake_Actions.csv, Pre_Change_Coverage.json,
Propagation_Plan.md, Supersession_Delta.csv, Supersession_Map.csv) and the
C-02 note. All pass at the time of writing.

**Not an input and no effect: DEL-03-04 `Design/HOST_INTEGRATION_GUIDE.md`**,
changed at `a68a9e06e2` (pass-3 closeout, after the baseline). Design file
contents are not hashed (BASELINE D-7); Check 6 matches file names, and the
file name is unchanged. `extensions.artifact_matches` is identical in both
runs, so the GUIDE change moves no finding.

Unchanged and held: every `ScopeOfWork.md`, `Dependencies.csv` and
`_DEPENDENCIES.md`; `SOFTWARE_DECOMP.md` (B-01 held); `_ScopeChange/_LATEST.md`
(C-01 held); `Coverage_Telemetry.json`; the DAG-003 source manifest
(130/130 OK, `RUN/Application/DAG_CURRENCY.txt`).

## 2. Issue-log differences (`Decomp_Coverage_IssueLog.csv`)

Baseline 128 issues, post-change 129. Issue IDs COV-001…COV-128 keep their
positions and entities (checked by script); every difference is listed.

| Post-change ID | Baseline | Check | Severity | What differs | Attribution |
|---|---|---|---|---|---|
| COV-038…COV-049 (12), COV-057, COV-058, COV-059, COV-062 | same IDs, INFO | 6 | INFO → **WARNING** | The 16 anticipated-artifact absences of DEL-01-02 (4), 01-03 (2), 01-04 (4), 01-05 (2), 02-02 (3) and 02-04 (1) now read "lifecycle IN_PROGRESS" and are graded WARNING | **The Q-13 act**, not the amendment. The audit grades absences WARNING at IN_PROGRESS and INFO at INITIALIZED (BASELINE D-8). Predicted by the baseline (R22-5: 16 INFO → WARNING, 35 → 51) and by OWNER_ITEMS Q-13. The findings themselves are pre-existing (same entities and artifacts) |
| COV-116 | COV-116 | 9 | INFO | Working `Open_Issues.csv` now has 22 OPEN and lists `OI-009: RESOLVED_BY_OWNER_DECISION` among the non-OPEN rows; the stale telemetry still says 24 | **B-02 option B** (register row 21; Q-10). The telemetry stays `STALE_REBUILD_REQUIRED`, carried from SCA-V4-001; its difference widens by one, as IMPACT_ASSESSMENT §5 and BASIS_AMENDMENT B-02 state |
| COV-121 | COV-121 | 9 | INFO | Working `Open_Issues.csv` hash `a1178218…` → `9c2d916c…` against frozen GROUP3 | **B-02 and B-03** (rows 21, 22). The unchanged script still attributes the file to the SCA-V4-001 and SCA-V4-002 registers only, because it reads accepted amendments; SCA-V4-003's register also names it. Wording limit of the script, not a defect |
| **COV-129** | — | 10 | **WARNING** | **New.** "Historical snapshot residue is incomplete but not active truth" for `_ScopeChange/SCA-V4-003_2026-10-03_1827`. The script treats every `SCA-*` folder other than the active one as historical residue and checks it for 13 required artifacts | **The candidate folder, not an applied edit.** At the audit it lacked `Post_Change_Coverage.json` (this run's output), `Decision_Log.md`, `Handoff_State.md` and `RUN_SUMMARY.md`, which follow this audit. Recommended classification: `EXPECTED_CONSEQUENCE` of the accepted sequence (group-2 `Handoff_State.md` step 5; IMPACT_ASSESSMENT §10 step 3; DECISION-1), as SCA-V4-002's COV-139 was. The label "historical" is a wording limit of the unchanged script |

No other issue differs in any field. No Check 5 finding changed (MATCH
32/32); no new orphan, unmapped, or parentless row; Checks 7, 8 and 9b are
unchanged.

## 3. Matrix and summary differences

- `Decomp_Coverage_Matrix.csv`: only the lifecycle column of the six Q-13
  deliverables (INITIALIZED → IN_PROGRESS). Every coverage cell is unchanged.
- `coverage_summary.json`: `issues_warning` 35 → 52, `issues_info` 93 → 77,
  `lifecycle_distribution` 18/14 → 12/20 (scoped); the run label, timestamp,
  handoff phase and revision. Extensions:
  - `open_issue_status_counts`: OPEN 23 → 22, `RESOLVED_BY_OWNER_DECISION` 1 (B-02);
  - `working_vs_group3_differences`: the `Open_Issues.csv` hash (B-02, B-03);
  - `expected_source`: 147 of 148 files equal SCA-V4-002's accepted poststate;
    the one difference is `Open_Issues.csv` (B-02, B-03);
  - `active_snapshot_check`: `SCA-V4-003_2026-10-03_1827` listed among other
    SCA folders and as incomplete residue (COV-129);
  - `whole_decomposition.lifecycle_distribution`: 27/14 → 21/20 (Q-13).
  - Every other extension, including `artifact_matches`, `scope_check` and
    `decomposition_pointers`, is identical.

## 4. Classification and audit states

| Group | Count | Classification |
|---|---:|---|
| Pre-existing WARNINGs carried | 35 | pre-existing (34 Check 6 lifecycle, 1 Check 9b) |
| Check 6 WARNINGs re-graded by the Q-13 act | 16 | pre-existing absences; attributed to the separate owner act, not to the amendment; not new defects |
| COV-129 | 1 | `EXPECTED_CONSEQUENCE` (recommended) |
| COV-116, COV-121 (INFO) | 2 | intended effects of B-02/B-03, attributed |

- `AuditState`: `WARNINGS` (52 WARNING, 0 BLOCKER).
- `AdjustedAuditState`: `WARNINGS` (51 WARNING excluding COV-129).
- No new finding stems from an applied SCA-V4-003 edit. The intended changes
  occurred: OI-009 resolved, OI-018 pointer present, OPEN 22, and nothing
  else in the decomposition package changed.
