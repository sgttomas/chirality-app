# Estimate Summary — EST_DEL-02-01_2026-02-18_0800

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| ROUNDING | DOLLAR |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |
| RUN_STATUS | WARNINGS |

## Scope

| Field | Value |
|---|---|
| Deliverable | DEL-02-01 — Architectural Program, Layout & Code Planning |
| Package | PKG-002 — Main Public Services Building (PSB) |
| Cost Drivers | Architectural design fees; interior partitions; doors/frames/hardware; finishes (sealed concrete floors, ceiling system); accessibility features; code-required signage |

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count | Status |
|---|---|---|---|---|
| 3100 | Architectural design fees | TBD | 1 | TBD — depends on construction subtotal |
| 3200 | Interior partitions | TBD | 1 | No rate table evidence |
| 3300 | Interior doors, frames, hardware | $47,200 | 3 | Priced |
| 3400 | Interior finishes (floor, ceiling, paint) | TBD | 3 | No rate table evidence |
| 3500 | Accessibility features | TBD | 1 | No rate table evidence |
| 3600 | Code-required signage | TBD | 1 | No rate table evidence |
| **TOTAL** | | **$47,200 + TBD** | **10** | **Partial** |

## Priced vs TBD Summary

| Category | Line Count | Amount |
|---|---|---|
| Priced (RATE_TABLE) | 3 | $47,200 |
| TBD (no rate evidence) | 7 | TBD |
| **Total** | **10** | **$47,200 + TBD** |

## Key Findings

1. **Only 3 of 10 line items are priced.** The provided PRICE_SOURCES contain rate tables primarily oriented toward structural, envelope, mechanical, and electrical trades. Interior architectural construction rates (partitions, finishes, ceiling, paint, signage, accessibility) are absent.

2. **The $47,200 priced amount covers interior doors, frames, and hardware only.** This is a narrow subset of the DEL-02-01 scope. The priced total should not be interpreted as the deliverable estimate.

3. **Architectural design fees cannot be computed.** DF-01 (7% of construction cost) requires a construction subtotal, which is incomplete due to TBD line items.

4. **The estimate is materially incomplete.** Under STRICT fallback policy, no amounts were invented. The TBD items represent a significant portion of the expected cost (estimated at 70-80% of total DEL-02-01 cost based on typical institutional construction cost distributions).

## Warnings and Blockers

- 7 line items are TBD due to missing rate table entries (see QA_Report.md)
- Functional Program (Appendix B) not yet accessible; shared-space area breakdown is assumption-based
- Alberta Building Code not accessible; accessibility feature scope is approximate
- No dependency-related blockers identified that would prevent estimation (blockers are design-execution related, not pricing-related)

## Recommendations for Next Run

To achieve a meaningful total for DEL-02-01, the following rate table entries should be added to PRICE_SOURCES:

1. **Interior partition walls** (metal stud + gypsum board, $/sf of wall face area)
2. **Suspended acoustical ceiling tile** ($/sf of ceiling area)
3. **Concrete floor sealer/hardener** ($/sf, finish-only application)
4. **Interior paint** ($/sf of wall surface, materials + labour)
5. **Accessibility provisions** ($/sf or lump sum for barrier-free upgrades)
6. **Code-required signage** (lump sum or $/sign for exit, room ID, accessibility, fire signage)

Alternatively, set `FALLBACK_POLICY=ALLOW_ALLOWANCE` and provide an allowance table to price TBD items as allowances.
