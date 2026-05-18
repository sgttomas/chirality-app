# TOOL POLICY — content-digest

## Preferred tool order

1. Read the bounded deliverable-local files listed in the skill contract.
2. Use direct reasoning to extract and summarize structured information into the seven-section digest.

## Allowed deterministic tools

### TASK-enforced

None. The `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked

None.

## Expected use of reasoning

This skill performs bounded extraction and summarization only. It should identify specific quality-observation signals from the deliverable-local files without crossing into engineering judgment or cross-deliverable synthesis.

## Disallowed use

- No writes outside `OUTPUT_PATH`.
- No modification of any file in `DELIVERABLE_PATH`.
- No reading files outside the specified deliverable folder.
- No cross-deliverable scanning or comparison.

## Write boundary

The skill may write exactly one file at `RuntimeOverrides.OUTPUT_PATH`.
