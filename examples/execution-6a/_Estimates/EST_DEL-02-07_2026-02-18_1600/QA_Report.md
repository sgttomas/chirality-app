# QA Report — EST_DEL-02-07_2026-02-18_1600

## RUN_STATUS: WARNINGS

Totals are produced ($201,000 CAD) but material assumptions and unconfirmed inputs remain. All pricing uses ALLOWANCE fallback — no vendor quotes.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under `_Estimates/EST_DEL-02-07_2026-02-18_1600/` | PASS |
| No modifications to deliverable working files | PASS |
| No modifications to lifecycle files | PASS |
| No modifications to decomposition outputs | PASS |
| No modifications to dependency registers | PASS |

**Result: PASS**

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists at `_Estimates/EST_DEL-02-07_2026-02-18_1600/` | PASS |

**Result: PASS**

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | PASS (QUOTE) |
| Value is valid enum | PASS |
| Fallback applied | YES — ALLOW_ALLOWANCE used; ALLOW_MIXED_METHODS=TRUE |

**Result: PASS (with fallback)**

---

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

**Result: PASS**

---

## S5 — Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv is parseable CSV | PASS |
| All required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (all ALLOWANCE) | PASS |
| Allowance convention respected (Qty=1, Unit=LS, UnitRate=Amount for all ALLOWANCE lines) | PASS |
| Row count | 5 |

**Result: PASS**

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| **Total priced rows** | 5 |
| **Rows with non-TBD SourceRef** | 5 (100%) |
| **Rows with `location TBD` SourceRef** | 0 |
| **Provenance completeness** | 100% |

All rows reference either a PRICE_SOURCES file + item ID, or a Decision_Log/Assumptions_Log entry.

**Result: PASS**

---

## S7 — Basis-Consistency Checks

| Check | Result | Notes |
|---|---|---|
| Requested basis | QUOTE | |
| Methods used | ALLOWANCE (all 5 lines) | |
| Basis match | NO — fallback applied | Expected: FALLBACK_POLICY=ALLOW_ALLOWANCE + ALLOW_MIXED_METHODS=TRUE authorizes this deviation |
| Fallback logged | YES — DEC-EST-001 in Decision_Log.md | |

**Result: PASS (authorized deviation)**

---

## Coverage Analysis

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered | 1 (DEL-02-07) |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Scope items covered | SOW-0222 (primary), SOW-0216 (backup mechanism aspects) |
| Scope items not covered | None within DEL-02-07 boundary |

---

## Blocker Summary

| Category | Count |
|---|---|
| PENDING external constraints | 2 (Owner runtime confirmation; AHJ seismic ruling) |
| TBD upstream prerequisites | 5 (DEL-02-04, DEL-02-06, DEL-03-01, DEL-03-04, DEL-02-05) |
| Downstream handovers | 1 (DEL-01-07) |

---

## Confidence Assessment

| Metric | Value |
|---|---|
| Overall confidence | LOW |
| Lines at LOW confidence | 5 of 5 (100%) |
| Lines at MED confidence | 0 |
| Lines at HIGH confidence | 0 |

Confidence is LOW because: (a) no vendor quotes, (b) parametric pricing with wide ranges ($120k-$180k for primary item), (c) unconfirmed runtime assumption, (d) door backup mechanism not yet designed.

---

## Double-Count Risk Assessment

| Risk | Lines | Mitigation |
|---|---|---|
| EQ-04 includes "distribution to essential loads" but L-0207-020 also prices distribution | L-0207-010 + L-0207-020 | DEC-EST-003 distinguishes generator-side vs building-side distribution. Verify with vendor quote. |
| EQ-04 includes "commissioning" but L-0207-040 includes installation labour | L-0207-010 + L-0207-040 | DEC-EST-005 treats L-0207-040 as incremental site-specific labour. Verify with vendor quote. |
| DF-05 design fee may overlap with DEL-02-06 electrical engineering fees | L-0207-050 | ASM-008 flags this. Confirm allocation during design coordination. |

---

## What to Fix for a Cleaner Rerun

1. **Obtain a vendor quote** for the diesel generator system (genset, ATS, fuel tank, pad, exhaust, commissioning). This would replace the ALLOWANCE method with QUOTE and increase confidence from LOW to MED/HIGH.

2. **Confirm 72-hour runtime** with Owner (PP-26 / DEP-0207-E006). This resolves the primary assumption driving fuel tank and generator sizing.

3. **Obtain AHJ ruling on seismic anchorage** (DEP-0207-E009). This determines whether to add $3k-$8k for anchorage.

4. **Determine door backup mechanism type** during design. Battery backup vs generator-fed circuit will affect L-0207-030 pricing.

5. **Resolve DEL-02-06 interface** for electrical distribution concept. This determines emergency distribution routing and L-0207-020 accuracy.

6. **Clarify design fee allocation** — is generator design included in overall DEL-02-06 electrical engineering fees or separate?

---

## Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS — gaps are clearly identified and bounded |
| Basis-consistency checks pass or deviations approved | PASS — fallback authorized by FALLBACK_POLICY |
| Provenance completeness reported | PASS — 100% (5/5 rows) |
| Scope coverage explicit | PASS — 1/1 deliverables covered; exclusions listed |
| No writes outside _Estimates/ | PASS |
| **Overall** | **ACCEPTABLE for publication as preliminary budget allowance** |
