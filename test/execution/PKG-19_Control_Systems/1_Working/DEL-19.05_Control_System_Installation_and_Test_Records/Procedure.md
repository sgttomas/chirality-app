# Procedure: DEL-19.05 Control System Installation & Test Records

## Purpose

Defines process for creating, managing, and archiving installation and test records for PKG-19 Control Systems.

**Deliverable purpose:** Provides evidence of completion, inspection, and testing for control system. **Source:** `_CONTEXT.md`

## Prerequisites

**Dependencies (NOT_TRACKED — coordinated externally):**
- DEL-19.01 (drawings) — installation basis
- DEL-19.02 (specification) — testing requirements
- DEL-19.03 (equipment) — installed equipment
- DEL-19.04 (software) — software to be tested
- Equipment installation complete (or in progress for progressive testing)

**Personnel:**
- QA/QC inspector/coordinator
- I&C technicians (installation and testing)
- I&C engineer (test witness, approval)

**Tools:**
- QA/QC forms and checklists per project procedures
- Test equipment (multimeters, signal generators, loop calibrators)

## Steps

### Step 1: Prepare FAT Test Procedures and Forms
- Review DEL-19.02 TC-01 FAT requirements
- Prepare FAT test procedures (what to test, how to test, acceptance criteria)
- Prepare FAT record forms (test data sheets, checklists, sign-off sheets)
- Submit FAT procedures for approval (I&C lead, QA/QC, Owner if required)

### Step 2: Conduct FAT and Document Results
- Witness FAT at vendor facility per DEL-19.02 TC-01
- Execute FAT test procedures
- Record all test results (pass/fail, data, observations)
- Document punch list (issues identified)
- Obtain witness signatures (Owner, Contractor, vendor)
- Verify punch list resolution
- Obtain FAT approval sign-off

**Output:** FAT records package (procedures, results, punch list, approvals)

### Step 3: Document Software Versions (Pre-Installation)
- Obtain software backups from vendor (post-FAT version)
- Document software versions (PLC/DCS, HMI, historian: name, version, date)
- Verify backup integrity (restore test)
- Archive software backups (multiple locations)

**Output:** Software version records (pre-installation baseline)

### Step 4: Conduct Installation Inspection
- Inspect equipment installation (per DEL-19.01 drawings: location, mounting, leveling)
- Inspect cable installation and termination (per DEL-19.01: routing, termination, labeling)
- Verify grounding (per CSA C22.1: continuity, resistance)
- Inspect enclosures (sealed, gaskets, environmental rating appropriate for location)
- Power-on checkout (apply power, verify no faults, verify communications)

**Output:** Installation inspection records

### Step 5: Prepare SAT Test Procedures and Forms
- Review DEL-19.02 TC-02 SAT requirements
- Prepare SAT test procedures (I/O checkout, loop checkout, interlock verification, performance verification)
- Prepare SAT record forms (loop checkout sheets, test data sheets, sign-off sheets)
- Submit SAT procedures for approval

### Step 6: Conduct SAT and Document Results
- Execute SAT test procedures:
  - I/O checkout (verify all field devices communicating, signals correct)
  - Loop checkout (verify control loops functional, tune PID, verify alarms)
  - Interlock verification (test all interlocks, verify safe states)
  - Alarm verification (test all alarms, verify priorities and setpoints)
  - Performance verification (measure scan time, response time per DEL-19.02 PR-01, PR-02)
- Integration testing (test with process systems PKG-10-16)
- Record all test results
- Document punch list
- Verify punch list resolution
- Obtain SAT approval sign-off (Owner, Contractor)

**Output:** SAT records package

### Step 7: Document Software Versions (As-Commissioned)
- Create software backups of as-commissioned state (post-SAT, post-tuning)
- Document software versions and any changes since FAT
- Document software change log (what changed, why, when, who approved)
- Update software as-built documentation
- Archive software backups

**Output:** Software version records (as-commissioned)

### Step 8: Document Commissioning and Training
- Compile loop checkout records (all loops checked, tuned, alarmed)
- Compile calibration records (instruments calibrated)
- Compile training records (attendance, completion certificates)
- Obtain operator acceptance sign-off (operators trained and accept system)

**Output:** Commissioning and training records

### Step 9: Final Record Package Assembly and Archiving
- Assemble complete record package:
  - FAT records
  - SAT records
  - Software version records
  - Installation inspection records
  - Commissioning records
  - Training records
- QA/QC review of record package for completeness
- Obtain final approvals (I&C lead, QA/QC manager, Owner representative)
- File records in `3_Issued/`
- Upload to project DMS
- Update `_STATUS.md` to ISSUED (when appropriate per lifecycle)

**Output:** Complete DEL-19.05 Installation & Test Records package (issued)

## Verification

| Step | Verification Activity | Verifier |
|------|----------------------|----------|
| 1-2 | FAT procedures approval, FAT test results review | I&C lead, QA/QC, Owner |
| 4 | Installation inspection | QA/QC inspector, I&C engineer |
| 5-6 | SAT procedures approval, SAT test results review | I&C lead, QA/QC, Owner |
| 9 | Final record package completeness | QA/QC manager |

**Acceptance Criteria:** All tests passed, all punch lists resolved, all sign-offs obtained, all records complete

## Records

**Final Record Package:**
1. FAT records (procedures, results, punch list, approvals)
2. SAT records (procedures, results, punch list, approvals)
3. Software version records (backups, versions, change logs, as-built docs)
4. Installation inspection records
5. Commissioning records (loop checkout, calibration)
6. Training records (attendance, certificates, operator acceptance)

**Filing:** `3_Issued/` after commissioning completion and final acceptance
**Retention:** Per project retention schedule — **ASSUMPTION**: Life of facility
