# QA Report — EST_DEL-001-06_2026-02-27_0630

**RUN_STATUS: OK**

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
| Snapshot folder exists: EST_DEL-001-06_2026-02-27_0630/ | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS — valid enum value |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PASS |
| Items.csv | PASS |
| Summary.md | PASS |
| QA_Report.md | PASS (this file) |
| Source_Index.md | PASS |
| Decision_Log.md | PASS |
| Assumptions_Log.md | PASS |
| WBS_CBS_Matrix.csv | PASS |
| Detail.csv | PASS (optional; produced) |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 23 items |
| Items with TBD quantities | 3 (ITM-016, ITM-018, ITM-019) — flagged in notes; these are scope elements on drawings, not independently procured |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all PARAMETRIC) | PASS |
| Row count | 5 priced lines |
| Allowance/parametric convention | N/A — all lines are UNIT_RATE with explicit Qty, Unit, and UnitRate; no LS parametric lines |

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows in Detail.csv | 5 |
| Rows with non-TBD SourceRef | 5 (100%) |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

All five priced line items have SourceRef pointing to specific rows in Professional_Staff_Rates.csv and Level_of_Effort.csv.

---

## S7 — Status Reporting

| Field | Value |
|---|---|
| **RUN_STATUS** | **OK** |
| Rationale | All priced line items have complete provenance. Totals are meaningful. No critical input gaps. All 5 labour roles have both hours and rates from price sources. No TBD amounts in Detail.csv. |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | RUN_STATUS = OK |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 23 items extracted covering all four source documents; 3 items with TBD quantities are drawing-element counts that do not affect pricing |
| Basis-consistency checks pass | PASS | All 5 Detail.csv lines use Method=PARAMETRIC, matching BASIS_OF_ESTIMATE=PARAMETRIC; no mixed methods |
| Provenance completeness reported | PASS | 100% provenance in Detail.csv |
| Scope coverage explicit | PASS | 1 deliverable in scope (DEL-001-06); all 4 documents read; all spaces and elements from Datasheet captured in Items.csv |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet | 14 items (ITM-009 through ITM-023 excluding ITM-020, ITM-021, ITM-022) | Spaces, ceiling-mounted elements, construction attributes |
| Specification | 1 item (ITM-023 P.Eng. stamp) | Verification/compliance requirements |
| Guidance | 0 items directly | Guidance informs trade-offs and principles; no additional priceable items identified beyond those in Datasheet |
| Procedure | 8 items (ITM-001 through ITM-008, ITM-020, ITM-021, ITM-022) | Work activities, coordination steps, field verification, QA |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 23 |
| Items with priced lines in Detail.csv | 5 (labour roles covering ITM-001 through ITM-005) |
| Items not independently priced | 18 (scope items whose effort is embedded in the 5 labour line items) |
| Items with TBD amounts in Detail.csv | 0 |
| Pricing coverage of labour cost | 100% |

---

## What to Fix for a Cleaner Rerun

1. No critical fixes required. This run produced complete results.
2. **Optional improvement:** If future price sources include separate line items for P.Eng. stamp fees, field survey costs, or printing/reproduction costs, those could be broken out as separate priced lines in Detail.csv rather than embedded in labour hours.
3. **Optional improvement:** Resolve TBD quantities for exhaust fans (ITM-016), forced air makeup units (ITM-018), and exhaust hose drop points (ITM-019) once mechanical/electrical coordination confirms counts. This does not affect cost since these are drawing elements, not procured items.
