# Source Index

## Indexed Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | 25 roles with hourly CAD rates; all MEDIUM confidence | Unit rates for labour line items (ITEM-006 through ITEM-013) |
| PS-02 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | PARAMETRIC (hours allocation) | Per-deliverable hour estimates by role; DEL-021-03 has 8 role entries | Quantities (hours) for labour line items |
| PS-03 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (context parameters) | 19 project parameters; PP-17 confirms CAD currency | Currency confirmation; project context for parametric derivation |
| PS-04 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv` | PARAMETRIC (allowance ranges) | 5 items; FP-03 and FP-04 directly support insurance premiums | Insurance premium estimates for ITEM-001 through ITEM-005 |

## Source Gaps

- WCB assessment rates are not included in any price source; WCB premium is typically payroll-based and varies by employer classification. Estimated as a parametric allowance based on general Alberta construction rates.
- E&O and Employer's Liability premium estimates are not individually broken out in Fees_Permits_Insurance.csv. FP-04 (General liability insurance allowance) provides a general range. Individual policy premiums are estimated parametrically.
- Broker fees are not broken out as a separate line item; assumed included in insurance premium amounts.
