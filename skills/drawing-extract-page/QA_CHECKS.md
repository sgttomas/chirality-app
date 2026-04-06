# drawing-extract-page — QA Checks

## Minimum checks for a valid run

1. `IMAGE_PATH` exists and is a `.png` file (or `RUN_STATUS=FAILED_INPUTS` was returned).
2. When provided, `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and each `HEADER_SLICE_PATHS` entry exist and are `.png` files.
3. `OUTPUT_PATH` has a `.md` extension and its parent directory exists before the skill writes to it.
4. `DRAWING_TYPE` is a known value (`PFD`, `P_AND_ID`, `ISOMETRIC`, or `GA`).
5. If `DRAWING_TYPE ∈ {P_AND_ID, ISOMETRIC, GA}`: run returned `RUN_STATUS=FAILED_INPUTS` without reading any image files (stubbed-type fail-fast).
6. `(DRAWING_TYPE, EXTRACTION_TARGET)` is a valid combination per the registry in SKILL.md.
7. For detailed target: `REQUESTED_KNOWN_FIELDS`, `EXTRA_FIELDS`, and `REQUIRED_FIELDS` are present (may be empty lists).
8. Exactly one file exists at `OUTPUT_PATH` after the run.
9. No files other than `OUTPUT_PATH` were written.
10. No files outside the declared read boundary were read (no cross-page context, no other page images).

## Stubbed-type fail-fast expectations

When `DRAWING_TYPE ∈ {P_AND_ID, ISOMETRIC, GA}` is provided:

| Check | Requirement |
|---|---|
| No image reading | The skill MUST return `RUN_STATUS=FAILED_INPUTS` without calling Read on any image file |
| Clear error message | The failure placeholder at `OUTPUT_PATH` MUST note that the drawing_type is registered but not implemented |
| Extension-point pointer | The message SHOULD point to "How to add a new drawing type" in AGENT_DRAWING_EXTRACT.md |

## EXTRA_FIELDS collision checks (detailed target)

When `EXTRA_FIELDS` is non-empty, all of the following must hold before any extraction begins:

| Check | Requirement |
|---|---|
| Name regex | Every `name` matches `^[a-z][a-z0-9_]*$`, max 40 chars |
| Description well-formed | Every `description` is non-empty, max 200 chars, single line |
| No base-column collision | No `name` matches `equipment_number`, `equipment_name`, `system_name`, `drawing`, or `source_page` |
| No catalog collision | No `name` matches any catalog field name (even unrequested ones) |
| No intra-run duplicates | No two extra fields share the same `name` |
| REQUIRED_FIELDS subset | Every REQUIRED_FIELDS entry is in `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name` |

Any collision → `RUN_STATUS=FAILED_INPUTS` with error describing which rule fired.

## Self-describing output frontmatter

Every stub output must begin with YAML frontmatter (`---` delimited) that is well-formed and contains target-appropriate keys:

### Required for `top_equipment_header_basic`

| Key | Constraint |
|---|---|
| `drawing_type` | MUST equal `PFD` |
| `extraction_target` | MUST equal `top_equipment_header_basic` |
| `source_pdf` | MUST match `SOURCE_PDF_NAME` (or `unknown` if unset) |
| `source_page` | MUST equal `PAGE_NUM` as integer |
| `drawing` | MUST be the extracted DWG NO. (or empty for FAILED) |
| `system_name` | MUST be the extracted system name (or empty for FAILED) |
| `status` | MUST be one of `SUCCESS`, `NO_FINDINGS`, `FAILED_INPUTS`, `FAILED` |

### Required for `top_equipment_header_detailed` (adds to basic)

| Key | Constraint |
|---|---|
| `requested_known_fields` | MUST equal the run's `REQUESTED_KNOWN_FIELDS` list (may be `[]`) |
| `requested_extra_fields` | MUST equal the run's `EXTRA_FIELDS` list (name + description pairs; may be `[]`) |
| `required_fields` | MUST equal the run's `REQUIRED_FIELDS` list (may be `[]`) |

## Required title-block provenance

When `RUN_STATUS` is `SUCCESS` or `NO_FINDINGS`, the output frontmatter must contain:

| Field | Requirement |
|---|---|
| `drawing` | Extracted verbatim from the page title block (`DWG NO.`) |
| `system_name` | Extracted from the title block as the line between the project line and the title suffix line |

If either field cannot be extracted with confidence, `RUN_STATUS=FAILED` must be returned and a failure artifact must still be written to `OUTPUT_PATH`.

## Finding validation (both targets)

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

## Detail-field validation (detailed target only)

For each requested detail field:

| Check | Requirement |
|---|---|
| No invention | Any non-blank detail value must be visible in one of the helper crops (`HEADER_IMAGE_PATH` or `HEADER_SLICE_PATHS`) for that equipment item |
| Spatial association | Value attaches to an item only when visible directly beneath or adjacent within the item's own equipment block |
| Ambiguity → blank | When descriptor ownership between two items is unclear, the value is blank (not guessed) |
| Blank-valid | Blank detail values are always valid; never a failure condition |
| Unrequested fields not emitted | A detail field not in `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name` MUST NOT appear in the output table |

## Crops-only-for-detail discipline (detailed target)

| Check | Requirement |
|---|---|
| Full-page not consulted for detail | Detail field values MUST NOT originate from content visible only in `IMAGE_PATH` (full-page); they must be visible in at least one helper crop |
| Spatial-context exception | The full-page image MAY be consulted to resolve parent-item ambiguity for a descriptor visible in a crop, but not to discover new descriptor content |

## Crop-first discipline checks (both targets)

When helper crops were provided:
- The skill must have inspected `TITLEBLOCK_IMAGE_PATH` first for `DWG NO.` and `system_name`.
- The skill must have inspected `HEADER_IMAGE_PATH` and all `HEADER_SLICE_PATHS` first for equipment findings.
- The full-page image should only have been used to resolve spatial context that a crop could not answer alone.

## Multiblock completeness checks (both targets)

- All provided `HEADER_SLICE_PATHS` entries must have been inspected before concluding extraction is complete.
- When the top header was arranged as multiple separated clusters across the page width, each underlined tag/name cluster must have been treated as an independent finding.
- Deduplication must have happened only for the same tag/name cluster appearing in overlapping slices; distinct grouped-tag findings must not have been collapsed.
- A valid page may contain both left-to-right top-row findings and a second staggered row of findings within the same header band — both must be represented.

## Low-count skepticism checks (both targets)

- A `NO_FINDINGS` outcome is only valid when the bounded header region truly lacks discrete equipment header blocks.
- A 0/1/2-finding outcome must be corroborated by the helper slices showing no additional underlined tag/name clusters.
- If helper slices show additional clusters that were not extracted, the run is invalid.

## Required-fields warnings (detailed target, orchestrator-side)

`REQUIRED_FIELDS` does NOT fail the page-worker. Instead, orchestrator QA via `report_stub_counts.py` (detailed mode) generates per-page warnings:

| Condition | Warning emitted |
|---|---|
| A row has blank value for a REQUIRED_FIELD | `row {N} on page {P}: missing required field '{field}'` |

Warnings never block assembly.

## Detail capture rate (detailed target, orchestrator-side)

Orchestrator QA computes, per run:
- Per-field detail capture rate = (non-blank cells) / (total rows)
- Suspicious-detail heuristic: if all rows on a page share the identical value for a requested detail field, flag for human review (possible copy-across hallucination)

## Output format validation

Output at `OUTPUT_PATH` must:

1. Begin with YAML frontmatter (`---` delimited) per the self-describing schema above.
2. Contain H1 page title.
3. Contain findings table with target-appropriate columns:
   - basic: `equipment_number | equipment_name | system_name | drawing` (4 columns)
   - detailed: base (4) + requested_known_fields (canonical catalog order) + requested_extra_fields.name (request order)
4. For NO_FINDINGS: an empty-row table plus a note stating that no separated top-of-sheet equipment header was identified.
5. End with extraction status line: `- Extraction status: {SUCCESS|NO_FINDINGS|FAILED_INPUTS|FAILED}`.

Per-page CSV output (`csv_row`) is not supported in v2. A stub with CSV content at `OUTPUT_PATH` is invalid.

## RUN_STATUS expectations

| Status | When returned |
|---|---|
| `SUCCESS` | One or more findings were extracted |
| `NO_FINDINGS` | Page was readable but no relevant extraction target was present |
| `FAILED_INPUTS` | Inputs were invalid (missing file, unsupported combination, stubbed drawing_type, EXTRA_FIELDS collision, etc.) |
| `FAILED` | Page could not be interpreted, or `DWG NO.` / `system_name` could not be extracted with confidence |

`FINDING_COUNT` must match the number of populated rows in the output artifact.

## Failure posture

- On input validation failure: write a failure placeholder to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.
- On stubbed-type dispatch: write failure placeholder with "registered but not implemented" note and return `RUN_STATUS=FAILED_INPUTS` without image reading.
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
- Detailed target only: `DETAIL_CAPTURE_COUNTS` (map of requested field name → count of populated cells)

## Reporting groups

When issues are surfaced to the orchestrator, group them by:

- invalid inputs (missing files, unsupported combination, stubbed drawing_type, EXTRA_FIELDS collision, bad output path)
- missing title-block fields (`DWG NO.` or `system_name` could not be extracted)
- ambiguous tags (tag partially legible or conflicting across slices)
- region boundary uncertainty (whether a block belongs to the top header or the body)
- suspected multiblock incompleteness (helper slices show clusters that were not extracted)
- ambiguous descriptor association (detailed target: descriptor ownership between two items unclear → blank emitted)
- crop insufficiency suspected (detailed target: page may need per-page crop override per orchestrator runbook)
