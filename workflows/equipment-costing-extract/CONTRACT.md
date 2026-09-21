# equipment-costing-extract contract

## Brief

Use this workflow with a generic TASK shell (no profile) like this:

```md
PURPOSE: Extract costing-relevant equipment specs from KTY-04-05
RequestedBy: WORKING_ITEMS

ScopePath: {DOMAIN_ROOT}
Workflow: equipment-costing-extract

AllowedWriteTargets:
  - "{DOMAIN_ROOT}/_Aggregation/Equipment_Extract/"

RuntimeOverrides:
  KTY_PATH: /abs/path/to/CAT-004_Process Description/1_Working/KTY-04-05_Inlet-Compressors
  OUTPUT_ROOT: /abs/path/to/_Aggregation/Equipment_Extract/
  EQUIPMENT_TYPES: "COMPRESSOR MODULE;SEPARATOR MODULE;STABILIZER MODULE;DEHYDRATION MODULE;FILTER COALESCER MODULE;ACCUMULATOR MODULE;EXPANSION TANK;FLARE KO DRUM MODULE;FLARE STACK;INSTRUMENT AIR MODULE;NEUTRAL GROUNDING RESISTOR;PROCESS PUMP MODULE;PROCESS HEAT MEDIUM HEATER MODULE;STORAGE TANK;VAPOUR RECOVERY UNIT MODULE"
  EQUIPMENT_EXTRACT_PATH: /abs/path/to/_Aggregation/Equipment_Extract/KTY-04-05_Equipment_Extract.md
```

### Required fields

| Field | Value | Notes |
|---|---|---|
| `ScopePath` | `{DOMAIN_ROOT}` | Top-level domain execution root |
| `Workflow` | `equipment-costing-extract` | Must match workflow folder name |
| `AllowedWriteTargets` | `["{DOMAIN_ROOT}/_Aggregation/Equipment_Extract/"]` | Exactly this path |
| `RuntimeOverrides.KTY_PATH` | Absolute path to the KTY folder | Must contain `KA-*.md` files |
| `RuntimeOverrides.OUTPUT_ROOT` | `{DOMAIN_ROOT}/_Aggregation/Equipment_Extract/` | Must already exist |
| `RuntimeOverrides.EQUIPMENT_TYPES` | Semicolon-delimited target module type list | Matching is case-insensitive |

### Optional fields

| Field | Value | Notes |
|---|---|---|
| `RuntimeOverrides.EQUIPMENT_EXTRACT_PATH` | Absolute path to `{KTY_ID}_Equipment_Extract.md` | When provided, enriches `Subcomponents` column |

### Recommended CustomInstructions

For format-critical defense-in-depth, orchestrators SHOULD include:

```md
CustomInstructions:
  - "Output CSV must have exactly 17 columns: Equipment_Module_Type, Match_Quality, Equipment_Instance, Equipment_Tag, Quantity_and_Sparing, Description, Capacity_Throughput, Power_Duty, Size_Dimensions, Design_Pressure, Design_Temperature, Fluid_Process_Service, Subcomponents, Key_Costing_Parameters, Source_KTY, Source_KA_Files, Notes"
  - "One row per distinct equipment service (not per tag when identical units share a costing basis)"
  - "Quote fields containing commas or semicolons"
  - "Use TBD for values stated as pending in the source; leave blank for values not addressed"
```

### Read boundary

The workflow reads only:

- `{KTY_PATH}/KA-*.md`
- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_REFERENCES.md`
- `{EQUIPMENT_EXTRACT_PATH}` (when provided)

It must NOT read arbitrary files under `ScopePath`.

### Write boundary

The workflow writes only:

- `{OUTPUT_ROOT}/{KTY_ID}_Equipment_Costing_Extract.csv`

`OUTPUT_ROOT` must already exist. The workflow does not create the directory.

### Notes

- `KTY_ID` is derived at runtime from `_CONTEXT.md` or from the folder name.
- One invocation processes one KTY folder. The orchestrator spawns one TASK per relevant KTY for parallelism.
- Equipment module type matching is case-insensitive. The output normalizes to the casing provided in `EQUIPMENT_TYPES`.
- KTYs with zero matches produce a header-only CSV with no data rows.

## Acceptance

Minimum checks for a valid run:

1. `KTY_PATH` exists and contains at least one `KA-*.md` file (or absence is reported as `FAILED_INPUTS`).
2. `OUTPUT_ROOT` exists before the workflow writes to it.
3. `EQUIPMENT_TYPES` is non-empty and parseable.
4. Every `KA-*.md` file in the KTY folder was read, or its absence was explicitly reported.
5. The output file `{KTY_ID}_Equipment_Costing_Extract.csv` was written to `OUTPUT_ROOT`.
6. No files in `{KTY_PATH}` were written or modified.

### CSV schema compliance (required)

The output CSV must satisfy:

| Check | Requirement |
|---|---|
| Column count | Exactly 17 columns |
| Column order | `Equipment_Module_Type`, `Match_Quality`, `Equipment_Instance`, `Equipment_Tag`, `Quantity_and_Sparing`, `Description`, `Capacity_Throughput`, `Power_Duty`, `Size_Dimensions`, `Design_Pressure`, `Design_Temperature`, `Fluid_Process_Service`, `Subcomponents`, `Key_Costing_Parameters`, `Source_KTY`, `Source_KA_Files`, `Notes` |
| Header row | Present as first row |
| Quoting | Fields containing commas, semicolons, or newlines are quoted |

### Source traceability (required for every extracted row)

Every row in the CSV must satisfy all of the following:

| Check | Requirement |
|---|---|
| KA source cited | The `Source_KA_Files` column names the specific KA file(s) from which values were extracted |
| Equipment exists in source | The equipment item appears in the cited KA file text; no invented items |
| Tag is verbatim | The `Equipment_Tag` value is an exact match from KA source text or Equipment_Extract.md, or `No tag` when unstated in either source. Multiple tags use comma-space delimiter. |
| Parameters are sourced | All non-empty specification columns contain values from KA source text; `TBD` is used for values stated as pending in the source |
| Match quality is classified | `Match_Quality` is one of `Exact`, `Near`, or `Out_of_Scope` |
| Module type is from target list | `Equipment_Module_Type` matches one of the types provided in `EQUIPMENT_TYPES` |
| Out_of_Scope has Description | `Out_of_Scope` rows MUST have a non-blank `Description` stating the scope exclusion basis (e.g., "Excluded from 3-25 scope; shared 4-25 asset per DBM Table 1-8 Item 3") |

A run with untraceable equipment rows or invented parameter values is invalid.

### Match coverage validation

- Every target module type in `EQUIPMENT_TYPES` should be checked against KTY content. Not every type will produce matches in every KTY — that is expected.
- KTYs with zero matches produce a header-only CSV. This is a valid result.
- The run record must state: (a) which module types produced matches, (b) which did not, and (c) total row count.

### Null-result validation

KTYs with zero equipment matches must still produce:
- A CSV file with the 17-column header row and no data rows
- A run record stating no matches were found and listing the module types checked

### Reporting groups

When issues are found during extraction, group them by:

- ambiguous match quality (equipment could map to multiple module types)
- TBD/TBC parameters (values pending detailed engineering)
- scope boundary items (equipment explicitly excluded from DBM scope)
- missing parameter data (KA file mentions equipment but lacks spec detail)
- subcomponent enrichment gaps (Equipment_Extract.md unavailable or incomplete)

### Success case

A clean run reports:

- `RUN_STATUS=SUCCESS`
- Output file path
- Matched equipment count (integer)
- Module types matched (list)
- Module types with no matches (list)
- KA files read (list)
- No warnings (or explicit statement that none were encountered)

## Tool use

### Preferred tool order

Reasoning-first: this workflow is LLM-driven; no deterministic tool ordering applies during extraction. The agent reads KA markdown files within a single Knowledge Type folder and applies matching and extraction logic directly, producing a per-KTY CSV with costing-relevant design parameters.

### Allowed deterministic tools

#### Operationally invoked

- None — no operational helpers declared during extraction (WORKFLOW.md states: "No deterministic tools during extraction. This is a reasoning-first workflow.")

**Downstream note:** The orchestrator (not this workflow) invokes `tools/reporting/merge_equipment_costing_csv.py` after all per-KTY extractions complete. This tool is not part of the workflow's execution scope.

### Expected use of reasoning

This is a reasoning-first extraction workflow. The agent:

1. Reads `_CONTEXT.md` and `_REFERENCES.md` for KTY identity and source context.
2. Reads all `KA-*.md` files in the KTY folder in order.
3. Applies matching logic to identify equipment items corresponding to target module types from `EQUIPMENT_TYPES`.
4. Extracts costing-relevant parameters (capacity, power/duty, size, design pressure, temperature, fluid service, subcomponents, key costing parameters) from markdown tables and prose.
5. Optionally reads an existing `Equipment_Extract.md` for subcomponent enrichment.
6. Assembles and writes the per-KTY CSV output.

Reasoning governs every phase: preconditions, context read, KA enumeration, equipment matching, parameter extraction, CSV composition, and output file writing.

### Disallowed use

- No writing outside `OUTPUT_ROOT`.
- No modification of any file in `KTY_PATH`.
- No widening scope beyond the designated KTY folder (plus optional Equipment_Extract.md).
- No hidden reliance on tools outside the declared list.
- No invention of parameter values not stated in KA source text.

### Write boundary

Writes are limited to:

- `{RuntimeOverrides.OUTPUT_ROOT}/{KTY_ID}_Equipment_Costing_Extract.csv`

`OUTPUT_ROOT` must already exist. The workflow does not create the directory. No files in `{KTY_PATH}` may be written or modified.
