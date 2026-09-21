# pandid-valve-symbol-instance contract

## Brief

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

## Acceptance

- Reject text-only observations as rows.
- Confirm every emitted row has integer page-global center and bounding-box coordinates.
- Confirm every counted row has a valve `symbol_class`, `count_include=true`, and `symbol_confidence` of `medium` or `high`.
- Keep tag evidence separate: `visible_tag_text` is only for `tag_status=true_tag`; line/spec text belongs in `nearby_line_text`.
- Treat tag-profile conflicts as review warnings only. They do not delete rows or alter symbol counts.
- Ensure `finding_count` equals the number of emitted rows for `SUCCESS`.

## Tool use

WORKING_ITEMS invokes these preparation, validation, and assembly tools around the bounded extraction. TASK receives the rendered output template and prepared images; any additional crop operation needs an explicit tool and write target in its brief:

- `tools/drawing_extract/build_pandid_valve_tile_brief.py`
- `tools/drawing_extract/validate_valve_tile_stub_format.py`
- `tools/drawing_extract/assemble_valve_candidates_csv.py`
- `tools/drawing_extract/assign_valve_symbol_geometry_duplicates.py`
- `tools/drawing_extract/aggregate_valve_counts.py`
- `tools/drawing_extract/flag_duplicate_valve_candidates.py`

Disallowed:

- Inferring a counted valve row from text patterns alone.
- Mutating raw candidate CSVs to encode later human review decisions.
- Auto-migrating legacy `pandid-valve-tile` stubs into `symbol_instance_v1`.
