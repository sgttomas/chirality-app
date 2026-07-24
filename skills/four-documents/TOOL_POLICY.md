# TOOL POLICY — four-documents

This is a compatibility-only policy for an existing complete
`LEGACY_FOUR_DOC` contract. It rejects new PROJECT/SOFTWARE initialization,
`SOW_V1`, missing/partial/invalid formats, and any dual state.

## Preferred tool order

1. Read deliverable-local context and authoritative source materials.
2. Use direct reasoning to draft or enrich the four-document kit.
3. Preserve `_STATUS.md` byte-identically; do not invoke lifecycle writers.

## Allowed deterministic tools

### TASK-enforced

None. The `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked

- No lifecycle writer is authorized by this compatibility skill.

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
