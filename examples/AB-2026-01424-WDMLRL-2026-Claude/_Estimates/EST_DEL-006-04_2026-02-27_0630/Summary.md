# Estimate Summary — EST_DEL-006-04_2026-02-27_0630

## Basis of Estimate Used

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Hours x Hourly Rate (LOE-based) |
| **Currency** | CAD |
| **Scope** | DEL-006-04 — Cistern & Pump Details (Drawing Set) |
| **Package** | PKG-006 — Plumbing Design |
| **Price Sources** | Level_of_Effort.csv (hour allocations) + Professional_Staff_Rates.csv (hourly rates) |
| **Fallback Used** | No — all items priced from primary PARAMETRIC sources |

## Total by Package

| WBS_PackageID | Amount (CAD) |
|---|---|
| PKG-006 | 11,365 |
| **Grand Total** | **11,365** |

## Total by Deliverable

| WBS_DeliverableID | Name | Amount (CAD) |
|---|---|---|
| DEL-006-04 | Cistern & Pump Details | 11,365 |

## Total by CBS

| CBS | Amount (CAD) | % of Total |
|---|---|---|
| Design-Plumbing | 9,835 | 86.5% |
| Management | 1,530 | 13.5% |
| **Total** | **11,365** | **100%** |

## Effort Summary

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-18 | Plumbing Engineer | 49 | 160 | 7,840 |
| R-13 | BIM Technician | 21 | 95 | 1,995 |
| R-01 | Project Manager | 6 | 165 | 990 |
| R-08 | Cost Estimator | 4 | 135 | 540 |
| **Total** | | **80** | | **11,365** |

## Key Warnings and Coverage Gaps

1. **Design deliverable only.** This estimate covers the professional design fee (hours) to produce the Cistern & Pump Details drawing set. It does NOT include material procurement, equipment costs, or construction/installation costs for the cistern and pump systems themselves (those would fall under PKG-014 Plumbing & Water Systems Installation).

2. **Multiple TBD attributes in Datasheet.** The following design parameters remain TBD and could affect design hours if resolution requires additional engineering iterations:
   - Cistern material/type (concrete, fiberglass, polyethylene, or steel)
   - Cistern installation type (above-grade, in-slab, or below-grade)
   - Pump type selection (centrifugal vs. pressure-booster)
   - Pressure tank inclusion decision (pressure tank vs. VFD)
   - Bulk fill pump specifications (flow rate, head, power)
   - Water quality classification (potable vs. non-potable)

3. **No travel/site visit costs included.** Rural site near Ferintosh, Alberta; any site visits for coordination are not costed in the price sources provided.

4. **No external printing/plotting costs included.** IFC drawing reproduction costs not in scope of available price sources.

5. **Two unresolved conflicts** (CONF-001: cistern location physical fit; CONF-002: fire hose pump identity) may generate design rework hours not captured in the parametric LOE allocation.

6. **Hour allocation confidence is MEDIUM.** The Level_of_Effort.csv notes for DEL-006-04 are marked "PKG-006 Plumbing Engineer -- TBD", indicating the LOE allocation is a parametric estimate, not a bottom-up task-level estimate.
