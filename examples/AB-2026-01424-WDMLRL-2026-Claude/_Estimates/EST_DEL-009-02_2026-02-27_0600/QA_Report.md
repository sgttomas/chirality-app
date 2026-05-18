# QA_Report.md
## EST_DEL-009-02_2026-02-27_0600

---

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all line items are priced, but material parametric assumptions exist for 12 of 15 line items where LOE source data was incomplete. The estimate is usable with bounded gaps.

---

## Schema Validity

### Items.csv

| Check | Result |
|-------|--------|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have valid PricingMode (UNIT_RATE or LUMP_SUM) | PASS — 14 UNIT_RATE, 1 LUMP_SUM |
| All rows trace to a source document | PASS — all rows reference Procedure, Specification, or Datasheet |
| All rows trace to a source section | PASS |
| No TBD quantities | PASS — all quantities are numeric |

### Detail.csv

| Check | Result |
|-------|--------|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS — all 15 rows use PARAMETRIC |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS — L-015 uses Qty=1, Unit=LS, UnitRate=0, Amount=0 |
| All amounts computed correctly (Qty x UnitRate = Amount) | PASS — verified for all 15 rows |
| Currency consistent | PASS — all rows CAD |

---

## Quantity Takeoff Coverage

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 (DEL-009-02) |
| Documents read | 5 of 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 15 |
| Items with numeric quantities | 15 (100%) |
| Items with TBD quantities | 0 (0%) |

### Items by Source Document

| SourceDoc | Count |
|-----------|-------|
| Procedure | 9 |
| Specification | 5 |
| Datasheet | 1 |

---

## Pricing Coverage

| Metric | Value |
|--------|-------|
| Total line items in Detail.csv | 15 |
| Items with numeric Amount | 15 (100%) |
| Items with TBD Amount | 0 (0%) |
| Items with Amount = 0 (intentional exclusion) | 1 (L-015 — permit fees, County responsibility) |
| Priced items (Amount > 0) | 14 |
| Pricing coverage | 100% |

---

## Provenance Completeness

| Metric | Value |
|--------|-------|
| Total Detail.csv rows | 15 |
| Rows with non-TBD SourceRef | 15 (100%) |
| Rows with "location TBD" SourceRef | 0 (0%) |
| Provenance completeness | **100%** |

All line items have traceable source references to pricing source files and/or deliverable documents.

---

## Basis-Consistency Checks

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (all 15 rows) |
| Method mix consistent with BASIS_OF_ESTIMATE | PASS — 100% PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE (not exercised — no method mixing occurred) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (exercised for 12 rows where LOE source was incomplete) |

---

## Scope Coverage

| Aspect | Status |
|--------|--------|
| DEL-009-02 included | YES |
| All 5 procedure phases covered | YES (Phase 1-5 mapped to ITEM-003 through ITEM-007) |
| Management oversight covered | YES (ITEM-001, ITEM-002 from LOE source) |
| Design discipline review covered | YES (ITEM-009 through ITEM-014; all 6 disciplines per REQ-009-02-03) |
| Document control covered | YES (ITEM-008) |
| Permit fees addressed | YES (ITEM-015, excluded at $0 per contract) |

### Exclusions (intentional)

| Exclusion | Reason |
|-----------|--------|
| Permit fees | County responsibility (R-01, §3.3.1; SOW-0202) — recorded at $0 |
| Development permit work | Separate deliverable (DEL-009-01) |
| Safety Code permits | Separate deliverable (DEL-009-03) |
| Code compliance register | Separate deliverable (DEL-009-04) |
| Design work (IFC drawings) | Covered by PKG-001 through PKG-006 deliverables; only permit-specific review effort included here |

---

## Warnings Summary

| ID | Severity | Description |
|----|----------|-------------|
| W-001 | MEDIUM | LOE source data covers only 2 of 10 roles for DEL-009-02; remaining 8 roles estimated parametrically from Procedure.md scope |
| W-002 | LOW | Permitting Specialist (R-22) hours (40 hrs) are parametric estimate; actual effort depends on authority responsiveness and inspection count |
| W-003 | LOW | Inspection coordination hours (10 hrs, Phase 5) based on ~7 anticipated inspection stages; actual stages TBD upon permit issuance |
| W-004 | INFO | LOE Notes column shows "PKG-009 Project Manager -- TBD" confirming source data is preliminary |

---

## What to Fix for a Cleaner Rerun

1. **Update Level_of_Effort.csv** to include Permitting Specialist (R-22), Document Controller (R-09), and design discipline review hours for DEL-009-02. Currently only PM and Cost Estimator are allocated.
2. **Confirm inspection stages** with Camrose County building authority upon permit issuance to refine Phase 5 effort estimate.
3. **Confirm permit processing timeline** with authority to validate schedule assumptions in Guidance.md.
4. **Confirm Permitting Specialist hours** once pre-application engagement (Phase 1) is complete and authority requirements are known.

---

## Write Quarantine Verification

| Check | Result |
|-------|--------|
| All files written under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |
| No deliverable content modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |
