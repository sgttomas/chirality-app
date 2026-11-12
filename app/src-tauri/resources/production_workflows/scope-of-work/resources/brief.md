# BRIEF SCHEMA — scope-of-work

## Required fields

| Field | Meaning |
|---|---|
| `PURPOSE` | One PROJECT/SOFTWARE `INIT`, `CONVERT`, `REVISE`, or `VERIFY` operation |
| `ScopePath` | Exact deliverable folder under accepted run authority |
| `Workflow` | `scope-of-work` |
| `AllowedWriteTargets` | Exact contract targets; never legacy or underscore files |
| `RuntimeOverrides.DELIVERABLE_PATH` | Same resolved deliverable folder as `ScopePath` |
| `RuntimeOverrides.DECOMPOSITION_BASIS` | Accepted decomposition path |
| `RuntimeOverrides.PROJECT_SCOPE_REFS` | Non-empty accepted project-scope references |
| `RuntimeOverrides.PACKAGE_OBJECTIVE_REFS` | Non-empty accepted package-objective references |
| `RuntimeOverrides.MODE` | `INIT`, `CONVERT`, `REVISE`, or `VERIFY` |
| `RuntimeOverrides.FORMAT_AUTHORITY_REF` | Required only for `CONVERT`/authorized `MIGRATION_DUAL`; exact path-scoped accepted authority |
| `RuntimeOverrides.SOURCE_STATE` | Actual lifecycle state only where the project adopts one. Current `INIT`/`VERIFY`/`REVISE` may state `not used`; do not create a status file. `REVISE` under an explicitly adopted legacy lifecycle accepts only `INITIALIZED`, `SEMANTIC_READY` or `IN_PROGRESS` |
| `RuntimeOverrides.AMENDMENT_REF` | Required only for `REVISE`: the amendment ID, the exact accepted amendment/review basis (checkpoint group 3 accepted), accepted actions naming this deliverable with `MODIFY` or `RECLASSIFY`, and their source revision/content binding; snapshot path and register hash where the selected route uses them |
| `RuntimeOverrides.REVISION_SCOPE` | Required only for `REVISE`: the contract parts (sections, IDs, matrix rows, frontmatter references) the amendment changes |
| `RuntimeOverrides.PRIOR_CONTRACT_SHA256` | Required only for `REVISE`: hash of the `ScopeOfWork.md` being revised |
| `ExpectedOutputs` | Contract or verification result, applicable checks and findings through the normal return; conversion additionally needs its distinct evidence candidate, clean production contract and mapping/parity/finalization evidence. No routine receipt for current INIT/VERIFY/REVISE |

The brief identifies the selected current-project or adopted legacy profile and
the governing project instructions; do not infer that choice from file presence.

The brief also supplies or authorizes grounded determination of the initial
`OUT-*`, `AC-*`, and `VER-*` definitions. Tests may implement a verification
method but may not create scope or acceptance criteria.

## Optional fields

| Field | Meaning | Default |
|---|---|---|
| `RuntimeOverrides.RENDER_HTML` | Produce an on-demand derivative | `false` |
| `RuntimeOverrides.ISSUED_PREPARATION_BINDING` | Required source commit, four source hashes, status hash, and accepted basis for `ISSUED` preparation; does not satisfy H1 | empty |
| `CustomInstructions` | Deliverable-specific emphasis within the frozen scope | none |
| `RuntimeOverrides.STATUS_POLICY` | `PRESERVE_CURRENT` or `NO_STATUS_TOUCH`: existing status bytes remain unchanged and absent status remains absent. `REVISE` uses `NO_STATUS_TOUCH`. Any separately authorized status act belongs to its actual actor outside this workflow | `NO_STATUS_TOUCH` |
| `RuntimeOverrides.DECOMP_VARIANT` | `PROJECT` or `SOFTWARE`, matching the accepted decomposition basis; canonical enum `DECOMP_VARIANT` in `tools/validation/validate_enum.py`. `DOMAIN` is out of this workflow's scope | inferred from `DECOMPOSITION_BASIS` |
| `RuntimeOverrides.PHASE` | Project-loop phase label carried for attribution only; it grants no authority and changes no tool behavior | empty |

## Write boundary

Permitted targets are limited to:

- for `INIT`, the production `ScopeOfWork.md` at `{ScopePath}/ScopeOfWork.md`;
- for `REVISE`, the existing production `{ScopePath}/ScopeOfWork.md`, changed
  only within `REVISION_SCOPE`;
- for `CONVERT`, an evidence-candidate `ScopeOfWork.md` in the isolated
  conversion workspace, plus a separate clean production-candidate
  `ScopeOfWork.md` and external finalization report;
- a requested untracked/on-demand `ScopeOfWork.html`; and
- applicable claim-map, parity, deterministic checklist and boundary-owner report
  (`check_boundary_owner_resolution.py --json`) outputs for an actual review or
  conversion need. A retained receipt is written only for an explicitly adopted
  requirement; current INIT/VERIFY/REVISE return through the host without a routine file.

The four legacy documents and `_STATUS.md` are always read-only inputs.

A `REVISE` brief names `MODE=VERIFY` as its closing step. The dispatcher may
run that verification as a separate brief; the revision is not complete until
it passes.
