# QA Report — EST_DEL-018-05_2026-02-27_0855

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all 26 line items are priced (no TBD amounts). However, multiple physical parameters remain TBD in the source documents (sump dimensions, capacity, pipe material/diameter, invert elevations, frost depth), and two line items use ALLOWANCE method rather than PARAMETRIC. The estimate relies on parametric proxies for items without direct rate table entries. The estimate is usable for budgeting purposes with the understanding that design development will refine quantities and rates.

---

## S1 — Write Quarantine Respected

**PASS.** All files written under `_Estimates/EST_DEL-018-05_2026-02-27_0855/`. No project truth files modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-018-05_2026-02-27_0855` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:
- Run_Context.md
- Items.csv (21 items)
- Detail.csv (26 priced lines)
- Summary.md
- QA_Report.md
- Source_Index.md
- WBS_CBS_Matrix.csv
- Decision_Log.md
- Assumptions_Log.md

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes — all present.
- 21 rows; all rows trace to a source document (Datasheet, Specification, Procedure, or Guidance) and section.
- PricingMode values: UNIT_RATE (12 items), LUMP_SUM (9 items) — all valid.
- No TBD quantities (all quantities resolved to numeric values via assumptions).

### Detail.csv
**PASS.**
- Columns: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes — all present.
- 26 rows; all amounts numeric (no TBD).
- Method values: PARAMETRIC (24 lines), ALLOWANCE (2 lines) — all valid.
- Allowance convention check: DL-019 and DL-020 have Qty=1, Unit=LS, UnitRate=Amount — **PASS**.

## S6 — Provenance Discipline

**PASS (with notes).**
- Provenance completeness: **26/26 lines (100%)** have non-TBD SourceRef entries.
- All SourceRef entries point to a price source file + item ID, or to an explicit ASSUMPTION with rationale.
- 8 lines reference explicit ASSUMPTIONs (no direct rate table match); these are flagged in Source_Index.md under Source Gaps.

### Top Source Gap Items (no direct rate table entry)

| LineID | Description | Method | Confidence | Issue |
|--------|-------------|--------|-----------|-------|
| DL-003 | Precast concrete mud sump | PARAMETRIC | LOW | Proxy from UU-04 septic tank rate; largest cost item ($18,500) |
| DL-007 | Floor drain supply + install | PARAMETRIC | LOW | No rate table entry; parametric estimate |
| DL-008 | Sump inlet penetration | PARAMETRIC | LOW | No rate table entry; parametric estimate |
| DL-011 | Water flow test | PARAMETRIC | LOW | No rate table entry; parametric estimate |
| DL-019 | Cold-weather allowance | ALLOWANCE | LOW | No rate table entry; allowance |
| DL-020 | Environmental regulatory scoping | ALLOWANCE | LOW | No rate table entry; allowance |

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Warnings:
1. Six physical parameters remain TBD (sump dimensions, capacity, construction material, floor drain count, pipe material/diameter, invert elevations) — these affect the accuracy of parametric estimates for ITM-001, ITM-003, ITM-004, ITM-005, ITM-006, ITM-007.
2. Four additional parameters TBD from semantic lensing (drainage pipe minimum slope, site frost depth, excavator access clearance envelope, as-built survey scope).
3. Two lines use ALLOWANCE method (DL-019 cold-weather, DL-020 regulatory) — consistent with FALLBACK_POLICY=ALLOW_PARAMETRIC and ALLOW_MIXED_METHODS=TRUE.
4. Precast sump price ($18,500) is the largest single item at 40.5% of total and carries LOW confidence due to parametric proxy.
5. Unresolved Conflict Table items: CF-001 (scope boundary), CF-002 (environmental permit), CF-003 (permit conditionality) — all flagged TBD in Guidance.md.

## S8 — Operator Acceptance Checklist

| Check | Status |
|-------|--------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS — gaps are bounded and enumerated above |
| Items.csv reviewed for completeness | 21 items extracted from 4 documents; covers all major scope elements |
| Basis-consistency checks | 24/26 PARAMETRIC, 2/26 ALLOWANCE; consistent with ALLOW_MIXED_METHODS=TRUE |
| Provenance completeness reported | 100% SourceRef populated; source gaps documented |
| Scope coverage explicit | 1 deliverable in scope (DEL-018-05); exclusions documented in Items.csv and Summary.md |
| No writes outside _Estimates/ | PASS |

---

## What to Fix for a Cleaner Rerun

1. **Resolve sump dimensions** — obtain civil design (DEL-005-02, DEL-005-03) to replace assumed sump volume and obtain actual precast sump pricing.
2. **Confirm pipe material/diameter** — IFC drawings (DEL-005, DEL-006) needed to select correct unit rate for drainage pipe.
3. **Obtain precast sump quotation** — replace parametric proxy (UU-04) with a vendor quote for the actual sump configuration.
4. **Resolve floor drain count** — confirm 1 vs. multiple floor drains from plumbing IFC drawings.
5. **Confirm frost depth** — geotechnical report (SOW-0001) needed to validate assumed excavation/burial depths.
6. **Resolve CF-001** — scope boundary confirmation between GC and Plumbing Contractor will clarify labour allocation.
7. **Resolve CF-002/CF-003** — environmental regulatory scoping outcome will determine whether $2,500 allowance is adequate.
