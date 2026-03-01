# Decision Log — EST_DEL-020-03_2026-02-27_0900

| Decision ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used PARAMETRIC method for all 8 line items | BASIS_OF_ESTIMATE = PARAMETRIC; Level_of_Effort.csv and Professional_Staff_Rates.csv both provide PARAMETRIC data with MEDIUM confidence. No fallback needed. | All lines consistently use PARAMETRIC method |
| DEC-002 | CBS categories assigned based on Professional_Staff_Rates.csv Category column | Rate table categorizes each role as Management, Construction, Admin, or Specialty. Used these categories directly as CBS values. | WBS_CBS_Matrix rollups reflect rate-table categories |
| DEC-003 | Scope resolved as single deliverable DEL-020-03 | SCOPE input = DEL-020-03; confirmed in decomposition as DEL-020-03_Closeout-Docs under PKG-020 | 1 deliverable estimated |
| DEC-004 | Quantity takeoff based on Level_of_Effort.csv allocations rather than independent bottom-up estimate | Level_of_Effort.csv provides pre-calculated hour allocations per role for DEL-020-03. These allocations are consistent with the scope described in the four deliverable documents. Used as-is. | 8 line items extracted, 80 total hours |
| DEC-005 | Optional items (OPT-01, OPT-02) from Optional_Items_Pricing.csv excluded | Optional items cover winter conditions and contaminated soils handling — not applicable to closeout documentation scope | No allowance items included |
| DEC-006 | No rounding applied | ROUNDING default = NONE; no explicit rounding instruction in brief | Amounts reported to cent precision |
| DEC-007 | UPDATE_LATEST_POINTER = FALSE respected | Brief specifies FALSE; no pointer file modified | _LATEST.md not touched |
