# QA report — post-acceptance audit (node AK2)

- **Run timestamp (UTC):** 2026-09-29T13:35:41Z.
- **Subject:** commit `3d006a909`, plus the uncommitted SCA-V4-001
  post-acceptance edits: H-1…H-4, the finalized snapshot records and
  `_ScopeChange/_LATEST.md`.
- **Interpreter:** Python 3.13.7 (`PYTHONDONTWRITEBYTECODE=1`).

## Method loaded

The identity is `chirality-root:bundled:workflow:audit-decomp`. Every method
file is byte-identical to the one BASELINE and POSTCHANGE loaded:

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
| `tools/evaluation/audit_structure.py` | `d37ffbd040ace47ea990fd6fbb0911ea073358303a40ac32b3b7d7b111ecdb3f` | from `tools/evaluation/`: `python3 audit_structure.py --root ../../projects/chirality-app-v4/execution --variant SOFTWARE --output <POSTACCEPT>/structure.json --inventory <POSTACCEPT>/inventory.json` | 0 (`run_status` COMPLETE) | `structure.json`: 41/41 PASS, SOW_V1; INITIALIZED 27, IN_PROGRESS 14 |
| imports `audit_common.py`, `scope_of_work/common.py`, `validate_dependencies_schema.py` | unchanged (`c610cb5b…`, `61a34722…`, `75cd7476…`) | — | — | — |
| `POSTACCEPT/audit_checks.py` | `013a0d73ace71f1f30c85248781061135b6859416078a152841eeaed3ebea238` | `RUN_LABEL=APP_V4_SCA_V4_001_POSTACCEPT HANDOFF_PHASE=… RUN_TS=2026-09-29T13:35:41Z BASIS_COMMIT=… python3 audit_checks.py <repo> <POSTACCEPT> PKG-01,PKG-02,PKG-03,PKG-04,PKG-05,PKG-08,PKG-09` | 0 | IssueLog, Matrix, `coverage_summary.json` |
| `tools/validation/validate_domain_decomposition_integrity.py` | not run | DOMAIN only | — | — |

**Like-for-like.** `audit_checks.py` is `POSTCHANGE/audit_checks.py` with a
docstring note and two additions. No other check, rule or severity changed.

- **Addition (a), Check 9b.** The fixed clause "the scope-change Change
  Register … is UNRESOLVED" is emitted only while that binding is unbound.
  Once the binding resolves, the clause names it instead. Without this
  change, the fixed clause would misstate the D-15 result.
- **Addition (b), Check 10.** This is audit-decomp method Step 10, active
  when `_ScopeChange/_LATEST.md` exists. It checks that:
  - `_LATEST.md` names exactly one active `SCA-*` snapshot;
  - the folder exists;
  - the 13 required PROJECT/SOFTWARE artifacts of the scope-change contract
    "Snapshot layout" are present (the DOMAIN-only files are excluded);
  - the eight state fields in `Handoff_State.md` and `RUN_SUMMARY.md` are
    admissible and agree;
  - the closure verdict is one value, and no closure or complete-derivative
    claim coexists with a recorded stale derivative;
  - `ReadyForNextPhase` is `NOT_APPLICABLE` (SOFTWARE has no phase ladder);
  - any other `SCA-*` folder is flagged if incomplete.

  A failure is a BLOCKER, "Active snapshot contract failed", and incomplete
  residue is a WARNING, as the method specifies. Findings are appended after
  Check 11, so every earlier issue ID keeps its position.

`inventory.json` is byte-identical to BASELINE's and POSTCHANGE's
(`e9088c41…`).

**Control and negative runs (scratch, not deliverables).**
- **Control.** On a `git archive` extract of `230bf1e64`, the POSTACCEPT
  script reproduces POSTCHANGE's `Decomp_Coverage_IssueLog.csv`
  (`ed5b8e76…2893`) and `Decomp_Coverage_Matrix.csv` (`32ec176d…c500`) byte
  for byte.
- **Negative.** On the same extract with this `_LATEST.md` copied in,
  Check 10 raised 10 BLOCKERs. At that commit the snapshot had no
  `Handoff_State.md` or `RUN_SUMMARY.md`, and so no state fields or verdict.

## Bound inputs (sha256 of the audited state; paths under `projects/chirality-app-v4/execution/`)

| Path | sha256 | vs POSTCHANGE |
|---|---|---|
| `_Decomposition/SOFTWARE_DECOMP.md` | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` | changed (H-3, D-15) |
| `_Decomposition/Consolidated_Coverage.csv` | `4eee4bcb1cb296a9e96f9c44f934f19913dd827b43666475505e684a646a8db1` | recomputed (H-4) |
| `_Decomposition/ScopeLedger.csv`, `Vocabulary_Map.csv`, `Deliverables.csv`, `Packages.csv`, `Open_Issues.csv` | as in `POSTCHANGE/QA_Report.md` | unchanged |
| `_Decomposition/Coverage_Telemetry.json` | `178ec20abeddfb55e558869f0b33157106f7da95b71b804fda80a302a5f2f620` | unchanged (`STALE_REBUILD_REQUIRED`) |
| `_ScopeChange/_LATEST.md` | `a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d` | new |
| 30 scoped `ScopeOfWork.md`, `_CONTEXT.md` and `_STATUS.md` | — | unchanged |

## Scan coverage, parse issues and limits

- **Registers.** All parsed with `csv.DictReader(strict=True)` without
  error: 262 ledger rows, 41 deliverables, 11 packages, 10 objectives and
  26 open issues.
- **Heading binding.** The Change Register binds to `## Decision Log` at rank
  exact. Ledger, Objectives, Partitions and Production Units still have no
  heading hit; they bind through `Companion_Inventory.csv`, as in BASELINE.
- **Check 9 (DOMAIN parity).** SKIPPED. Check 10 now runs (PASS).
- **Not assessed:**
  - product behavior;
  - the dependency registers and `_DAG`. DAG currency is checked separately,
    in the post-acceptance record;
  - the text of the `docs/` basis files beyond the Consolidated_Coverage
    recompute;
  - SoW bodies.
- **Writes:** only `POSTACCEPT/`. Git is read-only: `git hash-object` runs
  without `-w`, and extracts go to scratch. No network.
