# QA Report

**RunID:** EST_DEL-01-03_2026-02-18_1400
**Date:** 2026-02-18

---

## RUN_STATUS: WARNINGS

Totals are meaningful but material assumptions remain on premium allowance lines (96% of total value).

---

## Schema Validity (S5)

| Check | Result | Notes |
|---|---|---|
| Detail.csv parseable | PASS | 7 data rows + header |
| All required columns present | PASS | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS | RATE_TABLE (3 rows), ALLOWANCE (4 rows) -- both are valid enum values |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS | All 4 ALLOWANCE lines use Qty=1, Unit=LS, UnitRate=Amount |
| Currency consistency | PASS | All rows = CAD |
| Rounding applied | PASS | All amounts are whole dollars |

---

## Coverage (S4, S8)

| Check | Result | Notes |
|---|---|---|
| Deliverables in scope | 1 (DEL-01-03) | |
| Deliverables with line items | 1 (DEL-01-03) | |
| Deliverables missing | 0 | |
| Deliverables blocked | 0 | |
| Line items produced | 7 | |
| Total estimated amount | $545,560 CAD | |

---

## Provenance Completeness (S6)

| Metric | Value |
|---|---|
| Total priced rows | 7 |
| Rows with non-TBD SourceRef | 7 (100%) |
| Rows with "location TBD" SourceRef | 0 |
| Top missing-source offenders | None |

All 7 line items have complete source references pointing to specific files and row/parameter identifiers.

---

## Basis Consistency

| Check | Result | Notes |
|---|---|---|
| Primary BASIS_OF_ESTIMATE | RATE_TABLE | |
| RATE_TABLE rows | 3 (43%) | Production hour lines |
| ALLOWANCE rows | 4 (57%) | Premium/fee allowance lines |
| ALLOW_MIXED_METHODS | TRUE | Mixed methods are authorized |
| FALLBACK_POLICY | ALLOW_ALLOWANCE | Allowance fallback is authorized |
| Unauthorized method used | NONE | No HISTORICAL or PARAMETRIC methods used without authorization |

Mixed methods are consistent with brief instructions: production hours use RATE_TABLE (primary basis), premium lines use ALLOWANCE (fallback authorized by FALLBACK_POLICY=ALLOW_ALLOWANCE).

---

## Blocker Assessment (from Dependencies)

| Check | Result | Notes |
|---|---|---|
| Dependencies loaded | 13 rows from Dependencies.csv | |
| Upstream prerequisites | DEL-01-04 (near-final base price), DEL-01-05 (template availability) | |
| Blocking estimate production | NONE | Estimate can be produced using PP-25 parametric contract value |
| Blocking estimate accuracy | DEL-01-04 base price finalization | Premium lines (96% of value) will need revision when Schedule A is finalized |

---

## Confidence Distribution

| Confidence Level | Line Count | Amount (CAD) | % of Total |
|---|---|---|---:|
| MEDIUM | 3 | $2,060 | 0.4% |
| LOW | 4 | $543,500 | 99.6% |

**Risk note:** 99.6% of the estimated value is LOW confidence. This is inherent to the deliverable's cost structure -- bond/insurance premiums are percentage-based and depend on a contract value that is not yet determined.

---

## What to Fix for a Cleaner Rerun

1. **Finalize DEL-01-04 Schedule A base price.** Replace PP-25 ($12M parametric estimate) with actual Schedule A line 1-1 value. This will adjust all premium lines.
2. **Obtain insurer CCIP rate quote.** Replace FP-03 recommended rate (2.00%) with actual quoted rate. This could swing the CCIP line by +/- $60,000 (at the $12M level).
3. **Confirm surety broker fee.** Replace FP-19 recommended rate ($3,500) with actual broker quote.
4. After the above, rerun with `BASIS_OF_ESTIMATE=QUOTE` for premium lines if actual quotes are available.

---

## Artifact Checklist (S4)

| Required Artifact | Present | Notes |
|---|---|---|
| Run_Context.md | YES | |
| Summary.md | YES | |
| QA_Report.md | YES | This file |
| Source_Index.md | YES | |
| Decision_Log.md | YES | |
| Assumptions_Log.md | YES | |
| WBS_CBS_Matrix.csv | YES | |
| Detail.csv | YES | Full pricing detail with 7 line items |

---

## Write Quarantine Check (S1)

All files written under `_Estimates/EST_DEL-01-03_2026-02-18_1400/`. No files were modified outside the estimating tool root.
