# Assumptions Log — PKG-15 Pumps & Rotating Equipment Estimate

**Snapshot ID:** EST_PKG15_DRAFT_2026-01-28_2345
**Package:** PKG-15 Pumps & Rotating Equipment
**Date:** 2026-01-28

---

## Assumption Entries

### A-001: Total Pump Unit Count
**ID:** A-001
**Statement:** Total of 14 pump units for the facility (4 railcar unloading transfer, 2 marine loading, 2 tank transfer, 6 sump pumps).

**Why Needed:** All deliverable documents list pump quantities as "TBD" pending DEL-15.03 calculations.

**Impacted WBS/CBS:**
- WBS: DEL-15.01 through DEL-15.05
- CBS: Materials (MAT), Construction Directs (CD), Commissioning (COM)

**Cost Impact:** $850,000 base equipment cost (14 pumps × average $60,000/unit)
**Range:** If actual quantity is 10-18 pumps, cost range: $600,000 - $1,080,000 (±25%)

**Confidence:** LOW

**Resolution Path:** Complete DEL-15.03 (Pump Design Calculations) to finalize pump quantities per system requirements and ER Part 2 specifications.

**Related Decisions:** D-005

---

### A-002: Pump Equipment Unit Costs
**ID:** A-002
**Statement:** API 610 process pump costs estimated as follows:
- Large pumps (400 m³/hr, 50 kW): $125,000/unit
- Medium pumps (200 m³/hr, 30 kW): $75,000/unit
- Small transfer pumps (150 m³/hr, 15 kW): $45,000/unit
- Sump pumps (25 m³/hr, 3 kW): $12,000/unit

**Why Needed:** No vendor quotes or budgetary pricing available; no rate tables with pump costs.

**Impacted WBS/CBS:**
- WBS: All PKG-15 deliverables
- CBS: Materials (MAT)

**Cost Impact:** $850,000 total pump equipment cost
**Range:** API 610 pump costs can vary ±30% based on materials, features, and vendor
- Low range (commercial-grade): $595,000 (-30%)
- High range (premium features): $1,105,000 (+30%)

**Confidence:** LOW

**Resolution Path:**
1. Finalize pump specifications (DEL-15.02)
2. Solicit budgetary quotes from API 610 pump vendors (e.g., Flowserve, Sulzer, ITT Goulds, KSB)
3. Confirm API 610 vs. commercial pump requirements per ER Part 2

**Related Decisions:** D-005, D-006, D-007, D-008

---

### A-003: Installation Labor Productivity
**ID:** A-003
**Statement:** Installation labor assumed as:
- Pump setting and alignment: 24 manhours per pump unit (average)
- Baseplate grouting: 8 manhours per pump
- Mechanical completion: 8 manhours per pump
- Total installation: 40 manhours per pump × 14 pumps = 560 manhours

**Why Needed:** No project-specific installation productivity data or historical records from similar BC projects.

**Impacted WBS/CBS:**
- WBS: DEL-15.01 (installation design), DEL-15.05 (installation records)
- CBS: Construction Directs (CD)

**Cost Impact:** 560 manhours × $95/hr = $53,200
**Range:** Productivity can vary ±20% based on site access, pump size/weight, and crew experience
- Low productivity (more hours): $63,840 (+20%)
- High productivity (fewer hours): $42,560 (-20%)

**Confidence:** MEDIUM

**Resolution Path:**
1. Obtain historical installation data from similar pump installations at Fraser Surrey Terminal
2. Confirm site access and rigging constraints with PKG-00 (Site Establishment)
3. Validate with installation contractor or construction manager

**Related Decisions:** D-014

---

### A-004: Motor and Drive Costs
**ID:** A-004
**Statement:** Electric motors and variable frequency drives (VFDs) estimated as:
- Motors: $500/kW (NEMA Premium efficiency, TEFC enclosure)
- VFDs (if required): $300/kW for critical pumps only (50% of pumps assumed VFD-equipped)

**Why Needed:** Motor specifications TBD per DEL-15.02 and PKG-17/19 electrical coordination; no vendor quotes.

**Impacted WBS/CBS:**
- WBS: DEL-15.04 (motor data sheets)
- CBS: Materials (MAT) for motors, Electrical (EI) for VFDs

**Cost Impact:**
- Motors: 406 kW total × $500/kW = $203,000
- VFDs: 203 kW × $300/kW = $60,900 (for 50% of pumps)
- **Total: $263,900**

**Range:** Motor/VFD costs can vary ±25% based on features (premium efficiency, explosion-proof rating, soft starters vs. VFDs)
- Low range: $197,925 (-25%)
- High range: $329,875 (+25%)

**Confidence:** MEDIUM

**Resolution Path:**
1. Coordinate with PKG-17/19 (Electrical) for motor specifications and VFD requirements
2. Obtain budgetary pricing from motor vendors (ABB, Siemens, WEG, Baldor)
3. Confirm VFD requirements per operational flexibility needs (OBJ-4)

**Related Decisions:** D-006

---

### A-005: Canola Oil Fluid Properties
**ID:** A-005
**Statement:** Canola oil properties assumed as:
- Specific gravity: 0.91 @ 15°C
- Viscosity: 50 cP @ 20°C
- Operating temperature: 20-50°C
- Vapor pressure: Low (negligible)
- Non-corrosive, food-grade service

**Why Needed:** Fluid properties listed as "TBD" in DEL-15.02; required for pump selection and material compatibility.

**Impacted WBS/CBS:**
- WBS: DEL-15.02 (specification), DEL-15.03 (calculations)
- CBS: Engineering (E), Materials (MAT)

**Cost Impact:** Minimal direct cost impact; affects pump material selection and sizing accuracy.
**Range:** If viscosity is higher than assumed (winter operations), heating systems or larger motors may be required (+10-15% cost).

**Confidence:** MEDIUM (typical canola oil properties from industry data)

**Resolution Path:** Confirm canola oil properties from ER Part 2 (Process Mechanical Works) or product specification sheets from Employer.

**Related Decisions:** D-008

---

### A-006: Procurement Services Allowance
**ID:** A-006
**Statement:** Procurement services estimated at 2% of equipment cost ($850,000 × 2% = $17,000) covering:
- Vendor solicitation and technical evaluation
- Purchase order management
- Expediting and coordination
- Receiving inspection

**Why Needed:** No project-specific procurement rates; using fallback model from AGENT_ESTIMATING.md.

**Impacted WBS/CBS:**
- WBS: All PKG-15 equipment procurement
- CBS: Procurement (P)

**Cost Impact:** $17,000
**Range:** Procurement services typically 1-3% of equipment value
- Low range (minimal): $8,500 (1%)
- High range (intensive): $25,500 (3%)

**Confidence:** MEDIUM

**Resolution Path:** Obtain project-specific procurement services rates from EPCM or construction manager.

**Related Decisions:** D-010

---

### A-007: Construction Indirects Factor
**ID:** A-007
**Statement:** Construction indirects estimated at 18% of Construction Directs ($53,200 × 18% = $9,576) covering:
- Site supervision
- Temporary facilities
- Small tools and consumables
- HSE and QA/QC

**Why Needed:** No project-specific indirects rate; using fallback model from AGENT_ESTIMATING.md (range: 12-28%).

**Impacted WBS/CBS:**
- WBS: All PKG-15 field installation work
- CBS: Construction Indirects (CI)

**Cost Impact:** $9,576
**Range:** CI can vary 12-28% based on project complexity, site remoteness, schedule compression
- Low range: $6,384 (12%)
- High range: $14,896 (28%)

**Confidence:** MEDIUM

**Resolution Path:** Obtain project-specific CI rates from construction contractor or historical data from similar Fraser Surrey Terminal projects.

**Related Decisions:** D-010

---

### A-008: EPCM/PM Factor
**ID:** A-008
**Statement:** EPCM/Project Management estimated at 6% of (CD + CI + MAT) = 6% × ($53,200 + $9,576 + $1,113,900) = $70,621 covering:
- Project management
- Engineering management
- Document control
- Coordination and meetings

**Why Needed:** No project-specific PM rates; using fallback model from AGENT_ESTIMATING.md (range: 4-10%).

**Impacted WBS/CBS:**
- WBS: All PKG-15 deliverables
- CBS: Project Management (PM)

**Cost Impact:** $70,621
**Range:** PM typically 4-10% of (CD + CI + MAT)
- Low range: $47,081 (4%)
- High range: $117,668 (10%)

**Confidence:** MEDIUM

**Resolution Path:** Obtain project-specific PM rates from EPCM contractor or fee proposal.

**Related Decisions:** D-010

---

### A-009: Commissioning Effort
**ID:** A-009
**Statement:** Commissioning estimated at 16 manhours per pump unit (14 pumps × 16 hr = 224 manhours @ $95/hr = $21,280) covering:
- Performance testing (flow, head, power, vibration)
- Alignment verification
- Seal system checkout
- Documentation (test records, punch list)

**Why Needed:** DEL-15.05 commissioning scope defined conceptually but hours not quantified.

**Impacted WBS/CBS:**
- WBS: DEL-15.05 (Installation & Test Records)
- CBS: Commissioning (COM)

**Cost Impact:** $21,280
**Range:** Commissioning effort can vary ±30% based on complexity and acceptance criteria
- Low range: $14,896 (-30%)
- High range: $27,664 (+30%)

**Confidence:** MEDIUM

**Resolution Path:** Develop detailed commissioning plan in DEL-15.05 with estimated hours per activity.

**Related Decisions:** D-015

---

### A-010: Engineering Hours by Deliverable
**ID:** A-010
**Statement:** Engineering effort estimated at 480 total hours ($100,000 ÷ $208/hr loaded rate) distributed as:
- DEL-15.01 Design Drawings: 192 hours (40%)
- DEL-15.02 Specification: 120 hours (25%)
- DEL-15.03 Calculations: 96 hours (20%)
- DEL-15.04 Data Sheets: 48 hours (10%)
- DEL-15.05 Test Records: 24 hours (5%)

**Why Needed:** No engineering hours budget provided; parametric estimate based on deliverable complexity.

**Impacted WBS/CBS:**
- WBS: All PKG-15 deliverables
- CBS: Engineering (E)

**Cost Impact:** $100,000 total engineering
**Range:** Engineering hours can vary ±25% based on design iterations, coordination complexity, ER requirements
- Low range: $75,000 (-25%)
- High range: $125,000 (+25%)

**Confidence:** MEDIUM

**Resolution Path:** Obtain engineering hours estimate from mechanical discipline lead or compare to similar packages.

**Related Decisions:** D-009

---

### A-011: Seal Systems and Auxiliary Equipment
**ID:** A-011
**Statement:** Mechanical seal systems and auxiliary equipment (seal flush systems, cooling water, instrumentation) estimated at 15% of pump cost.

**Why Needed:** Seal specifications TBD per DEL-15.02 (API 682 Type 1/2/3; single vs. dual seal; piping plans).

**Impacted WBS/CBS:**
- WBS: DEL-15.02 (seal specification), DEL-15.04 (seal data)
- CBS: Materials (MAT)

**Cost Impact:** $850,000 × 15% = $127,500
**Range:** Seal systems typically 10-25% of pump cost based on criticality and complexity
- Low range (simple single seals): $85,000 (10%)
- High range (dual seals with barrier fluid systems): $212,500 (25%)

**Confidence:** LOW-MEDIUM

**Resolution Path:**
1. Define seal requirements per service criticality and environmental protection requirements (OBJ-7)
2. Coordinate with PKG-14 (Process Piping) for seal support piping
3. Obtain budgetary pricing from seal vendors (John Crane, Flowserve, EagleBurgmann)

**Related Decisions:** D-008

---

### A-012: Coupling and Baseplate Costs
**ID:** A-012
**Statement:** Pump couplings and fabricated baseplates estimated at 12% of pump cost.

**Why Needed:** No specific cost data; typical proportion for packaged pump/motor assemblies.

**Impacted WBS/CBS:**
- WBS: All pump units
- CBS: Materials (MAT)

**Cost Impact:** $850,000 × 12% = $102,000
**Range:** ±15% variation based on coupling type (spacer, flexible, gear) and baseplate design

**Confidence:** MEDIUM

**Resolution Path:** Confirm with pump vendor quotations (typically included in package price).

---

### A-013: Spare Parts Allowance
**ID:** A-013
**Statement:** Initial spare parts estimated at 8% of pump equipment cost ($850,000 × 8% = $68,000) covering:
- Mechanical seals (1 spare per pump type)
- Wear rings and impellers
- Bearings
- Coupling elements

**Why Needed:** Spare parts requirements TBD per ER and O&M philosophy; standard practice for critical equipment.

**Impacted WBS/CBS:**
- WBS: All pump equipment
- CBS: Materials (MAT)

**Cost Impact:** $68,000
**Range:** Spare parts allowances typically 5-15% of equipment cost
- Low range: $42,500 (5%)
- High range: $127,500 (15%)

**Confidence:** LOW

**Resolution Path:**
1. Define spare parts philosophy per ER requirements and OBJ-9 (lifecycle cost optimization)
2. Coordinate with operations team for preferred spares inventory strategy
3. Obtain vendor-recommended spare parts lists

---

## Summary

**Total Assumptions:** 13
**HIGH Impact:** 3 (A-001 pump quantities, A-002 equipment costs, A-011 seal systems)
**MEDIUM Impact:** 7
**LOW Impact:** 3

**Cumulative Cost Impact of Assumptions:**
| Assumption | Base Cost | Cost Range (Low-High) |
|------------|-----------|----------------------|
| A-001 (pump quantities) | $850,000 | $600,000 - $1,080,000 |
| A-002 (pump unit costs) | $850,000 | $595,000 - $1,105,000 |
| A-003 (installation labor) | $53,200 | $42,560 - $63,840 |
| A-004 (motors/VFDs) | $263,900 | $197,925 - $329,875 |
| A-010 (engineering) | $100,000 | $75,000 - $125,000 |
| A-011 (seal systems) | $127,500 | $85,000 - $212,500 |
| Other assumptions | ~$290,000 | ±20% |

**Overall Uncertainty Range:**
- **Low case:** ~$1,300,000 (-20% to -25%)
- **Base case:** ~$1,600,000
- **High case:** ~$2,100,000 (+25% to +30%)

**Top 3 Uncertainty Drivers:**
1. **Pump quantities** (TBD in all deliverables) — Assumption A-001
2. **Equipment unit costs** (no vendor quotes) — Assumption A-002
3. **Seal system complexity** (TBD per criticality) — Assumption A-011

**Recommended Actions:**
1. **Priority 1:** Complete DEL-15.03 calculations to finalize pump quantities and sizing
2. **Priority 2:** Review ER Part 2 for pump specifications and seal requirements
3. **Priority 3:** Solicit budgetary quotes from pump vendors
4. **Priority 4:** Develop project-specific rate tables for labor, indirects, PM

---

**Document Status:** FINAL
**Prepared By:** ESTIMATING Agent
**Date:** 2026-01-28
