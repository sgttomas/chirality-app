# Procedure: DEL-10.05 Railcar Unloading Installation & Test Records

## Purpose

This procedure defines the process for producing and managing the **Railcar Unloading Installation & Test Records** within **PKG-10 Railcar Unloading System**.

**Scope of Procedure:**
- Collection of FAT records for manufactured equipment
- Collection of installation records during construction
- Collection of hydrostatic test records during testing
- Compilation and submission of complete record package

**Deliverable Type:** Record
**Responsible Party:** D&B Contractor (QA/QC)
**Discipline:** Process

## Prerequisites

### Dependencies

- **Dependency Tracking:** NOT_TRACKED — dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`)
- **Upstream Inputs (typical):**

  | Input | Source | Status |
  |-------|--------|--------|
  | Equipment specifications | DEL-10.02 Technical Specification | Required for test criteria |
  | Equipment data sheets | DEL-10.04 Data Sheet Package | Required for equipment identification |
  | Installation drawings | DEL-10.01 Design Drawing Set | Required for installation reference |
  | Record templates | Project quality procedures | Required for documentation |
  | Equipment manufacture | Procurement / vendors | Required for FAT |
  | Equipment installation | Construction | Required for installation records |
  | System completion | Construction | Required for hydrostatic test |

### Reference Materials

| Reference | Location | Purpose |
|-----------|----------|---------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope; DEL-10.05 definition |
| Employer's Requirements | `test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` | Record requirements (clauses **TBD**) |
| Specification.md | This deliverable folder | Requirements for record package |
| Guidance.md | This deliverable folder | Record principles and examples |
| Datasheet.md | This deliverable folder | Equipment list and record types |
| DEL-10.01 | PKG-10 folder | Installation reference drawings |
| DEL-10.02 | PKG-10 folder | Test criteria and specifications |
| DEL-10.04 | PKG-10 folder | Equipment identification |

### Personnel Requirements

| Role | Qualification | Responsibility |
|------|---------------|----------------|
| QA/QC Engineer | QA/QC discipline; **TBD** qualifications | Record collection and review |
| Inspector | Inspection certification; **TBD** | Installation inspection |
| Test Engineer | Test procedures; **TBD** | Hydrostatic testing |
| Witness (if required) | Per ER requirements | Independent verification |
| Document Controller | Document control procedures | Record management |

**ASSUMPTION:** Personnel competency requirements per project quality procedures.

## Steps

### Step 1: Define Record Requirements and Templates

**Objective:** Establish required records and obtain templates.

**Actions:**
1. Review Specification.md §Scope for required records
2. Review Datasheet.md §Construction for equipment requiring records
3. Confirm record list:

   | Record Type | Equipment | Quantity |
   |-------------|-----------|----------|
   | FAT Records | Unloading Arms | 32 |
   | FAT Records | Sump Pumps | **TBD** |
   | Installation Records | All PKG-10 equipment | Per equipment count |
   | Hydrostatic Test Records | Header piping | Per test section |

4. Obtain record templates per project quality procedures
5. Confirm witness requirements per ER (**TBD**)
6. Establish equipment tag list from DEL-10.04

**Output:** Approved record list and templates.

**Verification:** QA/QC lead sign-off on record requirements.

### Step 2: Collect FAT Records

**Objective:** Obtain and verify factory acceptance test records for manufactured equipment.

**Actions:**

#### 2a: Unloading Arms (32 units)
1. Confirm FAT requirements from DEL-10.02 specification
2. Coordinate FAT witness attendance (if required)
3. Review vendor FAT procedure
4. Witness FAT execution (if required)
5. Obtain completed FAT record for each arm:
   - Equipment identification (tag, model, serial)
   - Test results and pass/fail determination
   - Vendor signatures
   - Contractor/witness signatures
   - Test certificates and attachments
6. Verify record completeness against Specification.md FAT-xx requirements
7. File FAT records

#### 2b: Sump Pumps
1. Confirm FAT requirements from DEL-10.02 specification
2. Follow same process as 2a for each pump

**Output:** Complete FAT records for all equipment.

**Traceability:**

| Requirement | Record | Status |
|-------------|--------|--------|
| FN-01: 32 arm FAT records | Per arm | Collected |
| FN-02: Sump pump FAT records | Per pump | Collected |
| FAT-01 through FAT-06 | All FAT records | Verified |

### Step 3: Collect Installation Records

**Objective:** Document installation completion for all equipment.

**Actions:**
1. Prepare installation checklists per equipment type
2. Coordinate with construction for inspection hold points
3. Inspect each equipment installation:
   - Verify against DEL-10.01 drawings
   - Complete installation checklist
   - Document any as-built deviations
   - Take photos as required
4. Complete installation record for each equipment:
   - Equipment identification (tag, location)
   - Drawing references
   - Checklist completion
   - As-built notes
   - Inspector signatures
5. Verify record completeness against Specification.md IR-xx requirements
6. File installation records

**Output:** Complete installation records for all equipment.

**Traceability:**

| Requirement | Record | Status |
|-------------|--------|--------|
| FN-03: Installation records | Per equipment | Collected |
| IR-01 through IR-05 | All installation records | Verified |

### Step 4: Collect Hydrostatic Test Records

**Objective:** Document hydrostatic testing of header piping.

**Actions:**
1. Confirm test requirements from DEL-10.02 specification:
   - Test pressure (**TBD** — per code)
   - Test duration (**TBD** — per code)
   - Test medium (**TBD** — typically water)
2. Define test sections per DEL-10.01 layout
3. Coordinate test witness attendance (if required)
4. Execute hydrostatic test per test procedure:
   - Prepare system (isolation, fill, vent)
   - Pressurize to test pressure
   - Hold for required duration
   - Inspect for leaks
   - Record pressure readings
5. Complete test record for each section:
   - Test boundary identification
   - Test parameters (pressure, duration, medium)
   - Test results and observations
   - Pass/fail determination
   - Engineer and witness signatures
   - Pressure charts and calibration records
6. Verify record completeness against Specification.md HT-xx requirements
7. File hydrostatic test records

**Output:** Complete hydrostatic test records.

**Traceability:**

| Requirement | Record | Status |
|-------------|--------|--------|
| FN-04: Hydrostatic test records | Per test section | Collected |
| HT-01 through HT-06 | All test records | Verified |

### Step 5: Verify Completeness and Compile Package

**Objective:** Verify all records complete and compile final package.

**Actions:**
1. Create record index listing all records
2. Verify completeness against record list (Step 1):

   | Record Type | Required | Collected | Complete |
   |-------------|----------|-----------|----------|
   | FAT — Arms | 32 | | |
   | FAT — Pumps | **TBD** | | |
   | Installation | Per equipment | | |
   | Hydrostatic | Per section | | |

3. Verify each record meets Specification.md requirements:
   - Traceability to equipment tags (FN-05)
   - Reference to specifications/drawings (FN-06)
   - Required signatures/witness (FAT-05, IR-05, HT-05)
   - Pass/fail determination where applicable
4. Resolve any incomplete records or NCRs
5. Compile complete record package

**Output:** Verified complete record package.

**Verification:** QA/QC lead sign-off on completeness.

### Step 6: Submit and Archive

**Objective:** Submit record package and archive in project DMS.

**Actions:**
1. Review record package for submission readiness
2. Obtain QA/QC lead approval
3. Finalize document metadata (Datasheet.md §Attributes):
   - Record numbers (confirmed)
   - Revision (initial issue)
   - Retention period
4. Prepare transmittal per project document control procedure (**TBD**)
5. Submit record package
6. Archive records in project document management system per QA-05
7. File records per §Records below

**Output:** Submitted and archived record package.

**Verification:**
- QA/QC lead approval sign-off
- Document controller confirmation of archive

## Verification

**Verification Summary:**

| Step | Verification Activity | Responsible | Record |
|------|----------------------|-------------|--------|
| 1 | Record requirements approval | QA/QC lead | Approved list |
| 2 | FAT record collection | QA/QC engineer | FAT records |
| 3 | Installation record collection | Inspector | Installation records |
| 4 | Hydrostatic test record collection | Test engineer | Test records |
| 5 | Completeness verification | QA/QC lead | Completeness check |
| 6 | Archive confirmation | Document controller | Archive record |

**Requirement Verification Matrix:**

| Req ID | Requirement Summary | Verification Step | Method |
|--------|---------------------|-------------------|--------|
| FN-01 | 32 arm FAT records | 2a, 5 | Record count |
| FN-02 | Sump pump FAT records | 2b, 5 | Record check |
| FN-03 | Installation records | 3, 5 | Record check |
| FN-04 | Hydrostatic test records | 4, 5 | Record check |
| FN-05 | Equipment traceability | 5 | Traceability review |
| FN-06 | Specification reference | 5 | Document review |
| FAT-01–06 | FAT record content | 2, 5 | Document review |
| IR-01–05 | Installation record content | 3, 5 | Document review |
| HT-01–06 | Test record content | 4, 5 | Document review |
| QA-01–05 | Quality requirements | 5, 6 | Document review |
| IF-01–04 | Interface requirements | 5 | Cross-document review |

## Records

**Documentation Outputs:**

| Record | Description | Filing Location |
|--------|-------------|-----------------|
| FAT Records — Unloading Arms (32) | Factory acceptance test records | `3_Issued/` |
| FAT Records — Sump Pumps | Factory acceptance test records | `3_Issued/` |
| Installation Records | Installation completion records | `3_Issued/` |
| Hydrostatic Test Records | Pressure test records | `3_Issued/` |
| Record Index | Summary of all records | `3_Issued/` |
| Record requirements | Approved record list | `1_Working/` |
| Completeness check | Verification record | `1_Working/` |
| Transmittal record | Submission documentation | `1_Working/` |

**Record Management:**
- Working records: `1_Working/` in deliverable folder during collection
- Review packages: `2_Checking/To/` during review cycle
- Issued records: `3_Issued/` upon approval and archive
- Retention period: **TBD** — per Employer's Requirements / regulatory requirements
- Archive: Project document management system per QA-05
- **ASSUMPTION:** Electronic records maintained with appropriate backup
