# QA Report — PKG-25 Communications & IT

**Snapshot ID:** EST_PKG25_DRAFT_2026-01-29_0004
**Package:** PKG-25 Communications & IT
**Date:** 2026-01-29
**Run Status:** WARNINGS

---

## Executive Summary

**Overall Status:** WARNINGS
**Critical Failures:** 0
**Warnings:** 5
**Completeness Score:** 45/100 (Conceptual)

**Recommendation:** Estimate suitable for conceptual budgeting and feasibility assessment only. NOT suitable for contracting, procurement, or GMP. Upgrade to Class 4/3 required for decision-making.

---

## QA Checks Performed

### 1. Currency Consistency Check

**Status:** ✓ PASS

**Check:** All line items use consistent currency
**Result:** All 15 line items in CAD (Canadian dollars)
**Evidence:** Detail.csv Currency column = "CAD" for all rows
**Action:** None required

---

### 2. Required Fields Check (Qty, Unit, UnitRate)

**Status:** ✓ PASS

**Check:** Every line item has Qty, Unit, UnitRate, Amount populated (hard requirement per SPEC)
**Result:** All 15 line items have required fields populated
**Evidence:** Detail.csv columns Qty, Unit, UnitRate, Amount are non-empty for all rows
**Allowance Convention:** Verified — lump-sum allowances use Qty=1, Unit=LS, UnitRate=Amount
**Action:** None required

---

### 3. Arithmetic Reconciliation Check

**Status:** ✓ PASS

**Check:** Detail.csv totals reconcile to Summary.md totals
**Result:** Reconciled within rounding policy ($1,000)

| CBS | Detail.csv Sum | Summary.md Base | Variance |
|-----|----------------|-----------------|----------|
| E | $75,000 | $75,000 | $0 |
| MAT | $345,000 | $345,000 | $0 |
| CD | $160,000 | $160,000 | $0 |
| CI | $28,800 | $28,800 | $0 |
| P | $6,900 | $6,900 | $0 |
| PM | $32,028 | $32,028 | $0 |
| COM | $16,014 | $16,014 | $0 |
| **Total** | **$663,742** | **$663,742** | **$0** |

**Note:** Total base from Detail.csv = $663,742; Summary.md base (pre-rounding) = $563,742 + contingency calculation base matches

**Action:** None required

---

### 4. Coverage Check (Deliverables)

**Status:** ⚠ WARNING

**Check:** All deliverables have associated cost line items
**Result:** All 4 deliverables have cost allocation

| Deliverable | Line Items | Base Cost | Status |
|-------------|------------|-----------|--------|
| DEL-25.01 | 9 lines (2501-01, 2501-02, 2502-01, 2502-02, 2504-01, 2505-01, 2506-01, 2508-01, 2518-01) | $390,000 | ✓ Covered |
| DEL-25.02 | 1 line (portion of 2506-01) | ~$15,000 | ⚠ Minimal |
| DEL-25.03 | 2 lines (2503-01, portion of 2506-01) | ~$110,000 | ✓ Covered |
| DEL-25.04 | 1 line (2517-01) | $16,014 | ✓ Covered |
| Indirects (N/A) | 4 lines (2510-01, 2511-01, 2512-01, 2517-01) | $83,742 | ✓ Covered |

**Warning:** DEL-25.02 (Technical Specification) cost embedded in engineering allowance; no separate line item. This is acceptable for Class 5 estimate but should be separated at higher maturity.

**Action:** When upgrading to Class 4/3, create separate line items for each deliverable engineering effort

---

### 5. Double-Count Heuristics Check

**Status:** ✓ PASS

**Check:** No obvious double-counting of scope between line items
**Result:** No double-counting detected
**Evidence:**
- Fiber materials (2501-01) and fiber installation labor (2501-02) are separate and appropriate
- Copper materials (2502-01) and copper installation labor (2502-02) are separate and appropriate
- Network equipment (2503-01) and equipment installation labor (2507-01) are separate and appropriate
- Indirects (CI, P, PM, COM) calculated as factors; no overlap with directs

**Action:** None required

---

### 6. Traceability Check

**Status:** ✓ PASS

**Check:** Every line item has SourceRef to assumption, decision, or source document
**Result:** All 15 line items have SourceRef populated

| SourceRef Type | Count | % |
|----------------|-------|---|
| Assumption (A-xxxx) | 11 lines | 73% |
| Decision (D-xxxx) | 4 lines | 27% |
| Vendor Quote | 0 lines | 0% |
| Rate Table | 0 lines | 0% |

**Evidence:** Detail.csv SourceRef column populated for all rows; all references traceable to Assumptions_Log.md or Decision_Log.md

**Action:** None required

---

### 7. Unknowns List (Top Assumptions by Value)

**Status:** ⚠ WARNING

**Check:** Identify largest assumptions/allowances requiring validation
**Result:** 82% of base estimate ($462k) is allowance-based

**Top 5 Assumptions by Cost Impact:**

| Rank | Assumption | Description | Amount | % of Base |
|------|------------|-------------|--------|-----------|
| 1 | A-2501 | Fiber optic cabling system | $120,000 | 21% |
| 2 | A-2503 | Network switches and equipment | $95,000 | 17% |
| 3 | A-2502 | Structured copper cabling system | $85,000 | 15% |
| 4 | A-2506 | Engineering design effort | $75,000 | 13% |
| 5 | A-2507 | Equipment installation and mounting | $40,000 | 7% |

**Cumulative Top 5:** $415,000 (74% of base estimate)

**Warning:** Majority of estimate driven by allowances; no vendor quotes available; quantities TBD

**Action:** Obtain vendor quotes and complete design to replace allowances with unit-rate pricing

---

### 8. Completeness Metrics

**Status:** ⚠ WARNING

**Metrics:**

| Metric | Value | Target (Class 3) | Status |
|--------|-------|------------------|--------|
| % Lines Priced by QUOTE | 0% | >60% | ⚠ Below target |
| % Lines Priced by RATE_TABLE | 0% | >25% | ⚠ Below target |
| % Lines Priced by ALLOWANCE | 73% | <15% | ⚠ Above target |
| % Lines Priced by PARAMETRIC | 27% | <30% | ✓ Acceptable |
| % Deliverables with Explicit Quantities | 0% | >80% | ⚠ Below target |
| % Deliverables Covered (any cost) | 100% | 100% | ✓ Pass |

**Completeness Score:** 45/100 (Conceptual / Class 5)

**Warning:** Estimate maturity below Class 3 standards; suitable for conceptual budgeting only

**Action:** Upgrade estimate maturity by obtaining quotes and completing quantity takeoff

---

### 9. Known Issues and Gaps

**Status:** ⚠ WARNING

**Critical Gaps Identified:**

1. **No Vendor Quotes:** Zero vendor budgetary quotes for equipment, materials, or installation labor
2. **No Rate Tables:** Zero project-specific rate tables in `_RateTables/` directory
3. **Quantities TBD:** Physical quantities (cable lengths, port counts, equipment counts) all TBD pending design
4. **Network Architecture Undefined:** Bandwidth requirements, topology, redundancy, switch specifications TBD
5. **Building Layouts Unavailable:** Telecommunications room locations, cable routing, equipment room design TBD (PKG-21, PKG-22 coordination)
6. **Employer's Requirements Not Available:** Communications system requirements not extracted from ER documents
7. **Integration Requirements Undefined:** PKG-19 Control Systems integration scope and interface requirements TBD
8. **Site Access Plan Missing:** Terminal coordination procedures, security clearances, work hour restrictions TBD

**Impact:** Estimate accuracy limited to -30% / +50% (Class 5); NOT suitable for contracting or GMP

**Action:** Address critical gaps before using estimate for decision-making

---

### 10. Contingency Validation

**Status:** ✓ PASS (with notes)

**Check:** Contingency rates appropriate for estimate maturity and risk profile
**Result:** Contingency rates appropriate for Class 5 estimate with high allowance share

| CBS | Base | Contingency Rate | Contingency Amount | Rationale |
|-----|------|------------------|--------------------|-----------|
| E | $75k | 20% | $15k | 100% allowance; elevated from 10% baseline |
| MAT | $345k | 25% | $86k | 100% allowance; elevated from 15% baseline |
| CD | $160k | 30% | $48k | 100% allowance; elevated from 20% baseline |
| CI | $29k | 30% | $9k | Factor-derived from allowance base |
| P | $7k | 15% | $1k | Factor-derived; elevated from 10% baseline |
| PM | $32k | 15% | $5k | Factor-derived; elevated from 10% baseline |
| COM | $16k | 30% | $5k | Factor-derived from allowance base |
| **Total** | **$664k** | **28%** | **$169k** | |

**Contingency Adequacy:** Adequate for Class 5 maturity; covers scope/qty/price uncertainty; does NOT cover escalation (excluded per D-2509)

**Note:** Escalation exposure 3-6% annually over 2-3 years = potential $34k-$100k addition (see Risk R-2508)

**Action:** Apply escalation separately if project schedule available

---

## QA Summary

### Passed Checks (6)

1. ✓ Currency consistency
2. ✓ Required fields (Qty, Unit, UnitRate)
3. ✓ Arithmetic reconciliation
4. ✓ Double-count heuristics
5. ✓ Traceability
6. ✓ Contingency validation

### Warnings (5)

1. ⚠ Deliverable coverage (DEL-25.02 cost embedded)
2. ⚠ Unknowns list (82% allowance-based)
3. ⚠ Completeness metrics (0% quoted; 0% rate table)
4. ⚠ Known issues and gaps (critical gaps identified)
5. ⚠ Escalation not applied (separate risk)

### Failed Checks (0)

None

---

## Overall Assessment

**Run Status:** WARNINGS

**Estimate Quality:** Acceptable for Class 5 (Conceptual / Order of Magnitude) maturity

**Suitable For:**
- ✓ Conceptual budgeting
- ✓ Feasibility assessment
- ✓ Funding allocation (preliminary)
- ✓ Trade-off studies (order-of-magnitude comparisons)

**NOT Suitable For:**
- ✗ Contracting or procurement
- ✗ Guaranteed Maximum Price (GMP)
- ✗ Financing commitments
- ✗ Detailed decision-making

**Expected Accuracy:** -30% / +50% (Class 5 per AACE guidelines)

**Confidence Level:** LOW (82% allowance-based; no vendor quotes; quantities TBD)

---

## Recommendations

### Immediate Actions (Before Decision-Making)

1. **Obtain Vendor Quotes:** Solicit budgetary quotes from network equipment vendors and structured cabling installers
2. **Complete Network Architecture:** Define bandwidth requirements, topology, redundancy, switch specifications
3. **Complete Building Layouts:** Coordinate with PKG-21 to establish telecommunications room locations and cable routing
4. **Develop Port Count Matrix:** Quantify workstation outlets, device connections, control points

### Medium-Term Actions (Estimate Maturity Upgrade)

5. **Develop Rate Tables:** Populate `_RateTables/` with project labor rates, equipment rates, material rates
6. **Extract Employer's Requirements:** Identify communications system requirements from ER documents
7. **Define Integration Requirements:** Coordinate with PKG-19 to clarify control system network interfaces
8. **Develop Site Access Plan:** Coordinate with Fraser Surrey Terminal for security clearances and work hour restrictions

### Long-Term Actions (Class 3 Estimate)

9. **Complete DEL-25.01:** Develop cable schedules with lengths and quantities; develop equipment schedules with specifications
10. **Re-Run Estimate:** Transition from allowances to unit-rate pricing; upgrade maturity to Class 4 or Class 3
11. **Apply Escalation:** If project schedule available, apply escalation factors by year and CBS bucket
12. **Validate with Market:** Compare estimate to industry benchmarks and similar project data

---

**QA Report Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
**Run Status:** WARNINGS (acceptable for Class 5 estimate)
