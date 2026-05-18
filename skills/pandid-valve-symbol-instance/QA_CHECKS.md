# QA_CHECKS

- Reject text-only observations as rows.
- Confirm every emitted row has integer page-global center and bounding-box coordinates.
- Confirm every counted row has a valve `symbol_class`, `count_include=true`, and `symbol_confidence` of `medium` or `high`.
- Keep tag evidence separate: `visible_tag_text` is only for `tag_status=true_tag`; line/spec text belongs in `nearby_line_text`.
- Treat tag-profile conflicts as review warnings only. They do not delete rows or alter symbol counts.
- Ensure `finding_count` equals the number of emitted rows for `SUCCESS`.
