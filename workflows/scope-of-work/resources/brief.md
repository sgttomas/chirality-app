# BRIEF SCHEMA — scope-of-work

## Required fields

| Field | Meaning |
|---|---|
| `PURPOSE` | One PROJECT/SOFTWARE `INIT`, `CONVERT`, or `VERIFY` operation |
| `ScopePath` | Exact deliverable folder under accepted run authority |
| `Workflow` | `scope-of-work` |
| `AllowedWriteTargets` | Exact contract/run-record targets; never legacy or underscore files |
| `RuntimeOverrides.DELIVERABLE_PATH` | Same resolved deliverable folder as `ScopePath` |
| `RuntimeOverrides.DECOMPOSITION_BASIS` | Accepted decomposition path and commit |
| `RuntimeOverrides.PROJECT_SCOPE_REFS` | Non-empty accepted project-scope references |
| `RuntimeOverrides.PACKAGE_OBJECTIVE_REFS` | Non-empty accepted package-objective references |
| `RuntimeOverrides.MODE` | `INIT`, `CONVERT`, or `VERIFY` |
| `RuntimeOverrides.FORMAT_AUTHORITY_REF` | Required only for `CONVERT`/authorized `MIGRATION_DUAL`; exact path-scoped accepted authority |
| `RuntimeOverrides.SOURCE_STATE` | Current lifecycle state; operation must be authorized for it |
| `ExpectedOutputs` | Contract or verification result; for conversion, distinct evidence candidate, clean production contract, and finalization report; applicable claim map/parity/checklist, receipt, and structured return |

The brief also supplies or authorizes grounded determination of the initial
`OUT-*`, `AC-*`, and `VER-*` definitions. Tests may implement a verification
method but may not create scope or acceptance criteria.

## Optional fields

| Field | Meaning | Default |
|---|---|---|
| `RuntimeOverrides.RENDER_HTML` | Produce an on-demand derivative | `false` |
| `RuntimeOverrides.ISSUED_PREPARATION_BINDING` | Required source commit, four source hashes, status hash, and accepted basis for `ISSUED` preparation; does not satisfy H1 | empty |
| `CustomInstructions` | Deliverable-specific emphasis within the frozen scope | none |
| `RuntimeOverrides.STATUS_POLICY` | `PRESERVE_CURRENT`, `ADVANCE_ON_PASS`, or `NO_STATUS_TOUCH`, with the meanings defined in `workflows/semantic-matrix-build/WORKFLOW.md`. `ADVANCE_ON_PASS` additionally requires the brief to authorize `_STATUS.md` writes; absent that authorization the run does not edit status and reports the ruling | `NO_STATUS_TOUCH` |
| `RuntimeOverrides.DECOMP_VARIANT` | `PROJECT` or `SOFTWARE`, matching the accepted decomposition basis; canonical enum `DECOMP_VARIANT` in `tools/validation/validate_enum.py`. `DOMAIN` is out of this workflow's scope | inferred from `DECOMPOSITION_BASIS` |
| `RuntimeOverrides.PHASE` | Project-loop phase label carried for run-record attribution only; it grants no authority and changes no tool behavior | empty |

## Write boundary

Permitted targets are limited to:

- for `INIT`, the production `ScopeOfWork.md` at `{ScopePath}/ScopeOfWork.md`;
- for `CONVERT`, an evidence-candidate `ScopeOfWork.md` in the isolated
  conversion workspace, plus a separate clean production-candidate
  `ScopeOfWork.md` and external finalization report;
- a requested untracked/on-demand `ScopeOfWork.html`; and
- run-local claim-map, parity, deterministic checklist, boundary-owner report
  (`check_boundary_owner_resolution.py --json`), receipt, and return artifacts.

The four legacy documents and `_STATUS.md` are always read-only inputs.
