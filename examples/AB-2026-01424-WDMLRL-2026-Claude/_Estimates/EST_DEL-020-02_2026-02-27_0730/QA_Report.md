# QA Report — EST_DEL-020-02_2026-02-27_0730

## RUN_STATUS: OK

---

## 1. Schema Validity

### Items.csv
- **Parseable:** YES
- **Required columns present:** YES (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes)
- **PricingMode values valid:** YES (all values are UNIT_RATE or LUMP_SUM)
- **Row count:** 17 items
- **Every row traces to a source document and section:** YES

### Detail.csv
- **Parseable:** YES
- **Required columns present:** YES (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes)
- **Method values valid:** YES (all PARAMETRIC)
- **Allowance/parametric convention respected:** N/A (all items are UNIT_RATE with hr quantities; no LS parametric lines)
- **Row count:** 8 priced lines

### WBS_CBS_Matrix.csv
- **Parseable:** YES
- **Required columns present:** YES
- **Row count:** 1 summary row

---

## 2. Quantity Takeoff Coverage

| Deliverable | Items Extracted | Documents Read | Missing Documents |
|-------------|----------------|----------------|-------------------|
| DEL-020-02 | 17 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | None |

- All four production documents were read and contributed to item extraction.
- 9 activity items (ITEM-020-02-001 through 009) describe procedural work steps from the Procedure.
- 8 labour items (ITEM-020-02-010 through 017) describe role-based effort from Level_of_Effort.csv cross-referenced with document content.

---

## 3. Pricing Coverage

| Metric | Value |
|--------|-------|
| Total items in Items.csv | 17 |
| Items with corresponding priced lines in Detail.csv | 8 (ITEM-020-02-010 through 017) |
| Items without independent pricing | 9 (ITEM-020-02-001 through 009 — activity items costed via labour allocations) |
| TBD amounts in Detail.csv | 0 |
| Pricing coverage | 100% of labour items priced; 0 TBD amounts |

**Note:** The 9 activity items (ITEM-020-02-001 through 009) are not independently priced because they represent the work activities that the 8 labour roles perform. Pricing them separately would double-count. This is documented in the Decision_Log.

---

## 4. Provenance Completeness

| Metric | Value |
|--------|-------|
| Detail.csv rows with non-TBD SourceRef | 8 of 8 (100%) |
| Detail.csv rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

All 8 priced lines reference both Professional_Staff_Rates.csv (for unit rate) and Level_of_Effort.csv (for quantity). Provenance is complete.

---

## 5. Basis-Consistency Checks

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (8 of 8 lines) |
| Mixed methods? | No — 100% PARAMETRIC |
| Consistent with BASIS_OF_ESTIMATE? | YES |
| ALLOW_MIXED_METHODS setting | TRUE (not exercised; no mixing needed) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised; all items have basis evidence) |

---

## 6. Scope Coverage

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 (DEL-020-02) |
| Deliverables estimated | 1 (DEL-020-02) |
| SOW items covered | SOW-0091, SOW-0092, SOW-0093 |
| Packages | PKG-020 (Commissioning & Closeout) |
| Exclusions | None within the defined scope |

---

## 7. SPEC Validation (S1-S8)

| SPEC | Requirement | Status |
|------|-------------|--------|
| S1 | Write quarantine respected | PASS — all outputs written under _Estimates/EST_DEL-020-02_2026-02-27_0730/ |
| S2 | Snapshot created | PASS — EST_DEL-020-02_2026-02-27_0730 folder exists |
| S3 | BASIS_OF_ESTIMATE validated | PASS — PARAMETRIC is a valid enum value |
| S4 | Required artifacts exist | PASS — Run_Context.md, Items.csv, Summary.md, QA_Report.md, Source_Index.md all present |
| S5 | CSV schema integrity | PASS — Items.csv and Detail.csv contain all required columns with valid enum values |
| S6 | Provenance discipline | PASS — 100% of priced rows have non-TBD SourceRef |
| S7 | Status reporting | PASS — RUN_STATUS declared as OK |
| S8 | Operator acceptance checklist | PASS — see below |

### S8 Operator Acceptance Checklist

- [x] RUN_STATUS is OK (no critical input gaps)
- [x] Quantity takeoff (Items.csv) extracted 17 items from 4 documents
- [x] Basis-consistency check passes (100% PARAMETRIC)
- [x] Provenance completeness is 100%
- [x] Scope coverage explicit (1 deliverable, 3 SOW items, no exclusions)
- [x] No writes occurred outside _Estimates/

---

## 8. What to Fix for a Cleaner Rerun

No issues identified. This is a clean run.

Potential improvements for future iterations:
1. Confirm parametric hourly rates against firm quotes when available (current confidence: MEDIUM).
2. Validate level-of-effort hours against actual project schedule and staffing plan once established.
3. Consider whether any non-labour costs (e.g., third-party inspection fees, printing/reproduction of inspection documents) should be scoped for this deliverable.
