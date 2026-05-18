# Decision Log — EST_DEL-006-07_2026-02-27_0700

## DEC-001 — Pricing Method Selection

| Field | Value |
|---|---|
| Decision | Use Level_of_Effort (hours x rate) parametric method rather than Professional_Design_Fees (percentage-of-construction) method |
| Rationale | Level_of_Effort.csv provides DEL-006-07-specific hour allocations by role, yielding more granular and traceable pricing than a discipline-level fee percentage. Additionally, Professional_Design_Fees.csv does not include a plumbing-specific entry (DF-03 covers Mechanical only). |
| Alternatives Considered | Fee-based pricing using DF-03 (Mechanical, 1.6% of construction value) as a proxy for plumbing — rejected because: (a) no plumbing-specific fee entry exists, (b) construction value for plumbing scope is not yet established, (c) LOE method is more direct and traceable. |
| Impact | All 4 priced lines use hours from Level_of_Effort.csv and rates from Professional_Staff_Rates.csv. |

## DEC-002 — Sub-Artifact Pricing Approach

| Field | Value |
|---|---|
| Decision | Price calculation sub-artifacts (ITEM-001 through ITEM-013) at $0 individually, with total engineering effort captured in the Plumbing Engineer role allocation (DL-004, 49 hours) |
| Rationale | The Level_of_Effort model allocates hours by role, not by calculation sub-artifact. The 49-hour Plumbing Engineer allocation covers all engineering tasks (water demand, pipe sizing, pressure drop, drainage, venting, septic, code compliance, assumptions, equipment data, assembly, emergency shower, cistern, washroom). Splitting the 49 hours across 13 sub-artifacts would require sub-allocation assumptions not supported by the price sources. |
| Alternatives Considered | Pro-rata split of 49 hours across 13 sub-artifacts — rejected because no basis exists in the price sources for sub-artifact-level hour allocation. |
| Impact | Items.csv provides the full sub-artifact-level takeoff for scope traceability; Detail.csv prices at the role level to avoid fabricated sub-allocations. |

## DEC-003 — Scope Boundary for Cost Estimate

| Field | Value |
|---|---|
| Decision | Estimate covers professional design labour for DEL-006-07 only (New North Shop plumbing calculation package). Old North Shop renovation plumbing (CFT-001) is excluded pending human ruling. |
| Rationale | _CONTEXT.md description focuses on New North Shop; Guidance.md CFT-001 flags Old North Shop scope as TBD requiring human ruling. Including Old North Shop without authorization would violate the no-invention invariant. |
| Alternatives Considered | Include an allowance for Old North Shop plumbing calculations — rejected because FALLBACK_POLICY = ALLOW_PARAMETRIC, not ALLOW_ALLOWANCE, and no parametric basis exists for the additional scope. |
| Impact | If Old North Shop is later included, a rerun with updated LOE hours will be needed. |

## DEC-004 — CBS Category Assignment

| Field | Value |
|---|---|
| Decision | Assign CBS categories as DESIGN_MGMT (PM + Estimator), DESIGN_PROD (BIM), DESIGN_ENG (Plumbing Engineer + all sub-artifacts) |
| Rationale | CBS categories reflect the functional nature of each role's contribution to the deliverable. No construction or procurement costs are in scope for this design-phase calculation package. |
| Alternatives Considered | Single CBS category (DESIGN) for all lines — rejected because the three-category split provides more useful rollup information. |
| Impact | WBS_CBS_Matrix.csv shows breakdown by functional CBS category. |

## DEC-005 — Rounding Applied

| Field | Value |
|---|---|
| Decision | No rounding applied (ROUNDING = NONE, the default) |
| Rationale | Brief did not specify a rounding policy. All amounts are exact products of integer hours and integer rates. |
| Impact | All amounts are exact; no rounding artifacts. |
