# decomposition-package-review — Tool Policy

## Preferred tool order

Reasoning-first:

1. read `_Decomposition/`
2. resolve the active `_ScopeChange` snapshot from `_LATEST.md`
3. enumerate package-local derivative surfaces
4. build the parity matrix and classify findings
5. in `REVIEW_AND_REPAIR` mode only, apply explicitly authorized,
   mechanically derivable package-local repairs
6. write the report and optional structured outputs

## Allowed deterministic tools

### Declared command restrictions
The optional execution.json contains declared command restrictions. Effective authorization also depends on the host, role, and brief; report the actual enforcement boundary.

- None — no additional command restriction (the `allowed-tools`
  frontmatter field is intentionally omitted)

### Operationally invoked
_Tools named in `## Tool usage` body; operational guidance within effective permissions._

- None — no deterministic helpers declared

## Expected use of reasoning

This workflow is a bounded package-level review. Reasoning governs:

- which local surfaces count as duplicated package truth
- whether a finding belongs to package repair, snapshot repair, rerun, or human
  escalation
- whether a repair is genuinely mechanical and authorized
- whether handoff-state claims are supported by actual package evidence

## Disallowed use

- No KTY-local reads or writes outside what the brief explicitly authorizes for
  package review artifacts.
- No use as a substitute for cross-root conformity review.
- No repairs to hypergraph, audit, or publication outputs.
- No silent synthesis of missing snapshot artifacts.
- No repair when the authority basis is ambiguous.

## Write boundary

Writes are limited to:

- `{REVIEW_OUTPUT_PATH}`
- optional `{FINDINGS_CSV_PATH}`
- optional `{PARITY_MATRIX_PATH}`
- explicit package-local repair targets under `_Decomposition/` or
  `_ScopeChange/` when `MODE = REVIEW_AND_REPAIR`

No other files may be created or modified by this workflow.
