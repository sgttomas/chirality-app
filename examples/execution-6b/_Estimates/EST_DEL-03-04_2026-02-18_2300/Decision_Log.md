# Decision Log

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS assigned as `PROF_SERVICES_DESIGN` for all DEL-03-04 line items | All work for the mechanical design brief is professional engineering services (design-phase narrative authoring). No construction, procurement, or specialty consulting costs apply. Deterministic mapping rule documented in Run_Context.md. |
| EST-D-002 | Single line item produced (one role: R-11 Mechanical Engineer Senior) | Level_of_Effort.csv assigns only one role to DEL-03-04. No additional roles are indicated in the source data. This is consistent with the deliverable being a single-author narrative. |
| EST-D-003 | No fallback pricing applied | All required pricing inputs (hours and rates) are available in the designated price sources. FALLBACK_POLICY = STRICT is satisfied without requiring any TBD amounts. |
| EST-D-004 | Rounding applied at DOLLAR level | Per brief instruction ROUNDING=DOLLAR. Amount of $1,600 is already a whole dollar figure; no rounding adjustment needed. |
| EST-D-005 | Assumed_Project_Parameters.csv reviewed but not used for pricing | Project parameters provide context (building areas, bay counts) but do not directly factor into professional services hours for a narrative deliverable. No parametric scaling was applied. |
