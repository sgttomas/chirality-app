# Procedure: DEL-19.02 Control System Technical Specification

## Purpose

This procedure defines the process for **producing** the **Control System Technical Specification** within **PKG-19 Control Systems**.

**Deliverable purpose:** Defines performance, materials, and workmanship requirements for control system per ER requirements.

**Source:** `_CONTEXT.md`

**Deliverable type:** Specification (Technical Specification)
**Responsible party:** D&B Contractor
**Discipline:** I&C

This procedure guides the I&C team through the development, review, and approval of the control system technical specification, ensuring all functional, performance, interface, and quality requirements are defined and documented.

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md` and `_DEPENDENCIES.md`)

**Upstream deliverables** (coordination required but not formally tracked):
- **DEL-00.xx (PKG-00):** Project design basis, Employer's Requirements
- **DEL-19.01:** Control System Design Drawing Set (parallel development, coordination required)
- **Process deliverables (PKG-10-16):** Process design information (P&IDs, control strategies, I/O lists)
- **DEL-20.xx (PKG-20):** Field instrumentation requirements (I/O types, signal types, protocols)
- **DEL-17.xx (PKG-17):** Electrical power requirements
- **DEL-30.xx (PKG-30):** Area classification (hazardous area equipment ratings)

**Source:** Typical specification development dependencies; specific sequencing TBD per project schedule

### Reference Materials

**Required reference documents:**
- Employer's Requirements (Volumes 2 Part 1, 2, 3) — **TBD** — **location TBD**
- Project Design Basis — **TBD**
- Applicable codes and standards (see Specification.md):
  - IEC 61131-3 (Programming Languages)
  - ISA 84 / IEC 61511 (SIS, if applicable)
  - CSA C22.1 (Electrical Code)
  - API 554 (Process Instrumentation)
  - ISA/IEC 62443 (Cybersecurity)
  - ISA 18.2 (Alarm Management)
- Control system vendor pre-qualification list (if applicable) — **TBD**
- Existing terminal control system information (for integration) — **TBD**

**Available reference materials:** See `_REFERENCES.md` and `0_References/` in package directory

### Personnel Requirements

**Qualified personnel:**
- **Lead Author:** Senior I&C engineer with control system specification experience — **ASSUMPTION**: Per project staffing plan
- **Reviewers:** I&C discipline team, interdisciplinary reviewers (electrical, process, safety)
- **Approver:** I&C discipline lead or authorized representative — **TBD**

**Competency requirements:**
- Familiarity with DCS/PLC systems, HMI, and historian technologies
- Knowledge of IEC 61131-3, ISA/IEC 62443, and applicable I&C standards
- Understanding of bulk liquid handling process control
- Specification writing experience

**Source:** **ASSUMPTION**: Standard personnel competency requirements; specific qualifications TBD per project quality procedures

### Tools and Resources

- Specification template (project-standard) — **TBD**
- Requirements management tool (if applicable) — **TBD**
- Access to project document management system — **TBD**

## Steps

### Step 1: Requirements Gathering and Design Basis

**Objective:** Compile all applicable requirements and establish specification basis

**Activities:**
1. Review Employer's Requirements for control system requirements
2. Review project objectives (OBJ-1, OBJ-2, OBJ-4, OBJ-8, OBJ-10) and understand control system role
3. Coordinate with process disciplines to understand:
   - Process control strategies (continuous, batch, discrete)
   - Control loops and interlocks
   - Operational modes (tank storage, direct rail-to-ship transfer per OBJ-4)
   - Capacity and throughput requirements (1,000,000 MT/a per OBJ-2)
4. Coordinate with field instrumentation (PKG-20) for I/O requirements
5. Coordinate with electrical (PKG-17) for power and UPS requirements
6. Coordinate with safety systems (PKG-23) for safety interface requirements
7. Review applicable codes and standards
8. Identify vendor pre-qualification requirements (if any)
9. Prepare requirements summary and design basis note

**Outputs:**
- Requirements summary
- Design basis note
- I/O summary (preliminary)

**Verification:** Requirements review by discipline lead

**Source:** Typical specification initiation workflow; Specification.md requirements sections

### Step 2: Draft Specification Structure and Content

**Objective:** Develop specification content for DCS/PLC, HMI, and historian

**Activities:**
1. Establish specification structure using project template (or create structure per Guidance.md example)
2. Draft General section (scope, definitions, abbreviations, references)
3. Draft System Architecture section:
   - Define DCS vs. PLC (coordinate with Employer if not specified)
   - Define redundancy level per Guidance.md Trade-offs analysis
   - Define network architecture and segmentation
4. Draft Hardware Requirements section (DCS/PLC):
   - Controller specifications (processor, memory, I/O capacity)
   - I/O module specifications (AI, AO, DI, DO, communication interfaces)
   - Redundancy and fail-over requirements
   - Environmental ratings per installation locations
5. Draft Software Requirements section (DCS/PLC):
   - Programming languages per IEC 61131-3
   - Licensing requirements (perpetual or subscription)
   - Version control and configuration management
6. Draft HMI Requirements section:
   - HMI platform and software requirements
   - Workstation hardware requirements
   - Operator interface requirements (screen layouts, alarm management, trending)
   - Graphics standards and style guide (or reference to separate document)
7. Draft Historian Requirements section:
   - Historian platform and database requirements
   - Server hardware requirements
   - Data collection requirements (tags, sampling rates, retention)
   - Reporting and analytics requirements
8. Draft Performance Requirements section per Specification.md PR-01 through PR-04
9. Draft Interface Requirements section per Specification.md IR-01 through IR-05
10. Draft Environmental and Installation Requirements section
11. Draft Testing and Commissioning Requirements section (FAT, SAT, integration)
12. Draft Documentation and Training Requirements section
13. Draft Warranty and Support Requirements section
14. Mark all TBDs clearly; label all assumptions

**Outputs:**
- Draft DCS/PLC specification
- Draft HMI specification
- Draft historian specification

**Verification:** Self-check for completeness and internal consistency

**Source:** Specification.md requirements structure; Guidance.md specification structure example

### Step 3: Interdisciplinary Coordination

**Objective:** Verify interfaces and resolve conflicts with other disciplines

**Activities:**
1. Coordinate with field instrumentation (PKG-20):
   - Verify I/O counts, signal types, communication protocols
   - Verify smart device integration (HART, Fieldbus, Modbus, etc.)
2. Coordinate with electrical (PKG-17):
   - Verify power requirements (voltage, current, UPS backup duration)
   - Verify grounding and wiring requirements
3. Coordinate with process disciplines (PKG-10-16):
   - Verify control strategies and interlocks
   - Verify operator interface requirements
4. Coordinate with safety systems (PKG-23):
   - Verify fire protection and ESD interfaces
   - Verify SIS requirements (if applicable)
5. Coordinate with building design (PKG-21/PKG-22):
   - Verify control room layout and HVAC requirements
6. Conduct interdisciplinary check (IDC) meeting(s)
7. Revise specification to incorporate IDC comments

**Outputs:**
- IDC comment log
- Revised specification addressing IDC comments

**Verification:** IDC sign-off by affected disciplines

**Source:** Specification.md interface requirements; typical engineering workflow **ASSUMPTION**

### Step 4: Technical Review

**Objective:** Perform technical review for compliance with standards and Employer's Requirements

**Activities:**
1. Submit specification to I&C discipline team for technical review
2. Reviewers check for:
   - Compliance with Employer's Requirements
   - Compliance with applicable codes and standards
   - Technical adequacy and achievability
   - Completeness (all sections complete, all TBDs addressed or justified)
   - Consistency across DCS/PLC, HMI, and historian specifications
3. Reviewers prepare review comments
4. Author addresses review comments and revises specification
5. Reviewers verify comment closure

**Outputs:**
- Technical review comment log
- Revised specification addressing review comments

**Verification:** Technical review sign-off

**Source:** Specification.md verification methods; typical technical review process **ASSUMPTION**

### Step 5: Employer Review (if required)

**Objective:** Obtain Employer review and comments

**Activities:**
1. Submit specification to Employer for review (if required by project procedures)
2. Conduct specification review meeting with Employer (if required)
3. Receive Employer comments
4. Address Employer comments and revise specification
5. Obtain Employer acceptance or approval (if required)

**Outputs:**
- Employer comment log
- Revised specification addressing Employer comments
- Employer acceptance letter (if applicable)

**Verification:** Employer acceptance or approval

**Source:** **ASSUMPTION**: Typical Employer review process for D&B contracts; specific requirements TBD per project procedures

### Step 6: Finalization and Approval

**Objective:** Finalize specification and obtain approval for issue

**Activities:**
1. Apply final revisions per technical review and Employer review
2. Verify all sections complete and all TBDs resolved (or justified as future work)
3. Verify document formatting, numbering, and revision control per project standards
4. Submit specification to discipline lead or approver
5. Approver reviews for overall adequacy and readiness for procurement use
6. Approver signs specification

**Outputs:**
- Approved Control System Technical Specification (DEL-19.02)

**Verification:** Approver signature confirming approval for issue

**Source:** Typical approval workflow **ASSUMPTION**

### Step 7: Document Issuance and Distribution

**Objective:** Issue specification and distribute per project procedures

**Activities:**
1. Assign final document number and revision per project numbering system
2. Upload specification to project document management system
3. Distribute specification per project distribution matrix:
   - To procurement for vendor RFQ/bidding
   - To design team for coordination
   - To construction for planning
   - To commissioning for planning
4. File issued specification in `3_Issued/` folder (copy)
5. Update `_STATUS.md` to reflect issuance (when appropriate per lifecycle progression)

**Outputs:**
- Issued specification (final)
- Distribution records
- Updated `_STATUS.md` (when transitioned to ISSUED state)

**Verification:** Confirmation of distribution and document management system upload

**Source:** Typical document issuance workflow **ASSUMPTION**

## Verification

### Verification Activities Summary

| Step | Verification Activity | Verifier |
|------|----------------------|----------|
| 1 | Requirements review | Discipline lead |
| 2 | Self-check during drafting | Author |
| 3 | Interdisciplinary check (IDC) | Affected disciplines |
| 4 | Technical review | I&C discipline team |
| 5 | Employer review (if required) | Employer |
| 6 | Approval review | Discipline lead / Approver |
| 7 | Distribution confirmation | Document control |

**Source:** Specification.md verification methods

### Acceptance Criteria (from Specification.md)

See `Specification.md` Verification section for full acceptance criteria (AC-01, AC-02, AC-03). Summary below:

**AC-01 — Specification Completeness:**
- All sections complete (DCS/PLC, HMI, historian specifications)
- All requirements clearly stated and verifiable
- All interfaces identified and coordinated
- **TBD** — Specific completeness checklist per project procedures

**AC-02 — Technical Adequacy:**
- Requirements consistent with Employer's Requirements
- Requirements consistent with applicable codes and standards
- Requirements achievable with current technology
- **TBD** — Technical review and approval procedures

**AC-03 — Vendor Compliance:**
- Specification written to enable competitive bidding (unless sole source justified)
- Requirements verifiable during FAT and SAT
- **TBD** — Compliance matrix and evaluation criteria for vendor proposals

### Sign-off Requirements

- Author sign-off
- Technical reviewers sign-off
- Interdisciplinary reviewers sign-off
- Employer acceptance (if required)
- Approver sign-off
- **TBD** — Specific sign-off authority matrix per project quality procedures

## Records

### Documentation Outputs (from Specification.md and `_CONTEXT.md`)

**Primary deliverable artifacts:**
1. DCS/PLC Technical Specification
2. HMI Technical Specification
3. Historian Technical Specification

**Supporting records:**
- Requirements summary and design basis note
- I/O summary
- IDC comment log and closure records
- Technical review comment log
- Employer review comment log (if applicable)
- Distribution records

### Record Management

**Filing locations:**
- Working files: `1_Working/DEL-19.02_Control_System_Technical_Specification/`
- Checking copies: `2_Checking/To/` (during review phase) → `2_Checking/From/` (returned with comments)
- Issued copies: `3_Issued/` (final approved specification with issue date/revision in filename)

**Document management system:**
- All specifications uploaded to project DMS — **TBD** — DMS path and conventions
- Revision control per project procedures — **TBD**

**Retention requirements:**
- Retention per project records retention schedule — **TBD**
- **ASSUMPTION**: Electronic records retained for life of facility plus regulatory retention period

**Source:** Typical engineering records management practice; specific requirements TBD per project procedures

### Lifecycle State Management

**`_STATUS.md` transitions** (when appropriate per project lifecycle):
- `OPEN` → `INITIALIZED` (initial drafts generated)
- `INITIALIZED` → `IN_PROGRESS` (active specification development underway)
- `IN_PROGRESS` → `CHECKING` (submitted for review)
- `CHECKING` → `IN_PROGRESS` (if comments require rework) or → `ISSUED` (if approved)
- `ISSUED` (final state for this phase)

**Note:** Status transitions are human-managed decisions; this procedure describes when transitions are typical, but does not automatically change status.

**Source:** Framework lifecycle model per `AGENTS.md`
