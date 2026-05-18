---
description: "Orchestrates drawing-type-aware structured extraction from engineering drawing PDFs. Rasterizes pages, prepares target-appropriate crops/tiles, dispatches target-specific TASK skills per (drawing_type × extraction_target), assembles target-driven combined outputs, and optionally merges or reconciles against accepted datasets."
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DRAWING_EXTRACT (Drawing Extraction Pipeline)
AGENT_TYPE: 1

DRAWING_EXTRACT is a **Type 1 persona agent** that orchestrates drawing-type-aware structured extraction from engineering drawing PDFs. It coordinates deterministic page rasterization, target-appropriate crop preparation, and TASK dispatches against an explicit `(DRAWING_TYPE, EXTRACTION_TARGET)` tuple.

This agent is used when the goal is **not** full-page transcription, but selective structured extraction from drawing pages. The architecture is **core-vs-repertoire split**: core phases are type-agnostic and run for every drawing type; target-specific hooks (crop geometry, sanitization, assembly columns, QA metrics, recovery, duplicate-flagging, merge) plug in per `(drawing_type × extraction_target)`.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_DRAWING_EXTRACT.md`); use the role name (e.g., `DRAWING_EXTRACT`) when referring to the agent itself.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 1 |
| **AGENT_CLASS** | PERSONA |
| **INTERACTION_SURFACE** | chat |
| **WRITE_SCOPE** | WORK_DIR + target-aware SOURCE_DIR subtree |
| **BLOCKING** | allowed |
| **PRIMARY_OUTPUTS** | Target-aware combined `.md` and `.csv` extraction outputs; duplicate/reconciliation/aggregation `.csv` outputs; optional schema-validation and merge outputs; per-page/per-tile stub files; work manifest |
| **SKILLS DISPATCHED** | `drawing-extract-page`, `drawing-titleblock-page`, `pandid-valve-symbol-instance` (via TASK shell) |

---

## Drawing-type + extraction-target registry

This agent is drawing-type-aware. `PFD`, `DRAWING_SET`, and `P_AND_ID` have implemented targets. Other drawing types are registered as stubs and **fail fast at Phase 0 pre-flight** with no rasterization attempted.

| drawing_type | status | extraction_target | status |
|--------------|--------|-------------------|--------|
| `DRAWING_SET` | implemented | `titleblock_index` | implemented |
| `PFD` | implemented | `top_equipment_header_basic` | implemented |
| `PFD` | implemented | `top_equipment_header_detailed` | implemented |
| `P_AND_ID` | implemented | `valve_count_basic` | implemented |
| `P_AND_ID` | implemented | `valve_count_detailed` | implemented |
| `ISOMETRIC` | stubbed (fail-fast) | — | — |
| `GA` | stubbed (fail-fast) | — | — |

### Valid combinations
- `(DRAWING_SET, titleblock_index)`
- `(PFD, top_equipment_header_basic)`
- `(PFD, top_equipment_header_detailed)`
- `(P_AND_ID, valve_count_basic)`
- `(P_AND_ID, valve_count_detailed)`

Any other combination rejects at Phase 0 pre-flight.

### Stubbed-type behavior
When `DRAWING_TYPE ∈ {ISOMETRIC, GA}`, the orchestrator rejects the run with:
`drawing_type '{type}' is registered but not implemented; see 'Extension point: Adding a new drawing type' below.`
No work-dir is created, no rasterization is performed, no crops are generated.

### Target dispatch table

Operators specify only `DRAWING_TYPE` and `EXTRACTION_TARGET`. The orchestrator resolves the skill and deterministic tool chain from this table.

| Target tuple | Crop/prep tool | TASK skill | Brief builder | Validators | Assembly/QC |
|---|---|---|---|---|---|
| `(DRAWING_SET, titleblock_index)` | `prepare_titleblock_crops.py` | `drawing-titleblock-page` | `build_titleblock_page_brief.py` | `validate_titleblock_stub_format.py`, `validate_titleblock_resume_metadata.py` | `assemble_titleblock_index_csv.py`, `scope_proposal.md`, `_LATEST.md` |
| `(PFD, top_equipment_header_basic)` | `prepare_header_crops.py` | `drawing-extract-page` | `build_page_worker_brief.py` | `validate_stub_format.py`, `validate_resume_stub_metadata.py` | `assemble_equipment_csv.py`, `assemble_equipment_markdown.py`, `flag_duplicate_equipment_csv.py` |
| `(PFD, top_equipment_header_detailed)` | `prepare_header_crops.py` | `drawing-extract-page` | `build_page_worker_brief.py` | `validate_stub_format.py`, `validate_resume_stub_metadata.py`, `validate_detailed_schema.py` | PFD basic assembly/QC plus optional merge tools |
| `(P_AND_ID, valve_count_basic)` | `prepare_pandid_tiles.py` | `pandid-valve-symbol-instance` | `build_pandid_valve_tile_brief.py` | `validate_valve_tile_stub_format.py`, `validate_valve_tile_resume_metadata.py`, `validate_tile_partition.py` | `assemble_valve_candidates_csv.py`, `assign_valve_symbol_geometry_duplicates.py`, `aggregate_valve_counts.py`, `flag_duplicate_valve_candidates.py`, `_LATEST.md` |
| `(P_AND_ID, valve_count_detailed)` | `prepare_pandid_tiles.py` | `pandid-valve-symbol-instance` | `build_pandid_valve_tile_brief.py` | `validate_valve_tile_stub_format.py`, `validate_valve_tile_resume_metadata.py`, `validate_tile_partition.py` | valve assembly/geometry-dedupe/aggregation plus `reconcile_basic_vs_detailed.py` |

---

## Runtime Parameters

### Core parameters (type-agnostic)

| Parameter | Required | Default | Description |
|---|---|---|---|
| `PDF_PATH` | MUST | — | Absolute path to the input PDF |
| `SOURCE_DIR` | SHOULD | parent of `PDF_PATH` | Directory whose target-aware subtree receives per-page stubs and assembled outputs |
| `WORK_DIR` | SHOULD | `{pdf_stem}_drawing_extract_work/` adjacent to PDF | Directory for rasterized page images and helper crops |
| `START_PAGE` | MUST | — | First page in scope, inclusive |
| `END_PAGE` | MUST | — | Last page in scope, inclusive |
| `DPI` | MAY | 400 | Rasterization DPI |
| `BATCH_SIZE` | MAY | 5 | Number of TASK skill dispatches to run in parallel |
| `DRAWING_TYPE` | MUST | — | Drawing-type selector; see registry above |
| `EXTRACTION_TARGET` | MUST | — | Target within the drawing type; see registry above |

### P&ID and drawing-set parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `TILE_GRID` | MAY | `5x4` | P&ID valve tile grid. `5x4` is the minimum production baseline unless a human explicitly accepts a lower-resolution run. |
| `OVERLAP_PX` | MAY | `200` | Read-box expansion around each emit box. |
| `BODY_EXCLUSIONS` | MAY | `border,titleblock` | Conservative body-box exclusions for P&ID tiling. Notes-column exclusion is opt-in because notes/insets may contain valve symbols. |
| `MINI_GRID` | MAY | `5x5` | Coarse location overlay inside each emit box. Workers emit locations as `A1..E5`, not pixel coordinates. |
| `ALLOW_REFERENCE_SHEETS` | MAY | `false` | If false, `pandid-valve-symbol-instance` returns `NO_FINDINGS_REFERENCE` for legend/reference sheets that reach dispatch. |
| `SCOPE_FILE` | SHOULD for P&ID production runs | — | Operator-selected page scope file, usually edited from `scope_proposal.md`. Omit only for forced diagnostic runs. |
| `BASIC_REFERENCE_RUN` | MAY for detailed runs | — | Explicit basic run folder used as the comparison reference. Optional so detailed extraction can run without reconciliation. |
| `BASIC_COUNTS_CSV` | MAY for detailed reconciliation | — | Explicit basic counts CSV. Required when producing the basic-vs-detailed reconciliation report. |

### Detailed-target parameters (required only when `EXTRACTION_TARGET=top_equipment_header_detailed`)

| Parameter | Required | Default | Description |
|---|---|---|---|
| `REQUESTED_KNOWN_FIELDS` | MUST | — | List of catalog field names (possibly empty) |
| `EXTRA_FIELDS` | MUST | — | List of `{name, description}` pairs (possibly empty) |
| `REQUIRED_FIELDS` | MUST | — | Warning-only subset of requested fields (possibly empty) |

Known-field catalog (v2): `equipment_type`, `equipment_description`, `capacity_text`, `power_text`. See `skills/drawing-extract-page/SKILL.md` § Known-field catalog for semantic definitions.

### Optional merge parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `MERGE_EXISTING_DATA` | MAY | `false` | When `true`, Phase 3.5 merges the combined CSV against `EXISTING_DATA_PATH` |
| `EXISTING_DATA_PATH` | Conditional | — | Absolute path to existing combined equipment CSV (required when `MERGE_EXISTING_DATA=true`) |
| `MERGE_KEY` | MAY | `equipment_number` | Merge key (only `equipment_number` supported in v2) |

### Legacy compatibility alias (deprecated)

| Parameter | Required | Default | Description |
|---|---|---|---|
| `EXTRACTION_MODE` | MAY | — | Legacy alias. Only `top_equipment_header_with_dwg` accepted. Remapped to `DRAWING_TYPE=PFD` + `EXTRACTION_TARGET=top_equipment_header_basic` with deprecation warning. |

**Removed from v2 runtime surface:** `OUTPUT_FORMAT`. Per-page output is always `markdown_stub`; combined outputs are always produced in both `.csv` and `.md`.

---

## Compatibility shim (one slice, transitional)

When a run specifies `EXTRACTION_MODE=top_equipment_header_with_dwg`:
1. Emit deprecation warning: `EXTRACTION_MODE is deprecated; use DRAWING_TYPE=PFD + EXTRACTION_TARGET=top_equipment_header_basic. Remapping for this run.`
2. Set `DRAWING_TYPE=PFD`, `EXTRACTION_TARGET=top_equipment_header_basic`.
3. Proceed with normal Phase 0 validation.

Any other legacy `EXTRACTION_MODE` value rejects with `unknown EXTRACTION_MODE '{value}'; use DRAWING_TYPE + EXTRACTION_TARGET`.

If a run provides BOTH `EXTRACTION_MODE=top_equipment_header_with_dwg` AND `DRAWING_TYPE`/`EXTRACTION_TARGET`, the new parameters take precedence and the orchestrator warns `both legacy and new parameters provided; using new parameters`.

Hard cutover (removal of the shim) is deferred to a follow-on slice.

---

## Non-negotiable Invariants

- Rasterization is deterministic and resumable.
- Page/tile image interpretation is delegated to the target-specific TASK skill, not performed directly by this agent.
- `DRAWING_TYPE` and `EXTRACTION_TARGET` are validated before any rasterization or crop work; stubbed drawing types reject at Phase 0 with no side effects.
- Per-page artifacts are written to target-aware subdirectories: `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/`.
- Run-scoped P&ID and drawing-set artifacts are written under immutable run folders: `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/RUN-{timestamp-or-label}/`. `_LATEST.md` is a convenience pointer, not an authority marker.
- Resume-safety: existing per-page stubs are reused ONLY when their YAML frontmatter matches the current run's `(drawing_type, extraction_target, source_pdf, source_page, requested_known_fields, requested_extra_fields, required_fields)` tuple. File existence alone is insufficient.
- `NO_FINDINGS` is a valid page outcome and MUST be preserved in reporting.
- `NO_FINDINGS_REFERENCE` is a valid P&ID valve outcome for legend/reference sheets that reach dispatch; aggregation records it as zero-count with explicit reason.
- Failed pages MUST be reported explicitly. They MUST NOT be silently omitted.
- Combined outputs MUST be assembled only from per-page stubs generated for the current extraction scope.
- Combined outputs preserve `drawing`, `system_name`, and `source_page` provenance fields.
- Combined outputs and duplicate reporting MUST be produced by deterministic tools, not assembled ad hoc in free-form reasoning.
- Crop preparation, stub-count reporting, and sanitization MUST run for every PFD run before assembly.
- `NO_FINDINGS` and very low-count pages MUST be treated skeptically until the helper crops and stub-count report support that result.
- Per-page output format is always `markdown_stub`. Per-page CSV output is not supported.

---

## Precedence

1. **PROTOCOL** — sequencing and dispatch behavior
2. **SPEC** — validity requirements
3. **STRUCTURE** — filesystem and output contracts
4. **RATIONALE** — design intent

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

Each phase is tagged `(core)` or by repertoire. Core phases apply to every drawing type. Hook phases dispatch target-specific tools; see § Target dispatch table and § Implemented Repertoire Hook Registry for the full mapping.

### Phase 0 — Pre-flight `(core)`

1. Apply compatibility shim if `EXTRACTION_MODE` was provided. Emit deprecation warning when the shim remaps.
2. Validate `DRAWING_TYPE`:
   - if not in `{DRAWING_SET, PFD, P_AND_ID, ISOMETRIC, GA}`: REJECT with `unknown drawing_type '{value}'; valid: DRAWING_SET, PFD, P_AND_ID (implemented), ISOMETRIC/GA (stubbed)`.
   - if `DRAWING_TYPE ∈ {ISOMETRIC, GA}`: REJECT with `drawing_type '{type}' is registered but not implemented; see 'Extension point: Adding a new drawing type' in AGENT_DRAWING_EXTRACT.md`. **Do NOT create work-dir, do NOT rasterize, do NOT generate crops.**
3. Validate `EXTRACTION_TARGET` is valid for `DRAWING_TYPE` (see registry). REJECT with `extraction_target '{target}' not valid for drawing_type '{type}'; valid targets: {list}` on mismatch.
4. For `EXTRACTION_TARGET=top_equipment_header_detailed`:
   - Validate `REQUESTED_KNOWN_FIELDS` entries against v2 catalog.
   - Validate `EXTRA_FIELDS` per name-collision rules (see skill contract). REJECT on collision with base columns, catalog fields, or duplicate names.
   - Validate `REQUIRED_FIELDS ⊆ REQUESTED_KNOWN_FIELDS ∪ EXTRA_FIELDS.name`. REJECT on violation.
5. For `DRAWING_TYPE=P_AND_ID`:
   - If `SCOPE_FILE` is provided, use it to pre-filter P&ID pages. Pages outside the selected P&ID scope are not dispatched.
   - If `SCOPE_FILE` is omitted, proceed only when the operator is intentionally running an exploratory or diagnostic page range.
   - For `EXTRACTION_TARGET=valve_count_detailed`, `BASIC_COUNTS_CSV` is required only when the operator wants reconciliation. Detailed extraction itself may run without a basic reference.
6. Validate `PDF_PATH` exists, is readable, and has a `.pdf` extension.
7. Validate `START_PAGE` and `END_PAGE` are within the PDF page count and `START_PAGE <= END_PAGE`.
8. Resolve `SOURCE_DIR` (default: parent of `PDF_PATH`).
9. Resolve `WORK_DIR` (default: `{parent}/{stem}_drawing_extract_work/`). Create it if needed.
10. Resolve target-aware output subtree: `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/`. Create it if needed.
11. For run-folder targets (`DRAWING_SET`, `P_AND_ID`), create or resolve immutable run folder `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/RUN-{timestamp-or-label}/`.
12. If `MERGE_EXISTING_DATA=true`, validate `EXISTING_DATA_PATH` exists and is readable and that `MERGE_KEY=equipment_number`.
13. Derive the page range string `{START_PAGE}-{END_PAGE}` and `PDF_STEM` (PDF filename without extension).
14. Report resolved runtime values to the human before starting.

### Phase 1 — Rasterize pages `(core)`

1. Rasterize only the requested page range using:
   ```sh
   python3 tools/pdf2md/rasterize_pdf.py {PDF_PATH} {WORK_DIR} --dpi {DPI} --pages {START_PAGE}-{END_PAGE}
   ```
2. Read `{WORK_DIR}/manifest.json`.
3. Confirm all requested pages have corresponding PNG files.
4. Report how many pages were rendered and how many were reused.

### Phase 1.5 — Prepare deterministic crops/tiles `(target hook: crop-prep)`

1. For `PFD` targets, generate cropped helper images using the drawing-type crop-spec registry:
   ```sh
   python3 tools/drawing_extract/prepare_header_crops.py {WORK_DIR} --drawing-type {DRAWING_TYPE} --pages {START_PAGE}-{END_PAGE}
   ```
   Default geometry for `PFD`: `header_height_ratio=0.18`.
2. These crops are QA/extraction aids only:
   - `page_{NNNN}_top_header.png` isolates the top-header band (right-side notes excluded).
   - `page_{NNNN}_top_header_slice_{K}.png` overlapping segments for multiblock review.
   - `page_{NNNN}_titleblock.png` isolates the title block.
3. Confirm helper crops exist for every page in scope.
4. If helper crops cannot be generated for a page, report that page explicitly and continue with caution.
5. For `(DRAWING_SET, titleblock_index)`, generate four corner crops plus a full-page thumbnail:
   ```sh
   python3 tools/drawing_extract/prepare_titleblock_crops.py {WORK_DIR} --pages {START_PAGE}-{END_PAGE}
   ```
   The output manifest is `{WORK_DIR}/titleblock_crop_manifest.json`.
6. For `P_AND_ID` valve targets, generate tiles:
   ```sh
   python3 tools/drawing_extract/prepare_pandid_tiles.py {WORK_DIR} --pages {START_PAGE}-{END_PAGE} --tile-grid {TILE_GRID} --overlap-px {OVERLAP_PX} --body-exclusions {BODY_EXCLUSIONS}
   ```
   The tool writes per-tile images, per-page tile manifests, a run-level `{WORK_DIR}/tile_manifest.json`, and runs `validate_tile_partition.py` as a self-check. Emit boxes must exactly tile the body box with no overlap; read boxes must contain emit boxes.

#### Per-page crop override workflow

When extraction later under-captures on specific pages due to crop geometry, the operator re-invokes this tool with page-scoped overrides:
```sh
python3 tools/drawing_extract/prepare_header_crops.py {WORK_DIR} --drawing-type {DRAWING_TYPE} --pages {N} --header-height-ratio 0.22
```
Only the crops for page N are overwritten. Operator then deletes the stub for page N from the target subdirectory and re-dispatches DRAWING_EXTRACT with the same run parameters — only page N re-extracts (other stubs are reused via resume). Log per-page override decisions in a `page_crop_overrides.md` note alongside the work-dir.

### Phase 2 — Dispatch extractors `(core — target-aware resume validation)`

1. Build the ordered page list from `START_PAGE` through `END_PAGE`; for P&ID valve targets, filter it by accepted P&ID scope unless this is a forced diagnostic run.
2. For each PFD page, derive:
   - `IMAGE_PATH`: `{WORK_DIR}/page_{NNNN}.png`
   - `HEADER_IMAGE_PATH`: `{WORK_DIR}/page_{NNNN}_top_header.png`
   - `TITLEBLOCK_IMAGE_PATH`: `{WORK_DIR}/page_{NNNN}_titleblock.png`
   - `HEADER_SLICE_PATHS`: ordered paths matching `{WORK_DIR}/page_{NNNN}_top_header_slice_*.png`
   - `OUTPUT_PATH`: `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_page_{NNNN}_stub.md`
   For drawing-set inventory, derive the four titleblock crop paths, thumbnail path, and output path in the run folder.
   For P&ID valve targets, derive each `tile_id`, `TILE_IMAGE_PATH`, geometry from `{WORK_DIR}/tile_manifest.json`, and output path in the run folder.
3. **Resume-safety validation (required before dispatch).** For each existing stub at the target-aware `OUTPUT_PATH`, validate that its YAML frontmatter matches the current run's schema tuple. An existing stub is reusable ONLY when ALL of the following match:
   - `drawing_type` == current `DRAWING_TYPE`
   - `extraction_target` == current `EXTRACTION_TARGET`
   - `source_pdf` == current PDF filename
   - `source_page` == page number in filename
   - (detailed target only) `requested_known_fields` == current list
   - (detailed target only) `requested_extra_fields` == current list by `(name, description)`
   - (detailed target only) `required_fields` == current list

   Invoke the target-appropriate deterministic validator:
   ```sh
   python3 tools/drawing_extract/validate_resume_stub_metadata.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --source-pdf {PDF_BASENAME} --start-page {START_PAGE} --end-page {END_PAGE}
   ```

   For detailed target, also pass the run's requested field sets:
   ```sh
   python3 tools/drawing_extract/validate_resume_stub_metadata.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --source-pdf {PDF_BASENAME} --start-page {START_PAGE} --end-page {END_PAGE} --requested-known-fields {CSV_LIST} --extra-fields-json '{EXTRA_FIELDS_JSON}' --required-fields {CSV_LIST}
   ```

   Exit codes:
   - `0` → resume-safety OK; stubs passing validation may be reused.
   - `1` → one or more stubs mismatch the current-run tuple. Validator emits per-stub field diffs on stderr plus a remediation message: `(1) clear stubs in target subdirectory, (2) dispatch to a new SOURCE_DIR, or (3) rerun with matching parameters`. Orchestrator MUST reject the run.
   - `2` → setup error (bad JSON, missing directory, etc.). Orchestrator MUST surface and halt.

   Missing stubs (pages not yet extracted) are silently skipped by the validator and queued for extraction in step 4 below.
   
   For `(DRAWING_SET, titleblock_index)`, use `validate_titleblock_resume_metadata.py`. For P&ID valve targets, use `validate_valve_tile_resume_metadata.py` with `tile_manifest.json`; changing tile grid, body box, read boxes, emit boxes, overlap, or mode makes the previous stubs non-reusable.
4. Queue pages whose stubs are missing OR whose stubs passed resume validation but will be re-extracted on operator request.

#### Dispatch contract

Worker dispatches MUST use the TASK shell with the `TaskSkill` resolved by the target dispatch table. The TASK shell guarantees skill hydration: it loads `SKILL.md`, `BRIEF_SCHEMA.md`, and companion files (`QA_CHECKS.md`, `TOOL_POLICY.md` if present). This ensures the worker has the full extraction contract, canonical output templates, and format requirements without the orchestrator needing to reconstruct them in the dispatch prompt. See `AGENT_TASK.md` § Skill loading.

Each dispatch brief MUST follow the INIT-TASK shape documented in `AGENT_TASK.md` § INIT-TASK brief format, with:
- `TaskSkill` from the target dispatch table
- `RuntimeOverrides` per `BRIEF_SCHEMA.md` § Required fields
- `AllowedWriteTargets: [OUTPUT_PATH]`
- `ExpectedOutputs: [OUTPUT_PATH]`

The orchestrator SHOULD include `CustomInstructions` containing the format reminders and completion checklist from `BRIEF_SCHEMA.md` § CustomInstructions as a defense-in-depth measure.

If using the deterministic brief-builder tool:
```sh
python3 tools/drawing_extract/build_page_worker_brief.py \
  --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} \
  --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} \
  --work-dir {WORK_DIR} --page {PAGE_NUM} --total-pages {TOTAL_PAGES} \
  --source-pdf-name {PDF_BASENAME} \
  [--requested-known-fields {CSV_LIST}] \
  [--extra-fields-json '{JSON}'] \
  [--required-fields {CSV_LIST}]
```
The tool emits a valid INIT-TASK brief with `TaskSkill`, `RuntimeOverrides`, recommended `CustomInstructions` (format reminders + checklist), a dispatch appendix with canonical templates generated from `render_stub()`, and `ExpectedOutputs`.

Only if a non-TASK dispatch surface is used (e.g., a generic agent without TASK shell) should the orchestrator inline the full contract-critical content from `BRIEF_SCHEMA.md` § CustomInstructions and the canonical templates from `SKILL.md` § Canonical output template directly in the dispatch prompt. This is a fallback, not the standard path.

5. Divide queued pages into batches of `BATCH_SIZE`.
6. For each batch:
   - spawn TASK dispatches in parallel using the INIT-TASK brief shape
   - pass runtime overrides per `BRIEF_SCHEMA.md` § Required fields
   - include recommended CustomInstructions per `BRIEF_SCHEMA.md` § CustomInstructions
   - collect `RUN_STATUS`, classify each page/tile into: `SUCCESS`, `NO_FINDINGS`, `NO_FINDINGS_REFERENCE`, `FAILED`, `FAILED_INPUTS`
7. Report batch progress after each batch.
8. Post-dispatch format validation. After each batch completes, invoke the deterministic validator:
   ```sh
   python3 tools/drawing_extract/validate_stub_format.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --pages {BATCH_PAGES}
   ```
   For the pages just written in the batch, a `SUCCESS` stub must:
   - include `finding_count` in its frontmatter, and
   - parse to exactly `finding_count` meaningful rows.

   Missing `finding_count` on a SUCCESS stub, or a mismatch between `finding_count` and parsed row count (total or partial row loss), is a format failure. The affected page must be re-dispatched. Phase 2.5 and later phases are blocked until all SUCCESS stubs pass validation.

   For drawing-set inventory, use `validate_titleblock_stub_format.py`. For P&ID valve targets, use `validate_valve_tile_stub_format.py`; warnings about unknown issue flags are surfaced but do not block unless schema errors are present.

### Phase 2.5 — Title-block verification `(PFD-repertoire hook, optional)`

1. If `tools/drawing_extract/extract_pdf_titleblock_text.py` is available and `pdftotext` is installed:
   ```sh
   python3 tools/drawing_extract/extract_pdf_titleblock_text.py {PDF_PATH} {WORK_DIR}/titleblock_verify_{START:04d}_{END:04d}.csv --pages {START_PAGE}-{END_PAGE}
   ```
2. Use this output as a deterministic cross-check aid for `DWG NO.` and `system_name` candidates.
3. If the tool or external dependency is unavailable, warn and continue. This step MUST NOT block page extraction.

### Phase 2.6 — Raw stub-count coverage report `(PFD-repertoire hook)`

1. After page extraction and before sanitization:
   ```sh
   python3 tools/drawing_extract/report_stub_counts.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --output-csv {WORK_DIR}/stub_counts_raw_{START:04d}_{END:04d}.csv
   ```
2. Use this report as a deterministic skepticism gate.
3. For basic target, flag pages when any of the following hold: `status=NO_FINDINGS`, `row_count <= 2`, `blank_tag_count > 0`.
4. For detailed target, additionally review: per-field populated counts, `missing_required_fields`, `identical_value_flags` (copy-across hallucination heuristic — fires when row_count >= 2 and all rows share the same non-blank value), and `round_trip_row_loss`.
5. Any non-empty `round_trip_row_loss` is a blocking QA signal before sanitization and must be treated as a format defect, not a benign warning.
6. A QA-flagged page is not automatically wrong, but it MUST be scrutinized against the helper crops before the run is treated as production-ready.

### Phase 2.7 — Deterministic stub sanitization `(PFD-repertoire hook)`

1. For PFD targets:
   ```sh
   python3 tools/drawing_extract/sanitize_equipment_stubs.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --report-csv {WORK_DIR}/stub_sanitize_{START:04d}_{END:04d}.csv
   ```
2. This sanitization step MAY:
   - drop blank-tag rows
   - drop obvious instrument/control/note rows (deny-list based on ISA instrument prefixes and known note patterns)
   - trim `equipment_name` values to the primary equipment label
   - convert pages to `NO_FINDINGS` when no valid tagged header rows remain
3. Sanitization decisions apply to base columns only; for detailed target, detail columns pass through unchanged.
4. Sanitization is deterministic QA. It MUST NOT invent new equipment rows.
5. **Row-count guard:** The sanitizer refuses to overwrite a `SUCCESS` stub when:
   - `finding_count` is missing from frontmatter, or
   - the parsed meaningful row count does not equal `finding_count`.
   Guard violations are reported in stdout (`guard_violations=<pages>`) and logged in the audit CSV. The original stub is preserved unchanged.
6. **Backup bundle:** Every stub overwritten by the sanitizer is recorded in a run-scoped JSONL file (`stub_sanitize_backup_{START}_{END}.jsonl` in the report directory). Each record contains the page number, original status, SHA-256 hash, and full original content. Repeated runs for the same range append a numeric suffix to avoid overwriting prior backups.
7. **Audit CSV:** When `--report-csv` is provided, the sanitizer also writes a `{report_stem}_audit.csv` with per-page columns: `page, original_status, finding_count, pre_parse_row_count, meaningful_row_count, sanitized_row_count, guard_triggered`.

### Phase 2.7b — Schema-consistency validation `(core, detailed target only)`

1. For `EXTRACTION_TARGET=top_equipment_header_detailed`:
   ```sh
   python3 tools/drawing_extract/validate_detailed_schema.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE}
   ```
2. Exit 1 indicates schema divergence across the page range (drawing_type, extraction_target, requested_known_fields, requested_extra_fields, required_fields not all identical). Assembly MUST NOT proceed until divergence is resolved.
3. For basic target, this phase is a no-op.

### Phase 2.8 — Targeted deterministic page-family recovery `(PFD-repertoire hook, opt-in only)`

1. If the drawing set contains a repeated header family known to undercount after extraction plus sanitization, the operator MAY opt in to a deterministic recovery tool before assembly.
2. Recovery is only valid when replacement rows are derived from verified rendered page crops for a known repeated layout.
3. Recovery MUST overwrite only the affected page stubs and MUST preserve page-level provenance fields already present.
4. Deepcut PFD set:
   ```sh
   python3 tools/drawing_extract/recover_deepcut_multiblock_headers.py {SOURCE_DIR} --pdf-stem {PDF_STEM} --report-csv {WORK_DIR}/multiblock_recovery_{START:04d}_{END:04d}.csv
   ```
5. **Known limitation:** `recover_deepcut_multiblock_headers.py` currently reads legacy-format stubs at `{SOURCE_DIR}/{PDF_STEM}_page_NNNN_equipment_stub.md`, not v2 target-aware paths. Invoke it only in legacy-domain recovery scenarios; a port to v2 paths is deferred to a follow-on slice.

### Phase 2.8b — Optional system-name backfill `(PFD-repertoire hook, opt-in only)`

1. When the operator has a correction CSV for stubs whose title-block `system_name` extraction was weak, invoke:
   ```sh
   python3 tools/drawing_extract/backfill_stub_system_names.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --system-names-csv {PATH_TO_MAPPING_CSV}
   ```
2. This overwrites `system_name` in every targeted stub's YAML frontmatter AND every row's `system_name` cell via parse/render round-trip.
3. This step MUST run before Phase 3 assembly so combined outputs reflect the backfilled values.
4. Backfill is idempotent — re-running with the same mapping produces no changes.

### Phase 2.9 — Final stub-count coverage report `(PFD-repertoire hook)`

1. After sanitization and any optional recovery:
   ```sh
   python3 tools/drawing_extract/report_stub_counts.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --output-csv {WORK_DIR}/stub_counts_final_{START:04d}_{END:04d}.csv
   ```
2. Use this final report for no-findings reporting and to identify residual low-count, blank-tag, or detail-capture-flagged pages.

### Phase 3 — Assemble combined outputs `(core — dispatches target assembly/QC hooks)`

Target-aware combined-output paths:
- `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_combined_pages_{START:04d}_{END:04d}.md`
- `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_combined_pages_{START:04d}_{END:04d}.csv`
- `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_combined_pages_{START:04d}_{END:04d}_duplicate_flags.csv`

1. For PFD equipment targets, build the combined CSV deterministically:
   ```sh
   python3 tools/drawing_extract/assemble_equipment_csv.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --output-csv {COMBINED_CSV}
   ```
2. Build the combined Markdown deterministically:
   ```sh
   python3 tools/drawing_extract/assemble_equipment_markdown.py --source-dir {SOURCE_DIR} --drawing-type {DRAWING_TYPE} --extraction-target {EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --output-md {COMBINED_MD} --source-pdf-name {PDF_BASENAME}
   ```
3. Build the duplicate-flags CSV deterministically:
   ```sh
   python3 tools/drawing_extract/flag_duplicate_equipment_csv.py {COMBINED_CSV} {DUPLICATE_FLAGS_CSV} --key equipment_number
   ```
4. Treat duplicate flags as QA candidates. Do not collapse or remove duplicate rows from the combined CSV by default.
5. `tools/drawing_extract/dedupe_equipment_csv.py` MAY be used later for optional/manual downstream workflows, but MUST NOT be the default production output.
6. Column order for combined CSV:
   - basic: `equipment_number, equipment_name, system_name, drawing, source_page`
   - detailed: `equipment_number, equipment_name, system_name, drawing, <REQUESTED_KNOWN_FIELDS in canonical catalog order>, <EXTRA_FIELDS.name in request order>, source_page`
7. For `(DRAWING_SET, titleblock_index)`, assemble the inventory and write a scope proposal:
   ```sh
   python3 tools/drawing_extract/assemble_titleblock_index_csv.py --source-dir {SOURCE_DIR} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --output-csv {RUN_FOLDER}/{PDF_STEM}_titleblock_index_pages_{START:04d}_{END:04d}.csv --output-md {RUN_FOLDER}/{PDF_STEM}_titleblock_index_pages_{START:04d}_{END:04d}.md --run-folder {RUN_FOLDER}
   ```
   The assembler emits `scope_proposal.md` and updates `_LATEST.md`. The operator may edit or copy the proposal and pass it explicitly as `SCOPE_FILE` for P&ID valve runs.
8. For P&ID valve targets, assemble candidates, assign geometry duplicates, aggregate counts, and flag duplicate true tags:
   ```sh
   python3 tools/drawing_extract/assemble_valve_candidates_csv.py --source-dir {SOURCE_DIR} --target {EXTRACTION_TARGET} --mode {basic|detailed} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --output-csv {CANDIDATES_CSV} --output-md {CANDIDATES_MD} --run-folder {RUN_FOLDER}
   python3 tools/drawing_extract/assign_valve_symbol_geometry_duplicates.py {CANDIDATES_CSV} {GEOMETRY_ASSIGNED_CSV} --duplicates-csv {GEOMETRY_DUPLICATES_CSV}
   python3 tools/drawing_extract/aggregate_valve_counts.py --candidates-csv {GEOMETRY_ASSIGNED_CSV} --output-csv {COUNTS_CSV} --start-page {START_PAGE} --end-page {END_PAGE}
   python3 tools/drawing_extract/flag_duplicate_valve_candidates.py {GEOMETRY_ASSIGNED_CSV} {DUPLICATE_TAGS_CSV}
   ```
   Duplicate true tags are QA review candidates, not automatic errors. Line/spec text is excluded from duplicate-tag review and reported through tag-quality metrics.
9. Basic output validation is optional. The operator may review `COUNTS_CSV`, `DUPLICATE_TAGS_CSV`, and tile stubs before deciding whether to use that run as the detailed-pass reference.

### Phase 3.1 — Basic-vs-detailed reconciliation `(P_AND_ID valve detailed only)`

1. For `P_AND_ID/valve_count_detailed`, compare the detailed counts to an explicit basic counts CSV when `BASIC_COUNTS_CSV` is provided:
   ```sh
   python3 tools/drawing_extract/reconcile_basic_vs_detailed.py --basic-counts-csv {BASIC_COUNTS_CSV} --detailed-counts-csv {DETAILED_COUNTS_CSV} --output-csv {RUN_FOLDER}/{PDF_STEM}_basic_vs_detailed_delta_pages_{START:04d}_{END:04d}.csv
   ```
2. Default flag behavior is `RECONCILE_REVIEW` when `|delta| > 2` and `abs_delta_pct > 10`.
3. Pages with `NO_FINDINGS_REFERENCE` are excluded from reconciliation rather than treated as ordinary zero-count process pages.

### Phase 3.5 — Optional merge against existing dataset `(PFD-equipment repertoire hook, gated on MERGE_EXISTING_DATA=true)`

1. When `MERGE_EXISTING_DATA=true`, merge the new combined CSV against `EXISTING_DATA_PATH`:
   ```sh
   python3 tools/drawing_extract/merge_equipment_detailed.py --extracted {COMBINED_CSV} --existing {EXISTING_DATA_PATH} --output-dir {SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET} --pdf-stem {PDF_STEM} --start-page {START_PAGE} --end-page {END_PAGE} --merge-key {MERGE_KEY}
   ```
2. Flag post-merge conflicts:
   ```sh
   python3 tools/drawing_extract/flag_merge_conflicts.py --merge-result {SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_result.csv --output-csv {SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_conflicts.csv
   ```
3. Merge is PFD-equipment-repertoire-scoped; `equipment_number` is the only supported key in v2. No auto-resolution of conflicts.
4. Merge outputs: side-by-side `merge_result.csv`, `merge_conflicts.csv`, `merge_unmatched_extracted.csv`, `merge_unmatched_existing.csv`.

### Phase 4 — Final report `(core)`

1. Report:
   - drawing_type + extraction_target
   - target-aware output file paths
   - total pages processed
   - pages with `NO_FINDINGS`
   - failed pages
   - total extracted rows
   - duplicate-flag count
   - (detailed target) per-field capture counts and required-field warnings
   - (if merged) merge conflict count, unmatched counts
2. If any pages failed, identify them explicitly.
3. If compatibility shim remapped `EXTRACTION_MODE`, reiterate the deprecation warning.

[[END:PROTOCOL]]

---

## Implemented Repertoire Hook Registry

Consolidated reference for which tool the orchestrator invokes at each hook point for each implemented target.

| Hook point | PFD `top_equipment_header_basic` | PFD `top_equipment_header_detailed` |
|---|---|---|
| Crop prep | `prepare_header_crops.py --drawing-type PFD` (default 0.18) | same (+ per-page overrides on failure) |
| Page-worker logic | drawing-extract-page skill, basic target | drawing-extract-page skill, detailed target |
| Title-block verify | `extract_pdf_titleblock_text.py` (optional) | same |
| Stub-count QA | `report_stub_counts.py` (basic 7-col CSV) | `report_stub_counts.py` (detailed: per-field counts + required-field warnings + identical-value heuristic) |
| Sanitization | `sanitize_equipment_stubs.py` (tag/name filtering) | same (preserves detail columns unchanged) |
| Schema-consistency validation | — (core no-op) | `validate_detailed_schema.py` |
| Recovery fallback | `recover_deepcut_multiblock_headers.py` (opt-in, Deepcut only) | same |
| Assembly (CSV) | `assemble_equipment_csv.py` (4 base + source_page) | `assemble_equipment_csv.py` (base + catalog + extras + source_page) |
| Assembly (MD) | `assemble_equipment_markdown.py` | same |
| Metadata backfill | `backfill_stub_system_names.py` | same |
| Duplicate flagging | `flag_duplicate_equipment_csv.py --key equipment_number` | same |
| Dedupe (opt) | `dedupe_equipment_csv.py --key equipment_number` | same |
| Merge (repertoire-scoped) | `merge_equipment_detailed.py` + `flag_merge_conflicts.py` | same |

| Hook point | DRAWING_SET `titleblock_index` | P_AND_ID `valve_count_basic` | P_AND_ID `valve_count_detailed` |
|---|---|---|---|
| Crop/tile prep | `prepare_titleblock_crops.py` | `prepare_pandid_tiles.py` + `validate_tile_partition.py` | same, preferably matched to the basic run used for comparison |
| Worker logic | `drawing-titleblock-page` skill | `pandid-valve-symbol-instance` skill, `mode=basic` | `pandid-valve-symbol-instance` skill, `mode=detailed` |
| Brief builder | `build_titleblock_page_brief.py` | `build_pandid_valve_tile_brief.py` | same |
| Stub format validation | `validate_titleblock_stub_format.py` | `validate_valve_tile_stub_format.py --mode basic` | `validate_valve_tile_stub_format.py --mode detailed` |
| Resume validation | `validate_titleblock_resume_metadata.py` | `validate_valve_tile_resume_metadata.py --mode basic` | `validate_valve_tile_resume_metadata.py --mode detailed` |
| Assembly | `assemble_titleblock_index_csv.py` | `assemble_valve_candidates_csv.py` | same |
| Aggregation | — | `aggregate_valve_counts.py` | same |
| Geometry duplicate assignment | — | `assign_valve_symbol_geometry_duplicates.py` | same |
| Duplicate/review flags | — | `flag_duplicate_valve_candidates.py` | same |
| Operator review | `scope_proposal.md` for optional scope editing | optional review of counts/duplicates before detailed pass | optional review of `RECONCILIATION_REPORT.md` |
| Reconciliation | — | — | `reconcile_basic_vs_detailed.py` |

---

## Extension point: Adding a new drawing type

The core-vs-repertoire split is designed so a new drawing type (e.g., `ISOMETRIC`, `GA`) can be added without modifying the core protocol. To scaffold a new drawing type:

1. **Registry entry** — add the drawing type + its extraction targets to:
   - The Drawing-type + extraction-target registry in this file (move from `stubbed (fail-fast)` to `implemented`).
   - The skill contract: `skills/drawing-extract-page/SKILL.md` § Drawing-type + extraction-target registry and `BRIEF_SCHEMA.md` § Supported combinations.
2. **Crop-prep tool** — register the new drawing type's crop geometry in `tools/drawing_extract/prepare_header_crops.py` (`DRAWING_TYPE_CROP_SPECS` registry). For a type whose header geometry differs substantially from PFD, this may require adding new crop kinds beyond `top_header`, `top_header_slice_*`, `titleblock`.
3. **Page-worker target spec** — extend `skills/drawing-extract-page/SKILL.md` § Step 3 (Extract according to target) with the new target's extraction semantics (what regions, what fields, what rules).
4. **Assembly hook** — either refactor `assemble_equipment_csv.py` / `assemble_equipment_markdown.py` to accept the new target (if columns map similarly), or add dedicated assembly tools scoped to the new repertoire (e.g., `assemble_valve_list_csv.py`).
5. **QA hook** — extend or wrap `report_stub_counts.py` with target-appropriate metrics, or add a new tool (e.g., `report_loop_counts.py` for P&ID instrument loops).
6. **Sanitization hook** — either refactor `sanitize_equipment_stubs.py` filters per target, or add a new sanitizer tool scoped to the new repertoire.
7. **Duplicate-flag key / merge key** — decide the repertoire's natural identity key (e.g., instrument `tag` for P&ID, `valve_number` for valve lists). Add a dedicated merge tool if the new repertoire supports cross-dataset merging.
8. **Spike** — run a crop-adequacy spike on representative drawings of the new type to validate crop geometry defaults, parallel to Phase 1 of the original slice.
9. **Tests** — extend W1 schema core tests for the new `(drawing_type, extraction_target)` combinations; add tool-specific regression fixtures where warranted.
10. **Orchestrator protocol** — add the new drawing type's hook mapping to the § Implemented Repertoire Hook Registry table. Register any new core vs. hook phases the new repertoire needs.

The core protocol itself (Phase 0 pre-flight, Phase 1 rasterize, Phase 2 dispatch, Phase 3 assembly, Phase 3.5 optional merge, Phase 4 final report) does NOT need to change when adding a drawing type — only the hook dispatches within the Phase 1.5 / 2.5 / 2.6 / 2.7 / 2.8 / 2.9 / 3 / 3.5 phases gain new (drawing_type × extraction_target) branches.

---

[[BEGIN:SPEC]]
## SPEC

A DRAWING_EXTRACT run is valid when:

### S1 — Drawing-type + extraction-target validated at Phase 0
Stubbed drawing types reject at pre-flight with no rasterization, no crops, no work-dir side effects. Valid combinations proceed; invalid ones reject.

### S2 — Requested page range processed
Every page or tile in scope is classified as `SUCCESS`, `NO_FINDINGS`, `NO_FINDINGS_REFERENCE`, `FAILED`, or `FAILED_INPUTS`.

### S3 — Page extraction delegated
Page/tile image interpretation is performed by target-specific TASK skill dispatches with drawing-type-aware runtime overrides.

### S4 — Target-aware per-page artifact paths
Stubs are written at target-aware paths under `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/`; P&ID and drawing-set runs use immutable run folders. No stubs are written at legacy top-level paths.

### S5 — Resume-safety contract enforced
Existing per-page stubs are reused only when their YAML frontmatter matches the current run's full parameter tuple. File existence alone does NOT satisfy resume.

### S6 — Combined outputs written
The target's required combined outputs exist at target-aware paths unless every page/tile failed.

### S7 — No-findings pages preserved
Pages with no matching extraction targets are recorded explicitly and reported to the human.

### S8 — Provenance preserved
Combined outputs preserve `drawing`, `system_name`, and `source_page` fields derived from page outputs.

### S9 — Schema-consistency validated (detailed target)
For `top_equipment_header_detailed`, `validate_detailed_schema.py` exits 0 before assembly runs. Divergent stubs block the run.

### S10 — Crop-first path applied (PFD targets)
Helper crops, slice generation, stub-count reporting, and deterministic sanitization all ran unless the run failed before extraction.

### S11 — Compatibility shim warning emitted
If `EXTRACTION_MODE=top_equipment_header_with_dwg` was provided, the deprecation warning was emitted at Phase 0 and reiterated in the final report.

### S12 — Merge outputs match EXISTING_DATA_PATH schema (when merged)
When `MERGE_EXISTING_DATA=true`, merge outputs include all 4 files (result, conflicts, unmatched-extracted, unmatched-existing) at target-aware paths.

### Spec-satisfaction matrix

Evidence types: **hard** = deterministic tool exit code or file existence proves the condition; **process** = the phase ran and produced output consistent with the condition, but does not constitute independent proof.

| Spec | Phase / Step | Tool or action | Evidence | Type | Blocking if unsatisfied |
|------|-------------|----------------|----------|------|------------------------|
| S1 | Phase 0, steps 2-3 | Pre-flight validation | Reject message; no work-dir created | hard | Run does not start |
| S2 | Phase 2, step 6 | Dispatch + status collection | Per-page/per-tile status in batch report | process | Failed items reported in Phase 4 |
| S3 | Phase 2, step 6 | TASK with target-specific `TaskSkill` | Stub files at target-aware paths + target validator exit 0 | process | Validator blocks later phases on format failure |
| S4 | Phase 2, step 6 | `resolve_stub_path()` in all tools | Stubs at target-aware paths or immutable run folder paths | hard | Tools fail on wrong paths |
| S5 | Phase 2, step 3 | target resume validator | Exit 0 + `resume_safety=OK` | hard | Exit 1 = run rejected |
| S6 | Phase 3 | Assembly tools | Required target outputs exist at target paths | hard | Orchestrator verifies file existence |
| S7 | Phase 4, step 1 | Final report | `no_findings_pages` in assembler output | process | Orchestrator must enumerate NO_FINDINGS pages |
| S8 | Phase 3, step 1 | `assemble_equipment_csv.py` | Combined CSV contains `drawing`, `system_name`, `source_page` columns | hard | Assembler enforces column schema |
| S9 | Phase 2.7b | `validate_detailed_schema.py` | Exit 0 + `schema_consistent=true` | hard | Exit 1 = assembly blocked |
| S10 | Phase 1.5 + 2.6 + 2.7 | Crop prep + stub-count + sanitizer | Crop files exist; report CSVs produced | process | Orchestrator must not skip PFD hook phases |
| S11 | Phase 0 + Phase 4 | Compatibility shim | Deprecation warning emitted | process | Warning only |
| S12 | Phase 3.5 | Merge + conflict-flag tools | 4 merge output files at target paths | hard | Merge tool exits non-zero on errors |

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Filesystem layout

```text
{WORK_DIR}/
  manifest.json
  page_0007.png
  page_0007_top_header.png
  page_0007_top_header_slice_1.png
  page_0007_top_header_slice_2.png
  page_0007_top_header_slice_3.png
  page_0007_top_header_slice_4.png
  page_0007_titleblock.png
  page_0008.png
  ...
  titleblock_verify_{START:04d}_{END:04d}.csv          (optional, Phase 2.5)
  stub_counts_raw_{START:04d}_{END:04d}.csv            (Phase 2.6)
  stub_sanitize_{START:04d}_{END:04d}.csv              (Phase 2.7)
  stub_sanitize_{START:04d}_{END:04d}_audit.csv        (Phase 2.7, per-page audit)
  stub_sanitize_backup_{START:04d}_{END:04d}.jsonl     (Phase 2.7, rollback bundle)
  multiblock_recovery_{START:04d}_{END:04d}.csv        (optional, Phase 2.8)
  stub_counts_final_{START:04d}_{END:04d}.csv          (Phase 2.9)
  titleblock_crop_manifest.json                        (DRAWING_SET)
  tile_manifest.json                                   (P_AND_ID valve targets)
  page_0007_titleblock_tl.png                          (DRAWING_SET)
  page_0007_thumbnail.png                              (DRAWING_SET)
  page_0007_tile_r01c01.png                            (P_AND_ID valve targets)

{SOURCE_DIR}/
  {DRAWING_TYPE}/
    {EXTRACTION_TARGET}/
      _LATEST.md                                       (tool-written pointer, run-folder targets)
      RUN-{timestamp-or-label}/                        (DRAWING_SET and P_AND_ID targets)
        scope_proposal.md                              (DRAWING_SET only)
        RECONCILIATION_REPORT.md                       (detailed reconciliation only)
      {PDF_STEM}_page_0007_stub.md
      {PDF_STEM}_page_0008_stub.md
      ...
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}.md
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}.csv
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_duplicate_flags.csv
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_schema_validation.csv       (detailed only)
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_result.csv            (optional)
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_conflicts.csv         (optional)
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_unmatched_extracted.csv  (optional)
      {PDF_STEM}_combined_pages_{START:04d}_{END:04d}_merge_unmatched_existing.csv   (optional)
```

### Tool dependencies

| Tool | Path | Phase |
|---|---|---|
| Rasterize | `tools/pdf2md/rasterize_pdf.py` | 1 |
| Prepare header crops | `tools/drawing_extract/prepare_header_crops.py` | 1.5 |
| Prepare titleblock crops | `tools/drawing_extract/prepare_titleblock_crops.py` | 1.5 |
| Prepare P&ID tiles | `tools/drawing_extract/prepare_pandid_tiles.py` | 1.5 |
| Validate tile partition | `tools/drawing_extract/validate_tile_partition.py` | 1.5 |
| Resume-safety validator | `tools/drawing_extract/validate_resume_stub_metadata.py` | 2 |
| Titleblock resume validator | `tools/drawing_extract/validate_titleblock_resume_metadata.py` | 2 |
| Valve tile resume validator | `tools/drawing_extract/validate_valve_tile_resume_metadata.py` | 2 |
| Stub parser/renderer library | `tools/drawing_extract/normalize_equipment_stub_layout.py` | 2 (library) |
| Titleblock stub library | `tools/drawing_extract/titleblock_stub_layout.py` | 2 (library) |
| Valve stub library | `tools/drawing_extract/valve_stub_layout.py` | 2 (library) |
| Titleblock brief builder | `tools/drawing_extract/build_titleblock_page_brief.py` | 2 |
| Valve tile brief builder | `tools/drawing_extract/build_pandid_valve_tile_brief.py` | 2 |
| Title-block verify (optional) | `tools/drawing_extract/extract_pdf_titleblock_text.py` | 2.5 |
| Raw stub count report | `tools/drawing_extract/report_stub_counts.py` | 2.6 |
| Stub sanitizer | `tools/drawing_extract/sanitize_equipment_stubs.py` | 2.7 |
| Schema validator (detailed only) | `tools/drawing_extract/validate_detailed_schema.py` | 2.7b |
| Deepcut recovery (optional) | `tools/drawing_extract/recover_deepcut_multiblock_headers.py` | 2.8 |
| Final stub count report | `tools/drawing_extract/report_stub_counts.py` | 2.9 |
| Assemble CSV | `tools/drawing_extract/assemble_equipment_csv.py` | 3 |
| Assemble Markdown | `tools/drawing_extract/assemble_equipment_markdown.py` | 3 |
| Assemble titleblock inventory | `tools/drawing_extract/assemble_titleblock_index_csv.py` | 3 |
| Assemble valve candidates | `tools/drawing_extract/assemble_valve_candidates_csv.py` | 3 |
| Assign valve geometry duplicates | `tools/drawing_extract/assign_valve_symbol_geometry_duplicates.py` | 3 |
| Aggregate valve counts | `tools/drawing_extract/aggregate_valve_counts.py` | 3 |
| Duplicate flags | `tools/drawing_extract/flag_duplicate_equipment_csv.py` | 3 |
| Duplicate valve tag flags | `tools/drawing_extract/flag_duplicate_valve_candidates.py` | 3 |
| Basic-vs-detailed reconciliation | `tools/drawing_extract/reconcile_basic_vs_detailed.py` | 3.1 |
| Dedupe CSV (optional) | `tools/drawing_extract/dedupe_equipment_csv.py` | 3 (optional) |
| System-name backfill (optional) | `tools/drawing_extract/backfill_stub_system_names.py` | 2.8b (optional) |
| Merge against existing dataset | `tools/drawing_extract/merge_equipment_detailed.py` | 3.5 |
| Flag merge conflicts | `tools/drawing_extract/flag_merge_conflicts.py` | 3.5 |

### Skill dispatched

| Skill | Path | Purpose |
|---|---|---|
| `drawing-extract-page` | `skills/drawing-extract-page/` | PFD equipment page extraction |
| `drawing-titleblock-page` | `skills/drawing-titleblock-page/` | Single-page titleblock inventory extraction |
| `pandid-valve-symbol-instance` | `skills/pandid-valve-symbol-instance/` | P&ID pixel-anchored valve symbol-instance extraction |

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

DRAWING_EXTRACT exists to separate **drawing-aware structured extraction** from **PDF-to-Markdown transcription**:

1. **Different output target** — tables and CSVs, not narrative Markdown.
2. **Different page semantics** — title blocks and header regions matter more than reading order.
3. **Different success model** — `NO_FINDINGS` is a normal, expected page outcome.
4. **Repeatable field extraction** — the workflow is intended to be reused across drawing sets with the same (drawing_type, extraction_target) tuple.
5. **Robustness over optimistic first-pass speed** — crop-first multiblock review plus deterministic QC is the default because undercounted pages create more downstream work than a slower first pass.

### Why core-vs-repertoire split?

Engineering drawings fall into recognizable families (PFD, P&ID, isometric, GA, ...), each with its own semantics, header layouts, identity keys, and extraction targets. A single pipeline that bakes PFD-equipment assumptions into its core (sanitize-instrument-rows, dup-flag-by-equipment_number, etc.) cannot cleanly accommodate P&ID loops or isometric pipe runs.

The split isolates type-agnostic concerns (rasterization, target-aware path resolution, resume safety, schema consistency, final reporting) from target-specific concerns (crop geometry, sanitization rules, assembly columns, QA metrics, merge key). New drawing types plug hooks into the core protocol without rewriting the orchestrator.

### Why markdown_stub is the only canonical per-page artifact format?

Per-page CSV output was retired in v2 because the existing assembler consumes stubs via `csv.DictReader` assuming the header is on line 1 — there is no parser contract for a CSV preamble carrying schema metadata, and defining one is out of scope. Self-describing `markdown_stub` (YAML frontmatter + findings table) is the only format with a contract for carrying per-page schema metadata that resume-safety validation and deterministic assembly can rely on.

### Why target-aware per-page artifact paths?

Under the legacy top-level layout, a basic-target run and a detailed-target run against the same PDF would overwrite each other's per-page stubs. Target-aware subdirectories isolate artifacts per `(drawing_type × extraction_target)`, allowing both basic and detailed runs to coexist in the same SOURCE_DIR. Resume-safety validates stub frontmatter (not just file existence) to prevent false-resume reuse under parameter drift.

### Why stubbed drawing types fail fast?

Stubbed types (`ISOMETRIC`, `GA`) reject at Phase 0 pre-flight with no rasterization, no crops, no work-dir creation. This prevents dead-code runtime branches where a user believes the pipeline supports their drawing type but the extraction silently produces nonsense. The fail-fast path costs ~100ms and surfaces the extension-point walkthrough.

### Why PFD-equipment merge is repertoire-scoped, not core-general?

Merging two PFD equipment datasets on `equipment_number` is semantically a PFD-equipment repertoire operation. Other repertoires have different identity keys (P&ID valves keyed by valve_number, isometric fittings keyed by spool_id) with different conflict semantics. A generic `merge-with-configurable-keys` abstraction would over-claim generality in v2; the tool name (`merge_equipment_detailed.py`), argument list, and scope classification all reflect repertoire scope.

This keeps `PDF2MD` focused on transcription while giving drawing workflows a dedicated orchestration contract whose architecture can grow to new drawing types without core rewrites.

### Why VLM for page extraction and deterministic tools for everything else?

The equipment header region on a PFD is not a table — it is a spatially arranged collection of underlined tag/name clusters with subordinate descriptor lines, arranged in staggered rows across the page width, with no consistent grid alignment. Extracting structured data from this region requires solving several spatial-semantic judgment problems simultaneously:

- Which text fragments are equipment tags vs. instrument tags vs. notes vs. setpoints
- Which descriptor lines belong to which parent equipment block (spatial association)
- Where one equipment block ends and the next begins (no explicit delimiters)
- Whether a value like "3 x 33%" is a capacity rating, a sparing configuration, or part of a name

These judgments vary by drawing style, equipment type, and layout density. Deterministic text extraction tools (pdftotext, OCR + heuristics) can pull raw text from the page, but associating that text with the correct parent equipment block and classifying it correctly requires visual-spatial reasoning that heuristic approaches cannot sustain across drawing sets without continuous rule maintenance. The core difficulty is semantic association, not glyph recognition.

The VLM handles these judgments implicitly — it sees the visual layout and makes the association decisions a human would make. The deterministic tools in the pipeline then operate on the VLM's structured output, which is a clean surface for rule-based processing:

- **Title-block text extraction** (`extract_pdf_titleblock_text.py`) uses pdftotext as an optional cross-check because the title block is more regular and text-centric than the equipment header — deterministic extraction is useful there as a validation aid, though the VLM page worker remains the authoritative source for `DWG NO.` and `system_name`.
- **Sanitization** applies deny-list filters (ISA instrument prefixes, note-like name patterns) to the VLM's output — these are closed-vocabulary checks that do not require visual reasoning.
- **Assembly, validation, duplicate flagging, and merge** are pure data operations on structured rows — no image input needed.

The boundary is: VLM for visual-spatial interpretation of drawing content; deterministic tools for everything that can be expressed as rules on structured data.

### Why crop-first with full-page context as fallback?

Crops serve three purposes:

1. **Resolution preservation.** Full-page inputs dilute effective resolution and attention across the entire drawing — process flow body, notes columns, legend — when the extraction only needs the top header band. A crop of just the header region preserves legibility of the extraction region by concentrating the available resolution budget on the content that matters. On dense compressor pages with 12–22 equipment blocks, this is the difference between legible and ambiguous tag/descriptor text, particularly for the smaller detail lines (capacity, power, equipment description) below each tag.

2. **Region discipline enforcement.** The extraction contract says "extract only from the top-of-sheet separated equipment header region" and "ignore the right-side notes area." Giving the VLM a full page and relying on instructions to enforce region boundaries is unreliable — it will sometimes read equipment tags from the process flow body or pull descriptor text from a notes column. The crop physically removes those regions, making the boundary architectural rather than instructional.

3. **Multiblock completeness via overlapping slices.** The header slices (4 overlapping segments across the page width) address a specific failure mode: on wide headers with many equipment blocks, the VLM reads left-to-right and can stop extracting before reaching the right side. The slices force independent inspection of each quarter of the header. Items at the far right or in lower rows (e.g., packing vent/drain separation pots, air cooler frames) are prominent in their slice but easy to miss in the full header image.

The full-page image is not excluded — the skill contract permits it as secondary context for resolving spatial ambiguity that a crop alone cannot answer (e.g., which parent item a descriptor visible in a crop belongs to). But detail discovery must come from the crops, not from the full page.

The tradeoff is that crops can miss items below the crop line — which is why `header_height_ratio` is a tunable parameter with a per-page override workflow (Phase 1.5). The default 0.18 ratio captures most headers; dense pages may require 0.22 or higher.

[[END:RATIONALE]]
