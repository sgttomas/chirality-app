# FX return — DEL-01-03 absolute TargetLocation repair

## Node

- **Executor:** node FX, a Type 2 TASK (Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis HEAD `c147bb3abe`.
- **Authority:** DECISION-3 effect 4 and `BRIEFS.md` "FX".
- **Method:**
  - `workflows/dependency-extract` UPDATE (CONSERVATIVE), limited by the brief to a TargetLocation repair;
  - then the `project-dag` currency audit (`resources/currency.md`) against DAG-004.
- **Boundaries:** read-only git; no network.

## Outputs (SHA256)

| File | SHA256 |
|---|---|
| `PKG-01_…/DEL-01-03_…/Dependencies.csv` | `048c2b271ed21627957d1c83948129111ec90cbbc0bc488e2e21ac1301debccc` (was `8b56b4cf…dc6ad`) |
| `PKG-01_…/DEL-01-03_…/_DEPENDENCIES.md` | `4567ff65bace12914765629b431cad2db0eeb07f132f92e0d750401c0edf874e` (was `c31cbc9d…55f367`) |
| `PKG-01_…/DEL-01-03_…/_run_records/dependency-extract-20261004-fx.md` | `31489f5768f664ca58f28403ce7d71bb5f7cfbf03b14a509bd80a948d7f03a1b` |
| `_Evaluation/DAGCurrency/CURRENCY_APP_V4_DEL0103_TLFIX_2026-10-03_2016/CURRENCY_REPORT.md` | `afdf1ad3d5ca4eef90ba0ec4714c050caaca0c8e7c49bee1cb864c7536db8362` |
| `_Evaluation/DAGCurrency/CURRENCY_APP_V4_DEL0103_TLFIX_2026-10-03_2016/Tool_Run.json` (binds the 29 `Evidence/` files by hash) | `9305be4bae4430f9abfba028e1c6f8cad9e4ca4d8916510b9cf2529229b4f63a` |
| `_Evaluation/DAGCurrency/_LATEST.md` | `25b882c6e82f6623d3e1434b90e9c196a205a5258b7585c945565270289cff09` (was `29baad23…cc67a`) |

## Repair

- **Rows changed:** DEP-01-03-001…014, TargetLocation only. The worktree-root prefix was removed. Each value now begins `projects/chirality-app-v4/execution/`, the form the other 40 registers use.
- **How it was checked:**
  - a byte-level diff of the parsed cells shows exactly 14 changed cells, all TargetLocation;
  - each repaired path exists in the repository;
  - CRLF line endings were kept.
- **What was left alone:** LastSeen was not refreshed (brief: no other cell). `_DEPENDENCIES.md` gained one Run History entry only.

## Validators

- `validate_dependencies_schema.py`: exit 0, VALID (29 columns, 22 rows).
- `validate_enum.py`: 23 invocations, 23 PASS.
- `validate_id_format.sh`: 34 invocations, 34 PASS.
- One parent anchor; IDs unique.
- `validate_decomposition_registers.py --families EVQ,DRB`: exit 0; 41 registers, 929 rows, 0 ERROR, 0 WARNING.

## Currency verdict: `CURRENT_WITH_EVIDENCE_DRIFT`, 0 `DAG pending`

This is the result the DAG-004 handoff expected.

- **Manifests:**
  - DAG-004 snapshot: 37/37 OK;
  - DAG-004 source manifest: 128/130 OK, the two failures being DEL-01-03's `Dependencies.csv` and `_DEPENDENCIES.md`;
  - DAG-003, DAG-002 and DAG-001: 37/37, 37/37 and 61/61 OK.
- **Inventory:** unchanged; the pointer still names GROUP3-20260928T001055Z.
- **Scratch re-application** of SR-1…SR-7 against DAG-004:
  - 212 arcs (129 admitted, 83 candidate), with 0 added, 0 removed and 0 layer changes;
  - SCCs unchanged, and 0 representative changes;
  - the only drift is TargetLocation on the admitted representatives DEP-01-03-011 and -012;
  - the strict audit is exit 0 with 0 findings.
- **Guards** (R17-10, DEL-04-01, the guard arcs, the DEL-09-06 reach of 20 consumed by DEL-03-04 and DEL-09-07): all hold.
- **Analyzer:** `NO_DEPARTURE_FOUND` against DAG-004. Its raw stdout was byte-identical to the 2012 audit's.
- **Evidence handling:** two absolute repository-root values in the kept analyzer stdout were replaced by `<repository root>/`. The raw hash is recorded in Tool_Run.json.

## Absolute home paths elsewhere under `projects/chirality-app-v4` (reported, not fixed)

**How this was checked:**

- `git grep` for `/Users/<name>/`, `/home/<name>/` and `~/.codex` over the tracked files, as they stand in the working tree;
- each CSV hit parsed by column, and each JSON hit by key.

### Live registers: none

- **41 `Dependencies.csv`:** after the repair, none holds an absolute home path in any cell. DEL-01-03's was the only one.
- **`_Decomposition` CSV registers:** none.
- **Declared sections of `_DEPENDENCIES.md`:** none.

### Agent prose in 19 `_DEPENDENCIES.md` files

These are agent-owned Run Notes or Run History lines, not data fields: DEL-01-03, 01-06, 06-01, 06-02, 07-01, 07-02, 08-01, 08-02, 09-01, 09-02, 09-05, 09-10, 09-11, 09-12, 10-02, 10-04, 11-01, 11-02 and 11-03.

- Most give the old RUN_ROOT or DECOMPOSITION_PATH under `/Users/…/.codex/worktrees/077c/`.
- DEL-01-03's is DX's note about this defect.

### Frozen copies of the old DEL-01-03 values (data fields, accepted or snapshot history)

| Rows | Field | Where |
|---|---|---|
| DEP-01-03-011 and -012 | TargetLocation | `DependencyEdges.csv` and `Evidence/admissible_edges.csv` |
| DEP-01-03-014 | TargetLocation | `Evidence/NonTopologicalInputs.csv` |
| DEP-01-03-011…014 | TargetLocation | `Evidence/all_execution_rows.csv` |

Those four files appear in `_DAG/DAG-001…004`, in `_DAG/_Candidates/DAG-001…004` and in `RUN/DAG_PREP/DAG-004`. The same two rows also appear in `scratch_admissible_edges.csv` of the BASISALIGN, SCA002 and SCA003 currency snapshots (the SCA003 one also under `RUN/DAG_PREP/`).

### Tool-output JSON (run provenance fields)

| Field | Files |
|---|---|
| `accepted_dag.path` and `.pointer` | `analyzer.stdout.json` of 5 currency snapshots, plus the DAG_PREP copy |
| `accepted_dag.path` and `.pointer`, or `.error` | `closure_summary.json` of 3 closure snapshots, plus the DAG_PREP copy |
| `instruction_root` | `register_validation.json` of 4 closure snapshots |
| `cwd` and `arguments` | `Tool_Run.json`, `ManifestCheck_Run.json` and `NarrativeRefresh_Run.json` of DAG-001 and its candidate; `Tool_Run.json` of the ACCEPTANCE currency snapshot and of the INITIAL and TARGETS closure snapshots |
| `root`, `units[].path`, `partitions[].path` and `inventory_source` | `structure.json` in the BASELINE, POSTCHANGE and POSTACCEPT folders of runs BASIS-ALIGN, SCA002 and SCA003 |
| `[].path` | `BOUNDARY.json` and `VALIDATION.txt` of six INITIAL-SETUP task folders |
| `root` | `reference/archives/archive_digests.json` |

### Design and prototype material

- DEL-01-01: `Design/prototype/obs1…3/*_harness.py` and `Design/generated/0.158.0/_spike/generate.sh`;
- DEL-01-05: `Design/prototype/run_cases.py` and `results/RUN_2026-10-0{1,2}.txt`;
- and Design notes.

### Markdown prose

About 134 tracked `.md` files mention such paths in narrative text: run records, briefs, reviews, `conceptual/`, `reference/`, `_COORDINATION.md` and others.

### Should any be changed?

- **The frozen copies and tool outputs** are hash-bound accepted or snapshot history; changing them is outside this brief and would break their manifests.
- **The 19 Run Notes lines** could be normalized by a later `dependency-extract` run if the owner wants it.

## Not done

- No DAG, case, ScopeOfWork, `_STATUS.md`, Design or decomposition file was touched.
- No git write.
- My writes are uncommitted, for HELP_HUMAN to commit.
