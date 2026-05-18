# QA Report — EST_DEL-011-06_2026-02-27_0600

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful for budget planning purposes. Material TBDs and assumptions remain, particularly around pit dimensions (all quantities are assumed) and several line items lacking direct price source support. The estimate is not suitable for firm bid pricing without IFC structural drawings.

---

## S1 — Write Quarantine Respected

**PASS.** All output files were written exclusively under `_Estimates/EST_DEL-011-06_2026-02-27_0600/`. No files outside the estimating tool root were modified.

---

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-011-06_2026-02-27_0600` created under `_Estimates/`.

---

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

---

## S4 — Required Artifacts Exist

**PASS.** All required files are present:

| File | Status |
|---|---|
| Run_Context.md | Present |
| Items.csv | Present |
| Summary.md | Present |
| QA_Report.md | Present |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |
| Detail.csv | Present (optional but recommended — produced) |
| Risk_Register.md | Present (optional — produced due to identified risks) |

---

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| All rows trace to source document and section | Yes — 19/19 rows have SourceDoc and SourceSection populated |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | Yes — 9 UNIT_RATE, 10 LUMP_SUM |
| Row count | 19 items |

### Detail.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Method values valid (QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC) | Yes — all 19 rows use PARAMETRIC |
| Allowance/parametric convention (LS items: Qty=1, Unit=LS, UnitRate=Amount) | Yes — verified for all lump-sum items |
| ItemID traceability to Items.csv | Yes — all 19 Detail lines reference valid ItemIDs |
| Row count | 19 lines |

---

## S6 — Provenance Discipline

### Provenance Completeness

| Category | Count | Pct |
|---|---|---|
| Lines with direct price source SourceRef | 11 | 57.9% |
| Lines with assumption-only SourceRef | 8 | 42.1% |
| Lines with TBD SourceRef | 0 | 0% |
| **Total** | **19** | **100%** |

### Top Missing-Source Offenders

The following lines lack direct price source support and rely on parametric assumptions recorded in Assumptions_Log.md:

| LineID | Description | Confidence | Issue |
|---|---|---|---|
| DL-006 | Waterproofing / damp-proofing | LOW | No waterproofing rate in any price source |
| DL-007 | Pit interior lining and finishing | LOW | No finish/lining rate in any price source |
| DL-008 | Safety railings and edge protection | MED | No railing rate in any price source; parametric assumption used |
| DL-009 | Pit cover / grating system | MED | No grating rate in any price source; parametric assumption used |
| DL-011 | Ventilation rough-in provisions | LOW | Lump-sum allowance; no rate basis |
| DL-012 | Lighting rough-in provisions | LOW | Lump-sum allowance; no rate basis |
| DL-013 | Floor drain rough-in provisions | LOW | Lump-sum allowance; no rate basis; scope boundary TBD |
| DL-014 | Excavation safety measures | LOW | Lump-sum allowance; depends on soil conditions |

---

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Totals exist and are meaningful for budget planning. Material TBDs and assumptions remain:
- All quantities based on assumed pit dimensions (not confirmed by IFC drawings)
- 42.1% of priced lines lack direct price source support
- 4 unresolved Guidance Conflict Table items affecting scope and design decisions
- Overall estimate confidence: LOW-MEDIUM

---

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are bounded and documented |
| Items.csv reviewed for completeness | PASS | 19 items covering all priceable scope from the four documents |
| Basis-consistency checks pass | PASS | All 19 Detail lines use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 57.9% direct source; 42.1% assumption-based; 0% TBD |
| Scope coverage explicit | PASS | 1 deliverable (DEL-011-06) fully covered; 4 documents read; 0 missing documents |
| No writes outside _Estimates/ | PASS | All output under _Estimates/EST_DEL-011-06_2026-02-27_0600/ |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-011-06 | Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 19 |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 19 |
| Items priced in Detail.csv | 19 (100%) |
| Items with TBD Amount | 0 |
| Items with Amount = 0 | 0 |
| Total estimate (CAD) | $97,160 |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (19/19 = 100%) |
| ALLOW_MIXED_METHODS | TRUE (but no mixing needed — all PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (no fallback needed — all items priced) |
| Consistency | PASS — 100% method alignment with stated basis |

---

## What to Fix for a Cleaner Rerun

1. **Obtain IFC structural drawings (DEL-002-06)** to replace assumed pit dimensions with confirmed quantities.
2. **Obtain Owner equipment fleet dimensions** from Camrose County to validate pit depth and width assumptions.
3. **Resolve Guidance Conflict Table items** C-011-06-01 through C-011-06-04, especially the floor drainage scope boundary.
4. **Add waterproofing, lining, railing, and grating rates** to price sources for direct provenance support.
5. **Add MEP rough-in pricing** to price sources (ventilation, electrical, plumbing rough-in rates).
6. **Confirm cold-weather concrete protection scope** based on anticipated construction schedule.
7. **Confirm as-built survey requirement** per RFP section 3.3.2 applicability to this specific deliverable.
