# Summary — EST_DEL-004-06_2026-02-27_0833

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method Used** | PARAMETRIC — Level-of-Effort hours x Professional Staff Rates |
| **Currency** | CAD |
| **Fallback Policy** | ALLOW_PARAMETRIC |
| **Mixed Methods** | Allowed (TRUE) — not exercised; all lines are PARAMETRIC |

The estimate for DEL-004-06 (Panel Schedules) is based on a parametric level-of-effort model. Estimated professional hours per role are sourced from `Level_of_Effort.csv`, and hourly rates per role are sourced from `Professional_Staff_Rates.csv`. Both sources carry MEDIUM confidence and PARAMETRIC basis.

## Totals

### By Deliverable

| DeliverableID | Deliverable Name | Amount (CAD) | Hours |
|---|---|---|---|
| DEL-004-06 | Panel Schedules | **$7,290.00** | 50 |

### By CBS Category

| CBS | Amount (CAD) | Lines |
|---|---|---|
| Design-Management | $1,530.00 | 2 |
| Design-Production | $1,140.00 | 1 |
| Design-Electrical | $4,620.00 | 1 |
| **TOTAL** | **$7,290.00** | **4** |

### By Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-01 | Project Manager | 6 | $165.00 | $990.00 |
| R-08 | Cost Estimator | 4 | $135.00 | $540.00 |
| R-13 | BIM Technician | 12 | $95.00 | $1,140.00 |
| R-16 | Electrical Engineer | 28 | $165.00 | $4,620.00 |
| | **TOTAL** | **50** | | **$7,290.00** |

### By Package

| PackageID | Package Name | Amount (CAD) |
|---|---|---|
| PKG-004 | Electrical Design | $7,290.00 |

## Key Observations

1. **Design effort is Electrical-Engineer-dominant.** The Electrical Engineer accounts for 56% of total hours (28 of 50) and 63% of total cost ($4,620 of $7,290), consistent with the lead design role for panel schedule production.
2. **This is a design-professional-services estimate only.** It covers professional staff hours for design production of the Panel Schedules deliverable. It does not include physical materials, panel hardware, construction labor, or installation costs (those are in PKG-015 Electrical & Low-Voltage Installation scope).
3. **Parametric model confidence is MEDIUM.** Both the hourly rates and LOE hours are parametric estimates. Actual hours may vary based on design complexity, number of design iterations, and County review cycles.

## Warnings and Coverage Gaps

| Warning | Severity | Notes |
|---|---|---|
| Items ITEM-005 through ITEM-020 are quantity-takeoff entries from the engineering documents (load enumeration) but are not independently priced — their cost is captured in the professional LOE hours (ITEM-001 through ITEM-004). | INFO | These items demonstrate scope completeness of the takeoff but do not produce separate cost lines in Detail.csv. |
| Multiple load quantities are TBD in Items.csv (receptacle counts, overhead door count, exhaust fan count, service pit circuits, low-voltage provisions, welding station count). | INFO | These TBDs are design-stage unknowns documented in the Datasheet. They do not affect the LOE-based design cost estimate but are flagged for downstream construction estimating (PKG-015). |
| No cross-check performed against Professional_Design_Fees.csv (DF-04 Electrical: 1.6% of construction value). | INFO | Fee-based cross-check requires a total construction value, which is not available at single-deliverable scope. |
