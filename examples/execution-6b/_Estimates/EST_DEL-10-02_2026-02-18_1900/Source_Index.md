# Source Index

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | RATE_TABLE | 30 roles with RoleID, HourlyRate_CAD; all rates basis=MARKET, confidence=MEDIUM | Hourly rates for all professional staff roles |
| 2 | `_PriceSources/Level_of_Effort.csv` | RATE_TABLE (hours) | 73 rows mapping Execution 6b deliverables to RoleID + EstimatedHours; basis=PARAMETRIC | Hours per role per deliverable |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (reference) | 29 parameters covering duration, area, quantities, financial estimates | Background context; not directly used for DEL-10-02 line item pricing |

## Decomposition Source

| Source File | Version | Status | Notes |
|---|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | ACCEPTED | Provides PackageID, DeliverableID, scope item mappings, and deliverable descriptions |

## Dependency Source

| Source File | Record Count | Notes |
|---|---|---|
| `DEL-10-02/Dependencies.csv` | 16 rows (v3.1 schema) | 4 anchors, 6 upstream prerequisites (documents), 1 constraint (DEC-013), 5 downstream handovers |

## Source Usage for DEL-10-02

All 3 line items in Detail.csv are priced using:
- **Hours**: Level_of_Effort.csv (rows for DEL-10-02: R-02 @ 8 hrs, R-07 @ 6 hrs, R-29 @ 4 hrs)
- **Rates**: Professional_Staff_Rates.csv (R-02 @ $175/hr, R-07 @ $155/hr, R-29 @ $155/hr)

Assumed_Project_Parameters.csv was reviewed but not directly used in pricing for this deliverable (no parametric area/quantity drivers apply to this narrative-type deliverable).
