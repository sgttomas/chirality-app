# TOOL_POLICY

Preferred deterministic tools:

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
