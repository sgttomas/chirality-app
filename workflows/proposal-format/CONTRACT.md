# proposal-format contract

## Brief

### Required fields

| Field | Source | Notes |
|---|---|---|
| `ScopePath` | Brief | Run/context anchor, normally the deliverable folder |
| `Workflow` | Brief | `proposal-format` |
| `RuntimeOverrides.DELIVERABLE_PATH` | Brief | Absolute path to the deliverable folder |
| `RuntimeOverrides.ProductionFormat` | Brief | resolver-selected `LEGACY_FOUR_DOC`, `SOW_V1`, or authorized `MIGRATION_DUAL` |

### Optional fields

| Field | Default | Notes |
|---|---|---|
| `Tasks` | (baseline scan) | Specific asks; if omitted, workflow runs baseline assessment |
| `ApplyEdits` | `false` | Whether to apply proposed changes; edits require explicit brief write authorization |
| `UseSemanticLensing` | `false` | Whether to include `Lens:` tags |
| `RuntimeOverrides.MaxProposals` | `10` | Soft cap on proposals |
| `RuntimeOverrides.FocusDocs` | all | Restrict to named docs |
| `RuntimeOverrides.ProposalDepth` | `full` | `summary` or `full` |
| `RuntimeOverrides.IncludeLensTags` | `false` | Lens tags without full lensing |
| `RuntimeOverrides.FormatAuthorityRef` | empty | Required only for authorized `MIGRATION_DUAL` |

### Example brief (targeted)

```markdown
PURPOSE: Review Specification.md for verification gaps
RequestedBy: WORKING_ITEMS
ScopePath: /path/to/DEL-02.01_Pipeline-Design-Basis
Workflow: proposal-format
Tasks:
  - Identify requirements without verification methods
  - Propose verification approaches for unmatched requirements
ApplyEdits: false
RuntimeOverrides:
  DELIVERABLE_PATH: /path/to/DEL-02.01_Pipeline-Design-Basis
  FocusDocs: Specification.md
  MaxProposals: 5
```

### Example brief (baseline scan)

```markdown
PURPOSE: Baseline assessment of deliverable quality
RequestedBy: WORKING_ITEMS
ScopePath: /path/to/DEL-08.01_Steam-line
Workflow: proposal-format
ApplyEdits: false
RuntimeOverrides:
  DELIVERABLE_PATH: /path/to/DEL-08.01_Steam-line
```

## Acceptance

### Minimum output validity

| Check | Validation |
|---|---|
| PROPOSAL blocks complete | Every block contains Evidence, Change, Why, Risk, Status |
| Evidence grounded | Evidence cites file + section/heading (or `location TBD`) |
| Change specific | Change descriptions are actionable without further interpretation |
| Status correct | PROPOSED (default), APPLIED (only when edit was made), NEEDS_HUMAN_RULING (contradictions/trade-offs) |
| No unsupported proposals | No proposal lacks evidence |
| Decision interface present | MISSING, NEEDS_HUMAN_RULING, DEPENDENCY_NOTES sections all present (may be `none`) |
| Scope respected | All proposals reference content within the single deliverable |

### Failure reporting

- If no production documents exist: report in `MISSING`
- If no meaningful issues are found: state this explicitly — do not pad output
- If `Tasks` specified work that could not be completed: report in `MISSING` with reason

### Baseline scan checks (when Tasks omitted)

- At least one category of proposals was assessed (completeness, consistency, verification, source fidelity, or identity)
- TBD items are reported separately from proposals
- Dependency notes are reported when cross-deliverable interfaces are visible

## Tool use

### Preferred tool order

Reasoning-first: this workflow is LLM-driven; no deterministic tool ordering applies. When combined with other workflows that use deterministic tools (e.g., deliverable-consistency), the other tool's output provides the evidence base; this workflow provides the output structure.

### Allowed deterministic tools

#### Operationally invoked

- None — no operational helpers declared (this is a reasoning-only workflow).

### Expected use of reasoning

This is a reasoning-only workflow. All phases — evidence gathering, PROPOSAL block authoring, status assignment, grouping, baseline scan, and the MISSING / NEEDS_HUMAN_RULING / DEPENDENCY_NOTES decision interface — are performed by direct LLM reasoning against deliverable-local content under `RuntimeOverrides.DELIVERABLE_PATH`. No deterministic tools are required.

### Disallowed use

- No hidden reliance on tools outside the declared list unless the human expands AllowedTools. No writes outside declared scope.
- No inventing evidence to justify a proposal.
- No widening scope beyond the single deliverable.
- No edits outside the effective bounded task brief's write authorization.
- No silent conflict resolution — contradictions go in `NEEDS_HUMAN_RULING`.

### Write boundary

Writes are limited to the effective bounded task brief's write authorization for the single deliverable under `RuntimeOverrides.DELIVERABLE_PATH`. Optional applied edits require `ApplyEdits: true`; `MEMORY.md` updates require explicit brief authorization.
