# Decision Log -- DEL-01-02

**RunID:** EST_DEL-01-02_2026-02-18_2359

---

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-0102-01 | CBS = ADMIN assigned to R-22 Proposal Coordinator line item | Role category in Professional_Staff_Rates.csv is Administrative; deterministic mapping rule applied consistently across all estimate snapshots |
| DEC-EST-0102-02 | CBS = MGMT assigned to R-02 Project Manager line item | Role category in Professional_Staff_Rates.csv is Management; deterministic mapping rule applied consistently across all estimate snapshots |
| DEC-EST-0102-03 | Rounding applied at DOLLAR level to all amounts | Per brief ROUNDING=DOLLAR. Both computed amounts ($1,680 and $700) are already whole dollar amounts; no rounding adjustment required |
| DEC-EST-0102-04 | Dependencies from Dependencies.csv used for blocker reporting only, not for pricing | Per AGENT_ESTIMATING invariant: "Dependencies are not pricing evidence." 18 dependencies recorded in Blockers.md for sequencing context |
| DEC-EST-0102-05 | Assumed_Project_Parameters.csv listed as context-only source for DEL-01-02 | No parameters in the file directly affect DEL-01-02 pricing (no area, quantity, or financial parameters apply to final PDF assembly) |
| DEC-EST-0102-06 | DEL-01-02 treated as pure production cost with no content creation hours | Per brief: "This is PURE PRODUCTION COST -- the final assembly of all other deliverable outputs." All substantive content production costs belong to their respective deliverables |
