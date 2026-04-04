# BRIEF_SCHEMA — proposal-format

## Required fields

| Field | Source | Notes |
|---|---|---|
| `DeliverablePath` | Brief | Absolute path to the deliverable folder |
| `TaskSkill` | Brief | `proposal-format` |

## Optional fields

| Field | Default | Notes |
|---|---|---|
| `Tasks` | (baseline scan) | Specific asks; if omitted, skill runs baseline assessment |
| `ApplyEdits` | `false` | Whether to apply proposed changes |
| `UseSemanticLensing` | `false` | Whether to include `Lens:` tags |
| `RuntimeOverrides.MaxProposals` | `10` | Soft cap on proposals |
| `RuntimeOverrides.FocusDocs` | all | Restrict to named docs |
| `RuntimeOverrides.ProposalDepth` | `full` | `summary` or `full` |
| `RuntimeOverrides.IncludeLensTags` | `false` | Lens tags without full lensing |

## Example brief (targeted)

```markdown
PURPOSE: Review Specification.md for verification gaps
RequestedBy: WORKING_ITEMS
DeliverablePath: /path/to/DEL-02.01_Pipeline-Design-Basis
TaskSkill: proposal-format
Tasks:
  - Identify requirements without verification methods
  - Propose verification approaches for unmatched requirements
ApplyEdits: false
RuntimeOverrides:
  FocusDocs: Specification.md
  MaxProposals: 5
```

## Example brief (baseline scan)

```markdown
PURPOSE: Baseline assessment of deliverable quality
RequestedBy: WORKING_ITEMS
DeliverablePath: /path/to/DEL-08.01_Steam-line
TaskSkill: proposal-format
ApplyEdits: false
```
