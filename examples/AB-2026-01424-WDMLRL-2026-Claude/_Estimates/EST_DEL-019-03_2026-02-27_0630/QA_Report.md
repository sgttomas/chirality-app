# QA Report — EST_DEL-019-03_2026-02-27_0630

## RUN_STATUS: OK

**Justification:** All priced line items have complete parametric pricing from validated sources. No TBD amounts. Provenance is 100% complete. The estimate is labour-only by design (consistent with the available price sources) and this limitation is clearly documented.

---

## S1 — Write Quarantine Respected

**PASS.** All output files are written under `_Estimates/EST_DEL-019-03_2026-02-27_0630/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-019-03_2026-02-27_0630` exists under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts are present:

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional; produced) |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | YES |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | YES |
| All rows trace to source document and section | YES (13/13 rows) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | YES — 6 UNIT_RATE, 7 LUMP_SUM |
| Row count | 13 items |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | YES |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | YES |
| Method values valid | YES — all 6 lines are PARAMETRIC |
| Allowance/parametric convention | N/A — all lines are UNIT_RATE with actual Qty and UnitRate (not lump sum parametric) |
| Row count | 6 priced lines |

**Note on Items.csv vs Detail.csv mismatch:** Items.csv has 13 rows; Detail.csv has 6 rows. Items ITM-007 through ITM-013 are process/activity items whose labour cost is fully captured by ITM-001 through ITM-006 (the staff hour items). They are not separately priced in Detail.csv to avoid double-counting. This is documented in Decision_Log.md (DEC-002).

## S6 — Provenance Discipline

**PASS.**

| Metric | Value |
|---|---|
| Total priced rows in Detail.csv | 6 |
| Rows with non-TBD SourceRef | 6 (100%) |
| Rows with `location TBD` | 0 |
| Provenance completeness | 100% |

**Top missing-source offenders:** None. All rows have complete provenance.

Each SourceRef traces to a specific row in Professional_Staff_Rates.csv (for the hourly rate) and Level_of_Effort.csv (for the hour quantity).

## S7 — Status Reporting

**RUN_STATUS = OK**

- Totals are meaningful ($5,590.00 CAD).
- No critical input gaps.
- All line items priced with PARAMETRIC method from validated sources.
- Labour-only limitation is a known scope constraint of the price sources, not a pricing failure.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No gaps |
| Items.csv reviewed for completeness | COMPLETE | 13 items covering all Procedure steps and all LOE roles |
| Basis-consistency checks pass | PASS | All 6 Detail.csv lines use PARAMETRIC method, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | 100% | All rows traceable to named source files and rows |
| Scope coverage explicit | YES | 1 deliverable (DEL-019-03) in 1 package (PKG-019); included/excluded stated in Summary.md |
| No writes outside _Estimates/ | CONFIRMED | All outputs in EST_DEL-019-03_2026-02-27_0630/ |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-019-03 | 4/4 (Datasheet, Specification, Guidance, Procedure) | 13 | None |

### Items by Source Document

| SourceDoc | Item Count |
|---|---|
| Procedure | 12 |
| Specification | 1 |

### Items by Pricing Mode

| PricingMode | Item Count |
|---|---|
| UNIT_RATE | 6 |
| LUMP_SUM | 7 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 13 |
| Items priced in Detail.csv | 6 |
| Items not separately priced (process items, cost captured in staff hours) | 7 |
| Amount = TBD | 0 |
| Total amount | $5,590.00 CAD |

---

## What to Fix for a Cleaner Rerun

1. **Non-labour cost sources.** If a price source for non-labour costs (document management software, legal review, printing) becomes available, it should be added to PRICE_SOURCES to enable a more comprehensive estimate.
2. **Hour granularity.** The Level_of_Effort.csv provides aggregate hours per role for the entire deliverable. A more detailed effort breakdown by Procedure step would improve estimate granularity and confidence.
3. **Process item pricing.** Items ITM-007 through ITM-013 could be individually priced if effort data were available at the process-step level, rather than relying on the aggregate role-hour allocation.
