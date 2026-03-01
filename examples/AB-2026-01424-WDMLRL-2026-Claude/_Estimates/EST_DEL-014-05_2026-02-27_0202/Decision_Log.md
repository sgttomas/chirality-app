# Decision_Log — EST_DEL-014-05_2026-02-27_0202

## Decisions

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-01 | PARAMETRIC fallback applied for 5 material line items (L-01 through L-05) where no pricing evidence exists in PRICE_SOURCES | FALLBACK_POLICY = ALLOW_PARAMETRIC permits parametric estimation for items without direct evidence. Material items (emergency shower unit, TMV, piping, supports, signage) have no quotes or rate table entries in any provided source file. | $4,550.00 of $13,052.80 total (34.9%) is LOW confidence. Recommend quote replacement. |
| DEC-02 | Emergency shower priced as combination shower/eyewash unit at $2,800 (midpoint of $2,000-$4,000 parametric range) | ASSUMPTION per CF-002. Guidance T-1 recommends defaulting to combination unit. Industrial maintenance shop environment warrants combination type. | If shower-only is confirmed, material cost may reduce by $500-$1,000. |
| DEC-03 | Thermostatic mixing valve included at $650 | ASSUMPTION per CF-001. Guidance P-4 states tepid water is a design requirement, not optional. In Alberta climate with cistern-fed cold water, TMV is likely required. | If TMV is not required, remove $650 material + some labour savings. |
| DEC-04 | Plumber installation labour estimated at 16 hours (rough-in through pressure test) | Parametric estimate for a single emergency shower installation: mark-out (1h), supply piping installation (6h), TMV installation (2h), unit mounting and connections (4h), pressure test and leak check (2h), cleanup (1h). | MEDIUM confidence. Actual hours depend on piping routing complexity and site conditions. |
| DEC-05 | Commissioning labour estimated at 4 hours | Procedure Step 9 requires 15-min timed flow test plus temperature measurement, activation test, drain performance observation, and documentation. Setup/teardown, instrument calibration, and record writing add overhead. | MEDIUM confidence. |
| DEC-06 | Safety Code permit fee allocated at $500 for this deliverable | Plumbing permit covers all of PKG-014. $500 is a parametric allocation for DEL-014-05's share. Total PKG-014 permit cost may be a single fee covering all 6 deliverables. | LOW confidence. Actual fee structure depends on municipal fee schedule. |
| DEC-07 | Scope resolution: DEL-014-05 resolved to 1 deliverable per SCOPE parameter | SCOPE = DEL-014-05 is a single deliverable ID. Confirmed in decomposition as part of PKG-014. | No ambiguity. |
| DEC-08 | Owner orientation labour (2h) priced at plumber trade rate | Procedure Step 10 describes a brief demonstration and documentation handover. 2 hours accounts for plumber presence during demonstration. PM time is already included in overhead LOE hours. | Minor line item. |
