# Basis of Estimate — PKG-17 Electrical Power Distribution

**Snapshot ID:** EST_PKG17_DRAFT_2026-01-28_0005
**Package:** PKG-17 Electrical Power Distribution
**Discipline:** Electrical
**Date:** 2026-01-28

---

## 1. Estimate Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG17_DRAFT_2026-01-28_0005 |
| Estimate Label | PKG17_DRAFT |
| Pricing Date | January 2026 |
| Currency | CAD (Canadian Dollars) |
| Estimate Class | Class 5 (Order of Magnitude) |
| Expected Accuracy | -30% to +50% |
| Base Estimate | $3,866,000 |
| Contingency | $962,000 (25%) |
| Total Estimate | $4,828,000 |

---

## 2. Scope Definition

### 2.1 Inclusions

This estimate covers PKG-17 Electrical Power Distribution as defined in the project decomposition:

**Deliverables (5):**
- DEL-17.01 Electrical Power Design Drawing Set (Drawing)
- DEL-17.02 Electrical Power Technical Specification (Specification)
- DEL-17.03 Electrical Power Design Calculations (Calculation)
- DEL-17.04 Electrical Power Data Sheet Package (Data Sheet)
- DEL-17.05 Electrical Power Installation & Test Records (Record)

**Physical Scope:**
- MV/LV transformers (2 units, 1000-1500 kVA each, pad-mounted)
- MV switchgear (5-bay metal-clad lineup, incoming breaker and feeders)
- LV switchgear (main-tie-main configuration, distribution feeders)
- Motor Control Centers (3 MCCs for railcar area, tank farm, marine area)
- Distribution panels and subpanels (8 panels for lighting, receptacles, small power)
- UPS system (10 kVA for control systems and critical loads)
- Grounding system (ground grid, electrodes, bonding, testing)
- Power cables (MV: 800m, LV: 3500m, Control: 2500m)
- Cable tray and ladder rack (900m total with supports)
- Conduit and fittings (600m for underground and local routing)
- Installation materials and hardware

**Cost Categories Included:**
- Engineering & Design (E) — drawings, calculations, specifications, data sheets, test documentation
- Project Management (PM) — electrical engineering coordination, EPCM allocation
- Procurement (P) — vendor coordination, expediting, FAT witness, inspection
- Materials (MAT) — transformers, switchgear, MCCs, panels, UPS, grounding, cables, cable tray, conduit
- Freight/Logistics (FRT) — electrical equipment transport and delivery
- Construction Directs (CD) — equipment installation, terminations, testing, grounding installation, cable pulling
- Construction Indirects (CI) — field supervision, electrical safety, QA/QC
- Commissioning (COM) — relay testing, energization, integrated systems testing

### 2.2 Exclusions

- Owner's costs and project oversight
- Land acquisition or lease costs
- Financing costs
- Permits obtained by Employer (per decomposition Section 1.2)
- Lighting systems (covered under PKG-18 Lighting)
- Control system equipment and I/O (covered under PKG-19 Control Systems and PKG-20 Field Instrumentation)
- Building electrical distribution within MCC building (covered under PKG-22 Building Interior & MEP where applicable)
- Utility company service connection charges and metering (Owner-supplied service assumed available at site boundary)
- Escalation (pricing date = January 2026, escalation_mode = NONE)
- Taxes (excluded per project convention)

---

## 3. Pricing Basis

### 3.1 Currency and Pricing Date

| Parameter | Value | Basis |
|-----------|-------|-------|
| Currency | CAD | Project location: Surrey, BC, Canada (D-1701) |
| Pricing Date | 2026-01 | Current date; no historical pricing sources (D-1702) |
| Escalation | None | escalation_mode = NONE per config (D-1702) |

### 3.2 Pricing Sources Hierarchy

Per D-1703, no project-specific pricing sources were discovered:

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
| ALLOWANCE | 29 | $3,342,000 | 86.4% |
| PARAMETRIC | 4 | $523,852 | 13.6% |
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| **Total** | **33** | **$3,865,852** | **100%** |

---

## 4. Estimate Methodology

### 4.1 Work Breakdown Structure (WBS) to Cost Breakdown Structure (CBS) Mapping

Per D-1704, deliverables were mapped to CBS buckets based on deliverable type and electrical scope:

| CBS Bucket | WBS Scope | Line Items | Amount | % of Base |
|------------|-----------|------------|--------|-----------|
| E (Engineering) | DEL-17.01 through DEL-17.05 | 5 | $245,000 | 6.3% |
| MAT (Materials) | Transformers, switchgear, MCCs, panels, UPS, grounding, cables, cable tray | 13 | $1,989,500 | 51.5% |
| FRT (Freight) | Equipment transport and logistics | 1 | $58,000 | 1.5% |
| CD (Construction Directs) | Installation, terminations, testing, grounding, cable pulling | 10 | $1,049,500 | 27.1% |
| CI (Construction Indirects) | Supervision, safety, QA/QC (parametric) | 1 | $188,910 | 4.9% |
| PM (Project Mgmt) | EPCM allocation (parametric) | 1 | $197,155 | 5.1% |
| P (Procurement) | Vendor coordination (parametric) | 1 | $40,950 | 1.1% |
| COM (Commissioning) | Testing, energization, proving (parametric) | 1 | $96,837 | 2.5% |

### 4.2 Quantity Takeoff (QTO) Approach

No deliverable folders exist for PKG-17 (not yet scaffolded in execution workspace). Per Protocol Phase 3.2, when explicit quantities do not exist, the agent proceeds with allowance line items priced by the fallback model (Decision D-1705).

**Quantity Assumptions (per A-1706 through A-1729):**
- MV/LV Transformers: 2 units, 1000-1500 kVA each (requires load calculations to confirm)
- MV Switchgear: 5-bay lineup (incoming + transformer feeders + spares)
- LV Switchgear: Main-tie-main configuration
- MCCs: 3 units distributed across facility (railcar area, tank farm, marine area)
- Distribution Panels: 8 units for lighting/receptacles/small power
- UPS: 1 unit, 10 kVA for control systems
- Grounding: 1200m ground conductor, 15 driven electrodes
- MV Cable: 800m (transformer feeders, main distribution)
- LV Cable: 3500m (feeder and branch circuits)
- Control Cable: 2500m (motor controls and I/O signals)
- Cable Tray: 900m with supports and fittings
- Conduit: 600m (underground duct banks and local routing)

These assumptions are placeholders pending design development (DEL-17.01, DEL-17.03) and load calculations.

### 4.3 Allowance Sizing Approach

Per Decision D-1706, allowances were sized using:
1. **Engineering deliverables:** Comparable to other discipline packages, scaled for electrical complexity and coordination requirements (5 deliverables)
2. **Materials:** Industry-typical unit rates for industrial electrical equipment (transformers, switchgear, MCCs) with marine-environment ratings where exposed
3. **Construction:** Electrical installation rates reflecting industrial electrical contractor requirements (specialized tools, testing equipment, certified electricians)

No project-specific quotes or rate tables were available; all pricing is allowance-based.

### 4.4 Indirects, Management, and Commissioning

Per D-1708, indirects and management were calculated using the Fallback Typical Model:

- **Construction Indirects (CI):** 18% of CD = $188,910
  - Justification: Electrical work requires field supervision, electrical safety oversight, QA/QC for terminations/testing
- **EPCM/PM:** 6% of (CD + CI + MAT + FRT) = $197,155
  - Justification: Electrical engineering coordination across multiple disciplines and load centers
- **Procurement (P):** 2% of (MAT + FRT) = $40,950
  - Justification: Vendor coordination for major electrical equipment and FAT witness
- **Commissioning (COM):** 3% of (CD + CI + MAT) = $96,837
  - Justification: Protection relay testing, energization support, integrated systems testing

---

## 5. Design Maturity and Confidence

### 5.1 Design Maturity Assessment

No deliverable folders exist for PKG-17 in the execution workspace (not yet scaffolded). Estimate is based solely on decomposition scope description.

**Design Maturity:** Pre-conceptual (0%)

**Key Design Inputs Still TBD:**
- Employer's Requirements clause extraction (ER Vol 2 Parts 1-3 present but not extracted)
- Load calculations (motor loads, lighting loads, receptacle loads, heating loads)
- Equipment locations and layouts (affects cable routing and lengths)
- Voltage levels (MV service voltage, LV distribution voltage)
- Redundancy requirements (N, N+1, or other)
- Motor starting methodology (VFD vs soft-start vs DOL)
- Service entrance location and utility interface details
- Grounding system design (ground grid sizing, soil resistivity, step/touch potential analysis)
- Codes and standards requirements (CSA, NEC, local AHJ)
- Hazardous area classification (if any areas are Class I Div 2)

### 5.2 Confidence Assessment

| Line Item Type | Confidence | Rationale |
|----------------|------------|-----------|
| Engineering (E) deliverables | LOW | No ER extraction; complexity and scope assumptions only |
| Materials (MAT) | LOW | No load calculations; equipment sizes/quantities estimated; cable lengths approximate |
| Freight (FRT) | LOW | Equipment transport depends on supplier locations and equipment sizes |
| Construction Directs (CD) | LOW | No design drawings; installation complexity and labor productivity assumptions |
| Indirects/PM/P/COM (parametric) | LOW-MED | Factor-based using fallback model; typical for electrical work but unverified |

**Overall Estimate Confidence:** LOW

---

## 6. Contingency

### 6.1 Contingency Method

Per Decision D-1707, contingency method = `PCT_BY_BUCKET` (percentage by CBS bucket).

Given the high allowance share (86.4% of base estimate is ALLOWANCE or PARAMETRIC), a 25% average contingency is applied to the base estimate.

### 6.2 Contingency Calculation

| CBS Bucket | Base Amount | Baseline % | Allowance Adjustment | Applied % | Contingency |
|------------|-------------|------------|----------------------|-----------|-------------|
| E | $245,000 | 10% | +10% (100% allowance) | 20% | $49,000 |
| MAT | $1,989,500 | 15% | +10% (100% allowance) | 25% | $497,375 |
| FRT | $58,000 | 15% | +10% (100% allowance) | 25% | $14,500 |
| CD | $1,049,500 | 20% | +10% (100% allowance) | 30% | $314,850 |
| CI | $188,910 | 20% | 0% (parametric) | 20% | $37,782 |
| PM | $197,155 | 10% | 0% (parametric) | 10% | $19,716 |
| P | $40,950 | 10% | 0% (parametric) | 10% | $4,095 |
| COM | $96,837 | 25% | 0% (parametric) | 25% | $24,209 |
| **Total** | **$3,865,852** | — | — | **25%** | **$961,527** |

**Rounded Contingency:** $962,000 (25% of $3,866,000 rounded base)

### 6.3 Contingency Rationale

High contingency reflects:
- Pre-conceptual design maturity (0% - no deliverable folders exist)
- 100% allowance/parametric pricing (no quotes or rate tables)
- Electrical load uncertainties (motor loads, process loads, building loads all TBD)
- Equipment sizing dependencies on loads from other packages (PKG-10, PKG-11, PKG-13, PKG-15)
- Cable routing lengths approximate (no equipment layout drawings)
- Grounding system sizing TBD (soil resistivity, grid sizing, touch/step potential)
- Hazardous area classification TBD (affects equipment ratings and cable types)

---

## 7. Exclusions and Assumptions

### 7.1 Key Exclusions

1. Lighting systems (PKG-18 Lighting)
2. Control system equipment and I/O modules (PKG-19 Control Systems, PKG-20 Field Instrumentation)
3. Building electrical distribution within MCC building (PKG-22 Building Interior & MEP)
4. Utility company service connection charges and metering equipment
5. Employer-responsible permits and approvals
6. Escalation beyond January 2026 pricing
7. Taxes and financing costs
8. Emergency generator or backup power systems (not mentioned in decomposition scope)

### 7.2 Key Assumptions

Documented in `Assumptions_Log.md` (A-1701 through A-1729). Summary:

- MV/LV Transformers: 2 units, 1000-1500 kVA each, pad-mounted, oil-filled
- MV Switchgear: 5-bay lineup, 5kV or 15kV class (depends on utility service)
- LV Switchgear: 480V or 600V (typical Canadian industrial), main-tie-main for reliability
- MCCs: 3 units distributed across facility areas for motor loads (pumps, agitators, unloading arms)
- Distribution Panels: 8 units for lighting, receptacles, small power
- UPS: 10 kVA for control system loads (DCS, HMI, instrumentation)
- Grounding: 1200m bare copper ground conductor, 15 driven electrodes, exothermic welds
- MV Cable: 800m total (5kV-15kV shielded EPR or XLPE)
- LV Cable: 3500m total (600V TECK90 or equivalent)
- Control Cable: 2500m (multi-conductor shielded)
- Cable Tray: 900m galvanized or stainless (marine areas)
- Conduit: 600m PVC and rigid for underground/embedded/local routing
- No hazardous area classification (Class I Div 2) unless ER specifies
- Utility service available at site boundary (no extensive service extension required)
- Standard industrial electrical installation productivity (no extreme access constraints)

---

## 8. Risks and Opportunities

### 8.1 Key Risks

Documented in `Risk_Register.md` (R-1701 through R-1708). Summary:

- **R-1701:** Actual motor loads significantly exceed assumptions (affects transformer/switchgear/MCC sizing)
- **R-1702:** Hazardous area classification required (affects equipment ratings and cable types)
- **R-1703:** Utility service voltage/configuration different than assumed (affects transformer and switchgear specifications)
- **R-1704:** Cable routing lengths significantly exceed estimates (affects material and labor costs)
- **R-1705:** Poor soil resistivity requiring enhanced grounding system (deep electrodes, ground enhancement material)
- **R-1706:** Equipment delivery lead times requiring schedule acceleration and premium pricing
- **R-1707:** ER requirements not extracted (may specify additional redundancy, monitoring, or special features)
- **R-1708:** Integration complexity with control systems and instrumentation packages

### 8.2 Potential Opportunities

- Optimization of equipment sizing through accurate load calculations
- Value engineering of MCC locations to minimize cable runs
- Competitive bidding for major electrical equipment
- Consolidation of electrical equipment procurement packages
- Use of modular/pre-fabricated electrical assemblies where applicable

---

## 9. Completeness Metrics

| Metric | Value | Target |
|--------|-------|--------|
| Deliverables with line items | 5/5 | 100% |
| Line items priced by QUOTE | 0% | 50%+ (future) |
| Line items priced by RATE_TABLE | 0% | 30%+ (future) |
| Line items priced by ALLOWANCE | 85.7% | < 30% (future) |
| Line items with Qty/Unit/UnitRate | 100% | 100% |
| CBS buckets covered | 8/8 | 100% |

**Status:** All deliverables and physical scope covered with allowances. No project-specific pricing sources available.

---

## 10. Recommendations

### 10.1 Immediate Actions to Improve Estimate

1. **Extract ER requirements** (Vol 2 Parts 1-3) for electrical design criteria and standards
2. **Develop load calculations** (DEL-17.03) to size transformers, switchgear, MCCs, cables
3. **Coordinate with other packages** for motor loads (PKG-10, PKG-11, PKG-15), building loads (PKG-21, PKG-22), and control system loads (PKG-19, PKG-20)
4. **Confirm utility service parameters** (voltage, capacity, connection point)
5. **Obtain budgetary quotes** for transformers, switchgear, and MCCs
6. **Develop preliminary electrical layout** (DEL-17.01) to refine cable routing lengths
7. **Conduct soil resistivity survey** for grounding system design
8. **Determine hazardous area classification** requirements (if any)

### 10.2 Next Estimate Iteration Triggers

- Load calculations complete (DEL-17.03)
- Electrical design drawings at 30% maturity (DEL-17.01)
- Vendor budgetary quotes received for transformers, switchgear, MCCs
- Equipment layout drawings available from other packages
- Utility service parameters confirmed

---

## 11. References

### 11.1 Decomposition

- Project decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- PKG-17 scope: Lines 435-449
- Deliverables: DEL-17.01 through DEL-17.05

### 11.2 Deliverable Folders

- No deliverable folders exist yet for PKG-17 (not yet scaffolded in execution workspace)

### 11.3 Configuration

- Estimate config: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md`

### 11.4 Decision and Assumption Logs

- `Decision_Log.md` (D-1701 through D-1708)
- `Assumptions_Log.md` (A-1701 through A-1729)

---

## 12. Approvals and Revisions

| Revision | Date | Description | Prepared By |
|----------|------|-------------|-------------|
| 0 | 2026-01-28 | Initial PKG-17 estimate snapshot | ESTIMATING Agent |

**Status:** DRAFT (Class 5, Order of Magnitude)

**Next Review:** After load calculations and 30% design drawings

---

**END OF BASIS OF ESTIMATE**
