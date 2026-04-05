# pdf2md-page — QA Checks

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension (or `FAILED_INPUTS` is returned with a placeholder written to `OUTPUT_PATH`).
2. `OUTPUT_PATH` parent directory exists before the skill writes to it.
3. `OUTPUT_PATH` exists after the run and is non-empty.
4. No files other than `OUTPUT_PATH` were written.
5. No files other than `IMAGE_PATH` were read.
6. The output is raw VLM Markdown — no markdown fences, no commentary, no "Page X of Y" markers, no post-processing applied.

## Output content checks

The written Markdown at `OUTPUT_PATH` should satisfy:

| Check | Requirement |
|---|---|
| Content fidelity | All visible text, tables, and structural elements from the page image are represented |
| No invention | No content appears that is not visible in the image (no hallucinated URLs, text, or structure) |
| Heading hierarchy | At most one `#` title per page; subsequent headings use `##`, `###`, `####` |
| Table format | Tables use GFM pipe format with alignment markers, or HTML `<table>` when pipe format is insufficient |
| Code fencing | Code blocks use triple-backtick fences with language identifier; inline code uses single backticks |
| Formulas | Mathematical expressions use LaTeX delimiters (`$inline$`, `$$display$$`) |
| No page chrome | Page numbers, repeated headers/footers, and decorative borders are omitted |
| No output fences | The output is NOT wrapped in ` ```markdown ``` ` fences |

## Failure posture

If the input image cannot be read or its content cannot be interpreted, the skill still writes a placeholder to `OUTPUT_PATH`:

| Failure mode | Placeholder written | RUN_STATUS |
|---|---|---|
| `IMAGE_PATH` missing or not a `.png` | `*[Page {PAGE_NUM}: image not found]*` | `FAILED_INPUTS` |
| Image unreadable (blank page, unreadable scan, VLM cannot extract) | `*[Page {PAGE_NUM}: content not extractable]*` | `FAILED` |
| Conversion succeeded | (raw Markdown content) | `SUCCESS` |

`OUTPUT_PATH` is never left unwritten. The orchestrator relies on every per-page output existing so that assembly can account for the full page range.

## Success case

A clean run reports:

- `RUN_STATUS=SUCCESS`
- `PAGE_NUM` (the page number processed)
- `CHARS` (approximate character count of the output Markdown)
- `OUTPUT_PATH` (the exact file written)

## Orchestrator-side considerations

These checks are out of scope for this skill but are expected of the PDF2MD orchestrator that spawns it:

- Aggregating `RUN_STATUS` across all per-page invocations
- Reporting partial-success runs explicitly (listing pages with `FAILED` / `FAILED_INPUTS`)
- Running `postprocess_page.py` on raw per-page Markdown after fanout completes
- Running `assemble_markdown.py` to stitch per-page files into the final document
- Producing the final `manifest.json`

A `pdf2md-page` invocation is valid on its own merits when the checks above pass, regardless of the orchestrator's downstream handling.
