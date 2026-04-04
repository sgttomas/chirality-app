# equipment-extract — Brief Schema

Use this skill with a generic TASK shell (no profile) like this:

```md
PURPOSE: Extract equipment items from KTY-04-01 KA files
RequestedBy: ORCHESTRATOR

ScopePath: {EXECUTION_ROOT}
TaskSkill: equipment-extract

AllowedWriteTargets:
  - "{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/"

RuntimeOverrides:
  KTY_PATH: /abs/path/to/KTY-04-01_Gas_Dehydration
  OUTPUT_ROOT: "{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/"
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `ScopePath` | `{EXECUTION_ROOT}` | Top-level execution root |
| `TaskSkill` | `equipment-extract` | Must match skill folder name |
| `AllowedWriteTargets` | `["{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/"]` | Exactly this path |
| `RuntimeOverrides.KTY_PATH` | Absolute path to the KTY folder | Must contain `KA-*.md` files |
| `RuntimeOverrides.OUTPUT_ROOT` | `{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/` | Must already exist |

## Optional fields

None. This skill has no optional brief fields.

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads only:

- `{KTY_PATH}/KA-*.md`
- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_REFERENCES.md`

It must NOT read arbitrary files under `ScopePath`.

## Write boundary

The skill writes only:

- `{OUTPUT_ROOT}/{KTY_ID}_Equipment_Extract.md`

`OUTPUT_ROOT` must already exist. The skill does not create the directory.

## Notes

- `KTY_ID` is derived at runtime from `_CONTEXT.md` or from the folder name when `_CONTEXT.md` is unavailable.
- One invocation processes one KTY folder. ORCHESTRATOR spawns one task per in-scope KTY for parallelism.
- The brief does not include `AllowedTools` because this is a reasoning-only extraction skill with no deterministic tool dependencies.
