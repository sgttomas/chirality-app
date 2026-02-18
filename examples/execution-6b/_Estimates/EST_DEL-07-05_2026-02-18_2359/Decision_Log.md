# Decision Log

**RunID:** EST_DEL-07-05_2026-02-18_2359
**Date:** 2026-02-18

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS code `MGMT` assigned to both line items | Both roles (Quality Lead R-23 = Management category; Project Manager R-02 = Management category) map to Management per Professional_Staff_Rates.csv Category column. Deterministic rule: CBS = role Category. |
| EST-DEC-002 | No fallback methods used | FALLBACK_POLICY = STRICT and all line items have direct rate table evidence. No TBD amounts needed. |
| EST-DEC-003 | Rounding applied at DOLLAR level | Per brief ROUNDING = DOLLAR. Both computed amounts ($1,040 and $700) are already whole-dollar values; no rounding adjustment needed. |
| EST-DEC-004 | Dependencies used for blocker assessment only, not pricing | Per AGENT_ESTIMATING invariant: "Dependencies are not pricing evidence." All 13 dependency rows inform readiness; none affect unit rates or quantities. |
| EST-DEC-005 | Assumed_Project_Parameters.csv indexed but not used for pricing | File provides project-level context (areas, durations, financial parameters) not applicable to DEL-07-05 staff-hours pricing. Indexed in Source_Index.md for audit trail. |
| EST-DEC-006 | Cost ownership boundary: construction QC in DEL-07-05, design QC plan in DEL-06-02 | Per brief BOE context: "construction QC is in DEL-07-05" and "NOT in DEL-06-02 which covers design QC plan in PKG-006." DEL-07-05 covers the quality management narrative including design QC, construction QC, commissioning QC, and documentation QC domains. DEL-06-02 covers the design documents plan with its own QC checkpoints. No overlap in hours. |
