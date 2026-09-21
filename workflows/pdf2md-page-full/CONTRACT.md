# pdf2md-page-full contract

## Brief

Use this workflow with `TASK` for one PDF page image when the worker must produce
both the Markdown transcription and the page asset JSON from a single vision
read.

```md
PURPOSE: Transcribe one PDF page and identify page assets
RequestedBy: WORKING_ITEMS
ParentWorkflow: pdf2md-orchestration
ScopePath: /abs/path/to/pdf_work_dir
Workflow: pdf2md-page-full

Tasks:
  - Read one page raster exactly once
  - Write the page Markdown transcription
  - Write the bbox-normalized page asset JSON

ApplyEdits: true

AllowedWriteTargets:
  - "/abs/path/to/pdf_work_dir/page_0003.md"
  - "/abs/path/to/pdf_work_dir/page_0003_assets.json"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/pdf_work_dir/page_0003.png
  OUTPUT_MD_PATH: /abs/path/to/pdf_work_dir/page_0003.md
  OUTPUT_JSON_PATH: /abs/path/to/pdf_work_dir/page_0003_assets.json
  DOC_STEM: MWK_1956
  PAGE_NUM: 3
  TOTAL_PAGES: 386
  ASSET_POLICY: prose-document-assets-v1

ExpectedOutputs:
  - /abs/path/to/pdf_work_dir/page_0003.md
  - /abs/path/to/pdf_work_dir/page_0003_assets.json
```

### Required fields

| Field | Value | Notes |
|---|---|---|
| `Workflow` | `pdf2md-page-full` | Must match workflow folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to page PNG | Must exist and end `.png` |
| `RuntimeOverrides.OUTPUT_MD_PATH` | Absolute path to page Markdown output | Parent directory must exist |
| `RuntimeOverrides.OUTPUT_JSON_PATH` | Absolute path to page asset JSON output | Parent directory must exist |
| `RuntimeOverrides.DOC_STEM` | Document stem | Used for downstream deterministic naming context |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total page count | Positive integer, >= `PAGE_NUM` |

### Optional fields

| Field | Default | Notes |
|---|---|---|
| `RuntimeOverrides.ASSET_POLICY` | `prose-document-assets-v1` | Policy label echoed into JSON |

### Read boundary

The workflow reads only:

- `{IMAGE_PATH}`

It must not read neighbouring page images, page Markdown, manifests, sibling
outputs, or public asset folders.

### Write boundary

The workflow writes only:

- `{OUTPUT_MD_PATH}`
- `{OUTPUT_JSON_PATH}`

### AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only workflow with no deterministic
tool dependency inside the TASK worker.

## Acceptance

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension, or the workflow returns
   `FAILED_INPUTS`.
2. `OUTPUT_MD_PATH` parent directory exists before write.
3. `OUTPUT_JSON_PATH` parent directory exists before write.
4. `OUTPUT_MD_PATH` exists after the run and is non-empty unless the page has no
   recoverable text, in which case it must contain the workflow's failure marker.
5. `OUTPUT_JSON_PATH` exists after the run, is non-empty, and parses with
   `json.loads`.
6. No task data outside `IMAGE_PATH` were read.
7. No files other than `OUTPUT_MD_PATH` and `OUTPUT_JSON_PATH` were written.

### Markdown checks

- Output is raw Markdown, not fenced in a Markdown code block.
- Reading order follows the visible page.
- Tables are transcribed as GFM or HTML tables and have a matching `[TABLE: ...]`
  placeholder.
- Figures use `[FIGURE: ...]` placeholders.
- Non-table/non-figure images use the descriptor placeholder forms defined in
  `WORKFLOW.md`.

### JSON shape checks

The output JSON must include:

| Field | Requirement |
|---|---|
| `schema_version` | `pdf2md-page-assets/v1` |
| `run_status` | `SUCCESS`, `NO_ASSETS`, `FAILED`, or `FAILED_INPUTS` |
| `doc_stem` | Echo of runtime override |
| `page` | Echo of `PAGE_NUM` |
| `total_pages` | Echo of `TOTAL_PAGES` |
| `asset_policy` | Echo of `ASSET_POLICY` or default |
| `assets` | List, possibly empty |
| `issues` | List, possibly empty |

### Asset row checks

Each item in `assets` must satisfy the same canonical shape used by
`pdf2md-page-assets`:

- `kind` is exactly `fig`, `tbl`, or `img`.
- `ordinal` is a positive integer within `(page, kind)` reading order.
- `caption` is the visible caption or concise visual description.
- `bbox_norm` is `[x0, y0, x1, y1]` with normalized coordinates and strict
  ordering.
- `confidence` is `high`, `medium`, or `low`.
- `tbl` entries use structured `table_data` when legible, or
  `needs_extraction: true` with an issue when not safely transcribable.

### Failure posture

| Failure mode | Required output |
|---|---|
| Missing image or invalid output paths | `FAILED_INPUTS` return; write the failure marker and JSON only to valid authorized targets, and report unavailable outputs |
| Page read succeeds but no assets exist | Markdown transcription plus JSON with `run_status: "NO_ASSETS"` and empty `assets` |
| Visual interpretation fails | Best-effort Markdown/failure marker plus JSON with `run_status: "FAILED"` and issue details |

## Tool use

### Preferred tool order

Reasoning-first: this workflow is VLM-driven. The worker reads the page PNG as
multimodal input once, then writes both output files.

Deterministic tools run outside this workflow, under the `pdf2md-orchestration` orchestrator:

1. `tools/pdf2md/build_page_full_brief.py` renders the dispatch brief.
2. `tools/pdf2md/postprocess_page.py` or `tools/reporting/clean_pdf2md_output.py`
   performs Markdown cleanup after the worker writes raw page Markdown.
3. `tools/pdf2md/materialize_page_assets.py` crops/render assets from the page
   asset JSON.
4. `tools/pdf2md/rewrite_inline_asset_refs.py` rewrites placeholders to
   materialized asset links.
5. `tools/pdf2md/aggregate_asset_manifest.py` and `tools/pdf2md/validate_assets.py`
   handle document-level manifest and validation work.

### Allowed deterministic tools

#### Operationally invoked

- None inside this workflow. Operational deterministic tools are invoked by
  `pdf2md-orchestration`, not by the page worker.

### Expected use of reasoning

Reasoning is limited to visual transcription, reading-order reconstruction,
asset identification, bbox estimation, caption/slug proposal, confidence
labeling, and structured table transcription from the visible page.

### Disallowed use

- Read task data only from `IMAGE_PATH`; role, workflow, and brief context are supplied separately.
- MUST NOT write any file other than `OUTPUT_MD_PATH` and `OUTPUT_JSON_PATH`.
- MUST NOT run deterministic tools.
- MUST NOT crop images, render XLSX files, rewrite Markdown links, assemble
  manifests, or validate final filesystem references.
- MUST NOT widen scope beyond the designated page.

### Write boundary

Writes are limited to exactly two files:

- `OUTPUT_MD_PATH`
- `OUTPUT_JSON_PATH`
