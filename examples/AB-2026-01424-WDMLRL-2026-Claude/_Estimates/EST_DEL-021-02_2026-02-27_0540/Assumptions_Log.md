# Assumptions Log — EST_DEL-021-02_2026-02-27_0540

| AssumptionID | Assumption | Impact | Source | Status |
|---|---|---|---|---|
| ASM-001 | Contract price is TBD; bond premiums are estimated using parametric allowances from Fees_Permits_Insurance.csv | Bond premium costs ($39,000 combined) may vary significantly ($21K–$63K range) when actual contract price is known | Fees_Permits_Insurance.csv FP-01, FP-02; Datasheet Attributes — Contract Price | OPEN — requires contract award to resolve |
| ASM-002 | Bond premium allowances include all surety company fees (administrative, rider, etc.) — no separate surety fee line items | If surety charges additional fees beyond premium, total bonding cost will increase | Fees_Permits_Insurance.csv FP-01, FP-02 Notes | OPEN — confirm with surety company |
| ASM-003 | Same surety company from bid security (DEL-021-01) will provide performance/payment bonds | Switching surety companies would introduce timeline risk and potentially different premium rates | Guidance Principle 2; _DEPENDENCIES.md upstream DEL-021-01 | OPEN — verify upon award |
| ASM-004 | Labour hours from Level_of_Effort.csv are sufficient for the bonding process including surety coordination, Owner liaison, document control, and QA review | If bond procurement encounters complications (e.g., surety rejection, form disputes per Procedure Step 3A/4A), actual hours may exceed parametric allocation | Level_of_Effort.csv DEL-021-02 rows | OPEN |
| ASM-005 | Currency is CAD for all items | Alberta project; consistent with Assumed_Project_Parameters.csv PP-17 | Assumed_Project_Parameters.csv PP-17 | CONFIRMED |
| ASM-006 | Bond premiums are a proponent cost and are the priceable scope; bond face amounts (50% of contract price each) are coverage values, not direct costs | If the proponent needs to fund bond face amounts as collateral, additional financing costs may apply | Guidance Considerations — Bond Amount Calculation | OPEN |
