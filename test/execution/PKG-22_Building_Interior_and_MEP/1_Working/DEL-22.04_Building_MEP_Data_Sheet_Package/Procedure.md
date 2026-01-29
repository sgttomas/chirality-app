# Procedure: DEL-22.04 Building MEP Data Sheet Package

## Purpose

This procedure defines the process for producing and managing **Building MEP Data Sheet Package** within **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Defines and substantiates building MEP equipment in accordance with Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.04 entry; _CONTEXT.md

### Scope of This Procedure

This procedure covers:
- **Data sheet preparation**: Steps to develop equipment data sheets from design basis through approved data sheets
- **Vendor coordination**: Obtaining and validating vendor-supplied data
- **Quality control**: Review and verification processes
- **Coordination**: Interface coordination with related deliverables
- **Documentation**: Data sheet formatting and records management

**Deliverable Classification:**
- **Type:** Data Sheet
- **Responsible Party:** D&B Contractor

**Source:** _CONTEXT.md; standard data sheet workflow

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)

**Source:** _DEPENDENCIES.md

**Upstream Inputs Required**:

1. **Design Calculations** (DEL-22.03):
   - Equipment capacities (heating, cooling, flow, pressure)
   - Operating conditions (temperature, pressure)
   - Design margins and safety factors

2. **Design Drawings** (DEL-22.01):
   - Equipment tags and locations
   - Equipment schedules (preliminary)
   - Space constraints and mounting requirements

3. **Technical Specifications** (DEL-22.02):
   - Performance requirements
   - Material specifications
   - Manufacturer requirements

4. **Interface Requirements**:
   - Control system requirements (PKG-19)
   - Electrical power availability (PKG-17)
   - Utility service parameters (PKG-03)

**Source:** Package interface descriptions; Specification.md IF-01 through IF-05

### Reference Materials

**Required References**:
- See `_REFERENCES.md` for applicable reference documents
- See `execution/PKG-22_Building_Interior_and_MEP/0_References/` for reference materials

**Key Reference Documents**:
- Employer's Requirements Volume 2 — **TBD** (location TBD)
- ASHRAE 90.1 (equipment efficiency requirements)
- NFPA 13 (fire protection equipment requirements)
- Manufacturer catalogs and data sheets
- Project data sheet templates — **TBD** (location TBD)

**Source:** Specification.md Standards section; _REFERENCES.md

### Personnel Requirements

**Minimum Qualifications** (ASSUMPTION: to be confirmed per project Quality Plan):

| Role | Qualification |
|------|--------------|
| Equipment Engineer | Engineering degree with MEP equipment selection experience |
| Lead MEP Engineer | Professional Engineer (P.Eng.) registered in BC; responsible for data sheet approval |
| Procurement Coordinator | Familiar with equipment procurement and vendor coordination |
| Reviewer | Independent engineer to verify data sheets against requirements |

**Source:** ASSUMPTION: standard EPC personnel qualifications

### Tools and Resources

**Required Resources**:
- Project data sheet templates (Excel, PDF forms, or similar) — **TBD**
- Manufacturer catalogs and online configurators
- Equipment selection software (for pumps, fans, etc.)
- Access to vendor technical support for equipment selection assistance

**Source:** ASSUMPTION: standard equipment data sheet tools

## Steps

### Step 1: Parameter Identification

**Objective**: Identify required equipment parameters from design calculations and drawings.

**Requirements Addressed**: Supports FR-01 (completeness), establishes foundation for FR-02/03/04 (equipment-specific requirements). Addresses Specification.md IF-03 (support from calculations).

**Activities**:

1.1. **Extract Equipment List**:
   - Obtain equipment list from DEL-22.01 drawings (equipment tags and descriptions)
   - Organize by system (HVAC, plumbing, fire protection)

1.2. **Extract Performance Requirements from DEL-22.03**:
   - HVAC: heating/cooling capacities, airflow, efficiency requirements
   - Plumbing: flow rates, pressures, tank capacities
   - Fire Protection: flow, pressure, design area, K-factors

1.3. **Extract Specification Requirements from DEL-22.02**:
   - Performance criteria
   - Material requirements
   - Certification requirements (UL, FM, CSA, NSF/ANSI)
   - Acceptable manufacturers

1.4. **Identify Interface Requirements**:
   - Electrical power requirements (coordinate with PKG-17)
   - Control interfaces (coordinate with PKG-19)
   - Utility connections (coordinate with PKG-03)

**Verification**: Parameter list reviewed and approved by lead engineer.

**Source:** Specification.md IF-01/02/03; Procedure workflow

### Step 2: Data Population

**Objective**: Populate data sheets with required parameters and project requirements.

**Requirements Addressed**: Addresses FR-01 through FR-04 (equipment-specific requirements), PR-03 (equipment ratings), IF-04/05 (control and electrical interfaces).

**Activities**:

2.1. **Create Data Sheets**:
   - Use project data sheet templates for each equipment item
   - Assign equipment tag numbers per project numbering system

2.2. **Populate Required Performance**:
   - Enter capacities, operating conditions, and efficiency requirements from Step 1
   - Document design margins (typically 10-15% beyond calculated requirements)

2.3. **Define Materials and Construction**:
   - Specify materials per DEL-22.02 specifications
   - Specify required certifications and approvals
   - Define environmental ratings (indoor/outdoor, temperature range, corrosion resistance)

2.4. **Define Interfaces**:
   - Electrical: voltage, phase, FLA, MCA, MOCP, disconnect requirements
   - Controls: control points, communication protocol, BAS integration
   - Piping/Ductwork: connection sizes and types
   - Mounting: support and installation requirements

2.5. **Add Notes and Special Requirements**:
   - Installation clearances and access requirements
   - Testing and commissioning requirements
   - Spare parts recommendations
   - Warranty requirements

**Verification**: Data sheets reviewed for completeness by equipment engineer.

**Source:** Specification.md FR-01 through FR-04; Guidance.md (equipment content sections)

### Step 3: Vendor Coordination

**Objective**: Obtain vendor data and confirm equipment selections meet requirements.

**Requirements Addressed**: Addresses PR-01 (vendor data accuracy), PR-02 (efficiency compliance), FR-02.2/03.2/04.2 (certifications and approvals).

**Activities**:

3.1. **Issue Requests for Information (RFIs) to Vendors**:
   - Send data sheets with required parameters to multiple vendors (typically 3 vendors for competitive selection)
   - Request vendor data sheets, performance curves, and submittal data

3.2. **Review Vendor Submittals**:
   - Verify vendor equipment meets required performance (capacity, efficiency, operating range)
   - Verify certifications and approvals are documented (UL, FM, CSA, NSF/ANSI, ASHRAE 90.1 efficiency)
   - Review performance curves (pumps, fans) to confirm equipment operates at required point
   - Verify equipment dimensions fit space shown on DEL-22.01 drawings

3.3. **Compare Vendor Options**:
   - Compare multiple vendors for cost, performance, lead time, and quality
   - Document comparison in vendor evaluation matrix (if required)

3.4. **Select Equipment**:
   - Select equipment that meets all requirements at best value
   - Document manufacturer, model number, and vendor data sheet reference in data sheet
   - Obtain approval from procurement (if required) before committing to vendor

**Verification**: Vendor data validated against requirements per Specification.md PR-01; lead engineer approves vendor selections.

**Source:** Specification.md PR-01, FR-02/03/04; Guidance.md (Vendor Data Validation)

### Step 4: Verification

**Objective**: Verify data sheets are complete, accurate, and coordinated with other deliverables.

**Requirements Addressed**: Addresses all interface requirements (IF-01 through IF-05), quality requirements (QR-01/02), and performance requirements (PR-02/03).

**Activities**:

4.1. **Self-Check**:
   - Equipment engineer verifies data sheet completeness per FR-01
   - Verify all required parameters documented
   - Verify vendor data is current and accurate

4.2. **Technical Review**:
   - Independent reviewer verifies equipment meets design requirements
   - Verify capacities match DEL-22.03 calculations
   - Verify efficiency meets ASHRAE 90.1 requirements
   - Verify certifications are documented

4.3. **Interface Coordination**:
   - Cross-check equipment tags with DEL-22.01 drawings (IF-01)
   - Cross-check performance requirements with DEL-22.02 specifications (IF-02)
   - Cross-check capacities with DEL-22.03 calculations (IF-03)
   - Coordinate control interfaces with PKG-19 (IF-04)
   - Coordinate electrical requirements with PKG-17 (IF-05)

4.4. **Format and Consistency Check**:
   - Verify data sheet format per project templates (QR-02)
   - Verify equipment tagging consistent across all deliverables
   - Verify units and nomenclature consistent

**Verification**: All checks completed; all coordination items resolved.

**Source:** Specification.md Verification section; QR-01/02

### Step 5: Approval and Issue

**Objective**: Obtain final approval and issue data sheets.

**Activities**:

5.1. **Discipline Lead Approval**:
   - Lead MEP engineer reviews and approves data sheets
   - Sign-off confirms data sheets are complete, accurate, and coordinated

5.2. **Issue Process**:
   - Generate PDF of complete data sheet package
   - Submit to project document control for distribution
   - Issue to procurement for equipment purchase
   - Issue to construction for installation reference

5.3. **Record Management**:
   - Copy issued package to `3_Issued/` folder
   - Retain working files in `1_Working/` for future revisions
   - Update equipment register or database (if required)

5.4. **Revision Control** (if required during procurement or construction):
   - If vendor substitutions or changes are required, revise data sheets
   - Update revision history and reissue through approval process
   - Coordinate changes with affected deliverables (drawings, specifications)

**Verification**: Data sheets issued with proper approvals and document control.

**Source:** ASSUMPTION: standard data sheet issue process

## Verification

### Quality Control Checkpoints

**Self-Check (Equipment Engineer)**:
- [ ] All equipment from DEL-22.01 have data sheets
- [ ] All required parameters documented per FR-01
- [ ] Vendor data obtained and validated per PR-01
- [ ] Format and tagging consistent per QR-02

**Technical Review (Reviewer)**:
- [ ] Equipment meets DEL-22.03 calculated requirements (IF-03)
- [ ] Equipment meets DEL-22.02 specification requirements (IF-02)
- [ ] Equipment efficiency meets ASHRAE 90.1 per PR-02
- [ ] Certifications and approvals documented per FR-02/03/04
- [ ] Vendor data validated and reasonable

**Coordination Review (Lead Engineer)**:
- [ ] Equipment tags match DEL-22.01 drawings (IF-01)
- [ ] Control interfaces coordinated with PKG-19 (IF-04)
- [ ] Electrical requirements coordinated with PKG-17 (IF-05)
- [ ] Utility connections coordinated with PKG-03

**Approval (Discipline Lead)**:
- [ ] All checks completed and signed off
- [ ] Data sheets meet professional standard
- [ ] Ready for procurement and construction

**Source:** Specification.md Verification section; Procedure quality checkpoints

### Sign-Off Requirements

**ASSUMPTION: Standard sign-off protocol to be confirmed per project Quality Management Plan**

| Milestone | Required Sign-Offs |
|-----------|-------------------|
| Parameters Identified | Lead Equipment Engineer |
| Data Populated | Equipment Engineer (self-check) |
| Vendor Data Obtained | Equipment Engineer, Procurement Coordinator |
| Verification Complete | Reviewer, Lead Engineer |
| Approval for Issue | Discipline Lead (P.Eng. BC), Document Control Manager |

**Source:** ASSUMPTION: standard EPC data sheet sign-off requirements

## Records

### Documentation Outputs

**Primary Deliverables** (per Decomposition DEL-22.04):
- **HVAC equipment datasheets**
- **Plumbing equipment datasheets**
- **Fire suppression system datasheets**

**Supporting Documentation**:
- Equipment tag register
- Vendor data sheet collection
- Vendor evaluation matrix (if used)
- Equipment selection justification

**Source:** Decomposition REVISED_v2.md, DEL-22.04 anticipated artifacts; Specification.md

### Record Management

**File Storage Locations**:

| Stage | Location | Contents |
|-------|----------|----------|
| Working | `1_Working/` | Active data sheet files, vendor data, work-in-progress |
| Checking | `2_Checking/To/` | Copies submitted for review (with DEL-ID + date + rev) |
| Issued | `3_Issued/` | Issued data sheets (PDF + native files) |

**Source:** README.md Section 6 (review and issue conventions)

**File Naming Convention** (ASSUMPTION: to be confirmed):
- Native files: `DEL-22.04_[System]_DataSheets_[Rev].[ext]`
- Issued PDF: `DEL-22.04_[System]_DataSheets_[Rev]_[Date].pdf`

**Retention Requirements**:
- Working files: Retain through project closeout
- Issued data sheets: Retain in project archives; form part of operations and maintenance documentation
- Data sheets required for equipment replacement and facility modifications

**Source:** ASSUMPTION: standard document control and records management
