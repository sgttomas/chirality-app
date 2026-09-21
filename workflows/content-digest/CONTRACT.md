# content-digest contract

## Brief

This file defines the INIT-TASK dispatch contract for `TASK + content-digest`.

### Purpose

Use this workflow when evaluation-protocol needs one structured digest for one deliverable folder.

### Scope model

- `ScopePath` should normally be the execution root.
- `AllowedWriteTargets` should be limited to the intended digest output path under `_Evaluation/content-digests/`.

### Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why this digest run exists | `Produce a content digest for DEL-014-03.` |
| `ScopePath` | path | Execution root | `/repo/execution/` |
| `Workflow` | string | Must equal the workflow folder/name | `content-digest` |
| `AllowedWriteTargets` | list[path] | Digest output path | `[/repo/execution/_Evaluation/content-digests/PKG-014/DEL-014-03.md]` |
| `RuntimeOverrides.DELIVERABLE_PATH` | path | Target deliverable folder | `/repo/execution/PKG-014/DEL-014-03_Compressor-Controls/` |
| `RuntimeOverrides.OUTPUT_PATH` | path | Digest output file | `/repo/execution/_Evaluation/content-digests/PKG-014/DEL-014-03.md` |
| `ExpectedOutputs` | list[path] | Expected single digest file | `[/repo/execution/_Evaluation/content-digests/PKG-014/DEL-014-03.md]` |

### Optional brief fields

This workflow currently defines no optional runtime overrides.

### Runtime-override guidance

- `DELIVERABLE_PATH` must identify exactly one deliverable folder.
- `OUTPUT_PATH` must already have an existing parent directory under `_Evaluation/content-digests/`.
- The run must remain single-deliverable and read-only on production files.

## Acceptance

### Minimum output validity checks

1. Exactly one digest file is written to `OUTPUT_PATH`.
2. The digest contains all seven required sections in the required order.
3. Identity fields come from `_CONTEXT.md` or are explicitly marked absent; they are not invented.
4. Dependency counts and key upstream/downstream items are derived from deliverable-local files only.
5. Quality observations are specific factual flags rather than vague judgments.
6. No file in `DELIVERABLE_PATH` is modified.
7. No file outside the specified deliverable folder is read.

### Failure reporting expectations

Use `FAILED_INPUTS` when:
- `DELIVERABLE_PATH` is missing or not a directory,
- the parent directory of `OUTPUT_PATH` does not exist.

Absent deliverable-local files should not fail the run by themselves; they should be reported as missing in the digest.

## Tool use

### Preferred tool order

1. Read the bounded deliverable-local files listed in the workflow contract.
2. Use direct reasoning to extract and summarize structured information into the seven-section digest.

### Allowed deterministic tools

#### Operationally invoked

None.

### Expected use of reasoning

This workflow performs bounded extraction and summarization only. It should identify specific quality-observation signals from the deliverable-local files without crossing into engineering judgment or cross-deliverable synthesis.

### Disallowed use

- No writes outside `OUTPUT_PATH`.
- No modification of any file in `DELIVERABLE_PATH`.
- No reading files outside the specified deliverable folder.
- No cross-deliverable scanning or comparison.

### Write boundary

The workflow may write exactly one file at `RuntimeOverrides.OUTPUT_PATH`.
