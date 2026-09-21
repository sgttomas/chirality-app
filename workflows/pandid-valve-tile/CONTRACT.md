# pandid-valve-tile contract

## Brief

Use this workflow with TASK, dispatched by `drawing-extract` for one P&ID tile.

### Required fields

| Field | Requirement |
|---|---|
| `Workflow` | `pandid-valve-tile` |
| `AllowedWriteTargets` | Exactly `[RuntimeOverrides.OUTPUT_PATH]` |
| `RuntimeOverrides.SOURCE_PDF_NAME` | Source PDF basename |
| `RuntimeOverrides.PAGE_NUM` | Positive integer |
| `RuntimeOverrides.TILE_ID` | `page_NNNN_rRRcCC` |
| `RuntimeOverrides.TILE_IMAGE_PATH` | Existing tile PNG |
| `RuntimeOverrides.OUTPUT_PATH` | Target `.md` path |
| `RuntimeOverrides.MODE` | `basic` or `detailed` |
| `RuntimeOverrides.TILE_GEOMETRY` | Geometry metadata from `tile_manifest.json` |

### Optional fields

| Field | Meaning |
|---|---|
| `RuntimeOverrides.ALLOW_REFERENCE_SHEETS` | When true, do not self-skip reference sheets |
| `RuntimeOverrides.SCOPE_FILE` | Optional operator-selected page scope provenance |
| `RuntimeOverrides.BASIC_REFERENCE_RUN` | Optional detailed-mode provenance |
| `RuntimeOverrides.BASIC_COUNTS_CSV` | Optional detailed-mode provenance |

### Recommended CustomInstructions

- Use the whole tile image for context.
- Emit rows only for valve symbols whose visual center is inside the solid emit-zone border.
- Candidates visible outside the emit zone belong in notes only.
- Use the 5x5 grid overlay for `approx_location_in_emit_box`.
- Do not emit pixel coordinates.
- `issue_flags` is a list; empty is `[]`.
- Unknown/unreadable classification fields are `TBD`.
- If the tile is from a legend/reference/symbol sheet and `ALLOW_REFERENCE_SHEETS` is false, return `NO_FINDINGS_REFERENCE`.

### Brief example

```md
PURPOSE: Extract P&ID valve candidates from page 8 tile r02_c03
RequestedBy: WORKING_ITEMS
ParentWorkflow: drawing-extract
ActingSurface: TASK+pandid-valve-tile

ScopePath: /abs/path/to/work
Workflow: pandid-valve-tile

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

## Acceptance

### Minimum checks

1. `TILE_IMAGE_PATH` exists.
2. `OUTPUT_PATH` has a `.md` extension and parent directory exists.
3. `MODE` is `basic` or `detailed`.
4. `TILE_GEOMETRY` includes body, read, and emit boxes.
5. Exactly one output file is written.
6. Frontmatter matches runtime parameters.
7. `finding_count` equals emitted row count.
8. `approx_location_in_emit_box` is one of `A1..E5`.
9. `issue_flags` serializes as `[]` or `[FLAG_A, FLAG_B]`.
10. Basic mode does not emit detailed columns.
11. Detailed mode includes `valve_size_text`, `valve_type_code`, `valve_type_name`, and `actuation`.

### Reference-sheet handling

Reference, legend, symbol, and abbreviation pages return `NO_FINDINGS_REFERENCE` with `finding_count: 0` unless `ALLOW_REFERENCE_SHEETS=true`.

### Failure posture

- Invalid runtime inputs produce `FAILED_INPUTS`.
- Unreadable tile content produces `FAILED`.
- No valve candidates in the emit zone produces `NO_FINDINGS`.
- Unknown issue flags are warnings for deterministic validators, not page-worker failures.

## Tool use

### Preferred tool order

Reasoning-first. Deterministic tile preparation happens before dispatch. The workflow reads one prepared tile image and writes one stub.

### Allowed deterministic tools

#### Operationally invoked

- None. All deterministic operations are orchestrator/tool responsibilities.

### Expected use of reasoning

Use visual reasoning over the tile image to identify valve candidates, respect the emit-zone contract, and classify candidate fields according to the active mode.

### Disallowed use

- No shell commands.
- No web access.
- No deterministic OCR invocation.
- No reading images outside the declared tile input.
- No writing outside `OUTPUT_PATH`.
- No sub-agent fanout.

### Write boundary

The workflow writes exactly one file: `RuntimeOverrides.OUTPUT_PATH`.
