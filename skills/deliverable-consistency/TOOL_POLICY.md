# deliverable-consistency — Tool Policy

## Preferred tool order

This skill is tool-first for the initial sweep, then reasoning-first for adjudication.

1. run `tools/validation/scan_deliverable_consistency.py` against the deliverable
2. read the flagged production docs and nearby context from `RuntimeOverrides.DELIVERABLE_PATH`
3. compare files directly where the scan surfaces a plausible inconsistency
4. emit evidence-backed proposals
5. apply minimal edits only if authorized

Normal invocation shape:

```sh
python3 tools/validation/scan_deliverable_consistency.py "$DELIVERABLE_PATH"
```

Use the optional flags only when the brief calls for them: `--focus-doc`, `--strictness`, `--max-findings`, `--check-identity`, `--check-unsourced-numerics`.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- `python3 tools/validation/scan_deliverable_consistency.py:*`

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no additional operational helpers declared beyond the TASK-enforced scanner.

## Expected use of reasoning

The tool is a first-pass detector, not a final judge:
- unresolved markers are deterministic findings
- identity mismatches are candidate inconsistencies until checked in context
- unsourced numeric lines are review prompts, not automatic defects

Reasoning takes over after the deterministic sweep: the agent reads flagged production docs and nearby context, compares files directly where the scan cannot decide, and produces evidence-backed PROPOSAL blocks and human-ruling items.

## Disallowed use

- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.
- no project-wide scanning
- no widening scope beyond the single deliverable
- no edits outside the effective bounded task brief's write authorization
- no silent conflict resolution
- no dependency register edits unless separately authorized by the brief

## Write boundary

Writes are limited to the effective bounded task brief's write authorization for the single deliverable under `RuntimeOverrides.DELIVERABLE_PATH`. Optional applied minimal edits require `ApplyEdits: true`. `MEMORY.md` updates and dependency register edits require explicit brief authorization.
