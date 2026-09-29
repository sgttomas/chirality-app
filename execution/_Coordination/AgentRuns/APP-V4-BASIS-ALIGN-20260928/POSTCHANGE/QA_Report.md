# QA report — post-change audit (node AK1)

Run timestamp (UTC): 2026-09-29T04:02:46Z. Subject: commit `f4ba34c2c` plus the uncommitted SCA-V4-001 candidate
edits. Interpreter: Python 3.13.7 (`PYTHONDONTWRITEBYTECODE=1`).

## Method loaded

Identity `chirality-root:bundled:workflow:audit-decomp`. Every method file is byte-identical to the one BASELINE
loaded (`BASELINE/QA_Report.md`):

| File | sha256 |
|---|---|
| `workflows/audit-decomp/WORKFLOW.md` | `7ba6291c836973a6af0aeb81d56d60ede89466c3d006673d7ef07f09b984246b` |
| `workflows/audit-decomp/execution.json` | `5183e34217c8d68e63456eb698531882b8c9aebdf083a2fc1a705e27f540d8d1` |
| `workflows/audit-decomp/resources/contract.md` | `704929c7c006a20a5fbe3fc903d4f172e2edb4c6a451c4b6db40506b40004e75` |
| `workflows/audit-decomp/resources/method.md` | `51a0c69b389d0c641f88e8faa7bebbc2b3650518eede8882436853c583308827` |
| `workflows/scope-change/WORKFLOW.md` | `b5fd144603c70e977a59988cb7dfe94dd710cac28db97a19f35c437399efbca9` |
| `workflows/scope-change/resources/contract.md` | `3e097df0fc0fe5f062d4e2e9ded86a1b84b1c7b4e692ef3510fa239ab1963e9a` |
| `workflows/scope-change/resources/method.md` | `a3bb270b320dae36c728cad352c189c4e29fea177cdb8a1468f46e8d777b7108` |

## Deterministic tools

| Tool | sha256 | Command | Exit | Output |
|---|---|---|---|---|
| `tools/evaluation/audit_structure.py` | `d37ffbd040ace47ea990fd6fbb0911ea073358303a40ac32b3b7d7b111ecdb3f` | from `tools/evaluation/`: `python3 audit_structure.py --root ../../projects/chirality-app-v4/execution --variant SOFTWARE --output <POSTCHANGE>/structure.json --inventory <POSTCHANGE>/inventory.json` | 0 (`run_status` COMPLETE) | `structure.json`: 41/41 PASS, SOW_V1; INITIALIZED 27, IN_PROGRESS 14 |
| imports `audit_common.py`, `scope_of_work/common.py`, `validate_dependencies_schema.py` | unchanged from BASELINE (`c610cb5b…`, `61a34722…`, `75cd7476…`) | — | — | — |
| `POSTCHANGE/audit_checks.py` | `8dedc11daea28662ec2cec5a90b445b02307b7057b91eeea2e042829a5efe04e` | `RUN_LABEL=… HANDOFF_PHASE=… RUN_TS=… BASIS_COMMIT=… python3 audit_checks.py <repo> <POSTCHANGE> PKG-01,PKG-02,PKG-03,PKG-04,PKG-05,PKG-08,PKG-09` | 0 | IssueLog, Matrix, `coverage_summary.json` |
| `POSTCHANGE/projections.py` | `83f767308047be682f32ee3334355bd6e50c75ecbc0639877b31a8aff7e88f13` | `python3 projections.py <repo> <POSTCHANGE>` (read-only) | 0 | `projections.json` |
| `tools/validation/validate_domain_decomposition_integrity.py` | not run | DOMAIN only | — | — |

**Like-for-like.** `audit_checks.py` is `BASELINE/audit_checks.py` with exactly two lines changed: `run_label` and
`expected_handoff_phase` are read from the environment. Every check, rule and severity is the same.
`inventory.json` is byte-identical to BASELINE's (`e9088c41…`).

**Control run (scratch, not a deliverable).** The same script and structure tool were run on the pre-application tree at
`f4ba34c2c`, before any SCA-V4-001 edit (0 BLOCKER, 39 WARNING, 89 INFO). It separates the basis drift
`306291bdd` → `f4ba34c2c` (DECISION-6 lifecycle) from the amendment's effects (`COMPARISON.md`).

## Bound inputs (sha256 of the audited candidate; paths under `projects/chirality-app-v4/execution/`)

| Path | sha256 | vs BASELINE |
|---|---|---|
| `_Decomposition/SOFTWARE_DECOMP.md` | `98e8bc4b17707a3eb395bf63ff73e89f6c802566d6e11c9f0278d26bf26d1940` | changed (D-16) |
| `_Decomposition/ScopeLedger.csv` | `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` | changed (D-01…D-08) |
| `_Decomposition/Vocabulary_Map.csv` | `863ccc77d5988753d47d56e5b0b5fe59e5b165d336c3f2125da2b1548b4d2f5c` | changed (D-09) |
| `_Decomposition/Deliverables.csv` | `2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44` | changed (D-10…D-12) |
| `_Decomposition/Packages.csv` | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` | changed (D-13) |
| `_Decomposition/Open_Issues.csv` | `f6b92362c4f334ffe65522557acb515d247ba67133403cc6c805f1c5c4182bf7` | changed (D-14a/b) |
| `_Decomposition/Consolidated_Coverage.csv` | `a988f5a603429e785a19e1f8f5d98418d3a715acc3b4bbd13d6d8746b72d174f` | recomputed (B8) |
| `_Decomposition/Coverage_Telemetry.json` | `178ec20abeddfb55e558869f0b33157106f7da95b71b804fda80a302a5f2f620` | unchanged |
| `_Decomposition/Companion_Inventory.csv`, `Objectives.csv`, `External_Dependencies.csv`, `ContextBudgetQA.csv`, `Allocation_Rationale.csv`, `Source_Coverage.csv`, `Source_Sections.csv`, `Scope_Classification.csv`, `_LATEST.md`, `checkpoint_snapshots/*` | as in `BASELINE/QA_Report.md` | unchanged |
| 30 scoped `ScopeOfWork.md` | `coverage_summary.json` → `extensions.sow_frontmatter` | unchanged (all 30 hashes identical to BASELINE) |
| 30 scoped `_CONTEXT.md` | — | 4 changed (DEL-02-03, 05-01, 05-02, 09-07; B7) |
| 30 scoped `_STATUS.md` | — | 14 changed since BASELINE (IN_PROGRESS, DECISION-6, commit `67a2fac4b`) |

## Scan coverage, parse issues and limits

- Registers parsed with `csv.DictReader(strict=True)` without error: 262 ledger rows, 41 deliverables, 11 packages,
  10 objectives, 26 open issues. The main-document package summary table parsed 11/11 rows.
- Heading binding: as in BASELINE, no semantic section binds by heading in `SOFTWARE_DECOMP.md`; the Change Register
  remains unbound because D-15 (the `## Decision Log` section) is acceptance-conditional and not yet applied.
  `projections.json` shows it binds at rank "exact" once D-15 is applied.
- Checks 9 (DOMAIN parity) and 10 (no `_ScopeChange/_LATEST.md`) are SKIPPED, as in BASELINE. The candidate
  `_ScopeChange/` folder now exists but has no `_LATEST.md` (FIRST_AMENDMENT posture).
- Not assessed: product behavior, the dependency registers and `_DAG` (DAG currency is checked separately,
  `DAG_CURRENCY.txt`), the text of the `docs/` basis files beyond the Consolidated_Coverage recompute, SoW bodies.
- Writes: only `POSTCHANGE/`. Git read-only (`git hash-object` without `-w` in the B8 recompute). No network.
