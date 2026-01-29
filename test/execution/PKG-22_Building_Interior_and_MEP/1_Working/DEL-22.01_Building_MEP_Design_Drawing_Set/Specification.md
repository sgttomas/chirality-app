# Specification: DEL-22.01 Building MEP Design Drawing Set

## Scope

This specification defines the requirements for **Building MEP Design Drawing Set** within **PKG-22 Building Interior & MEP**.

**Deliverable Description:** Defines the design arrangement and details for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.01 entry; _CONTEXT.md

### Included

This drawing set shall include:

1. **HVAC layout** — Heating, ventilation, and air conditioning system design drawings
2. **Plumbing layout** — Domestic water, sanitary, and process water piping drawings
3. **Interior electrical layout** — Building interior lighting, receptacles, and small power distribution
4. **Fire suppression layout** — Automatic sprinkler system and fire protection equipment drawings

**Source:** Decomposition REVISED_v2.md, DEL-22.01 anticipated artifacts

### Excluded

The following are **excluded** from this deliverable and covered by other packages:

- Main electrical power distribution (covered by PKG-17 Electrical Power Distribution)
- Process piping systems (covered by PKG-14 Process Piping)
- Control system logic and programming (covered by PKG-19 Control Systems, though interfaces shall be shown)
- Building structure and envelope design (covered by PKG-21 Building Structures & Envelope)
- Site utilities and connections (covered by PKG-03 Site Services)

**Source:** Decomposition REVISED_v2.md, PKG-22 scope and adjacent package scopes; ASSUMPTION: standard EPC scope splits

### Scope Boundaries

**Per Decomposition Section 1.2:** "This decomposition covers the Contractor's scope of work only. Employer-responsible items (permits obtained by Employer, nitrogen skid supply) are excluded except for interface connections."

MEP drawings shall show interface connections to Employer-furnished systems but shall not include design of Employer-furnished equipment.

**Source:** Decomposition REVISED_v2.md, Section 1.2 Scope Focus

## Requirements

### Functional Requirements

#### HVAC System Requirements

- **FR-HVAC-01**: HVAC system shall maintain building interior design temperature and humidity per NBC 2020 and ASHRAE 90.1 requirements. **TBD** — Design setpoints per Employer's Requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "HVAC System Principles"
  - **Verification**: See Procedure.md, Step 2.1, Step 3.1 (design development and calculations)

- **FR-HVAC-02**: Ventilation rates shall comply with ASHRAE 62.1 for building occupancy type. **TBD** — Occupancy classification and ventilation rates (location TBD)
  - **Rationale**: See Guidance.md, Section "HVAC System Principles"
  - **Verification**: See Procedure.md, Step 3.1 (load calculations documented in DEL-22.03)

- **FR-HVAC-03**: HVAC system shall integrate with building automation system (BAS) per PKG-19 Control Systems interface requirements. **TBD** — Interface requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "Considerations - Coordination Requirements (PKG-19)"
  - **Verification**: See Procedure.md, Step 2.1, Step 3.1 (control interfaces and BAS integration)

**Source:** NBC 2020, ASHRAE 90.1, ASHRAE 62.1 (locations TBD)

#### Plumbing System Requirements

- **FR-PLUMB-01**: Domestic water supply shall provide adequate flow and pressure for all building fixtures. **TBD** — Flow rates and pressure requirements per fixture schedule (location TBD)
  - **Rationale**: See Guidance.md, Section "Plumbing System Principles"
  - **Verification**: See Procedure.md, Step 2.2, Step 3.2 (hydraulic calculations)

- **FR-PLUMB-02**: Sanitary drainage shall comply with NBC 2020 plumbing requirements and CSA B64 series standards. **TBD** — Specific standard editions (location TBD)
  - **Rationale**: See Guidance.md, Section "Plumbing System Principles"
  - **Verification**: See Procedure.md, Step 3.2 (drainage design and calculations)

- **FR-PLUMB-03**: Hot water system shall be provided if required by building occupancy. **TBD** — Hot water requirements per Employer's Requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "Plumbing System Principles"
  - **Verification**: See Procedure.md, Step 3.2 (equipment selection documented in DEL-22.04)

**Source:** NBC 2020, CSA B64 series (locations TBD)

#### Electrical (Building Services) Requirements

- **FR-ELEC-01**: Interior lighting shall provide illumination levels per NBC 2020 and applicable workplace standards. **TBD** — Illumination levels per space type (location TBD)
  - **Rationale**: See Guidance.md, Section "Electrical Building Services Principles"
  - **Verification**: See Procedure.md, Step 2.3, Step 3.3 (lighting design and calculations)

- **FR-ELEC-02**: Receptacle distribution shall serve anticipated equipment loads and allow for operational flexibility. **TBD** — Equipment list and power requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "Electrical Building Services Principles"
  - **Verification**: See Procedure.md, Step 3.3 (load calculations documented in DEL-22.03)

- **FR-ELEC-03**: Emergency lighting and exit signage shall comply with NBC 2020 life safety requirements. **TBD** — Emergency lighting design criteria (location TBD)
  - **Rationale**: See Guidance.md, Section "Electrical Building Services Principles"
  - **Verification**: See Procedure.md, Step 3.3 (emergency lighting layout)

**Source:** NBC 2020, CEC (Canadian Electrical Code) (locations TBD)

#### Fire Suppression Requirements

- **FR-FIRE-01**: Automatic sprinkler system shall comply with NFPA 13 and NBC 2020 requirements. **TBD** — Sprinkler system design criteria per Employer's Requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "Fire Suppression Principles"
  - **Verification**: See Procedure.md, Step 2.4, Step 3.4 (sprinkler design and hydraulic calculations)

- **FR-FIRE-02**: Fire suppression system shall be designed for building occupancy classification and commodity hazard per applicable codes. **TBD** — Occupancy and hazard classification (location TBD)
  - **Rationale**: See Guidance.md, Section "Fire Suppression Principles"
  - **Verification**: See Procedure.md, Step 1.2 (occupancy classification); Step 3.4 (design per NFPA 13)

- **FR-FIRE-03**: Fire protection water supply shall interface with site fire water system per PKG-03. **TBD** — Interface requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "Considerations - Coordination Requirements (PKG-03)"
  - **Verification**: See Procedure.md, Step 2.4 (coordinate with PKG-03)

**Source:** NFPA 13, NBC 2020 (locations TBD); PKG-03 interface (coordination TBD)

### Performance Requirements

#### Design Criteria

- **PR-01**: All MEP systems shall be designed for a minimum design life of **TBD** years (**ASSUMPTION**: 25 years per industrial facility practice)
  - **Rationale**: See Guidance.md, Section "Engineering Rationale" (Design Philosophy - Reliability)
  - **Verification**: See Procedure.md, Step 1.2 (establish design criteria); Datasheet.md (Design Life = 25 years assumed)

- **PR-02**: Seismic design shall comply with NBC 2020 for project site location (Surrey, BC). **TBD** — Site-specific seismic parameters (location TBD)
  - **Rationale**: See Guidance.md, Section "Fire Suppression Principles" (seismic bracing requirements)
  - **Verification**: See Procedure.md, Step 3.4 (seismic bracing per NBC 2020); Datasheet.md (Seismic Design Category TBD)

- **PR-03**: Energy efficiency shall meet or exceed ASHRAE 90.1 minimum requirements. **TBD** — Energy performance targets per Employer's Requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "Engineering Rationale" (Design Philosophy - Energy Efficiency); Trade-offs "Energy Efficiency vs. Capital Cost"
  - **Verification**: See Procedure.md, Step 3.1 (HVAC energy compliance)

- **PR-04**: Equipment selections shall consider lifecycle cost optimization per project objectives. **TBD** — Lifecycle cost criteria (location TBD)
  - **Rationale**: See Guidance.md, Trade-offs "Cost vs. Performance"
  - **Verification**: See Procedure.md, Step 3.1-3.4 (equipment selection and documentation in DEL-22.04)

**Source:** NBC 2020, ASHRAE 90.1 (locations TBD); Decomposition objectives (OBJ-6 Regulatory Compliance, OBJ-9 Lifecycle Cost Optimization inferred as relevant)

#### Reliability and Maintainability

- **PR-05**: MEP systems shall be designed for reliable operation in industrial canola oil transload facility environment.
- **PR-06**: Equipment shall be accessible for maintenance and service per applicable codes and good engineering practice.
- **PR-07**: Redundancy requirements: **TBD** — Per Employer's Requirements for critical systems (location TBD)

**Source:** ASSUMPTION: standard industrial facility reliability expectations; specific requirements TBD

### Interface Requirements

#### Interdisciplinary Coordination

- **IF-01**: MEP drawings shall coordinate with building structural drawings (PKG-21) for equipment supports, penetrations, and clearances.
- **IF-02**: HVAC control interfaces shall coordinate with PKG-19 Control Systems deliverables.
- **IF-03**: Electrical building services shall coordinate with main power distribution from PKG-17.
- **IF-04**: Fire protection water supply connections shall coordinate with site services (PKG-03).
- **IF-05**: MEP equipment installation shall follow building erection per Decision DEC-06: "MCC building equipment installed on-site after building erection."

**Source:** Decomposition REVISED_v2.md, DEC-06; package scope interfaces (coordination per `_DEPENDENCIES.md` NOT_TRACKED mode)

### Quality Requirements

#### Drawing Quality Standards

- **QR-01**: All drawings shall comply with project CAD Manual and drawing standards. **TBD** — CAD Manual reference (location TBD)
- **QR-02**: Drawing accuracy: Dimensions and locations shall be coordinated with architectural and structural drawings to within **TBD** mm tolerance.
- **QR-03**: All drawings shall undergo interdisciplinary check (IDC) before issue.
- **QR-04**: Checker qualifications: **TBD** — Per project Quality Management Plan (location TBD)

**Source:** ASSUMPTION: standard EPC drawing quality procedures; specific project requirements TBD

#### Design Quality

- **QR-05**: All designs shall be stamped by a Professional Engineer licensed in British Columbia (for NBC 2020 compliance).
- **QR-06**: Design calculations supporting drawings shall be documented per DEL-22.03 Building MEP Design Calculations.
- **QR-07**: Equipment selections shall be documented in data sheets per DEL-22.04 Building MEP Data Sheet Package.

**Source:** NBC 2020 professional seal requirements; cross-reference to related PKG-22 deliverables per Decomposition

## Standards

### Applicable Codes and Standards

**Primary Building Codes:**

- **NBC 2020** — National Building Code of Canada 2020
- **ABC 2019** — **TBD** — Identify full name and applicability (likely Alberta Building Code or municipal code) (location TBD)

**MEP Design Standards:**

- **ASHRAE 90.1** — Energy Standard for Buildings Except Low-Rise Residential Buildings (latest edition) (location TBD)
- **ASHRAE 62.1** — Ventilation for Acceptable Indoor Air Quality (latest edition) **TBD** (location TBD)
- **NFPA 13** — Standard for the Installation of Sprinkler Systems **TBD** (location TBD)
- **CSA B64** series — Plumbing standards **TBD** (location TBD)
- **CEC (CE Code)** — Canadian Electrical Code **TBD** (location TBD)

**Structural/Material Standards (for coordination):**

- **CSA A23.3** — Design of Concrete Structures
- **CSA S16** — Design of Steel Structures

**Source:** Decomposition REVISED_v2.md, inferred applicable standards for Buildings discipline; specific editions TBD per Employer's Requirements

### Employer's Requirements

- **Employer's Requirements Volume 2** — **TBD** — Project-specific requirements (location TBD; files noted as `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` but not to be read per instructions)

**Note:** Employer's Requirements shall take precedence over general standards where conflicts exist.

## Verification

### Verification Methods for Drawing Deliverables

**Design Verification:**

| Verification Activity | Description | Responsibility |
|----------------------|-------------|----------------|
| Self-Check | Originator reviews own work for completeness and accuracy | Design Engineer |
| Independent Check | Peer review by qualified checker | Senior Engineer / Checker |
| Interdisciplinary Check (IDC) | Coordination review across disciplines (architectural, structural, process, etc.) | IDC Coordinator |
| Design Review | Formal design review at key milestones (30%, 60%, 90%, IFC) | Design Manager |

**Drawing-Specific Checks:**

- **Dimensional verification**: Check dimensions, coordinates, elevations against architectural/structural base drawings
- **CAD standards compliance**: Verify drawing format, layering, line types, text standards per project CAD Manual
- **Equipment tag consistency**: Verify equipment tags match across drawings, datasheets (DEL-22.04), and specifications (DEL-22.02)
- **Specification compliance**: Verify designs comply with DEL-22.02 Building MEP Technical Specification
- **Calculation support**: Verify all design assumptions are supported by DEL-22.03 calculations

**Source:** ASSUMPTION: standard EPC drawing verification procedures; specific project procedures TBD

### Acceptance Criteria

**Drawing Completeness:**

- [ ] All required views, sections, and details are provided
- [ ] All equipment is shown with tags, schedules, and specifications
- [ ] All interface connections are clearly indicated
- [ ] All notes, legends, and symbols are complete and correct
- [ ] Drawing title block information is complete and accurate

**Design Compliance:**

- [ ] Design meets all functional requirements (Section: Requirements - Functional)
- [ ] Design meets all performance requirements (Section: Requirements - Performance)
- [ ] Design complies with all applicable codes and standards (Section: Standards)
- [ ] All interfaces are coordinated (Section: Requirements - Interface)

**Quality:**

- [ ] Drawing quality meets project CAD standards (QR-01)
- [ ] All checks completed and signed off (QR-03, QR-04)
- [ ] Professional Engineer seal applied (QR-05, where required by NBC 2020)

**Source:** ASSUMPTION: standard drawing acceptance criteria; specific project criteria TBD per Quality Management Plan

## Documentation

### Required Documentation Outputs

**Drawing Set Components (per Decomposition DEL-22.01 anticipated artifacts):**

1. **HVAC layout drawings**
2. **Plumbing layout drawings**
3. **Interior electrical layout drawings**
4. **Fire suppression layout drawings**

**Supporting Documentation:**

- Design calculations (see DEL-22.03 Building MEP Design Calculations)
- Equipment data sheets (see DEL-22.04 Building MEP Data Sheet Package)
- Technical specifications (see DEL-22.02 Building MEP Technical Specification)

**Source:** Decomposition REVISED_v2.md, DEL-22.01 through DEL-22.06 package scope

### Documentation Format and Control

- **Native CAD format**: **TBD** — Per project CAD standards (ASSUMPTION: DWG or similar)
- **Issued format**: PDF for issue to construction and review
- **Drawing numbering**: **TBD** — Per project drawing numbering system
- **Revision control**: All revisions tracked per project document control procedure; revision clouds and triangles per CAD standards
- **File naming**: **TBD** — Per project file naming convention

**Filing and retention:**

- Working files: `1_Working/` (this folder)
- Issued for review: `2_Checking/To/` (review copies with DEL-ID + date/rev)
- Issued for construction: `3_Issued/` (final issued copies)

**Source:** ASSUMPTION: standard project document control conventions per README.md Section 6; specific project procedures TBD
