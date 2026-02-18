# Decision Log

**RunID:** EST_DEL-01-04_2026-02-18_2359

---

| DecisionID | Decision | Rationale |
|---|---|---|
| ED-01 | Use RecommendedRate from all price source CSVs (not min or max) | RecommendedRate represents the best single-point estimate per source file; min/max range noted in source files for sensitivity analysis if needed |
| ED-02 | Dual cost nature: Group A (production) + Group B (construction content) | Per INIT-TASK brief; DEL-01-04 has both a compilation cost and the actual Schedule A pricing content |
| ED-03 | Cold storage priced as PEMB turnkey (PB-02 $48/sf) rather than component-by-component | PEMB turnkey rate is the most reliable parametric for an unheated pre-engineered metal building; component rates would double-count items included in the turnkey price |
| ED-04 | General requirements computed as fee percentages on construction scope values | Per Professional_Design_Fees.csv methodology; percentage basis aligned with Alberta DB market practice |
| ED-05 | Bond premiums calculated on 50% of PP-25 ($12M) estimated project value | Per RFP requirement C-08: Performance Bond 50% + Labour and Materials Bond 50%; applied to full project value as bond is on contract price |
| ED-06 | CCIP insurance at 2.00% of $12M project value | Mid-range of FP-03 (1.50%-2.50%); per DEC-011 confirming CCIP approach |
| ED-07 | Building permit at 0.75% of base construction value ($8.7M per PP-24) | Mid-range of FP-06 (0.50%-1.00%); applied to construction value not total project value |
| ED-08 | ALLOW_MIXED_METHODS enabled: 5 ALLOWANCE lines + 1 PARAMETRIC line retained | FALLBACK_POLICY=ALLOW_ALLOWANCE permits allowance-based pricing where rate table evidence is insufficient; PARAMETRIC used for cold storage per ED-03 |
| ED-09 | DB margin, contingency, and escalation excluded from estimate | These are commercial decisions requiring human input; ESTIMATING produces direct cost + general requirements; gap to PP-25 ($12M) noted in Summary.md |
| ED-10 | Quantities derived from Assumed_Project_Parameters.csv and architectural program assumptions | No detailed design quantities available; parametric quantities used based on building type and size |
| ED-11 | Radiant in-floor heating included for all 12,000 sf of apparatus/shop bays | MS-14 ($10/sf) applied to all bay areas; represents hydronic loops in slab shared with building boiler system; may be value-engineered in detailed design |
| ED-12 | Main PSB structural system: screw piles + steel frame (not spread footings) | SC-14 screw piles selected based on Penhold soils per geotechnical context; 80 piles at 6m centres for 18,000 sf footprint |
| ED-13 | Design fees rounded up to $640k to include coordination and management markup | Raw discipline fee percentages total ~$459k; management/coordination/overhead markup (~40%) applied per Alberta DB market practice; total aligns with ~8-9% of construction value |
| ED-14 | Municipal utility tie-in priced as cash allowance ($35k) per C-12 / Addendum 03 | Cash allowance approach explicitly permitted by RFP; tie-in costs highly variable and location-dependent |
| ED-15 | FF&E fixed at $20,000 cash allowance per DEC-012 | Not estimated -- fixed amount per project decision; allocated to Option 6 (Line 1-7) |
