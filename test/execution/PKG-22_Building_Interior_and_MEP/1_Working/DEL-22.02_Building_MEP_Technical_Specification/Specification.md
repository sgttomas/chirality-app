# Specification: DEL-22.02 Building MEP Technical Specification

## Scope

This specification defines the requirements for **Building MEP Technical Specification** within **PKG-22 Building Interior & MEP**.

**Deliverable Description:** Defines performance, materials, and workmanship requirements for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.02 entry; _CONTEXT.md

### Included

This technical specification deliverable shall include:

1. **HVAC specification** — Equipment, materials, and installation requirements for heating, ventilation, and air conditioning systems
2. **Building plumbing specification** — Equipment, materials, and installation requirements for plumbing systems
3. **Fire suppression specification** — Equipment, materials, and installation requirements for fire protection systems
4. **Electrical building services specification** (if required) — **TBD** — Confirm whether electrical specification is included in DEL-22.02 scope (not listed in anticipated artifacts but is part of PKG-22 scope per DEL-22.01)

**Source:** Decomposition REVISED_v2.md, DEL-22.02 anticipated artifacts; PKG-22 scope

### Excluded

The following are **excluded** from this specification and covered by other deliverables or packages:

- Design drawings (covered by DEL-22.01 Building MEP Design Drawing Set)
- Design calculations (covered by DEL-22.03 Building MEP Design Calculations)
- Equipment data sheets (covered by DEL-22.04 Building MEP Data Sheet Package)
- Main electrical power distribution specifications (covered by PKG-17)
- Control system specifications (covered by PKG-19, though MEP interfaces shall be specified)
- Building structure and envelope specifications (covered by PKG-21)
- Process piping specifications (covered by PKG-14)

**Source:** PKG-22 deliverable scope and adjacent package scopes per Decomposition

### Relationship to Other Deliverables

This technical specification:

- **Supports DEL-22.01 drawings** by providing detailed material, equipment, and installation requirements
- **References DEL-22.03 calculations** for equipment sizing and performance verification
- **Is implemented by DEL-22.04 datasheets** which provide manufacturer-specific equipment information
- **Establishes testing requirements** for DEL-22.05 installation and test records
- **Defines submittal requirements** for DEL-22.06 shop drawings

**Source:** Standard EPC deliverable relationships

## Requirements

### Functional Requirements

#### FR-01: Specification Completeness

The technical specification shall completely define all materials, equipment, and workmanship requirements necessary for:
- Procurement of MEP equipment and materials
- Installation of MEP systems per DEL-22.01 drawings
- Testing and commissioning per NBC 2020 and applicable standards

**Rationale**: See Guidance.md, Section "Purpose and Role of Technical Specifications"

**Verification**: See Procedure.md, Step 3 (completeness review)

**Source:** ASSUMPTION: standard specification completeness requirement

#### FR-02: Standards Compliance

The specification shall reference and require compliance with all applicable codes and standards including:
- NBC 2020 (National Building Code of Canada)
- ASHRAE standards (90.1, 62.1, etc.)
- NFPA 13 (fire suppression)
- CSA B64 series (plumbing)
- CEC (Canadian Electrical Code, if electrical scope included)
- SMACNA (duct construction)
- Material standards (ASTM, CSA, UL/FM/CSA approvals)

**Rationale**: See Guidance.md, Section "Principles - Codes and Standards Framework"

**Verification**: See Procedure.md, Step 2 (standards identification); Datasheet.md (Applicable Standards list)

**Source:** Applicable MEP codes and standards per Decomposition and industry practice

#### FR-03: Performance Criteria

The specification shall define clear performance criteria for:
- HVAC system capacity, efficiency, noise levels
- Plumbing system flow rates, pressures, temperatures
- Fire suppression system flow, pressure, coverage per NFPA 13
- Equipment efficiency and energy performance per ASHRAE 90.1

**Rationale**: See Guidance.md, Section "Principles - Performance-Based Specifications"

**Verification**: See Procedure.md, Step 3 (performance requirements development)

**Source:** ASHRAE 90.1, NFPA 13, NBC 2020 (locations TBD)

#### FR-04: Material Standards

The specification shall specify:
- Acceptable materials with referenced material standards (ASTM, CSA, etc.)
- Required certifications and approvals (UL, FM, CSA, NSF)
- Material properties (pressure ratings, temperature ratings, corrosion resistance, etc.)
- Prohibited materials (if any, per project requirements or environmental concerns)

**Rationale**: See Guidance.md, Section "Considerations - Material Selection"

**Verification**: See Procedure.md, Step 3 (products section development)

**Source:** Material standards per industry practice (ASTM, CSA, UL/FM/CSA)

#### FR-05: Equipment Specifications

The specification shall define equipment requirements including:
- Performance parameters (capacity, efficiency, power, etc.)
- Operating conditions (temperature, pressure, flow, etc.)
- Control and monitoring requirements (interface to PKG-19)
- Acceptable manufacturers and models (or performance-based equivalency criteria)
- Factory testing and certifications required

**Rationale**: See Guidance.md, Section "Principles - Equipment Specification Approaches"

**Verification**: See Procedure.md, Step 3 (products section); cross-check with DEL-22.04 datasheets

**Source:** ASSUMPTION: standard equipment specification requirements; details TBD per equipment type

#### FR-06: Installation Requirements

The specification shall define installation requirements including:
- Installation methods and workmanship standards
- Support and anchoring requirements (coordinate with PKG-21 structural)
- Clearances and access requirements per NBC 2020 and manufacturer requirements
- Seismic restraint requirements per NBC 2020 for Surrey, BC location
- Protection during construction
- Coordination with other trades

**Rationale**: See Guidance.md, Section "Considerations - Constructability and Installation"

**Verification**: See Procedure.md, Step 3 (execution section development)

**Source:** NBC 2020 installation requirements; ASSUMPTION: standard installation specification content

#### FR-07: Submittal Requirements

The specification shall define submittal requirements including:
- Shop drawings (for fabricated items, coordinate with DEL-22.06)
- Product data (for equipment and materials, coordinate with DEL-22.04)
- Samples (if required for materials approval)
- Test reports (factory and field testing)
- Operations and maintenance (O&M) manuals
- Warranties

**Rationale**: See Guidance.md, Section "Principles - Quality Assurance Through Submittals"

**Verification**: See Procedure.md, Step 3 (submittals subsection in General section)

**Source:** ASSUMPTION: standard EPC submittal requirements

#### FR-08: Testing and Commissioning Requirements

The specification shall define:
- Factory testing requirements (equipment performance verification)
- Installation testing requirements (leak testing, pressure testing, functional testing)
- Commissioning requirements (system startup, performance verification, training)
- Acceptance criteria and documentation requirements (coordinate with DEL-22.05)

**Rationale**: See Guidance.md, Section "Considerations - Commissioning and Acceptance"

**Verification**: See Procedure.md, Step 3 (quality assurance and execution sections)

**Source:** NBC 2020, ASHRAE, NFPA 13 testing requirements (locations TBD); standard commissioning practice

### Performance Requirements

#### PR-01: Specification Format and Organization

The specification shall be organized per:
- **TBD** — Project specification standards (CSI MasterFormat or alternative format) (location TBD)
- Consistent section structure (General / Products / Execution) per Datasheet.md typical structure
- Clear section numbering and cross-referencing
- Coordinated with DEL-22.01 drawing references

**Rationale**: See Guidance.md, Section "Principles - Specification Format and Structure"

**Verification**: See Procedure.md, Step 1 (specification format selection)

**Source:** ASSUMPTION: CSI MasterFormat or similar; to be confirmed with project standards

#### PR-02: Clarity and Constructability

The specification shall be:
- Written in clear, unambiguous language using imperative mood ("shall", not "should" or "may")
- Constructible by qualified contractors without requiring engineering interpretation
- Free of contradictions (internal and with DEL-22.01 drawings)
- Coordinated across all specification sections (no conflicts between divisions)

**Rationale**: See Guidance.md, Section "Principles - Specification Writing Best Practices"

**Verification**: See Procedure.md, Step 4 (quality review and coordination check)

**Source:** ASSUMPTION: standard specification writing best practices

#### PR-03: Lifecycle and Sustainability Considerations

The specification shall consider:
- Equipment lifecycle cost (capital cost vs. operating cost per OBJ-9 Lifecycle Cost Optimization)
- Energy efficiency per ASHRAE 90.1 and project sustainability goals **TBD** (location TBD)
- Maintainability and serviceability requirements
- Spare parts and warranty terms

**Rationale**: See Guidance.md, Trade-offs "First Cost vs. Lifecycle Cost"

**Verification**: See Procedure.md, Step 3 (equipment specification development)

**Source:** ASHRAE 90.1; Decomposition OBJ-9 (inferred as applicable)

### Interface Requirements

#### IF-01: Coordination with Drawings (DEL-22.01)

The specification shall:
- Be fully coordinated with DEL-22.01 drawing content (no contradictions)
- Reference drawing numbers where applicable
- Define items shown on drawings but requiring additional detail

**Rationale**: See Guidance.md, Section "Considerations - Drawings and Specifications Coordination"

**Verification**: See Procedure.md, Step 4 (cross-check with DEL-22.01)

**Source:** Standard drawings/specifications coordination requirement

#### IF-02: Support from Calculations (DEL-22.03)

The specification requirements shall be:
- Supported by calculations documented in DEL-22.03
- Equipment sizing and performance criteria verified by calculations
- Design assumptions documented and consistent

**Rationale**: See Guidance.md, Section "Considerations - Calculations Support"

**Verification**: See Procedure.md, Step 4 (cross-check with DEL-22.03)

**Source:** Standard specification/calculation coordination

#### IF-03: Consistency with Equipment Datasheets (DEL-22.04)

The specification shall:
- Define equipment types and performance requirements
- Be consistent with equipment selections documented in DEL-22.04
- Allow for approved equals or performance-based substitutions per specified criteria

**Rationale**: See Guidance.md, Section "Equipment Specification Approaches"

**Verification**: See Procedure.md, Step 4 (cross-check with DEL-22.04)

**Source:** Standard specification/datasheet coordination

#### IF-04: Interface with Control Systems (PKG-19)

The specification shall define:
- Control and monitoring points for MEP equipment
- Communication protocols and interfaces to building automation system (BAS)
- Coordination requirements with PKG-19 Control Systems specifications

**Rationale**: See Guidance.md, Section "Considerations - Control System Interfaces"

**Verification**: See Procedure.md, Step 3 (controls subsection); coordination with PKG-19

**Source:** Interface requirement per PKG-22 and PKG-19 scopes

#### IF-05: Interface with Electrical Power (PKG-17)

The specification shall:
- Define electrical power requirements for MEP equipment (voltage, phase, full-load amps)
- Coordinate with PKG-17 electrical power distribution specifications
- Define equipment disconnects and local control requirements per CEC

**Rationale**: See Guidance.md, Section "Considerations - Electrical Coordination"

**Verification**: See Procedure.md, Step 3 (electrical requirements for each equipment type); coordination with PKG-17

**Source:** Interface requirement per PKG-22 and PKG-17 scopes; CEC requirements

### Quality Requirements

#### QR-01: Specification Review and Approval

The specification shall undergo:
- Internal technical review by qualified engineer
- Interdisciplinary coordination check with affected disciplines
- Review for constructability by construction management (if available)
- Approval by discipline lead and project manager

**Rationale**: See Guidance.md, Section "Considerations - Quality Assurance Process"

**Verification**: See Procedure.md, Step 4 (review and approval process)

**Source:** ASSUMPTION: standard EPC specification quality process

#### QR-02: Professional Responsibility

The specification shall:
- Be prepared under the responsible charge of a Professional Engineer registered in British Columbia
- Comply with professional standards and code of ethics
- Be stamped/sealed if required by contract or NBC 2020

**Rationale**: NBC 2020 professional requirements; professional liability considerations

**Verification**: See Procedure.md, Step 5 (professional review and seal if required)

**Source:** NBC 2020 and professional engineering requirements for BC

## Standards

### Applicable Codes and Standards

**Building Codes:**

- **NBC 2020** — National Building Code of Canada 2020
- **ABC 2019** — **TBD** — Identify full name and applicability (location TBD)

**MEP Design and Installation Standards:**

- **ASHRAE 90.1** — Energy Standard for Buildings (latest edition) **TBD** (location TBD)
- **ASHRAE 62.1** — Ventilation for Acceptable Indoor Air Quality **TBD** (location TBD)
- **NFPA 13** — Installation of Sprinkler Systems **TBD** (location TBD)
- **CSA B64** series — Plumbing standards **TBD** (location TBD)
- **CEC** — Canadian Electrical Code (if electrical scope included) **TBD** (location TBD)
- **SMACNA** — HVAC duct construction standards **TBD** (location TBD)

**Material and Equipment Standards** (to be specified per material/equipment type):

- **ASTM** — Material standards (pipes, fittings, insulation, etc.)
- **CSA** — Canadian Standards Association standards
- **UL** / **FM** / **CSA** — Equipment listings and approvals
- **NSF/ANSI** — Standards for potable water contact materials

**Specification Format Standards:**

- **CSI MasterFormat** — **TBD** — Confirm specification format standard (location TBD)

**Source:** Decomposition REVISED_v2.md standards list; industry-standard MEP specification standards; specific editions TBD per Employer's Requirements

### Employer's Requirements

- **Employer's Requirements Volume 2** — **TBD** — Project-specific requirements (location TBD)

Employer's Requirements shall take precedence over general standards where conflicts exist.

## Verification

### Verification Methods

| Verification Activity | Description | Responsibility |
|----------------------|-------------|----------------|
| Completeness Review | Verify all required specification sections are present and complete per FR-01 | Lead Specification Writer / Engineer |
| Standards Check | Verify all applicable codes and standards are referenced correctly per FR-02 | Technical Reviewer |
| Performance Criteria Review | Verify performance requirements are clear and supported by calculations (DEL-22.03) per FR-03 | Lead Engineer |
| Material Standards Review | Verify material specifications reference correct standards per FR-04 | Materials Engineer / Reviewer |
| Equipment Review | Verify equipment specifications are adequate and coordinated with datasheets (DEL-22.04) per FR-05 | Equipment Engineer / Reviewer |
| Installation Review | Verify installation requirements are constructible and comply with codes per FR-06 | Construction Advisor / Reviewer |
| Submittal Requirements Review | Verify submittal requirements are complete per FR-07 | Quality Manager |
| Testing Requirements Review | Verify testing requirements comply with codes and coordinate with DEL-22.05 per FR-08 | Commissioning Manager |
| Drawings Coordination | Verify specification is coordinated with DEL-22.01 drawings per IF-01 | IDC Coordinator |
| Calculations Coordination | Verify specification is supported by DEL-22.03 calculations per IF-02 | Lead Engineer |
| Datasheets Coordination | Verify specification is consistent with DEL-22.04 datasheets per IF-03 | Equipment Engineer |
| Controls Interface Coordination | Verify controls requirements coordinate with PKG-19 per IF-04 | Controls Engineer |
| Electrical Interface Coordination | Verify electrical requirements coordinate with PKG-17 per IF-05 | Electrical Engineer |
| Format and Clarity Review | Verify specification format and writing quality per PR-01 and PR-02 | Specification Reviewer |
| Professional Review | Professional engineer review and seal (if required) per QR-02 | P.Eng. BC |

**Source:** Requirements sections above; ASSUMPTION: standard specification verification process

### Acceptance Criteria

**Completeness:**

- [ ] All required specification sections present (HVAC, Plumbing, Fire Suppression, Electrical if required)
- [ ] All equipment types shown on DEL-22.01 drawings are specified
- [ ] All materials shown on DEL-22.01 drawings are specified
- [ ] Submittal requirements defined for all products
- [ ] Testing and commissioning requirements defined

**Compliance:**

- [ ] All applicable codes and standards referenced correctly
- [ ] NBC 2020 requirements addressed
- [ ] ASHRAE 90.1 energy requirements addressed
- [ ] NFPA 13 fire suppression requirements addressed (if applicable)
- [ ] CEC electrical requirements addressed (if electrical scope included)

**Coordination:**

- [ ] No contradictions with DEL-22.01 drawings
- [ ] Equipment sizing supported by DEL-22.03 calculations
- [ ] Equipment selections consistent with DEL-22.04 datasheets
- [ ] Controls interfaces coordinated with PKG-19
- [ ] Electrical requirements coordinated with PKG-17

**Quality:**

- [ ] Written in clear, imperative language
- [ ] No internal contradictions
- [ ] Constructible by qualified contractors
- [ ] Professional review completed and documented
- [ ] Professional seal applied (if required)

**Source:** ASSUMPTION: standard specification acceptance criteria

## Documentation

### Required Documentation Outputs

**Specification Documents (per Decomposition DEL-22.02 anticipated artifacts):**

1. **HVAC specification**
2. **Building plumbing specification**
3. **Fire suppression specification**
4. **Electrical building services specification** (if required) — **TBD**

**Supporting Documentation:**

- Specification outline (section list with brief descriptions)
- Standards and references list
- Coordination meeting minutes (with disciplines)
- Review comments and resolution log

**Source:** Decomposition REVISED_v2.md, DEL-22.02 anticipated artifacts

### Documentation Format and Control

- **Draft format**: **TBD** — Per project standards (MS Word, Adobe InDesign, or similar)
- **Issued format**: PDF for issue to construction
- **Document numbering**: **TBD** — Per project specification numbering system
- **Revision control**: All revisions tracked per project document control procedure
- **File naming**: **TBD** — Per project file naming convention

**Filing and retention:**

- Working files: `1_Working/` (this folder)
- Issued for review: `2_Checking/To/` (review copies with DEL-ID + date/rev)
- Issued for construction: `3_Issued/` (final issued copies)

**Source:** ASSUMPTION: standard project document control conventions per README.md Section 6
