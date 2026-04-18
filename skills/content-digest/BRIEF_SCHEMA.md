# BRIEF SCHEMA — content-digest

This file defines the INIT-TASK dispatch contract for `TASK + content-digest`.

## Purpose

Use this skill when EVALUATION needs one structured digest for one deliverable folder.

## Scope model

- `ScopePath` should normally be the execution root.
- `AllowedWriteTargets` should be limited to the intended digest output path under `_Evaluation/content-digests/`.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this digest run exists | `Produce a content digest for DEL-014-03.` |
| `ScopePath` | path | Execution root | `/repo/execution/` |
| `TaskSkill` | string | Must equal the skill folder/name | `content-digest` |
| `AllowedWriteTargets` | list[path] | Digest output path | `[/repo/execution/_Evaluation/content-digests/PKG-014/DEL-014-03.md]` |
| `RuntimeOverrides.DELIVERABLE_PATH` | path | Target deliverable folder | `/repo/execution/PKG-014/DEL-014-03_Compressor-Controls/` |
| `RuntimeOverrides.OUTPUT_PATH` | path | Digest output file | `/repo/execution/_Evaluation/content-digests/PKG-014/DEL-014-03.md` |
| `ExpectedOutputs` | list[path] | Expected single digest file | `[/repo/execution/_Evaluation/content-digests/PKG-014/DEL-014-03.md]` |

## Optional brief fields

This skill currently defines no optional runtime overrides.

## Runtime-override guidance

- `DELIVERABLE_PATH` must identify exactly one deliverable folder.
- `OUTPUT_PATH` must already have an existing parent directory under `_Evaluation/content-digests/`.
- The run must remain single-deliverable and read-only on production files.
