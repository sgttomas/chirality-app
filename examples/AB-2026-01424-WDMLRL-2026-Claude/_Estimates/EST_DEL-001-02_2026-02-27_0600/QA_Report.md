# QA Report — EST_DEL-001-02_2026-02-27_0600

**RUN_STATUS: OK**

---

## 1. Schema Validity

### Items.csv
- **Parseable:** Yes
- **Required columns present:** ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes — all present.
- **PricingMode values:** UNIT_RATE (5 rows), LUMP_SUM (4 rows) — all valid enum values.
- **Source traceability:** Every row traces to a SourceDoc (Procedure or Specification) and SourceSection.
- **Result:** PASS

### Detail.csv
- **Parseable:** Yes
- **Required columns present:** LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes — all present.
- **Method values:** All 5 rows = PARAMETRIC — valid enum.
- **Allowance/parametric convention:** Not applicable (all rows are UNIT_RATE with measurable quantities; no LS lines in Detail.csv).
- **Result:** PASS

### WBS_CBS_Matrix.csv
- **Parseable:** Yes
- **Required columns present:** WBS_PackageID, WBS_DeliverableID, CBS, Currency, Amount_Total, LineCount, ProvenanceCompletenessPct, Notes — all present.
- **Result:** PASS

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-001-02) |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted (Items.csv) | 9 |
| Items with priced detail (Detail.csv) | 5 |
| Items tracked as scope notes only (no separate pricing) | 4 (ITM-006, ITM-007, ITM-008, ITM-009) |

**Assessment:** All four production documents were read successfully. The quantity takeoff identified 9 priceable/scope items. 5 items correspond to professional labour roles with hours and rates from price sources. 4 items are scope-tracking entries whose effort is captured within the 5 priced labour lines. No priceable scope appears to be missing.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 9 |
| Items priced in Detail.csv | 5 |
| Items with Amount=TBD | 0 |
| Pricing coverage (priced/total items) | 100% (5/5 priced lines; 4 scope-only lines deliberately unpriced) |

**Assessment:** All items that warrant separate pricing have been priced. The 4 scope-only items are explicitly noted as included within the professional staff hours and do not represent coverage gaps.

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 5 / 5 (100%) |
| Detail.csv rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

**Assessment:** All 5 priced lines in Detail.csv have complete SourceRef fields pointing to specific rows in Professional_Staff_Rates.csv (rate) and Level_of_Effort.csv (quantity).

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (5/5 lines) |
| Method mix consistent with basis? | Yes — 100% PARAMETRIC |
| Fallback used? | No |
| ALLOW_MIXED_METHODS triggered? | No |

**Assessment:** PASS — all methods are consistent with the declared PARAMETRIC basis.

---

## 6. Scope Coverage

| Check | Result |
|---|---|
| Deliverables included | 1 (DEL-001-02 Architectural Floor Plans) |
| Deliverables excluded | 0 (scope was single deliverable) |
| Package context | PKG-001 Architectural Design |
| Reasons for exclusion | N/A |

---

## 7. Write Quarantine Check

| Check | Result |
|---|---|
| All files written under _Estimates/? | Yes |
| Any files modified outside _Estimates/? | No |

---

## 8. Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK |
| Quantity takeoff (Items.csv) reviewed for completeness | 9 items extracted; all programmatic spaces and professional activities covered |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported | 100% — no gaps |
| Scope coverage explicit | 1 deliverable included; 0 excluded; reasons documented |
| No writes outside _Estimates/ | Confirmed |

---

## What to Fix for a Cleaner Rerun

1. **Nothing critical.** This run produced a clean estimate with full provenance and consistent method.
2. **Optional improvement:** If actual firm-specific staff rates become available (replacing parametric benchmarks), re-run with RATE_TABLE basis for higher confidence.
3. **Optional improvement:** If the Owner confirms scope changes to floor plan content (e.g., additional sheets, revised program), update the Level_of_Effort.csv inputs and re-run.
