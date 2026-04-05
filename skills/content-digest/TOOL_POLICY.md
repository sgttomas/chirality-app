# content-digest — Tool Policy

## Preferred tool order
Reasoning-first: this skill is LLM-driven; no deterministic tool ordering applies.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted)

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no operational helpers declared (this is a reasoning-first, semantic-matching extraction skill)

## Expected use of reasoning
This is a reasoning-first, semantic-matching extraction skill. All phases are reasoning-only: reading the deliverable-local files within the declared Read boundary, extracting structured information from document patterns (Identity, Scope, Document Kit Summary, Dependencies, References, Semantic, Quality Observations), and writing a single digest per run. Semantic matching, not deep reasoning or engineering judgment, drives extraction; evaluative scoring is out of scope.

## Disallowed use
From SKILL.md's "Disallowed behavior" section:
- No writing outside `OUTPUT_PATH`
- No modification of any file in `DELIVERABLE_PATH`
- No reading files outside the specified deliverable folder
- No cross-deliverable scanning or comparison

No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary
Writes are limited to `{RuntimeOverrides.OUTPUT_PATH}` — exactly one file per run. The parent directory of `OUTPUT_PATH` must already exist; the skill does not create the directory. `AllowedWriteTargets` is `["{EXECUTION_ROOT}/_Evaluation/content-digests/"]`.
