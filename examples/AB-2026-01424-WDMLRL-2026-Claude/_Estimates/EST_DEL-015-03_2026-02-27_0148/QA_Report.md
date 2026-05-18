# QA Report — EST_DEL-015-03_2026-02-27_0148

## RUN_STATUS: WARNINGS

**Rationale:** All 28 line items are priced with non-TBD amounts and all have provenance references. However, material TBDs remain in the engineering documents (exact quantities, NEMA configurations, device grades) and several pricing lines rely on parametric estimation without direct supplier evidence. The estimate is meaningful but has bounded gaps that should be resolved at IFC stage.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under _Estimates/ only | PASS |
| No deliverable files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition files modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: EST_DEL-015-03_2026-02-27_0148 | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS (valid enum) |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT (optional; produced) |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document | PASS — all rows reference Datasheet, Specification, or Procedure |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 28 rows |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS — all rows = PARAMETRIC |
| Allowance/parametric convention (Qty=1, Unit=LS for LS items) | PASS — L-016, L-027, L-028 use Qty=1, Unit=LS |
| Row count | 28 rows |
| All ItemIDs in Detail.csv match Items.csv | PASS |

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 28 / 28 (100%) |
| Rows referencing price source files directly | 12 / 28 (43%) — L-005 (ES-04), L-017 through L-020 (T-04), L-021 through L-026 (LoE + staff rates) |
| Rows with parametric-only provenance | 16 / 28 (57%) — material items without direct rate source |

### Top Missing-Source Items (parametric-only, no direct rate table evidence)

| LineID | Description | Amount (CAD) | Gap |
|---|---|---|---|
| L-012 | Circuit breakers (45 EA) | $2,025 | No breaker rate table in price sources |
| L-007/L-008 | Rough-in packages — 15A/20A circuits | $2,520 | No itemized conduit/wire/box rates |
| L-001/L-002 | 15A and 20A receptacle devices | $930 | No explicit device rate table for standard receptacles |
| L-027 | Electrical Safety Code Permit | $1,500 | No permit fee schedule in price sources |

---

## S7 — Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | 100% PARAMETRIC |
| ALLOW_MIXED_METHODS = TRUE | N/A — no mixed methods used |
| FALLBACK_POLICY = ALLOW_PARAMETRIC | N/A — primary basis is already PARAMETRIC |
| Consistency | PASS — all methods match basis |

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS) | Gaps are bounded: quantity TBDs, parametric device/material rates |
| Items.csv reviewed for completeness | REVIEW RECOMMENDED | 28 items cover all 5 receptacle types, rough-in, labour, professional staff, permits, coordination |
| Basis-consistency checks pass | PASS | All methods = PARAMETRIC |
| Provenance completeness reported | PASS | 100% SourceRef populated; 43% with direct rate source, 57% parametric |
| Scope coverage explicit | PASS | 1 deliverable, 4/4 documents read, 28/28 items priced |
| No writes outside _Estimates/ | PASS | Verified |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Present | Items Extracted | Notes |
|---|---|---|---|
| DEL-015-03 | 4/4 (Datasheet, Specification, Guidance, Procedure) | 28 | All document types present and read |

### Coverage Notes

- Receptacle quantities are derived from the conceptual electrical drawing (App B-Elec) as referenced in the Datasheet. Exact counts are TBD pending IFC drawings (DEL-004-05).
- The following receptacle types and approximate quantities were extracted: 15A/120V (12 EA), 20A/120V (18 EA), 20A/240V (6 EA), 30A/240V (3 EA), 50A/240V (6 EA) = 45 total receptacle points.
- Professional staff effort is sourced directly from Level_of_Effort.csv (6 role-rows for DEL-015-03).
- Electrician trade labour hours (144 hrs total) are parametrically estimated based on per-point productivity rates.

---

## What to Fix for a Cleaner Rerun

1. **Obtain IFC drawings (DEL-004-05, DEL-004-06)** to confirm exact receptacle quantities by type and zone. Current counts are approximate.
2. **Add receptacle device rate table** covering 15A, 20A/120V, 20A/240V, and 30A/240V devices to PRICE_SOURCES for direct provenance.
3. **Add conduit/wire/box material rate table** for rough-in cost buildup with direct evidence.
4. **Add circuit breaker rate table** (by amperage) to PRICE_SOURCES.
5. **Confirm NEMA configurations** for 240V receptacles (D-009 scope change trigger).
6. **Add Alberta Safety Codes permit fee schedule** or obtain actual permit fee quote.
7. **Include electrician trade hours in Level_of_Effort.csv** for DEL-015-03 (currently only professional staff hours are provided).
