# drawing-extract-page contract

## Brief

Use this workflow with a TASK shell dispatched by the `drawing-extract` orchestrator, one invocation per page.

### Basic-target brief example (PFD + top_equipment_header_basic)

```md
PURPOSE: Extract top-of-sheet equipment header from drawing page 7 of 55
RequestedBy: WORKING_ITEMS
ParentWorkflow: drawing-extract
ActingSurface: TASK+drawing-extract-page

ScopePath: /abs/path/to/drawing_extract_work
Workflow: drawing-extract-page

AllowedWriteTargets:
  - "/abs/path/to/_Sources/PFD/top_equipment_header_basic/<pdf_stem>_page_0007_stub.md"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/drawing_extract_work/page_0007.png
  HEADER_IMAGE_PATH: /abs/path/to/drawing_extract_work/page_0007_top_header.png
  TITLEBLOCK_IMAGE_PATH: /abs/path/to/drawing_extract_work/page_0007_titleblock.png
  HEADER_SLICE_PATHS:
    - /abs/path/to/drawing_extract_work/page_0007_top_header_slice_1.png
    - /abs/path/to/drawing_extract_work/page_0007_top_header_slice_2.png
    - /abs/path/to/drawing_extract_work/page_0007_top_header_slice_3.png
    - /abs/path/to/drawing_extract_work/page_0007_top_header_slice_4.png
  OUTPUT_PATH: /abs/path/to/_Sources/PFD/top_equipment_header_basic/<pdf_stem>_page_0007_stub.md
  PAGE_NUM: 7
  TOTAL_PAGES: 55
  DRAWING_TYPE: PFD
  EXTRACTION_TARGET: top_equipment_header_basic
  SOURCE_PDF_NAME: PFD-242510_B_(3-25_Doe)_Process_Flow_Diagram_Combined.pdf

ExpectedOutputs:
  - /abs/path/to/_Sources/PFD/top_equipment_header_basic/<pdf_stem>_page_0007_stub.md
```

### Detailed-target brief example (PFD + top_equipment_header_detailed)

```md
PURPOSE: Extract top-of-sheet equipment header with descriptor fields from drawing page 7
RequestedBy: WORKING_ITEMS
ParentWorkflow: drawing-extract
ActingSurface: TASK+drawing-extract-page

ScopePath: /abs/path/to/drawing_extract_work
Workflow: drawing-extract-page

AllowedWriteTargets:
  - "/abs/path/to/_Sources/PFD/top_equipment_header_detailed/<pdf_stem>_page_0007_stub.md"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/drawing_extract_work/page_0007.png
  HEADER_IMAGE_PATH: /abs/path/to/drawing_extract_work/page_0007_top_header.png
  TITLEBLOCK_IMAGE_PATH: /abs/path/to/drawing_extract_work/page_0007_titleblock.png
  HEADER_SLICE_PATHS:
    - /abs/path/to/drawing_extract_work/page_0007_top_header_slice_1.png
    - /abs/path/to/drawing_extract_work/page_0007_top_header_slice_2.png
    - /abs/path/to/drawing_extract_work/page_0007_top_header_slice_3.png
    - /abs/path/to/drawing_extract_work/page_0007_top_header_slice_4.png
  OUTPUT_PATH: /abs/path/to/_Sources/PFD/top_equipment_header_detailed/<pdf_stem>_page_0007_stub.md
  PAGE_NUM: 7
  TOTAL_PAGES: 55
  DRAWING_TYPE: PFD
  EXTRACTION_TARGET: top_equipment_header_detailed
  REQUESTED_KNOWN_FIELDS:
    - equipment_type
    - equipment_description
    - capacity_text
  EXTRA_FIELDS: []
  REQUIRED_FIELDS: []
  SOURCE_PDF_NAME: PFD-242510_B_(3-25_Doe)_Process_Flow_Diagram_Combined.pdf

ExpectedOutputs:
  - /abs/path/to/_Sources/PFD/top_equipment_header_detailed/<pdf_stem>_page_0007_stub.md
```

### Required fields (both targets)

| Field | Value | Notes |
|---|---|---|
| `Workflow` | `drawing-extract-page` | Must match workflow folder name |
| `AllowedWriteTargets` | `[OUTPUT_PATH]` | Exactly the designated output path |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to page PNG | `.png` extension required |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path for the single output artifact | Must be a `.md` file; parent directory must exist |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total pages in source PDF | Positive integer |
| `RuntimeOverrides.DRAWING_TYPE` | Drawing-type selector | v2 implemented: `PFD`. Stubbed fail-fast: `P_AND_ID`, `ISOMETRIC`, `GA` |
| `RuntimeOverrides.EXTRACTION_TARGET` | Target within the drawing type | See Supported combinations below |

### Required fields (detailed target only)

| Field | Value | Notes |
|---|---|---|
| `RuntimeOverrides.REQUESTED_KNOWN_FIELDS` | List of catalog field names | May be empty `[]`; members must be from v2 catalog |
| `RuntimeOverrides.EXTRA_FIELDS` | List of `{name, description}` pairs | May be empty `[]`; see Name-collision rules |
| `RuntimeOverrides.REQUIRED_FIELDS` | Warning-only subset | May be empty `[]`; must be subset of `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name` |

### Strongly recommended fields

| Field | Notes |
|---|---|
| `RuntimeOverrides.HEADER_IMAGE_PATH` | Top-header crop for crop-first bounded reading |
| `RuntimeOverrides.TITLEBLOCK_IMAGE_PATH` | Title-block crop for `DWG NO.` and `system_name` |
| `RuntimeOverrides.HEADER_SLICE_PATHS` | Overlapping header slices for multiblock completeness and detail discovery |

### Optional fields

| Field | Notes |
|---|---|
| `RuntimeOverrides.SOURCE_PDF_NAME` | Used for provenance in output artifact |
| `RuntimeOverrides.EXTRACTION_MODE` | **Legacy compatibility alias — deprecated.** Accepts only `top_equipment_header_with_dwg`, remapped to `DRAWING_TYPE=PFD` + `EXTRACTION_TARGET=top_equipment_header_basic` with deprecation warning. |

### Supported `DRAWING_TYPE` + `EXTRACTION_TARGET` combinations (v2)

| DRAWING_TYPE | EXTRACTION_TARGET | Status |
|--------------|-------------------|--------|
| `PFD` | `top_equipment_header_basic` | ✅ Implemented |
| `PFD` | `top_equipment_header_detailed` | ✅ Implemented |
| `P_AND_ID` | — | 🚫 Stubbed — fails fast |
| `ISOMETRIC` | — | 🚫 Stubbed — fails fast |
| `GA` | — | 🚫 Stubbed — fails fast |

Any other combination or unknown `DRAWING_TYPE`/`EXTRACTION_TARGET` causes the run to return `RUN_STATUS=FAILED_INPUTS`.

### Known-field catalog (v2)

The `REQUESTED_KNOWN_FIELDS` list may contain any of:

- `equipment_type` — broad equipment class (e.g., VESSEL, PUMP, COMPRESSOR, EXCHANGER, DRUM, DRIVER)
- `equipment_description` — make/model, specific type, configuration, internals (e.g., ARIEL KBZ/6, VERTICAL INLINE CENTRIFUGAL, 2 x 50%, TWO PHASE c/w CYCLONIC ELEMENT)
- `capacity_text` — throughput, thermal duty, or capacity rating (e.g., 1624 kW, 4.2 m3)
- `power_text` — motor/driver power (e.g., 5000 kW @ 891 RPM, 100 HP)

(See `WORKFLOW.md` § Known-field catalog for full semantic definitions.)

### EXTRA_FIELDS — naming rules

Every element has shape `{name, description}`:
- `name` MUST match `^[a-z][a-z0-9_]*$`, max 40 chars
- `description` MUST be non-empty, max 200 chars, single line

#### Collision rules (reject at pre-flight)

- `name` MUST NOT collide with base columns (`equipment_number`, `equipment_name`, `system_name`, `drawing`, `source_page`)
- `name` MUST NOT collide with any catalog field name (even if not in `REQUESTED_KNOWN_FIELDS`)
- `name` MUST NOT duplicate another extra field's `name` in the same run

### REQUIRED_FIELDS semantics

`REQUIRED_FIELDS` is a warning-only mechanism. If a required field is absent for a row:
- The row is still emitted.
- The page-worker does not fail.
- Orchestrator QA (via `report_stub_counts.py` detailed mode) emits a per-page warning enumerating missing required fields.

`REQUIRED_FIELDS` entries must be a subset of `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name` (you cannot require what you did not request).

### Canonical per-page artifact format (v2)

Per-page output is always `markdown_stub` — a `.md` file with YAML frontmatter and a findings table. Per-page CSV output is not supported in v2.

Combined CSV is produced by orchestrator-invoked assembly tools from the per-page markdown stubs.

### Per-page artifact path convention (target-aware)

```
{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_page_{NNNN}_stub.md
```

Example:
```
domains/West_Doe_Deepcut_DBM/_Sources/PFD/top_equipment_header_detailed/
  PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined_page_0007_stub.md
```

Per-target subdirectories prevent cross-target artifact collisions (basic and detailed do not share stub namespace).

### Resume semantics

Orchestrator validates existing stub YAML frontmatter against the current run's parameters (drawing_type, extraction_target, requested field sets). If any page's existing stub has a schema mismatch:
- Orchestrator rejects the run.
- Operator remediation: (1) clear stubs in the target subdirectory, (2) dispatch to a distinct SOURCE_DIR, or (3) rerun with matching parameters.

### Read boundary

The workflow reads only:
- `IMAGE_PATH`
- `HEADER_IMAGE_PATH` (if provided)
- `TITLEBLOCK_IMAGE_PATH` (if provided)
- each path in `HEADER_SLICE_PATHS` (if provided)

The workflow MUST NOT read any other files and MUST NOT use any cross-page context.

### Write boundary

The workflow writes only:
- `OUTPUT_PATH`

`AllowedWriteTargets` must be exactly the single `OUTPUT_PATH`. The workflow does not create directories.

### CustomInstructions

The extraction contract is fully determined by `DRAWING_TYPE` + `EXTRACTION_TARGET` + (for detailed) the requested field lists. When dispatching through TASK with `Workflow: drawing-extract-page`, the TASK shell loads `WORKFLOW.md` and companion files automatically — the orchestrator does not need to inline the full contract.

The orchestrator SHOULD include the following as CustomInstructions to reinforce format-critical requirements as a defense-in-depth measure:

#### Format reminders (recommended)

1. YAML lists use block style (`  - item`) for multi-element lists. Empty lists use inline `[]`.
2. Table separator MUST be the spaced form: `| --- | --- | ... |`
3. `status` MUST be exactly one of: `SUCCESS`, `NO_FINDINGS`, `FAILED`, `FAILED_INPUTS`.
4. `finding_count` MUST equal the number of meaningful equipment rows (non-empty `equipment_number` or `equipment_name` or `drawing`). For `NO_FINDINGS`, `finding_count` MUST be `0`.
5. Data rows MUST have exactly as many columns as the table header (base columns + requested known fields + extra fields).
6. Detail field values must be visible in helper crops. Not visible = blank. Do not invent.

#### Completion checklist (recommended)

- Output file written at OUTPUT_PATH
- YAML frontmatter has all required keys including `finding_count`
- `finding_count` matches the number of meaningful data rows
- Table separator uses spaced form
- All data rows match the column count of the header
- Status is one of the four legal tokens
- No instrument tags (PSV, PCV, FIC, etc.) in findings

Any page-specific interpretation hints from the orchestrator (e.g., "this page is a dense compressor layout, expect 12+ items") should also be attached as CustomInstructions.

### Compatibility shim (one slice, transitional)

If a brief passes `EXTRACTION_MODE=top_equipment_header_with_dwg`:
- The workflow remaps to `DRAWING_TYPE=PFD`, `EXTRACTION_TARGET=top_equipment_header_basic`.
- A deprecation warning is emitted.
- The run proceeds normally under the new parameters.

If both legacy `EXTRACTION_MODE` and new `DRAWING_TYPE`/`EXTRACTION_TARGET` are provided, the new parameters take precedence and a warning is emitted.

Any legacy `EXTRACTION_MODE` value other than `top_equipment_header_with_dwg` rejects with `RUN_STATUS=FAILED_INPUTS`.

### Notes

- One brief = one page = one output artifact. The orchestrator spawns one TASK invocation per in-scope page.
- The brief does not include `AllowedTools` because this workflow is VLM-reasoning-only with no deterministic tool dependencies.
- All crops and slices are prepared by the orchestrator before dispatch; this workflow does not invoke crop-preparation tools itself.
- Per-page crop overrides (for pages where extraction fails due to crop geometry) are invoked by the operator on the orchestrator side, not by this workflow.

## Acceptance

### Minimum checks for a valid run

1. `IMAGE_PATH` exists and is a `.png` file (or `RUN_STATUS=FAILED_INPUTS` was returned).
2. When provided, `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and each `HEADER_SLICE_PATHS` entry exist and are `.png` files.
3. `OUTPUT_PATH` has a `.md` extension and its parent directory exists before the workflow writes to it.
4. `DRAWING_TYPE` is a known value (`PFD`, `P_AND_ID`, `ISOMETRIC`, or `GA`).
5. If `DRAWING_TYPE ∈ {P_AND_ID, ISOMETRIC, GA}`: run returned `RUN_STATUS=FAILED_INPUTS` without reading any image files (stubbed-type fail-fast).
6. `(DRAWING_TYPE, EXTRACTION_TARGET)` is a valid combination per the registry in WORKFLOW.md.
7. For detailed target: `REQUESTED_KNOWN_FIELDS`, `EXTRA_FIELDS`, and `REQUIRED_FIELDS` are present (may be empty lists).
8. Exactly one file exists at `OUTPUT_PATH` after the run.
9. No files other than `OUTPUT_PATH` were written.
10. No files outside the declared read boundary were read (no cross-page context, no other page images).

### Stubbed-type fail-fast expectations

When `DRAWING_TYPE ∈ {P_AND_ID, ISOMETRIC, GA}` is provided:

| Check | Requirement |
|---|---|
| No image reading | The workflow MUST return `RUN_STATUS=FAILED_INPUTS` without calling Read on any image file |
| Clear error message | The failure placeholder at `OUTPUT_PATH` MUST note that the drawing_type is registered but not implemented |
| Extension-point pointer | The message SHOULD point to "How to add a new drawing type" in workflows/drawing-extract/WORKFLOW.md |

### EXTRA_FIELDS collision checks (detailed target)

When `EXTRA_FIELDS` is non-empty, all of the following must hold before any extraction begins:

| Check | Requirement |
|---|---|
| Name regex | Every `name` matches `^[a-z][a-z0-9_]*$`, max 40 chars |
| Description well-formed | Every `description` is non-empty, max 200 chars, single line |
| No base-column collision | No `name` matches `equipment_number`, `equipment_name`, `system_name`, `drawing`, or `source_page` |
| No catalog collision | No `name` matches any catalog field name (even unrequested ones) |
| No intra-run duplicates | No two extra fields share the same `name` |
| REQUIRED_FIELDS subset | Every REQUIRED_FIELDS entry is in `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name` |

Any collision → `RUN_STATUS=FAILED_INPUTS` with error describing which rule fired.

### Self-describing output frontmatter

Every stub output must begin with YAML frontmatter (`---` delimited) that is well-formed and contains target-appropriate keys:

#### Required for `top_equipment_header_basic`

| Key | Constraint |
|---|---|
| `drawing_type` | MUST equal `PFD` |
| `extraction_target` | MUST equal `top_equipment_header_basic` |
| `source_pdf` | MUST match `SOURCE_PDF_NAME` (or `unknown` if unset) |
| `source_page` | MUST equal `PAGE_NUM` as integer |
| `drawing` | MUST be the extracted DWG NO. (or empty for FAILED) |
| `system_name` | MUST be the extracted system name (or empty for FAILED) |
| `status` | MUST be one of `SUCCESS`, `NO_FINDINGS`, `FAILED_INPUTS`, `FAILED` |

#### Required for `top_equipment_header_detailed` (adds to basic)

| Key | Constraint |
|---|---|
| `requested_known_fields` | MUST equal the run's `REQUESTED_KNOWN_FIELDS` list (may be `[]`) |
| `requested_extra_fields` | MUST equal the run's `EXTRA_FIELDS` list (name + description pairs; may be `[]`) |
| `required_fields` | MUST equal the run's `REQUIRED_FIELDS` list (may be `[]`) |

### Required title-block provenance

When `RUN_STATUS` is `SUCCESS` or `NO_FINDINGS`, the output frontmatter must contain:

| Field | Requirement |
|---|---|
| `drawing` | Extracted verbatim from the page title block (`DWG NO.`) |
| `system_name` | Extracted from the title block as the line between the project line and the title suffix line |

If either field cannot be extracted with confidence, `RUN_STATUS=FAILED` must be returned and a failure artifact must still be written to `OUTPUT_PATH`.

### Finding validation (both targets)

Every finding row must satisfy all of the following:

| Check | Requirement |
|---|---|
| Tag present | `equipment_number` is non-blank (blank-tag rows are invalid) |
| Tag verbatim | `equipment_number` is an exact match from the source image, preserving grouped identifiers like `P-7260-2/7270-2` |
| Name is primary label | `equipment_name` is the primary equipment label only — no adjacent notes, duty text, vendor/model text, frame/common-base text, API/TEMA references, dimensions, setpoints, or operating comments |
| No invention | The finding appears in the bounded top-header region of the current page image |
| Region discipline | No findings come from the body of the drawing or from right-side notes areas |
| Companion fields populated | `system_name` and `drawing` match the extracted title-block values; `source_page` matches `PAGE_NUM` |

A run with even one invalid finding row is invalid.

### Detail-field validation (detailed target only)

For each requested detail field:

| Check | Requirement |
|---|---|
| No invention | Any non-blank detail value must be visible in one of the helper crops (`HEADER_IMAGE_PATH` or `HEADER_SLICE_PATHS`) for that equipment item |
| Spatial association | Value attaches to an item only when visible directly beneath or adjacent within the item's own equipment block |
| Ambiguity → blank | When descriptor ownership between two items is unclear, the value is blank (not guessed) |
| Blank-valid | Blank detail values are always valid; never a failure condition |
| Unrequested fields not emitted | A detail field not in `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name` MUST NOT appear in the output table |

### Crops-only-for-detail discipline (detailed target)

| Check | Requirement |
|---|---|
| Full-page not consulted for detail | Detail field values MUST NOT originate from content visible only in `IMAGE_PATH` (full-page); they must be visible in at least one helper crop |
| Spatial-context exception | The full-page image MAY be consulted to resolve parent-item ambiguity for a descriptor visible in a crop, but not to discover new descriptor content |

### Crop-first discipline checks (both targets)

When helper crops were provided:
- The workflow must have inspected `TITLEBLOCK_IMAGE_PATH` first for `DWG NO.` and `system_name`.
- The workflow must have inspected `HEADER_IMAGE_PATH` and all `HEADER_SLICE_PATHS` first for equipment findings.
- The full-page image should only have been used to resolve spatial context that a crop could not answer alone.

### Multiblock completeness checks (both targets)

- All provided `HEADER_SLICE_PATHS` entries must have been inspected before concluding extraction is complete.
- When the top header was arranged as multiple separated clusters across the page width, each underlined tag/name cluster must have been treated as an independent finding.
- Deduplication must have happened only for the same tag/name cluster appearing in overlapping slices; distinct grouped-tag findings must not have been collapsed.
- A valid page may contain both left-to-right top-row findings and a second staggered row of findings within the same header band — both must be represented.

### Low-count skepticism checks (both targets)

- A `NO_FINDINGS` outcome is only valid when the bounded header region truly lacks discrete equipment header blocks.
- A 0/1/2-finding outcome must be corroborated by the helper slices showing no additional underlined tag/name clusters.
- If helper slices show additional clusters that were not extracted, the run is invalid.

### Required-fields warnings (detailed target, orchestrator-side)

`REQUIRED_FIELDS` does NOT fail the page-worker. Instead, orchestrator QA via `report_stub_counts.py` (detailed mode) generates per-page warnings:

| Condition | Warning emitted |
|---|---|
| A row has blank value for a REQUIRED_FIELD | `row {N} on page {P}: missing required field '{field}'` |

Warnings never block assembly.

### Detail capture rate (detailed target, orchestrator-side)

Orchestrator QA computes, per run:
- Per-field detail capture rate = (non-blank cells) / (total rows)
- Suspicious-detail heuristic: if all rows on a page share the identical value for a requested detail field, flag for human review (possible copy-across hallucination)

### Output format validation

Output at `OUTPUT_PATH` must:

1. Begin with YAML frontmatter (`---` delimited) per the self-describing schema above.
2. Contain H1 page title.
3. Contain findings table with target-appropriate columns:
   - basic: `equipment_number | equipment_name | system_name | drawing` (4 columns)
   - detailed: base (4) + requested_known_fields (canonical catalog order) + requested_extra_fields.name (request order)
4. For NO_FINDINGS: an empty-row table plus a note stating that no separated top-of-sheet equipment header was identified.
5. End with extraction status line: `- Extraction status: {SUCCESS|NO_FINDINGS|FAILED_INPUTS|FAILED}`.

Per-page CSV output (`csv_row`) is not supported in v2. A stub with CSV content at `OUTPUT_PATH` is invalid.

### RUN_STATUS expectations

| Status | When returned |
|---|---|
| `SUCCESS` | One or more findings were extracted |
| `NO_FINDINGS` | Page was readable but no relevant extraction target was present |
| `FAILED_INPUTS` | Inputs were invalid (missing file, unsupported combination, stubbed drawing_type, EXTRA_FIELDS collision, etc.) |
| `FAILED` | Page could not be interpreted, or `DWG NO.` / `system_name` could not be extracted with confidence |

`FINDING_COUNT` must match the number of populated rows in the output artifact.

### Failure posture

- On input validation failure: write a failure placeholder to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.
- On stubbed-type dispatch: write failure placeholder with "registered but not implemented" note and return `RUN_STATUS=FAILED_INPUTS` without image reading.
- On interpretation failure: write a failure artifact to `OUTPUT_PATH` and return `RUN_STATUS=FAILED`.
- Never silently drop a page. The orchestrator must always receive exactly one output artifact per dispatched page.

### Success case reporting

A clean run reports:
- `RUN_STATUS` = `SUCCESS` or `NO_FINDINGS`
- `PAGE_NUM`
- `FINDING_COUNT` (integer; `0` for `NO_FINDINGS`)
- `DWG_NO` (extracted drawing number)
- `SYSTEM_NAME` (extracted title-block system name)
- Output file path
- Detailed target only: `DETAIL_CAPTURE_COUNTS` (map of requested field name → count of populated cells)

### Reporting groups

When issues are surfaced to the orchestrator, group them by:

- invalid inputs (missing files, unsupported combination, stubbed drawing_type, EXTRA_FIELDS collision, bad output path)
- missing title-block fields (`DWG NO.` or `system_name` could not be extracted)
- ambiguous tags (tag partially legible or conflicting across slices)
- region boundary uncertainty (whether a block belongs to the top header or the body)
- suspected multiblock incompleteness (helper slices show clusters that were not extracted)
- ambiguous descriptor association (detailed target: descriptor ownership between two items unclear → blank emitted)
- crop insufficiency suspected (detailed target: page may need per-page crop override per orchestrator runbook)

## Tool use

### Preferred tool order

Reasoning-first: this workflow is LLM-driven; no deterministic tool ordering applies. The agent uses its native Read tool to load page images and helper crops, performs VLM reasoning over the image contents, and uses its native Write tool to produce the single output artifact.

### Allowed deterministic tools

#### Operationally invoked

- None — no operational helpers declared (WORKFLOW.md states: "No deterministic tools. This workflow is VLM-reasoning-only"; PDF-level cross-checking belongs to the orchestrator)

### Expected use of reasoning

This workflow is bounded visual extraction via direct image inspection, not deterministic tooling. The agent uses the native Read tool to load the page image (and any provided helper crops and header slices), applies VLM reasoning to identify page regions according to the `DRAWING_TYPE` + `EXTRACTION_TARGET`, applies the extraction rules (no invention, region discipline, required companion fields, primary name only, multi-block header completeness, low-count skepticism, grouped tags, crops-only for detail discovery, spatial association for descriptor text), and writes the structured output with self-describing YAML frontmatter. Reasoning governs every phase: input validation (including DRAWING_TYPE + EXTRACTION_TARGET registry check and EXTRA_FIELDS collision rules), crop-first region identification, per-target extraction, rule application, and output assembly.

### Disallowed use

- No deterministic tool invocation; no shell commands.
- No writing outside `OUTPUT_PATH`.
- No reading of files outside the declared read boundary (no cross-page context, no Scoping.md, no other page images).
- No sub-agent fanout.
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools.
- No writes outside declared scope.
- **Full-page `IMAGE_PATH` is not consulted to discover detail field values** (crops-only for detail discovery); it may only resolve spatial ambiguity for content visible in crops.

### Write boundary

Writes are limited to exactly one file per invocation:

- `OUTPUT_PATH` — exactly one `markdown_stub` artifact (`.md` file) with self-describing YAML frontmatter

Per-page CSV output (`csv_row`) is not supported in v2. Combined CSV is produced by orchestrator-invoked assembly tools from per-page markdown stubs.

No other files are written. `OUTPUT_PATH`'s parent directory must already exist; the workflow does not create directories.
