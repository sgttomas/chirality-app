# QA Report

## EST_DEL-05-04_2026-02-18_1800

---

## RUN_STATUS: WARNINGS

**Rationale:** Totals exist and are traceable to source evidence, but all pricing is parametric (LOW confidence) because no vendor quote is available. Material assumptions remain (camera count, scope boundary). The estimate is usable as a budget placeholder but must be replaced with vendor-quoted pricing before final submission.

---

## S1 -- Write Quarantine Respected

- **PASS.** All files written under `_Estimates/EST_DEL-05-04_2026-02-18_1800/` only.
- No deliverable working files, lifecycle files, decomposition outputs, or dependency registers were modified.

## S2 -- Snapshot Created

- **PASS.** Snapshot folder `EST_DEL-05-04_2026-02-18_1800` exists.

## S3 -- BASIS_OF_ESTIMATE Validated

- **PASS.** `QUOTE` is a valid enum value.
- **Note:** Actual method used is PARAMETRIC due to absence of vendor quotes. This is authorized by FALLBACK_POLICY=ALLOW_ALLOWANCE and ALLOW_MIXED_METHODS=TRUE. Logged in Decision_Log.md (DEC-EST-01).

## S4 -- Required Artifacts Exist

- **PASS.** All required files present:
  - Run_Context.md
  - Summary.md
  - QA_Report.md (this file)
  - Source_Index.md
  - Decision_Log.md
  - Assumptions_Log.md
  - WBS_CBS_Matrix.csv

## S5 -- Detail Schema Integrity

- **PASS.** Detail.csv contains all 14 required columns.
- **Method values:** Both lines use `PARAMETRIC` -- valid enum value.
- **Allowance/parametric convention:** Both lines have Qty=1, Unit=LS, UnitRate=Amount -- compliant.
- **Line count:** 2 lines.

## S6 -- Provenance Discipline

- **PASS.** Provenance completeness: **100%** (2/2 lines have non-TBD SourceRef).
  - L-0504-01: `Optional_Items_Pricing.csv > OPT-08`
  - L-0504-02: `Optional_Items_Pricing.csv > OPT-09`
- No `location TBD` entries.

## S7 -- Status Reporting

- **RUN_STATUS: WARNINGS** (declared above).
- Justification: Meaningful totals exist ($55,400 CAD), but:
  - All lines are LOW confidence
  - No vendor quote available (basis deviation)
  - Camera count is assumed
  - Scope boundary with DEL-02-06 is coordination-dependent

## Basis-Consistency Check

| Check | Result | Notes |
|---|---|---|
| Declared basis | QUOTE | Per brief |
| Actual methods used | PARAMETRIC (2/2 lines) | 100% deviation from declared basis |
| Deviation authorized? | YES | FALLBACK_POLICY=ALLOW_ALLOWANCE; ALLOW_MIXED_METHODS=TRUE; DEC-EST-01 |
| Mixed methods present? | NO | All lines use same method (PARAMETRIC) |

## Coverage Check

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-05-04) |
| Deliverables with pricing | 1 |
| Deliverables missing pricing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 2 |
| Lines with Amount=TBD | 0 |

## Dependency / Blocker Check

| Metric | Value |
|---|---|
| Dependencies loaded | 6 (from Dependencies.csv) |
| Blockers to final (QUOTE) pricing | 3 (B-01, B-02, B-03) |
| Blockers to this parametric run | 0 |

## What to Fix for a Cleaner Rerun

1. **Obtain vendor quotes** for camera system installation and monitoring service. This would allow a true QUOTE-basis run with higher confidence.
2. **Confirm camera count** by finalizing DEL-02-01 architectural layout. Update PP-29 accordingly.
3. **Define scope split** with DEL-02-06 for network equipment (PoE switches, VLAN, cabling beyond camera zone). Document in a coordination artifact.
4. **Clarify monitoring contract terms** (annual vs multi-year, escalation, service levels) to refine OPT-09 pricing.
5. **If both DEL-05-03 and DEL-05-04 are elected**, add an integration line item for access control + camera system coordination.

## Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS -- gaps are clearly bounded (3 blockers, all actionable) |
| Basis-consistency checks pass or deviations approved | Deviation approved: FALLBACK + MIXED authorized; logged |
| Provenance completeness reported | 100% -- reported above |
| Scope coverage explicit | 1/1 deliverable covered; 2 lines; 0 TBD amounts |
| No writes outside _Estimates/ | Confirmed |
