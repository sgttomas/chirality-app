# semantic-matrix-build — Tool Policy

## Tool posture

Reasoning-first. The semantic derivation is LLM-driven. Deterministic tools are used only for validation and filesystem safety when available.

The `allowed-tools` frontmatter field is intentionally omitted in `SKILL.md`. TASK and the run brief decide whether tool execution is restricted.

## Preferred tool sequence

1. Read files inside `ScopePath` needed by the skill.
2. Generate `_SEMANTIC.md` by reasoning from the skill contract.
3. Run the semantic audit specified in `QA_CHECKS.md`.
4. If available and permitted, run:

```sh
python3 tools/validation/validate_semantic_matrix.py "{deliverable_folder}"
```

5. If available and permitted, run the semantic pipeline scope validator used by the project for Phase 2.3.
6. Write/update the TASK run record according to `AGENT_TASK.md`.

## Allowed deterministic tools

### TASK-enforced

None declared by this skill frontmatter. If the brief supplies `AllowedTools`, TASK enforces that list.

### Operational helpers

| Tool | Use | Required? |
|---|---|---|
| `python3 tools/validation/validate_semantic_matrix.py` | Validate `_SEMANTIC.md` structure and matrix invariants. | Required in normal repo runs when available and permitted. |
| `python3 tools/validation/validate_semantic_pipeline_scope.py` | Confirm Phase 2.3 touched only allowed semantic-scope files. | Required when project PROJECT_SETUP policy calls for it and the tool is available. |

If a validator is unavailable, do not claim validator PASS. Report `validator not available`.

## Expected use of reasoning

Reasoning is required for:

- deriving the deliverable perspective;
- choosing deliverable-conditioned but non-literal semantic phrases;
- resolving each axis anchor;
- resolving every projected contributor in Step 2;
- selecting centroid attractors;
- auditing final cells for semantic product validity.

## Disallowed use

Do not use tools or scripts to bypass the semantic reasoning work. A generated table of formulas without resolved semantic phrases is invalid.

Do not:

- edit production documents;
- edit `_CONTEXT.md`, `_REFERENCES.md`, `_DEPENDENCIES.md`, or `MEMORY.md`;
- write outside the effective bounded task brief's authorization;
- scan sibling deliverables;
- claim cross-deliverable conclusions;
- claim engineering correctness;
- claim validator PASS unless the validator actually ran;
- hide conflicts between TASK write authorization, brief instructions, and skill requirements.

## Write boundary

Allowed write target:

- `{deliverable_folder}/_SEMANTIC.md`

Conditional write target:

- `{deliverable_folder}/_STATUS.md` only when both conditions are true:
  1. the brief/runtime override requires a status action; and
  2. TASK/brief write authorization allows `_STATUS.md` edits.

Normal PROJECT_SETUP Phase 2.3 uses `STATUS_POLICY=PRESERVE_CURRENT`; it may write only `_SEMANTIC.md` unless the brief explicitly authorizes a history note.

## Fallback rules

| Situation | Required fallback |
|---|---|
| Validator unavailable | Complete semantic audit manually; report validator unavailable. |
| `_CONTEXT.md` missing | Fail with `FAILED_INPUTS`. |
| Production document missing | Record as absent in Inputs Read; continue. |
| Status edit requested but unauthorized | Do not edit `_STATUS.md`; report the contradiction. |
| Tool output contradicts the file content | Report discrepancy; do not hide it. |
| Brief asks for out-of-scope writes | Refuse those writes and report scope violation. |
