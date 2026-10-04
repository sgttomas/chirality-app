# SCA-V4-003 post-acceptance validation

Owner act: DECISION-2, 2026-10-03, America/Denver ("I accept the audited result."; `checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/`). Accepted basis `84b520742d` (candidate `fa16393978`, records `388fc730b9`). Applied state: uncommitted working tree over `84b520742d`. Record `SCA-V4-003_20261004T005706Z`, written by `verify_post_acceptance.py`, which recomputes the applied bytes from the accepted basis independently of `apply_group3_edits.py`. The candidate evidence reviewed at group 3 (POSTCHANGE/, V24) is not modified. No `ScopeOfWork.md`, register or DAG file is changed under this record: the 19 REVISEs, the register UPDATE and DAG-004 follow as propagation.

| Check | Result | Detail |
|---|---|---|
| 1a group-3 DECISION.md first line is the accepted heading (check_amendment_reopen.py form) | PASS | # SCA-V4-003 checkpoint group 3 — accepted audited poststate |
| 1b the act text is quoted in DECISION.md and in the DECISION-2 section of OWNER_DECISIONS.md | PASS | I accept the audited result. |
| 1c OWNER_DECISIONS.md custody hash equals the cited hash and its blob at 84b520742d | PASS | 29c0a07b50d695a15bbff52b36d5925725cc7f3e78d0caf997ee9fd3c3b28c2e |
| 1d commit 84b520742d changes only OWNER_DECISIONS.md over the presentation commit 388fc730b9 | PASS | projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md |
| 1e group-3 ACCEPTED_MANIFEST.csv binds the presented bytes (every row equals its blob at 84b520742d) | PASS | 42 rows; mismatches [] |
| 1f group-3 folder holds DECISION.md, ACCEPTED_MANIFEST.csv, Handoff_State.md | PASS | ['ACCEPTED_MANIFEST.csv', 'DECISION.md', 'Handoff_State.md'] |
| 1g check_amendment_reopen.py (unanchored, read-only) finds the group-3 acceptance and the group-2 register at its bound hash | PASS | projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03; projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/Amendment_Actions.csv; 9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c |
| 2a BASIS_AMENDMENT.md is the accepted bytes | PASS | 151bc6fffcac482f6f8e77bf3d7b2822ec65f94012e0b66720f14644efbe35bf |
| 2b B-01 old block occurs exactly once in the accepted state, the new block zero times | PASS | old 1, new 0 |
| 2c SOFTWARE_DECOMP.md equals the accepted state + filled B-01, and the expected hash 983199cc... | PASS | 983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d |
| 2d SOFTWARE_DECOMP.md carries no unfilled slot and gained exactly two lines | PASS | {"{ACCEPT_DATE}": "2026-10-03", "{AMENDMENT_SNAPSHOT}": "SCA-V4-003_2026-10-03_1827", "{Q5_CLAUSE}": ", including the App act control in DEL-01-04", "{OI018_CLAUSE}": " and the OI-018 Consequence pointer", "{D021_CLAUSE}": "; and a Supersession_Delta row binding the GROUP3 OI-009 Status", "{OI009_CLAUSE}": "Open_Issues OI-009 Status (RESOLVED_BY_OWNER_DECISION) and Consequence"} |
| 3a pre-act _LATEST.md (blob at 84b520742d) is 2b7938bc... naming SCA-V4-002 | PASS | 2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1 |
| 3b _LATEST.md equals the C-01 text with every slot filled and nothing else | PASS | 19cf31f14da259d64c52b33f52598dbe66381f0a887b34a13d3eccce9388e657 |
| 3c registered parser _latest_pointer_target resolves the pointer to the accepted snapshot and _pointer_matches is True | PASS | target 'SCA-V4-003_2026-10-03_1827' match True |
| 3d first two lines are 'Latest:' and 'Updated:' (SPEC 11.2 form) | PASS | Latest: SCA-V4-003_2026-10-03_1827 / Updated: 2026-10-03 |
| 3e exactly one '**Active snapshot:**' line, naming the accepted snapshot | PASS | ['execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/'] |
| 3f every path _LATEST.md names exists | PASS | 7 paths; missing [] |
| 3g no unfilled slot in _LATEST.md | PASS |  |
| 4a Consolidated_Coverage.csv unchanged (no basis text changed) and no row names SOFTWARE_DECOMP.md | PASS | 366773650b588dc995f396be02d7e2690d9738c8d22afb98a85260dfb87313ea; 144 rows |
| 5a every changed path since 84b520742d is inside the acceptance-time write boundary | PASS | 29 paths; outside [] |
| 5b no ScopeOfWork, register, _DEPENDENCIES, _DAG, _STATUS, _CONTEXT, Coverage_Telemetry, _LATEST_ACCEPTED or Open_Issues byte changed | PASS | [] |
| 5c no SCA-V4-001 or SCA-V4-002 byte changed | PASS | [] |
| 5d-GROUP-1 GROUP-1 ACCEPTED_MANIFEST.csv rows still match (append-only custody record and, for group 2, the by-design pre-change Open_Issues row excepted) | PASS | 11 rows; mismatches ['projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md'] |
| 5d-GROUP-2 GROUP-2 ACCEPTED_MANIFEST.csv rows still match (append-only custody record and, for group 2, the by-design pre-change Open_Issues row excepted) | PASS | 13 rows; mismatches ['projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md', 'projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv'] |
| 5e of the 13 artifacts only the three status records changed (F-2..F-4); the other ten equal their presented hashes | PASS | ['Decision_Log.md', 'Handoff_State.md', 'RUN_SUMMARY.md'] |
| 5f F-2 changed only the standing lines, added the DECISION-2 row and appended the AK2 section | PASS |  |
| 5g F-3 and F-4: reproducing the listed status-line replacements on the presented bytes gives the working files | PASS |  |
| 6a active snapshot holds every required artifact | PASS | 13 |
| 6b exactly three SCA-* amendment snapshot folders exist (two predecessors and the active one), all complete | PASS | ['SCA-V4-001_2026-09-28_2155', 'SCA-V4-002_2026-09-29_1901', 'SCA-V4-003_2026-10-03_1827'] |
| 7a audit-decomp rerun (unchanged baseline script): 0 BLOCKER | PASS | 0/51/77 |
| 7b the audit script is byte-identical to BASELINE/audit_checks.py | PASS | 8c3bef0676f826692d82261742488dd45148fdb5bb718a9dd9c39e7b903eb0d3 |
| 7c no 'Historical snapshot residue' finding (COV-129 closed) | PASS |  |
| 7d Check 10 active snapshot and handoff state PASS; active snapshot is SCA-V4-003; registered parser matches | PASS | {"status": "RUN", "target": "SCA-V4-003_2026-10-03_1827", "pointer_matches_active": true} |
| 7e topology unchanged (11 packages, 41 deliverables, 10 objectives, 262 scope items) | PASS | {"packages": 11, "deliverables": 41, "objectives": 10, "scope_items": 262, "ledger_rows": 262} |
| 7f counts equal the recorded simulation (0/51/77) | PASS | simulation 0/51/77 |
| 7g IssueLog and Matrix byte-identical to the simulation's outputs (scratch copy of AK1-R's run) | PASS | <scratch>/ak1r_sim/out |
| 8 accumulate_supersession_map.py --check-map on the active snapshot (prior = SCA-V4-002 map, delta = SCA-V4-003) | PASS | Wrote supersession map: <scratch>/Supersession_Map.regen.csv Rows: 30 Findings: 0 total, 0 blocking |
| 9a DAG-003 currency: SOURCE_MANIFEST (from the execution root) and MANIFEST all OK | PASS | 130 and 37 OK |
| 9b no deliverable is ISSUED or CHECKING (the ISSUED-reopen rule does not apply) | PASS | {"IN_PROGRESS": 20, "INITIALIZED": 21} |

## Applied and finalized files (sha256)

| File | sha256 |
|---|---|
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d` |
| `projects/chirality-app-v4/execution/_ScopeChange/_LATEST.md` | `19cf31f14da259d64c52b33f52598dbe66381f0a887b34a13d3eccce9388e657` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/Decision_Log.md` | `25367610eb3b2c15217ee9c6e998d83ca390de8471623f21d1470ed936e280f6` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/Handoff_State.md` | `775fb93ffebb0114ba70c395ac42b1b4361a4ed8145a2c96d23dbf30813038f8` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/RUN_SUMMARY.md` | `e864fd27d729fad472e4b2d1215424c85870a1500e0ea17387f802730649ccd0` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/DECISION.md` | `b6e90900b32b7ca38c2fc50e49c85619812dace6fee4c10cb5c28e7b6d81af60` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/ACCEPTED_MANIFEST.csv` | `b3651c16fb39a8db6e36ab8a71164a4d46e3664f740bdb31f8d5b4a52deba847` |
| `projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/Handoff_State.md` | `07a2f0f0728b937deba00c0e4f7f3aca0b937842742c1f1a29d938f578e0fe01` |

Result: PASS
