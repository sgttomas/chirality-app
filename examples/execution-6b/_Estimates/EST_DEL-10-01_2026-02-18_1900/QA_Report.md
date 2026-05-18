# QA Report -- EST_DEL-10-01_2026-02-18_1900

## RUN_STATUS: OK

All totals are meaningful. No critical input gaps. No TBD amounts. Full provenance on all line items.

---

## Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| All required columns present | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method enum valid | PASS (all values = RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method lines) |
| Amount = Qty x UnitRate | PASS (L-001: 10 x 175 = 1750; L-002: 4 x 155 = 620) |
| Currency consistent | PASS (all = CAD) |
| Rounding applied | PASS (all amounts are whole dollars) |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-10-01) |
| Deliverables priced | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 2 |

## Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 (100%) |
| Rows with TBD SourceRef | 0 (0%) |
| Top missing-source offenders | None |

## Basis-Consistency

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Methods in Detail.csv | RATE_TABLE (2/2 = 100%) |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS | FALSE |
| Consistency verdict | PASS |

## Blocker Assessment (from Dependencies.csv)

| Blocker ID | Description | Impact | Status |
|---|---|---|---|
| DEP-10-01-003 | DEL-10-02 is upstream prerequisite for site/env risk entries | Does not block estimate pricing; content dependency only | No pricing impact |
| DEP-10-01-010 | 2021 Geotech report location TBD | Does not block estimate pricing; content dependency only | No pricing impact |
| DEP-10-01-011 | Wetland Assessment report location TBD | Does not block estimate pricing; content dependency only | No pricing impact |
| DEP-10-01-012 | Desktop Environmental Assessment location TBD | Does not block estimate pricing; content dependency only | No pricing impact |

**Blocker count affecting pricing: 0**

## Arithmetic Verification

| Line | Qty | UnitRate | Expected Amount | Actual Amount | Match |
|---|---:|---:|---:|---:|---|
| L-001 | 10 | 175 | 1,750 | 1,750 | PASS |
| L-002 | 4 | 155 | 620 | 620 | PASS |
| **Total** | | | **2,370** | **2,370** | **PASS** |

## WBS_CBS_Matrix Reconciliation

| Matrix Total | Detail.csv Total | Match |
|---:|---:|---|
| 2,370 | 2,370 | PASS |

## What to Fix for a Cleaner Rerun

Nothing. This run is clean. All checks pass.
