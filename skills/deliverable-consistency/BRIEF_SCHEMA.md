# deliverable-consistency — Brief Schema

Use this skill with the generic TASK shell like this:

```md
PURPOSE: Run a deliverable-local consistency sweep
RequestedBy: WORKING_ITEMS

ScopePath: /abs/path/to/DEL-XXX_Name
TaskSkill: deliverable-consistency

Tasks:
  - Review the four documents for contradictions and unresolved placeholders
  - Flag unsourced numeric parameters
  - Propose minimal edits only where clearly warranted

ApplyEdits: false

RuntimeOverrides:
  DELIVERABLE_PATH: /abs/path/to/DEL-XXX_Name
  ProductionFormat: LEGACY_FOUR_DOC
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

- `ScopePath`
- `TaskSkill: deliverable-consistency`
- `RuntimeOverrides.DELIVERABLE_PATH`
- `RuntimeOverrides.ProductionFormat` — resolver-selected `LEGACY_FOUR_DOC`,
  `SOW_V1`, or authorized `MIGRATION_DUAL`; dual mode also requires
  `RuntimeOverrides.FormatAuthorityRef`.

## Typical tasks

- contradiction sweep
- unresolved `TBD` / `ASSUMPTION` / `CONFLICT:` marker review
- identity normalization proposals
- source/evidence completeness review

## Notes

- `ApplyEdits: false` is the normal safe default.
- Turn `ApplyEdits: true` on only when you want the task to apply minimal corrections directly, and provide either `AllowedWriteTargets` or explicit writable targets in the brief.
