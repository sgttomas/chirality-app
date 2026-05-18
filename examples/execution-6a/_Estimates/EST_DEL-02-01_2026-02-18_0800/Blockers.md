# Blockers Report — EST_DEL-02-01_2026-02-18_0800

## Pricing Blockers (preventing estimate completion)

| # | Blocker | Impact | Resolution Path |
|---|---|---|---|
| PB-01 | No rate table entries for interior partitions, ceiling, floor finish, paint, accessibility, or signage | 7 of 10 line items are TBD; construction subtotal cannot be computed; design fee (DF-01) cannot be applied | Add rate table entries to PRICE_SOURCES for these items, or change FALLBACK_POLICY to ALLOW_ALLOWANCE |
| PB-02 | Architectural design fee (DF-01) is dependent on a construction subtotal that is incomplete | Design fee cannot be calculated as a percentage of an unknown base | Resolve PB-01 first; fee will be computable once construction lines are priced |

## Information Blockers (affecting quantity accuracy but not methodology)

| # | Blocker | Dependency Ref | Impact | Resolution Path |
|---|---|---|---|---|
| IB-01 | Functional Program (Appendix B) not accessible | DEP-02-01-011 | Room count and areas for shared spaces are estimated, not confirmed; door count (ASM-004) and partition area (ASM-005) may change | Obtain and review Functional Program; update area assumptions |
| IB-02 | Alberta Building Code not directly accessible | DEP-02-01-014 | Accessibility feature scope is approximate; specific requirements for occupancy classification unknown | Obtain Alberta Building Code text; confirm occupancy classification with AHJ |

## Design-Execution Blockers (informational; do not affect this estimate run)

| # | Blocker | Dependency Ref | Notes |
|---|---|---|---|
| DEB-01 | Site plan concept from DEL-03-01 not yet available | DEP-02-01-015 | Required before finalizing floor plan layouts; does not affect this cost estimate which uses parametric areas |
| DEB-02 | Structural bay grid from DEL-02-04 not yet available | DEP-02-01-016 | Required for floor plan efficiency; does not directly affect cost estimate quantities at this stage |
