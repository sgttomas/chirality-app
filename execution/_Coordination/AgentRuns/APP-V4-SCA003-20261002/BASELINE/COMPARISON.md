# SCA-V4-003 pre-change baseline vs SCA-V4-002 post-acceptance audit

**Runs.** This run, `APP_V4_SCA_V4_003_PRECHANGE` (2026-10-03T02:46:41Z, subject `897a107cc`), against
`APP_V4_SCA_V4_002_POSTACCEPT` (2026-09-30T02:17:43Z, subject `851ec3d88` plus the uncommitted group-3 application,
committed as `af918ee50`). Same scope: PKG-01, 02, 03, 04, 05, 09, 10 (32 deliverables). Same tools:
`audit_structure.py` and the audit-decomp and scope-change method files are byte-identical (QA_Report).
`inventory.json` is byte-identical.

**Result.** 0 / 35 / 93 here against 0 / 38 / 100 there. Every difference is attributed below to one of three
causes: SCA-V4-002's completed propagation (B-06a), Design files added by design passes 2 and 3, or this run's
documented script changes (h) and (i). No new finding appears.

**Control.** POSTACCEPT's own script, run on a `git archive` of `af918ee50`, reproduces POSTACCEPT's IssueLog and
Matrix byte for byte. Run on the current state, it gives 0 / 35 / 94 and the same Matrix as this run. So the state
change accounts for −3 WARNING and −6 INFO, and change (h) for the one further INFO.

## 1. Input differences (INPUT_MANIFEST.sha256)

185 files are hashed by both runs; **21 changed**. POSTACCEPT also hashed the SCA-V4-002 IMPACT_ASSESSMENT and
BASIS_AMENDMENT, which this run's script does not read. This run adds 30 files: GROUP3's 16 canonical files (read by
Check 9), the SCA-V4-002 post-acceptance checks and effective-state record (2), the DAG pointer and DAG-003's two
manifests (3), the seven SCA-V4-003 proposal records (pass-2 C1-A/B/C and CLOSEOUT_ACCOUNT, pass-3 C1-A/B and
F0_JOINS) and this run's BRIEFS and OWNER_DECISIONS (2).

| Changed files | Cause | Commit |
|---|---|---|
| `ScopeOfWork.md` of DEL-01-01, 01-04, 02-01, 02-02, 02-03, 03-03, 04-02, 09-07, 10-03 | SCA-V4-002 propagation stage 1 (REVISE + VERIFY, NO_STATUS_TOUCH) | `1efd4bcda` |
| `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (`d5d873b3…` → `6ef9c0ba…`) | B-06a reading-rule note | `1efd4bcda` |
| `Dependencies.csv` of the nine above plus DEL-04-01 and DEL-04-03 | `dependency-extract` UPDATE (four arc rows, re-quoting, DEP-09-07-016) | `8cd783d8d` |

All 21 equal DAG-003's `SOURCE_MANIFEST.sha256`. No `_CONTEXT.md`, `_STATUS.md`, other `_Decomposition` file, basis
document or `_ScopeChange` file changed.

Not hashed but read by Check 6 (file names only): design passes 2 and 3 added Design documents, schemas, examples
and prototypes in the scoped deliverables (`extensions.artifact_matches`).

## 2. Issue-log differences (138 → 128 rows)

Matched on (check, severity, entity type, entity ID, description). 123 rows match exactly; 82 of them are
renumbered because rows earlier in the log were removed.

| POSTACCEPT issue | Change | Attribution |
|---|---|---|
| COV-042 (DEL-01-03 CODE plan/revision and tool/delegation views), INFO | removed | Matched by `Design/NATIVE_PLANS_TOOLS_DELEGATION.md`, `npt.plan-revision.schema.json` and fixtures (design pass 3) |
| COV-049, COV-051 (DEL-01-05 CODE sign-in/provider selection; DOC account-home/API-key decisions), INFO | removed | `Design/ACCOUNT_AND_PROVIDER_ACCESS.md`, `Design/ACCOUNT_HOME_DECISION_RECORD.md` (pass 3) |
| COV-060 (DEL-02-02 CODE draft review/registration workspace), INFO | removed | `Design/WORKSPACE_AND_REGISTRATION.md` and `workspace-registration.*` (pass 3) |
| COV-064 (DEL-02-03 CODE required-tool and checkpoint receiving), **WARNING** | removed | `Design/prototype/required_tool_check.py` (pass 2) |
| COV-067, COV-068 (DEL-02-04 CODE role selection and supply; DOC guidance identity and enforcement-limit account), INFO | removed | `Design/ROLE_SUPPLY.md`, `prototype/role_supply.py`, `role-supply-record.*`, `role-limit-account.*` (pass 3) |
| COV-083 (DEL-04-03 DOC record authority and host receipt links), **WARNING** | removed | `Design/RS_RECORD.valid.host-destinations.example.jsonl`, `RS_RECORD.valid.host-run.example.jsonl` (pass 2) |
| COV-084 (DEL-05-01 CONFIG tool-call/model interface fixtures), **WARNING** | removed | `Design/LOOP_TOOL_CALL.schema.json` and its examples (pass 2) |
| COV-127 (Check 9 INFO, `_Decomposition/_LATEST.md`, ASC-ISS-006) | removed | B-06a applied (`1efd4bcda`); change (h). POSTACCEPT's COMPARISON had said it "closes only with B-06a" |
| COV-128, 129, 131, 133 → COV-118, 119, 121, 123 (Check 9 INFO) | wording | change (i): each now also names the SCA-V4-002 `AffectedFiles` row; hashes unchanged |
| COV-130 → COV-120 (Check 9 INFO, `External_Dependencies.csv`) | wording | change (i): "not named in SCA-V4-001 or SCA-V4-002" |

The Check 6 removals are heuristic matches of Design-stage files; none is a product artifact (Decision_Log D-6).
The 35 WARNINGs are POSTACCEPT's 38 minus COV-064, 083 and 084: 34 Check 6 absences at IN_PROGRESS and the
heading-binding WARNING (now COV-127).

## 3. Matrix differences (32 rows)

Seven rows differ, in `ArtifactCoverage` and `IssueCount` only: DEL-01-03 0/3 → 1/3; DEL-01-05 0/4 → 2/4; DEL-02-02
0/4 → 1/4; DEL-02-03 0/3 → 1/3; DEL-02-04 0/3 → 2/3; DEL-04-03 0/4 → 1/4; DEL-05-01 1/4 → 2/4. Context match,
objective mapping and lifecycle are unchanged in all 32 rows.

## 4. Summary-field differences (coverage_summary.json)

| Field | POSTACCEPT | This run | Cause |
|---|---|---|---|
| `issues_warning` / `issues_info` | 38 / 100 | 35 / 93 | §2 |
| `artifact_presence_pct` | 10.78 (11/102) | 19.61 (20/102) | Design files (§2) |
| `extensions.expected_source.parity_basis` | SCA-V4-001 PAV `applied_hashes` + SCA-V4-001 GROUP-3 rows | SCA-V4-002 PAV `applied_hashes` + SCA-V4-002 GROUP-3 rows + DAG-003 `SOURCE_MANIFEST` | change (j) |
| `extensions.expected_source.files_equal` | 12 of 22 | 148 of 148 | change (j); the subject equals the accepted poststate |
| `extensions.scope_check` | derived from the SCA-V4-002 register | derived from the SCA-V4-003 proposal records; covers PKG-01…05, 09; PKG-10 beyond | change (e2) |
| `extensions.decomposition_pointers`, `extensions.artifact_matches` | absent | present | changes (h), (k) |
| `run_label`, `timestamp`, `expected_handoff_phase`, `decomposition_revision` | POSTACCEPT values | this run's values | run identity |

Unchanged: topology 11 / 41 / 10 / 262; forward, reverse, context and objective coverage 100 %; Check 10 PASS /
PASS with the same active snapshot, state fields, verdict and resolved registered parser; lifecycle 18 / 14 scoped,
27 / 14 repository-wide; `working_vs_group3_differences` (8 files, same hashes); open-issue counts.
