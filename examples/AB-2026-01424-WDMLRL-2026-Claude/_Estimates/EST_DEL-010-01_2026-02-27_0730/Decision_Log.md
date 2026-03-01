# Decision Log — EST_DEL-010-01_2026-02-27_0730

| DecisionID | Decision | Rationale | Source |
|---|---|---|---|
| DEC-001 | Use PARAMETRIC method for all line items | BASIS_OF_ESTIMATE = PARAMETRIC; ALLOW_MIXED_METHODS = TRUE but no other method sources available | Run brief; AGENT_ESTIMATING protocol |
| DEC-002 | Derive building footprint as 130 ft x 100 ft = ~1208 m2 | Appendix B conceptual drawing dimensions; confirmed by Assumed_Project_Parameters.csv PP-10 (~13,000 sqft) | Datasheet.md Building Foundation Program; PP-10 |
| DEC-003 | Exclude service pit from estimate | Scope boundary between PKG-010 and PKG-011 is unresolved (Conflict CF-010-01); safer to exclude than to double-count | Guidance.md Conflict Table CF-010-01 |
| DEC-004 | Assume normal ground conditions for all quantities | RFP §4.8.2 explicitly directs preliminary estimate to assume normal ground without deleterious material | RFP §4.8.2; Datasheet.md Pricing Structure |
| DEC-005 | Use RecommendedRate from rate tables (not min or max) | RecommendedRate represents the best-estimate parametric rate; min/max used for range context only | Structural_Concrete_Rates.csv; Earthwork_Civil_Rates.csv |
| DEC-006 | Use fully-burdened rates for construction labour | Fully-burdened rates from Construction_Labour_Rates.csv include base wage plus burden multiplier | Construction_Labour_Rates.csv |
| DEC-007 | Exclude steel plate embedments from scope | Steel plate floor embedments are assigned to PKG-011 (DEL-011-02) per Decomposition; Specification.md Out of Scope table confirms | Decomposition §7 PKG-011; Specification.md Out of Scope |
| DEC-008 | Include topsoil stripping as conditional item | RFP §3.3.2 assigns to Proponent "if not already performed by Owner"; included in estimate at full footprint area as conservative approach | RFP §3.3.2; Datasheet.md Site Conditions |
| DEC-009 | Assume perimeter footing is reduced by shared wall with existing building | Existing Old North Shop shares one wall with addition; perimeter reduced from ~140 m to ~92 m | Appendix B drawing; Vocabulary Map (Old North Shop 105 ft x 40 ft adjacent) |
| DEC-010 | Exclude cold-weather premium | Insufficient schedule information to determine if foundation work extends into winter; flagged as warning | Guidance.md C-7; Warning in Summary.md |
| DEC-011 | Use aggregate placement rate for County-supplied material | County supplies aggregate per RFP §3.3.1; Proponent pays for placement only; used same rate as imported fill which may overstate | RFP §3.3.1; Earthwork_Civil_Rates.csv EC-02 |
