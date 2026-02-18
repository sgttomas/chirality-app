# Estimate Summary -- DEL-05-02: Option -- Yard Lighting (Per Light)

## Basis of Estimate Used

- **BASIS_OF_ESTIMATE:** RATE_TABLE
- **Currency:** CAD
- **Rounding:** DOLLAR
- **Fallback Policy:** STRICT (no fallback pricing used)
- **Mixed Methods:** Not allowed; all lines use RATE_TABLE

## Pricing Structure (Unit Rate Option)

This is an **optional priced item** structured as a **unit rate per light installed**, per the RFP requirement. The Owner elects a quantity; the total scales accordingly.

### Per-Light Unit Rate Components

| Component | Rate | Unit | Notes |
|---|---|---|---|
| Yard light (pole + LED fixture + concrete base + wiring) | $7,500 | per light | 25-30 ft pole; IES dark-sky compliant LED; includes base and wiring |
| **Per-light installed rate** | **$7,500** | **per light** | |

### Fixed Cost (One-Time, Not Per Light)

| Component | Rate | Qty | Amount | Notes |
|---|---|---|---|---|
| Conduit run -- panel to first pole | $80/lm | 100 lm (assumed) | $8,000 | Underground conduit + wiring from building electrical room to first pole; one-time cost |

### Totals by CBS (at assumed 12-pole quantity)

| CBS | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| 26-ELEC | Yard light poles/fixtures/bases/wiring | $90,000 | 1 |
| 26-COND | Conduit run (panel to first pole) | $8,000 | 1 |
| **TOTAL** | **DEL-05-02 at 12 poles** | **$98,000** | **2** |

### Scaling Formula

For any Owner-elected quantity **N** lights:

> **Total = (N x $7,500) + $8,000**

| Example Qty | Per-Light Cost | Fixed Conduit | Total | Effective $/Light |
|---|---|---|---|---|
| 6 | $45,000 | $8,000 | $53,000 | $8,833 |
| 8 | $60,000 | $8,000 | $68,000 | $8,500 |
| 10 | $75,000 | $8,000 | $83,000 | $8,300 |
| **12 (assumed)** | **$90,000** | **$8,000** | **$98,000** | **$8,167** |
| 15 | $112,500 | $8,000 | $120,500 | $8,033 |
| 20 | $150,000 | $8,000 | $158,000 | $7,900 |

## Cost Ownership Boundaries

| Scope Area | Cost Owner | NOT in DEL-05-02 |
|---|---|---|
| Yard lighting (pole/fixture/base/wiring per unit) | **DEL-05-02** | -- |
| Conduit from panel to first pole | **DEL-05-02** | -- |
| Electrical service point for yard lighting (panel/breaker at building) | DEL-02-06 | Excluded from this estimate |
| Site electrical conduit routing beyond yard light scope | DEL-03-04 | Excluded from this estimate |

## Key Warnings and Blockers

1. **Quantity is assumed (12 poles, LOW confidence).** Actual count depends on site layout / fence line perimeter / spacing from DEL-03-01 (site plan not yet finalized).
2. **Conduit run length is assumed (100 lm).** Actual distance from building electrical room to first pole depends on site plan from DEL-03-01.
3. **Price source rates are PARAMETRIC in origin** (range-based, not firm quotes). Used as rate table for this estimate. Recommend confirming with supplier quotes before final submission.
4. **Upstream dependency on DEL-03-01** (site plan) is unresolved -- fixture layout planning cannot be finalized.
5. **Upstream interface with DEL-02-06** (base electrical) -- service point location and capacity not yet confirmed.
