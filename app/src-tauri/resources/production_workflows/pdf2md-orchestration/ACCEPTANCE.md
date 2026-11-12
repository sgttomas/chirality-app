# pdf2md-orchestration acceptance

A pdf2md-orchestration conversion run is valid when:

### S1 — Output exists and is non-empty
`OUTPUT_PATH` is a file containing Markdown with content from at least one page.

### S2 — Manifest is preserved
`{WORK_DIR}/manifest.json` exists and records all parameters (pdf_path, dpi, pages_rendered).

### S3 — Partial conversion is reported
If any pages failed, the failure count and page numbers are reported to the human. The pipeline does not silently drop pages.

### S4 — Tools are invoked correctly
Rasterization, post-processing, and assembly are performed by deterministic tools, not by LLM reasoning.

### S5 — VLM work is delegated via compliant TASK dispatch
Per-page conversion (Markdown AND asset JSON) is performed by `pdf2md-page-full` workflow dispatches using the INIT-TASK brief shape. pdf2md-orchestration does not read page images, produce page Markdown, or emit asset bboxes itself. One TASK dispatch per page; no separate asset-discovery dispatch.

### S6 — Resumability holds with content-hash validation
Re-running the pipeline with matching `pdf_sha256` and `dpi` skips completed work. Mismatched work-dirs are rejected at Phase 0. File existence alone does not satisfy resume. Replacing a PDF at the same path produces a different SHA256 and is detected as a mismatch. Legacy manifests (pre-`pdf_sha256`) fall back to `pdf_path` + `dpi` comparison with a warning.

### S7 — Degraded output is gated
If the assembled output contains placeholder pages, the Phase 4 report identifies them and recommends rerun. Downstream pipeline transition requires human acknowledgment.

### S8 — Asset materialization is validated when enabled
When `ASSET_MODE=prose`, `{ASSETS_ROOT}/{PDF_STEM}_assets_manifest.json` exists, every asset link in `OUTPUT_PATH` resolves to a real file under `{ASSETS_ROOT}`, and every manifest-declared asset path is referenced by the assembled Markdown.

### S9 — Asset discovery stays page-bounded
When `ASSET_MODE=prose`, each `pdf2md-page-full` dispatch reads only its page PNG and writes only `{WORK_DIR}/page_{NNNN}.md` and `{WORK_DIR}/page_{NNNN}_assets.json`. Cropping, XLSX rendering, Markdown anchoring, and manifest aggregation are performed by deterministic tools, not by the TASK worker.
