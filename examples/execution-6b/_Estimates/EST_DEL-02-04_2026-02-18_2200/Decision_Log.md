# Decision Log -- EST_DEL-02-04_2026-02-18_2200

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | CBS assigned as DESIGN_SERVICES for all DEL-02-04 line items | Both roles (R-11 Mechanical Engineer Senior, R-12 Mechanical Engineer Intermediate) are categorized as "Design" in Professional_Staff_Rates.csv. Deterministic mapping rule: Design-category roles map to CBS = DESIGN_SERVICES. Documented in Run_Context.md. |
| EST-D-002 | Hours sourced from Level_of_Effort.csv rows where Execution=6b and DeliverableID=DEL-02-04 | Two matching rows found: R-11 (16 hrs) and R-12 (8 hrs). No filtering ambiguity. |
| EST-D-003 | Rates sourced from Professional_Staff_Rates.csv matched by RoleID | R-11 = $160/hr CAD, R-12 = $130/hr CAD. Direct lookup; no interpolation needed. |
| EST-D-004 | Rounding applied as DOLLAR (nearest whole dollar) | Per brief. Amounts are already whole dollars (2560, 1040); no rounding adjustment was needed. |
| EST-D-005 | Assumed_Project_Parameters.csv treated as context-only, not direct pricing input | Parameters (building area, bay counts, equipment quantities) provide context for the mechanical scope but do not directly determine hours or rates for the proposal narrative production cost. |
| EST-D-006 | Dependencies treated as informational for sequencing; no pricing blockers identified | Upstream prerequisites (DEL-02-01, DEL-02-02, DEL-02-03) affect production sequencing but not the cost to produce the narrative. Hours are proposal production effort, not construction. |
| EST-D-007 | Mechanical concept scope boundaries per brief Cost Ownership Rules | Mechanical NARRATIVE cost owned entirely by DEL-02-04; Addendum 03 mechanical requirements (exhaust, generator, fill stations) costed here, not in DEL-02-01 or DEL-02-05. This is a pass-through of brief instructions, not an agent decision. |
