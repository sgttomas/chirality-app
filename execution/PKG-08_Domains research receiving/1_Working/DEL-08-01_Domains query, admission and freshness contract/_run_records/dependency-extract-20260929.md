# DEL-08-01 dependency extraction — 2026-09-29 (DX-3)

Executor: Type 2 TASK node DX-3, a Claude Code `Agent` subagent (no delegation), run `APP-V4-BASIS-ALIGN-20260928`. Basis commit `557716cf7`. Git read-only; no network. Host filesystem permissions exceed the instruction write boundary; no narrower host enforcement is claimed. Writes: this deliverable's `Dependencies.csv`, `_DEPENDENCIES.md` and this record; the run-folder return file `DX/DX-3_DEL-08-01.md`; scratch only under the session scratchpad.

## Basis and method

Selected `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md + resources/brief.md, checks.md, tools.md, execution.json loaded in full). Brief: `BRIEFS.md` § "DX — dependency-extract UPDATE for 18 deliverables" plus the DX-3 dispatch guards. SCOPE=DEL-08-01; MODE=UPDATE; STRICTNESS=CONSERVATIVE; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md`. Design files were not read.

## Extraction result

- Pass 1: parent PKG-08; traces SOW-023, SOW-024, SOW-025, SOW-247, SOW-249, OBJ-007 re-confirmed (unchanged).
- Pass 2 against the SCA-V4-001-revised SoW (only CLM-003 revised; AX-005 added):
  - **Refreshed in place** `DEP-08-01-008` (→ DEL-05-01): Statement names the host-agent destination constraint (PRD V4-HOST-02 as revised by APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5). Quote, type, target, RequiredMaturity, SatisfactionStatus unchanged.
  - **Added:** none. **Retired:** none. **Unchanged** (LastSeen only): the other 15 rows.
- The SoW does not name DEL-03-04; the P2-deferred supplier mirror M-04-08-01 is not extracted.
- Declaration mirrors 0/0/0; 2 placeholders skipped. Human-owned prefix byte-identical; prior Run Notes/History retained.
- Counts: ACTIVE 16 (ANCHOR 7, EXECUTION 9: 6 UPSTREAM, 3 DOWNSTREAM), RETIRED 0.
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
| `projects/chirality-app-v4/execution/PKG-08_Domains research receiving/1_Working/DEL-08-01_Domains query, admission and freshness contract/ScopeOfWork.md` | deliverable-local input (before run) | `df2795869011f9364d5acf7541d66e2c32ffdd382c757153ad8d1fe8492607d7` |
| `projects/chirality-app-v4/execution/PKG-08_Domains research receiving/1_Working/DEL-08-01_Domains query, admission and freshness contract/_REFERENCES.md` | deliverable-local input (before run) | `990e199098b211182c8eef64c035a68b4af6449b6757e7b937cd16cbe0beb347` |
| `projects/chirality-app-v4/execution/PKG-08_Domains research receiving/1_Working/DEL-08-01_Domains query, admission and freshness contract/Dependencies.csv` | deliverable-local input (before run) | `99605b53b22a4c0a127316660bad70f32f6dc03ea560db4e3e2e1b81fdd94c1b` |
| `projects/chirality-app-v4/execution/PKG-08_Domains research receiving/1_Working/DEL-08-01_Domains query, admission and freshness contract/_DEPENDENCIES.md` | deliverable-local input (before run) | `9351dc2673dafa05e5feed3b34c875276a524133d1b992cebebad3215a134696` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/REGISTER_CHANGES.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `89be49e53a9dcc4231fb17012d8496c5bebb2136dd5745982cf753e51cb05696` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `7daf474ba17c799740edbd42c1ba811b3cf431641277707c81834bef358478f2` |
| `projects/chirality-app-v4/execution/_DAG/DAG-001/GRAPH_BASIS.md` | coordinator comparison only (read after extraction decisions; not an extraction input) | `d09b49cfa4c82c7c7caf8e45d82e4ed4ec904b345e7c9b68ab3c2b3e660cb3f0` |

## Actual checks

```
SCHEMA exit 0 | VALID: /Users/ryan/ai-env/projects/chirality/.claude/worktrees/test-ci-optimization-f6cacd/projects/chirality-app-v4/execution/PKG-08_Domains research receiving/1_Working/DEL-08-01_Domains query, admission and freshness contract/Dependencies.csv Columns: 29 (29 required + 0 extension) Data rows: 16
ENUM invocations 23 failures []
DUP IDS []
ID invocations 31 failures []
PREFIX mismatches []
PARENT anchors 1
ACTIVE missing evidence []
EVQ-003 blank quotes [] EVQ-004 placeholder []
DECLARED rows 0 CANDIDATE status 0
placement errors []
```

Validators: `python3 tools/validation/validate_dependencies_schema.py <register>`; `python3 tools/validation/validate_enum.py <ENUM> <value>` for every distinct value of the ten enum columns; `bash tools/validation/validate_id_format.sh <TYPE> <value>` for every DEP/DEL/PKG/SOW/OBJ identifier present; inline Python assertions for quote verbatim-ness against the current SoW (whitespace-normalized), quote length <=30 words, ID uniqueness/prefix, parent-anchor count, evidence presence and target-ID placement.

## Output identities

- `projects/chirality-app-v4/execution/PKG-08_Domains research receiving/1_Working/DEL-08-01_Domains query, admission and freshness contract/Dependencies.csv` — SHA256 `69bc284d0f71ed0d13d3c6c49e7267e447bc02f8d5e37df790eff1e2d4432a06`
- `projects/chirality-app-v4/execution/PKG-08_Domains research receiving/1_Working/DEL-08-01_Domains query, admission and freshness contract/_DEPENDENCIES.md` — SHA256 `3280f16a83f1d51cc04c38ae09ef83f6f3b819b04d455e7858b39285d6d7de7f`
- this run record (self-hash omitted).
