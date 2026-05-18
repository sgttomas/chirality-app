# pandid-valve-tile - Tool Policy

## Preferred tool order

Reasoning-first. Deterministic tile preparation happens before dispatch. The skill reads one prepared tile image and writes one stub.

## Allowed deterministic tools

### TASK-enforced

- None. The skill has no `allowed-tools` frontmatter.

### Operationally invoked

- None. All deterministic operations are orchestrator/tool responsibilities.

## Expected use of reasoning

Use visual reasoning over the tile image to identify valve candidates, respect the emit-zone contract, and classify candidate fields according to the active mode.

## Disallowed use

- No shell commands.
- No web access.
- No deterministic OCR invocation.
- No reading images outside the declared tile input.
- No writing outside `OUTPUT_PATH`.
- No sub-agent fanout.

## Write boundary

The skill writes exactly one file: `RuntimeOverrides.OUTPUT_PATH`.
