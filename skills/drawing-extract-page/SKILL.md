---
name: drawing-extract-page
description: Per-page bounded extraction of structured data from a single engineering drawing page image, using crop-first multiblock VLM reasoning. Drawing-type-aware (PFD implemented; P_AND_ID, ISOMETRIC, GA stubbed). Invoked by the DRAWING_EXTRACT orchestrator for per-page fanout.
compatibility: Chirality TASK; invoked by DRAWING_EXTRACT orchestrator for per-page fanout
metadata:
  chirality-skill-version: "2"
  chirality-task-profile: NONE
---

# SKILL — drawing-extract-page

Scope note: this skill is PFD-equipment-scoped in the implemented runtime. Drawing-set titleblock inventory uses `drawing-titleblock-page`; P&ID valve counting uses `pandid-valve-tile`.

## Purpose

Read **one engineering drawing page image** and extract **targeted structured information** from that page against an explicit `DRAWING_TYPE` + `EXTRACTION_TARGET`. This is a **bounded extraction** skill, not a full-page transcription skill.

One invocation processes one page and writes exactly one output artifact. No cross-page context. Orchestrator dispatches one invocation per page for parallelism.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `DRAWING_EXTRACT` orchestrator.

Not the best fit for:
- full-page transcription (use `pdf2md-page` or `PDF2MD_PAGE` instead)
- multi-page context reasoning (orchestrator owns that)
- orchestration/dispatch itself (the parent `DRAWING_EXTRACT` persona owns that)

## Drawing-type + extraction-target registry

This skill is drawing-type-aware. Only `PFD` is implemented in v2. Other types are registered as stubs and fail fast at orchestrator entry.

| drawing_type | status | extraction_target | status |
|--------------|--------|-------------------|--------|
| `PFD` | implemented | `top_equipment_header_basic` | implemented |
| `PFD` | implemented | `top_equipment_header_detailed` | implemented |
| `P_AND_ID` | stubbed (fail-fast) | — | — |
| `ISOMETRIC` | stubbed (fail-fast) | — | — |
| `GA` | stubbed (fail-fast) | — | — |

### Valid combinations (v2)
- `(PFD, top_equipment_header_basic)`
- `(PFD, top_equipment_header_detailed)`

Any other combination rejects at orchestrator Phase 0 pre-flight with `drawing_type '{type}' is registered but not implemented; see 'How to add a new drawing type' in AGENT_DRAWING_EXTRACT.md`.

### Stubbed-type behavior

When the skill receives a `DRAWING_TYPE` of `P_AND_ID`, `ISOMETRIC`, or `GA`, it immediately returns `RUN_STATUS=FAILED_INPUTS` and writes a failure placeholder noting the type is registered but not implemented. No page-image reading or VLM reasoning is performed.

### Legacy compatibility shim (v2 transitional)

For one slice, this skill accepts the legacy `EXTRACTION_MODE=top_equipment_header_with_dwg` runtime override and remaps it to `DRAWING_TYPE=PFD`, `EXTRACTION_TARGET=top_equipment_header_basic`. A deprecation warning is emitted. Any other legacy `EXTRACTION_MODE` value rejects with `unknown EXTRACTION_MODE '{value}'; use DRAWING_TYPE + EXTRACTION_TARGET`.

If both legacy and new parameters are provided, new parameters take precedence and a warning is emitted.

## Inputs

### Required (both targets)

- `RuntimeOverrides.IMAGE_PATH` — absolute path to the drawing page PNG
- `RuntimeOverrides.OUTPUT_PATH` — absolute path to write the extraction output
- `RuntimeOverrides.PAGE_NUM` — 1-indexed page number
- `RuntimeOverrides.TOTAL_PAGES` — total pages in the source document
- `RuntimeOverrides.DRAWING_TYPE` — `PFD` (v2 implemented types only)
- `RuntimeOverrides.EXTRACTION_TARGET` — target for the drawing type

### Required (detailed target only)

- `RuntimeOverrides.REQUESTED_KNOWN_FIELDS` — list of catalog field names (possibly empty)
- `RuntimeOverrides.EXTRA_FIELDS` — list of `{name, description}` pairs (possibly empty)
- `RuntimeOverrides.REQUIRED_FIELDS` — warning-only subset of requested fields (possibly empty)

### Strongly recommended

- `RuntimeOverrides.HEADER_IMAGE_PATH` — cropped top-header PNG for the same page
- `RuntimeOverrides.TITLEBLOCK_IMAGE_PATH` — cropped title-block PNG for the same page

### Optional

- `RuntimeOverrides.HEADER_SLICE_PATHS` — ordered list of overlapping top-header slice PNGs for multiblock review
- `RuntimeOverrides.SOURCE_PDF_NAME` — PDF filename for provenance in output

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `IMAGE_PATH` | Absolute path to drawing page PNG | **Required** | `.png` file path |
| `HEADER_IMAGE_PATH` | Absolute path to cropped top-header PNG | None | `.png` file path |
| `TITLEBLOCK_IMAGE_PATH` | Absolute path to cropped title-block PNG | None | `.png` file path |
| `HEADER_SLICE_PATHS` | Ordered list of overlapping header slice PNGs | `[]` | List of `.png` file paths |
| `OUTPUT_PATH` | Absolute path for the single output artifact | **Required** | Parent directory must exist; must be a `.md` file |
| `PAGE_NUM` | 1-indexed page number | **Required** | Positive integer |
| `TOTAL_PAGES` | Total pages in source PDF | **Required** | Positive integer |
| `DRAWING_TYPE` | Drawing-type selector | **Required** | `PFD` (v2); `P_AND_ID`/`ISOMETRIC`/`GA` (stubbed fail-fast) |
| `EXTRACTION_TARGET` | Target within the drawing type | **Required** | See registry above |
| `REQUESTED_KNOWN_FIELDS` | Catalog fields to capture (detailed only) | `[]` | List of catalog-field names |
| `EXTRA_FIELDS` | User-defined fields (detailed only) | `[]` | List of `{name, description}` pairs |
| `REQUIRED_FIELDS` | Warning-only required subset (detailed only) | `[]` | Subset of requested fields |
| `SOURCE_PDF_NAME` | PDF filename for provenance | None | Any string |
| `EXTRACTION_MODE` | Legacy compatibility alias (deprecated) | None | `top_equipment_header_with_dwg` only |

### Known-field catalog (v2)

Documented here as authoritative source. Catalog changes require a skill version bump.

| Field | One-line semantic definition |
|-------|------------------------------|
| `equipment_type` | Broad equipment class (e.g., "VESSEL", "PUMP", "COMPRESSOR", "EXCHANGER", "DRUM", "DRIVER", "HEATER") |
| `equipment_description` | Specific equipment descriptor: make/model, pump or exchanger type, redundancy configuration, vessel internals, or other identifying detail (e.g., "ARIEL KBZ/6", "VERTICAL INLINE CENTRIFUGAL", "2 x 50%", "TWO PHASE c/w CYCLONIC ELEMENT", "8 POLE INDUCTION MOTOR") |
| `capacity_text` | Throughput, volume, thermal duty, or capacity rating (e.g., "1624 kW", "4.2 m3", "100 BBL/day") |
| `power_text` | Motor/driver rating or power specification (e.g., "100 HP", "5000 kW @ 891 RPM", "6700 BHP @ 891 RPM") |

All catalog fields are free-text descriptors in v2; no controlled vocabularies. Operators extend a run via `EXTRA_FIELDS`, not by implicitly redefining the catalog.

## Read boundary

Reads are limited to:

- `IMAGE_PATH` — current page drawing PNG
- `HEADER_IMAGE_PATH` — current page top-header crop (when provided)
- `TITLEBLOCK_IMAGE_PATH` — current page title-block crop (when provided)
- each path in `HEADER_SLICE_PATHS` — current page header slices (when provided)

The skill MUST NOT read any other files, and MUST NOT use any cross-page context.

## Write boundary

Writes are limited to:

- `OUTPUT_PATH` — exactly one structured artifact per invocation

No other files are written. `OUTPUT_PATH`'s parent directory must already exist; the skill does not create directories.

**In v2, the only canonical per-page artifact format is `markdown_stub` (a `.md` file with YAML frontmatter + findings table).** Per-page CSV output is not supported in v2.

## Tool usage

- No deterministic tools. This skill is VLM-reasoning-only (the agent reads image files directly via the Read tool).
- The `allowed-tools` frontmatter field is intentionally omitted.
- The orchestrator (parent `DRAWING_EXTRACT` agent) is responsible for any deterministic PDF-level cross-checking, header/title-block crop preparation, schema-consistency validation, and stub assembly. This skill does not invoke PDF-level tools itself.
- See `AGENT_DRAWING_EXTRACT.md` § RATIONALE ("Why VLM for page extraction" and "Why crop-first with full-page context as fallback") for the design rationale behind the VLM/deterministic split and the crop-first workflow.

Disallowed behavior:
- No deterministic tool invocation; no shell commands.
- No writing outside `OUTPUT_PATH`.
- No reading of files outside the declared read boundary (no cross-page context, no Scoping.md, no other page images).
- No sub-agent fanout.

## Self-describing stub frontmatter schema (v2)

Every output stub (both basic and detailed targets) begins with YAML frontmatter carrying metadata that makes the stub self-describing. This enables deterministic assembly, schema-consistency validation, and safe resume.

### `top_equipment_header_basic` frontmatter keys (required)

```yaml
---
drawing_type: PFD
extraction_target: top_equipment_header_basic
source_pdf: <filename>
source_page: <integer>
drawing: <DWG NO.>
system_name: <title-block system name>
status: SUCCESS | NO_FINDINGS | FAILED_INPUTS | FAILED
finding_count: <integer>
---
```

### `top_equipment_header_detailed` frontmatter keys (required)

```yaml
---
drawing_type: PFD
extraction_target: top_equipment_header_detailed
source_pdf: <filename>
source_page: <integer>
requested_known_fields: [<catalog field names>]
requested_extra_fields:
  - name: <extra field name>
    description: <semantic description>
required_fields: [<required subset>]
drawing: <DWG NO.>
system_name: <title-block system name>
status: SUCCESS | NO_FINDINGS | FAILED_INPUTS | FAILED
finding_count: <integer>
---
```

`finding_count` is the number of meaningful equipment rows in the findings table (rows with a non-empty `equipment_number`, `equipment_name`, or `drawing`). For `NO_FINDINGS` stubs, `finding_count` is `0`. The post-dispatch validator and sanitizer both require `finding_count` on SUCCESS stubs and reject the stub if the parsed row count does not match.

Empty lists are represented as `[]`. All required keys must be present even when values are empty.

## EXTRA_FIELDS — naming rules

Every element of `requested_extra_fields` has shape `{name, description}`:

- `name` MUST match regex `^[a-z][a-z0-9_]*$` (lowercase ASCII letters/digits/underscores, starting with letter), max 40 characters
- `description` MUST be non-empty, max 200 characters, single line

### Collision rules (fail-fast at orchestrator pre-flight; skill also validates if dispatched directly)

| Collision | Behavior |
|-----------|----------|
| `name` matches base column (`equipment_number`, `equipment_name`, `system_name`, `drawing`, `source_page`) | REJECT: `extra field name '{name}' collides with base column` |
| `name` matches any catalog field (requested or not) | REJECT: `extra field name '{name}' collides with known-field catalog entry '{field}'` |
| Two extra fields share same `name` in one run | REJECT: `duplicate extra field name '{name}'` |
| `name` does not match regex | REJECT: `invalid extra field name '{name}'; must match /^[a-z][a-z0-9_]*$/` |

## Spatial association rule (detailed target)

For `top_equipment_header_detailed`, descriptor text is associated with a parent equipment item by **bounded local grouping** within the top-header region:

1. The **tag/name cluster** is the anchor for each equipment item.
2. **Subordinate descriptor lines** directly beneath or immediately adjacent within the same equipment block attach to that item.
3. Helper crops (`HEADER_IMAGE_PATH`, `HEADER_SLICE_PATHS`) are the **primary reading region** for descriptor discovery.
4. If descriptor text clearly belongs to a different adjacent item, do not attach it to this item.
5. If a descriptor line straddles two items and ownership is ambiguous, **leave the affected requested field blank** rather than invent.
6. **Detail capture is subordinate to correct row identity.** Do not sacrifice tag/name correctness for aggressive detail fill.

### Crops-only for detail discovery

**The full-page `IMAGE_PATH` is not consulted to discover detail field values.** Detail text must be visible in the helper crops (`HEADER_IMAGE_PATH` or `HEADER_SLICE_PATHS`). The full-page image may still be used to resolve local spatial context (e.g., which parent item a descriptor visible in a crop belongs to), but it is never a source of new detail content the crop does not show.

If a page's descriptor text is not captured by the current helper crops (crop geometry insufficient), the page-level override workflow applies — operator re-invokes `prepare_header_crops.py --pages N --header-height-ratio X` for the affected page and re-dispatches the page worker. This is documented in the orchestrator runbook.

## Method

### Step 1 — Validate inputs

1. Confirm `IMAGE_PATH` exists and is a `.png` file.
2. If provided, confirm `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and each path in `HEADER_SLICE_PATHS` exists and is a `.png` file.
3. Confirm `OUTPUT_PATH` parent directory exists and that `OUTPUT_PATH` has a `.md` extension.
4. Resolve effective `DRAWING_TYPE` + `EXTRACTION_TARGET` (apply compatibility shim if `EXTRACTION_MODE` provided).
5. Confirm `(DRAWING_TYPE, EXTRACTION_TARGET)` is a valid combination per the registry.
6. If `DRAWING_TYPE ∈ {P_AND_ID, ISOMETRIC, GA}`: write failure placeholder + return `RUN_STATUS=FAILED_INPUTS` with `note=drawing_type '{type}' is registered but not implemented`.
7. For detailed target: validate `EXTRA_FIELDS` name collisions + regex; validate `REQUIRED_FIELDS` is a subset of `REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name`.
8. If any input is invalid, write a failure placeholder to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.

### Step 2 — Read and inspect the page image (crop-first)

1. Use the Read tool to load `IMAGE_PATH`.
2. If provided, also load `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and every path in `HEADER_SLICE_PATHS`.
3. Identify the following page regions as needed by the extraction target:
   - the **top-of-sheet separated equipment header region**
   - the **title block / `DWG NO.` region**
   - the **title block title region** containing the project line, system-name line, and title suffix line
4. **Prefer helper crops over the full-page image for bounded reading:**
   - use `TITLEBLOCK_IMAGE_PATH` first for `DWG NO.` and `system_name`
   - use `HEADER_IMAGE_PATH` and `HEADER_SLICE_PATHS` first for equipment findings (both targets) **and for detail discovery (detailed target)**
   - use the full-page image only to resolve current-page spatial context when a helper crop is insufficient for identity/association — **never to discover detail values**
5. Ignore decorative borders, general process lines, and repeated in-body equipment tags unless the extraction target explicitly requires them.

### Step 3 — Extract according to target

#### For `top_equipment_header_basic`:

1. Extract the page `DWG NO.` from the title block.
2. Extract `system_name` from the title block as the line between the project line and the title suffix line.
3. Inspect the separated equipment/header region at the top of the sheet.
4. For each equipment item in that top region, extract:
   - `equipment_number`
   - `equipment_name`
   - `system_name` = extracted title-block `system_name`
   - `drawing` = extracted `DWG NO.`
   - `source_page` = `PAGE_NUM`
5. **When helper slices are provided, inspect all slices before concluding extraction is complete.**
6. **When the top header is arranged as multiple separated clusters across the page width, treat each underlined tag/name cluster as an independent finding even if some clusters sit lower than others within the same header band.**
7. **Deduplicate within the page only when the same tag/name cluster appears in overlapping slices; do not collapse distinct grouped-tag findings.**
8. If the top-of-sheet region contains no relevant equipment header, record **no findings**.
9. Do not backfill from the body of the drawing when the top header is absent.
10. If the apparent top region contains only notes, setpoints, spec text, or instrument/control annotations rather than discrete equipment header blocks, record **no findings**.

#### For `top_equipment_header_detailed`:

1. Perform all steps 1-10 from `top_equipment_header_basic` (base fields + identity).
2. For each identified equipment item, additionally extract **only the fields listed in `REQUESTED_KNOWN_FIELDS`** (from the catalog) and **only the fields listed in `EXTRA_FIELDS`** (user-defined), per the spatial association rule.
3. A field that is visible in the crop but belongs to a different adjacent item is NOT attached to the current item.
4. A field that is not present on the page → emit **blank** (empty string) for that column, do not invent.
5. A field that has ambiguous ownership between two items → emit **blank**, do not invent.
6. Requested fields that are not visible for an item are blank, not failures. `REQUIRED_FIELDS` generate warnings post-extraction, not failures.
7. Do not emit catalog or extra fields that were not requested for this run.

### Step 4 — Apply extraction rules (both targets)

**RULE 1 — NO INVENTION**
- Extract only what is visible.
- If a tag or name is ambiguous, preserve what is legible and do not normalize beyond certainty.
- Detail fields (detailed target): blank is always a valid emit; inventing values is invalid.

**RULE 2 — REGION DISCIPLINE**
- Respect the extraction scope.
- Only the separated top header region counts for equipment findings.
- Ignore the right-side notes area even when it sits at the top of the sheet.
- Ignore lower vendor/model/specification lines inside a dense header block if they are not part of the primary equipment name (unless they match a requested detail field per the spatial association rule).
- When helper crops are provided, they define the primary bounded reading region unless they are clearly incomplete for the current page.

**RULE 3 — REQUIRED COMPANION FIELDS**
- `DWG NO.` and `system_name` are mandatory.
- If either cannot be extracted with confidence, return `RUN_STATUS=FAILED` and write a failure artifact.

**RULE 3.5 — TAG REQUIRED FOR A FINDING**
- Do not emit a finding row when `equipment_number` is blank.
- Do not emit control/instrument rows such as setpoint bubbles, controller tags, PSV/PCV/FIC style annotations, or standards references.

**RULE 3.6 — PRIMARY NAME ONLY**
- `equipment_name` must be the primary equipment label only.
- Exclude adjacent notes, duty text, vendor/model text, frame/common-base text, API/TEMA references, dimensions, pressure/temperature setpoints, and operating comments **from `equipment_name`**.
- Detail fields (detailed target) capture this auxiliary content per the spatial association rule — they are the correct home for duty/capacity/power/size/material text.

**RULE 3.7 — MULTI-BLOCK HEADER COMPLETENESS**
- Do not assume all findings share one baseline or appear in one continuous top row.
- On compressor-train style sheets and similar repeated layouts, include lower standalone pump/header blocks and right-side frame blocks when they are still part of the separated top-header region.
- A valid page may contain both left-to-right top-row findings and a second staggered row of findings within the same header band.

**RULE 3.8 — LOW-COUNT SKEPTICISM**
- Do not assume `0`, `1`, or `2` findings are correct simply because a few tags were found.
- If helper slices show additional underlined tag/name clusters, keep extracting until all visible current-page header blocks have been accounted for or explicitly excluded as non-equipment.
- `NO_FINDINGS` is only valid when the bounded header region truly lacks discrete equipment header blocks.

**RULE 4 — GROUPED TAGS**
- Preserve grouped identifiers exactly as shown when they are presented as one item, such as `P-7260-2/7270-2`.

**RULE 5 — EMPTY PAGES ARE VALID**
- If the page has no matching extraction targets, that is a valid result, not an error.

### Step 5 — Write structured output

Write a single `markdown_stub` artifact at `OUTPUT_PATH`:

1. **YAML frontmatter** per the self-describing schema above (fields depend on extraction_target). Must include `finding_count` set to the number of meaningful equipment rows written to the table.
2. **H1 page title** (e.g., `# Page 7 — PFD top_equipment_header_detailed`).
3. **Findings table** with target-appropriate columns:
   - basic: `equipment_number | equipment_name | system_name | drawing` (4 columns)
   - detailed: `equipment_number | equipment_name | system_name | drawing | <requested_known_fields in canonical order> | <requested_extra_fields.name in request order>` (variable columns)
4. **NO_FINDINGS narrative** (when applicable): an empty-row table plus a note stating that no separated top-of-sheet equipment header was identified. `finding_count` must be `0`.
5. **Extraction status line** at bottom (e.g., `- Extraction status: SUCCESS`).

### Canonical output template

Use the exact byte-level shapes below. These are the canonical `render_stub()` outputs for the detailed target.

SUCCESS:

```text
---
drawing_type: PFD
extraction_target: top_equipment_header_detailed
source_pdf: <SOURCE_PDF_NAME>
source_page: 7
requested_known_fields:
  - equipment_type
  - equipment_description
  - capacity_text
  - power_text
requested_extra_fields: []
required_fields:
  - equipment_type
  - equipment_description
  - capacity_text
  - power_text
drawing: <DWG_NO>
system_name: <SYSTEM_NAME>
status: SUCCESS
finding_count: 1
---

# Page 7 — PFD top_equipment_header_detailed

| equipment_number | equipment_name | system_name | drawing | equipment_type | equipment_description | capacity_text | power_text |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <TAG> | <NAME> | <SYSTEM_NAME> | <DWG_NO> | <type or empty> | <desc or empty> | <cap or empty> | <power or empty> |

-
- Extraction status: `SUCCESS`
```

NO_FINDINGS:

```text
---
drawing_type: PFD
extraction_target: top_equipment_header_detailed
source_pdf: <SOURCE_PDF_NAME>
source_page: 7
requested_known_fields:
  - equipment_type
  - equipment_description
  - capacity_text
  - power_text
requested_extra_fields: []
required_fields:
  - equipment_type
  - equipment_description
  - capacity_text
  - power_text
drawing: <DWG_NO>
system_name: <SYSTEM_NAME>
status: NO_FINDINGS
finding_count: 0
---

# Page 7 — PFD top_equipment_header_detailed

| equipment_number | equipment_name | system_name | drawing | equipment_type | equipment_description | capacity_text | power_text |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

- No separated top-of-sheet equipment header was identified.
- Extraction status: `NO_FINDINGS`
```

The format-sensitive elements are fixed:
- YAML lists must use block style in the places shown above.
- The table separator must be the spaced `| --- | --- | ... |` form.
- `status` must be exactly one of `SUCCESS`, `NO_FINDINGS`, `FAILED`, or `FAILED_INPUTS`.
- `finding_count` must equal the number of meaningful equipment rows in the table. The post-dispatch validator and sanitizer both enforce this.

### Step 6 — Return status

Return exactly one of:
- `RUN_STATUS=SUCCESS` — one or more findings were extracted
- `RUN_STATUS=NO_FINDINGS` — page was readable but no relevant extraction target was present
- `RUN_STATUS=FAILED_INPUTS` — inputs were invalid (including stubbed DRAWING_TYPE)
- `RUN_STATUS=FAILED` — page could not be interpreted, or `DWG NO.` / `system_name` could not be extracted

Also return: `PAGE_NUM`, `FINDING_COUNT`, `DWG_NO` (if available), `SYSTEM_NAME` (if available). For detailed target: also `DETAIL_CAPTURE_COUNTS` (map of requested field name → count of populated cells).

## Outputs

- Exactly one `.md` file at `OUTPUT_PATH` (self-describing markdown_stub).
- Structured return values: `RUN_STATUS`, `PAGE_NUM`, `FINDING_COUNT`, `DWG_NO`, `SYSTEM_NAME`. Detailed target also: `DETAIL_CAPTURE_COUNTS`.

## Non-negotiable constraints

- **Single-page scope.** One invocation reads one page. No cross-page context.
- **OUTPUT_PATH-only writes.** Exactly one file is written per invocation. No other side effects.
- **markdown_stub only.** Per-page CSV output is not supported in v2.
- **Self-describing output.** Every stub carries YAML frontmatter identifying drawing_type + extraction_target + (for detailed) requested field sets.
- **Crop-first workflow.** When helper crops and slices are provided, prefer them over the full-page image; use the full page only to resolve spatial context a crop cannot answer alone.
- **Crops-only for detail discovery.** Detail field values must be visible in helper crops; full-page image is never consulted for detail content.
- **Multiblock completeness.** Inspect all provided header slices before concluding; treat each underlined tag/name cluster as an independent finding even across staggered rows.
- **VLM-reasoning contract.** This skill performs bounded visual extraction via direct image inspection, not deterministic tooling.
- **No invention.** Extract only what is visible; do not normalize, backfill, or synthesize. Blank is a valid emit for detail fields.
- **Required companion fields.** `DWG NO.` and `system_name` are mandatory for both targets.
- **Tag required for a finding.** Rows with blank `equipment_number` are invalid.
- **No deterministic PDF-level tools.** PDF-level cross-checking belongs to the orchestrator.
- **NO_FINDINGS is valid.** Empty pages still produce a valid artifact and a `NO_FINDINGS` status.
- **Low-count skepticism.** Treat 0/1/2-finding outcomes skeptically until all helper slices have been accounted for.
- **Stubbed drawing types fail fast.** `P_AND_ID`, `ISOMETRIC`, `GA` reject at input validation with no reading performed.
- **Old-mode contract frozen.** `top_equipment_header_basic` reproduces the legacy `top_equipment_header_with_dwg` behavior with logically-equivalent (not byte-identical) outputs. Base columns and rules are frozen.

## QA expectations

- Exactly one file exists at `OUTPUT_PATH` after the run.
- No files other than `OUTPUT_PATH` were written.
- YAML frontmatter is present and well-formed.
- Frontmatter `drawing_type` + `extraction_target` match the run parameters.
- Detailed target: frontmatter `requested_known_fields` + `requested_extra_fields` + `required_fields` match run parameters.
- When the run succeeded or returned `NO_FINDINGS`, the output contains `DWG NO.` and `system_name`.
- Findings (if any) reflect only the region and semantics required by `EXTRACTION_TARGET`.
- No findings have a blank `equipment_number`.
- Detailed target: requested-but-not-visible detail fields are blank (not "NO_VALUE", not null).
- `RUN_STATUS` is one of: `SUCCESS`, `NO_FINDINGS`, `FAILED`, `FAILED_INPUTS`.
- `FINDING_COUNT` matches the number of populated rows in the output artifact.
- Frontmatter `finding_count` is present and equals the number of meaningful rows in the findings table. The post-dispatch validator and sanitizer both enforce this; a mismatch blocks downstream processing.

## Relationship to DRAWING_EXTRACT

This skill is the per-page worker invoked by the `DRAWING_EXTRACT` orchestrator for per-page fanout. The orchestrator:
- validates `DRAWING_TYPE` + `EXTRACTION_TARGET` (fails fast on stubbed types),
- applies the compatibility shim for legacy `EXTRACTION_MODE`,
- rasterizes the PDF,
- prepares top-header and title-block crops and overlapping header slices,
- dispatches one `TASK` + `drawing-extract-page` invocation per page with drawing_type-aware runtime overrides,
- runs deterministic schema-consistency validation, stub-count reporting, sanitization, and assembly,
- optionally invokes the PFD-equipment repertoire merge suite.

This skill is a sibling of `pdf2md-page` — same per-page fanout pattern, but bounded drawing-type-aware extraction instead of full-page transcription.
