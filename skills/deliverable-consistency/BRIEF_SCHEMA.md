# deliverable-consistency — Brief Schema

Use this skill with the deliverable profile like this:

```md
PURPOSE: Run a deliverable-local consistency sweep
RequestedBy: WORKING_ITEMS

DeliverablePath: /abs/path/to/DEL-XXX_Name
TaskProfile: DELIVERABLE_TASK
TaskSkill: deliverable-consistency

Tasks:
  - Review the four documents for contradictions and unresolved placeholders
  - Flag unsourced numeric parameters
  - Propose minimal edits only where clearly warranted

ApplyEdits: false

RuntimeOverrides:
  FocusDocs:
    - Datasheet.md
    - Specification.md
    - Guidance.md
    - Procedure.md
  Strictness: conservative
  MaxFindings: 12
  CheckIdentity: true
  CheckUnsourcedNumerics: true

AllowedTools:
  - tools/validation/scan_deliverable_consistency.py

EXCLUSIONS:
  - Procedure.md#Draft Notes
```

## Required fields

- `DeliverablePath`
- `TaskProfile: DELIVERABLE_TASK`
- `TaskSkill: deliverable-consistency`

## Typical tasks

- contradiction sweep
- unresolved `TBD` / `ASSUMPTION` / `CONFLICT:` marker review
- identity normalization proposals
- source/evidence completeness review

## Notes

- `ApplyEdits: false` is the normal safe default.
- Turn `ApplyEdits: true` on only when you want the task to apply minimal corrections directly.
