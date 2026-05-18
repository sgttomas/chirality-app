# QA Report — EST_DEL-002-08_2026-02-27_0630

**RUN_STATUS: WARNINGS**

---

## 1. Schema Validity

### Items.csv
- **Parseable:** YES
- **Required columns present:** YES (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes)
- **PricingMode values valid:** YES (all values are UNIT_RATE or LUMP_SUM)
- **Row count:** 6 items
- **Result:** PASS

### Detail.csv
- **Parseable:** YES
- **Required columns present:** YES (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes)
- **Method values valid:** YES (all values are PARAMETRIC)
- **Allowance/parametric convention check:** LN-005 uses Qty=1, Unit=LS, UnitRate=0.00, Amount=0.00 — compliant (zero-value lump sum). LN-006 uses Qty=1, Unit=LS, UnitRate=TBD, Amount=TBD — convention acceptable for TBD items.
- **Row count:** 6 lines
- **Result:** PASS

### WBS_CBS_Matrix.csv
- **Parseable:** YES
- **Required columns present:** YES
- **Totals consistent with Detail.csv:** YES (Management $1,530 + Design $17,700 = $19,230 total; matches sum of Detail.csv priced lines)
- **Result:** PASS

---

## 2. Quantity Takeoff Coverage

| Deliverable | Documents Available | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|---|
| DEL-002-08 | 4 of 4 | 4 of 4 | 6 | None |

- **Datasheet.md:** Read. Provides steel plate zone descriptions, material TBDs, conditions, and construction artifacts.
- **Specification.md:** Read. Provides 11 requirements and verification matrix.
- **Guidance.md:** Read. Provides principles, considerations, and trade-offs.
- **Procedure.md:** Read. Provides 8-step work procedure with prerequisites and verification checks. Primary source for work activity item extraction.

**Result:** PASS — all 4 documents present and read.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 6 |
| Items with Amount (priced) | 5 |
| Items with Amount = TBD | 1 (ITM-006 / LN-006 — peer review) |
| Pricing coverage | 83% (5 of 6) |
| Priced total | $19,230.00 CAD |

**Top TBD items:**
1. **LN-006 (ITM-006):** Independent peer review of IFC drawings — hours not in Level_of_Effort.csv; ASSUMPTION-tagged activity in Procedure Enrichment D-003. Estimated impact if priced: $680-$1,360 CAD (4-8 hrs Structural Engineer @ $170/hr).

**Result:** PASS with WARNING — material TBD exists but is bounded and non-critical (peer review is a best-practice enrichment, not a contractual requirement).

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail.csv lines | 6 |
| Lines with SourceRef (non-TBD) | 6 of 6 |
| Provenance completeness | 100% |

All lines include explicit SourceRef pointing to pricing source files (Professional_Staff_Rates.csv and Level_of_Effort.csv) or to Procedure sections.

**Result:** PASS

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE declared | PARAMETRIC |
| All Method values in Detail.csv | PARAMETRIC (6 of 6) |
| Method mix consistent with basis | YES — 100% PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE (permitted but not exercised) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not invoked) |

**Result:** PASS — no method deviations.

---

## 6. Scope Coverage

- **Scope requested:** DEL-002-08
- **Deliverables included:** 1 (DEL-002-08 Steel Plate Embedment Plan)
- **Deliverables excluded:** 0
- **Package context:** PKG-002 Structural Design
- **Reason for inclusions/exclusions:** Single-deliverable scope per INIT-TASK brief.

**Result:** PASS

---

## 7. Write Quarantine Check

- All output files written to: `_Estimates/EST_DEL-002-08_2026-02-27_0630/`
- No files written outside `_Estimates/`.
- No modifications to deliverable content, lifecycle files, decomposition outputs, or dependency registers.

**Result:** PASS

---

## 8. RUN_STATUS Determination

| Criterion | Status |
|---|---|
| S1 — Write quarantine respected | PASS |
| S2 — Snapshot created | PASS |
| S3 — BASIS_OF_ESTIMATE validated | PASS (PARAMETRIC) |
| S4 — Required artifacts exist | PASS (Run_Context.md, Items.csv, Summary.md, QA_Report.md, Source_Index.md) |
| S5 — CSV schema integrity | PASS |
| S6 — Provenance discipline | PASS (100% provenance) |
| S7 — Status reporting | WARNINGS |
| S8 — Operator acceptance checklist | See below |

**RUN_STATUS = WARNINGS**

Rationale: Totals are meaningful ($19,230.00 CAD) and based on consistent PARAMETRIC method with full provenance. However, one TBD item (peer review) represents a bounded gap ($680-$1,360 estimated range if required). The TBD is clearly identified, bounded, and non-critical.

---

## 9. Operator Acceptance Checklist (S8)

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | YES | WARNINGS; single TBD is bounded at $680-$1,360 CAD |
| Quantity takeoff (Items.csv) reviewed for completeness | YES | 6 items covering all procedure steps and work activities |
| Basis-consistency checks pass | YES | 100% PARAMETRIC |
| Provenance completeness reported | YES | 100% SourceRef coverage |
| Scope coverage explicit | YES | 1 deliverable included; 0 excluded |
| No writes outside _Estimates/ | YES | Confirmed |

---

## 10. What to Fix for a Cleaner Rerun

1. **Resolve peer review scope (ITM-006):** Project team should decide whether independent peer review is required for DEL-002-08 IFC drawings. If yes, add 4-8 hours of Structural Engineer time to Level_of_Effort.csv for DEL-002-08 with a note referencing Procedure Enrichment D-003. This would bring pricing coverage to 100% and RUN_STATUS to OK.

2. **Rate confidence upgrade:** If project-specific subcontract rates or firm proposals become available, update Professional_Staff_Rates.csv Confidence from MEDIUM to HIGH for the applicable roles. This does not change the estimate total but improves confidence scoring.
