# Specification: DEL-23.03 Fire Protection Design Calculations

## Scope

This specification defines the requirements for **Fire Protection Design Calculations** within **PKG-23 Fire Protection** for the Canola Oil Transload Facility — Phase 1 Design & Build project.

**Project Context:**
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- Employer: DP World Fraser Surrey Inc.
- Contract Type: Design & Build
- Source: Decomposition document Section 1.1

**Deliverable Scope:**

This deliverable provides the engineering basis and sizing/verification calculations for fire protection systems per Employer's Requirements (ER), including:

**Anticipated deliverable artifacts (calculation packages):**
- Fire water demand calculations (Source: Decomposition DEL-23.03 anticipated artifacts)
- Hydraulic calculations (Source: Decomposition DEL-23.03 anticipated artifacts)

**Additional calculations (typical for comprehensive fire protection design):**
- Tank foam system calculations — **ASSUMPTION**: Required for combustible liquid storage per NFPA 30
- Marine loading foam system calculations — **ASSUMPTION**: Required for marine loading protection
- Fire pump sizing calculation (if applicable) — **ASSUMPTION**: If fire pump in Contractor scope
- Fire alarm system calculations (battery capacity, coverage analysis) — **ASSUMPTION**: Fire alarm system design support

**Purpose of Calculations:**

The fire protection design calculations serve to:
1. Establish design basis and performance requirements for fire protection systems
2. Size fire protection equipment and systems (piping, pumps, foam systems)
3. Verify fire protection systems meet code requirements and performance criteria
4. Provide technical basis for fire protection drawings (DEL-23.01) and specifications (DEL-23.02)
5. Support permitting and approval by authorities having jurisdiction (AHJ)
6. Document engineering rationale for design decisions
- Source: **ASSUMPTION**: Standard purpose of engineering design calculations

**Scope Boundaries:**

| Included | Excluded / Interface |
|----------|---------------------|
| Fire protection system sizing and verification calculations | Detailed fire modeling or computational fluid dynamics (CFD) analysis (unless specifically required by Employer or code) |
| Code-based calculation methodologies (NFPA, etc.) | Cost estimating calculations (estimating team activity) |
| Performance verification against design criteria | Construction means and methods calculations (constructor responsibility) |
| Equipment selection calculations | Operations and maintenance procedures (separate O&M deliverable) |

**Project Objectives Supported:**

This deliverable supports **OBJ-1: Safe & Reliable Operation** — calculations ensure fire protection systems are properly sized and meet performance requirements for safe facility operations.
- Source: Decomposition Section 2 (Project Objectives) and Section 6 (Objective-to-Deliverable Mapping)

## Requirements

### Functional Requirements

**FR-1: Comprehensive Calculation Coverage**
- Calculations shall address all fire protection systems requiring sizing or verification, including:
  - Fire water distribution system (demand, hydraulics, pipe sizing)
  - Fire pump (if required) (capacity, head, power)
  - Foam suppression systems (foam concentrate storage, proportioning, discharge devices)
  - Fire alarm system (battery capacity, coverage)
- Source: **ASSUMPTION**: Calculation completeness requirement
- Verification: Cross-check calculation list with system list from DEL-23.01 drawings

**FR-2: Code-Based Methodologies**
- Calculations shall use methodologies prescribed by applicable codes and standards (NFPA 30, NFPA 24, NFPA 20, NFPA 11, NFPA 16, NFPA 72)
- Where codes do not prescribe methodology, use recognized engineering methods and document basis
- Source: **ASSUMPTION**: Code compliance requirement
- Verification: Calculation methodology review against cited codes

**FR-3: Design Basis Documentation**
- Each calculation package shall document design basis including:
  - Facility description and fire protection zones
  - Product properties and classification
  - Applicable codes and standards
  - Design criteria and assumptions
  - Input data sources
- Source: **ASSUMPTION**: Calculation documentation standard
- Verification: Design basis section review in each calculation package

**FR-4: Input Data Traceability**
- All calculation input data shall be traceable to source (drawings, data sheets, codes, Employer's Requirements, site data, manufacturer data)
- Assumptions shall be clearly identified and justified
- Source: **ASSUMPTION**: Engineering calculation best practice
- Verification: Input data sources cited in calculations

**FR-5: Calculation Verification and Checking**
- Calculations shall be independently checked by qualified engineer (P.Eng.) not the originator
- Complex calculations verified using hand calculations, alternative methods, or comparison to published data
- Source: **ASSUMPTION**: Engineering quality control requirement
- Verification: Checker sign-off on calculations

**FR-6: Results and Conclusions**
- Each calculation package shall clearly state results, conclusions, and design recommendations
- Results shall be in format suitable for use in drawings, specifications, and data sheets
- Source: **ASSUMPTION**: Calculation usability requirement
- Verification: Results clearly stated and actionable

**FR-7: Calculation Updates**
- Calculations shall be updated when design changes affect inputs, assumptions, or results
- Calculation revisions tracked and documented
- Source: **ASSUMPTION**: Design change management
- Verification: Calculation revision control

### Performance Requirements

**PR-1: Calculation Accuracy**
- Calculations shall be accurate and free from errors that would affect design decisions or system performance
- Calculation methods appropriate for application and level of accuracy required
- Source: **ASSUMPTION**: Engineering accuracy standard
- Verification: Independent check and verification

**PR-2: Consistency with Design Documents**
- Calculation results shall be consistent with fire protection drawings (DEL-23.01), specifications (DEL-23.02), and data sheets (DEL-23.04)
- No conflicts between calculations and other design documents
- Source: **ASSUMPTION**: Document set consistency requirement
- Verification: Cross-document consistency check

**PR-3: Code Compliance Verification**
- Calculations shall demonstrate compliance with applicable codes (NFPA 30, NFPA 24, NFPA 20, NFPA 11, NFPA 16, NFPA 72, NBCC, BCFC)
- Code requirements explicitly checked and verified in calculations
- Source: **ASSUMPTION**: Code compliance verification requirement
- Verification: Code compliance review of calculations

**PR-4: Conservative Design**
- Calculations shall use conservative assumptions and safety factors appropriate to fire protection applications
- Uncertainties addressed through conservatism or sensitivity analysis
- Source: **ASSUMPTION**: Fire protection engineering practice
- Verification: Review of assumptions and safety factors

**PR-5: Calculation Completeness**
- Calculation packages sufficiently complete to support design decisions, equipment procurement, and AHJ approval
- No significant information gaps requiring assumptions by others
- Source: **ASSUMPTION**: Design-build calculation adequacy
- Verification: Design team review of calculation completeness

**PR-6: Professional Engineer Certification**
- Calculations prepared under responsible charge of Professional Engineer (P.Eng.) licensed in Canada
- Calculations signed and sealed by P.Eng. if required by jurisdiction or Employer
- Source: **ASSUMPTION**: Professional engineering requirement for BC
- Verification: P.Eng. seal and signature on calculation packages (if required)

### Interface Requirements

**INT-1: Fire Protection Design Drawings (DEL-23.01)**
- Calculation inputs: system layouts, pipe routing, equipment locations, dimensions from drawings
- Calculation outputs: pipe sizes, equipment capacities, performance requirements appear on drawings
- Source: **ASSUMPTION**: Calculation-drawing coordination
- Verification: Cross-check calculations and drawings for consistency

**INT-2: Fire Protection Technical Specification (DEL-23.02)**
- Calculation outputs: performance requirements, equipment capacities incorporated into specifications
- Specification requirements: material properties, standards used as calculation inputs
- Source: **ASSUMPTION**: Calculation-specification coordination
- Verification: Cross-check calculations and specifications for consistency

**INT-3: Fire Protection Data Sheets (DEL-23.04)**
- Calculation outputs: equipment sizing and performance requirements define data sheet content
- Data sheet information: equipment characteristics used as calculation inputs (iterative)
- Source: **ASSUMPTION**: Calculation-data sheet coordination
- Verification: Cross-check calculations and data sheets for consistency

**INT-4: Fire Protection Installation & Test Records (DEL-23.05)**
- Calculation assumptions: test results verify calculation assumptions (e.g., pipe roughness, system leakage)
- Calculation requirements: testing requirements based on calculation methodology (e.g., flow test per NFPA 291)
- Source: **ASSUMPTION**: Calculation-testing coordination
- Verification: Test procedures aligned with calculation assumptions

**INT-5: Other Discipline Calculations**
- Structural calculations (PKG-06): fire protection equipment loads (fire pump, foam tanks) for structural design
- Electrical calculations (PKG-17): fire pump power requirements for electrical design
- Civil calculations (PKG-03): fire water loop burial depth, trench design
- Source: **ASSUMPTION**: Interdisciplinary calculation coordination
- Verification: Interface data exchange and verification

**INT-6: Employer's Requirements**
- Employer's Requirements: fire protection performance criteria, design basis, constraints as calculation inputs
- Source: **ASSUMPTION**: ER compliance
- Verification: ER requirements incorporated into calculations

**INT-7: Authority Having Jurisdiction (AHJ)**
- AHJ requirements: jurisdiction-specific criteria or methodologies incorporated into calculations
- AHJ review: calculations may be submitted for AHJ review and approval
- Source: **ASSUMPTION**: AHJ coordination
- Verification: AHJ approval obtained (if required)

### Quality Requirements

**QR-1: Calculation Standards Compliance**
- Calculations shall comply with applicable codes and engineering standards
- Calculation format and documentation meet professional engineering standards
- Source: **ASSUMPTION**: Engineering quality standard
- Verification: Code compliance review and professional review

**QR-2: Calculation Checking and Review**
- All calculations independently checked by qualified P.Eng. not the originator
- Checker reviews methodology, inputs, calculations, and results
- Checker sign-off documented
- Source: **ASSUMPTION**: Engineering quality control
- Verification: Checker sign-off records

**QR-3: Calculation Documentation Quality**
- Calculations clearly documented with all inputs, assumptions, methodology, and results stated
- Calculations legible, organized, and reproducible by others
- Source: **ASSUMPTION**: Calculation documentation standard
- Verification: Documentation quality review

**QR-4: Version Control and Revision Tracking**
- Calculation revisions controlled and tracked
- Revision history documented
- Superseded calculations clearly marked and archived
- Source: **ASSUMPTION**: Document control requirement
- Verification: Calculation revision control system

**QR-5: Calculation Software Validation**
- Calculation software (hydraulic analysis software, spreadsheets) validated or verified for accuracy
- Software version documented
- Source: **ASSUMPTION**: Software quality assurance
- Verification: Software validation records or comparison checks

## Standards

**Governing Codes and Standards (Fire Protection Calculations):**

The following codes and standards provide calculation methodologies and requirements:

**NFPA Codes:**
| Code | Title | Application to Calculations | Source |
|------|-------|----------------------------|--------|
| NFPA 30 | Flammable and Combustible Liquids Code | Fire water demand calculation methodology for combustible liquid facilities; tank spacing and foam system requirements | **ASSUMPTION**: Primary calculation basis |
| NFPA 24 | Installation of Private Fire Service Mains | Hydraulic calculation requirements; pipe sizing methods; pressure/flow requirements | **ASSUMPTION**: Hydraulic calculation standard |
| NFPA 20 | Installation of Stationary Pumps for Fire Protection | Fire pump sizing methodology; pump capacity and head calculations | **ASSUMPTION**: Fire pump calculation standard |
| NFPA 11 | Low-, Medium-, and High-Expansion Foam | Foam system design calculations; foam concentrate quantity and application rates | **ASSUMPTION**: Foam calculation standard |
| NFPA 16 | Installation of Foam-Water Sprinkler and Foam-Water Spray Systems | Tank foam system calculations; foam discharge device sizing | **ASSUMPTION**: Tank foam calculation standard |
| NFPA 72 | National Fire Alarm and Signaling Code | Fire alarm battery capacity calculation; audibility/visibility coverage calculations | **ASSUMPTION**: Fire alarm calculation requirements |
| NFPA 13 | Installation of Sprinkler Systems | Hydraulic calculation methods (if sprinkler systems included) | **ASSUMPTION**: Sprinkler hydraulic calculations |
| NFPA 291 | Recommended Practice for Fire Flow Testing | Fire flow testing procedures (used to verify hydraulic calculations) | **ASSUMPTION**: Testing standard for verification |

**Engineering Standards:**
| Standard | Application | Source |
|----------|-------------|--------|
| Hazen-Williams Equation | Pipe friction loss calculation for water flow | **ASSUMPTION**: Standard hydraulic calculation method |
| Darcy-Weisbach Equation | Alternative pipe friction loss calculation method | **ASSUMPTION**: Alternative hydraulic method |
| ASME B31.1 | Piping code for pressure design verification | **ASSUMPTION**: Piping design code |

**Building Codes:**
| Code | Application | Source |
|------|-------------|--------|
| NBCC 2020 | Building code fire protection requirements | **ASSUMPTION**: BC building code |
| BCFC | Provincial fire code requirements | **ASSUMPTION**: BC fire code |

**Other Standards:**
- Employer's Requirements Volume 2 Parts 1–3 (Source: Decomposition Section 3)
- Fire equipment manufacturer design guides and technical data

**Calculation Software:**

The following software may be used for fire protection calculations:
- Hydraulic analysis: AFT Fathom, PIPE-FLO, AutoSPRINK, or equivalent — **ASSUMPTION**: Industry-standard hydraulic software
- Spreadsheet calculations: Microsoft Excel, MathCAD, or equivalent — **ASSUMPTION**: General calculation tools
- Fire alarm coverage: Fire alarm design software (if applicable) — **ASSUMPTION**: Specialized tool

Software shall be validated for accuracy per **QR-5** requirement.

## Verification

**Verification Methods for Design Calculations:**

**V-1: Calculation Self-Check**
- Engineer performing calculation reviews for completeness, accuracy, correct methodology, proper units
- Self-check includes rechecking arithmetic, verifying formulas, confirming input data sources
- Verification record: Self-check notation on calculation or checklist
- Source: **ASSUMPTION**: Engineering practice

**V-2: Independent Calculation Check**
- Qualified checker (P.Eng., independent from originator) reviews calculation for:
  - Methodology appropriate and correct
  - Input data correct and from valid sources
  - Calculations correct (spot-check arithmetic, verify formulas)
  - Results reasonable and conclusions sound
  - Documentation complete and clear
- Verification record: Checker sign-off on calculation package
- Source: **ASSUMPTION**: Engineering quality control

**V-3: Calculation Verification by Alternative Method**
- Complex or critical calculations verified using:
  - Hand calculation for simplified case
  - Alternative calculation method or software
  - Comparison to published data or design charts
  - Sensitivity analysis to verify results reasonable over range of inputs
- Verification record: Verification calculation or comparison documentation
- Source: **ASSUMPTION**: Engineering verification practice

**V-4: Cross-Document Consistency Verification**
- Calculation results cross-checked with drawings (DEL-23.01), specifications (DEL-23.02), data sheets (DEL-23.04) for consistency
- Interface data verified with other discipline calculations
- Verification record: Consistency check log or reconciliation record
- Source: **ASSUMPTION**: Document coordination requirement

**V-5: Code Compliance Verification**
- Calculations reviewed for compliance with applicable codes and standards
- Code requirements explicitly checked in calculations (e.g., NFPA 30 fire water demand requirements)
- Verification record: Code compliance checklist or review notes
- Source: **ASSUMPTION**: Code compliance verification

**V-6: Software Validation (if applicable)**
- Calculation software validated by:
  - Comparison to hand calculation for simple case
  - Comparison to published benchmark problems
  - Verification of software version and validity
- Verification record: Software validation record or comparison calculation
- Source: **ASSUMPTION**: Software quality assurance

**V-7: Peer Review or Design Review**
- Calculations reviewed at design review meetings (30%/60%/90% or as required)
- Peer engineers review calculation approach, assumptions, and results
- Verification record: Design review minutes or comment log
- Source: **ASSUMPTION**: Design review practice

**V-8: Testing Verification (Post-Construction)**
- Calculation assumptions verified by field testing (flow test per NFPA 291, pump performance test)
- Test results compared to calculated values
- Verification record: Installation and test records (DEL-23.05)
- Source: **ASSUMPTION**: Testing verification

**Acceptance Criteria:**

Calculations are acceptable when:
- Self-check completed by originator
- Independent check completed by qualified checker with sign-off
- Calculation verification performed (alternative method, comparison, etc.)
- Cross-document consistency verified
- Code compliance verified
- All review comments resolved
- Calculation documentation complete and clear
- Source: **ASSUMPTION**: Calculation acceptance criteria — specific criteria **TBD** per project quality procedures

**Hold Points / Witness Points:**

| Hold/Witness Point | Description | Party | Source |
|--------------------|-------------|-------|--------|
| Independent check completion | Calculations not issued until independent check complete and signed off | Checker | **ASSUMPTION**: Quality hold point |
| Design review milestone | Calculations reviewed at design milestones (30%/60%/90%) | Employer, design team | **ASSUMPTION**: Design review gate (if required) |
| AHJ review (if required) | Calculations submitted for AHJ review/approval if required for permit | Fire marshal / AHJ | **ASSUMPTION**: Permitting requirement |

Specific hold points **TBD** per project quality plan

## Documentation

**Required Documentation Outputs:**

**Calculation Packages:**

| Calculation Package | Content | Source |
|---------------------|---------|--------|
| Fire Water Demand Calculation | Design basis, facility description, fire protection zones, NFPA 30 methodology, tank foam demand, cooling demand, hydrant demand, marine loading demand, total demand, duration, references | Decomposition: fire water demand calculations (anticipated artifact) |
| Hydraulic Calculation | Design basis, fire water loop layout, input data (pipe lengths/sizes/elevations), hydraulic analysis methodology, friction losses, pressure at hydrants, pipe sizing verification, fire pump sizing (if required), results, references | Decomposition: hydraulic calculations (anticipated artifact) |

**Additional Calculation Packages (typical):**

| Calculation Package | Content | Source |
|---------------------|---------|--------|
| Tank Foam System Calculations | Design basis, tank sizes, foam application rates, foam solution demand, foam concentrate demand, foam storage sizing, proportioning system sizing, discharge device sizing, references | **ASSUMPTION**: Required for combustible liquid tanks |
| Marine Loading Foam System Calculations | Design basis, loading arm configuration, foam demand, foam system sizing, references | **ASSUMPTION**: Required for marine loading protection |
| Fire Pump Sizing Calculation | Design basis, fire water demand, available supply pressure, required pump head, pump capacity, pump power, pump selection, references | **ASSUMPTION**: If fire pump required |
| Fire Alarm Battery Capacity Calculation | Design basis, alarm system load, battery capacity per NFPA 72, battery sizing, references | **ASSUMPTION**: Fire alarm system calculation |
| Fire Alarm Coverage Analysis | Design basis, device locations, audibility/visibility coverage, code compliance verification, references | **ASSUMPTION**: Fire alarm system calculation |

**Calculation Package Format:**

Each calculation package shall include:

| Section | Content | Source |
|---------|---------|--------|
| Cover Sheet | Project name, calculation title, calculation number, revision, date, engineer, checker, approver, P.Eng. seal (if required) | **ASSUMPTION**: Standard calculation format |
| Design Basis | Facility description, fire protection zones, codes/standards, design criteria, objectives | **ASSUMPTION**: Calculation documentation standard |
| Input Data | All input data with sources cited, assumptions identified | **ASSUMPTION**: Calculation documentation standard |
| Methodology | Calculation methods, formulas, procedures, code references | **ASSUMPTION**: Calculation documentation standard |
| Calculations | Detailed calculations, tables, charts, intermediate results | **ASSUMPTION**: Calculation documentation standard |
| Results and Conclusions | Summary of results, design recommendations, conclusions | **ASSUMPTION**: Calculation documentation standard |
| References | List of references (codes, standards, drawings, data sheets, manufacturer data) | **ASSUMPTION**: Calculation documentation standard |
| Appendices (if applicable) | Supporting information, software output, charts, vendor data | **ASSUMPTION**: Calculation documentation standard |
| Revision History | Revision number, date, description of changes, engineer | **ASSUMPTION**: Revision control |

**Documentation Format:**

| Requirement | Description | Source |
|-------------|-------------|--------|
| Format | Calculation report format with cover sheet, sections, appendices; or calculation sheets with header/footer | **ASSUMPTION**: Standard calculation format |
| Page Numbering | Sequential page numbering with total pages (e.g., "Page X of Y") | **ASSUMPTION**: Standard practice |
| File Format | Electronic calculation files (Excel, MathCAD, PDF of software output, or PDF report) and PDF final package | **ASSUMPTION**: Electronic deliverable |
| Sign-offs | Engineer, checker, approver sign-offs on cover sheet or designated location | **ASSUMPTION**: Quality sign-off requirement |
| P.Eng. Seal | Professional Engineer seal and signature if required by jurisdiction or Employer — **TBD** | **ASSUMPTION**: Professional engineering requirement |

**Documentation Management:**

| Requirement | Description | Source |
|-------------|-------------|--------|
| Calculation Numbering | Per project calculation numbering system — **TBD** | **ASSUMPTION**: Document control |
| Revision Control | Calculation revisions tracked with revision number, date, description | **ASSUMPTION**: Document control |
| Storage | Calculations stored in project document management system — **TBD** | **ASSUMPTION**: Electronic document management |
| Retention | Calculations retained per project retention requirements — **TBD** (typically 25+ years for design calculations) | **ASSUMPTION**: Permanent design record |
| Backup | Electronic calculation files backed up; source files (Excel, MathCAD) retained in addition to PDFs | **ASSUMPTION**: Data management best practice |

**Deliverable Status and Location:**

- Working files: `1_Working/DEL-23.03_Fire_Protection_Design_Calculations/`
- Review copies: `2_Checking/` (during CHECKING state)
- Issued copies: `3_Issued/` (upon ISSUED state)
- Lifecycle state tracked in `_STATUS.md`
- Source: Framework conventions per README.md

**Related Documentation:**

| Deliverable | Relationship | Source |
|-------------|-------------|--------|
| DEL-23.01 | Fire Protection Design Drawing Set — provides layout data as calculation inputs; calculation results appear on drawings | Decomposition PKG-23 |
| DEL-23.02 | Fire Protection Technical Specification — calculation results define specification performance requirements | Decomposition PKG-23 |
| DEL-23.04 | Fire Protection Data Sheet Package — calculation results size equipment; data sheets provide equipment data for calculations | Decomposition PKG-23 |
| DEL-23.05 | Fire Protection Installation & Test Records — testing verifies calculation assumptions and results | Decomposition PKG-23 |
