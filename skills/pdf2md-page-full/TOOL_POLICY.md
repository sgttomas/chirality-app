# pdf2md-page-full - Tool Policy

## Preferred tool order

Reasoning-first: this skill is VLM-driven. The worker reads the page PNG as
multimodal input once, then writes both output files.

Deterministic tools run outside this skill, under the `PDF2MD` orchestrator:

1. `tools/pdf2md/build_page_full_brief.py` renders the dispatch brief.
2. `tools/pdf2md/postprocess_page.py` or `tools/pdf2md/clean_pdf2md_output.py`
   performs Markdown cleanup after the worker writes raw page Markdown.
3. `tools/pdf2md/materialize_page_assets.py` crops/render assets from the page
   asset JSON.
4. `tools/pdf2md/rewrite_inline_asset_refs.py` rewrites placeholders to
   materialized asset links.
5. `tools/pdf2md/aggregate_asset_manifest.py` and `tools/pdf2md/validate_assets.py`
   handle document-level manifest and validation work.

## Allowed deterministic tools

### TASK-enforced

- None. The `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked

- None inside this skill. Operational deterministic tools are invoked by
  `PDF2MD`, not by the page worker.

## Expected use of reasoning

Reasoning is limited to visual transcription, reading-order reconstruction,
asset identification, bbox estimation, caption/slug proposal, confidence
labeling, and structured table transcription from the visible page.

## Disallowed use

- MUST NOT read any file other than `IMAGE_PATH`.
- MUST NOT write any file other than `OUTPUT_MD_PATH` and `OUTPUT_JSON_PATH`.
- MUST NOT run deterministic tools.
- MUST NOT crop images, render XLSX files, rewrite Markdown links, assemble
  manifests, or validate final filesystem references.
- MUST NOT widen scope beyond the designated page.

## Write boundary

Writes are limited to exactly two files:

- `OUTPUT_MD_PATH`
- `OUTPUT_JSON_PATH`
