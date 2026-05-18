# kty-metadata-align — Tool Policy

## Preferred tool order

Reasoning-first:

1. read decomposition truth for the target KTY
2. read existing `_CONTEXT.md`, `_STATUS.md`, sibling `_MEMORY.md` / `MEMORY.md`
   when present as non-authoritative operational context, and `_REFERENCES.md`
3. classify observed drift into `REPAIRED_NOW`, `RERUN_LATER`, or `UNRESOLVED`
4. in `ALIGN_METADATA` mode only, repair authorized metadata files
5. write the optional report and any follow-on recommendations

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill
load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools`
  frontmatter field is intentionally omitted)

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no deterministic helpers declared

## Expected use of reasoning

This skill is a bounded metadata-normalization pass. Reasoning governs:

- matching the folder to one decomposition KTY row
- determining whether lifecycle drift is actually unambiguous
- preserving human-authored reference notes while keeping authoritative pointers
  current
- deciding when content drift requires rerun rather than metadata editing

## Disallowed use

- No edits outside `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, and the
  optional report path.
- No rewriting `Scoping.md`, `KA-*.md`, `_DEPENDENCIES.md`, `_MEMORY.md`, or
  lifecycle semantics that are not authority-backed.
- No use of `_MEMORY.md` / `MEMORY.md` as decomposition truth or lifecycle
  authority. It is context only and is read only when paired with `_STATUS.md`.
- No invented `SourceSpan`, source paths, or lifecycle states.
- No silent deletion of human-authored notes unless the brief explicitly
  authorizes replacement.

## Write boundary

Writes are limited to:

- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_STATUS.md`
- `{KTY_PATH}/_REFERENCES.md`
- optional `{REVIEW_OUTPUT_PATH}`

No other files may be created or modified by this skill.
