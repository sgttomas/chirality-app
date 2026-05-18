# BRIEF SCHEMA — four-documents

This file defines the INIT-TASK dispatch contract for `TASK + four-documents`.

## Purpose

Use this skill when ORCHESTRATOR needs the standard four-document kit (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) drafted or enriched for one PROJECT or SOFTWARE deliverable.

## Scope model

- `ScopePath` should be the target deliverable folder.
- `AllowedWriteTargets` should be limited to the four kit documents plus `_STATUS.md` when a safe state transition is expected.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this run exists | `Draft the four-document kit for DEL-014-03.` |
| `ScopePath` | path | Deliverable-local folder | `/repo/execution/PKG-014/DEL-014-03_Compressor-Controls/` |
| `TaskSkill` | string | Must equal the skill folder/name | `four-documents` |
| `AllowedWriteTargets` | list[path] | Kit-doc outputs and optional `_STATUS.md` | `[/.../Datasheet.md, /.../Specification.md, /.../Guidance.md, /.../Procedure.md, /.../_STATUS.md]` |
| `RuntimeOverrides.DELIVERABLE_PATH` | path | Deliverable folder | `/repo/.../DEL-014-03_Compressor-Controls/` |
| `RuntimeOverrides.DECOMPOSITION_REF` | path | Decomposition reference | `/repo/execution/_Decomposition/PROJECT_DECOMP.md` |
| `RuntimeOverrides.RUN_PASSES` | enum | Which passes to run | `P1_P2` |
| `ExpectedOutputs` | list[path] | Required outputs for the run | `[/.../Datasheet.md, /.../Specification.md, /.../Guidance.md, /.../Procedure.md]` |

## Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.ALLOW_OVERWRITE_STATES` | string | Safe-write state gate | `OPEN, INITIALIZED, SEMANTIC_READY` |
| `RuntimeOverrides.OBJECTIVE_ASSOCIATION_MODE` | string | Objective-association mode | `PACKAGE_HEURISTIC` |
| `RuntimeOverrides.DECOMP_VARIANT` | enum | Variant of the originating decomposition | `PROJECT` |
| `CustomInstructions` | string | Run-specific emphasis only | `Be conservative about clause-level requirements without source text.` |

## Runtime-override guidance

- `DECOMP_VARIANT=DOMAIN` is invalid for this skill.
- `RUN_PASSES=P3_ONLY` requires the four existing documents plus `_SEMANTIC_LENSING.md` to already exist.
- `AllowedWriteTargets` should not widen beyond the deliverable folder.
