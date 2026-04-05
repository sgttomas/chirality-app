---
name: drawing-extract-page
description: Per-page bounded extraction of structured data from a single engineering drawing page image, using crop-first multiblock VLM reasoning. Invoked by the DRAWING_EXTRACT orchestrator for per-page fanout.
compatibility: Chirality TASK; invoked by DRAWING_EXTRACT orchestrator for per-page fanout
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — drawing-extract-page

## Purpose

Read **one engineering drawing page image** and extract **targeted structured information** from that page against an explicit `EXTRACTION_MODE`. This is a **bounded extraction** skill, not a full-page transcription skill.

One invocation processes one page and writes exactly one output artifact. No cross-page context. Orchestrator dispatches one invocation per page for parallelism.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `DRAWING_EXTRACT` orchestrator.

Not the best fit for:
- full-page transcription (use `pdf2md-page` or `PDF2MD_PAGE` instead)
- multi-page context reasoning (orchestrator owns that)
- orchestration/dispatch itself (the parent `DRAWING_EXTRACT` persona owns that)

## Inputs

### Required

- `RuntimeOverrides.IMAGE_PATH` — absolute path to the drawing page PNG
- `RuntimeOverrides.OUTPUT_PATH` — absolute path to write the extraction output
- `RuntimeOverrides.PAGE_NUM` — 1-indexed page number
- `RuntimeOverrides.TOTAL_PAGES` — total pages in the source document
- `RuntimeOverrides.EXTRACTION_MODE` — extraction target definition (see supported modes)
- `RuntimeOverrides.OUTPUT_FORMAT` — `markdown_stub` or `csv_row`

### Strongly recommended

- `RuntimeOverrides.HEADER_IMAGE_PATH` — cropped top-header PNG for the same page
- `RuntimeOverrides.TITLEBLOCK_IMAGE_PATH` — cropped title-block PNG for the same page

### Optional

- `RuntimeOverrides.HEADER_SLICE_PATHS` — ordered list of overlapping top-header slice PNGs for multiblock review
- `RuntimeOverrides.SOURCE_PDF_NAME` — PDF filename for provenance in output

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `IMAGE_PATH` | Absolute path to drawing page PNG | **Required** | `.png` file path |
| `HEADER_IMAGE_PATH` | Absolute path to cropped top-header PNG | None | `.png` file path |
| `TITLEBLOCK_IMAGE_PATH` | Absolute path to cropped title-block PNG | None | `.png` file path |
| `HEADER_SLICE_PATHS` | Ordered list of overlapping header slice PNGs | `[]` | List of `.png` file paths |
| `OUTPUT_PATH` | Absolute path for the single output artifact | **Required** | Parent directory must exist |
| `PAGE_NUM` | 1-indexed page number | **Required** | Positive integer |
| `TOTAL_PAGES` | Total pages in source PDF | **Required** | Positive integer |
| `EXTRACTION_MODE` | Extraction target definition | **Required** | `top_equipment_header_with_dwg` |
| `OUTPUT_FORMAT` | Per-page output format | **Required** | `markdown_stub` or `csv_row` |
| `SOURCE_PDF_NAME` | PDF filename for provenance | None | Any string |

### Supported extraction modes

| Mode | Meaning |
|---|---|
| `top_equipment_header_with_dwg` | Extract equipment numbers and names from the separated top-of-sheet equipment header; extract the page `DWG NO.`; extract the title-block `system_name` |

The skill MUST fail inputs for any extraction mode not explicitly listed above.

## Read boundary

Reads are limited to:

- `IMAGE_PATH` — current page drawing PNG
- `HEADER_IMAGE_PATH` — current page top-header crop (when provided)
- `TITLEBLOCK_IMAGE_PATH` — current page title-block crop (when provided)
- each path in `HEADER_SLICE_PATHS` — current page header slices (when provided)

The skill MUST NOT read any other files, and MUST NOT use any cross-page context.

## Write boundary

Writes are limited to:

- `OUTPUT_PATH` — exactly one structured artifact per invocation

No other files are written. `OUTPUT_PATH`'s parent directory must already exist; the skill does not create directories.

## Tool usage

- No deterministic tools. This skill is VLM-reasoning-only (the agent reads image files directly via the Read tool).
- The `allowed-tools` frontmatter field is intentionally omitted.
- The orchestrator (parent `DRAWING_EXTRACT` agent) is responsible for any deterministic PDF-level cross-checking, header/title-block crop preparation, and stub assembly. This skill does not invoke PDF-level tools itself.

Disallowed behavior:

- No deterministic tool invocation; no shell commands.
- No writing outside `OUTPUT_PATH`.
- No reading of files outside the declared read boundary (no cross-page context, no Scoping.md, no other page images).
- No sub-agent fanout.

## Method

### Step 1 — Validate inputs

1. Confirm `IMAGE_PATH` exists and is a `.png` file.
2. If provided, confirm `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and each path in `HEADER_SLICE_PATHS` exists and is a `.png` file.
3. Confirm `OUTPUT_PATH` parent directory exists.
4. Confirm `EXTRACTION_MODE` is supported.
5. Confirm `OUTPUT_FORMAT` is `markdown_stub` or `csv_row`.
6. If any input is invalid, write a failure placeholder to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.

### Step 2 — Read and inspect the page image (crop-first)

1. Use the Read tool to load `IMAGE_PATH`.
2. If provided, also load `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and every path in `HEADER_SLICE_PATHS`.
3. Identify the following page regions as needed by the extraction mode:
   - the **top-of-sheet separated equipment header region**
   - the **title block / `DWG NO.` region**
   - the **title block title region** containing the project line, system-name line, and title suffix line (e.g., `PROCESS FLOW DIAGRAM`)
4. **Prefer helper crops over the full-page image for bounded reading:**
   - use `TITLEBLOCK_IMAGE_PATH` first for `DWG NO.` and `system_name`
   - use `HEADER_IMAGE_PATH` and `HEADER_SLICE_PATHS` first for equipment findings
   - use the full-page image only to resolve current-page spatial context when a helper crop is insufficient
5. Ignore decorative borders, general process lines, and repeated in-body equipment tags unless the extraction mode explicitly requires them.

### Step 3 — Extract according to mode

For `top_equipment_header_with_dwg`:

1. Extract the page `DWG NO.` from the title block.
2. Extract `system_name` from the title block as the line between the project line and the title suffix line.
3. Inspect the separated equipment/header region at the top of the sheet.
4. For each equipment item in that top region, extract:
   - `equipment_number`
   - `equipment_name`
   - `system_name` = extracted title-block `system_name`
   - `drawing` = extracted `DWG NO.`
   - `source_page` = `PAGE_NUM`
5. **When helper slices are provided, inspect all slices before concluding extraction is complete.**
6. **When the top header is arranged as multiple separated clusters across the page width, treat each underlined tag/name cluster as an independent finding even if some clusters sit lower than others within the same header band.**
7. **Deduplicate within the page only when the same tag/name cluster appears in overlapping slices; do not collapse distinct grouped-tag findings.**
8. If the top-of-sheet region contains no relevant equipment header, record **no findings**.
9. Do not backfill from the body of the drawing when the top header is absent.
10. If the apparent top region contains only notes, setpoints, spec text, or instrument/control annotations rather than discrete equipment header blocks, record **no findings**.

### Step 4 — Apply extraction rules

**RULE 1 — NO INVENTION**
- Extract only what is visible.
- If a tag or name is ambiguous, preserve what is legible and do not normalize beyond certainty.

**RULE 2 — REGION DISCIPLINE**
- Respect the extraction scope.
- For `top_equipment_header_with_dwg`, only the separated top header region counts for equipment findings.
- Ignore the right-side notes area even when it sits at the top of the sheet.
- Ignore lower vendor/model/specification lines inside a dense header block if they are not part of the primary equipment name.
- When helper crops are provided, they define the primary bounded reading region unless they are clearly incomplete for the current page.

**RULE 3 — REQUIRED COMPANION FIELDS**
- `DWG NO.` and `system_name` are mandatory.
- If either cannot be extracted with confidence, return `RUN_STATUS=FAILED` and write a failure artifact.

**RULE 3.5 — TAG REQUIRED FOR A FINDING**
- Do not emit a finding row when `equipment_number` is blank.
- Do not emit control/instrument rows such as setpoint bubbles, controller tags, PSV/PCV/FIC style annotations, or standards references when the extraction mode is equipment-focused.

**RULE 3.6 — PRIMARY NAME ONLY**
- `equipment_name` must be the primary equipment label only.
- Exclude adjacent notes, duty text, vendor/model text, frame/common-base text, API/TEMA references, dimensions, pressure/temperature setpoints, and operating comments.
- When a dense multi-line block is present, prefer the shortest line that still names the equipment.

**RULE 3.7 — MULTI-BLOCK HEADER COMPLETENESS**
- Do not assume all findings share one baseline or appear in one continuous top row.
- On compressor-train style sheets and similar repeated layouts, include lower standalone pump/header blocks and right-side frame blocks when they are still part of the separated top-header region.
- A valid page may contain both left-to-right top-row findings and a second staggered row of findings within the same header band.

**RULE 3.8 — LOW-COUNT SKEPTICISM**
- Do not assume `0`, `1`, or `2` findings are correct simply because a few tags were found.
- If helper slices show additional underlined tag/name clusters, keep extracting until all visible current-page header blocks have been accounted for or explicitly excluded as non-equipment.
- `NO_FINDINGS` is only valid when the bounded header region truly lacks discrete equipment header blocks.

**RULE 4 — GROUPED TAGS**
- Preserve grouped identifiers exactly as shown when they are presented as one item, such as `P-7260-2/7270-2`.

**RULE 5 — EMPTY PAGES ARE VALID**
- If the page has no matching extraction targets, that is a valid result, not an error.

### Step 5 — Write structured output

If `OUTPUT_FORMAT=markdown_stub`:

1. Write a page-scoped Markdown artifact containing:
   - source PDF name if provided
   - source page
   - `DWG NO.`
   - `system_name`
   - a four-column table: `equipment_number`, `equipment_name`, `system_name`, `drawing`
2. If no findings are present, write an empty-row table and a note that no separated top-of-sheet equipment header was identified.

If `OUTPUT_FORMAT=csv_row`:

1. Write CSV content only.
2. Header MUST be: `equipment_number,equipment_name,system_name,drawing,source_page,status`
3. If findings exist, write one row per extracted item with `status=FOUND`.
4. If no findings exist, write one row with blank equipment fields, populated `drawing`, populated `source_page`, and `status=NO_FINDINGS`.

### Step 6 — Return status

Return exactly one of:

- `RUN_STATUS=SUCCESS` — one or more findings were extracted
- `RUN_STATUS=NO_FINDINGS` — page was readable but no relevant extraction target was present
- `RUN_STATUS=FAILED_INPUTS` — inputs were invalid
- `RUN_STATUS=FAILED` — page could not be interpreted, or `DWG NO.` / `system_name` could not be extracted

Also return: `PAGE_NUM`, `FINDING_COUNT`, `DWG_NO` (if available), `SYSTEM_NAME` (if available).

## Outputs

- Exactly one file at `OUTPUT_PATH`:
  - a `markdown_stub` artifact, or
  - a `csv_row` artifact
- Structured return values: `RUN_STATUS`, `PAGE_NUM`, `FINDING_COUNT`, `DWG_NO`, `SYSTEM_NAME`

## Non-negotiable constraints

- **Single-page scope.** One invocation reads one page. No cross-page context.
- **OUTPUT_PATH-only writes.** Exactly one file is written per invocation. No other side effects.
- **Crop-first workflow.** When helper crops and slices are provided, prefer them over the full-page image; use the full page only to resolve spatial context a crop cannot answer alone.
- **Multiblock completeness.** Inspect all provided header slices before concluding; treat each underlined tag/name cluster as an independent finding even across staggered rows.
- **VLM-reasoning contract.** This skill performs bounded visual extraction via direct image inspection, not deterministic tooling.
- **No invention.** Extract only what is visible; do not normalize, backfill, or synthesize.
- **Required companion fields.** `DWG NO.` and `system_name` are mandatory whenever a supported extraction mode is run.
- **Tag required for a finding.** Rows with blank `equipment_number` are invalid for `top_equipment_header_with_dwg`.
- **No deterministic PDF-level tools.** PDF-level cross-checking belongs to the orchestrator.
- **NO_FINDINGS is valid.** Empty pages still produce a valid artifact and a `NO_FINDINGS` status.
- **Low-count skepticism.** Treat 0/1/2-finding outcomes skeptically until all helper slices have been accounted for.

## QA expectations

- Exactly one file exists at `OUTPUT_PATH` after the run.
- No files other than `OUTPUT_PATH` were written.
- When the run succeeded or returned `NO_FINDINGS`, the output contains `DWG NO.` and `system_name`.
- Findings (if any) reflect only the region and semantics required by `EXTRACTION_MODE`.
- No findings have a blank `equipment_number` in `top_equipment_header_with_dwg` mode.
- `RUN_STATUS` is one of: `SUCCESS`, `NO_FINDINGS`, `FAILED`, `FAILED_INPUTS`.
- `FINDING_COUNT` matches the number of populated rows in the output artifact.

## Relationship to DRAWING_EXTRACT

This skill is the per-page worker invoked by the `DRAWING_EXTRACT` orchestrator for per-page fanout. The orchestrator:

- rasterizes the PDF,
- prepares top-header and title-block crops and overlapping header slices,
- dispatches one `TASK` + `drawing-extract-page` invocation per page,
- runs deterministic stub-count reporting, sanitization, and assembly.

This skill is the direct successor to `AGENT_DRAWING_EXTRACT_PAGE.md` in skill form. It is a sibling of `pdf2md-page` — same per-page fanout pattern, but bounded extraction instead of full-page transcription.
