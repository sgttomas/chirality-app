# Guidance: DEL-21.03 Building Design Calculations

## Purpose

This guidance supports development of **Building Design Calculations** for **PKG-21 Building Structures & Envelope**.

**Deliverable Purpose:** Provides engineering basis and sizing/verification calculations for building.
**Source:** Decomposition line 515

**Role:** Calculations establish structural adequacy per NBC 2020, provide basis for drawings (DEL-21.01) and specifications (DEL-21.02), and demonstrate code compliance to authorities having jurisdiction.

**Project Objectives Supported:**
- **OBJ-1: Safe & Reliable Operation** — Structural design ensures safe building performance
- **OBJ-6: Regulatory Compliance** — Calculations demonstrate NBC 2020 compliance

## Principles

### P1: Limit States Design (NBC 2020)

NBC 2020 uses limit states design method:
- **Ultimate Limit State (ULS):** Factored loads ≤ Factored resistance (strength/stability)
- **Serviceability Limit State (SLS):** Service loads → acceptable deflections/vibrations

**Load Factors:** NBC 2020 Section 4.1.3 (1.4D, 1.5L, 1.5S, 1.4W, 1.0E with combinations)
**Resistance Factors:** CSA S16/A23.3 (ϕ factors for steel/concrete)

### P2: Seismic Design (Western Canada)

Surrey, BC is in seismic zone requiring seismic design:
- **NBC 2020 Part 4:** Seismic hazard parameters (Sa(0.2), Sa(1.0), Sa(2.0))
- **Ductile vs. Conventional:** Ductile design (Rd, Ro factors) for lower seismic demands
- **Site class:** From geotechnical investigation — **TBD**

### P3: Wind Load Analysis

**NBC 2020 Part 4 Wind Provisions:**
- Reference wind pressure (qref) for Surrey, BC — **TBD**
- Exposure factor (Ce) based on terrain
- Gust effect factor (Cg)
- External/internal pressure coefficients (Cp, Cpi)

### P4: Professional Accountability

BC requires professional engineer (P.Eng.) seal for structural design:
- Engineer assumes professional responsibility
- Calculations must be clear and checkable
- Professional liability for design errors

### P5: Coordination with Geotechnical

Foundation design requires geotechnical investigation:
- Soil bearing capacity
- Settlement criteria
- Frost depth
- Groundwater considerations
- **TBD** — Geotechnical report

## Considerations

### C1: Load Determination

**Dead Loads:** Self-weight of structure plus permanent components (envelope, equipment)
**Live Loads:** NBC 2020 Table 4.1.5.3 (industrial/storage occupancy loads)
**Snow Loads:** NBC 2020 climatic data for Surrey, BC — **TBD**
**Wind Loads:** NBC 2020 climatic data and analysis
**Seismic Loads:** NBC 2020 seismic hazard parameters — **TBD**

### C2: Structural System Selection

**Steel vs. Concrete:**
- Steel: Faster erection, lighter foundations, spans
- Concrete: Fire resistance, stiffness, economy for certain applications

**Pre-Engineered vs. Custom:**
- Pre-engineered: Manufacturer provides structural design
- Custom: Full engineer analysis and design

### C3: Connection Design

Connections often govern design:
- Bolted connections: CSA S16 bolt capacity, bearing, block shear
- Welded connections: CSA W59 weld capacity, effective throat
- Base plates: Anchor bolts, bearing on concrete

### C4: Serviceability Limits

**Deflection Limits (typical):**
- Beams/joists supporting plaster: L/360 under live load
- Beams/joists not supporting plaster: L/240 under live load
- **TBD** — More stringent limits if required

**Drift Limits (NBC 2020):**
- Structural drift under specified loads

## Trade-offs

### T1: Analysis Method — 3D Model vs. Hand Calculations

**3D Computer Model:**
- Advantages: Handles complex geometry, provides detailed results
- Disadvantages: Time to build model, software cost, validation required

**Hand Calculations:**
- Advantages: Transparent, easy to check
- Disadvantages: Tedious for complex structures

**Guidance:** Use 3D model for complex structures; hand calculations for simple/regular buildings.

### T2: Foundation Type

**Shallow Foundations:**
- Advantages: Lower cost if soil adequate
- Disadvantages: Settlement risk, frost depth requirements

**Deep Foundations (Piles):**
- Advantages: Reliable bearing, less settlement
- Disadvantages: Higher cost, specialized equipment

**Decision:** Based on geotechnical investigation.

## Examples

### E1: Typical Calculation Organization

1. **Cover Sheet** — Project, date, engineer seal, revisions
2. **Table of Contents**
3. **Design Criteria** — Loads, materials, codes
4. **Structural Analysis** — Load takedown, lateral analysis
5. **Member Design** — Beams, columns, connections
6. **Foundation Design**
7. **Appendices** — Computer output, sketches

### E2: Seismic Base Shear Calculation (NBC 2020)

V = S(Ta) × Mv × Ie / (Rd × Ro) × W

Where:
- S(Ta) = Spectral acceleration
- Mv = Higher mode factor
- Ie = Importance factor
- Rd, Ro = Ductility factors
- W = Seismic weight

**TBD** — Site-specific values

---

**Note:** This guidance is based on NBC 2020 structural provisions and CSA S16/A23.3 standards. Specific design requires site data, geotechnical investigation, and equipment loads.
