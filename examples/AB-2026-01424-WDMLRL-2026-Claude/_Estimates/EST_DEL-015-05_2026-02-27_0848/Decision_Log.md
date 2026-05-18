# Decision Log — EST_DEL-015-05_2026-02-27_0848

## Defaults Applied

| ID | Decision | Rationale |
|---|---|---|
| DEC-001 | Rounding set to NONE (default) | No ROUNDING parameter provided in brief; default applied per protocol |
| DEC-002 | UPDATE_LATEST_POINTER = FALSE | Per brief instruction; no pointer file modified |
| DEC-003 | RUN_TIMESTAMP generated at runtime (2026-02-27T08:48Z) | No RUN_TIMESTAMP provided in brief |

## Scope Resolution Decisions

| ID | Decision | Rationale |
|---|---|---|
| DEC-004 | Scope interpreted as wiring/conduit rough-in only | SOW-0064 says "wiring for security cameras" and SOW-0065 says "antenna wire for 2-way radios" -- language implies wiring/conduit scope, not equipment supply. Consistent with Datasheet ASSUMPTION and Guidance Principle 3. CONF-015-05-01/02 remain TBD. |
| DEC-005 | Excluded camera hardware, NVR, radio base stations, antenna hardware from estimate | Per DEC-004; these items are assumed Owner-furnished or separately specified |
| DEC-006 | Excluded data networking / structured cabling from estimate | Not referenced in RFP or decomposition for DEL-015-05; per Specification §Excluded |

## Fallback Uses

| ID | Decision | Rationale |
|---|---|---|
| DEC-007 | All items priced via PARAMETRIC method | Consistent with BASIS_OF_ESTIMATE=PARAMETRIC. No fallback required. FALLBACK_POLICY=ALLOW_PARAMETRIC would permit PARAMETRIC fallback if needed, but primary basis already matches. |

## Pricing Model Decisions

| ID | Decision | Rationale |
|---|---|---|
| DEC-008 | Used ES-05 ($280/ea) from Electrical_System_Rates.csv for security camera rough-in | Direct match: ES-05 "Security camera rough-in (cable + box)" |
| DEC-009 | Derived antenna rough-in rate ($450/ea) from ES-05 + labour premium | No direct antenna rough-in rate in sources; adapted ES-05 with premium for exterior penetration and weatherproofing |
| DEC-010 | Derived conduit rate ($22/m) from material estimate + T-04 labour rate | No direct conduit per-meter rate in Electrical_System_Rates.csv; parametric derivation from material + install labour |
| DEC-011 | Used T-04 Electrician fully burdened rate ($96/hr) for all direct installation labour | Direct match from Construction_Labour_Rates.csv |
| DEC-012 | Used Level_of_Effort.csv hours and Professional_Staff_Rates.csv rates for management/QA/HSE lines | Direct match: 6 rows in LoE for DEL-015-05 mapped to corresponding staff rates |
