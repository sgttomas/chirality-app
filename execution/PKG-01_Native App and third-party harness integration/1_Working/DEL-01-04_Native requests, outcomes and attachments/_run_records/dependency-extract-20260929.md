# DEL-01-04 dependency extraction — 2026-09-29T14:34:59Z

- Executor: node DX-1 of run APP-V4-BASIS-ALIGN-20260928 — a Claude Code `Agent` subagent (Type 2 TASK) dispatched by HELP_HUMAN; it created no descendant. Basis commit 557716cf7. Git read-only; no network.
- Method: chirality-root:bundled:workflow:dependency-extract (WORKFLOW.md and resources/brief.md, checks.md, tools.md loaded in full). Brief: BRIEFS.md section "DX — dependency-extract UPDATE for 18 deliverables" plus the dispatch message (SCOPE DEL-01-04; MODE UPDATE; STRICTNESS CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; DECOMPOSITION_PATH execution/_Decomposition/SOFTWARE_DECOMP.md; guard on DEL-09-06 relay-file pointers).
- Write boundary: this deliverable's Dependencies.csv, _DEPENDENCIES.md (agent-owned sections) and this record, plus the return file DX/DX-1_DEL-01-04.md in the run folder. The host filesystem allowed more; the brief set the narrower boundary. Other deliverables' registers changed in the same worktree during this run by sibling nodes DX-2/DX-3; DX-1 did not touch them.
- Result: ACTIVE 19 (ANCHOR 6 / EXECUTION 13); RETIRED 0; EXTERNAL (ACTIVE) 7; UNKNOWN 0; DECLARED 0. Declared mirroring 0/0/0; 2 placeholders skipped. Parameters and per-row reasons are in _DEPENDENCIES.md Run Notes.

## Actual read identities

`EX` = `projects/chirality-app-v4/execution`. The hashes identify the files read. Read order: ARC_ANALYSIS.md, REGISTER_CHANGES.md §1–§3 (which include the per-deliverable arc summary) and the DAG-001 edge files were read during the DEL-04-01 comparison, so before this deliverable was extracted. This deliverable's REGISTER_CHANGES §4/§5 section and proposed_rows file were read only after its extraction. Every row rests on the ScopeOfWork text it quotes. No row change followed that reading.

| Path | SHA256 | Read scope |
|---|---|---|
| AGENTS.md | c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd | full |
| agents/AGENT_TASK.md | 1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7 | full |
| workflows/dependency-extract/WORKFLOW.md | e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3 | full |
| workflows/dependency-extract/execution.json | bfb5417afe85ee0e268a4c0353f4378a42a015925f383232bdaa766b866110e2 | full |
| workflows/dependency-extract/resources/brief.md | b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde | full |
| workflows/dependency-extract/resources/checks.md | a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457 | full |
| workflows/dependency-extract/resources/tools.md | dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8 | full |
| EX/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/BRIEFS.md | aec0fa8ed521a1067826a980e840d8540db5d26efd1a9c832a96a769ad691211 | DX section / node table |
| EX/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DISPATCH.md | 934492e0b78da56758028c2fdd167ca4e07762cc1371fb832c868c70febe8beb | DX section / node table |
| EX/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/REGISTER_CHANGES.md | 89be49e53a9dcc4231fb17012d8496c5bebb2136dd5745982cf753e51cb05696 | post-extraction coordinator comparison only |
| EX/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md | 7daf474ba17c799740edbd42c1ba811b3cf431641277707c81834bef358478f2 | post-extraction coordinator comparison only |
| EX/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/evidence/scc_result.json | 5725d57aa1023be77fdf3e48f28452c9b5f0b99f50bc47db21d38969acdc9a51 | post-extraction coordinator comparison only |
| EX/_Decomposition/SOFTWARE_DECOMP.md | 7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747 | identity/label rows used |
| EX/_Decomposition/Deliverables.csv | 2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44 | identity/label rows used |
| EX/_Decomposition/ScopeLedger.csv | d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f | identity/label rows used |
| EX/_Decomposition/Objectives.csv | e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248 | identity/label rows used |
| EX/_Decomposition/Packages.csv | f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663 | identity/label rows used |
| EX/_Decomposition/Open_Issues.csv | f6b92362c4f334ffe65522557acb515d247ba67133403cc6c805f1c5c4182bf7 | identity/label rows used |
| EX/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv | bcdf6f2f5352e00360c19a956bd22c026909c388d77c76f92b4983ed906415eb | identity/label rows used |
| EX/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv | 363643306d3bbda80f4496943a5d1de5187d7910fabdf5b89f929e6c9605fd73 | identity/label rows used |
| EX/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Objectives.csv | e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248 | identity/label rows used |
| EX/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Packages.csv | b8a9b949b629fb8dbe3343e0e5a1f09a30621785d99676f71adb1b285f741fbd | identity/label rows used |
| EX/_DAG/DAG-001/DependencyEdges.csv | 5693c36fb573078eb00d959a926c461fde275f5b4a54535da32096fcaf2d1905 | post-extraction coordinator comparison only |
| EX/_DAG/DAG-001/CandidateEdges.csv | 1c3edb4f7079b8046e7161df45b1ffaf674621cf35186ec20787be0f82b9b0e9 | post-extraction coordinator comparison only |
| tools/validation/validate_dependencies_schema.py | 75cd74768cc8edf91c6f40b582f0fb570d2427894e6c2236ea2fe7d384291f5f | executed validator (not read) |
| tools/validation/validate_enum.py | 562934b075b20e7ec366baf60146cf7524acaebad8612b87873c4828dbeeaa70 | executed validator (not read) |
| tools/validation/validate_id_format.sh | 370c946c301323b1bb273d268f04d4dc4187b865d9d2865b5273f0dd27d0acac | executed validator (not read) |
| projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md | 7261a58f93d4531ca080c16d7fe088818871c3444085bade2eb2350ace94e60a | full (unchanged before/after) |
| projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Dependencies.csv (pre-run) | 45546cfeeac2509b975d42dccb132fee6f1baf62600d1c9b8559c7ac665f61e3 | full |
| projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/_DEPENDENCIES.md (pre-run) | 3caaec7fb441ac3fa4110738e806f08f05beb096d1c0954ddc86b3088228f74f | full |

## Mandatory validation evidence (run from the repository root)

Commands: `python3 tools/validation/validate_dependencies_schema.py '<deliverable>/Dependencies.csv'`; `python3 tools/validation/validate_enum.py <ENUM> <value>` for every distinct value in the ten enum columns; `bash tools/validation/validate_id_format.sh <TYPE> <value>` for every FromDeliverableID/FromPackageID/DependencyID/TargetDeliverableID/TargetPackageID and every PKG/SOW/OBJ TargetRefID.

```
### schema
VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Dependencies.csv
  Columns: 29 (29 required + 0 extension)
  Data rows: 19
exit 0
### enums
DEPENDENCY_CLASS ANCHOR rc=0
DEPENDENCY_CLASS EXECUTION rc=0
ANCHOR_TYPE IMPLEMENTS_NODE rc=0
ANCHOR_TYPE NOT_APPLICABLE rc=0
ANCHOR_TYPE TRACES_TO_REQUIREMENT rc=0
DIRECTION DOWNSTREAM rc=0
DIRECTION UPSTREAM rc=0
DEPENDENCY_TYPE CONSTRAINT rc=0
DEPENDENCY_TYPE HANDOVER rc=0
DEPENDENCY_TYPE INTERFACE rc=0
DEPENDENCY_TYPE OTHER rc=0
DEPENDENCY_TYPE PREREQUISITE rc=0
TARGET_TYPE DELIVERABLE rc=0
TARGET_TYPE EXTERNAL rc=0
TARGET_TYPE REQUIREMENT rc=0
TARGET_TYPE WBS_NODE rc=0
EXPLICITNESS EXPLICIT rc=0
CONFIDENCE HIGH rc=0
ORIGIN EXTRACTED rc=0
STATUS ACTIVE rc=0
SATISFACTION_STATUS NOT_APPLICABLE rc=0
SATISFACTION_STATUS TBD rc=0
enum checks: 22, failures: 0
### ids
id checks: 33, failures: 0
```

IDs checked: DEL:DEL-01-01, DEL:DEL-01-02, DEL:DEL-01-04, DEL:DEL-02-02, DEL:DEL-04-01, DEL:DEL-04-03, DEP:DEP-01-04-001, DEP:DEP-01-04-002, DEP:DEP-01-04-003, DEP:DEP-01-04-004, DEP:DEP-01-04-005, DEP:DEP-01-04-006, DEP:DEP-01-04-007, DEP:DEP-01-04-008, DEP:DEP-01-04-009, DEP:DEP-01-04-010, DEP:DEP-01-04-011, DEP:DEP-01-04-012, DEP:DEP-01-04-013, DEP:DEP-01-04-014, DEP:DEP-01-04-015, DEP:DEP-01-04-016, DEP:DEP-01-04-017, DEP:DEP-01-04-018, DEP:DEP-01-04-019, OBJ:OBJ-001, OBJ:OBJ-002, PKG:PKG-01, PKG:PKG-02, PKG:PKG-04, SOW:SOW-005, SOW:SOW-014, SOW:SOW-129.

Local in-memory checks: unique DependencyIDs and ACTIVE semantic keys; DEP-01-04- prefix; FromDeliverableID DEL-01-04; exactly one ACTIVE IMPLEMENTS_NODE; target-ID placement; every ACTIVE EvidenceQuote verbatim in the source (markdown emphasis/code marks ignored) and at most 30 words; no placeholder SourceRef; human-owned prefix of _DEPENDENCIES.md byte-identical; Run History append-only; _DEPENDENCIES.md counts equal to the CSV. Source, _REFERENCES.md and _STATUS.md SHA256 unchanged. Optional validate_decomposition_registers.py not run (the brief names only the three validators).
