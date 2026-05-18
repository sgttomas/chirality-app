# Estimate Summary — EST_DEL-006-06_2026-02-27_0630

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Professional staff hourly rates x level-of-effort hours |
| **Currency** | CAD |
| **Scope** | DEL-006-06 — Plumbing Fixture Schedule |
| **Package** | PKG-006 — Plumbing Design |
| **Responsible Party** | Plumbing Engineer |
| **Artifact Type** | Schedule (design deliverable) |

## Total by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) | Line Count |
|---|---|---|---|
| PKG-006 | DEL-006-06 | **$11,365.00** | 4 |

## Total by Cost Breakdown Structure (CBS)

| CBS | Amount (CAD) | Line Count |
|---|---|---|
| Professional Services — Management | $1,530.00 | 2 |
| Professional Services — Design | $9,835.00 | 2 |
| **Grand Total** | **$11,365.00** | **4** |

## Staffing Summary

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| Project Manager | R-01 | 6 | $165.00 | $990.00 | 8.7% |
| Cost Estimator | R-08 | 4 | $135.00 | $540.00 | 4.8% |
| BIM Technician | R-13 | 21 | $95.00 | $1,995.00 | 17.6% |
| Plumbing Engineer | R-18 | 49 | $160.00 | $7,840.00 | 69.0% |
| **Total** | | **80** | | **$11,365.00** | **100.0%** |

## Key Observations

1. **Design-heavy deliverable.** 69% of the estimated cost is Plumbing Engineer time (49 hours), reflecting the engineering judgment required for fixture selection, code review, accessibility compliance, and cross-discipline coordination.

2. **This is a professional services estimate only.** The estimate covers the cost to *produce* the Plumbing Fixture Schedule as a design deliverable. It does not include the cost of the plumbing fixtures themselves, their procurement, or their installation (which would fall under PKG-014 Plumbing Installation).

3. **80 total hours** across 4 roles is consistent with the parametric level-of-effort model for a Schedule-type deliverable in the plumbing discipline.

## Warnings and Coverage Gaps

1. **Items.csv includes priceable items (ITEM-005 through ITEM-017) for which no material/equipment pricing is available.** These items represent the fixtures and activities identified in the deliverable documents. Since DEL-006-06 is a design schedule (not a construction deliverable), the cost to produce the schedule is the appropriate pricing scope. Material costs for fixtures would be estimated under PKG-014 or a separate procurement estimate.

2. **Several fixture quantities are TBD** (ITEM-006: sump drains, ITEM-010: Old North Shop washroom fixtures, ITEM-012: New North Shop washroom fixtures). These quantities will be determined during detailed plumbing engineering design and do not affect the professional services estimate.

3. **No plumbing-specific design fee row** exists in Professional_Design_Fees.csv. The LOE-based approach from Level_of_Effort.csv is used instead, which is more granular and appropriate for a single-deliverable estimate.
