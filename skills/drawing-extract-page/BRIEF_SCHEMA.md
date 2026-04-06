# drawing-extract-page — Brief Schema

Use this skill with a TASK shell dispatched by the `DRAWING_EXTRACT` orchestrator, one invocation per page.

## Basic-target brief example (PFD + top_equipment_header_basic)

```md
PURPOSE: Extract top-of-sheet equipment header from drawing page 7 of 55
RequestedBy: DRAWING_EXTRACT
ActingSurface: TASK+drawing-extract-page

ScopePath: /abs/path/to/drawing_extract_work
TaskSkill: drawing-extract-page

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

## Detailed-target brief example (PFD + top_equipment_header_detailed)

```md
PURPOSE: Extract top-of-sheet equipment header with descriptor fields from drawing page 7
RequestedBy: DRAWING_EXTRACT
ActingSurface: TASK+drawing-extract-page

ScopePath: /abs/path/to/drawing_extract_work
TaskSkill: drawing-extract-page

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

## Required fields (both targets)

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `drawing-extract-page` | Must match skill folder name |
| `AllowedWriteTargets` | `[OUTPUT_PATH]` | Exactly the designated output path |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to page PNG | `.png` extension required |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path for the single output artifact | Must be a `.md` file; parent directory must exist |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total pages in source PDF | Positive integer |
| `RuntimeOverrides.DRAWING_TYPE` | Drawing-type selector | v2 implemented: `PFD`. Stubbed fail-fast: `P_AND_ID`, `ISOMETRIC`, `GA` |
| `RuntimeOverrides.EXTRACTION_TARGET` | Target within the drawing type | See Supported combinations below |

## Required fields (detailed target only)

| Field | Value | Notes |
|---|---|---|
| `RuntimeOverrides.REQUESTED_KNOWN_FIELDS` | List of catalog field names | May be empty `[]`; members must be from v2 catalog |
| `RuntimeOverrides.EXTRA_FIELDS` | List of `{name, description}` pairs | May be empty `[]`; see Name-collision rules |
| `RuntimeOverrides.REQUIRED_FIELDS` | Warning-only subset | May be empty `[]`; must be subset of `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name` |

## Strongly recommended fields

| Field | Notes |
|---|---|
| `RuntimeOverrides.HEADER_IMAGE_PATH` | Top-header crop for crop-first bounded reading |
| `RuntimeOverrides.TITLEBLOCK_IMAGE_PATH` | Title-block crop for `DWG NO.` and `system_name` |
| `RuntimeOverrides.HEADER_SLICE_PATHS` | Overlapping header slices for multiblock completeness and detail discovery |

## Optional fields

| Field | Notes |
|---|---|
| `RuntimeOverrides.SOURCE_PDF_NAME` | Used for provenance in output artifact |
| `RuntimeOverrides.EXTRACTION_MODE` | **Legacy compatibility alias — deprecated.** Accepts only `top_equipment_header_with_dwg`, remapped to `DRAWING_TYPE=PFD` + `EXTRACTION_TARGET=top_equipment_header_basic` with deprecation warning. |

## Supported `DRAWING_TYPE` + `EXTRACTION_TARGET` combinations (v2)

| DRAWING_TYPE | EXTRACTION_TARGET | Status |
|--------------|-------------------|--------|
| `PFD` | `top_equipment_header_basic` | ✅ Implemented |
| `PFD` | `top_equipment_header_detailed` | ✅ Implemented |
| `P_AND_ID` | — | 🚫 Stubbed — fails fast |
| `ISOMETRIC` | — | 🚫 Stubbed — fails fast |
| `GA` | — | 🚫 Stubbed — fails fast |

Any other combination or unknown `DRAWING_TYPE`/`EXTRACTION_TARGET` causes the run to return `RUN_STATUS=FAILED_INPUTS`.

## Known-field catalog (v2)

The `REQUESTED_KNOWN_FIELDS` list may contain any of:

- `equipment_type` — broad equipment class (e.g., VESSEL, PUMP, COMPRESSOR, EXCHANGER, DRUM, DRIVER)
- `equipment_description` — make/model, specific type, configuration, internals (e.g., ARIEL KBZ/6, VERTICAL INLINE CENTRIFUGAL, 2 x 50%, TWO PHASE c/w CYCLONIC ELEMENT)
- `capacity_text` — throughput, thermal duty, or capacity rating (e.g., 1624 kW, 4.2 m3)
- `power_text` — motor/driver power (e.g., 5000 kW @ 891 RPM, 100 HP)

(See `SKILL.md` § Known-field catalog for full semantic definitions.)

## EXTRA_FIELDS — naming rules

Every element has shape `{name, description}`:
- `name` MUST match `^[a-z][a-z0-9_]*$`, max 40 chars
- `description` MUST be non-empty, max 200 chars, single line

### Collision rules (reject at pre-flight)

- `name` MUST NOT collide with base columns (`equipment_number`, `equipment_name`, `system_name`, `drawing`, `source_page`)
- `name` MUST NOT collide with any catalog field name (even if not in `REQUESTED_KNOWN_FIELDS`)
- `name` MUST NOT duplicate another extra field's `name` in the same run

## REQUIRED_FIELDS semantics

`REQUIRED_FIELDS` is a warning-only mechanism. If a required field is absent for a row:
- The row is still emitted.
- The page-worker does not fail.
- Orchestrator QA (via `report_stub_counts.py` detailed mode) emits a per-page warning enumerating missing required fields.

`REQUIRED_FIELDS` entries must be a subset of `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name` (you cannot require what you did not request).

## Canonical per-page artifact format (v2)

Per-page output is always `markdown_stub` — a `.md` file with YAML frontmatter and a findings table. Per-page CSV output is not supported in v2.

Combined CSV is produced by orchestrator-invoked assembly tools from the per-page markdown stubs.

## Per-page artifact path convention (target-aware)

```
{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_page_{NNNN}_stub.md
```

Example:
```
domain-test/domains/West_Doe_Deepcut_DBM/_Sources/PFD/top_equipment_header_detailed/
  PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined_page_0007_stub.md
```

Per-target subdirectories prevent cross-target artifact collisions (basic and detailed do not share stub namespace).

## Resume semantics

Orchestrator validates existing stub YAML frontmatter against the current run's parameters (drawing_type, extraction_target, requested field sets). If any page's existing stub has a schema mismatch:
- Orchestrator rejects the run.
- Operator remediation: (1) clear stubs in the target subdirectory, (2) dispatch to a distinct SOURCE_DIR, or (3) rerun with matching parameters.

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile. It is dispatched by the `DRAWING_EXTRACT` persona for per-page fanout.

## Read boundary

The skill reads only:
- `IMAGE_PATH`
- `HEADER_IMAGE_PATH` (if provided)
- `TITLEBLOCK_IMAGE_PATH` (if provided)
- each path in `HEADER_SLICE_PATHS` (if provided)

The skill MUST NOT read any other files and MUST NOT use any cross-page context.

## Write boundary

The skill writes only:
- `OUTPUT_PATH`

`AllowedWriteTargets` must be exactly the single `OUTPUT_PATH`. The skill does not create directories.

## CustomInstructions

CustomInstructions are not used by this skill. The extraction contract is fully determined by `DRAWING_TYPE` + `EXTRACTION_TARGET` + (for detailed) the requested field lists. Any page-specific interpretation hints from the orchestrator should be attached as separate narrative context in the brief body, not through structured overrides.

## Compatibility shim (one slice, transitional)

If a brief passes `EXTRACTION_MODE=top_equipment_header_with_dwg`:
- The skill remaps to `DRAWING_TYPE=PFD`, `EXTRACTION_TARGET=top_equipment_header_basic`.
- A deprecation warning is emitted.
- The run proceeds normally under the new parameters.

If both legacy `EXTRACTION_MODE` and new `DRAWING_TYPE`/`EXTRACTION_TARGET` are provided, the new parameters take precedence and a warning is emitted.

Any legacy `EXTRACTION_MODE` value other than `top_equipment_header_with_dwg` rejects with `RUN_STATUS=FAILED_INPUTS`.

## Notes

- One brief = one page = one output artifact. The orchestrator spawns one TASK invocation per in-scope page.
- The brief does not include `AllowedTools` because this skill is VLM-reasoning-only with no deterministic tool dependencies.
- All crops and slices are prepared by the orchestrator before dispatch; this skill does not invoke crop-preparation tools itself.
- Per-page crop overrides (for pages where extraction fails due to crop geometry) are invoked by the operator on the orchestrator side, not by this skill.
