# QA Report — EST_DEL-015-01_2026-02-26_2232

## RUN_STATUS: WARNINGS

This estimate produces meaningful totals but has material TBDs and assumptions that require resolution before the estimate can be considered firm.

---

## S1 — Write Quarantine Respected

**PASS.** All files written exclusively under `_Estimates/EST_DEL-015-01_2026-02-26_2232/`. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-015-01_2026-02-26_2232` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Items.csv
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Detail.csv (recommended; produced)
- [x] WBS_CBS_Matrix.csv
- [x] Decision_Log.md
- [x] Assumptions_Log.md

## S5 — CSV Schema Integrity

### Items.csv
**PASS.**
- 21 rows, all required columns present: ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes
- PricingMode values: UNIT_RATE (16 rows), LUMP_SUM (5 rows) — all valid
- All rows trace to a source document and section
- No TBD quantities (all quantities specified, though some are parametric estimates)

### Detail.csv
**PASS.**
- 21 rows, all required columns present: LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes
- Method values: PARAMETRIC (14 rows), RATE_TABLE (6 rows), ALLOWANCE (1 row) — all valid
- Allowance convention respected: DL-001 has Qty=1, Unit=LS, UnitRate=Amount ($28,000)
- All Amount values are numeric (no TBD amounts)

## S6 — Provenance Discipline

**PASS.** Provenance completeness: **100%** (21/21 lines have non-TBD SourceRef).

All 21 Detail.csv lines include specific SourceRef citations pointing to:
- Electrical_System_Rates.csv (items ES-02, ES-03, ES-04)
- Underground_Utility_Rates.csv (item UU-03)
- Construction_Labour_Rates.csv (items T-04, T-07, T-08)
- Professional_Staff_Rates.csv (items R-01, R-02, R-03, R-05, R-06, R-08)
- Level_of_Effort.csv (DEL-015-01 rows)
- Parametric estimates with rationale (where no specific rate table applies)

### Top Confidence Gaps (not missing provenance, but LOW confidence):
1. DL-001 — Service entrance materials ($28,000) — LOW — voltage/ampacity TBD
2. DL-002 — MDP ($4,800) — LOW — generic panelboard rate, actual MDP may differ
3. DL-006 — Utility coordination ($2,500) — LOW — utility provider/fees TBD

## S7 — Status Reporting

**RUN_STATUS = WARNINGS**

Rationale: Totals are produced for all 21 line items (no TBD amounts), but:
- 3 lines (14.3%) are LOW confidence, representing $35,300 (53.4% of total)
- Service voltage and ampacity are TBD pending PKG-004 — these are the most significant design parameters
- Utility provider is unidentified — affects coordination costs
- Multiple assumptions are recorded (see Assumptions_Log.md)

This is not FAILED_INPUTS because all items are priced with traceable sources, and the estimate falls within the benchmark range (ES-03: $45k-$95k). However, it is not OK because the LOW-confidence items represent more than half the total cost.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS) | Gaps are clearly enumerated; 3 LOW-confidence lines identified |
| Items.csv reviewed for completeness | PASS | 21 items covering all 4 procedure phases + management + documentation |
| Basis-consistency checks | PASS | Primary method PARAMETRIC; mixed methods allowed (RATE_TABLE for staff, ALLOWANCE for service entrance) |
| Provenance completeness reported | PASS | 100% — all lines have SourceRef |
| Scope coverage explicit | PASS | 1 deliverable (DEL-015-01) in scope; in-scope/out-of-scope boundary defined in Specification |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## Quantity Takeoff Coverage

| Deliverable | Documents Read | Items Extracted | Missing Documents |
|---|---|---|---|
| DEL-015-01 | 4/4 (Datasheet, Specification, Guidance, Procedure) | 21 | None |

Items by source document:
- Datasheet: 4 items (service entrance, MDP, service trench, grounding)
- Specification: 4 items (welding receptacles, utility coordination, permit, conformance closure)
- Procedure: 13 items (inspections, commissioning, as-builts, management staff, trade labour)

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items | 21 |
| Items priced | 21 (100%) |
| Items TBD | 0 (0%) |
| HIGH confidence | 0 (0%) |
| MEDIUM confidence | 18 (85.7%) |
| LOW confidence | 3 (14.3%) |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| PRIMARY BASIS | PARAMETRIC |
| PARAMETRIC lines | 14 (66.7%) |
| RATE_TABLE lines | 6 (28.6%) |
| ALLOWANCE lines | 1 (4.8%) |
| ALLOW_MIXED_METHODS | TRUE — mixed methods allowed and documented |
| FALLBACK_POLICY | ALLOW_PARAMETRIC — ALLOWANCE fallback used for DL-001 (justified: service entrance scope too broad for parametric without design) |

---

## What to Fix for a Cleaner Rerun

1. **Obtain PKG-004 IFC electrical design** — resolves service voltage, ampacity, MDP size, and grounding design. This would convert DL-001 and DL-002 from LOW to MEDIUM/HIGH confidence.
2. **Identify utility provider** — enables firm pricing for utility application fees, connection costs. Would improve DL-006 confidence.
3. **Receive welding equipment specs from Owner** — confirms welding circuit count and sizing (ITEM-005).
4. **Measure service trench length from IFC drawings** — replaces the 15m parametric estimate with an actual measurement.
5. **Enumerate HVAC/mechanical loads** — ensures service sizing accounts for all downstream loads.
6. **Obtain Alberta Safety Code permit fee schedule** — replaces parametric permit cost estimate with actual fee.
