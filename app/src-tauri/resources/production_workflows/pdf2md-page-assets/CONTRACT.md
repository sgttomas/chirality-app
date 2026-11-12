# pdf2md-page-assets contract

## Brief

Use this workflow with `TASK` like this. It is normally spawned by the `pdf2md-orchestration` orchestrator after the page has been transcribed and cleaned:

```md
PURPOSE: Identify extractable prose-document assets on one PDF page
RequestedBy: WORKING_ITEMS
ParentWorkflow: pdf2md-orchestration
ScopePath: /abs/path/to/pdf_work_dir
Workflow: pdf2md-page-assets

Tasks:
  - Read one page raster and its clean Markdown context
  - Identify visible figures, tables, and other meaningful images
  - Emit bbox-normalized asset records and table CSV text per the workflow contract

ApplyEdits: true

AllowedWriteTargets:
  - "/abs/path/to/pdf_work_dir/page_0003_assets.json"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/pdf_work_dir/page_0003.png
  PAGE_MD_PATH: /abs/path/to/pdf_work_dir/page_0003.md
  OUTPUT_PATH: /abs/path/to/pdf_work_dir/page_0003_assets.json
  DOC_STEM: MWK_1956
  PAGE_NUM: 3
  TOTAL_PAGES: 386
  ASSET_POLICY: prose-document-assets-v1

ExpectedOutputs:
  - /abs/path/to/pdf_work_dir/page_0003_assets.json
```

### Required fields

| Field | Value | Notes |
|---|---|---|
| `Workflow` | `pdf2md-page-assets` | Must match workflow folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to the page PNG | Must exist, must have `.png` extension |
| `RuntimeOverrides.PAGE_MD_PATH` | Absolute path to clean page Markdown | Must exist, must have `.md` extension |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path to page asset JSON | Parent directory must exist |
| `RuntimeOverrides.DOC_STEM` | Document stem | Used for context only; deterministic tools assign final IDs |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total pages in the document | Positive integer, >= `PAGE_NUM` |

### Optional fields

| Field | Default | Notes |
|---|---|---|
| `RuntimeOverrides.ASSET_POLICY` | `prose-document-assets-v1` | Policy label echoed into JSON |

### Read boundary

The workflow reads only:

- `{IMAGE_PATH}`
- `{PAGE_MD_PATH}`

It must not read neighbouring page images, manifests, sibling markdown, or public asset folders.

### Write boundary

The workflow writes only:

- `{OUTPUT_PATH}`

### AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only workflow with no deterministic tool dependencies.

### Recommended brief-builder

The orchestrator should prefer:

```sh
python3 tools/pdf2md/build_page_assets_brief.py --work-dir WORK_DIR --doc-stem DOC_STEM --page PAGE_NUM --total-pages TOTAL_PAGES
```

The brief-builder emits the required INIT-TASK shape and reduces prompt drift.

### CustomInstructions

Usually unnecessary. If used, keep them run-specific and do not restate the whole workflow contract. Good examples:

- "Treat cover-page publisher marks as `img`, not `fig`."
- "For tables, include the visible title/caption in `caption`; do not invent units."
- "If a table spans outside this page, extract only visible rows and add issue `possible_continuation`."

## Acceptance

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension, or the workflow returns `FAILED_INPUTS`.
2. `PAGE_MD_PATH` exists and has a `.md` extension, or the workflow returns `FAILED_INPUTS`.
3. `OUTPUT_PATH` parent directory exists before write.
4. `OUTPUT_PATH` exists after the run and is non-empty.
5. `OUTPUT_PATH` parses with `json.loads`.
6. No files other than `IMAGE_PATH` and `PAGE_MD_PATH` were read.
7. No files other than `OUTPUT_PATH` were written.

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

Each item in `assets` must satisfy:

| Field | Requirement |
|---|---|
| `kind` | Exactly `fig`, `tbl`, or `img` (STRICT: aliases like `figure`/`image`/`table`/`diagram`/`plot`/`chart`/`logo`/`photo` are rejected by the downstream `materialize_page_assets.py`; alternate keys `type`/`subtype` are also rejected) |
| `ordinal` | Positive integer within `(page, kind)` reading order |
| `caption` | Visible caption or concise visual description (STRICT: `caption` is the ONLY accepted field name — `title`/`label`/`name` are rejected) |
| `slug` | Short ASCII-friendly advisory slug, or blank if uncertain |
| `bbox_norm` | Four numbers `[x0, y0, x1, y1]`, top-left origin, each in `[0,1]`, with `x0 < x1` and `y0 < y1` (STRICT: must be a JSON array, NOT a dict `{"x0": ..., ...}`) |
| `confidence` | `high`, `medium`, or `low` |
| `table_data` | Required for `tbl` when legible — structured object conforming to the `pdf2md-table/v1` schema in `WORKFLOW.md` (STRICT: the legacy `csv_text` / `table_csv` fields are rejected by `materialize_page_assets.py`) |
| `needs_extraction` | Boolean, required on `tbl` entries that are visible but cannot be safely transcribed; in that case `table_data` MUST be omitted and an `issue` (e.g. `table_unreadable`) MUST be present |

#### `table_data` structural checks

When a `tbl` entry carries a `table_data` block, the materializer enforces:

- `schema_version` is exactly `"pdf2md-table/v1"`.
- `rows` is a non-empty JSON array; each row is `{"cells": [...]}` with `cells` a JSON array.
- `header_rows` is an integer in `[0, len(rows)]`.
- Every index in `section_dividers` is in `[0, len(rows))`.
- For each cell: `value` present; `row_span`/`col_span` (if present) are integers ≥ 1; `type` (if present) is one of `text|number|fraction|missing|formula|boolean`; `is_header` (if present) is boolean.
- Every `footnote_markers` entry on any cell appears in the table-level `footnotes` array's `marker` set.
- No row's `row_span` extends across a `section_dividers` boundary.
- `continuation_of` is either `null` or an object with `doc_stem` (string), `page` (int), `tbl_ordinal` (int).

### Top-level shape strictness enforced downstream

`tools/pdf2md/materialize_page_assets.py` validates and aborts with an explicit error pointing at the workflow contract if any of these shape defects are present:

- Top-level not a JSON object (must be a dict, not a list or scalar).
- Missing `assets` key.
- Sibling-keys legacy: `tables`, `figures`, or `images` appearing alongside `assets` at the top level. The canonical shape is the flat `assets: [...]` array; tables / figures / images are entries with `kind: "tbl" | "fig" | "img"`.
- `assets` not a JSON array.

The page-number field is `page` (not `page_num`).

### Inline placeholder drift (consumed by rewrite_inline_asset_refs.py)

The page Markdown emitted by the **`pdf2md-page` workflow** (not this workflow) carries the inline asset placeholders. Those placeholders MUST follow RULE 8 in `workflows/pdf2md-page/WORKFLOW.md`:

- `[FIGURE: <caption>]` — uppercase `FIGURE:` prefix is required.
- `[TABLE: <caption>]` — uppercase `TABLE:` prefix; appears immediately above the GFM/HTML transcription.
- `[<descriptor> <suffix>]` where suffix is one of `logo`/`emblem`/`seal`/`cover`/`photograph`/`photo`/`image`.

`tools/pdf2md/rewrite_inline_asset_refs.py` only rewrites these canonical shapes. Drift forms (e.g., `![Fig. 1.9 ...]` markdown-image syntax, bare-bracketed `[Fig. 1.1 ...]` without the `FIGURE:` prefix, lowercase prefixes) are surfaced as warnings on stderr — not silently rewritten — so the orchestrator and human reviewers can see when the `pdf2md-page` workflow drifts from RULE 8.

### Failure posture

| Failure mode | Required output |
|---|---|
| Missing input file | `run_status: "FAILED_INPUTS"`, empty `assets`, issue naming the missing input |
| No extractable assets | `run_status: "NO_ASSETS"`, empty `assets`, no invented placeholders |
| Unreadable page image | `run_status: "FAILED"`, empty `assets`, issue explaining the problem |
| Partial table uncertainty | `run_status: "SUCCESS"` with the table entry carrying `needs_extraction: true`, NO `table_data` block, and an explicit issue such as `table_unreadable` or `possible_continuation` |

### Orchestrator-side checks

These checks belong to `pdf2md-orchestration`, not this workflow:

- Running `materialize_page_assets.py` on every page asset JSON.
- Confirming crop PNGs exist for all non-skipped figure/image/table records.
- Confirming table XLSX files exist for table records that carry a `table_data` block (records flagged `needs_extraction: true` are exempt and do not require an XLSX).
- Aggregating the document asset manifest.
- Running `validate_assets.py` against the final assembled Markdown.
- Treating unresolved asset references as degraded output requiring human acknowledgment before downstream use.

## Tool use

### Preferred tool order

Reasoning-first: this workflow is VLM-driven. The agent reads the cleaned page Markdown for text context, then reads the page PNG as multimodal input, then writes one JSON file.

Deterministic tools run outside this workflow, under the `pdf2md-orchestration` orchestrator:

1. `tools/pdf2md/build_page_assets_brief.py` renders the dispatch brief.
2. `tools/pdf2md/materialize_page_assets.py` crops images, delegates to `render_table_xlsx.py` for table XLSX rendering, and writes anchored page Markdown.
3. `tools/pdf2md/render_table_xlsx.py` renders one deterministic XLSX per `table_data` block.
4. `tools/pdf2md/aggregate_asset_manifest.py` merges page manifests.
5. `tools/pdf2md/validate_assets.py` validates final references.

### Allowed deterministic tools

#### Operationally invoked

- None inside this workflow. Operational deterministic tools are invoked by `pdf2md-orchestration`, not by the page-assets worker.

### Expected use of reasoning

Reasoning is limited to visual asset identification, bounding-box estimation, caption/slug proposal, confidence labeling, and structured `table_data` transcription (rows, cells, merges, headers, footnotes, cell typing) from the visible page. The worker may use `PAGE_MD_PATH` only as context for visible captions or already-transcribed tables; the page image remains the authority for asset existence.

### Disallowed use

- MUST NOT crop images.
- MUST NOT write PNG files.
- MUST NOT write CSV or XLSX files.
- MUST NOT emit the legacy `csv_text` field — the canonical table representation is the structured `table_data` block defined in `WORKFLOW.md`.
- MUST NOT rewrite Markdown.
- MUST NOT aggregate manifests.
- MUST NOT validate final filesystem references.
- MUST NOT read files outside `IMAGE_PATH` and `PAGE_MD_PATH`.
- MUST NOT write files outside `OUTPUT_PATH`.
- MUST NOT assign final stable filenames.

### Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` - page-level asset JSON

The output filename is deterministic from the orchestrator brief. The workflow must not derive or modify it.
