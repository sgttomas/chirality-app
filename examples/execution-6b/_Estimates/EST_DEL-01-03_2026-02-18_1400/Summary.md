# Estimate Summary -- DEL-01-03 Bonding & Insurance Evidence

**RunID:** EST_DEL-01-03_2026-02-18_1400
**Date:** 2026-02-18
**Basis of Estimate:** RATE_TABLE (primary) + ALLOWANCE (premium lines)
**Currency:** CAD
**Rounding:** DOLLAR

---

## Totals

| Category | CBS | Method | Amount (CAD) | % of Total |
|---|---|---|---:|---:|
| Production hours (documentation) | 01.ADMIN.BOND_INS | RATE_TABLE | $2,060 | 0.4% |
| Bond premiums | 01.PREMIUM.BOND | ALLOWANCE | $300,000 | 55.0% |
| CCIP insurance premium | 01.PREMIUM.INS | ALLOWANCE | $240,000 | 44.0% |
| Surety broker fee | 01.PREMIUM.BROKER | ALLOWANCE | $3,500 | 0.6% |
| **TOTAL** | | | **$545,560** | **100.0%** |

---

## Basis Summary

### Production Hours ($2,060 -- RATE_TABLE)
- 10 total hours across 3 roles
- Project Manager (4h @ $175): surety broker coordination, insurance approach decisions
- Legal Review -- External (4h @ $300): bond document review, insurance documentation review
- Administrative / Document Control (2h @ $80): document compilation and filing
- Rates sourced from Professional_Staff_Rates.csv; hours sourced from Level_of_Effort.csv

### Bond Premiums ($300,000 -- ALLOWANCE)
- Performance bond (50% of contract): 1.50% of $12,000,000 = $180,000
- Labour & Materials bond (50% of contract): 1.00% of $12,000,000 = $120,000
- Estimated contract value from Assumed_Project_Parameters.csv (PP-25 = $12M, PARAMETRIC, LOW confidence)
- Premium rates from Fees_Permits_Insurance.csv (FP-01, FP-02)
- **These amounts will change when Schedule A base price (DEL-01-04) is finalized**

### CCIP Insurance ($240,000 -- ALLOWANCE)
- 2.00% of $12,000,000 estimated contract value
- Per DEC-011: CCIP confirmed as insurance approach
- Rate from Fees_Permits_Insurance.csv (FP-03, LOW confidence, range 1.50%-2.50%)
- **This amount will change when contract value and insurer rate are finalized**

### Surety Broker Fee ($3,500 -- ALLOWANCE)
- Recommended midpoint from market range $2,000-$5,000
- From Fees_Permits_Insurance.csv (FP-19)

---

## Key Warnings

1. **LOW confidence on premium lines (96% of total).** Bond and insurance premiums are calculated against an estimated contract value of $12M (PP-25, PARAMETRIC, LOW confidence). Actual premiums will depend on final Schedule A pricing.
2. **CCIP rate uncertainty.** The 2.00% CCIP rate is the recommended midpoint of a 1.50%-2.50% range. Actual rate depends on project risk profile and insurer selection.
3. **Circular dependency with DEL-01-04.** Bond premiums require the Schedule A base price (DEL-01-04), but bond costs are a component of that price. Current estimate uses PP-25 parametric value as a placeholder; iteration will be needed.
4. **Mixed methods authorized.** 3 lines use RATE_TABLE; 4 lines use ALLOWANCE. This is explicitly authorized by ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_ALLOWANCE.

---

## Blockers

No blockers prevent this estimate from being produced. However, accuracy of premium lines (96% of total value) is dependent on DEL-01-04 Schedule A pricing being finalized. See Dependencies.csv DEP-01-03-005.
