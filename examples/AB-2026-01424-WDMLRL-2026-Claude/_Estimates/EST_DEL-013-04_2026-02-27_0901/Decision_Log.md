# Decision Log — EST_DEL-013-04_2026-02-27_0901

| Decision ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used PARAMETRIC as primary method with ALLOWANCE fallback for equipment items | BASIS_OF_ESTIMATE=PARAMETRIC; FALLBACK_POLICY=ALLOW_PARAMETRIC; ALLOW_MIXED_METHODS=TRUE | 5 of 21 lines use ALLOWANCE method |
| DEC-002 | Assumed 4 exhaust hose drops (2 per repair bay) | Datasheet TBD-DS-01 unresolved; 2 drive-through bays per R-01 §3.1; assumed minimum 2 drops per bay to serve equipment at both ends | Qty directly affects MECHANICAL_EQUIPMENT cost; each additional drop adds ~$9,850 |
| DEC-003 | Assumed 2 exhaust fans (1 per bay) | Fan sizing TBD per TBD-DS-02; assumed distributed fan configuration (1 per bay) as reasonable default | Cost difference between centralized vs. distributed is minor at this scale |
| DEC-004 | Pro-rated MS-04 rate ($9,500/EA) into hose assembly (65%) and fan (35%) components | MS-04 is a combined "vehicle exhaust hose + fan system" rate; split required to price hose drops and fans separately since quantities differ | Allocation percentages are estimates; actual split depends on product selection |
| DEC-005 | Included filtration system as a conditional line item ($8,500) | CQ-002 is unresolved; _CONTEXT.md Scope lists filtration as in-scope; conservative to include | May be removed if direct discharge confirmed; $8,500 impact |
| DEC-006 | Ductwork parametric based on 10% of total building floor area | 13,000 sqft total shop; exhaust ductwork serves 2 repair bays; 10% (~130 m2) is a parametric allocation for trunk + branch duct serving the exhaust system | Ductwork cost is sensitive to this allocation; actual routing TBD |
| DEC-007 | Assumed 2 fire-rated penetrations | Standard for exhaust duct penetrating fire-rated assemblies between shop and exterior/adjacent spaces | Actual count depends on building fire separation layout |
| DEC-008 | Labour hours allocated parametrically: 80 hr ductwork + 32 hr hose/fan + 24 hr support | Based on 2-bay industrial exhaust system scale in 13,000 sqft building with 35 ft ceiling | +/-30% variance expected; refine with contractor input |
| DEC-009 | UPDATE_LATEST_POINTER=FALSE; no pointer file modified | Per run brief instruction | None |
| DEC-010 | Rounding=NONE applied (default) | No rounding instruction provided | Amounts shown to cent precision |
