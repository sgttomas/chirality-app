# Assumptions Log

**RunID:** EST_DEL-01-03_2026-02-18_1400

| AssumptionID | Assumption | Source | Impact if Wrong | Linked Lines |
|---|---|---|---|---|
| ASM-001 | Estimated total project value (contract basis for premium calculations) is $12,000,000 CAD | Assumed_Project_Parameters.csv PP-25 (PARAMETRIC, LOW confidence) | HIGH -- every $1M change in contract value shifts bond premiums by ~$25,000 and CCIP premium by ~$20,000 | L-004, L-005, L-006 |
| ASM-002 | Performance bond premium rate is 1.50% of contract price | Fees_Permits_Insurance.csv FP-01 (MARKET, MEDIUM confidence, range 1.25%-1.75%) | MEDIUM -- range of $150K to $210K at $12M contract value (current estimate: $180K) | L-004 |
| ASM-003 | Labour & Materials bond premium rate is 1.00% of contract price | Fees_Permits_Insurance.csv FP-02 (MARKET, MEDIUM confidence, range 0.75%-1.25%) | MEDIUM -- range of $90K to $150K at $12M contract value (current estimate: $120K) | L-005 |
| ASM-004 | CCIP insurance premium rate is 2.00% of contract price | Fees_Permits_Insurance.csv FP-03 (MARKET, LOW confidence, range 1.50%-2.50%) | HIGH -- range of $180K to $300K at $12M contract value (current estimate: $240K); rate is insurer-dependent | L-006 |
| ASM-005 | Surety broker fee is $3,500 (recommended midpoint) | Fees_Permits_Insurance.csv FP-19 (MARKET, LOW confidence, range $2,000-$5,000) | LOW -- maximum variance is +/-$1,500; immaterial relative to total | L-007 |
| ASM-006 | Level of effort for DEL-01-03 is 10 hours (4 PM + 4 Legal + 2 Admin) | Level_of_Effort.csv (PARAMETRIC basis per source file) | LOW -- even doubling hours adds only ~$2,060; immaterial relative to total | L-001, L-002, L-003 |
| ASM-007 | Bond premiums are calculated on total project value including general requirements, contingency, and options (PP-25), not just base construction value (PP-24 = $8.7M) | Brief Special Instructions: premiums are "percentage of contract"; RFP C-08 references "Contract Price" which is Schedule A total | HIGH -- using PP-24 instead of PP-25 would reduce bond premiums by ~$82,500 and CCIP by ~$66,000. The correct basis depends on the RFP's definition of "Contract Price" in the bonding context. |
