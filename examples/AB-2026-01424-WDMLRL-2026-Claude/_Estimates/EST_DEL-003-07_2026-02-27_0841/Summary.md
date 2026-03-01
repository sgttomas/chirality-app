# Summary — EST_DEL-003-07_2026-02-27_0841

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Level-of-effort (hours per role) x hourly staff rates |
| **Currency** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Rounding** | NONE |

All four line items are priced using the PARAMETRIC method. Hours are sourced from `Level_of_Effort.csv` (rows for DEL-003-07), and hourly rates are sourced from `Professional_Staff_Rates.csv`.

---

## Total by Deliverable

| WBS_PackageID | WBS_DeliverableID | Deliverable Name | Amount (CAD) | Hours |
|---|---|---|---|---|
| PKG-003 | DEL-003-07 | Mechanical Specification | **$10,170.00** | 70 |

---

## Total by CBS (Cost Breakdown Structure)

| CBS | Amount (CAD) | Line Count | % of Total |
|---|---|---|---|
| Management | $1,530.00 | 2 | 15.0% |
| Design | $8,640.00 | 2 | 85.0% |
| **TOTAL** | **$10,170.00** | **4** | **100.0%** |

---

## Total by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-01 | Project Manager | 6 | $165.00 | $990.00 |
| R-08 | Cost Estimator | 4 | $135.00 | $540.00 |
| R-13 | BIM Technician | 18 | $95.00 | $1,710.00 |
| R-15 | Mechanical Engineer | 42 | $165.00 | $6,930.00 |
| | **TOTAL** | **70** | | **$10,170.00** |

---

## Key Observations

1. **Mechanical Engineer hours dominate:** 42 of 70 hours (60%) and $6,930 of $10,170 (68.1%) are Mechanical Engineer time, which is expected for a specification deliverable requiring technical authoring, standards research, load calculation integration, and P.Eng. review.

2. **BIM Technician allocation:** 18 hours for graphics and schedule support; reasonable for a specification that cross-references equipment schedules and drawing sets.

3. **Management overhead is light:** PM (6h) and Cost Estimator (4h) represent 14.3% of total hours — appropriate for a design deliverable within a multi-discipline project.

4. **No material/equipment costs included:** This is a professional services (design) deliverable; the estimate covers only staff time to produce the specification document. Physical equipment and installation costs are covered under PKG-013 (Mechanical & HVAC Installation).

---

## Warnings and Coverage Gaps

- **None critical.** All four LOE rows from `Level_of_Effort.csv` for DEL-003-07 are priced. All rates are sourced from `Professional_Staff_Rates.csv`.
- **Design fee cross-check:** The Professional_Design_Fees.csv recommends mechanical design at 1.6% of construction value (DF-03). Without a construction value estimate for PKG-013, this cross-check cannot be completed. This is informational only and does not affect the parametric estimate validity.
- **Confidence level:** All rates and hours are marked MEDIUM confidence in the source files.
