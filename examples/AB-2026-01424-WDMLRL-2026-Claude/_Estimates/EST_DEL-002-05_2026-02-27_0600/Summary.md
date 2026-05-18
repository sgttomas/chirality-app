# Estimate Summary — EST_DEL-002-05_2026-02-27_0600

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Level-of-effort hours (from Level_of_Effort.csv) multiplied by professional staff hourly rates (from Professional_Staff_Rates.csv). Lump-sum items priced as parametric effort allowances using structural engineer rate and assumed hours. |
| **Currency** | CAD |
| **Fallback Policy** | ALLOW_PARAMETRIC |
| **Mixed Methods** | TRUE (all items are PARAMETRIC in this run) |

## Scope

| Field | Value |
|---|---|
| **Deliverable** | DEL-002-05 Mezzanine Framing Details |
| **Package** | PKG-002 Structural Design |
| **Discipline** | Structural Engineering |
| **Type** | Drawing Set |
| **SOW Coverage** | SOW-0012, SOW-0032, SOW-0033, SOW-0034 |

## Totals by CBS

| CBS | Amount (CAD) | Line Count | % of Total |
|---|---|---|---|
| Design-Structural | 21,780 | 7 | 78.5% |
| Management | 1,870 | 3 | 6.7% |
| Construction-Support | 4,080 | 2 | 14.7% |
| **TOTAL** | **27,730** | **12** | **100%** |

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) |
|---|---|---|
| PKG-002 | DEL-002-05 | 27,730 |

## Hour Breakdown (from Level_of_Effort.csv — direct hours only)

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| Structural Engineer (R-14) | 84 | 170 | 14,280 |
| BIM Technician (R-13) | 36 | 95 | 3,420 |
| Project Manager (R-01) | 6 | 165 | 990 |
| Cost Estimator (R-08) | 4 | 135 | 540 |
| **Subtotal (direct LOE)** | **130** | | **19,230** |

## Parametric Allowances (lump-sum items)

| Item | Assumed Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| Internal QA review | 8 | 170 | 1,360 |
| Multi-discipline coordination | 6 | 170 | 1,020 |
| Shop drawing review | 8 | 170 | 1,360 |
| Field reviews and inspection | 16 | 170 | 2,720 |
| Corrosion protection spec | 4 | 170 | 680 |
| Seismic determination | 4 | 170 | 680 |
| Fire protection determination | 2 | 170 | 340 |
| Permit submission support | 2 | 170 | 340 |
| **Subtotal (parametric allowances)** | **50** | | **8,500** |

## Grand Total

| Component | Amount (CAD) |
|---|---|
| Direct LOE (from Level_of_Effort.csv) | 19,230 |
| Parametric allowances (lump-sum) | 8,500 |
| **Grand Total** | **27,730** |

## Key Warnings and Coverage Gaps

1. **Lump-sum items are parametric estimates.** The 8 lump-sum items (ITEM-005 through ITEM-012) totalling $8,500 CAD are effort-based parametric allowances. Hour assumptions are recorded in Assumptions_Log.md. These should be validated against actual project experience.

2. **Construction support scope uncertainty.** Field review hours (ITEM-008, 16 hrs) are a parametric allowance. Actual field review effort depends on construction complexity, contractor quality, and inspection schedule. This item has the highest variability risk.

3. **Conditional items.** ITEM-009 (corrosion protection specification, $680) is conditional on CF-DS-002 ruling (whether mezzanine extends over wash bay). If the mezzanine does not extend over the wash bay, this item may be reduced or eliminated.

4. **This estimate covers professional design services only.** It does not include construction material costs, fabrication, erection labour, or other hard costs for the mezzanine structure itself. The scope is the production of the drawing set deliverable (DEL-002-05).

5. **Rate confidence is MEDIUM.** All staff rates are stated as PARAMETRIC basis with MEDIUM confidence per Professional_Staff_Rates.csv.
