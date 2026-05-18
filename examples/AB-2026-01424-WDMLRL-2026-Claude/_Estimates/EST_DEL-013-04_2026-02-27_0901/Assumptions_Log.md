# Assumptions Log — EST_DEL-013-04_2026-02-27_0901

| Assumption ID | Assumption | Basis | Impact if Wrong | Confidence |
|---|---|---|---|---|
| ASM-001 | 4 exhaust hose drops total (2 per repair bay) | R-01 §3.1 confirms 2 drive-through bays; Datasheet TBD-DS-01 unresolved | Each additional or fewer drop shifts equipment cost by ~$9,850 | LOW |
| ASM-002 | 2 exhaust fans total (1 per bay, distributed configuration) | Trade-off Option B in Guidance; reasonable default for 2-bay system | Centralized (1 fan) would reduce fan count but increase duct complexity; net cost impact moderate | MEDIUM |
| ASM-003 | Ductwork material is galvanized steel per SMACNA | Datasheet ASSUMPTION; standard for industrial exhaust | Stainless steel would increase ductwork cost by 50-100% | MEDIUM |
| ASM-004 | Ductwork allocation is ~10% of total building floor area (130 m2 equivalent) | Parametric estimate for exhaust trunk + branch duct in a 13,000 sqft building | If ductwork runs are longer (e.g., remote fan location), cost increases proportionally | MEDIUM |
| ASM-005 | Filtration system included at $8,500 (conditional on CQ-002) | _CONTEXT.md lists filtration in scope; CQ-002 unresolved | If direct discharge confirmed, $8,500 can be removed; if multi-stage filtration required, cost could be $15,000+ | LOW |
| ASM-006 | Equipment is diesel-powered (primary exhaust hazards: DPM, CO, NOx) | Guidance Equipment Type Uncertainty; landfill heavy equipment context | If gasoline-only or mixed fleet, filtration and exhaust classification may change | MEDIUM |
| ASM-007 | Construction labour hours: 80 hr duct + 32 hr hose/fan + 24 hr labourer | Parametric for 2-bay industrial exhaust install with 35 ft ceiling | Actual hours depend on duct routing complexity, hose type (fixed vs. retractable), and site conditions | LOW-MEDIUM |
| ASM-008 | 2 fire-rated penetrations required | Standard assumption for exhaust duct through building fire separations | If more separations exist (e.g., mezzanine, adjacent occupancies), additional penetrations needed at ~$850 each | MEDIUM |
| ASM-009 | Controls cost at $5,500 covers fan interlock + alarm panel + wiring for 2-fan system | Parametric; functional spec TBD per TBD-DS-05 | Complex BMS integration or remote monitoring could increase to $8,000-$12,000 | LOW |
| ASM-010 | No heat recovery interface included (treated as design evaluation per CQ-001) | Guidance CQ-001; assumed not cost-effective at this scale | If heat recovery is required, add $5,000-$15,000 for heat exchanger and controls | MEDIUM |
| ASM-011 | Commissioning: 16 hr commissioning agent + 8 hr mech contractor + instruments | Parametric for single exhaust system commissioning | If air quality sampling (hygienist) required, add ~$3,000-$5,000 | MEDIUM |
