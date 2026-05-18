# Estimate Summary — EST_DEL-001-03_2026-02-27_0545

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method used** | PARAMETRIC (all 5 lines) |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **Fallback used** | No — all items priced from primary sources |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Mixed methods used** | No — all lines use PARAMETRIC |

## Scope

| Field | Value |
|---|---|
| **Deliverable** | DEL-001-03 — Exterior Elevations |
| **Package** | PKG-001 — Architectural Design |
| **Discipline** | Architect |
| **Type** | Drawing Set |
| **SOW** | SOW-0011 (Complete final architectural design for the addition) |

## Totals by CBS

| CBS | Amount (CAD) | Line Count | % of Total |
|---|---|---|---|
| Design | 17,670 | 3 | 92.0% |
| Management | 1,530 | 2 | 8.0% |
| **TOTAL** | **19,200** | **5** | **100.0%** |

## Totals by Role

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| Senior Architect | R-11 | 54 | 180 | 9,720 | 50.6% |
| Architect | R-12 | 42 | 135 | 5,670 | 29.5% |
| BIM Technician | R-13 | 24 | 95 | 2,280 | 11.9% |
| Project Manager | R-01 | 6 | 165 | 990 | 5.2% |
| Cost Estimator | R-08 | 4 | 135 | 540 | 2.8% |
| **TOTAL** | — | **130** | — | **$19,200** | **100.0%** |

## Pricing Coverage

| Metric | Value |
|---|---|
| Items in takeoff (Items.csv) | 5 |
| Items priced (Detail.csv) | 5 |
| Items TBD | 0 |
| Pricing coverage | 100% |
| Provenance completeness | 100% (all SourceRef populated) |

## Key Observations

1. **Complete pricing.** All 5 line items are fully priced using parametric rates from Level_of_Effort.csv (hours) and Professional_Staff_Rates.csv (hourly rates). No TBDs or fallbacks required.

2. **Design-effort estimate only.** This estimate covers the professional design effort to produce the Exterior Elevations drawing set. It does not include:
   - Construction costs for exterior materials, cladding, doors, or finishes
   - Permit fees or AHJ review fees
   - Printing or reproduction costs
   - Travel or site visit costs (if any)

3. **Hours are parametric.** The Level_of_Effort.csv assigns DEL-001-03 the same hour profile as other PKG-001 Drawing Set deliverables (54h Senior Architect, 42h Architect, 24h BIM Technician, 6h PM, 4h Cost Estimator = 130h total). This is a parametric allocation based on deliverable type, not a bottom-up task estimate.

4. **Confidence: MEDIUM.** All rates and hours are tagged MEDIUM confidence in the source files, reflecting parametric estimates rather than firm quotes or historical actuals.

## Warnings

None. All inputs available; all items priced; no fallbacks used.
