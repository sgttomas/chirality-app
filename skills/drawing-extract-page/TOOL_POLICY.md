# drawing-extract-page — Tool Policy

## Preferred tool order

Reasoning-first: this skill is LLM-driven; no deterministic tool ordering applies. The agent uses its native Read tool to load page images and helper crops, performs VLM reasoning over the image contents, and uses its native Write tool to produce the single output artifact.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted)

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no operational helpers declared (SKILL.md states: "No deterministic tools. This skill is VLM-reasoning-only"; PDF-level cross-checking belongs to the orchestrator)

## Expected use of reasoning

This skill is bounded visual extraction via direct image inspection, not deterministic tooling. The agent uses the native Read tool to load the page image (and any provided helper crops and header slices), applies VLM reasoning to identify page regions according to the `EXTRACTION_MODE`, applies the extraction rules (no invention, region discipline, required companion fields, primary name only, multi-block header completeness, low-count skepticism, grouped tags), and writes the structured output. Reasoning governs every phase: input validation, crop-first region identification, per-mode extraction, rule application, and output assembly.

## Disallowed use

- No deterministic tool invocation; no shell commands.
- No writing outside `OUTPUT_PATH`.
- No reading of files outside the declared read boundary (no cross-page context, no Scoping.md, no other page images).
- No sub-agent fanout.
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary

Writes are limited to exactly one file per invocation:

- `OUTPUT_PATH` — exactly one structured artifact per invocation (a `markdown_stub` artifact, or a `csv_row` artifact)

No other files are written. `OUTPUT_PATH`'s parent directory must already exist; the skill does not create directories.
