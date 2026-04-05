# four-documents — Tool Policy

## Preferred tool order

Reasoning-first: drafting and enrichment of the four documents (Datasheet, Specification, Guidance, Procedure) is LLM-driven across Steps 0-6. The sole operational tool invocation is at Step 7 (safe `_STATUS.md` update) when `RUN_PASSES` includes Pass 1 or Pass 2 and the current state is `OPEN`:

1. `tools/scaffolding/write_status.sh {DELIVERABLE_PATH} INITIALIZED TASK+four-documents` — invoked only to transition `OPEN → INITIALIZED`.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter is intentionally omitted).

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- `tools/scaffolding/write_status.sh` — performs the safe `_STATUS.md` update during Step 7; invocation is guided operationally, not enforced through the TASK-consumed allowed-tools contract.

## Expected use of reasoning

This is a reasoning-only skill. Steps 0-6 (preconditions, context reads, DOMAIN/TASK establishment, document generation, cross-reference consistency check, and semantic lensing enrichment) are all LLM-driven. Drafting must be source-grounded in authoritative source slices referenced in `_REFERENCES.md`; decomposition summaries, prior drafts, and generic convention are not authority. Deterministic tooling is only invoked at Step 7 for the safe status update.

## Disallowed use

- No writes outside `{DELIVERABLE_PATH}` (except the status helper which writes to the same folder).
- No modifications to `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_MEMORY.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`.
- No cross-deliverable scanning or editing.
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary

- Write scope: `{DELIVERABLE_PATH}` only.
- Files produced/overwritten: `{DELIVERABLE_PATH}/Datasheet.md`, `{DELIVERABLE_PATH}/Specification.md`, `{DELIVERABLE_PATH}/Guidance.md`, `{DELIVERABLE_PATH}/Procedure.md`.
- Safe-update only: `{DELIVERABLE_PATH}/_STATUS.md` may transition `OPEN → INITIALIZED` when Pass 1/2 ran and current state is `OPEN`; no state regression.
- One deliverable per invocation; no cross-deliverable scanning or editing.
