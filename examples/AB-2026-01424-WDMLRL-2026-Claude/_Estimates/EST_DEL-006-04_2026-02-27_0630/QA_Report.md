# QA Report — EST_DEL-006-04_2026-02-27_0630

## RUN_STATUS: OK

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have non-empty ItemID | PASS |
| All rows trace to a SourceDoc (Datasheet, Specification, Guidance, or Procedure) | PASS |
| All rows trace to a SourceSection | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Lump-sum rows use Qty=1 and Unit=LS | PASS |
| Row count | 19 items |

### Detail.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All rows have valid Method values (PARAMETRIC) | PASS |
| All amounts are numeric (no TBD values) | PASS |
| Currency is consistently CAD | PASS |
| Row count | 4 priced lines |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-006-04) |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 19 |
| Items from Datasheet | 4 (ITEM-005, ITEM-006, ITEM-008, ITEM-009) |
| Items from Specification | 9 (ITEM-007, ITEM-010 through ITEM-015, ITEM-019) |
| Items from Procedure | 6 (ITEM-001 through ITEM-004, ITEM-016 through ITEM-018) |
| Items from Guidance | 0 (Guidance informed design context but did not introduce distinct priceable items beyond those captured in Specification and Procedure) |

**Note:** Items ITEM-005 through ITEM-019 are design sub-activities (drawing sheets, coordination tasks, QA activities) that are encompassed by the professional staff-hour allocations in ITEM-001 through ITEM-004. They are listed in Items.csv for completeness of the quantity takeoff but are not separately priced in Detail.csv to avoid double-counting. The 4 priced lines in Detail.csv represent the total professional effort allocation.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 19 |
| Items with direct pricing in Detail.csv | 4 (ITEM-001 through ITEM-004 — staff-hour lines) |
| Items priced indirectly (sub-activities of priced items) | 15 (ITEM-005 through ITEM-019 — covered by staff-hour LOE) |
| Items with TBD amounts | 0 |
| Pricing coverage | 100% (all items accounted for; no TBD amounts) |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with SourceRef | 4 / 4 (100%) |
| Detail.csv rows with "location TBD" SourceRef | 0 |
| Provenance completeness | 100% |

**All priced lines reference both Level_of_Effort.csv (for hours) and Professional_Staff_Rates.csv (for rates).**

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4 of 4 lines) |
| Method consistency | 100% PARAMETRIC — fully consistent with BASIS_OF_ESTIMATE |
| Fallback used | No |
| Mixed methods | No |

---

## 6. Scope Coverage

| Check | Result |
|---|---|
| Deliverables included | DEL-006-04 (1 of 1 in scope) |
| Deliverables excluded | 0 |
| Package context | PKG-006 Plumbing Design |
| Scope boundary | Design professional fees only; excludes material/equipment procurement and construction installation |

---

## 7. SPEC Compliance Matrix

| SPEC | Requirement | Status |
|---|---|---|
| S1 | Write quarantine respected | PASS — all files written under _Estimates/EST_DEL-006-04_2026-02-27_0630/ |
| S2 | Snapshot created | PASS — snapshot folder exists |
| S3 | BASIS_OF_ESTIMATE validated | PASS — PARAMETRIC is a valid enum value |
| S4 | Required artifacts exist | PASS — Run_Context.md, Items.csv, Summary.md, QA_Report.md, Source_Index.md all present |
| S5 | CSV schema integrity | PASS — Items.csv and Detail.csv have all required columns; PricingMode and Method values are valid |
| S6 | Provenance discipline | PASS — 100% of Detail.csv rows have non-TBD SourceRef |
| S7 | Status reporting | PASS — RUN_STATUS = OK declared |
| S8 | Operator acceptance checklist | See below |

---

## 8. Operator Acceptance Checklist (S8)

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | RUN_STATUS = OK |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 19 items extracted from all 4 documents; covers all anticipated artifacts and design activities |
| Basis-consistency checks pass | PASS | 100% PARAMETRIC |
| Provenance completeness reported | PASS | 100% |
| Scope coverage explicit | PASS | 1 deliverable, design fees only, exclusions documented |
| No writes outside _Estimates/ | PASS | All output under _Estimates/EST_DEL-006-04_2026-02-27_0630/ |

---

## 9. What to Fix for a Cleaner Rerun

1. **Refine LOE allocation.** The Level_of_Effort.csv notes for DEL-006-04 are marked "TBD" — a bottom-up task-level LOE estimate based on actual drawing sheet count and design complexity would increase confidence from MEDIUM to HIGH.

2. **Resolve TBD design parameters.** Multiple Datasheet attributes are TBD (cistern material/type, installation type, pump selection, pressure tank decision, bulk fill pump specs, water quality classification). Resolving these would confirm whether the parametric LOE allocation is adequate or needs adjustment.

3. **Resolve CONF-001 and CONF-002.** Two open design conflicts (cistern location physical fit; fire hose pump identity) may generate additional design hours not captured in current LOE.

4. **Add travel/site visit costs.** If site visits to the rural landfill site are required during design, those costs should be added to price sources.

5. **Add printing/reproduction costs.** IFC drawing plotting and distribution costs are not included.
