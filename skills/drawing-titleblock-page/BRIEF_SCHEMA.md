# drawing-titleblock-page - Brief Schema

Use this skill with the TASK shell, dispatched by `DRAWING_EXTRACT` for one page of `DRAWING_SET/titleblock_index`.

## Required fields

| Field | Requirement |
|---|---|
| `TaskSkill` | `drawing-titleblock-page` |
| `AllowedWriteTargets` | Exactly `[RuntimeOverrides.OUTPUT_PATH]` |
| `RuntimeOverrides.SOURCE_PDF_NAME` | Source PDF basename |
| `RuntimeOverrides.PAGE_NUM` | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Positive integer |
| `RuntimeOverrides.CORNER_CROP_PATHS` | Mapping with `tl`, `tr`, `bl`, `br` image paths |
| `RuntimeOverrides.THUMBNAIL_PATH` | Full-page thumbnail image path |
| `RuntimeOverrides.OUTPUT_PATH` | Target `.md` path |
| `RuntimeOverrides.CORNER_CROP_GEOMETRY` | Mapping with `width_ratio`, `height_ratio` |

## Brief example

```md
PURPOSE: Extract drawing sheet titleblock metadata from page 8 of 94
RequestedBy: DRAWING_EXTRACT
ActingSurface: TASK+drawing-titleblock-page

ScopePath: /abs/path/to/work
TaskSkill: drawing-titleblock-page

AllowedWriteTargets:
  - "/abs/path/to/source/DRAWING_SET/titleblock_index/RUN-.../stem_page_0008_titleblock_stub.md"

RuntimeOverrides:
  SOURCE_PDF_NAME: MFS-242510_(3-25_Doe)_rA_IFI_(Permit_Application).pdf
  PAGE_NUM: 8
  TOTAL_PAGES: 94
  CORNER_CROP_PATHS:
    tl: /abs/path/to/work/page_0008_titleblock_tl.png
    tr: /abs/path/to/work/page_0008_titleblock_tr.png
    bl: /abs/path/to/work/page_0008_titleblock_bl.png
    br: /abs/path/to/work/page_0008_titleblock_br.png
  THUMBNAIL_PATH: /abs/path/to/work/page_0008_thumbnail.png
  OUTPUT_PATH: /abs/path/to/source/DRAWING_SET/titleblock_index/RUN-.../stem_page_0008_titleblock_stub.md
  CORNER_CROP_GEOMETRY:
    width_ratio: 0.25
    height_ratio: 0.25

ExpectedOutputs:
  - /abs/path/to/source/DRAWING_SET/titleblock_index/RUN-.../stem_page_0008_titleblock_stub.md
```

## Recommended CustomInstructions

- Use the full-page thumbnail only to orient the sheet and identify whether a titleblock exists.
- Read all four corner crops before deciding the titleblock corner.
- `drawing_family_proposal` is a proposal, not final operator scope.
- Unknown fields are `TBD`; do not infer from page order.
- `confidence` must be `high`, `medium`, or `low`.
- `NO_TITLEBLOCK` is valid and must use `finding_count: 0`.
