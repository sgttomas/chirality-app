# dependency-extract — Tool Policy

## Preferred tool order

1. Reasoning-led two-pass extraction (Pass 1 ANCHOR from `{ANCHOR_DOC}`, then Pass 2 EXECUTION from `{EXECUTION_DOC_ORDER}`) over the deliverable's source documents, `_REFERENCES.md`, and `{DECOMPOSITION_PATH}` (when available).
2. Reasoning-led target resolution, row match/merge, and persistence to `Dependencies.csv` and `_DEPENDENCIES.md`.
3. `python3 tools/validation/validate_dependencies_schema.py {deliverable_folder}/Dependencies.csv` — Function 5 schema validation (confirms all 29 required v3.1 columns are present and CSV is parseable).
4. `python3 tools/validation/validate_enum.py {ENUM_NAME} {value}` — Function 5 enum-field normalization and validation on write.
5. `tools/validation/validate_id_format.sh {TYPE} {value}` — Function 5 ID-format validation for deliverable/package/WBS IDs.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- `python3 tools/validation/validate_dependencies_schema.py:*`
- `python3 tools/validation/validate_enum.py:*`

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- `tools/validation/validate_id_format.sh {TYPE} {value}` — validates deliverable/package/WBS ID formats

## Expected use of reasoning

Reasoning is the primary extraction engine. The agent performs evidence-first two-pass extraction: Pass 1 (Vertical) anchors the deliverable to the Tree (Definition) by reading the ANCHOR_DOC and emitting `DependencyClass=ANCHOR` rows; Pass 2 (Horizontal) maps DAG execution flow edges by reading EXECUTION_DOCS and emitting `DependencyClass=EXECUTION` rows. Reasoning also governs target resolution (best-effort, conservative; `UNKNOWN` when uncertain), match/merge precedence, enum normalization on write (e.g., `INBOUND` -> `UPSTREAM`), `_DEPENDENCIES.md` index updates (Run Notes, Run History, Lifecycle Summary), and Tree x DAG integrity checks (FLOATING_NODE, AMBIGUOUS_ANCHOR, MISSING_DECOMPOSITION warnings). Deterministic tools intervene during Function 5 local quality checks for schema validation, enum validation, and ID-format validation.

## Disallowed use

- No editing of any source document or `_REFERENCES.md`.
- No editing of decomposition outputs.
- No writes outside dependency artifacts (`{deliverable}/_DEPENDENCIES.md`, `{deliverable}/Dependencies.csv`).
- No hierarchy discovery (no creating or restructuring the decomposition Tree).
- No cross-deliverable synthesis (aggregation is downstream).
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary

Writes are limited to dependency artifacts only:

- `{deliverable}/_DEPENDENCIES.md`
- `{deliverable}/Dependencies.csv`

No other files may be created or modified.
