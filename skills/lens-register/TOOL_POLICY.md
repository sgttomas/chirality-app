# lens-register — Tool Policy

## Preferred tool order

Reasoning-first: this skill is LLM-driven; no deterministic tool ordering applies.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted).

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no operational helpers declared. SKILL.md states "Preferred tools: none (reasoning-first extraction)".

## Expected use of reasoning

This is a reasoning-only skill. No deterministic tools are required or allowed. All Protocol steps (Step 0 safety checks, Step 1 context + inputs read, Step 2 matrix parsing into a lens inventory, Step 3 applying lenses to production documents and recording warranted items, Step 4 writing the register, Step 5 completion report) are LLM-driven. The skill reasons over `_SEMANTIC.md` matrices (A, B, C, F, D, X, E) as lenses and scans the production documents to record warranted items with provenance.

## Disallowed use

- No writing to any file outside `{deliverable_folder}/_SEMANTIC_LENSING.md`.
- No modification of production documents (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`).
- No modification of `_SEMANTIC.md` under any circumstances.
- No cross-deliverable scanning or comparison.
- No modification of `_STATUS.md` (unless orchestrator later adds a lifecycle state for lensing).
- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary

- Write scope: `{deliverable_folder}/_SEMANTIC_LENSING.md` only (overwritten each run).
- One deliverable per run; operate on a single deliverable folder only.
- Read-only on production documents (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) and on `_SEMANTIC.md`.
