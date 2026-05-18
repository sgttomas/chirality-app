# Source Index — EST_DEL-021-02_2026-02-27_0540

## Indexed Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | `Professional_Staff_Rates.csv` | RATE_TABLE (parametric rates) | 25 roles with hourly rates in CAD; Basis=PARAMETRIC; Confidence=MEDIUM | Labour unit rates for all professional/staff line items |
| PS-02 | `Level_of_Effort.csv` | PARAMETRIC (hours model) | Deliverable-level hours allocation by role; matched on DeliverableID=DEL-021-02 | Quantities (hours) for labour line items ITEM-003 through ITEM-010 |
| PS-03 | `Assumed_Project_Parameters.csv` | PARAMETRIC (project context) | 18 project parameters including currency, facility size, schedule | Context for bond premium estimation; contract price remains TBD |
| PS-04 | `Fees_Permits_Insurance.csv` | PARAMETRIC / ALLOWANCE | 5 items including FP-01 (Performance bond premium allowance) and FP-02 (Labour & material payment bond premium allowance) with min/max/recommended ranges | Bond premium allowances for ITEM-001 and ITEM-002 |

## Source Coverage Assessment

| Item Category | Source Available | Coverage |
|---|---|---|
| Bond premiums (Performance + Payment) | PS-04 (Fees_Permits_Insurance.csv) — FP-01, FP-02 | Parametric allowance with recommended values; contract price TBD so absolute amounts are estimates |
| Labour hours (Contract Administrator, PM, CPM, etc.) | PS-02 (Level_of_Effort.csv) — DEL-021-02 rows | Full coverage — 8 roles with allocated hours |
| Labour rates | PS-01 (Professional_Staff_Rates.csv) | Full coverage — all 8 roles have hourly rates |
| Contract price (for bond face amount calculation) | None | NOT AVAILABLE — contract price is TBD; bond face amounts cannot be calculated |

## Unsupported Items

- **Bond face amounts** (50% x Contract Price each): Cannot be determined — contract price TBD. Only the bond premium cost to the proponent is estimated.
- **Surety company fees** beyond premium: Not itemized in sources; assumed included in premium allowances.
