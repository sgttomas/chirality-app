# Decision_Log.md
## EST_DEL-009-02_2026-02-27_0600

---

| Decision ID | Decision | Rationale | Impact |
|-------------|----------|-----------|--------|
| DEC-001 | Used PARAMETRIC method for all line items | BASIS_OF_ESTIMATE = PARAMETRIC; all pricing sources are parametric-basis; no quotes, historical data, or allowance tables available | All 15 lines use Method=PARAMETRIC; consistent with brief |
| DEC-002 | Estimated Permitting Specialist (R-22) hours parametrically from Procedure.md scope | LOE source (Level_of_Effort.csv) does not include R-22 for DEL-009-02; FALLBACK_POLICY = ALLOW_PARAMETRIC permits parametric estimation | 40 hrs allocated across 5 procedure phases (8+12+6+4+10); largest cost component at $5,000 |
| DEC-003 | Included design discipline review hours (R-11, R-14, R-15, R-16, R-17, R-18) | Specification REQ-009-02-03 requires P.Eng.-stamped IFC drawings across 6 disciplines; review for permit completeness is within DEL-009-02 scope | 14 hrs across 6 roles totaling $2,030; note that underlying design work is in PKG-001-006 |
| DEC-004 | Included Document Controller (R-09) hours | Datasheet Construction section describes a multi-component artifact set requiring compilation from 6 disciplines | 6 hrs at $75/hr = $450 |
| DEC-005 | Set permit fee amount to $0 | Datasheet Attributes explicitly state County pays fees (R-01, §3.3.1; SOW-0202); Guidance Principle 3 confirms exclusion | L-015 Amount = $0; recorded for completeness but excluded from Proponent cost |
| DEC-006 | Did not estimate re-submission effort (Step 9A) as a separate line item | Procedure Step 9A describes a rejection/re-submission workflow but this is a contingency scenario; base estimate assumes successful first submission | If re-submission occurs, additional Permitting Specialist and design review hours would be needed |
| DEC-007 | Applied hourly rates directly from Professional_Staff_Rates.csv without adjustments | Rates are labeled PARAMETRIC/MEDIUM confidence; no project-specific rate adjustments or multipliers provided in pricing sources | All rates used as-is in CAD |
| DEC-008 | CBS categories mapped to Professional_Staff_Rates.csv Category column | Rate table provides Category (Management, Construction, Admin, Design, Specialty); used directly as CBS | Consistent with source data structure |
| DEC-009 | UPDATE_LATEST_POINTER = FALSE; no pointer file modified | Per brief instruction | No _LATEST.md created or modified |
