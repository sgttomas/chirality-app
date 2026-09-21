# pdf2md-orchestration procedure

WORKING_ITEMS coordinates this procedure and assigns bounded visual or semantic stages to TASK. Tool commands resolve against the declared tool root.

### Phase 0 — Pre-flight

1. Validate `PDF_PATH` exists, is readable, and has a `.pdf` extension.
2. Resolve `WORK_DIR`:
   - If not provided, derive from `PDF_PATH`: `{parent}/{stem}_pdf2md_work/`
   - Create the directory if it does not exist.
3. Resolve `OUTPUT_PATH`:
   - Confirm the parent directory exists and is writable.
4. Resolve asset mode:
   - If `ASSET_MODE` is omitted or `none`, run the text-only pipeline.
   - If `ASSET_MODE=prose`, resolve `ASSETS_ROOT` (default: parent of `OUTPUT_PATH`) and ensure it is writable. The pipeline may create `figures/`, `tables/`, and `images/` below that root.
   - Any other `ASSET_MODE` value rejects at pre-flight.
5. Check for resume state and enforce manifest-parameter match:
   - If `{WORK_DIR}/manifest.json` exists, read it.
   - Compute the SHA256 of the bytes at `PDF_PATH`.
   - Compare against the manifest's `pdf_sha256` and `dpi` (and, informationally, `pdf_path`).
   - **Mismatch policy:** If `pdf_sha256` differs, OR `dpi` differs, the work-dir contains stale artifacts. REJECT reuse: report the mismatch (including the differing field) and require the human to either clear the work-dir (`rm -rf {WORK_DIR}`) or specify a new one. Do not silently mix stale and fresh artifacts.
   - **Legacy manifest compatibility:** A manifest without `pdf_sha256` cannot establish byte identity. Preserve its historical state, and use a fresh work directory for a verified conversion unless the brief supplies independent evidence tying the existing artifacts to the current PDF bytes. Matching path and DPI alone never permits reuse.
   - If parameters match (or no manifest exists — fresh run): report how many PNGs and `page_NNNN.md` files already exist.
6. **Gate (human confirmation):**
   > "PDF: `{PDF_PATH}` ({N} total pages). Work directory: `{WORK_DIR}`. Output: `{OUTPUT_PATH}`.
   > DPI: {DPI}. Batch size: {BATCH_SIZE}. Pages: {PAGES}.
   > Asset mode: {ASSET_MODE}. Assets root: {ASSETS_ROOT or 'n/a'}.
   > Resume state: {K} PNGs exist, {M} page .md files exist.
   > Proceed?"

### Phase 1 — Rasterize

1. Run the rasterization tool:
   ```
   python3 tools/pdf2md/rasterize_pdf.py {PDF_PATH} {WORK_DIR} --dpi {DPI} [--pages {PAGES}]
   ```
2. Read `{WORK_DIR}/manifest.json` to get the canonical page list and file mapping.
3. Report: "{N} pages rasterized ({K} reused from prior run)."

### Phase 1.5 — Folio extraction (optional, idempotent)

When the downstream consumer wants the **printed folio label** (the page number as it appears on the page itself — `47`, `xiv`, `B-3`, sometimes nothing) displayed in audit surfaces and Source HTML page-badges, run folio extraction. The output is additive metadata on the asset manifest; the immutable physical page index continues to anchor asset IDs.

1. For each page in `{WORK_DIR}/manifest.json`, dispatch one `TASK + pdf2md-folio-extract` with vision capability. Use `tools/pdf2md/build_folio_extract_brief.py --work-dir {WORK_DIR} --page <N>` to render the brief. Outputs land at `{WORK_DIR}/page_folios/page_NNNN.json`.
2. Aggregate via `python3 tools/pdf2md/run_folio_extraction.py --work-dir {WORK_DIR}` → writes `{WORK_DIR}/page_folios.json` keyed by physical page number.
3. The next `aggregate_asset_manifest.py` run (Phase 3.5) picks up `page_folios.json` automatically and emits `page_label` / `page_label_source` on every page record in the v3 manifest.

Failures on individual pages emit `page_label: null, page_label_source: "vlm_failed"` and do NOT abort the pipeline. The workflow is told to emit `null` over guessing — blank pages, cover pages, and unnumbered chapter openers are expected to produce `null` legitimately.

The workflow MUST NOT invent a folio from the sequence. Downstream consumers (domain-decomp) display the folio when present, fall back to the physical page index when absent or null. Human review of VLM-extracted folios happens at domain-decomp Gate 1.5-Fo (conditionally required when this phase has run).

### Phase 2 — Batch dispatch (merged VLM: Markdown + asset JSON)

The merged workflow produces BOTH `page_{NNNN}.md` and `page_{NNNN}_assets.json` per page from a single multimodal read of the page image. There is no separate asset-discovery phase; the JSON is part of Phase 2's output.

1. From `manifest.json`, build the ordered list of pages to convert.
2. For each page, check resume state:
   - If `{WORK_DIR}/page_{NNNN}.md` AND `{WORK_DIR}/page_{NNNN}_assets.json` both already exist and are non-empty AND Phase 0 confirmed source-identity match AND the pair passes the selected worker's output/schema checks: skip (resume). Invalid JSON, failed run_status, missing output correspondence, or placeholder-only Markdown requeues the page.
   - If only one of the two outputs exists: this indicates a partial prior run. Re-queue the page; the worker regenerates both outputs within the same bounded assignment.
   - If neither exists: add to the conversion queue.
3. Report: "{Q} pages need conversion ({S} already complete)."
4. Divide the conversion queue into batches of `BATCH_SIZE`.
5. For each page in a batch, render its INIT-TASK brief:
   ```sh
   python3 tools/pdf2md/build_page_full_brief.py \
       --work-dir {WORK_DIR} --doc-stem {PDF_STEM} \
       --page {PAGE_NUM} --total-pages {TOTAL_PAGES}
   ```
6. Spawn TASK+`Workflow: pdf2md-page-full` dispatches in parallel using the rendered briefs (see dispatch contract below).
7. Wait for all dispatches in the batch to complete. Collect `RUN_STATUS` from each. Record successes (`SUCCESS` or `NO_ASSETS`) and failures (`FAILED` / `FAILED_INPUTS`).
8. Report batch progress: "Batch {B}/{T}: {successes} succeeded, {failures} failed."
9. After all batches complete, report:
   > "Page conversion complete: {success}/{total} pages. Failed: {list or 'none'}. Pages with assets: {count}."

#### Dispatch contract

Page-worker dispatches use TASK with `Workflow: pdf2md-page-full`. Declare `WORKFLOW.md` and the selected package's `CONTRACT.md` as context. Record actual supplied files and fingerprints when the harness exposes them; otherwise identify loading as instruction-asserted.

Each dispatch brief is rendered by `tools/pdf2md/build_page_full_brief.py` and follows the bounded brief contract in `docs/AGENT_WORKFLOW_RUNTIME.md`. The tool emits this envelope:

```md
PURPOSE: Convert one PDF page image to BOTH raw Markdown AND asset JSON from a single multimodal vision read
RequestedBy: WORKING_ITEMS
ParentWorkflow: pdf2md-orchestration
ActingSurface: TASK+pdf2md-page-full

ScopePath: {WORK_DIR}
Workflow: pdf2md-page-full

Tasks:
  - Read the page image ONCE via multimodal vision
  - Transcribe its contents to Markdown per the 8 conversion rules in workflows/pdf2md-page-full/WORKFLOW.md (including [FIGURE:]/[TABLE:]/[... logo] placeholders in reading order)
  - Identify visible figures, tables, and meaningful images; emit the strict-schema asset JSON (pdf2md-page-assets/v1) with bbox_norm, table_data for legible tables, and one-to-one correspondence with the Markdown placeholders

ApplyEdits: true

AllowedWriteTargets:
  - "{WORK_DIR}/page_{NNNN}.md"
  - "{WORK_DIR}/page_{NNNN}_assets.json"

RuntimeOverrides:
  IMAGE_PATH: {WORK_DIR}/page_{NNNN}.png
  OUTPUT_MD_PATH: {WORK_DIR}/page_{NNNN}.md
  OUTPUT_JSON_PATH: {WORK_DIR}/page_{NNNN}_assets.json
  DOC_STEM: {PDF_STEM}
  PAGE_NUM: {N}
  TOTAL_PAGES: {total from manifest}
  ASSET_POLICY: prose-document-assets-v1

ExpectedOutputs:
  - {WORK_DIR}/page_{NNNN}.md
  - {WORK_DIR}/page_{NNNN}_assets.json
```

The worker execution configuration denies shell commands; its brief permits only the page-image read and the two output writes needed for this stage.

#### Legacy two-workflow split (deprecated)

The predecessor split — `pdf2md-page` for Markdown plus a separate `pdf2md-page-assets` pass after Phase 3 — is retained on disk for resuming PDFs that were processed under the old contract (the JSON schema is identical, so materialization composes cleanly with either path). All new dispatches MUST use `pdf2md-page-full`. Do not author new briefs against `pdf2md-page` or `pdf2md-page-assets`.

### Phase 3 — Post-process

1. For each page `.md` file in `{WORK_DIR}/`:
   a. Run the 10-rule deterministic cleanup:
      ```
      python3 tools/pdf2md/postprocess_page.py {WORK_DIR}/page_{NNNN}.md
      ```
   b. Run header/footer stripping (existing tool):
      ```
      python3 tools/reporting/clean_pdf2md_output.py {WORK_DIR}/page_{NNNN}.md
      ```
2. Report: "Post-processed {N} pages."

### Phase 3.5 — Prose asset anchoring and materialization (optional)

Run this phase only when `ASSET_MODE=prose`. The per-page asset JSON was already produced by Phase 2's merged dispatch; this phase is now purely deterministic (no VLM dispatches).

1. Create public asset folders if needed:
   - `{ASSETS_ROOT}/figures/`
   - `{ASSETS_ROOT}/tables/`
   - `{ASSETS_ROOT}/images/`
2. From `manifest.json`, build the ordered list of pages for asset materialization.
3. Validate any existing materialized asset outputs before reuse:
   ```sh
   python3 tools/pdf2md/validate_asset_resume.py {WORK_DIR} [--pages {PAGES}]
   ```
   Exit code `0` means existing materialization manifests are reusable where present and missing manifests should be queued. Exit code `1` means one or more existing materializations are stale or incomplete; reject reuse and require rerun/cleanup rather than mixing stale assets into the output. Exit code `2` is a setup error.
4. For each page, confirm `{WORK_DIR}/page_{NNNN}_assets.json` (written by Phase 2) exists; reject the page if missing (Phase 2 must have completed). For resume, check `{WORK_DIR}/page_{NNNN}.anchored.md`:
   - Existing anchored Markdown is reusable only when its paired materialization manifest `{WORK_DIR}/page_{NNNN}_assets_materialized.json` passed `validate_asset_resume.py`.
5. Optionally filter logo entries before materialization (campaign policy for sources with repeating header logos):
   ```sh
   python3 tools/pdf2md/filter_logo_assets.py {WORK_DIR}
   ```
   Idempotent. Removes `kind:"img"` entries whose caption matches `/logo/i`.
6. For each page asset JSON, run deterministic materialization. This tool assigns stable IDs, normalizes slugs, crops PNGs, and renders deterministic XLSX artifacts per table via `render_table_xlsx.py` (one .xlsx per `table_data` block; `needs_extraction: true` entries skip XLSX rendering and are honored by downstream validators). The materializer's per-page anchored Markdown is treated as a draft surface — the inline rewriter in step 7 produces the canonical anchored output:
   ```sh
   python3 tools/pdf2md/materialize_page_assets.py --page-image {WORK_DIR}/page_{NNNN}.png --page-md {WORK_DIR}/page_{NNNN}.md --asset-json {WORK_DIR}/page_{NNNN}_assets.json --assets-root {ASSETS_ROOT} --doc-stem {PDF_STEM} --page {N} --output-md {WORK_DIR}/page_{NNNN}.anchored.md --manifest-output {WORK_DIR}/page_{NNNN}_assets_materialized.json
   ```
7. For each materialized page, rewrite inline figure/table/oddball-image placeholders so they point at the materialized asset paths. This replaces the dead inline references emitted by the page worker (`[FIGURE: ...]`, `![FIG. ...]`, `[NAME logo]`) with working Markdown links. Materialized assets that did not match an inline placeholder land in a trailing "Unmatched Page Assets" block; if every materialized asset is matched inline, no trailing block is emitted. The rewriter overwrites `page_{NNNN}.anchored.md` with the canonical anchored Markdown:
   ```sh
   python3 tools/pdf2md/rewrite_inline_asset_refs.py --page-md {WORK_DIR}/page_{NNNN}.md --materialized-manifest {WORK_DIR}/page_{NNNN}_assets_materialized.json --output-md {WORK_DIR}/page_{NNNN}.anchored.md
   ```
8. After all pages complete, aggregate the public asset manifest:
    ```sh
    python3 tools/pdf2md/aggregate_asset_manifest.py {WORK_DIR} {ASSETS_ROOT}/{PDF_STEM}_assets_manifest.json --doc-stem {PDF_STEM}
    ```
9. Report:
    > "Asset pass complete. Manifest: `{ASSETS_ROOT}/{PDF_STEM}_assets_manifest.json`. Degraded assets: {count/list or 'none'}."

### Phase 4 — Assemble

1. Run the assembly tool:
   - Text-only mode:
   ```
   python3 tools/pdf2md/assemble_markdown.py {WORK_DIR} {OUTPUT_PATH} --separator "{SEPARATOR}"
   ```
   - Asset mode:
   ```
   python3 tools/pdf2md/assemble_markdown.py {WORK_DIR} {OUTPUT_PATH} --separator "{SEPARATOR}" --page-template "page_{page:04d}.anchored.md"
   ```
2. Run a final header/footer pass on the assembled document:
   ```
   python3 tools/reporting/clean_pdf2md_output.py {OUTPUT_PATH}
   ```
3. If `ASSET_MODE=prose`, validate final references:
   ```sh
   python3 tools/pdf2md/validate_assets.py --markdown {OUTPUT_PATH} --manifest {ASSETS_ROOT}/{PDF_STEM}_assets_manifest.json --assets-root {ASSETS_ROOT}
   ```
   Validation failures make the assembled output degraded. List missing files, orphan links, and manifest widows in the Phase 4 report.
4. Report:
   > "Assembly complete. Output: `{OUTPUT_PATH}` ({bytes} bytes, {pages} pages assembled)."
   > "Failed/missing pages: {list or 'none'}."
5. **Degraded-output guidance.** If any pages are failed, empty, contain only placeholder text, or asset validation fails:
   - List each affected page number and its failure mode (`FAILED`, `FAILED_INPUTS`, `empty`).
   - If asset validation failed, list the validation finding categories and counts.
   - State: "This assembly is degraded because it contains placeholder pages and/or unresolved asset references. Recommend rerunning failed pages or failed asset materialization before passing to domain-decomp."
   - The human must explicitly acknowledge the degraded state before downstream use. Automatic pipeline transition to domain-decomp with placeholder-containing output is not a valid workflow.

### Phase 5 — Equation-audit handoff (optional, recommended for math-heavy sources)

If the assembled `OUTPUT_PATH` contains substantive mathematical content (display equations rendered as `$$...$$` blocks), hand off to WORKING_ITEMS using `equation-audit` (`workflows/equation-audit/WORKFLOW.md`) before downstream consumers (domain-decomp) treat the source as canonical.

WORKING_ITEMS continues with the separate `equation-audit` workflow when selected. Freeze its review basis and begin its Gate 0; conversion completion alone does not establish equation verification.

Report:
> "Phase 5 (equation audit) is recommended for this source if it contains substantive mathematical content. To start: WORKING_ITEMS using `Workflow: equation-audit` with WORK_DIR={WORK_DIR}, SOURCE_MD={OUTPUT_PATH}."

For text-only sources (no display equations), skip Phase 5 and proceed directly to domain-decomp.
