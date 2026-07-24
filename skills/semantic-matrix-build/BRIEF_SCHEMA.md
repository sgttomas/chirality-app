# semantic-matrix-build — Brief Schema

This skill is consumed by `TASK`. The brief must make the TASK scope, semantic scope, status policy, and expected outputs explicit.

## Required TASK fields

| Field | Requirement |
|---|---|
| `TaskSkill` | Must be `semantic-matrix-build`. |
| `ScopePath` | Absolute path to exactly one deliverable / production unit folder. This is the TASK local scope. |
| `Tasks` | Must request generation of `_SEMANTIC.md` for this one scope. |
| `ExpectedOutputs` | Must include `_SEMANTIC.md` and the TASK run record. |

## Required semantic fields

Place these in `RuntimeOverrides` unless the local TASK convention passes them top-level.

| Field | Requirement |
|---|---|
| `deliverable_folder` | Absolute path to the same folder as `ScopePath`. |
| `decomposition_path` | Absolute path to the decomposition document, used for traceability only. |
| `DECOMP_VARIANT` | `PROJECT`, `SOFTWARE`, or `DOMAIN`. |
| `STATUS_POLICY` | `PRESERVE_CURRENT`, `ADVANCE_ON_PASS`, or `NO_STATUS_TOUCH`. Default for PROJECT_SETUP Phase 2.3 is `PRESERVE_CURRENT`. |
| `PRODUCTION_FORMAT` | Resolver-selected `LEGACY_FOUR_DOC`, `SOW_V1`, or authorized `MIGRATION_DUAL`. Dual mode requires exact accepted authority and `STATUS_POLICY=NO_STATUS_TOUCH`. |

## Normal PROJECT_SETUP Phase 2.3 brief

Use `ScopePath` as the TASK run/context anchor and provide `RuntimeOverrides.deliverable_folder` as the skill-local deliverable anchor. This skill must create or overwrite `_SEMANTIC.md`, so the brief must set `ApplyEdits: true` and authorize `_SEMANTIC.md` as a writable target.

```yaml
PURPOSE: Generate deliverable-local semantic lens
RequestedBy: PROJECT_SETUP
ScopePath: /absolute/path/to/PKG-XX/.../DEL-XX-YY_Name
TaskSkill: semantic-matrix-build
Tasks:
  - Generate _SEMANTIC.md for the single deliverable folder.
  - Read the deliverable-local truth set and production documents.
  - Adopt canonical matrices A and B.
  - Derive C, F, D, K, G, X, T, E in order with full interpretation work.
  - Run semantic audit and repo validator when available.
ApplyEdits: true
AllowedWriteTargets:
  - /absolute/path/to/PKG-XX/.../DEL-XX-YY_Name/_SEMANTIC.md
RuntimeOverrides:
  deliverable_folder: /absolute/path/to/PKG-XX/.../DEL-XX-YY_Name
  decomposition_path: /absolute/path/to/execution/_Decomposition/DECOMP.md
  DECOMP_VARIANT: SOFTWARE
  STATUS_POLICY: PRESERVE_CURRENT
CustomInstructions:
  - Run as sealed PROJECT_SETUP Phase 2.3 semantic matrix generation.
  - Do not author or repair production documents.
  - Do not change _STATUS.md state; preserve the current lifecycle state by runtime policy.
  - Use compact derivation tables for C, F, D, X, and E.
  - Step 1 axis anchors and Step 2 projections must resolve to semantic phrases.
  - Insert Matrix Z before Matrix Summary.
ExpectedOutputs:
  - _SEMANTIC.md
  - _run_records/TASK_RUN_*.md
```

## Brief for status advancement on PASS

Use only when project policy says this skill owns `SEMANTIC_READY` advancement.

```yaml
ScopePath: /absolute/path/to/deliverable
TaskSkill: semantic-matrix-build
ApplyEdits: true
AllowedWriteTargets:
  - /absolute/path/to/deliverable/_SEMANTIC.md
  - /absolute/path/to/deliverable/_STATUS.md
RuntimeOverrides:
  deliverable_folder: /absolute/path/to/deliverable
  decomposition_path: /absolute/path/to/decomposition.md
  DECOMP_VARIANT: PROJECT
  STATUS_POLICY: ADVANCE_ON_PASS
CustomInstructions:
  - On audit PASS, set or verify Current State as SEMANTIC_READY and append History.
  - On audit FAIL, leave _STATUS.md state unchanged.
```

## Variant behavior

| Variant | Production documents read | Notes |
|---|---|---|
| `PROJECT` | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` | Standard four-document set. |
| `SOFTWARE` | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` | Same document set and terminology as PROJECT. |
| `PROJECT` / `SOFTWARE` with `SOW_V1` or authorized `MIGRATION_DUAL` | `ScopeOfWork.md` | Read its registered sections and IDs; dual mode remains lifecycle-neutral. |
| `DOMAIN` | All non-metadata `.md` files not prefixed with `_`, typically `Scoping.md` and `KA-*.md` | Invoke only when explicitly requested; standard PROJECT_SETUP DOMAIN setup may skip semantic lensing. |

## Recommended CustomInstructions

Use these for format-sensitive runs:

- Generate exactly one `_SEMANTIC.md` for exactly one deliverable folder.
- Keep the lens deliverable-conditioned but not deliverable-literal.
- Final matrix cells must be category-level 2–5 word phrases.
- Step 2 projections must resolve semantic phrases, not just restate formulas.
- Matrix Summary must use compact markdown tables, not bullet lists.
- Include `Matrix Z — Summary Boundary` before Matrix Summary.
- Do not claim validator PASS unless the repo validator actually ran.

## Not accepted

- Multi-deliverable scope.
- Cross-deliverable scanning or comparison.
- PROJECT_SETUP authoring `_SEMANTIC.md` inline instead of dispatching TASK.
- Missing `decomposition_path`.
- Missing `STATUS_POLICY` in an PROJECT_SETUP Phase 2.3 brief.
- A brief that asks the skill to edit production documents.
- A brief that asks for both `STATUS_POLICY=ADVANCE_ON_PASS` and omits `_STATUS.md` write authorization.
