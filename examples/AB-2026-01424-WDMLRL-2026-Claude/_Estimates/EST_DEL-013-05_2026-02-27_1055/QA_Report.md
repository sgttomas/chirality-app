# QA Report — EST_DEL-013-05_2026-02-27_1055

## RUN_STATUS: WARNINGS

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written exclusively under `{RUN_ROOT}/_Estimates/EST_DEL-013-05_2026-02-27_1055/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-013-05_2026-02-27_1055` created under `{RUN_ROOT}/_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts produced:
- Run_Context.md
- Items.csv (22 items)
- Summary.md
- QA_Report.md (this file)
- Source_Index.md
- Decision_Log.md
- Assumptions_Log.md
- Detail.csv (22 lines)
- WBS_CBS_Matrix.csv

## S5 — CSV Schema Integrity

### Items.csv
**PASS.** Parseable CSV with all required columns (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes). All 22 rows have valid PricingMode values (UNIT_RATE or LUMP_SUM). Every row traces to a source document (Datasheet, Specification, or Procedure) and source section.

### Detail.csv
**PASS.** Parseable CSV with all required columns (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes). All 22 rows have valid Method values (ALLOWANCE or PARAMETRIC). Lump-sum rows correctly use Qty=1, Unit=LS, UnitRate=Amount convention where applicable.

**Exception noted:** DL-009 (spark arrestor) has Amount=0.00 which is valid (contingent item) but flagged as W-005.

## S6 — Provenance Discipline

**PASS.** Every priced row in Detail.csv includes a SourceRef pointing to a specific price source file and rate/row reference. No rows use "location TBD" for SourceRef.

| Metric | Value |
|---|---|
| Provenance completeness | 22/22 (100%) |
| Top missing-source offenders | None |

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Rationale: Totals are meaningful ($22,338.70 CAD) and all items are priced, but material TBDs and assumptions remain:
- 35.8% of the total ($8,000) is based on ALLOWANCE method with LOW confidence (MS-05 rate with wide range $4,500-$12,000)
- Welding station count not confirmed (assumes 1)
- Welding process types TBD (affects filtration and cost)
- All system design parameters TBD (fan sizing, ductwork routing, stack height)
- Method mix (ALLOWANCE + PARAMETRIC) is authorized under ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_PARAMETRIC

This is not FAILED_INPUTS because pricing sources exist and produce meaningful totals. It is not OK because the LOW confidence equipment pricing and multiple TBD design parameters create material uncertainty.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | PASS | WARNINGS with 6 specific, bounded gaps documented in Summary.md |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 22 items extracted covering all equipment, labour, design, management, and closeout scope from all 4 documents |
| Basis-consistency checks pass | PASS (with deviation) | 64.2% PARAMETRIC (matches BASIS_OF_ESTIMATE), 35.8% ALLOWANCE (authorized by ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_PARAMETRIC). Deviation logged in Decision_Log.md. |
| Provenance completeness reported | PASS | 100% provenance on all 22 lines |
| Scope coverage explicit | PASS | 1 deliverable in scope, 0 excluded, 4/4 documents read |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | 9 | Equipment and material components (ITM-001 through ITM-009) |
| Specification.md | 1 | Fire/spark hazard mitigation item (ITM-009 also sourced from Specification REQ-013) |
| Procedure.md | 12 | Design, permitting, procurement, installation labour, commissioning, closeout, management roles, photography |
| Guidance.md | 0 direct items | Guidance informed trade-off considerations and design context but did not independently identify priceable items beyond those in Datasheet/Specification/Procedure |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Items priced | 22/22 (100%) |
| Items with Amount > $0 | 21/22 (95.5%) |
| Items with Amount = TBD | 0/22 (0%) |
| Items with Amount = $0 (contingent) | 1/22 (4.5%) — DL-009 spark arrestor |

---

## Basis-Consistency Check

| Method | Expected per BASIS_OF_ESTIMATE | Actual | Authorized? |
|---|---|---|---|
| PARAMETRIC | Primary | 13 lines, $14,338.70 (64.2%) | Yes — primary basis |
| ALLOWANCE | Fallback | 9 lines, $8,000.00 (35.8%) | Yes — authorized by ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_PARAMETRIC |
| QUOTE | Not used | 0 lines | N/A |
| RATE_TABLE | Not used | 0 lines | N/A |
| HISTORICAL | Not used | 0 lines | N/A |

---

## What to Fix for a Cleaner Rerun

1. **Obtain County welding equipment specifications** to resolve welding process types and inform filtration selection.
2. **Confirm welding station count** (1 or more) with County to resolve CT-002 conflict and size system correctly.
3. **Complete mechanical design** to replace MS-05 allowance with engineered equipment specifications and firm pricing (quotes from suppliers).
4. **Obtain equipment quotes** to replace ALLOWANCE pricing with QUOTE basis (higher confidence).
5. **Define installation labour hours** based on actual ductwork routing from IFC drawings.
6. **Resolve spark arrestor requirement** per design engineer fire/spark evaluation (REQ-013).
7. **Confirm commissioning test method and acceptance thresholds** to refine commissioning effort estimate.
