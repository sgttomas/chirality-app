# QA Report -- EST_DEL-02-02_2026-02-18_2100

## RUN_STATUS: OK

---

## Schema Validity

| Check | Result | Notes |
|---|---|---|
| Detail.csv exists | PASS | 3 data rows + header |
| All required columns present | PASS | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS | All 3 rows: RATE_TABLE |
| Allowance/parametric convention | N/A | No ALLOWANCE or PARAMETRIC method rows |
| Amount = Qty x UnitRate | PASS | L-001: 24 x 155 = 3,720; L-002: 16 x 125 = 2,000; L-003: 16 x 95 = 1,520 |
| Currency consistent | PASS | All rows: CAD |
| WBS_CBS_Matrix.csv exists | PASS | 3 data rows (2 CBS subtotals + 1 deliverable total) |
| Matrix totals reconcile to Detail | PASS | CBS-200: 3,720 + 2,000 = 5,720; CBS-210: 1,520; Grand total: 7,240 |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-02) |
| Deliverables covered (priced) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 3 |
| Total hours | 56 |
| Total amount (CAD) | $7,240 |

## Provenance Completeness

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 3 / 3 (100%) |
| Top missing-source offenders | None |

All 3 line items have full provenance: each cites a specific row in `Level_of_Effort.csv` (for quantity) and a specific role in `Professional_Staff_Rates.csv` (for unit rate).

## Basis-Consistency Check

| Check | Result | Notes |
|---|---|---|
| BASIS_OF_ESTIMATE declared | RATE_TABLE | Valid enum value |
| Method values match basis | PASS | All 3 rows: RATE_TABLE |
| Mixed methods detected | No | ALLOW_MIXED_METHODS = FALSE; no deviation |
| Fallback used | No | FALLBACK_POLICY = STRICT; not triggered |

## Dependency / Blocker Assessment

| Check | Result | Notes |
|---|---|---|
| Dependency register loaded | Yes | 20 rows from Dependencies.csv |
| Upstream prerequisites identified | 8 (DEP-02-02-005 through DEP-02-02-012) | 1 deliverable prerequisite (DEL-02-01); 7 document prerequisites |
| Upstream interfaces identified | 3 (DEP-02-02-013 through DEP-02-02-015) | DEL-02-03, DEL-02-04, DEL-02-05 |
| Upstream constraints identified | 1 (DEP-02-02-019) | DEC-013: no additional geotech |
| Pricing blockers from dependencies | 0 | Dependencies inform production sequencing, not pricing |
| Unresolved inputs affecting estimate | 0 | All pricing sources present |

## Rounding Validation

| Check | Result | Notes |
|---|---|---|
| ROUNDING policy | DOLLAR | All amounts are whole dollar values |
| Fractional amounts detected | No | All Qty x UnitRate products are exact integers |

## Write Quarantine

| Check | Result |
|---|---|
| All files written under `_Estimates/EST_DEL-02-02_2026-02-18_2100/` | PASS |
| No files modified outside `_Estimates/` | PASS |

## What to Fix for a Cleaner Rerun

Nothing. This is a clean run with no warnings, no TBDs, and full provenance.
