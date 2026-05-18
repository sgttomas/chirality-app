# QA Report — EST_DEL-007-02_2026-02-27_0600

**RUN_STATUS: OK**

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS — all 8 items reference Procedure or Specification sections |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 3 UNIT_RATE, 5 LUMP_SUM |
| No TBD quantities in priced items | PASS — all quantities are numeric |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (PARAMETRIC for all 8 lines) | PASS |
| Allowance/Parametric convention for LS items | PASS — LS items (L-004 through L-008) have Qty=1, Unit=LS, UnitRate=Amount (all 0.00 for embedded activities) |
| Currency consistent | PASS — all CAD |

---

## 2. Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-007-02) |
| Documents read | 5 of 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 8 |
| Items with numeric quantities | 8 of 8 (100%) |
| Items with TBD quantities | 0 |

Coverage assessment: All four production documents plus _CONTEXT.md were read. Items were extracted covering the full design production lifecycle (design, coordination, QA, IFC production) and all three professional roles identified in the LOE model.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total line items in Detail.csv | 8 |
| Lines with non-zero Amount | 3 (L-001, L-002, L-003) |
| Lines with Amount = 0.00 (embedded activities) | 5 (L-004 through L-008) |
| Lines with Amount = TBD | 0 |
| Pricing coverage | 100% (all items priced or explicitly embedded in parent LOE) |

Note: The 5 zero-amount lines represent activities (coordination, geotech review, QA, P.Eng. stamp, IFC production) whose effort is embedded within the 70-hour Landscape Architect LOE and 6-hour PM LOE. They are retained as separate items for traceability to the Specification and Procedure, not because they carry incremental cost.

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Total lines in Detail.csv | 8 |
| Lines with non-TBD SourceRef | 8 (100%) |
| Lines with SourceRef = "location TBD" | 0 |
| Provenance completeness | 100% |

All SourceRef values point to specific rows/sections in Professional_Staff_Rates.csv, Level_of_Effort.csv, or both.

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (8 of 8 lines) |
| Method consistency | PASS — 100% PARAMETRIC; consistent with declared basis |
| Mixed methods | Not applicable (no mixing occurred) |

---

## 6. Scope Coverage

| Check | Result |
|---|---|
| Scope requested | DEL-007-02 |
| Deliverables included | 1 (DEL-007-02 Landscape Site Plans) |
| Deliverables excluded | 0 |
| Package context | PKG-007 Landscape Architectural Design (4 deliverables total; only DEL-007-02 in scope for this run) |

---

## 7. Warnings

| ID | Severity | Description |
|---|---|---|
| W-001 | LOW | LOE model notes for DEL-007-02 state "PKG-007 Landscape Architect -- TBD" suggesting the hour allocation (70 hr LA, 6 hr PM, 4 hr CE) may be preliminary. Recommend validation against comparable projects. |
| W-002 | LOW | P.Eng. stamp fee not separately quantified; assumed covered by project-wide professional services. If separate engagement required, incremental cost is unaccounted. |
| W-003 | INFO | No contingency applied to estimate. PARAMETRIC basis carries MEDIUM confidence per source data. |
| W-004 | INFO | Professional_Design_Fees.csv was indexed but not used; LOE model was preferred for deliverable-level granularity. |

---

## 8. What to Fix for a Cleaner Rerun

1. **Validate LOE hours**: Confirm or refine the 70-hour Landscape Architect allocation in Level_of_Effort.csv with discipline-specific input. The current "TBD" note suggests the figure is a placeholder.
2. **P.Eng. stamp cost**: If the P.Eng. review and stamp carries a separately billable cost, add it to the price sources.
3. **Plotting/reproduction costs**: If material/reproduction costs should be included, add a price source for drawing production materials.
4. **Contingency**: If a contingency factor is desired, specify in the run brief or add a contingency table to price sources.

---

## SPEC Compliance Summary

| SPEC | Requirement | Status |
|---|---|---|
| S1 | Write quarantine respected | PASS — all writes under _Estimates/ |
| S2 | Snapshot created | PASS — EST_DEL-007-02_2026-02-27_0600/ |
| S3 | BASIS_OF_ESTIMATE validated | PASS — PARAMETRIC is a valid enum value |
| S4 | Required artifacts exist | PASS — Run_Context.md, Items.csv, Summary.md, QA_Report.md, Source_Index.md all produced |
| S5 | CSV schema integrity | PASS — Items.csv and Detail.csv both parseable with all required columns and valid enum values |
| S6 | Provenance discipline | PASS — 100% provenance completeness; no "location TBD" entries |
| S7 | Status reporting | PASS — RUN_STATUS = OK declared |
| S8 | Operator acceptance checklist | PASS — all checklist criteria met with bounded gaps (see Warnings) |
