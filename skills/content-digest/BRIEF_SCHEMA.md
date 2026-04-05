# content-digest — Brief Schema

Use this skill with a generic TASK shell (no profile) like this:

```md
PURPOSE: Create content digest for DEL-02.01
RequestedBy: EVALUATION

ScopePath: {EXECUTION_ROOT}
TaskSkill: content-digest

AllowedWriteTargets:
  - "{EXECUTION_ROOT}/_Evaluation/content-digests/"

RuntimeOverrides:
  DELIVERABLE_PATH: /abs/path/to/DEL-02.01_Pipeline-Design-Basis
  OUTPUT_PATH: "{EXECUTION_ROOT}/_Evaluation/content-digests/PKG-02/DEL-02.01.md"
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `ScopePath` | `{EXECUTION_ROOT}` | Top-level execution root |
| `TaskSkill` | `content-digest` | Must match skill folder name |
| `AllowedWriteTargets` | `["{EXECUTION_ROOT}/_Evaluation/content-digests/"]` | Exactly this path prefix |
| `RuntimeOverrides.DELIVERABLE_PATH` | Absolute path to the deliverable folder | Must contain `_CONTEXT.md` |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path to the output digest file | Parent directory must already exist |

## Optional fields

None. This skill has no optional brief fields.

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads only files within `{DELIVERABLE_PATH}`:

- `_CONTEXT.md` (full)
- `_DEPENDENCIES.md` (full)
- `_REFERENCES.md` (full)
- `Datasheet.md` (first 80 lines)
- `Specification.md` (first 80 lines)
- `Guidance.md` (first 80 lines)
- `Procedure.md` (first 80 lines)
- `_SEMANTIC.md` (first 40 lines)

It must NOT read files outside the specified deliverable folder.

## Write boundary

The skill writes only:

- `{OUTPUT_PATH}` — exactly one file per run

The parent directory of `OUTPUT_PATH` must already exist. The skill does not create the directory.

## Notes

- `DEL-ID`, `DEL Name`, and `PKG-ID` are derived at runtime from `_CONTEXT.md` or inferred from the folder name when `_CONTEXT.md` is ambiguous.
- One invocation processes one deliverable folder. EVALUATION dispatches one task per in-scope deliverable, typically batched by package for manageability.
- The brief does not include `AllowedTools` because this is a reasoning-only, semantic-matching extraction skill with no deterministic tool dependencies.
- Output files are conventionally written to `{EXECUTION_ROOT}/_Evaluation/content-digests/{PKG-ID}/{DEL-ID}.md` when dispatched by EVALUATION.
