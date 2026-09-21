# equipment-extract contract

## Brief

Use this workflow with a generic TASK shell (no profile) like this:

```md
PURPOSE: Extract equipment items from KTY-04-01 KA files
RequestedBy: WORKING_ITEMS
ParentWorkflow: project-setup
ScopePath: {EXECUTION_ROOT}
Workflow: equipment-extract

AllowedWriteTargets:
  - "{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/"

RuntimeOverrides:
  KTY_PATH: /abs/path/to/KTY-04-01_Gas_Dehydration
  OUTPUT_ROOT: "{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/"
```

### Required fields

| Field | Value | Notes |
|---|---|---|
| `ScopePath` | `{EXECUTION_ROOT}` | Top-level execution root |
| `Workflow` | `equipment-extract` | Must match workflow folder name |
| `AllowedWriteTargets` | `["{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/"]` | Exactly this path |
| `RuntimeOverrides.KTY_PATH` | Absolute path to the KTY folder | Must contain `KA-*.md` files |
| `RuntimeOverrides.OUTPUT_ROOT` | `{EXECUTION_ROOT}/_Aggregation/Equipment_Extract/` | Must already exist |

### Optional fields

None. This workflow has no optional brief fields.

### Read boundary

The workflow reads only:

- `{KTY_PATH}/KA-*.md`
- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_REFERENCES.md`

It must NOT read arbitrary files under `ScopePath`.

### Write boundary

The workflow writes only:

- `{OUTPUT_ROOT}/{KTY_ID}_Equipment_Extract.md`

`OUTPUT_ROOT` must already exist. The workflow does not create the directory.

### Notes

- `KTY_ID` is derived at runtime from `_CONTEXT.md` or from the folder name when `_CONTEXT.md` is unavailable.
- One invocation processes one KTY folder. project-setup spawns one task per in-scope KTY for parallelism.
- The brief does not include `AllowedTools` because this is a reasoning-only extraction workflow with no deterministic tool dependencies.

## Acceptance

Minimum checks for a valid run:

1. `KTY_PATH` exists and contains at least one `KA-*.md` file (or absence is reported as `FAILED_INPUTS`).
2. `OUTPUT_ROOT` exists before the workflow writes to it.
3. Every `KA-*.md` file in the KTY folder was read, or its absence was explicitly reported.
4. The output file `{KTY_ID}_Equipment_Extract.md` was written to `OUTPUT_ROOT`.
5. The output file contains all required sections: title, metadata block, Equipment Table, Package Notes, equipment count footer.
6. No files in `{KTY_PATH}` were written or modified.

### Source traceability (required for every extracted item)

Every row in the Equipment Table must satisfy all of the following:

| Check | Requirement |
|---|---|
| KA source cited | The `KA Source` column names the specific `KA-*.md` file from which the item was extracted |
| Equipment exists in source | The equipment item appears in the cited KA file text; no invented items |
| Tag is verbatim | The `Equipment Tag` value is an exact match from the source text, or `No tag` when the source does not state one |
| Package assignment sourced | `Package Name` is a formal name from the source, a contextual name with `(indicated)` suffix, or `N/A` |

A run with even one untraceable equipment row is invalid.

### Null-result validation

KTYs with zero physical equipment must still produce an output file containing:

- An empty Equipment Table (or single explanatory row)
- Package Notes explaining why no equipment was found
- An equipment count footer reading `0` with parenthetical explanation

### Reporting groups

When issues are found during extraction, group them by:

- missing KA files (listed in folder but not on disk, or vice versa)
- ambiguous tags (tag partially stated or conflicting across KAs)
- scope boundary items (equipment where ownership is unclear)
- TBD items (equipment referenced as future or placeholder)
- package assignment uncertainty (formal vs. indicated vs. absent)

### Success case

A clean run reports:

- `RUN_STATUS=OK`
- Output file path
- Equipment count (integer)
- List of KA files read
- No warnings (or explicit statement that none were encountered)

## Tool use

### Preferred tool order

Reasoning-first: this workflow is LLM-driven; no deterministic tool ordering applies. The agent reads KA markdown files within a single Knowledge Type folder and applies extraction logic directly, producing a normalized, source-traceable equipment register.

### Allowed deterministic tools

#### Operationally invoked

- None — no operational helpers declared (WORKFLOW.md states: "No deterministic tools. This is a reasoning-first extraction workflow")

### Expected use of reasoning

This is a reasoning-first extraction workflow. The agent reads `_CONTEXT.md`, `_REFERENCES.md`, and all `KA-*.md` files in the KTY folder, then applies extraction logic directly to identify discrete physical equipment items per the in-scope / out-of-scope rules, records the required fields (Equipment Tag, Equipment Name, Package Name, Notes, KA Source), assembles the ordered equipment table, writes Package Notes, and produces the final per-KTY extract file. Reasoning governs every phase: preconditions, KTY context read, KA enumeration and ordering, per-KA equipment extraction, table assembly, Package Notes, and output file composition.

### Disallowed use

- No writing outside `OUTPUT_ROOT`.
- No modification of any file in `KTY_PATH`.
- No widening scope beyond the designated KTY folder.
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

### Write boundary

Writes are limited to:

- `{RuntimeOverrides.OUTPUT_ROOT}/{KTY_ID}_Equipment_Extract.md`

`OUTPUT_ROOT` must already exist. The workflow does not create the directory. No files in `{KTY_PATH}` may be written or modified.
