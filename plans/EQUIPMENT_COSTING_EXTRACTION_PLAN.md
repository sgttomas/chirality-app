# Equipment Costing Extraction — Reproducible Orchestration Plan

## Purpose

This plan documents the reproducible workflow for extracting equipment costing data from a Chirality DBM domain using the `equipment-costing-extract` skill. It is designed to be executed by WORKING_ITEMS (Type 1) and reused across multiple domains.

## Prerequisites

1. The domain must have populated KTY folders with KA files under `CAT-*/1_Working/KTY-*-*/`
2. `_Aggregation/Equipment_Extract/` must exist with per-KTY `{KTY_ID}_Equipment_Extract.md` files (produced by the `equipment-extract` skill)
3. The `equipment-costing-extract` skill must exist under `skills/`
4. The merge tool `tools/reporting/merge_equipment_costing_csv.py` must exist

## Parameters (set per domain)

| Parameter | Description | Example (West Doe Comp & Liquids) |
|---|---|---|
| `DOMAIN_ROOT` | Absolute path to domain root | `domain-test/domains/West_Doe_Comp_and_Liquids_DBM/` |
| `EQUIPMENT_TYPES` | Semicolon-delimited target module types | See below |
| `TARGET_KTYS` | List of KTY folders containing equipment to extract | See below |

### Default equipment module type list

```
COMPRESSOR MODULE;SEPARATOR MODULE;STABILIZER MODULE;DEHYDRATION MODULE;FILTER COALESCER MODULE;ACCUMULATOR MODULE;EXPANSION TANK;FLARE KO DRUM MODULE;FLARE STACK;INSTRUMENT AIR MODULE;NEUTRAL GROUNDING RESISTOR;PROCESS PUMP MODULE;PROCESS HEAT MEDIUM HEATER MODULE;STORAGE TANK;VAPOUR RECOVERY UNIT MODULE
```

### Target KTY identification

Identify KTY folders that contain equipment relevant to the target module types. For a typical compression and liquids facility:

| KTY | Equipment Types | Est. KA Count |
|---|---|---|
| KTY-04-02 | SEPARATOR MODULE | 5 |
| KTY-04-03 | STABILIZER MODULE, SEPARATOR MODULE (flash feed) | 10 |
| KTY-04-04 | COMPRESSOR MODULE (SOC) | 4 |
| KTY-04-05 | COMPRESSOR MODULE (Inlet) | 3 |
| KTY-04-06 | DEHYDRATION MODULE (TEG), FILTER COALESCER MODULE | 14 |
| KTY-04-10 | DEHYDRATION MODULE (C5+), ACCUMULATOR MODULE | 6 |
| KTY-04-11 | STORAGE TANK, PROCESS PUMP MODULE | 12 |
| KTY-04-12 | PROCESS PUMP MODULE (truck loading) | 1 |
| KTY-04-13 | STORAGE TANK, PROCESS PUMP MODULE (produced water) | 1 |
| KTY-04-14 | VAPOUR RECOVERY UNIT MODULE | 5 |
| KTY-05-02 | INSTRUMENT AIR MODULE | 2 |
| KTY-05-03 | EXPANSION TANK, PROCESS HEAT MEDIUM HEATER MODULE, PROCESS PUMP MODULE | 5 |
| KTY-05-05 | FLARE KO DRUM MODULE, FLARE STACK | 2 |
| KTY-05-06 | STORAGE TANK (lube oil) | 1 |
| KTY-12-06 | NEUTRAL GROUNDING RESISTOR | 1 |

## Execution Workflow

### Step 1 — Identify target KTYs

Scan the domain's CAT folders for KTY directories that may contain equipment matching the target types. Use the Equipment_Extract.md files and KTY names to filter.

### Step 2 — Dispatch per-KTY TASK agents

Dispatch one Sonnet subagent per KTY. Organize into **8 balanced batches** for parallel execution.

**Batch balancing principle:** Group KTYs so each batch has roughly equal total KA file count. Heavy KTYs (10+ KAs) get their own batch; light KTYs (1-2 KAs) are grouped together.

**Per-KTY dispatch brief:**

```markdown
PURPOSE: Extract costing-relevant equipment specs from {KTY_ID}
RequestedBy: WORKING_ITEMS

ScopePath: {DOMAIN_ROOT}
TaskSkill: equipment-costing-extract

AllowedWriteTargets:
  - "{DOMAIN_ROOT}/_Aggregation/Equipment_Extract/"

RuntimeOverrides:
  KTY_PATH: {DOMAIN_ROOT}/{CAT_PATH}/1_Working/{KTY_FOLDER}/
  OUTPUT_ROOT: {DOMAIN_ROOT}/_Aggregation/Equipment_Extract/
  EQUIPMENT_TYPES: "{EQUIPMENT_TYPES}"
  EQUIPMENT_EXTRACT_PATH: {DOMAIN_ROOT}/_Aggregation/Equipment_Extract/{KTY_ID}_Equipment_Extract.md

CustomInstructions:
  - "Output CSV must have exactly 17 columns: Equipment_Module_Type, Match_Quality, Equipment_Instance, Equipment_Tag, Quantity_and_Sparing, Description, Capacity_Throughput, Power_Duty, Size_Dimensions, Design_Pressure, Design_Temperature, Fluid_Process_Service, Subcomponents, Key_Costing_Parameters, Source_KTY, Source_KA_Files, Notes"
  - "One row per distinct equipment service (not per tag when identical units share a costing basis)"
  - "Quote fields containing commas or semicolons"
  - "Use TBD for values stated as pending in the source; leave blank for values not addressed"

ExpectedOutputs:
  - "{KTY_ID}_Equipment_Costing_Extract.csv"
```

### Step 3 — Merge per-KTY outputs

After all TASK agents return, run the deterministic merge tool:

```sh
python3 tools/reporting/merge_equipment_costing_csv.py \
  {DOMAIN_ROOT}/_Aggregation/Equipment_Extract/Equipment_Costing_Extract.csv \
  {DOMAIN_ROOT}/_Aggregation/Equipment_Extract/ \
  --sort-by Equipment_Module_Type
```

### Step 4 — Validate

1. Confirm all 15 equipment types have at least one row (or are documented as Out_of_Scope)
2. Spot-check 3-4 rows against source KA files
3. Verify CSV schema (17 columns, proper quoting)

## Dispatch patterns

### Canonical TASK dispatch (future)
When the orchestrator can invoke TASK with `TaskSkill: equipment-costing-extract`, TASK auto-loads the skill contract and companion files. The orchestrator provides only runtime parameters via `RuntimeOverrides`.

### Claude Code dispatch (current)
When dispatching via Claude Code Agent tool, the orchestrator must include the skill contract context in the agent prompt since TASK skill hydration does not occur. The agent reads `SKILL.md` directly as its first step. This produces equivalent results but the skill contract is "reconstructed" in the dispatch prompt rather than auto-loaded.

### Post-run review findings (v1 lessons learned)
From the first execution on West Doe Comp & Liquids:
- Out_of_Scope rows were produced with blank Description — skill updated to require scope exclusion note
- Multi-tag format varied between agents (comma vs slash) — skill updated to specify comma-space delimiter
- Equipment_Extract.md tags were not used when KA text lacked tags — skill updated to accept Equipment_Extract.md as valid tag source
- Row granularity rule (merge vs split identical units) was not explicit — skill updated with merge/split criteria

## Adaptation for new domains

To run on a different domain (e.g., West Doe Deepcut DBM):

1. Update `DOMAIN_ROOT` to the new domain path
2. Re-identify target KTYs (the KTY numbering/naming may differ)
3. Adjust `EQUIPMENT_TYPES` if the facility has different equipment categories
4. Re-run the same workflow
