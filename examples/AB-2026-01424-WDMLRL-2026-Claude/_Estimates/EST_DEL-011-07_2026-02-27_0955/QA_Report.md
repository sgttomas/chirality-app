# QA Report — EST_DEL-011-07_2026-02-27_0955

## RUN_STATUS: WARNINGS

---

## S1 — Write Quarantine Respected

**PASS.** All output files are written exclusively under `_Estimates/EST_DEL-011-07_2026-02-27_0955/`. No project truth files were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-011-07_2026-02-27_0955` exists under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts are present:
- [x] Run_Context.md
- [x] Items.csv (20 items)
- [x] Detail.csv (20 priced lines)
- [x] Summary.md
- [x] QA_Report.md (this file)
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- 20 rows; all rows have DeliverableID = DEL-011-07
- PricingMode values: UNIT_RATE (17 rows), LUMP_SUM (3 rows) — all valid
- All rows trace to a SourceDoc (Datasheet, Specification, or Procedure) and SourceSection
- No TBD quantities (all quantities are numeric, though several are parametric assumptions)

### Detail.csv
**PASS.**
- Columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- 20 rows; all have WBS_PackageID = PKG-011, WBS_DeliverableID = DEL-011-07
- Method values: PARAMETRIC (10), RATE_TABLE (8), ALLOWANCE (1) — valid per ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_PARAMETRIC
- Lump-sum items (DL-003, DL-005, DL-009, DL-010): Qty=1, Unit=LS, UnitRate=Amount — convention respected
- No TBD amounts; all 20 lines have numeric amounts

## S6 — Provenance Discipline

**PASS (with notes).**
- 20/20 lines (100%) have non-TBD SourceRef values
- 8 lines reference specific price source files and line IDs (RATE_TABLE method)
- 10 lines reference parametric derivations with cross-references to Assumptions_Log
- 1 line references Assumptions_Log for ALLOWANCE method
- No `location TBD` entries

**Top provenance notes:**
- DL-001 (steel framing $280/m2): Parametric rate not directly from a price source file; derived from industry parametric model for industrial mezzanine steel framing. Documented in Assumptions_Log A-002.
- DL-005 (connection hardware $4,500): ALLOWANCE with LOW confidence. No direct rate table match.
- DL-003 (stair system $9,000): Used SC-07 (concrete stairs $9,000 each) as parametric proxy for steel stair — documented in Assumptions_Log A-010.

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Rationale: Totals are meaningful and all 20 line items are priced (no TBD amounts). However, material assumptions remain that could significantly affect the total:
- Mezzanine floor area is a critical TBD (assumed 93 m2); a change in area would scale ~67% of the total
- Structural system is assumed (steel framing) and not confirmed
- One ALLOWANCE line item (DL-005, $4,500, LOW confidence)
- Mixed methods used: PARAMETRIC (10), RATE_TABLE (8), ALLOWANCE (1)

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS | Gaps are identified and bounded in Summary.md |
| Items.csv reviewed for completeness | PASS | 20 items covering structure, deck, stairs, guardrails, labour, materials, professional services, inspections, documentation |
| Basis-consistency checks | PASS (with mixed methods) | Primary basis PARAMETRIC; RATE_TABLE used for labour rates and material rates where available; 1 ALLOWANCE. Mixed methods allowed per ALLOW_MIXED_METHODS=TRUE. |
| Provenance completeness reported | PASS | 100% of lines have SourceRef; top gaps documented above |
| Scope coverage explicit | PASS | Single deliverable DEL-011-07; SOW-0032, SOW-0033, SOW-0034 covered; exclusions documented in Summary.md |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Source Document | Items Extracted | Notes |
|---|---|---|
| Datasheet.md | 5 items (ITM-001 through ITM-005) | Structural attributes, materials, physical components |
| Specification.md | 3 items (ITM-004, ITM-009, ITM-010) | Guardrails (R-07), inspection/certification (R-02), as-built docs (R-10) |
| Procedure.md | 12 items (ITM-006 through ITM-008, ITM-011 through ITM-020) | Labour, management hours, material procurement, concrete |

Note: Some items are informed by multiple documents (e.g., guardrails appear in both Datasheet attributes and Specification R-07).

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 20 |
| Items priced in Detail.csv | 20 |
| Items with TBD amount | 0 |
| Pricing coverage | 100% |

## Method Distribution

| Method | Line Count | Amount (CAD) | % of Total |
|---|---|---|---|
| PARAMETRIC | 10 | $81,020.00 | 58.1% |
| RATE_TABLE | 8 | $44,934.50 | 32.2% |
| ALLOWANCE | 1 | $4,500.00 | 3.2% |
| **Subtotal (professional services — RATE_TABLE from LOE)** | **6** | **$5,590.00** | **4.0%** |

Note: The 6 professional services RATE_TABLE lines (DL-011 to DL-016) are priced with rates from Professional_Staff_Rates.csv and hours from Level_of_Effort.csv, both classified as PARAMETRIC basis in those sources.

## What to Fix for a Cleaner Rerun

1. **Resolve mezzanine floor area.** Once IFC drawings (DEL-002-05) are available, replace the 93 m2 assumption with the actual area. This is the single highest-impact input.
2. **Confirm structural system.** Replace the steel-framing assumption with the Structural Engineer's confirmed system. If concrete, re-derive unit rates.
3. **Resolve CFT-011-07-01 (wash bay span extent).** This directly affects area and may affect framing complexity/rates.
4. **Resolve CFT-011-07-02 (scope boundary with PKG-012).** Confirm whether any wearing surface is included in DEL-011-07 or excluded.
5. **Replace connection hardware allowance (DL-005).** Obtain actual connection details from IFC drawings to convert from ALLOWANCE to RATE_TABLE or PARAMETRIC.
6. **Validate stair system cost.** SC-07 (concrete stairs) was used as a proxy for steel stairs; a steel stair-specific rate would improve accuracy.
7. **Add lifting equipment/crane rental if not included in parametric framing rate.** The current estimate assumes erection equipment is embedded in the $/m2 framing rate.
