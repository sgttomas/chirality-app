# Summary.md
## EST_DEL-009-02_2026-02-27_0600

---

## Basis of Estimate Used

| Field | Value |
|-------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Professional staff hourly rates applied to estimated level of effort by role and procedure phase |
| **Pricing sources** | Professional_Staff_Rates.csv (rates), Level_of_Effort.csv (partial LOE), Assumed_Project_Parameters.csv (context) |
| **Fallback applied** | Yes — ALLOW_PARAMETRIC used for 12 of 15 line items where LOE source did not provide hours; hours estimated from Procedure.md scope |
| **Currency** | CAD |
| **Mixed methods** | No — all line items use PARAMETRIC method (consistent with BASIS_OF_ESTIMATE) |

---

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Deliverable Name | Total (CAD) | Line Count |
|---------------|-------------------|------------------|-------------|------------|
| PKG-009 | DEL-009-02 | Building Permit Application & Approval | **$9,340** | 15 |

*Note: Line count includes L-015 (permit fees, $0) — excluded per contract (County pays fees). Proponent cost total is $9,340.*

---

## Totals by CBS Category

| CBS | Total (CAD) | % of Total | Line Count |
|-----|-------------|------------|------------|
| Management | $1,530 | 16.4% | 2 |
| Specialty | $5,000 | 53.5% | 5 |
| Design | $2,360 | 25.3% | 6 |
| Admin | $450 | 4.8% | 1 |
| Excluded | $0 | 0.0% | 1 |
| **TOTAL** | **$9,340** | **100%** | **15** |

---

## Effort Summary

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|------|-------|---------------|-------------|
| Project Manager (R-01) | 6 | $165 | $990 |
| Cost Estimator (R-08) | 4 | $135 | $540 |
| Permitting Specialist (R-22) | 40 | $125 | $5,000 |
| Document Controller (R-09) | 6 | $75 | $450 |
| Senior Architect (R-11) | 4 | $180 | $720 |
| Structural Engineer (R-14) | 2 | $170 | $340 |
| Mechanical Engineer (R-15) | 2 | $165 | $330 |
| Electrical Engineer (R-16) | 2 | $165 | $330 |
| Civil Engineer (R-17) | 2 | $160 | $320 |
| Plumbing Engineer (R-18) | 2 | $160 | $320 |
| **TOTAL** | **70** | | **$9,340** |

---

## Key Warnings and Coverage Gaps

1. **LOE source coverage is partial.** Level_of_Effort.csv provides hours for only 2 of 10 roles (PM and Cost Estimator). The remaining 8 roles (Permitting Specialist, Document Controller, 5 discipline engineers, Senior Architect) were estimated parametrically from Procedure.md phase scope. The LOE Notes column shows "PKG-009 Project Manager -- TBD," confirming the source data is preliminary.

2. **Permitting Specialist hours are the largest cost driver.** The 40-hour allocation for R-22 across 5 procedure phases is a parametric estimate. Actual effort depends on Camrose County authority responsiveness, application complexity, number of RFI cycles, and inspection count (~7 anticipated stages). Range: 30-60 hrs plausible.

3. **Permit fees excluded.** Building permit fees are the County's responsibility (R-01, §3.3.1; SOW-0202) and are excluded from the Proponent estimate at $0. The actual fee amount is TBD until confirmed with Camrose County building services.

4. **Design review hours are minimal.** The 14 hours allocated to discipline engineers (2 hrs each for 5 disciplines + 4 hrs for Senior Architect) represent permit-specific review only. The underlying design work is estimated separately in PKG-001 through PKG-006 deliverables.

5. **Inspection coordination hours depend on permit conditions.** The 10-hour allocation for Phase 5 (inspection coordination) is based on ~7 anticipated inspection stages. Actual stages and effort will be confirmed upon permit issuance.
