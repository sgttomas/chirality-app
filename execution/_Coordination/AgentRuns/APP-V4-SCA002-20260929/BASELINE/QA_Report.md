# QA report — SCA-V4-002 pre-change baseline (node P3)

- **Run timestamp (UTC):** 2026-09-30T00:52:43Z. This is the final run into `BASELINE/`. An identical scratch run at
  2026-09-29T20:22:02Z, before the connection interruption, produced byte-identical IssueLog and Matrix.
- **Subject:** commit `f05bd1bbd4d7822deed22eeacfe89ad8d7c96fbd`. The worktree was clean apart from `BASELINE/`.
- **Interpreter:** Python 3.13.7 (`PYTHONDONTWRITEBYTECODE=1`).

## Method loaded

The identity is `chirality-root:bundled:workflow:audit-decomp`. Every file is byte-identical to the one the
APP-V4-BASIS-ALIGN BASELINE, POSTCHANGE and POSTACCEPT runs loaded:

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
| `tools/evaluation/audit_structure.py` | `d37ffbd040ace47ea990fd6fbb0911ea073358303a40ac32b3b7d7b111ecdb3f` | from `tools/evaluation/`: `python3 audit_structure.py --root ../../projects/chirality-app-v4/execution --variant SOFTWARE --output <BASELINE>/structure.json --inventory <BASELINE>/inventory.json` | 0 (`run_status` COMPLETE) | `structure.json`: 41/41 PASS, all SOW_V1; INITIALIZED 27, IN_PROGRESS 14 |
| its imports: `audit_common.py`, `tools/scope_of_work/common.py`, `tools/validation/validate_dependencies_schema.py` | `c610cb5b…`, `61a34722…`, `75cd7476…` (unchanged) | — | — | — |
| `BASELINE/audit_checks.py` | `ea6c2be722f5e1abb5abeef2844455755ba4b9588172e464678b8e09edf1d30b` | `RUN_LABEL=APP_V4_SCA_V4_002_PRECHANGE HANDOFF_PHASE=… RUN_TS=2026-09-30T00:52:43Z BASIS_COMMIT=f05bd1bbd… python3 audit_checks.py <repo> <BASELINE> PKG-01,PKG-02,PKG-03,PKG-04,PKG-05,PKG-09,PKG-10` | 0 | IssueLog, Matrix, `coverage_summary.json` |
| `tools/validation/validate_domain_decomposition_integrity.py` | not run as a tool (DOMAIN only) | only its `_latest_pointer_target` and `_pointer_matches` are imported for COV-139 | — | — |

`inventory.json` is byte-identical to the one used by the earlier runs (`e9088c41…`). It lists all 41 declared
DeliverableIDs, and each folder exists; `Deliverables.csv` is unchanged.

**Like-for-like control (scratch, not a deliverable).** Both scripts were run with the POSTACCEPT scope on a
`git archive` extract of `a0af39f8c`, the committed POSTACCEPT subject:
- POSTACCEPT's script reproduces POSTACCEPT's IssueLog (`ecaea862…`) and Matrix (`32ec176d…`) byte for byte.
- This script gives 0 differences outside `Description`, in the 11 reworded Check 9 rows (COV-119…129 there), plus
  the one appended Check 10 INFO. Its Matrix is identical.

## Bound inputs

`INPUT_MANIFEST.sha256` lists all 170 audited files with their sha256:
- the `_Decomposition/` package and its pointers;
- the four `docs/` basis files;
- `_ScopeChange/_LATEST.md`, the SCA-V4-001 snapshot and its group-3 decision folder;
- the SCA-V4-002 IMPACT_ASSESSMENT;
- `_CONTEXT.md`, `_STATUS.md`, `ScopeOfWork.md` and `Dependencies.csv` for the 32 scoped deliverables.

Key rows (paths under `projects/chirality-app-v4/execution/` unless shown):

| Path | sha256 | Note |
|---|---|---|
| `_Decomposition/SOFTWARE_DECOMP.md` | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` | = SCA-V4-001 applied poststate |
| `_Decomposition/Deliverables.csv` | `2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44` | row 14 target |
| `_Decomposition/Open_Issues.csv` | `f6b92362c4f334ffe65522557acb515d247ba67133403cc6c805f1c5c4182bf7` | row 12 target |
| `_Decomposition/Consolidated_Coverage.csv` | `4eee4bcb1cb296a9e96f9c44f934f19913dd827b43666475505e684a646a8db1` | row 11 target; 31 HOST_INTEGRATION rows |
| `_Decomposition/ScopeLedger.csv` | `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` | NO_CHANGE |
| `_Decomposition/Packages.csv` | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` | NO_CHANGE |
| `_Decomposition/Coverage_Telemetry.json` | `178ec20abeddfb55e558869f0b33157106f7da95b71b804fda80a302a5f2f620` | `STALE_REBUILD_REQUIRED` (carried) |
| `_Decomposition/_LATEST.md` | `8eb0519416e80c1016cf464efb86624a42eaa94c867fe2b46ead7e5b80c9bb91` | row 15 target |
| `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` | `d5d873b3b918fd508685871abf177e90104b98524c5cea52944dfa2f5a695ead` | row 15 target |
| `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` | `6c6854f941c714d8287bf799e1427bd4d99450847341bdf885ce4158d77eb122` | row 10 target |
| `_ScopeChange/_LATEST.md` | `a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d` | active pointer (SCA-V4-001) |

## Scan coverage, parse issues and limits

- **Registers.** All were parsed with `csv.DictReader(strict=True)` without error: 262 ledger rows, 41 deliverables,
  11 packages, 10 objectives and 26 open issues.
- **Proposed register.** The CSV block in IMPACT_ASSESSMENT §3.2 parsed as 16 rows. Every `AffectedFiles` path exists.
- **Heading binding.** The Change Register binds to `## Decision Log` at rank exact. Ledger, Objectives, Partitions
  and Production Units still get no heading hit, so they bind through `Companion_Inventory.csv` (COV-137, carried).
- **Check 9 (DOMAIN parity).** SKIPPED. Check 10 runs and passes.
- **Not assessed:**
  - product behavior;
  - the dependency registers and `_DAG` (their currency is a separate audit);
  - SoW bodies beyond the frontmatter;
  - the text of the `docs/` basis files.
- **Writes:** only `BASELINE/`. Git was read-only; the control extract went to scratch. No network.
