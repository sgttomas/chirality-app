# pdf2md-page — Tool Policy

## Preferred tool order

Reasoning-first: this skill is LLM-driven; no deterministic tool ordering applies. The agent uses its native Read tool to load the page PNG as multimodal (vision) input, performs VLM transcription of the image contents to Markdown, and uses its native Write tool to produce the single output file.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted)

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no operational helpers declared (SKILL.md states: "No deterministic tools. This is a VLM-reasoning-only skill"; post-processing is PDF2MD's responsibility)

## Expected use of reasoning

This is a VLM-reasoning-only skill. The agent's entire value is the multimodal perception step: reading a page image and transcribing its contents to Markdown. Reasoning governs input validation, image examination, Markdown structuring per the declared rules (text preservation, structure, tables, code, formulas, ignore-list, output format), and failure-placeholder handling. All cleanup, coordination, and assembly belong to the PDF2MD orchestrator and are out of scope for this skill.

## Disallowed use

- MUST NOT run `postprocess_page.py` or any other cleanup tool. Post-processing is PDF2MD's responsibility.
- MUST NOT read any file other than `IMAGE_PATH`.
- MUST NOT write any file other than `OUTPUT_PATH`.
- MUST NOT widen scope beyond the designated page.
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` — the page Markdown (or a failure placeholder)

The output filename is deterministic: it is precisely `OUTPUT_PATH` as provided in the brief. The skill does not derive or modify the filename.
