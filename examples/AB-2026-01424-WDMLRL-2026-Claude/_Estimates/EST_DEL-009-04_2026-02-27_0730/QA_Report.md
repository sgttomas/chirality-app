# QA_Report.md
## Estimate QA Report — DEL-009-04 Code Compliance Register & Inspection Log

**RunID:** EST_DEL-009-04_2026-02-27_0730
**RUN_STATUS: WARNINGS**

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs written under _Estimates/ | PASS |
| No files outside _Estimates/ modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists: EST_DEL-009-04_2026-02-27_0730/ | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE value | PARAMETRIC |
| Valid enum value | PASS |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PASS |
| Items.csv | PASS |
| Summary.md | PASS |
| QA_Report.md | PASS (this file) |
| Source_Index.md | PASS |
| Detail.csv | PASS (optional; produced) |
| WBS_CBS_Matrix.csv | PASS |
| Decision_Log.md | PASS |
| Assumptions_Log.md | PASS |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| Row count | 20 rows |
| All rows trace to source document and section | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| TBD quantities flagged in Notes | PASS (ITEM-011 through ITEM-017) |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Row count | 20 rows |
| Method values valid (all PARAMETRIC) | PASS |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS |
| All ItemIDs in Detail.csv match Items.csv | PASS |

---

## S6 — Provenance Discipline

### Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail.csv rows | 20 |
| Rows with substantive SourceRef | 10 (DL-001 through DL-008, DL-019, DL-020) |
| Rows with "location TBD" SourceRef | 10 (DL-009 through DL-018) |
| Provenance completeness | 50% |

### Top Missing-Source Offenders

| LineID | Description | Reason |
|---|---|---|
| DL-009 | Code identification completeness check | No LOE hours allocated; activity not in source |
| DL-010 | Population completeness checkpoint | No LOE hours allocated; activity not in source |
| DL-011 | Ongoing inspection coordination (Phase 3) | Construction-phase operational effort; depends on permit condition count |
| DL-012 | Periodic register audit and KPI reporting | Audit count depends on construction duration |
| DL-013 | County representative coordination per inspection | Inspection count TBD pending permit issuance |
| DL-014 | Inspection report delivery per inspection | Inspection count TBD pending permit issuance |
| DL-015 | Deficiency documentation and tracking | Deficiency count unknown and variable |
| DL-016 | Mid-lifecycle regulatory change incorporation | Contingent activity; may not occur |
| DL-017 | Register maintenance through guarantee period | 2-year post-CCC effort; not in LOE source |
| DL-018 | Final compliance summary and closeout | Closeout effort not in LOE source |

---

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Rationale: Meaningful priced totals exist for register setup activities ($1,530.00 CAD from 10 hours of allocated professional effort). However, material TBDs remain for construction-phase operational effort (50% of line items are TBD). The priced total represents setup effort only and significantly underestimates the full lifecycle cost of DEL-009-04.

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS) | Gaps are clearly bounded: setup effort is priced; operational effort is explicitly TBD with reasons |
| Items.csv reviewed for completeness | PASS | 20 items extracted across all 5 Procedure phases and Specification requirements |
| Basis-consistency checks pass | PASS | All Method values are PARAMETRIC, consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 50% provenance; top gaps listed above |
| Scope coverage explicit | PASS | 1 deliverable included (DEL-009-04); exclusions documented in Summary.md |
| No writes outside _Estimates/ | PASS | |

---

## What to Fix for a Cleaner Rerun

1. **Add operational LOE hours.** The Level_of_Effort.csv should include hours for Phase 3 (construction-phase register operation), Phase 4 (guarantee period), and Phase 5 (closeout). This requires an estimate of permit condition count and construction duration.

2. **Include Permitting Specialist (R-22) in LOE.** Consider allocating R-22 Permitting Specialist hours for ongoing code process tracking during construction, rather than relying solely on R-01 (PM) and R-08 (CE).

3. **Quantify inspection count.** Once permits are issued (DEL-009-01, DEL-009-02, DEL-009-03), the inspection count can drive UNIT_RATE pricing for items DL-011 through DL-014.

4. **Estimate audit frequency.** Confirm monthly or milestone-based audit frequency and construction duration to price DL-012 (periodic register audits).

5. **Estimate guarantee period effort.** A parametric model for guarantee-period register maintenance (e.g., hours per month x 24 months) would price DL-017.
