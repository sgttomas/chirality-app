# Decision Log — EST_DEL-001-04_2026-02-27_0840

| DecisionID | Decision | Rationale | Source |
|---|---|---|---|
| DEC-001 | Used LOE-based parametric pricing (hours x rates) rather than fee-percentage method | Level_of_Effort.csv provides deliverable-specific hour allocations per role, which is more granular and traceable than applying a percentage fee to an unknown construction value. Professional_Design_Fees.csv was available but not used. | FALLBACK_POLICY: ALLOW_PARAMETRIC; Level_of_Effort.csv; Professional_Staff_Rates.csv |
| DEC-002 | Classified CBS as Design-Management (PM + Cost Estimator) and Design-Architecture (Senior Architect + Architect + BIM Technician) | Aligns with role Category from Professional_Staff_Rates.csv: R-01 and R-08 are Management category; R-11, R-12, R-13 are Design category. CBS labels prefixed with "Design-" to distinguish from construction CBS. | Professional_Staff_Rates.csv Category column |
| DEC-003 | Applied NONE rounding (default) | No rounding instruction was provided in the brief. Default per protocol. | AGENT_ESTIMATING.md PROTOCOL — Inputs |
| DEC-004 | Did not update _LATEST.md pointer | UPDATE_LATEST_POINTER = FALSE per brief. | INIT-TASK brief |
| DEC-005 | Professional_Design_Fees.csv not used | Fee-percentage method requires a known construction value (FeeBase = construction_value). No construction value is available. LOE method is more specific for this deliverable. | Professional_Design_Fees.csv Notes column |
