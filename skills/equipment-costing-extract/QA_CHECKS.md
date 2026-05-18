# equipment-costing-extract — QA Checks

Minimum checks for a valid run:

1. `KTY_PATH` exists and contains at least one `KA-*.md` file (or absence is reported as `FAILED_INPUTS`).
2. `OUTPUT_ROOT` exists before the skill writes to it.
3. `EQUIPMENT_TYPES` is non-empty and parseable.
4. Every `KA-*.md` file in the KTY folder was read, or its absence was explicitly reported.
5. The output file `{KTY_ID}_Equipment_Costing_Extract.csv` was written to `OUTPUT_ROOT`.
6. No files in `{KTY_PATH}` were written or modified.

## CSV schema compliance (required)

The output CSV must satisfy:

| Check | Requirement |
|---|---|
| Column count | Exactly 17 columns |
| Column order | `Equipment_Module_Type`, `Match_Quality`, `Equipment_Instance`, `Equipment_Tag`, `Quantity_and_Sparing`, `Description`, `Capacity_Throughput`, `Power_Duty`, `Size_Dimensions`, `Design_Pressure`, `Design_Temperature`, `Fluid_Process_Service`, `Subcomponents`, `Key_Costing_Parameters`, `Source_KTY`, `Source_KA_Files`, `Notes` |
| Header row | Present as first row |
| Quoting | Fields containing commas, semicolons, or newlines are quoted |

## Source traceability (required for every extracted row)

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

## Match coverage validation

- Every target module type in `EQUIPMENT_TYPES` should be checked against KTY content. Not every type will produce matches in every KTY — that is expected.
- KTYs with zero matches produce a header-only CSV. This is a valid result.
- The run record must state: (a) which module types produced matches, (b) which did not, and (c) total row count.

## Null-result validation

KTYs with zero equipment matches must still produce:
- A CSV file with the 17-column header row and no data rows
- A run record stating no matches were found and listing the module types checked

## Reporting groups

When issues are found during extraction, group them by:

- ambiguous match quality (equipment could map to multiple module types)
- TBD/TBC parameters (values pending detailed engineering)
- scope boundary items (equipment explicitly excluded from DBM scope)
- missing parameter data (KA file mentions equipment but lacks spec detail)
- subcomponent enrichment gaps (Equipment_Extract.md unavailable or incomplete)

## Success case

A clean run reports:

- `RUN_STATUS=SUCCESS`
- Output file path
- Matched equipment count (integer)
- Module types matched (list)
- Module types with no matches (list)
- KA files read (list)
- No warnings (or explicit statement that none were encountered)
