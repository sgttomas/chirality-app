# Specification: DEL-22.04 Building MEP Data Sheet Package

## Scope

This specification defines the requirements for **Building MEP Data Sheet Package** within **PKG-22 Building Interior & MEP**.

**Deliverable Description:** Defines and substantiates building MEP equipment in accordance with Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.04 entry; _CONTEXT.md

### Included

This data sheet package shall include:

1. **HVAC equipment datasheets** — HVAC units, fans, ductwork accessories
2. **Plumbing equipment datasheets** — Water heaters, pumps, fixtures, accessories
3. **Fire suppression system datasheets** — Sprinkler system components and equipment

**Source:** Decomposition REVISED_v2.md, DEL-22.04 anticipated artifacts

### Excluded

The following are **excluded** from this deliverable:

- Main electrical power distribution equipment (covered by PKG-17)
- Control system components (covered by PKG-19, though MEP equipment control interfaces shall be documented)
- Process equipment (covered by other packages)
- Vendor shop drawings (covered by DEL-22.06)

**Source:** Package scope boundaries

### Relationship to Other Deliverables

These data sheets:

- **Document equipment shown in DEL-22.01** drawings with detailed performance parameters
- **Detail items specified in DEL-22.02** specifications with manufacturer-specific information
- **Reflect capacities calculated in DEL-22.03** design calculations
- **Establish acceptance criteria for DEL-22.05** installation and test records
- **Provide basis for DEL-22.06** shop drawing requirements

**Source:** Standard EPC deliverable relationships

## Requirements

### Functional Requirements

#### FR-01: Data Sheet Completeness

Each equipment data sheet shall completely define:
- Equipment identification (tag, service, location)
- Required performance parameters (capacity, efficiency, operating conditions)
- Material specifications and certifications
- Electrical, control, and utility connection requirements
- Installation and testing requirements

**Rationale**: See Guidance.md, Section "Purpose and Content of Equipment Data Sheets"

**Verification**: See Procedure.md, Step 2 (data population), Step 4 (verification)

**Source:** ASSUMPTION: standard data sheet completeness requirement

#### FR-02: HVAC Equipment Data Sheets

HVAC equipment data sheets shall include:
- **FR-02.1**: Equipment capacities per DEL-22.03 calculations (heating capacity, cooling capacity, airflow)
  - **Rationale**: See Guidance.md, Section "HVAC Equipment Data Sheet Content"
  - **Verification**: See Procedure.md, Step 1 (parameter identification from calculations); cross-check with DEL-22.03

- **FR-02.2**: Equipment efficiency per ASHRAE 90.1 minimum requirements. **TBD** — Specific efficiency requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "Energy Efficiency Requirements"
  - **Verification**: See Procedure.md, Step 3 (vendor coordination); verify efficiency meets ASHRAE 90.1

- **FR-02.3**: Control interfaces per PKG-19 requirements (BAS integration, control points, communication protocol)
  - **Rationale**: See Guidance.md, Section "Considerations - Control System Interfaces"
  - **Verification**: See Procedure.md, Step 2; coordinate with PKG-19

**Source:** ASHRAE 90.1 (location TBD); DEL-22.03 calculations; PKG-19 interface requirements

#### FR-03: Plumbing Equipment Data Sheets

Plumbing equipment data sheets shall include:
- **FR-03.1**: Equipment capacities per DEL-22.03 calculations (flow rates, pressure ratings, tank capacities)
  - **Rationale**: See Guidance.md, Section "Plumbing Equipment Data Sheet Content"
  - **Verification**: See Procedure.md, Step 1; cross-check with DEL-22.03

- **FR-03.2**: Materials suitable for potable water service (NSF/ANSI approved where applicable)
  - **Rationale**: See Guidance.md, Section "Material Selection for Plumbing"
  - **Verification**: See Procedure.md, Step 3 (vendor coordination); verify NSF/ANSI certification

- **FR-03.3**: Pressure and temperature ratings adequate for system design conditions
  - **Rationale**: See Guidance.md, Section "Plumbing Equipment Data Sheet Content"
  - **Verification**: See Procedure.md, Step 4 (verification); cross-check with DEL-22.03 calculated conditions

**Source:** NBC 2020, CSA B64 (locations TBD); DEL-22.03 calculations

#### FR-04: Fire Suppression Equipment Data Sheets

Fire suppression equipment data sheets shall include:
- **FR-04.1**: Sprinkler system components per NFPA 13 requirements (sprinkler type, temperature rating, K-factor, coverage area)
  - **Rationale**: See Guidance.md, Section "Fire Protection Equipment Data Sheet Content"
  - **Verification**: See Procedure.md, Step 1; cross-check with DEL-22.03 hydraulic calculations

- **FR-04.2**: Equipment approvals (UL/FM listing for fire protection equipment)
  - **Rationale**: See Guidance.md, Section "Fire Protection Equipment Approvals"
  - **Verification**: See Procedure.md, Step 3 (vendor coordination); verify UL/FM approval

- **FR-04.3**: Performance parameters per DEL-22.03 hydraulic calculations (flow, pressure, design area)
  - **Rationale**: See Guidance.md, Section "Fire Protection Equipment Data Sheet Content"
  - **Verification**: See Procedure.md, Step 4; cross-check with DEL-22.03

**Source:** NFPA 13 (location TBD); DEL-22.03 hydraulic calculations

### Performance Requirements

#### PR-01: Vendor Data Accuracy

- **PR-01.1**: All vendor-supplied data shall be from current manufacturer literature or certified data sheets
- **PR-01.2**: Performance curves (pumps, fans) shall be provided and shall demonstrate equipment meets required performance
- **PR-01.3**: Vendor data shall be cross-checked against project requirements before acceptance

**Rationale**: See Guidance.md, Section "Vendor Data Validation"

**Verification**: See Procedure.md, Step 3 (vendor coordination), Step 4 (verification)

**Source:** ASSUMPTION: standard vendor data requirements

#### PR-02: Equipment Efficiency and Energy Compliance

All equipment shall meet or exceed ASHRAE 90.1 minimum efficiency requirements:
- HVAC equipment: minimum EER, COP, SEER per ASHRAE 90.1 equipment tables
- Pumps: motor efficiency per ASHRAE 90.1
- Lighting: efficacy per ASHRAE 90.1 (if included in data sheet package)

**TBD** — Specific efficiency targets beyond code minimum (location TBD)

**Rationale**: See Guidance.md, Trade-offs "Energy Efficiency vs. Equipment Cost"

**Verification**: See Procedure.md, Step 4 (verification); DEL-22.01 Specification PR-03

**Source:** ASHRAE 90.1 (location TBD)

#### PR-03: Equipment Ratings and Margins

- Equipment shall be rated for continuous duty at specified operating conditions
- Equipment selections shall include appropriate margins per DEL-22.03 calculations (typically 10-15%)
- Equipment shall be suitable for environmental conditions (temperature, humidity, corrosion)

**Rationale**: See Guidance.md, Section "Equipment Selection Margins"

**Verification**: See Procedure.md, Step 4 (verification); cross-check with DEL-22.03

**Source:** DEL-22.03 calculations; standard equipment selection practice

### Interface Requirements

#### IF-01: Consistency with Drawings (DEL-22.01)

Data sheets shall:
- Match equipment tags shown on DEL-22.01 drawings
- Confirm equipment locations and arrangements shown on drawings
- Support equipment schedules shown on drawings

**Rationale**: See Guidance.md, Section "Data Sheets and Drawings Coordination"

**Verification**: See Procedure.md, Step 5 (approval); cross-check with DEL-22.01

**Source:** DEL-22.01 drawings cross-reference

#### IF-02: Consistency with Specifications (DEL-22.02)

Data sheets shall:
- Meet performance requirements specified in DEL-22.02
- Comply with material and manufacturer requirements in DEL-22.02
- Demonstrate compliance with codes and standards referenced in DEL-22.02

**Rationale**: See Guidance.md, Section "Data Sheets and Specifications Coordination"

**Verification**: See Procedure.md, Step 5; cross-check with DEL-22.02

**Source:** DEL-22.02 specifications cross-reference

#### IF-03: Support from Calculations (DEL-22.03)

Data sheets shall:
- Reflect equipment capacities calculated in DEL-22.03
- Document operating conditions used in DEL-22.03 calculations
- Demonstrate selected equipment meets calculated requirements

**Rationale**: See Guidance.md, Section "Calculations and Equipment Selection"

**Verification**: See Procedure.md, Step 1 (parameter identification); Step 4 (verification)

**Source:** DEL-22.03 calculations establish equipment parameters

#### IF-04: Interface with Control Systems (PKG-19)

Data sheets shall define:
- Control points and monitoring requirements for each equipment
- Communication protocol and BAS integration requirements
- Electrical control interfaces (voltage, dry contacts, 4-20mA, etc.)

**Rationale**: See Guidance.md, Section "Considerations - Control System Interfaces"

**Verification**: See Procedure.md, Step 2 (data population); coordinate with PKG-19

**Source:** PKG-19 control system requirements

#### IF-05: Interface with Electrical Power (PKG-17)

Data sheets shall define:
- Electrical power requirements (voltage, phase, frequency, FLA, MCA, MOCP)
- Disconnect and overcurrent protection requirements
- Coordinate with PKG-17 for power distribution adequacy

**Rationale**: See Guidance.md, Section "Considerations - Electrical Coordination"

**Verification**: See Procedure.md, Step 2; coordinate with PKG-17

**Source:** PKG-17 electrical power distribution interface

### Quality Requirements

#### QR-01: Data Sheet Review and Approval

- All data sheets shall undergo technical review by qualified engineer
- Vendor-supplied data shall be verified against project requirements
- Data sheets shall be approved by discipline lead before issue

**Rationale**: See Guidance.md, Section "Quality Assurance for Equipment Data"

**Verification**: See Procedure.md, Step 4 (verification), Step 5 (approval)

**Source:** ASSUMPTION: standard equipment data sheet quality process

#### QR-02: Format and Consistency

- All data sheets shall use project-standard format and templates — **TBD** (location TBD)
- Equipment tagging shall be consistent across all deliverables (drawings, specifications, data sheets)
- Units and nomenclature shall be consistent and per project standards

**Rationale**: See Guidance.md, Section "Data Sheet Format Standards"

**Verification**: See Procedure.md, Step 2 (data population); format compliance check

**Source:** ASSUMPTION: standard data sheet format requirements

## Standards

### Applicable Codes and Standards

**Equipment Standards:**

- **ASHRAE 90.1** — Equipment efficiency requirements **TBD** (location TBD)
- **NFPA 13** — Fire protection equipment requirements **TBD** (location TBD)
- **CSA B64** series — Plumbing fixture standards **TBD** (location TBD)
- **CEC** — Canadian Electrical Code (equipment electrical ratings) **TBD** (location TBD)

**Certification and Approval Standards:**

- **UL** — Underwriters Laboratories (equipment safety certifications)
- **FM** — Factory Mutual (fire protection equipment approvals)
- **CSA** — Canadian Standards Association (equipment certifications for Canada)
- **NSF/ANSI** — Standards for potable water contact materials

**Source:** Applicable equipment standards per DEL-22.02; equipment certification requirements

### Employer's Requirements

- **Employer's Requirements Volume 2** — **TBD** — Project-specific equipment requirements (location TBD)

Employer's Requirements shall take precedence over general standards where conflicts exist.

## Verification

### Verification Methods

| Verification Activity | Description | Responsibility |
|----------------------|-------------|----------------|
| Parameter Identification | Verify equipment parameters from DEL-22.03 calculations | Equipment Engineer |
| Required Performance Check | Verify data sheet requirements match DEL-22.02 specifications | Lead Engineer |
| Vendor Data Validation | Verify vendor data is current and accurate per PR-01 | Equipment Engineer |
| Performance Verification | Verify vendor equipment meets required performance per FR-02/03/04 | Checker |
| Efficiency Compliance | Verify equipment efficiency meets ASHRAE 90.1 per PR-02 | Checker |
| Interface Coordination | Verify interfaces with DEL-22.01, DEL-22.02, DEL-22.03 per IF-01/02/03 | Lead Engineer |
| Control Interface Check | Verify control interfaces coordinated with PKG-19 per IF-04 | Controls Engineer |
| Electrical Interface Check | Verify electrical requirements coordinated with PKG-17 per IF-05 | Electrical Engineer |
| Format Compliance | Verify data sheet format per QR-02 | Technical Reviewer |

**Source:** Requirements sections above; ASSUMPTION: standard data sheet verification process

### Acceptance Criteria

**Completeness:**

- [ ] All equipment types from DEL-22.01 drawings have data sheets
- [ ] All required parameters documented per FR-01
- [ ] All vendor data provided and validated per PR-01

**Performance:**

- [ ] Equipment capacities meet DEL-22.03 calculated requirements
- [ ] Equipment efficiency meets ASHRAE 90.1 per PR-02
- [ ] Equipment ratings adequate for operating conditions per PR-03

**Compliance:**

- [ ] HVAC equipment meets ASHRAE 90.1 efficiency requirements (FR-02.2)
- [ ] Plumbing materials approved for potable water (FR-03.2)
- [ ] Fire protection equipment UL/FM listed (FR-04.2)

**Coordination:**

- [ ] Equipment tags match DEL-22.01 drawings (IF-01)
- [ ] Performance meets DEL-22.02 specifications (IF-02)
- [ ] Capacities match DEL-22.03 calculations (IF-03)
- [ ] Control interfaces coordinated with PKG-19 (IF-04)
- [ ] Electrical requirements coordinated with PKG-17 (IF-05)

**Quality:**

- [ ] Technical review completed and signed off (QR-01)
- [ ] Format and consistency standards met (QR-02)

**Source:** ASSUMPTION: standard data sheet acceptance criteria

## Documentation

### Required Documentation Outputs

**Data Sheet Packages (per Decomposition DEL-22.04 anticipated artifacts):**

1. **HVAC equipment datasheets**
2. **Plumbing equipment datasheets**
3. **Fire suppression system datasheets**

**Supporting Documentation:**

- Equipment tag register (cross-reference to drawings)
- Vendor data sheet collection
- Equipment selection justification (if required)

**Source:** Decomposition REVISED_v2.md, DEL-22.04 anticipated artifacts

### Documentation Format and Control

- **Data sheet format**: **TBD** — Per project data sheet templates (Excel forms, PDF forms, or similar)
- **Issued format**: PDF for issue and review
- **Numbering**: **TBD** — Per project equipment data sheet numbering system
- **Revision control**: All revisions tracked per project document control procedure
- **File naming**: **TBD** — Per project file naming convention

**Filing and retention:**

- Working files: `1_Working/` (this folder)
- Issued for review: `2_Checking/To/` (review copies with DEL-ID + date/rev)
- Issued for construction: `3_Issued/` (final issued copies)

**Source:** ASSUMPTION: standard project document control conventions per README.md Section 6
