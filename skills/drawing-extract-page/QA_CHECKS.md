# drawing-extract-page — QA Checks

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and is a `.png` file (or `RUN_STATUS=FAILED_INPUTS` was returned).
2. When provided, `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and each `HEADER_SLICE_PATHS` entry exist and are `.png` files.
3. `OUTPUT_PATH` parent directory exists before the skill writes to it.
4. `EXTRACTION_MODE` is a supported mode (currently only `top_equipment_header_with_dwg`).
5. `OUTPUT_FORMAT` is `markdown_stub` or `csv_row`.
6. Exactly one file exists at `OUTPUT_PATH` after the run.
7. No files other than `OUTPUT_PATH` were written.
8. No files outside the declared read boundary were read (no cross-page context, no other page images).

## Required title-block provenance

When `RUN_STATUS` is `SUCCESS` or `NO_FINDINGS`, the output artifact must contain:

| Field | Requirement |
|---|---|
| `DWG NO.` | Extracted verbatim from the page title block |
| `system_name` | Extracted from the title block as the line between the project line and the title suffix line |

If either field cannot be extracted with confidence, `RUN_STATUS=FAILED` must be returned and a failure artifact must still be written to `OUTPUT_PATH`.

## Finding validation (for `top_equipment_header_with_dwg`)

Every finding row must satisfy all of the following:

| Check | Requirement |
|---|---|
| Tag present | `equipment_number` is non-blank (blank-tag rows are invalid) |
| Tag verbatim | `equipment_number` is an exact match from the source image, preserving grouped identifiers like `P-7260-2/7270-2` |
| Name is primary label | `equipment_name` is the primary equipment label only — no adjacent notes, duty text, vendor/model text, frame/common-base text, API/TEMA references, dimensions, setpoints, or operating comments |
| No invention | The finding appears in the bounded top-header region of the current page image |
| Region discipline | No findings come from the body of the drawing or from right-side notes areas |
| Companion fields populated | `system_name` and `drawing` match the extracted title-block values; `source_page` matches `PAGE_NUM` |

A run with even one invalid finding row is invalid.

## Crop-first discipline checks

When helper crops were provided:

- The skill must have inspected `TITLEBLOCK_IMAGE_PATH` first for `DWG NO.` and `system_name`.
- The skill must have inspected `HEADER_IMAGE_PATH` and all `HEADER_SLICE_PATHS` first for equipment findings.
- The full-page image should only have been used to resolve spatial context that a crop could not answer alone.

## Multiblock completeness checks

- All provided `HEADER_SLICE_PATHS` entries must have been inspected before concluding extraction is complete.
- When the top header was arranged as multiple separated clusters across the page width, each underlined tag/name cluster must have been treated as an independent finding.
- Deduplication must have happened only for the same tag/name cluster appearing in overlapping slices; distinct grouped-tag findings must not have been collapsed.
- A valid page may contain both left-to-right top-row findings and a second staggered row of findings within the same header band — both must be represented.

## Low-count skepticism checks

- A `NO_FINDINGS` outcome is only valid when the bounded header region truly lacks discrete equipment header blocks.
- A 0/1/2-finding outcome must be corroborated by the helper slices showing no additional underlined tag/name clusters.
- If helper slices show additional clusters that were not extracted, the run is invalid.

## Output format validation

### `markdown_stub`

The output must contain:

1. A page title
2. Source metadata (source PDF name if provided, source page)
3. `DWG NO.`
4. `system_name`
5. A four-column findings table: `equipment_number | equipment_name | system_name | drawing`
6. When no findings, an empty-row table plus a note stating that no separated top-of-sheet equipment header was identified

### `csv_row`

The output must contain:

1. Header line: `equipment_number,equipment_name,system_name,drawing,source_page,status`
2. One row per finding with `status=FOUND`, OR
3. One row with blank equipment fields, populated `drawing`, populated `source_page`, and `status=NO_FINDINGS`

## RUN_STATUS expectations

| Status | When returned |
|---|---|
| `SUCCESS` | One or more findings were extracted |
| `NO_FINDINGS` | Page was readable but no relevant extraction target was present |
| `FAILED_INPUTS` | Inputs were invalid (missing file, unsupported mode, etc.) |
| `FAILED` | Page could not be interpreted, or `DWG NO.` / `system_name` could not be extracted with confidence |

`FINDING_COUNT` must match the number of populated rows in the output artifact.

## Failure posture

- On input validation failure: write a failure placeholder to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.
- On interpretation failure: write a failure artifact to `OUTPUT_PATH` and return `RUN_STATUS=FAILED`.
- Never silently drop a page. The orchestrator must always receive exactly one output artifact per dispatched page.

## Success case reporting

A clean run reports:

- `RUN_STATUS` = `SUCCESS` or `NO_FINDINGS`
- `PAGE_NUM`
- `FINDING_COUNT` (integer; `0` for `NO_FINDINGS`)
- `DWG_NO` (extracted drawing number)
- `SYSTEM_NAME` (extracted title-block system name)
- Output file path

## Reporting groups

When issues are surfaced to the orchestrator, group them by:

- invalid inputs (missing files, unsupported mode, bad output format)
- missing title-block fields (`DWG NO.` or `system_name` could not be extracted)
- ambiguous tags (tag partially legible or conflicting across slices)
- region boundary uncertainty (whether a block belongs to the top header or the body)
- suspected multiblock incompleteness (helper slices show clusters that were not extracted)
