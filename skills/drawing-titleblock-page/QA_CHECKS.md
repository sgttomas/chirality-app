# drawing-titleblock-page - QA Checks

## Minimum checks

1. All four corner crop paths exist.
2. The thumbnail path exists.
3. `OUTPUT_PATH` has a `.md` extension and its parent exists.
4. Exactly one output file is written.
5. Frontmatter contains `drawing_type: DRAWING_SET` and `extraction_target: titleblock_index`.
6. `status` is one of `SUCCESS`, `NO_TITLEBLOCK`, `FAILED`, `FAILED_INPUTS`.
7. `finding_count` is `1` for `SUCCESS` and `0` for `NO_TITLEBLOCK`.
8. Body table columns match the canonical schema.
9. `confidence` is `high`, `medium`, or `low` when a row is emitted.

## Failure posture

- Invalid inputs produce `FAILED_INPUTS` and a failure stub.
- A readable page without a titleblock produces `NO_TITLEBLOCK`, not `FAILED`.
- Unreadable fields are `TBD`.
