---
name: drawing-titleblock-page
description: Per-page titleblock extraction from drawing sheets using four corner crops and a full-page thumbnail; emits a governed sheet-inventory stub.
compatibility: Chirality TASK; dispatched by DRAWING_EXTRACT for DRAWING_SET/titleblock_index
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - drawing-titleblock-page

## Purpose

Extract titleblock metadata from one drawing page for the `DRAWING_SET/titleblock_index` workflow. This is a bounded per-page visual extraction skill. It does not inventory a full PDF, choose downstream page scope, or accept drawing-family classifications.

The output is a single markdown stub with YAML frontmatter and a one-row findings table.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `DRAWING_EXTRACT` orchestrator.

## Inputs

### Required

- `RuntimeOverrides.SOURCE_PDF_NAME` - source PDF basename.
- `RuntimeOverrides.PAGE_NUM` - 1-indexed page number.
- `RuntimeOverrides.TOTAL_PAGES` - total pages in the PDF.
- `RuntimeOverrides.CORNER_CROP_PATHS` - paths for `tl`, `tr`, `bl`, and `br` titleblock crops.
- `RuntimeOverrides.THUMBNAIL_PATH` - low-resolution full-page thumbnail.
- `RuntimeOverrides.OUTPUT_PATH` - path for the output markdown stub.
- `RuntimeOverrides.CORNER_CROP_GEOMETRY` - `width_ratio` and `height_ratio` used for the crops.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `SOURCE_PDF_NAME` | PDF basename for provenance | Required | String |
| `PAGE_NUM` | Page number | Required | Positive integer |
| `TOTAL_PAGES` | Total pages | Required | Positive integer |
| `CORNER_CROP_PATHS` | Four corner crop paths keyed by `tl,tr,bl,br` | Required | Existing image paths |
| `THUMBNAIL_PATH` | Full-page thumbnail path | Required | Existing image path |
| `OUTPUT_PATH` | Stub output path | Required | `.md` file path |
| `CORNER_CROP_GEOMETRY` | Crop ratios | Required | `width_ratio`, `height_ratio` |

## Tool usage

No deterministic tools are invoked by this skill. The parent orchestrator prepares crops, validates stubs, and assembles the index.

## Method

1. Validate that all required image paths and `OUTPUT_PATH` are present.
2. Read the full-page thumbnail to understand page orientation and whether a titleblock is present.
3. Read all four corner crops and identify the titleblock corner.
4. Extract visible metadata:
   - `dwg_no`
   - `sheet_no`
   - `sheet_title`
   - `revision`
   - `area_or_module`
   - `drawing_family_proposal`
   - `titleblock_corner`
   - `confidence`
5. If no titleblock is visible, emit `NO_TITLEBLOCK` with `finding_count: 0`.
6. Write exactly one markdown stub at `OUTPUT_PATH`.

## Drawing-family proposal

`drawing_family_proposal` is not authoritative. It is a proposal for the human to review during scope acceptance. Use one of:

- `PFD`
- `P_AND_ID`
- `ISOMETRIC`
- `GA`
- `OTHER`
- `REFERENCE_OR_LEGEND`
- `TBD`

## No-invention rule

Unreadable fields are `TBD`. Do not infer a drawing number or sheet number from surrounding page order. Do not convert a proposal into final operator scope.

## Output format

Every stub begins with YAML frontmatter:

```yaml
---
drawing_type: DRAWING_SET
extraction_target: titleblock_index
source_pdf: <SOURCE_PDF_NAME>
source_page: <PAGE_NUM>
corner_crop_geometry:
  width_ratio: 0.25
  height_ratio: 0.25
status: SUCCESS | NO_TITLEBLOCK | FAILED | FAILED_INPUTS
finding_count: 0 | 1
---
```

The body table columns are:

```text
dwg_no | sheet_no | sheet_title | revision | area_or_module | drawing_family_proposal | titleblock_corner | confidence
```

`confidence` is `high`, `medium`, or `low`.

## Outputs

- Exactly one markdown stub at `OUTPUT_PATH`.
- Structured return values: `RUN_STATUS`, `PAGE_NUM`, `DWG_NO`, `DRAWING_FAMILY_PROPOSAL`, `CONFIDENCE`.

## Non-negotiable constraints

- One invocation handles one page.
- The skill reads only declared crop and thumbnail images.
- The skill writes only `OUTPUT_PATH`.
- `drawing_family_proposal` is always a proposal.
- Unknown or unreadable fields are `TBD`.
- `NO_TITLEBLOCK` is a valid non-error outcome.

## QA expectations

- Output file exists at `OUTPUT_PATH`.
- Frontmatter matches the run parameters.
- `finding_count=1` only when the body row contains a detected titleblock.
- `finding_count=0` for `NO_TITLEBLOCK`.
- `confidence` is one of `high`, `medium`, `low`.
- Table columns match the canonical schema.
