# Estimate Summary — EST_DEL-006-07_2026-02-27_0700

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method Used | Parametric: hourly rates x level-of-effort hours, sourced from Professional_Staff_Rates.csv and Level_of_Effort.csv |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Method Consistency | All priced lines use PARAMETRIC method — consistent with BASIS_OF_ESTIMATE |

## Scope

| Field | Value |
|---|---|
| Deliverable | DEL-006-07 — Plumbing Calculation Package |
| Package | PKG-006 — Plumbing Design |
| Discipline | Plumbing Engineering |
| Artifact Type | Calculation Package |
| Responsible Party | Plumbing Engineer |
| SOW Reference | SOW-0016 (Complete final plumbing design) |

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) |
|---|---|---|
| PKG-006 | DEL-006-07 | **$11,365.00** |

## Totals by CBS Category

| CBS | Description | Amount (CAD) | % of Total |
|---|---|---|---|
| DESIGN_MGMT | Project Management + Cost Estimating | $1,530.00 | 13.5% |
| DESIGN_PROD | BIM / Production Support | $1,995.00 | 17.6% |
| DESIGN_ENG | Plumbing Engineering | $7,840.00 | 69.0% |
| **TOTAL** | | **$11,365.00** | **100.0%** |

## Effort Breakdown

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| Project Manager | R-01 | 6 | $165 | $990 |
| Cost Estimator | R-08 | 4 | $135 | $540 |
| BIM Technician | R-13 | 21 | $95 | $1,995 |
| Plumbing Engineer | R-18 | 49 | $160 | $7,840 |
| **Total** | | **80** | | **$11,365** |

## Key Warnings and Coverage Gaps

1. **No material/equipment costs included.** This estimate covers professional design labour only. The calculation package is a design-phase deliverable; it does not include procurement of physical plumbing equipment (cistern, pumps, septic tank, fixtures). Those costs belong to construction/installation packages (PKG-014).

2. **LOE hours are parametric estimates.** The 80 total hours (49 hr Plumbing Engineer + 21 hr BIM + 6 hr PM + 4 hr Estimator) are parametric estimates from the Level_of_Effort model. Actual hours may vary based on design complexity, number of design iterations, and scope resolution of open conflict items (CFT-001 through CFT-003).

3. **Scope boundary TBD — Old North Shop plumbing.** CFT-001 in Guidance.md flags that the scope boundary for this calculation package (New North Shop only vs. including Old North Shop renovation plumbing) is unresolved. If scope expands to include Old North Shop, additional engineering hours would be required.

4. **Multiple TBD parameters.** The Datasheet and Specification identify several TBD parameters (occupancy count, simultaneous demand factor, bulk water fill flow rate, mud sump volume, oil/water separator requirement). These do not affect the design labour cost estimate but may affect design complexity and hours if resolution requires additional analysis cycles.

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 17 |
| Items with non-zero pricing | 4 (labour lines DL-001 through DL-004) |
| Items at $0 (effort included in parent) | 13 (calculation sub-artifacts — effort captured in Plumbing Engineer hours) |
| Items with TBD amount | 0 |
| Provenance completeness | 100% — all priced lines have SourceRef to price source files |
