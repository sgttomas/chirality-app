# pdf2md-folio-extract contract

## Brief

Use this workflow with `TASK` like this. It is normally spawned by the `pdf2md-orchestration` orchestrator after rasterization and before per-page asset fan-out:

```md
PURPOSE: Extract the visible printed folio label from one rasterized PDF page
RequestedBy: WORKING_ITEMS
ParentWorkflow: pdf2md-orchestration
ScopePath: /abs/path/to/pdf_work_dir
Workflow: pdf2md-folio-extract

Tasks:
  - Read one page raster
  - Identify the printed folio label visible on the page, if any
  - Emit a single folio JSON record per the workflow contract

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

### Required fields

| Field | Value | Notes |
|---|---|---|
| `Workflow` | `pdf2md-folio-extract` | Must match workflow folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to the page PNG | Must exist, must have `.png` extension |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path to page folio JSON | Parent directory must exist |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed physical PDF page number | Positive integer; echoed into JSON as `page` |

### Optional fields

None. This workflow takes no optional runtime overrides.

### Read boundary

The workflow reads only:

- `{IMAGE_PATH}`

It must not read neighbouring page images, sibling folio JSON, manifests, the source PDF, the page Markdown, or any TOC / outline artifact.

### Write boundary

The workflow writes only:

- `{OUTPUT_PATH}`

### AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only workflow with no deterministic tool dependencies.

### Output JSON shape

The workflow writes exactly one JSON file with this shape:

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

#### Field-by-field rules

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

#### Status semantics

| `run_status` | When to emit | `page_label` | `location` |
|---|---|---|---|
| `SUCCESS` | A folio is visibly printed and legible | string | one of six zone literals |
| `NO_FOLIO` | The page has no printed folio (blank page, cover, chapter opener with suppressed folio, untitled front-matter, full-bleed plate, etc.) | `null` | `null` |
| `FAILED` | The page image is unreadable, corrupt, or otherwise prevents inspection | `null` | `null` |
| `FAILED_INPUTS` | Required runtime overrides are missing, paths do not exist, or extensions are wrong | `null` | `null` |

### CustomInstructions

Usually unnecessary. If used, keep them run-specific and do not restate the whole workflow contract. Good examples:

- "Treat the leading section letter (e.g. `A-`, `B-`) as part of the folio; do not strip it."
- "On chapter-opener pages where this house style suppresses the folio, return `NO_FOLIO` even if a chapter number appears in display type."

## Acceptance

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension, or the workflow returns `FAILED_INPUTS`.
2. `OUTPUT_PATH` parent directory exists before write.
3. `OUTPUT_PATH` exists after the run and is non-empty.
4. `OUTPUT_PATH` parses with `json.loads`.
5. No task data outside `IMAGE_PATH` were read.
6. No files other than `OUTPUT_PATH` were written.

### JSON shape checks

The output JSON must include exactly these top-level fields:

| Field | Requirement |
|---|---|
| `schema_version` | Exactly `"pdf2md-folio-extract/v1"` |
| `run_status` | One of `"SUCCESS"`, `"NO_FOLIO"`, `"FAILED"`, `"FAILED_INPUTS"` |
| `page` | Integer; equals runtime `PAGE_NUM` (field name is `page`, NOT `page_num`) |
| `page_label` | JSON string when `run_status == "SUCCESS"`, JSON `null` otherwise |
| `page_label_source` | Exactly `"vlm"` |
| `location` | One of `"top-left"`, `"top-center"`, `"top-right"`, `"bottom-left"`, `"bottom-center"`, `"bottom-right"` when `page_label` is a string; JSON `null` otherwise |
| `confidence` | One of `"high"`, `"medium"`, `"low"` |
| `rationale` | Non-empty string; one short sentence |

### Field-value strictness

- `schema_version` is a literal — `"pdf2md-folio/v1"`, `"v1"`, or other shortened forms are rejected.
- `run_status` uppercase literals only — `"ok"`, `"success"`, `"none"`, `"done"` are rejected.
- `page_label` MUST be the verbatim visible glyph; downstream tools rely on the exact surface form:
  - Roman numerals stay Roman (`"xiv"`, not `"14"`).
  - Case is preserved (`"xiv"` vs. `"XIV"`).
  - Section prefixes are kept (`"B-3"`, not `"3"`).
  - No zero-padding (`"7"`, not `"007"`).
- `page_label_source` is always the literal `"vlm"` from this workflow, including on failure rows.
- `location` and `page_label` co-vary: both are `null` together, or both are non-null together. A `null` `page_label` with a non-null `location` is invalid, and vice versa.

### Folio-invention guard

The most important QA invariant for this workflow:

- A `SUCCESS` row's `page_label` MUST be visible on the page image.
- It MUST NOT be derived from `PAGE_NUM` (the physical sequence index).
- It MUST NOT be inferred from neighbouring pages' numbering.
- When no folio is visibly printed, the correct emission is `NO_FOLIO` with `page_label: null` and `location: null` — never a fabricated label.

### Failure posture

| Failure mode | Required output |
|---|---|
| Missing or wrong-extension `IMAGE_PATH` | `run_status: "FAILED_INPUTS"`, `page_label: null`, `location: null`, rationale naming the missing input |
| `OUTPUT_PATH` parent directory missing | `run_status: "FAILED_INPUTS"`, `page_label: null`, `location: null`, rationale naming the issue |
| No folio printed on the page | `run_status: "NO_FOLIO"`, `page_label: null`, `location: null`, rationale explaining (blank page / cover / chapter opener / etc.) |
| Page image unreadable or corrupt | `run_status: "FAILED"`, `page_label: null`, `location: null`, rationale explaining the problem |

### Orchestrator-side checks

These checks belong to `pdf2md-orchestration`, not this workflow:

- Running the folio-extract workflow across every page in parallel.
- Aggregating per-page folio JSON into a document-level folio map.
- Reconciling Roman-numeral front matter against Arabic body numbering.
- Detecting suspicious jumps in the folio sequence and surfacing them for review.
- Propagating `page_label` into downstream per-page asset records.
- Treating unresolved or contradictory folio reports as degraded output requiring human acknowledgment before downstream use.

## Tool use

### Preferred tool order

Reasoning-first: this workflow is VLM-driven. The agent reads the page PNG as multimodal input and writes one JSON file. There are no deterministic helpers inside this workflow.

Deterministic tools run outside this workflow, under the `pdf2md-orchestration` orchestrator (folio-map assembly, reconciliation against the physical sequence, propagation into per-page asset records, etc.).

### Allowed deterministic tools

#### Operationally invoked

- None inside this workflow. Operational deterministic tools are invoked by `pdf2md-orchestration`, not by the folio-extract worker.

### Expected use of reasoning

Reasoning is limited to:

- Locating the printed folio in conventional folio zones on the page image.
- Transcribing the visible glyph verbatim (Arabic / Roman / prefixed / hyphenated forms) without normalization.
- Naming the zone (`top-left`, `top-center`, `top-right`, `bottom-left`, `bottom-center`, `bottom-right`).
- Assigning a confidence label based on legibility and zone conventionality.
- Recognizing when no folio is printed and emitting `NO_FOLIO` rather than inventing a value.

The page image is the sole authority for folio existence and form.

### Disallowed use

- MUST NOT crop images.
- MUST NOT write PNG, CSV, or XLSX files.
- MUST NOT rewrite Markdown.
- MUST NOT assemble or aggregate folio maps.
- MUST NOT read files outside `IMAGE_PATH`.
- MUST NOT write files outside `OUTPUT_PATH`.
- MUST NOT consult neighbouring page images, sibling folio JSON, manifests, the source PDF, the page Markdown, or any TOC / outline artifact.
- MUST NOT invent a folio from the physical PDF sequence (`PAGE_NUM`).
- MUST NOT infer a folio from neighbouring pages' numbering.
- MUST NOT normalize Roman numerals to Arabic, strip section prefixes, or zero-pad.
- MUST NOT assign final stable filenames.

### Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` - page-level folio JSON

The output filename is deterministic from the orchestrator brief. The workflow must not derive or modify it.
