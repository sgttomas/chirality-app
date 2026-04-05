# estimate-prep — Tool Policy

## Preferred tool order

1. `tools/validation/validate_enum.py` — validate the `PHASE` input at the start of the run.
2. `tools/scaffolding/scaffold_tool_root.sh` — create the `_EstimatePrep/` tool root if it does not yet exist.
3. `tools/scaffolding/create_snapshot_folder.sh` — create the immutable per-run snapshot folder (`EPREP_SCAFFOLD_…` or `EPREP_BOE_…`).
4. `tools/reporting/generate_index_md.sh` — generate the file-inventory portion of `PriceSources/INDEX.md` during Phase SCAFFOLD.
5. Reasoning + file-write operations then produce CSVs, the BOE scaffold, the full BOE, and the handoff artifacts against the canonical schemas.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted).

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- `tools/validation/validate_enum.py` — validates `PHASE` input.
- `tools/scaffolding/scaffold_tool_root.sh` — creates `_EstimatePrep/` tool root.
- `tools/scaffolding/create_snapshot_folder.sh` — creates immutable snapshot folder.
- `tools/reporting/generate_index_md.sh` — generates file inventory portion of `INDEX.md`.

## Expected use of reasoning

Deterministic helpers are used operationally for enum validation, tool-root and snapshot folder creation, and the file-inventory portion of `INDEX.md`. Everything else — CSV content generation against the canonical Schema Annex, the BOE scaffold, the full `BASIS_OF_ESTIMATE.md`, tier sequencing, aggregation strategy, confidence assignment, override logging, conflict surfacing, and all QA/handoff artifacts — is produced by reasoning + file-write operations.

## Disallowed use

- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.
- No writes outside `{EXECUTION_ROOT}/_EstimatePrep/`.
- No overwriting prior snapshots.
- No modification of `_PriceSources/`, `_Estimates/`, deliverable folders, decomposition outputs, or dependency registers.
- No recursive ingestion of prior `_EstimatePrep/` outputs unless explicitly provided as `PRIOR_SNAPSHOT` / `SCAFFOLD_PATH`.

## Write boundary

Write ONLY under `{EXECUTION_ROOT}/_EstimatePrep/`, into a new per-run snapshot folder (`EPREP_SCAFFOLD_{LABEL}_{DATE}_{TIME}/` or `EPREP_BOE_{LABEL}_{DATE}_{TIME}/`). Snapshots are immutable — never overwrite prior snapshots. Never modify `_PriceSources/`, `_Estimates/`, deliverable folders, decomposition outputs, or dependency registers. Publishing to canonical locations is a separate, human-approved step handled by the invoker.
