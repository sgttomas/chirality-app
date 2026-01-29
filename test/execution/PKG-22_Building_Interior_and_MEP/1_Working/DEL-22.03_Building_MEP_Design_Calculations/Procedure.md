# Procedure: DEL-22.03 Building MEP Design Calculations

## Purpose

This procedure defines the process for producing and managing **Building MEP Design Calculations** within **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Provides the engineering basis and sizing/verification calculations for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.03 entry; _CONTEXT.md

### Scope of This Procedure

This procedure covers:
- **Calculation preparation**: Steps to develop MEP design calculations from design basis through approved calculations
- **Quality control**: Checking and verification processes
- **Coordination**: Interface coordination with related deliverables
- **Documentation**: Calculation formatting and records management

**Deliverable Classification:**
- **Type:** Calculation
- **Responsible Party:** D&B Contractor

**Source:** _CONTEXT.md; standard calculation workflow

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)

**Source:** _DEPENDENCIES.md

**Upstream Inputs Required** (ASSUMPTION: typical MEP calculation inputs; to be confirmed):

1. **Building Architecture and Geometry** (PKG-21):
   - Building floor plans and elevations
   - Envelope construction details (wall/roof assemblies, window types, insulation)
   - Room dimensions and occupancy types

2. **Site Utilities** (PKG-03):
   - Fire water supply availability (pressure and flow)
   - Domestic water service parameters (pressure at meter)
   - Sanitary sewer connection elevation

3. **Electrical Loads** (PKG-17):
   - MCC equipment heat dissipation (for HVAC cooling loads)
   - Lighting power density (for internal gains)

4. **Control Strategy** (PKG-19):
   - HVAC control approach (affects equipment selection and operating modes)

5. **Design Basis**:
   - Employer's Requirements — **TBD** (location TBD)
   - Design criteria memorandum — **TBD** (location TBD)
   - Climate data for Surrey, BC (from NBC 2020)

**Source:** Package interface descriptions; ASSUMPTION: standard calculation input requirements

### Reference Materials

**Required References**:
- See `_REFERENCES.md` for applicable reference documents
- See `execution/PKG-22_Building_Interior_and_MEP/0_References/` for reference materials

**Key Reference Documents** (to be confirmed):
- Employer's Requirements Volume 2 — **TBD** (location TBD)
- NBC 2020 (National Building Code of Canada)
- ASHRAE 90.1, ASHRAE 62.1, ASHRAE Fundamentals Handbook
- CSA B64 series (plumbing fixture units and pipe sizing)
- NFPA 13 (fire protection hydraulic calculations)

**Source:** Specification.md Standards section; _REFERENCES.md

### Personnel Requirements

**Minimum Qualifications** (ASSUMPTION: to be confirmed per project Quality Plan):

| Role | Qualification |
|------|--------------|
| Lead MEP Engineer | Professional Engineer (P.Eng.) registered in British Columbia; minimum 5 years MEP design experience |
| HVAC Engineer | Engineering degree with HVAC load calculation experience; proficiency in load calculation software |
| Plumbing Engineer | Engineering degree or technologist with plumbing design experience |
| Fire Protection Engineer | NICET Level III or P.Eng. with fire protection experience; proficiency in hydraulic calculation software |
| Checker | Independent qualified engineer (P.Eng. preferred), not involved in original calculation |

**Professional Seal Requirement**: Calculations must be prepared under responsible charge of P.Eng. registered in BC; seal may be required per NBC 2020 or contract.

**Source:** NBC 2020 professional requirements; ASSUMPTION: standard EPC personnel qualifications

### Tools and Software

**Required Software** (ASSUMPTION: to be confirmed):
- **HVAC Load Calculations**: Carrier HAP, Trane TRACE, IES VE, or equivalent approved software
- **Fire Protection Hydraulics**: HydraCAD, AutoSPRINK, or equivalent NFPA 13 approved software
- **Plumbing/General Calculations**: Excel, MathCAD, or equivalent
- **PDF Generation**: For issuing calculations

**Software Validation**: All software shall have documented validation per recognized standards (e.g., ASHRAE 140 for building energy software).

**Source:** ASSUMPTION: standard MEP calculation software suite; Specification.md (Calculation Software Standards)

## Steps

### Step 1: Input Data Collection

**Objective**: Gather all required input data for calculations.

**Requirements Addressed**: This step supports all calculation requirements by establishing the data foundation. Addresses Specification.md PR-01 (accuracy), QR-03 (documentation).

**Activities**:

1.1. **Establish Design Basis**:
   - Review Employer's Requirements for MEP system requirements — **TBD** (location TBD)
   - Extract design temperatures (indoor/outdoor) from NBC 2020 climate data for Surrey, BC
   - Establish occupancy and use patterns for ventilation calculations

1.2. **Collect Building Data** (from PKG-21):
   - Building geometry (floor area, volume, dimensions)
   - Envelope construction (wall/roof assemblies with R-values)
   - Window properties (area, U-value, solar heat gain coefficient)
   - Internal loads (lighting power density, equipment loads, occupancy)

1.3. **Collect Utility Data** (from PKG-03):
   - Fire water supply: available pressure and flow
   - Domestic water: service pressure at meter
   - Sanitary sewer: invert elevation at connection

1.4. **Document Sources**:
   - Create input data summary sheet with all values and sources
   - Flag any assumptions or estimated values for future confirmation

**Verification**: Input data reviewed and approved by lead engineer.

**Source:** ASSUMPTION: standard calculation input data process; Specification.md IF-04

### Step 2: Methodology Selection

**Objective**: Select appropriate calculation methods and tools for each calculation type.

**Requirements Addressed**: Addresses Specification.md PR-01 (calculation method), FR-02 through FR-04 (specific calculation requirements).

**Activities**:

2.1. **HVAC Load Calculation Method**:
   - Select load calculation software (e.g., Carrier HAP, Trane TRACE)
   - Confirm software has documented validation (ASHRAE 140 or equivalent)
   - Establish calculation methodology: ASHRAE Fundamentals, ASHRAE 62.1 for ventilation

2.2. **Plumbing Sizing Method**:
   - Use fixture unit method per NBC 2020 / CSA B64
   - Establish pipe sizing tables and pressure loss calculation method
   - Select drainage sizing method per NBC 2020

2.3. **Fire Protection Hydraulic Calculation Method**:
   - Select hydraulic calculation software (HydraCAD, AutoSPRINK, or equivalent)
   - Confirm software approved for NFPA 13 calculations
   - Establish design area and density per NFPA 13

2.4. **Document Methodology**:
   - Prepare calculation methodology section citing applicable codes and standards
   - Document software versions and validation status

**Verification**: Methodology reviewed and approved by lead engineer and checker.

**Source:** ASSUMPTION: standard methodology selection process; Specification.md (Applicable Codes and Standards)

### Step 3: Calculation Execution

**Objective**: Perform all required calculations per selected methodologies.

**Requirements Addressed**: Executes all functional requirements (FR-01 through FR-04) from Specification.md. Produces calculations supporting Datasheet.md parameters.

**Activities**:

3.1. **HVAC Load Calculations** (Specification.md FR-02):
   - Build building model in load calculation software
   - Input envelope properties, internal loads, occupancy
   - Run heating load calculation for design winter conditions
   - Run cooling load calculation for design summer conditions
   - Calculate ventilation requirements per ASHRAE 62.1
   - Size HVAC equipment based on peak loads plus design margin (typically 10-15%)
   - Document results: equipment capacities, airflow rates, heating/cooling loads

3.2. **Plumbing Sizing Calculations** (Specification.md FR-03):
   - List all plumbing fixtures and assign fixture units per NBC 2020 / CSA B64
   - Calculate total fixture units for each pipe section
   - Size water supply piping using fixture unit tables
   - Calculate pressure losses and verify adequate pressure at fixtures
   - Size hot water heater (if required) based on peak demand and recovery
   - Size drainage piping using drainage fixture units and slope requirements
   - Document results: pipe sizes, flow rates, pressures

3.3. **Fire Protection Hydraulic Calculations** (Specification.md FR-04):
   - Build sprinkler system model in hydraulic calculation software
   - Input pipe sizes, fittings, sprinkler types, and elevations
   - Establish design area per NFPA 13 (most hydraulically remote area)
   - Run hydraulic calculation to determine required pressure and flow at source
   - Add hose stream demand per NFPA 13
   - Compare calculated demand to available supply from PKG-03
   - Document results: required flow and pressure, comparison to available supply

3.4. **Additional Calculations** (as required):
   - Ductwork sizing (if not in load calculation software)
   - Electrical load calculations for MEP equipment (coordinate with PKG-17)
   - Other calculations as needed to support design

**Verification**: Self-check by originator; results reasonableness review by lead engineer.

**Source:** ASSUMPTION: standard calculation execution process; Specification.md FR-02/03/04

### Step 4: Results Interpretation and Summary

**Objective**: Interpret calculation results, assess reasonableness, and prepare summary.

**Requirements Addressed**: Addresses Specification.md PR-02 (design margins), PR-03 (code compliance demonstration), QR-03 (documentation).

**Activities**:

4.1. **Results Reasonableness Check**:
   - Compare results to industry benchmarks (e.g., typical cooling load per square foot for similar buildings)
   - Compare to similar projects or published guidelines
   - Identify any results that seem unexpectedly high or low and investigate

4.2. **Design Margin Assessment**:
   - Verify design margins are appropriate (typically 10-15% for equipment sizing)
   - Justify any deviations from standard margins
   - Document equipment selection margins in results summary

4.3. **Code Compliance Summary**:
   - Prepare summary demonstrating compliance with NBC 2020, ASHRAE 90.1, ASHRAE 62.1, NFPA 13
   - Document any code-required features or design decisions
   - Identify any areas requiring further review or AHJ approval

4.4. **Results Summary**:
   - Prepare calculation summary sheet with key results
   - Tabulate equipment sizes and capacities for easy reference
   - Highlight any critical assumptions or design decisions

**Verification**: Results summary reviewed by lead engineer.

**Source:** ASSUMPTION: standard calculation results interpretation; Specification.md PR-02/03

### Step 5: Independent Check

**Objective**: Independent qualified checker verifies calculations.

**Requirements Addressed**: Addresses Specification.md QR-01 (independent check), QR-02 (professional responsibility), QR-03 (documentation standards).

**Activities**:

5.1. **Checker Assignment**:
   - Assign independent checker (not involved in original calculation)
   - Checker must be qualified engineer, preferably P.Eng. registered in BC

5.2. **Check Scope**:
   - Verify input data is correct and from approved sources
   - Verify methodology is appropriate and complies with codes
   - Verify calculation execution (spot-check key calculations or full recalculation)
   - Verify software inputs and outputs are reasonable
   - Verify results support equipment selections in DEL-22.01 and DEL-22.04
   - Verify code compliance per Specification.md PR-03

5.3. **Comment Generation**:
   - Checker prepares comment list with any errors, questions, or recommendations
   - Comments categorized by severity (critical, major, minor, observation)

5.4. **Comment Resolution**:
   - Originator reviews checker comments
   - Resolve all critical and major comments (may require recalculation)
   - Address minor comments and observations
   - Document resolution in comment/response log

5.5. **Checker Sign-Off**:
   - Checker reviews comment resolutions
   - Checker signs calculation as verified
   - Unresolved comments escalated to lead engineer or project manager

**Verification**: Independent check completed; all comments resolved and documented.

**Source:** ASSUMPTION: standard engineering check process; Specification.md QR-01

### Step 6: Coordination and Approval

**Objective**: Coordinate calculations with related deliverables and obtain final approval.

**Requirements Addressed**: Addresses Specification.md IF-01 through IF-04 (interface coordination), QR-02 (professional review).

**Activities**:

6.1. **Cross-Check with DEL-22.01 Drawings** (Specification.md IF-01):
   - Verify equipment sizes on drawings match calculation results
   - Verify system capacities shown on schedules match calculations
   - Resolve any discrepancies

6.2. **Cross-Check with DEL-22.02 Specifications** (Specification.md IF-02):
   - Verify specified equipment performance requirements are achievable per calculations
   - Verify specified materials are adequate for calculated conditions
   - Resolve any discrepancies

6.3. **Cross-Check with DEL-22.04 Datasheets** (Specification.md IF-03):
   - Verify equipment parameters in datasheets match calculation results
   - Ensure vendor selections meet calculated requirements
   - Resolve any discrepancies

6.4. **Coordinate with Other Packages**:
   - Confirm fire water supply from PKG-03 is adequate per calculations
   - Confirm domestic water supply from PKG-03 is adequate
   - Coordinate electrical loads with PKG-17
   - Coordinate control strategy with PKG-19

6.5. **Professional Review**:
   - Professional Engineer (P.Eng. BC) reviews calculations for professional standard of care
   - P.Eng. confirms calculations demonstrate code compliance
   - P.Eng. applies seal if required by NBC 2020 or contract

6.6. **Discipline Lead Approval**:
   - Lead MEP engineer approves calculations for issue
   - Sign-off confirms calculations are complete, checked, and coordinated

**Verification**: All coordination items resolved; professional review and approval completed.

**Source:** ASSUMPTION: standard calculation coordination and approval process; Specification.md IF-01/02/03/04, QR-02

### Step 7: Issue and Record

**Objective**: Issue calculations and maintain records.

**Activities**:

7.1. **Final Formatting**:
   - Verify all calculation sheets have project identification, titles, signatures
   - Verify page numbering and table of contents
   - Apply calculation number per project numbering system — **TBD**

7.2. **Issue Process**:
   - Generate PDF of complete calculation package
   - Submit to project document control for distribution
   - File native calculation files (software files, spreadsheets) per document control procedure

7.3. **Record Management**:
   - Copy issued package to `3_Issued/` folder
   - Update `_STATUS.md` to ISSUED with date and revision information — **Note:** Status files not to be changed per user instructions; this is for future reference
   - Retain working files in `1_Working/` for future revisions

7.4. **Revision Control**:
   - If calculations are revised during design or construction, follow revision process:
     - Update calculation sheets with revision markers
     - Update revision history on cover sheet
     - Reissue through check and approval process
     - Maintain revision log

**Verification**: Calculations issued with proper document control; records filed.

**Source:** ASSUMPTION: standard calculation issue process

## Verification

### Quality Control Checkpoints

**Self-Check (Originator)**:
- [ ] All input data documented with sources
- [ ] All assumptions documented and justified
- [ ] Methodology appropriate and complies with codes
- [ ] Calculations traceable and reproducible
- [ ] Results summarized clearly
- [ ] Code compliance demonstrated
- [ ] Calculation format and documentation standards met

**Independent Check (Checker)**:
- [ ] Input data verified correct
- [ ] Methodology verified appropriate
- [ ] Calculations spot-checked or fully recalculated
- [ ] Results reasonable compared to benchmarks
- [ ] Code compliance verified (NBC 2020, ASHRAE, NFPA 13, etc.)
- [ ] Software inputs and outputs verified
- [ ] Calculation supports design (DEL-22.01, DEL-22.02, DEL-22.04)

**Coordination Review (Lead Engineer)**:
- [ ] Equipment sizes match DEL-22.01 drawings
- [ ] Performance requirements match DEL-22.02 specifications
- [ ] Equipment parameters match DEL-22.04 datasheets
- [ ] Interfaces coordinated with PKG-03, PKG-17, PKG-19, PKG-21

**Professional Review (P.Eng.)**:
- [ ] Calculations meet professional standard of care
- [ ] Code compliance demonstrated adequately
- [ ] Assumptions reasonable and documented
- [ ] Results support design decisions

**Source:** Specification.md Verification section; ASSUMPTION: standard calculation quality control

### Sign-Off Requirements

**ASSUMPTION: Standard sign-off protocol to be confirmed per project Quality Management Plan**

| Milestone | Required Sign-Offs |
|-----------|-------------------|
| Input Data Collected | Lead MEP Engineer |
| Methodology Selected | Lead MEP Engineer, Checker |
| Calculations Executed | Originator (self-check), Lead Engineer (reasonableness) |
| Independent Check Complete | Checker (P.Eng. or qualified engineer) |
| Coordination Complete | Lead Engineer, affected discipline leads |
| Professional Review | Professional Engineer Seal (P.Eng. BC, if required) |
| Issue for Construction | Discipline Lead, Document Control Manager |

**Source:** ASSUMPTION: standard EPC calculation sign-off requirements

## Records

### Documentation Outputs

**Primary Deliverables** (per Decomposition DEL-22.03):
- **HVAC load calculations**
- **Plumbing sizing calculations**

**Additional Calculations** (inferred from scope):
- Ventilation calculations (ASHRAE 62.1)
- Fire protection hydraulic calculations (NFPA 13)
- Ductwork sizing (as required)
- Electrical load calculations (coordinate with PKG-17)

**Source:** Decomposition REVISED_v2.md, DEL-22.03 anticipated artifacts; Specification.md

**Supporting Documentation**:
- Calculation cover sheets with signatures
- Design basis and assumptions summary
- Input data sources and references
- Checker comment/response log
- Software validation documentation

**Source:** Specification.md Documentation section

### Record Management

**File Storage Locations**:

| Stage | Location | Contents |
|-------|----------|----------|
| Working | `1_Working/` | Active calculation files, native software files, work-in-progress |
| Checking | `2_Checking/To/` | Copies submitted for review (with DEL-ID + date + rev) |
| Issued | `3_Issued/` | Issued calculations (PDF + native files) |

**Source:** README.md Section 6 (review and issue conventions)

**File Naming Convention** (ASSUMPTION: to be confirmed):
- Native files: `DEL-22.03_[Calculation-Title]_[Rev].[ext]`
- Issued PDF: `DEL-22.03_[Calculation-Title]_[Rev]_[Date].pdf`

**Retention Requirements**:
- Working files: Retain through project closeout, archive per project procedures
- Issued calculations: Retain in project archives per company and regulatory requirements — **TBD** (retention period per project records management plan)
- Calculations form part of design records and may be required for facility operations, modifications, and regulatory compliance

**Source:** ASSUMPTION: standard document control and records management

### Audit Trail

**Calculation Development Records to Maintain**:
- Input data sources and correspondence
- Methodology selection rationale
- Software validation documentation
- Checker comments and resolution log
- Coordination meeting minutes (with other packages)
- Revision history and change justifications

**Purpose**: Demonstrate due diligence, support professional liability, enable future design modifications or investigations.

**Source:** ASSUMPTION: standard engineering records management practice
