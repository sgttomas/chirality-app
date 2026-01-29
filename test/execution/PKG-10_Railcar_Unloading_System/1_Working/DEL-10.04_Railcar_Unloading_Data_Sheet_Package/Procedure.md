# Procedure: DEL-10.04 Railcar Unloading Data Sheet Package

## Purpose

This procedure defines the process for producing and managing the **Railcar Unloading Data Sheet Package** within **PKG-10 Railcar Unloading System**.

**Scope of Procedure:**
- Development of equipment data sheets for railcar unloading system
- Vendor coordination for equipment data
- Review, approval, and issue workflow

**Deliverable Type:** Data Sheet
**Responsible Party:** D&B Contractor
**Discipline:** Process

## Prerequisites

### Dependencies

- **Dependency Tracking:** NOT_TRACKED — dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)
- **Upstream Inputs (typical):**

  | Input | Source | Status |
  |-------|--------|--------|
  | Equipment arrangement | DEL-10.01 Design Drawing Set | **TBD** |
  | Equipment specifications | DEL-10.02 Technical Specification | **TBD** |
  | Equipment sizing | DEL-10.03 Design Calculations | **TBD** |
  | Project tagging standard | ER / project procedures | **TBD** |
  | Data sheet templates | ER / project standards | **TBD** |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope; DEL-10.04 definition |
| Employer's Requirements | `test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` | Data sheet requirements (clauses **TBD**) |
| Specification.md | This deliverable folder | Requirements for data sheets |
| Guidance.md | This deliverable folder | Data sheet principles and examples |
| Datasheet.md | This deliverable folder | Equipment list and fields |
| DEL-10.01 | PKG-10 folder | Equipment locations, P&ID references |
| DEL-10.02 | PKG-10 folder | Equipment specifications |
| DEL-10.03 | PKG-10 folder | Equipment sizing basis |

### Personnel Requirements

| Role | Qualification | Responsibility |
|------|---------------|----------------|
| Data Sheet Author | Process discipline; **TBD** qualifications | Data sheet development |
| Checker | Process discipline; independent | Data sheet review |
| Discipline Lead | Process discipline; approval authority | Data sheet approval |
| Vendor Coordinator | Procurement/technical | Vendor data coordination |
| Document Controller | Document control procedures | Issue and transmittal |

**ASSUMPTION:** Personnel competency requirements per project quality procedures.

## Steps

### Step 1: Define Data Sheet List and Templates

**Objective:** Establish data sheet list and templates based on equipment scope.

**Actions:**
1. Review Specification.md §Scope for equipment to be documented
2. Review Datasheet.md §Construction for anticipated artifacts
3. Confirm data sheet list:

   | Equipment Type | Quantity | Data Sheet Template |
   |----------------|----------|---------------------|
   | Unloading Arms | 32 | Arm data sheet template |
   | Quick-Connect Couplers | 32 (may combine) | Coupler section or separate |
   | Sump Pumps | **TBD** | Pump data sheet template |

4. Obtain/confirm data sheet templates per project standards
5. Establish equipment tag numbering scheme per project tagging standard

**Output:** Approved data sheet list, templates, and tagging scheme.

**Verification:** Discipline lead sign-off on data sheet list.

### Step 2: Gather Input Data

**Objective:** Collect design data required to populate data sheets.

**Actions:**
1. Obtain process conditions from DEL-10.03 calculations:
   - Flow rates per station
   - Operating temperatures
   - Design pressures
2. Obtain equipment specifications from DEL-10.02:
   - Material requirements
   - Performance requirements
   - Standards compliance
3. Obtain layout information from DEL-10.01:
   - Equipment locations
   - P&ID references
   - Arrangement details
4. Identify vendor data requirements (if vendor-selected equipment)

**Output:** Input data compilation for data sheet population.

**Traceability:**

| Data Sheet Field | Source |
|------------------|--------|
| Process conditions | DEL-10.03 |
| Material specifications | DEL-10.02 |
| Equipment locations | DEL-10.01 |
| Performance requirements | DEL-10.02 |

### Step 3: Populate Data Sheets

**Objective:** Complete data sheets for all equipment.

**Actions:**

#### 3a: Unloading Arm Data Sheets (32)
1. Populate identification section for each arm (tag, service, location)
2. Populate process data from DEL-10.03
3. Populate mechanical/construction data per DEL-10.02
4. Populate quick-connect coupler section
5. Populate materials per DEL-10.02
6. Reference applicable standards
7. Mark **TBD** where data not yet available

#### 3b: Sump Pump Data Sheet(s)
1. Populate identification section
2. Populate operating conditions from DEL-10.03 (containment drainage requirements)
3. Populate pump construction details
4. Populate motor/driver data (coordinate with PKG-17)
5. Populate materials per DEL-10.02
6. Reference applicable standards

**Output:** Draft data sheet package.

**Quality Checks (during population):**
- Tag numbers sequential and consistent
- Units consistent throughout
- P&ID references correct
- Values plausible for application

### Step 4: Vendor Coordination (as required)

**Objective:** Obtain vendor-specific data for selected equipment.

**Actions:**
1. Identify equipment requiring vendor data
2. Issue requisitions or technical queries to vendors
3. Receive and review vendor data
4. Incorporate vendor data into data sheets
5. Flag any vendor data that conflicts with project requirements

**Output:** Data sheets updated with vendor data.

**Verification:** Technical review of vendor data for compliance with DEL-10.02.

### Step 5: Review and Check

**Objective:** Verify data sheet accuracy, completeness, and consistency.

**Actions:**
1. Self-check by author:
   - All 32 arms have data sheets
   - All required fields populated or marked TBD
   - Tagging consistent
   - Units consistent
2. Issue for independent check
3. Checker reviews against:
   - Specification.md requirements (FN-xx, UA-xx, SP-xx, QA-xx)
   - DEL-10.02 specification requirements
   - DEL-10.03 calculation results
   - DEL-10.01 drawing references
4. Resolve checker comments
5. Update data sheets

**Output:** Checked data sheet package.

**Verification:** Checker sign-off (QA-04).

### Step 6: Approval and Issue

**Objective:** Obtain approval and issue data sheet package.

**Actions:**
1. Submit checked data sheet package for discipline lead approval
2. Discipline lead reviews:
   - Completeness (all equipment covered)
   - Consistency across package
   - Alignment with specifications
3. Obtain sign-offs (author, checker, approver)
4. Finalize document metadata (Datasheet.md §Attributes):
   - Data sheet numbers (confirmed)
   - Revision (initial issue)
   - Date
   - Sign-offs
5. Prepare transmittal per project document control procedure (**TBD**)
6. Issue data sheet package
7. File records per §Records below

**Output:** Issued data sheet package.

**Verification:**
- Discipline lead approval sign-off
- Document controller confirmation of issue

## Verification

**Verification Summary:**

| Step | Verification Activity | Responsible | Record |
|------|----------------------|-------------|--------|
| 1 | Data sheet list approval | Discipline lead | Approved list |
| 2 | Input data compilation | Author | Input summary |
| 3 | Draft completion | Author | Draft data sheets |
| 4 | Vendor data review | Author | Vendor correspondence |
| 5 | Independent check | Checker | Checker sign-off |
| 6 | Approval | Discipline lead | Approval sign-off |
| 6 | Issue confirmation | Document controller | Transmittal record |

**Requirement Verification Matrix:**

| Req ID | Requirement Summary | Verification Step | Method |
|--------|---------------------|-------------------|--------|
| FN-01 | 32 unloading arm data sheets | 3a, 5 | Document count |
| FN-02 | Quick-connect coupler data sheets | 3a, 5 | Document check |
| FN-03 | Sump pump data sheet | 3b, 5 | Document check |
| FN-04–07 | Data sheet content fields | 3, 5 | Document review |
| UA-01–06 | Arm data sheet content | 3a, 5 | Document review |
| SP-01–05 | Pump data sheet content | 3b, 5 | Document review |
| QA-01 | Consistent tagging | 3, 5 | Tag audit |
| QA-02 | Consistent units | 3, 5 | Unit check |
| QA-03 | Document metadata | 6 | Document check |
| QA-04 | Independent check | 5 | Checker sign-off |
| QA-05 | Alignment with DEL-10.02 | 5 | Cross-document review |
| IF-01–03 | Interface requirements | 2, 5 | Cross-document review |

## Records

**Documentation Outputs:**

| Record | Description | Filing Location |
|--------|-------------|-----------------|
| Unloading Arm Data Sheets (32) | Individual arm specifications | `3_Issued/` |
| Quick-Connect Coupler Data Sheets | Coupler specifications | `3_Issued/` |
| Sump Pump Data Sheet(s) | Pump specifications | `3_Issued/` |
| Equipment List | Summary of all equipment | `3_Issued/` |
| Data sheet list | Approved list and templates | `1_Working/` |
| Input data compilation | Design data sources | `1_Working/` |
| Vendor correspondence | Vendor data coordination | `1_Working/` |
| Checker comments | Review records | `1_Working/` |
| Transmittal record | Issue documentation | `1_Working/` |

**Record Management:**
- Working records: `1_Working/` in deliverable folder
- Review packages: `2_Checking/To/` during review cycle
- Issued data sheets: `3_Issued/` upon approval
- Retention requirements: **TBD** — per project document control procedure
- **ASSUMPTION:** Electronic records maintained in project document management system
