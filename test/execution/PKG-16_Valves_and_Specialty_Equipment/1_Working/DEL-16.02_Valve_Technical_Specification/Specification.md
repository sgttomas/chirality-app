# Specification: DEL-16.02 Valve Technical Specification

## Scope

This specification defines the requirements for producing **Valve Technical Specification** within **PKG-16 Valves & Specialty Equipment**.

**Purpose:** Defines performance, materials, and workmanship requirements for valves per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Anticipated deliverable artifacts:**
- Control valve specification
- Isolation valve specification
- Relief valve specification

**Source:** `_CONTEXT.md`

**Valve Categories (per PKG-16 scope):**
- Control valves (flow, pressure, level control)
- Isolation valves (manual and automated)
- Relief valves (pressure and thermal relief)
- Strainers (Y-type, basket-type)
- Specialty items

**Source:** Decomposition document Section 5, PKG-16 scope (location TBD)

**Inclusions:**
- Valve performance requirements (pressure, temperature, flow capacity, rangeability, response time)
- Valve materials requirements (body, trim, seats, gaskets, bolting)
- Valve workmanship requirements (manufacturing, assembly, testing, inspection)
- Actuator and accessory requirements (actuators, positioners, limit switches, solenoids)
- Quality assurance and testing requirements (factory acceptance testing, pressure testing, set pressure testing)
- Documentation requirements (certifications, test reports, O&M manuals)

**Exclusions:**
- Valve sizing calculations (see DEL-16.03 Valve Design Calculations)
- Valve arrangement and installation drawings (see DEL-16.01 Valve Design Drawing Set)
- Individual valve datasheets (see DEL-16.04 Valve Data Sheet Package)
- Valve installation and test records (see DEL-16.05)

**Source:** Scope definition inferred from deliverable type and package structure

## Requirements

### Functional Requirements

**Specification Document Structure:**

The valve technical specifications shall be organized to support procurement and shall include the following sections (typical procurement specification format):

1. **Scope and Applicability**
   - Define which valves are covered by this specification
   - Reference applicable systems and services
   - Define exclusions and interfaces

2. **Reference Documents**
   - List applicable codes, standards, and project documents
   - Specify edition/revision of each standard
   - Identify precedence in case of conflicts

3. **Performance Requirements**
   - Operating conditions (pressure, temperature, flow)
   - Control performance (rangeability, linearity, response time for control valves)
   - Shutoff requirements (leakage class)
   - Fail-safe modes (for automated valves)

4. **Design Requirements**
   - Valve type and body style
   - Pressure-temperature ratings
   - End connections (flanged, threaded, welded)
   - Trim design and characteristics
   - Actuator type and sizing basis

5. **Materials of Construction**
   - Body material
   - Trim material (seat, plug, stem)
   - Gasket and packing materials
   - Bolting materials
   - Material compatibility with process fluid
   - Material certifications (MTRs)

6. **Manufacturing and Workmanship**
   - Manufacturing process requirements
   - Welding requirements (WPS, PQR, welder qualifications)
   - Surface finish requirements
   - Dimensional tolerances
   - Marking and identification

7. **Testing and Inspection**
   - Factory acceptance testing (FAT) requirements
   - Pressure testing (hydrostatic or pneumatic)
   - Seat leakage testing per API 598 or ISO 5208
   - Relief valve set pressure testing and certification (API 527)
   - Non-destructive examination (NDE) requirements (if applicable)
   - Witnessing and hold points

8. **Actuators and Accessories**
   - Actuator type, sizing, and performance
   - Positioner requirements (analog, smart, communication protocol)
   - Limit switches and position transmitters
   - Solenoid valves and air sets
   - Manual override provisions

9. **Documentation and Submittals**
   - Vendor drawing submittals (outline drawings, cross-sections)
   - Material certificates (MTRs, chemical analysis, mechanical properties)
   - Test certificates (pressure test, seat test, set pressure test)
   - Operation and maintenance manuals
   - Spare parts lists and recommended spares

10. **Quality Assurance**
    - Quality management system requirements (ISO 9001 or equivalent)
    - Inspection and test plan (ITP)
    - Non-conformance reporting and resolution
    - Traceability requirements

**Source:** Typical procurement specification structure for valves; specific content TBD based on design development and ER requirements

**Specification Format:**
- **Option A:** Unified specification covering all valve types with subsections per valve category
- **Option B:** Separate specifications per valve category (control, isolation, relief)
- **TBD:** Format selection based on project document management preferences and procurement strategy

### Performance Requirements

**Specification Content Requirements:**

1. **Completeness:** Specification shall include all information necessary for valve procurement and fabrication without ambiguity

2. **Traceability:** All requirements shall be traceable to:
   - Employer's Requirements (Volume 2 Parts 1–3) — **TBD**
   - Applicable codes and standards
   - Design calculations (DEL-16.03)
   - HAZOP recommendations (DEL-27.02) — **TBD**
   - Process design (P&IDs, line list)

3. **Consistency:** Specification requirements shall be consistent with:
   - Valve sizing calculations (DEL-16.03) — valve sizes, Cv/Kv, pressure drops
   - Valve datasheets (DEL-16.04) — individual valve selections
   - Piping specification (DEL-14.02) — material compatibility, flange ratings
   - Instrumentation specification (DEL-20.02) — control valve instrumentation

4. **Clarity:** Requirements shall be stated clearly and unambiguously using "shall" for mandatory requirements, "should" for recommended practices, and "may" for permissible options

5. **Verifiability:** All performance requirements shall be verifiable through inspection, testing, analysis, or demonstration

**Source:** General specification quality requirements; specific criteria TBD per project quality procedures

**Product-Specific Performance Requirements:**

For CSD Canola Oil Service:
- **Viscosity Handling:** Valves shall be suitable for variable viscosity service (high viscosity at low temperatures)
- **Food-Grade Cleanliness:** Product-contact valves shall have smooth internal surfaces suitable for food-grade service; dead-leg minimization
- **Drainability:** Valve design shall minimize product entrapment; drain connections provided where required
- **Temperature Control:** Valve body heating provisions (steam tracing, electric heat tracing) where required to maintain product temperature — **TBD**

**Source:** Product characteristics (CSD canola oil) from decomposition Section 1.1; specific requirements TBD pending process design

### Interface Requirements

**Multi-Discipline Coordination:**

The valve technical specification shall be coordinated with the following disciplines/deliverables:

1. **Process (PKG-10, PKG-11, PKG-12):**
   - Process design (P&IDs, PFDs) defines valve service, normal/design conditions
   - Valve performance requirements align with process requirements

2. **Mechanical Piping (PKG-14):**
   - Piping specification (DEL-14.02) — valve materials compatible with piping materials
   - Piping stress analysis — valve weights and dimensions within allowable pipe loads

3. **Instrumentation (PKG-20):**
   - Instrumentation specification (DEL-20.02) — control valve instrumentation (positioners, transmitters)
   - Signal types and communication protocols (4–20 mA, HART, Foundation Fieldbus, Profibus)

4. **Control Systems (PKG-19):**
   - Control philosophy — control valve fail-safe modes
   - Control system architecture — communication protocol selection

5. **Electrical (PKG-17):**
   - Electric actuator motor specifications (voltage, enclosure rating)
   - Hazardous area classification — actuator and accessory ratings

6. **Safety (DEL-27.02 HAZOP):**
   - HAZOP recommendations — safety-critical valve requirements, fail-safe modes, ESD functions

**Source:** Interface requirements inferred from multi-discipline nature of valve specifications; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

**Procurement Interface:**
- Specification shall support competitive bidding with multiple qualified vendors
- Specification shall provide "or equal" provisions allowing vendor alternates subject to approval
- Specification shall define submittal requirements and approval process

**Source:** Typical EPC procurement requirements

### Quality Requirements

**Document Quality:**
- Specification document shall comply with project Quality Management Plan
- Specification shall be reviewed and approved per project quality procedures
- Specification shall undergo interdisciplinary check (IDC) prior to issue for procurement

**Technical Quality:**
- Requirements shall be based on applicable codes and standards (see Standards section)
- Requirements shall be consistent with good engineering practice
- Requirements shall be appropriate for the service conditions and design life

**Procurement Quality:**
- Specification shall require vendors to have ISO 9001 certified quality management system (or equivalent)
- Specification shall define factory acceptance test (FAT) requirements and witness hold points
- Specification shall require material traceability and test certification

**Format and Style:**
- Document format: **TBD** — **ASSUMPTION**: Project specification template or company standard format
- Language: English (Canadian English spelling conventions)
- Units: **TBD** — SI units (metric) or Imperial units; consistent throughout document
- Terminology: Consistent with project glossary and industry standards

**Source:** Quality requirements typical for procurement specifications; specific requirements TBD per project procedures

## Standards

**Applicable codes and standards:**

**Valve Design and Manufacturing:**
- API 600 — Steel Gate Valves
- API 6D — Pipeline Valves
- API 526 — Flanged Steel Pressure-Relief Valves
- API 527 — Seat Tightness of Pressure Relief Valves
- API 598 — Valve Inspection and Testing
- API 607 — Fire Test for Quarter-Turn Valves
- API 608 — Metal Ball Valves
- API 609 — Butterfly Valves
- ASME B16.34 — Valves – Flanged, Threaded, and Welding End
- ASME B16.5 — Pipe Flanges and Flanged Fittings
- ISO 5208 — Industrial Valves – Pressure Testing
- MSS-SP-61 — Pressure Testing of Steel Valves
- MSS-SP-25 — Standard Marking System for Valves

**Control Valves:**
- IEC 60534 / ISA-75 series — Industrial-Process Control Valves

**Relief Valves:**
- ASME BPVC Section VIII — Pressure Vessels (relief requirements)
- API 520 — Sizing, Selection, and Installation of Pressure-Relieving Devices
- API 521 — Pressure-Relieving and Depressuring Systems

**Materials:**
- ASTM standards for valve materials (A105, A182, A351, SA-479, etc.)
- NACE MR0175/ISO 15156 — Materials for Sour Service (if applicable)

**Quality and Testing:**
- ISO 9001 — Quality Management Systems
- ISO 15848 — Fugitive Emissions Measurement

**Canadian Codes:**
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code

**Project-Specific:**
- Employer's Requirements (Volume 2 Parts 1–3) — **TBD**
- Project Engineering Standards — **TBD**

**Source:** Standards inferred from valve scope; applicability to be confirmed during specification development

## Verification

**Verification methods for Specification deliverables:**

### 1. Self-Check (Originator)
- Completeness check against specification outline/template
- Consistency check with design calculations (DEL-16.03) and datasheets (DEL-16.04)
- Compliance check with applicable codes and standards
- Clarity and grammar review

### 2. Technical Review (Discipline Lead)
- Technical accuracy of performance requirements
- Appropriateness of materials for service conditions
- Adequacy of testing and inspection requirements
- Compliance with applicable codes

### 3. Interdisciplinary Review (IDC)
- Process discipline review — valve performance requirements match process requirements
- Piping discipline review — valve materials compatible with piping specification
- Instrumentation discipline review — control valve instrumentation requirements
- Electrical discipline review — electric actuator specifications
- Control systems review — communication protocols and fail-safe logic

### 4. Employer Review and Comment
- Issue specification for Employer review (30%, 60%, 90% submittals) — **TBD**
- Incorporate Employer comments and obtain approval

### 5. Compliance Matrix Verification
- Create compliance matrix mapping specification requirements to:
  - Employer's Requirements (clause-by-clause) — **TBD**
  - Applicable codes and standards
  - HAZOP recommendations (DEL-27.02) — **TBD**
- Verify all ER requirements are addressed in specification

**Acceptance criteria:**
- All sections of specification complete and approved
- Zero unresolved Category A comments from IDC
- Employer approval obtained (if required)
- Compliance matrix complete with 100% coverage
- Document approved by discipline lead (P.Eng.) per project authority matrix — **TBD**

**Source:** Verification methods typical for procurement specifications; specific criteria TBD per project quality procedures

## Documentation

**Required documentation outputs:**

### Primary Deliverables (per _CONTEXT.md)
- **Control Valve Specification:** Technical requirements for control valves (flow, pressure, level control applications)
- **Isolation Valve Specification:** Technical requirements for isolation valves (gate, ball, butterfly valves; manual and automated)
- **Relief Valve Specification:** Technical requirements for pressure relief valves

**Format Options:**
- **Option A:** Three separate specification documents (one per valve category)
- **Option B:** One unified specification document with three major sections
- **TBD:** Format selection based on project document management and procurement strategy

### Supporting Documentation
- **Compliance Matrix:** Maps specification requirements to Employer's Requirements and codes/standards
- **IDC Comment/Response Log:** Record of interdisciplinary comments and resolutions
- **Employer Comment/Response Log:** Record of Employer review comments and resolutions (if applicable)
- **Specification Basis of Design:** Narrative explaining key specification decisions and trade-offs
- **Vendor Qualification Criteria:** Pre-qualification requirements for valve vendors (if separate from specification)

**Documentation Requirements:**

**Document Control:**
- All documents shall comply with project document control procedures
- Document numbering per project specification numbering system — **TBD**
- Revision control: Initial issue Rev 0 or A; subsequent revisions per project convention — **TBD**
- Distribution list: **TBD** — Employer, procurement, vendors (once bid packages issued)

**Format:**
- **TBD** — **ASSUMPTION**: MS Word or PDF format for text-based specifications
- Page size: **TBD** — Letter (8.5" × 11") or A4
- Header/footer: Project title, document number, revision, page number

**Submittal Requirements:**
- 30% Design submittal — **TBD** — Draft specification for Employer review
- 60% Design submittal — **TBD** — Revised specification incorporating Employer comments
- 90% Design submittal — **TBD** — Near-final specification
- IFP (Issued for Procurement) — **TBD** — Final specification for vendor bidding

**Source:** Submittal milestones inferred from decomposition Section 5, PKG-27, DEL-27.04 (Design Submission Packages); specific requirements TBD

**Records Retention:**
- Retention period: **TBD** — **ASSUMPTION**: Project life + 25 years typical for procurement specifications
- Archival format: **TBD** — **ASSUMPTION**: PDF/A for long-term preservation

**Source:** Records retention typical for EPC projects; specific requirements TBD per project procedures
