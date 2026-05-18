---
name: equation-bbox-detect
description: Detect display-equation bounding boxes on one rasterized page PNG using multimodal vision and emit normalized coordinates for downstream cropping. Per-page bounded dispatch invoked by EQUATION_AUDIT during Phase 1 when per-equation crops are enabled.
compatibility: Chirality TASK; invoked by EQUATION_AUDIT for per-page bbox detection in Phase 1
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — equation-bbox-detect

## Purpose

Look at one rasterized page PNG, identify every DISPLAY equation visible on the page (block-level math, set off from running prose), and emit normalized bounding-box coordinates as `page_NNNN_eq_bboxes.json` — the schema `tools/equation_audit/crop_equation_regions.py` already consumes.

This skill is the missing producer for `crop_equation_regions.py`. That tool has been functional in the repo but had no upstream — the per-page bbox JSONs it expected were never generated. This skill closes that gap: one TASK dispatch per page, normalized coordinates in [0,1], cross-checked against the per-page Markdown's equation list when expected hashes are provided.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `EQUATION_AUDIT` persona during Phase 1 when per-equation crops are enabled.

Not the right fit for:
- per-equation interpretation of human notes (use `equation-flag-interpret`)
- whole-document figure/table bounding-box detection (use `pdf2md-page-assets`)
- inline-equation detection (this skill targets DISPLAY equations only)
- cross-page reasoning (one page per invocation)

## Inputs

### Required (via `RuntimeOverrides`)

- `IMAGE_PATH` — absolute path to `page_NNNN.png`
- `PAGE_MD_PATH` — absolute path to the per-page Markdown (provides context: which equations to look for)
- `PAGE_NUM` — 1-indexed page number; must match the `NNNN` in `IMAGE_PATH`
- `OUTPUT_PATH` — absolute path to write `page_NNNN_eq_bboxes.json`

### Optional

- `EXPECTED_EQUATION_HASHES` — list of 12-hex hashes the persona expects to find on this page (extracted by `audit_equations.py`). The skill cross-checks its findings against this list and notes mismatches in the `latex_excerpt` field.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `IMAGE_PATH` | Path to page PNG | **Required** | Existing `.png` file |
| `PAGE_MD_PATH` | Path to per-page Markdown | **Required** | Existing `.md` file |
| `PAGE_NUM` | Page number | **Required** | Positive integer |
| `OUTPUT_PATH` | Path to write bbox JSON | **Required** | Parent dir exists; `.json` |
| `EXPECTED_EQUATION_HASHES` | Expected hash cross-check list | `[]` | List of 12-hex strings |

## Read boundary

Reads are limited to:

- `IMAGE_PATH` — the single page PNG, multimodal load.
- `PAGE_MD_PATH` — the per-page Markdown, text load.

No other reads. The skill MUST NOT:

- read other pages
- read `equations.jsonl` or any audit artifact
- read other source files (skeleton, assets, sidecars)

## Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` — `page_NNNN_eq_bboxes.json` matching the schema `crop_equation_regions.py` consumes

No other side effects.

## Tool usage

- No deterministic tools are invoked. This is a VLM-vision skill.
- The `allowed-tools` frontmatter field is intentionally omitted.
- The agent uses its native `Read` tool for multimodal PNG input and text MD input, and its native `Write` tool for the single output JSON.

Disallowed behavior:

- MUST NOT shell out to any subprocess or external command.
- MUST NOT widen scope beyond the assigned page.
- MUST NOT modify the page Markdown or any audit artifact.
- MUST NOT re-OCR text outside display equations (transcription is `pdf2md-page`'s job).
- MUST NOT write any file other than `OUTPUT_PATH`.

## Method

### Step 1 — Validate inputs

1. Confirm `IMAGE_PATH` exists and is a `.png` file.
2. Confirm `PAGE_MD_PATH` exists.
3. Confirm `OUTPUT_PATH` parent directory exists.
4. If any required input is invalid, write `{"page": <PAGE_NUM>, "equations": [], "error": "<reason>"}` to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.

### Step 2 — Read the page Markdown for expected equation list

1. Use the `Read` tool to load `PAGE_MD_PATH` (text).
2. Scan for `$$...$$` blocks to know which equations the page is expected to contain. This is context for Step 4's cross-check, NOT ground truth for bbox extraction (bbox extraction is vision-only).

### Step 3 — Load the page raster

1. Use the `Read` tool to load `IMAGE_PATH` (multimodal PNG).

### Step 4 — Identify display equations on the page

1. Find every block of typeset mathematics that is **set off from the surrounding running prose** — typically:
   - Centered or visually offset from the column body
   - Preceded and followed by paragraph spacing
   - Often labeled with equation numbers (e.g., `(1.5)`, `(2.3a)`) at right margin
2. DO NOT box inline equations (math symbols embedded in running sentences).
3. DO NOT box section headings, table cells, figure labels, or page numbers.
4. For each display equation, determine its tightest enclosing rectangle on the page raster.

### Step 5 — Normalize coordinates

For each detected display equation:

1. Compute normalized coordinates `[x0, y0, x1, y1]` where:
   - `x0`, `y0` is the top-left corner (image origin convention: `(0,0)` at top-left)
   - `x1`, `y1` is the bottom-right corner
   - All values are floats in `[0.0, 1.0]` relative to the page raster's width × height
2. Order detected equations top-to-bottom on the page; assign 1-based `index`.
3. Capture the first ~20 characters of the visible LaTeX/symbolic content as `latex_excerpt` for cross-check against `EXPECTED_EQUATION_HASHES`. This is a freeform string — DO NOT attempt full LaTeX transcription (that's `pdf2md-page`'s job).

### Step 6 — Write outputs

Write `OUTPUT_PATH` as a single JSON object matching the consumer's schema:

```json
{
  "page": <PAGE_NUM>,
  "equations": [
    {
      "index": 1,
      "bbox_norm": [0.12, 0.21, 0.85, 0.27],
      "latex_excerpt": "\\frac{2}{\\sqrt{3}} Y ="
    },
    {
      "index": 2,
      "bbox_norm": [0.18, 0.42, 0.78, 0.46],
      "latex_excerpt": "d\\epsilon/\\sigma ="
    }
  ]
}
```

When the page has no display equations:

```json
{"page": <PAGE_NUM>, "equations": []}
```

### Step 7 — Return status

Return one of:

- `RUN_STATUS=SUCCESS` — at least one display equation detected; bboxes emitted.
- `RUN_STATUS=NO_FINDINGS` — no display equations on this page (empty `equations` list).
- `RUN_STATUS=FAILED_INPUTS` — required inputs were missing or malformed.
- `RUN_STATUS=FAILED` — bbox detection failed for an unexpected reason.

Also return: `PAGE_NUM`, `EQUATION_COUNT`.

## Non-negotiable constraints

- **Display-equation-only.** Do NOT detect inline math inside running prose.
- **Normalized coordinates.** All bbox values in [0.0, 1.0]. Pixel coordinates are forbidden.
- **Top-to-bottom ordering.** `index` is 1-based and increases top-to-bottom on the page.
- **No transcription.** The skill does not produce LaTeX — `latex_excerpt` is at most a ~20-char hint for cross-check, not authoritative.
- **No cross-page state.** One page per invocation; no carryover.
- **Output-path-only writes.** Exactly one file is written per invocation. No other side effects.

## QA expectations

- Exactly one file exists at `OUTPUT_PATH` after the run.
- The file is valid JSON; top-level is a single object with `page` (int) and `equations` (list).
- Each `equations[*]` entry has `index` (int ≥ 1), `bbox_norm` (4-tuple of floats in [0,1]).
- `index` is 1-based and strictly increasing.
- No `bbox_norm` overlaps with another `bbox_norm` by more than ~10% area (two display equations should not share a region — overlap is a detection error).
- `x0 < x1` and `y0 < y1` for every box.
- `RUN_STATUS` is one of: `SUCCESS`, `NO_FINDINGS`, `FAILED_INPUTS`, `FAILED`.

## Relationship to EQUATION_AUDIT

This skill is the per-page worker invoked by the `EQUATION_AUDIT` persona during Phase 1 when per-equation crops are enabled. The persona:

- runs `tools/equation_audit/audit_equations.py` to extract every display equation per page into `equations.jsonl` (text only; no bboxes),
- for each page that has display equations, renders one INIT-TASK brief via `tools/equation_audit/build_equation_bbox_brief.py`, optionally embedding `EXPECTED_EQUATION_HASHES` derived from the JSONL,
- dispatches one `TASK + equation-bbox-detect` invocation per page,
- collects the per-page `page_NNNN_eq_bboxes.json` files into the page work-dir,
- runs `tools/equation_audit/crop_equation_regions.py` to produce per-equation PNG crops under `audit/equations/working/crops/`,
- embeds the crops in the audit HTML for visual review.

This skill is a sibling of `pdf2md-page-assets` (per-page figure/table bbox detection) and `drawing-extract-page` (per-page drawing-element detection) — same per-page VLM fanout pattern, narrowed to display equations.
