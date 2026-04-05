# estimate-snapshot — Tool Policy

## Preferred tool order

1. `tools/validation/validate_enum.py` — validate `BASIS_OF_ESTIMATE` at Step 0 (halt with `FAILED_INPUTS` if invalid).
2. `tools/scaffolding/create_snapshot_folder.sh` — create the immutable snapshot folder with canonical naming.
3. `tools/scaffolding/update_latest_pointer.sh` — update `_LATEST.md` pointer only when `UPDATE_LATEST_POINTER=TRUE`.
4. Reasoning + file-write operations then load decomposition, enumerate scope, load dependency and pricing evidence, generate `Detail.csv` / rollups / matrices, and emit QA and log artifacts.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- `python3 tools/validation/validate_enum.py:*`
- `bash tools/scaffolding/create_snapshot_folder.sh:*`
- `bash tools/scaffolding/update_latest_pointer.sh:*`

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no additional operational helpers declared beyond the TASK-enforced tools.

## Expected use of reasoning

Deterministic tools handle enum validation and snapshot folder / pointer management. All substantive work — scope resolution, decomposition reading, dependency evidence loading, pricing source indexing, line-item generation against `BASIS_OF_ESTIMATE`, WBS×CBS rollup, provenance assignment, blocker identification, and QA reporting — is reasoning-driven against local inputs.

## Disallowed use

- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.
- No writes outside `{ESTIMATES_ROOT}`.
- No modification of any file in deliverable folders, decomposition outputs, dependency registers, or lifecycle files.
- No overwriting an existing snapshot folder.
- No internet fetching (only local `PRICE_SOURCES`).
- No treating prior snapshots under `_Estimates/` as pricing sources unless explicitly included in `PRICE_SOURCES`.

## Write boundary

Write ONLY under `{ESTIMATES_ROOT}` (tool-root-only), into a new per-run snapshot folder `{ESTIMATES_ROOT}/EST_{OUTPUT_LABEL}_{YYYY-MM-DD}_{HHMM}/`. Optionally update `{ESTIMATES_ROOT}/_LATEST.md` when `UPDATE_LATEST_POINTER=TRUE`. No writes outside `ESTIMATES_ROOT`. No modification of project truth (deliverable content, lifecycle files, decomposition outputs, dependency registers).
