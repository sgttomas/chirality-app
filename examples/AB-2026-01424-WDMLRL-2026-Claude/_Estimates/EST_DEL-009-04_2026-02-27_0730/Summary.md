# Summary.md
## Estimate Snapshot — DEL-009-04 Code Compliance Register & Inspection Log

---

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Hours (from Level_of_Effort.csv) x Rates (from Professional_Staff_Rates.csv) |
| **Currency** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **RUN_STATUS** | WARNINGS |

---

## Totals

### By Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Priced Amount (CAD) | TBD Lines | Priced Lines | Notes |
|---|---|---|---|---|---|
| PKG-009 | DEL-009-04 | 1,530.00 | 10 | 10 | Priced total covers register setup (Phase 1-2) only; excludes operational effort |

### By CBS

| CBS | Priced Amount (CAD) | TBD Lines | Priced Lines |
|---|---|---|---|
| Professional Services | 1,530.00 | 10 | 10 |

### Direct LOE Source Totals (Cross-check)

| Role | Hours | Rate (CAD/h) | Amount (CAD) | Source |
|---|---|---|---|---|
| R-01 Project Manager | 6 | 165.00 | 990.00 | Level_of_Effort.csv row 255 |
| R-08 Cost Estimator | 4 | 135.00 | 540.00 | Level_of_Effort.csv row 256 |
| **Total** | **10** | | **1,530.00** | |

The priced amount of $1,530.00 CAD represents the **allocated sub-total from the LOE source** (6h PM + 4h CE), distributed across Phase 1 and Phase 2 setup activities (DL-001 through DL-008). The DL-019 and DL-020 lines represent the same LOE source amounts in aggregate form and are NOT additive with DL-001 through DL-008.

---

## Key Warnings and Coverage Gaps

1. **Material TBD coverage gap (50% of line items):** 10 of 20 Detail.csv lines have Amount = TBD. These represent Phase 3 (construction-phase inspection coordination), Phase 4 (guarantee period maintenance), and Phase 5 (closeout) operational effort that is not quantifiable until permits are issued and the inspection schedule is known.

2. **LOE source covers setup only:** The Level_of_Effort.csv allocates only 10 total hours to DEL-009-04. This is reasonable for register framework design and initial permit condition loading but does not cover the months-long operational lifecycle of the register during construction and the 2-year guarantee period.

3. **Permit condition count unknown:** The number of permit conditions, required inspections, and potential deficiencies are all TBD pending permit issuance (DEL-009-01, DEL-009-02, DEL-009-03). These are the primary quantity drivers for operational effort.

4. **No Permitting Specialist (R-22) hours allocated:** The LOE source does not include R-22 Permitting Specialist ($125/h) hours for DEL-009-04, despite R-22 being defined in Professional_Staff_Rates.csv as "Permits, code process tracking." All hours are allocated to R-01 (PM) and R-08 (CE).

5. **Guarantee period effort not estimated:** Phase 4 (2-year guarantee period maintenance) represents a potentially significant but unquantified cost.

---

## Scope

- **Included:** DEL-009-04 — Code Compliance Register & Inspection Log (1 deliverable in PKG-009)
- **Excluded:** All other deliverables and packages. Permit fees excluded per RFP §3.3.1 (County responsibility). Upstream permit deliverables (DEL-009-01, DEL-009-02, DEL-009-03) estimated separately.
