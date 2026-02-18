# Decision Log -- EST_DEL-10-02_2026-02-18_1900

| DecID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS codes assigned as GR-PM (PM hours) and GR-DESIGN (civil + geotech hours) | No CBSHint in decomposition. Proposal production professional services for a narrative deliverable map to General Requirements CBS. PM coordination = GR-PM; technical review = GR-DESIGN. |
| EST-D-002 | All line items priced as RATE_TABLE (no fallback needed) | Level_of_Effort.csv provides explicit hours for all 3 roles on DEL-10-02; Professional_Staff_Rates.csv provides rates for all 3 RoleIDs. No gaps; FALLBACK_POLICY=STRICT not triggered. |
| EST-D-003 | Rounding applied at line item level to nearest dollar | ROUNDING=DOLLAR. All line item amounts (1400, 930, 620) are already whole dollars since rates and hours are whole numbers. No rounding adjustment needed. |
| EST-D-004 | Assumed_Project_Parameters.csv reviewed but not used for direct pricing | DEL-10-02 is a narrative deliverable. No area/quantity parametric drivers apply. Parameters file is informational context only. |
| EST-D-005 | Upstream document blockers (geotech, wetland, environmental, flood mapping) do not block the estimate | These block deliverable *production* (content authoring) but not *estimating*. The level of effort to summarize reference reports is determined by report complexity and scope, which is already captured in the LoE hours. |
