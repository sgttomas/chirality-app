# lens-register — Tool Policy

## Preferred tool order

Reasoning-first generation, validator-last when available.

1. Read deliverable-local inputs inside `ScopePath` / `deliverable_folder`.
2. Generate `_SEMANTIC_LENSING.md` by reasoning over `_SEMANTIC.md` lenses and production documents.
3. Run optional validation tools when present and permitted by the TASK brief.
4. Report validator status honestly.

## Allowed deterministic tools

### TASK-enforced

No `allowed-tools` frontmatter is declared. TASK may still enforce an allowlist supplied by the brief.

### Operationally invoked

No deterministic tools are required for generation.

Optional validators / read-only checkers may be used when they exist in the repository and are permitted by the brief, especially:

- `python3 tools/validation/validate_lens_register.py {deliverable_folder}`
- `python3 tools/validation/validate_semantic_pipeline_scope.py {deliverable_folder} --step lens`

Do not claim validator PASS unless the validator actually ran and returned PASS. If the validator is unavailable or not allowed, report `Validator: NOT_RUN — <reason>`.

## Expected use of reasoning

This is an LLM-driven lensing-register skill. The agent reasons over:

- `_SEMANTIC.md` primary Result tables for matrices A, B, C, F, D, X, E;
- deliverable-local production documents;
- `_CONTEXT.md`, `_STATUS.md`, and `_REFERENCES.md` as local metadata only.

The skill treats matrix cells as lenses, not authorities. It records warranted gaps, conflicts, weak statements, normalization risks, and questions; it does not rewrite production documents.

`ProductionFormat=LEGACY_FOUR_DOC` selects the four legacy production files.
`ProductionFormat=SOW_V1` selects validated `ScopeOfWork.md`.
`ProductionFormat=MIGRATION_DUAL` requires exact accepted path authority and
selects the validated candidate plus legacy sources only for parity. SOW
targets use section and claim IDs; absent required authority fails closed.

## Disallowed use

- Do not modify production documents (`Datasheet.md`, `Specification.md`,
  `Guidance.md`, `Procedure.md`, or `ScopeOfWork.md`).
- Do not modify `_SEMANTIC.md`.
- Do not modify `_STATUS.md`; normal policy is `STATUS_POLICY=NO_STATUS_TOUCH`.
- Do not read, compare, or scan sibling deliverables.
- Do not follow external source paths from `_REFERENCES.md` during normal runs.
- Do not treat `_SEMANTIC.md` as engineering authority.
- Do not invent facts, numeric values, requirements, or acceptance claims.
- Do not claim validator PASS unless the validator actually ran.

## Write boundary

Skill-authored output:

- `{deliverable_folder}/_SEMANTIC_LENSING.md` only.

TASK shell output:

- `{deliverable_folder}/_run_records/TASK_RUN_*.md` may be created or updated by TASK. This is not a skill-authored output and is allowed when TASK executes the skill.

Read-only:

- `_SEMANTIC.md`
- `_STATUS.md`
- `_CONTEXT.md`
- `_REFERENCES.md`
- `_DEPENDENCIES.md` / `Dependencies.csv` if present
- all production documents

No other writes are allowed unless a future human-approved skill revision explicitly changes the contract.
