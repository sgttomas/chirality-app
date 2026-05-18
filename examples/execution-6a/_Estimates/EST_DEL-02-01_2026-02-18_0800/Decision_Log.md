# Decision Log — EST_DEL-02-01_2026-02-18_0800

## Run Decisions

| DecisionID | Category | Decision | Rationale | Affected Lines |
|---|---|---|---|---|
| DEC-R-001 | Method interpretation | DF-01 (architectural fee as % of construction cost) treated as RATE_TABLE method | DF-01 is a rate table entry expressing a fee percentage rate (7.0%); this is consistent with RATE_TABLE basis since the rate is sourced from Professional_Design_Fees.csv, a rate table file | L-010 |
| DEC-R-002 | Computation dependency | Design fee (L-010) set to TBD because the construction subtotal it depends on is incomplete | DF-01 requires a base construction cost to apply the 7% rate. With 7 of 9 construction line items at TBD, the subtotal is not meaningful. Fee will be computable when construction lines are priced. | L-010 |
| DEC-R-003 | Missing source — ceiling | Ceiling system (L-006) set to TBD per STRICT fallback policy | No rate table entry for suspended acoustical ceiling tile or any ceiling system in any of the 8 provided PRICE_SOURCES files. Cannot price without evidence. | L-006 |
| DEC-R-004 | Missing source — accessibility | Accessibility features (L-007) set to TBD per STRICT fallback policy | No rate table entry for accessibility provisions (ramps, tactile indicators, barrier-free hardware, accessible signage) in any provided source. Alberta Building Code requirements confirmed in SOW-0219 but no cost data provided. | L-007 |
| DEC-R-005 | Missing source — signage | Code-required signage (L-008) set to TBD per STRICT fallback policy | No rate table entry for exit signs, room identification, accessibility signage, or fire signage in any provided source. SOW-0229 confirms base scope inclusion. | L-008 |
| DEC-R-006 | Missing source — partitions | Interior partitions (L-004) set to TBD per STRICT fallback policy | No rate table entry for metal stud + gypsum board interior partitions in any provided source. Carpenter labour rate (T-02, $72/hr) available but not sufficient to derive a combined material+labour rate. | L-004 |
| DEC-R-007 | Missing source — floor finish | Sealed concrete floor finish (L-005) set to TBD per STRICT fallback policy | SC-03 and SC-04 in Structural_Concrete_Rates.csv cover complete slab-on-grade (which is DEL-02-04 structural scope). No finish-only rate (sealer/hardener application) is available. | L-005 |
| DEC-R-008 | Missing source — paint | Interior paint (L-009) set to TBD per STRICT fallback policy | T-12 painter labour rate ($60/hr) available, but no combined material+labour painting rate ($/sf) is provided. Cannot derive a reliable rate from labour-only data without material cost and productivity assumptions. | L-009 |
| DEC-R-009 | Scope boundary — bay flooring | Bay area sealed concrete floors attributed to DEL-02-04 (structural slab), not DEL-02-01 | The concrete slab-on-grade (SC-03/SC-04) is a structural element. The sealer/hardener finish on bay floors is a minor additive cost; however, bay functional fit-up belongs to DEL-02-02 and DEL-02-03 per cost ownership rules. DEL-02-01 owns office/shared area floor finishes only. | L-005 |
| DEC-R-010 | Door count | 18 single doors + 1 double door = 19 openings estimated for office/admin/shared areas | Derived from room list in Datasheet.md: 7 offices (2 exec + 5 regular) + 2 washrooms + 1 kitchen + 1 meeting room + 4 utility/custodial/IT + 2 misc = 17 single + 1 double (meeting room) + 1 additional for circulation = 18 single + 1 double. See ASM-004. | L-001, L-002, L-003 |

## Defaults Applied

| Default | Value | Notes |
|---|---|---|
| FALLBACK_POLICY | STRICT | No items priced without direct rate table evidence |
| ALLOW_MIXED_METHODS | FALSE | All methods = RATE_TABLE |
| ROUNDING | DOLLAR | Applied to all computed amounts |
| UPDATE_LATEST_POINTER | FALSE | No pointer file modified |
| CBS mapping | Deterministic rule documented in Run_Context.md | 3100=design fees, 3200=partitions, 3300=doors, 3400=finishes, 3500=accessibility, 3600=signage |
