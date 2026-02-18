# Source Index: EST_DEL-01-03_2026-02-18_1500

## Indexed Price Sources

| # | Source File | Source Type | Items Used | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | R-02 (PM $175/hr), R-24 (Admin $80/hr), R-25 (Legal $300/hr) | Production cost line items (L-001, L-002, L-003) |
| 2 | `_PriceSources/Level_of_Effort.csv` | Parametric Hours | DEL-01-03 rows: R-02 (4h), R-25 (4h), R-24 (2h) | Production hours per role |
| 3 | `_PriceSources/Fees_Permits_Insurance.csv` | Rate Table / Allowance | FP-01 (1.50%), FP-02 (1.00%), FP-03 (2.00%), FP-04 (0.20%), FP-05 (0.75%), FP-19 ($3,500) | Bond premiums (L-010, L-011), insurance premiums (L-020, L-021, L-022), broker fee (L-030) |
| 4 | `_PriceSources/Assumed_Project_Parameters.csv` | Parameters | Not directly priced; PP-24 ($8,700,000) and PP-25 ($12,000,000) used for context/cross-check | Contract value context |

## Upstream Estimate References

| # | Reference | Type | Value Used | Purpose |
|---|---|---|---|---|
| 5 | `_Estimates/EST_DEL-05-01_2026-02-18_1400/Summary.md` | Prior Estimate Snapshot | Base construction = $9,863,000 (L-010 through L-022 subtotal) | Contract value basis for bond/insurance percentage calculations |

## Parsing Notes

- **Professional_Staff_Rates.csv**: 30 roles; 3 used for DEL-01-03 production. R-30 (Surety Broker) has $0 rate — cost captured in Fees_Permits_Insurance.csv FP-19 instead.
- **Level_of_Effort.csv**: 67 rows total; 3 rows for DEL-01-03 (R-02, R-25, R-24). All marked Basis=PARAMETRIC.
- **Fees_Permits_Insurance.csv**: 19 items; 6 used for DEL-01-03 (FP-01 through FP-05 for premiums, FP-19 for broker fee). Bond/insurance rates are percentage-based; applied to upstream contract value.
- **Assumed_Project_Parameters.csv**: 29 parameters; not directly used for pricing but PP-24/PP-25 provide order-of-magnitude context for the contract value used.

## Source Coverage Assessment

| Source Category | Available | Used | Notes |
|---|---|---|---|
| Professional hourly rates | YES | 3 of 30 roles | R-02, R-24, R-25 per LOE matrix |
| Level of effort hours | YES | 3 rows | PM (4h), Legal (4h), Admin (2h) |
| Bond premium rates | YES | 2 items | FP-01 (performance 1.5%), FP-02 (L&M 1.0%) |
| Insurance premium rates | YES | 3 items | FP-03 (CCIP 2.0%), FP-04 (builder's risk 0.2%), FP-05 (CGL 0.75%) |
| Surety broker fee | YES | 1 item | FP-19 ($3,500 recommended) |
| Contract value basis (upstream) | YES | 1 reference | DEL-05-01 base construction $9,863,000 |

**Provenance completeness: 9/9 lines (100%) have non-TBD SourceRef.**
