# QA Report — EST_DEL-012-03_2026-02-27_0630

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and fully priced (no TBD amounts), but material assumptions remain regarding office floor area, millwork applicability, and scope boundary with PKG-015. All confidence ratings are MEDIUM or LOW, consistent with pre-IFC parametric estimating.

---

## S1 — Write Quarantine Respected

**Status: PASS**

All files written to `_Estimates/EST_DEL-012-03_2026-02-27_0630/` only. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**Status: PASS**

Snapshot folder `EST_DEL-012-03_2026-02-27_0630` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**Status: PASS**

`BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value. Recorded in Run_Context.md.

## S4 — Required Artifacts Exist

**Status: PASS**

| Artifact | Present |
|---|---|
| Run_Context.md | Yes |
| Items.csv | Yes |
| Summary.md | Yes |
| QA_Report.md | Yes (this file) |
| Source_Index.md | Yes |
| Decision_Log.md | Yes |
| Assumptions_Log.md | Yes |
| WBS_CBS_Matrix.csv | Yes |
| Detail.csv | Yes (optional; produced) |
| Risk_Register.md | Yes (optional; produced) |

## S5 — CSV Schema Integrity

### Items.csv

**Status: PASS**

- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 23 rows, all with valid PricingMode (UNIT_RATE or LUMP_SUM)
- All rows have non-empty SourceDoc and SourceSection
- No TBD quantities — all Qty values are numeric
- Lump-sum convention: ITM-011, ITM-013, ITM-015, ITM-016, ITM-017, ITM-018 have Qty=1 and Unit=LS or EA

### Detail.csv

**Status: PASS**

- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 23 rows, all with valid Method (PARAMETRIC or ALLOWANCE)
- Allowance convention: DL-018 has Qty=1, Unit=LS, UnitRate=Amount ($11,000) — PASS
- All Amount values are numeric (no TBD)
- All Currency values are CAD

### WBS_CBS_Matrix.csv

**Status: PASS**

- Columns present: WBS_PackageID, WBS_DeliverableID, CBS, Currency, Amount_Total, LineCount, ProvenanceCompletenessPct, Notes
- 3 rows (Management, Construction, ALL rollup)
- Totals verified: Management ($2,340.00) + Construction ($34,907.40) = $37,247.40 (ALL)

## S6 — Provenance Discipline

**Status: PASS**

- 23 of 23 Detail.csv rows (100%) have a non-TBD SourceRef
- All SourceRefs point to identifiable price source files + row/item identifiers or to Decision_Log.md entries
- No `location TBD` entries

### Provenance Quality Notes

While 100% of lines have SourceRefs, several lines reference Decision_Log.md entries rather than direct price source evidence. These are parametric derivations where no single rate table row directly applies:

| LineID | SourceRef Type | Quality |
|---|---|---|
| DL-011 | Decision_Log DEC-003 | Parametric derivation — no direct rate table match for door supply+install |
| DL-012 | Decision_Log DEC-004 | Composite parametric — material + labour derivation |
| DL-013 | Decision_Log DEC-004 | Composite parametric — fixture + labour derivation |
| DL-014 | Decision_Log DEC-004 | Composite parametric — material + labour derivation |
| DL-015 | Decision_Log DEC-005 | Parametric allowance — labour + materials |
| DL-016 | Decision_Log DEC-006 | Parametric allowance |
| DL-017 | Decision_Log DEC-007 | Parametric allowance — component breakdown |

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Declared at top of this report. Justification:
- All 23 lines are priced (0% TBD amounts) — supports OK
- But: office floor area is assumed, not confirmed (material quantity driver)
- But: millwork applicability is uncertain ($11,000 / 29.5% of total)
- But: scope boundary with PKG-015 unresolved (3 lines / $1,890)
- But: all confidence ratings are MEDIUM or LOW
- Net assessment: WARNINGS — totals are directionally useful but contain bounded gaps requiring human review

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | PASS | WARNINGS with 4 specific bounded gaps documented |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 23 items covering professional staff, materials, finishes, MEP coordination, accessibility, safety, trade labour, inspection |
| Basis-consistency checks pass | PASS (with noted exception) | 22/23 lines PARAMETRIC; 1 line ALLOWANCE. ALLOW_MIXED_METHODS=TRUE permits this mix |
| Provenance completeness reported | PASS | 100% SourceRef coverage; 7 lines reference Decision_Log derivations |
| Scope coverage explicit | PASS | 1 deliverable in scope (DEL-012-03); exclusions noted (furniture, PKG-015 final wiring, structural shell) |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | 7 items (ITM-007 through ITM-011, ITM-014, ITM-018) | Spatial attributes, fit-out attributes, electrical attributes |
| Specification.md | 5 items (ITM-012, ITM-013, ITM-016, ITM-017, plus REQ-009 finishes) | Requirements REQ-003 through REQ-014 |
| Guidance.md | 0 items directly | Informed finish level assumptions (Principle 3) |
| Procedure.md | 11 items (ITM-001 through ITM-006, ITM-015, ITM-019 through ITM-023) | Phase 1-3 work steps, professional staff, trade labour |

All four documents were read and contributed to the quantity takeoff. No documents were missing.

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items in Detail.csv | 23 |
| Lines with numeric Amount | 23 (100%) |
| Lines with TBD Amount | 0 (0%) |
| Lines with PARAMETRIC method | 22 (95.7%) |
| Lines with ALLOWANCE method | 1 (4.3%) |
| Lines with HIGH confidence | 0 (0%) |
| Lines with MED confidence | 14 (60.9%) |
| Lines with LOW confidence | 9 (39.1%) |

---

## What to Fix for a Cleaner Rerun

1. **Confirm office floor area** from IFC architectural drawings (currently assumed 25 m2). This will update ITM-007 through ITM-010, ITM-019 through ITM-022 quantities and all dependent amounts.
2. **Resolve millwork applicability** — confirm with County/Architect whether the office includes casework. If not, remove ITM-018/DL-018 ($11,000).
3. **Resolve PKG-012 / PKG-015 scope boundary** (CONF-001) — confirm whether electrical device installation (receptacles, lighting, data outlets) is PKG-012 or PKG-015 scope. If PKG-015, remove ITM-012/DL-012, ITM-013/DL-013, ITM-014/DL-014 ($1,890).
4. **Obtain IFC finish schedule** to replace parametric finish rates with specification-specific rates for flooring, ceiling, and drywall finish level.
5. **Confirm door type and hardware** from IFC door/window schedule to replace parametric door allowance (DL-011).
6. **Add contingency / escalation** if required by project estimating policy.
