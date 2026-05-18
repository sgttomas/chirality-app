# Decision Log — EST_DEL-018-06_2026-02-27_0930

## Defaults Applied

| Dec ID | Decision | Rationale |
|--------|----------|-----------|
| DEC-001 | Rounding set to NONE (default) | No rounding specified in brief. |
| DEC-002 | UPDATE_LATEST_POINTER = FALSE | As specified in brief. No pointer file modified. |
| DEC-003 | FALLBACK_POLICY = ALLOW_PARAMETRIC applied | Brief specifies ALLOW_PARAMETRIC. All items without direct evidence are priced as PARAMETRIC allowances rather than left as TBD. |
| DEC-004 | ALLOW_MIXED_METHODS = TRUE | Brief specifies TRUE. In practice all lines used PARAMETRIC method — no mixing occurred. |

## Scope Resolution Decisions

| Dec ID | Decision | Rationale |
|--------|----------|-----------|
| DEC-005 | Scope = DEL-018-06 only (single deliverable) | Brief specifies SCOPE: DEL-018-06. No package-level rollup required. |
| DEC-006 | SOW mapping: SOW-0080 = Natural Gas, SOW-0081 = Electrical, SOW-0082 = Communications | Per Decomposition SS3 and RFP SS3.3.2. Datasheet CONF-001 notes that MEMORY.md and _CONTEXT.md contain incorrect SOW labeling. Decomposition and RFP are authoritative. |
| DEC-007 | Water and sewer excluded from scope | Datasheet explicitly notes water and sewer are NOT in scope for DEL-018-06 despite references in _CONTEXT.md. Decomposition is authoritative. |

## Pricing Decisions

| Dec ID | Decision | Rationale |
|--------|----------|-----------|
| DEC-008 | Trench distance set to 75m (assumed) | No civil design or utility provider data available to determine actual distance. 75m is a parametric estimate for a rural landfill site (building footprint to property boundary/service point). |
| DEC-009 | Gas piping rate derived from UU-01 water line rate ($130/m) | No gas piping rate in Underground_Utility_Rates.csv. Water line installation is comparable scope (buried utility pipe in trench). Used as proxy. |
| DEC-010 | Communication conduit rate derived from UU-03 lower bound ($65/m) | Communications conduit is simpler than power conduit (no high-voltage considerations). Used RateMin from UU-03 as proxy. |
| DEC-011 | Trade labour hours estimated parametrically | No task-level labour breakdown in source documents. Hours estimated based on scope of work: 40 hr plumber (gas service), 48 hr electrician (electrical service), 24 hr equipment operator (trenching), 32 hr labourer (support). |
| DEC-012 | Utility service LS allowances set at $25,000 (gas), $45,000 (electrical), $8,000 (communications) | Parametric estimates for rural Alberta utility service connections. Electrical is highest due to three-phase service complexity. Gas second due to potential infrastructure requirements. Communications lowest as minimal scope (antenna conduit only). |
| DEC-013 | Assumes utility-owned transformer (no customer-owned transformer cost included) | Transformer ownership TBD per REQ-02.9. Estimate assumes the lower-cost scenario (utility-owned). If customer-owned, add $30,000-$80,000. Documented as risk. |
| DEC-014 | No gas main extension cost included | Gas main proximity is TBD. Estimate assumes the site is within reasonable service distance of existing gas infrastructure. If main extension required, add $50,000-$200,000+. Documented as risk. |
| DEC-015 | Building penetration rate set at $1,500/EA | Parametric rate for foundation/wall utility penetration (core drill, sleeve, seal). No rate in source data. |
