# QA Report

**RunID:** EST_DEL-04-01_2026-02-18_1300
**RUN_STATUS: OK**

---

## Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| All required columns present | PASS (14/14: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | PASS (all rows = RATE_TABLE; valid enum) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| Amount = Qty x UnitRate | PASS (L-04-01-001: 12 x 165 = 1980; L-04-01-002: 4 x 145 = 580) |
| Currency consistent | PASS (all rows = CAD) |
| Rounding applied | PASS (DOLLAR; all amounts are whole dollars) |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-04-01) |
| Deliverables covered (priced) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 2 |

## Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 (100%) |
| Rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Detail.csv Method values | All RATE_TABLE |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS | FALSE |
| Consistency | PASS |

## Dependency / Blocker Assessment

| Metric | Value |
|---|---|
| Dependency rows loaded | 15 |
| UPSTREAM dependencies | 9 (DEP-04-01-001 through DEP-04-01-009, DEP-04-01-013) |
| DOWNSTREAM dependencies | 6 (DEP-04-01-010 through DEP-04-01-012, DEP-04-01-014, DEP-04-01-015) |
| Unresolved blockers to estimating | 0 |
| Information gaps that affect pricing | 0 |

Note: Dependencies are interface/handover/constraint type. None block the ability to estimate professional hours for this narrative deliverable. The upstream interfaces (DEL-02-01 architectural concept, DEL-04-02 mechanical, DEL-04-03 electrical) affect the deliverable content but not the professional effort required to produce it.

## WBS/CBS Matrix Reconciliation

| Check | Result |
|---|---|
| Detail.csv total | $2,560 CAD |
| WBS_CBS_Matrix.csv total | $2,560 CAD |
| Reconciliation | PASS |

## What to Fix for a Cleaner Rerun

1. **Rate confidence upgrade:** If firm-specific negotiated rates become available, update Professional_Staff_Rates.csv and rerun for higher confidence.
2. **Historical validation:** If prior proposal-stage envelope strategy efforts have tracked actuals, they could validate the 16-hour total for this deliverable type.
3. **No action required at this time.** All inputs are sufficient for a meaningful estimate.
