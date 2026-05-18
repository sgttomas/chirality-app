# Estimate Summary — EST_DEL-005-06_2026-02-27_0546

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

- **Deliverable:** DEL-005-06 — Civil Calculation Package
- **Package:** PKG-005 — Civil Design
- **Discipline:** Civil Engineering
- **Delivery Type:** Calculation Package
- **Responsible Role:** Civil Engineer
- **SOW Coverage:** SOW-0015 (detailed design and drawing preparation), SOW-0020 (positive site drainage), SOW-0021 (no alteration of neighbouring drainage)
- **Objectives:** OBJ-001, OBJ-003

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) | Line Count |
|---|---|---|---|
| PKG-005 | DEL-005-06 | **12,770.00** | 4 |

## Totals by Cost Breakdown Structure (CBS)

| CBS | Amount (CAD) | Line Count | Detail |
|---|---|---|---|
| LABOUR-MGMT | 1,530.00 | 2 | Project Manager ($990) + Cost Estimator ($540) |
| LABOUR-DESIGN | 11,240.00 | 2 | BIM Technician ($2,280) + Civil Engineer ($8,960) |
| **TOTAL** | **12,770.00** | **4** | |

## Totals by Role

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| Project Manager | R-01 | 6 | 165 | 990.00 |
| Cost Estimator | R-08 | 4 | 135 | 540.00 |
| BIM Technician | R-13 | 24 | 95 | 2,280.00 |
| Civil Engineer | R-17 | 56 | 160 | 8,960.00 |
| **TOTAL** | | **90** | | **12,770.00** |

## Key Observations

1. **Full pricing coverage.** All 4 priced line items have complete pricing evidence from the parametric model. No TBD amounts.
2. **Civil Engineer dominates.** 56 of 90 total hours (62%) and $8,960 of $12,770 (70%) are Civil Engineer effort. This is consistent with a civil calculation package requiring intensive engineering analysis — drainage sizing, hydrology/hydraulic analysis, grading volumes, driving surface design, slope stability assessment, utility sizing, compliance verification, and P.Eng. sealing.
3. **Higher effort than Preliminary Design (DEL-005-01).** Compared to the preliminary civil design (70 hr, $9,960), the calculation package requires 90 hr ($12,770) — a 29% increase in hours and cost. The increase is driven by the Civil Engineer (+14 hr) and BIM Technician (+6 hr), reflecting the substantially greater analytical depth of a sealed calculation package versus a preliminary design presentation.
4. **No material or equipment costs.** This is a professional services / engineering calculation deliverable. All costs are labour. No material, procurement, or construction costs are included.
5. **Scope coverage items (ITM-005 through ITM-021) have zero standalone cost.** These 17 items represent specific calculation topics and design activities extracted from the Datasheet, Specification, and Procedure documents. Their labour is embedded in ITM-001 through ITM-004 (the four role-based labour lines). They are included in Items.csv for scope traceability only.
6. **Critical upstream dependencies.** The calculation package depends on DEL-008-01 (Geotechnical Investigation Report) and DEL-008-02 (Preliminary Site Survey). The Procedure defines four hold points (HP-01 through HP-04) that gate progress. Delays in these upstream deliverables will affect the schedule for completing this calculation package but do not change the estimated effort.
7. **Alternative cross-check available.** Professional_Design_Fees.csv provides a fee-percentage model (DF-05: Civil design at 1.0% of construction value). This cannot be computed without a construction value estimate but is available for future cross-checking when construction estimates are developed.

## Warnings and Coverage Gaps

- **None critical.** All items are priced. All sources are traceable.
- **Rate confidence is MEDIUM** for all roles per the source data. Rates are parametric estimates, not contracted rates.
- **Hours are parametric estimates** from Level_of_Effort.csv, not bottom-up task-level estimates. Actual hours may vary.
- **Upstream dependency risk:** If geotechnical conditions are adverse (e.g., high water table, poor subgrade), the slope stability analysis and driving surface design may require additional engineering hours beyond the parametric estimate.
