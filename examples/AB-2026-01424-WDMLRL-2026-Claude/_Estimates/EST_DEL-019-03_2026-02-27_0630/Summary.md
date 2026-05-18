# Summary — EST_DEL-019-03_2026-02-27_0630

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method Used** | PARAMETRIC (all 6 priced lines) |
| **ALLOW_MIXED_METHODS** | TRUE (not exercised; all lines are PARAMETRIC) |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC (not exercised; all items priced from primary sources) |
| **CURRENCY** | CAD |
| **Pricing Model** | Hours (from Level_of_Effort.csv) x Hourly Rates (from Professional_Staff_Rates.csv) |

## Totals by Deliverable

| WBS_DeliverableID | Deliverable Name | Amount (CAD) | Line Count | Priced % |
|---|---|---|---|---|
| DEL-019-03 | Subcontractor Management | $5,590.00 | 6 | 100% |

## Totals by Package

| WBS_PackageID | Package Name | Amount (CAD) | Deliverables | Line Count |
|---|---|---|---|---|
| PKG-019 | Construction Management & OH&S | $5,590.00 | 1 | 6 |

## Totals by CBS

| CBS | Description | Amount (CAD) | % of Total |
|---|---|---|---|
| LABOUR-MGMT | Management labour (PM, Construction PM, Cost Estimator) | $2,770.00 | 49.6% |
| LABOUR-FIELD | Field labour (Site Superintendent) | $1,450.00 | 25.9% |
| LABOUR-QC | Quality control labour (QA/QC Lead) | $810.00 | 14.5% |
| LABOUR-HSE | Health Safety & Environment labour (HSE Manager) | $560.00 | 10.0% |
| **TOTAL** | | **$5,590.00** | **100.0%** |

## Staff Hour Summary

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| Project Manager | R-01 | 6 | $165.00 | $990.00 |
| Construction Project Manager | R-02 | 8 | $155.00 | $1,240.00 |
| Site Superintendent | R-03 | 10 | $145.00 | $1,450.00 |
| Cost Estimator | R-08 | 4 | $135.00 | $540.00 |
| QA/QC Lead | R-06 | 6 | $135.00 | $810.00 |
| HSE Manager | R-05 | 4 | $140.00 | $560.00 |
| **Total** | | **38** | | **$5,590.00** |

## Key Warnings and Coverage Gaps

1. **Labour-only estimate.** This estimate covers professional staff labour hours only. Non-labour costs (e.g., document management software, printing, insurance verification services, legal review for subcontractor contract templates) are not priced because no price source provides non-labour cost data for this deliverable. The total of $5,590.00 CAD represents the Design-Builder's internal management labour allocation for subcontractor management activities.

2. **Parametric hour estimates are low-granularity.** The Level_of_Effort.csv provides a single hour total per role for the entire deliverable lifecycle (framework establishment through close-out). These are parametric estimates at MEDIUM confidence. Actual hours will depend on the number of subcontractors engaged, project complexity, and duration of the construction phase (approximately 6-8 months based on the Dec 31, 2026 deadline).

3. **No TBD amounts.** All 6 priced lines have complete pricing from the parametric sources. Items ITM-007 through ITM-013 in the quantity takeoff (Items.csv) represent process steps whose labour cost is captured by ITM-001 through ITM-006; they are not separately priced in Detail.csv to avoid double-counting.

4. **Scope is single-deliverable.** This estimate covers DEL-019-03 only, not the full PKG-019 package. Other PKG-019 deliverables (DEL-019-01, DEL-019-02, DEL-019-04) are out of scope for this run.
