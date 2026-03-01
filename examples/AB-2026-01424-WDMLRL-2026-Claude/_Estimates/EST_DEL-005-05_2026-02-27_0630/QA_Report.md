# QA Report — EST_DEL-005-05_2026-02-27_0630

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS — EST_DEL-005-05_2026-02-27_0630/ |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | PASS — PARAMETRIC |
| Value is valid enum | PASS — PARAMETRIC is in {QUOTE, RATE_TABLE, HISTORICAL, PARAMETRIC, ALLOWANCE} |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PASS |
| Items.csv | PASS |
| Summary.md | PASS |
| QA_Report.md | PASS (this file) |
| Source_Index.md | PASS |
| Detail.csv | PASS (optional; produced) |
| WBS_CBS_Matrix.csv | PASS |
| Decision_Log.md | PASS |
| Assumptions_Log.md | PASS |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS — all 9 columns present |
| All rows trace to a source document | PASS — every row has SourceDoc in {Datasheet, Specification, Guidance, Procedure} |
| All rows have SourceSection | PASS |
| PricingMode values valid | PASS — all values in {UNIT_RATE, LUMP_SUM} |
| Row count | 19 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS — all 15 columns present |
| Method values valid | PASS — all values are PARAMETRIC |
| Allowance/parametric convention | N/A — no allowance lines; all lines are UNIT_RATE with actual Qty and UnitRate |
| Row count | 4 priced lines |

---

## S6 — Provenance Discipline

| Check | Result |
|---|---|
| Priced rows with SourceRef | 4 of 4 (100%) |
| Priced rows with "location TBD" SourceRef | 0 of 4 (0%) |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

---

## S7 — Status Reporting

| Field | Value |
|---|---|
| **RUN_STATUS** | **OK** |
| Rationale | All 4 priced line items have meaningful amounts derived from PARAMETRIC sources (staff rates x LOE hours). No TBD amounts. No critical input gaps. Provenance is 100% complete. Basis-consistency check passes (all PARAMETRIC, matching BASIS_OF_ESTIMATE). |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — OK | |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 19 items extracted from 4 documents; 4 are directly priceable staff-hour items; 15 are scope-tracking items (design activities priced through staff hours) |
| Basis-consistency checks pass | PASS | All 4 Detail.csv lines use PARAMETRIC method; matches BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% — all lines have full SourceRef |
| Scope coverage explicit | PASS | 1 deliverable in scope (DEL-005-05); all 4 documents read; no missing documents |
| No writes outside _Estimates/ | PASS | |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted | Priceable Staff Lines |
|---|---|---|---|---|
| DEL-005-05 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | 0 | 19 | 4 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 19 |
| Items with direct pricing in Detail.csv | 4 (staff-hour line items ITM-001 through ITM-004) |
| Items tracked as scope items (priced through staff hours) | 15 (ITM-005 through ITM-019) |
| Items with TBD amounts | 0 |
| Pricing coverage | 100% of priceable items |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4 of 4 lines) |
| Non-matching methods | 0 |
| ALLOW_MIXED_METHODS | TRUE (not needed — all PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not needed — all primary method) |

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes required.** This run produced a complete, fully-priced estimate with 100% provenance.

2. **Optional improvements:**
   - If a construction value estimate becomes available for the overall project, a cross-check against the Professional_Design_Fees.csv civil fee percentage (DF-05: recommended 1.0% of construction value) would provide an independent reasonableness validation.
   - If the geotechnical report (PKG-008) results in design revisions requiring additional hours, the LOE model should be updated and the estimate rerun.
   - Items ITM-005 through ITM-019 are scope-tracking items that do not carry independent pricing. If a more granular allocation of staff hours across design activities is desired, the LOE model could be decomposed into activity-level allocations.
