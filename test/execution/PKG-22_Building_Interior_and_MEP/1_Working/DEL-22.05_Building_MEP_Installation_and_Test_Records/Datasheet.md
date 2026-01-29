# Datasheet: DEL-22.05 Building MEP Installation and Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-22.05 |
| Name | Building MEP Installation and Test Records |
| Package | PKG-22 Building Interior & MEP |
| Discipline | Buildings |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Number Prefix | **TBD** — Per project record numbering system |
| Record Category | Installation Records, Test Records, Commissioning Records |
| Record Format | **TBD** — **ASSUMPTION**: Standardized forms, test sheets, checklists per project QA/QC procedures |
| File Format | **TBD** — **ASSUMPTION**: PDF scans of completed forms with signatures |
| Retention Period | **TBD** — Per project record retention requirements and NBC 2020 / regulatory requirements |
| Classification | Quality Records (for project closeout and owner O&M documentation) |

**Source:** Decomposition REVISED_v2.md, DEL-22.05 entry; _CONTEXT.md

## Conditions

**Operating / Environmental Context:**

This deliverable provides evidence of completion, inspection, and testing for building MEP systems per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.05 description

### Purpose and Use

| Purpose | Description |
|---------|-------------|
| Quality Assurance | Documents that MEP systems were installed per design and specifications |
| Code Compliance | Provides evidence of code compliance for building permit closeout and inspections by AHJ (Authority Having Jurisdiction) |
| Performance Verification | Demonstrates MEP systems meet design performance requirements through testing and commissioning |
| Operations Reference | Provides baseline performance data for future operations, maintenance, and troubleshooting |
| Warranty Baseline | Establishes as-built condition for warranty claims and future repairs |

**Source:** ASSUMPTION: standard test record purposes in EPC projects

### Applicable System Context

Per Decomposition PKG-22 scope and DEL-22.01/22.02, these records document:

| MEP System | Record Types |
|------------|-------------|
| HVAC | Duct pressure testing, airflow balancing, equipment startup, functional performance testing, temperature control verification |
| Plumbing | Pressure testing (water supply), leak testing, flow testing, backflow preventer testing, hot water system performance |
| Fire Suppression | Hydrostatic testing, main drain test, sprinkler system functional test, alarm and monitoring verification, fire pump testing (if applicable), AHJ acceptance inspection |
| Electrical Building Services | Lighting level measurements, emergency lighting duration test, receptacle testing, panel testing (coordinate with PKG-17) |

**Source:** Decomposition REVISED_v2.md, PKG-22 scope; NBC 2020, NFPA 13, ASHRAE testing requirements

### Testing and Commissioning Context

**Installation Records** document:
- Materials received and inspected
- Installation per design drawings and specifications
- Dimensional and alignment verification
- Visual inspections and punch list items

**Test Records** document:
- Performance testing (flow, pressure, temperature, capacity)
- Leak testing and pressure testing
- Functional testing (controls, interlocks, alarms)
- Code compliance testing (per NBC 2020, NFPA 13, etc.)

**Commissioning Records** document:
- System startup and initial operation
- Performance verification against design criteria (DEL-22.03 calculations, DEL-22.04 data sheets)
- Operator training
- Documentation turnover (O&M manuals, as-built drawings)

**Source:** ASSUMPTION: standard commissioning scope per ASHRAE Guideline 0 / 1.1; NBC 2020 requirements

## Construction

**Materials / Configuration:**

### Anticipated Record Artifacts

Per Decomposition REVISED_v2.md, DEL-22.05 anticipated artifacts:

1. **HVAC test records** — Duct pressure testing, airflow balancing, system commissioning, temperature control verification
2. **Plumbing test records** — Pressure testing, leak testing, flow testing, backflow preventer testing
3. **Fire suppression test records** — Hydrostatic testing, main drain test, system acceptance testing per NFPA 13

**Source:** Decomposition REVISED_v2.md, DEL-22.05 anticipated artifacts

### Typical Record Types by System

**HVAC Installation and Test Records**:
- Duct pressure testing (leakage testing per SMACNA standards)
- Air and water balance report (TAB - Testing, Adjusting, and Balancing)
- Equipment startup reports (manufacturer startup or factory representative)
- Functional performance testing (heating, cooling, ventilation capacity)
- Control system functional testing (coordinate with PKG-19)
- Filter installation and initial differential pressure readings

**Plumbing Installation and Test Records**:
- Water supply pressure testing (hydrostatic test per NBC 2020 / CSA B64)
- Drainage system leak testing (air or water test)
- Backflow preventer testing and certification
- Hot water system performance testing (temperature, flow, recovery rate)
- Fixture flow and pressure testing
- Water quality testing (if required for potable water)

**Fire Suppression Installation and Test Records**:
- Hydrostatic testing of sprinkler piping (per NFPA 13 - 200 psi for 2 hours typical)
- Main drain test (flow and pressure verification)
- Sprinkler system trip test (alarm valve actuation and alarm verification)
- Fire pump testing (if applicable - flow vs. pressure curve, run test, weekly/monthly tests)
- Control valve supervision testing (tamper switches)
- Fire alarm interface testing (coordinate with PKG-19 and fire alarm system)
- Authority Having Jurisdiction (AHJ) final inspection and acceptance

**Source:** NFPA 13, NBC 2020, CSA B64, SMACNA, ASHRAE testing requirements; standard commissioning practices

### Testing Standards and Protocols

**Applicable Testing Standards:**

- **ASHRAE Guideline 1.1** — HVAC&R Technical Requirements for Commissioning
- **NFPA 13** — Acceptance testing requirements for sprinkler systems
- **SMACNA** — HVAC Systems Testing, Adjusting and Balancing (TAB) standards
- **NBC 2020** — Plumbing and building system testing requirements
- **CSA B64** series — Plumbing system testing requirements

**Source:** Applicable testing and commissioning standards; specific editions TBD per DEL-22.02 and Employer's Requirements

## References

### Project References

- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Context: `_CONTEXT.md`
- Dependencies: `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Additional references: See `_REFERENCES.md` and `execution/PKG-22_Building_Interior_and_MEP/0_References/`

### Applicable Testing Standards

**Testing and Commissioning Standards:**

- **ASHRAE Guideline 0** — The Commissioning Process **TBD** (location TBD)
- **ASHRAE Guideline 1.1** — HVAC&R Technical Requirements for Commissioning **TBD** (location TBD)
- **NFPA 13** — Installation of Sprinkler Systems (Chapter on Acceptance Tests) **TBD** (location TBD)
- **SMACNA** — HVAC Systems Testing, Adjusting and Balancing **TBD** (location TBD)
- **NBC 2020** — Testing requirements for building systems
- **CSA B64** series — Plumbing testing requirements **TBD** (location TBD)

**Source:** Applicable testing standards per industry practice; specific editions TBD per Employer's Requirements

### Cross-References

**Related Deliverables (within PKG-22):**

- **DEL-22.01** — Building MEP Design Drawing Set (test records verify installation per drawings)
- **DEL-22.02** — Building MEP Technical Specification (test records verify compliance with specifications)
- **DEL-22.03** — Building MEP Design Calculations (commissioning verifies performance per design calculations)
- **DEL-22.04** — Building MEP Data Sheet Package (test records verify equipment performs per data sheet requirements)

**Related Deliverables (other packages):**

- **PKG-03** — Site Services (coordinate fire water supply testing, utility connections)
- **PKG-17** — Electrical Power Distribution (coordinate electrical testing for MEP equipment)
- **PKG-19** — Control Systems (coordinate control system functional testing and BAS commissioning)

**Source:** PKG-22 deliverable relationships; testing coordination with upstream packages
