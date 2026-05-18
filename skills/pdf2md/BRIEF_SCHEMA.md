# pdf2md — Brief Schema

Use this skill with `TASK` like this:

```md
PURPOSE: Convert a bounded PDF reference to Markdown
RequestedBy: WORKING_ITEMS

ScopePath: /abs/path/to/source-folder-or-work-area
TaskSkill: pdf2md

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

## Required fields

- `TaskSkill: pdf2md`
- `RuntimeOverrides.PDF_PATH`
- `RuntimeOverrides.OUTPUT_PATH`

## Strongly recommended fields

- `AllowedTools`
- `RuntimeOverrides.WORK_DIR`
- `RuntimeOverrides.DPI`
- `CustomInstructions`

## Notes

- `ScopePath` should normally be the folder containing the PDF and outputs.
- `ApplyEdits: true` is appropriate because this skill is expected to write output artifacts.
