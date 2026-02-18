# QA Report — EST_DEL-01-02_2026-02-18_0900

## RUN_STATUS: WARNINGS

**Rationale:** Priced totals exist and are meaningful ($13,900 CAD from 2 priced lines), but 1 of 3 line items is TBD due to missing pricing source (software/tools). The TBD gap is bounded and non-critical relative to total.

---

## S1 — Write Quarantine

**PASS.** All files written under `{ESTIMATES_ROOT}/EST_DEL-01-02_2026-02-18_0900/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder exists at `_Estimates/EST_DEL-01-02_2026-02-18_0900/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (optional but produced)
- [x] Blockers.md (optional but produced)

## S5 — Detail Schema Integrity

**PASS.** `Detail.csv` contains all 14 required columns. Method values are all `RATE_TABLE` (consistent with BASIS_OF_ESTIMATE). No ALLOWANCE/PARAMETRIC convention applies (no LS lines with those methods).

| Check | Result |
|---|---|
| All required columns present | PASS |
| Method values valid | PASS (all RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| TBD rows handled | PASS (L-003 has TBD amounts, flagged in QA) |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total line items | 3 |
| Lines with non-TBD SourceRef | 2 (L-001, L-002) |
| Lines with `location TBD` SourceRef | 1 (L-003) |
| Provenance completeness | 67% |

**Top missing-source offenders:**
1. L-003 (Scheduling software / tools) — no pricing source provided for this cost driver.

## S7 — Status Reporting

**RUN_STATUS = WARNINGS**

- Totals are meaningful ($13,900 CAD priced).
- Material TBD: 1 line (software/tools) — bounded gap, likely low-value relative to total.
- Assumptions: LOE hours are PARAMETRIC basis (professional judgment); see Assumptions_Log.

## S8 — Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS; gap is 1 bounded TBD line) |
| Basis-consistency checks pass | PASS (all Method = RATE_TABLE) |
| Provenance completeness reported | PASS (67%; 1 gap identified) |
| Scope coverage explicit | PASS (1 deliverable in scope; 0 excluded; 0 blocked) |
| No writes outside _Estimates/ | PASS |

---

## What to Fix for a Cleaner Rerun

1. **Provide software/tools pricing.** Add a rate table entry, quote, or allowance for scheduling software to PRICE_SOURCES. This would resolve L-003 and raise provenance completeness to 100%.
2. **Consider overhead treatment.** If software costs are embedded in overhead/markup applied at aggregation, document this decision and L-003 may be removed or set to $0 with a note.
