# QA Report — EST_DEL-004-08_2026-02-27_0600

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under _Estimates/ | PASS |
| No project truth files modified | PASS |
| No deliverable content modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |

**Result: PASS**

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: EST_DEL-004-08_2026-02-27_0600/ | PASS |
| Snapshot folder is new (not overwriting prior) | PASS |
| UPDATE_LATEST_POINTER = FALSE; no pointer file modified | PASS |

**Result: PASS**

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS |
| Value is valid enum member (QUOTE / RATE_TABLE / HISTORICAL / PARAMETRIC / ALLOWANCE) | PASS |

**Result: PASS**

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT (optional; included for full run) |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

**Result: PASS**

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| All rows have non-empty SourceDoc | PASS |
| All rows have non-empty SourceSection | PASS |
| Row count | 30 rows |
| LUMP_SUM rows: Qty=1, Unit=LS | PASS (26 rows) |
| UNIT_RATE rows: Qty is numeric, Unit is valid | PASS (4 rows: hr) |

### Detail.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| All Amount values are numeric (no TBD) | PASS |
| Currency consistent (CAD) | PASS |
| Allowance/parametric convention not applicable (all lines are UNIT_RATE with hours) | N/A |
| Row count | 4 rows |

**Result: PASS**

---

## S6 — Provenance Discipline

| Check | Result |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 4 / 4 (100%) |
| Detail.csv rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

**Provenance completeness: 100%**

**Result: PASS**

---

## S7 — Status Reporting

| Check | Result |
|---|---|
| RUN_STATUS declared | OK |
| Totals are meaningful | PASS — $13,050.00 CAD total, fully sourced |
| Critical input gaps | None for pricing; technical TBDs exist in deliverable scope (crane data, welding specs, CEC edition) but do not affect parametric LOE pricing |

**Result: PASS**

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | All items priced; no TBD amounts |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 30 items extracted from all 4 documents; 24 requirements from Specification, 6 procedural/management items |
| Basis-consistency checks | PASS | All Detail.csv Method values = PARAMETRIC, matching BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% — all rows have SourceRef |
| Scope coverage explicit | PASS | 1 deliverable in scope, 1 estimated; no exclusions |
| No writes outside _Estimates/ | PASS | Verified |

**Result: PASS — Snapshot is acceptable for publication**

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-004-08 | Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 30 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 30 |
| Items with pricing applied (via Detail.csv role lines) | 30 (all scope items covered by 4 role-based Detail lines) |
| Items with TBD pricing | 0 |
| Pricing coverage | 100% |

---

## Basis-Consistency

| Metric | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Methods used in Detail.csv | PARAMETRIC (4/4 lines) |
| Method deviations from basis | None |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| Fallback invocations | 0 |

---

## What to Fix for a Cleaner Rerun

1. **No fixes required for pricing.** All lines are fully priced with PARAMETRIC method.
2. **Optional enhancement:** If a more granular estimate is desired, the 56 Electrical Engineer hours and 24 BIM Technician hours could be allocated across the 24 technical items (ITEM-001 through ITEM-026) to provide per-calculation-section effort visibility. This would require an effort allocation model not present in current PRICE_SOURCES.
3. **Optional enhancement:** Include disbursement, overhead, and profit line items if the estimate scope is expanded beyond professional labour.
4. **Technical TBDs in deliverable documents** (crane data, welding specs, exhaust fan data, CEC edition) are scope risks but do not affect the current parametric estimate. If these TBDs result in scope growth, a re-estimate with updated LOE would be warranted.
