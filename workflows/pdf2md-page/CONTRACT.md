# pdf2md-page contract

## Brief

Use this workflow with `TASK` like this (typically spawned by the pdf2md-orchestration orchestrator, one invocation per page):

```md
PURPOSE: Convert one PDF page image to raw Markdown
RequestedBy: WORKING_ITEMS
ParentWorkflow: pdf2md-orchestration
ScopePath: /abs/path/to/pdf_work_dir
Workflow: pdf2md-page

Tasks:
  - Read the page image and transcribe its contents to Markdown per the 8 conversion rules

ApplyEdits: true

AllowedWriteTargets:
  - "/abs/path/to/pdf_work_dir/pages/page_003.md"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/pdf_work_dir/pages/page_003.png
  OUTPUT_PATH: /abs/path/to/pdf_work_dir/pages/page_003.md
  PAGE_NUM: 3
  TOTAL_PAGES: 42

ExpectedOutputs:
  - /abs/path/to/pdf_work_dir/pages/page_003.md
```

### Required fields

| Field | Value | Notes |
|---|---|---|
| `Workflow` | `pdf2md-page` | Must match workflow folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to the page PNG | Must exist, must have `.png` extension |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path to the page `.md` | Parent directory must exist |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total pages in the document | Positive integer, >= `PAGE_NUM` |

### Optional fields

None. This workflow has no optional brief fields and no optional runtime overrides.

### Read boundary

The workflow reads only:

- `{IMAGE_PATH}`

It must NOT read any other file, including neighbouring page images, manifests, or sibling markdown.

### Write boundary

The workflow writes only:

- `{OUTPUT_PATH}`

The output filename is deterministic — it is precisely the `OUTPUT_PATH` supplied in the brief. The workflow does not derive or modify the filename.

### AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only workflow with no deterministic tool dependencies; the workflow uses only the agent's native `Read` (multimodal) and `Write` tools.

### Notes

- `ScopePath` should normally be the PDF working directory so that `IMAGE_PATH` and `OUTPUT_PATH` both resolve within scope.
- `ApplyEdits: true` is appropriate because this workflow is expected to write the per-page Markdown artifact.
- One invocation processes one page. The pdf2md-orchestration orchestrator spawns one task per page for parallel fanout.
- The orchestrator is responsible for post-processing (`postprocess_page.py`), assembly (`assemble_markdown.py`), and final cleanup. This workflow emits raw VLM Markdown only.
- On any failure, the workflow still writes a placeholder line to `OUTPUT_PATH` so that the orchestrator's assembly step can account for the missing page.

## Acceptance

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension (or `FAILED_INPUTS` is returned with a placeholder written to `OUTPUT_PATH`).
2. `OUTPUT_PATH` parent directory exists before the workflow writes to it.
3. `OUTPUT_PATH` exists after the run and is non-empty.
4. No files other than `OUTPUT_PATH` were written.
5. No task data outside `IMAGE_PATH` were read.
6. The output is raw VLM Markdown — no markdown fences, no commentary, no "Page X of Y" markers, no post-processing applied.

### Output content checks

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

### Failure posture

If the input image cannot be read or its content cannot be interpreted, the workflow still writes a placeholder to `OUTPUT_PATH`:

| Failure mode | Placeholder written | RUN_STATUS |
|---|---|---|
| `IMAGE_PATH` missing or not a `.png` | `*[Page {PAGE_NUM}: image not found]*` | `FAILED_INPUTS` |
| Image unreadable (blank page, unreadable scan, VLM cannot extract) | `*[Page {PAGE_NUM}: content not extractable]*` | `FAILED` |
| Conversion succeeded | (raw Markdown content) | `SUCCESS` |

`OUTPUT_PATH` is never left unwritten. The orchestrator relies on every per-page output existing so that assembly can account for the full page range.

### Success case

A clean run reports:

- `RUN_STATUS=SUCCESS`
- `PAGE_NUM` (the page number processed)
- `CHARS` (approximate character count of the output Markdown)
- `OUTPUT_PATH` (the exact file written)

### Orchestrator-side considerations

These checks are out of scope for this workflow but are expected of the pdf2md-orchestration orchestrator that spawns it:

- Aggregating `RUN_STATUS` across all per-page invocations
- Reporting partial-success runs explicitly (listing pages with `FAILED` / `FAILED_INPUTS`)
- Running `postprocess_page.py` on raw per-page Markdown after fanout completes
- Running `assemble_markdown.py` to stitch per-page files into the final document
- Producing the final `manifest.json`

A `pdf2md-page` invocation is valid on its own merits when the checks above pass, regardless of the orchestrator's downstream handling.

## Tool use

### Preferred tool order

Reasoning-first: this workflow is LLM-driven; no deterministic tool ordering applies. The agent uses its native Read tool to load the page PNG as multimodal (vision) input, performs VLM transcription of the image contents to Markdown, and uses its native Write tool to produce the single output file.

### Allowed deterministic tools

#### Operationally invoked

- None — no operational helpers declared (WORKFLOW.md states: "No deterministic tools. This is a VLM-reasoning-only workflow"; post-processing is pdf2md-orchestration's responsibility)

### Expected use of reasoning

This is a VLM-reasoning-only workflow. The agent's entire value is the multimodal perception step: reading a page image and transcribing its contents to Markdown. Reasoning governs input validation, image examination, Markdown structuring per the declared rules (text preservation, structure, tables, code, formulas, ignore-list, output format), and failure-placeholder handling. All cleanup, coordination, and assembly belong to the pdf2md-orchestration orchestrator and are out of scope for this workflow.

### Disallowed use

- MUST NOT run `postprocess_page.py` or any other cleanup tool. Post-processing is pdf2md-orchestration's responsibility.
- Read task data only from `IMAGE_PATH`; role, workflow, and brief context are supplied separately.
- MUST NOT write any file other than `OUTPUT_PATH`.
- MUST NOT widen scope beyond the designated page.
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

### Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` — the page Markdown (or a failure placeholder)

The output filename is deterministic: it is precisely `OUTPUT_PATH` as provided in the brief. The workflow does not derive or modify the filename.
