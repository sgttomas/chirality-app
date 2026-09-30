# SCA-V4-002 post-acceptance validation

Owner act: DECISION-3, 2026-09-29 ("Accept (Recommended)"; `checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/`). Accepted basis `851ec3d88` (candidate `70376aff2`, presentation `ffdb56e1a`). Applied state: uncommitted working tree over `851ec3d88`. Record `SCA-V4-002_20260930T021014Z`. Written by `verify_post_acceptance.py`, which recomputes the applied bytes from the accepted basis independently of `apply_group3_edits.py`. The candidate evidence reviewed at group 3 (POSTCHANGE/, V14) is not modified. No `ScopeOfWork.md` is changed under this record: the nine REVISEs and B-06a follow as propagation stage 1.

| Check | Result | Detail |
|---|---|---|
| 1a group-3 DECISION.md first line is the accepted heading (check_amendment_reopen.py form) | PASS | # SCA-V4-002 checkpoint group 3 — accepted audited poststate |
| 1b DECISION-3 label quoted verbatim in DECISION.md and present in the DECISION-3 section of OWNER_DECISIONS.md | PASS | "Accept (Recommended)" |
| 1c OWNER_DECISIONS.md custody hash equals the cited hash and its blob at 851ec3d88 | PASS | f2dda563beaadc737c73d897d6801a78332e5a722334dd8ef6d26c0dd0c38ef3 |
| 1d commit 851ec3d88 changes only OWNER_DECISIONS.md over the presentation commit ffdb56e1a | PASS | projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md |
| 1e group-3 ACCEPTED_MANIFEST.csv binds the presented bytes (every row equals its blob at 851ec3d88) | PASS | 61 rows; mismatches [] |
| 1f group-3 folder holds DECISION.md, ACCEPTED_MANIFEST.csv, Handoff_State.md | PASS | ['ACCEPTED_MANIFEST.csv', 'DECISION.md', 'Handoff_State.md'] |
| 1g the manifest binds the register at the group-2 hash | PASS | 158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d |
| 2a BASIS_AMENDMENT.md is the accepted bytes | PASS | 091871fd90283b27b2d067c1eeb3137e3cf8f9d50dab87ad92a9b871cc634238 |
| 2b the five clause texts equal the B-04 slot table | PASS | ['{Q10_CLAUSE}', '{Q11_CLAUSE}', '{Q12_CLAUSE}', '{Q6_CLAUSE}', '{Q7_CLAUSE}'] |
| 2c B-04 filled old block occurs exactly once in the accepted candidate | PASS | old 1, new 0 |
| 2d SOFTWARE_DECOMP.md equals accepted candidate + filled B-04 | PASS | ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5 |
| 2e SOFTWARE_DECOMP.md carries no unfilled token | PASS |  |
| 2f Q-5 option A: no 'OI-001/OI-002 Status' clause in the entry | PASS |  |
| 3a pre-act _LATEST.md at the basis named the predecessor (sha a9a7cdc8...) | PASS | a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d |
| 3b _LATEST.md equals the C-01 template with every slot filled and nothing else changed | PASS | ['{ACCEPT_DATE}', '{AMENDMENT_ID}', '{AMENDMENT_SNAPSHOT}', '{ARC_LIST}', '{CLOSURE_VERDICT}', '{GROUP12_REFS}', '{OPEN_LIST}', '{SCA001_CLOSURE}', '{UTC}'] |
| 3c slot values: AMENDMENT_SNAPSHOT, ACCEPT_DATE, AMENDMENT_ID, CLOSURE_VERDICT, UTC, ARC_LIST | PASS | {"AMENDMENT_SNAPSHOT": "SCA-V4-002_2026-09-29_1901", "ACCEPT_DATE": "2026-09-29", "AMENDMENT_ID": "SCA-V4-002", "CLOSURE_VERDICT": "OPEN_PENDING_DERIVATIVE_CLOSURE", "UTC": "20260930T021014Z", "ARC_LIST": "N-18, N-21, N-24 and X-1"} |
| 3d every repeated slot carries the same value (template refilled reproduces the file) | PASS |  |
| 3e GROUP12_REFS names the two actual decision folders | PASS | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/`, `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-2_2026-09-29/` |
| 3f SCA001_CLOSURE is OPEN_PENDING_DERIVATIVE_CLOSURE and cites the C-02 record at its committed path | PASS | `OPEN_PENDING_DERIVATIVE_CLOSURE` per `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md` |
| 3g OPEN_LIST carries the group-3 Handoff_State open items and the carried SCA-V4-001 items | PASS | ['9 ScopeOfWork REVISEs', 'B-06a', 'dependency-register', 'DAG-003', 'Coverage_Telemetry.json', '17 Design re-pins', 'ASC-ISS-001', 'audit-scope-closure'] |
| 3h first two lines are 'Latest:' and 'Updated:' (SPEC 11.2 form) | PASS | Latest: SCA-V4-002_2026-09-29_1901 / Updated: 2026-09-29 |
| 3i registered parser _latest_pointer_target resolves the pointer to the accepted snapshot and _pointer_matches is True | PASS | target 'SCA-V4-002_2026-09-29_1901' match True |
| 3j exactly one '**Active snapshot:**' line, naming the accepted snapshot | PASS | ['execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/'] |
| 3k no unfilled token in _LATEST.md | PASS |  |
| 4a Consolidated_Coverage.csv unchanged from the accepted candidate (the register carries no SOFTWARE_DECOMP.md row) | PASS | 366773650b588dc995f396be02d7e2690d9738c8d22afb98a85260dfb87313ea |
| 4b no Consolidated_Coverage.csv row names SOFTWARE_DECOMP.md | PASS | ['projects/chirality-app-v4/docs/ARCHITECTURE.md', 'projects/chirality-app-v4/docs/EXAMINATION.md', 'projects/chirality-app-v4/docs/HOST_INTEGRATION.md', 'projects/chirality-app-v4/docs/OPERATING_METHOD.md', 'projects/chirality-app-v4/docs/PRD.md'] |
| 4c the B8 rule recomputed over all rows against the working documents changes no row | PASS | 144 rows; drift [] |
| 5a every changed path is inside the post-acceptance write boundary (_ScopeChange/, SOFTWARE_DECOMP.md, POSTACCEPT/) | PASS | 20 paths; outside [] |
| 5b no ScopeOfWork.md, Dependencies.csv, _DEPENDENCIES.md, _DAG, _STATUS.md, Coverage_Telemetry.json or _LATEST_ACCEPTED.md changed | PASS | [] |
| 5c no SCA-V4-001 byte changed (snapshot, decision folders, validation records) | PASS | [] |
| 5d GROUP-1 ACCEPTED_MANIFEST.csv rows still match the working tree (append-only custody record excepted) | PASS | 9 rows; mismatches ['projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md'] |
| 5d GROUP-2 ACCEPTED_MANIFEST.csv rows still match the working tree (append-only custody record excepted) | PASS | 13 rows; mismatches ['projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md'] |
| 5e no group-1- or group-2-bound file was rewritten | PASS | [] |
| 6a active snapshot holds every required PROJECT/SOFTWARE artifact | PASS | missing [] |
| 6b accepted Handoff_State.md names the snapshot, register, derivative status, verdict, next workflows, V14 dispositions and carried items | PASS | missing [] |
| 6c exactly two SCA-* amendment snapshot folders exist (the predecessor and the active one), both complete | PASS | ['SCA-V4-001_2026-09-28_2155', 'SCA-V4-002_2026-09-29_1901'] |
| 6d candidate Handoff_State.md and RUN_SUMMARY.md bytes presented at group 3 are bound in the group-3 manifest | PASS |  |
| 7a audit-decomp rerun: 0 BLOCKER | PASS | 0/38/100 |
| 7b COV-139 absent: no 'Historical snapshot residue' finding | PASS | [] |
| 7c the registered-parser INFO is absent | PASS | {"status": "RUN", "target": "SCA-V4-002_2026-09-29_1901", "pointer_matches_active": true} |
| 7d Check 10 active snapshot and handoff state PASS, active snapshot is the accepted one | PASS | execution/_ScopeChange/SCA-V4-002_2026-09-29_1901 |
| 7e topology unchanged (11 packages, 41 deliverables, 10 objectives, 262 scope items) | PASS | {"packages": 11, "deliverables": 41, "objectives": 10, "scope_items": 262, "ledger_rows": 262} |
| 7f Change Register binds ('Decision Log' at rank exact) in the 9b finding | PASS | COV-137 |
| 7g the seven-package scope equals the register-derived scope | PASS | ['PKG-01', 'PKG-02', 'PKG-03', 'PKG-04', 'PKG-05', 'PKG-09', 'PKG-10'] |
| 8 accumulate_supersession_map.py --check-map on the active snapshot (prior = SCA-V4-001 map, delta = SCA-V4-002) | PASS | Wrote supersession map: <scratch>/Supersession_Map.regen.csv Rows: 29 Findings: 0 total, 0 blocking |
| 9a DAG-002 currency (run from the execution root): every bound file OK | PASS | 130/130 OK, exit 0 |
| 9b no deliverable is ISSUED or CHECKING (the ISSUED-reopen rule does not apply) | PASS | {"INITIALIZED": 27, "IN_PROGRESS": 14} |

## Applied and finalized files (sha256)

| File | sha256 |
|---|---|
| `projects/chirality-app-v4/execution/_Decomposition/Consolidated_Coverage.csv` | `366773650b588dc995f396be02d7e2690d9738c8d22afb98a85260dfb87313ea` |
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/Decision_Log.md` | `7d37092ea8aaa927c646c7f60d2e757bff2e0ff627c8ad3d540e747a83a67246` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/Handoff_State.md` | `5264b8e2a1cf35fd8fd3b6210621e8784d5fea6c3e309fea19b3664555469ff1` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/RUN_SUMMARY.md` | `b594856f2aea94eb40ed31d63026f8a3037fa16c8eeb59c465b20102bdd54de7` |
| `projects/chirality-app-v4/execution/_ScopeChange/_LATEST.md` | `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/ACCEPTED_MANIFEST.csv` | `c2244080bebc49584095e2e031dee40859bf9631f039ed28953866322282413d` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/DECISION.md` | `47f04469bd21fcbe1fb55dcb0c99392fd3c5c7050204e082d1c228770c33846d` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/Handoff_State.md` | `8385788837416cde73034e2cb320b880eebb4e7490d4b02574a9806046e17b7e` |

Result: PASS
## Notes

- **H-3.** The register carries rows for PRD, HOST_INTEGRATION, EXAMINATION, OPERATING_METHOD and ARCHITECTURE only. `SOFTWARE_DECOMP.md` carries none, so the H-1 entry shifts no row (4a–4c). No byte of `Consolidated_Coverage.csv` changed.
- **Audit script.** `POSTACCEPT/audit_checks.py` is `BASELINE/audit_checks.py` with the documented changes (f) and (g) only (the active amendment resolved from the pointer; the `**Accepted predecessor:**` line excluded from the one-snapshot reading). The unchanged base script's result on the same state (1 BLOCKER from its predecessor-line heuristic; the registered-parser INFO with a description that is no longer true) is disclosed in `POSTACCEPT/COMPARISON.md`. Neither is a finding against the applied state; the accepted C-01 text is not edited.
- **Not done under this record.** The nine `ScopeOfWork.md` REVISEs, B-06a, the register UPDATE and DAG-003 follow as propagation (DECISION-3 "Effects").
- **Files in this folder.** `apply_group3_edits.py` and `apply_log.json` are the application script and its log (a dry run to scratch first produced identical bytes); `verify_post_acceptance.py` wrote this file, `post_acceptance_checks.json`, `DAG_CURRENCY.txt` and `Supersession_Findings.csv`.
