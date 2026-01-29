# Procedure: DEL-19.04 Control System Software

## Purpose

Defines process for developing, testing, and commissioning control system software within PKG-19 Control Systems.

**Deliverable purpose:** Defines and substantiates control system software in accordance with ER requirements. **Source:** `_CONTEXT.md`

## Prerequisites

**Dependencies (NOT_TRACKED — coordinated externally):**
- DEL-19.02 (Control System Technical Specification) — functional requirements basis
- DEL-19.03 (Control System Data Sheet Package) — vendor platform selection
- Process design deliverables (PKG-10-16): P&IDs, control strategies, process narratives
- Field instrumentation deliverables (PKG-20): I/O lists, tag numbering, signal types

**Personnel:**
- PLC/DCS programmer (IEC 61131-3 experience, vendor platform experience)
- HMI developer (HMI platform experience, graphics design skills)
- Historian administrator (historian platform experience, database/reporting skills)
- Test engineer (FAT and SAT testing experience)

**Tools:**
- Programming software per vendor platform (per DEL-19.03 selected equipment)
- HMI development software
- Historian configuration software
- Simulation tools (software/hardware-in-the-loop if available)

## Steps

### Step 1: Requirements Analysis and Design Basis

**Objective:** Understand all software requirements

**Activities:**
1. Review DEL-19.02 functional requirements (FR-01 through FR-05)
2. Review P&IDs (PKG-14) for control loops, valve sequencing, equipment interconnections
3. Review process narratives and control strategies (from process disciplines PKG-10-16)
4. Review I/O lists and tag database (PKG-20)
5. Identify all control loops, interlocks, sequences, alarms, operator actions
6. Prepare software requirements document or functional description outline

**Outputs:** Software requirements document, I/O assignment list (preliminary)

### Step 2: Software Architecture Design

**Objective:** Define software structure before programming

**Activities:**
1. Define software architecture (program structure, modules, function blocks)
2. Develop I/O assignment list (map physical I/O to software tags)
3. Develop interlock matrix (document all interlock logic: conditions, actions, priorities)
4. Develop alarm list (all alarms with tags, priorities, setpoints, descriptions, actions)
5. Develop control loop list (PID loops with tuning parameters, ranges, alarms)
6. Create functional description documents (describe what each program module does)
7. Design review with discipline lead

**Outputs:** Software architecture document, I/O assignment list, interlock matrix, alarm list, control loop list

### Step 3: PLC/DCS Programming

**Objective:** Develop control application software

**Activities:**
1. Develop PLC/DCS programs per IEC 61131-3 and vendor platform
   - Main control program (scan management, mode control)
   - Process control modules (unloading, storage, loading, metering)
   - Regulatory control (PID function blocks, loop configuration)
   - Sequential control (startup, shutdown, batch sequences if applicable)
   - Interlock logic (safety interlocks, process protection)
   - Alarm logic (alarm generation, prioritization, acknowledgment)
   - Communication modules (field device comm, HMI, historian)
2. Code commenting (all functions, complex logic)
3. Version control (commit code to version control system with change comments)
4. Peer code review

**Outputs:** PLC/DCS application software (source code)

### Step 4: HMI Graphics Development

**Objective:** Develop operator interface

**Activities:**
1. Develop HMI graphics per DEL-19.02 FR-05 and ISA 101 principles (if applicable):
   - Overview screens (facility PFD)
   - Area screens (unloading, storage, loading)
   - Equipment detail screens (pump, valve, tank faceplates)
   - Trend screens (real-time and historical)
   - Alarm screens (active alarms, alarm history)
   - Report screens (shift reports, production summary, custody transfer)
2. Implement consistent graphics standards (symbols, colors, navigation)
3. Configure alarm management (priorities, colors, sounds, acknowledgment)
4. Peer review of graphics (usability, consistency)

**Outputs:** HMI graphics package (HMI project files)

### Step 5: Historian Configuration

**Objective:** Configure data collection and reporting

**Activities:**
1. Configure historian tag database (import from I/O list, add calculated tags)
2. Configure data collection (sampling rates: fast ≤1 sec, normal 5-10 sec, slow 1 min)
3. Configure data retention (short-term full resolution, long-term compressed per DEL-19.02 FR-04)
4. Configure reports (shift, daily, monthly, custody transfer)
5. Test historian data collection (verify tags collecting, verify retention)

**Outputs:** Historian configuration files

### Step 6: Simulation Testing (Offline)

**Objective:** Test software without hardware

**Activities:**
1. Simulate I/O (force values or use simulation software)
2. Test control logic (verify loops respond correctly, verify sequencing)
3. Test interlocks (verify all interlock conditions trigger correct actions)
4. Test alarms (verify alarm generation, prioritization, acknowledgment)
5. Test HMI (verify screens update, verify operator actions work)
6. Document test results, fix bugs, iterate
7. Simulation test sign-off

**Outputs:** Simulation test report, bug fixes

### Step 7: FAT (Factory Acceptance Test)

**Objective:** Test software integrated with hardware at vendor facility

**Activities:**
1. Prepare FAT procedures (test cases for all functions per DEL-19.02 TC-01)
2. Load software onto controllers, HMI, historian
3. Integrated functional testing:
   - I/O testing (verify physical I/O responds correctly)
   - Control loop testing (verify PID loops, verify tuning, verify alarms)
   - Interlock testing (verify all interlocks, verify safe states)
   - Alarm testing (verify alarm response time, verify priorities)
   - HMI testing (verify screens, verify operator controls)
   - Historian testing (verify data collection, verify retention, verify reports)
4. Performance testing (scan time, alarm response time, historian data rate)
5. Witness testing (Owner, Contractor, Third-Party if required per contract)
6. Document punch list, resolve issues, retest
7. FAT sign-off

**Outputs:** FAT test report, punch list, FAT approval

### Step 8: Software Documentation

**Objective:** Finalize software documentation for handover

**Activities:**
1. Finalize functional description documents
2. Finalize I/O assignment lists (as-built)
3. Finalize interlock matrices (as-built)
4. Finalize alarm lists (as-built)
5. Create operator manuals (startup, normal operation, shutdown, alarms, abnormal conditions)
6. Create software backups (multiple generations, off-site storage)
7. Document software versions (PLC/DCS, HMI, historian software versions and revision dates)

**Outputs:** Complete software documentation package

### Step 9: SAT (Site Acceptance Test) and Commissioning

**Objective:** Test software with field devices, commission system

**Activities:**
1. Load software onto site controllers, HMI, historian (if not already loaded)
2. I/O checkout (verify all field devices communicate correctly per DEL-19.02 TC-02)
3. Control loop tuning (final tuning with actual process, adjust PID parameters)
4. Interlock verification (test all interlocks with field devices, verify safe states)
5. Alarm verification (verify alarms with field conditions, adjust setpoints if needed)
6. Performance verification (scan time, alarm response, historian data collection)
7. Operator training:
   - Normal operation (startup, operation, shutdown)
   - Alarm response
   - Abnormal conditions and troubleshooting
8. Operator acceptance (operator sign-off after training and operation)
9. SAT sign-off

**Outputs:** SAT test report, operator training records, SAT approval

### Step 10: Final Handover and Records Management

**Objective:** Handover to operations, archive records

**Activities:**
1. Final software backup (as-commissioned state)
2. As-built documentation (final revisions reflecting commissioning changes)
3. Handover package to operations:
   - Software backups
   - Documentation (functional descriptions, I/O lists, interlock/alarm matrices, operator manuals)
   - Test records (simulation, FAT, SAT)
   - Training records
4. Archive records in `3_Issued/` and project DMS
5. Update `_STATUS.md` to ISSUED (when appropriate per lifecycle)

**Outputs:** Final software package (issued), records archived

## Verification

| Step | Verification Activity | Verifier | Requirements Verified |
|------|----------------------|----------|----------------------|
| 2 | Software architecture review | I&C discipline lead | All FRs, QR-01 |
| 3 | Code peer review | Senior programmer | FR-01, FR-02, FR-03, QR-01 |
| 4 | HMI graphics review | I&C discipline lead, operator input | FR-05, PR-02 |
| 5 | Historian configuration review | I&C engineer | FR-04, PR-03 |
| 6 | Simulation testing | Test engineer | FR-01, FR-02, FR-03, PR-01, PR-02 |
| 7 | FAT | Owner, Contractor, Third-Party (if required) | All FRs, All PRs, QR-02 |
| 9 | SAT | Owner, Contractor | All FRs, All PRs, QR-02 |
| 9 | Operator acceptance | Operations team | FR-05, QR-02 |

**Acceptance Criteria (from Specification.md):**
- All simulation tests pass
- All FAT tests pass, punch list resolved
- All SAT tests pass
- Operator training complete and acceptance sign-off
- Software documentation complete

## Records

**Software Deliverables:**
1. PLC/DCS application software (source + compiled)
2. HMI graphics (project files + runtime)
3. Historian configuration
4. Software documentation (functional descriptions, I/O lists, interlock/alarm matrices)
5. Test records (simulation, FAT, SAT)
6. Training records
7. Software backups (versioned, multiple generations)
8. As-built documentation

**Filing:** `3_Issued/` after final commissioning and handover

**Retention:** Per project retention schedule — **TBD** — **ASSUMPTION**: Life of facility plus regulatory retention period
