# QA CHECKS — content-digest

## Minimum output validity checks

1. Exactly one digest file is written to `OUTPUT_PATH`.
2. The digest contains all seven required sections in the required order.
3. Identity fields come from `_CONTEXT.md` or are explicitly marked absent; they are not invented.
4. Dependency counts and key upstream/downstream items are derived from deliverable-local files only.
5. Quality observations are specific factual flags rather than vague judgments.
6. No file in `DELIVERABLE_PATH` is modified.
7. No file outside the specified deliverable folder is read.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- `DELIVERABLE_PATH` is missing or not a directory,
- the parent directory of `OUTPUT_PATH` does not exist.

Absent deliverable-local files should not fail the run by themselves; they should be reported as missing in the digest.
