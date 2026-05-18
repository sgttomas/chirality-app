---
name: pdf2md-page-assets
description: Identify visible figures, tables, and meaningful images on one rasterized prose PDF page and emit bbox-normalized asset records for deterministic materialization.
compatibility: Chirality TASK; invoked by PDF2MD asset-enabled mode after per-page Markdown cleanup.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - pdf2md-page-assets

## Purpose

Identify extractable assets on one rasterized prose-document PDF page:

- `fig` - captioned figures, diagrams, plots, charts, plates, or illustrations
- `tbl` - tabular data that should exist as a structured, auditable artifact (rendered as XLSX downstream)
- `img` - meaningful non-figure images such as logos, covers, photographs, or uncaptioned visual objects

The skill reads one page image plus that page's cleaned Markdown context and writes one JSON file. It does not crop images, render XLSX files, rewrite Markdown links, assemble manifests, or validate filesystem references. Those are deterministic PDF2MD tool responsibilities.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `PDF2MD` orchestrator

Not the right fit for:

- whole-PDF conversion
- cross-page asset stitching
- deterministic filename assignment
- cropping, XLSX file creation, Markdown rewriting, or manifest aggregation

## Inputs

Required runtime overrides:

- `IMAGE_PATH` - absolute path to the page PNG
- `PAGE_MD_PATH` - absolute path to the cleaned per-page Markdown
- `OUTPUT_PATH` - absolute path for the asset JSON
- `DOC_STEM` - document stem used by downstream deterministic naming tools
- `PAGE_NUM` - 1-indexed page number
- `TOTAL_PAGES` - total pages in the document

Optional runtime overrides:

- `ASSET_POLICY` - policy label; default `prose-document-assets-v1`

## Read boundary

Reads are limited to exactly two files:

- `{IMAGE_PATH}`
- `{PAGE_MD_PATH}`

Do not read neighbouring pages, manifests, sibling Markdown files, or previously materialized assets. This preserves page-level parallelism.

## Write boundary

Writes are limited to exactly one file:

- `{OUTPUT_PATH}`

The output filename is supplied by the orchestrator and must not be derived or changed by the skill.

## Tool usage

- No deterministic tools.
- The `allowed-tools` frontmatter field is intentionally omitted.
- The agent uses native multimodal reading for `IMAGE_PATH`, native text reading for `PAGE_MD_PATH`, and native writing for `OUTPUT_PATH`.

Disallowed behavior:

- Do not crop images.
- Do not write PNG, CSV, or XLSX files.
- Do not emit the legacy `csv_text` field on table records — the canonical table representation is the structured `table_data` block (see Step 3).
- Do not rewrite page Markdown.
- Do not assign final filenames.
- Do not widen read or write scope beyond the declared page files.

## Method

### Step 1 - Validate inputs

1. Confirm `IMAGE_PATH` exists and has a `.png` extension.
2. Confirm `PAGE_MD_PATH` exists and has a `.md` extension.
3. Confirm `OUTPUT_PATH` parent exists.
4. If required inputs are missing, write a valid JSON file with `run_status: "FAILED_INPUTS"` and an empty `assets` list.

### Step 2 - Inspect the page

1. Read `PAGE_MD_PATH` first to understand whether captions or inline tables already appear in text.
2. Read `IMAGE_PATH` and inspect the page visually.
3. Identify every visible asset that should remain auditable outside plain Markdown.
4. Preserve document reading order within each page.

### Step 3 - Emit JSON

Write only JSON, with no Markdown fences or commentary.

**REQUIRED EXACT VALUES — do not substitute synonyms or restructure.** The downstream materializer relies on these exact field names, types, and string literals:

- Top-level field names are exactly: `schema_version`, `run_status`, `doc_stem`, `page` (NOT `page_num`), `total_pages`, `asset_policy`, `assets`, `issues`.
- `schema_version` MUST be the literal string `"pdf2md-page-assets/v1"`.
- `run_status` MUST be one of the four uppercase literals: `"SUCCESS"`, `"NO_ASSETS"`, `"FAILED"`, `"FAILED_INPUTS"`. Do NOT use `"ok"`, `"success"`, `"done"`, etc.
- `assets` is a flat array. Do NOT add a sibling `tables: [...]` array; tables are entries inside `assets` with `kind: "tbl"`.
- Per-asset `kind` MUST be one of the three 3-letter literals: `"fig"`, `"tbl"`, or `"img"`. Do NOT use `"figure"`, `"image"`, `"table"`, `"diagram"`, `"plot"`, `"chart"`, `"logo"`, `"photo"`, etc.
- Per-asset `bbox_norm` MUST be a 4-element JSON array `[x0, y0, x1, y1]`. Do NOT emit a JSON object with named keys like `{"x0": ..., "y0": ..., "x1": ..., "y1": ...}`.
- Per-asset captions go in the `caption` field (NOT `label`, `title`, or `name`).
- `bbox_norm` should generously include the full asset AND its visible caption AND a small margin (~3-5% of page on each side). It is far better to include an extra few percent of whitespace than to clip the figure or caption text.

Example:

```json
{
  "schema_version": "pdf2md-page-assets/v1",
  "run_status": "SUCCESS",
  "doc_stem": "MWK_1956",
  "page": 3,
  "total_pages": 386,
  "asset_policy": "prose-document-assets-v1",
  "assets": [
    {
      "kind": "fig",
      "ordinal": 1,
      "caption": "Yield stress-strain curve of copper in compression",
      "slug": "yield-stress-strain-copper",
      "bbox_norm": [0.11, 0.18, 0.88, 0.55],
      "confidence": "medium",
      "notes": "Caption visible below plot"
    },
    {
      "kind": "tbl",
      "ordinal": 1,
      "caption": "Creep strength ratios",
      "slug": "creep-strength-ratios",
      "bbox_norm": [0.08, 0.22, 0.91, 0.64],
      "table_data": {
        "schema_version": "pdf2md-table/v1",
        "header_rows": 1,
        "section_dividers": [],
        "continuation_of": null,
        "footnotes": [],
        "rows": [
          { "cells": [
            { "value": "Material", "is_header": true },
            { "value": "Ratio", "is_header": true }
          ] },
          { "cells": [
            { "value": "Carbon steel", "type": "text" },
            { "value": 1.0, "type": "number" }
          ] }
        ]
      },
      "confidence": "medium",
      "notes": "Simple two-column table"
    }
  ],
  "issues": []
}
```

## The `table_data` block (canonical table representation)

For every `kind: "tbl"` asset that is legibly extractable, emit a `table_data` object. The block is the canonical hashable artifact for the table — downstream tools (`materialize_page_assets.py` → `render_table_xlsx.py`) render the XLSX from this block deterministically.

If the table is visible (bbox identifiable) but the cells cannot be transcribed with confidence, omit `table_data` entirely and emit `"needs_extraction": true` on the entry plus an `issue` such as `table_unreadable`. Do NOT emit a partial or guessed `table_data`.

### Table-level fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | string | yes | MUST be the literal `"pdf2md-table/v1"` |
| `header_rows` | int | yes | Count of leading rows that are headers (≥ 0; ≤ `len(rows)`) |
| `section_dividers` | array of int | yes | Row indices where a visible internal section break appears; empty array if none. No merge may cross a divider. |
| `continuation_of` | object or null | yes | `null` for standalone tables. Set to `{"doc_stem": "...", "page": N, "tbl_ordinal": M}` when this table is the continuation of a table on an earlier page. |
| `footnotes` | array of `{marker, text}` | yes | Empty array if none. `marker` is the literal string (e.g. `"*"`, `"a"`, `"1"`) that appears on cells referencing this footnote. |
| `rows` | array of row objects | yes | At least one row when the table is extractable. |

### Row + cell shape

Each row is `{ "cells": [...] }`. Each cell is an object with these fields:

| Field | Type | Default | Notes |
|---|---|---|---|
| `value` | primitive or null | (required) | JSON primitive: string / number / boolean / null. Use `null` only when `type` is `"missing"`. |
| `row_span` | int | `1` | Omit when 1. Cells covered by a span do NOT appear separately. |
| `col_span` | int | `1` | Omit when 1. |
| `is_header` | bool | `false` | Header cells are bolded by the renderer. Omit when false. |
| `type` | string | `"text"` | One of: `text`, `number`, `fraction`, `missing`, `formula`, `boolean`. |
| `unit` | string | (omitted) | Optional unit string for typed numerics (e.g. `"psig"`, `"°F"`, `"in"`). |
| `raw` | string | (omitted) | Optional verbatim VLM-perceived text. Preserve when typing alters the surface form (e.g. `raw: "1-1/2\""` with `value: "1-1/2"`, `type: "fraction"`). |
| `footnote_markers` | array of string | (omitted) | List of `marker` strings (matching entries in the table-level `footnotes`) attached to this cell. |

### Cell type semantics

- `text` — free-form string. Default.
- `number` — JSON number. Use for clean numeric values; pair with `unit` when a unit is shown.
- `fraction` — string carrying a mixed fraction the renderer must keep as text (e.g. `"1-1/2"`, `"3/8"`). Use `raw` to preserve quote-as-inch markers.
- `missing` — `value: null`. Use `raw` to record the surface marker (`"—"`, `"N/A"`, blank).
- `formula` — string formula that should remain a string (e.g. `"=A1*B1"` from the source — rare).
- `boolean` — JSON true/false (e.g. checkmarks vs. blanks).

### Structural rules

- `len(rows) >= 1` when `table_data` is present.
- `header_rows` is between `0` and `len(rows)` inclusive.
- Every `section_dividers` index is in `[0, len(rows))`.
- For each row, the sum of `col_span` across emitted cells (plus cells covered by upstream `col_span`/`row_span`) equals the table column count.
- `row_span` may not cross a `section_dividers` boundary.
- Every `footnote_markers` entry must appear in the table-level `footnotes` array.
- `continuation_of.doc_stem` should match the current `doc_stem` unless the table truly originates from a different source document (rare).

### Worked example with merges, multi-row header, fractions, missing, footnote

```json
"table_data": {
  "schema_version": "pdf2md-table/v1",
  "header_rows": 2,
  "section_dividers": [],
  "continuation_of": null,
  "footnotes": [
    { "marker": "*", "text": "Values at standard conditions" }
  ],
  "rows": [
    { "cells": [
      { "value": "Pipe Size", "row_span": 2, "is_header": true },
      { "value": "Rating",    "col_span": 2, "is_header": true }
    ] },
    { "cells": [
      { "value": "psig", "is_header": true },
      { "value": "°F",   "is_header": true }
    ] },
    { "cells": [
      { "value": "1-1/2", "type": "fraction", "raw": "1-1/2\"" },
      { "value": 150,     "type": "number",   "unit": "psig" },
      { "value": null,    "type": "missing",  "raw": "—", "footnote_markers": ["*"] }
    ] }
  ]
}
```

## Output rules

- `kind` must be exactly `fig`, `tbl`, or `img`.
- `ordinal` is 1-indexed within `(page, kind)` in reading order.
- `caption` should use the visible caption when present; otherwise use a concise visual description.
- `slug` is advisory only. Downstream tools normalize it and append it to a stable ID.
- `bbox_norm` is `[x0, y0, x1, y1]` in normalized page coordinates, top-left origin, values between 0 and 1. It MUST be a 4-element JSON array, NOT a dict.
- `bbox_norm` MUST include the full asset, the visible caption, AND a small margin of whitespace (~3-5% of page width/height) around both. Generous bboxes are preferred — clipped figures or truncated captions are a defect; including a little extra surrounding whitespace is fine.
- `table_data` is required for `tbl` when the table is legibly extractable. The block MUST conform to the schema documented above.
- `needs_extraction: true` is required on `tbl` entries where the table is visible but cannot be safely transcribed; in that case `table_data` MUST be omitted entirely.
- The legacy `csv_text` field is REMOVED. Do not emit it; downstream materialization will reject any record carrying it.
- If no assets are visible, return `run_status: "NO_ASSETS"` with an empty `assets` list.

## Non-negotiable constraints

- Single page in, one JSON out.
- No cross-page context.
- No final filename assignment.
- No asset materialization.
- No invented assets or table values.
- Every emitted asset must be visible on the page image.
- The JSON must parse with standard `json.loads`.

## QA expectations

- `OUTPUT_PATH` exists and is non-empty.
- JSON parses successfully.
- `run_status` is one of `SUCCESS`, `NO_ASSETS`, `FAILED`, or `FAILED_INPUTS`.
- Every asset has valid `kind`, `ordinal`, `caption`, `bbox_norm`, and `confidence`.
- Table assets include either a schema-conforming `table_data` block OR `needs_extraction: true` with an explicit issue explaining why structured extraction was not safe.
