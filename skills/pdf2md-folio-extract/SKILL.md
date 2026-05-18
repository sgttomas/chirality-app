---
name: pdf2md-folio-extract
description: Read one rasterized PDF page and emit the visible printed folio label (page number as it appears on the page itself — "47", "xiv", "B-3", or null when no folio is printed).
compatibility: Chirality TASK; invoked by PDF2MD asset-enabled mode after rasterization, before per-page asset fan-out.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - pdf2md-folio-extract

## Purpose

Read one rasterized PDF page image and emit the printed folio label that is visible on the page itself — the page number as the document prints it, not the physical PDF sequence position.

Examples of valid folio labels:

- Arabic numerals: `"47"`, `"128"`
- Roman numerals: `"xiv"`, `"iii"`, `"XLII"`
- Compound/prefixed labels: `"B-3"`, `"A-12"`, `"3-7"`
- Section-prefixed labels: `"Ch1-4"`, `"App-2"`

The skill reads exactly one page image and writes exactly one JSON file naming the visible folio. It does not assemble a folio map across pages, reconcile front-matter Roman numbering against body Arabic numbering, or interact with the PDF outline / TOC. Those are orchestrator-level concerns.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `PDF2MD` orchestrator

Not the right fit for:

- whole-PDF folio map assembly
- TOC / outline cross-referencing
- inferring a folio from neighbouring pages
- assigning final asset filenames or any non-folio metadata

## Inputs

Required runtime overrides:

- `IMAGE_PATH` - absolute path to the page PNG
- `OUTPUT_PATH` - absolute path for the folio JSON
- `PAGE_NUM` - 1-indexed physical PDF page number

## Read boundary

Reads are limited to exactly one file:

- `{IMAGE_PATH}`

Do not read neighbouring pages, manifests, sibling Markdown, the source PDF, or any other folio JSON. This preserves page-level parallelism and prevents folio invention by inference from neighbours.

## Write boundary

Writes are limited to exactly one file:

- `{OUTPUT_PATH}`

The output filename is supplied by the orchestrator and must not be derived or changed by the skill.

## Tool usage

- No deterministic tools.
- The `allowed-tools` frontmatter field is intentionally omitted.
- The agent uses native multimodal reading for `IMAGE_PATH` and native writing for `OUTPUT_PATH`.

Disallowed behavior:

- Do not crop images.
- Do not write PNG, CSV, or XLSX files.
- Do not read neighbouring page images or any other file.
- Do not invent a folio from the physical sequence (e.g. do NOT return `"47"` just because `PAGE_NUM` is 47).
- Do not infer a folio from neighbouring pages' numbering.
- Do not consult outlines, TOCs, or sibling JSON.

## Method

### Step 1 - Validate inputs

1. Confirm `IMAGE_PATH` exists and has a `.png` extension.
2. Confirm `OUTPUT_PATH` parent directory exists.
3. If required inputs are missing or malformed, write a valid JSON file with `run_status: "FAILED_INPUTS"`, `page_label: null`, `location: null`, and a rationale naming the missing input.

### Step 2 - Inspect the page

1. Read `IMAGE_PATH` and inspect the page visually.
2. Scan the typical folio zones in order: bottom-center, bottom-outer (left/right), top-outer (left/right), top-center.
3. Identify the printed folio if and only if it is visibly present as a page-number marking — typically a short numeric / Roman / alphanumeric token isolated in a header or footer, not part of running prose, figure captions, equation numbers, or section headings.
4. If no folio is printed (blank page, cover page, chapter-opener page where the folio is suppressed, front-matter without numbering, full-bleed plate without page furniture, etc.), record that there is no folio. Do NOT invent one.

### Step 3 - Emit JSON

Write only JSON, with no Markdown fences or commentary.

**REQUIRED EXACT VALUES — do not substitute synonyms or restructure.** Downstream consumers rely on these exact field names, types, and string literals:

- Top-level field names are exactly: `schema_version`, `run_status`, `page`, `page_label`, `page_label_source`, `location`, `confidence`, `rationale`.
- `schema_version` MUST be the literal string `"pdf2md-folio-extract/v1"`.
- `run_status` MUST be one of the four uppercase literals: `"SUCCESS"`, `"NO_FOLIO"`, `"FAILED"`, `"FAILED_INPUTS"`. Do NOT use `"ok"`, `"success"`, `"done"`, etc.
- `page` MUST be the integer 1-indexed physical PDF page number — i.e. echo `PAGE_NUM`. The field name is `page` (NOT `page_num`).
- `page_label` is a JSON string OR JSON `null`. Use `null` when no folio is visibly printed.
- `page_label_source` MUST be the literal string `"vlm"` on every successful skill run. On `FAILED` / `FAILED_INPUTS` / `NO_FOLIO` runs, set it to `"vlm"` as well — it identifies the producer of this record.
- `location` is one of the six zone literals: `"top-left"`, `"top-center"`, `"top-right"`, `"bottom-left"`, `"bottom-center"`, `"bottom-right"`, or JSON `null` when there is no folio.
- `confidence` is one of: `"high"`, `"medium"`, `"low"`.
- `rationale` is one short sentence in plain English describing what was visually observed (or, on failure, what went wrong).

Example - folio present:

```json
{
  "schema_version": "pdf2md-folio-extract/v1",
  "run_status": "SUCCESS",
  "page": 47,
  "page_label": "47",
  "page_label_source": "vlm",
  "location": "bottom-center",
  "confidence": "high",
  "rationale": "Arabic numeral 47 centered in footer."
}
```

Example - Roman numeral front-matter:

```json
{
  "schema_version": "pdf2md-folio-extract/v1",
  "run_status": "SUCCESS",
  "page": 9,
  "page_label": "xiv",
  "page_label_source": "vlm",
  "location": "bottom-center",
  "confidence": "high",
  "rationale": "Lowercase Roman numeral xiv centered in footer of preface page."
}
```

Example - no folio printed:

```json
{
  "schema_version": "pdf2md-folio-extract/v1",
  "run_status": "NO_FOLIO",
  "page": 3,
  "page_label": null,
  "page_label_source": "vlm",
  "location": null,
  "confidence": "high",
  "rationale": "Chapter-opener page; folio suppressed per house style."
}
```

Example - missing input:

```json
{
  "schema_version": "pdf2md-folio-extract/v1",
  "run_status": "FAILED_INPUTS",
  "page": 47,
  "page_label": null,
  "page_label_source": "vlm",
  "location": null,
  "confidence": "low",
  "rationale": "IMAGE_PATH does not exist."
}
```

## Output rules

- `page_label` MUST be the exact string visible on the page — preserve case, Roman vs. Arabic form, hyphens, and any section prefix. Do NOT normalize `"xiv"` to `"14"`, do NOT strip a `"B-"` prefix, do NOT zero-pad.
- `page_label` is `null` only when no folio is visibly printed.
- `location` MUST reflect the zone where the folio was observed; it is `null` if and only if `page_label` is `null`.
- `page_label_source` is always `"vlm"`.
- `confidence` should be `"high"` when the folio is clearly legible in a conventional folio zone, `"medium"` when the glyph is partially obscured or the zone is unusual, and `"low"` when the reading is a best guess.
- `rationale` is one sentence; do not include multi-paragraph explanations.

## Non-negotiable constraints

- Single page in, one JSON out.
- No cross-page context.
- No folio invention from the physical sequence or from neighbours.
- The emitted `page_label` must be visible on the page image.
- The JSON must parse with standard `json.loads`.

## QA expectations

- `OUTPUT_PATH` exists and is non-empty.
- JSON parses successfully.
- `run_status` is one of `SUCCESS`, `NO_FOLIO`, `FAILED`, or `FAILED_INPUTS`.
- `page` equals the runtime `PAGE_NUM`.
- `page_label` is a string when `run_status == "SUCCESS"`, and `null` otherwise.
- `location` is one of the six zone literals when `page_label` is a string, and `null` otherwise.
- `page_label_source` is the literal `"vlm"`.
