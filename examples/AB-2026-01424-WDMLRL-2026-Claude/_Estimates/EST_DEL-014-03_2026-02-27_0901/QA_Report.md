# QA Report — EST_DEL-014-03_2026-02-27_0901

## RUN_STATUS: WARNINGS

---

## S1 — Write Quarantine Respected

**PASS.** All outputs written exclusively under `{RUN_ROOT}/_Estimates/EST_DEL-014-03_2026-02-27_0901/`. No project truth files modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-014-03_2026-02-27_0901` created under `{RUN_ROOT}/_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` — valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required files produced:
- [x] Run_Context.md
- [x] Items.csv
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (optional but produced)

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- Columns: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes — all present.
- 23 rows; all rows trace to a source document and section.
- PricingMode values: UNIT_RATE (17 rows), LUMP_SUM (6 rows) — all valid.
- Lump-sum items correctly use Qty=1, Unit=LS.
- No TBD quantities; all quantities are populated (parametric assumptions where design is TBD).

### Detail.csv
**PASS.**
- Columns: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes — all present.
- 23 rows; all `Method` values = PARAMETRIC — valid.
- Allowance/parametric convention: lump-sum items have Qty=1, Unit=LS, UnitRate=Amount. **PASS.**
- All amounts are numeric (no TBD amounts).

## S6 — Provenance Discipline

**PASS with notes.**
- 23/23 rows (100%) have non-TBD SourceRef entries.
- 6 rows reference specific price source files (Construction_Labour_Rates.csv, Underground_Utility_Rates.csv, Level_of_Effort.csv + Professional_Staff_Rates.csv).
- 17 rows reference parametric derivations documented in Assumptions_Log.md.
- **No `location TBD` entries.**

### Provenance quality breakdown:
| Source Type | Line Count | Pct |
|---|---|---|
| Direct rate table reference | 6 | 26% |
| Parametric derivation (documented in Assumptions_Log) | 17 | 74% |
| location TBD | 0 | 0% |

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Rationale: Totals are meaningful ($38,324.20 CAD) but material assumptions remain:
- Multiple critical design parameters TBD (pump flow rate, pipe sizing, freeze protection, backflow device type)
- 100% PARAMETRIC method with no vendor quotes
- Pump equipment ($8,500) is the largest single line item and has LOW confidence
- Overall confidence is LOW-MEDIUM

The estimate is NOT `FAILED_INPUTS` because:
- All four deliverable documents were present and read
- Price sources provided usable labour rates and utility rates
- Parametric estimation was permitted per FALLBACK_POLICY=ALLOW_PARAMETRIC
- All items are priced (no TBD amounts)

The estimate is NOT `OK` because:
- No vendor quotes available for equipment
- Multiple design TBDs create material uncertainty bands
- Pump cost range ($5,000-$12,000) represents +/- 40% on the largest line item

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS — gaps are identified and bounded in Summary.md |
| Items.csv reviewed for completeness | PASS | 23 items covering all installation phases from Procedure.md |
| Basis-consistency checks | PASS | 100% PARAMETRIC — consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% of rows have SourceRef; 26% direct rate table, 74% parametric |
| Scope coverage explicit | PASS | 1 deliverable in scope; all 4 documents read; 0 missing documents |
| No writes outside _Estimates/ | PASS | Write quarantine respected |

---

## Warnings Summary

| # | Warning | Severity | Impact |
|---|---|---|---|
| W-001 | Pump flow rate TBD — blocks precise pump selection and pricing | HIGH | Pump cost uncertainty +/- $3,500 |
| W-002 | Fill connection size TBD — affects piping and hardware costs | MEDIUM | Piping rate sensitivity +/- 20% |
| W-003 | Freeze protection method TBD — heat trace assumed; alternatives may differ | MEDIUM | Freeze protection cost +/- $500 |
| W-004 | Backflow device type TBD — DCVA assumed | MEDIUM | Device cost +/- $800 |
| W-005 | Bidirectional operation ambiguity (Conflict C-003) — estimate covers cistern replenishment only | HIGH | If extraction required, could add $3,000-$8,000 |
| W-006 | Fill line run length assumed 15 m — actual routing TBD | LOW | $130/m piping + $85/m heat trace per metre change |
| W-007 | No vendor quotes — all items parametric | MEDIUM | Overall estimate accuracy +/- 25-40% |
| W-008 | Plumbing permit fee is jurisdictional allowance | LOW | Fee may be $500-$3,000 |

---

## What to Fix for a Cleaner Rerun

1. **Obtain pump vendor quote** — resolves W-001, W-007 partially. This is the single highest-value improvement.
2. **Complete PKG-006 IFC design** — resolves W-001, W-002, W-003, W-004, W-006. Provides actual pipe sizes, routing, freeze protection specification, and backflow device type.
3. **Owner ruling on Conflict C-003** (bidirectional operation) — resolves W-005. Confirms whether extraction scope is IN or OUT for DEL-014-03.
4. **Confirm actual permit fees** with Camrose County — resolves W-008.
5. **Provide fill line routing from IFC drawings** — resolves W-006 with actual run lengths.
