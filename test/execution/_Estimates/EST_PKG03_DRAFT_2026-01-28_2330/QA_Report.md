# QA Report — PKG-03 Underground Utilities & Drainage Estimate

**Snapshot ID:** EST_PKG03_DRAFT_2026-01-28_2330
**Package Scope:** PKG-03 Underground Utilities & Drainage
**Date:** 2026-01-28
**Run Status:** WARNINGS

---

## QA Summary

Estimate passes all schema validation requirements but has material assumptions and quantity gaps that warrant WARNINGS status.

---

## 1. Schema Validation Checks

### 1.1 Required Fields — PASS

**Check:** All Detail.csv line items have Qty, Unit, UnitRate, Amount populated

**Result:** ✓ PASS

**Findings:**
- 18 line items in Detail.csv
- All lines have required fields populated
- Allowance convention followed (Qty=1, Unit=LS, UnitRate=Amount)

**Issues:** None

---

### 1.2 Currency Consistency — PASS

**Check:** All line items use CAD currency

**Result:** ✓ PASS

**Findings:** All 18 lines use CAD; no mixing detected

**Issues:** None

---

### 1.3 Arithmetic Reconciliation — PASS

**Check:** Detail.csv totals match Summary.md

**Result:** ✓ PASS

**Calculation Check:**
- E: $232,000 ✓
- PM: $103,000 ✓
- P: $11,400 ✓
- COM: $52,000 ✓
- MAT: $570,000 ✓
- CD: $975,000 ✓
- CI: $175,500 ✓
- **Total:** $2,118,900 ✓

**Issues:** None

---

### 1.4 Traceability — PASS

**Check:** All line items have SourceRef with assumption or decision ID

**Result:** ✓ PASS

**Findings:**
- All 18 lines have SourceRef populated
- 14 lines reference Assumptions_Log entries
- 4 lines reference Decision D-009 (parametric factors)
- All IDs valid and documented

**Issues:** None (all traceable to assumptions, not quotes)

---

## 2. Completeness Checks

### 2.1 Deliverable Coverage — PASS

**Check:** All 6 PKG-03 deliverables have associated costs

**Result:** ✓ PASS

**Findings:** All deliverables covered; no $0 deliverables

**Issues:** None

---

### 2.2 Pricing Method Composition — HIGH ALLOWANCE SHARE

**Check:** Distribution of pricing methods

**Result:** ✓ Expected for draft estimate

| Method | Lines | Base (CAD) | % of Base | Confidence |
|--------|-------|------------|-----------|------------|
| QUOTE | 0 | $0 | 0% | - |
| RATE_TABLE | 0 | $0 | 0% | - |
| ALLOWANCE | 14 | $1,647,000 | 77.7% | LOW |
| PARAMETRIC | 4 | $471,900 | 22.3% | MED |

**Issues:**
- **HIGH:** 77.7% allowance-based without vendor validation
- **HIGH:** 0% quote or rate table based

**Impact:** Very low confidence; conceptual budgeting only

---

### 2.3 Deliverable Document Completeness — PARTIAL

**Check:** 4-document sets present; quantities available

**Result:** ⚠ PARTIAL

**Findings:**
- All 6 deliverables have 4-doc sets ✓
- Physical quantities marked "TBD" ⚠
- No external references in `_REFERENCES.md` files ⚠

**Issues:**
- **HIGH:** Pipe lengths, sizes, counts TBD
- **HIGH:** OWS capacity TBD pending calculations
- **MED:** Duct bank quantities TBD pending PKG-17

**Impact:** Cannot create detailed QTO; forced to use high-level allowances

---

## 3. Consistency Checks

### 3.1 Double Count — PASS

**Check:** No scope priced multiple times

**Result:** ✓ PASS

**Findings:** No overlap detected between line items

**Issues:** None

---

### 3.2 WBS-CBS Mapping — CLEAR

**Check:** Deliverable-to-CBS mappings unambiguous

**Result:** ✓ PASS

**Findings:** WBS_CBS_Matrix.csv documents clear mapping logic

**Issues:** None

---

### 3.3 Indirects Calculation — PASS

**Check:** Factors applied correctly

**Result:** ✓ PASS

| Indirect | Factor | Base | Calculated | Verified |
|----------|--------|------|------------|----------|
| CI | 18% | CD=$975k | $175,500 | ✓ |
| P | 2% | MAT=$570k | $11,400 | ✓ |
| PM | 6% | CD+CI+MAT=$1720.5k | $103,230≈$103k | ✓ |
| COM | 3% | CD+CI+MAT=$1720.5k | $51,615≈$52k | ✓ |

**Issues:** None (minor rounding)

---

## 4. Known Issues

### Issue 1: No Vendor Quotes (CRITICAL)

**Severity:** CRITICAL

**Impact:** Estimate accuracy LOW; ±40-60% uncertainty

**Recommendation:** Obtain quotes for pipe, manholes, OWS, trenchless boring before contracting

**Status:** UNRESOLVED

---

### Issue 2: Physical Quantities TBD (HIGH)

**Severity:** HIGH

**Impact:** Cannot create volume-based estimates

**Recommendation:** Complete design (DEL-03.01, DEL-03.03) to quantify pipe runs, OWS sizing, duct banks

**Status:** UNRESOLVED

---

### Issue 3: Duct Bank Pending PKG-17 (MED)

**Severity:** MED

**Impact:** Duct bank allowance ($240k) may change ±30%

**Recommendation:** Coordinate with PKG-17 electrical; finalize conduit schedules

**Status:** UNRESOLVED

---

## 5. Completeness Scoring

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| % priced by QUOTE | 0% | >50% | ✗ |
| % priced by RATE_TABLE | 0% | >30% | ✗ |
| % priced by ALLOWANCE/PARAMETRIC | 100% | <20% | ✗ |
| % deliverables with explicit quantities | 0% | >70% | ✗ |
| % deliverables covered | 100% | 100% | ✓ |
| Currency consistency | 100% | 100% | ✓ |
| Traceability | 100% | 100% | ✓ |
| Required fields | 100% | 100% | ✓ |

**Maturity:** Class 5 (Conceptual)
**Accuracy Range:** -30% / +50%

**Suitable for:** Conceptual budgeting, feasibility, ROM
**Not suitable for:** Contracting, procurement, financing

---

## 6. Top Unknowns by Value

| Rank | Assumption | Amount (CAD) | % of Base |
|------|------------|--------------|-----------|
| 1 | A-001: Storm drainage network | $770,000 | 36.3% |
| 2 | A-005: Trenchless crossings | $265,000 | 12.5% |
| 3 | A-004: Duct bank network | $240,000 | 11.3% |
| 4 | A-003: OWS equipment & install | $230,000 | 10.9% |
| 5 | A-006: Engineering labor | $232,000 | 10.9% |

**Top 3 unknowns represent 60% of base** — resolving these would significantly improve confidence.

---

## 7. Recommendations for Next Iteration

**Priority 1 (Critical):**
1. Complete hydraulic calculations (DEL-03.03) to size pipes
2. Complete drainage layout (DEL-03.01) with pipe routing
3. Obtain vendor quotes for OWS, pipe materials, trenchless boring

**Priority 2 (High):**
4. Obtain geotechnical report for excavation planning
5. Coordinate with PKG-17 for duct bank requirements
6. Develop project rate tables for labor/equipment

---

## Run Status: WARNINGS

**Rationale:**
- No critical schema failures (all fields populated, arithmetic correct)
- Material assumptions create HIGH uncertainty (77.7% allowance-based)
- Physical quantities TBD but deliverables exist with scope definitions
- Estimate meaningful for conceptual budgeting but requires refinement for contracting

**Next Run Triggers:** Design quantities available, vendor quotes obtained, ER Volume 2 Part 2 extracted

---

**QA Report Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
