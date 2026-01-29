# Risk Register — PKG-15 Pumps & Rotating Equipment Estimate

**Snapshot ID:** EST_PKG15_DRAFT_2026-01-28_2345
**Package:** PKG-15 Pumps & Rotating Equipment
**Date:** 2026-01-28

---

## Risk Summary

**Total Risks Identified:** 12
**HIGH Severity:** 3
**MEDIUM Severity:** 6
**LOW Severity:** 3

**Contingency Method:** PCT_BY_BUCKET with allowance-heavy adjustments
**Overall Contingency:** 23.9% of base cost ($373,000 on $1,559,000 base)

---

## Risk Entries

### R-001: Pump Quantity Uncertainty (HIGH)
**ID:** R-001
**Risk Driver:** Scope / Quantity
**Severity:** HIGH

**Cause:** All deliverable documents list pump quantities as "TBD" pending DEL-15.03 calculations and ER Part 2 specifications.

**Consequence:** Estimated 14 pump units may be under or over actual requirements by 25-30%.

**Affected Buckets:**
- CBS: Materials (MAT), Construction Directs (CD), Commissioning (COM)
- WBS: All PKG-15 deliverables

**Cost Impact:**
- Base estimate assumes 14 pumps
- If actual is 10 pumps: -$300,000 (-15%)
- If actual is 18 pumps: +$350,000 (+18%)

**Probability:** HIGH (quantities definitely TBD)
**Impact Magnitude:** $300,000 to $350,000 swing

**Suggested Mitigation:**
1. Prioritize completion of DEL-15.03 (Pump Design Calculations)
2. Review ER Part 2 for pump quantity requirements
3. Coordinate with PKG-10 (Railcar), PKG-11 (Marine), PKG-13 (Tanks) for system requirements
4. Update estimate immediately after quantities confirmed

**Contingency Handling:** Covered by 25% Materials contingency and 30% CD contingency (allowance-heavy buckets)

**Related Assumptions:** A-001
**Related Decisions:** D-005

---

### R-002: Equipment Pricing Uncertainty (HIGH)
**ID:** R-002
**Risk Driver:** Price / Quote
**Severity:** HIGH

**Cause:** No vendor quotes or budgetary pricing available; all equipment costs parametrically estimated.

**Consequence:** API 610 pump costs can vary significantly based on materials, features, vendor, and market conditions.

**Affected Buckets:**
- CBS: Materials (MAT)
- WBS: All pump equipment

**Cost Impact:**
- Estimated pump equipment: $712,000
- API 610 pumps can vary -30% to +50% from parametric estimates
- Low case: $498,400 (-30%)
- High case: $1,068,000 (+50%)
- **Potential swing:** $570,000

**Probability:** MEDIUM-HIGH (no quotes means pricing uncertainty)
**Impact Magnitude:** Up to $570,000

**Suggested Mitigation:**
1. Solicit budgetary quotes from API 610 pump vendors as soon as DEL-15.02 specifications available
2. Consider pre-qualification of vendors to assess pricing competitiveness
3. Explore alternative pump specifications (commercial vs. API 610) if budget constrained
4. Lock in vendor quotes early to minimize pricing volatility

**Contingency Handling:** 25% Materials contingency provides $178,300 buffer; may not fully cover high case.

**Related Assumptions:** A-002, A-011, A-012
**Related Decisions:** D-007, D-008

---

### R-003: Motor and VFD Requirements Uncertainty (MEDIUM)
**ID:** R-003
**Risk Driver:** Scope / Interface
**Severity:** MEDIUM

**Cause:** Motor specifications and VFD requirements TBD pending electrical coordination (PKG-17/19) and operational requirements.

**Consequence:**
- Motor power ratings may differ from estimated 406 kW total
- VFD coverage may be 0-100% of pumps (estimated 50%)
- Motor features may require premium (explosion-proof, special enclosures)

**Affected Buckets:**
- CBS: Materials (MAT), Electrical (EI if separated)
- WBS: DEL-15.04 (motor data sheets)

**Cost Impact:**
- Base estimate: $203,000 motors + $60,900 VFDs = $263,900
- If VFDs required on all pumps: +$60,900
- If explosion-proof motors required: +$50,000 to $100,000
- **Potential swing:** -$60,900 to +$160,900

**Probability:** MEDIUM
**Impact Magnitude:** $60,900 to $160,900

**Suggested Mitigation:**
1. Coordinate with PKG-17/19 (Electrical) for motor specifications and VFD strategy
2. Review hazardous area classification study for explosion-proof requirements
3. Define VFD requirements per operational flexibility (OBJ-4) and energy efficiency (OBJ-9)
4. Obtain motor vendor quotes with options (standard / explosion-proof / VFD)

**Contingency Handling:** 25% Materials contingency provides buffer.

**Related Assumptions:** A-004
**Related Decisions:** D-006

---

### R-004: Installation Productivity Variance (MEDIUM)
**ID:** R-004
**Risk Driver:** Productivity / Site Conditions
**Severity:** MEDIUM

**Cause:** No project-specific productivity data; site access and rigging constraints unknown.

**Consequence:** Installation manhours may vary ±20% from estimated 568 manhours (40 hr/pump average).

**Affected Buckets:**
- CBS: Construction Directs (CD), Construction Indirects (CI)
- WBS: DEL-15.01 (installation design), DEL-15.05 (installation records)

**Cost Impact:**
- Base estimate: 568 manhours @ $95/hr = $54,040
- Low productivity (more hours): +$10,808 (+20%)
- High productivity (fewer hours): -$10,808 (-20%)

**Probability:** MEDIUM
**Impact Magnitude:** ±$10,800

**Suggested Mitigation:**
1. Conduct site visit to assess access, rigging points, laydown areas
2. Coordinate with PKG-00 (Site Establishment) for crane availability and temporary facilities
3. Review DEL-15.01 for pump locations and installation constraints
4. Obtain historical productivity data from similar installations at Fraser Surrey Terminal

**Contingency Handling:** 30% CD contingency and 20% CI contingency provide buffer.

**Related Assumptions:** A-003
**Related Decisions:** D-014

---

### R-005: Seal System Complexity (MEDIUM)
**ID:** R-005
**Risk Driver:** Scope / Technical
**Severity:** MEDIUM

**Cause:** Seal specifications TBD per DEL-15.02; single vs. dual seals, API 682 piping plans not finalized.

**Consequence:**
- Simple single seals (API 682 Plan 11): -$42,500 (-33%)
- Dual seals with barrier fluid (API 682 Plan 53/54): +$85,000 (+67%)

**Affected Buckets:**
- CBS: Materials (MAT)
- WBS: DEL-15.02 (seal specification), DEL-15.04 (seal data)

**Cost Impact:**
- Base estimate: $127,500 (15% of pump cost)
- Range: $85,000 to $212,500
- **Potential swing:** $127,500

**Probability:** MEDIUM
**Impact Magnitude:** -$42,500 to +$85,000

**Suggested Mitigation:**
1. Define seal requirements early based on environmental protection requirements (OBJ-7)
2. Consider dual seals for critical pumps (marine loading, large transfer) and single seals for sump pumps
3. Coordinate seal support systems with PKG-14 (Process Piping) for flush/barrier fluid piping
4. Review ER Part 2 for seal system requirements

**Contingency Handling:** 25% Materials contingency partially covers; high case may exceed contingency.

**Related Assumptions:** A-011
**Related Decisions:** D-008

---

### R-006: Canola Oil Fluid Properties and Heating Requirements (MEDIUM)
**ID:** R-006
**Risk Driver:** Scope / Interface
**Severity:** MEDIUM

**Cause:** Canola oil properties assumed (SG 0.91, viscosity 50 cP @ 20°C); operating temperature range TBD.

**Consequence:**
- If winter heating required for viscosity reduction, additional heat trace or tank heating systems needed
- Higher viscosity → larger motors, more power consumption
- Lower temperature operation → potential for solidification or high viscosity pumping issues

**Affected Buckets:**
- CBS: Materials (MAT) for heating systems (if required), Engineering (E) for heating design
- WBS: Interfaces to PKG-13 (tank heating), PKG-14 (heat trace piping)

**Cost Impact:**
- Base estimate assumes no heating required in PKG-15
- If heat trace required on pump suction piping: +$25,000 to $50,000
- If higher motor power required: +$15,000 to $30,000
- **Potential addition:** $40,000 to $80,000

**Probability:** MEDIUM (BC winter temperatures can drop to -10°C)
**Impact Magnitude:** $40,000 to $80,000

**Suggested Mitigation:**
1. Review ER Part 2 for canola oil properties and operating temperature requirements
2. Coordinate with PKG-13 (Storage Tanks) for product heating strategy
3. Confirm lowest ambient temperature for pump operation
4. Include heat trace allowance in PKG-14 if required

**Contingency Handling:** 25% MAT contingency provides partial buffer.

**Related Assumptions:** A-005
**Related Decisions:** D-008

---

### R-007: Engineering Scope Creep or Coordination Effort (MEDIUM)
**ID:** R-007
**Risk Driver:** Scope / Coordination
**Severity:** MEDIUM

**Cause:** Engineering hours estimated parametrically; actual hours depend on design iterations, ER requirements, coordination complexity.

**Consequence:**
- If pump specifications require multiple vendor iterations: +20-30% engineering hours
- If foundation interface or piping nozzle loads require extensive coordination: +15-25% hours
- If ER Part 2 has stringent requirements requiring additional calculations: +10-20% hours

**Affected Buckets:**
- CBS: Engineering (E)
- WBS: All PKG-15 deliverables

**Cost Impact:**
- Base estimate: $99,840 (480 hours)
- Potential increase: +$20,000 to $30,000 (+20-30%)

**Probability:** MEDIUM
**Impact Magnitude:** $20,000 to $30,000

**Suggested Mitigation:**
1. Review ER Part 2 early to identify complex requirements
2. Establish clear scope boundaries with PKG-05 (foundations), PKG-14 (piping), PKG-17/19 (electrical)
3. Use vendor engineering support where possible (pump vendor provides some calculations)
4. Track engineering hours by deliverable and adjust estimate if trending high

**Contingency Handling:** 20% Engineering contingency provides $19,968 buffer; may not fully cover high case.

**Related Assumptions:** A-010
**Related Decisions:** D-009

---

### R-008: Commissioning Complexity and Schedule (MEDIUM)
**ID:** R-008
**Risk Driver:** Schedule / Technical
**Severity:** MEDIUM

**Cause:** Commissioning scope defined conceptually in DEL-15.05 but detailed test procedures and acceptance criteria TBD.

**Consequence:**
- If performance testing requires multiple attempts or troubleshooting: +30-50% commissioning hours
- If vendor support required on-site: +$15,000 to $30,000 travel and per diem
- If testing schedule compressed: +$10,000 to $20,000 overtime/acceleration

**Affected Buckets:**
- CBS: Commissioning (COM)
- WBS: DEL-15.05

**Cost Impact:**
- Base estimate: $29,280
- Potential increase: +$25,000 to $50,000 (+85% to +170%)

**Probability:** LOW-MEDIUM
**Impact Magnitude:** $25,000 to $50,000

**Suggested Mitigation:**
1. Develop detailed commissioning plan in DEL-15.05 with test procedures and hours
2. Negotiate vendor commissioning support scope and pricing at procurement
3. Include vendor startup supervision in equipment purchase
4. Coordinate commissioning schedule with PKG-29/30 (controls) and PKG-31 (startup)

**Contingency Handling:** 25% Commissioning contingency ($7,320) may be insufficient for high case.

**Related Assumptions:** A-009
**Related Decisions:** D-015

---

### R-009: Labor Rate Escalation (MEDIUM)
**ID:** R-009
**Risk Driver:** Price / Schedule
**Severity:** MEDIUM

**Cause:** Estimate in January 2026 dollars; installation may occur 12-24 months in future.

**Consequence:** BC industrial labor rates may escalate 3-5% per year.

**Affected Buckets:**
- CBS: Construction Directs (CD), Construction Indirects (CI), Commissioning (COM)
- WBS: All installation and commissioning work

**Cost Impact:**
- Labor content in base estimate: $92,880 (CD + COM labor)
- 12 months escalation @ 4%: +$3,715
- 24 months escalation @ 4% per year: +$7,590
- **Potential addition:** $3,700 to $7,600

**Probability:** HIGH (labor rates typically escalate)
**Impact Magnitude:** $3,700 to $7,600

**Suggested Mitigation:**
1. Update pricing date when installation timeline confirmed
2. Include escalation provision in contracts
3. Monitor BC labor market trends and union agreements
4. Consider labor cost escalation allowance if installation >18 months out

**Contingency Handling:** Current contingency does not include escalation (escalation_mode = NONE per D-013); may need explicit escalation provision.

**Related Decisions:** D-013

---

### R-010: Currency Exchange Rate Fluctuation (LOW)
**ID:** R-010
**Risk Driver:** Price / Market
**Severity:** LOW

**Cause:** Equipment vendors may quote in USD; conversion to CAD estimate currency required.

**Consequence:** CAD/USD exchange rate fluctuations could affect imported equipment costs.

**Affected Buckets:**
- CBS: Materials (MAT)
- WBS: All imported equipment

**Cost Impact:**
- If 50% of equipment imported and priced in USD: $636,700 exposed to FX
- CAD/USD rate variation ±5%: ±$31,835

**Probability:** MEDIUM (exchange rates fluctuate)
**Impact Magnitude:** ±$32,000

**Suggested Mitigation:**
1. Confirm vendor quote currencies
2. Lock in exchange rates with forward contracts if material exposure
3. Price in CAD where possible (Canadian vendors or fixed CAD pricing)
4. Include FX allowance if significant USD exposure

**Contingency Handling:** 25% MAT contingency provides buffer.

---

### R-011: API 610 Compliance Requirement Interpretation (MEDIUM)
**ID:** R-011
**Risk Driver:** Scope / Technical
**Severity:** MEDIUM

**Cause:** DEL-15.02 specifies API 610 for process pumps; unclear if all pumps (including sump pumps) require API 610 compliance.

**Consequence:**
- If all pumps must be API 610: estimate is reasonable
- If only process pumps (not sump pumps) require API 610: potential -$30,000 to -$40,000 savings (commercial sump pumps)
- If API 610 interpretation is more stringent than assumed: +$50,000 to $100,000 (premium features)

**Affected Buckets:**
- CBS: Materials (MAT)
- WBS: DEL-15.02 (specification)

**Cost Impact:**
- Current estimate: All pumps API 610 grade
- Alternative: Commercial sump pumps save $30,000-$40,000
- Risk: Premium API 610 features add $50,000-$100,000

**Probability:** LOW-MEDIUM
**Impact Magnitude:** -$40,000 to +$100,000

**Suggested Mitigation:**
1. Review ER Part 2 for pump standards requirements (which pumps require API 610?)
2. Clarify with Employer if sump/drainage pumps can be commercial-grade
3. Consider tiered specification (API 610 for critical process, commercial for auxiliary)
4. Obtain quotes for both API 610 and commercial-grade pumps for comparison

**Contingency Handling:** 25% MAT contingency provides buffer for upside risk.

**Related Decisions:** D-007

---

### R-012: Coordination and Interface Delays (LOW)
**ID:** R-012
**Risk Driver:** Schedule / Interface
**Severity:** LOW

**Cause:** PKG-15 interfaces with multiple packages (PKG-05 foundations, PKG-14 piping, PKG-17/19 electrical, PKG-29/30 controls).

**Consequence:**
- Design iteration loops if interfaces not coordinated early
- Potential rework if foundation loads or piping nozzle loads change
- Engineering hours increase if coordination is inefficient

**Affected Buckets:**
- CBS: Engineering (E)
- WBS: All PKG-15 deliverables

**Cost Impact:**
- Base estimate includes coordination time
- If significant rework: +$10,000 to $20,000 engineering hours

**Probability:** LOW (standard EPC coordination process)
**Impact Magnitude:** $10,000 to $20,000

**Suggested Mitigation:**
1. Establish Interface Definition Clearance (IDC) process early
2. Coordinate foundation loads with PKG-05 during DEL-15.01 development
3. Coordinate motor specs with PKG-17/19 during DEL-15.02 development
4. Use vendor engineering support to minimize Contractor coordination burden

**Contingency Handling:** 20% Engineering contingency provides buffer.

---

### R-013: Food-Grade Material Requirements (MEDIUM)
**ID:** R-013
**Risk Driver:** Scope / Regulatory
**Severity:** MEDIUM

**Cause:** Canola oil is food-grade product; material compatibility requirements may be more stringent than assumed.

**Consequence:**
- If food-grade certification required (FDA, USDA): potential premium for certified materials
- If 316SS required for all wetted parts (not just impeller): +$50,000 to $100,000
- If special cleaning/passivation required: +$5,000 to $10,000

**Affected Buckets:**
- CBS: Materials (MAT), Construction Directs (CD)
- WBS: DEL-15.02 (materials specification)

**Cost Impact:**
- Current estimate assumes 316SS wetted parts, cast iron/CS casings (food-compatible)
- If full 316SS construction required: +$50,000 to $100,000
- If certifications and cleaning required: +$5,000 to $10,000
- **Potential addition:** $55,000 to $110,000

**Probability:** LOW-MEDIUM
**Impact Magnitude:** $55,000 to $110,000

**Suggested Mitigation:**
1. Review ER Part 2 for food-grade material requirements
2. Coordinate with Employer/end customer on food-grade certification requirements
3. Confirm material requirements early in DEL-15.02 development
4. Obtain quotes for both standard and full-stainless construction

**Contingency Handling:** 25% MAT contingency provides $318,350 buffer; sufficient for this risk.

**Related Assumptions:** A-005
**Related Decisions:** D-008

---

### R-014: Spare Parts Strategy Unknown (LOW)
**ID:** R-014
**Risk Driver:** Scope
**Severity:** LOW

**Cause:** Spare parts requirements TBD per ER and operations philosophy (OBJ-9 lifecycle cost optimization).

**Consequence:**
- Minimal spares (run-to-failure): -$40,000 (-59%)
- Comprehensive spares (critical + insurance spares): +$60,000 (+88%)

**Affected Buckets:**
- CBS: Materials (MAT)
- WBS: All pump equipment

**Cost Impact:**
- Base estimate: $68,000 (8% of pump cost)
- Range: $28,000 (minimal) to $128,000 (comprehensive)
- **Potential swing:** -$40,000 to +$60,000

**Probability:** MEDIUM (spares strategy not defined)
**Impact Magnitude:** -$40,000 to +$60,000

**Suggested Mitigation:**
1. Define spare parts philosophy per ER requirements and OBJ-9
2. Coordinate with operations and maintenance team
3. Obtain vendor-recommended spare parts lists with pricing
4. Consider vendor consignment inventory or rapid-supply agreements

**Contingency Handling:** 25% MAT contingency provides buffer for upside.

**Related Assumptions:** A-013

---

### R-015: Vendor Lead Times and Schedule Impact (LOW)
**ID:** R-015
**Risk Driver:** Schedule
**Severity:** LOW

**Cause:** API 610 pump lead times typically 16-24 weeks; critical path risk if not ordered early.

**Consequence:**
- If expedited delivery required: +$20,000 to $50,000 premium
- If delayed delivery impacts schedule: indirect costs for schedule extension

**Affected Buckets:**
- CBS: Materials (MAT), PM (schedule impact)
- WBS: Procurement and installation

**Cost Impact:**
- Base estimate assumes normal lead times
- Expedite premium: +$20,000 to $50,000 (3-7% of equipment cost)

**Probability:** LOW (standard EPC procurement planning)
**Impact Magnitude:** $20,000 to $50,000

**Suggested Mitigation:**
1. Finalize pump specifications (DEL-15.02) early to enable procurement
2. Issue RFQ and place orders as soon as specifications approved
3. Track vendor lead times and expedite if critical path risk emerges
4. Consider long-lead-item procurement strategy

**Contingency Handling:** 25% MAT contingency provides buffer; schedule contingency not quantified.

---

### R-016: Freight and Logistics Costs (LOW)
**ID:** R-016
**Risk Driver:** Price
**Severity:** LOW

**Cause:** Freight costs not separately estimated; assumed included in equipment prices or minimal.

**Consequence:**
- Large pumps may require specialized transport/rigging
- Import duties if non-North American vendors selected
- Laydown and storage costs at site

**Affected Buckets:**
- CBS: Freight (FRT) if separated, or Materials (MAT)
- WBS: All equipment

**Cost Impact:**
- If freight separated at 5-8% of equipment FOB: +$40,000 to $70,000
- Current estimate assumes freight included in equipment unit costs

**Probability:** MEDIUM (freight typically separate line item)
**Impact Magnitude:** $40,000 to $70,000 if not included

**Suggested Mitigation:**
1. Clarify freight responsibility (vendor FOB or delivered to site)
2. Include explicit freight allowance if vendor quotes are FOB
3. Coordinate with site logistics plan (PKG-00)

**Contingency Handling:** 25% MAT contingency or separate freight line if material gap identified.

---

### R-017: Temporary Power and Utilities for Commissioning (LOW)
**ID:** R-017
**Risk Driver:** Scope
**Severity:** LOW

**Cause:** Temporary power for pump commissioning not explicitly estimated.

**Consequence:**
- Generator rental or temporary power connection required for testing: +$5,000 to $10,000

**Affected Buckets:**
- CBS: Commissioning (COM) or Construction Indirects (CI)
- WBS: DEL-15.05 commissioning

**Cost Impact:** +$5,000 to $10,000 if not covered by PKG-00 (Site Establishment)

**Probability:** LOW (likely covered in PKG-00 or CI)
**Impact Magnitude:** $5,000 to $10,000

**Suggested Mitigation:**
1. Coordinate with PKG-00 for temporary power availability during commissioning phase
2. Include in commissioning plan (DEL-15.05)

**Contingency Handling:** 25% COM contingency or 20% CI contingency covers.

---

### R-018: Quality Control and Inspection Effort (LOW)
**ID:** R-018
**Risk Driver:** Scope / Quality
**Severity:** LOW

**Cause:** QA/QC inspection requirements not explicitly quantified.

**Consequence:**
- If ER requires extensive hold points, inspection, or third-party verification: +$8,000 to $15,000

**Affected Buckets:**
- CBS: Construction Indirects (CI)
- WBS: DEL-15.05 (installation and test records)

**Cost Impact:** +$8,000 to $15,000 if inspection scope exceeds CI allowance

**Probability:** LOW
**Impact Magnitude:** $8,000 to $15,000

**Suggested Mitigation:**
1. Review ER Part 2 for QA/QC requirements and hold points
2. Include inspection plan in DEL-15.05
3. Coordinate with Employer QA/QC representative for witness points

**Contingency Handling:** 20% CI contingency provides buffer.

---

### R-019: Pump Redundancy and N+1 Configuration (MEDIUM)
**ID:** R-019
**Risk Driver:** Scope
**Severity:** MEDIUM

**Cause:** Duty/standby configuration assumed for critical pumps but not confirmed by ER or system requirements.

**Consequence:**
- If single pumps allowed (no redundancy): -2 pumps = -$150,000 (-10%)
- If N+1 required for all services (higher redundancy): +2 pumps = +$150,000 (+10%)

**Affected Buckets:**
- CBS: Materials (MAT), Construction Directs (CD)
- WBS: All pump services

**Cost Impact:** ±$150,000 (±10%)

**Probability:** MEDIUM
**Impact Magnitude:** -$150,000 to +$150,000

**Suggested Mitigation:**
1. Review ER Part 2 for redundancy requirements
2. Coordinate with operations team on reliability requirements (OBJ-1)
3. Confirm duty/standby or N+1 configuration per service criticality
4. Update DEL-15.03 calculations to reflect confirmed configuration

**Contingency Handling:** 25% MAT contingency covers downside; upside may require budget increase.

**Related Assumptions:** A-001
**Related Decisions:** D-005

---

### R-020: Site-Specific Installation Challenges (LOW)
**ID:** R-020
**Risk Driver:** Site Conditions
**Severity:** LOW

**Cause:** Site conditions at Fraser Surrey Terminal not fully characterized (soil bearing, access, existing utilities interference).

**Consequence:**
- Poor soil bearing → additional foundation work (in PKG-05)
- Congested site → rigging complexity, longer installation time
- Existing utilities conflicts → relocation or special routing

**Affected Buckets:**
- CBS: Construction Directs (CD)
- WBS: DEL-15.01 (installation design)

**Cost Impact:**
- If site challenges increase installation hours by 15-25%: +$8,000 to $13,500

**Probability:** LOW (industrial terminal site, likely well-characterized)
**Impact Magnitude:** $8,000 to $13,500

**Suggested Mitigation:**
1. Review site survey and geotechnical reports (PKG-02)
2. Conduct site visit during DEL-15.01 arrangement design
3. Coordinate pump locations with existing infrastructure (utilities, structures)

**Contingency Handling:** 30% CD contingency provides buffer.

---

### R-021: Regulatory and Code Compliance Requirements Beyond API 610 (LOW)
**ID:** R-021
**Risk Driver:** Regulatory / Scope
**Severity:** LOW

**Cause:** ER Part 2 may specify additional codes/standards beyond API 610 (e.g., CSA B51, WorkSafeBC, environmental regulations).

**Consequence:**
- Additional certifications or testing: +$5,000 to $15,000
- Design modifications for code compliance: +$10,000 to $20,000 engineering

**Affected Buckets:**
- CBS: Engineering (E), Materials (MAT)
- WBS: DEL-15.02 (specifications), DEL-15.05 (testing)

**Cost Impact:** +$15,000 to $35,000 if significant additional requirements

**Probability:** LOW (API 610 is comprehensive; BC codes generally aligned)
**Impact Magnitude:** $15,000 to $35,000

**Suggested Mitigation:**
1. Review ER Part 2 and Part 1 for code/standard requirements
2. Confirm CSA B51, WorkSafeBC, NBC 2015 requirements
3. Include compliance requirements in DEL-15.02 specification

**Contingency Handling:** Engineering and MAT contingency provides buffer.

---

### R-022: Integration with Control System (MEDIUM)
**ID:** R-022
**Risk Driver:** Interface / Scope
**Severity:** MEDIUM

**Cause:** Integration requirements with PKG-19 (Control Systems) not detailed (VFD control, instrumentation, alarms).

**Consequence:**
- If pumps require extensive instrumentation (flow, pressure, temperature, vibration sensors): +$25,000 to $50,000
- If control panel integration complex: +$15,000 to $30,000
- Scope boundary unclear (PKG-15 vs. PKG-19/20)

**Affected Buckets:**
- CBS: Materials (MAT) for instruments, Engineering (E) for integration design
- WBS: Interface between PKG-15 and PKG-19/20

**Cost Impact:**
- Instrumentation: +$25,000 to $50,000 (if in PKG-15 scope)
- Integration engineering: +$10,000 to $20,000

**Probability:** LOW (likely instrumentation in PKG-20, not PKG-15)
**Impact Magnitude:** $0 to $70,000 if scope boundary unclear

**Suggested Mitigation:**
1. Define scope boundary between PKG-15 (pumps) and PKG-19/20 (controls/instrumentation)
2. Coordinate VFD interface requirements
3. Clarify if pump-mounted instruments are in PKG-15 or PKG-20 scope
4. Review Decisions Captured section of decomposition for responsibility splits

**Contingency Handling:** If scope addition confirmed, revise estimate; current contingency may not cover.

---

## Contingency Summary

**Contingency Method:** PCT_BY_BUCKET with allowance-heavy adjustments per AGENT_ESTIMATING.md fallback model.

**Contingency by CBS:**

| CBS | Base Amount | Base % | Allowance Adjustment | Final % | Contingency Amount |
|-----|-------------|--------|---------------------|---------|-------------------|
| Engineering (E) | $99,840 | 10% | +10% (parametric) | **20%** | $19,968 |
| PM | $70,620 | 10% | 0% | **10%** | $7,062 |
| Procurement (P) | $22,000 | 10% | 0% | **10%** | $2,200 |
| Materials (MAT) | $1,273,400 | 15% | +10% (100% allowance) | **25%** | $318,350 |
| Construction Directs (CD) | $54,040 | 20% | +10% (100% parametric) | **30%** | $16,212 |
| Construction Indirects (CI) | $9,730 | 20% | 0% | **20%** | $1,946 |
| Commissioning (COM) | $29,280 | 25% | 0% | **25%** | $7,320 |
| **Total** | **$1,558,910** | — | — | **23.9%** | **$373,058** |
| **Rounded** | **$1,559,000** | — | — | **23.9%** | **$373,000** |

**Contingency Adequacy Assessment:**

Given the risk profile:
- **HIGH risks** (R-001, R-002): Equipment quantities and pricing uncertainty
- **MEDIUM risks** (7 risks): Scope, interface, productivity, schedule
- **LOW risks** (5 risks): Minor scope additions, site conditions

**Assessment:** 23.9% overall contingency is **appropriate but potentially insufficient** for the HIGH uncertainty level:
- Materials contingency (25%) may not fully cover combined quantity + pricing risk (potential +50% upside)
- Construction Directs contingency (30%) is adequate for productivity variance
- Engineering contingency (20%) is adequate for coordination and iterations

**Recommendation:** Consider additional risk reserve or management reserve of 5-10% ($78,000 to $156,000) beyond the 23.9% contingency, given the high TBD content and lack of vendor quotes. Alternatively, re-estimate after DEL-15.03 completed and budgetary quotes obtained.

---

## Risk Mitigation Timeline

**Immediate actions (prior to next estimate update):**
1. Complete DEL-15.03 (Pump Design Calculations) — Resolves R-001 pump quantities
2. Review ER Part 2 — Resolves R-006 fluid properties, R-011 API 610 requirements, R-013 food-grade materials
3. Define scope boundaries with PKG-05, PKG-14, PKG-17/19, PKG-20 — Resolves R-012, R-022

**Short-term actions (30-60 days):**
1. Solicit budgetary quotes from pump vendors — Resolves R-002 pricing uncertainty
2. Coordinate motor and VFD requirements with Electrical — Resolves R-003
3. Develop commissioning plan in DEL-15.05 — Resolves R-008
4. Define spare parts strategy — Resolves R-014

**Medium-term actions (90+ days):**
1. Finalize pump procurement and confirm vendor pricing — Closes R-002, R-015
2. Validate installation productivity assumptions — Refines R-004
3. Monitor labor rate trends — Manages R-009

---

**Document Status:** FINAL
**Prepared By:** ESTIMATING Agent
**Date:** 2026-01-28
