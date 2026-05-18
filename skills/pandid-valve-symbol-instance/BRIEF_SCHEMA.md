# BRIEF_SCHEMA

Required fields:

- `SOURCE_PDF_NAME`
- `PAGE_NUM`
- `TILE_ID`
- `SOURCE_RASTER_PATH`
- `TILE_IMAGE_PATH`
- `OUTPUT_PATH`
- `MODE`: `basic` or `detailed`
- `TILE_GEOMETRY`: `tile_grid`, `body_box_px`, `body_exclusions`, `read_box_px`, `emit_box_px`, `overlap_px`, `mini_grid`

Optional fields:

- `ALLOW_REFERENCE_SHEETS`
- `SCOPE_FILE`
- `BASIC_REFERENCE_RUN`
- `BASIC_COUNTS_CSV`

The brief must include the canonical output template rendered by `build_pandid_valve_tile_brief.py`.
