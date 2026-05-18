# Decision Log — EST_DEL-01-08_2026-02-18_1500

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS code assigned as PROPOSAL_ADMIN for all DEL-01-08 line items | DEL-01-08 is a Tier 0 / Administrative deliverable. Both roles (HR Coordinator, Proposal Coordinator/Writer) are classified as "Administrative" in Professional_Staff_Rates.csv. No CBSHint was present in the decomposition. Deterministic rule: Administrative roles on Administrative deliverables = PROPOSAL_ADMIN. |
| EST-DEC-002 | Method set to RATE_TABLE for all line items | Hours are sourced from Level_of_Effort.csv and rates from Professional_Staff_Rates.csv. The combination of externally defined quantities and externally defined rates constitutes a RATE_TABLE method. The Level_of_Effort.csv lists its own basis as PARAMETRIC, but the estimating method applied here uses the hours as given quantities priced against rate table rates. ALLOW_MIXED_METHODS=FALSE is satisfied since all lines use RATE_TABLE. |
| EST-DEC-003 | Rounding applied at DOLLAR level | Per brief ROUNDING=DOLLAR. All computed amounts are whole-dollar values (1020, 840) so rounding has no effect on this run. |
| EST-DEC-004 | Assumed_Project_Parameters.csv reviewed but not used for pricing | This source provides project-level context (areas, durations, financial estimates) but contains no inputs directly applicable to DEL-01-08 pricing. Recorded in Source_Index.md as REFERENCE only. |
| EST-DEC-005 | Dependency evidence used for blocker assessment only, not for pricing | Per AGENT_ESTIMATING invariant: "Dependencies are not pricing evidence." Dependency registers inform readiness/blockers. Two upstream prerequisites (DEL-01-07, DEL-01-09) are noted but do not affect pricing computation. |
