# equipment-extract — Tool Policy

## Preferred tool order

Reasoning-first: this skill is LLM-driven; no deterministic tool ordering applies. The agent reads KA markdown files within a single Knowledge Type folder and applies extraction logic directly, producing a normalized, source-traceable equipment register.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted)

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no operational helpers declared (SKILL.md states: "No deterministic tools. This is a reasoning-first extraction skill")

## Expected use of reasoning

This is a reasoning-first extraction skill. The agent reads `_CONTEXT.md`, `_REFERENCES.md`, and all `KA-*.md` files in the KTY folder, then applies extraction logic directly to identify discrete physical equipment items per the in-scope / out-of-scope rules, records the required fields (Equipment Tag, Equipment Name, Package Name, Notes, KA Source), assembles the ordered equipment table, writes Package Notes, and produces the final per-KTY extract file. Reasoning governs every phase: preconditions, KTY context read, KA enumeration and ordering, per-KA equipment extraction, table assembly, Package Notes, and output file composition.

## Disallowed use

- No writing outside `OUTPUT_ROOT`.
- No modification of any file in `KTY_PATH`.
- No widening scope beyond the designated KTY folder.
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary

Writes are limited to:

- `{RuntimeOverrides.OUTPUT_ROOT}/{KTY_ID}_Equipment_Extract.md`

`OUTPUT_ROOT` must already exist. The skill does not create the directory. No files in `{KTY_PATH}` may be written or modified.
