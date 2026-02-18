# Source Index: EST_DEL-03-04_2026-02-18_2100

## Price Sources

| # | Source File | Source Type | Items Used | Parsing Notes | Supports |
|---|-----------|-------------|------------|---------------|----------|
| 1 | _PriceSources/Underground_Utility_Rates.csv | Rate Table / Allowance | UU-01 through UU-12 | 13 rows; CSV parseable; mixes RATE_TABLE (UU-01 through UU-09) and ALLOWANCE (UU-10 through UU-12) items | On-site utility distribution unit rates (water, sewer, gas, power, telecom, trench); municipal tie-in allowance (DEC-004) |
| 2 | _PriceSources/Construction_Labour_Rates.csv | Rate Table | T-08, T-09 | 15 rows; CSV parseable; fully burdened Alberta labour rates | Labour rates for heavy/light equipment operators (cross-reference with UU rates which are all-inclusive) |
| 3 | _PriceSources/Professional_Design_Fees.csv | Rate Table (percentage) | DF-02 | 8 rows; CSV parseable; fee percentages of construction cost | Civil engineering design fees for utility routing scope |
| 4 | _PriceSources/Fees_Permits_Insurance.csv | Allowance | FP-11 through FP-15 | 19 rows; CSV parseable; mix of MARKET and ALLOWANCE basis | Utility connection fees (water, sewer, power, gas, telecom) |
| 5 | _PriceSources/Assumed_Project_Parameters.csv | Parameters | PP-05, PP-07, PP-09, PP-10, PP-23 | 29 rows; CSV parseable; project parameters for quantity derivation | Site dimensions, building footprints, site/civil construction value estimate for design fee percentage base |

## Decomposition Source

| Source File | Status | Items Used |
|------------|--------|------------|
| _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md | Available (v1.0 Phase 7) | DEL-03-04 identification, PKG-003 assignment, SOW-0109/SOW-0110 traceability, DEC-004 |

## Dependency Source

| Source File | Status | Items Used |
|------------|--------|------------|
| DEL-03-04/Dependencies.csv | Available (16 ACTIVE rows) | DEP-03-04-006 through DEP-03-04-010 (upstream prerequisites -- PENDING); DEP-03-04-011/012 (interfaces with DEL-03-01/DEL-03-02) |

## Source Coverage Notes

- Underground_Utility_Rates.csv provides all-inclusive unit rates for pipe/conduit installation (includes trench, bedding, pipe, backfill, compaction). Labour rates in Construction_Labour_Rates.csv are referenced for cross-validation but are not separately applied since UU rates are composite.
- Professional_Design_Fees.csv DF-02 provides civil design fees as a percentage (2.5%) of site/civil construction cost. The fee base used is the sum of distribution line items in this estimate (not PP-23, which covers all site/civil scope beyond DEL-03-04).
- Fees_Permits_Insurance.csv FP-11 through FP-15 are ALLOWANCE-basis items. These are carried at recommended rates subject to actual provider fee schedules.
- UU-12 ($35,000 combined tie-in allowance) is the primary DEC-004 allowance line item. Owner must confirm value.

## Source Gaps

| Gap | Impact | Mitigation |
|-----|--------|-----------|
| Actual utility run lengths unknown (pending post-award survey and underground services drawings) | Quantities are assumed; could be materially different | Flagged as ASM-001 through ASM-007; rerun with actual survey data post-award |
| Town of Penhold connection fee schedules not available | FP-11 through FP-15 carried at recommended parametric values | Confirm with Town during design phase |
| Cold Storage utility requirements partially TBD | Water and sanitary connections for Cold Storage assumed but not confirmed | ASM-004, ASM-005; confirm during design |
