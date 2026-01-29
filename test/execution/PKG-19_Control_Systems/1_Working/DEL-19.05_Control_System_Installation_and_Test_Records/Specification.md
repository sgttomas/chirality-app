# Specification: DEL-19.05 Control System Installation & Test Records

## Scope

Defines requirements for installation and test records for PKG-19 Control Systems.

**Deliverable purpose:** Provides evidence of completion, inspection, and testing for control system. **Source:** `_CONTEXT.md`

### Included
- FAT records (Factory Acceptance Test at vendor facility)
- SAT records (Site Acceptance Test after installation)
- Software version records (backups, versions, change logs)
- Installation inspection records
- Commissioning and loop checkout records
- Training records

### Excluded
- Equipment procurement records (see procurement/contract files)
- Vendor manufacturing quality records (vendor responsibility)

## Requirements

### Record Requirements

**RR-01: FAT Records** (per DEL-19.02 TC-01)
- FAT test procedures (approved)
- FAT test results (all tests documented with pass/fail status)
- Equipment inspection records
- Functional and performance test results
- Punch list and resolutions
- FAT approval and witness sign-off
- **Rationale:** Guidance.md §Principles (Evidence of Quality); **Verification:** Procedure.md Steps 1–2

**RR-02: SAT Records** (per DEL-19.02 TC-02)
- SAT test procedures (approved)
- I/O checkout, loop checkout, interlock verification
- Performance verification (scan time, response time per DEL-19.02 PR-01, PR-02)
- Integration testing with process systems
- SAT approval and witness sign-off
- **Rationale:** Guidance.md §Considerations (FAT vs. SAT Scope); **Verification:** Procedure.md Steps 5–6

**RR-03: Software Version Records** (per DEL-19.04)
- Software backups (PLC/DCS, HMI, historian)
- Version documentation (software name, version, date)
- Change logs (all software changes documented)
- As-built software documentation
- **Rationale:** Guidance.md §Considerations (Software Version Control); **Verification:** Procedure.md Steps 3, 7

**RR-04: Installation Records**
- Equipment installation inspection (per DEL-19.01 drawings)
- Cable installation and termination inspection
- Grounding verification (per CSA C22.1)
- Power-on checkout
- **Verification:** Procedure.md Step 4

**RR-05: Training Records** (per DEL-19.02 DR-02)
- Training attendance
- Training completion certificates
- Operator acceptance sign-off
- **Verification:** Procedure.md Step 8

### Quality Requirements

**QR-01: Traceability**
- Records shall demonstrate traceability from requirements (DEL-19.02) to design (DEL-19.01) to as-built (DEL-19.05)

**QR-02: Completeness**
- All required tests completed and documented
- All punch list items resolved and documented
- All sign-offs obtained

**QR-03: Retention**
- Records retained per project retention schedule
- Electronic and hard copy storage per project procedures

## Standards

- CSA C22.1 (electrical installation)
- ISA 5.1 (tagging and identification)
- Project Quality Management Plan

## Verification

- QA/QC review of all records for completeness
- Sign-off by I&C discipline lead, QA/QC manager, Owner representative (as applicable)

## Documentation

**Required Record Categories:**
1. FAT records package
2. SAT records package
3. Software version records package
4. Installation inspection records
5. Commissioning records
6. Training records

**Format:** Per project QA/QC procedures
**Filing:** `3_Issued/` after commissioning completion and final acceptance
