# DEL-09-09 dependency extraction — 2026-09-29 (DX-3)

Executor: Type 2 TASK node DX-3, a Claude Code `Agent` subagent (no delegation), run `APP-V4-BASIS-ALIGN-20260928`. Basis commit `557716cf7`. Git read-only; no network. Host filesystem permissions exceed the instruction write boundary; no narrower host enforcement is claimed. Writes: this deliverable's `Dependencies.csv`, `_DEPENDENCIES.md` and this record; the run-folder return file `DX/DX-3_DEL-09-09.md`; scratch only under the session scratchpad.

## Basis and method

Selected `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md + resources/brief.md, checks.md, tools.md, execution.json loaded in full). Brief: `BRIEFS.md` § "DX — dependency-extract UPDATE for 18 deliverables" plus the DX-3 dispatch guards. SCOPE=DEL-09-09; MODE=UPDATE; STRICTNESS=CONSERVATIVE; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`. Design files were not read.

## Extraction result

- Pass 1: parent PKG-09; traces SOW-073, SOW-203, SOW-204, OBJ-004, OBJ-008 re-confirmed (unchanged).
- Pass 2 against the SCA-V4-001-revised SoW:
  - **Added** `DEP-09-09-021` UPSTREAM PREREQUISITE → DEL-05-01; `DEP-09-09-022` UPSTREAM PREREQUISITE → DEL-04-02; `DEP-09-09-023` UPSTREAM PREREQUISITE → DEL-02-03 (revised CLM-002 plus "This deliverable consumes their identified contributions"). Arcs DEL-09-09 → DEL-05-01 / DEL-04-02 / DEL-02-03.
  - **Added** `DEP-09-09-024` UPSTREAM CONSTRAINT → EXTERNAL APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3 (new TBD-005: host joins deferred until the owner resumes SWBPIPE UI-SUCCESSOR; point of need before the live XC cases). Non-topological.
  - **Refreshed in place** `DEP-09-09-014` (DEP-001 contributions; revised CLM-004 relay standing and the coordination-route statement) and `DEP-09-09-015` (person's enablement; TBD-005 A13 facility and SQ-28 answer). Quotes, types, targets, SatisfactionStatus unchanged.
  - **Unchanged** (LastSeen only): the other 18 rows. **Retired:** none.
- **Guard held:** CLM-004 names DEL-09-06's relay files as "a coordination route, not an input this examination consumes". No input or prerequisite row on DEL-09-06 was written. No row names DEL-03-04. There is no DEL-09-09 → DEL-09-06 arc and no DEL-09-09 → DEL-03-04 arc.
- Declaration mirrors 0/0/0; 2 placeholders skipped. Human-owned prefix byte-identical; prior Run Notes/History retained.
- Counts: ACTIVE 24 (ANCHOR 6, EXECUTION 18: 17 UPSTREAM, 1 DOWNSTREAM), RETIRED 0.

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
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/ScopeOfWork.md` | deliverable-local input (before run) | `e887a579f75335aa91b59ae195053eabae81ce031fe91136df5c81df2297e53a` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/_REFERENCES.md` | deliverable-local input (before run) | `359be24980b063e2816abc3b6e591c559156ff36dd1f76583874aa44e48daed9` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Dependencies.csv` | deliverable-local input (before run) | `02d738c7ae0cecd809bac16f8e94d67354ac95a874bd3090ef62ed6a790ffbe2` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/_DEPENDENCIES.md` | deliverable-local input (before run) | `bd82758a315e989473ea213c946d353542dfa43e836befa4640ee8db277c57a3` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/REGISTER_CHANGES.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `89be49e53a9dcc4231fb17012d8496c5bebb2136dd5745982cf753e51cb05696` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `7daf474ba17c799740edbd42c1ba811b3cf431641277707c81834bef358478f2` |
| `projects/chirality-app-v4/execution/_DAG/DAG-001/GRAPH_BASIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `d09b49cfa4c82c7c7caf8e45d82e4ed4ec904b345e7c9b68ab3c2b3e660cb3f0` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/proposed_rows/DEL-09-09_proposed_rows.csv` | coordinator comparison only (read after extraction decisions; not an extraction input) | `aad32f380baf5353b00acd5bb2e29316753ecad5dfa50b2ddb505502b9107059` |

## Actual checks

```
SCHEMA exit 0 | VALID: /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd/projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Dependencies.csv Columns: 29 (29 required + 0 extension) Data rows: 24
ENUM invocations 21 failures []
DUP IDS []
ID invocations 44 failures []
PREFIX mismatches []
PARENT anchors 1
ACTIVE missing evidence []
EVQ-003 blank quotes [] EVQ-004 placeholder []
DECLARED rows 0 CANDIDATE status 0
placement errors []
```

Validators: `python3 tools/validation/validate_dependencies_schema.py <register>`; `python3 tools/validation/validate_enum.py <ENUM> <value>` for every distinct value of the ten enum columns; `bash tools/validation/validate_id_format.sh <TYPE> <value>` for every DEP/DEL/PKG/SOW/OBJ identifier present; inline Python assertions for quote verbatim-ness against the current SoW (whitespace-normalized), quote length <=30 words, ID uniqueness/prefix, parent-anchor count, evidence presence and target-ID placement.

## Output identities

- `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Dependencies.csv` — SHA256 `e0e3297adb7350c58694aae88062d1bb35778c4440a5e91374f3d8c7c9663bb8`
- `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/_DEPENDENCIES.md` — SHA256 `fb23e7bfb2a572298233a501f40e5cb2bf810568478874d246d012328643fc39`
- this run record (self-hash omitted).
