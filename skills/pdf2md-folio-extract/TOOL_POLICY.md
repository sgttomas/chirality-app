# pdf2md-folio-extract - Tool Policy

## Preferred tool order

Reasoning-first: this skill is VLM-driven. The agent reads the page PNG as multimodal input and writes one JSON file. There are no deterministic helpers inside this skill.

Deterministic tools run outside this skill, under the `PDF2MD` orchestrator (folio-map assembly, reconciliation against the physical sequence, propagation into per-page asset records, etc.).

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None - no TASK-enforced deterministic allowlist. The `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None inside this skill. Operational deterministic tools are invoked by `PDF2MD`, not by the folio-extract worker.

## Expected use of reasoning

Reasoning is limited to:

- Locating the printed folio in conventional folio zones on the page image.
- Transcribing the visible glyph verbatim (Arabic / Roman / prefixed / hyphenated forms) without normalization.
- Naming the zone (`top-left`, `top-center`, `top-right`, `bottom-left`, `bottom-center`, `bottom-right`).
- Assigning a confidence label based on legibility and zone conventionality.
- Recognizing when no folio is printed and emitting `NO_FOLIO` rather than inventing a value.

The page image is the sole authority for folio existence and form.

## Disallowed use

- MUST NOT crop images.
- MUST NOT write PNG, CSV, or XLSX files.
- MUST NOT rewrite Markdown.
- MUST NOT assemble or aggregate folio maps.
- MUST NOT read files outside `IMAGE_PATH`.
- MUST NOT write files outside `OUTPUT_PATH`.
- MUST NOT consult neighbouring page images, sibling folio JSON, manifests, the source PDF, the page Markdown, or any TOC / outline artifact.
- MUST NOT invent a folio from the physical PDF sequence (`PAGE_NUM`).
- MUST NOT infer a folio from neighbouring pages' numbering.
- MUST NOT normalize Roman numerals to Arabic, strip section prefixes, or zero-pad.
- MUST NOT assign final stable filenames.

## Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` - page-level folio JSON

The output filename is deterministic from the orchestrator brief. The skill must not derive or modify it.
