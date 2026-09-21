---
name: drawing-titleblock-page
description: Extract titleblock metadata from one drawing page using four corner crops and a full-page thumbnail, then write one governed sheet-inventory stub.
---

# Drawing Titleblock Page

Handle one page at a time. Require the source PDF name, one-indexed page number, total pages, `tl`/`tr`/`bl`/`br` crop paths, full-page thumbnail, crop geometry, and one authorized Markdown output path.

Read [references/stub-contract.md](references/stub-contract.md) before writing the stub; it preserves exact input validation and output shape.

Use the thumbnail to determine orientation and whether a titleblock exists, then inspect all four corner crops before choosing a corner. Extract only visible values for:

```text
dwg_no | sheet_no | sheet_title | revision | area_or_module | drawing_family_proposal | titleblock_corner | confidence
```

Use `TBD` for unreadable values. Never derive drawing or sheet numbers from page order. `drawing_family_proposal` is advisory and must be one of `PFD`, `P_AND_ID`, `ISOMETRIC`, `GA`, `OTHER`, `REFERENCE_OR_LEGEND`, or `TBD`. Confidence is `high`, `medium`, or `low`.

Write exactly one stub with YAML frontmatter containing `drawing_type: DRAWING_SET`, `extraction_target: titleblock_index`, source PDF and page, crop geometry, `status`, and `finding_count`. Valid statuses are `SUCCESS`, `NO_TITLEBLOCK`, `FAILED`, and `FAILED_INPUTS`. Use `finding_count: 1` only with a detected-titleblock row; a readable page with no titleblock is `NO_TITLEBLOCK` with `finding_count: 0`.

Read only the declared images and write only the declared output path. Return the run status, page number, drawing number, family proposal, and confidence. Do not inventory the full PDF, choose downstream scope, or accept a drawing-family classification.
