# QA Report: EST_DEL-03-02_2026-02-18_1130

## RUN_STATUS: WARNINGS

Totals are meaningful and all line items are priced (no TBD amounts), but material quantity assumptions remain unresolved for cut/fill volumes and stormwater pond sizing. Over 53% of the estimate total is driven by assumed quantities.

---

## S1 -- Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under _Estimates/ | PASS |
| No deliverable files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition files modified | PASS |
| No dependency registers modified | PASS |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS |
| Folder name | EST_DEL-03-02_2026-02-18_1130 |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| Value provided | RATE_TABLE |
| Valid enum | PASS (RATE_TABLE is in {QUOTE, RATE_TABLE, HISTORICAL, PARAMETRIC, ALLOWANCE}) |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT |
| Blockers.md | PRESENT |
| Risk_Register.md | PRESENT |

## S5 -- Detail Schema Integrity

| Check | Result | Notes |
|---|---|---|
| Detail.csv parseable | PASS | 15 data rows + 1 header |
| Required columns present | PASS | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS | All 15 rows: RATE_TABLE |
| Allowance/parametric convention | N/A | No ALLOWANCE or PARAMETRIC method rows in this snapshot |
| Amount = Qty x UnitRate | PASS | Verified for all 15 rows (within DOLLAR rounding) |
| Currency consistent | PASS | All rows: CAD |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 15 |
| Rows with SourceRef (non-TBD) | 15 |
| Rows with "location TBD" | 0 |
| **Provenance completeness** | **100%** |

All line items have traceable SourceRef values pointing to specific rate table items (EC-xx, DF-xx) and/or assumption IDs (ASM-xxx).

### Source Coverage Detail

| SourceRef Pattern | Count | Notes |
|---|---|---|
| Earthwork_Civil_Rates.csv EC-xx | 14 | Primary rate source |
| Professional_Design_Fees.csv DF-02 | 1 | Design fee |
| Assumed_Project_Parameters.csv PP-xx | 8 | Quantity basis (co-cited with rate refs) |
| ASM-xxx references | 9 | Quantity assumptions (co-cited with rate refs) |

## S7 -- Basis-Consistency Check

| Check | Result | Notes |
|---|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE | |
| Method values in Detail.csv | All RATE_TABLE | |
| ALLOW_MIXED_METHODS | FALSE | |
| Mixed methods detected | NO | PASS |
| Fallback methods used | NONE | FALLBACK_POLICY=STRICT; no fallback needed |

## Confidence Distribution

| Confidence | Count | Amount (CAD) | % of Total |
|---|---|---|---|
| HIGH | 0 | $0 | 0% |
| MED | 9 | $282,562 | 59.9% |
| LOW | 6 | $189,500 | 40.1% |
| **Total** | **15** | **$472,062** | **100%** |

40% of the estimate total is LOW confidence, driven primarily by assumed cut/fill quantities and stormwater pond sizing.

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-03-02) |
| Deliverables covered | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Scope items covered | SOW-0105, SOW-0106 |

## Blocker Summary (from Dependency Analysis)

| Metric | Value |
|---|---|
| Total dependencies reviewed | 11 |
| Blocking prerequisites affecting estimate quality | 2 |
| Non-blocking interfaces | 2 |
| Satisfied prerequisites | 2 |
| External constraints | 2 |

## What to Fix for a Cleaner Rerun

1. **Resolve cut/fill quantities (ASM-001, ASM-002).** Civil engineer should extract volumes from TPN46 Sheets C2-C3 or perform independent quantity takeoff. This would move L-003 and L-004 from LOW to MED/HIGH confidence and reduce assumption-driven cost from 53% to ~31%.

2. **Determine stormwater pond sizing criteria (ASM-005).** Confirm design storm return period, pond capacity, and outlet flow rate per municipal development standards (Specification item A-003). This would move L-010 and L-011 from LOW to MED confidence.

3. **Confirm AEPA Water Act approval status.** If approved, ASM-007 can be closed. If conditions are imposed, additional earthwork scope may need to be added.

4. **Finalize site plan layout (DEL-03-01 input).** This would allow refinement of drainage swale lengths (ASM-004) and topsoil/seeding area (ASM-008).

5. **Confirm geotechnical report sufficiency.** If supplemental investigation is needed (per REQ-3214 / Datasheet item B-002), the $32,000 geotech line (L-014) may need to be increased.

With items 1 and 2 resolved, RUN_STATUS could be upgraded to OK.

---

## Operator Acceptance Checklist (S8)

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS OK or WARNINGS with bounded gaps | PASS (WARNINGS) | Gaps are clearly bounded: 53% assumption-driven; top 2 issues identified |
| Basis-consistency checks pass | PASS | All methods = RATE_TABLE; no mixed methods |
| Provenance completeness reported | PASS | 100% (15/15 rows have SourceRef) |
| Scope coverage explicit | PASS | 1 deliverable in scope, 1 covered, 0 missing, 0 blocked |
| No writes outside _Estimates/ | PASS | All output in EST_DEL-03-02_2026-02-18_1130/ |
| Top gaps are actionable | PASS | 5 specific actions listed above |
