# Specification: DEL-15.01 Pump Design Drawing Set

## Scope

This specification defines the requirements for the **Pump Design Drawing Set** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility at Fraser Surrey Terminal, Surrey, BC.

**Deliverable scope:** Defines the design arrangement and details for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.01 entry

### Included

The drawing set shall include:

1. **Pump arrangement drawings** — Overall layout, elevations, plan views, spacing
2. **Pump foundation details** — Foundation dimensions, anchor bolt layout, grout details, baseplate configuration
3. **Piping interface drawings** — Nozzle locations, sizes, orientations, flange details

**Source:** `_CONTEXT.md` (anticipated artifacts)

### Pump Types Covered

The drawing set shall cover all pumps required for the facility:

- Railcar unloading pumps
- Marine loading pumps
- Sump pumps
- Transfer pumps (if applicable)

**Source:** DEL-15.02 anticipated artifacts (pump specifications); specific pump count and duties TBD per ER Part 2

### Excluded

- Vendor pump internal design details (provided by pump manufacturer)
- Electrical motor internal drawings (covered under Electrical discipline packages)
- Control system logic and instrumentation details (covered under I&C discipline packages)
- Piping system design beyond immediate pump connections (covered under DEL-14.01–DEL-14.08)

**Source:** Decomposition Section 1.2 (Scope Focus: Contractor scope only); typical discipline boundaries

## Requirements

### Functional Requirements

#### FR-1: Support Project Objectives

The drawing set shall provide design information necessary to achieve:

- **OBJ-1 (Safe & Reliable Operation):** Drawings shall clearly show safe access, maintenance clearances, and proper support
- **OBJ-2 (Throughput Capacity):** Pump sizing and arrangement shall support 1,000,000 MT/annum facility throughput
- **OBJ-4 (Operational Flexibility):** Arrangement shall accommodate both tank storage and direct rail-to-ship transfer operations
- **OBJ-7 (Environmental Protection):** Drawings shall show containment provisions, leak detection interfaces, and spill prevention features (coordinate with civil/containment packages)

**Source:** Decomposition Section 2 (Objectives), Section 6 (Objective-Deliverable Mapping for PKG-15)

#### FR-2: Provide Complete Design Information

Drawings shall provide sufficient information for:

- Foundation design and construction (coordinate with PKG-05 Concrete Structures)
- Structural support design (coordinate with PKG-06 Structural Steelwork)
- Piping fabrication and installation (coordinate with DEL-14.01)
- Electrical installation (coordinate with Electrical packages)
- Equipment procurement (support DEL-15.04 Data Sheet Package)
- Construction and installation (support DEL-15.05 Installation & Test Records)

**Source:** Typical drawing deliverable purpose; cross-package coordination per engineering practice

#### FR-3: Represent As-Designed Condition

Drawings shall accurately represent the pump design arrangement, dimensions, and interfaces as determined by:

- System hydraulic calculations (DEL-15.03)
- Equipment specifications (DEL-15.02)
- Equipment data sheets (DEL-15.04)
- Site constraints and layout requirements

**Source:** Standard engineering documentation requirements; cross-reference to related PKG-15 deliverables

### Performance Requirements

#### PR-1: Drawing Content Standards

Drawings shall comply with:

- Project CAD standards — **TBD** (reference to project CAD standards document)
- Drawing title block requirements — **TBD** (per project document control procedures)
- Line types, symbols, and notation conventions — **TBD** (per project standards)
- Sheet size and scale conventions — **ASSUMPTION**: ISO A1 or ANSI D typical

**Source:** Industry practice; project-specific standards TBD

#### PR-2: Dimensional Accuracy

Drawings shall provide:

- Pump centerline dimensions and elevations (relative to project datum)
- Foundation dimensions and anchor bolt locations (tolerance per ACI 318 or CSA A23.3)
- Nozzle locations and orientations (coordinate with piping model)
- Clearance envelopes for installation, operation, and maintenance
- **Accuracy:** **TBD** — Drawing tolerance standards per project requirements

**Source:** API 610 Section 6.1 (installation requirements); dimensional accuracy TBD per project standards

#### PR-3: Coordination Accuracy

Drawings shall be coordinated with:

- Process piping drawings (DEL-14.01) — nozzle loads, piping support independence
- Foundation drawings (PKG-05) — anchor bolt embedment, foundation dimensions
- Structural steel drawings (PKG-06) — support steel connections (if elevated pumps)
- Electrical drawings (PKG-19/20) — motor terminal box orientation, conduit routing
- I&C drawings — instrument connections, local indication mounting

**Source:** Typical interdisciplinary coordination requirements; formal coordination per project procedures

### Interface Requirements

#### IF-1: Foundation Interface

Foundation drawings shall show:

- Foundation plan dimensions and elevation
- Anchor bolt pattern (number, size, material, embedment depth)
- Sleeve/blockout requirements for piping pass-throughs
- Grout pad dimensions and thickness
- Concrete strength requirements — **TBD** (per structural design)
- Reinforcement general notes (detailed design by structural engineer)

**Source:** API 610 Section 6.1.4 (grouting and alignment); ACI 318 / CSA A23.3 (foundation design)

#### IF-2: Piping Interface

Piping interface drawings shall show:

- Suction and discharge nozzle locations (coordinates relative to pump centerline/baseplate)
- Nozzle sizes and flange ratings (per ASME B16.5 and process conditions)
- Nozzle orientations (typical: suction horizontal, discharge vertical or as required)
- Flange face finish and gasket requirements
- Allowable nozzle loads — **TBD** (per pump vendor data and API 610 Section 4.2.9)
- Piping support requirements near pump connections

**Source:** API 610 Section 4.2.9 (nozzle loads), Section 6.2 (piping installation); ASME B31.3 (piping design)

#### IF-3: Electrical Interface

Electrical interface details shall show:

- Motor terminal box location and orientation
- Conduit entry points and sizes — **TBD** (coordinate with Electrical)
- Grounding lug locations
- Space heater connections (if applicable)
- Local disconnect location (if required)

**Source:** Typical mechanical-electrical interface requirements; details TBD via coordination with Electrical discipline

#### IF-4: Access and Maintenance Interface

Drawings shall show:

- Minimum clearances per API 610 Section 6.1.1 (adequate space for maintenance)
- Coupling guard removal envelopes
- Impeller/seal removal space requirements
- Platform access requirements (coordinate with PKG-06 if elevated)
- Lifting lug locations and capacities — **TBD** (per pump weight and rigging plan)

**Source:** API 610 Section 6.1.1 (clearances for maintenance); ASME B30.20 (rigging requirements)

### Quality Requirements

#### QR-1: Design Review and Checking

All drawings shall be subject to:

- Self-check by originator (completeness, accuracy, compliance with standards)
- Interdisciplinary check (IDC) — coordination with affected disciplines
- Independent check by qualified checker (technical review, code compliance)
- Approval by discipline lead or responsible engineer

**Source:** Standard engineering quality procedures; specific requirements TBD per project Quality Management Plan

#### QR-2: Document Control

Drawings shall comply with:

- Project document numbering system — **TBD**
- Revision control procedures — **TBD**
- Electronic file naming conventions — **TBD**
- Transmittal and distribution requirements — **TBD**

**Source:** Project document control procedures (TBD)

#### QR-3: As-Built Requirements

Drawings shall support as-built documentation:

- Maintain red-line markup provisions during construction
- Incorporate field changes per project change management procedures
- Final as-built drawings issued upon project completion — **TBD** (as-built requirements per ER Part 1)

**Source:** Standard as-built documentation practice; specific requirements TBD per ER Part 1

### Regulatory and Code Compliance

#### RC-1: Applicable Codes and Standards

Drawings shall comply with:

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
- **ASME B31.3** — Process Piping (for piping interface requirements)
- **ASME B16.5** — Pipe Flanges and Flanged Fittings (for flange specifications)
- **ACI 318** / **CSA A23.3** — Structural Concrete (for foundation design coordination)
- **NBC 2015** — National Building Code of Canada (structural and seismic requirements)
- **WorkSafeBC** — Occupational health and safety regulations (access, guarding, clearances)
- **CSA B51** — Boiler, Pressure Vessel, and Pressure Piping Code (if applicable to specific services)

**Source:** Standards typical for pump installations in Canadian industrial facilities; specific editions TBD per ER Part 1

#### RC-2: Environmental Compliance

Drawings shall show:

- Secondary containment provisions (coordinate with PKG-03 drainage and PKG-05 structures)
- Spill prevention features per OBJ-7 (Environmental Protection)
- Leak detection interfaces (coordinate with I&C packages)
- Drip pans or catch basins (if required by environmental regulations)

**Source:** OBJ-7 from decomposition; specific environmental requirements TBD per ER Part 1 and applicable environmental permits

#### RC-3: Seismic Design Compliance

Drawings shall reflect seismic design requirements:

- Anchor bolt design for seismic loads — **TBD** (per seismic calculations and NBC 2015)
- Flexible piping connections near pump nozzles (if required for seismic isolation)
- Equipment seismic bracing (if pumps are elevated or rack-mounted)

**Source:** NBC 2015 seismic provisions; specific requirements TBD per ER Part 1 seismic criteria and structural calculations

## Standards

### Primary Standards

- **API 610** (latest edition) — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
  - Section 4.2.9: Nozzle loads
  - Section 5: Design features
  - Section 6: Installation and testing
- **API 682** (latest edition) — Pumps—Shaft Sealing Systems for Centrifugal and Rotary Pumps
- **ASME B31.3** (latest edition) — Process Piping
- **ASME B16.5** (latest edition) — Pipe Flanges and Flanged Fittings

**Source:** Industry-standard codes for pump and piping design; specific editions TBD per project requirements

### Structural and Foundation Standards

- **ACI 318** — Building Code Requirements for Structural Concrete
- **CSA A23.3** — Design of Concrete Structures
- **CSA G40.21** — Structural Quality Steel (for baseplates)

**Source:** Foundation and structural interface requirements

### Canadian Codes and Regulations

- **NBC 2015** — National Building Code of Canada (structural loads, seismic, wind, snow)
- **WorkSafeBC** — Occupational Health and Safety Regulation
- **CSA B51** — Boiler, Pressure Vessel, and Pressure Piping Code

**Source:** Applicable Canadian regulations for BC industrial facilities

### Project-Specific Standards

- Project CAD Standards — **TBD** (location of project CAD standards document)
- Project Drawing Standards — **TBD**
- Project Document Control Procedures — **TBD**
- Employer's Requirements Volume 2 Parts 1 and 2 — **location TBD** (specific clauses for pump design requirements)

**Source:** Project-specific requirements (TBD)

## Verification

### Design Verification Methods

| Requirement Category | Verification Method | Acceptance Criteria |
|---------------------|---------------------|---------------------|
| Dimensional accuracy | Design review, dimensional check | Dimensions consistent with calculations and vendor data; tolerances per project standards |
| Code compliance | Independent check, code review | Compliance with API 610, ASME B31.3, NBC 2015, and applicable standards |
| Interdisciplinary coordination | IDC review, coordination meetings | No conflicts with piping, structural, electrical, or I&C drawings |
| Constructability | Constructability review | Installation sequence feasible; access and clearances adequate |
| Operability | Operability review | Maintenance access per API 610 Section 6.1.1; safe operation per WorkSafeBC |

**Source:** Standard engineering verification practices; API 610 Section 6.1.1 (installation clearances)

### Review and Approval Process

1. **Self-Check** — Originator reviews for completeness and accuracy
2. **Interdisciplinary Check (IDC)** — Affected disciplines review and comment
3. **Independent Check** — Qualified checker performs technical review
4. **Approval** — Discipline lead or responsible engineer approves for issue
5. **Client Review** — Submit to Employer for review and acceptance (if required by contract)

**Source:** Standard engineering quality procedures; specific process TBD per project Quality Management Plan

### Acceptance Criteria

Drawings shall be considered acceptable when:

- All self-check, IDC, and independent check comments are resolved
- Dimensional accuracy is verified against calculations and vendor data
- Code compliance is confirmed by checker
- Interdisciplinary coordination is confirmed by affected disciplines
- Constructability and operability are confirmed by reviewers
- Approval signatures are obtained per project procedures

**Source:** Standard engineering acceptance criteria; specific signoff requirements TBD per project Quality Management Plan

## Documentation

### Required Drawing Deliverables

1. **Pump Arrangement Drawings**
   - Overall layout plan view
   - Elevation views (minimum 2 orthogonal views)
   - Section views as required for clarity
   - Dimensions to pump centerlines and key features
   - Clearance envelopes for maintenance

2. **Pump Foundation Details**
   - Foundation plan and elevation views
   - Anchor bolt layout and details
   - Grout pad dimensions
   - Interface with structural concrete drawings
   - General notes and material specifications

3. **Piping Interface Drawings**
   - Nozzle schedule (size, rating, orientation, elevation)
   - Flange details and gasket specifications
   - Piping support requirements near pump
   - Interface with process piping drawings

**Source:** `_CONTEXT.md` anticipated artifacts; typical pump drawing content

### Drawing Format Requirements

- **Sheet size:** **TBD** — Per project standards (typical: ISO A1 or ANSI D)
- **Scale:** **TBD** — Appropriate for drawing type (typical: 1:50, 1:20, 1:10, NTS for details)
- **Title block:** Per project standards — **TBD**
- **Revision cloud and delta:** Per project standards — **TBD**
- **Electronic format:** **TBD** — Native CAD format + PDF

**Source:** Industry practice; project-specific requirements TBD

### Supporting Documentation

The drawing set shall be supported by:

- Design calculations (DEL-15.03)
- Equipment specifications (DEL-15.02)
- Equipment data sheets (DEL-15.04)
- Design basis memoranda (if applicable)
- Material take-off (MTO) for procurement support

**Source:** Standard engineering documentation hierarchy; cross-reference to related PKG-15 deliverables

### Record Management

- **Filing location:** `1_Working/DEL-15.01_Pump_Design_Drawing_Set/` during development; `2_Checking/` during review; `3_Issued/` upon approval
- **Revision control:** Per project document control procedures — **TBD**
- **Archiving:** Per project records management plan — **TBD**
- **Retention:** Per ER Part 1 requirements — **TBD** — **ASSUMPTION**: Minimum 25 years (typical for engineering records)

**Source:** Project document control procedures (TBD); retention per engineering records standards

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Equipment attributes, materials, conditions
- Guidance.md — Engineering principles and design considerations
- Procedure.md — Drawing production process and verification steps
- DEL-15.02 — Pump Technical Specification (performance and materials requirements)
- DEL-15.03 — Pump Design Calculations (sizing and NPSH verification)
- DEL-15.04 — Pump Data Sheet Package (vendor data integration)
- DEL-15.05 — Pump Installation & Test Records (installation verification)
