# proposal-format — Tool Policy

## Preferred tool order

Reasoning-first: this skill is LLM-driven; no deterministic tool ordering applies. When combined with other skills that use deterministic tools (e.g., deliverable-consistency), the other tool's output provides the evidence base; this skill provides the output structure.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist.

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no operational helpers declared (this is a reasoning-only skill).

## Expected use of reasoning

This is a reasoning-only skill. All phases — evidence gathering, PROPOSAL block authoring, status assignment, grouping, baseline scan, and the MISSING / NEEDS_HUMAN_RULING / DEPENDENCY_NOTES decision interface — are performed by direct LLM reasoning against deliverable-local content under `RuntimeOverrides.DELIVERABLE_PATH`. No deterministic tools are required.

## Disallowed use

- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.
- No inventing evidence to justify a proposal.
- No widening scope beyond the single deliverable.
- No edits outside the effective bounded task brief's write authorization.
- No silent conflict resolution — contradictions go in `NEEDS_HUMAN_RULING`.

## Write boundary

Writes are limited to the effective bounded task brief's write authorization for the single deliverable under `RuntimeOverrides.DELIVERABLE_PATH`. Optional applied edits require `ApplyEdits: true`; `MEMORY.md` updates require explicit brief authorization.
