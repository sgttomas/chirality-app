# Guidance: DEL-22.01 Building MEP Design Drawing Set

## Purpose

This guidance document supports the development of **Building MEP Design Drawing Set** for **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Defines the design arrangement and details for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.01 entry; _CONTEXT.md

### Role in Project Delivery

This drawing set serves as the definitive design record for building mechanical, electrical, and plumbing systems. It provides:

- **Design intent communication** to construction contractors and trades
- **Coordination basis** for interdisciplinary design integration (structural, architectural, process)
- **Construction guidance** for installation of MEP systems
- **Regulatory compliance documentation** for building permit and NBC 2020 code compliance
- **As-built basis** for future operations and maintenance (updated during construction)

**Deliverable Classification:**
- **Type:** Drawing
- **Discipline:** Buildings
- **Responsible Party:** D&B Contractor

**Source:** Standard EPC deliverable purposes; _CONTEXT.md

## Principles

### Engineering Rationale for MEP Building Systems

**Building Function Context:**

The building MEP systems support the operational requirements of the canola oil transload facility, primarily serving the MCC (Motor Control Center) building which houses electrical equipment and potentially control rooms or other support spaces.

**Design Philosophy (ASSUMPTION: to be confirmed with Employer's Requirements):**

1. **Reliability**: MEP systems shall support continuous facility operations with minimal downtime
2. **Maintainability**: Equipment and systems shall be accessible and serviceable
3. **Energy Efficiency**: Design shall meet or exceed ASHRAE 90.1 requirements while optimizing lifecycle costs
4. **Code Compliance**: All systems shall comply with NBC 2020, provincial codes, and local authority requirements
5. **Integration**: MEP systems shall integrate seamlessly with facility-wide control and monitoring systems (PKG-19)

**Source:** ASSUMPTION: standard industrial facility design principles; to be confirmed per project-specific requirements

### MEP System Design Principles by Discipline

#### HVAC System Principles

**Climate Context**: Surrey, BC location requires heating for winter conditions and potentially cooling for internal heat loads from electrical equipment.

**Design Approach** (ASSUMPTION):
- Provide adequate ventilation for equipment cooling and occupant comfort
- Consider heat recovery where economically justified per ASHRAE 90.1
- Size equipment for design conditions with appropriate safety margins
- Provide zoning for operational flexibility
- Integrate with building automation system for optimal control

**Source:** ASHRAE fundamentals; NBC 2020 climate data; ASSUMPTION: standard industrial HVAC practice

#### Plumbing System Principles

**Functional Requirements**:
- Domestic water for occupant use (washrooms, break rooms, safety showers if required)
- Sanitary drainage to site services (PKG-03 interface)
- Process water connections if required for equipment

**Design Approach** (ASSUMPTION):
- Size piping per NBC 2020 and CSA B64 fixture unit method
- Provide freeze protection for exposed piping
- Design for ease of maintenance and future modifications
- Coordinate drainage routing with structural framing

**Source:** NBC 2020, CSA B64 standards; ASSUMPTION: standard plumbing design practice

#### Electrical Building Services Principles

**Scope Clarification**: This covers interior building electrical only. Main power distribution is PKG-17.

**Design Approach** (ASSUMPTION):
- Provide adequate lighting levels per NBC 2020 and workplace regulations
- Distribute receptacles for operational flexibility and future changes
- Provide dedicated circuits for critical loads
- Comply with CEC (Canadian Electrical Code) for all installations
- Coordinate panel locations and circuit routing with architectural layout

**Source:** NBC 2020, CEC requirements; ASSUMPTION: standard building electrical practice

#### Fire Suppression Principles

**Life Safety Priority**: Fire protection is a critical life safety system requiring rigorous compliance with codes.

**Design Approach**:
- Classify building occupancy per NBC 2020 (likely Group F - Industrial)
- Design sprinkler system per NFPA 13 for occupancy and commodity hazard
- Provide adequate coverage with hydraulic calculations (documented separately)
- Interface with site fire water supply (PKG-03)
- Coordinate with building structure for pipe support and clearances

**Source:** NBC 2020, NFPA 13 requirements; ASSUMPTION: standard fire protection design approach

### Applicable Standards Context

**National Building Code of Canada (NBC 2020)**:
- Governs all aspects of building design and construction in Canada
- Establishes minimum requirements for health, safety, accessibility, and structural adequacy
- Referenced throughout MEP design for loads, clearances, fire protection, and plumbing

**ASHRAE Standards**:
- ASHRAE 90.1: Establishes energy efficiency requirements for building systems
- ASHRAE 62.1: Establishes ventilation requirements for indoor air quality
- Industry-standard reference for HVAC design in North America

**Canadian Standards Association (CSA)**:
- CSA B64 series: Plumbing standards
- CSA structural standards: Used for coordination with structural design

**NFPA 13**: Industry-standard for sprinkler system design

**Source:** Standards references from Specification.md; industry standard applicability

## Considerations

### Factors to Consider During Development

#### Project-Specific Context

**Package Scope**: PKG-22 Building Interior & MEP includes interior finishes, HVAC, plumbing, building electrical distribution, fire suppression.

**Source:** Decomposition REVISED_v2.md, PKG-22 scope

**Facility Context**: Canola oil transload facility with railcar unloading, storage tanks, and marine loading operations. Building MEP systems support the operational infrastructure.

**Source:** Decomposition REVISED_v2.md, project description

#### Coordination Requirements

**Critical Interfaces** (see Specification.md, Interface Requirements):

1. **PKG-21 (Building Structures & Envelope)**:
   - Coordinate MEP equipment locations with structural framing
   - Coordinate penetrations through structure
   - Coordinate roof-mounted equipment supports
   - **Note DEC-06**: "MCC building equipment installed on-site after building erection" — design must accommodate post-erection installation

2. **PKG-17 (Electrical Power Distribution)**:
   - Coordinate main power feeds to building panels
   - Coordinate panel locations and sizes
   - Coordinate grounding and bonding

3. **PKG-19 (Control Systems)**:
   - Coordinate HVAC control interfaces
   - Coordinate BAS integration points
   - Coordinate control wiring and communication

4. **PKG-03 (Site Services)**:
   - Coordinate fire water supply connection
   - Coordinate sanitary sewer connection
   - Coordinate domestic water service
   - Coordinate site grading for drainage

**Source:** Package scope descriptions and interfaces; Decomposition DEC-06

**Coordination Method**: Dependencies are tracked externally (NOT_TRACKED mode per `_DEPENDENCIES.md`). Coordination to be managed through IDC (Interdisciplinary Check) process and design review meetings.

#### Regulatory and Permit Considerations

- **Building Permit Required**: MEP drawings will form part of building permit submission to local authority (Surrey, BC)
- **Professional Seal**: Drawings must be sealed by Professional Engineer registered in British Columbia per NBC 2020 requirements
- **Code Compliance**: Design must demonstrate compliance with NBC 2020, CEC, NFPA 13, and provincial regulations
- **Authority Having Jurisdiction (AHJ)**: Local fire marshal and building inspector will review fire protection and life safety systems

**Source:** NBC 2020 requirements; standard Canadian building permit process

#### Constructability Considerations

**Installation Sequence** (per DEC-06):
- Building structure (PKG-21) erected first
- MEP systems installed after building enclosure
- Design must allow for rigging and installation access
- Consider modular or prefabricated assemblies where practical

**Construction-Friendly Design**:
- Provide adequate clearances for installation
- Minimize field welds and joints where possible
- Standardize components for ease of procurement
- Provide clear installation details and notes

**Source:** DEC-06 decision; ASSUMPTION: standard constructability principles

#### Operability and Maintainability

**Access for Maintenance**:
- Provide service access to all equipment
- Design for filter changes, cleaning, and routine maintenance
- Consider future component replacement (design for disassembly)

**Operational Flexibility**:
- Provide zoning and control flexibility
- Design for potential future modifications or expansions
- Document system capacities and available margins

**Commissioning Requirements**: MEP systems will require functional performance testing per DEL-22.05 Building MEP Installation and Test Records.

**Source:** ASSUMPTION: standard O&M design principles; DEL-22.05 cross-reference

## Trade-offs

### Competing Concerns to Evaluate

#### Cost vs. Performance

**Decision Point**: Specify high-efficiency equipment vs. standard efficiency

**Trade-off**:
- Higher efficiency equipment has higher capital cost but lower operating cost (energy savings)
- Lifecycle cost analysis (OBJ-9: Lifecycle Cost Optimization) should guide selection
- ASHRAE 90.1 sets minimum efficiency requirements; exceeding minimums requires justification

**Recommendation**: Perform lifecycle cost analysis for major equipment (HVAC units, pumps, lighting). **TBD** — Economic criteria and discount rate per project procedures (location TBD)

**Source:** ASHRAE 90.1 requirements; Decomposition OBJ-9 (inferred as applicable)

#### Redundancy vs. Simplicity

**Decision Point**: Provide redundant systems for critical functions vs. single-path design

**Trade-off**:
- Redundancy increases reliability but adds capital cost and maintenance burden
- Industrial facilities typically require higher reliability than commercial buildings
- Identify critical vs. non-critical systems

**Recommendation**:
- **Critical systems** (e.g., ventilation for equipment cooling, fire suppression): Consider redundancy or rapid-repair capability
- **Non-critical systems** (e.g., comfort cooling for break rooms): Single-path acceptable
- **TBD** — Criticality classification per Employer's Requirements (location TBD)

**Source:** ASSUMPTION: standard reliability design approach; specific requirements TBD

#### Standardization vs. Optimization

**Decision Point**: Use standardized equipment selections vs. optimize each application

**Trade-off**:
- Standardization reduces design effort, simplifies procurement, and reduces spare parts inventory
- Optimization can reduce capital cost and improve performance for each specific application
- Over-standardization can result in oversized equipment and wasted energy

**Recommendation**: Standardize where practical (lighting fixtures, receptacle types, common valves/fittings) but optimize major equipment (HVAC units, pumps) for specific loads.

**Source:** ASSUMPTION: standard design approach balancing cost and complexity

#### Schedule vs. Design Quality

**Decision Point**: Design completion timeline vs. thoroughness of design

**Trade-off**:
- Compressed design schedule may result in less optimization and more conservative (costly) designs
- Extended design schedule may delay procurement and construction start
- Incomplete designs lead to RFIs, changes, and construction delays (higher cost impact)

**Recommendation**: Prioritize design quality and completeness. Use stage gate reviews (30%, 60%, 90%, IFC) to balance progress and quality. **TBD** — Project schedule milestones (location TBD)

**Source:** ASSUMPTION: standard EPC schedule/quality balance; specific project milestones TBD

#### Energy Efficiency vs. Capital Cost

**Decision Point**: Meet minimum code requirements vs. exceed for better lifecycle performance

**Trade-off**:
- ASHRAE 90.1 prescriptive requirements provide code minimum
- Performance path (ASHRAE 90.1 Appendix G) allows trade-offs but requires additional modeling
- Higher performance reduces operating cost and may align with owner sustainability goals

**Recommendation**: Meet ASHRAE 90.1 prescriptive requirements as baseline. Evaluate cost-effective improvements (LED lighting, heat recovery, VFD on large motors). **TBD** — Sustainability goals and incentives per Employer's Requirements (location TBD)

**Source:** ASHRAE 90.1 requirements; ASSUMPTION: standard energy efficiency design approach

## Examples

### Reference Examples and Precedents

**Project-Specific References**:

- **Employer's Requirements** — **TBD** (location TBD; shall be primary reference for project-specific expectations)
- **Previous Similar Facilities** — **TBD** — Precedent canola oil or vegetable oil transload facilities (if available)

**Source:** Employer's Requirements to be provided; industry precedents TBD

### MEP Drawing Set Organization Example

**Typical Industrial Building MEP Drawing Set Structure** (ASSUMPTION: to be tailored to project):

**Mechanical (HVAC) Drawings:**
- M-001: HVAC First Floor Plan
- M-002: HVAC Roof Plan
- M-003: HVAC Sections and Details
- M-004: HVAC Equipment Schedules
- M-005: HVAC Control Diagram (interface to PKG-19)

**Plumbing Drawings:**
- P-001: Plumbing First Floor Plan
- P-002: Plumbing Riser Diagram
- P-003: Plumbing Details
- P-004: Plumbing Fixture and Equipment Schedule

**Electrical (Building Services) Drawings:**
- E-001: Lighting First Floor Plan
- E-002: Power First Floor Plan
- E-003: Panel Schedules
- E-004: Electrical Details

**Fire Protection Drawings:**
- FP-001: Fire Protection First Floor Plan
- FP-002: Fire Protection Riser Diagram
- FP-003: Fire Protection Details
- FP-004: Sprinkler Equipment Schedule

**Source:** ASSUMPTION: typical MEP drawing organization; to be confirmed with project CAD standards

### Design Detail Examples

**HVAC Equipment Location**:
- Rooftop units preferred for ease of access and to free up floor space
- Indoor units require adequate service clearance per manufacturer and NBC
- Consider vibration isolation and noise impacts
- Coordinate structural support requirements with PKG-21

**Plumbing Routing**:
- Route piping in service corridors or above ceiling where possible
- Minimize penetrations through structural members
- Slope drainage piping continuously per NBC 2020 requirements
- Provide cleanouts per code requirements at changes in direction

**Electrical Layout**:
- Distribute lighting to provide uniform illumination per NBC 2020
- Provide receptacles at spacing suitable for anticipated equipment (typically 6-10 m spacing for general use)
- Emergency lighting at egress paths and exits per NBC life safety requirements
- Coordinate electrical room locations for convenient circuit distribution

**Fire Protection Coverage**:
- Sprinkler head spacing per NFPA 13 and hydraulic design
- Avoid obstructions that create shadows in coverage
- Provide seismic bracing per NBC 2020 requirements for Surrey, BC
- Coordinate piping routing to maintain required clearances to structure

**Source:** ASSUMPTION: standard MEP design practices; NBC 2020, NFPA 13, CEC requirements

### Anticipated Artifacts (from DEL-22.01)

1. **HVAC layout** — Ductwork, equipment, diffusers, controls
2. **Plumbing layout** — Water supply, drainage, fixtures, equipment
3. **Interior electrical layout** — Lighting, receptacles, panels, circuits
4. **Fire suppression layout** — Sprinklers, piping, standpipes, connections

**Source:** Decomposition REVISED_v2.md, DEL-22.01 anticipated artifacts

## Conflict Table (for human ruling)

No conflicts identified at this stage. Conflicts will be documented here if contradictions are found between sources during design development.

**Format**:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none yet) | | | | | | |
