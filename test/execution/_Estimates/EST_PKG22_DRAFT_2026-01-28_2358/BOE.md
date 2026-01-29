# Basis of Estimate (BoE) — PKG-22 Building Interior & MEP

**Snapshot ID:** EST_PKG22_DRAFT_2026-01-28_2358
**Estimate Label:** PKG22_DRAFT
**Package Scope:** PKG-22 Building Interior & MEP
**Date:** 2026-01-28
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

**Total Estimate:** $2,133,000 CAD (rounded, includes contingency)
**Base Estimate:** $1,687,000 CAD (before contingency)
**Contingency:** $446,000 CAD (26% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW (100% allowance/parametric; no vendor quotes; building size TBD)
**Maturity:** Class 5 (Conceptual / Order of Magnitude)

---

## 1. Project Overview

### 1.1 Project Description

**Project:** Canola Oil Transload Facility — Phase 1 Design & Build Contract
**Employer:** DP World Fraser Surrey Inc.
**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Key Parameters:**
- Throughput: 1,000,000 MT per annum
- Storage: 45,000 MT (3 × 15,000 MT tanks)
- Product: CSD canola oil
- Contract: Design & Build

---

### 1.2 PKG-22 Scope

**Package Description:** Interior finishes, HVAC, plumbing, building electrical distribution, fire suppression

**Deliverables (6 total):**
- DEL-22.01: Building MEP Design Drawing Set (HVAC, plumbing, electrical, fire suppression layouts)
- DEL-22.02: Building MEP Technical Specification (HVAC, plumbing, fire suppression specs)
- DEL-22.03: Building MEP Design Calculations (loads, sizing, hydraulics)
- DEL-22.04: Building MEP Data Sheet Package (equipment data sheets)
- DEL-22.05: Building MEP Installation & Test Records (QA/QC, testing, commissioning)
- DEL-22.06: Building MEP Shop Design Drawing Set (shop drawings)

**Source:** Decomposition Section 5, PKG-22, lines 521-537

---

### 1.3 Building Context

**Building Type:** MCC building (Motor Control Center building)

**Building Size:** 300 m² (3,230 SF) assumed (TBD from PKG-21)

**Building Function:** MCC electrical equipment, control room, operator workstations, support facilities for canola oil transload operations

**Occupancy:** Low occupancy industrial (5-10 operators/staff typical per shift)

**Decision DEC-06:** "MCC building equipment installed on-site after building erection" (affects MEP installation sequencing)

**Source:** Decomposition Section 7 Decisions; PKG-22 scope; A-022 building size assumption

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

- **Engineering & Design (E):** Drawings, specifications, calculations, data sheets, shop drawing review for MEP systems
- **Materials (MAT):**
  - HVAC equipment (rooftop units or split systems, ductwork, diffusers, controls)
  - Plumbing fixtures and materials (fixtures, piping, water heater, backflow preventer)
  - Fire suppression system (automatic sprinklers, piping, alarm valve, trim)
  - Interior electrical (lighting fixtures, receptacles, panels, wiring, emergency lighting)
  - Interior finishes (flooring, wall finishes, ceilings)
- **Construction Directs (CD):** Installation labor and equipment for HVAC, plumbing, fire suppression, electrical, finishes
- **Construction Indirects (CI):** Field supervision, QA/QC, HSE, site overhead
- **Project Management (PM):** EPCM allocation, coordination
- **Procurement (P):** Vendor coordination, expediting
- **Commissioning (COM):** Testing, performance verification, handover

---

### 2.2 Exclusions

- Owner's costs, land, financing, Employer-obtained permits
- Other packages (PKG-00 through PKG-21, PKG-23 through PKG-35)
- Main electrical power distribution (covered by PKG-17 Electrical Power Distribution)
- Process piping and equipment (covered by other packages)
- Control system logic and programming (covered by PKG-19 Control Systems, though MEP interfaces shall be provided)
- Building structure and envelope (covered by PKG-21 Building Structures & Envelope)
- Site fire water loop (covered by PKG-23 Fire Protection)
- Escalation (January 2026 pricing basis)
- Taxes (GST/PST)

**Source:** `_CONFIG.md`; Decision D-005; Decomposition Section 1.2; PKG-22 scope boundaries

---

## 3. Pricing Sources and Methods

### 3.1 Source Hierarchy Applied

1. Vendor quotes: 0% (none available)
2. Rate tables: 0% (none available)
3. Allowances: 85% ($1,431k base)
4. Parametric factors: 15% ($256k base)

**Decision:** D-008 (use fallback model)

**Source Index:** See `Source_Index.md`

---

### 3.2 Fallback Model Disclosure

**Primary pricing basis:** Fallback typical model (no project-specific sources)

**Components used:**
- Allowance placeholders for materials and construction (A-001 through A-022)
- Indirects factors: CI=18%, P=2%, PM=6%, COM=3% (D-009)
- Contingency baseline by bucket with allowance-heavy adjustment (D-010)

**Transparency:** All uses labeled ALLOWANCE or PARAMETRIC with LOW/MED confidence and traced to assumptions/decisions

**Source:** AGENT_ESTIMATING fallback model, lines 643-691

---

## 4. Currency and Pricing Date

**Currency:** CAD (D-002) — project location Surrey, BC
**Pricing Date:** January 2026 (D-003) — current pricing
**Escalation:** NONE (D-009) — no escalation applied

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

- Design deliverables (DEL-22.01 through DEL-22.04, DEL-22.06) → Engineering (E)
- QA/QC records (DEL-22.05) → Construction Indirects (CI) / Commissioning (COM)
- Physical materials (HVAC equipment, plumbing materials, fire suppression components, electrical fixtures, finishes) → Materials (MAT)
- Installation work (HVAC, plumbing, fire suppression, electrical, finishes installation) → Construction Directs (CD)

**Source:** WBS_CBS_Matrix.csv; Decision D-011

---

### 5.2 Building Size Assumption (Critical)

**Assumption:** 300 m² (3,230 SF) MCC building

**Basis:** Typical industrial MCC building range 200-400 m² for 1,000,000 MT/a facility; 300 m² is mid-range baseline

**Impact:** All MEP system sizes and costs scale with building area

**Sensitivity:** ±33% building size variation → ±25-35% MEP cost variation

**Source:** A-022 (building size assumption); D-012 (building size decision)

**Resolution:** Complete PKG-21 DEL-21.01 building design drawings to determine actual floor area

---

### 5.3 Quantity Extraction

**Extracted:**
- Deliverable artifact counts (drawings, specs, calculations, data sheets)
- Qualitative scope descriptions (HVAC, plumbing, fire suppression, electrical, finishes)

**Not Extracted (TBD):**
- HVAC equipment capacities (DEL-22.03 load calculations pending)
- Plumbing fixture counts and piping quantities (DEL-22.01 layout pending)
- Fire sprinkler head counts and piping quantities (DEL-22.01 layout and DEL-22.03 hydraulics pending)
- Electrical lighting/receptacle counts (DEL-22.01 layout pending)
- Interior finishes quantities (PKG-21 building design and finish schedules pending)

**Impact:** Cannot create unit-rate-based QTO; forced to use LS allowances scaled to building size

**Source:** Exploration findings; Assumptions A-001 through A-005

---

### 5.4 Pricing Methodology

**Allowance Sizing (scaled to 300 m² building):**
- HVAC: $490k (equipment $295k + installation $195k) — 45-75 tons capacity; A-001
- Plumbing: $215k (materials $90k + installation $125k) — 8-12 fixtures, piping, water heater; A-002
- Fire suppression: $225k (materials $110k + installation $115k) — 40-60 sprinkler heads, wet-pipe system; A-003
- Interior electrical: $200k (materials $95k + installation $105k) — 30-50 lighting fixtures, 15-25 receptacles; A-004
- Interior finishes: $177k (materials $85k + installation $92k) — flooring, walls, ceilings; A-005
- Engineering: $124k (1,200-1,600 hours @ $140-175/hr blended) — A-006

**Calculated Indirects:**
- CI = 18% × CD ($632k) = $114k
- P = 2% × MAT ($675k) = $14k
- PM = 6% × (CD+CI+MAT) ($1,421k) = $85k
- COM = 3% × (CD+CI+MAT) ($1,421k) = $43k

**Source:** Assumptions_Log.md, Decision_Log.md

---

## 6. Location and Productivity

**Location:** Fraser Surrey Terminal, Surrey, BC

**Labor Market:** Vancouver/Lower Mainland BC rates
**Site Conditions:** Active marine terminal; MEP installation coordinated with PKG-00 site establishment and PKG-21 building erection
**Productivity:** Standard EPC productivity for industrial building MEP installation

**Adjustments:** Terminal operational interface may affect access and schedule (productivity reflected in labor hour assumptions)

**Source:** Assumptions A-010 (labor rates), A-012 (productivity), A-018 (site conditions)

---

## 7. Indirects Model

**Model:** Factor-based (D-006, D-009)

**Rationale:** No construction schedule available; factor-based appropriate for conceptual estimate

| Indirect | Factor | Base | Amount (CAD) |
|----------|--------|------|--------------|
| CI | 18% | CD=$632k | $114,000 |
| P | 2% | MAT=$675k | $14,000 |
| PM | 6% | CD+CI+MAT=$1,421k | $85,000 |
| COM | 3% | CD+CI+MAT=$1,421k | $43,000 |

**Source:** AGENT_ESTIMATING fallback factors (lines 643-652)

---

## 8. Contingency Method

**Method:** PCT_BY_BUCKET with allowance-heavy adjustment (D-010)

**Rates Applied:**

| CBS | Base (CAD) | Allowance Share | Baseline Rate | Adjustment | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|---------------|------------|------------|-------------------|
| E | $124,000 | 100% | 10% | +10% | 20% | $25,000 |
| MAT | $675,000 | 100% | 15% | +10% | 25% | $169,000 |
| CD | $632,000 | 100% | 20% | +10% | 30% | $190,000 |
| CI | $114,000 | 100% (factor) | 20% | +10% | 30% | $34,000 |
| P | $14,000 | 100% (factor) | 10% | +5% | 15% | $2,000 |
| PM | $85,000 | 100% (factor) | 10% | +5% | 15% | $13,000 |
| COM | $43,000 | 100% (factor) | 25% | +5% | 30% | $13,000 |

**Total Contingency:** $446,000 CAD (26%)

**Rationale:** Elevated rates due to:
- No vendor quotes (pricing uncertainty)
- Building size TBD (scope uncertainty)
- No design quantities (all deliverables INITIALIZED)
- Interface coordination risks (PKG-21, PKG-19, PKG-17, PKG-23)

**Source:** AGENT_ESTIMATING contingency model (lines 653-667); Risk_Register.md

---

## 9. Escalation

**Mode:** NONE (D-009)
**Rationale:** Current pricing (2026-01); no schedule available for escalation calculation
**Exposure:** 3-6% annual escalation over 2-3 year project = potential $84k-$202k addition (see Risk R-008)

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD (D-007)
**Application:** Summary totals only; Detail.csv retains calculated precision

---

## 11. Completeness Metrics

### Pricing Method Distribution

- ALLOWANCE: 85% ($1,431k)
- PARAMETRIC: 15% ($256k)
- QUOTE: 0%
- RATE_TABLE: 0%

### Quantity Extraction Success

- Deliverable counts: 100% (6/6)
- Building size: Assumed (300 m²)
- Physical quantities: 0% (all TBD)

---

## 12. Known Gaps

**Critical Gaps:**
1. No building design from PKG-21 (building size, room layouts, finish schedules)
2. No vendor quotes or rate tables
3. No HVAC load calculations (DEL-22.03 INITIALIZED)
4. No fire protection hydraulic calculations (DEL-22.03 INITIALIZED)
5. No plumbing fixture schedules (DEL-22.01 INITIALIZED)
6. No electrical load calculations (DEL-22.03 INITIALIZED)
7. Building occupancy classification TBD (affects plumbing, ventilation, fire suppression)
8. Control system interface scope split (PKG-19/PKG-22) TBD
9. Electrical power interface scope split (PKG-17/PKG-22) TBD
10. Fire water supply adequacy TBD (PKG-23 coordination required)

**Impact:** Estimate suitable for conceptual budgeting only

---

## 13. Key Assumptions Requiring Validation

1. **A-022:** Building size (300 m²) — $1,687k total base, 100% of estimate scales with building size
2. **A-001:** HVAC capacity (45-75 tons) — $490k, 29% of base
3. **A-003:** Fire suppression system (Light Hazard, 40-60 heads) — $225k, 13% of base; fire pump excluded (potential $80k-$150k add if required)
4. **A-002:** Plumbing fixtures (8-12 units) and hot water requirements — $215k, 13% of base
5. **A-005:** Interior finishes (industrial grade) — $177k, 10% of base
6. **A-004:** Interior electrical (30-50 lighting fixtures, 15-25 receptacles) — $200k, 12% of base

**Validation Path:** Complete PKG-21 building design; complete DEL-22.01 MEP design drawings; complete DEL-22.03 calculations; obtain vendor quotes

---

## 14. Supporting Documents

- Decision_Log.md (13 decisions)
- Assumptions_Log.md (22 assumptions)
- Source_Index.md (no pricing sources found; fallback model used)
- Detail.csv (19 lines, all fields populated)
- WBS_CBS_Matrix.csv (WBS-CBS mapping)
- Risk_Register.md (12 risks)
- QA_Report.md (Run Status: WARNINGS)
- Summary.md (CBS/deliverable breakdown)

**Traceability:** All line items traceable to assumptions or decisions

---

## 15. Estimate Preparation Process

**Method:** Automated straight-through pipeline per AGENT_ESTIMATING protocol

**Steps Completed:**
1. ✓ Initialize + auto-discover
2. ✓ Index sources (none found)
3. ✓ Map WBS → CBS
4. ✓ Extract quantities (deliverable counts only; physical quantities TBD)
5. ✓ Price line items (allowances scaled to building size)
6. ✓ Apply indirects (factor-based)
7. ✓ QA checks
8. ✓ Risk register + contingency
9. ✓ Publish snapshot

**Human Interaction:** None (straight-through)
**Decisions:** 13 documented
**Assumptions:** 22 documented

---

## 16. MEP System Breakdown

### HVAC System

**Scope:** Heating, ventilation, and air conditioning for 300 m² MCC building

**Equipment:** Packaged rooftop units or split systems (45-75 tons cooling; 250-400 MBH heating)

**Distribution:** Ductwork (200-350 LM), diffusers/grilles (40-60 units), controls, BAS integration

**Cost:** $490k (equipment $295k + installation $195k)

**Source:** A-001, A-007, A-014

---

### Plumbing System

**Scope:** Domestic water, sanitary drainage, hot water for 300 m² MCC building

**Fixtures:** 8-12 total (water closets, lavatories, sinks, safety shower/eyewash)

**Piping:** Domestic water (80-120 LM), sanitary drainage (60-100 LM)

**Equipment:** Water heater (150-300L if required), backflow preventer

**Cost:** $215k (materials $90k + installation $125k)

**Source:** A-002, A-008

---

### Fire Suppression System

**Scope:** Automatic wet-pipe sprinkler system per NFPA 13 Light Hazard for 300 m² building

**System:** 40-60 sprinkler heads, piping DN25-DN100 (150-250 LM), alarm valve, trim, flow/tamper switches

**Hydraulic Demand:** ~500-800 LPM @ 100-150 kPa (estimated; calculations TBD)

**Water Supply:** Connection to site fire water loop (PKG-23); fire pump excluded (may be required if supply inadequate)

**Cost:** $225k (materials $110k + installation $115k); excludes fire pump (+$80k-$150k if required)

**Source:** A-003, A-009, A-016

---

### Interior Electrical (Building Services)

**Scope:** Interior lighting, receptacles, small power distribution for 300 m² MCC building

**Lighting:** LED fixtures (30-50 units), emergency lighting (8-12 units)

**Power:** Receptacles (15-25 units), small power panels (2-3 units)

**Load:** 12-18 kW connected load for building services (excludes main MCC electrical load from process equipment)

**Cost:** $200k (materials $95k + installation $105k)

**Source:** A-004, A-015

---

### Interior Finishes

**Scope:** Flooring, wall finishes, ceilings for 300 m² MCC building (industrial grade)

**Flooring:** Sealed concrete or epoxy (300 m²)

**Walls:** Painted drywall or metal panels (150-200 m² wall area)

**Ceilings:** Suspended acoustic tile or exposed (50-80% coverage)

**Cost:** $177k (materials $85k + installation $92k)

**Source:** A-005, D-013

---

## 17. Interface Coordination Requirements

### PKG-21 (Building Structures & Envelope)

**Interface:** Building size, room layouts, equipment supports, penetrations, clearances

**Impact:** MEP system sizes scale with building area; equipment locations and supports coordinate with structure

**Coordination Required:** Early coordination to avoid rework

**Source:** A-017, Risk R-006

---

### PKG-19 (Control Systems)

**Interface:** HVAC equipment control interfaces, BAS integration

**Scope Split:** PKG-19 likely responsible for BAS controllers/network/HMI; PKG-22 responsible for equipment factory controls and interface points

**Coordination Required:** Clarify control system scope split; define interface points and responsibilities

**Source:** A-014, Risk R-007

---

### PKG-17 (Electrical Power Distribution)

**Interface:** Electrical load coordination, power distribution to building interior panels

**Scope Split:** PKG-17 likely responsible for service entrance/transformers/main panels; PKG-22 responsible for interior lighting/receptacle panels

**Coordination Required:** Clarify electrical scope split; coordinate electrical loads

**Source:** A-015

---

### PKG-23 (Fire Protection)

**Interface:** Fire water supply for building sprinkler system

**Coordination Required:** Verify site fire water supply adequacy (pressure and flow) for building sprinkler hydraulic demand; fire pump may be required if supply inadequate

**Source:** A-016, Risk R-003

---

## 18. Recommended Next Steps

**Immediate (Before Decision-Making):**
1. Complete PKG-21 DEL-21.01 building design drawings to determine actual building floor area and room layouts
2. Complete DEL-22.03 HVAC load calculations to size HVAC equipment
3. Complete DEL-22.03 fire protection hydraulic calculations to size sprinkler system and verify fire water supply adequacy
4. Obtain budgetary quotes for HVAC equipment, fire suppression system, plumbing equipment
5. Confirm building occupancy classification per NBC 2020

**Medium-Term:**
6. Complete DEL-22.01 MEP design drawings with equipment schedules, piping/ductwork routing, fixture layouts
7. Coordinate with PKG-19 (control systems), PKG-17 (electrical power), PKG-23 (fire protection) to clarify scope interfaces
8. Obtain Employer's Requirements Volume 2 Part 3 (Building Works)
9. Develop project rate tables for labor, equipment, materials
10. Re-run estimate to upgrade from Class 5 to Class 4/3

---

## 19. Approvals and Limitations

**Prepared By:** Estimating Agent (Automated)
**Reviewed By:** Not reviewed
**Approved By:** Not approved

**Limitations:**
- Conceptual budgeting and feasibility only
- NOT for contracting, procurement, GMP, or financing
- Expected accuracy: -30% / +50% (Class 5)
- Validity: January 2026 pricing; subject to escalation
- Building size assumption (300 m²) critical; estimate scales ±25-35% with ±33% building size variation

**Re-Estimate Triggers:**
- PKG-21 building design available (actual floor area)
- Vendor quotes obtained
- DEL-22.03 calculations complete (HVAC loads, fire sprinkler hydraulics, electrical loads)
- DEL-22.01 MEP design drawings complete (equipment schedules, piping/ductwork routing)
- Scope interfaces clarified (PKG-17, PKG-19, PKG-21, PKG-23)

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Snapshot:** EST_PKG22_DRAFT_2026-01-28_2358
