# Procedure: DEL-29.03 Test Installation & Test Records

## Purpose

This procedure defines the process for collecting, reviewing, compiling, and archiving **Test Installation & Test Records**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for test. **Source:** Decomposition line 648

**Type:** Record | **Responsible:** D&B Contractor (QA/QC)

## Prerequisites

### Dependencies

See `_DEPENDENCIES.md` — **NOT_TRACKED** (coordinated externally)

**Required Prior Deliverables:**
- DEL-29.01: Test Procedures (defines how records are generated)
- DEL-29.02: ITP (defines hold/witness requirements for records)

### Reference Materials

- Test procedures (DEL-29.01)
- ITP with hold/witness points (DEL-29.02)
- Project Quality Management Plan **location TBD**
- Applicable codes (ASME, API, NFPA, IEC) **location TBD**

### Personnel

- QC Inspectors (conduct tests, complete records)
- Test technicians (perform tests)
- Engineers (review and approve records)
- QA/QC Manager (final approval of record package)

**Qualifications:** Per project quality plan **location TBD**

## Steps

### Step 1: Prepare Record Forms

**Objective:** Ensure test record forms are available before testing.

**Activities:**
1.1. Extract blank record forms/data sheets from test procedures (DEL-29.01)
1.2. Pre-populate forms with equipment tags, test IDs, ITP activity numbers
1.3. Reproduce sufficient copies for all tests
1.4. Provide forms to test crews

**Outputs:** Blank test record forms ready for use

### Step 2: Conduct Tests and Record Data

**Objective:** Execute tests per procedures and document results.

**Activities:**
2.1. Perform test per approved procedure (DEL-29.01)
2.2. Record data in real-time on test record form:
   - Equipment/system identification
   - Test date, time, personnel
   - Test instrument IDs and calibration status
   - Measured data (pressures, resistances, readings, etc.)
   - Ambient conditions (if relevant)
   - Observations (leaks, alarms, performance)
2.3. Compare results to acceptance criteria
2.4. Determine pass/fail
2.5. Photograph test setup and results
2.6. If hold/witness point: Obtain required signatures (Employer, third-party)
2.7. If test fails: Initiate non-conformance report (NCR), document failure mode

**Outputs:** Completed test record (signed)

### Step 3: Review and Verify Records

**Objective:** Ensure record completeness and accuracy.

**Activities:**
3.1. QC Inspector or Engineer reviews each record for:
   - All required fields completed
   - Data legible and reasonable (no obvious errors)
   - Calculations correct (if any)
   - Pass/fail determination correct
   - Required signatures present
3.2. If deficiencies found: Return to test crew for completion/correction
3.3. Verify traceability:
   - ITP activity number correct
   - Test procedure reference correct
   - Design document references correct
3.4. File verified record in project system

**Outputs:** Reviewed and verified test records

### Step 4: Manage Failed Tests and Re-Tests

**Objective:** Document failures and corrective actions.

**Activities:**
4.1. For failed tests: Ensure NCR is issued
4.2. NCR describes: Failure mode, root cause (if known), corrective action, re-test plan
4.3. After repair/correction: Conduct re-test per procedure
4.4. Re-test record cross-references original test and NCR
4.5. If re-test passes: Close NCR, finalize records
4.6. If re-test fails: Repeat process or escalate for engineering disposition

**Outputs:** Closed NCRs, passed re-test records

### Step 5: Compile Record Package

**Objective:** Assemble records into deliverable format.

**Activities:**
5.1. Collect all test records (by system, test type, or chronologically)
5.2. Organize records:
   - **Option A:** By system (all TK-101 records together)
   - **Option B:** By test type (all hydrostatic tests together)
   - **Option C:** By ITP activity sequence
   - **Selection depends on user preference and project standards**
5.3. Create index or table of contents
5.4. Include:
   - Test records (data sheets, reports)
   - Photographs
   - Calibration certificates (for test instruments)
   - NCRs and re-test records (if applicable)
   - ITP sign-off tracking (summary showing all activities completed)
5.5. Compile into binders (hardcopy) and/or electronic folders (PDF)

**Outputs:** Organized record package

### Step 6: Prepare Submittal

**Objective:** Submit record package for acceptance.

**Activities:**
6.1. Prepare cover letter or transmittal summarizing:
   - Scope of testing covered
   - Number of tests performed
   - Pass/fail summary
   - NCRs and resolutions
6.2. QA/QC Manager reviews and approves package
6.3. Submit to:
   - Employer (if required per contract)
   - Engineering (for project records)
   - Commissioning team (as prerequisite for commissioning)
6.4. Address any review comments
6.5. Issue final approved package

**Outputs:** Submitted and accepted test record package

### Step 7: Archive Records

**Objective:** Preserve records for facility lifetime.

**Activities:**
7.1. File records in project document management system:
   - Native format (scanned PDFs, database entries)
   - Indexed and searchable
7.2. Store hardcopy records (if required):
   - Controlled storage (fireproof, climate-controlled)
   - Access log maintained
7.3. Implement retention schedule (permanent facility records **ASSUMPTION**)
7.4. Provide copies to Employer and O&M contractor as required

**Outputs:** Archived records in controlled storage

## Verification

**V-1: Completeness:** All required tests have records (cross-check to ITP and test log)
**V-2: Accuracy:** Data verified, calculations checked
**V-3: Signatures:** Required approvals and witness signatures present
**V-4: Traceability:** Records linked to ITPs, procedures, drawings

### Acceptance Criteria

**AC-1:** 100% of tests documented
**AC-2:** All test records complete and signed
**AC-3:** All failed tests resolved (NCRs closed, re-tests passed)
**AC-4:** QA/QC Manager approval obtained
**AC-5:** Records archived per retention requirements

## Records

**Primary Deliverables:**

1. **Hydrostatic Test Records** — Tanks, piping, loading arms
2. **Electrical Test Records** — Insulation, continuity, protection, energization
3. **Instrument Calibration Records** — All field instruments

**Compilation Format:**
- Binders (hardcopy) and/or electronic folders
- Index provided
- Cross-referenced to ITP

**Filing:**
- Working records: `1_Working/DEL-29.03_Test_Installation_and_Test_Records/`
- Submitted records: `2_Checking/To/`
- Accepted records: `3_Issued/`
- Archive: Project document management system (permanent retention)

**Status Tracking:** See `_STATUS.md` for deliverable lifecycle state

---

**Note:** This Procedure describes the process for managing test records. The actual test records are generated during test execution per DEL-29.01 procedures.
