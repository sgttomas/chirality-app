# DEL-09-06 dependency extraction — 2026-09-29 (DX-3)

Executor: Type 2 TASK node DX-3, a Claude Code `Agent` subagent (no delegation), run `APP-V4-BASIS-ALIGN-20260928`. Basis commit `557716cf7`. Git read-only; no network. Host filesystem permissions exceed the instruction write boundary; no narrower host enforcement is claimed. Writes: this deliverable's `Dependencies.csv`, `_DEPENDENCIES.md` and this record; the run-folder return file `DX/DX-3_DEL-09-06.md`; scratch only under the session scratchpad.

## Basis and method

Selected `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md + resources/brief.md, checks.md, tools.md, execution.json loaded in full). Brief: `BRIEFS.md` § "DX — dependency-extract UPDATE for 18 deliverables" plus the DX-3 dispatch guards. SCOPE=DEL-09-06; MODE=UPDATE; STRICTNESS=CONSERVATIVE; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`. Design files were not read.

## Guard stop and clarification

As first dispatched, the guard read "DEL-09-06 must not gain rows that consume any SCC-002 member". Read literally, it fired on 6 rows that the revised CLM-003 forces (→ DEL-02-01, 02-02, 03-01, 03-02, 03-03, 04-02). The deliverable was stopped, and a candidate was built and validated in scratch only. The integrator then ruled that the intended guard, per node P2, is: no row that makes an SCC-002 member depend on DEL-09-06, and no DOWNSTREAM row from DEL-09-06 to an SCC-002 member. DEL-09-06 consuming SCC-002 members is allowed; the six rows are in the refreshed 41-arc set accepted under DECISION-6. The validated candidate was applied unchanged: the applied file is field-identical to it, and the SoW and register hashes were unchanged since the stop.

## Extraction result

- Pass 1: parent PKG-09; traces SOW-040, -041, -236, -237, -238, -240, -241 and OBJ-001, -004, -008 re-confirmed.
- Pass 2:
  - **Added**, all UPSTREAM INTERFACE from revised CLM-003: DEP-09-06-025 → DEL-02-01, -026 → DEL-02-02, -027 → DEL-03-01, -028 → DEL-03-02, -029 → DEL-03-03, -030 → DEL-04-01, -031 → DEL-04-02, -032 → DEL-01-01.
  - **Added:** DEP-09-06-033, DOWNSTREAM HANDOVER to EXTERNAL DEP-001 (OUT-004), and DEP-09-06-034, UPSTREAM CONSTRAINT on EXTERNAL DECISION-3 (TBD-003(c)).
  - **Refreshed in place:** 016, 017 (re-quote); 022, 023 (TBD-002 rulings); 024 (checkpoint phasing). 012 and 014 got notes only.
  - **Unchanged** (LastSeen only): the other 12 rows. **Retired:** none.
- Intended guard satisfied: DEL-09-06 has no DOWNSTREAM deliverable rows. Arcs into DEL-09-06 in the working tree come only from DEL-03-04 and DEL-09-07, and neither is in SCC-002.
- SCC check over all 41 working-tree registers after the write: 198 arcs (161 from DAG-001 plus 37 added; none removed). The six SCCs are identical to DAG-001's, SCC-002 has 13 members, and DEL-09-06 is in no SCC.
- Declaration mirrors 0/0/0; 2 placeholders skipped. Human-owned prefix byte-identical; prior Run Notes/History retained.
- Counts: ACTIVE 34 (ANCHOR 11, EXECUTION 23: 21 UPSTREAM, 2 DOWNSTREAM), RETIRED 0.

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
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/ScopeOfWork.md` | deliverable-local input (before run) | `287d47a1260e7433c3f16578c67345d067472165421c65848bd15e44d92a7923` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/_REFERENCES.md` | deliverable-local input (before run) | `0e15a1c57eca50583818cf1c8dccd55366e91eea5a02d2dc7ffacbd7217f6b9d` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/Dependencies.csv` | deliverable-local input (before run) | `ce3218a22a8629a731a05f5d24093e9aee6660b011a63414b1589c828e4297ed` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/_DEPENDENCIES.md` | deliverable-local input (before run) | `0943c9beccc31781aa20ecfd49945664001ab398c83ea6fd4d1057f482711f08` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/REGISTER_CHANGES.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `89be49e53a9dcc4231fb17012d8496c5bebb2136dd5745982cf753e51cb05696` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `7daf474ba17c799740edbd42c1ba811b3cf431641277707c81834bef358478f2` |
| `projects/chirality-app-v4/execution/_DAG/DAG-001/GRAPH_BASIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `d09b49cfa4c82c7c7caf8e45d82e4ed4ec904b345e7c9b68ab3c2b3e660cb3f0` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/proposed_rows/DEL-09-06_proposed_rows.csv` | coordinator comparison only (read after extraction decisions; not an extraction input) | `f7d37e607c4a664bd75754579e11dd0f13194c4bf7e0924b086b21f72885fd52` |

## Actual checks

```
SCHEMA exit 0 | VALID: /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd/projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/Dependencies.csv Columns: 29 (29 required + 0 extension) Data rows: 34
ENUM invocations 23 failures []
DUP IDS []
ID invocations 63 failures []
PREFIX mismatches []
PARENT anchors 1
ACTIVE missing evidence []
EVQ-003 blank quotes [] EVQ-004 placeholder []
DECLARED rows 0 CANDIDATE status 0
placement errors []
```

Validators: `python3 tools/validation/validate_dependencies_schema.py <register>`; `python3 tools/validation/validate_enum.py <ENUM> <value>` for every distinct value of the ten enum columns; `bash tools/validation/validate_id_format.sh <TYPE> <value>` for every DEP/DEL/PKG/SOW/OBJ identifier present; inline Python assertions for quote verbatim-ness against the current SoW (whitespace-normalized), quote length <=30 words, ID uniqueness/prefix, parent-anchor count, evidence presence and target-ID placement.

## Output identities

- `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/Dependencies.csv` — SHA256 `0f8ecad83cca72f7c65786ff0cd0252a2b7664c145a6e39193cff332a639f2f6`
- `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/_DEPENDENCIES.md` — SHA256 `79e780eeab12c6ff84326ee0b74a0953cb0046ffac7998c41bda5fac87182313`
- this run record (self-hash omitted).
