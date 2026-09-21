---
name: preparation
description: Materialize accepted Chirality package, deliverable, category, knowledge-type, or tool-root scope as idempotent folders and source-faithful control files. Use for structural workspace setup, not production-content drafting.
---

# Preparation

Create one bounded scaffold from accepted decomposition data. Preserve every pre-existing path and report exactly what the run created or skipped.

## Inputs

Require an execution root, the selected operation, the accepted identifiers and names, and the decomposition source for any metadata-bearing item. The supported operations are:

- package or category lifecycle hierarchy;
- package reference index;
- deliverable or knowledge-type minimum fileset;
- aggregation or domain tool-root prerequisites.

If a required source field is absent, stop that operation and report the missing field. Do not infer names, descriptions, dependencies, artifacts, or lifecycle state.

Read [references/scaffold-contract.md](references/scaffold-contract.md) before creating a deliverable or knowledge type; it preserves the operation map and exact control-file schemas.

## Method

1. Resolve the target paths using filesystem-safe labels while retaining canonical names inside control files. Replace `/`, `\\`, `:`, `*`, `?`, `"`, `<`, `>`, and `|` with `-`; collapse and trim whitespace.
2. Inventory every target before invoking a scaffold tool. Prefer the repository helpers under `tools/scaffolding/`, including `scaffold_package.sh`, `scaffold_deliverable.sh`, `scaffold_tool_root.sh`, and `write_status.sh`.
3. Capture each tool-emitted `CREATED_PATH` and compare it with the pre-run inventory. Treat an existing empty file as existing work.
4. Populate only files created by this invocation. Initialize `OPEN` status only when `_STATUS.md` is new.
5. For a deliverable or knowledge type, ensure `_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md`, `_REFERENCES.md`, and a placeholder `_SEMANTIC.md` exist. `_CONTEXT.md` must reproduce accepted decomposition fields exactly. Add only human-declared dependencies; otherwise record the declared coordination mode without inventing edges.
6. Run `tools/validation/check_min_viable_fileset.sh` for each deliverable or knowledge-type scaffold. Use `tools/validation/validate_id_format.sh` before creating a path when identifier validity is uncertain.
7. Return exact `created_paths`, `skipped_paths`, validation results, and unresolved source fields.

## Boundaries

This skill is structural. Do not draft engineering, software, publication, or Knowledge Subject content. New PROJECT or SOFTWARE production content belongs to the applicable production workflow. Create `_MEMORY.md` only when the request explicitly selects it and authorizes that path. Never overwrite or repair an existing file unless a separate repair request authorizes that change.
