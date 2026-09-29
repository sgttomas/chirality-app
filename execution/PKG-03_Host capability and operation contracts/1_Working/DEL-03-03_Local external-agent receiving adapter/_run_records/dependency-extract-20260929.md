# DEL-03-03 dependency extraction — 2026-09-29 (DX-3)

Executor: Type 2 TASK node DX-3, a Claude Code `Agent` subagent (no delegation), run `APP-V4-BASIS-ALIGN-20260928`. Basis commit `557716cf7`. Git read-only; no network. Host filesystem permissions exceed the instruction write boundary; no narrower host enforcement is claimed. Writes: this deliverable's `Dependencies.csv`, `_DEPENDENCIES.md` and this record; the run-folder return file `DX/DX-3_DEL-03-03.md`; scratch only under the session scratchpad.

## Basis and method

Selected `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md + resources/brief.md, checks.md, tools.md, execution.json loaded in full). Brief: `BRIEFS.md` § "DX — dependency-extract UPDATE for 18 deliverables" plus the DX-3 dispatch guards. SCOPE=DEL-03-03; MODE=UPDATE; STRICTNESS=CONSERVATIVE; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`. Design files were not read.

## Extraction result

- Pass 1: parent anchor PKG-03 and traces SOW-148, SOW-183, SOW-184, OBJ-004 re-confirmed from the unchanged frontmatter and scope table; labels unchanged (none of these IDs was amended by SCA-V4-001).
- Pass 2 against the SCA-V4-001-revised SoW:
  - **Added** `DEP-03-03-013` EXECUTION UPSTREAM INTERFACE → DEL-01-01 (CLM-002: "App `DEL-01-01`'s supplier MCP/dynamic-tool surfaces and channel-status facts at the definition pin 0.158.0"). Arc DEL-03-03 → DEL-01-01.
  - **Added** `DEP-03-03-014` EXECUTION UPSTREAM INTERFACE → DEL-02-03 (CLM-002: checkpoint statement for the current phase; governance-phase hold machine, hold-support values, required-tool check; REQ-003). Arc DEL-03-03 → DEL-02-03.
  - **Refreshed in place** `DEP-03-03-008` (→ DEL-04-01): Statement, SourceRef, Notes for revised TBD-001/TBD-002. Quote, type, direction, RequiredMaturity=TBD, SatisfactionStatus=PENDING unchanged.
  - **Unchanged** (LastSeen only): 001–007, 009–012. **Retired:** none.
- Not written: DEL-04-03 (N-B8, withheld; SoW names no DEL-04-03 input), DEL-09-06 (K-11; not named), supplier-side mirrors and DEL-04-02/DEL-02-01 consumer rows (no SoW ground). Applied owner decisions (DECISION-2 D5; SWBPIPE-INTAKE DECISION-4/-5) yield no rows.
- Declaration mirrors 0/0/0; 2 placeholders skipped. Human-owned prefix of `_DEPENDENCIES.md` SHA256 `cbe608187bbdd8dc594f2ba713142932349ff5297dd3190fcc8b98547de02330` before and after (byte-identical); prior Run Notes and Run History retained verbatim.
- Counts: ACTIVE 14 (ANCHOR 5, EXECUTION 9: 8 UPSTREAM, 1 DOWNSTREAM), RETIRED 0.
- Guards: none triggered for this deliverable.

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
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/ScopeOfWork.md` | deliverable-local input (before run) | `fdd22e25a0a43c55d31ca38f3fcb44931af8ebee6d34da62ff1f214013fb2881` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/_REFERENCES.md` | deliverable-local input (before run) | `2ba400b208c1ad0276eac4046ec5f2b3b48d0abaec4becbca46e2b51a6a79402` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Dependencies.csv` | deliverable-local input (before run) | `a962d4d5007fd037b07a8e65bce42957d995a8e34bc3f17581d0eda3748067cf` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/_DEPENDENCIES.md` | deliverable-local input (before run) | `95efc22df551f741c558167811842c03437990c6f214b5561eadce61a425e2f0` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/REGISTER_CHANGES.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `89be49e53a9dcc4231fb17012d8496c5bebb2136dd5745982cf753e51cb05696` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `7daf474ba17c799740edbd42c1ba811b3cf431641277707c81834bef358478f2` |
| `projects/chirality-app-v4/execution/_DAG/DAG-001/GRAPH_BASIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `d09b49cfa4c82c7c7caf8e45d82e4ed4ec904b345e7c9b68ab3c2b3e660cb3f0` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/proposed_rows/DEL-03-03_proposed_rows.csv` | coordinator comparison only (read after extraction decisions; not an extraction input) | `24762c2b82ad1bd7d9e8452af6227daae78238d9e1c456ed98ff4c3e1b767287` |

## Actual checks

```
SCHEMA exit 0 | VALID: /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd/projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Dependencies.csv Columns: 29 (29 required + 0 extension) Data rows: 14
ENUM invocations 21 failures []
DUP IDS []
ID invocations 30 failures []
PREFIX mismatches []
PARENT anchors 1
ACTIVE missing evidence []
EVQ-003 blank quotes [] EVQ-004 placeholder []
DECLARED rows 0 CANDIDATE status 0
placement errors []
```

Validators: `python3 tools/validation/validate_dependencies_schema.py <register>`; `python3 tools/validation/validate_enum.py <ENUM> <value>` for every distinct value of the ten enum columns; `bash tools/validation/validate_id_format.sh <TYPE> <value>` for every DEP/DEL/PKG/SOW/OBJ identifier present; inline Python assertions for quote verbatim-ness against the current SoW (whitespace-normalized), quote length <=30 words, ID uniqueness/prefix, parent-anchor count, evidence presence and target-ID placement.

## Output identities

- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Dependencies.csv` — SHA256 `006a3abdfcbf68056d64ce670d68b3bc9ee2a36b905629fcc9d27167f8fce87e`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/_DEPENDENCIES.md` — SHA256 `8ebee300ee80f97d5c09127c900246ae249b2ae52b2fff125b11d2562c98c484`
- this run record (self-hash omitted).
