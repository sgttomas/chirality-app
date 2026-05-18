# pandid-valve-tile - QA Checks

## Minimum checks

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

## Reference-sheet handling

Reference, legend, symbol, and abbreviation pages return `NO_FINDINGS_REFERENCE` with `finding_count: 0` unless `ALLOW_REFERENCE_SHEETS=true`.

## Failure posture

- Invalid runtime inputs produce `FAILED_INPUTS`.
- Unreadable tile content produces `FAILED`.
- No valve candidates in the emit zone produces `NO_FINDINGS`.
- Unknown issue flags are warnings for deterministic validators, not page-worker failures.
