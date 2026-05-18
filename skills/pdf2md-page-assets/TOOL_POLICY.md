# pdf2md-page-assets - Tool Policy

## Preferred tool order

Reasoning-first: this skill is VLM-driven. The agent reads the cleaned page Markdown for text context, then reads the page PNG as multimodal input, then writes one JSON file.

Deterministic tools run outside this skill, under the `PDF2MD` orchestrator:

1. `tools/pdf2md/build_page_assets_brief.py` renders the dispatch brief.
2. `tools/pdf2md/materialize_page_assets.py` crops images, delegates to `render_table_xlsx.py` for table XLSX rendering, and writes anchored page Markdown.
3. `tools/pdf2md/render_table_xlsx.py` renders one deterministic XLSX per `table_data` block.
4. `tools/pdf2md/aggregate_asset_manifest.py` merges page manifests.
5. `tools/pdf2md/validate_assets.py` validates final references.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None - no TASK-enforced deterministic allowlist. The `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None inside this skill. Operational deterministic tools are invoked by `PDF2MD`, not by the page-assets worker.

## Expected use of reasoning

Reasoning is limited to visual asset identification, bounding-box estimation, caption/slug proposal, confidence labeling, and structured `table_data` transcription (rows, cells, merges, headers, footnotes, cell typing) from the visible page. The worker may use `PAGE_MD_PATH` only as context for visible captions or already-transcribed tables; the page image remains the authority for asset existence.

## Disallowed use

- MUST NOT crop images.
- MUST NOT write PNG files.
- MUST NOT write CSV or XLSX files.
- MUST NOT emit the legacy `csv_text` field — the canonical table representation is the structured `table_data` block defined in `SKILL.md`.
- MUST NOT rewrite Markdown.
- MUST NOT aggregate manifests.
- MUST NOT validate final filesystem references.
- MUST NOT read files outside `IMAGE_PATH` and `PAGE_MD_PATH`.
- MUST NOT write files outside `OUTPUT_PATH`.
- MUST NOT assign final stable filenames.

## Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` - page-level asset JSON

The output filename is deterministic from the orchestrator brief. The skill must not derive or modify it.
