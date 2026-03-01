# Source Index

## Indexed Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | 25 roles with hourly CAD rates; all MEDIUM confidence | Unit rates for labour line items (ITEM-006 through ITEM-013) |
| PS-02 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | PARAMETRIC (hours allocation) | Per-deliverable hour estimates by role; DEL-021-03 has 8 role entries | Quantities (hours) for labour line items |
| PS-03 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (context parameters) | 19 project parameters; PP-17 confirms CAD currency | Currency confirmation; project context for parametric derivation |
| PS-04 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv` | PARAMETRIC (allowance ranges) | 12 items; FP-03 and FP-04 for builders risk and CGL; FP-06, FP-07, FP-08 for WCB, E&O, and Employer's Liability (newly available) | Insurance premium estimates for ITEM-001 through ITEM-005 |

## Source Gaps Resolved

The following gaps from the prior run (EST_DEL-021-03_2026-02-26_2233) have been resolved:

| Gap | Prior Status | Current Status | Resolution |
|---|---|---|---|
| WCB assessment rates | TBD — no source data | Resolved | FP-06 added to Fees_Permits_Insurance.csv; recommended rate $28,000 (range $15,000-$45,000) |
| E&O premium | TBD — no source data | Resolved | FP-07 added to Fees_Permits_Insurance.csv; recommended rate $18,000 (range $12,000-$25,000) |
| Employer's Liability premium | TBD — no source data | Resolved | FP-08 added to Fees_Permits_Insurance.csv; recommended rate $8,000 (range $5,000-$12,000) |

## Remaining Notes

- Broker fees are not broken out as a separate line item; assumed included in insurance premium amounts.
- E&O tail coverage is not priced; a separate cost if required for the 2-year guarantee period.
