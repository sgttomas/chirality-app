# Tool Registry

Deterministic tools for the Chirality agent operating system. These tools codify repeatable, LLM-independent operations that agents invoke during pipeline execution.

**Maintained by:** TOOLMAKER (Type 1, `agents/AGENT_TOOLMAKER.md`), operating under the Type 0 standard `AGENT_HELPS_HUMANS.md`. TOOLMAKER owns deterministic tool contracts; its outcomes conform to HELPS_HUMANS R11 + R12 and the "Design Outcomes for Tool Contracts" section. SKILLMAKER (Type 1) owns the skill subsystem (no overlap with the tool layer).

---

## Scaffolding

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `scaffold_package.sh` | zsh | Create package folder with 9 lifecycle subfolders | EXECUTION_ROOT, PKG_ID, PkgLabel | Idempotent folder tree |
| `scaffold_deliverable.sh` | zsh | Create deliverable folder with 5 minimum viable stub files | WORKING_DIR, DEL_ID, DelLabel | Stub files: _STATUS, _CONTEXT, _DEPENDENCIES, _REFERENCES, _SEMANTIC |
| `scaffold_tool_root.sh` | zsh | Create tool root with _Archive/ and _LATEST.md stub | EXECUTION_ROOT, ROOT_NAME | Tool root folder |
| `create_snapshot_folder.sh` | zsh | Create timestamped immutable snapshot folder | TOOL_ROOT, PREFIX, LABEL | Folder path (stdout) |
| `update_latest_pointer.sh` | zsh | Overwrite _LATEST.md to point to a snapshot | TOOL_ROOT, SNAPSHOT_NAME | Updated _LATEST.md |
| `write_status.sh` | zsh | Write or update _STATUS.md with lifecycle transition | DEL_PATH, STATE, ACTOR | Updated _STATUS.md with history |

## Query

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `count_workspace_state.sh` | zsh | Count packages, deliverables, lifecycle states, tool roots | EXECUTION_ROOT | Summary table |
| `scan_next_amendment_id.sh` | zsh | Scan _ScopeChange/ for next available SCA-{NNN} ID | SCOPE_CHANGE_ROOT | Next ID string (stdout) |

## Validation

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `validate_enum.py` | Python 3 | Validate a value against 24 named enum sets | enum_name, value | VALID/INVALID (exit code) |
| `validate_id_format.sh` | zsh | Validate ID against format pattern (PKG, DEL, DEP, SOW, OBJ, CAT, KTY, SUB) | ID_TYPE, ID_VALUE | VALID/INVALID (exit code) |
| `validate_dependencies_schema.py` | Python 3 | Validate Dependencies.csv against v3.1 schema (29 columns) | csv_path | VALID/INVALID + column counts |
| `check_min_viable_fileset.sh` | zsh | Verify 5 required metadata files in a deliverable folder | DELIVERABLE_PATH | PASS/FAIL (exit code) + missing list |
| `check_four_documents.sh` | zsh | Verify 4 document kit files in a deliverable folder | DELIVERABLE_PATH | PASS/FAIL (exit code) + missing list |
| `scan_deliverable_consistency.py` | Python 3 | Scan one deliverable for missing files, unresolved markers, simple identity mismatches, and candidate unsourced numeric lines | deliverable_path, [--output-json], [--focus-doc], [--strictness], [--max-findings], [--check-identity], [--check-unsourced-numerics] | JSON report to stdout or file |
| `validate_skill_metadata.py` | Python 3 | Validate repo-native skill folders for required `SKILL.md` frontmatter, required companion files (`BRIEF_SCHEMA.md`, `TOOL_POLICY.md`, `QA_CHECKS.md`), folder/name alignment, single-line descriptions, machine-consumed metadata fields, and canonical `allowed-tools` syntax/path resolution | [skills_root], [--json] | PASS/FAIL summary or JSON report |
| `validate_build_hypergraph_fixture.py` | Python 3 | Regression check for `tools/aggregation/build_hypergraph.py` using bundled fixtures at `tools/aggregation/testdata/`. Verifies determinism, clean-run PASS coverage, warning detection, ledger/objectives path coverage, semicolon-list normalization equivalence, and `UNIT_MULTIPLE_CATEGORIES` blocker detection | [--keep-tmp] | PASS/FAIL summary (exit 0/1) |

## Reporting

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `merge_detail_csvs.py` | Python 3 | Merge multiple Detail.csv files with SourcePath provenance | output_path, csv_paths or --glob | Project_Detail.csv |
| `generate_index_md.sh` | zsh | List folder contents into an INDEX.md manifest | FOLDER_PATH | INDEX.md |
| `summarize_by_wbs.py` | Python 3 | Group and sum Amount by WBS (Package/Deliverable) | input_csv, output_csv | Project_Summary_WBS.csv |
| `summarize_by_cbs.py` | Python 3 | Group and sum Amount by CBS category | input_csv, output_csv | Project_Summary_CBS.csv |
| `generate_wbs_cbs_matrix.py` | Python 3 | Pivot detail data into WBS x CBS cost matrix | input_csv, output_csv | Project_WBS_CBS_Matrix.csv |
| `generate_coverage_csv.py` | Python 3 | Cross-reference deliverables vs found artifacts (deps, estimates, doc kit) | EXECUTION_ROOT, output_csv | Coverage.csv with per-deliverable presence flags |
| `clean_pdf2md_output.py` | Python 3 | Remove repeating page headers, separators, and boilerplate from PDF-to-markdown conversion output | file.md [file2.md ...] | Cleaned files in-place + line removal counts |
| `merge_equipment_costing_csv.py` | Python 3 | Merge per-KTY Equipment_Costing_Extract CSV files into a single consolidated CSV | OUTPUT_CSV, INPUT_DIR, [--sort-by COLUMN] | Consolidated Equipment_Costing_Extract.csv |

## PDF-to-Markdown

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `rasterize_pdf.py` | Python 3 | Render PDF pages to numbered PNG files via pymupdf (idempotent — skips existing PNGs) | pdf_path, output_dir, [--dpi 300], [--pages 1-5,7] | `page_{NNNN}.png` files + `manifest.json` |
| `postprocess_page.py` | Python 3 | Apply 10-rule deterministic cleanup to VLM-generated markdown (strip fences, fix tables, remove hallucinations, normalise whitespace) | input.md, [output.md] | Cleaned markdown file |
| `assemble_markdown.py` | Python 3 | Join per-page markdown files into a single assembled document with page separators | pages_dir, output_file, [--separator "---"] | Assembled `.md` file |

## Drawing Extraction

Drawing-type-aware tool chain. v2 tools read/write per-page stubs at target-aware paths `{source_dir}/{drawing_type}/{extraction_target}/{pdf_stem}_page_{NNNN}_stub.md` with self-describing YAML frontmatter. Combined outputs land in the same per-target subdirectory. See `plans/DRAWING_EXTRACT_ARCHITECTURE_DESIGN.md` for the frozen v2 contract.

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `normalize_equipment_stub_layout.py` | Python 3 | Canonical parser/renderer for per-page drawing-extract equipment stubs (v2 + legacy). Library API: `parse_stub`, `parse_stub_text`, `render_stub`, `resolve_stub_path`, `build_column_order`, `validate_extra_fields_collisions`. CLI: in-place legacy normalization OR legacy→v2 migration to target-aware path | source_dir, --pdf-stem, --start-page, --end-page, [--drawing-type, --extraction-target] | Normalized/migrated stub `.md` files + summary counts |
| `prepare_header_crops.py` | Python 3 | Create deterministic top-header and titleblock crops from rasterized drawing pages. Drawing-type crop-spec registry (PFD implemented; P_AND_ID/ISOMETRIC/GA stubbed fail-fast). CLI overrides win over registry defaults for per-page geometry | work_dir, --drawing-type, --pages, [--header-height-ratio], [--titleblock-width-ratio], [--header-slices] | Header/titleblock PNGs per page |
| `assemble_equipment_csv.py` | Python 3 | Assemble per-page v2 stubs into combined CSV. Target-driven columns (basic=4 base; detailed=base+catalog+extras per canonical order) + source_page | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --start-page, --end-page, --output-csv | Combined equipment CSV |
| `assemble_equipment_markdown.py` | Python 3 | Assemble per-page v2 stubs into combined Markdown table with target-aware columns + no-findings page list + missing-page list | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --start-page, --end-page, --output-md, [--source-pdf-name] | Combined equipment Markdown |
| `build_page_worker_brief.py` | Python 3 | Render a valid INIT-TASK brief for a single drawing-extract-page dispatch. Emits TaskSkill, RuntimeOverrides, CustomInstructions (format reminders), a dispatch appendix with canonical templates from `render_stub()`, and ExpectedOutputs. Single source of truth for dispatch prompts | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --work-dir, --page, --total-pages, --source-pdf-name, [--requested-known-fields], [--extra-fields-json], [--required-fields] | INIT-TASK brief on stdout |
| `validate_stub_format.py` | Python 3 | Post-dispatch format validator for v2 stubs. Fails on: missing pages, legacy stubs at target-aware paths, SUCCESS stubs missing `finding_count`, or SUCCESS stubs where parsed meaningful row count ≠ `finding_count` (catches both total and partial row loss). Read-only | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --start-page, --end-page, [--pages] | PASS/FAIL summary (exit 0/1/2) |
| `validate_detailed_schema.py` | Python 3 | Validate that v2 stubs in a page range share identical schema metadata (drawing_type, extraction_target, requested_known_fields, requested_extra_fields, required_fields). Fail-fast on divergence | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --start-page, --end-page | PASS/FAIL summary (exit 0/1) |
| `validate_resume_stub_metadata.py` | Python 3 | Resume-safety validator: verify every existing v2 per-page stub in a target-aware subtree matches the current-run schema tuple (drawing_type, extraction_target, source_pdf, source_page, and for detailed target also requested_known_fields + requested_extra_fields + required_fields). Missing stubs are skipped (queued for extraction). Read-only | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --source-pdf, --start-page, --end-page, [--requested-known-fields], [--extra-fields-json], [--required-fields] | `stubs_checked`/`resume_safety` key=value on stdout, per-stub mismatch diffs + remediation on stderr (exit 0/1/2) |
| `sanitize_equipment_stubs.py` | Python 3 | Target-aware post-extraction QC on v2 stubs. Filters: instrument-tag deny-list (ISA prefixes), note-like name patterns, blank tags. Name trimming at class-word boundaries. Row-count guard: refuses to overwrite SUCCESS stubs when `finding_count` is missing or parsed row count mismatches. Writes run-scoped JSONL rollback bundle for all overwritten stubs. Emits per-page audit CSV | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --start-page, --end-page, [--report-csv] | Sanitized v2 stub `.md` files in-place + QC report CSV + audit CSV + rollback JSONL |
| `report_stub_counts.py` | Python 3 | Target-aware per-page coverage report from v2 stubs. Basic: status CSV + `round_trip_row_loss`. Detailed: per-field populated/total counts + required-field warnings + identical-value heuristic (possible copy-across hallucination flag) + `round_trip_row_loss` QA signal | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --start-page, --end-page, --output-csv | Coverage report CSV |
| `backfill_stub_system_names.py` | Python 3 | Update `system_name` frontmatter + every row's system_name cell in v2 stubs via parse/render round-trip | --source-dir, --drawing-type, --extraction-target, --pdf-stem, --start-page, --end-page, --system-names-csv | Updated v2 stub `.md` files in-place + summary counts |
| `flag_duplicate_equipment_csv.py` | Python 3 | Flag repeated equipment numbers in a combined equipment CSV without collapsing rows. Target-agnostic; passes detail columns through | input_csv, output_csv, [--key equipment_number] | Duplicate-flags CSV with conflict classification |
| `dedupe_equipment_csv.py` | Python 3 | Deduplicate a combined equipment CSV by key while preserving first occurrence order. Target-agnostic; passes detail columns through | input_csv, output_csv, [--key equipment_number] | Deduped equipment CSV (optional/manual use) |
| `merge_equipment_detailed.py` | Python 3 | PFD-equipment-repertoire-scoped deterministic side-by-side merge of two combined CSVs on equipment_number key. No auto-resolution; produces merge_result + unmatched_extracted + unmatched_existing CSVs | --extracted, --existing, --output-dir, --pdf-stem, --start-page, --end-page, [--merge-key equipment_number] | 3 CSVs: merge_result, unmatched_extracted, unmatched_existing |
| `flag_merge_conflicts.py` | Python 3 | Post-merge conflict reporter. Emits per-equipment-number conflict summary from side-by-side merge result | --merge-result, --output-csv | Conflicts CSV (equipment_number, conflict_count, conflicting_columns, conflict_detail) |
| `extract_pdf_titleblock_text.py` | Python 3 | Extract drawing-number candidates and title-block text snippets from PDF pages using external `pdftotext` | pdf_path, output_csv, --pages 7-61 | CSV with page, `dwg_no`, status, titleblock text excerpt |
| `reconcile_west_doe_comp_and_liquids_packages.py` | Python 3 | Add `package_name` column to a PFD equipment CSV using manual package inference rules (project fallback — West Doe Comp & Liquids) | source_csv | Updated CSV in-place with `package_name` column + appended master rows |
| `recover_deepcut_multiblock_headers.py` | Python 3 | Deterministically backfill known undercounted multi-block header pages from verified fixtures (project fallback — West Doe Deepcut). Currently operates on legacy-format stubs | source_dir, [--pdf-stem], [--report-csv] | Updated stub `.md` files in-place + optional recovery report CSV |
| `report_west_doe_comp_and_liquids_package_matches.py` | Python 3 | Generate package-match provenance reports from final and master equipment CSVs (project fallback — West Doe Comp & Liquids) | final_csv, master_csv, output_dir | Package match report CSV + master row disposition CSV |
| `vision_ocr.swift` | Swift | Run macOS Vision framework OCR on an image and output recognized text lines with bounding boxes | image_path | JSON to stdout with lines, confidence, bounding boxes |

## Domain Extraction

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `assemble_equipment_master_csv.py` | Python 3 | Assemble per-KTY Equipment Extract markdown files into a single consolidated master list CSV | source_dir, output_csv | CSV with Source_KTY, Source_KA, Equipment_Tag, Equipment_Name, Package_Name, Notes |

## Coordination

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `analyze_dep_closure.py` | Python 3 | Full dependency graph analysis: schema, orphans, cycles (SCC), hubs, bidirectional pairs, coverage | EXECUTION_ROOT, --output-dir | closure_summary.json + 6 CSV reports |

---

## Aggregation

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `build_hypergraph.py` | Python 3 | Build DOMAIN hypergraph from staging CSVs: deterministic SHA1-based HyperedgeID generation, 9 QA checks, optional delta vs prior snapshot. Reads 8 Evidence CSVs (2 required, 6 conditional); writes nodes/hyperedges/incidence tables + hypergraph.json + QA_Report.md | `--staging-dir`, `--output-dir`, `--run-label`, `--execution-root`, `--scope`, [`--normalize-ids`], [`--edgeset`], [`--variant`], [`--prior-snapshot`] | `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`, `QA_Report.md` |

**Determinism:** same staging inputs → byte-identical CSVs + canonical JSON (excluding `generated_at` timestamp).

---

## Evaluation

Canonical versions at `tools/evaluation/`. Project-specific variants may also exist at `{EXECUTION_ROOT}/_Evaluation/tools/`.

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `verify_digest_coverage.sh` | zsh | Verify 1:1 deliverable-to-digest mapping | EXECUTION_ROOT | PASS/FAIL (exit code) |
| `count_deliverable_files.sh` | zsh | Count MUST/SHOULD/MAY files across all deliverables | EXECUTION_ROOT | Per-file count table |
| `extract_lifecycle_states.sh` | zsh | Extract and summarize lifecycle state distribution | EXECUTION_ROOT | State distribution |
| `count_deliverables_per_package.sh` | zsh | Count deliverable folders per package | EXECUTION_ROOT | Per-package count |
| `check_dependency_schema.sh` | zsh | Validate Dependencies.csv v3.1 columns across all files | EXECUTION_ROOT | Per-file VALID/INVALID |
| `check_implements_node.sh` | zsh | Verify IMPLEMENTS_NODE anchor in every Dependencies.csv | EXECUTION_ROOT | Missing anchor list |
| `check_evidence_coverage.sh` | zsh | Check EvidenceFile population rate across all dependency rows | EXECUTION_ROOT | Coverage percentage |
| `extract_agent_output.py` | Python 3 | Extract final assistant text from Claude agent JSONL output files | agent_output_file, [output_file] | Extracted text |

---

## Backlog (CREATE LATER)

Tools identified as useful but not yet needed — either used by only one agent, already handled inline by existing tools, or the agent currently manages the operation via LLM reasoning with an adequate fallback.

| Name | Category | Purpose | Why deferred |
|------|----------|---------|--------------|
| `find_dependencies_csvs.sh` | query | Glob all Dependencies.csv under an execution root | Already handled inline by `analyze_dep_closure.py` and individual agent `find` commands |
| `find_estimate_snapshots.sh` | query | Glob all EST_* snapshot folders | AGGREGATION already uses `merge_detail_csvs.py --glob` which embeds the lookup |
| `find_detail_csvs.sh` | query | Find Detail.csv within estimate snapshots | Same — embedded in `merge_detail_csvs.py --glob` pattern |
| `extract_decomp_ids.py` | query | Parse decomposition markdown to extract PKG/DEL IDs, names, fields | ORCHESTRATOR and PREPARATION currently parse via LLM reading; useful for deterministic coverage checks once decomposition format stabilizes further |
| `build_blocker_dag.py` | coordination | Topological sort of hard execution dependencies into tier assignments | SCHEDULING computes tiers inline; `analyze_dep_closure.py` already produces SCC/cycle analysis. Tier assignment would add standalone topological output |
| `serialize_workspace_state.py` | reporting | Serialize filesystem state to JSON | Superseded by AUDIT_DECOMP's `coverage_summary.json`; no agent protocol invokes a generic filesystem-to-JSON dump |

**Promotion criteria:** A backlog tool should be promoted to CREATE NOW when (1) a second agent needs the same operation, or (2) an existing agent's inline implementation diverges across runs and needs standardization.

---

EOF
