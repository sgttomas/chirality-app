# drawing-extract procedure

WORKING_ITEMS coordinates this procedure and assigns bounded visual or semantic stages to TASK. Tool commands resolve against the declared tool root.

Each phase is tagged `(core)` or by repertoire. Core phases apply to every drawing type. Hook phases dispatch target-specific tools; see the target-dispatch registry in CONTRACT.md for the mapping.

### Phase 0 — Pre-flight `(core)`

1. Apply compatibility shim if `EXTRACTION_MODE` was provided. Emit deprecation warning when the shim remaps.
2. Validate `DRAWING_TYPE`:
   - if not in `{DRAWING_SET, PFD, P_AND_ID, ISOMETRIC, GA}`: REJECT with `unknown drawing_type '{value}'; valid: DRAWING_SET, PFD, P_AND_ID (implemented), ISOMETRIC/GA (stubbed)`.
   - if `DRAWING_TYPE ∈ {ISOMETRIC, GA}`: REJECT with `drawing_type '{type}' is registered but not implemented; see workflows/drawing-extract/EXTENDING.md`. **Do NOT create work-dir, do NOT rasterize, do NOT generate crops.**
3. Validate `EXTRACTION_TARGET` is valid for `DRAWING_TYPE` (see registry). REJECT with `extraction_target '{target}' not valid for drawing_type '{type}'; valid targets: {list}` on mismatch.
4. For `EXTRACTION_TARGET=top_equipment_header_detailed`:
   - Validate `REQUESTED_KNOWN_FIELDS` entries against v2 catalog.
   - Validate `EXTRA_FIELDS` per name-collision rules (see workflow contract). REJECT on collision with base columns, catalog fields, or duplicate names.
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
11. For run-folder targets (`DRAWING_SET`, `P_AND_ID`), create or resolve working run folder `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/RUN-{timestamp-or-label}/`.
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
Only the crops for page N are overwritten. Operator then deletes the stub for page N from the target subdirectory and re-dispatches drawing-extract with the same run parameters — only page N re-extracts (other stubs are reused via resume). Log per-page override decisions in a `page_crop_overrides.md` note alongside the work-dir.

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

WORKING_ITEMS dispatches TASK with the `Workflow` from the target registry and explicitly supplies the selected package's `WORKFLOW.md` and `CONTRACT.md`. Record actual supplied context when available; instruction-mediated loading remains instruction-asserted.

Each dispatch brief MUST follow the bounded brief contract in `docs/AGENT_WORKFLOW_RUNTIME.md`, with:
- `Workflow` from the target dispatch table
- `RuntimeOverrides` per the selected worker package’s `CONTRACT.md#brief` § Required fields
- `AllowedWriteTargets: [OUTPUT_PATH]`
- `ExpectedOutputs: [OUTPUT_PATH]`

The orchestrator SHOULD include `CustomInstructions` containing the format reminders and completion checklist from the selected worker package’s `CONTRACT.md#brief` § CustomInstructions as a defense-in-depth measure.

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
The tool emits a valid INIT-TASK brief with `Workflow`, `RuntimeOverrides`, recommended `CustomInstructions` (format reminders + checklist), a dispatch appendix with canonical templates generated from `render_stub()`, and `ExpectedOutputs`.

Only if a non-TASK dispatch surface is used (e.g., a generic agent without TASK shell) should the orchestrator inline the full contract-critical content from the selected worker package’s `CONTRACT.md#brief` § CustomInstructions and the canonical templates from `WORKFLOW.md` § Canonical output template directly in the dispatch prompt. This is a fallback, not the standard path.

5. Divide queued pages into batches of `BATCH_SIZE`.
6. For each batch:
   - spawn TASK dispatches in parallel using the INIT-TASK brief shape
   - pass runtime overrides per the selected worker package’s `CONTRACT.md#brief` § Required fields
   - include recommended CustomInstructions per the selected worker package’s `CONTRACT.md#brief` § CustomInstructions
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
