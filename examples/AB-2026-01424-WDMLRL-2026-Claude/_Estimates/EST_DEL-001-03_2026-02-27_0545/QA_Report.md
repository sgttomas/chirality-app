# QA Report — EST_DEL-001-03_2026-02-27_0545

## RUN_STATUS: OK

All totals are meaningful; no critical input gaps. All 5 line items priced from parametric sources with full provenance.

---

## S1 — Write Quarantine Respected

**PASS.** All files written exclusively under `_Estimates/EST_DEL-001-03_2026-02-27_0545/`. No project truth files modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-001-03_2026-02-27_0545` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:

| Artifact | Status |
|---|---|
| Run_Context.md | Created |
| Items.csv | Created |
| Summary.md | Created |
| QA_Report.md | Created (this file) |
| Source_Index.md | Created |
| Detail.csv | Created |
| WBS_CBS_Matrix.csv | Created |
| Decision_Log.md | Created |
| Assumptions_Log.md | Created |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| Row count | 5 rows |
| PricingMode values valid | Yes — all UNIT_RATE (valid enum) |
| All rows trace to source document and section | Yes — all SourceDoc = Procedure; all SourceSection populated |
| Qty values | All numeric (54, 42, 24, 6, 4) — no TBDs |
| Unit values | All "hr" — consistent with design effort items |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Row count | 5 rows |
| Method values valid | Yes — all PARAMETRIC (valid enum) |
| Allowance/parametric convention | N/A — items are UNIT_RATE with Qty > 1 and Unit = hr; convention applies only to LS items |
| All ItemIDs trace to Items.csv | Yes — ITM-001 through ITM-005 |
| Amount computation | All rows: Amount = Qty * UnitRate (verified) |

**Amount verification:**

| LineID | Qty | UnitRate | Expected Amount | Actual Amount | Match |
|---|---|---|---|---|---|
| LN-001 | 54 | 180 | 9720 | 9720 | Yes |
| LN-002 | 42 | 135 | 5670 | 5670 | Yes |
| LN-003 | 24 | 95 | 2280 | 2280 | Yes |
| LN-004 | 6 | 165 | 990 | 990 | Yes |
| LN-005 | 4 | 135 | 540 | 540 | Yes |
| **TOTAL** | **130** | — | **19200** | **19200** | **Yes** |

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Total priced rows | 5 |
| Rows with non-TBD SourceRef | 5 |
| Provenance completeness | 100% |
| Top missing-source offenders | None |

All SourceRef entries point to specific rows in Level_of_Effort.csv (for hours) and Professional_Staff_Rates.csv (for rates).

## S7 — Status Reporting

**RUN_STATUS = OK.**

Justification:
- All 5 items priced with meaningful amounts
- No TBD quantities or rates
- No critical input gaps
- All provenance complete
- Basis consistency: 100% PARAMETRIC (matches BASIS_OF_ESTIMATE)

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No gaps |
| Quantity takeoff reviewed for completeness | PASS | 5 items covering all LOE roles for this deliverable type |
| Basis-consistency checks pass | PASS | All lines PARAMETRIC; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% |
| Scope coverage explicit | PASS | 1 deliverable (DEL-001-03); all roles from LOE data included |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-001-03 | _CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 5 |

All four production documents were available and read. Items were extracted based on the Level_of_Effort.csv role assignments for DEL-001-03, validated against the Procedure document work steps.

## Pricing Coverage

| Metric | Value |
|---|---|
| Items in takeoff | 5 |
| Items with price | 5 (100%) |
| Items with TBD price | 0 (0%) |
| Total estimate | $19,200 CAD |

## Basis-Consistency Check

| Method | Line Count | % of Lines | Amount | % of Amount |
|---|---|---|---|---|
| PARAMETRIC | 5 | 100% | 19,200 | 100% |
| Other | 0 | 0% | 0 | 0% |

**Consistent with BASIS_OF_ESTIMATE = PARAMETRIC.** No mixed methods; no fallback required.

## What to Fix for a Cleaner Rerun

Nothing required. This is a clean run with:
- All documents available
- All pricing sources indexed and used
- 100% pricing coverage
- 100% provenance completeness
- No TBDs, no warnings, no fallbacks

Optional improvements for future runs:
1. **Bottom-up hour estimates** could replace the parametric LOE allocation if the Architect provides task-level effort breakdowns for exterior elevation production specifically (vs. a generic Drawing Set allocation).
2. **Rate confidence** could be upgraded from MEDIUM to HIGH if firm rate quotes are obtained from staff or subconsultants.
