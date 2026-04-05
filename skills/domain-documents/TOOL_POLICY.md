# domain-documents — Tool Policy

## Preferred tool order

Reasoning-first: extraction and authoring of `Scoping.md` plus variable `KA-*.md` Knowledge Artifact files is LLM-driven across Steps 0-6. The sole operational tool invocation is at Step 7 (safe `_STATUS.md` update) when `RUN_PASSES` includes Pass 1 or Pass 2 and the current state is `OPEN`:

1. `tools/scaffolding/write_status.sh {kty_folder} INITIALIZED TASK+domain-documents` — invoked only to transition `OPEN → INITIALIZED`.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted).

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- `tools/scaffolding/write_status.sh` — preferred utility script for safe `_STATUS.md` updates under safe-update rules only.

## Expected use of reasoning

This is a reasoning-first extraction + authoring skill. No deterministic tools are used for drafting. Steps 0-6 (preconditions, context + decomposition reads, draft-plan parsing, default-schema establishment, document generation, cross-artifact consistency check, and source-fidelity verification) are all LLM-driven. Artifact prose must be grounded in authoritative source slices bounded by `SourceSpan`; decomposition summaries, atomic statements, and prior draft wording are not authority. Deterministic tooling is only invoked at Step 7 for the safe status update.

## Disallowed use

- No modification of metadata files: `_CONTEXT.md`, `_REFERENCES.md`, `_MEMORY.md`/`MEMORY.md`, `_SEMANTIC.md`.
- No overwriting Knowledge Artifact files when `Current State` is outside `ALLOW_OVERWRITE_STATES`.
- No cross-Knowledge-Type scanning — one Knowledge Type folder per run.
- No fabrication of source excerpts when the source file is inaccessible.
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary

- Write scope: `{KTY_PATH}` only.
- Files produced/overwritten: `Scoping.md` (stable entrypoint with identity, canonical schema, evidence table, artifact plan table, conflict table, source-fidelity log) and variable `KA-*.md` Knowledge Artifact files (one per Knowledge Subject) in `{KTY_PATH}`.
- Safe-update only: `{KTY_PATH}/_STATUS.md` may transition `OPEN → INITIALIZED` when Pass 1/2 ran and current state is `OPEN`; no state regression.
- One Knowledge Type folder per run; no cross-Knowledge-Type scanning.
