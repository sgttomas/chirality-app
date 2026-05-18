---
name: domain-prose-validate
description: Independently re-extract one rasterized PDF page's prose, equations, and asset placeholders for downstream extraction-reproducibility comparison (Gate 1.5-P Stage 1).
compatibility: Chirality TASK; invoked by DOMAIN_DECOMP Gate 1.5-P orchestration as the first stage of the three-stage prefilter.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - domain-prose-validate

## Purpose

Produce an **independent** Markdown re-extract of one rasterized PDF page so that a downstream deterministic comparator (Gate 1.5-P Stage 2) can detect divergences against the original `pdf2md` extract. This skill is the perception stage of the Gate 1.5-P extraction-reproducibility prefilter described in `agents/AGENT_DOMAIN_DECOMP.md`.

The skill reads one page image plus a bbox-hints JSON describing where assets are expected, and writes one Markdown file containing:

- Prose paragraphs in reading order.
- Display equations as `$$...$$` blocks at their reading-order position.
- Asset placeholders inline at their reading-order position, in the canonical bracketed form (`[FIGURE: ...]`, `[TABLE: ...]`, `[IMAGE: ...]`).

It does **not** crop assets, transcribe table cells, assign asset IDs, write JSON, or emit a manifest. Those responsibilities belong to other skills and to the Stage 2 comparator.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the Gate 1.5-P Stage 1 orchestration helper

Not the right fit for:

- whole-PDF re-extraction
- cross-page reasoning
- comparator/diff logic (Stage 2 is deterministic, not VLM)
- adjudicating equation differences (Stage 3 dispatches `equation-flag-interpret`)
- asset materialization, manifest aggregation, or filename assignment

## Inputs

Required runtime overrides:

- `IMAGE_PATH` - absolute path to the page PNG
- `ASSET_BBOX_HINTS_PATH` - absolute path to a JSON file listing expected asset bboxes + kinds for this page
- `OUTPUT_PATH` - absolute path for the re-extract `.md` file
- `PAGE_NUM` - 1-indexed page number

Optional runtime overrides:

- none

### `ASSET_BBOX_HINTS_PATH` shape

The hints file is consumed for **guidance only** — it tells the skill *where* placeholders are expected so the agent can be deliberate about emitting them. It is not authoritative; the page raster remains the source of truth for caption text and reading order.

```json
{
  "page": 47,
  "assets": [
    {"kind": "fig", "asset_id": "BookX_p0047_fig01", "bbox_norm": [0.1, 0.2, 0.9, 0.5]},
    {"kind": "tbl", "asset_id": "BookX_p0047_tbl01", "bbox_norm": [0.1, 0.55, 0.9, 0.85]}
  ]
}
```

Each entry's `kind` is one of `fig`, `tbl`, or `img`. The `asset_id` is informational only and MUST NOT appear in the output Markdown.

## Read boundary

Reads are limited to exactly two files:

- `{IMAGE_PATH}`
- `{ASSET_BBOX_HINTS_PATH}`

**Anti-confirmation-bias clause (cornerstone of Gate 1.5-P):**

The skill MUST NOT read, peek at, infer, or reference any pre-existing per-page Markdown extract (e.g. `page_NNNN.md` under `_Sources/<book>_pdf2md_work/`), the assembled `<book>.md`, sibling pages, the audit sidecars, or any other materialized extraction artifact. The entire point of Stage 1 is to produce a re-extract that is causally independent of the original pdf2md output — reading the original would defeat the comparator and silently collapse Gate 1.5-P. If any path matching `page_*.md` or the book-level assembled Markdown is encountered, the skill MUST refuse to read it.

Do not read neighbouring pages, manifests, sibling Markdown files, asset XLSX files, or previously materialized assets. This preserves page-level parallelism and prevents cross-page priming.

## Write boundary

Writes are limited to exactly one file:

- `{OUTPUT_PATH}`

The output filename is supplied by the orchestrator and must not be derived or changed by the skill.

## Tool usage

- No deterministic tools.
- The `allowed-tools` frontmatter field is intentionally omitted.
- The agent uses native multimodal reading for `IMAGE_PATH`, native text reading for `ASSET_BBOX_HINTS_PATH`, and native writing for `OUTPUT_PATH`.

Disallowed behavior:

- Do not read any pre-existing per-page Markdown or the assembled book Markdown (see anti-confirmation-bias clause).
- Do not crop images.
- Do not write PNG, CSV, JSON, or XLSX files.
- Do not transcribe table cells — emit a `[TABLE: ...]` placeholder.
- Do not assign asset filenames or asset IDs.
- Do not emit Markdown frontmatter, page numbers, or any metadata header in the output.
- Do not widen read or write scope beyond the declared two inputs and one output.

## Method

### Step 1 - Validate inputs

1. Confirm `IMAGE_PATH` exists and has a `.png` extension.
2. Confirm `ASSET_BBOX_HINTS_PATH` exists and has a `.json` extension.
3. Confirm `OUTPUT_PATH` parent exists.
4. If any required input is missing or unreadable, abort without writing a partial file. (Stage 2 will treat the missing re-extract as a structural fail for the page.)

### Step 2 - Read the hints file

1. Parse `ASSET_BBOX_HINTS_PATH` as JSON.
2. Note, for each entry, the `kind` (`fig` / `tbl` / `img`) and the approximate `bbox_norm` region of the page where that asset sits. This is to set expectations only — do not copy `asset_id`, captions, or any other text from the hints into the output. Caption text comes from reading the raster.

### Step 3 - Re-extract the page from the raster

This step is performed **without** consulting any prior extract. The page image is the sole authority for textual content.

1. Read `IMAGE_PATH` as multimodal input.
2. Transcribe prose paragraphs in document reading order.
3. When a display equation appears in reading order, emit it as a `$$...$$` block on its own line(s) at that position.
4. Inline equations remain inline as `$...$` (single-dollar). Only standalone display equations use `$$...$$`.
5. When an asset region appears in reading order (cross-referenced against `ASSET_BBOX_HINTS_PATH` for expected placement), emit a placeholder on its own line using the exact syntax in the "Output format" section below. The caption / description text inside the placeholder is what the VLM reads from the raster — not what the hints file says.
6. Preserve printed line breaks within paragraphs as they appear on the page. The Stage 2 comparator handles whitespace normalization (NFKC, whitespace collapse, line-break-hyphen repair) before strict-compare.
7. Do not invent content. If a region is unreadable, transcribe what is legible and stop; do not paraphrase or summarize.

### Step 4 - Write the output

Write `OUTPUT_PATH` containing the page body only. No frontmatter, no `# Page N` heading, no metadata footer. End the file with a single trailing newline.

## Output format

The re-extract is plain Markdown with three kinds of structural elements:

### Prose

Plain Markdown paragraphs. Preserve printed line breaks within a paragraph. Separate paragraphs with a blank line.

### Equations

- **Display equations** appear on their own line(s) as `$$...$$` blocks at the reading-order position where they print.
- **Inline equations** remain inline within prose as `$...$`.

Example:

```
The Reynolds number is defined as

$$Re = \frac{\rho v L}{\mu}$$

where $\mu$ is the dynamic viscosity.
```

### Asset placeholders

When an asset region appears in reading order, emit exactly one of the following placeholder forms on its own line:

- `[FIGURE: <caption text as printed on the page>]` — for `kind: "fig"`
- `[TABLE: <caption text as printed on the page>]` — for `kind: "tbl"`
- `[IMAGE: <one-line visual description>]` — for `kind: "img"` (uncaptioned images, logos, photographs)

Rules:

- The prefix is uppercase and must be exactly `FIGURE:` / `TABLE:` / `IMAGE:` followed by a single space.
- The placeholder is on its own line, surrounded by blank lines (so it is a structural block, not part of a prose paragraph).
- The caption text comes from reading the raster. Do **not** copy text from `ASSET_BBOX_HINTS_PATH` (which only carries `kind`, `asset_id`, and `bbox_norm`).
- Do not include the `asset_id` from the hints file. Do not emit Markdown image syntax (`![alt](path)`) or link syntax (`[XLSX](...)`) — those are Stage 2's responsibility to align against.
- If a figure or table has no visible caption, emit a concise visual description in the placeholder body (e.g. `[FIGURE: schematic of two-stage compressor with intercooler]`).

## Non-negotiable constraints

- One page raster + one hints JSON in; one Markdown re-extract out.
- No reading of prior extracts. Confirmation bias defeats Gate 1.5-P.
- No cross-page context.
- No invented prose, equations, or asset placeholders.
- Asset placeholders are emitted in the canonical bracketed form only. No Markdown image / link syntax.
- The output file body contains no frontmatter and no page-number metadata.
- The file ends with a single trailing newline.

## QA expectations

- `OUTPUT_PATH` exists and is non-empty.
- File ends with a newline.
- Count of `[FIGURE:` / `[TABLE:` / `[IMAGE:` placeholders is consistent with the number of `kind=="fig"` / `kind=="tbl"` / `kind=="img"` entries in `ASSET_BBOX_HINTS_PATH`, within reasonable tolerance. Mismatch is not a hard skill failure (it is exactly the signal Stage 2 needs to surface), but a large drift should be noted as an issue by the orchestrator.
- No file other than `IMAGE_PATH` and `ASSET_BBOX_HINTS_PATH` was read. In particular, no `page_*.md` or assembled book Markdown was opened.
- No file other than `OUTPUT_PATH` was written.
