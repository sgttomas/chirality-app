# semantic-lensing — Tool Policy

## Preferred tool order
Reasoning-first: this workflow is LLM-driven; no deterministic tool ordering applies.

## Allowed deterministic tools

### Declared command restrictions
The optional execution.json contains declared command restrictions. Effective authorization also depends on the host, role, and brief; report the actual enforcement boundary.

- None — no additional command restriction

### Operationally invoked
_Tools named in `## Tool usage` body; operational guidance within effective permissions._

- None — no operational helpers declared (this is a reasoning-only workflow; no deterministic tools are required or allowed)

## Expected use of reasoning
This is a reasoning-only workflow. All phases are reasoning-driven: reading `_SEMANTIC.md` to understand the matrix structure and question framework, reading production documents under `RuntimeOverrides.DELIVERABLE_PATH`, reading `_SEMANTIC_LENSING.md` entries as candidate improvements (not evidence), and generating `PROPOSAL:` blocks with `Lens:` tags grounded in evidence from the production documents.

## Disallowed use
From WORKFLOW.md's "Disallowed behavior" section:
- no treating `_SEMANTIC.md` or `_SEMANTIC_LENSING.md` as evidence authority
- no inventing facts to fill lens-identified gaps — use `TBD`
- no widening scope beyond the single deliverable
- no edits to `_SEMANTIC.md` under any circumstances

No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.

## Write boundary
Per WORKFLOW.md's Outputs section:
- `PROPOSAL:` blocks with `Lens: <Matrix.Row.Column>` tags for each finding
- `MISSING:` items where lens-identified content gaps exist
- `NEEDS_HUMAN_RULING:` items where lensing surfaces contradictions
- optionally updated `_SEMANTIC_LENSING.md` (when `AllowLensLogUpdate: true` and the brief authorizes the write)
- optionally updated `_TRANSFERABLE_CONTEXT.md` (when `AllowTransferableContextUpdate: true` and the brief authorizes the write)
- optional `MEMORY.md` update only when explicitly authorized by the brief

`_SEMANTIC.md` is read-only and must never be modified. Writes are limited to the effective bounded task brief's authorization for the single deliverable under `RuntimeOverrides.DELIVERABLE_PATH`.
