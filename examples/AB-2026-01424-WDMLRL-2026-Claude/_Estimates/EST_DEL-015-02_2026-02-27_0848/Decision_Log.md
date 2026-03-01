# Decision Log — EST_DEL-015-02_2026-02-27_0848

| DecID | Decision | Rationale | Impact |
|---|---|---|---|
| D-001 | Used ES-01 from Electrical_System_Rates.csv ($520/EA) as the base rate for high-bay LED fixtures | ES-01 is described as "High-bay LED fixture, installed" at 150W class; matches Main Shop fixture specification exactly | DL-001 ($10,400) |
| D-002 | Applied 15% wet-location premium to Wash Bay fixtures ($520 -> $600/EA) | No separate wet-rated fixture rate available; 15% premium is a conservative industry parametric for IP65-rated industrial fixtures over standard models | DL-002 ($3,600) |
| D-003 | Used $280/EA parametric rate for 8-foot LED linear fixtures | Electrical_System_Rates.csv contains no 8-foot linear fixture rate; $280 is an industry parametric for supply + installation of commercial-grade 8ft LED strip fixtures; falls within reasonable range for Alberta market | DL-003, DL-004, DL-005 ($2,520 total) |
| D-004 | Used T-04 Electrician fully-burdened rate ($96.00/hr) from Construction_Labour_Rates.csv for all trade labour items | Lighting installation is electrician work; T-04 is the appropriate trade classification | DL-014 through DL-021, DL-028, DL-029 ($24,000 total) |
| D-005 | Priced professional staff hours directly from Level_of_Effort.csv quantities x Professional_Staff_Rates.csv rates | Level_of_Effort.csv provides DEL-015-02-specific hour allocations for 6 professional roles; rates are per the rate table | DL-022 through DL-027 ($5,590 total) |
| D-006 | Excluded emergency/exit lighting from estimate | Specification REQ-L-15 status is TBD; scope inclusion is unresolved per Guidance CONF-L-02; estimating does not add scope that the deliverable documents treat as unresolved | No cost included; noted in W-04 |
| D-007 | Excluded Old North Shop lighting from estimate | Specification §Scope explicitly excludes Old North Shop lighting (Enrichment X-001) | No cost included |
| D-008 | Excluded ceiling fans from estimate | Ceiling fans are noted as separate scope item per App B-Elec; not assigned to DEL-015-02; see Guidance CONF-L-03 | No cost included |
| D-009 | Switching/controls priced as ALLOWANCE ($2,500) rather than PARAMETRIC | Controls strategy is TBD (Spec REQ-L-14); cannot apply parametric model without knowing scope (manual vs occupancy vs daylight harvesting); allowance is conservative for manual-switch-only scenario | DL-012; flagged in QA |
| D-010 | FALLBACK_POLICY=ALLOW_PARAMETRIC applied: all items priced using parametric methods even where rate tables lack direct line items | Per run brief; enables meaningful totals despite gaps in Electrical_System_Rates.csv | All DL lines with parametric assumptions |
| D-011 | ALLOW_MIXED_METHODS=TRUE applied: DL-012 uses ALLOWANCE method while remaining 28 lines use PARAMETRIC | Per run brief; controls/switching cannot be parametrically modeled without scope definition | DL-012 |
