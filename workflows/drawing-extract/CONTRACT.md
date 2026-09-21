# drawing-extract contract

## Drawing-type + extraction-target registry

WORKING_ITEMS resolves the bounded workflow and deterministic tool chain from this table. These five combinations are implemented. `ISOMETRIC` and `GA` remain registered stubs; they reject before creating a work directory, rasterizing, or generating crops. Any unlisted type/target pair rejects. For authorized extension work, load [EXTENDING.md](EXTENDING.md).

| Target tuple | Crop/prep tool | TASK workflow | Brief builder | Validators | Assembly/QC |
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
| `BATCH_SIZE` | MAY | 5 | Number of TASK workflow dispatches to run in parallel |
| `DRAWING_TYPE` | MUST | — | Drawing-type selector; see registry above |
| `EXTRACTION_TARGET` | MUST | — | Target within the drawing type; see registry above |

### P&ID and drawing-set parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `TILE_GRID` | MAY | `5x4` | P&ID valve tile grid. `5x4` is the minimum production baseline unless a human explicitly accepts a lower-resolution run. |
| `OVERLAP_PX` | MAY | `200` | Read-box expansion around each emit box. |
| `BODY_EXCLUSIONS` | MAY | `border,titleblock` | Conservative body-box exclusions for P&ID tiling. Notes-column exclusion is opt-in because notes/insets may contain valve symbols. |
| `MINI_GRID` | MAY | `5x5` | Coarse location overlay inside each emit box. Optional visual aid. Current symbol-instance outputs require page-global pixel centers and bounding boxes; grid labels do not substitute for geometry. |
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

Known-field catalog (v2): `equipment_type`, `equipment_description`, `capacity_text`, `power_text`. See `workflows/drawing-extract-page/CONTRACT.md` § Known-field catalog for semantic definitions.

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

## Workflow requirements

- **Human-frozen extraction contract.** Before repetitive sheet work, the human confirms drawing type, extraction target, output schema, required review, duplicate/recovery posture, and acceptance thresholds.
- **Novel-target path.** A target absent from the implemented registry is fail-closed by default. The human may instead authorize an experimental run after defining its schema and review contract; that run uses an ephemeral generalist Agent 2 with disjoint sheet scopes and run-local outputs, subject to runtime policy. It does not silently become a registry entry.
- **Promotion rule.** A repeated target with stable schema, QA, and recovery semantics is proposed to HELPS_HUMANS for graduation into a TASK workflow and deterministic hook set.

- Rasterization is deterministic and resumable.
- Page/tile image interpretation is delegated to the target-specific TASK workflow, not performed directly by WORKING_ITEMS.
- `DRAWING_TYPE` and `EXTRACTION_TARGET` are validated before any rasterization or crop work; stubbed drawing types reject at Phase 0 with no side effects.
- Per-page artifacts are written to target-aware subdirectories: `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/`.
- Run-scoped P&ID and drawing-set artifacts are assembled in working run folders and frozen at closure: `{SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/RUN-{timestamp-or-label}/`. `_LATEST.md` is a convenience pointer, not an authority marker.
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

## Artifacts and tool interfaces

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

### Workflow dispatched

| Workflow | Path | Purpose |
|---|---|---|
| `drawing-extract-page` | `workflows/drawing-extract-page/` | PFD equipment page extraction |
| `drawing-titleblock-page` | `workflows/drawing-titleblock-page/` | Single-page titleblock inventory extraction |
| `pandid-valve-symbol-instance` | `workflows/pandid-valve-symbol-instance/` | P&ID pixel-anchored valve symbol-instance extraction |
