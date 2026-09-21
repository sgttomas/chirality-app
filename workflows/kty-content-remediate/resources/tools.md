# kty-content-remediate - Tool Policy

## Preferred tool order

Reasoning-first:

1. read the accepted WORKING_ITEMS (workflow: scope-change) snapshot and admitted decomposition authority
2. enumerate root-level `Scoping.md` and `KA-*.md` under the target KTY
3. exclude `.Archive/` from current-content enumeration
4. in `RETIRE_KTY`, archive active-looking files and write tombstone stubs
5. in `VERIFY_KTY` or `EMIT_DISPOSITION`, report current disposition only
6. emit report and optional structured evidence

## Allowed deterministic tools

### Declared command restrictions

The optional execution.json contains declared command restrictions. Effective authorization also depends on the host, role, and brief; report the actual enforcement boundary.

- None - no additional command restriction. The `allowed-tools`
  frontmatter field is intentionally omitted.

### Operationally invoked

_Tools named in `## Tool usage` body; operational guidance within effective permissions._

- None - no deterministic helpers declared.

Do not list or invoke `tools/scaffolding/write_status.sh`; this workflow does not
write `_STATUS.md`.

## Expected use of reasoning

This workflow is a bounded disposition and evidence pass. Reasoning governs:

- whether a file is active-looking or already tombstoned
- whether the observed state matches structured SCA disposition expectations
- whether authority is sufficient to claim factual-use safety
- how to classify blocker notes for WORKING_ITEMS (workflow: scope-change)

## Disallowed use

- No active content rewriting. The workflow never modifies active factual content.
- No dispatching other workflows.
- No edits to `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`,
  `_MEMORY.md` / `MEMORY.md`, `_SEMANTIC.md`, decomposition files, WORKING_ITEMS (workflow: scope-change)
  manifests, `_Aggregation`, hypergraph outputs, or publication outputs.
- No treatment of `.Archive/` as factual authority.
- No hidden source override of accepted SCA/decomposition truth.
- Do not infer supersessions from SCA prose.

## Write boundary

Writes are limited by `MODE` and `AllowedWriteTargets`:

- `RETIRE_KTY`: `{KTY_PATH}/.Archive/{ARCHIVE_RUN_ID}/...`, tombstone stubs at
  original `Scoping.md` / `KA-*.md` paths, `REVIEW_OUTPUT_PATH`, and optional
  `DISPOSITION_EVIDENCE_PATH`.
- `VERIFY_KTY`: `REVIEW_OUTPUT_PATH` and optional
  `DISPOSITION_EVIDENCE_PATH`.
- `EMIT_DISPOSITION`: `REVIEW_OUTPUT_PATH` and optional
  `DISPOSITION_EVIDENCE_PATH`.

No other files may be created or modified.

## .Archive/ scanner exclusion

`.Archive/` scanner exclusion is mandatory. Downstream scanners, allowlists,
section maps, publication inputs, and regeneration inputs must consume only
root-level current content unless explicitly performing historical audit.
