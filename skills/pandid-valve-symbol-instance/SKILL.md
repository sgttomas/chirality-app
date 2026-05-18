---
name: pandid-valve-symbol-instance
description: "Extract pixel-anchored P&ID valve symbol instances from prepared tiles using isolated-crop classification before any row may count."
compatibility: "TASK shell"
metadata:
  chirality-skill-version: "1.0.0"
  chirality-task-profile: DRAWING_EXTRACT
---
# pandid-valve-symbol-instance

## Purpose

Extract visible P&ID valve body symbol instances from one prepared tile. A row may exist only after an isolated symbol crop has been classified as a valve class. Text never produces rows, and tag profiles never delete rows.

## Protocol

1. Use the tile image only to detect plausible valve glyphs whose page-global center falls inside the emit box.
2. For each plausible glyph, reason from a tight isolated crop that excludes nearby line/spec/tag text as much as practical.
3. Emit one row per crop classified as a valve class. Use `count_include=true` only for valve classes with `symbol_confidence` of `medium` or `high`.
4. Do not emit text-only rows. Nearby line/spec text may populate `nearby_line_text` with `tag_status=line_spec_only` or `ambiguous` only after a valve row exists.
5. Use `visible_tag_text` only for actual valve/control-loop tags and set `tag_status=true_tag`.
6. Return `NO_FINDINGS_REFERENCE` for reference/legend sheets unless explicitly allowed by the brief.

## Output Contract

The output file is a markdown stub using `valve_schema_version: symbol_instance_v1` and the canonical table columns from `tools/drawing_extract/valve_stub_layout.py`.

Required row evidence:

- page-global `center_x_px`, `center_y_px`
- page-global `bbox_*_px`
- `symbol_crop_path`
- `symbol_class`
- `symbol_confidence`
- `count_include`
- `review_status`
- `review_reason`

Valid valve classes are `manual_block`, `manual_throttle`, `check`, `control`, `esd_block`, `relief`, and `specialty_valve`.
