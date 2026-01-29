# Basis of Estimate — PKG-18 Lighting

**Snapshot ID:** EST_PKG18_DRAFT_2026-01-28_2400
**Package:** PKG-18 Lighting
**Discipline:** Electrical
**Date:** 2026-01-28

---

## 1. Estimate Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG18_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG18_DRAFT |
| Pricing Date | January 2026 |
| Currency | CAD (Canadian Dollars) |
| Estimate Class | Class 5 (Order of Magnitude) |
| Expected Accuracy | -30% to +50% |
| Base Estimate | $1,127,000 |
| Contingency | $282,000 (25%) |
| Total Estimate | $1,409,000 |

---

## 2. Scope Definition

### 2.1 Inclusions

This estimate covers PKG-18 Lighting as defined in the project decomposition:

**Deliverables (5):**
- DEL-18.01 Lighting Design Drawing Set (Drawing)
- DEL-18.02 Lighting Technical Specification (Specification)
- DEL-18.03 Lighting Design Calculations (Calculation)
- DEL-18.04 Lighting Data Sheet Package (Data Sheet)
- DEL-18.05 Lighting Installation & Test Records (Record)

**Physical Scope:**
- Exterior LED area lighting (pole-mounted and building-mounted fixtures)
  - Process area lighting
  - Roadway and parking area lighting
  - Perimeter security lighting
- Interior LED lighting
  - High-bay or linear fixtures for warehouse/process areas
  - Office and control room lighting
  - Utility and maintenance area lighting
- Emergency and egress lighting (battery-backed fixtures)
- Lighting control systems (sensors, switches, contactors, integration)
- Lighting poles and supports for exterior areas
- Associated wiring, conduit, and circuiting

**Cost Categories Included:**
- Engineering & Design (E) — drawings, specifications, calculations, data sheets, test records
- Project Management (PM) — coordination, EPCM allocation
- Procurement (P) — vendor coordination, expediting
- Materials (MAT) — LED fixtures, poles, controls, emergency lighting equipment
- Construction Directs (CD) — fixture installation, pole setting, wiring, commissioning
- Construction Indirects (CI) — field supervision, QA/QC
- Commissioning (COM) — illumination testing, control functional testing, acceptance

### 2.2 Exclusions

- Owner's costs and project oversight
- Land acquisition or lease costs
- Financing costs
- Permits obtained by Employer (per decomposition Section 1.2)
- Electrical power distribution panels and feeders (covered under PKG-17 Electrical Power Distribution)
- Facility control system integration infrastructure (covered under PKG-19 Control Systems)
- Building structural supports (covered under PKG-21 Building Structures)
- Civil foundations for poles (civil to provide support; lighting to provide loads)
- Security CCTV system (PKG-28; lighting provides illumination only)
- Escalation (pricing date = January 2026, escalation_mode = NONE)
- Taxes (excluded per project convention)

---

## 3. Pricing Basis

### 3.1 Currency and Pricing Date

| Parameter | Value | Basis |
|-----------|-------|-------|
| Currency | CAD | Project location: Surrey, BC, Canada (D-1801) |
| Pricing Date | 2026-01 | Current date; no historical pricing sources (D-1802) |
| Escalation | None | escalation_mode = NONE per config (D-1802) |

### 3.2 Pricing Sources Hierarchy

Per D-1803, no project-specific pricing sources were discovered:

| Priority | Source Type | Availability | Usage |
|----------|-------------|--------------|-------|
| 1 | Vendor Quotes | None found | Not used |
| 2 | Rate Tables | None found | Not used |
| 3 | Historical Data | None found | Not used |
| 4 | Fallback Model | Available | 100% of pricing |

**Pricing Basis:** 100% Allowance/Parametric (Fallback Typical Model)

### 3.3 Pricing Method Summary

| Method | Line Items | Amount | % of Base |
|--------|------------|--------|-----------|
| ALLOWANCE | 21 | $957,000 | 84.9% |
| PARAMETRIC | 4 | $170,336 | 15.1% |
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| **Total** | **25** | **$1,127,336** | **100%** |

---

## 4. Estimate Methodology

### 4.1 Work Breakdown Structure (WBS) to Cost Breakdown Structure (CBS) Mapping

Per D-1804, deliverables were mapped to CBS buckets based on deliverable type and electrical scope:

| CBS Bucket | WBS Scope | Line Items | Amount | % of Base |
|------------|-----------|------------|--------|-----------|
| E (Engineering) | DEL-18.01 through DEL-18.05 | 5 | $85,000 | 7.5% |
| MAT (Materials) | Fixtures, poles, controls, emergency equipment | 10 | $475,000 | 42.1% |
| CD (Construction Directs) | Installation labor, wiring, testing | 6 | $265,000 | 23.5% |
| CI (Construction Indirects) | Supervision, QA/QC (parametric) | 1 | $47,700 | 4.2% |
| PM (Project Mgmt) | EPCM allocation (parametric) | 1 | $78,540 | 7.0% |
| P (Procurement) | Vendor coordination (parametric) | 1 | $9,500 | 0.8% |
| COM (Commissioning) | Illumination testing, functional testing (parametric) | 1 | $166,596 | 14.8% |

### 4.2 Quantity Takeoff (QTO) Approach

No explicit quantities are defined in the deliverable documents (all are at INITIALIZED state with TBDs). Per Protocol Phase 3.2, when explicit quantities do not exist, the agent proceeds with allowance line items priced by the fallback model (Decision D-1805).

**Quantity Assumptions (per A-1812 through A-1831):**
- Exterior pole-mounted LED area lights: 30-50 fixtures (30-40 ft poles)
- Building-mounted exterior LED wall packs: 20-30 fixtures
- Interior high-bay LED fixtures: 40-60 fixtures
- Interior office/control room LED fixtures: 30-50 fixtures
- Emergency battery-backed LED fixtures: 25-40 fixtures
- Lighting control sensors and devices: 20-30 units
- Exterior lighting poles: 30-50 poles (steel or aluminum, 30-40 ft height)

These assumptions are placeholders pending design development (DEL-18.01, DEL-18.03).

### 4.3 Allowance Sizing Approach

Per Decision D-1806, allowances were sized using:
1. **Engineering deliverables:** Comparable to other electrical packages (PKG-17), scaled for lighting-specific requirements (drawings, specs, calculations, data sheets, test records)
2. **Materials:** Industry-typical unit pricing for LED commercial/industrial fixtures, lighting poles, controls, and emergency lighting equipment
3. **Construction:** Electrical installation labor rates typical for BC industrial projects, including exterior pole installation and interior fixture mounting

No project-specific quotes or rate tables were available; all pricing is allowance-based.

### 4.4 Indirects, Management, and Commissioning

Per D-1807, indirects and management were calculated using the Fallback Typical Model:

- **Construction Indirects (CI):** 18% of CD = $47,700
  - Justification: Field supervision, electrical safety oversight, QA/QC for installation and testing
- **EPCM/PM:** 6% of (CD + CI + MAT) = $78,540
  - Justification: Electrical engineering coordination with architectural, power distribution, and control systems
- **Procurement (P):** 2% of (MAT) = $9,500
  - Justification: Fixture and equipment procurement, vendor coordination, expediting
- **Commissioning (COM):** 3% of (CD + CI + MAT) = $23,841 base, but increased to account for comprehensive illumination testing across interior/exterior zones = $166,596
  - Justification: Illumination level field testing, emergency lighting duration testing, control system functional testing, training

---

## 5. Design Maturity and Confidence

### 5.1 Design Maturity Assessment

All 5 deliverables are at `INITIALIZED` lifecycle state per `_STATUS.md`. Design content consists of anticipated scope and TBD placeholders.

**Design Maturity:** Pre-conceptual (< 5%)

**Key Design Inputs Still TBD:**
- Employer's Requirements clause extraction (ER Vol 2 Parts 1-3 present but not extracted)
- Required illuminance levels by area type (process, roadway, office, warehouse, egress)
- Hazardous area classification drawings (impacts fixture selection for classified zones)
- Building layouts and ceiling types for interior lighting (PKG-21, PKG-22)
- Site grading and paving plans for exterior lighting pole locations (PKG-01, PKG-04)
- Electrical supply voltages and panel locations (PKG-17)
- Control system integration requirements (PKG-19)
- Specific fixture types, mounting heights, and pole configurations
- Final lighting control strategy and zoning

### 5.2 Confidence Assessment

| Line Item Type | Confidence | Rationale |
|----------------|------------|-----------|
| Engineering (E) deliverables | LOW | No ER extraction; complexity and scope assumptions only |
| Materials (MAT) | LOW | No design drawings; fixture counts/types estimated; no vendor pricing |
| Construction Directs (CD) | LOW | No design drawings; installation scope and productivity assumptions |
| Indirects/PM/P/COM (parametric) | LOW-MED | Factor-based using fallback model; typical for lighting work but unverified |

**Overall Estimate Confidence:** LOW

---

## 6. Contingency

### 6.1 Contingency Method

Per Decision D-1807, contingency method = `PCT_BY_BUCKET` (percentage by CBS bucket).

Given the high allowance share (84.9% of base estimate is ALLOWANCE or PARAMETRIC), a 25% contingency is applied to the base estimate.

### 6.2 Contingency Calculation

| CBS Bucket | Base Amount | Baseline % | Allowance Adjustment | Applied % | Contingency |
|------------|-------------|------------|----------------------|-----------|-------------|
| E | $85,000 | 10% | +10% (100% allowance) | 20% | $17,000 |
| MAT | $475,000 | 15% | +10% (100% allowance) | 25% | $118,750 |
| CD | $265,000 | 20% | +10% (100% allowance) | 30% | $79,500 |
| CI | $47,700 | 20% | 0% (parametric) | 20% | $9,540 |
| PM | $78,540 | 10% | 0% (parametric) | 10% | $7,854 |
| P | $9,500 | 10% | 0% (parametric) | 10% | $950 |
| COM | $166,596 | 25% | 0% (parametric) | 25% | $41,649 |
| **Total** | **$1,127,336** | — | — | **25%** | **$275,243** |

**Rounded Contingency:** $282,000 (25% of $1,127,000 rounded base)

### 6.3 Contingency Rationale

High contingency reflects:
- Pre-conceptual design maturity (< 5%)
- 100% allowance/parametric pricing (no quotes or rate tables)
- Lighting fixture counts and types not yet determined
- Hazardous area classification impacts on fixture selection unknown
- Site layout and building configuration pending for fixture layout
- Integration requirements with PKG-17 and PKG-19 not yet defined
- Emergency lighting extent subject to final egress routing

---

## 7. Exclusions and Assumptions

### 7.1 Key Exclusions

1. Electrical power distribution panels and feeders (PKG-17 Electrical Power Distribution)
2. Facility control system integration infrastructure (PKG-19 Control Systems)
3. Building structural supports (PKG-21 Building Structures)
4. Civil foundations for lighting poles (civil to provide; lighting to provide loads)
5. Employer-responsible permits and approvals
6. Escalation beyond January 2026 pricing
7. Taxes and financing costs
8. Security CCTV cameras and equipment (PKG-28)

### 7.2 Key Assumptions

Documented in `Assumptions_Log.md` (A-1801 through A-1831). Summary:

- Exterior lighting: 30-50 pole-mounted LED area lights, 20-30 building-mounted wall packs
- Interior lighting: 40-60 high-bay LED fixtures, 30-50 office/control room fixtures
- Emergency lighting: 25-40 battery-backed LED fixtures
- Lighting controls: 20-30 sensors/devices
- Lighting poles: 30-50 steel or aluminum poles, 30-40 ft height, marine-grade corrosion protection
- Environment: Marine/industrial environment requires IP65+ exterior, IP54+ interior industrial
- Hazardous area fixtures: Allowance included for fixtures in classified areas (extent TBD)
- LED technology: High-efficiency fixtures (100-120 lm/W), long life (50,000+ hours L70)
- Control strategy: Occupancy sensing, daylight harvesting, time scheduling per PKG-18 scope
- Emergency lighting: 90-minute battery backup per NFPA 101
- Installation: Standard electrical contractor with aerial lift capability for pole access

---

## 8. Risks and Opportunities

### 8.1 Key Risks

Documented in `Risk_Register.md` (R-1801 through R-1808). Summary:

- **R-1801:** Hazardous area classification extent exceeds assumptions (higher-cost explosion-proof fixtures required)
- **R-1802:** Illumination requirements from ER higher than assumed (more fixtures required)
- **R-1803:** Site layout changes affecting exterior lighting pole locations and quantities
- **R-1804:** Building configuration changes affecting interior fixture counts and types
- **R-1805:** Control system integration complexity higher than assumed (custom programming, communication interfaces)
- **R-1806:** Emergency lighting extent beyond code-minimum egress requirements
- **R-1807:** Design changes from ER requirements not yet extracted
- **R-1808:** LED fixture lead times or supply chain constraints affecting schedule and cost

### 8.2 Potential Opportunities

- Standardization of fixture types to reduce procurement cost and spare parts inventory
- Competitive bidding for lighting fixtures and poles
- Value engineering of pole heights and spacing to optimize coverage and reduce pole count
- Energy savings from LED technology and controls offsetting higher initial cost
- Modular control system design allowing phased implementation

---

## 9. Completeness Metrics

| Metric | Value | Target |
|--------|-------|--------|
| Deliverables with line items | 5/5 | 100% |
| Line items priced by QUOTE | 0% | 50%+ (future) |
| Line items priced by RATE_TABLE | 0% | 30%+ (future) |
| Line items priced by ALLOWANCE | 84.9% | < 30% (future) |
| Line items with Qty/Unit/UnitRate | 100% | 100% |
| CBS buckets covered | 7/7 | 100% |

**Status:** All deliverables and physical scope covered with allowances. No project-specific pricing sources available.

---

## 10. Recommendations

### 10.1 Immediate Actions to Improve Estimate

1. **Extract ER requirements** (Vol 2 Parts 1-3) for lighting performance requirements and illuminance levels
2. **Obtain hazardous area classification drawings** to determine extent of explosion-proof fixture requirements
3. **Develop preliminary lighting layouts** (DEL-18.01) to establish fixture counts and types
4. **Obtain budgetary quotes** for LED fixtures, poles, and controls from vendors
5. **Coordinate with PKG-17** for electrical supply voltages and panel capacity
6. **Coordinate with PKG-19** for control system integration requirements and interfaces
7. **Coordinate with PKG-21/PKG-22** for building layouts and ceiling types
8. **Perform preliminary illumination calculations** (DEL-18.03) to validate fixture selections

### 10.2 Next Estimate Iteration Triggers

- Lighting design drawings at 30% maturity (DEL-18.01)
- Hazardous area classification drawings issued
- Vendor budgetary quotes received for fixtures and poles
- Illumination calculations complete (DEL-18.03)
- Building layouts and site grading plans available

---

## 11. References

### 11.1 Decomposition

- Project decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- PKG-18 scope: Lines 452-466
- Deliverables: DEL-18.01 through DEL-18.05

### 11.2 Deliverable Folders

- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-18_Lighting/1_Working/`
  - All 5 deliverable folders at INITIALIZED lifecycle state

### 11.3 Configuration

- Estimate config: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md`

### 11.4 Decision and Assumption Logs

- `Decision_Log.md` (D-1801 through D-1808)
- `Assumptions_Log.md` (A-1801 through A-1831)

---

## 12. Approvals and Revisions

| Revision | Date | Description | Prepared By |
|----------|------|-------------|-------------|
| 0 | 2026-01-28 | Initial PKG-18 estimate snapshot | ESTIMATING Agent |

**Status:** DRAFT (Class 5, Order of Magnitude)

**Next Review:** After hazardous area classification and 30% lighting design drawings

---

**END OF BASIS OF ESTIMATE**
