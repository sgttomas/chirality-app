# BRIEF_SCHEMA — semantic-lensing

## Required fields

| Field | Source | Notes |
|---|---|---|
| `DeliverablePath` | Brief | Absolute path to the deliverable folder |
| `UseSemanticLensing` | Brief | Must be `true` — DELIVERABLE_TASK will not activate lensing otherwise |
| `TaskSkill` | Brief | `semantic-lensing` |

## Optional fields

| Field | Default | Notes |
|---|---|---|
| `ActiveMatrices` | all | Comma-separated matrix letters (e.g., `A,B,F`) |
| `FocusLensTags` | all | Restrict to specific `Matrix.Row.Column` tags |
| `ApplyEdits` | `false` | Whether to apply proposed changes to production docs |
| `AllowLensLogUpdate` | `false` | Whether to create/update `_SEMANTIC_LENSING.md` |
| `AllowTransferableContextUpdate` | `false` | Whether to create/update `_TRANSFERABLE_CONTEXT.md` |

## Example brief

```markdown
PURPOSE: Apply semantic lensing analysis to identify gaps and inconsistencies
RequestedBy: WORKING_ITEMS
DeliverablePath: /path/to/DEL-02.01_Pipeline-Design-Basis
TaskSkill: semantic-lensing
UseSemanticLensing: true
ActiveMatrices: A,B,F
Tasks:
  - Analyze production documents through the lens framework
  - Surface gaps and weak statements
ApplyEdits: false
AllowLensLogUpdate: true
```

## RuntimeOverrides example

```markdown
RuntimeOverrides:
  ActiveMatrices: A,B
  FocusLensTags: A.2.3,B.1.1
  LensDepth: shallow
```
