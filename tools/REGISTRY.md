# Tool Registry

Deterministic tools for the Chirality agent operating system. These tools codify repeatable, LLM-independent operations that agents invoke during pipeline execution.

**Maintained by:** AGENT_TOOLMAKER (Type 1)

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

## PDF-to-Markdown

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `rasterize_pdf.py` | Python 3 | Render PDF pages to numbered PNG files via pymupdf (idempotent — skips existing PNGs) | pdf_path, output_dir, [--dpi 300], [--pages 1-5,7] | `page_{NNNN}.png` files + `manifest.json` |
| `postprocess_page.py` | Python 3 | Apply 10-rule deterministic cleanup to VLM-generated markdown (strip fences, fix tables, remove hallucinations, normalise whitespace) | input.md, [output.md] | Cleaned markdown file |
| `assemble_markdown.py` | Python 3 | Join per-page markdown files into a single assembled document with page separators | pages_dir, output_file, [--separator "---"] | Assembled `.md` file |

## Drawing Extraction

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `assemble_equipment_markdown.py` | Python 3 | Assemble per-page drawing extraction outputs into a combined Markdown table | source_dir, output_md, --pdf-stem, --start-page, --end-page, [--source-pdf-name] | Combined equipment Markdown + no-findings page list |
| `assemble_equipment_csv.py` | Python 3 | Assemble per-page drawing extraction outputs into a combined CSV with provenance | source_dir, output_csv, --pdf-stem, --start-page, --end-page | Combined equipment CSV with `source_page` |
| `flag_duplicate_equipment_csv.py` | Python 3 | Flag repeated equipment numbers in a combined equipment CSV without collapsing rows | input_csv, output_csv, [--key equipment_number] | Duplicate-flags CSV with conflict classification |
| `dedupe_equipment_csv.py` | Python 3 | Deduplicate a combined equipment CSV by key while preserving first occurrence order | input_csv, output_csv, [--key equipment_number] | Deduped equipment CSV (optional/manual use) |
| `extract_pdf_titleblock_text.py` | Python 3 | Extract drawing-number candidates and title-block text snippets from PDF pages using external `pdftotext` | pdf_path, output_csv, --pages 7-61 | CSV with page, `dwg_no`, status, titleblock text excerpt |

## Coordination

| Name | Language | Purpose | Inputs | Outputs |
|------|----------|---------|--------|---------|
| `analyze_dep_closure.py` | Python 3 | Full dependency graph analysis: schema, orphans, cycles (SCC), hubs, bidirectional pairs, coverage | EXECUTION_ROOT, --output-dir | closure_summary.json + 6 CSV reports |

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
