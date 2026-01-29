# Datasheet: DEL-15.01 Pump Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-15.01 |
| Name | Pump Design Drawing Set |
| Package | PKG-15 Pumps & Rotating Equipment |
| Discipline | Mechanical |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`, decomposition DEL-15.01

## Attributes

### Drawing Metadata

| Attribute | Value |
|-----------|-------|
| Drawing Number Prefix | **TBD** — Project numbering convention to be confirmed |
| Sheet Size | **ASSUMPTION**: ISO A1 or ANSI D (typical for mechanical arrangement drawings) |
| Scale | **ASSUMPTION**: Varies by drawing type (1:50, 1:20, 1:10, NTS for details) |
| CAD Standard | **TBD** — Project CAD standards document reference |
| Revision | **ASSUMPTION**: Rev 0 for initial issue |
| Classification | **TBD** — Per project document classification system |
| Drawing Types | Arrangement, foundation details, piping interfaces |

**Source:** Anticipated artifacts from `_CONTEXT.md`; drawing conventions ASSUMPTION based on industry practice

### Pump System Scope

| Attribute | Value |
|-----------|-------|
| Pump Types Covered | Railcar unloading pumps, marine loading pumps, sump pumps, transfer pumps |
| Design Capacity | **TBD** — Per ER Part 2 (process mechanical requirements) |
| Facility Throughput | 1,000,000 MT/annum (project objective OBJ-2) |
| Service | CSD canola oil transfer and handling |
| Number of Pumps | **TBD** — To be confirmed from ER Part 2 and system calculations |

**Source:** Decomposition Section 2 (OBJ-2), DEL-15.02 anticipated artifacts (pump types), project context

### Drawing Content

| Content Type | Description |
|--------------|-------------|
| Pump Arrangement | Overall layout, elevation views, plan views, spacing requirements |
| Foundation Details | Foundation dimensions, anchor bolt layout, grout details, pedestal/baseplate configuration |
| Piping Interface | Suction/discharge nozzle locations, sizes, orientations, flange details |
| Electrical Interface | **TBD** — Motor termination box location, conduit entry points (coordinate with Electrical discipline) |
| Access & Maintenance | Clearances for maintenance, removal envelopes, platform access |
| Structural Interface | **TBD** — Support steel connections (coordinate with Structural discipline) |

**Source:** Anticipated artifacts from `_CONTEXT.md`; typical pump drawing content per API 610 Section 6 (installation)

## Conditions

### Operating Context

**Facility parameters:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Service:** CSD canola oil transload facility
- **Throughput:** 1,000,000 MT/annum (OBJ-2)
- **Operations:** Tank storage and direct rail-to-ship transfer (OBJ-4)

**Source:** Decomposition Section 1 (Project Overview), Section 2 (Objectives)

### Environmental Conditions

| Condition | Value |
|-----------|-------|
| Ambient Temperature Range | **TBD** — Per ER Part 1 (site environmental data) |
| Seismic Design | **TBD** — Per ER Part 1 (seismic criteria) — **ASSUMPTION**: NBC 2015, Site Class per geotechnical |
| Wind Loading | **TBD** — Per ER Part 1 (wind criteria) |
| Snow/Ice Loading | **TBD** — Per ER Part 1 (snow load criteria) |
| Coastal/Marine Exposure | Yes (Fraser River terminal location) — consider corrosion protection |
| Hazardous Area Classification | **TBD** — Per facility hazardous area classification study (if applicable) |

**Source:** Project location (decomposition Section 1); seismic/environmental criteria TBD pending ER Part 1 clause extraction

### Design Life

| Parameter | Value |
|-----------|-------|
| Design Life | **TBD** — Per ER Part 1 (design life requirements) — **ASSUMPTION**: 25 years typical for industrial facilities |
| Maintenance Philosophy | **TBD** — To support OBJ-9 (Lifecycle Cost Optimization) |

**Source:** OBJ-9 from decomposition Section 2; design life TBD pending ER confirmation

## Construction

### Materials

| Component | Material Specification |
|-----------|------------------------|
| Pump Casing | **TBD** — Per ER Part 2 and API 610 material requirements for canola oil service |
| Impeller | **TBD** — Compatible with CSD canola oil (typically cast iron, ductile iron, or stainless steel) |
| Shaft | **TBD** — Per API 610 (typically 316 SS or equivalent) |
| Seal | **TBD** — Mechanical seal per API 682 |
| Baseplate | **ASSUMPTION**: Structural steel ASTM A36 or CSA G40.21 350W (typical) |
| Foundation | Concrete per ACI 318, CSA A23.3 — **TBD**: Mix design and reinforcement details |
| Piping Connections | **TBD** — Flange rating and material per ASME B16.5 and process conditions |

**Source:** API 610 (centrifugal pumps for petroleum, petrochemical and natural gas industries); material selection TBD pending ER Part 2 requirements and process data

### Configuration

| Feature | Description |
|---------|-------------|
| Pump Orientation | **TBD** — Horizontal or vertical configuration per space constraints and NPSH requirements |
| Driver Type | **ASSUMPTION**: Electric motor (typical for fixed installation) — confirm with Electrical package |
| Coupling Type | **TBD** — Flexible coupling per API 610 Section 5.4 |
| Baseplate Type | **TBD** — Fabricated steel baseplate or concrete sole plate |
| Mounting | **ASSUMPTION**: Floor-mounted on foundations (typical for process pumps) |

**Source:** API 610 standards for pump configurations; specific configuration TBD based on system design

### Installation Requirements

| Requirement | Description |
|-------------|-------------|
| Foundation Preparation | Level, clean, and properly cured concrete surface |
| Grouting | Non-shrink grout per manufacturer recommendations and API 610 Section 6.1.4 |
| Alignment | Shaft alignment per API 610 Section 6.3 (dial indicator method, laser alignment) |
| Piping Support | Piping independently supported to avoid imposing loads on pump nozzles (per API 610 Section 6.2) |
| Anchor Bolts | **TBD** — Size, material, embedment per structural calculations and foundation design |
| Electrical Connections | **TBD** — Coordinate with Electrical discipline (PKG-19, PKG-20) |

**Source:** API 610 Section 6 (installation requirements)

### Commissioning Requirements

| Activity | Description |
|----------|-------------|
| Pre-Start Checks | Rotation check, coupling alignment verification, lubrication system check |
| Performance Testing | **TBD** — Flow, head, power consumption per DEL-15.05 (Installation & Test Records) |
| Vibration Monitoring | Per API 610 Section 6.9 — acceptance criteria per ISO 10816 or API 610 Figure 15 |
| NPSH Verification | **TBD** — Verify available NPSH exceeds required NPSH per DEL-15.03 (calculations) |

**Source:** API 610 Section 6.9 (field performance test); cross-reference to DEL-15.03, DEL-15.05

## References

### Primary References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section 1: Project Overview, Section 2: Objectives, DEL-15.01 entry)
- **Context:** `_CONTEXT.md` (deliverable identity and anticipated artifacts)
- **Reference Index:** `PKG-15/0_References/_REFERENCE_INDEX.md`
- **Employer's Requirements:**
  - Volume 2 Part 1 (General Requirements) — **location TBD**: specific clauses for seismic, environmental, design life
  - Volume 2 Part 2 (Civil & Process Mechanical Works) — **location TBD**: pump performance requirements, materials, standards
  - Volume 2 Part 3 (Building Works) — if applicable

### Applicable Standards

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (11th Edition or later)
- **API 682** — Pumps—Shaft Sealing Systems for Centrifugal and Rotary Pumps
- **ASME B31.3** — Process Piping (piping interface requirements)
- **ASME B16.5** — Pipe Flanges and Flanged Fittings
- **ACI 318** / **CSA A23.3** — Building Code Requirements for Structural Concrete (foundation design)
- **CSA G40.21** — Structural Quality Steel (baseplate material)
- **ISO 10816** — Mechanical vibration—Evaluation of machine vibration by measurements on non-rotating parts
- **NBC 2015** — National Building Code of Canada (seismic and structural loads)

**Source:** Standards typical for mechanical pump design in Canadian industrial facilities; specific edition/year requirements TBD per ER Part 1

### Cross-References

- **DEL-15.02** — Pump Technical Specification (performance requirements, materials)
- **DEL-15.03** — Pump Design Calculations (NPSH, sizing, system curves)
- **DEL-15.04** — Pump Data Sheet Package (equipment data sheets)
- **DEL-15.05** — Pump Installation & Test Records (commissioning verification)
- **DEL-14.01** — Process Piping Design Drawing Set (piping interface coordination)
- **PKG-05** — Concrete Structures (foundation design coordination)
- **PKG-19/PKG-20** — Electrical packages (motor and power supply coordination)

**Source:** Dependencies inferred from deliverable scope and typical engineering coordination; formal dependency tracking per `_DEPENDENCIES.md` (NOT_TRACKED)

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle
