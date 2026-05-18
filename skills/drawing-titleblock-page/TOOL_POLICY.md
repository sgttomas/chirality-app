# drawing-titleblock-page - Tool Policy

## Preferred tool order

Reasoning-first. The orchestrator prepares deterministic crops before dispatch. The skill reads only the provided images and writes one stub.

## Allowed deterministic tools

### TASK-enforced

- None. The skill has no `allowed-tools` frontmatter.

### Operationally invoked

- None. Crop preparation, validation, and assembly are orchestrator responsibilities.

## Expected use of reasoning

Use visual reasoning over the four corner crops and the full-page thumbnail to identify a titleblock and extract visible metadata. Leave unreadable values as `TBD`.

## Disallowed use

- No shell commands.
- No web access.
- No deterministic OCR invocation.
- No reading images outside the declared runtime overrides.
- No writing outside `OUTPUT_PATH`.

## Write boundary

The skill writes exactly one file: `RuntimeOverrides.OUTPUT_PATH`.
