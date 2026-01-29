# QA Report — PKG-00 Site Establishment Estimate

**Snapshot ID:** EST_PKG00_DRAFT_2026-01-28_2315
**Package Scope:** PKG-00 Site Establishment
**Date:** 2026-01-28
**Run Status:** WARNINGS

---

## QA Summary

This report documents quality assurance checks performed on the PKG-00 estimate. The estimate passes all schema validation requirements but has material assumptions and uncertainties that warrant WARNINGS status.

---

## 1. Schema Validation Checks

### 1.1 Required Fields — PASS

**Check:** All Detail.csv line items have required fields populated (Qty, Unit, UnitRate, Amount)

**Result:** ✓ PASS

**Findings:**
- 18 line items in Detail.csv
- All lines have Qty, Unit, UnitRate, Amount populated
- Allowance convention followed (Qty=1, Unit=LS, UnitRate=Amount) for all allowance lines

**Issues:** None

---

### 1.2 Currency Consistency — PASS

**Check:** All line items use consistent currency (CAD)

**Result:** ✓ PASS

**Findings:**
- All 18 line items use CAD currency
- No currency mixing detected
- Currency selection documented in D-002

**Issues:** None

---

### 1.3 Arithmetic Reconciliation — PASS

**Check:** Detail.csv totals reconcile to Summary.md totals (within rounding policy)

**Result:** ✓ PASS

**Findings:**

| CBS | Detail.csv Total | Summary.md Base | Variance | Status |
|-----|------------------|-----------------|----------|--------|
| E | $65,000 | $65,000 | $0 | ✓ |
| PM | $97,630 | $97,630 | $0 | ✓ |
| P | $10,400 | $10,400 | $0 | ✓ |
| MAT | $520,000 | $520,000 | $0 | ✓ |
| CD | $475,000 | $475,000 | $0 | ✓ |
| CI | $265,500 | $265,500 | $0 | ✓ |
| **TOTAL** | **$1,433,530** | **$1,433,530** | **$0** | **✓** |

**Issues:** None (exact reconciliation)

---

### 1.4 Traceability — PASS (with notes)

**Check:** All line items have SourceRef populated with assumption ID or decision ID

**Result:** ✓ PASS

**Findings:**
- All 18 line items have SourceRef populated
- 13 lines reference Assumptions_Log entries (A-001 through A-013)
- 5 lines reference Decision_Log entries (D-006 for parametric factors)
- All assumption IDs and decision IDs are valid and documented

**Issues:** None (all line items traceable to documented assumptions or decisions)

**Note:** Traceability is to fallback assumptions rather than vendor quotes or rate tables; this is acceptable per SPEC requirements but indicates low estimate maturity.

---

## 2. Completeness Checks

### 2.1 Deliverable Coverage — PASS

**Check:** All PKG-00 deliverables have associated cost lines

**Result:** ✓ PASS

**Findings:**

| Deliverable ID | Name | Cost Lines | Base Cost (CAD) | Coverage |
|----------------|------|------------|-----------------|----------|
| DEL-00.01 | Site Establishment Design Drawing Set | L001 | $12,000 | ✓ |
| DEL-00.02 | Site Establishment Technical Specification | L002 | $10,000 | ✓ |
| DEL-00.03 | Site Establishment Procedures | L003 | $9,000 | ✓ |
| DEL-00.04 | Contractor's Equipment Schedule | L004 | $5,000 | ✓ |
| DEL-00.05 | Road Access & Security (docs + physical) | L005, L012 | $83,000 | ✓ |
| DEL-00.06 | Pre-Works Road Survey | L006 | $15,000 | ✓ |
| DEL-00.07 | Post-Works Road Survey (survey + remediation) | L007, L008 | $43,000 | ✓ |
| DEL-00.08 | Temporary Water Supply (design + install) | L009, L010, L011 | $55,000 | ✓ |

**Uncovered Deliverables:** None (0 deliverables with $0 cost)

**Issues:** None

---

### 2.2 Pricing Method Composition — HIGH ALLOWANCE SHARE (Expected for Draft)

**Check:** Distribution of pricing methods

**Result:** ✓ Expected for draft estimate without vendor quotes

**Findings:**

| Pricing Method | Line Count | Base Cost (CAD) | % of Base | Confidence |
|----------------|------------|-----------------|-----------|------------|
| QUOTE | 0 | $0 | 0% | - |
| RATE_TABLE | 0 | $0 | 0% | - |
| ALLOWANCE | 13 | $1,257,000 | 87.7% | LOW |
| PARAMETRIC | 5 | $176,530 | 12.3% | MED |
| **TOTAL** | **18** | **$1,433,530** | **100%** | **LOW** |

**Issues:**
- **HIGH:** 87.7% of base cost uses ALLOWANCE method without vendor quotes or rate tables
- **HIGH:** 0% of base cost uses project-specific pricing (quotes or rate tables)

**Impact:** Estimate has very low confidence and wide uncertainty ranges; suitable for conceptual budgeting only, not for procurement or contracting.

**Recommendation:** Obtain vendor quotes and develop rate tables to replace allowances in next iteration.

---

### 2.3 Deliverable Document Completeness — PARTIAL

**Check:** Presence of 4-document sets in each deliverable folder

**Result:** ⚠ PARTIAL (documents exist but mark quantities as "TBD")

**Findings:**
- All 8 deliverables have 4-document sets (Datasheet, Specification, Guidance, Procedure) present
- All deliverables have metadata files (_CONTEXT, _DEPENDENCIES, _REFERENCES, _STATUS) present
- **However:** Most deliverables mark physical quantities, standards, and requirements as "TBD" pending Employer's Requirements
- `_REFERENCES.md` files state "no references identified yet" for all deliverables

**Issues:**
- **MED:** Physical quantities (office count, fencing length, laydown area sizes) marked as "TBD" in deliverable Datasheets
- **MED:** Specific standards and codes marked as "TBD" in deliverable Specifications
- **MED:** No external reference documents available in `_REFERENCES.md` files

**Impact:** Estimate relies on typical assumptions rather than project-specific quantities; accuracy limited until ER and reference documents available.

**Recommendation:** Obtain Employer's Requirements (Volume 2 Part 1) and update deliverable reference sections.

---

## 3. Consistency Checks

### 3.1 Double Count Heuristics — PASS

**Check:** Same scope not priced in multiple places

**Result:** ✓ PASS

**Findings:**
- Each deliverable has distinct line items
- No overlap detected between engineering deliverables (DEL-00.01, DEL-00.02, DEL-00.08 designs)
- Physical works clearly separated (L012 security, L010-L011 water, L013-L014 general facilities)
- Calculated indirects (CI, PM, P) use non-overlapping factors on distinct bases

**Issues:** None

---

### 3.2 WBS-CBS Mapping Ambiguities — DOCUMENTED

**Check:** Deliverable-to-CBS mappings are clear and unambiguous

**Result:** ⚠ MINOR AMBIGUITIES (documented in WBS_CBS_Matrix)

**Findings:**
- Most deliverables have clear primary CBS assignments
- **Ambiguous cases:**
  - DEL-00.05 (Road Access & Security): Maps to both PM (planning/procedures) and CD (physical installation) — addressed by splitting into L005 (PM) and L012 (CD)
  - DEL-00.07 (Post-Works Survey): Maps to both E (survey) and CD (remediation) — addressed by splitting into L007 (E) and L008 (CD)
  - DEL-00.08 (Water Supply): Maps to E (design), MAT (materials), CD (installation) — addressed by splitting into L009 (E), L010 (MAT), L011 (CD)

**Issues:** None (ambiguities resolved by multi-CBS allocation per WBS_CBS_Matrix.csv)

---

### 3.3 Indirects Calculation — PASS

**Check:** Indirects factors applied correctly per fallback model (D-006)

**Result:** ✓ PASS

**Findings:**

| Indirect Type | Factor | Base | Calculated Amount | Status |
|---------------|--------|------|-------------------|--------|
| CI (factor-based) | 18% | CD = $475k | $85,500 | ✓ Correct |
| PM (factor-based) | 6% | CD+CI+MAT = $1,260.5k | $75,630 | ✓ Correct |
| P (procurement) | 2% | MAT = $520k | $10,400 | ✓ Correct |

**Issues:** None (calculations verified)

---

## 4. Known Issues and Gaps

### Issue 1: No Project-Specific Pricing Sources (CRITICAL)

**Severity:** CRITICAL

**Description:** Zero vendor quotes, budgetary proposals, or project rate tables available. All line items use fallback allowances.

**Impact:** Estimate accuracy is LOW; suitable for conceptual budgeting only.

**Recommendation:** Acquire vendor quotes for major cost drivers (site facilities, security, utilities) before using estimate for decision-making or contracting.

**Status:** UNRESOLVED (requires external input)

---

### Issue 2: Missing Physical Quantities (HIGH)

**Severity:** HIGH

**Description:** Deliverable Datasheets mark physical quantities as "TBD" (office count, laydown size, fencing length, utility capacities, etc.)

**Impact:** Cannot create detailed quantity takeoffs; forced to use high-level allowances with wide ranges.

**Recommendation:** Obtain Employer's Requirements and develop preliminary site layout (DEL-00.01) to quantify physical scope elements.

**Status:** UNRESOLVED (requires ER and design development)

---

### Issue 3: Construction Schedule Not Available (MED)

**Severity:** MED

**Description:** Detailed construction schedule with durations and milestones not available; time-based costs (gate staffing, trailer rentals, equipment rentals) estimated using assumptions.

**Impact:** Time-based costs have high uncertainty; duration changes significantly affect total cost.

**Recommendation:** Develop construction schedule (milestone dates, critical path, overall duration) and update time-based cost estimates.

**Status:** UNRESOLVED (requires project scheduling)

---

### Issue 4: Employer's Requirements Not Available (MED)

**Severity:** MED

**Description:** ER Volume 2 Part 1 (General Requirements) listed in decomposition but not yet available in deliverable references.

**Impact:** Cannot validate assumptions against Employer standards; specifications, facility requirements, and quality standards are assumed rather than specified.

**Recommendation:** Obtain ER documents and update deliverable reference sections.

**Status:** UNRESOLVED (requires document procurement)

---

## 5. Completeness Scoring

### Overall Estimate Maturity

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| % of lines priced by QUOTE | 0% | >50% | ✗ |
| % priced by RATE_TABLE | 0% | >30% | ✗ |
| % priced by ALLOWANCE/PARAMETRIC | 100% | <20% | ✗ |
| % of deliverables with explicit quantities extracted | 0% | >70% | ✗ |
| % of deliverables covered (non-zero cost) | 100% | 100% | ✓ |
| Currency consistency | 100% | 100% | ✓ |
| Traceability (SourceRef populated) | 100% | 100% | ✓ |
| Required fields populated | 100% | 100% | ✓ |

**Overall Maturity Classification:** Class 5 (Conceptual) / Order of Magnitude

**Estimated Accuracy Range:** -30% / +50% (typical for Class 5 estimates per AACE guidelines)

**Suitability:**
- ✓ Suitable for: Conceptual budgeting, feasibility assessment, rough order of magnitude
- ✗ Not suitable for: Contracting, procurement, detailed project controls, financing commitments

---

## 6. Unknowns List (Top Assumptions by Value)

Ranked by base cost impact:

| Rank | Assumption ID | Description | Amount (CAD) | % of Base | Confidence |
|------|---------------|-------------|--------------|-----------|------------|
| 1 | A-012 | Site facilities & infrastructure | $850,000 | 59.3% | LOW |
| 2 | A-013 | Gate staffing operations | $180,000 | 12.6% | LOW |
| 3 | A-010 | Water supply installation | $45,000 | 3.1% | LOW |
| 4 | A-011 | Security gate installation | $75,000 | 5.2% | LOW |
| 5 | A-007 | Post-works road survey | $18,000 | 1.3% | LOW |
| 6 | A-006 | Pre-works road survey | $15,000 | 1.0% | LOW |
| 7 | A-001 | Drawing production | $12,000 | 0.8% | LOW |
| 8 | A-002 | Specification writing | $10,000 | 0.7% | LOW |
| 9 | A-009 | Water supply design | $10,000 | 0.7% | LOW |
| 10 | A-003 | Procedure development | $9,000 | 0.6% | LOW |

**Top 3 Unknowns (A-012, A-013, A-010) represent 75% of base cost.** Resolving these three assumptions would significantly improve estimate confidence.

---

## 7. QA Checks Summary Table

| QA Check | Requirement | Result | Status | Issues |
|----------|-------------|--------|--------|--------|
| Required fields populated | Qty, Unit, UnitRate, Amount on all lines | 18/18 lines pass | PASS | None |
| Currency consistency | All lines use same currency | CAD on 18/18 lines | PASS | None |
| Arithmetic reconciliation | Detail totals = Summary totals | $1,433,530 both | PASS | None |
| Deliverable coverage | All deliverables have cost lines | 8/8 covered | PASS | None |
| Double count check | No scope priced multiple times | No overlaps found | PASS | None |
| Traceability | SourceRef on all lines | 18/18 lines have SourceRef | PASS | All trace to assumptions (not quotes) |
| Quote-based pricing | >50% by quote | 0% by quote | FAIL | No vendor quotes available |
| Explicit quantities | >70% with QTO | 0% with QTO | FAIL | Physical quantities TBD in deliverables |
| Decision capture | Defaults and ambiguities logged | 9 decisions logged | PASS | All defaults documented |
| Assumption logging | Allowances documented | 13 assumptions logged | PASS | All allowances documented |

**Pass Rate:** 8/10 checks pass
**Critical Failures:** None (schema validation passed)
**Material Issues:** 2 (no quotes, no explicit quantities) — expected for draft estimate

---

## 8. Recommendations for Next Iteration

### Priority 1 (Critical — Improve Estimate Confidence)

1. **Obtain vendor budgetary quotes** for top 3 cost drivers:
   - A-012: Site facilities & infrastructure ($850k, 59% of base)
   - A-013: Gate staffing operations ($180k, 13% of base)
   - A-010: Water supply installation ($45k, 3% of base)

2. **Obtain Employer's Requirements** (Volume 2 Part 1) to extract:
   - Office trailer count and sizes
   - Laydown area dimensions
   - Security fencing linear footage and standards
   - Temporary utility capacities and service requirements

### Priority 2 (High — Refine Estimate Accuracy)

3. **Develop project-specific rate tables** for:
   - Engineering labor (CAD drafting, specification writing, design review)
   - Construction labor (installers, operators, laborers)
   - Equipment rental rates (common equipment types)

4. **Develop preliminary site layout** (DEL-00.01) to quantify:
   - Pipe routing distances for water supply
   - Fencing linear footage
   - Laydown area square footage
   - Traffic control zone boundaries

### Priority 3 (Medium — Add Schedule Basis)

5. **Obtain construction schedule** with:
   - Overall project duration (months)
   - Key milestone dates
   - Equipment mobilization/demobilization dates
   - Enable time-based indirects calculation

---

## 9. Run Status Determination

**Run Status:** WARNINGS

**Rationale:**

| Status Criteria | Assessment | Result |
|-----------------|------------|--------|
| Critical schema failures? | None — all required fields populated | ← No failure |
| Material assumptions/ambiguities? | Yes — 100% allowance-based, no vendor quotes | → WARNINGS |
| Missing inputs making totals non-meaningful? | Partial — deliverables exist but quantities TBD | ← Not FAILED |

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
- 0% of deliverables have explicit quantities from ER or project documents

**Recommended Use:**
- ✓ Conceptual budgeting and feasibility assessment
- ✓ Order of magnitude cost planning
- ✓ Identifying cost drivers for further investigation
- ✗ Contracting or procurement commitments
- ✗ Detailed project budget or cost baseline
- ✗ Financing or investment decisions without further validation

**Expected Accuracy Range:** -30% / +50% (Class 5 Order of Magnitude per AACE)

**Next Steps:** Obtain vendor quotes and ER to upgrade estimate to Class 4 (Factored) or Class 3 (Budget) maturity.

---

**QA Report Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Run Status:** WARNINGS
