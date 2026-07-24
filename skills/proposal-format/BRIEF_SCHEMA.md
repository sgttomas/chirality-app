# BRIEF_SCHEMA — proposal-format

## Required fields

| Field | Source | Notes |
|---|---|---|
| `ScopePath` | Brief | Run/context anchor, normally the deliverable folder |
| `TaskSkill` | Brief | `proposal-format` |
| `RuntimeOverrides.DELIVERABLE_PATH` | Brief | Absolute path to the deliverable folder |
| `RuntimeOverrides.ProductionFormat` | Brief | resolver-selected `LEGACY_FOUR_DOC`, `SOW_V1`, or authorized `MIGRATION_DUAL` |

## Optional fields

| Field | Default | Notes |
|---|---|---|
| `Tasks` | (baseline scan) | Specific asks; if omitted, skill runs baseline assessment |
| `ApplyEdits` | `false` | Whether to apply proposed changes; edits require explicit brief write authorization |
| `UseSemanticLensing` | `false` | Whether to include `Lens:` tags |
| `RuntimeOverrides.MaxProposals` | `10` | Soft cap on proposals |
| `RuntimeOverrides.FocusDocs` | all | Restrict to named docs |
| `RuntimeOverrides.ProposalDepth` | `full` | `summary` or `full` |
| `RuntimeOverrides.IncludeLensTags` | `false` | Lens tags without full lensing |
| `RuntimeOverrides.FormatAuthorityRef` | empty | Required only for authorized `MIGRATION_DUAL` |

## Example brief (targeted)

```markdown
PURPOSE: Review Specification.md for verification gaps
RequestedBy: WORKING_ITEMS
ScopePath: /path/to/DEL-02.01_Pipeline-Design-Basis
TaskSkill: proposal-format
Tasks:
  - Identify requirements without verification methods
  - Propose verification approaches for unmatched requirements
ApplyEdits: false
RuntimeOverrides:
  DELIVERABLE_PATH: /path/to/DEL-02.01_Pipeline-Design-Basis
  FocusDocs: Specification.md
  MaxProposals: 5
```

## Example brief (baseline scan)

```markdown
PURPOSE: Baseline assessment of deliverable quality
RequestedBy: WORKING_ITEMS
ScopePath: /path/to/DEL-08.01_Steam-line
TaskSkill: proposal-format
ApplyEdits: false
RuntimeOverrides:
  DELIVERABLE_PATH: /path/to/DEL-08.01_Steam-line
```
