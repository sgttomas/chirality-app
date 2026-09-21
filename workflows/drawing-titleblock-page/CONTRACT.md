# drawing-titleblock-page contract

## Brief

Use this workflow with the TASK shell, dispatched by `drawing-extract` for one page of `DRAWING_SET/titleblock_index`.

### Required fields

| Field | Requirement |
|---|---|
| `Workflow` | `drawing-titleblock-page` |
| `AllowedWriteTargets` | Exactly `[RuntimeOverrides.OUTPUT_PATH]` |
| `RuntimeOverrides.SOURCE_PDF_NAME` | Source PDF basename |
| `RuntimeOverrides.PAGE_NUM` | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Positive integer |
| `RuntimeOverrides.CORNER_CROP_PATHS` | Mapping with `tl`, `tr`, `bl`, `br` image paths |
| `RuntimeOverrides.THUMBNAIL_PATH` | Full-page thumbnail image path |
| `RuntimeOverrides.OUTPUT_PATH` | Target `.md` path |
| `RuntimeOverrides.CORNER_CROP_GEOMETRY` | Mapping with `width_ratio`, `height_ratio` |

### Brief example

```md
PURPOSE: Extract drawing sheet titleblock metadata from page 8 of 94
RequestedBy: WORKING_ITEMS
ParentWorkflow: drawing-extract
ActingSurface: TASK+drawing-titleblock-page

ScopePath: /abs/path/to/work
Workflow: drawing-titleblock-page

AllowedWriteTargets:
  - "/abs/path/to/source/DRAWING_SET/titleblock_index/RUN-.../stem_page_0008_titleblock_stub.md"

RuntimeOverrides:
  SOURCE_PDF_NAME: MFS-242510_(3-25_Doe)_rA_IFI_(Permit_Application).pdf
  PAGE_NUM: 8
  TOTAL_PAGES: 94
  CORNER_CROP_PATHS:
    tl: /abs/path/to/work/page_0008_titleblock_tl.png
    tr: /abs/path/to/work/page_0008_titleblock_tr.png
    bl: /abs/path/to/work/page_0008_titleblock_bl.png
    br: /abs/path/to/work/page_0008_titleblock_br.png
  THUMBNAIL_PATH: /abs/path/to/work/page_0008_thumbnail.png
  OUTPUT_PATH: /abs/path/to/source/DRAWING_SET/titleblock_index/RUN-.../stem_page_0008_titleblock_stub.md
  CORNER_CROP_GEOMETRY:
    width_ratio: 0.25
    height_ratio: 0.25

ExpectedOutputs:
  - /abs/path/to/source/DRAWING_SET/titleblock_index/RUN-.../stem_page_0008_titleblock_stub.md
```

### Recommended CustomInstructions

- Use the full-page thumbnail only to orient the sheet and identify whether a titleblock exists.
- Read all four corner crops before deciding the titleblock corner.
- `drawing_family_proposal` is a proposal, not final operator scope.
- Unknown fields are `TBD`; do not infer from page order.
- `confidence` must be `high`, `medium`, or `low`.
- `NO_TITLEBLOCK` is valid and must use `finding_count: 0`.

## Acceptance

### Minimum checks

1. All four corner crop paths exist.
2. The thumbnail path exists.
3. `OUTPUT_PATH` has a `.md` extension and its parent exists.
4. Exactly one output file is written.
5. Frontmatter contains `drawing_type: DRAWING_SET` and `extraction_target: titleblock_index`.
6. `status` is one of `SUCCESS`, `NO_TITLEBLOCK`, `FAILED`, `FAILED_INPUTS`.
7. `finding_count` is `1` for `SUCCESS` and `0` for `NO_TITLEBLOCK`.
8. Body table columns match the canonical schema.
9. `confidence` is `high`, `medium`, or `low` when a row is emitted.

### Failure posture

- Invalid inputs produce `FAILED_INPUTS` and a failure stub.
- A readable page without a titleblock produces `NO_TITLEBLOCK`, not `FAILED`.
- Unreadable fields are `TBD`.

## Tool use

### Preferred tool order

Reasoning-first. The orchestrator prepares deterministic crops before dispatch. The workflow reads only the provided images and writes one stub.

### Allowed deterministic tools

#### Operationally invoked

- None. Crop preparation, validation, and assembly are orchestrator responsibilities.

### Expected use of reasoning

Use visual reasoning over the four corner crops and the full-page thumbnail to identify a titleblock and extract visible metadata. Leave unreadable values as `TBD`.

### Disallowed use

- No shell commands.
- No web access.
- No deterministic OCR invocation.
- No reading images outside the declared runtime overrides.
- No writing outside `OUTPUT_PATH`.

### Write boundary

The workflow writes exactly one file: `RuntimeOverrides.OUTPUT_PATH`.
