# QA Report — EST_DEL-017-04_2026-02-27_0730

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all line items are priced (no TBD amounts), but material TBDs remain in the underlying engineering documents (room footprint, workforce headcount, laundry scope, shower requirement, finish specifications, door fire rating). These TBDs are bounded by documented assumptions but represent real variance risk. The estimate is suitable for early-stage budgeting with the caveats documented below.

---

## Schema Validity

### Items.csv

| Check | Result | Notes |
|-------|--------|-------|
| File exists and is parseable | PASS | 33 data rows |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS | All 9 columns present |
| All ItemIDs unique | PASS | ITM-001 through ITM-033 |
| All DeliverableID values = DEL-017-04 | PASS | Single deliverable in scope |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS | 17 UNIT_RATE, 16 LUMP_SUM |
| Every row has SourceDoc reference | PASS | Datasheet: 7, Specification: 8, Procedure: 12, Guidance: 1 (excludes multi-source ITM-030-032 which cite Procedure) |
| Every row has SourceSection reference | PASS | |
| Qty values: no TBD entries | PASS | All quantities are numeric |

### Detail.csv

| Check | Result | Notes |
|-------|--------|-------|
| File exists and is parseable | PASS | 33 data rows |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS | All 15 columns present |
| All LineIDs unique | PASS | DL-001 through DL-033 |
| Every LineID traces to an ItemID in Items.csv | PASS | 1:1 mapping ITM-001 to ITM-033 |
| Method values valid (QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC) | PASS | PARAMETRIC: 29, RATE_TABLE: 4 |
| Amount = Qty * UnitRate for all UNIT_RATE rows | PASS | Verified |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS | All LUMP_SUM items have Qty=1, Unit=LS |
| Currency = CAD for all rows | PASS | |
| Confidence values valid (LOW, MED, HIGH) | PASS | MED: 19, LOW: 14 |

---

## Quantity Takeoff Coverage

### Items Extracted per Document

| Source Document | Items Extracted | Notes |
|-----------------|----------------|-------|
| Datasheet | 7 items | Partitions, door, plumbing rough-in, locker system, bench seating, laundry rough-in, finishes |
| Specification | 8 items | Plumbing fixtures, electrical rough-in (3 items), exhaust ventilation, inspections, laundry equipment (2 items) |
| Procedure | 12 items | Design phases, permitting, site prep, demolition, mechanical, insulation, flooring, ceiling, paint, commissioning, punch-list, as-builts |
| Guidance | 1 item | Dedicated laundry circuits (from Considerations section) |
| Level_of_Effort.csv | 3 items | PM, construction management, QA/QC + HSE (derived from LoE hours) |
| **Total** | **33 items** | |

### Deliverable Document Status

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read successfully |
| Datasheet.md | Read successfully |
| Specification.md | Read successfully |
| Guidance.md | Read successfully |
| Procedure.md | Read successfully |

No missing documents. All four production documents were present and read.

---

## Pricing Coverage

| Metric | Value |
|--------|-------|
| Total line items | 33 |
| Items with numeric Amount (priced) | 33 (100%) |
| Items with Amount = TBD | 0 (0%) |
| Items priced from RATE_TABLE | 4 (12%) |
| Items priced PARAMETRIC | 29 (88%) |

**Assessment:** 100% of items are priced. However, 88% are priced parametrically (many relying on assumptions rather than rate table lookups), reflecting the limited coverage of pricing sources for equipment, fixtures, and specialty items.

---

## Provenance Completeness

| Metric | Value |
|--------|-------|
| Total Detail.csv rows | 33 |
| Rows with substantive SourceRef | 33 (100%) |
| Rows with "location TBD" SourceRef | 0 (0%) |

**Assessment:** All rows have a SourceRef pointing to either a pricing source file (rate table CSV + row reference) or an explicit assumption ID in Assumptions_Log.md. Provenance is complete.

### Top Assumption-Dependent Lines (by Amount)

| LineID | Amount | Description | Key Assumption |
|--------|--------|-------------|----------------|
| DL-022 | $3,600 | Locker system (8 EA) | ASM-004: 8 lockers at $450/EA; count and price assumed |
| DL-024 | $3,500 | Commercial washer | ASM-012: commercial washer $3,500; spec TBD |
| DL-003 | $3,500 | Final design and IFC drawings | ASM-007: parametric design fee for small renovation |
| DL-025 | $3,000 | Commercial dryer | ASM-013: commercial dryer $3,000; spec TBD |
| DL-009 | $1,200 | Door supply and install | ASM-009: interior door $1,200; fire rating TBD |

---

## Basis-Consistency Checks

| Check | Result | Notes |
|-------|--------|-------|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS | Declared basis |
| ALLOW_MIXED_METHODS = TRUE | PASS | Mixed methods permitted |
| RATE_TABLE lines present (4 of 33) | PASS | IA-01 partitions, IA-02 paint, IA-03 ceiling, IA-04 flooring from Interior_Architectural_Rates.csv; consistent with ALLOW_MIXED_METHODS=TRUE |
| No QUOTE, HISTORICAL, or ALLOWANCE methods used | PASS | Only PARAMETRIC and RATE_TABLE |
| FALLBACK_POLICY = ALLOW_PARAMETRIC respected | PASS | All items without rate table evidence are priced PARAMETRIC (not left TBD) |

---

## Scope Coverage

| Status | Count | Notes |
|--------|-------|-------|
| SOW items IN scope | 1 | SOW-0073 (Construct new locker/change room with laundry services) |
| SOW items OUT of scope | N/A | SOW-0070, SOW-0071, SOW-0072, SOW-0074 are other PKG-017 deliverables (excluded) |
| Deliverables estimated | 1 | DEL-017-04 |
| Deliverables excluded | 0 | Scope = DEL-017-04 only |

---

## What to Fix for a Cleaner Rerun

1. **Obtain workforce headcount from County** — resolves locker count, room sizing, and bench/fixture requirements. This is the highest-value information gap.
2. **Clarify laundry scope [C-001]** — confirm whether supply and installation of washer/dryer is included or only rough-in. $6,500 variance.
3. **Confirm shower requirement** — if showers are required, significant additional cost for tiling, plumbing, and ventilation.
4. **Provide detailed design fee schedule** — replace parametric design cost assumptions (DL-001 through DL-003, $5,530 combined) with actual design team quotes.
5. **Provide equipment/fixture quotes** — locker system, laundry equipment, plumbing fixtures, lighting fixtures, and door/hardware ($14,950 combined) are all parametrically estimated. Supplier quotes would move 14 line items from LOW to HIGH confidence.
6. **Confirm occupancy classification [A-001]** — affects ventilation rates, fire separation, plumbing fixture counts, and accessibility requirements.
7. **Confirm door fire rating [F-001]** — could increase door cost from $1,200 to $2,500+.
8. **Update Level_of_Effort.csv** — the DEL-017-04 entries carry "PKG-017 TBD -- TBD" notes, indicating placeholder status.

---

## SPEC Compliance Checklist

| SPEC | Requirement | Status |
|------|-------------|--------|
| S1 | Write quarantine respected — no files outside _Estimates/ modified | PASS |
| S2 | Snapshot created — EST_DEL-017-04_2026-02-27_0730/ exists | PASS |
| S3 | BASIS_OF_ESTIMATE validated — PARAMETRIC is valid enum | PASS |
| S4 | Required artifacts exist — Run_Context.md, Items.csv, Summary.md, QA_Report.md, Source_Index.md | PASS |
| S5 | CSV schema integrity — Items.csv and Detail.csv parseable, all required columns, valid enums, conventions respected | PASS |
| S6 | Provenance discipline — all priced rows have SourceRef; provenance completeness reported; top assumption-dependent lines listed | PASS |
| S7 | Status reporting — RUN_STATUS = WARNINGS declared | PASS |
| S8 | Operator acceptance checklist | See below |

### S8 — Operator Acceptance Checklist

| Criterion | Status |
|-----------|--------|
| RUN_STATUS is OK or WARNINGS with clearly bounded gaps | PASS — WARNINGS; gaps are bounded by documented assumptions |
| Quantity takeoff (Items.csv) reviewed for completeness | PASS — 33 items covering all scope elements from all 4 documents |
| Basis-consistency checks pass | PASS — PARAMETRIC primary with 4 RATE_TABLE lines; ALLOW_MIXED_METHODS=TRUE |
| Provenance completeness reported with top gaps actionable | PASS — 100% provenance; top 5 assumption-dependent lines identified |
| Scope coverage explicit | PASS — 1 deliverable, 1 SOW item, inclusions/exclusions documented |
| No writes outside _Estimates/ | PASS |
