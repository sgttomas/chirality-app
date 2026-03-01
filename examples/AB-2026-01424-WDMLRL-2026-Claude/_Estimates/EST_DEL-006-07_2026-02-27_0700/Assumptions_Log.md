# Assumptions Log — EST_DEL-006-07_2026-02-27_0700

## ASM-001 — Hourly Rates Are Current

| Field | Value |
|---|---|
| Assumption | The hourly rates in Professional_Staff_Rates.csv are valid for the 2026 project execution period |
| Source/Basis | Professional_Staff_Rates.csv — all rates listed with Basis=PARAMETRIC, Confidence=MEDIUM |
| Status | OPEN |
| Impact if Invalid | All priced amounts would need recalculation if rates are adjusted (e.g., for inflation, market conditions, or negotiated rates) |

## ASM-002 — LOE Hours Are Sufficient

| Field | Value |
|---|---|
| Assumption | The 80 total hours allocated in Level_of_Effort.csv (49 hr Plumbing Engineer, 21 hr BIM, 6 hr PM, 4 hr Estimator) are sufficient to produce a complete plumbing calculation package for the New North Shop scope |
| Source/Basis | Level_of_Effort.csv — DEL-006-07 rows, Basis=PARAMETRIC |
| Status | OPEN |
| Impact if Invalid | Underestimate if hours are insufficient (e.g., additional design iterations, complex regulatory requirements); overestimate if scope is simpler than modeled |

## ASM-003 — Scope Excludes Old North Shop

| Field | Value |
|---|---|
| Assumption | DEL-006-07 covers only New North Shop addition plumbing calculations; Old North Shop renovation plumbing (CFT-001) is excluded |
| Source/Basis | _CONTEXT.md (description focuses on New North Shop); Guidance.md CFT-001 (scope TBD, human ruling required) |
| Status | OPEN — pending human ruling on CFT-001 |
| Impact if Invalid | Additional Plumbing Engineer hours would be required for Old North Shop washroom, locker room, and laundry plumbing calculations |

## ASM-004 — No Material or Equipment Costs in Scope

| Field | Value |
|---|---|
| Assumption | This estimate covers professional design labour only; no physical materials, equipment procurement, or construction costs are included |
| Source/Basis | DEL-006-07 is a Calculation Package (design-phase artifact); construction and procurement belong to PKG-014 (Plumbing & Water Systems Installation) |
| Status | CONFIRMED — by artifact type |
| Impact if Invalid | N/A — material/equipment costs are properly scoped to construction packages |

## ASM-005 — All Four Roles Required

| Field | Value |
|---|---|
| Assumption | All four roles (PM, Cost Estimator, BIM Technician, Plumbing Engineer) are required for DEL-006-07 production |
| Source/Basis | Level_of_Effort.csv assigns hours to all four roles for DEL-006-07 |
| Status | OPEN |
| Impact if Invalid | If a role is not needed (e.g., BIM support is minimal for a calculation package vs. a drawing set), the estimate includes unnecessary hours. The 21 BIM hours represent 26% of total hours and should be validated against actual calculation package production needs. |

## ASM-006 — Single Calculation Package (No Phased Submission)

| Field | Value |
|---|---|
| Assumption | DEL-006-07 is produced as a single complete calculation package, not as phased or partial submissions |
| Source/Basis | Procedure.md Step 9 describes a single assembly and P.Eng. review process |
| Status | OPEN |
| Impact if Invalid | If phased submissions are required (e.g., preliminary calculations for permit pre-application, then final package), additional coordination and review hours may be needed |

## ASM-007 — Currency Is CAD

| Field | Value |
|---|---|
| Assumption | All costs are in Canadian Dollars (CAD) |
| Source/Basis | Brief specifies CURRENCY=CAD; Assumed_Project_Parameters.csv PP-17 confirms CAD; Professional_Staff_Rates.csv column is HourlyRate_CAD |
| Status | CONFIRMED |
| Impact if Invalid | N/A — currency is confirmed from multiple sources |
