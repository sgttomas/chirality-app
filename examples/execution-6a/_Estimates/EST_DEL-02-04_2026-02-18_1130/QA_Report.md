# QA Report — EST_DEL-02-04_2026-02-18_1130

## RUN_STATUS: WARNINGS

Some totals exist and are meaningful, but material assumptions remain regarding building dimensions, foundation type, and overhead door count that could shift the total by +/- 15-20%.

---

## S1 — Write Quarantine

| Check | Result |
|---|---|
| All files written under ESTIMATES_ROOT only | PASS |
| No deliverable working files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |
| No dependency registers modified | PASS |

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS |
| Folder name | EST_DEL-02-04_2026-02-18_1130 |

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | PASS |
| Value | RATE_TABLE |
| Valid enum value | PASS |

## S4 — Required Artifacts Exist

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

## S5 — Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable | PASS |
| Required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all RATE_TABLE) | PASS |
| Total line count | 28 |
| Allowance/parametric convention check | N/A (no ALLOWANCE or PARAMETRIC method lines) |
| Amount = Qty x UnitRate for all lines | PASS (verified) |

### Method Distribution

| Method | Count | Percentage |
|---|---|---|
| RATE_TABLE | 28 | 100% |

**Basis-consistency check:** ALLOW_MIXED_METHODS=FALSE. All lines use RATE_TABLE, consistent with BASIS_OF_ESTIMATE=RATE_TABLE. **PASS.**

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced lines | 28 |
| Lines with rate-table SourceRef | 27 (96.4%) |
| Lines with assumed rate (not from rate table) | 1 (L-027: sump rough-in; SourceRef points to ASM-23) |
| Lines with "location TBD" SourceRef | 0 |
| **Provenance completeness** | **96.4%** (27/28 have direct rate table source) |

### Provenance Gap Details

| LineID | Description | Issue | Impact |
|---|---|---|---|
| L-027 | Sump rough-in blockouts | Rate ($750/each) is estimated, not from a rate table; SourceRef points to ASM-23 in Assumptions_Log.md | LOW ($6,000 total; 0.3% of estimate) |

## S7 — Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-04) |
| Deliverables covered with line items | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items per deliverable | 28 |

### Scope Coverage vs SOW Items

| SOW Item | Covered | Notes |
|---|---|---|
| SOW-0201 (50-year design life) | YES | Material selections reflect durability intent; design fee included |
| SOW-0215 (Overhead doors 16ft clear; car-wash grade) | YES | L-019 (8 doors at $20,000 each) |
| SOW-0216 (16x16 doors; motorized; secondary mechanism) | PARTIAL | Doors and motorized openers included; secondary mechanism excluded (DEL-02-07 per cost rules) |
| SOW-0217 (Resilient flooring; sealed concrete) | YES | L-025, L-026 (sealed concrete for all areas) |
| SOW-0220 (Durability/adaptability) | YES | Envelope and structural selections reflect durability; expansion consideration in structural design |
| SOW-0221 (Solar-ready roof) | YES | L-015 (insulated metal roof panels; solar-ready; structural capacity for future solar loading) |

## S8 — Operator Acceptance Checklist

| Criterion | Assessment |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS — gaps are bounded: foundation type TBD (+/-20%), building dimensions TBD (+/-15%), OH door count TBD (+$0 to +$160k) |
| Basis-consistency checks pass | PASS — all lines RATE_TABLE |
| Provenance completeness reported | PASS — 96.4% (1 gap: sump rough-in at 0.3% of total) |
| Scope coverage explicit | PASS — 1/1 deliverable covered; 6 SOW items addressed |
| No writes outside _Estimates/ | PASS |

---

## Confidence Summary

| Confidence Level | Lines | Amount | Share |
|---|---|---|---|
| MED | 27 | $1,715,269 | 99.7% |
| LOW | 1 | $6,000 | 0.3% |
| HIGH | 0 | $0 | 0.0% |

## What to Fix for a Cleaner Rerun

1. **Confirm building dimensions from DEL-02-01 architectural program.** This would convert geometric assumptions (ASM-01 through ASM-06) from ASSUMED to CONFIRMED, improving confidence from MEDIUM to HIGH for most lines.

2. **Confirm bay layouts from DEL-02-02 and DEL-02-03.** This would validate ASM-03 (bay area) and resolve BLK-05 (overhead door count for drive-through configuration).

3. **Review geotechnical report** to confirm or change foundation type (DEC-01). Currently assumed as screw piles.

4. **Obtain Alberta Building Code load tables for Penhold, AB** to validate structural steel intensity assumption (ASM-13).

5. **Provide a sump rough-in rate from a rate table** to eliminate the single non-rate-table line item (L-027). Alternatively, a supplier quote for sump blockout formwork/sleeves would satisfy provenance.

6. **Clarify drive-through door count.** If all 8 bays are drive-through (doors on both ends = 16 doors total), the overhead door line item needs to double. PP-13 states 8 as the assumed count; confirm with design team.
