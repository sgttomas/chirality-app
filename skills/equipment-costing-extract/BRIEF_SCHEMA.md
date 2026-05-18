# equipment-costing-extract — Brief Schema

Use this skill with a generic TASK shell (no profile) like this:

```md
PURPOSE: Extract costing-relevant equipment specs from KTY-04-05
RequestedBy: WORKING_ITEMS

ScopePath: {DOMAIN_ROOT}
TaskSkill: equipment-costing-extract

AllowedWriteTargets:
  - "{DOMAIN_ROOT}/_Aggregation/Equipment_Extract/"

RuntimeOverrides:
  KTY_PATH: /abs/path/to/CAT-004_Process Description/1_Working/KTY-04-05_Inlet-Compressors
  OUTPUT_ROOT: /abs/path/to/_Aggregation/Equipment_Extract/
  EQUIPMENT_TYPES: "COMPRESSOR MODULE;SEPARATOR MODULE;STABILIZER MODULE;DEHYDRATION MODULE;FILTER COALESCER MODULE;ACCUMULATOR MODULE;EXPANSION TANK;FLARE KO DRUM MODULE;FLARE STACK;INSTRUMENT AIR MODULE;NEUTRAL GROUNDING RESISTOR;PROCESS PUMP MODULE;PROCESS HEAT MEDIUM HEATER MODULE;STORAGE TANK;VAPOUR RECOVERY UNIT MODULE"
  EQUIPMENT_EXTRACT_PATH: /abs/path/to/_Aggregation/Equipment_Extract/KTY-04-05_Equipment_Extract.md
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `ScopePath` | `{DOMAIN_ROOT}` | Top-level domain execution root |
| `TaskSkill` | `equipment-costing-extract` | Must match skill folder name |
| `AllowedWriteTargets` | `["{DOMAIN_ROOT}/_Aggregation/Equipment_Extract/"]` | Exactly this path |
| `RuntimeOverrides.KTY_PATH` | Absolute path to the KTY folder | Must contain `KA-*.md` files |
| `RuntimeOverrides.OUTPUT_ROOT` | `{DOMAIN_ROOT}/_Aggregation/Equipment_Extract/` | Must already exist |
| `RuntimeOverrides.EQUIPMENT_TYPES` | Semicolon-delimited target module type list | Matching is case-insensitive |

## Optional fields

| Field | Value | Notes |
|---|---|---|
| `RuntimeOverrides.EQUIPMENT_EXTRACT_PATH` | Absolute path to `{KTY_ID}_Equipment_Extract.md` | When provided, enriches `Subcomponents` column |

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile.

## Recommended CustomInstructions

For format-critical defense-in-depth, orchestrators SHOULD include:

```md
CustomInstructions:
  - "Output CSV must have exactly 17 columns: Equipment_Module_Type, Match_Quality, Equipment_Instance, Equipment_Tag, Quantity_and_Sparing, Description, Capacity_Throughput, Power_Duty, Size_Dimensions, Design_Pressure, Design_Temperature, Fluid_Process_Service, Subcomponents, Key_Costing_Parameters, Source_KTY, Source_KA_Files, Notes"
  - "One row per distinct equipment service (not per tag when identical units share a costing basis)"
  - "Quote fields containing commas or semicolons"
  - "Use TBD for values stated as pending in the source; leave blank for values not addressed"
```

## Read boundary

The skill reads only:

- `{KTY_PATH}/KA-*.md`
- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_REFERENCES.md`
- `{EQUIPMENT_EXTRACT_PATH}` (when provided)

It must NOT read arbitrary files under `ScopePath`.

## Write boundary

The skill writes only:

- `{OUTPUT_ROOT}/{KTY_ID}_Equipment_Costing_Extract.csv`

`OUTPUT_ROOT` must already exist. The skill does not create the directory.

## Notes

- `KTY_ID` is derived at runtime from `_CONTEXT.md` or from the folder name.
- One invocation processes one KTY folder. The orchestrator spawns one TASK per relevant KTY for parallelism.
- Equipment module type matching is case-insensitive. The output normalizes to the casing provided in `EQUIPMENT_TYPES`.
- KTYs with zero matches produce a header-only CSV with no data rows.
