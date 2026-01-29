# Specification: DEL-21.03 Building Design Calculations

## Scope

This specification defines the requirements for **Building Design Calculations** within **PKG-21 Building Structures & Envelope**.

**Purpose:** Provides the engineering basis and sizing/verification calculations for building.
**Source:** Decomposition line 515

**Anticipated Calculation Artifacts:**
1. Building structural calculations — Member sizing, connection design
2. Foundation calculations — Footing/pile design, bearing/settlement analysis
3. Wind/seismic analysis — Lateral load analysis, drift verification

## Requirements

### Functional Requirements

**FR-01: Design Basis**
- Establish design criteria per NBC 2020 Part 4 (loads, materials, factors of safety)
- Document design assumptions and methodologies
- **TBD** — Design criteria document or basis of design

**FR-02: Load Calculations**
- Calculate all applicable loads: Dead, Live, Snow, Wind, Seismic
- Apply NBC 2020 load factors and load combinations
- **TBD** — Specific load values per site/occupancy

**FR-03: Structural Analysis**
- Perform structural analysis (2D/3D model or hand calculations)
- Determine member forces, reactions, deflections
- **TBD** — Analysis software and modeling assumptions

**FR-04: Member Design**
- Design structural members per CSA S16 (steel) or CSA A23.3 (concrete)
- Verify strength and serviceability (deflections, vibrations)
- Design connections per CSA S16, CSA W59

**FR-05: Foundation Design**
- Design foundations per geotechnical recommendations
- Verify bearing capacity and settlement limits
- Consider frost depth per NBC 2020

**FR-06: Lateral Systems**
- Design lateral load-resisting systems (braced frames, shear walls)
- Verify drift limits per NBC 2020 serviceability criteria
- Seismic design per NBC 2020 ductility requirements (if applicable)

### Performance Requirements

**PR-01: Code Compliance**
- Comply with NBC 2020 Part 4 structural provisions
- Comply with CSA S16 (steel) or CSA A23.3 (concrete)
- Comply with provincial building code amendments — **TBD**

**PR-02: Safety Factors**
- Use NBC 2020 factored resistance and load factors
- Material resistance factors per CSA S16/A23.3

**PR-03: Serviceability**
- Deflection limits: **TBD** — NBC 2020 or more stringent if required (L/360, L/240 typical)
- Vibration limits (if applicable): **TBD**
- Drift limits: **TBD** — NBC 2020 Part 4 Section 4.1.8.13

**PR-04: Durability**
- Design for coastal/marine environment (corrosion considerations)
- Design life: **TBD** — **ASSUMPTION**: 50 years typical

**PR-05: Professional Accountability**
- Calculations sealed by professional engineer licensed in BC (P.Eng.)
- Engineer assumes professional responsibility for design

### Interface Requirements

**IR-01: Coordination with Drawings**
- Member sizes in calculations match drawings (DEL-21.01)
- Connection details match drawings

**IR-02: Coordination with Specifications**
- Material properties in calculations match specifications (DEL-21.02)
- Steel grades, concrete strengths, connection types coordinated

**IR-03: Geotechnical Interface**
- Foundation design based on geotechnical investigation — **TBD**
- Soil bearing capacity, settlement criteria, frost depth

### Quality Requirements

**QR-01: Calculation Documentation**
- Calculations clearly documented with design criteria, assumptions, analysis, results
- Calculations traceable and checkable by independent reviewer
- Sketches/diagrams included where helpful

**QR-02: Independent Check**
- Calculations checked by qualified independent checker (P.Eng. or senior engineer)
- Check comments documented and resolved

**QR-03: Revision Control**
- Calculations revisioned per document control procedures
- Superseded calculations archived

## Standards

**Design Codes:**
- **NBC 2020** Part 4 — Structural Design
- **Provincial code** — **TBD**: BCBC or ABC amendments

**Material/Design Standards:**
- **CSA S16-19** — Design of Steel Structures
- **CSA A23.3-19** — Design of Concrete Structures
- **CSA W59-18** — Welded Steel Construction
- **CSA G40.20/G40.21** — Structural steel
- **CSA G30.18** — Reinforcing steel

**Analysis Software (if used):**
- **TBD** — ETABS, SAP2000, STAAD, RISA, or similar (validation/verification required)

**Employer's Requirements:**
- **TBD** — ER Volume 2 Part 3 (Building Works) — structural performance requirements

## Verification

**Verification Methods:**

**VM-01: Independent Check**
- Qualified checker (P.Eng.) reviews calculations
- Spot-checks critical elements
- Verifies design criteria, assumptions, code compliance

**VM-02: Peer Review**
- Senior structural engineer reviews design approach and results
- Reviews for reasonableness and compliance with good engineering practice

**VM-03: Software Validation** (if applicable)
- Analysis software validated against hand calculations or benchmark problems
- Model assumptions verified (supports, releases, load application)

**Acceptance Criteria:**
- Calculations complete and clear
- All design checks pass (strength, serviceability)
- Independent check complete with no unresolved comments
- Professional engineer seal and signature

## Documentation

**Required Outputs:**
1. **Building Structural Calculations** — Framing design, connection design
2. **Foundation Calculations** — Footing/pile sizing, bearing/settlement analysis
3. **Wind/Seismic Analysis** — Lateral load calculations, drift verification

**Supporting Documentation:**
- Design criteria summary
- Load calculations and combinations
- Analysis results (member forces, reactions, deflections)
- Design summary tables (member schedules)
- Sketches/diagrams

**Format:** **TBD** — PDF calculation packages with P.Eng. seal

**Lifecycle Management:** `1_Working/` → `2_Checking/` → `3_Issued/` per `_STATUS.md`
