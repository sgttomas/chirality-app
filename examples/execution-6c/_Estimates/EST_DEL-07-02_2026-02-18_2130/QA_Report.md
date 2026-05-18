# QA Report — EST_DEL-07-02_2026-02-18_2130

## RUN_STATUS: OK

---

## Schema Validity (Detail.csv)

- [PASS] Detail.csv is parseable CSV.
- [PASS] All 14 required columns present: LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes.
- [PASS] Method values: all rows = `RATE_TABLE` (valid enum).
- [PASS] No ALLOWANCE or PARAMETRIC rows; allowance/parametric convention check not applicable.
- [PASS] Amounts are numeric and rounded to DOLLAR.
- [PASS] Currency = CAD on all rows.

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (priced) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Total line items | 2 |
| Total amount (CAD) | $1,860 |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 |
| Rows with TBD SourceRef | 0 |
| **Provenance completeness** | **100%** |

No missing-source offenders.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Method values in Detail.csv | All RATE_TABLE |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS setting | FALSE |
| **Basis consistency** | **PASS** |

---

## Blocker Assessment (from dependency evidence)

| DependencyID | Direction | Target | Type | Impact on Estimate |
|---|---|---|---|---|
| DEP-07-02-004 | UPSTREAM | DEL-07-01 (Firm Experience Profile) | INTERFACE | Not a pricing blocker; coordination data for content consistency |
| DEP-07-02-005 | DOWNSTREAM | DEL-07-03 (Appendix I) | HANDOVER | Not a pricing blocker; DEL-07-02 feeds DEL-07-03 |
| DEP-07-02-006 | UPSTREAM | DEL-08-01 (Project Schedule) | INTERFACE | Not a pricing blocker; schedule data for availability alignment |
| DEP-07-02-007 | DOWNSTREAM | DEL-01-02 (Formal Submission) | HANDOVER | Not a pricing blocker; final package handover |

**Blocker count:** 0 (no dependencies block the estimate for DEL-07-02)

---

## Arithmetic Verification

| LineID | Qty | UnitRate | Expected Amount | Actual Amount | Match |
|---|---:|---:|---:|---:|---|
| L-07-02-01 | 12 | 85 | 1020 | 1020 | PASS |
| L-07-02-02 | 8 | 105 | 840 | 840 | PASS |
| **Total** | | | **1860** | **1860** | **PASS** |

---

## WBS_CBS_Matrix Consistency

- [PASS] Matrix total ($1,860) matches Detail.csv sum ($1,860).
- [PASS] Line count in matrix (2) matches Detail.csv row count (2).
- [PASS] ProvenanceCompletenessPct (100%) matches provenance assessment above.

---

## Spec Compliance

| Spec | Status | Notes |
|---|---|---|
| S1 — Write quarantine | PASS | All writes under `_Estimates/EST_DEL-07-02_2026-02-18_2130/` |
| S2 — Snapshot created | PASS | Snapshot folder exists |
| S3 — BASIS_OF_ESTIMATE validated | PASS | RATE_TABLE is a valid enum value |
| S4 — Required artifacts exist | PASS | Run_Context.md, Summary.md, QA_Report.md, Source_Index.md all present |
| S5 — Detail schema integrity | PASS | All columns present; Method values valid; no convention violations |
| S6 — Provenance discipline | PASS | 100% provenance completeness; no TBD SourceRefs |
| S7 — Status reporting | PASS | RUN_STATUS = OK declared |
| S8 — Operator acceptance | PASS | No critical gaps; totals meaningful; scope fully covered |

---

## What to Fix for a Cleaner Rerun

Nothing required. This is a clean run with full coverage, 100% provenance, and consistent basis methodology. The estimate is ready for aggregation.
