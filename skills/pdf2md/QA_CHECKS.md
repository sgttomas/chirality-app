# pdf2md — QA Checks

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
