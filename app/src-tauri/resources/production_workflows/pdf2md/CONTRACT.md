# pdf2md contract

## Brief

Use this workflow with `TASK` like this:

```md
PURPOSE: Convert a bounded PDF reference to Markdown
RequestedBy: WORKING_ITEMS

ScopePath: /abs/path/to/source-folder-or-work-area
Workflow: pdf2md

Tasks:
  - Convert the PDF to Markdown
  - Apply any page-specific interpretation rules from CustomInstructions

ApplyEdits: true
AllowedTools:
  - tools/pdf2md/rasterize_pdf.py
  - tools/pdf2md/postprocess_page.py
  - tools/pdf2md/assemble_markdown.py
  - tools/reporting/clean_pdf2md_output.py

RuntimeOverrides:
  PDF_PATH: /abs/path/to/file.pdf
  OUTPUT_PATH: /abs/path/to/file.md
  WORK_DIR: /abs/path/to/file_pdf2md_work
  DPI: 400
  PAGES: all
  SEPARATOR: ---

CustomInstructions:
  - Pages 6, 8, 9, 10, 12: express diagrams as semantic tagging logic
  - Pages 14-21: convert side-by-side tables to single vertical tables

ExpectedOutputs:
  - /abs/path/to/file.md
  - /abs/path/to/file_pdf2md_work/manifest.json
```

### Required fields

- `Workflow: pdf2md`
- `RuntimeOverrides.PDF_PATH`
- `RuntimeOverrides.OUTPUT_PATH`

### Strongly recommended fields

- `AllowedTools`
- `RuntimeOverrides.WORK_DIR`
- `RuntimeOverrides.DPI`
- `CustomInstructions`

### Notes

- `ScopePath` should normally be the folder containing the PDF and outputs.
- `ApplyEdits: true` is appropriate because this workflow is expected to write output artifacts.

## Acceptance

Minimum checks for a valid run:

1. `PDF_PATH` exists and is readable.
2. `OUTPUT_PATH` exists after the run and is non-empty.
3. `WORK_DIR/manifest.json` exists.
4. The run report states whether all pages were converted or whether partial success occurred.
5. If `CustomInstructions` mention special pages, those pages receive an explicit manual or interpretive pass.
6. Repeated headers/footers should be reduced where practical; obvious residual artifacts should be reported.

Recommended spot checks:

- first page
- one ordinary body-text page
- one page affected by `CustomInstructions`
- final page

Failure posture:

- If some pages cannot be interpreted, keep partial outputs, mark the failure explicitly, and do not pretend the document is complete.

## Tool use

### Preferred tool order

1. `tools/pdf2md/rasterize_pdf.py`
2. direct page interpretation by the agent
3. `tools/pdf2md/postprocess_page.py`
4. `tools/reporting/clean_pdf2md_output.py`
5. `tools/pdf2md/assemble_markdown.py`
6. final `tools/reporting/clean_pdf2md_output.py`

### Allowed deterministic tools

#### Operationally invoked

- None declared

### Expected use of reasoning

Reasoning is appropriate for:
- reconstructing diagram logic in prose, lists, or tables
- reflowing visually side-by-side tables into a different semantic layout when instructed
- spotting obvious OCR/interpretation defects

### Disallowed use

- No hidden reliance on tools outside the declared list unless the human expands `AllowedTools`.
- No sub-agent fanout under generic `TASK`.

### Write boundary

Writes should stay within:
- `OUTPUT_PATH`
- `WORK_DIR`
- or the `ScopePath` bounded local area

No writes elsewhere unless explicitly authorized by the brief.
