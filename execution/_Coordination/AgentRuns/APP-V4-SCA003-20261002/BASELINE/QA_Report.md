# QA report — SCA-V4-003 pre-change baseline (node P3)

- **Run timestamp (UTC):** 2026-10-03T02:46:41Z (the final run into `BASELINE/`). A rerun to scratch after the
  reports were written gave byte-identical IssueLog and Matrix.
- **Subject:** commit `897a107cc90e48792cf4e05b5d1313017292f290`. At the start the worktree was clean. During the
  run other actors edited three Design files (DEL-01-02, DEL-01-04, DEL-02-04) and wrote the pass-3
  `closeout/CLOSEOUT_ACCOUNT.md`, then committed them with the design-pass-3 closeout (`e510aa84f`, `bb9ab6182`) and
  a merge of `origin/main`; HEAD is now `f47ca8f6b`. `git diff --name-status 897a107cc f47ca8f6b` lists 27 files:
  those three Design files and DEL-03-04 `HOST_INTEGRATION_GUIDE.md` (GUIDE re-pin), 18 `MEMORY.md` files (5 new;
  `MEMORY.md` is a control file excluded from Check 6) and 5 pass-3 run records. No audited input changed: `INPUT_MANIFEST.sha256` passes 215/215 at `f47ca8f6b`, and the
  rerun there gave identical IssueLog and Matrix (Decision_Log D-7). `AMENDMENT_PACKET/` (P1) was empty
  throughout.
- **Interpreter:** Python 3.13.7 (`PYTHONDONTWRITEBYTECODE=1`).

## Method loaded

Identity `chirality-root:bundled:workflow:audit-decomp`, as the scope-change pre-change baseline (method step 5).
Every file is byte-identical to the one the SCA-V4-002 BASELINE, POSTCHANGE and POSTACCEPT runs loaded:

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
| `tools/evaluation/audit_structure.py` | `d37ffbd040ace47ea990fd6fbb0911ea073358303a40ac32b3b7d7b111ecdb3f` (unchanged) | from `tools/evaluation/`: `python3 audit_structure.py --root ../../projects/chirality-app-v4/execution --variant SOFTWARE --output <BASELINE>/structure.json --inventory <BASELINE>/inventory.json` | 0 (`run_status` COMPLETE) | `structure.json`: 41/41 PASS, all SOW_V1; INITIALIZED 27, IN_PROGRESS 14; workspace issue "required tool roots are missing" |
| its imports `audit_common.py`, `tools/scope_of_work/common.py`, `tools/validation/validate_dependencies_schema.py` | `c610cb5b…`, `61a34722…`, `75cd7476…` (unchanged) | — | — | — |
| `BASELINE/audit_checks.py` | `8c3bef0676f826692d82261742488dd45148fdb5bb718a9dd9c39e7b903eb0d3` | `RUN_LABEL=APP_V4_SCA_V4_003_PRECHANGE HANDOFF_PHASE=… RUN_TS=2026-10-03T02:46:41Z BASIS_COMMIT=897a107cc… python3 audit_checks.py <repo> <BASELINE> PKG-01,PKG-02,PKG-03,PKG-04,PKG-05,PKG-09,PKG-10` | 0 | IssueLog, Matrix, `coverage_summary.json` |
| `tools/validation/validate_domain_decomposition_integrity.py` | `cb5b1077a4ce0bf60ea700b50688b10119379f21cb8ae94a47e6bfc16c4124fc` (no commit since POSTACCEPT) | not run as a tool (DOMAIN only); `_latest_pointer_target` and `_pointer_matches` imported for the registered-parser check | — | target `SCA-V4-002_2026-09-29_1901`, match True |

`inventory.json` is byte-identical to POSTACCEPT's (`e9088c41…`): all 41 declared DeliverableIDs, each folder present;
`Deliverables.csv` is unchanged.

`audit_checks.py` is POSTACCEPT's script (`86c2b41f…05e0`) with changes (h), (i), (j), (e2) and (k), described in
its docstring and Decision_Log D-5.

## Controls (scratch under `$TMPDIR/P3-SCA003/`, not deliverables)

1. **Reproduction.** `git archive af918ee50` (the committed POSTACCEPT subject) → `audit_structure.py` →
   POSTACCEPT's `audit_checks.py`, same scope: IssueLog and Matrix byte-identical to POSTACCEPT's (0 / 38 / 100).
2. **Like for like on the current state.** POSTACCEPT's script on the subject: 0 / 35 / 94; Matrix identical to
   this run's. Its IssueLog differs from this run's only by the COV-127 row that change (h) suppresses and the five
   Check 9 descriptions that change (i) rewords.
3. **Stability.** This script rerun after the reports were written, at HEAD `f47ca8f6b`: IssueLog and Matrix
   identical; `audit_structure.py` rerun gives the same `structure.json` content.

## Bound inputs

`INPUT_MANIFEST.sha256` lists 215 files with sha256; `shasum -a 256 -c` from the repository root passes 215/215.
It covers the `_Decomposition/` package, its three checkpoint pointers and GROUP3's 16 canonical files; the four
`docs/` basis files; `_ScopeChange/_LATEST.md`; the SCA-V4-001 and SCA-V4-002 snapshots (13 each) and group-3
folders (3 each); the SCA-V4-002 post-acceptance checks and effective-state record; `_DAG/_LATEST.md` and DAG-003's
two manifests; the SCA-V4-003 proposal records and run brief; and `_CONTEXT.md`, `_STATUS.md`, `ScopeOfWork.md`
and `Dependencies.csv` for the 32 scoped deliverables.

Key rows (paths under `projects/chirality-app-v4/execution/` unless shown):

| Path | sha256 | Note |
|---|---|---|
| `_Decomposition/SOFTWARE_DECOMP.md` | `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5` | = SCA-V4-002 applied (H-1) |
| `_Decomposition/Deliverables.csv` | `552df0609e7c5b4d0837b8571224fe20885a7252f99444dca2266701889f6bf3` | |
| `_Decomposition/Open_Issues.csv` | `a11782181531ce77e564b774787537d3e11cc1d4304123cba0d83f539bb280f0` | possible SCA-V4-003 target (OI-009, OI-018) |
| `_Decomposition/Consolidated_Coverage.csv` | `366773650b588dc995f396be02d7e2690d9738c8d22afb98a85260dfb87313ea` | 31 HOST_INTEGRATION rows |
| `_Decomposition/ScopeLedger.csv` | `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` | |
| `_Decomposition/Packages.csv` | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` | |
| `_Decomposition/Objectives.csv` | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` | |
| `_Decomposition/Coverage_Telemetry.json` | `178ec20abeddfb55e558869f0b33157106f7da95b71b804fda80a302a5f2f620` | `STALE_REBUILD_REQUIRED` (owner-deferred) |
| `_Decomposition/_LATEST.md` | `b1b8410b074b528536114485bc2a8e54b3b070849bb6d44f17eecde6f6c7ccc3` | `Latest: (none)` with the B-06b reading line |
| `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` | `6ef9c0ba66ee42f6b786540aa3f26b1104a6fd82c4623d00f28d564d493afabb` | B-06a applied |
| `_ScopeChange/_LATEST.md` | `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1` | active SCA-V4-002, §11.2 form |
| `_DAG/_LATEST.md` | `4d381ba4e87b41a83b9d0d2dc591c4bf04eacb84df0b5c27314091cd2a992f56` | `Latest: DAG-003` |
| `_DAG/DAG-003/SOURCE_MANIFEST.sha256` | `d0fc611d95ee80ba64b86ea5b0eaa1a1ba90e85e461fb18459dd8162df6a40c5` | 130/130 pass at the subject; `MANIFEST.sha256` 37/37 |
| `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` | unchanged since SCA-V4-002 |

## Scan coverage, parse issues and limits

- **Registers.** All parsed with `csv.DictReader(strict=True)` without error: 262 ledger rows, 41 deliverables,
  11 packages, 10 objectives, 26 open issues (23 OPEN).
- **Proposal records.** The five C1 records' per-deliverable headings and F0_JOINS §3 parsed into 20 target
  deliverables; each exists in `Deliverables.csv`. The 20 `ScopeOfWork.md` and 20 `Dependencies.csv` hash prefixes
  the records cite match the current bytes; one `_STATUS.md` prefix in pass-3 C1-A (DEL-01-04) is mistyped in its
  16th hex digit (report finding 1).
- **Heading binding.** The Change Register binds to `## Decision Log` at rank exact; Ledger, Objectives, Partitions
  and Production Units bind through `Companion_Inventory.csv` only (COV-127, carried).
- **Check 9 (DOMAIN parity).** SKIPPED. Check 10 runs and passes.
- **Check 6** reads file names, not contents; the matched names are in `extensions.artifact_matches`.
- **Not assessed:** product behavior; Design-file content; dependency-register content and DAG currency beyond the
  manifest checks (a separate `project-dag` audit); SoW bodies beyond the frontmatter; the text of the `docs/` basis
  files.
- **Writes:** only `BASELINE/`, plus scratch under `$TMPDIR/P3-SCA003/`. Git read-only (`log`, `diff`, `status`,
  `ls-files`, `archive` to scratch). No network; no Codex or model runs.
