---
name: pdf2md-page-full
description: Single-page merged VLM pass that produces BOTH the raw Markdown transcription and the bbox-normalized asset JSON from one vision read of the page image. Replaces the prior two-skill split (pdf2md-page + pdf2md-page-assets) for new dispatches.
compatibility: Chirality TASK; invoked by PDF2MD orchestrator for per-page fanout
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — pdf2md-page-full

## Purpose

Convert **one PDF page image** to BOTH:

1. clean, well-structured Markdown (text + structure + asset placeholders), and
2. a strict-schema asset JSON identifying every visible figure, table, and meaningful image with normalized bounding boxes.

A single multimodal `Read` of the page image produces both outputs. This replaces the prior two-pass design (`pdf2md-page` for Markdown, `pdf2md-page-assets` for asset JSON) — halving Sonnet dispatches per page without sacrificing the contracts that downstream deterministic tools depend on.

Both output schemas are unchanged from the prior split skills, so `postprocess_page.py`, `clean_pdf2md_output.py`, `filter_logo_assets.py`, `materialize_page_assets.py`, `rewrite_inline_asset_refs.py`, `aggregate_asset_manifest.py`, and `validate_assets.py` consume the outputs of this skill with no modification.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the PDF2MD orchestrator

Not the right fit for:
- whole-PDF conversion (use the full PDF2MD persona)
- post-processing, cleanup, materialization, or assembly (PDF2MD's deterministic tools handle those)
- any task that needs cross-page context

## Relationship to `pdf2md-page` and `pdf2md-page-assets`

The two predecessor skills remain on disk for legacy compatibility and for resuming any PDF that was processed under the split contract. New dispatches should use this merged skill.

- `pdf2md-page` — DEPRECATED for new runs. Same Markdown contract as Output A here.
- `pdf2md-page-assets` — DEPRECATED for new runs. Same JSON contract as Output B here, with one input-boundary difference: the merged skill does NOT read a page Markdown sidecar (there is none yet — both outputs are produced together from the image alone).

## Inputs

### Required runtime overrides

| Key | Meaning |
|---|---|
| `IMAGE_PATH` | Absolute path to the page PNG file. Must exist; must end `.png`. |
| `OUTPUT_MD_PATH` | Absolute path where the page Markdown will be written. Parent dir must exist. |
| `OUTPUT_JSON_PATH` | Absolute path where the asset JSON will be written. Parent dir must exist. |
| `DOC_STEM` | Document stem used by downstream deterministic naming tools. |
| `PAGE_NUM` | 1-indexed page number. |
| `TOTAL_PAGES` | Total page count. Positive integer, ≥ `PAGE_NUM`. |

### Optional runtime overrides

| Key | Default | Notes |
|---|---|---|
| `ASSET_POLICY` | `prose-document-assets-v1` | Policy label recorded in the asset JSON. |

## Read boundary

Reads are limited to exactly one file:

- `{IMAGE_PATH}` — the single page PNG.

The skill MUST NOT read any other file. Zero cross-page context. No sibling page Markdown.

## Write boundary

Writes are limited to exactly two files:

- `{OUTPUT_MD_PATH}` — page Markdown (or a failure placeholder line)
- `{OUTPUT_JSON_PATH}` — page asset JSON (always valid JSON, even on failure)

The filenames are deterministic — exactly as provided in the brief.

## Tool usage

- No deterministic tools. This is a VLM-reasoning-only skill.
- The `allowed-tools` frontmatter field is intentionally omitted.
- The agent uses its native `Read` tool for multimodal PNG input and its native `Write` tool for both output files.

Disallowed behavior:
- MUST NOT run `postprocess_page.py` or any other cleanup tool. Post-processing is PDF2MD's responsibility.
- MUST NOT read any file other than `IMAGE_PATH`.
- MUST NOT write any file other than `OUTPUT_MD_PATH` and `OUTPUT_JSON_PATH`.
- MUST NOT widen scope beyond the designated page.
- MUST NOT crop the image, render XLSX, rewrite Markdown link targets, or assemble manifests.

## Method

### Step 1 — Validate inputs

1. Confirm `IMAGE_PATH` exists and is a `.png` file.
2. Confirm `OUTPUT_MD_PATH` parent directory exists.
3. Confirm `OUTPUT_JSON_PATH` parent directory exists.
4. On failure: write `*[Page {PAGE_NUM}: image not found]*` to `OUTPUT_MD_PATH`, write a valid-JSON failure record (see Output B, `run_status: "FAILED_INPUTS"`, empty `assets`) to `OUTPUT_JSON_PATH`, and return `RUN_STATUS=FAILED_INPUTS`.

### Step 2 — Single vision read

Use the `Read` tool ONCE to load `IMAGE_PATH` as multimodal input. Examine the page image and prepare both outputs from this single vision pass — do not re-read the image. Both outputs must be consistent with each other: every `[FIGURE: …]` / `[TABLE: …]` / `[<descriptor> logo|emblem|seal|cover|photograph|photo|image]` placeholder emitted in the Markdown MUST have a corresponding entry in the asset JSON, and vice versa.

### Step 3 — Produce Output A (Markdown)

Transcribe the page contents to Markdown following these rules precisely.

**RULE 1 — TEXT PRESERVATION**
- Preserve ALL text content completely and accurately.
- Maintain the reading order as a human would read the page.
- Correct obvious OCR-like errors only if you are completely certain.

**RULE 2 — STRUCTURE**
- Use `#` for the main page title (at most one per page).
- Use `##` for major sections, `###` for subsections, `####` for minor headings.
- Use `-` for unordered lists and `1. 2. 3.` for ordered lists.
- Preserve list nesting with indentation.
- Use `**bold**` and `*italic*` to match the visual emphasis.

**RULE 3 — TABLES**
- Convert tables to GFM pipe format.
- Add alignment markers (`:---`, `:---:`, `---:`) matching visual alignment.
- If a table is too complex for pipe format, use HTML `<table>` markup.
- Also emit a `[TABLE: <visible caption>]` placeholder line immediately above the GFM/HTML transcription, per RULE 8. The inline GFM and the placeholder are both required.

**RULE 4 — CODE**
- Wrap code blocks in triple backticks with language identifier.
- Wrap inline code in single backticks.

**RULE 5 — FORMULAS**
- Render mathematical expressions using LaTeX: `$inline$` and `$$display$$`.

**RULE 6 — WHAT TO IGNORE**
- Page numbers (bottom/top of page).
- Repeated headers/footers that appear on every page.
- Decorative borders and lines that carry no content meaning.

**RULE 7 — OUTPUT FORMAT**
- Output ONLY the Markdown content to `OUTPUT_MD_PATH`.
- Do NOT wrap in ` ```markdown ``` ` fences.
- Do NOT add commentary or explanations.
- Do NOT add "Page X of Y" markers.
- Start directly with the page content.

**RULE 8 — ASSET PLACEHOLDERS**

Every visible figure, table, or non-text image on the page MUST be marked with a deterministic placeholder so downstream tooling (`tools/pdf2md/rewrite_inline_asset_refs.py`) can rewrite each placeholder to a working asset link. Placeholders are part of the Markdown content (RULE 7 still applies — no external commentary), and they appear in document reading order at the position of the asset on the page.

Required placeholder formats:

- **Figures (captioned plots, diagrams, charts, schematics, illustrations):**
  - Format: `[FIGURE: <full visible caption text including the figure number>]`
  - Example: `[FIGURE: Fig. 1.1 Yield stress-strain curve of copper in compression. After Cook and Larke [1].]`
  - One placeholder per visible figure. If a caption spans multiple lines on the page, join them into one line inside the brackets.
  - The leading `FIGURE:` token is REQUIRED — it is what the downstream rewriter keys on. Do not substitute `Figure:` (camelcase), `FIG:`, or omit it. Citations like `[1]` inside the caption are fine; the rewriter handles one level of nested brackets.

- **Tables (any tabular data, captioned or not):**
  - Format: `[TABLE: <full visible caption text, OR a brief summary if no caption>]`
  - Example: `[TABLE: Table 4.2 Comparison of stress values - Guided Cantilever vs General Analytical]`
  - The placeholder appears IMMEDIATELY ABOVE the GFM/HTML transcription required by RULE 3. Both surfaces are required: the placeholder for the asset rewriter, the GFM/HTML for human readability.
  - The leading `TABLE:` token is REQUIRED.

- **Non-figure non-table images (cover logos, decorative emblems, photographs, equation plates, etc.):**
  - Format: `[<short descriptor> logo]` / `[<descriptor> emblem]` / `[<descriptor> seal]` / `[<descriptor> cover]` / `[<descriptor> photograph]` / `[<descriptor> photo]` / `[<descriptor> image]`.
  - Example: `[Kellogg logo]`, `[Cover image]`, `[ASME emblem]`.
  - Use the trailing keyword that best describes the asset. The rewriter recognizes `logo`, `emblem`, `seal`, `cover`, `photograph`, `photo`, and `image`.

What MUST NOT happen in the Markdown:

- Do NOT describe a figure or table only in prose ("As shown in Fig. 1.4, the curve...") without also emitting the bracketed placeholder.
- Do NOT use `![Fig. ...](...)` markdown-image syntax for figures — use `[FIGURE: ...]`.
- Do NOT skip the placeholder for cover-page logos or other one-off images on the assumption that they are "decorative" (RULE 6 ignores page numbers and repeating headers/footers, NOT one-off images).
- Do NOT invent placeholders for assets that are not visible on the page.

### Step 4 — Produce Output B (asset JSON)

Write only JSON, with no Markdown fences or commentary, to `OUTPUT_JSON_PATH`.

**REQUIRED EXACT VALUES — do not substitute synonyms or restructure.** The downstream materializer (`tools/pdf2md/materialize_page_assets.py`) relies on these exact field names, types, and string literals:

- Top-level field names are exactly: `schema_version`, `run_status`, `doc_stem`, `page` (NOT `page_num`), `total_pages`, `asset_policy`, `assets`, `issues`.
- `schema_version` MUST be the literal string `"pdf2md-page-assets/v1"`. (The merged skill emits the SAME schema as the predecessor `pdf2md-page-assets` so downstream tools are unchanged.)
- `run_status` MUST be one of the four uppercase literals: `"SUCCESS"`, `"NO_ASSETS"`, `"FAILED"`, `"FAILED_INPUTS"`. Do NOT use `"ok"`, `"success"`, `"done"`, etc.
- `assets` is a flat array. Do NOT add a sibling `tables: [...]` array; tables are entries inside `assets` with `kind: "tbl"`.
- Per-asset `kind` MUST be one of the three 3-letter literals: `"fig"`, `"tbl"`, or `"img"`. Do NOT use `"figure"`, `"image"`, `"table"`, `"diagram"`, `"plot"`, `"chart"`, `"logo"`, `"photo"`, etc.
- Per-asset `bbox_norm` MUST be a 4-element JSON array `[x0, y0, x1, y1]` in normalized page coordinates, top-left origin, values between 0 and 1. Do NOT emit a JSON object with named keys.
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

### The `table_data` block (canonical table representation)

Identical to the `pdf2md-page-assets` skill — for every `kind: "tbl"` asset that is legibly extractable, emit a `table_data` object conforming to `pdf2md-table/v1`. If the table is visible but cannot be transcribed with confidence, omit `table_data` entirely and emit `"needs_extraction": true` on the entry plus an `issue` such as `table_unreadable`. Do NOT emit a partial or guessed `table_data`. See `skills/pdf2md-page-assets/SKILL.md` for the full table-level field list, row/cell shape, cell-type semantics, structural rules, and worked example.

### Step 5 — Cross-check consistency between A and B

Before writing, verify:

1. Every `[FIGURE: …]` placeholder in the Markdown has a matching `kind: "fig"` entry in the JSON, in the same reading order.
2. Every `[TABLE: …]` placeholder has a matching `kind: "tbl"` entry, in the same reading order.
3. Every `[… logo|emblem|seal|cover|photograph|photo|image]` placeholder has a matching `kind: "img"` entry.
4. No JSON asset entry lacks a corresponding placeholder in the Markdown.

If a mismatch is unavoidable (e.g. an asset is visible but you chose not to emit a placeholder because it's a recurring page header), prefer to DROP the JSON entry rather than leave a widow placeholder. The downstream materializer treats unmatched assets as a defect.

### Step 6 — Write outputs and return status

1. Write the Markdown to `OUTPUT_MD_PATH` using the `Write` tool.
2. Write the JSON to `OUTPUT_JSON_PATH` using the `Write` tool.
3. Return:
   - `RUN_STATUS=SUCCESS page={n} md_bytes=<n> assets=<n>` on success with ≥ 1 asset.
   - `RUN_STATUS=NO_ASSETS page={n} md_bytes=<n> assets=0` on success with no assets visible.
   - `RUN_STATUS=FAILED page={n} <reason>` if the image was unreadable / extraction failed. Write the failure placeholder to the Markdown and a valid-JSON `FAILED` record to the JSON.
   - `RUN_STATUS=FAILED_INPUTS page={n} <reason>` if validation in Step 1 failed.

## Outputs

| Path | Content |
|---|---|
| `{OUTPUT_MD_PATH}` | Page Markdown — same contract as the legacy `pdf2md-page` skill. |
| `{OUTPUT_JSON_PATH}` | Page asset JSON — same `pdf2md-page-assets/v1` schema as the legacy `pdf2md-page-assets` skill. |

## Return value

The skill returns to the caller a single status line:

- `RUN_STATUS`: `SUCCESS` | `NO_ASSETS` | `FAILED` | `FAILED_INPUTS`
- `PAGE_NUM`: the page number processed
- `MD_BYTES`: approximate Markdown byte count
- `ASSETS`: count of `assets` written

## Non-negotiable constraints

- **Single-page scope.** One page in, two artifacts out. No cross-page context.
- **Single vision read.** Read `IMAGE_PATH` once; produce both outputs from that one pass.
- **Two-target writes.** Write scope is strictly the designated `OUTPUT_MD_PATH` and `OUTPUT_JSON_PATH`.
- **Single-file reads.** Read scope is strictly `IMAGE_PATH`. No other files may be read.
- **Raw VLM output for Markdown.** No post-processing, no cleanup rules applied. PDF2MD handles that.
- **Strict JSON schema.** The asset JSON MUST validate against `pdf2md-page-assets/v1` exactly (field names, literal string values, array vs object shapes).
- **A/B consistency.** Placeholders in the Markdown and entries in the JSON must align one-to-one.
- **No invention.** Do not add content that is not visible in the image. No hallucinated text, URLs, structural elements, captions, or asset bounding boxes.
- **Content fidelity.** All visible text, tables, and structural elements from the page image must be represented in the Markdown.
- **Failure placeholders.** On read failure or extraction failure, write a placeholder line to `OUTPUT_MD_PATH`, write a valid-JSON failure record to `OUTPUT_JSON_PATH`, and return the appropriate failure status. Never leave either output unwritten.

## QA expectations

- `OUTPUT_MD_PATH` exists after the run and is non-empty.
- `OUTPUT_JSON_PATH` exists, is non-empty, and parses with `json.loads`.
- The JSON `run_status` is one of `SUCCESS`, `NO_ASSETS`, `FAILED`, or `FAILED_INPUTS`.
- Every asset has valid `kind`, `ordinal`, `caption`, `bbox_norm`, and `confidence`.
- Table assets include either a schema-conforming `table_data` block OR `needs_extraction: true` with an explicit issue.
- Placeholders in the Markdown align one-to-one with entries in the JSON.
- No files other than `OUTPUT_MD_PATH` and `OUTPUT_JSON_PATH` were written.
- No files other than `IMAGE_PATH` were read.
