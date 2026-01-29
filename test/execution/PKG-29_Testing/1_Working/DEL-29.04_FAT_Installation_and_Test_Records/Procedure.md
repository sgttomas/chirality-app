# Procedure: DEL-29.04 FAT Installation & Test Records

## Purpose

Process for managing **FAT Installation & Test Records** within **PKG-29 Testing**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for FAT. **Source:** Decomposition line 649

**Type:** Record | **Responsible:** D&B Contractor (QA/QC)

## Prerequisites

### Dependencies

See `_DEPENDENCIES.md` — **NOT_TRACKED** (coordinated externally)

**Required Inputs:**
- DEL-29.02: ITP (identifies equipment requiring FAT and witness requirements)
- Purchase orders with FAT requirements
- Vendor FAT procedures

### Personnel

- Procurement Manager (coordinates FAT scheduling with vendors)
- QC Inspector or Engineer (witnesses FATs)
- Employer representative (witnesses per ITP)

## Steps

### Step 1: Identify Equipment Requiring FAT

**Objective:** Determine which equipment needs FAT.

**Activities:**
1.1. Review ITP (DEL-29.02) for equipment designated for FAT
1.2. Review purchase orders for FAT requirements
1.3. Create FAT schedule/tracker listing equipment, vendor, planned FAT date

**Outputs:** FAT schedule

### Step 2: Coordinate FAT Scheduling

**Objective:** Schedule FATs with adequate notice.

**Activities:**
2.1. Procurement requests FAT schedule from vendor (typically 4-6 weeks before equipment ready)
2.2. Vendor proposes FAT date and provides draft FAT procedure
2.3. Review vendor FAT procedure for adequacy (covers specification requirements)
2.4. Approve FAT procedure or request revisions
2.5. Coordinate witness travel (Contractor QC, Employer, third parties)
2.6. Confirm FAT attendance 1-2 weeks prior

**Outputs:** Scheduled FATs with confirmed witnesses, approved FAT procedures

### Step 3: Conduct FAT

**Objective:** Witness equipment testing at vendor facility.

**Activities:**
3.1. Witness travels to vendor facility
3.2. Pre-FAT meeting: Review test procedure, acceptance criteria, schedule
3.3. Pre-test inspection: Verify equipment configuration, dimensions, materials, workmanship
3.4. Witness performance testing per approved procedure
3.5. Document test data, observations, photographs
3.6. Review test results against acceptance criteria
3.7. Identify any deficiencies
3.8. Conduct post-test meeting: Discuss results, deficiencies, resolution plan
3.9. Sign FAT report (acceptance, acceptance with punch list, or rejection)

**Outputs:** Completed FAT report signed by vendor, Contractor, Employer

### Step 4: Manage Deficiencies

**Objective:** Ensure deficiencies are resolved.

**Activities:**
4.1. Document deficiencies in FAT report or separate punch list
4.2. Classify deficiency severity (critical, major, minor)
4.3. Agree on resolution plan:
   - Critical: Correct before shipment, re-test
   - Major: Correct before shipment or documented punch list
   - Minor: Punch list for site completion
4.4. If re-test required: Re-schedule and re-witness
4.5. Verify deficiencies closed before final acceptance

**Outputs:** Deficiency resolution documentation

### Step 5: Accept Equipment and Authorize Shipment

**Objective:** Provide formal acceptance for shipment.

**Activities:**
5.1. Verify FAT passed and deficiencies resolved (or on acceptable punch list)
5.2. Contractor QC/Procurement issues acceptance to vendor
5.3. Authorize shipment
5.4. Obtain final vendor documentation package (manuals, certificates, FAT report)

**Outputs:** Equipment acceptance letter, shipment authorization

### Step 6: Compile FAT Records

**Objective:** File FAT reports in project records.

**Activities:**
6.1. Collect FAT reports from all equipment
6.2. Verify reports are complete and signed
6.3. Organize by equipment tag or system
6.4. Create index
6.5. File in project document management system
6.6. Provide copies to commissioning team

**Outputs:** Compiled FAT record package (this deliverable)

## Verification

**V-1:** All equipment requiring FAT has FAT report
**V-2:** All FAT reports complete with required signatures
**V-3:** All deficiencies resolved or on documented punch list
**V-4:** FAT records filed and accessible

### Acceptance Criteria

**AC-1:** FAT conducted for all specified equipment
**AC-2:** All FAT reports complete
**AC-3:** All equipment accepted (passed FAT)
**AC-4:** FAT records compiled and archived

## Records

**Primary Deliverables:**
- **Factory Acceptance Test Reports (by equipment)** — Individual FAT reports from vendors

**Filing:**
- Working: `1_Working/DEL-29.04_FAT_Installation_and_Test_Records/`
- Issued: `3_Issued/` (upon compilation)
- Archive: Project document management system (permanent)

**Status:** See `_STATUS.md`

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Datasheet.md | §Construction, §References | Provides FAT content structure and equipment types for Steps 1, 6 |
| Specification.md | §Requirements (FR, PR, IR, QR), §Verification | Defines requirements this Procedure implements |
| Guidance.md | §Principles, §Considerations, §Trade-offs, §Examples | Provides rationale and examples for procedure steps |

**Procedure Step-to-Specification Traceability:**
| Procedure Step | Specification Section(s) | Verification |
|---------------|-------------------------|--------------|
| Step 1 (Identify Equipment) | FR-1 (Scope Definition) | V-1 |
| Step 2 (Coordinate Scheduling) | PR-2 (Witness), QR-1 (Procedure Approval) | V-2 |
| Step 3 (Conduct FAT) | FR-2 (Content), FR-3 (Traceability) | V-2, V-3 |
| Step 4 (Manage Deficiencies) | QR-2 (Deficiency Management) | V-3 |
| Step 5 (Accept/Authorize) | PR-1 (Acceptance) | AC-3 |
| Step 6 (Compile Records) | IR-3 (Documentation Flow) | V-4, AC-4 |

**Procedure Step-to-Guidance Traceability:**
| Procedure Step | Guidance Section(s) |
|---------------|---------------------|
| Step 1 | §Considerations Item 1 (Equipment Selection) |
| Step 2 | §Considerations Items 2-3 (Timing, Procedure Adequacy) |
| Step 3 | §Examples (FAT Report Structure), §Principles |
| Step 4 | §Considerations Item 4, §Trade-offs Item 3 |
| Step 5 | §Trade-offs Items 1-2 |
