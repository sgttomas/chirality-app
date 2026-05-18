# equipment-costing-extract — Tool Policy

## Preferred tool order

Reasoning-first: this skill is LLM-driven; no deterministic tool ordering applies during extraction. The agent reads KA markdown files within a single Knowledge Type folder and applies matching and extraction logic directly, producing a per-KTY CSV with costing-relevant design parameters.

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- None — no TASK-enforced deterministic allowlist (the `allowed-tools` frontmatter field is intentionally omitted)

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None — no operational helpers declared during extraction (SKILL.md states: "No deterministic tools during extraction. This is a reasoning-first skill.")

**Downstream note:** The orchestrator (not this skill) invokes `tools/reporting/merge_equipment_costing_csv.py` after all per-KTY extractions complete. This tool is not part of the skill's execution scope.

## Expected use of reasoning

This is a reasoning-first extraction skill. The agent:

1. Reads `_CONTEXT.md` and `_REFERENCES.md` for KTY identity and source context.
2. Reads all `KA-*.md` files in the KTY folder in order.
3. Applies matching logic to identify equipment items corresponding to target module types from `EQUIPMENT_TYPES`.
4. Extracts costing-relevant parameters (capacity, power/duty, size, design pressure, temperature, fluid service, subcomponents, key costing parameters) from markdown tables and prose.
5. Optionally reads an existing `Equipment_Extract.md` for subcomponent enrichment.
6. Assembles and writes the per-KTY CSV output.

Reasoning governs every phase: preconditions, context read, KA enumeration, equipment matching, parameter extraction, CSV composition, and output file writing.

## Disallowed use

- No writing outside `OUTPUT_ROOT`.
- No modification of any file in `KTY_PATH`.
- No widening scope beyond the designated KTY folder (plus optional Equipment_Extract.md).
- No hidden reliance on tools outside the declared list.
- No invention of parameter values not stated in KA source text.

## Write boundary

Writes are limited to:

- `{RuntimeOverrides.OUTPUT_ROOT}/{KTY_ID}_Equipment_Costing_Extract.csv`

`OUTPUT_ROOT` must already exist. The skill does not create the directory. No files in `{KTY_PATH}` may be written or modified.
