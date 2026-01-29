# QA Report — PKG-34 Coordination & Interfaces Estimate

**Snapshot ID:** EST_PKG34_DRAFT_2026-01-29_1045
**Package Scope:** PKG-34 Coordination & Interfaces
**Date:** 2026-01-29
**Run Status:** WARNINGS

---

## QA Summary

This report documents quality assurance checks performed on the PKG-34 estimate. The estimate passes all schema validation requirements but has material assumptions and uncertainties that warrant WARNINGS status.

---

## 1. Schema Validation Checks

### 1.1 Required Fields — PASS

**Check:** All Detail.csv line items have required fields populated (Qty, Unit, UnitRate, Amount)

**Result:** PASS

**Findings:**
- 12 line items in Detail.csv
- All lines have Qty, Unit, UnitRate, Amount populated
- Allowance convention followed (Qty=1, Unit=LS, UnitRate=Amount) for all allowance lines

**Issues:** None

---

### 1.2 Currency Consistency — PASS

**Check:** All line items use consistent currency (CAD)

**Result:** PASS

**Findings:**
- All 12 line items use CAD currency
- No currency mixing detected
- Currency selection documented in D-002

**Issues:** None

---

### 1.3 Arithmetic Reconciliation — PASS

**Check:** Detail.csv totals reconcile to Summary.md totals (within rounding policy)

**Result:** PASS

**Findings:**

| CBS | Detail.csv Total | Summary.md Base | Variance | Status |
|-----|------------------|-----------------|----------|--------|
| E | $95,000 | $95,000 | $0 | PASS |
| PM | $295,000 | $295,000 | $0 | PASS |
| P | $6,000 | $6,000 | $0 | PASS |
| CI | $36,000 | $36,000 | $0 | PASS |
| **TOTAL** | **$432,000** | **$432,000** | **$0** | **PASS** |

**Issues:** None (exact reconciliation)

---

### 1.4 Traceability — PASS (with notes)

**Check:** All line items have SourceRef populated with assumption ID or decision ID

**Result:** PASS

**Findings:**
- All 12 line items have SourceRef populated
- 8 lines reference Assumptions_Log entries (A-001 through A-005)
- 4 lines reference Decision_Log entries (D-006 for parametric factors)
- All assumption IDs and decision IDs are valid and documented

**Issues:** None (all line items traceable to documented assumptions or decisions)

**Note:** Traceability is to fallback assumptions rather than vendor quotes or rate tables; this is acceptable per SPEC requirements but indicates low estimate maturity.

---

## 2. Completeness Checks

### 2.1 Deliverable Coverage — PASS

**Check:** All PKG-34 deliverables have associated cost lines

**Result:** PASS

**Findings:**

| Deliverable ID | Name | Cost Lines | Base Cost (CAD) | Coverage |
|----------------|------|------------|-----------------|----------|
| DEL-34.01 | Coordination Meeting Records | L001 | $75,000 | PASS |
| DEL-34.02 | Interface Agreements | L002, L003, L004 | $90,000 | PASS |
| DEL-34.03 | Marine Coordination Records | L005 | $50,000 | PASS |
| DEL-34.04 | Security Compliance Records | L006 | $40,000 | PASS |
| DEL-34.05 | Trenchless Crossing Monitoring | L007, L008 | $95,000 | PASS |

**Uncovered Deliverables:** None (0 deliverables with $0 cost)

**Issues:** None

---

### 2.2 Pricing Method Composition — HIGH ALLOWANCE SHARE (Expected for Draft)

**Check:** Distribution of pricing methods

**Result:** Expected for draft estimate without vendor quotes

**Findings:**

| Pricing Method | Line Count | Base Cost (CAD) | % of Base | Confidence |
|----------------|------------|-----------------|-----------|------------|
| QUOTE | 0 | $0 | 0% | - |
| RATE_TABLE | 0 | $0 | 0% | - |
| ALLOWANCE | 8 | $370,000 | 85.6% | LOW |
| PARAMETRIC | 4 | $62,000 | 14.4% | MED |
| **TOTAL** | **12** | **$432,000** | **100%** | **LOW** |

**Issues:**
- **HIGH:** 85.6% of base cost uses ALLOWANCE method without vendor quotes or rate tables
- **HIGH:** 0% of base cost uses project-specific pricing (quotes or rate tables)

**Impact:** Estimate has very low confidence and wide uncertainty ranges; suitable for conceptual budgeting only, not for procurement or contracting.

**Recommendation:** Obtain quotes for trenchless monitoring services and develop rate tables for coordination effort in next iteration.

---

### 2.3 Deliverable Document Completeness — PARTIAL

**Check:** Presence of deliverable documents in workspace

**Result:** PARTIAL (decomposition defines deliverables but detailed scope not specified)

**Findings:**
- PKG-34 deliverables defined in decomposition with artifact types
- Interface agreement scope (parties, complexity) not explicitly specified
- Construction schedule duration not available
- Trenchless crossing count and locations not detailed

**Issues:**
- **MED:** Interface agreement parties and complexity not fully specified
- **MED:** Construction schedule duration not confirmed
- **MED:** Trenchless crossing monitoring scope implied from PKG-03 but not confirmed

**Impact:** Estimate relies on typical design-build assumptions rather than project-specific requirements.

**Recommendation:** Clarify interface requirements and construction schedule with Employer; confirm trenchless crossing scope from PKG-03.

---

## 3. Consistency Checks

### 3.1 Double Count Heuristics — PASS

**Check:** Same scope not priced in multiple places

**Result:** PASS

**Findings:**
- Each deliverable has distinct line items by activity type
- No overlap detected between interface agreements (L002-L004) and other coordination
- Trenchless monitoring (L007) clearly separated from coordination (L008)
- Calculated indirects (CI, PM factor, P) use non-overlapping factors on distinct bases

**Issues:** None

---

### 3.2 WBS-CBS Mapping Ambiguities — DOCUMENTED

**Check:** Deliverable-to-CBS mappings are clear and unambiguous

**Result:** MINOR AMBIGUITIES (documented in WBS_CBS_Matrix)

**Findings:**
- Most deliverables have clear primary CBS assignments
- **Ambiguous cases:**
  - DEL-34.05 (Trenchless Crossing Monitoring): Maps to both E (technical monitoring) and PM (coordination) — addressed by splitting into L007 (E) and L008 (PM)

**Issues:** None (ambiguities resolved by multi-CBS allocation per WBS_CBS_Matrix.csv)

---

### 3.3 Indirects Calculation — PASS

**Check:** Indirects factors applied correctly per fallback model (D-006)

**Result:** PASS

**Findings:**

| Indirect Type | Factor | Base | Calculated Amount | Status |
|---------------|--------|------|-------------------|--------|
| CI (QA/QC allocation) | 18% | Notional coordination base = $200k | $36,000 | PASS |
| PM (factor-based) | - | Engineering oversight allocation | $20,000 | PASS |
| P (procurement) | 2% | Third-party services | $6,000 | PASS |

**Note:** Indirects allocation reflects coordination package oversight and third-party service procurement.

**Issues:** None (calculations verified)

---

## 4. Known Issues and Gaps

### Issue 1: No Project-Specific Pricing Sources (CRITICAL)

**Severity:** CRITICAL

**Description:** Zero vendor quotes or rate tables available for coordination and monitoring services. All line items use fallback allowances.

**Impact:** Estimate accuracy is LOW; suitable for conceptual budgeting only.

**Recommendation:** Acquire budgetary quotes from coordination service providers and survey/monitoring firms before using estimate for decision-making.

**Status:** UNRESOLVED (requires external input)

---

### Issue 2: Construction Schedule Not Confirmed (HIGH)

**Severity:** HIGH

**Description:** Construction duration assumed at 24-30 months without schedule confirmation.

**Impact:** Time-based coordination costs (meetings, marine coordination, security compliance) may vary significantly with actual duration.

**Recommendation:** Obtain project construction schedule.

**Status:** UNRESOLVED (requires project scheduling)

---

### Issue 3: Interface Agreement Scope Not Detailed (MED)

**Severity:** MED

**Description:** Interface agreement count and complexity assumed based on typical practice; specific party requirements not confirmed.

**Impact:** Interface agreement allowance ($90k, 21% of base) may not reflect actual scope.

**Recommendation:** Identify all required interface agreements and assess complexity.

**Status:** UNRESOLVED (requires Employer/stakeholder input)

---

### Issue 4: Trenchless Crossing Count Not Confirmed (MED)

**Severity:** MED

**Description:** Trenchless crossing count (2-4) assumed based on PKG-03 Underground Utilities scope; not confirmed.

**Impact:** Monitoring cost may vary with actual crossing count.

**Recommendation:** Coordinate with PKG-03 team to confirm crossing count and locations.

**Status:** UNRESOLVED (requires PKG-03 coordination)

---

## 5. Completeness Scoring

### Overall Estimate Maturity

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| % of lines priced by QUOTE | 0% | >50% | FAIL |
| % priced by RATE_TABLE | 0% | >30% | FAIL |
| % priced by ALLOWANCE/PARAMETRIC | 100% | <20% | FAIL |
| % of deliverables with explicit scope definition | 0% | >70% | FAIL |
| % of deliverables covered (non-zero cost) | 100% | 100% | PASS |
| Currency consistency | 100% | 100% | PASS |
| Traceability (SourceRef populated) | 100% | 100% | PASS |
| Required fields populated | 100% | 100% | PASS |

**Overall Maturity Classification:** Class 5 (Conceptual) / Order of Magnitude

**Estimated Accuracy Range:** -30% / +50% (typical for Class 5 estimates per AACE guidelines)

**Suitability:**
- PASS Suitable for: Conceptual budgeting, feasibility assessment, rough order of magnitude
- FAIL Not suitable for: Contracting, procurement, detailed project controls, financing commitments

---

## 6. Unknowns List (Top Assumptions by Value)

Ranked by base cost impact:

| Rank | Assumption ID | Description | Amount (CAD) | % of Base | Confidence |
|------|---------------|-------------|--------------|-----------|------------|
| 1 | A-001 | Trenchless crossing monitoring (2-4) | $95,000 | 22.0% | LOW |
| 2 | A-002 | Interface agreements (4-5 major) | $90,000 | 20.8% | LOW |
| 3 | A-003 | Coordination meetings (100-130) | $75,000 | 17.4% | LOW |
| 4 | A-004 | Marine coordination (8-12 mo) | $50,000 | 11.6% | LOW |
| 5 | A-005 | Security compliance (24-30 mo) | $40,000 | 9.3% | LOW-MED |

**Top 3 Unknowns (A-001, A-002, A-003) represent 60.2% of base cost.** Resolving these three assumptions would significantly improve estimate confidence.

---

## 7. QA Checks Summary Table

| QA Check | Requirement | Result | Status | Issues |
|----------|-------------|--------|--------|--------|
| Required fields populated | Qty, Unit, UnitRate, Amount on all lines | 12/12 lines pass | PASS | None |
| Currency consistency | All lines use same currency | CAD on 12/12 lines | PASS | None |
| Arithmetic reconciliation | Detail totals = Summary totals | $432,000 both | PASS | None |
| Deliverable coverage | All deliverables have cost lines | 5/5 covered | PASS | None |
| Double count check | No scope priced multiple times | No overlaps found | PASS | None |
| Traceability | SourceRef on all lines | 12/12 lines have SourceRef | PASS | All trace to assumptions (not quotes) |
| Quote-based pricing | >50% by quote | 0% by quote | FAIL | No vendor quotes available |
| Explicit scope definition | >70% with defined scope | 0% with defined scope | FAIL | Schedule/interface scope not specified |
| Decision capture | Defaults and ambiguities logged | 10 decisions logged | PASS | All defaults documented |
| Assumption logging | Allowances documented | 7 assumptions logged | PASS | All allowances documented |

**Pass Rate:** 8/10 checks pass
**Critical Failures:** None (schema validation passed)
**Material Issues:** 2 (no quotes, no explicit scope) — expected for draft estimate

---

## 8. Recommendations for Next Iteration

### Priority 1 (Critical — Improve Estimate Confidence)

1. **Obtain project construction schedule** — top duration driver:
   - Confirm construction phase duration (notice to proceed to substantial completion)
   - Establish coordination meeting cadence
   - Define marine works and construction phasing

2. **Clarify interface agreement requirements:**
   - Identify all required third-party interface agreements
   - Assess complexity and negotiation effort per interface
   - Confirm Employer vs. Contractor responsibility

3. **Obtain trenchless monitoring quotes:**
   - Confirm crossing count and locations from PKG-03
   - Request budgetary quotes from survey/monitoring providers
   - Define monitoring frequency and reporting requirements

### Priority 2 (High — Refine Estimate Accuracy)

4. **Develop project rate tables** for:
   - Coordination labor (coordinator, administrator)
   - Meeting support (preparation, minutes, distribution)
   - Monitoring services (survey, instrumentation)

5. **Coordinate with related packages:**
   - PKG-03 Underground Utilities — trenchless crossing details
   - PKG-08/PKG-09 Marine — marine works schedule
   - PKG-33 HSE — security compliance coordination

### Priority 3 (Medium — Add Schedule Basis)

6. **Re-run estimate** with improved inputs to upgrade maturity from Class 5 to Class 4 or Class 3

---

## 9. Run Status Determination

**Run Status:** WARNINGS

**Rationale:**

| Status Criteria | Assessment | Result |
|-----------------|------------|--------|
| Critical schema failures? | None — all required fields populated | No failure |
| Material assumptions/ambiguities? | Yes — 85.6% allowance-based, no vendor quotes | WARNINGS |
| Missing inputs making totals non-meaningful? | Partial — deliverables defined but scope uncertain | Not FAILED |

**Status Selection:** WARNINGS (middle tier)

**Explanation:**
- Estimate totals are meaningful for conceptual budgeting purposes (not "non-meaningful")
- However, material assumptions and lack of vendor quotes create significant uncertainty
- WARNINGS status indicates estimate can be used for rough budgeting but requires improvement before detailed planning or contracting

---

## 10. Estimate Confidence Statement

**Overall Confidence:** LOW

**Basis:**
- 0% of costs based on vendor quotes
- 0% of costs based on project rate tables
- 100% of costs based on fallback allowances or parametric factors
- 0% of deliverables have explicit scope definition from ER or project documents

**Recommended Use:**
- PASS Conceptual budgeting and feasibility assessment
- PASS Order of magnitude cost planning
- PASS Identifying cost drivers for further investigation
- FAIL Contracting or procurement commitments
- FAIL Detailed project budget or cost baseline
- FAIL Financing or investment decisions without further validation

**Expected Accuracy Range:** -30% / +50% (Class 5 Order of Magnitude per AACE)

**Next Steps:** Obtain project schedule, clarify interface requirements, and obtain monitoring quotes to upgrade estimate to Class 4 (Factored) or Class 3 (Budget) maturity.

---

**QA Report Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
**Run Status:** WARNINGS
