# QA Report -- EST_DEL-001-01_2026-03-26_1759

**RUN_STATUS: OK**

---

## Schema Validity

| Check | Result | Notes |
|---|---|---|
| Detail.csv parseable | PASS | 5 data rows, all required columns present |
| Detail.csv column completeness | PASS | All 14 required columns populated |
| Method enum validity | PASS | All rows: RATE_TABLE (valid enum) |
| CBS codes valid | PASS | CBS-01, CBS-02 -- both in CBS_Taxonomy.csv |
| WBS_PackageID valid | PASS | PKG-001 confirmed in decomposition |
| WBS_DeliverableID valid | PASS | DEL-001-01 confirmed in decomposition |
| Allowance/parametric convention | N/A | No allowance or parametric-convention lines |
| Amount = Qty x UnitRate | PASS | All 5 rows verified |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables priced | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items total | 5 |
| Line items with TBD amounts | 0 |

## Provenance Completeness

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 5 / 5 (100%) |
| Rows with `location TBD` | 0 |
| Top missing-source offenders | None |

## Basis-Consistency Check

| Check | Result | Notes |
|---|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE | Valid enum |
| Methods used vs basis | PASS | All 5 rows use RATE_TABLE, consistent with brief |
| ALLOW_MIXED_METHODS | TRUE | No fallback needed; all lines match primary method |
| FALLBACK_POLICY | ALLOW_ALLOWANCE | Not exercised (no missing evidence) |

## Blocker Assessment (from Dependencies.csv)

| Blocker | Status | Impact on Estimate |
|---|---|---|
| DEP-001-01-E01: Geotechnical Investigation (DEL-008-01) | PENDING | Does not block this LOE estimate; foundation approach does not affect preliminary architectural design hours |
| DEP-001-01-E02: Preliminary Site Survey (DEL-008-02) | PENDING | Does not block this LOE estimate; site data may affect design content but not design effort hours |
| DEP-001-01-E05: County Approval Gate | PENDING | Does not block this estimate; gate is downstream of preliminary design delivery |

**Blocker count impacting estimate:** 0

## Change vs Prior Snapshot

| Change | Description |
|---|---|
| Scope change SCA-001 | Interior walls changed to precast concrete (Add. 4, Q5) |
| Hours adjustment | +4 hrs Senior Architect, +3 hrs BIM Technician (DEC-001) |
| Total delta | +$1,005 CAD (+9.7%) |
| Method change | Prior: PARAMETRIC; Current: RATE_TABLE (per brief) |

## What to Fix for a Cleaner Rerun

1. Update Level_of_Effort.csv to reflect the precast interior wall scope change natively (eliminating the manual +7 hr adjustment).
2. Obtain firm hourly rate quotes from the architect of record to replace MEDIUM-confidence parametric staff rates.
3. Confirm whether the precast interior wall design requires additional specialist coordination (precast engineer) not currently in the LOE model.
