# QA Report — EST_DEL-018-01_2026-02-27_0600

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all 16 line items are priced. However, material TBDs and assumptions remain: the stripping area (the primary cost driver) is a parametric assumption pending survey and IFC drawing inputs, and 39.5% of the total value is based on allowances with LOW confidence. The estimate is usable for budgeting purposes but should be updated once SURVEY-001 and DEL-005-02 are available.

---

## S1 — Write Quarantine Respected

| Check | Result |
|-------|--------|
| All outputs written under `_Estimates/EST_DEL-018-01_2026-02-27_0600/` | PASS |
| No files modified outside `_Estimates/` | PASS |
| No deliverable content, lifecycle files, decomposition, or dependency registers modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|-------|--------|
| Snapshot folder `EST_DEL-018-01_2026-02-27_0600` exists | PASS |
| Folder is new (no prior DEL-018-01 snapshot) | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE value | PARAMETRIC |
| Value is valid enum (QUOTE / RATE_TABLE / HISTORICAL / PARAMETRIC / ALLOWANCE) | PASS |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|----------|--------|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional; produced) |
| Risk_Register.md | PRESENT (optional; produced) |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|-------|--------|
| Parseable as CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| Row count | 16 rows |
| All rows have DeliverableID = DEL-018-01 | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 10 UNIT_RATE, 6 LUMP_SUM |
| Every row traces to SourceDoc and SourceSection | PASS |
| Qty values: numeric or TBD | PASS — all numeric |

### Detail.csv

| Check | Result |
|-------|--------|
| Parseable as CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Row count | 16 rows |
| All ItemIDs trace back to Items.csv | PASS |
| Method values valid (QUOTE / RATE_TABLE / HISTORICAL / ALLOWANCE / PARAMETRIC) | PASS — 9 PARAMETRIC, 7 ALLOWANCE |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS — all 7 ALLOWANCE lines use Qty=1, Unit=LS, UnitRate=Amount |
| Currency consistent | PASS — all CAD |

---

## S6 — Provenance Discipline

### Provenance Completeness

| Metric | Value |
|--------|-------|
| Total priced lines | 16 |
| Lines with non-TBD SourceRef | 16 |
| Lines with `location TBD` SourceRef | 0 |
| **Provenance Completeness** | **100%** |

### Source Reference Quality

All 16 lines have SourceRef pointing to specific price source files (CSV name + item ID) or to Assumptions_Log.md entries. No `location TBD` references.

### Top Missing-Source Offenders

None. All lines have source references. However, 7 lines (L-002 through L-008) reference Assumptions_Log.md allowance entries rather than external rate evidence, which is lower-quality provenance.

---

## S7 — Status Reporting

| Field | Value |
|-------|-------|
| **RUN_STATUS** | **WARNINGS** |
| Critical input gaps | Stripping area TBD (ASM-002), topsoil depth TBD (ASM-003) |
| TBD amounts | 0 |
| ALLOWANCE items | 7 of 16 (43.75% of lines; 39.5% of value) |
| Confidence LOW items | 7 of 16 (all ALLOWANCE items) |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|-----------|--------|-------|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | PASS | WARNINGS; gaps are explicitly listed in Summary.md |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 16 items extracted from all 4 deliverable documents |
| Basis-consistency checks pass | PASS with note | Primary basis is PARAMETRIC; 7 items use ALLOWANCE fallback. This is permitted by ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_PARAMETRIC. Logged in Decision_Log.md. |
| Provenance completeness reported | PASS | 100% provenance; top gaps are qualitative (allowance refs vs. rate table refs) |
| Scope coverage explicit | PASS | 1 deliverable in scope, 4/4 documents read, 16 items extracted |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Document | Items Extracted | Key Content |
|----------|----------------|-------------|
| Datasheet.md | 1 | ITEM-001 (stripping area, volume, equipment type, exclusions) |
| Specification.md | 3 | ITEM-004 (utility locate), ITEM-006 (erosion control), ITEM-005 (staking from IFC compliance) |
| Guidance.md | 1 | ITEM-007 (stockpile protection — trade-off on management approach) |
| Procedure.md | 11 | ITEM-002 (mob/demob), ITEM-003 (pre-construction), ITEM-008 (final inspection), ITEM-009-016 (labour/staff) |
| Missing documents | 0 | All 4 documents present and read |

---

## Pricing Coverage

| Metric | Value |
|--------|-------|
| Items priced | 16 of 16 (100%) |
| Items with TBD amount | 0 |
| Items with PARAMETRIC method | 9 (56.25%) |
| Items with ALLOWANCE method | 7 (43.75%) |
| Value coverage: PARAMETRIC | $19,943.60 (60.5%) |
| Value coverage: ALLOWANCE | $13,000.00 (39.5%) |

---

## What to Fix for a Cleaner Rerun

1. **Resolve stripping area (ASM-002).** Obtain SURVEY-001 output and/or IFC drawings (DEL-005-02) to replace the 3,500 m2 parametric assumption with an actual measured area. This is the highest-impact improvement.

2. **Resolve topsoil depth (ASM-003).** Obtain SURVEY-001 topsoil depth assessment to confirm or revise the 200 mm assumed average depth. This affects production rate assumptions and may affect the EC-04 unit rate applicability.

3. **Replace allowances with rate evidence.** Obtain quotes or historical data for:
   - Equipment mobilization/demobilization (L-002, $3,500)
   - Erosion and sediment control (L-006, $2,500)
   - Survey staking (L-005, $1,800)
   - Pre-construction assessment (L-003, $1,500)
   - Stockpile stabilization (L-007, $1,500)
   - Utility locate (L-004, $1,200)
   - Final inspection coordination (L-008, $1,000)

4. **Validate production rate assumption (ASM-004).** The 150 m2/hr production rate for equipment operator stripping is a parametric assumption. Confirm against contractor production data for similar Alberta rural sites.

5. **Confirm labour support ratio (ASM-005).** The 0.67x labourer-to-operator ratio is an assumption. Validate against contractor crew composition standards.
