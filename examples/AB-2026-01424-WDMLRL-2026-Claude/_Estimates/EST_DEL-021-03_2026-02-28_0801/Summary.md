# Estimate Summary — DEL-021-03 (Insurance Package)

**RunID:** EST_DEL-021-03_2026-02-28_0801
**Date:** 2026-02-28
**Currency:** CAD
**Basis of Estimate:** PARAMETRIC

---

## Basis of Estimate Used

- **Primary method:** PARAMETRIC
- **Pricing sources:** Fees_Permits_Insurance.csv (insurance premium ranges), Professional_Staff_Rates.csv (hourly labour rates), Level_of_Effort.csv (hours by role per deliverable)
- **Fallback policy:** ALLOW_PARAMETRIC applied; all insurance lines now priced using newly available data from Fees_Permits_Insurance.csv (FP-06, FP-07, FP-08)
- **Mixed methods:** TRUE (allowed); all lines use PARAMETRIC method
- **Re-run note:** This snapshot resolves 3 previously-TBD insurance premium lines (WCB, E&O, Employer's Liability) using pricing data added to Fees_Permits_Insurance.csv since the prior run (EST_DEL-021-03_2026-02-26_2233)

---

## Totals by Cost Breakdown Structure (CBS)

| CBS | Description | Amount (CAD) | Line Count | Notes |
|---|---|---|---|---|
| INS | Insurance Premiums | 74,000 | 5 | All 5 insurance lines now priced: builders risk ($14,000) + CGL ($6,000) + WCB ($28,000) + E&O ($18,000) + employer's liability ($8,000) |
| LAB | Professional Labour | 7,960 | 8 | 60 total hours across 8 roles; fully priced (unchanged from prior run) |
| **TOTAL** | | **81,960** | **13** | **All lines priced; no TBD items remain** |

---

## Totals by Package / Deliverable

| Package | Deliverable | Priced Amount (CAD) | TBD Count | Total Lines |
|---|---|---|---|---|
| PKG-021 | DEL-021-03 | 81,960 | 0 | 13 |

---

## Labour Detail

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| Contract Administrator (R-25) | 16 | 120 | 1,920 |
| Project Manager (R-01) | 6 | 165 | 990 |
| Construction Project Manager (R-02) | 8 | 155 | 1,240 |
| Site Superintendent (R-03) | 10 | 145 | 1,450 |
| Cost Estimator (R-08) | 4 | 135 | 540 |
| QA/QC Lead (R-06) | 6 | 135 | 810 |
| HSE Manager (R-05) | 4 | 140 | 560 |
| Document Controller (R-09) | 6 | 75 | 450 |
| **Total** | **60** | | **7,960** |

---

## Insurance Premium Detail

| Coverage | Amount (CAD) | Status | Source |
|---|---|---|---|
| Builders risk / course of construction | 14,000 | Priced | FP-03 recommended rate |
| Automobile / BI / PD (CGL) — $5M | 6,000 | Priced | FP-04 recommended rate |
| WCB — Alberta statutory | 28,000 | Priced | FP-06 recommended rate (NEW) |
| Professional Liability (E&O) — $5M | 18,000 | Priced | FP-07 recommended rate (NEW) |
| Employer's Liability — $5M | 8,000 | Priced | FP-08 recommended rate (NEW) |
| **Subtotal** | **74,000** | | |

---

## Key Warnings and Coverage Gaps

1. **All 5 insurance premium lines are now priced.** WCB ($28,000), E&O ($18,000), and Employer's Liability ($8,000) have been resolved using newly available data from Fees_Permits_Insurance.csv (FP-06, FP-07, FP-08). All three are LOW confidence with wide parametric ranges.

2. **Builder's risk coverage status remains uncertain.** RFP §4.2 does not explicitly require it; CCDC 14-2013 provisions (not accessible) may. The $14,000 estimate is included as a parametric allowance but may be eliminated or increased depending on contract review.

3. **Insurance premiums are project-value-dependent.** The Fees_Permits_Insurance.csv ranges are wide (e.g., FP-06 WCB: $15,000-$45,000; FP-07 E&O: $12,000-$25,000). Actual premiums will depend on the final contract value, payroll, and Proponent's claims history.

4. **No subcontractor insurance costs are included.** Per ASMP-01, subcontractors are assumed responsible for their own insurance. If the Proponent must procure a wrap-up or OCIP policy, this would add significant cost.

5. **E&O tail coverage cost is not included.** Per Guidance note C-002, tail coverage may be needed for the 2-year guarantee period. This is an additional cost not captured in the estimate.
