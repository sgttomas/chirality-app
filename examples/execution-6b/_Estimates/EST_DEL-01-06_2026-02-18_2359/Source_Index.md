# Source Index

## Indexed Price Sources

| # | Source File | Source Type | Content Summary | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | RATE_TABLE | 30 roles with hourly rates in CAD; categories: Management, Design, Production, Construction, Financial, Administrative, Legal, Specialty, External. Confidence: MEDIUM. Basis: MARKET. | Unit rates for all labor line items |
| 2 | `_PriceSources/Level_of_Effort.csv` | RATE_TABLE (hours) | 73 rows mapping DeliverableID x RoleID to EstimatedHours; execution 6b; basis: PARAMETRIC. | Quantities (hours) for all deliverables |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (reference) | 29 parameters: durations, areas, quantities, financial estimates. Used for context only -- no direct pricing derivation for DEL-01-06. | Background context for assumptions; not used for pricing |

## DEL-01-06 Specific Source Coverage

**Level_of_Effort.csv rows for DEL-01-06:**

| RoleID | Role | EstimatedHours | Notes (from source) |
|---|---|---|---|
| R-02 | Project Manager | 12 | Narrative lead: allowances; exclusions; value alternatives; CCIP |
| R-18 | Estimator (Senior) | 8 | Pricing assumptions documentation; backup |

**Professional_Staff_Rates.csv rates used:**

| RoleID | Role | HourlyRate_CAD | Basis | Confidence |
|---|---|---|---|---|
| R-02 | Project Manager | 175 | MARKET | MEDIUM |
| R-18 | Estimator (Senior) | 145 | MARKET | MEDIUM |

## Parsing Notes

- All three CSVs are well-formed with headers.
- Level_of_Effort.csv uses `Execution=6b` filter; all rows with `DEL-01-06` were extracted.
- Professional_Staff_Rates.csv rate for R-30 (Surety Broker) is $0 (commission-based); not relevant to DEL-01-06.
- Assumed_Project_Parameters.csv provides background context (e.g., Schedule A total $7,710,000 referenced in brief) but no direct pricing input for this deliverable.
