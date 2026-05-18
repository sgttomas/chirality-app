# Source_Index.md

## Pricing Sources Used

| PS-ID | File | Source Type | Items Used | Parsing Notes |
|---|---|---|---|---|
| PS-UU | Underground_Utility_Rates.csv | ALLOWANCE / PARAMETRIC | UU-05 (Cistern 50,000L supply + set: $65,000 recommended; range $42,000-$95,000) | Direct match for cistern vessel; confidence LOW |
| PS-LAB | Construction_Labour_Rates.csv | PARAMETRIC | T-05 (Plumber: $92.80/hr fully burdened) | Used for trade labour pricing; confidence MEDIUM |
| PS-STAFF | Professional_Staff_Rates.csv | PARAMETRIC | R-01 ($165/hr), R-02 ($155/hr), R-03 ($145/hr), R-05 ($140/hr), R-06 ($135/hr), R-08 ($135/hr) | Staff hourly rates for management/overhead LOE |
| PS-LOE | Level_of_Effort.csv | PARAMETRIC | DEL-014-01 rows: R-01 (6hr), R-02 (8hr), R-03 (10hr), R-05 (4hr), R-06 (6hr), R-08 (4hr) | 6 roles x hours for DEL-014-01; total 38 management hours |
| PS-PARAMS | Assumed_Project_Parameters.csv | CONFIRMED/DERIVED | PP-14 (Cistern Volume: 50,000L), PP-17 (Currency: CAD), PP-18 (Base Year: 2026) | Project parameters for context and validation |
| PS-EQ | Equipment_Pricing.csv | ALLOWANCE | Not directly used for DEL-014-01 line items | EQ-02 (pressure washer) is downstream equipment, not in cistern scope |

## Sources NOT Available (gaps)

| Gap | Impact | Workaround Applied |
|---|---|---|
| No vendor quote for cistern vessel | Pricing relies on allowance (UU-05); LOW confidence | Used UU-05 recommended rate ($65,000) |
| No vendor quote for distribution pump | No pump pricing in sources | Parametric estimate ($8,500) based on industrial pump class sizing |
| No interior piping rate table | UU-01 is underground water line rate, not interior distribution | Adapted UU-01 rate with parametric adjustment for interior piping |
| No backflow preventer pricing table | Item not in any price source | Parametric estimate ($1,800) for RPZ backflow preventer |
| No freeze protection rate table | Item not in any price source | Parametric allowance ($5,000) for insulation + heat trace |
| No plumbing permit fee schedule | Item not in any price source | Parametric estimate ($1,500) for Alberta industrial plumbing permit |

## Documents Read (engineering content)

| Document | Path | Items Extracted |
|---|---|---|
| _CONTEXT.md | DEL-014-01_Cistern/_CONTEXT.md | Deliverable identity, package, SOW mapping |
| Datasheet.md | DEL-014-01_Cistern/Datasheet.md | Cistern attributes, pump attributes, distribution points, conditions, construction elements |
| Specification.md | DEL-014-01_Cistern/Specification.md | Requirements (12 REQs), scope boundaries, verification criteria, standards |
| Guidance.md | DEL-014-01_Cistern/Guidance.md | Principles, trade-offs, coordination considerations, conflict table |
| Procedure.md | DEL-014-01_Cistern/Procedure.md | 6-phase execution sequence with 15+ steps, verification checks, records |
| WDMLRL_Decomposition_Claude.md | _Decomposition/ | WBS traceability: PKG-014, DEL-014-01, SOW-0041, SOW-0042 |
