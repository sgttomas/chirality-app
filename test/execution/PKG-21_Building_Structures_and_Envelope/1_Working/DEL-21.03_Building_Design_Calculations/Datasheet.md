# Datasheet: DEL-21.03 Building Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-21.03 |
| Name | Building Design Calculations |
| Package | PKG-21 Building Structures & Envelope |
| Discipline | Buildings |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md` and Decomposition line 515

## Attributes

| Attribute | Value |
|-----------|-------|
| Calculation Number(s) | **TBD** — Per project numbering system |
| Analysis Software | **TBD** — **ASSUMPTION**: ETABS, SAP2000, STAAD, or similar for structural analysis; hand calculations for simpler elements |
| Design Codes | NBC 2020 Part 4, CSA S16, CSA A23.3 |
| Load Cases | **TBD** — Dead, Live, Snow, Wind, Seismic, Load Combinations per NBC 2020 |
| Foundation Design Method | **TBD** — Based on geotechnical investigation |
| Analysis Type | **TBD** — 2D/3D structural model, hand calculations |
| Professional Seal | **TBD** — P.Eng. (BC) required |
| Revision | **TBD** — Per document control |

## Conditions

**Project Context:**
Project: Canola Oil Transload Facility — Phase 1
Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Source:** Decomposition Section 1.1

**Deliverable Purpose:**
Provides the engineering basis and sizing/verification calculations for building.

**Source:** Decomposition line 515

**Anticipated Calculation Artifacts:**

Per decomposition (line 515):
1. **Building structural calculations** — Structural framing members, connections, load distribution
2. **Foundation calculations** — Foundation sizing, bearing capacity, settlement analysis
3. **Wind/seismic analysis** — Lateral load analysis, drift verification, base shear calculations

**Calculation Scope:**

**Loads (NBC 2020 Part 4):**
- Dead loads: Self-weight of structure and building components
- Live loads: Occupancy loads, equipment loads
- Snow loads: **TBD** — NBC 2020 climatic data for Surrey, BC
- Wind loads: **TBD** — NBC 2020 wind pressure for Surrey, BC
- Seismic loads: **TBD** — NBC 2020 seismic hazard for site (Western Canada seismic zone)
- Load combinations: NBC 2020 factored load combinations

**Structural Systems:**
- Structural framing: Steel or concrete or hybrid — **TBD**
- Connections: Bolted, welded, or hybrid per CSA S16 or CSA W59
- Roof structure: Beams, joists, purlins
- Wall framing: Columns, girts

**Foundation Systems:**
- Foundation type: **TBD** — Spread footings, piles, mat (based on geotechnical investigation)
- Bearing capacity analysis
- Settlement analysis
- Frost depth considerations

**Lateral Systems:**
- Wind resistance: Braced frames, moment frames, or shear walls
- Seismic resistance: NBC 2020 ductile/conventional design
- Drift limits: NBC 2020 serviceability criteria

**Material Properties:**
- Structural steel: **TBD** — CSA G40.21 grades (350W, 300W typical)
- Concrete: **TBD** — Compressive strength (25-35 MPa typical)
- Reinforcing steel: **TBD** — CSA G30.18 (400W typical)
- Soil bearing capacity: **TBD** — From geotechnical investigation

**Source:** NBC 2020 Part 4; CSA S16; CSA A23.3; typical building structural design

## Construction

**Calculation Content:**

**Structural Analysis:**
- Load takedown calculations (gravity loads to foundation)
- Lateral load distribution (wind and seismic)
- Structural model (if 3D analysis used) — **TBD**
- Member force diagrams

**Member Design:**
- Beam design: Flexure, shear, deflection checks
- Column design: Axial, bending, buckling checks
- Connection design: Bolts, welds, base plates
- Code compliance verification (CSA S16 or CSA A23.3)

**Foundation Design:**
- Footing/pile sizing
- Bearing pressure and settlement calculations
- Reinforcing design (if concrete foundations)
- Soil-structure interaction

**Wind/Seismic Analysis:**
- Wind pressure calculations (NBC 2020 Part 4)
- Seismic base shear (NBC 2020 Part 4)
- Lateral drift analysis
- P-delta effects (if applicable)

**Calculation Format:**
- **ASSUMPTION**: Calculation packages with cover sheet, table of contents, design criteria, analysis, member schedules, sketches/diagrams
- Professional engineer seal and signature
- Revision tracking

**Source:** Typical structural calculation organization; NBC 2020; CSA S16; CSA A23.3

## References

**Decomposition:** Line 515, PKG-21 section
**Deliverable Context:** `_CONTEXT.md`, `_REFERENCES.md`

**Design Codes:**
- **NBC 2020** — National Building Code of Canada 2020 Part 4 (Structural Design)
- **Provincial code** — **TBD**: BCBC or ABC

**Structural Design Standards:**
- **CSA S16-19** — Design of Steel Structures
- **CSA A23.3-19** — Design of Concrete Structures
- **CSA S6-19** — Canadian Highway Bridge Design Code (if applicable)
- **CSA G40.20/G40.21** — Structural steel material standards
- **CSA G30.18** — Reinforcing steel material standards

**Geotechnical:**
- **TBD** — Geotechnical investigation report (foundation design basis)

**Related Deliverables:**
- DEL-21.01: Building Design Drawing Set (drawings implement calculations)
- DEL-21.02: Building Technical Specification (material properties)
- DEL-21.04: Building Data Sheet Package

Dependencies coordinated externally per `_DEPENDENCIES.md` (NOT_TRACKED)
