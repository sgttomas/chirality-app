# QA Report — PKG-22 Building Interior & MEP

**Snapshot ID:** EST_PKG22_DRAFT_2026-01-28_2358
**Package:** PKG-22 Building Interior & MEP
**Date:** 2026-01-28
**QA Status:** WARNINGS

---

## Executive Summary

| Metric | Status | Notes |
|--------|--------|-------|
| Run Status | WARNINGS | 100% allowance/parametric pricing; no vendor quotes; building size TBD |
| Currency Consistency | PASS | All line items in CAD |
| Qty/Unit/UnitRate Present | PASS | All 19 line items have Qty, Unit, UnitRate populated |
| Arithmetic Reconciliation | PASS | Detail.csv totals match Summary.md (within rounding) |
| Traceability | PASS | All line items reference assumptions or decisions |
| Coverage Check | PASS | All 6 deliverables mapped to CBS buckets |

**Overall Assessment:** Estimate suitable for conceptual budgeting only. Expected accuracy: Class 5 (-30% / +50%). Not suitable for contracting, procurement, or financing.

---

## QA Checks Performed

### 1. Currency Consistency

**Check:** Verify all line items use consistent currency

**Result:** PASS

**Details:**
- All 19 line items priced in CAD
- No currency conversions required
- Currency consistent with project location (Surrey, BC)

---

### 2. Qty / Unit / UnitRate Completeness (Hard Requirement)

**Check:** Verify every Detail.csv line has non-empty Qty, Unit, UnitRate fields

**Result:** PASS

**Details:**
- 19 line items checked
- All line items have Qty = 1 (LS allowances or factor-based)
- All line items have Unit = LS
- All line items have UnitRate = Amount (per allowance convention)
- **Compliance:** 100% (19/19 lines)

**Note:** LS (lump sum) allowances used due to lack of design quantities; this is correct per AGENT_ESTIMATING allowance convention (Qty=1, Unit=LS, UnitRate=Amount).

---

### 3. Arithmetic Reconciliation

**Check:** Verify Detail.csv line item amounts reconcile to Summary.md CBS totals

**Result:** PASS

**Detail.csv Totals by CBS:**
- E: L-001 through L-005 = 48+28+22+10+16 = $124,000
- MAT: L-006 through L-010 = 295+90+110+95+85 = $675,000
- CD: L-011 through L-015 = 195+125+115+105+92 = $632,000
- CI: L-016 = $114,000
- P: L-017 = $14,000
- PM: L-018 = $85,000
- COM: L-019 = $43,000

**Total Detail.csv:** $1,687,000

**Summary.md Base Total:** $1,687,000

**Variance:** $0 (perfect reconciliation)

---

### 4. Coverage Check (Deliverables vs Line Items)

**Check:** Verify all PKG-22 deliverables have associated cost line items or explicit coverage note

**Result:** PASS

| Deliverable ID | Name | CBS Coverage | Line Items |
|----------------|------|--------------|------------|
| DEL-22.01 | Building MEP Design Drawing Set | E, MAT, CD | L-001, L-006 through L-015 |
| DEL-22.02 | Building MEP Technical Specification | E | L-002 |
| DEL-22.03 | Building MEP Design Calculations | E | L-003 |
| DEL-22.04 | Building MEP Data Sheet Package | E | L-004 |
| DEL-22.05 | Building MEP Installation and Test Records | CI, COM | Included in L-016 (CI) and L-019 (COM) factors |
| DEL-22.06 | Building MEP Shop Design Drawing Set | E | L-005 |

**Coverage:** 100% (6/6 deliverables mapped to CBS buckets)

**No uncovered deliverables detected**

---

### 5. Double-Count Check

**Check:** Verify no scope priced in multiple places (potential double-counting)

**Result:** PASS (no double-counting detected)

**Scope Separation:**
- Engineering (E): Design deliverables only (drawings, specs, calcs, data sheets, shop review)
- Materials (MAT): Physical equipment and materials only (HVAC, plumbing, fire suppression, electrical, finishes)
- Construction Directs (CD): Installation labor and equipment only (HVAC install, plumbing install, fire install, electrical install, finishes install)
- Indirects/Services (CI, P, PM, COM): Factor-based buckets calculated from base; no overlap with directs

**No scope overlap identified between line items**

---

### 6. Traceability Check

**Check:** Verify all line items have source reference (quote, rate, assumption, decision)

**Result:** PASS

**Traceability Summary:**
- 19 line items total
- 15 lines reference Assumptions (A-001 through A-022)
- 4 lines reference Decisions (D-009)
- 0 lines missing source reference

**Traceability Compliance:** 100%

---

### 7. Completeness Metrics

#### Pricing Method Distribution

| Method | Line Items | Base $ Amount | % of Base |
|--------|------------|---------------|-----------|
| ALLOWANCE | 15 | $1,431,000 | 85% |
| PARAMETRIC (factors) | 4 | $256,000 | 15% |
| RATE_TABLE | 0 | $0 | 0% |
| QUOTE | 0 | $0 | 0% |
| **Total** | **19** | **$1,687,000** | **100%** |

**Assessment:** 100% allowance/parametric pricing; no vendor quotes or rate tables available

**Impact:** HIGH pricing uncertainty; elevated contingency required

---

#### Quantity Extraction Success

| Category | Success Rate | Details |
|----------|-------------|---------|
| Deliverable artifact counts | 100% | 6/6 deliverables enumerated |
| Physical equipment counts | 0% | All TBD (building size, load calculations, fixture schedules not available) |
| Material quantities (lengths, areas, volumes) | 0% | All TBD (no design drawings or layouts available) |
| Labor productivity | N/A | Typical productivity assumptions used (see A-012) |

**Assessment:** Quantities based on building size assumption (300 m²) and typical industrial MCC building practice

**Impact:** HIGH quantity uncertainty; building size variation directly affects MEP system sizes and costs

---

#### Deliverable Maturity

| Deliverable ID | Status (from _STATUS.md) | Quantities Available | Design Maturity |
|----------------|--------------------------|---------------------|-----------------|
| DEL-22.01 | INITIALIZED | No | 0% (placeholder) |
| DEL-22.02 | INITIALIZED | No | 0% (placeholder) |
| DEL-22.03 | INITIALIZED | No | 0% (placeholder) |
| DEL-22.04 | INITIALIZED | No | 0% (placeholder) |
| DEL-22.05 | INITIALIZED | No | 0% (placeholder) |
| DEL-22.06 | INITIALIZED | No | 0% (placeholder) |

**Average Maturity:** 0% (all deliverables in INITIALIZED state)

**Impact:** Estimate based entirely on assumptions and industry practice; no project-specific design available

---

### 8. Known Issues and Warnings

#### Critical Issues (Require Resolution Before Decision-Making)

1. **No building design from PKG-21**
   - Building floor area assumed (300 m²); actual size TBD
   - Impact: ±33% building size variation → ±25-35% MEP cost variation
   - Resolution: Complete PKG-21 DEL-21.01 building design drawings

2. **No vendor quotes available**
   - 100% allowance-based equipment pricing
   - Impact: ±20-40% equipment pricing uncertainty
   - Resolution: Obtain budgetary quotes for HVAC, fire suppression, plumbing equipment

3. **No HVAC load calculations**
   - HVAC capacity assumption (45-75 tons) not verified
   - Impact: Equipment may be undersized or oversized
   - Resolution: Complete DEL-22.03 HVAC load calculations

4. **No fire protection hydraulic calculations**
   - Sprinkler system design density and hydraulic demand assumed
   - Fire water supply adequacy not verified (PKG-23 coordination required)
   - Impact: Fire pump may be required (+$80k-$150k potential add)
   - Resolution: Complete DEL-22.03 hydraulic calculations; coordinate with PKG-23

---

#### Material Issues (Affect Accuracy but Estimate is Usable)

5. **Building occupancy classification TBD**
   - Assumed Group F Industrial per NBC 2020
   - Impact: Affects plumbing fixture requirements, fire suppression design, ventilation rates
   - Resolution: Confirm occupancy classification with Owner and AHJ

6. **Interior finishes scope interpretation**
   - Industrial-grade finishes assumed; actual finish levels TBD
   - Impact: ±20-30% finishes cost variation
   - Resolution: Complete building design with finish schedules

7. **Control system interface scope split (PKG-19/PKG-22) not defined**
   - HVAC equipment controls vs. BAS integration scope TBD
   - Impact: Potential scope gap or overlap
   - Resolution: Clarify control system scope with PKG-19 coordination

8. **Electrical power interface scope split (PKG-17/PKG-22) not defined**
   - Main power distribution vs. interior electrical scope TBD
   - Impact: Potential scope gap or overlap
   - Resolution: Clarify electrical scope with PKG-17 coordination

---

#### Advisory Issues (Do Not Materially Affect Estimate)

9. **Escalation not included**
   - January 2026 pricing; no escalation to future execution dates
   - Impact: $84k-$202k escalation exposure over 2-3 years (noted separately in Risk_Register.md)
   - Resolution: Note escalation risk for project budgeting; consider early procurement

10. **Employer's Requirements Volume 2 Part 3 (Building Works) not extracted**
    - Building-specific requirements TBD
    - Impact: Requirements assumptions may need updating
    - Resolution: Extract ER Volume 2 Part 3 when available

---

### 9. Allowance Quality Assessment

**Top Allowances by Value (High-Impact Assumptions):**

| Rank | Allowance | Base Amount | % of Base | Confidence | Issue if Wrong |
|------|-----------|-------------|-----------|------------|----------------|
| 1 | HVAC equipment and installation (L-006, L-011) | $490,000 | 29% | LOW | Equipment undersized/oversized; rework |
| 2 | Plumbing materials and installation (L-007, L-012) | $215,000 | 13% | LOW | Fixture count variation; hot water requirements TBD |
| 3 | Fire suppression materials and installation (L-008, L-013) | $225,000 | 13% | LOW | Fire pump may be required; AHJ requirements TBD |
| 4 | Interior electrical materials and installation (L-009, L-014) | $200,000 | 12% | LOW | Lighting/receptacle count variation; load TBD |
| 5 | Interior finishes materials and installation (L-010, L-015) | $177,000 | 10% | LOW | Finish levels and area TBD |

**Total Top 5 Allowances:** $1,307,000 (77% of base estimate)

**Assessment:** Estimate heavily dependent on building size assumption and MEP system capacity assumptions

---

### 10. Contingency Adequacy Check

**Contingency Rates Applied (PCT_BY_BUCKET with Allowance-Heavy Adjustment):**

| CBS | Base Amount | Allowance Share | Baseline Rate | Adjustment | Final Rate | Contingency |
|-----|-------------|-----------------|---------------|------------|------------|-------------|
| E | $124,000 | 100% | 10% | +10% | 20% | $25,000 |
| MAT | $675,000 | 100% | 15% | +10% | 25% | $169,000 |
| CD | $632,000 | 100% | 20% | +10% | 30% | $190,000 |
| CI | $114,000 | 100% (factor) | 20% | +10% | 30% | $34,000 |
| P | $14,000 | 100% (factor) | 10% | +5% | 15% | $2,000 |
| PM | $85,000 | 100% (factor) | 10% | +5% | 15% | $13,000 |
| COM | $43,000 | 100% (factor) | 25% | +5% | 30% | $13,000 |
| **Total** | **$1,687,000** | | | | **26.7%** | **$446,000** |

**Total Estimate (Base + Contingency):** $2,133,000 CAD

**Contingency Assessment:** Adequate for Class 5 estimate given 100% allowance pricing and high scope uncertainty

**Rationale:** Elevated contingency rates (20-30%) reflect:
- 100% allowance/parametric pricing (no quotes or rates)
- Building size assumption (±33% variation risk)
- No design quantities available (all deliverables INITIALIZED)
- Interface coordination risks (PKG-21, PKG-19, PKG-17, PKG-23)

---

## QA Summary

| Check | Status | Critical Issues | Material Issues | Advisory Issues |
|-------|--------|-----------------|-----------------|-----------------|
| Currency Consistency | PASS | 0 | 0 | 0 |
| Qty/Unit/UnitRate | PASS | 0 | 0 | 0 |
| Arithmetic | PASS | 0 | 0 | 0 |
| Coverage | PASS | 0 | 0 | 0 |
| Double-Count | PASS | 0 | 0 | 0 |
| Traceability | PASS | 0 | 0 | 0 |
| Completeness | WARNINGS | 4 | 4 | 2 |

**Total Issues:** 10 (4 critical, 4 material, 2 advisory)

**Run Status:** WARNINGS

**Recommended Actions Before Decision-Making:**
1. Complete PKG-21 building design to determine actual floor area
2. Obtain budgetary quotes for major MEP equipment (HVAC, fire suppression, plumbing)
3. Complete DEL-22.03 HVAC load calculations and fire protection hydraulic calculations
4. Clarify scope interfaces with PKG-17 (electrical), PKG-19 (controls), PKG-23 (fire protection)

---

**QA Report Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Snapshot:** EST_PKG22_DRAFT_2026-01-28_2358
**Status:** Complete
