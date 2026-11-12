# pdf2md-orchestration contract

## Runtime Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `PDF_PATH` | MUST | — | Absolute path to the input PDF |
| `OUTPUT_PATH` | MUST | — | Absolute path for the final assembled `.md` output |
| `WORK_DIR` | SHOULD | `{pdf_stem}_pdf2md_work/` adjacent to PDF | Directory for PNGs and intermediate `.md` files |
| `BATCH_SIZE` | MAY | 5 | Number of `pdf2md-page-full` dispatches to run in parallel per batch |
| `DPI` | MAY | 300 | Rasterization DPI (72–400) |
| `PAGES` | MAY | all | Page range: `all`, `5`, `3-15`, or `1,3,5,7` |
| `SEPARATOR` | MAY | `---` | Page separator in assembled output |
| `ASSET_MODE` | MAY | `none` | `none` for text-only; `prose` to identify and materialize figures, tables, and meaningful images |
| `ASSETS_ROOT` | MAY | parent of `OUTPUT_PATH` | Public folder for `figures/`, `tables/`, `images/`, and `{doc_stem}_assets_manifest.json` when `ASSET_MODE=prose` |

---

## Workflow requirements

- **Human-frozen source contract.** Before repetitive page work, confirm the source-specific output target, transcription and asset schema, review depth, degraded-output policy, and recovery posture with the human.
- **Novel-target path.** If the accepted target is not represented by an existing workflow/schema, do not force it through `pdf2md-page-full`. Freeze a purpose-specific schema and bounded brief, then use an ephemeral generalist Agent 2 only when the runtime policy permits it. Keep the result run-local and explicitly experimental.
- **Promotion rule.** When a novel target recurs and its schema and acceptance checks stabilize, route a workflow proposal to HELPS_HUMANS.

- **Tools are deterministic; violation is a design defect.** Rasterization (`rasterize_pdf.py`), post-processing (`postprocess_page.py`, `clean_pdf2md_output.py`), and assembly (`assemble_markdown.py`) are Python scripts with no LLM API calls. If a pipeline stage requires LLM reasoning, it belongs in a workflow dispatch, not in a tool invocation.
- **VLM work is delegated via TASK+workflow dispatch.** Per-page image-to-Markdown conversion AND per-page asset identification are performed together by `pdf2md-page-full` workflow dispatches through the TASK shell, not by WORKING_ITEMS directly. pdf2md-orchestration does not read page images, produce page Markdown, or emit asset bboxes itself.
- **One vision read per page.** The merged workflow reads each page PNG exactly once and emits both Markdown and asset JSON from that single pass. Issuing two separate workflow dispatches per page (the deprecated two-workflow split) is a regression and should not be done.
- **Asset materialization is deterministic tool work.** Cropping, XLSX rendering, stable filename assignment, Markdown anchoring, manifest aggregation, and final reference validation are performed by deterministic tools. pdf2md-orchestration does not estimate bounding boxes or transcribe tables itself.
- **Resume-safety requires manifest-parameter match, not just file existence.** WORK_DIR belongs to one `(pdf_sha256, dpi)` tuple. Existing PNGs and page `.md` files are reusable only when the current run's PDF content hash (SHA256 of the bytes at `PDF_PATH`) and `DPI` match the manifest that produced them. Mismatches are rejected at Phase 0. See Phase 0 step 5 for the mismatch policy. The `pdf_sha256` field in `manifest.json` (added by `rasterize_pdf.py`) closes the same-path-different-content gap: replacing a PDF at the same path produces a different hash and is detected.
- **Asset references must resolve before downstream use.** If `ASSET_MODE=prose`, the final Markdown must be validated against the document asset manifest and asset folders. Missing referenced files, manifest widows, or orphan links make the output degraded and require human acknowledgment before downstream use.
- **Partial success produces a degraded artifact that requires human review.** Failed pages are noted in the report. The pipeline does not abort on individual page failures; the assembler inserts placeholder text (`*[Page N: conversion unavailable]*` or `*[Page N: empty]*`) for missing or empty pages. A placeholder-containing assembly is a degraded artifact. It MUST NOT be passed to downstream consumers (domain-decomp) without explicit human acknowledgment. The Phase 4 report MUST list affected pages and recommend rerun before downstream use.

---

## Artifacts and tool interfaces

### Filesystem layout

```
{WORK_DIR}/
  manifest.json           ← written by rasterize_pdf.py
  page_0001.png           ← rendered page images
  page_0002.png
  ...
  page_0001.md            ← per-page Markdown (written by pdf2md-page-full dispatch in Phase 2, cleaned by Phase 3)
  page_0002.md
  ...
  page_0001_assets.json                  ← per-page asset JSON (always written by pdf2md-page-full in Phase 2; ignored downstream when ASSET_MODE=none)
  page_0001_assets_materialized.json     ← optional materialization manifest (Phase 3.5)
  page_0001.anchored.md                  ← optional asset-anchored page Markdown (Phase 3.5)

{OUTPUT_PATH}             ← final assembled Markdown (written by assemble_markdown.py)

{ASSETS_ROOT}/            ← optional public asset root when ASSET_MODE=prose
  {PDF_STEM}_assets_manifest.json
  figures/                ← .png crops of figure regions
  tables/                 ← .xlsx artifacts rendered from table_data; PNG crops
                            of each table region. Legacy .csv (pre-table_data)
                            files are migrated into .archive/ by
                            tools/pdf2md/migrate_csv_assets_to_archive.py.
  images/                 ← .png crops of non-figure images
```

### Tool dependencies

| Tool | Path | Phase |
|---|---|---|
| Rasterize | `tools/pdf2md/rasterize_pdf.py` | 1 |
| Merged page brief builder (canonical) | `tools/pdf2md/build_page_full_brief.py` | 2 |
| Legacy page brief builder (deprecated) | `tools/pdf2md/build_page_brief.py` | 2 (legacy resume only) |
| Post-process (10-rule cleanup) | `tools/pdf2md/postprocess_page.py` | 3 |
| Header/footer strip | `tools/reporting/clean_pdf2md_output.py` | 3, 4 |
| Legacy asset brief builder (deprecated) | `tools/pdf2md/build_page_assets_brief.py` | 3.5 (legacy resume only) |
| Filter logo entries | `tools/pdf2md/filter_logo_assets.py` | 3.5 |
| Asset materialize | `tools/pdf2md/materialize_page_assets.py` | 3.5 |
| Table XLSX render (delegated by materializer) | `tools/pdf2md/render_table_xlsx.py` | 3.5 |
| Inline asset reference rewriter | `tools/pdf2md/rewrite_inline_asset_refs.py` | 3.5 |
| Asset manifest aggregate | `tools/pdf2md/aggregate_asset_manifest.py` | 3.5 |
| Asset resume validation | `tools/pdf2md/validate_asset_resume.py` | 3.5 |
| Asset validation | `tools/pdf2md/validate_assets.py` | 4 |
| Assemble | `tools/pdf2md/assemble_markdown.py` | 4 |

### Workflow dispatched

| Workflow | Path | Purpose |
|---|---|---|
| `pdf2md-folio-extract` | `workflows/pdf2md-folio-extract/` | Optional active printed-label extraction; null on absent or uncertain folio. |
| `pdf2md-page-full` | `workflows/pdf2md-page-full/` | **Canonical.** Single-page merged vision pass: emits Markdown AND asset JSON from one read. |
| `pdf2md-page` (deprecated) | `workflows/pdf2md-page/` | Legacy: Markdown only. Retained for resume on PDFs processed under the old contract. |
| `pdf2md-page-assets` (deprecated) | `workflows/pdf2md-page-assets/` | Legacy: asset JSON only, requires post-Phase-3 page Markdown. Retained for resume on PDFs processed under the old contract. |
