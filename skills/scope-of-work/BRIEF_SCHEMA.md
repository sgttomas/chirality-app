# BRIEF SCHEMA — scope-of-work

## Required fields

| Field | Meaning |
|---|---|
| `PURPOSE` | One PROJECT/SOFTWARE `INIT`, `CONVERT`, or `VERIFY` operation |
| `ScopePath` | Exact deliverable folder under accepted run authority |
| `TaskSkill` | `scope-of-work` |
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

## Write boundary

Permitted targets are limited to:

- an evidence-candidate `ScopeOfWork.md` in the isolated conversion workspace;
- a separate clean production-candidate `ScopeOfWork.md` and external finalization report;
- a requested untracked/on-demand `ScopeOfWork.html`; and
- run-local claim-map, parity, deterministic checklist, receipt, and return
  artifacts.

The four legacy documents and `_STATUS.md` are always read-only inputs.
