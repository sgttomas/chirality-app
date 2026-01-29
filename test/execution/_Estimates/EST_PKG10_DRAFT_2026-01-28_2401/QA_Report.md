# QA Report

## Overview

This report documents quality checks performed on the estimate and identifies known issues requiring resolution.

---

## Currency Consistency Check

**Status:** ✓ PASS

**Check:** All line items use consistent currency (CAD).

**Result:** All 30 line items in Detail.csv use CAD currency. No currency mixing detected.

**Action Required:** None

---

## Qty/Unit/UnitRate Completeness Check

**Status:** ✓ PASS

**Check:** Every line item has non-empty Qty, Unit, UnitRate fields (hard requirement per SPEC).

**Result:** All 30 line items have populated Qty, Unit, UnitRate fields.

**Verification:**
- Line items L-001 through L-030: All have Qty, Unit, UnitRate present
- Allowance convention verified: All LS items have Qty=1, Unit=LS, UnitRate=Amount
- Multi-unit items have correct Qty × UnitRate = Amount arithmetic

**Action Required:** None

---

## Arithmetic Reconciliation Check

**Status:** ✓ PASS (within rounding policy)

**Check:** Summary.md totals match Detail.csv line item sums.

**Detail.csv Sums by CBS:**
- E: $55,000 + $18,000 + $28,000 + $22,000 + $12,000 = $135,000
- MAT: $1,600,000 + $96,000 + $280,000 + $256,000 + $48,000 + $80,000 + $65,000 + $85,000 + $45,000 = $2,555,000
- CD: $256,000 + $180,000 + $144,000 + $24,000 + $32,000 + $28,000 + $18,000 + $22,000 + $13,000 = $717,000
- CI: $129,000
- P: $51,000
- PM: $204,000
- COM: $58,000 + $28,000 + $22,000 + $14,000 = $122,000
- **Detail Total:** $3,913,000

**Summary.md Base Total:** $3,913,000

**Variance:** $0 (exact match)

**Action Required:** None

---

## Coverage Check (WBS Deliverables)

**Status:** ✓ PASS

**Check:** All deliverables have associated engineering cost lines.

**PKG-10 Deliverables:**

| Deliverable | Covered | Line Item(s) | Amount |
|-------------|---------|--------------|--------|
| DEL-10.01 Design Drawing Set | Yes | L-001 | $55,000 |
| DEL-10.02 Technical Specification | Yes | L-002 | $18,000 |
| DEL-10.03 Design Calculations | Yes | L-003 | $28,000 |
| DEL-10.04 Data Sheet Package | Yes | L-004 | $22,000 |
| DEL-10.05 Installation & Test Records | Yes | L-005 | $12,000 |

**Result:** All 5 deliverables have engineering cost coverage. Equipment/materials and installation/commissioning costs captured in system-level line items (not attributed to individual deliverables).

**Action Required:** None

---

## Double-Count Heuristics Check

**Status:** ✓ PASS (no double-counting detected)

**Check:** Verify no scope is priced in multiple line items.

**Potential Overlaps Reviewed:**
1. Unloading arms (L-006) vs Quick-connects (L-007): Separate items; couplers may be integral to arms (see A-002 for resolution)
2. Header piping supply (L-008) vs Valves/fittings (L-013): Distinct scopes; header piping is pipe material, valves/fittings are components
3. Containment pans (L-009) vs Collection system in sump pumps (L-010): Distinct scopes; pans are containment structure, pumps are drainage equipment
4. Flow indicators supply (L-011) vs installation labor (L-019): Supply vs installation; standard separation
5. CI/PM/P factors vs labor/material: Factors applied to base costs; standard methodology

**Result:** No double-counting detected. Potential overlap on quick-connects (may be integral to arms) noted in assumptions (A-002) for resolution when vendor data available.

**Action Required:** Verify quick-connect pricing when vendor quotes obtained (may eliminate L-007 if integral to arms, or adjust arm pricing).

---

## Unknowns List (Top Assumptions/Allowances by Value)

**Status:** ⚠ WARNINGS (high allowance share)

**Top 10 Allowances by Amount:**

| Rank | Line ID | Description | Amount | % of Base | Assumption Ref |
|------|---------|-------------|--------|-----------|----------------|
| 1 | L-006 | Railcar Unloading Arms - Supply (32 units) | $1,600,000 | 40.9% | A-001 |
| 2 | L-008 | Gravity Flow Header Piping - Supply | $280,000 | 7.2% | A-003 |
| 3 | L-009 | Spill Containment Pans - Supply (32 units) | $256,000 | 6.5% | A-004 |
| 4 | L-015 | Unloading Arm Installation - Labor (32 units) | $256,000 | 6.5% | A-015 |
| 5 | L-026 | Project Management / EPCM | $204,000 | 5.2% | D-008 factor |
| 6 | L-016 | Header Piping Installation - Labor | $180,000 | 4.6% | A-016 |
| 7 | L-017 | Containment Pan Installation - Labor | $144,000 | 3.7% | A-017 |
| 8 | L-024 | Construction Indirects | $129,000 | 3.3% | D-008 factor |
| 9 | L-007 | Quick-Connect Couplers - Supply (32 units) | $96,000 | 2.5% | A-002 |
| 10 | L-013 | Isolation Valves & Fittings | $85,000 | 2.2% | A-013 |

**Top 10 Subtotal:** $3,230,000 (82.5% of base estimate)

**Observation:** Top 4 allowances represent 61% of base estimate. Unloading arms alone are 41% of base. Estimate highly sensitive to arm pricing and header/containment configuration.

**Action Required:** **Priority** — Obtain vendor quotes for unloading arms (L-006) to reduce single largest uncertainty.

---

## Completeness Scoring

**Lines Priced by Method:**

| Method | Count | % of Lines | Base $ | % of Base |
|--------|-------|------------|--------|-----------|
| QUOTE | 0 | 0% | $0 | 0% |
| RATE_TABLE | 0 | 0% | $0 | 0% |
| ALLOWANCE | 27 | 90% | $3,546,000 | 90.6% |
| PARAMETRIC | 3 | 10% | $367,000 | 9.4% |
| **Total** | **30** | **100%** | **$3,913,000** | **100%** |

**Deliverables with Explicit Quantities:**

| Deliverable | Explicit Quantities? | Notes |
|-------------|---------------------|-------|
| DEL-10.01 | No | Drawing effort estimated; no detailed takeoff |
| DEL-10.02 | No | Specification effort estimated |
| DEL-10.03 | No | Calculation effort estimated |
| DEL-10.04 | Yes | 32 arm data sheets + 32 couplers + 8 pumps (quantity from decomposition) |
| DEL-10.05 | No | Records effort estimated |

**Explicit Quantity Score:** 20% (1 of 5 deliverables with quantities)

**Overall Completeness:** LOW (0% quote pricing, 0% rate table pricing, 20% explicit quantities)

---

## Mapping Ambiguities

**Status:** ⚠ WARNINGS (minor ambiguities logged)

**Ambiguous Mappings:**

1. **Quick-connect couplers (L-007):** May be integral to unloading arms (L-006) or separate procurement — TBD when vendor data available (Decision D-011, Assumption A-002)
   - **Resolution:** Verify with unloading arm vendors whether couplers are included in arm pricing or separate line items
   - **Impact:** If integral, eliminate L-007 and adjust L-006 pricing (no net change if assumption accurate)

2. **Flow indicators (L-011):** Specified in PKG-10 scope but may interface with PKG-20 Field Instrumentation for wiring and integration
   - **Resolution:** Clarify responsibility split: PKG-10 provides indicators (local devices), PKG-20 provides wiring/integration/controls
   - **Impact:** Minimal if standard responsibility split; if PKG-20 includes indicator supply, eliminate L-011 and reduce PKG-10 estimate

3. **Commissioning scope split:** Commissioning lines (L-027 through L-030) allocated to PKG-10; system-level commissioning may involve PKG-12 (metering), PKG-19 (controls), PKG-20 (instrumentation)
   - **Resolution:** Define commissioning scope boundaries in project commissioning plan or DEL-10.05
   - **Impact:** Minimal; integrated commissioning may shift some costs to PKG-30 Commissioning package

**Action Required:** Document interface responsibilities in ICDs (Interface Control Documents) and clarify equipment supply/integration splits.

---

## Known Issues

**Status:** ⚠ WARNINGS (significant gaps affecting confidence)

### Issue 1: No Vendor Quotes Available

**Description:** All equipment and materials priced via allowances; no vendor budgetary quotes obtained.

**Impact:** HIGH — entire material estimate ($2,555,000) is allowance-based with ±20-30% variance potential.

**Affected Lines:** L-006 through L-014 (all MAT lines)

**Recommendation:** **Priority action** — obtain budgetary quotes for major equipment items:
1. Railcar unloading arms (32 units) — TechnipFMC, OPW, Emco Wheaton
2. Quick-connect couplers (32 units)
3. Header piping materials (400 lm of 8-12 inch pipe)
4. Spill containment fabrication (32 pans or zone fabrication)
5. Sump pumps (8 units)

**Timeline:** Quotes should be obtained before detailed design (30% milestone) to refine estimate.

---

### Issue 2: No Rate Tables Available

**Description:** All labor costs priced via allowances; no project labor rate library available.

**Impact:** MEDIUM — labor estimate ($717,000 CD) has ±20% variance potential.

**Affected Lines:** L-015 through L-023 (all CD labor lines), plus factors (CI, PM, P derived from CD/MAT)

**Recommendation:** Populate `_RateTables/` with project labor rates:
1. Craft labor rates (fitters, welders, operators) by trade
2. Supervision and indirect labor rates
3. Equipment rental rates (cranes, welding machines, tools)
4. Productivity benchmarks (hours per unit by activity)

**Timeline:** Rate tables should be established during project mobilization (before construction).

---

### Issue 3: Interface Documents Not Available

**Description:** Interface coordination with PKG-07 (rail tracks), PKG-14 (downstream piping), PKG-17 (electrical), PKG-20 (instrumentation) not yet completed.

**Impact:** MEDIUM — interface mismatches could require rework ($50k-150k potential); may affect equipment sizing or layout.

**Affected Deliverables:** DEL-10.01 (layout coordination), DEL-10.02 (interface requirements), DEL-10.03 (sizing basis)

**Recommendation:**
1. Establish Interface Control Documents (ICDs) for critical interfaces
2. Conduct early IDC (Interdisciplinary Coordination) reviews
3. Freeze interface points before equipment procurement
4. Priority interfaces: PKG-07 track alignment, PKG-14 header discharge connection

**Timeline:** Interface coordination should occur during preliminary design (before 30% milestone).

---

### Issue 4: Deliverables in INITIALIZED State

**Description:** All PKG-10 deliverables are in INITIALIZED lifecycle state; detailed design not yet progressed.

**Impact:** HIGH — scope, quantities, and requirements not yet refined through engineering process.

**Affected Deliverables:** DEL-10.01 through DEL-10.05 (all)

**Recommendation:** Progress deliverables from INITIALIZED → IN_PROGRESS through WORKING_ITEMS sessions to refine scope and requirements. Engineering estimate may increase $10k-30k (8-22%) as design develops and complexity becomes clearer.

**Timeline:** Deliverable progression should follow project schedule (typically progress to IN_PROGRESS at project kickoff).

---

### Issue 5: Regulatory Requirements Not Verified

**Description:** Environmental regulations for spill containment not yet obtained; containment volume requirements assumed.

**Impact:** MEDIUM — regulatory requirements may mandate larger containment (+$50k-150k potential).

**Affected Deliverables:** DEL-10.03 (containment calculations), DEL-10.01 (containment details)

**Recommendation:** Obtain applicable regulations (Environment Canada Code of Practice for Storage Tank Systems, BC Spill Reporting Regulation, municipal regulations) and verify containment volume formula/criteria.

**Timeline:** Regulatory review should occur early in design phase (before 30% design freeze).

---

## QA Summary

**Checks Passed:** 3 of 3 hard requirements
- ✓ Currency consistency
- ✓ Qty/Unit/UnitRate completeness
- ✓ Arithmetic reconciliation

**Warnings:** 5 issues logged (all expected for INITIALIZED-state deliverables with no vendor quotes)

**Critical Issues:** None (estimate is valid but LOW confidence)

**Run Status:** WARNINGS (estimate is complete and internally consistent, but has significant uncertainties noted in assumptions/risks)

---

## Recommendations for Next Estimate Run

**To improve estimate confidence from LOW to MEDIUM:**
1. Obtain budgetary quotes for unloading arms (32 units) — reduces $1.6M uncertainty
2. Populate labor rate tables — improves CD estimate confidence
3. Progress DEL-10.03 calculations — verifies throughput capacity and sizing basis
4. Coordinate PKG-07 interface — confirms station spacing and layout assumptions

**To improve estimate confidence from MEDIUM to HIGH:**
5. Progress all deliverables to IN_PROGRESS state with refined scope
6. Obtain all vendor quotes (arms, couplers, pumps, indicators, valves)
7. Complete interface coordination (PKG-07, PKG-14, PKG-17, PKG-20)
8. Verify regulatory requirements and containment compliance
9. Develop detailed installation method statements with productivity data

**Expected estimate variance by maturity:**
- Current (INITIALIZED, 100% allowance): ±30-40% variance (LOW confidence)
- After quotes obtained (30% design): ±20-25% variance (MEDIUM confidence)
- After detailed design (60-90% design): ±10-15% variance (HIGH confidence)

---

## Estimate Maturity Assessment

| Aspect | Maturity Level | Evidence |
|--------|---------------|----------|
| Scope definition | INITIALIZED | Deliverables in INITIALIZED state per _STATUS.md |
| Quantities | LOW | Parametric/assumed quantities; no detailed takeoffs |
| Pricing | LOW | 100% allowance/parametric; no vendor quotes |
| Interface coordination | LOW | Interface documents not available |
| Regulatory compliance | LOW | Regulatory requirements not verified |
| **Overall Maturity** | **LOW** | **Placeholder estimate only** |

**Maturity Progression Path:**
- **Current:** INITIALIZED deliverables → parametric estimate (this snapshot)
- **30% Design:** IN_PROGRESS deliverables + vendor quotes → budget estimate
- **60% Design:** Detailed design + confirmed quotes → control estimate
- **90% Design:** Final design + firm quotes → bid estimate

**Current Use:** This estimate is suitable for conceptual budgeting and funding approval only. Not suitable for procurement commitments or detailed cost control.

---

*QA performed per AGENT_ESTIMATING SPEC requirements. All checks documented for audit trail.*
