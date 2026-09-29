# DEL-09-07 dependency extraction — 2026-09-29 (DX-3)

Executor: Type 2 TASK node DX-3, a Claude Code `Agent` subagent (no delegation), run `APP-V4-BASIS-ALIGN-20260928`. Basis commit `557716cf7`. Git read-only; no network. Host filesystem permissions exceed the instruction write boundary; no narrower host enforcement is claimed. Writes: this deliverable's `Dependencies.csv`, `_DEPENDENCIES.md` and this record; the run-folder return file `DX/DX-3_DEL-09-07.md`; scratch only under the session scratchpad.

## Basis and method

Selected `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md + resources/brief.md, checks.md, tools.md, execution.json loaded in full). Brief: `BRIEFS.md` § "DX — dependency-extract UPDATE for 18 deliverables" plus the DX-3 dispatch guards. SCOPE=DEL-09-07; MODE=UPDATE; STRICTNESS=CONSERVATIVE; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`. Design files were not read.

## Extraction result

- Pass 1: parent PKG-09; traces SOW-199, SOW-200, SOW-201, SOW-202, SOW-239, OBJ-004, OBJ-005, OBJ-008, OBJ-009 re-confirmed. SOW-201/SOW-202 labels (TargetName) and locations re-resolved to the current `_Decomposition/ScopeLedger.csv`, which SCA-V4-001 amended; legacy GROUP3 labels kept in Notes.
- Pass 2: **added** none; **refreshed in place** `DEP-09-07-016` (DEP-001 external contribution; Statement for destination-enforcement wording) and `DEP-09-07-021` (person's checkpoint act; Statement, SourceRef and a re-quote from VER-005, because the old quote is no longer in the SoW); **unchanged** (LastSeen only) the other 21 rows; **retired** none.
- Not written: no deliverable target is newly named (the SoW names only DEL-09-06, DEL-11-03 and PKG-02/03/04/05, all already carried). No P2 proposals exist for DEL-09-07.
- Declaration mirrors 0/0/0; 2 placeholders skipped. Human-owned prefix byte-identical; prior Run Notes/History retained.
- Counts: ACTIVE 25 (ANCHOR 10, EXECUTION 15: 14 UPSTREAM, 1 DOWNSTREAM), RETIRED 0.
- Guards: not applicable; none triggered.

## Actual read identities (SHA256 of full file bytes)

| File | Role | SHA256 |
|---|---|---|
| `AGENTS.md` | method/brief/decomposition | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` |
| `workflows/dependency-extract/WORKFLOW.md` | method/brief/decomposition | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` |
| `workflows/dependency-extract/resources/brief.md` | method/brief/decomposition | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` |
| `workflows/dependency-extract/resources/checks.md` | method/brief/decomposition | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` |
| `workflows/dependency-extract/resources/tools.md` | method/brief/decomposition | `dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8` |
| `workflows/dependency-extract/execution.json` | method/brief/decomposition | `bfb5417afe85ee0e268a4c0353f4378a42a015925f383232bdaa766b866110e2` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/BRIEFS.md` | method/brief/decomposition | `aec0fa8ed521a1067826a980e840d8540db5d26efd1a9c832a96a769ad691211` |
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | method/brief/decomposition | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` |
| `projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv` | method/brief/decomposition | `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` |
| `projects/chirality-app-v4/execution/_Decomposition/Deliverables.csv` | method/brief/decomposition | `2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44` |
| `projects/chirality-app-v4/execution/_Decomposition/Packages.csv` | method/brief/decomposition | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` |
| `projects/chirality-app-v4/execution/_Decomposition/Objectives.csv` | method/brief/decomposition | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/ScopeOfWork.md` | deliverable-local input (before run) | `53b51d309d060089a6a88dae565867a92348789ee01430927e7464c7c2d3cba0` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/_REFERENCES.md` | deliverable-local input (before run) | `04228f89c617ee12039347d7af8e65ca78d4eefa72e5d80ff75cf1e32af66996` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/Dependencies.csv` | deliverable-local input (before run) | `a18008ceb3e1b1e7632775255cba1cd4e6842b35cd66e47bf1681167ae90bf75` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/_DEPENDENCIES.md` | deliverable-local input (before run) | `6705cd6f038e6effb566800d8b49bc4af7a8be9f24c1e7114774ca564aeb5776` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/REGISTER_CHANGES.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `89be49e53a9dcc4231fb17012d8496c5bebb2136dd5745982cf753e51cb05696` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `7daf474ba17c799740edbd42c1ba811b3cf431641277707c81834bef358478f2` |
| `projects/chirality-app-v4/execution/_DAG/DAG-001/GRAPH_BASIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `d09b49cfa4c82c7c7caf8e45d82e4ed4ec904b345e7c9b68ab3c2b3e660cb3f0` |

## Actual checks

```
SCHEMA exit 0 | VALID: /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd/projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/Dependencies.csv Columns: 29 (29 required + 0 extension) Data rows: 25
ENUM invocations 23 failures []
DUP IDS []
ID invocations 43 failures []
PREFIX mismatches []
PARENT anchors 1
ACTIVE missing evidence []
EVQ-003 blank quotes [] EVQ-004 placeholder []
DECLARED rows 0 CANDIDATE status 0
placement errors []
```

Validators: `python3 tools/validation/validate_dependencies_schema.py <register>`; `python3 tools/validation/validate_enum.py <ENUM> <value>` for every distinct value of the ten enum columns; `bash tools/validation/validate_id_format.sh <TYPE> <value>` for every DEP/DEL/PKG/SOW/OBJ identifier present; inline Python assertions for quote verbatim-ness against the current SoW (whitespace-normalized), quote length <=30 words, ID uniqueness/prefix, parent-anchor count, evidence presence and target-ID placement.

## Output identities

- `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/Dependencies.csv` — SHA256 `2de47a1272544eb201b1920c79bd6116eed037288e6109ec5012b9b7e3491d22`
- `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/_DEPENDENCIES.md` — SHA256 `40a9f0fe8ab99b7ee0f9cf1279a6fef543d18cd9ed368cda52c7c5d89c9868fc`
- this run record (self-hash omitted).
