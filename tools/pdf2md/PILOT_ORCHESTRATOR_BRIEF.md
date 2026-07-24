# PDF2MD pilot-tranche orchestrator runbook

You are a PDF2MD orchestrator handling **one** PDF end-to-end through the protocol's
4 phases plus 3.5 prose-asset materialization plus redaction. The campaign is the
industry-practices corpus pilot tranche.

**Per-page dispatch contract (canonical):** the merged `pdf2md-page-full` skill
emits both `page_NNNN.md` and `page_NNNN_assets.json` from a single multimodal
read. There is no separate asset-discovery dispatch. (The legacy two-skill split
— `pdf2md-page` + a Phase 3.5 `pdf2md-page-assets` pass — remains on disk for
resuming PDFs that were already processed under the old contract; do not use
for new PDFs.)

You will be given exactly two inputs by the parent caller:
- `PDF_PATH` — absolute path to the single PDF you own
- `STEM` — the file stem (PDF basename without `.pdf`)

All other paths derive from these. Resolve `REPO_ROOT` with
`git rev-parse --show-toplevel` and use derived absolute paths.

## Derived paths

- `PDF_DIR`     = directory containing PDF
- `CHAPTER_DIR` = `PDF_DIR` (chapter folder; PDFs live directly in chapter folders)
- `WORK_DIR`    = `PDF_DIR/{STEM}_pdf2md_work`
- `ASSETS_ROOT` = `CHAPTER_DIR/_assets/{STEM}`
- `OUTPUT_MD`   = `PDF_DIR/{STEM}.md`
- `MANIFEST`    = `ASSETS_ROOT/{STEM}_assets_manifest.json`

## Campaign parameters (frozen)

- DPI=300, model=sonnet, ASSET_MODE=prose
- Merged page workers dispatched via Agent tool, `subagent_type: general-purpose`, `model: sonnet`. Each worker produces BOTH `page_NNNN.md` and `page_NNNN_assets.json` from one vision read; there is no separate asset-discovery wave.
- **Use BATCH_SIZE up to 40 per wave.** Validated end-to-end across PDFs 06–10 with zero rejections at this size (one isolated worker-level rejection in PDF 06 wave 2, handled by re-dispatch). After each wave, **audit on-disk** by counting `page_*.md` and `page_*_assets.json` files in `WORK_DIR` and re-dispatching any missing page solo before proceeding.

## Execution steps

### 1. Rasterize

```
python3 tools/pdf2md/rasterize_pdf.py {PDF_PATH} {WORK_DIR} --dpi 300
```

Read `WORK_DIR/manifest.json`; capture `total_pages` = N.

### 2. Build all merged page briefs

For pages 1..N (zero-padded 4 digits):

```
python3 tools/pdf2md/build_page_full_brief.py \
  --work-dir {WORK_DIR} --doc-stem {STEM} \
  --page {n} --total-pages {N} \
  > {WORK_DIR}/briefs/page_{nn}.brief.md
```

(Create `briefs/` if needed. The brief builder writes to stdout; redirect to the output path.)

Check the first brief to confirm format.

### 3. Dispatch merged page workers in waves of up to 40 (parallel sub-agents)

Each dispatch produces BOTH the per-page Markdown and the per-page asset JSON from one multimodal read of the page image. For each wave, spawn up to 40 parallel Agent calls in a single message (last wave may be smaller). Each sub-agent uses this prompt template:

```
TASK+pdf2md-page-full worker.
Brief: {WORK_DIR}/briefs/page_{nn}.brief.md
Steps: Read brief → Read skills/pdf2md-page-full/SKILL.md (cwd {REPO_ROOT}) → Read IMAGE_PATH (single multimodal read) → Transcribe to Markdown per the 8 SKILL rules with [FIGURE:]/[TABLE:]/[... logo] placeholders → Identify visible assets and emit pdf2md-page-assets/v1 JSON with one-to-one placeholder↔entry correspondence → Write Markdown to OUTPUT_MD_PATH and JSON to OUTPUT_JSON_PATH → Report: RUN_STATUS=<literal> page={n} md_bytes=<n> assets=<n>.
```

`subagent_type: general-purpose`, `model: sonnet`. **All workers in a single message** so they run in parallel.

After each wave, do an **on-disk audit**: count `page_*.md` and `page_*_assets.json` files in WORK_DIR and identify any missing pages. Re-dispatch missing pages solo before proceeding (a worker can occasionally be rejected by the harness without a clear failure signal in the return text — trust the filesystem, not the agent reports).

### 4. Postprocess + clean each page

After all N pages converted:

```
for n in 1..N:
    python3 tools/pdf2md/postprocess_page.py {WORK_DIR}/page_{nn}.md
    python3 tools/reporting/clean_pdf2md_output.py {WORK_DIR}/page_{nn}.md
```

Single Bash command using a shell loop is fine.

### 5. Filter logo img assets (campaign policy)

```
python3 tools/pdf2md/filter_logo_assets.py {WORK_DIR}
```

Idempotent. Removes `kind:"img"` entries whose caption matches `/logo/i`.

### 6. Materialize + rewrite each page

```
for n in 1..N:
    python3 tools/pdf2md/materialize_page_assets.py \
      --page-image {WORK_DIR}/page_{nn}.png \
      --page-md {WORK_DIR}/page_{nn}.md \
      --asset-json {WORK_DIR}/page_{nn}_assets.json \
      --assets-root {ASSETS_ROOT} \
      --doc-stem {STEM} --page {n} \
      --output-md {WORK_DIR}/page_{nn}.anchored.md \
      --manifest-output {WORK_DIR}/page_{nn}_assets_materialized.json

    python3 tools/pdf2md/rewrite_inline_asset_refs.py \
      --page-md {WORK_DIR}/page_{nn}.anchored.md \
      --materialized-manifest {WORK_DIR}/page_{nn}_assets_materialized.json \
      --output-md {WORK_DIR}/page_{nn}.anchored.md
```

Note: manifest output MUST be named `page_{nn}_assets_materialized.json` (the aggregator's filename regex).

Industry-source redaction is intentionally **not** part of the pipeline. The corpus retains source-organization names verbatim; downstream consumers can apply their own obscuration if needed. The single-word "Shell" alias in particular collided too often with the engineering noun (shell-and-tube, head-to-shell seam, shell-side flow), and similar precision problems exist for other terms.

### 7. Aggregate + assemble + validate

```
python3 tools/pdf2md/aggregate_asset_manifest.py {WORK_DIR} {MANIFEST} --doc-stem {STEM}
python3 tools/pdf2md/assemble_markdown.py {WORK_DIR} {OUTPUT_MD} \
  --separator "---" --page-template "page_{page:04d}.anchored.md"
python3 tools/reporting/clean_pdf2md_output.py {OUTPUT_MD}
python3 tools/pdf2md/validate_assets.py --markdown {OUTPUT_MD} \
  --manifest {MANIFEST} --assets-root {ASSETS_ROOT}
```

Expected final line of validate output: `asset_validation=PASS`.

### 8. Final smoke checks (report these to the parent)

```
# Final file size
wc -c {OUTPUT_MD}

# Asset count (from manifest)
python3 -c "import json,sys; print('assets=', len(json.load(open(sys.argv[1])).get('assets', [])))" {MANIFEST}
```

Note: leak-grep and Industry-Source histogram are no longer part of smoke checks — the corpus retains source-org names verbatim.
```

## Report (single message at the end)

```
PDF_STEM={STEM}
PAGES=N
OUTPUT_MD={OUTPUT_MD} (size=...)
ASSETS_MATERIALIZED=<count>
VALIDATE_ASSETS=PASS|FAIL
DEGRADED_PAGES=<list or none>
NOTES=<anything unexpected>
```

If anything fails at any phase, stop and report which phase, the error, and what state was left on disk.

## Important guardrails

- Never use `--no-verify` or any destructive git ops; you are not committing here.
- Do not create or edit any file outside `WORK_DIR`, `ASSETS_ROOT`, or `OUTPUT_MD`.
- Always check existence of the source PDF before rasterizing.
- Use absolute paths everywhere.
- Use the Bash tool with `run_in_background` only if a single command would exceed 2 min; per-page loops are fast (< 30s for 100 pages).
