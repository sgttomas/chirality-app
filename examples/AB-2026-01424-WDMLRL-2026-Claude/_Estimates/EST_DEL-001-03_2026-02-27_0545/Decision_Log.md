# Decision Log — EST_DEL-001-03_2026-02-27_0545

## Defaults Applied

| DEC-ID | Decision | Rationale |
|---|---|---|
| DEC-001 | Used Level_of_Effort.csv as the primary hour source for DEL-001-03 | LOE data provides deliverable-specific hour allocations by role; directly applicable to PARAMETRIC basis |
| DEC-002 | Used Professional_Staff_Rates.csv as the primary rate source | Staff rate table provides hourly rates for all 5 roles assigned to DEL-001-03 in LOE data |
| DEC-003 | Classified items as UNIT_RATE (hours * rate) rather than LUMP_SUM | Deliverable effort is naturally decomposed by role and hours; UNIT_RATE provides better traceability than a lump sum |
| DEC-004 | Did not use Professional_Design_Fees.csv (fee-percentage approach) | LOE-based pricing provides more granular traceability than a percentage-of-construction-value fee; LOE data is directly available for this deliverable |
| DEC-005 | Did not use Parametric_Building_Rates.csv | Building rates apply to construction costs, not design effort; out of scope for this deliverable estimate |
| DEC-006 | CBS categories assigned as "Design" for architect/BIM roles and "Management" for PM/estimator roles | Consistent with the Category column in Professional_Staff_Rates.csv (R-11/R-12/R-13 = Design; R-01 = Management; R-08 = Management) |
| DEC-007 | UPDATE_LATEST_POINTER = FALSE; no pointer file modified | Per INIT-TASK brief instruction |

## Fallback Uses

None. All items priced from primary PARAMETRIC sources.

## Scope Resolution Decisions

| Decision | Detail |
|---|---|
| Scope limited to DEL-001-03 only | Per INIT-TASK brief; single deliverable estimate |
| Design effort only (no construction costs) | Exterior Elevations is a Drawing Set deliverable; the estimate covers the professional effort to produce the drawings, not the construction scope depicted on them |
