# pandid-valve-tile - Brief Schema

Use this skill with TASK, dispatched by `DRAWING_EXTRACT` for one P&ID tile.

## Required fields

| Field | Requirement |
|---|---|
| `TaskSkill` | `pandid-valve-tile` |
| `AllowedWriteTargets` | Exactly `[RuntimeOverrides.OUTPUT_PATH]` |
| `RuntimeOverrides.SOURCE_PDF_NAME` | Source PDF basename |
| `RuntimeOverrides.PAGE_NUM` | Positive integer |
| `RuntimeOverrides.TILE_ID` | `page_NNNN_rRRcCC` |
| `RuntimeOverrides.TILE_IMAGE_PATH` | Existing tile PNG |
| `RuntimeOverrides.OUTPUT_PATH` | Target `.md` path |
| `RuntimeOverrides.MODE` | `basic` or `detailed` |
| `RuntimeOverrides.TILE_GEOMETRY` | Geometry metadata from `tile_manifest.json` |

## Optional fields

| Field | Meaning |
|---|---|
| `RuntimeOverrides.ALLOW_REFERENCE_SHEETS` | When true, do not self-skip reference sheets |
| `RuntimeOverrides.SCOPE_FILE` | Optional operator-selected page scope provenance |
| `RuntimeOverrides.BASIC_REFERENCE_RUN` | Optional detailed-mode provenance |
| `RuntimeOverrides.BASIC_COUNTS_CSV` | Optional detailed-mode provenance |

## Recommended CustomInstructions

- Use the whole tile image for context.
- Emit rows only for valve symbols whose visual center is inside the solid emit-zone border.
- Candidates visible outside the emit zone belong in notes only.
- Use the 5x5 grid overlay for `approx_location_in_emit_box`.
- Do not emit pixel coordinates.
- `issue_flags` is a list; empty is `[]`.
- Unknown/unreadable classification fields are `TBD`.
- If the tile is from a legend/reference/symbol sheet and `ALLOW_REFERENCE_SHEETS` is false, return `NO_FINDINGS_REFERENCE`.

## Brief example

```md
PURPOSE: Extract P&ID valve candidates from page 8 tile r02_c03
RequestedBy: DRAWING_EXTRACT
ActingSurface: TASK+pandid-valve-tile

ScopePath: /abs/path/to/work
TaskSkill: pandid-valve-tile

AllowedWriteTargets:
  - "/abs/path/to/source/P_AND_ID/valve_count_basic/RUN-.../stem_page_0008_tile_r02_c03_basic_stub.md"

RuntimeOverrides:
  SOURCE_PDF_NAME: MFS.pdf
  PAGE_NUM: 8
  TILE_ID: page_0008_r02_c03
  TILE_IMAGE_PATH: /abs/path/to/work/page_0008_tile_r02_c03.png
  OUTPUT_PATH: /abs/path/to/source/P_AND_ID/valve_count_basic/RUN-.../stem_page_0008_tile_r02_c03_basic_stub.md
  MODE: basic
  TILE_GEOMETRY:
    tile_grid: 5x4
    body_box_px: [100, 100, 6400, 4100]
    body_exclusions: [border, titleblock]
    read_box_px: [2300, 1000, 3900, 2300]
    emit_box_px: [2500, 1200, 3700, 2100]
    overlap_px: 200
    mini_grid: 5x5

ExpectedOutputs:
  - /abs/path/to/source/P_AND_ID/valve_count_basic/RUN-.../stem_page_0008_tile_r02_c03_basic_stub.md
```
