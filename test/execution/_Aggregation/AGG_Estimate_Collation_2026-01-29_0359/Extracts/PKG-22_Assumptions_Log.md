# Assumptions Log — PKG-22 Building Interior & MEP

**Snapshot ID:** EST_PKG22_DRAFT_2026-01-28_2358
**Package:** PKG-22 Building Interior & MEP
**Date:** 2026-01-28

---

## Purpose

This document records all assumptions and allowances used in the estimate when project-specific sources were not available.

---

## Assumption Entries

### A-001: HVAC System Capacity and Equipment

**Statement:** HVAC system for 300 m² MCC building requires approximately 45-75 tons of cooling and 250-400 MBH heating capacity, served by packaged rooftop units or split systems

**Why Needed:** No HVAC load calculations available (DEL-22.03 INITIALIZED); no equipment data sheets (DEL-22.04 INITIALIZED)

**Impacted WBS/CBS:** MAT (HVAC equipment), CD (HVAC installation)

**Cost Impact:** $185k (equipment) + $155k (installation) = $340k total

**Confidence:** LOW

**Resolution Path:** Complete DEL-22.03 HVAC load calculations; obtain budgetary quotes for HVAC equipment

**Basis:**
- Typical industrial MCC building: 15-25 W/m² cooling load; 60-100 W/m² heating load (BC climate)
- 300 m² building × 20 W/m² cooling = 6 kW (1.7 tons) per 10 m² → ~45-75 tons total for envelope + ventilation + internal gains
- Equipment: 2-3 packaged rooftop units @ $60k-$95k each OR split systems
- BC Lower Mainland climate (ASHRAE Zone 5): moderate heating/cooling loads

**Line Items:** L-006, L-010

---

### A-002: Plumbing Fixture Count and Equipment

**Statement:** MCC building requires 8-12 plumbing fixtures (water closets, lavatories, sinks, janitor sink, safety shower/eyewash), domestic water supply piping, sanitary drainage, and hot water heater (if required)

**Why Needed:** No plumbing layout (DEL-22.01 INITIALIZED); no fixture schedules

**Impacted WBS/CBS:** MAT (fixtures, piping, water heater), CD (plumbing installation)

**Cost Impact:** $45k (fixtures/materials) + $95k (installation) = $140k total

**Confidence:** LOW

**Resolution Path:** Complete DEL-22.01 plumbing layout; determine occupancy and fixture requirements per NBC 2020

**Basis:**
- NBC 2020 plumbing fixture requirements: Group F industrial occupancy
- Assumed 5-10 occupants: 2 water closets, 2 lavatories, 1 service sink, 1 janitor sink, safety shower/eyewash per industrial practice
- Domestic water piping: 80-120 LM total (DN20-DN50)
- Sanitary drainage: 60-100 LM (DN75-DN100)
- Electric water heater: 150-300 L capacity (if required for handwashing/cleanup)

**Line Items:** L-007, L-011

---

### A-003: Fire Suppression System (Automatic Sprinklers)

**Statement:** Automatic wet-pipe sprinkler system per NFPA 13 for 300 m² MCC building; Light Hazard occupancy; 40-60 sprinkler heads; hydraulic demand ~500-800 LPM @ 100-150 kPa

**Why Needed:** No fire protection design (DEL-22.01 INITIALIZED); no NFPA 13 hydraulic calculations (DEL-22.03 INITIALIZED)

**Impacted WBS/CBS:** MAT (sprinkler system components), CD (sprinkler installation)

**Cost Impact:** $65k (materials) + $85k (installation) = $150k total

**Confidence:** LOW

**Resolution Path:** Complete DEL-22.03 fire protection hydraulic calculations; coordinate with PKG-23 for site fire water supply adequacy; obtain sprinkler system design-build quote

**Basis:**
- NFPA 13 Light Hazard: 0.1 gpm/ft² over 1,500 ft² design area (typical for MCC/control buildings)
- 300 m² (3,230 SF) building: 40-60 sprinkler heads @ 12-15 SF/head coverage
- Wet-pipe system (no freezing risk in heated building)
- Sprinkler piping: DN25-DN100 (1"-4"), 150-250 LM total
- Hydraulic demand: ~500-800 LPM (130-210 GPM) @ 100-150 kPa (14-22 psi)
- Coordination with PKG-23 site fire water loop required

**Line Items:** L-008, L-012

---

### A-004: Interior Electrical (Building Services)

**Statement:** Interior electrical includes lighting (LED), receptacles, small power distribution panels, emergency lighting; 12-18 kW connected load for building services (excludes main MCC electrical load from process equipment)

**Why Needed:** No electrical layout (DEL-22.01 INITIALIZED); no electrical load calculations (DEL-22.03 INITIALIZED)

**Impacted WBS/CBS:** MAT (lighting fixtures, receptacles, panels), CD (electrical installation)

**Cost Impact:** $55k (materials) + $75k (installation) = $130k total

**Confidence:** LOW

**Resolution Path:** Complete DEL-22.01 interior electrical layout; complete DEL-22.03 electrical load calculations; coordinate with PKG-17 for power distribution adequacy

**Basis:**
- Lighting: 300 m² × 300-400 lux × 0.01 W/lux = 900-1,200 W (LED efficacy) → 30-50 LED fixtures @ $200-$400 each
- Receptacles: 15-25 receptacles (120V 15A) for general power
- Small power panels: 2-3 panels (lighting panel, receptacle panel)
- Emergency lighting: 8-12 battery backup units or emergency lighting inverter
- Excludes main MCC electrical distribution (PKG-17 scope)

**Line Items:** L-009, L-013

---

### A-005: Interior Finishes (Flooring, Walls, Ceilings)

**Statement:** Industrial-grade interior finishes for 300 m² MCC building: sealed concrete or epoxy flooring, painted drywall or metal panel walls, suspended acoustic tile or exposed ceiling

**Why Needed:** No building design drawings (PKG-21 DEL-21.01 INITIALIZED); no finish schedules

**Impacted WBS/CBS:** MAT (finish materials), CD (finishes installation)

**Cost Impact:** $48k (materials) + $72k (installation) = $120k total

**Confidence:** LOW

**Resolution Path:** Complete PKG-21 building design; complete DEL-22.01 MEP design with finish schedules; clarify finish levels with Owner

**Basis:**
- Flooring: Sealed concrete ($10-15/m²) OR epoxy coating ($30-50/m²) for 300 m²
- Walls: Painted drywall ($40-60/m²) OR pre-finished metal panels ($50-80/m²); 150-200 m² wall area estimated
- Ceilings: Suspended acoustic tile ($25-40/m²) for control/office areas OR exposed structure (painted) for equipment areas; 50-80% ceiling coverage
- Industrial finish level (not architectural grade)

**Line Items:** L-005, L-014

**Cross-reference:** D-013 (interior finishes scope interpretation)

---

### A-006: Engineering Design Effort (6 Deliverables)

**Statement:** Engineering effort for PKG-22 deliverables: 600-900 hours total for drawings, specifications, calculations, data sheets, shop drawing review

**Why Needed:** No engineering hour budget available; deliverables in INITIALIZED state

**Impacted WBS/CBS:** E (Engineering & Design)

**Cost Impact:** $114k total (blended rate $140-175/hr × 650-800 hours)

**Confidence:** LOW

**Resolution Path:** Develop engineering hour budget by deliverable and discipline; track actual hours during execution

**Basis:**
- DEL-22.01 Drawings: 150-250 hours (4-6 MEP disciplines, 8-15 sheets estimated)
- DEL-22.02 Specifications: 80-120 hours (3 spec sections: HVAC, Plumbing, Fire Suppression)
- DEL-22.03 Calculations: 100-150 hours (HVAC loads, plumbing sizing, fire sprinkler hydraulics, electrical loads)
- DEL-22.04 Data Sheets: 60-100 hours (equipment data sheets for HVAC, plumbing, fire suppression equipment)
- DEL-22.06 Shop Drawing Review: 80-120 hours (review vendor shop drawings)
- Blended engineering rate: $140-175/hr (senior engineer, intermediate engineer, CAD technician)

**Line Items:** L-001, L-002, L-003, L-004

---

### A-007: HVAC Ductwork and Distribution

**Statement:** HVAC ductwork for 300 m² building: 200-350 LM total ductwork (supply, return, exhaust) plus diffusers, grilles, dampers, insulation

**Why Needed:** No ductwork routing layout (DEL-22.01 INITIALIZED); no duct sizing calculations (DEL-22.03 INITIALIZED)

**Impacted WBS/CBS:** MAT (duct materials), CD (duct installation)

**Cost Impact:** Included in A-001 HVAC allowance ($340k)

**Confidence:** LOW

**Resolution Path:** Complete DEL-22.01 HVAC layout with duct routing; complete DEL-22.03 duct sizing per ASHRAE/SMACNA

**Basis:**
- Typical duct runs from rooftop units to interior spaces: 15-25 LM per unit × 10-15 branches = 200-350 LM total
- Duct sizes: DN200-DN600 (8"-24")
- Materials: Galvanized steel duct; fiberglass insulation (exterior duct); diffusers/grilles (40-60 units)
- SMACNA standards for duct construction

**Line Items:** Included in L-006, L-010

---

### A-008: Plumbing Piping Materials and Routing

**Statement:** Domestic water piping: copper Type L or PEX; sanitary drainage: PVC Schedule 40 or ABS; vent piping: PVC Schedule 40

**Why Needed:** No piping layout (DEL-22.01 INITIALIZED); no piping specifications (DEL-22.02 INITIALIZED)

**Impacted WBS/CBS:** MAT (piping materials), CD (piping installation)

**Cost Impact:** Included in A-002 plumbing allowance ($140k)

**Confidence:** LOW

**Resolution Path:** Complete DEL-22.01 plumbing layout; complete DEL-22.02 plumbing specification with material standards

**Basis:**
- Domestic water: Copper Type L (traditional) OR PEX (cost-effective); 80-120 LM
- Sanitary drainage: PVC Schedule 40 OR ABS; 60-100 LM
- NBC 2020 and CSA B64 plumbing code requirements
- Backflow preventer required for potable water protection

**Line Items:** Included in L-007, L-011

---

### A-009: Fire Sprinkler Piping and Fittings

**Statement:** Fire sprinkler piping: Schedule 40 black steel OR CPVC (if permitted); pipe sizes DN25-DN100 (1"-4"); grooved fittings or threaded fittings

**Why Needed:** No sprinkler layout (DEL-22.01 INITIALIZED); no material specification (DEL-22.02 INITIALIZED)

**Impacted WBS/CBS:** MAT (sprinkler piping), CD (sprinkler installation)

**Cost Impact:** Included in A-003 fire suppression allowance ($150k)

**Confidence:** LOW

**Resolution Path:** Complete DEL-22.01 fire protection layout; complete DEL-22.02 fire suppression specification; verify CPVC acceptability with AHJ

**Basis:**
- NFPA 13 sprinkler system materials: Schedule 40 black steel (traditional) OR CPVC (cost-effective for light hazard)
- Grooved mechanical fittings (Victaulic or similar) for DN50+ (2"+); threaded fittings for smaller sizes
- Alarm valve, trim, flow switches, tamper switches, test connection per NFPA 13
- 150-250 LM piping estimated

**Line Items:** Included in L-008, L-012

---

### A-010: Construction Labor Rates (BC Lower Mainland)

**Statement:** Construction labor rates for BC Lower Mainland: HVAC technician $65-85/hr; Plumber $70-90/hr; Sprinkler fitter $68-88/hr; Electrician $70-90/hr; General labor $45-60/hr (all-in rates including burden, benefits, overhead)

**Why Needed:** No project labor rate tables available

**Impacted WBS/CBS:** CD (Construction Directs)

**Cost Impact:** Significant; labor is 50-60% of construction directs

**Confidence:** MEDIUM

**Resolution Path:** Develop project labor rate tables based on union rates, market survey, or contractor quotes

**Basis:**
- BC Building Trades union rates (2026): journeyman rates $35-50/hr base + 70-85% burden = $60-90/hr all-in
- Lower Mainland BC market (Vancouver/Surrey area): tight labor market, industrial project rates
- Rates include: base wage, benefits, statutory costs, small tools allowance, contractor markup

**Line Items:** L-010, L-011, L-012, L-013, L-014

---

### A-011: Construction Equipment Rental Rates

**Statement:** Construction equipment rental for MEP installation: Aerial lift $250-400/day; Forklift $200-300/day; Welding machine $80-120/day; Hand tools and power tools included in labor burden

**Why Needed:** No project equipment rate tables available

**Impacted WBS/CBS:** CD (Construction Directs)

**Cost Impact:** Equipment is 5-10% of construction directs

**Confidence:** MEDIUM

**Resolution Path:** Develop project equipment rate tables based on rental market survey or contractor quotes

**Basis:**
- BC Lower Mainland equipment rental rates (2026)
- Aerial lifts required for HVAC equipment installation, ductwork, sprinkler installation, lighting
- Forklifts required for material handling and equipment placement
- Specialty tools (threading machines, grooving tools) typically contractor-furnished

**Line Items:** Included in CD line items (L-010 through L-014)

---

### A-012: MEP Installation Productivity

**Statement:** Productivity assumptions: HVAC installation 30-50 hours/ton; Plumbing installation 2-4 hours/fixture + 0.5-1.0 hours/m pipe; Sprinkler installation 0.8-1.2 hours/head + 0.4-0.6 hours/m pipe; Electrical installation 0.3-0.5 hours/fixture

**Why Needed:** No project-specific productivity data or historical data available

**Impacted WBS/CBS:** CD (Construction Directs)

**Cost Impact:** Significant; productivity drives labor hours and cost

**Confidence:** MEDIUM

**Resolution Path:** Use contractor historical productivity or obtain installation quotes

**Basis:**
- Industry-standard productivity rates for industrial buildings
- BC Lower Mainland conditions: skilled labor availability, moderate climate
- Productivity adjusted for new construction (not retrofit) and normal site access

**Line Items:** L-010, L-011, L-012, L-013, L-014

---

### A-013: Testing and Commissioning Scope

**Statement:** MEP testing and commissioning includes: HVAC TAB (test/adjust/balance), plumbing pressure testing, fire sprinkler hydrostatic and flow testing, electrical testing, functional performance testing, owner training

**Why Needed:** No commissioning plan available; no test procedures (DEL-22.05 INITIALIZED)

**Impacted WBS/CBS:** COM (Commissioning)

**Cost Impact:** $43k (3% of CD+CI+MAT per fallback factor)

**Confidence:** MEDIUM

**Resolution Path:** Develop commissioning plan per ASHRAE Guideline 1.1; clarify testing requirements with Owner and AHJ

**Basis:**
- ASHRAE Guideline 1.1 commissioning requirements
- NFPA 13 acceptance testing (hydrostatic, main drain test, trip test)
- NBC 2020 testing requirements for plumbing and building systems
- TAB services: independent testing firm or contractor self-perform

**Line Items:** L-018 (COM bucket)

---

### A-014: Control System Interfaces (Coordination with PKG-19)

**Statement:** HVAC equipment includes basic factory controls; BAS integration via hard-wired points or BACnet protocol; coordinate with PKG-19 for BAS programming and HMI graphics

**Why Needed:** No control system design (PKG-19 INITIALIZED); no HVAC control interface specifications (DEL-22.02 INITIALIZED)

**Impacted WBS/CBS:** MAT (HVAC equipment with controls), coordination effort in E

**Cost Impact:** Control interface cost included in A-001 HVAC allowance; BAS integration in PKG-19 estimate

**Confidence:** LOW

**Resolution Path:** Coordinate with PKG-19 control systems deliverables; clarify control system scope split between PKG-19 and PKG-22

**Basis:**
- Typical packaged HVAC equipment includes factory controls (thermostats, safeties)
- BAS integration for monitoring and setpoint adjustments requires interface points
- PKG-19 likely responsible for BAS controllers, network, HMI; PKG-22 responsible for field devices and equipment interfaces

**Line Items:** Coordination note only; cost impact in L-006 (HVAC equipment)

**Cross-reference:** PKG-19 Control Systems estimate

---

### A-015: Electrical Power Coordination (PKG-17 Interface)

**Statement:** Main electrical power distribution from PKG-17; PKG-22 includes interior electrical panels (lighting, receptacles) fed from PKG-17 main panels; electrical load coordination required

**Why Needed:** No electrical power distribution design (PKG-17 INITIALIZED); no electrical load summary (DEL-22.03 INITIALIZED)

**Impacted WBS/CBS:** MAT (interior panels), coordination effort in E

**Cost Impact:** Interior panel cost included in A-004 electrical allowance; main power distribution in PKG-17 estimate

**Confidence:** LOW

**Resolution Path:** Coordinate with PKG-17 electrical power distribution deliverables; clarify electrical scope split

**Basis:**
- PKG-17 typically responsible for service entrance, transformers, main switchgear/MCC
- PKG-22 responsible for building interior lighting, receptacles, small power panels
- Electrical load for HVAC equipment, pumps, fire alarm panel must be coordinated with PKG-17

**Line Items:** Coordination note only; cost impact in L-009 (electrical materials)

**Cross-reference:** PKG-17 Electrical Power Distribution estimate

---

### A-016: Fire Water Supply (PKG-23 Interface)

**Statement:** Fire water supply from site fire water loop (PKG-23); fire sprinkler system connection to site loop; hydraulic calculations require coordination to verify adequate pressure/flow

**Why Needed:** No site fire water design (PKG-23 INITIALIZED); no fire water supply data available

**Impacted WBS/CBS:** Coordination effort in E; fire suppression design in DEL-22.03

**Cost Impact:** Fire water connection included in A-003 fire suppression allowance; site fire water loop in PKG-23 estimate

**Confidence:** LOW

**Resolution Path:** Coordinate with PKG-23 fire protection deliverables; verify site fire water supply adequacy for building sprinkler demand

**Basis:**
- PKG-23 likely responsible for site fire water loop, hydrants, fire department connections
- PKG-22 responsible for building sprinkler system and connection to site loop
- NFPA 13 requires adequate water supply for sprinkler hydraulic demand plus hose stream allowance

**Line Items:** Coordination note only; cost impact in L-008 (fire suppression materials)

**Cross-reference:** PKG-23 Fire Protection estimate

---

### A-017: Building Coordination (PKG-21 Interface)

**Statement:** Building structure and envelope from PKG-21; MEP equipment supports, penetrations, and clearances must be coordinated with structural and architectural design

**Why Needed:** No building design (PKG-21 INITIALIZED)

**Impacted WBS/CBS:** Coordination effort in E; potential rework risk if coordination issues arise

**Cost Impact:** Coordination included in engineering allowance (A-006); rework risk noted in Risk_Register.md

**Confidence:** LOW

**Resolution Path:** Coordinate with PKG-21 building deliverables; establish interdisciplinary coordination process

**Basis:**
- MEP equipment locations, roof penetrations, wall/floor penetrations must be coordinated with PKG-21
- Equipment supports (HVAC curbs, seismic bracing) require structural coordination
- Standard interdisciplinary coordination requirement for building projects

**Line Items:** Coordination note only

**Cross-reference:** PKG-21 Building Structures & Envelope

---

### A-018: Site Conditions and Access

**Statement:** Normal site access for MEP installation; active marine terminal operations may require coordination for material deliveries and equipment placement; laydown area available per PKG-00

**Why Needed:** No site logistics plan available; no construction execution plan

**Impacted WBS/CBS:** CD (Construction Directs) - productivity impact; CI (Construction Indirects) - site overhead

**Cost Impact:** Site coordination included in CI allowance; productivity impact reflected in A-012

**Confidence:** MEDIUM

**Resolution Path:** Develop construction execution plan with site logistics; coordinate with PKG-00 site establishment

**Basis:**
- Active terminal operations per Decomposition OBJ-5 (Terminal Continuity)
- Material deliveries and equipment placement may require off-hours or coordinated access
- Laydown area and temporary facilities per PKG-00 scope

**Line Items:** Impact included in L-015 (CI bucket)

**Cross-reference:** PKG-00 Site Establishment

---

### A-019: Environmental and HSE Compliance

**Statement:** Standard HSE requirements for industrial construction; environmental controls for MEP installation (waste disposal, spill prevention); compliance with PKG-33 HSE Management deliverables

**Why Needed:** No HSE plan available (PKG-33 INITIALIZED)

**Impacted WBS/CBS:** CI (Construction Indirects) - HSE oversight included in CI factor

**Cost Impact:** HSE included in CI allowance (18% of CD)

**Confidence:** MEDIUM

**Resolution Path:** Coordinate with PKG-33 HSE Management deliverables

**Basis:**
- BC WorkSafeBC requirements for construction safety
- Environmental compliance for waste disposal (packaging, scrap materials, test water)
- Standard HSE practices for industrial facility construction

**Line Items:** Impact included in L-015 (CI bucket)

**Cross-reference:** PKG-33 HSE Management

---

### A-020: Warranty and Spare Parts

**Statement:** Equipment warranties per manufacturer standard (1-2 years typical); extended warranties and spare parts recommendations per DEL-22.04 data sheets (when completed)

**Why Needed:** No warranty requirements specified; no equipment data sheets (DEL-22.04 INITIALIZED)

**Impacted WBS/CBS:** MAT (equipment procurement)

**Cost Impact:** Standard manufacturer warranty included in equipment pricing (no cost impact)

**Confidence:** MEDIUM

**Resolution Path:** Clarify warranty requirements with Owner; document in DEL-22.02 specifications and DEL-22.04 data sheets

**Basis:**
- HVAC equipment: 1-year parts and labor (standard); 5-year compressor warranty (typical)
- Plumbing fixtures: 1-year to lifetime (varies by manufacturer)
- Fire suppression equipment: 1-year installation warranty
- Extended warranties available at additional cost

**Line Items:** Note only; no cost impact assumed

---

### A-021: Shop Drawings and Submittals

**Statement:** Shop drawings required for HVAC equipment, fire sprinkler system, major plumbing equipment; submittal review effort included in engineering allowance (A-006)

**Why Needed:** No submittal requirements defined (DEL-22.02 INITIALIZED); no shop drawing scope (DEL-22.06 INITIALIZED)

**Impacted WBS/CBS:** E (Engineering & Design) - review effort

**Cost Impact:** Review effort included in A-006 engineering allowance ($114k)

**Confidence:** LOW

**Resolution Path:** Complete DEL-22.02 specifications with submittal requirements; allocate shop drawing review hours

**Basis:**
- Typical shop drawings: HVAC equipment layouts, ductwork fabrication, sprinkler system layout, plumbing equipment
- Review effort: 80-120 hours (included in A-006)

**Line Items:** Included in L-001 through L-004 (Engineering)

---

### A-022: Building Size for MEP Allowance Scaling

**Statement:** 300 m² (3,230 SF) MCC building size used for MEP system sizing and allowance scaling

**Why Needed:** No building floor area available from PKG-21 deliverables (INITIALIZED state)

**Impacted WBS/CBS:** All MEP line items

**Cost Impact:** Significant; all MEP allowances scaled to building size

**Confidence:** LOW

**Resolution Path:** Complete PKG-21 DEL-21.01 building design drawings to determine actual building floor area

**Basis:**
- Typical MCC building for 1,000,000 MT/a facility: 200-400 m² range
- 300 m² is mid-range baseline suitable for conceptual budgeting
- Actual building size may vary -33% to +33% from this assumption

**Line Items:** All MEP line items (L-005 through L-014)

**Cross-reference:** D-012 (building size assumption decision)

---

## Assumption Summary by Impact

| Assumption ID | Topic | Impact Level | Cost Impact | Confidence |
|---------------|-------|--------------|-------------|------------|
| A-001 | HVAC capacity & equipment | High | $340k | LOW |
| A-002 | Plumbing fixtures & equipment | High | $140k | LOW |
| A-003 | Fire suppression system | High | $150k | LOW |
| A-004 | Interior electrical | Medium | $130k | LOW |
| A-005 | Interior finishes | Medium | $120k | LOW |
| A-006 | Engineering effort | High | $114k | LOW |
| A-007 | HVAC ductwork | Medium | Included in A-001 | LOW |
| A-008 | Plumbing piping materials | Medium | Included in A-002 | LOW |
| A-009 | Fire sprinkler piping | Medium | Included in A-003 | LOW |
| A-010 | Construction labor rates | High | 50-60% of CD | MEDIUM |
| A-011 | Equipment rental rates | Low | 5-10% of CD | MEDIUM |
| A-012 | MEP installation productivity | High | Drives CD hours | MEDIUM |
| A-013 | Testing & commissioning scope | Medium | $43k | MEDIUM |
| A-014 | Control interfaces (PKG-19) | Medium | Coordination | LOW |
| A-015 | Electrical power (PKG-17) | Medium | Coordination | LOW |
| A-016 | Fire water supply (PKG-23) | Medium | Coordination | LOW |
| A-017 | Building coordination (PKG-21) | Medium | Rework risk | LOW |
| A-018 | Site conditions & access | Medium | Productivity impact | MEDIUM |
| A-019 | Environmental & HSE | Low | Included in CI | MEDIUM |
| A-020 | Warranty & spare parts | Low | No cost impact | MEDIUM |
| A-021 | Shop drawings review | Low | Included in A-006 | LOW |
| A-022 | Building size (300 m²) | High | All MEP allowances | LOW |

---

**Total Assumptions:** 22

**Assumptions with HIGH cost impact:** 6 (A-001, A-002, A-003, A-006, A-010, A-012, A-022)

**Assumptions Log Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Snapshot:** EST_PKG22_DRAFT_2026-01-28_2358
**Status:** Complete
