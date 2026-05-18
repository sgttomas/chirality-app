# pdf2md-folio-extract - Brief Schema

Use this skill with `TASK` like this. It is normally spawned by the `PDF2MD` orchestrator after rasterization and before per-page asset fan-out:

```md
PURPOSE: Extract the visible printed folio label from one rasterized PDF page
RequestedBy: PDF2MD

ScopePath: /abs/path/to/pdf_work_dir
TaskSkill: pdf2md-folio-extract

Tasks:
  - Read one page raster
  - Identify the printed folio label visible on the page, if any
  - Emit a single folio JSON record per the skill contract

ApplyEdits: true

AllowedWriteTargets:
  - "/abs/path/to/pdf_work_dir/page_0047_folio.json"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/pdf_work_dir/page_0047.png
  OUTPUT_PATH: /abs/path/to/pdf_work_dir/page_0047_folio.json
  PAGE_NUM: 47

ExpectedOutputs:
  - /abs/path/to/pdf_work_dir/page_0047_folio.json
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `pdf2md-folio-extract` | Must match skill folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to the page PNG | Must exist, must have `.png` extension |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path to page folio JSON | Parent directory must exist |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed physical PDF page number | Positive integer; echoed into JSON as `page` |

## Optional fields

None. This skill takes no optional runtime overrides.

## TaskProfile

`NONE` - this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads only:

- `{IMAGE_PATH}`

It must not read neighbouring page images, sibling folio JSON, manifests, the source PDF, the page Markdown, or any TOC / outline artifact.

## Write boundary

The skill writes only:

- `{OUTPUT_PATH}`

## AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only skill with no deterministic tool dependencies.

## Output JSON shape

The skill writes exactly one JSON file with this shape:

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

### Field-by-field rules

| Field | Type | Allowed values | Notes |
|---|---|---|---|
| `schema_version` | string | exactly `"pdf2md-folio-extract/v1"` | Literal — do not alter |
| `run_status` | string | `"SUCCESS"` / `"NO_FOLIO"` / `"FAILED"` / `"FAILED_INPUTS"` | Uppercase literals only |
| `page` | int | positive integer | Echo of runtime `PAGE_NUM`; field name is `page` (NOT `page_num`) |
| `page_label` | string OR null | exact visible glyph (`"47"`, `"xiv"`, `"B-3"`, ...) OR `null` | `null` iff no folio is printed; preserve case, Roman vs. Arabic, prefixes, hyphens |
| `page_label_source` | string | exactly `"vlm"` | Literal — identifies producer |
| `location` | string OR null | `"top-left"` / `"top-center"` / `"top-right"` / `"bottom-left"` / `"bottom-center"` / `"bottom-right"` OR `null` | `null` iff `page_label` is `null` |
| `confidence` | string | `"high"` / `"medium"` / `"low"` | Visual reading confidence |
| `rationale` | string | one short sentence | Plain English; one sentence |

### Status semantics

| `run_status` | When to emit | `page_label` | `location` |
|---|---|---|---|
| `SUCCESS` | A folio is visibly printed and legible | string | one of six zone literals |
| `NO_FOLIO` | The page has no printed folio (blank page, cover, chapter opener with suppressed folio, untitled front-matter, full-bleed plate, etc.) | `null` | `null` |
| `FAILED` | The page image is unreadable, corrupt, or otherwise prevents inspection | `null` | `null` |
| `FAILED_INPUTS` | Required runtime overrides are missing, paths do not exist, or extensions are wrong | `null` | `null` |

## CustomInstructions

Usually unnecessary. If used, keep them run-specific and do not restate the whole skill contract. Good examples:

- "Treat the leading section letter (e.g. `A-`, `B-`) as part of the folio; do not strip it."
- "On chapter-opener pages where this house style suppresses the folio, return `NO_FOLIO` even if a chapter number appears in display type."
