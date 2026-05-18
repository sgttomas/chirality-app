# Summary — EST_DEL-005-02_2026-02-26_2246

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Level-of-Effort (hours) x Staff Hourly Rates |
| **Currency** | CAD |
| **Rounding** | NONE |
| **Fallback Policy** | ALLOW_PARAMETRIC |
| **Mixed Methods** | TRUE (allowed; not exercised — all lines are PARAMETRIC) |

This estimate prices the professional design effort required to produce the Site Grading Plan (DEL-005-02) IFC drawing set for the WDMLRL Maintenance Shop Addition project. The parametric model uses deliverable-level hour allocations from Level_of_Effort.csv multiplied by role-specific hourly rates from Professional_Staff_Rates.csv.

## Deliverable Total

| Deliverable | Package | Total (CAD) | Hours | Lines |
|---|---|---|---|---|
| DEL-005-02 — Site Grading Plan | PKG-005 — Civil Design | **$18,390.00** | 130 | 4 |

## Breakdown by CBS

| CBS | Amount (CAD) | % of Total | Description |
|---|---|---|---|
| Design-Management | $1,530.00 | 8.3% | Project management and cost estimating support |
| Design-Production | $3,420.00 | 18.6% | BIM/CAD drafting and drawing production |
| Design-Technical | $13,440.00 | 73.1% | Civil engineering design, analysis, QA, and P.Eng. stamp |
| **TOTAL** | **$18,390.00** | **100.0%** | |

## Breakdown by Role

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| Project Manager | R-01 | 6 | $165.00 | $990.00 | 5.4% |
| Cost Estimator | R-08 | 4 | $135.00 | $540.00 | 2.9% |
| BIM Technician | R-13 | 36 | $95.00 | $3,420.00 | 18.6% |
| Civil Engineer | R-17 | 84 | $160.00 | $13,440.00 | 73.1% |
| **TOTAL** | | **130** | | **$18,390.00** | **100.0%** |

## Cross-Check Against Fee Percentage Model

Professional_Design_Fees.csv (DF-05) suggests a civil/site design fee of 1.0% (recommended) of construction value. Without a confirmed construction value for civil/sitework scope, this cross-check is noted for reference only. If the total civil construction value for sitework were in the range of $1.5M-$2.0M (a rough parametric range for a project of this type), the fee-percentage model would suggest $15,000-$20,000 for civil design. The LOE-based estimate of $18,390 falls within this range, providing directional corroboration.

## Key Warnings and Coverage Gaps

- **No construction/material items priced.** DEL-005-02 is a design deliverable (IFC Drawing Set). Construction execution of grading is covered under PKG-018, not this deliverable.
- **All rates are PARAMETRIC / MEDIUM confidence.** Replace with actual contracted or quoted rates when available.
- **Hour allocations are parametric estimates.** The 130-hour total (84 hr Civil Engineer, 36 hr BIM, 6 hr PM, 4 hr Cost Estimator) is a parametric baseline. Actual effort may vary based on site complexity, survey data quality, and number of design iterations with County.
- **Upstream dependency risk.** Grading design cannot be finalized until geotechnical report (DEL-008-01), preliminary survey (DEL-008-02), and County approval of preliminary civil design (DEL-005-01) are received. Delays in these inputs may increase total design effort (rework, waiting, re-coordination).
