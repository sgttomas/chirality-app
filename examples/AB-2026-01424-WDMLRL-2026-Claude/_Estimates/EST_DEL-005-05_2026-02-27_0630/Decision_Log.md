# Decision Log — EST_DEL-005-05_2026-02-27_0630

## Defaults Applied

| ID | Decision | Rationale |
|---|---|---|
| DEC-001 | Rounding set to NONE (default) | ROUNDING not specified in brief; default applied per protocol. |
| DEC-002 | UPDATE_LATEST_POINTER = FALSE | Explicitly set in brief; no pointer file modified. |
| DEC-003 | OUTPUT_LABEL = DEL-005-05 | Explicitly set in brief. |

## Scope Resolution

| ID | Decision | Rationale |
|---|---|---|
| DEC-004 | Scope resolved to single deliverable DEL-005-05 (Civil Sections & Details) under PKG-005 (Civil Design). | SCOPE field in brief specified DEL-005-05. Deliverable folder located at PKG-005_Civil Design/1_Working/DEL-005-05_Civil-Sections/. All 4 production documents found and read. |

## Pricing Method

| ID | Decision | Rationale |
|---|---|---|
| DEC-005 | Pricing method: PARAMETRIC using staff hours x hourly rates. | BASIS_OF_ESTIMATE = PARAMETRIC. Level_of_Effort.csv provides role-specific hours for DEL-005-05. Professional_Staff_Rates.csv provides corresponding hourly rates. This is a professional design services deliverable (drawing set) — staff-hours-based pricing is the natural parametric approach. |
| DEC-006 | Professional_Design_Fees.csv (DF-05) not used for primary pricing; retained for cross-check reference only. | Fee-percentage method requires a construction_value input that is not available for a single-deliverable estimate run. Staff-hours method provides a more granular and directly substantiated estimate. |
| DEC-007 | Items ITM-005 through ITM-019 recorded as scope-tracking items, not independently priced. | These items represent individual design activities and drawing elements whose costs are captured within the staff-hour allocations (ITM-001 through ITM-004). Independent pricing would require activity-level LOE decomposition not available in the current pricing sources. Recording them ensures scope traceability without double-counting. |

## Fallback Uses

| ID | Decision | Rationale |
|---|---|---|
| — | No fallback required. | All 4 priceable items were priced using PARAMETRIC method from primary sources. FALLBACK_POLICY (ALLOW_PARAMETRIC) was not invoked. |

## CBS Assignment

| ID | Decision | Rationale |
|---|---|---|
| DEC-008 | CBS categories assigned as Professional Services — Management (PM, Cost Estimator) and Professional Services — Design (BIM Technician, Civil Engineer). | Based on Category field in Professional_Staff_Rates.csv: R-01 and R-08 are Management; R-13 and R-17 are Design. |
