# QA Report

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG12_DRAFT_2026-01-28_2341 |
| Estimate Label | PKG12_DRAFT |
| Package | PKG-12 Product Transfer & Metering |
| Date | 2026-01-28 |
| Run Status | WARNINGS |

---

## QA Checks Performed

### 1. Currency Consistency Check

**Status:** PASS

**Check:** All line items use consistent currency (CAD)

**Result:** 25 line items reviewed; all use CAD currency per config

**Reference:** Detail.csv column "Currency"; _CONFIG.md line 9

---

### 2. Required Fields Check (Qty / Unit / UnitRate)

**Status:** PASS

**Check:** Every Detail.csv line item has Qty, Unit, UnitRate populated (hard requirement per AGENT_ESTIMATING SPEC)

**Result:** All 25 line items have complete Qty, Unit, UnitRate fields

**Validation:**
- Engineering deliverables (L-001 through L-005): Qty=1, Unit=LS, UnitRate=Amount
- Equipment items (L-006 through L-015): Qty and Unit match item type; UnitRate populated
- Labor (L-016, L-017): Qty in MH, UnitRate per hour
- Factors/allowances (L-018 through L-025): Qty=1, Unit=LS, UnitRate=Amount

**Reference:** AGENT_ESTIMATING SPEC line 443-444; Detail.csv schema

---

### 3. Arithmetic Reconciliation Check

**Status:** PASS (within rounding tolerance)

**Check:** Detail.csv line item sum reconciles to Summary.md totals

**Detail.csv Sum by CBS:**

| CBS | Detail.csv Sum | Summary.md Base | Difference | Status |
|-----|---------------|-----------------|------------|--------|
| E | $138,000 | $138,000 | $0 | OK |
| MAT | $717,000 | $717,000 | $0 | OK |
| CD | $311,000 | $311,000 | $0 | OK |
| CI | $56,000 | $56,000 | $0 | OK |
| PM | $71,000 | $71,000 | $0 | OK |
| P | $13,000 | $13,000 | $0 | OK |
| COM | $120,000 | $120,000 | $0 | OK |
| **TOTAL** | **$1,426,000** | **$1,426,000** | **$0** | **OK** |

**Contingency Reconciliation:**

| CBS | Base | Contingency % | Calculated | Summary.md | Difference | Status |
|-----|------|---------------|------------|------------|------------|--------|
| E | $138k | 20% | $27,600 | $28,000 | $400 | OK (rounding) |
| MAT | $717k | 25% | $179,250 | $179,000 | -$250 | OK (rounding) |
| CD | $311k | 30% | $93,300 | $93,000 | -$300 | OK (rounding) |
| CI | $56k | 30% | $16,800 | $17,000 | $200 | OK (rounding) |
| PM | $71k | 15% | $10,650 | $11,000 | $350 | OK (rounding) |
| P | $13k | 15% | $1,950 | $2,000 | $50 | OK (rounding) |
| COM | $120k | 30% | $36,000 | $36,000 | $0 | OK |
| **TOTAL** | **$1,426k** | **25.7%** | **$365,550** | **$366,000** | **$450** | **OK** |

**Note:** Minor differences due to rounding to nearest $1,000 per config; within acceptable tolerance.

---

### 4. Coverage Check (Deliverables with Associated Costs)

**Status:** PASS

**Check:** All deliverables have associated cost line items; no deliverables are uncovered

**Coverage Map:**

| Deliverable | Line Items | Base Cost | Status |
|-------------|------------|-----------|--------|
| DEL-12.01 | L-001 | $28,000 | Covered |
| DEL-12.02 | L-002 | $38,000 | Covered |
| DEL-12.03 | L-003 | $42,000 | Covered |
| DEL-12.04 | L-004 | $18,000 | Covered |
| DEL-12.05 | L-005 | $12,000 | Covered |

**Equipment and Installation (N/A WBS):** 20 line items covering materials, construction, indirects, services, commissioning

**Result:** All 5 deliverables have cost coverage; equipment and installation scope captured in N/A (package-level) line items

---

### 5. Double Count Check

**Status:** PASS

**Check:** No scope element priced in multiple line items (no double counting)

**Review:**
- Engineering deliverables: Each deliverable has one E line item (L-001 through L-005); no overlap
- Flow meters: Two meters priced separately (L-006 rail, L-007 marine); no overlap
- Transmitters: Temperature (L-008) and pressure (L-009) separate; no overlap with flow meter integral instruments
- Structural: Metering skid structural (L-011) is metering-specific; general structural in PKG-06; no overlap
- Piping: Meter run piping (L-012) is metering-specific straight-runs; process piping in PKG-14; no overlap
- Installation labor: L-016 covers metering installation; general construction in other packages; no overlap
- Indirects: CI (L-019), P (L-020), PM (L-021) are PKG-12-specific factors; no double count with other packages
- Commissioning: FAT/SAT/proving (L-022 through L-025) are metering-specific; no overlap with general commissioning (PKG-35/36)

**Result:** No double counting identified; scope boundaries with adjacent packages (PKG-06, PKG-14, PKG-17, PKG-19, PKG-20) assumed per typical practice

**Warning:** Interface scope boundaries not formally coordinated (dependency mode NOT_TRACKED); scope overlaps or gaps possible; recommend interface coordination meeting

---

### 6. Unknowns List (Top Assumptions/Allowances by Value)

**Status:** 25 line items reviewed; top allowances identified

| Rank | LineID | Description | Amount | Method | Confidence | Issue |
|------|--------|-------------|--------|--------|------------|-------|
| 1 | L-016 | Metering System Installation Labor | $288,000 | ALLOWANCE | LOW | No labor rates or work breakdown; parametric manhour estimate |
| 2 | L-007 | Flow Meter - Marine Loading (10") | $230,000 | ALLOWANCE | LOW | No vendor quote; Coriolis technology assumed; size assumed |
| 3 | L-006 | Flow Meter - Rail Unloading (6") | $180,000 | ALLOWANCE | LOW | No vendor quote; Coriolis technology assumed; size assumed |
| 4 | L-010 | Portable Prover System | $120,000 | ALLOWANCE | LOW | Proving method not selected; portable assumed; no vendor quote |
| 5 | L-021 | Project Management / EPCM | $71,000 | PARAMETRIC | MED | Factor-based (6%); no project-specific PM plan or rates |
| 6 | L-019 | Construction Indirects | $56,000 | PARAMETRIC | MED | Factor-based (18%); no project schedule or site logistics plan |
| 7 | L-011 | Metering Skid Structural Steel | $55,000 | ALLOWANCE | LOW | Skid design not detailed; structural scope boundary with PKG-06 unclear |
| 8 | L-024 | Initial Proving (Commissioning) | $48,000 | ALLOWANCE | LOW | Proving scope not detailed; specialist costs assumed |
| 9 | L-003 | Metering Design Calculations | $42,000 | ALLOWANCE | LOW | Engineering effort not scoped; typical custody transfer calculation complexity assumed |
| 10 | L-002 | Metering Technical Specification | $38,000 | ALLOWANCE | LOW | Engineering effort not scoped; 30-50 page specification assumed |

**Top 10 Unknowns Total:** $1,128,000 (79% of base estimate)

**Implication:** Majority of estimate is driven by high-value allowances; vendor quotes and scope definition would significantly improve estimate confidence

---

### 7. Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Lines priced by QUOTE | 0 / 25 (0%) | >50% | FAIL |
| Lines priced by RATE_TABLE | 0 / 25 (0%) | >30% | FAIL |
| Lines priced by ALLOWANCE/PARAMETRIC | 25 / 25 (100%) | <50% | FAIL |
| Deliverables with explicit quantities | 0 / 5 (0%) | >70% | FAIL |
| Deliverables covered by cost lines | 5 / 5 (100%) | 100% | PASS |
| CBS buckets covered | 7 / 7 (100%) | 100% | PASS |

**Completeness Assessment:**

| Category | Rating | Notes |
|----------|--------|-------|
| Quantity Maturity | LOW | Equipment counts parametric; flow rates not specified; meter sizes assumed |
| Pricing Maturity | LOW | No vendor quotes; no rate tables; all allowances |
| Scope Definition | LOW | Deliverables in INITIALIZED state; technology and proving method not selected |
| Traceability | HIGH | All line items traceable to assumptions or decisions |
| Coverage | HIGH | All deliverables covered; all CBS buckets present |
| **Overall Maturity** | **LOW** | **Placeholder estimate only** |

---

### 8. Known Issues

#### Issue 1: No Vendor Quotes for Custody Transfer Equipment

**Severity:** HIGH

**Impact:** Flow meter costs ($410k, 29% of base) and proving equipment ($120k, 8% of base) are parametric; actual costs may vary ±30-50%

**Recommendation:** Obtain budgetary quotes from:
- Emerson (Micro Motion Coriolis)
- Endress+Hauser (Proline Promass Coriolis)
- Krohne (Optimass Coriolis)
- Portable prover suppliers (Actaris, Brooks, etc.)

**Cost Impact:** ±$160k-265k (±30-50% variance on $530k equipment allowances)

#### Issue 2: Meter Technology and Proving Method Not Selected

**Severity:** HIGH

**Impact:** Technology selection (Coriolis vs. alternatives) affects meter cost ±$100k-200k; proving method (portable vs. in-line) affects cost ±$200k-300k

**Recommendation:**
1. Progress DEL-12.02 specification to define meter technology and proving method
2. Perform technology trade study considering accuracy (OBJ-10), cost, product properties, pressure drop
3. Re-estimate after technology and proving method confirmed

**Cost Impact:** Combined swing ±$300k-500k depending on selections

#### Issue 3: Design Flow Rates Not Specified

**Severity:** MEDIUM

**Impact:** Meter sizes uncertain (6" rail, 10" marine assumed); actual sizes affect equipment cost ±$50k-100k and installation labor ±$20k-40k

**Recommendation:**
1. Obtain design flow rates from ER Vol 2 Part 2 or PKG-10/PKG-11
2. Perform meter sizing calculations in DEL-12.03
3. Update meter cost estimates with vendor quotes for confirmed sizes

**Cost Impact:** ±$70k-140k total

#### Issue 4: Metering Skid Structural Scope Boundary Unclear

**Severity:** MEDIUM

**Impact:** Structural steel allowance $55k may shift to PKG-06 or may be insufficient if complex skid design required

**Recommendation:**
1. Develop metering skid GA in DEL-12.01 with structural requirements
2. Coordinate with PKG-06: Who designs, details, and fabricates metering skid structure?
3. Clarify scope boundary and adjust estimate accordingly

**Cost Impact:** ±$30k-80k (could shift between PKG-12 and PKG-06)

#### Issue 5: No Project Labor Rates

**Severity:** MEDIUM

**Impact:** Installation labor ($311k CD, 22% of base) uses assumed $120/hr all-in rate; actual project labor rates may differ ±20-40%

**Recommendation:**
1. Obtain project labor rate table for BC lower mainland
2. Develop craft-specific rates (pipefitter, instrument tech, electrician, welder, rigger)
3. Refine labor estimate with project rates

**Cost Impact:** ±$60k-125k if labor rates differ from assumption

#### Issue 6: Interface Coordination Not Performed

**Severity:** LOW

**Impact:** Scope boundaries with PKG-06/14/17/19/20 assumed per typical practice; actual scope splits may differ

**Recommendation:**
1. Conduct interface coordination meeting for PKG-12 interfaces
2. Clarify scope boundaries: metering skid structure (PKG-06), meter run piping (PKG-14), power supply (PKG-17), flow computers/totalizers (PKG-19), transmitter installation (PKG-20)
3. Adjust estimate if scope shifts identified

**Cost Impact:** Scope shifts may move ±$50k-100k between packages (not a total cost impact, but affects PKG-12 estimate)

---

## Completeness Scoring

### Pricing Method Distribution

| Method | Line Count | Base $ | % of Base |
|--------|-----------|--------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| HISTORICAL | 0 | $0 | 0% |
| PARAMETRIC | 4 | $140,000 | 9.8% |
| ALLOWANCE | 21 | $1,286,000 | 90.2% |
| **TOTAL** | **25** | **$1,426,000** | **100%** |

**Analysis:**
- PARAMETRIC lines: CI, P, PM, COM base factor (L-019, L-020, L-021) = $140k
- ALLOWANCE lines: All engineering deliverables, all equipment, installation labor, commissioning activities = $1,286k
- 90% of base estimate is ALLOWANCE-based; indicates low pricing maturity

### Confidence Distribution

| Confidence | Line Count | Base $ | % of Base |
|------------|-----------|--------|-----------|
| LOW | 16 | $1,113,000 | 78.0% |
| MED | 9 | $313,000 | 22.0% |
| HIGH | 0 | $0 | 0% |
| **TOTAL** | **25** | **$1,426,000** | **100%** |

**Analysis:**
- LOW confidence lines (78%): All engineering deliverables, flow meters, prover, structural, installation labor, FAT/SAT/proving
- MED confidence lines (22%): Transmitters, piping, consumables, factors (CI, P, PM, COM)
- No HIGH confidence lines (no quotes or verified rates)

### Deliverable Coverage

| Deliverable | Engineering Cost | Equipment/Installation Cost | Total Attributed | Status |
|-------------|------------------|----------------------------|-----------------|--------|
| DEL-12.01 | $28,000 | — | $28,000 | Covered |
| DEL-12.02 | $38,000 | — | $38,000 | Covered |
| DEL-12.03 | $42,000 | — | $42,000 | Covered |
| DEL-12.04 | $18,000 | — | $18,000 | Covered |
| DEL-12.05 | $12,000 | — | $12,000 | Covered |
| PKG-12 Equipment/Installation | — | $1,288,000 | $1,288,000 | Covered |
| **TOTAL** | **$138,000** | **$1,288,000** | **$1,426,000** | **100% Coverage** |

**Result:** All deliverables have associated engineering costs; equipment and installation scope covered by package-level line items (N/A WBS)

---

## Estimate Maturity Assessment

### Maturity by Category

| Category | Maturity Level | Evidence | Score (0-10) |
|----------|---------------|----------|--------------|
| **Scope Definition** | LOW | Deliverables in INITIALIZED state; meter technology, proving method, flow rates TBD | 3/10 |
| **Quantity Basis** | LOW | Equipment counts parametric; meter sizes assumed; no flow rate specifications | 3/10 |
| **Pricing Basis** | LOW | No vendor quotes; no rate tables; all allowances | 2/10 |
| **Engineering Detail** | LOW | INITIALIZED deliverables provide limited detail; design not started | 3/10 |
| **Traceability** | HIGH | All line items traceable to assumptions/decisions; transparent basis | 9/10 |
| **Completeness** | HIGH | All deliverables covered; all CBS buckets present; full artifact set published | 9/10 |
| **Overall** | **LOW** | **Placeholder estimate; requires vendor quotes and scope definition** | **3/10** |

### Estimate Class (AACE Classification)

Based on maturity assessment:

| AACE Class | Typical Range | Expected Accuracy | PKG-12 Assessment |
|------------|---------------|-------------------|-------------------|
| Class 5 (Order of Magnitude) | -20% to -50% / +30% to +100% | ±50% | **Closest match** |
| Class 4 (Feasibility/Study) | -15% to -30% / +20% to +50% | ±30% | Not achieved (no quotes) |
| Class 3 (Budget/Authorization) | -10% to -20% / +10% to +30% | ±20% | Not achieved (scope immature) |

**Assessment:** This estimate is **Class 5 (Order of Magnitude)** suitable for early budgeting only.

**Recommendation:** Progress to Class 4 by obtaining vendor quotes and defining scope in DEL-12.02/12.03; progress to Class 3 by advancing deliverables to IN_PROGRESS with detailed design.

---

## Warnings and Recommendations

### Warnings

1. **CRITICAL:** 100% allowance-based pricing; no vendor quotes or rate tables available
2. **CRITICAL:** Meter technology and proving method not selected; affects cost ±$300k-500k (±21-35% of base)
3. **HIGH:** Design flow rates not specified; meter sizing uncertain; affects equipment cost and installation
4. **HIGH:** Deliverables in INITIALIZED state; scope definition incomplete
5. **MEDIUM:** No Measurement Canada requirements specified; regulatory compliance costs TBD
6. **MEDIUM:** Interface scope boundaries with PKG-06/14/17/19/20 not coordinated; potential overlaps or gaps
7. **MEDIUM:** Labor rates assumed ($120/hr); no project-specific rates available
8. **LOW:** Metering skid structural design not detailed; structural scope complexity uncertain

### Recommendations (Priority Order)

#### Priority 1 (Critical — Before Next Estimate)

1. **Obtain vendor budgetary quotes** for custody transfer flow meters (Coriolis, ultrasonic, or as specified)
2. **Obtain design flow rates** from ER Vol 2 Part 2 or PKG-10/PKG-11 hydraulics
3. **Confirm meter technology** in DEL-12.02 specification based on accuracy requirements and product properties
4. **Confirm proving method** in DEL-12.02 specification; obtain prover quotes

#### Priority 2 (High — Improve Estimate Confidence)

5. **Progress DEL-12.02 and DEL-12.03** to IN_PROGRESS to define scope, technology, proving method, and sizing
6. **Obtain project labor rate table** for BC lower mainland (pipefitter, instrument tech, electrician, etc.)
7. **Confirm Measurement Canada requirements** from ER Vol 2 Part 2 or regulatory research
8. **Develop metering skid structural design** in DEL-12.01; coordinate scope with PKG-06

#### Priority 3 (Medium — Refine Estimate)

9. **Coordinate interface scope boundaries** with PKG-06 (structural), PKG-14 (piping), PKG-17 (electrical), PKG-19 (controls/flow computers), PKG-20 (instrumentation)
10. **Confirm FAT/SAT/proving scope** in DEL-12.02 and ER requirements
11. **Obtain portable prover or in-line prover quotes**
12. **Develop detailed installation work breakdown** in Procedure.md to refine labor estimate

#### Priority 4 (Low — Further Refinement)

13. Progress all deliverables (DEL-12.01 through DEL-12.05) to IN_PROGRESS with detailed scope
14. Conduct site visit or obtain site logistics plan for productivity factor validation
15. Obtain transmitter and flow computer quotes
16. Develop metering system commissioning plan with detailed proving procedures

---

## Run Status Summary

**Status:** WARNINGS

**Reason:** Estimate is complete and internally consistent, but has material warnings requiring attention

**Warnings Summary:**
- No vendor quotes (all equipment allowances)
- Meter technology not selected (±$200k variance)
- Proving method not selected (±$300k variance)
- Flow rates not specified (sizing uncertain)
- Deliverables in INITIALIZED state (scope immature)

**Estimate Usability:**
- **Suitable for:** Early budgeting, order-of-magnitude planning, feasibility assessment
- **Not suitable for:** Authorization, procurement, contracting, detailed planning

**Next Steps:**
1. Obtain vendor quotes for flow meters and proving equipment
2. Confirm meter technology and proving method in DEL-12.02
3. Obtain design flow rates and perform sizing in DEL-12.03
4. Re-run estimate after critical inputs obtained (expect Class 4 maturity with vendor quotes)

---

*QA report prepared per AGENT_ESTIMATING SPEC requirements. Checks performed, issues identified, maturity assessed, recommendations provided.*
