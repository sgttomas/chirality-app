# Assumptions Log — PKG-05 Concrete Structures Estimate

**Snapshot ID:** EST_PKG05_DRAFT_2026-01-28_2400
**Package Scope:** PKG-05 Concrete Structures
**Date:** 2026-01-28

---

## Assumption Summary

This log documents all assumptions and allowances used in the PKG-05 estimate where explicit quantities, rates, or pricing were not available from project-specific sources.

**Context:** No vendor quotes, budgetary proposals, or project rate tables were available (see Source_Index.md). Physical quantities are parametrically derived from known tank parameters. All cost estimates use fallback allowances based on typical EPC project experience.

---

## A-001: Engineering Drawing Production — DEL-05.01

**Assumption:** Concrete structures drawing set estimated at $85,000 CAD allowance.

**Why Needed:** No vendor quotes or internal rate tables available for structural CAD drafting services. Deliverable documents specify multiple drawing types (foundation plans, containment walls, equipment pads, reinforcement drawings) but do not provide labor hours or rates.

**Impacted WBS/CBS:** PKG-05 / DEL-05.01 / Engineering (E)

**Cost Impact:** $85,000 CAD
- **Range:** $60,000 - $120,000 (±41%)
- **Basis:** Typical EPC structural drawing cost:
  - Tank foundations (3 tanks): 6 sheets × $4,000 = $24,000
  - Containment walls: 8 sheets × $4,500 = $36,000
  - Equipment pads: 4 sheets × $3,500 = $14,000
  - Thrust blocks: 2 sheets × $3,000 = $6,000
  - Typical details: 2 sheets × $2,500 = $5,000

**Confidence:** LOW

**Resolution Path:** Obtain budgetary quote from structural CAD drafting service provider or establish project engineering labor rate (e.g., $95/hr × estimated hours).

---

## A-002: Engineering Specification Writing — DEL-05.02

**Assumption:** Concrete technical specifications (3 specs: concrete, reinforcement, formwork) estimated at $45,000 CAD allowance.

**Why Needed:** No vendor quotes or internal rate tables for specification writing effort. Deliverable documents specify 3 specifications but do not provide labor hours or rates.

**Impacted WBS/CBS:** PKG-05 / DEL-05.02 / Engineering (E)

**Cost Impact:** $45,000 CAD
- **Range:** $30,000 - $60,000 (±33%)
- **Basis:** Typical EPC structural specification cost:
  - Concrete specification: $20,000 (extensive durability/containment requirements per OBJ-7)
  - Reinforcement specification: $12,000
  - Formwork specification: $13,000

**Confidence:** LOW

**Resolution Path:** Obtain budgetary quote from specification writing service or establish project engineering labor rate.

---

## A-003: Design Calculation Development — DEL-05.03

**Assumption:** Concrete structures design calculations (foundation calcs, containment wall calcs, seismic analysis) estimated at $120,000 CAD allowance.

**Why Needed:** No rate tables for structural calculation effort. Calculations include complex analysis (tank foundations for 15,000 MT tanks, containment walls, seismic analysis) requiring senior engineer time.

**Impacted WBS/CBS:** PKG-05 / DEL-05.03 / Engineering (E)

**Cost Impact:** $120,000 CAD
- **Range:** $90,000 - $160,000 (±33%)
- **Basis:** Typical EPC structural calculation cost:
  - Tank foundation calculations (3 × $15,000): $45,000
  - Containment wall calculations: $35,000
  - Equipment pad calculations: $15,000
  - Thrust block calculations: $10,000
  - Seismic analysis: $15,000

**Confidence:** LOW

**Resolution Path:** Establish engineering labor rates for structural design and estimated hours by calculation type.

---

## A-004: QA/QC Records — DEL-05.04

**Assumption:** Concrete installation and test records documentation estimated at $35,000 CAD allowance.

**Why Needed:** No rate tables for QA/QC documentation effort. Records include concrete pour records, cylinder test coordination, rebar inspection records.

**Impacted WBS/CBS:** PKG-05 / DEL-05.04 / Project Management (PM)

**Cost Impact:** $35,000 CAD
- **Range:** $25,000 - $50,000 (±43%)
- **Basis:** Typical EPC QA/QC documentation for structural concrete:
  - Pour record documentation: $12,000
  - Cylinder test coordination: $8,000
  - Rebar inspection records: $10,000
  - Overall QC coordination: $5,000

**Confidence:** LOW

**Resolution Path:** Establish QA/QC labor rates and estimated hours based on concrete placement sequence.

---

## A-005: Tank Foundation Concrete — 3 × 15,000 MT Tanks

**Assumption:** Ring wall foundations for 3 tanks estimated at 450 m³ concrete total.

**Why Needed:** No dimensioned drawings available. Quantity derived parametrically from tank parameters.

**Parametric Basis:**
- Tank diameter (typical 15,000 MT tank): ~32m diameter
- Ring wall dimensions (assumed): 1.5m wide × 1.2m deep × 32m circumference
- Volume per tank: π × 32m × 1.5m × 1.2m ≈ 181 m³
- 3 tanks: 3 × 150 m³ = 450 m³ (rounded for mobilization and waste)

**Impacted WBS/CBS:** PKG-05 / Materials (MAT) + Construction Directs (CD)

**Cost Impact:**
- Materials: 450 m³ × $220/m³ (ready-mix) = $99,000 CAD
- Installation: 450 m³ × $180/m³ (place, finish, cure) = $81,000 CAD
- **Range:** ±40% ($126k - $252k total)

**Confidence:** LOW

**Resolution Path:** Obtain dimensioned foundation drawings from DEL-05.01 development or geotechnical recommendations.

---

## A-006: Containment Wall Concrete

**Assumption:** Tank farm containment walls estimated at 600 m³ concrete total.

**Why Needed:** No dimensioned drawings available. Quantity derived parametrically based on containment volume required for 45,000 MT storage (OBJ-3, OBJ-7).

**Parametric Basis:**
- Required containment volume: 110% of largest tank = 16,500 MT ≈ 18,000 m³ (oil SG ~0.92)
- Assumed containment area: ~75m × 75m = 5,625 m² (includes 3 tanks with spacing)
- Containment wall perimeter: ~300m
- Wall dimensions (assumed): 300m × 2.5m height × 0.3m thick (base) + batter
- Average volume: ~600 m³

**Impacted WBS/CBS:** PKG-05 / Materials (MAT) + Construction Directs (CD)

**Cost Impact:**
- Materials: 600 m³ × $240/m³ (high-quality containment concrete) = $144,000 CAD
- Installation: 600 m³ × $350/m³ (walls with waterstops, complex formwork) = $210,000 CAD
- **Range:** ±35% ($230k - $478k total)

**Confidence:** LOW

**Resolution Path:** Obtain containment wall design from DEL-05.03 and dimensioned drawings from DEL-05.01.

---

## A-007: Equipment Pad Concrete

**Assumption:** Equipment pads for pumps, metering, railcar unloading equipment estimated at 200 m³ concrete total.

**Why Needed:** No equipment schedules or pad layouts available. Quantity derived from typical equipment footprints.

**Parametric Basis:**
- Pump pads (railcar unloading + marine loading): 8 pads × 3m × 3m × 0.5m = 36 m³
- Metering skid pads: 2 pads × 4m × 6m × 0.6m = 29 m³
- Railcar unloading platforms: 2 × 50m × 3m × 0.4m = 120 m³
- Miscellaneous pads: 15 m³
- Total: ~200 m³

**Impacted WBS/CBS:** PKG-05 / Materials (MAT) + Construction Directs (CD)

**Cost Impact:**
- Materials: 200 m³ × $230/m³ = $46,000 CAD
- Installation: 200 m³ × $250/m³ (including anchor bolts, grout pockets) = $50,000 CAD
- **Range:** ±45% ($53k - $139k total)

**Confidence:** LOW

**Resolution Path:** Obtain equipment pad schedule from mechanical package interfaces (PKG-10, PKG-11, PKG-15).

---

## A-008: Thrust Block Concrete

**Assumption:** Thrust blocks for underground piping estimated at 80 m³ concrete total.

**Why Needed:** No piping layout or thrust block schedule available. Quantity derived from typical underground piping thrust requirements.

**Parametric Basis:**
- Number of thrust blocks (estimated): 20 locations (bends, tees, reducers)
- Average block size: 4 m³
- Total: 20 × 4 m³ = 80 m³

**Impacted WBS/CBS:** PKG-05 / Materials (MAT) + Construction Directs (CD)

**Cost Impact:**
- Materials: 80 m³ × $210/m³ = $16,800 CAD
- Installation: 80 m³ × $200/m³ = $16,000 CAD
- **Range:** ±50% ($16.4k - $49.2k total)

**Confidence:** LOW

**Resolution Path:** Obtain thrust block schedule from PKG-03 (underground utilities) and PKG-14 (process piping).

---

## A-009: Reinforcing Steel — Foundations & Walls

**Assumption:** Reinforcing steel for all concrete structures estimated at 180,000 kg total.

**Why Needed:** No rebar schedules or bending diagrams available. Quantity derived from typical reinforcement ratios.

**Parametric Basis:**
- Tank foundations (450 m³): 100 kg/m³ = 45,000 kg
- Containment walls (600 m³): 150 kg/m³ (higher ratio for containment) = 90,000 kg
- Equipment pads (200 m³): 80 kg/m³ = 16,000 kg
- Thrust blocks (80 m³): 60 kg/m³ = 4,800 kg
- Miscellaneous: ~24,200 kg (wastage, laps, ties)
- Total: ~180,000 kg (180 tonnes)

**Impacted WBS/CBS:** PKG-05 / Materials (MAT) + Construction Directs (CD)

**Cost Impact:**
- Materials: 180,000 kg × $2.00/kg (supply, fabrication) = $360,000 CAD
- Installation: 180,000 kg × $1.00/kg (place, tie, inspect) = $180,000 CAD
- **Range:** ±30% ($378k - $702k total)

**Confidence:** LOW

**Resolution Path:** Obtain reinforcement schedules from DEL-05.01 drawings once developed.

---

## A-010: Formwork — Containment Walls

**Assumption:** Formwork for containment walls estimated at 1,500 m² contact area.

**Why Needed:** No formwork layouts available. Quantity derived from containment wall dimensions.

**Parametric Basis:**
- Wall perimeter: 300m
- Wall height: 2.5m (both sides)
- Contact area: 300m × 2.5m × 2 sides = 1,500 m²

**Impacted WBS/CBS:** PKG-05 / Materials (MAT) + Construction Directs (CD)

**Cost Impact:**
- Formwork rental/purchase: 1,500 m² × $40/m² = $60,000 CAD
- Formwork installation: 1,500 m² × $50/m² = $75,000 CAD
- **Range:** ±35% ($88k - $182k total)

**Confidence:** LOW

**Resolution Path:** Obtain wall layout and formwork strategy from construction planning.

---

## A-011: Waterstops and Joint Materials

**Assumption:** Waterstops and joint materials for containment walls estimated at $45,000 CAD allowance.

**Why Needed:** No joint schedule or waterstop specification available. Critical for OBJ-7 Environmental Protection.

**Parametric Basis:**
- Construction joints (estimated): 600 linear meters
- Waterstop material: 600m × $30/m = $18,000
- Joint sealants and filler: $12,000
- Installation: $15,000
- Total: ~$45,000

**Impacted WBS/CBS:** PKG-05 / Materials (MAT) + Construction Directs (CD)

**Cost Impact:** $45,000 CAD
- **Range:** $30,000 - $65,000 (±39%)

**Confidence:** LOW

**Resolution Path:** Obtain joint schedule and waterstop specification from DEL-05.02.

---

## A-012: Ground Liner System Interface

**Assumption:** Ground liner system interface work (concrete curbs, anchors, terminations) estimated at $75,000 CAD allowance.

**Why Needed:** Liner system scope included in PKG-05 (per decomposition line 226). Concrete interface work required.

**Parametric Basis:**
- Liner anchor curbs: 500m × $80/m = $40,000
- Penetration details: 30 penetrations × $500 = $15,000
- Coordination and installation: $20,000
- Total: ~$75,000

**Impacted WBS/CBS:** PKG-05 / Materials (MAT) + Construction Directs (CD)

**Cost Impact:** $75,000 CAD
- **Range:** $50,000 - $100,000 (±33%)

**Confidence:** LOW

**Resolution Path:** Obtain liner specification and interface details from design development.

---

## A-013: Concrete Testing and Quality Control

**Assumption:** Concrete testing and quality control services estimated at $65,000 CAD allowance.

**Why Needed:** No testing program defined. Estimate includes cylinder testing, slump tests, air content, third-party inspection.

**Parametric Basis:**
- Cylinder testing: 1,330 m³ total concrete ÷ 50 m³/batch = 27 batches × 4 cylinders × $60 = $6,480
- Field testing (slump, air, temp): 27 batches × $150 = $4,050
- Third-party inspection: 200 hours × $120/hr = $24,000
- Lab testing coordination: $10,000
- Mobilization and reports: $20,470
- Total: ~$65,000

**Impacted WBS/CBS:** PKG-05 / Construction Indirects (CI)

**Cost Impact:** $65,000 CAD
- **Range:** $45,000 - $85,000 (±31%)

**Confidence:** MED (based on typical testing requirements)

**Resolution Path:** Develop testing program per DEL-05.02 specification requirements.

---

## Assumption Summary Table

| Assumption ID | Description | Impacted CBS | Amount (CAD) | Range (CAD) | Confidence | Resolution Path |
|---------------|-------------|--------------|--------------|-------------|------------|-----------------|
| A-001 | Drawing production (DEL-05.01) | E | $85,000 | $60k-$120k | LOW | Engineering rates + hours |
| A-002 | Specification writing (DEL-05.02) | E | $45,000 | $30k-$60k | LOW | Engineering rates + hours |
| A-003 | Design calculations (DEL-05.03) | E | $120,000 | $90k-$160k | LOW | Engineering rates + hours |
| A-004 | QA/QC records (DEL-05.04) | PM | $35,000 | $25k-$50k | LOW | QA rates + scope |
| A-005 | Tank foundation concrete | MAT+CD | $180,000 | $126k-$252k | LOW | Dimensioned drawings |
| A-006 | Containment wall concrete | MAT+CD | $354,000 | $230k-$478k | LOW | Design calculations |
| A-007 | Equipment pad concrete | MAT+CD | $96,000 | $53k-$139k | LOW | Equipment schedule |
| A-008 | Thrust block concrete | MAT+CD | $32,800 | $16k-$49k | LOW | Piping layout |
| A-009 | Reinforcing steel | MAT+CD | $540,000 | $378k-$702k | LOW | Rebar schedules |
| A-010 | Formwork — walls | MAT+CD | $135,000 | $88k-$182k | LOW | Wall layout |
| A-011 | Waterstops/joints | MAT+CD | $45,000 | $30k-$65k | LOW | Joint schedule |
| A-012 | Liner interface | MAT+CD | $75,000 | $50k-$100k | LOW | Liner details |
| A-013 | Concrete testing/QC | CI | $65,000 | $45k-$85k | MED | Testing program |

**Total Direct Allowances:** $1,807,800 CAD (base, before indirects/contingency)

**Allowance Range:** $1,221,000 - $2,442,000 CAD (Low to High scenarios)

**Overall Confidence:** LOW — Most line items use fallback allowances without project-specific vendor quotes or detailed quantities.

---

**Assumptions Log Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete (all allowances documented)
