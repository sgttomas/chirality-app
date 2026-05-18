# Estimate Summary — EST_DEL-005-01_2026-02-27_0539

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Estimated hours (Level_of_Effort.csv) x hourly rates (Professional_Staff_Rates.csv) |
| **Currency** | CAD |
| **Rounding** | NONE |
| **Fallback Policy** | ALLOW_PARAMETRIC |
| **Mixed Methods** | Allowed (TRUE) — all lines use PARAMETRIC; no fallback required |

## Scope

- **Deliverable:** DEL-005-01 — Preliminary Civil Design
- **Package:** PKG-005 — Civil Design
- **Discipline:** Civil Engineering
- **Delivery Type:** Design Presentation
- **Responsible Role:** Civil Engineer

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) | Line Count |
|---|---|---|---|
| PKG-005 | DEL-005-01 | **9,960.00** | 4 |

## Totals by Cost Breakdown Structure (CBS)

| CBS | Amount (CAD) | Line Count | Detail |
|---|---|---|---|
| LABOUR-MGMT | 1,530.00 | 2 | Project Manager ($990) + Cost Estimator ($540) |
| LABOUR-DESIGN | 8,430.00 | 2 | BIM Technician ($1,710) + Civil Engineer ($6,720) |
| **TOTAL** | **9,960.00** | **4** | |

## Totals by Role

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| Project Manager | R-01 | 6 | 165 | 990.00 |
| Cost Estimator | R-08 | 4 | 135 | 540.00 |
| BIM Technician | R-13 | 18 | 95 | 1,710.00 |
| Civil Engineer | R-17 | 42 | 160 | 6,720.00 |
| **TOTAL** | | **70** | | **9,960.00** |

## Key Observations

1. **Full pricing coverage.** All 4 priced line items have complete pricing evidence from the parametric model. No TBD amounts.
2. **Civil Engineer dominates.** 42 of 70 total hours (60%) and $6,720 of $9,960 (67%) are Civil Engineer effort, consistent with this being a preliminary civil design deliverable.
3. **No material or equipment costs.** This is a professional services / design deliverable. All costs are labour. No material, procurement, or construction costs are included.
4. **Scope coverage items (ITM-005 through ITM-017) have zero standalone cost.** These 13 items represent specific design scope activities extracted from the Specification and Procedure documents. Their labour is embedded in ITM-001 through ITM-004 (the four role-based labour lines). They are included in Items.csv for scope traceability only.
5. **Alternative cross-check available.** Professional_Design_Fees.csv provides a fee-percentage model (DF-05: Civil design at 1.0% of construction value). This cannot be computed without a construction value estimate but is available for future cross-checking when construction estimates are developed.

## Warnings and Coverage Gaps

- **None critical.** All items are priced. All sources are traceable.
- **Rate confidence is MEDIUM** for all roles per the source data. Rates are parametric estimates, not contracted rates.
- **Hours are parametric estimates** from Level_of_Effort.csv, not bottom-up task-level estimates. Actual hours may vary.
