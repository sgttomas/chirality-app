# QA_Report.md
## Estimate QA Report — DEL-009-04 Code Compliance Register & Inspection Log

**RunID:** EST_DEL-009-04_2026-02-28_0806
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
| Snapshot folder exists: EST_DEL-009-04_2026-02-28_0806/ | PASS |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE value | PARAMETRIC |
| Valid enum value | PASS |
| Mixed methods present (ALLOWANCE used for 3 items) | PASS (ALLOW_MIXED_METHODS = TRUE) |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PASS |
| Items.csv | PASS |
| Summary.md | PASS |
| QA_Report.md | PASS (this file) |
| Source_Index.md | PASS |
| Detail.csv | PASS |
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
| All Qty x UnitRate = Amount | PASS |
| Method values valid (17 PARAMETRIC + 3 ALLOWANCE) | PASS |
| ALLOWANCE items flagged with LOW confidence | PASS (DL-015, DL-016, DL-017) |
| All ItemIDs in Detail.csv match Items.csv | PASS |
| No TBD values in Qty, UnitRate, or Amount | PASS (all resolved) |

---

## S6 — Provenance Discipline

### Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail.csv rows | 20 |
| Rows with substantive SourceRef | 17 |
| Rows with empty SourceRef (ALLOWANCE items) | 3 (DL-015, DL-016, DL-017) |
| Provenance completeness | 85% |

### ALLOWANCE Items Without Parametric Source

| LineID | Description | Amount (CAD) | Rationale |
|---|---|---|---|
| DL-015 | Deficiency documentation and corrective action tracking | 1,500.00 | Deficiency count unknown and inherently variable; fixed allowance based on professional judgment |
| DL-016 | Mid-lifecycle regulatory change incorporation | 900.00 | Contingent activity; may or may not occur during construction lifecycle |
| DL-017 | Register maintenance through guarantee period (Phase 4) | 1,500.00 | 2-year post-CCC maintenance period; effort level depends on outstanding deficiencies at CCC |

---

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Rationale: All 20 detail lines are now priced (0 TBDs, up from 10 TBDs in the prior snapshot). The total priced amount is $10,670.00 CAD. However, 3 items totalling $3,900.00 (36.6% of total) are ALLOWANCE-method at LOW confidence, representing operationally contingent activities whose scope cannot be parametrically derived. These allowances are bounded and documented but introduce material uncertainty into the total.

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS) | Gaps are bounded: 3 explicit allowance items with documented rationale |
| Items.csv reviewed for completeness | PASS | 20 items across all 5 Procedure phases and Specification requirements |
| Basis-consistency checks pass | PASS | 17 PARAMETRIC + 3 ALLOWANCE; ALLOW_MIXED_METHODS = TRUE |
| Provenance completeness reported | PASS | 85% provenance; 3 allowance items lack parametric source by definition |
| Scope coverage explicit | PASS | 1 deliverable included (DEL-009-04); exclusions documented in Summary.md |
| No writes outside _Estimates/ | PASS | |
| Arithmetic verified | PASS | All Qty x UnitRate = Amount; total cross-checked |

---

## S9 — Comparison with Prior Snapshot

| Metric | Prior (0730) | Current (0806) | Delta |
|---|---|---|---|
| TBD lines | 10 | 0 | -10 |
| Priced total (CAD) | 3,090.00 | 10,670.00 | +7,580.00 |
| PARAMETRIC lines | 10 | 17 | +7 |
| ALLOWANCE lines | 0 | 3 | +3 |
| Provenance completeness | 50% | 85% | +35pp |
| Roles priced | 2 (R-01, R-08) | 5 (R-01, R-06, R-08, R-09, R-22) | +3 |

---

## What to Fix for a Cleaner Rerun

1. **Replace allowance items with parametric pricing.** Once permit conditions are issued and deficiency history from comparable projects is available, DL-015 (deficiency tracking) can be converted to a UNIT_RATE basis. Similarly, DL-016 (regulatory change) and DL-017 (guarantee maintenance) can be parametrically modelled with better scope definition.

2. **Validate allowance quantum.** The $1,500 deficiency tracking and $1,500 guarantee period allowances are professional-judgment estimates. Benchmarking against comparable projects would improve confidence.

3. **Reconcile LOE hours fully.** Approximately 6 hours across R-06, R-09, and R-22 are implicitly absorbed within allowance items. A full hour-by-hour allocation table would improve traceability.
