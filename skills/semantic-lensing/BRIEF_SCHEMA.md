# BRIEF_SCHEMA — semantic-lensing

## Required fields

| Field | Source | Notes |
|---|---|---|
| `ScopePath` | Brief | Run/context anchor, normally the deliverable folder |
| `TaskSkill` | Brief | `semantic-lensing` |
| `RuntimeOverrides.DELIVERABLE_PATH` | Brief | Absolute path to the deliverable folder |

## Optional fields

| Field | Default | Notes |
|---|---|---|
| `UseSemanticLensing` | `true` | Compatibility flag accepted by existing dispatchers |
| `ActiveMatrices` | all | Comma-separated matrix letters (e.g., `A,B,F`) |
| `FocusLensTags` | all | Restrict to specific `Matrix.Row.Column` tags |
| `ApplyEdits` | `false` | Whether to apply authorized writes |
| `AllowLensLogUpdate` | `false` | Whether the brief intends to create/update `_SEMANTIC_LENSING.md`; also requires write authorization |
| `AllowTransferableContextUpdate` | `false` | Whether the brief intends to create/update `_TRANSFERABLE_CONTEXT.md`; also requires write authorization |

## Example brief

```markdown
PURPOSE: Apply semantic lensing analysis to identify gaps and inconsistencies
RequestedBy: WORKING_ITEMS
ScopePath: /path/to/DEL-02.01_Pipeline-Design-Basis
TaskSkill: semantic-lensing
UseSemanticLensing: true
ActiveMatrices: A,B,F
Tasks:
  - Analyze production documents through the lens framework
  - Surface gaps and weak statements
ApplyEdits: false
AllowLensLogUpdate: false
RuntimeOverrides:
  DELIVERABLE_PATH: /path/to/DEL-02.01_Pipeline-Design-Basis
```

## RuntimeOverrides example

```markdown
RuntimeOverrides:
  DELIVERABLE_PATH: /path/to/DEL-02.01_Pipeline-Design-Basis
  ActiveMatrices: A,B
  FocusLensTags: A.2.3,B.1.1
  LensDepth: shallow
```

If `AllowLensLogUpdate` or `AllowTransferableContextUpdate` is true, the brief must also set `ApplyEdits: true` and authorize the target file(s), either through `AllowedWriteTargets` or explicit writable-target text.
