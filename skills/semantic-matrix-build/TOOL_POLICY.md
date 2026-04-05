# semantic-matrix-build — Tool Policy

## Preferred tool order
Reasoning-first: this skill is LLM-driven; no deterministic tool ordering applies.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted)

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no operational helpers declared (this is a reasoning-first semantic-algebra skill)

## Expected use of reasoning
This is a reasoning-first semantic-algebra skill. All phases are reasoning-driven: reading deliverable context (`_CONTEXT.md`, `_STATUS.md`, production documents), deriving the deliverable perspective statement, adopting canonical Matrix A and Matrix B values, deriving matrices C, F, D, K, G, X, T, and E via semantic algebra (with every list-valued cell showing the three-step `I(r,c,L)` interpretation operator: axis anchor, projections, centroid), auditing final cell values, writing `_SEMANTIC.md`, and updating `_STATUS.md` readiness state per audit result.

## Disallowed use
From SKILL.md's Non-negotiable constraints and "Skill Does / Does Not" table:
- Do not edit production documents (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`, or for DOMAIN variants any `KA-*.md` or `Scoping.md`)
- Do not specify project particulars (numbers, tags, exact code clauses)
- Do not skip steps or handwave interpretation
- Do not write outside the deliverable folder
- Do not regress lifecycle state or skip ahead
- Do not pretend missing inputs were present or claim PASS when audit failed
- Do not silently reconcile conflicts — surface as contradictions and request human resolution
- No cross-deliverable scanning (one deliverable per run)

No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary
Deliverable-local. May write/overwrite only:
- `{deliverable_folder}/_SEMANTIC.md` (primary output; overwritten each run; includes audit result)
- `{deliverable_folder}/_STATUS.md` to record readiness (deliverable-local only):
  - On audit **PASS**: ensure state = `SEMANTIC_READY` and append History.
  - On audit **FAIL**: do **not** advance state; append failure History.

Read-only on all production documents.
