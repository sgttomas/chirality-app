# DEL-03-04 dependency extraction — 2026-09-29 (DX-3)

Executor: Type 2 TASK node DX-3, a Claude Code `Agent` subagent (no delegation), run `APP-V4-BASIS-ALIGN-20260928`. Basis commit `557716cf7`. Git read-only; no network. Host filesystem permissions exceed the instruction write boundary; no narrower host enforcement is claimed. Writes: this deliverable's `Dependencies.csv`, `_DEPENDENCIES.md` and this record; the run-folder return file `DX/DX-3_DEL-03-04.md`; scratch only under the session scratchpad.

## Basis and method

Selected `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md + resources/brief.md, checks.md, tools.md, execution.json loaded in full). Brief: `BRIEFS.md` § "DX — dependency-extract UPDATE for 18 deliverables" plus the DX-3 dispatch guards. SCOPE=DEL-03-04; MODE=UPDATE; STRICTNESS=CONSERVATIVE; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`. Design files were not read.

## Extraction result

- Pass 1: parent anchor PKG-03 and traces SOW-156, SOW-187, OBJ-004 re-confirmed (unchanged frontmatter; none of these IDs amended by SCA-V4-001).
- Pass 2 against the SCA-V4-001-revised SoW:
  - **Added** `DEP-03-04-021` UPSTREAM INTERFACE → DEL-01-01; `DEP-03-04-022` UPSTREAM INTERFACE → DEL-09-06; `DEP-03-04-023` UPSTREAM INTERFACE → DEL-09-09. All from the new CLM-003 final sentence ("The guide also consumes App v4 DEL-01-01's supplier boundary …, DEL-09-06's relay questions and recorded SWBPIPE answers … and DEL-09-09's external trace cases"). Arcs DEL-03-04 → DEL-01-01, → DEL-09-06, → DEL-09-09.
  - **Refreshed in place** `DEP-03-04-011` (→ DEL-04-01): Statement, SourceRef, Notes for revised REQ-004 and TBD-001/TBD-002. Quote, type, direction, RequiredMaturity, SatisfactionStatus unchanged.
  - **Unchanged** (LastSeen only): 001–010, 012–020. **Retired:** none.
- Declaration mirrors 0/0/0; 2 placeholders skipped. Human-owned prefix byte-identical before/after; prior Run Notes/History retained verbatim.
- Counts: ACTIVE 23 (ANCHOR 4, EXECUTION 19: all UPSTREAM), RETIRED 0.
- Guards: none triggered. No reverse rows are implied (E-2 DEL-09-09 → DEL-03-04 and E-5 DEL-09-06 → DEL-03-04 remain absent from those registers' scope).

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
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/ScopeOfWork.md` | deliverable-local input (before run) | `895f004e4d0f133798f461d8157ac63fff880da09f471be9bae885fe0cfb7c28` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/_REFERENCES.md` | deliverable-local input (before run) | `1279ea2225a3faf0e226b2457fa868dae729799fb2655c071e37a80b677283fd` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/Dependencies.csv` | deliverable-local input (before run) | `b41eacd01cdef10e455017cda7afdfae85b2a2a2e989fad481d697f4e862ac17` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/_DEPENDENCIES.md` | deliverable-local input (before run) | `87c9fdf1227ae59dcf709755b1be6a6d003c8f5961abd09899f9ed41632407d5` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/REGISTER_CHANGES.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `89be49e53a9dcc4231fb17012d8496c5bebb2136dd5745982cf753e51cb05696` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `7daf474ba17c799740edbd42c1ba811b3cf431641277707c81834bef358478f2` |
| `projects/chirality-app-v4/execution/_DAG/DAG-001/GRAPH_BASIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `d09b49cfa4c82c7c7caf8e45d82e4ed4ec904b345e7c9b68ab3c2b3e660cb3f0` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/proposed_rows/DEL-03-04_proposed_rows.csv` | coordinator comparison only (read after extraction decisions; not an extraction input) | `b3a56c023abc47cb992c3d1c2f90181e009a29d87bf8fec11b555fd5abd668a2` |

## Actual checks

```
SCHEMA exit 0 | VALID: /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd/projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/Dependencies.csv Columns: 29 (29 required + 0 extension) Data rows: 23
ENUM invocations 19 failures []
DUP IDS []
ID invocations 53 failures []
PREFIX mismatches []
PARENT anchors 1
ACTIVE missing evidence []
EVQ-003 blank quotes [] EVQ-004 placeholder []
DECLARED rows 0 CANDIDATE status 0
placement errors []
```

Validators: `python3 tools/validation/validate_dependencies_schema.py <register>`; `python3 tools/validation/validate_enum.py <ENUM> <value>` for every distinct value of the ten enum columns; `bash tools/validation/validate_id_format.sh <TYPE> <value>` for every DEP/DEL/PKG/SOW/OBJ identifier present; inline Python assertions for quote verbatim-ness against the current SoW (whitespace-normalized), quote length <=30 words, ID uniqueness/prefix, parent-anchor count, evidence presence and target-ID placement.

## Output identities

- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/Dependencies.csv` — SHA256 `977d8712e02b4e22eb1191da82013fc974aedf76fc482e63302c5f6512bee32b`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/_DEPENDENCIES.md` — SHA256 `8d68928a6dc838811d82b693b402b0d0f45b2c631398e34748e657857b69a6b2`
- this run record (self-hash omitted).
