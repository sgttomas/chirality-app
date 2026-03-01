# Summary — EST_DEL-007-01_2026-02-27_0546

## Basis of Estimate

| Field | Value |
|-------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Level-of-effort hours (from parametric LOE model) x professional staff hourly rates |
| **Currency** | CAD |
| **Rounding** | NONE |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE (all items priced as PARAMETRIC; no mixed methods required) |

## Scope

- **Deliverable:** DEL-007-01 — Preliminary Landscape Design
- **Package:** PKG-007 — Landscape Architectural Design
- **Type:** Design Presentation (professional services labour only; no construction materials or physical works)
- **Purpose:** Preliminary landscape architectural design concept for WDMLRL Maintenance Shop Addition expansion area, submitted to Camrose County for approval as a gate to final design (DEL-007-02, DEL-007-03, DEL-007-04).

## Totals by Deliverable

| WBS_DeliverableID | Description | Amount (CAD) | Hours |
|-------------------|-------------|-------------|-------|
| DEL-007-01 | Preliminary Landscape Design | 10,980.00 | 80 |

## Totals by CBS Category

| CBS | Description | Amount (CAD) | Line Count |
|-----|-------------|-------------|-----------|
| DESIGN_LABOUR | Landscape Architect design hours | 9,450.00 | 1 |
| MGMT_LABOUR | Project Manager + Cost Estimator | 1,530.00 | 2 |
| **TOTAL** | | **10,980.00** | **3** |

## Totals by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|--------|------|-------|---------------|-------------|
| R-19 | Landscape Architect | 70 | 135.00 | 9,450.00 |
| R-01 | Project Manager | 6 | 165.00 | 990.00 |
| R-08 | Cost Estimator | 4 | 135.00 | 540.00 |
| | **TOTAL** | **80** | | **10,980.00** |

## Key Observations

1. **Design labour dominates:** The Landscape Architect accounts for 86.1% of the total cost (70 of 80 hours, $9,450 of $10,980).
2. **No construction or material costs:** DEL-007-01 is a preliminary design presentation deliverable; all costs are professional services.
3. **No fallback pricing required:** All items fully priced from primary PARAMETRIC sources (LOE + staff rates).
4. **100% provenance completeness:** Every line item has a traceable SourceRef to both the hours source (Level_of_Effort.csv) and the rate source (Professional_Staff_Rates.csv).

## Warnings and Coverage Gaps

- **No Landscape Architect fee line in Professional_Design_Fees.csv.** This source was not usable for DEL-007-01. No gap in coverage because the LOE + staff rates method provides complete pricing.
- **Confidence level is MEDIUM** for all line items (per the MEDIUM confidence designation in both the staff rates and LOE sources).
- **Deliverable has 16 open TBD/ASSUMPTION items** in its Datasheet register (REG-001 through REG-016). These are design content uncertainties, not pricing uncertainties. They do not affect the cost estimate for professional labour hours but may affect scope if the County directs changes at the approval gate.
