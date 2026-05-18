# Source Index

## Indexed Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | 25 roles with hourly CAD rates; all MEDIUM confidence | Unit rates for labour line items (ITEM-006 through ITEM-013) |
| PS-02 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | PARAMETRIC (hours allocation) | Per-deliverable hour estimates by role; DEL-021-04 has 8 role entries totalling 60 hours | Quantities (hours) for labour line items |
| PS-03 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (context parameters) | 19 project parameters; PP-06 confirms CCDC 14-2013 contract form; PP-17 confirms CAD currency | Currency confirmation; contract form identification |
| PS-04 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv` | PARAMETRIC (allowance ranges) | 5 items; no items directly map to contract execution costs (FP-01/FP-02 are bonds under DEL-021-02; FP-03/FP-04 are insurance under DEL-021-03; FP-05 is permits) | No direct support for DEL-021-04 non-labour items |

## Source Gaps

- CCDC 14-2013 form purchase cost is not included in any price source. The CCDC standard form is a copyrighted document that must be purchased from the Canadian Construction Documents Committee. Typical cost is estimated parametrically.
- Legal counsel review fees are not included in any price source. Legal review of a CCDC 14-2013 contract package is a standard prerequisite but hourly rates and expected hours for external counsel are not provided.
- Contract execution meeting logistics (travel, venue, reproduction) are not separately broken out in price sources.
- Contract distribution costs (reproduction of originals/certified copies, courier/delivery) are not in price sources.
- Fees_Permits_Insurance.csv does not contain any line items applicable to the contract execution deliverable itself; all FP items map to DEL-021-02 (bonds), DEL-021-03 (insurance), or permits.
