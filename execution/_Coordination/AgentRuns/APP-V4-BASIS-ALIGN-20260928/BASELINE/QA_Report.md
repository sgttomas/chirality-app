# QA report — pre-change baseline (node P3)

Run timestamp (UTC): 2026-09-29T02:30:11Z. Basis commit `306291bddde7862e2a4a14856e325dcf8bf5e2cd`, clean working tree.
Interpreter: Python 3.13.7 (`PYTHONDONTWRITEBYTECODE=1` for the check script).

## Method loaded

| File | sha256 | git blob @306291bdd |
|---|---|---|
| `workflows/audit-decomp/WORKFLOW.md` | `7ba6291c836973a6af0aeb81d56d60ede89466c3d006673d7ef07f09b984246b` | `142f4ce0` |
| `workflows/audit-decomp/execution.json` | `5183e34217c8d68e63456eb698531882b8c9aebdf083a2fc1a705e27f540d8d1` | `94054ce5` |
| `workflows/audit-decomp/resources/contract.md` | `704929c7c006a20a5fbe3fc903d4f172e2edb4c6a451c4b6db40506b40004e75` | `daf15ff5` |
| `workflows/audit-decomp/resources/method.md` | `51a0c69b389d0c641f88e8faa7bebbc2b3650518eede8882436853c583308827` | `4bb01b75` |
| `workflows/scope-change/WORKFLOW.md` (step 5 context) | `b5fd144603c70e977a59988cb7dfe94dd710cac28db97a19f35c437399efbca9` | `f0a2ae80` |
| `workflows/scope-change/resources/method.md` | `a3bb270b320dae36c728cad352c189c4e29fea177cdb8a1468f46e8d777b7108` | `61232ee7` |
| `workflows/scope-change/resources/contract.md` | `3e097df0fc0fe5f062d4e2e9ded86a1b84b1c7b4e692ef3510fa239ab1963e9a` | `230ef193` |

Identity: `chirality-root:bundled:workflow:audit-decomp` (Root `workflows/`, bundled source tree).

## Deterministic tools

| Tool | sha256 | Command (from `tools/evaluation/`) | Exit | Output |
|---|---|---|---|---|
| `tools/evaluation/audit_structure.py` (contract `structure-audit/v1`) | `d37ffbd040ace47ea990fd6fbb0911ea073358303a40ac32b3b7d7b111ecdb3f` | `python3 audit_structure.py --root ../../projects/chirality-app-v4/execution --variant SOFTWARE --output <BASELINE>/structure.json --inventory <BASELINE>/inventory.json` | 0 (`run_status` COMPLETE) | `structure.json` |
| imported `tools/evaluation/audit_common.py` | `c610cb5b427610a9be94d59fb8ad8c050c4955c91e69525e277957351464e8c2` | — | — | — |
| imported `tools/scope_of_work/common.py` | `61a3472216fc1c6e42730e99952670e2a02a806810cbbc67a382f4a3eb220389` | — | — | — |
| imported `tools/validation/validate_dependencies_schema.py` | `75cd74768cc8edf91c6f40b582f0fb570d2427894e6c2236ea2fe7d384291f5f` | — | — | — |
| `BASELINE/audit_checks.py` (this run's Checks 1–11 script, kept for replay) | see RUN_SUMMARY | `python3 audit_checks.py <repo> <BASELINE> PKG-01,PKG-02,PKG-03,PKG-04,PKG-05,PKG-08,PKG-09` | 0 | IssueLog, Matrix, coverage_summary.json |
| `tools/validation/validate_domain_decomposition_integrity.py` | not run | DOMAIN only; variant is SOFTWARE | — | — |

`inventory.json` lists all 41 DeliverableIDs of `Deliverables.csv`. Each folder is resolved by
`PKG-{PID}_*/{1_Working|2_Checking|3_Issued}/DEL-{ID}_*`, and each ID matched exactly one folder.

The structure tool reports 41/41 units PASS, all INITIALIZED, all `SOW_V1` and valid. Its workspace-level
`subject_status` is FAIL only because of `required tool roots are missing`: `_Aggregation`, `_Estimates` and
`_Reconciliation` are absent. This is outside the 12 checks (COV-128, INFO).

`structure.json` records absolute local paths in `root` and `units[].path`.

## Bound inputs (sha256 at 306291bdd, paths under `projects/chirality-app-v4/execution/`)

| Path | sha256 |
|---|---|
| `_Decomposition/SOFTWARE_DECOMP.md` | `5b66fefdaa54fa0046275bee40ac8f627230b3cc599f727a102e92d9f7bf4ded` |
| `_Decomposition/Companion_Inventory.csv` | `ee9d8542bcf536e4111fa09bc44fd9bc6e34eb740bbcb93107336dd572107902` |
| `_Decomposition/Packages.csv` | `b8a9b949b629fb8dbe3343e0e5a1f09a30621785d99676f71adb1b285f741fbd` |
| `_Decomposition/Deliverables.csv` | `bcdf6f2f5352e00360c19a956bd22c026909c388d77c76f92b4983ed906415eb` |
| `_Decomposition/ScopeLedger.csv` | `363643306d3bbda80f4496943a5d1de5187d7910fabdf5b89f929e6c9605fd73` |
| `_Decomposition/Objectives.csv` | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `_Decomposition/Vocabulary_Map.csv` | `af6c21872119f299516fb63b68914a0293d4f028b3bb6c93d2e26976e866d8ba` |
| `_Decomposition/Open_Issues.csv` | `77ecfea2cbe7382715bc4cefedf21e2caf4ad57d2fd5b7c6ed111eb04132aef4` |
| `_Decomposition/External_Dependencies.csv` | `055703d9a7147ab982731b783366b5fde2ef1ba805a9fe60b6c2b742182aa56e` |
| `_Decomposition/ContextBudgetQA.csv` | `837ae64f74fac345f861491196c0953a1f677684d077489cd98700553bfa0641` |
| `_Decomposition/Allocation_Rationale.csv` | `b3969e6363a4f60452410994dfa61ae6e8a08da9cafac9a746304694301f68e2` |
| `_Decomposition/Consolidated_Coverage.csv` | `df7a204581a1f95beab3a1d1bae5c715940e8fc6fe128a3ad4cfb3b81b6e5f7f` |
| `_Decomposition/Source_Coverage.csv` | `20e717cc62cd16a7dc2a8b11cccc3a2a194a64b404db6db7ddbac972d7621adc` |
| `_Decomposition/Source_Sections.csv` | `2e57c3678f484f3920f1b4777d7117615c7298bdbeebcbf4236d359654ab2045` |
| `_Decomposition/Scope_Classification.csv` | `d884ed9833572dc4e3dc7a4990edc158762ca5829810c01f5a485e8652420ed8` |
| `_Decomposition/Coverage_Telemetry.json` | `178ec20abeddfb55e558869f0b33157106f7da95b71b804fda80a302a5f2f620` |
| `_Decomposition/_LATEST.md` | `8eb0519416e80c1016cf464efb86624a42eaa94c867fe2b46ead7e5b80c9bb91` |
| `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` | `d5d873b3b918fd508685871abf177e90104b98524c5cea52944dfa2f5a695ead` |
| `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/ACCEPTED_MANIFEST.csv` | `33004257fdf2a5ff05635c4f2837bf6a27802526d801d3b0879201242de9234b` |
| `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/DECISION.md` | `14a64fe7ef67ff59568f8b0aa8d292c9ff4d66b34aa3fc1d3ea7fc21aeb23982` |
| concatenation of the 30 scoped `_CONTEXT.md` (glob order) | `dd9a38584f0ab395960a99d5772fb7db8a9fd1fab15af32c8aa0b4120e0946a6` |
| concatenation of the 30 scoped `_STATUS.md` (glob order) | `85e0300a992ed9eff6592d9d2592dcb5c6f90d1b170fb3c8520d9a9e71b3bb94` |

The sha256 of each scoped `ScopeOfWork.md` is in `coverage_summary.json` → `extensions.sow_frontmatter`. For example,
DEL-02-03 is `9a921ba5…`, which matches the C1 hash cited by IMPACT_ASSESSMENT §2. All 30 SoWs pin
`decomposition_basis …/GROUP3-20260928T001055Z@941c4d35f…`.

**Reuse test (method step 5).** The working package differs from the GROUP3 canonical copy in `SOFTWARE_DECOMP.md`,
`Open_Issues.csv` and `External_Dependencies.csv`. This confirms IMPACT_ASSESSMENT U-1: the GROUP3 final audit cannot be
reused, and this fresh baseline replaces it.

## Scan coverage, parse issues and limits

- **Registers.** Every register parsed with `csv.DictReader(strict=True)` with no errors: 262 ledger rows, 41
  deliverables, 11 packages, 10 objectives and 26 open issues. The main-document package summary table parsed 11 of 11
  rows.
- **Heading binding (partial parse, disclosed).** No semantic section binds by heading in `SOFTWARE_DECOMP.md`. The
  registers bind through `Companion_Inventory.csv` (Decision_Log D-4). The Change Register is unbound.
- **Check 6 is heuristic** (D-8).
- **Checks not run:**
  - Check 9 (DOMAIN parity) is SKIPPED because the variant is not DOMAIN.
  - Check 10 is SKIPPED because there is no `_ScopeChange/_LATEST.md`.
  - Check 12 (comparison) is not requested.
- **Not assessed:**
  - product behavior, dependency registers, the `_DAG`, and the `docs/` basis files;
  - the SoW body text beyond its frontmatter;
  - the Design drafts' content.
- **Writes.** Only to `BASELINE/`. The scratch folder is outside the repository. Git was used read-only. No network.
