# QA Report -- EST_DEL-05-02_2026-02-18_1600

## RUN_STATUS: WARNINGS

Some totals exist and are meaningful, but material assumptions remain (quantity and conduit length are TBD pending upstream deliverables).

---

## Schema Validity (Detail.csv)

- **Columns present:** LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes -- **PASS**
- **Method values:** All rows use `RATE_TABLE` -- **PASS** (consistent with BASIS_OF_ESTIMATE)
- **Allowance/parametric convention:** N/A (no ALLOWANCE or PARAMETRIC method rows) -- **PASS**
- **Amount computation check:**
  - L-0502-01: 12 x $7,500 = $90,000 -- **PASS**
  - L-0502-02: 100 x $80 = $8,000 -- **PASS**
- **Rounding check (DOLLAR):** All amounts are whole dollars -- **PASS**

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-05-02) |
| Deliverables covered (with priced lines) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 2 |

## Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 (100%) |
| Rows with `location TBD` SourceRef | 0 |
| **Provenance completeness** | **100%** |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Detail.csv Method values | All RATE_TABLE |
| Mixed methods detected | NO |
| Fallback pricing used | NO |
| **Basis-consistency** | **PASS** |

## Dependency / Blocker Assessment

| Blocker | Source | Impact |
|---|---|---|
| DEL-03-01 (site plan) not finalized | DEP-0502-003 | Pole quantity and conduit length are assumed; cannot finalize fixture layout |
| DEL-02-06 (base electrical) interface open | DEP-0502-004 | Service point location/capacity not confirmed |

- **Blocker count:** 2 upstream dependencies unresolved
- **Impact on estimate:** Totals are meaningful but quantity-sensitive; per-unit rate is substantiated

## Warnings Summary

| ID | Warning | Severity | Actionable Fix |
|---|---|---|---|
| W-001 | Pole quantity assumed at 12 (PP-20, LOW confidence) | MATERIAL | Finalize site plan (DEL-03-01) to determine actual pole count and spacing |
| W-002 | Conduit run length assumed at 100 lm | MATERIAL | Confirm distance from building electrical room to first pole via site plan |
| W-003 | Price source rates are PARAMETRIC-origin (not firm quotes) | MODERATE | Obtain supplier quotes for poles/fixtures and conduit before final submission |
| W-004 | Upstream DEL-03-01 dependency unresolved | MODERATE | Complete site plan / circulation layout to enable fixture layout planning |
| W-005 | Upstream DEL-02-06 interface unresolved | LOW | Confirm electrical service point location and capacity for yard lighting panel |

## What to Fix for a Cleaner Rerun

1. **Finalize DEL-03-01** (site plan) to resolve pole quantity and conduit run length.
2. **Obtain supplier quotes** for yard light poles/fixtures to move from PARAMETRIC-origin rates to firm QUOTE-basis pricing.
3. **Confirm DEL-02-06 interface** (electrical service point for yard lighting panel/feeder).
4. Once the above are resolved, rerun with `BASIS_OF_ESTIMATE=QUOTE` for higher confidence.

## Acceptance Checklist (S8)

- [x] RUN_STATUS declared: WARNINGS
- [x] Basis-consistency checks: PASS
- [x] Provenance completeness reported: 100%
- [x] Scope coverage explicit: 1 in scope, 1 covered, 0 missing, 0 blocked
- [x] No writes outside `_Estimates/`
- [x] Gaps are clearly bounded (quantity assumption and conduit length)
