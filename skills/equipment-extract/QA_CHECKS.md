# equipment-extract — QA Checks

Minimum checks for a valid run:

1. `KTY_PATH` exists and contains at least one `KA-*.md` file (or absence is reported as `FAILED_INPUTS`).
2. `OUTPUT_ROOT` exists before the skill writes to it.
3. Every `KA-*.md` file in the KTY folder was read, or its absence was explicitly reported.
4. The output file `{KTY_ID}_Equipment_Extract.md` was written to `OUTPUT_ROOT`.
5. The output file contains all required sections: title, metadata block, Equipment Table, Package Notes, equipment count footer.
6. No files in `{KTY_PATH}` were written or modified.

## Source traceability (required for every extracted item)

Every row in the Equipment Table must satisfy all of the following:

| Check | Requirement |
|---|---|
| KA source cited | The `KA Source` column names the specific `KA-*.md` file from which the item was extracted |
| Equipment exists in source | The equipment item appears in the cited KA file text; no invented items |
| Tag is verbatim | The `Equipment Tag` value is an exact match from the source text, or `No tag` when the source does not state one |
| Package assignment sourced | `Package Name` is a formal name from the source, a contextual name with `(indicated)` suffix, or `N/A` |

A run with even one untraceable equipment row is invalid.

## Null-result validation

KTYs with zero physical equipment must still produce an output file containing:

- An empty Equipment Table (or single explanatory row)
- Package Notes explaining why no equipment was found
- An equipment count footer reading `0` with parenthetical explanation

## Reporting groups

When issues are found during extraction, group them by:

- missing KA files (listed in folder but not on disk, or vice versa)
- ambiguous tags (tag partially stated or conflicting across KAs)
- scope boundary items (equipment where ownership is unclear)
- TBD items (equipment referenced as future or placeholder)
- package assignment uncertainty (formal vs. indicated vs. absent)

## Success case

A clean run reports:

- `RUN_STATUS=OK`
- Output file path
- Equipment count (integer)
- List of KA files read
- No warnings (or explicit statement that none were encountered)
