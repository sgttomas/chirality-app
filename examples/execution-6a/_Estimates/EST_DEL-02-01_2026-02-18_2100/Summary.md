# Estimate Summary — EST_DEL-02-01_2026-02-18_2100

## Revision

| Field | Value |
|---|---|
| This Run | EST_DEL-02-01_2026-02-18_2100 |
| Prior Run | EST_DEL-02-01_2026-02-18_0800 |
| Revision Type | TBD resolution pass |
| Changes | 7 TBD lines resolved using Interior_Architectural_Rates.csv (PS-27) and Professional_Design_Fees.csv |

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| ROUNDING | DOLLAR |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |
| RUN_STATUS | OK |

## Scope

| Field | Value |
|---|---|
| Deliverable | DEL-02-01 — Architectural Program, Layout & Code Planning |
| Package | PKG-002 — Main Public Services Building (PSB) |

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count | Status |
|---|---|---|---|---|
| 3100 | Architectural design fees | $11,012 | 1 | Priced (7% of $157,317) |
| 3200 | Interior partitions | $30,225 | 1 | Priced (IA-01/02/04 blended) |
| 3300 | Interior doors, frames, hardware | $47,200 | 3 | Priced (unchanged) |
| 3400 | Interior finishes (floor, ceiling, paint) | $58,882 | 3 | Priced (IA-05/08/12/13) |
| 3500 | Accessibility features | $9,490 | 1 | Priced (IA-15/16/17/18) |
| 3600 | Code-required signage | $11,520 | 1 | Priced (IA-19/20/21) |
| **TOTAL** | | **$168,329** | **10** | **Complete** |

## Construction vs Design Fee Split

| Category | Amount | Lines |
|---|---|---|
| Construction subtotal (L-001 through L-009) | $157,317 | 9 |
| Architectural design fee (L-010 = 7% of above) | $11,012 | 1 |
| **Total** | **$168,329** | **10** |

## Key Findings

1. **All 10 line items now priced.** The addition of Interior_Architectural_Rates.csv (PS-27) to PRICE_SOURCES resolved the 7 TBD items that blocked the prior run. All lines use RATE_TABLE method — no mixed methods required.

2. **Quantities remain assumption-based.** Area breakdowns (5,200 sf office/shared, 3,500 sf partitions, 7,000 sf paint) are derived from parametric assumptions (ASM-003 through ASM-007), not from a confirmed floor plan. Functional Program (Appendix B) would improve quantity accuracy.

3. **Design fee is now computable.** DF-01 at 7% of the $157,317 construction subtotal yields $11,012. This is a relatively small fee reflecting the interior-only architectural scope of DEL-02-01.

4. **No mixed methods.** Unlike the PKG-001 TBD resolutions which required ALLOWANCE method, all DEL-02-01 items are priced from rate tables (Interior_Architectural_Rates.csv + Building_Envelope_Rates.csv + Professional_Design_Fees.csv).
