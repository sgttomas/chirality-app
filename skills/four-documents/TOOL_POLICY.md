# TOOL POLICY — four-documents

## Preferred tool order

1. Read deliverable-local context and authoritative source materials.
2. Use direct reasoning to draft or enrich the four-document kit.
3. Optionally invoke `tools/scaffolding/write_status.sh` only for the safe `_STATUS.md` update described in the skill contract.

## Allowed deterministic tools

### TASK-enforced

None. The `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked

- `tools/scaffolding/write_status.sh` — safe `_STATUS.md` update when Pass 1/2 completed and the current state allows transition.

## Expected use of reasoning

This is a reasoning-first drafting skill. It should ground content in locally accessible authoritative source materials, use decomposition/context files as supporting context, and preserve unsupported content as `TBD`, assumptions, or conflicts rather than inventing detail.

## Disallowed use

- No writes outside the target deliverable folder.
- No modification of deliverable metadata files other than the safe `_STATUS.md` update.
- No cross-deliverable scanning or editing.
- No use of `_SEMANTIC_LENSING.md` as evidence authority.

## Write boundary

Writes are limited to:
- `Datasheet.md`
- `Specification.md`
- `Guidance.md`
- `Procedure.md`
- optional `_STATUS.md` safe update within the same deliverable folder
