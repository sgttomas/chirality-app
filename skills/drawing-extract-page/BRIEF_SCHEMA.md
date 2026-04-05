# drawing-extract-page — Brief Schema

Use this skill with a TASK shell dispatched by the `DRAWING_EXTRACT` orchestrator, one invocation per page:

```md
PURPOSE: Extract top-of-sheet equipment header from drawing page 7 of 42
RequestedBy: DRAWING_EXTRACT

ScopePath: /abs/path/to/drawing_extract_work
TaskSkill: drawing-extract-page

AllowedWriteTargets:
  - "/abs/path/to/drawing_extract_work/page_stubs/page_007.md"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/drawing_extract_work/pages/page_007.png
  HEADER_IMAGE_PATH: /abs/path/to/drawing_extract_work/crops/page_007_header.png
  TITLEBLOCK_IMAGE_PATH: /abs/path/to/drawing_extract_work/crops/page_007_titleblock.png
  HEADER_SLICE_PATHS:
    - /abs/path/to/drawing_extract_work/slices/page_007_slice_1.png
    - /abs/path/to/drawing_extract_work/slices/page_007_slice_2.png
    - /abs/path/to/drawing_extract_work/slices/page_007_slice_3.png
  OUTPUT_PATH: /abs/path/to/drawing_extract_work/page_stubs/page_007.md
  PAGE_NUM: 7
  TOTAL_PAGES: 42
  EXTRACTION_MODE: top_equipment_header_with_dwg
  OUTPUT_FORMAT: markdown_stub
  SOURCE_PDF_NAME: WestDoe_300MMSCFD_DeepcutGasPlant.pdf

ExpectedOutputs:
  - /abs/path/to/drawing_extract_work/page_stubs/page_007.md
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `drawing-extract-page` | Must match skill folder name |
| `AllowedWriteTargets` | `[OUTPUT_PATH]` | Exactly the designated output path |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to page PNG | `.png` extension required |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path for the single output artifact | Parent directory must exist |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total pages in source PDF | Positive integer |
| `RuntimeOverrides.EXTRACTION_MODE` | Extraction target definition | Must be a supported mode |
| `RuntimeOverrides.OUTPUT_FORMAT` | Per-page output format | `markdown_stub` or `csv_row` |

## Strongly recommended fields

| Field | Notes |
|---|---|
| `RuntimeOverrides.HEADER_IMAGE_PATH` | Top-header crop for crop-first bounded reading |
| `RuntimeOverrides.TITLEBLOCK_IMAGE_PATH` | Title-block crop for `DWG NO.` and `system_name` |
| `RuntimeOverrides.HEADER_SLICE_PATHS` | Overlapping header slices for multiblock completeness |

## Optional fields

| Field | Notes |
|---|---|
| `RuntimeOverrides.SOURCE_PDF_NAME` | Used for provenance in output artifact |

## Supported EXTRACTION_MODE values

| Mode | Meaning |
|---|---|
| `top_equipment_header_with_dwg` | Extract separated top-of-sheet equipment header entries plus page `DWG NO.` and title-block `system_name` |

Any other extraction mode MUST cause the run to return `RUN_STATUS=FAILED_INPUTS`.

## Supported OUTPUT_FORMAT values

| Format | Meaning |
|---|---|
| `markdown_stub` | Page-scoped Markdown artifact with metadata and findings table |
| `csv_row` | CSV content with header `equipment_number,equipment_name,system_name,drawing,source_page,status` |

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile. It is dispatched by the `DRAWING_EXTRACT` persona for per-page fanout.

## Read boundary

The skill reads only:

- `IMAGE_PATH`
- `HEADER_IMAGE_PATH` (if provided)
- `TITLEBLOCK_IMAGE_PATH` (if provided)
- each path in `HEADER_SLICE_PATHS` (if provided)

The skill MUST NOT read any other files and MUST NOT use any cross-page context.

## Write boundary

The skill writes only:

- `OUTPUT_PATH`

`AllowedWriteTargets` must be exactly the single `OUTPUT_PATH`. The skill does not create directories.

## RuntimeOverrides examples

### Example 1 — all helper crops provided (preferred)

```yaml
RuntimeOverrides:
  IMAGE_PATH: /work/pages/page_012.png
  HEADER_IMAGE_PATH: /work/crops/page_012_header.png
  TITLEBLOCK_IMAGE_PATH: /work/crops/page_012_titleblock.png
  HEADER_SLICE_PATHS:
    - /work/slices/page_012_slice_1.png
    - /work/slices/page_012_slice_2.png
  OUTPUT_PATH: /work/page_stubs/page_012.md
  PAGE_NUM: 12
  TOTAL_PAGES: 42
  EXTRACTION_MODE: top_equipment_header_with_dwg
  OUTPUT_FORMAT: markdown_stub
```

### Example 2 — CSV row output

```yaml
RuntimeOverrides:
  IMAGE_PATH: /work/pages/page_003.png
  HEADER_IMAGE_PATH: /work/crops/page_003_header.png
  TITLEBLOCK_IMAGE_PATH: /work/crops/page_003_titleblock.png
  OUTPUT_PATH: /work/page_rows/page_003.csv
  PAGE_NUM: 3
  TOTAL_PAGES: 42
  EXTRACTION_MODE: top_equipment_header_with_dwg
  OUTPUT_FORMAT: csv_row
  SOURCE_PDF_NAME: WestDoe_300MMSCFD_DeepcutGasPlant.pdf
```

### Example 3 — full page only (fallback, no crops)

```yaml
RuntimeOverrides:
  IMAGE_PATH: /work/pages/page_005.png
  OUTPUT_PATH: /work/page_stubs/page_005.md
  PAGE_NUM: 5
  TOTAL_PAGES: 42
  EXTRACTION_MODE: top_equipment_header_with_dwg
  OUTPUT_FORMAT: markdown_stub
```

## CustomInstructions

CustomInstructions are not used by this skill. The extraction contract is fully determined by `EXTRACTION_MODE`. Any page-specific interpretation hints from the orchestrator should be attached as separate narrative context in the brief body, not through structured overrides.

## Notes

- One brief = one page = one output artifact. The orchestrator spawns one TASK invocation per in-scope page.
- The brief does not include `AllowedTools` because this skill is VLM-reasoning-only with no deterministic tool dependencies.
- All crops and slices are prepared by the orchestrator before dispatch; this skill does not invoke crop-preparation tools itself.
