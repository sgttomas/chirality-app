# Summary — EST_DEL-004-01_2026-02-26_2043

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method Used | Level-of-effort hours (from Level_of_Effort.csv) multiplied by staff hourly rates (from Professional_Staff_Rates.csv) |
| Currency | CAD |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods | TRUE (allowed) — all lines priced as PARAMETRIC in this run |

## Totals by Deliverable

| WBS_DeliverableID | Name | Amount (CAD) | Line Count |
|---|---|---|---|
| DEL-004-01 | Preliminary Electrical Design | **10,170.00** | 4 |

## Totals by CBS

| CBS | Amount (CAD) | Line Count | Description |
|---|---|---|---|
| Design-Management | 1,530.00 | 2 | Project Manager + Cost Estimator |
| Design-Production | 1,710.00 | 1 | BIM Technician (CAD/BIM layout production) |
| Design-Engineering | 6,930.00 | 1 | Electrical Engineer (lead design effort) |
| **TOTAL** | **10,170.00** | **4** | |

## Totals by Package

| WBS_PackageID | Amount (CAD) |
|---|---|
| PKG-004 | **10,170.00** |

## Effort Summary

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| Project Manager (R-01) | 6 | 165.00 | 990.00 |
| Cost Estimator (R-08) | 4 | 135.00 | 540.00 |
| BIM Technician (R-13) | 18 | 95.00 | 1,710.00 |
| Electrical Engineer (R-16) | 42 | 165.00 | 6,930.00 |
| **Total** | **70** | — | **10,170.00** |

## Key Observations

1. **Scope:** DEL-004-01 is a preliminary design presentation (SOW-0010d). It is a design-stage deliverable only — no material or construction costs are included.
2. **Labour composition:** The Electrical Engineer accounts for 68.1% of the total cost (42 of 70 hours). This is consistent with a lead-engineer-driven preliminary design where the engineer performs source review, design development, quality review, coordination, and submission compilation.
3. **BIM Technician:** 18 hours allocated for layout drawing production, representing 25.7% of total hours. This covers preliminary electrical layout drafting per Procedure Step 3.
4. **Management overhead:** PM (6h) + Cost Estimator (4h) = 10h combined (14.3% of total), which is a light management touch consistent with a preliminary-stage design deliverable.
5. **No TBD pricing:** All 4 priced lines have complete rates and quantities from the price sources. 100% pricing coverage.

## Warnings and Coverage Gaps

- **No material/construction costs:** This deliverable is design-only. Items 5–25 in Items.csv represent design scope verification lines (systems and features the engineer must address) but are priced through the labour effort in Items 1–4. They are not separately costed.
- **Professional Design Fees cross-check:** DF-04 in Professional_Design_Fees.csv suggests electrical design fees of 1.0%–2.2% of construction value. Without a confirmed construction value, this cross-check cannot be completed. If construction value is estimated at ~$2M–$3M, the full electrical design package (PKG-004, all deliverables DEL-004-01 through DEL-004-09) would be $20K–$66K. The DEL-004-01 preliminary design at $10,170 represents one deliverable of nine in PKG-004, which is directionally consistent.
