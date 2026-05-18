# Source Index — EST_DEL-001-10_2026-02-27_0600

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `PriceSources/Professional_Staff_Rates.csv` | Rate table | 25 roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates PARAMETRIC basis, MEDIUM confidence. | Hourly rates for all 5 roles assigned to DEL-001-10 (R-01, R-08, R-11, R-12, R-13) |
| 2 | `PriceSources/Level_of_Effort.csv` | Parametric LOE model | Multi-deliverable file; filtered to DEL-001-10 rows. Columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. 5 rows for DEL-001-10. | Hours for each role on DEL-001-10: R-01 (6 hr), R-08 (4 hr), R-11 (54 hr), R-12 (42 hr), R-13 (24 hr). Total: 130 hrs. |
| 3 | `PriceSources/Assumed_Project_Parameters.csv` | Project parameters | 18 parameters covering identity, location, contract, schedule, facility, equipment, plumbing, currency, economics. | Project context: facility is ~13,000 sqft maintenance shop addition; CAD currency; 2026 base year. Not directly used for line-item pricing but supports parametric context. |
| 4 | `PriceSources/Professional_Design_Fees.csv` | Fee percentage model | 5 disciplines (Architecture, Structural, Mechanical, Electrical, Civil); columns: ItemID, Discipline, FeePercentMin/Max, RecommendedPercent, FeeBase, Basis, Confidence. | Architecture recommended fee = 4.5% of construction_value. Not used as primary pricing method for this deliverable (LOE method preferred for individual deliverable-level estimate). Available as cross-check. |
| 5 | `PriceSources/Parametric_Building_Rates.csv` | Parametric building rate model | 2 items: PB-01 (maintenance shop at $285/sf recommended) and PB-02 (wash bay premium at $70/sf). | Overall building cost cross-check (13,000 sqft x $285/sf = $3,705,000 construction value). Architecture fee cross-check: 4.5% x $3,705,000 = $166,725. Not directly used for DEL-001-10 line-item pricing. |

## Source Coverage Summary

- **Primary pricing method:** PARAMETRIC (LOE hours x hourly rates)
- **All 5 line items in Detail.csv are fully sourced** from Professional_Staff_Rates.csv (rates) and Level_of_Effort.csv (hours).
- Professional_Design_Fees.csv and Parametric_Building_Rates.csv provide cross-check context but are not the primary pricing basis for this individual deliverable.

## Cross-Check: Fee-Based vs. LOE-Based

| Approach | Value | Notes |
|---|---|---|
| LOE-based (this estimate) | $19,200.00 CAD | 130 hrs across 5 roles for DEL-001-10 only |
| Fee-based cross-check (architecture total) | $166,725 CAD | 4.5% of $3,705,000 construction value; covers ALL PKG-001 deliverables (11 deliverables), not just DEL-001-10 |
| DEL-001-10 share of architecture fee (approximate) | ~$15,157 CAD | $166,725 / 11 deliverables (simple average); actual allocation varies by deliverable complexity |

The LOE-based estimate of $19,200 for DEL-001-10 is higher than the simple average fee share (~$15,157) but within reasonable range, reflecting that renovation plans involve field survey and existing conditions assessment activities that increase effort relative to new-build drawing sets.
