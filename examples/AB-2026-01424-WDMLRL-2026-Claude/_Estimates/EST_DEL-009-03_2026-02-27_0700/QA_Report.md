# QA_Report.md
## Estimate QA Report — DEL-009-03 Safety Code Permits

---

### RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all lines are priced (no TBD amounts), but 9 of 11 lines rely on parametric hour assumptions not backed by the LOE source data. Material TBDs remain in the underlying deliverable documents (permit categories, inspection counts). The estimate is usable for budgeting but requires validation of assumed hours before commitment.

---

### S1 — Write Quarantine Respected

| Check | Result |
|-------|--------|
| All outputs written under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |

---

### S2 — Snapshot Created

| Check | Result |
|-------|--------|
| Snapshot folder exists | PASS |
| Folder name: EST_DEL-009-03_2026-02-27_0700 | PASS |

---

### S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE provided | PASS |
| Value: PARAMETRIC | PASS (valid enum) |

---

### S4 — Required Artifacts Exist

| Artifact | Status |
|----------|--------|
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

### S5 — CSV Schema Integrity

#### Items.csv

| Check | Result |
|-------|--------|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to a source document | PASS (all rows have SourceDoc + SourceSection) |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 11 items |
| Qty values | All numeric (no TBDs) |

#### Detail.csv

| Check | Result |
|-------|--------|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS (all PARAMETRIC) |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS |
| Row count | 11 lines |
| Amount values | All numeric (no TBDs) |

---

### S6 — Provenance Discipline

| Metric | Value |
|--------|-------|
| Total priced rows | 11 |
| Rows with non-TBD SourceRef | 11 (100%) |
| Rows with SourceRef = "location TBD" | 0 |
| Provenance completeness | 100% |

**Top provenance notes:**
- Lines L-009-03-01 and L-009-03-02 have strong provenance (LOE + rate table).
- Lines L-009-03-03 through L-009-03-11 reference Professional_Staff_Rates.csv for rates but rely on Assumptions_Log.md for hour quantities (parametric estimates with assumed hours).

---

### S7 — Status Reporting

| Field | Value |
|-------|-------|
| RUN_STATUS | WARNINGS |
| Reason | All lines priced but 82% (9/11) rely on parametric hour assumptions not in LOE. Multiple Datasheet TBDs (permit types, counts) affect quantity certainty. |

---

### S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|-----------|--------|-------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are clearly bounded (LOE sparse for specialty roles; permit category count TBD) |
| Items.csv reviewed for completeness | PASS | 11 items covering all 5 procedure phases, Prime Contractor designation, and OH&S pre-qualification |
| Basis-consistency checks pass | PASS | All 11 lines use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 100% provenance; assumptions documented |
| Scope coverage explicit | PASS | 1 deliverable in scope; exclusions documented (permit fees, DEL-019-01, DEL-009-04, design packages) |
| No writes outside _Estimates/ | PASS | Verified |

---

### Quantity Takeoff Coverage

| Deliverable | Documents Available | Documents Read | Items Extracted | Missing Documents |
|-------------|--------------------|--------------------|-----------------|-------------------|
| DEL-009-03 | 5 (CONTEXT + 4 production) | 5 | 11 | None |

---

### Pricing Coverage

| Metric | Value |
|--------|-------|
| Total items in Items.csv | 11 |
| Items priced in Detail.csv | 11 (100%) |
| Items with TBD amounts | 0 (0%) |
| Items backed by LOE data | 2 (18%) |
| Items with parametric assumptions | 9 (82%) |

---

### Basis-Consistency Check

| Metric | Value |
|--------|-------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Lines with Method=PARAMETRIC | 11 (100%) |
| Lines with other Method | 0 (0%) |
| ALLOW_MIXED_METHODS | TRUE (not exercised; all lines are PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (exercised for 9 lines without LOE backing) |
| Consistency | PASS |

---

### What to Fix for a Cleaner Rerun

1. **Add LOE rows for R-22 (Permitting Specialist) and R-05 (HSE Manager) to Level_of_Effort.csv for DEL-009-03.** The current LOE only covers R-01 and R-08 (10 total hours), which represent management oversight but not the specialty permitting effort. Adding LOE data for these roles would move 9 lines from LOW to MED confidence.

2. **Resolve Datasheet TBDs:** Confirm the specific Safety Code permit categories, the number of permits required, and the accredited agency identity. This would allow more precise quantity estimates for application preparation (ITM-009-03-06) and inspection coordination (ITM-009-03-08).

3. **Validate assumed hours for ITM-009-03-03 through ITM-009-03-11.** The current parametric hour estimates are based on procedure complexity and the number of anticipated permit categories. A subject-matter expert review would improve confidence.

4. **Consider adding a contingency line** if the estimate is to be used for budget commitment. The LOW confidence on 82% of lines suggests a contingency allowance of 15-25% may be appropriate.
