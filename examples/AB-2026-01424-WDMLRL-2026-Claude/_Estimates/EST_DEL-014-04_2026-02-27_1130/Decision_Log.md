# Decision Log — EST_DEL-014-04_2026-02-27_1130

| Decision ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-01 | Applied RATE_TABLE method for underground drain piping using UU-02 Sanitary line rate ($160/m) from Underground_Utility_Rates.csv | UU-02 is the closest available rate for sanitary/drain piping in PRICE_SOURCES; rate includes supply and installation | 4 piping line items (L-08 through L-11) priced at $160/m |
| DEC-02 | Applied PARAMETRIC method for drain bodies, grates, traps, and trap primers | No drain fixture pricing exists in PRICE_SOURCES; parametric rates based on Alberta industrial construction norms | 7 material line items (L-01 through L-07) priced parametrically; confidence LOW |
| DEC-03 | Used fully burdened labour rates from Construction_Labour_Rates.csv (T-05 Plumber $92.80/hr, T-08 Labourer $65.10/hr) | Direct rate table match for plumber and labourer trades | 7 labour line items priced via RATE_TABLE |
| DEC-04 | Used Level_of_Effort.csv allocations for professional staff (6 roles, 38 total hours) | LOE file provides per-deliverable hour allocations matched with Professional_Staff_Rates.csv hourly rates | 6 management/supervision line items (L-22 through L-27) |
| DEC-05 | Assumed sump drain quantity = 2 (minimum one per repair bay) based on REQ-014-04-02 assumption | RFP and Specification state "sump drains in repair bays" without specifying quantity; 2 bays visible on App B drawing | If final IFC design specifies more sump drains, cost increases proportionally |
| DEC-06 | Parametric pipe run lengths estimated from building geometry (~13,000 sqft footprint, ~100 ft x 130 ft approximate) | No IFC plumbing drawings available; run lengths are rough order-of-magnitude estimates | Underground piping: 55m total; above-ground vent: 15m; +/-30% uncertainty |
| DEC-07 | Excluded oil/grease interceptor from estimate | REQ-014-04-11 requires Plumbing Engineer determination before including; determination is TBD | If required, adds estimated $3,000-$8,000 to total |
| DEC-08 | Plumber labour hours estimated parametrically across 6 phases | No production rate data in PRICE_SOURCES; hours based on 9 drain points, typical industrial installation complexity | 90 plumber hours + 24 labourer hours total |
| DEC-09 | Applied above-ground vent piping rate of $95/m parametrically | No rate table for above-grade vent piping; estimated at approximately 60% of underground sanitary rate (lighter weight, no excavation) | L-12: $1,425 for 15m of vent piping |
| DEC-10 | Permit and inspection fees estimated as $1,800 lump sum | No fee schedule in PRICE_SOURCES; parametric estimate for Alberta Safety Code plumbing permit + 2 inspections (rough-in + final) | Could be higher or lower depending on jurisdiction and scope complexity |
