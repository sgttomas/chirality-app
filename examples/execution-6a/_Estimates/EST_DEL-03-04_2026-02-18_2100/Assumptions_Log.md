# Assumptions Log: EST_DEL-03-04_2026-02-18_2100

## Quantity Assumptions

| AssumptionID | Assumption | Basis | Confidence | Lines Affected | Sensitivity |
|-------------|-----------|-------|------------|---------------|-------------|
| ASM-001 | Distance from municipal stubs to Main PSB = 120 m | Stubs at site corner (Addendum 03 s1.6); building toward center of 12-acre parcel; ~4.5 acres developed (PP-10). 120 m is a reasonable mid-range estimate for a site this size. | LOW | L-0304-01, L-0304-05, L-0304-07, L-0304-08, L-0304-10 | HIGH: +/-30% change in length = +/-$26,000 to $33,000 in total |
| ASM-002 | Distance from Main PSB to Cold Storage Building = 40 m | Typical separation for operational layout on a municipal services site. Cold Storage is 60x100 ft ancillary building. | LOW | L-0304-02, L-0304-09 | MEDIUM: +/-50% change = +/-$8,800 |
| ASM-003 | Common trench shared corridor = 100 m (water, sewer, gas co-located) | Standard civil practice for utility corridors. 100 m of the 120 m run to PSB assumed to share alignment. | MED | L-0304-11 | LOW: $10,000 line; conservative since no credit taken against individual utility rates |
| ASM-004 | Cold Storage Building requires water service | Datasheet states "TBD"; included conservatively for potential wash-down or fire suppression needs. | LOW | L-0304-02, L-0304-04 | MEDIUM: If not required, remove $12,500 |
| ASM-005 | Cold Storage Building does NOT require sanitary sewer service | No plumbing fixtures identified for unheated storage building. | MED | (none -- excluded) | LOW: If required, add ~$13,000 |
| ASM-006 | Cold Storage Building does NOT require telecom/data service | Unheated storage building; no telecom requirements identified in Datasheet. | MED | (none -- excluded) | LOW: If required, add ~$4,000 (40m x $100/lm) |
| ASM-007 | Cold Storage Building does NOT require natural gas service | Unheated building per OSR 10.2 and DEC-001. | HIGH | (none -- excluded) | NEGLIGIBLE |

## Design and Scope Assumptions

| AssumptionID | Assumption | Basis | Confidence | Impact |
|-------------|-----------|-------|------------|--------|
| ASM-008 | UU rates are all-inclusive (trench, bedding, pipe, backfill, compaction) and no separate earthwork line item is needed for utility corridors | Underground_Utility_Rates.csv Notes column confirms each rate includes complete installation | HIGH | Avoids double-counting with DEL-03-02 bulk earthwork |
| ASM-009 | Common trench cost (L-0304-11) is additive to individual utility pipe rates | Conservative assumption: UU-09 represents shared trench excavation cost where utilities co-locate; individual UU rates also include trench cost for their respective pipe. In practice, common trench should reduce total cost (shared excavation), but no credit is taken. | MED | Estimate is conservative by approximately $10,000 |
| ASM-010 | Demarcation at 1.5 m outside building foundation wall per brief | Brief specifies this boundary. Distribution lengths calculated to this point. | HIGH | Consistent with PKG-002/PKG-003 scope boundary |
| ASM-011 | Civil design fee base is the distribution construction subtotal ($149,200), not the full site/civil value | DF-02 fee base is "construction cost of site/civil scope." DEL-03-04 is only the utility portion. Using distribution subtotal avoids overallocation. | MED | Design fee = $3,730 |

## Allowance Assumptions

| AssumptionID | Assumption | Basis | Confidence | Impact |
|-------------|-----------|-------|------------|--------|
| ASM-012 | DEC-004 tie-in allowance value = $35,000 (UU-12 recommended) | Owner has not pre-set allowance value. UU-12 range is $25,000-$50,000 with $35,000 recommended. | LOW | PENDING OWNER CONFIRMATION; +/-$15,000 range |
| ASM-013 | Utility connection fees at recommended parametric values | FP-11 through FP-15 recommended values used. Actual provider fee schedules not available. | LOW | $39,000 total; could vary significantly by provider |
