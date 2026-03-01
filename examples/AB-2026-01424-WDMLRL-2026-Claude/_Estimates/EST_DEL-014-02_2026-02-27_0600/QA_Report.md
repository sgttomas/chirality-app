# QA Report — EST_DEL-014-02_2026-02-27_0600

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all 20 items are priced. However, material TBDs (tank material, existing tank characteristics, sanitary line length, bedding requirements) and 1 provisional allowance (high-level alarm) result in bounded uncertainty. The estimate is suitable for budgetary planning but requires rerun once DEL-006-05 design and geotechnical investigation are complete.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under `_Estimates/EST_DEL-014-02_2026-02-27_0600/` | PASS |
| No deliverable files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-014-02_2026-02-27_0600` exists | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| `BASIS_OF_ESTIMATE = PARAMETRIC` | PASS (valid enum value) |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| `Run_Context.md` | PRESENT |
| `Items.csv` | PRESENT |
| `Summary.md` | PRESENT |
| `QA_Report.md` | PRESENT (this file) |
| `Source_Index.md` | PRESENT |
| `Detail.csv` | PRESENT (optional; produced) |
| `WBS_CBS_Matrix.csv` | PRESENT |
| `Decision_Log.md` | PRESENT |
| `Assumptions_Log.md` | PRESENT |
| `Risk_Register.md` | PRESENT |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS — all 9 columns present |
| All rows have valid PricingMode (UNIT_RATE or LUMP_SUM) | PASS — 12 UNIT_RATE, 8 LUMP_SUM |
| All rows trace to a source document | PASS — Datasheet (2), Specification (2), Procedure (12), Guidance (1), Procedure (3 additional) |
| All rows have SourceSection | PASS |
| Row count | 20 items |
| TBD quantities | 0 (all quantities resolved or parametrically assumed) |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS — all 15 columns present |
| All Method values valid | PASS — 19 PARAMETRIC, 1 ALLOWANCE |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS — L-010 (ALLOWANCE): Qty=1, Unit=LS, UnitRate=2500, Amount=2500 |
| All lump-sum items: Qty=1, Unit=LS | PASS |
| Row count | 20 lines |
| TBD amounts | 0 |

---

## S6 — Provenance Discipline

### Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows in Detail.csv | 20 |
| Rows with non-TBD SourceRef | 20 |
| **Provenance completeness** | **100%** |

### Confidence Distribution

| Confidence | Count | % |
|---|---|---|
| LOW | 4 | 20% |
| MED | 16 | 80% |
| HIGH | 0 | 0% |

### Top Missing-Source Offenders

No rows have TBD SourceRef. However, the following rows rely on parametric estimates without direct quote evidence:

| LineID | Description | Issue |
|---|---|---|
| L-001 | Septic holding tank supply + set | UU-04 is an ALLOWANCE-grade parametric range; no supplier quote |
| L-003 | Existing tank pump-out/disposal | Fully parametric; no subcontractor quote |
| L-004 | Existing tank excavation/extraction | Fully parametric; no subcontractor quote |
| L-010 | High-level alarm (provisional) | Provisional allowance; requirement TBD |

---

## S7 — Status Reporting

| Field | Value |
|---|---|
| **RUN_STATUS** | **WARNINGS** |
| Totals meaningful? | Yes — $66,416.80 CAD total |
| Critical input gaps? | No critical gaps; bounded TBDs identified |
| Material TBDs remaining? | 5 (tank material, existing tank characteristics, sanitary line length, bedding spec, alarm requirement) |
| Assumptions count | 8 (see Assumptions_Log.md) |

---

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | PASS | WARNINGS — 5 bounded TBDs, 1 provisional allowance |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS | 20 items covering all priceable scope from 4 documents |
| Basis-consistency checks pass | PASS | 19/20 lines = PARAMETRIC (matches BASIS_OF_ESTIMATE); 1 ALLOWANCE line per ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_PARAMETRIC |
| Provenance completeness reported | PASS | 100% SourceRef coverage; top gaps listed |
| Scope coverage explicit | PASS | 1 deliverable (DEL-014-02); 0 excluded; all 4 documents read |
| No writes outside _Estimates/ | PASS | Write quarantine respected |

---

## What to Fix for a Cleaner Rerun

1. **Obtain tank material specification** from DEL-006-05 (Plumbing Engineer of Record) and replace UU-04 parametric with a supplier quote.
2. **Complete pre-construction site survey** to characterize existing septic tank (size, material, location, condition, contents) — enables more accurate removal cost.
3. **Confirm sanitary line run length** from IFC plumbing drawings (DEL-006-05).
4. **Complete geotechnical investigation** to specify bedding, compaction, and frost protection requirements.
5. **Confirm high-level alarm code requirement** with Alberta Safety Codes — remove or refine the $2,500 provisional allowance.
6. **Obtain equipment rental rates** and subcontractor quotes for excavation/demolition work.
