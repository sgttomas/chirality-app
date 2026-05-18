# QA Report — EST_DEL-011-04_2026-02-27_0949

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all line items are priced, but material assumptions remain regarding door quantity (TBD in source documents), door specification, and fire-rating requirements. The estimate is fit for budgetary/parametric planning purposes but should be updated when IFC Architectural documents (DEL-001-07, DEL-001-11) are issued.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under `_Estimates/EST_DEL-011-04_2026-02-27_0949/` only | PASS |
| No modifications to deliverable working files, lifecycle files, decomposition, or dependency registers | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-011-04_2026-02-27_0949` exists | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE` = PARAMETRIC (valid enum value) | PASS |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT (optional; produced) |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 14 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (QUOTE/RATE_TABLE/HISTORICAL/ALLOWANCE/PARAMETRIC) | PASS — 13 PARAMETRIC, 1 ALLOWANCE |
| Allowance convention respected (L-014: Qty=1, Unit=LS, UnitRate=Amount) | PASS |
| All ItemID references match Items.csv | PASS |
| Row count | 14 lines |

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Lines with non-TBD SourceRef | 14 / 14 (100%) |
| Lines with `location TBD` SourceRef | 0 / 14 |
| Top missing-source offenders | None — all lines have source references |

**Provenance quality notes:**
- L-001 (door supply) traces to BE-04 in Building_Envelope_Rates.csv — strong provenance.
- L-002 (hardware) traces to BE-04 context + ASM-003 — moderate provenance (parametric derivation from general envelope rate context).
- L-013 (LOE) traces to Level_of_Effort.csv rows + Professional_Staff_Rates.csv — strong provenance.
- L-014 (fire-rated allowance) traces to ASM-005 + DEC-003 — weak provenance (allowance based on assumption).

---

## S7 — Basis-Consistency Checks

| Check | Result |
|---|---|
| Primary basis: PARAMETRIC | PASS |
| Method mix: 13 PARAMETRIC + 1 ALLOWANCE | PASS — ALLOW_MIXED_METHODS = TRUE |
| Fallback used: L-014 uses ALLOWANCE method | PASS — FALLBACK_POLICY = ALLOW_PARAMETRIC permits this |
| Deviation logged in Decision_Log.md | PASS — DEC-003 |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are bounded (door qty, fire rating) |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 14 items covering all Procedure steps and material scope |
| Basis-consistency checks pass | PASS | 1 ALLOWANCE fallback explicitly logged |
| Provenance completeness reported | PASS | 100% SourceRef coverage |
| Scope coverage explicit | PASS | 1 deliverable, 14 line items, in/out scope per Specification |
| No writes outside _Estimates/ | PASS | |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-011-04 | Datasheet.md, Specification.md, Guidance.md, Procedure.md | None | 14 |

**Coverage assessment:** All four production documents were read. Items cover: material supply (doors, hardware, accessibility, fire-rating), installation labour (frame, door, caulking), verification/testing activities, professional staff LOE, submittals, inspection, documentation, and temporary protection. No priceable activities from the documents were omitted.

---

## What to Fix for a Cleaner Rerun

1. **Resolve door quantity** — obtain IFC Door & Window Schedule (DEL-001-07) to replace ASM-001 (assumed 3 EA) with confirmed count.
2. **Confirm door specifications** — material, dimensions, hardware grade, thermal performance from DEL-001-07 / DEL-001-11 to refine unit rates.
3. **Resolve fire-rating requirement** — confirm from Architect whether any pedestrian doors require fire rating per compartmentation design.
4. **Obtain hardware pricing** — specific hardware schedule from DEL-001-07 would allow RATE_TABLE pricing instead of parametric estimate.
5. **Confirm accessibility scope** — number of accessible doors (currently assumed 1 per ASM-002).
