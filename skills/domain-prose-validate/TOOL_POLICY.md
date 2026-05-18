# domain-prose-validate - Tool Policy

## Preferred tool order

Reasoning-first: this skill is VLM-driven. The agent reads the asset bbox hints (text JSON) to set expectations, then reads the page PNG as multimodal input, then writes one Markdown file.

Deterministic tools run **outside** this skill, under the Gate 1.5-P orchestration in `DOMAIN_DECOMP`:

1. The Stage 1 orchestrator builds the per-page hints JSON from the asset manifest and dispatches one TASK per page.
2. `tools/source_audit/compare_extracts.py` (Stage 2) deterministically aligns the original `page_NNNN.md` against this skill's `page_NNNN.reextract.md` and emits `prose_validation.json`.
3. Stage 3 (persona) consolidates findings, dispatches `pdf2md-page-assets` re-dispatch for structural fails, and dispatches `equation-flag-interpret` for equation-content proposals.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None - no TASK-enforced deterministic allowlist. The `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None inside this skill. Operational deterministic tools are invoked by the Gate 1.5-P orchestration, not by the page-level re-extraction worker.

## Expected use of reasoning

Reasoning is limited to: prose transcription from the page raster, reading-order interpretation, display- vs. inline-equation classification, LaTeX transcription of display equations, and choosing the correct `[FIGURE:]` / `[TABLE:]` / `[IMAGE:]` placeholder form at each asset position. The bbox hints provide expected placement only; the page image remains the sole authority for textual content and caption text.

## Disallowed use

- MUST NOT read any pre-existing per-page Markdown (`page_*.md`), the assembled `<book>.md`, audit sidecars, or any other materialized extraction artifact. This is the cornerstone of Gate 1.5-P — reading the original extract collapses the comparator.
- MUST NOT read neighbouring page rasters, manifests, sibling Markdown, or asset XLSX files.
- MUST NOT crop images.
- MUST NOT write PNG, CSV, JSON, or XLSX files.
- MUST NOT transcribe table cells (emit a `[TABLE: ...]` placeholder instead).
- MUST NOT emit Markdown image syntax (`![alt](path)`) or link syntax (`[XLSX](...)`) — those are Stage 2's responsibility to align against.
- MUST NOT emit asset IDs, asset filenames, or any text copied from `ASSET_BBOX_HINTS_PATH` other than the implicit choice of placeholder kind.
- MUST NOT emit Markdown frontmatter, `# Page N` headings, or any metadata wrapping in the output.
- MUST NOT read files outside `IMAGE_PATH` and `ASSET_BBOX_HINTS_PATH`.
- MUST NOT write files outside `OUTPUT_PATH`.

## Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` - the per-page Markdown re-extract

The output filename is deterministic from the orchestrator brief. The skill must not derive or modify it.
