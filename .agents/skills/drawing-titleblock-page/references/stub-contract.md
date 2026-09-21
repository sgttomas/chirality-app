# Titleblock Stub Contract

## Input validation

Require an existing thumbnail and four existing crop images keyed exactly as `tl`, `tr`, `bl`, and `br`; positive integer page and total-page values; source PDF basename; numeric `width_ratio` and `height_ratio`; and an authorized `.md` output path. Missing or invalid inputs produce `FAILED_INPUTS` and a failure stub when the output path remains usable.

## Frontmatter

```yaml
---
drawing_type: DRAWING_SET
extraction_target: titleblock_index
source_pdf: <source PDF basename>
source_page: <one-indexed page number>
corner_crop_geometry:
  width_ratio: <supplied ratio>
  height_ratio: <supplied ratio>
status: SUCCESS | NO_TITLEBLOCK | FAILED | FAILED_INPUTS
finding_count: 0 | 1
---
```

## Findings table

Use exactly these columns, in order:

```text
dwg_no | sheet_no | sheet_title | revision | area_or_module | drawing_family_proposal | titleblock_corner | confidence
```

Emit one row only for `SUCCESS`. For `NO_TITLEBLOCK`, `FAILED`, and `FAILED_INPUTS`, use `finding_count: 0` and explain the outcome below the empty table. Use the supplied provenance values exactly. Unreadable extracted fields remain `TBD`.
