# Specification: DEL-16.01 Valve Design Drawing Set

## Scope

This specification defines the requirements for **Valve Design Drawing Set** within **PKG-16 Valves & Specialty Equipment**.

**Purpose:** Defines the design arrangement and details for valves per ER requirements for the Canola Oil Transload Facility at Fraser Surrey Terminal.

**Source:** `_CONTEXT.md`

**Anticipated deliverable artifacts:**
- Valve arrangement drawings
- Actuator details

**Valve scope includes:**
- Control valves (flow, pressure, level control)
- Isolation valves (manual and automated)
- Relief valves (pressure and thermal relief)
- Strainers (Y-type, basket-type)
- Specialty items

**Source:** Decomposition document Section 5, PKG-16 scope (location TBD)

**Inclusions:**
- Valve location and orientation within process systems
- Valve-to-piping interface details
- Actuator mounting and installation arrangements
- Valve schedules and specifications cross-reference
- Access and maintenance clearances

**Exclusions:**
- Valve procurement specifications (see DEL-16.02 Valve Technical Specification)
- Valve sizing calculations (see DEL-16.03 Valve Design Calculations)
- Valve datasheets (see DEL-16.04 Valve Data Sheet Package)
- Process piping design (see DEL-14.01 Process Piping Design Drawing Set)

**Source:** Package structure from decomposition (exclusions inferred from related deliverables)

## Requirements

### Functional Requirements

**Drawing Content:**
1. Valve arrangement drawings shall show (see also Datasheet.md — Attributes section for valve categories):
   - Valve location and tag identification
   - Valve orientation and centerline elevation
   - Piping connection size and flanged rating (see Datasheet.md — Construction section for connection types)
   - Actuator type and mounting orientation (see Guidance.md — Section 2 "Actuator Integration" for selection principles)
   - Access requirements for operation and maintenance (see Guidance.md — Section 3 "Considerations" for accessibility factors)
   - Support and foundation requirements where applicable

2. Actuator detail drawings shall show (see also Procedure.md — Step 3 for detail development process):
   - Actuator type: pneumatic, electric, hydraulic, manual (see Datasheet.md — Attributes for applicable systems)
   - Mounting arrangement and interface to valve (see Guidance.md — Trade-offs for actuator type selection)
   - Actuator sizing basis and torque/thrust requirements (cross-reference to DEL-16.03 — Valve Design Calculations)
   - Control signal interfaces for automated valves (coordinate with DEL-19.01 — Control System Design)
   - Manual override provisions for automated valves (see Guidance.md — Principles for operability requirements)
   - Failure mode indication: fail-open (FO), fail-closed (FC), fail-as-is (FL) (see Guidance.md — Trade-offs for fail-safe mode selection)

**Source:** Typical valve drawing requirements for process facilities; specific requirements TBD pending design basis and ER review

**Drawing Standards:**
- All drawings shall comply with project CAD standards — **TBD**
- Drawing numbering per project drawing register — **TBD**
- Title block format per project requirements — **TBD**
- Revision control per project document management procedures — **TBD**

### Performance Requirements

**Design Criteria:**
- Valves shall be suitable for CSD canola oil service
- Operating temperature range: **TBD**
- Operating pressure range: **TBD**
- Valve sizing basis: **TBD** — To be consistent with DEL-16.03 (Valve Design Calculations)
- Seismic qualification: **TBD** — **ASSUMPTION**: Seismic Category per BC Building Code

**Source:** Product grade from decomposition Section 1.1; design parameters TBD pending system design

**Environmental Design:**
- Coastal/marine environment suitability — **ASSUMPTION**: Corrosion protection per ISO 12944 C4 or C5-M
- Ambient temperature range: **TBD** — Fraser Surrey Terminal climate data
- Hazardous area compliance: **TBD** — Per facility area classification study

**Actuation Performance:**
- Control valve response time: **TBD** — Per process control requirements
- Fail-safe mode: **TBD** — Per process hazard analysis
- Shutoff class: **TBD** — Per application (ANSI/FCI 70-2 or equivalent)

### Interface Requirements

**Piping Interface:**
- Valve flanged connections shall match piping specification (see DEL-14.02)
- Valve orientation shall maintain piping flexibility requirements
- Valve-to-pipe spacing shall accommodate piping stress analysis requirements

**Instrumentation Interface:**
- Control valve instrumentation (positioners, limit switches) — coordinate with DEL-20.01
- Valve position indication — coordinate with control system (DEL-19.01)

**Electrical Interface:**
- Electric actuator power supply — coordinate with DEL-17.01 (Electrical Power Design Drawing Set)
- Motor starter and control wiring — coordinate with DEL-19.01

**Structural Interface:**
- Large valve support requirements — coordinate with DEL-06.01 (Structural Steel Design Drawing Set)
- Foundation requirements for heavy valves — coordinate with DEL-05.01 (Concrete Structures Design Drawing Set)

**Source:** Interface requirements inferred from multi-discipline nature of valve installations; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

### Quality Requirements

**Drawing Quality:**
- All work shall comply with the project Quality Management Plan
- Drawings shall be checked and approved per project quality procedures
- Interdisciplinary coordination checks (IDC) required prior to issue
- Design review required for critical valves (relief valves, ESDs) — **TBD**

**CAD Standards:**
- CAD software: **TBD** — **ASSUMPTION**: AutoCAD or MicroStation per project standards
- Layer standards: **TBD** — Per project CAD manual
- Line weights and styles: **TBD** — Per project CAD manual
- Symbol libraries: **TBD** — Per project standards

**Deliverable Format:**
- Native CAD format (DWG or DGN) — **TBD**
- PDF for review and approval
- Revision clouds and triangles per project standards — **TBD**

## Standards

**Applicable codes and standards:**

**Valve Design:**
- API 600 — Steel Gate Valves
- API 6D — Pipeline Valves
- API 526 — Flanged Steel Pressure-Relief Valves
- API 527 — Seat Tightness of Pressure Relief Valves
- API 598 — Valve Inspection and Testing
- ASME B16.34 — Valves – Flanged, Threaded, and Welding End
- ISA-75.01 — Control Valve Sizing Equations

**Piping Interface:**
- ASME B31.3 — Process Piping
- ASME B16.5 — Pipe Flanges and Flanged Fittings

**Materials:**
- NACE MR0175/ISO 15156 — Materials for Sour Service (if applicable)
- ASTM A105/A350 — Carbon Steel Forgings
- ASTM A182 — Stainless Steel Forgings

**Actuators:**
- ISA-75.25 — Test Procedure for Control Valve Actuators
- IEC 60034 — Rotating Electrical Machines (electric actuators)
- NEMA Standards — Motor enclosures and ratings

**Canadian Codes:**
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code
- NBCC — National Building Code of Canada (seismic requirements)

**Project-Specific:**
- Employer's Requirements — **TBD** — **ASSUMPTION**: Volume 2 Parts 1–3 contain valve requirements
- Project CAD Standards Manual — **TBD**
- Project Engineering Standards — **TBD**

**Source:** Standards inferred from Mechanical discipline and valve scope; applicability to be confirmed during design development

## Verification

**Verification methods for Drawing deliverables:**

1. **Design Self-Check:**
   - Originator reviews drawing for completeness, accuracy, and compliance with standards
   - Check valve selections against DEL-16.04 (Valve Data Sheet Package)
   - Verify actuator sizing against DEL-16.03 (Valve Design Calculations)

2. **Interdisciplinary Check (IDC):**
   - Piping discipline review (interface with DEL-14.01)
   - Instrumentation discipline review (interface with DEL-20.01)
   - Electrical discipline review for electric actuators (interface with DEL-17.01)
   - Control systems review for control valves (interface with DEL-19.01)
   - Structural review for large valve supports (interface with DEL-06.01)

3. **Independent Check:**
   - Peer review by qualified checker (not the originator)
   - Dimensional verification
   - CAD standards compliance check
   - Drawing register and numbering verification

4. **Design Review:**
   - Discipline lead approval
   - Critical valve review (relief valves, emergency shutdown valves) — **TBD**
   - Vendor drawing review where applicable — **TBD**

**Acceptance criteria:**
- Drawing completeness per project drawing checklist — **TBD**
- Zero Category A comments from IDC — **TBD**
- CAD file check passes project standards — **TBD**
- All markups resolved and closed
- Approval signatures obtained per project authority matrix — **TBD**

**Source:** Typical engineering drawing verification process; specific criteria TBD pending project quality procedures

## Documentation

**Required documentation outputs:**

**Primary Deliverables:**
- Valve arrangement drawings (multiple sheets anticipated)
- Actuator detail drawings (typical details for pneumatic, electric, manual actuators)

**Supporting Documentation:**
- Drawing register / index
- Revision history log
- IDC comment/response log
- Design review minutes (for critical valves)

**Documentation requirements:**
- All documents shall comply with project document control procedures
- Document numbering per project numbering system — **TBD**
- Revision control: Initial issue Rev 0 or A, subsequent revisions per project convention — **TBD**
- Format: Native CAD + PDF — **TBD**
- **ASSUMPTION**: Electronic records in project document management system (e.g., Aconex, ProjectWise, SharePoint)

**Submittal Requirements:**
- 30% Design submittal — **TBD**
- 60% Design submittal — **TBD**
- 90% Design submittal — **TBD**
- IFC (Issued for Construction) — **TBD**

**Source:** Submittal milestones inferred from decomposition Section 5, PKG-27, DEL-27.04 (Design Submission Packages); specific requirements TBD

**Records Retention:**
- Retention period: **TBD** — **ASSUMPTION**: Project life + 25 years typical for design documents
- Archival format: **TBD** — **ASSUMPTION**: PDF/A for long-term preservation

**Source:** Records retention typical for EPC projects; specific requirements TBD per project procedures
