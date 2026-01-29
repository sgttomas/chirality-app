# Specification: DEL-35.02 Training Installation & Test Records

## Scope

This specification defines the requirements for **Training Installation & Test Records** within **PKG-35 Training & Handover**.

**Purpose:** Provides evidence of completion, inspection, and testing for training activities.

*Source: _CONTEXT.md, Decomposition Section 5 (PKG-35, DEL-35.02)*

**Scope Coverage:**

Training records shall document:
- Training delivery for all facility personnel requiring training
- Competency assessment results demonstrating personnel readiness for facility operations
- Compliance with regulatory training requirements
- Evidence for handover that trained workforce is in place

*Source: **ASSUMPTION** based on typical training record scope*

**Facility Systems Covered by Training (cross-reference DEL-35.01):**
- Railcar unloading system (32 stations on 2 tracks)
- Storage tank operations (3 × 15,000 MT tanks)
- Marine loading system (ship loading via marine loading arms)
- Product transfer and metering systems
- Process control and instrumentation systems
- Electrical power distribution and lighting
- Safety and environmental protection systems
- Emergency response and spill management

*Source: Decomposition Section 1.1 (Key Parameters); cross-reference to DEL-35.01*

**Anticipated Deliverable Artifacts:**
- Training attendance records (evidence of training delivery)
- Competency records (evidence of competency assessment and verification)

*Source: _CONTEXT.md (Anticipated Artifacts)*

**Out of Scope:**
- Training materials themselves (covered by DEL-35.01)
- Ongoing post-handover training records (Employer responsibility after handover)
- Personnel hiring and HR management records (separate from training records)

## Requirements

### Functional Requirements

**FR-01: Training Attendance Documentation**

Training attendance records shall capture the following minimum information for each training session:

- **FR-01.1**: Training session identification (unique session ID or numbering)
- **FR-01.2**: Training date, time, and location
- **FR-01.3**: Training topic/module (linked to DEL-35.01 Training Materials structure)
- **FR-01.4**: Training material revision used (cross-reference DEL-35.01 document numbers and revisions)
- **FR-01.5**: Training duration (hours)
- **FR-01.6**: Training method (classroom, hands-on, simulator, e-learning, OEM-led)
- **FR-01.7**: Instructor/trainer name and qualifications
- **FR-01.8**: List of trainees (name, position, employee ID or unique identifier)
- **FR-01.9**: Trainee signatures confirming attendance
- **FR-01.10**: Instructor signature confirming training delivery
- **FR-01.11**: Any absences or incomplete training (with follow-up plan)

*Source: **ASSUMPTION** — typical training attendance record requirements*

**FR-02: Competency Assessment Documentation**

Competency records shall capture the following minimum information for each assessment:

- **FR-02.1**: Trainee identification (name, position, employee ID)
- **FR-02.2**: Competency being assessed (specific skill, knowledge area, or procedure)
- **FR-02.3**: Competency assessment method (written test, practical demonstration, simulator exercise, on-the-job evaluation)
- **FR-02.4**: Assessment date and location
- **FR-02.5**: Assessor name and qualifications (qualified to assess the competency)
- **FR-02.6**: Assessment criteria (pass/fail threshold, required score, specific performance standards)
- **FR-02.7**: Assessment result (pass/fail, score if applicable, performance rating if applicable)
- **FR-02.8**: Evidence of assessment (test results, observation checklist, witness statement)
- **FR-02.9**: Trainee signature acknowledging assessment result
- **FR-02.10**: Assessor signature verifying assessment was conducted per standard
- **FR-02.11**: Re-assessment records (if initial assessment was not passed)
- **FR-02.12**: Certificate or qualification issued (if applicable)

*Source: **ASSUMPTION** — typical competency record requirements*

**FR-03: Training Program Overview**

Training records package shall include a training program overview document containing:

- **FR-03.1**: Summary of training program structure (modules, topics, sequence)
- **FR-03.2**: Training objectives and learning outcomes
- **FR-03.3**: Competency matrix (which competencies are required for which positions)
- **FR-03.4**: Training schedule (as-planned and as-delivered)
- **FR-03.5**: Training material index (list of training materials used, cross-reference DEL-35.01)
- **FR-03.6**: Trainer/instructor qualifications summary
- **FR-03.7**: Assessment methods and criteria for each competency
- **FR-03.8**: Training program statistics (number of personnel trained, pass rates, training hours delivered)

*Source: **ASSUMPTION** — typical training program documentation for handover*

**FR-04: Traceability and Linking**

Training records shall enable traceability:

- **FR-04.1**: Each attendance record linked to specific training session and training material revision (cross-reference DEL-35.01)
- **FR-04.2**: Each competency record linked to specific trainee and competency definition
- **FR-04.3**: Training records indexed by trainee (individual training history)
- **FR-04.4**: Training records indexed by training topic/module (who was trained on what)
- **FR-04.5**: Training records indexed by date (chronological record of training delivery)

*Source: **ASSUMPTION** — good practice for training record management and auditability*

**FR-05: Confidentiality and Privacy**

Training records shall be managed in compliance with privacy regulations:

- **FR-05.1**: Personal information in training records protected per applicable privacy legislation
- **FR-05.2**: Access to training records restricted to authorized personnel
- **FR-05.3**: Training records provided to Employer at handover with confidentiality notice
- **FR-05.4**: **TBD** — Specific privacy requirements per Canadian privacy legislation and Employer policies

*Source: **ASSUMPTION** — training records contain personal information requiring confidentiality*

### Performance Requirements

**PR-01: Completeness**

Training records shall demonstrate 100% completion of required training:

- **PR-01.1**: All personnel identified as requiring training have attended all required training sessions
- **PR-01.2**: All personnel have completed all required competency assessments
- **PR-01.3**: No gaps in training or competency records
- **PR-01.4**: Any exceptions or outstanding training clearly documented with justification and completion plan

*Source: **ASSUMPTION** — fundamental requirement for training record completeness; supports OBJ-1 (Safe & Reliable Operation)*

**PR-02: Accuracy**

Training records shall be accurate and verifiable:

- **PR-02.1**: All signatures authentic (trainee, instructor, assessor)
- **PR-02.2**: Dates and times accurate
- **PR-02.3**: Assessment results accurately recorded
- **PR-02.4**: Training material revisions correctly referenced
- **PR-02.5**: No alterations or erasures without proper authorization and documentation

*Source: **ASSUMPTION** — training records are legal evidence; accuracy is critical*

**PR-03: Timeliness**

Training records shall be completed and submitted in a timely manner:

- **PR-03.1**: Attendance records completed immediately following each training session
- **PR-03.2**: Competency assessment results recorded immediately following assessment
- **PR-03.3**: Training records package compiled and submitted prior to commissioning completion
- **PR-03.4**: Final training records included in handover documentation (cross-reference DEL-35.03)

*Source: **ASSUMPTION** — timely record completion supports project schedule*

**PR-04: Support for Lifecycle Cost Optimization (OBJ-9)**

Training records shall support **OBJ-9: Lifecycle Cost Optimization** by:

- **PR-04.1**: Demonstrating that Employer operations team is trained and competent, reducing post-handover operating errors and associated costs
- **PR-04.2**: Providing evidence of competency to minimize post-handover support and re-training costs
- **PR-04.3**: Enabling Employer to identify training gaps and plan refresher training efficiently
- **PR-04.4**: Supporting Employer's future workforce planning and training needs assessment

*Source: Decomposition Section 2 (OBJ-9), Section 6 (Objective-to-Deliverable Mapping); **ASSUMPTION** on how training records support OBJ-9*
*See Guidance.md Principle 2 for detailed rationale on lifecycle cost optimization through training records.*

**PR-05: Regulatory Compliance**

Training records shall demonstrate compliance with applicable regulations:

- **PR-05.1**: Occupational health and safety training requirements (federal and BC provincial)
- **PR-05.2**: Environmental protection training requirements
- **PR-05.3**: Transportation of dangerous goods training (if applicable)
- **PR-05.4**: Marine terminal safety training requirements
- **PR-05.5**: Food safety training requirements (if applicable for food-grade product handling)
- **PR-05.6**: **TBD** — Specific regulatory references to be confirmed

*Source: **ASSUMPTION** — regulatory compliance is fundamental requirement; specific regulations TBD*

### Interface Requirements

**IF-01: Integration with Training Materials (DEL-35.01)**

- **IF-01.1**: Training attendance records shall reference the specific training material document number and revision used (cross-reference DEL-35.01)
- **IF-01.2**: Competency assessments shall align with competency criteria defined in training materials
- **IF-01.3**: Training program overview shall index all training materials (cross-reference DEL-35.01)

*Source: Logical interface between training materials and training records*

**IF-02: Integration with Handover Documentation (DEL-35.03)**

- **IF-02.1**: Training records shall be included in handover documentation package
- **IF-02.2**: Training records shall demonstrate that operations team readiness acceptance criteria are met
- **IF-02.3**: Training record summary shall be included in handover certificates or taking-over certificates

*Source: Logical interface between training records and handover process; cross-reference to DEL-35.03 per package scope*

**IF-03: Interface with Safety and Emergency Response Deliverables**

- **IF-03.1**: Training records shall demonstrate completion of safety training per PKG-32 (Health, Safety & Environmental Management) requirements
- **IF-03.2**: Training records shall demonstrate completion of emergency response training per PKG-33 (Emergency Response Planning) requirements
- **IF-03.3**: Training records shall be available for safety audits and regulatory inspections

*Source: **ASSUMPTION** — training records support safety management systems*

**IF-04: OEM/Supplier Coordination**

- **IF-04.1**: If OEM/suppliers provide training, OEM training certificates and records shall be incorporated into overall training record package
- **IF-04.2**: OEM training records shall meet the same format and content requirements as Contractor-provided training records (or be supplemented to meet requirements)
- **IF-04.3**: Contractor responsible for consolidating all training records (Contractor-led and OEM-led) into unified handover package

*Source: _CONTEXT.md (Responsible: D&B Contractor with OEM/Supplier)*

### Quality Requirements

**QR-01: Record Management**

All training records shall comply with the project Quality Management Plan and record management procedures.

*Source: **ASSUMPTION** — standard project requirement*

**QR-02: Verification and Witnessing**

Training records shall be verified:

- **QR-02.1**: Instructor/trainer qualifications verified before training delivery
- **QR-02.2**: Assessor qualifications verified before conducting competency assessments
- **QR-02.3**: **TBD** — Employer witness of training sessions or competency assessments (if required by contract)
- **QR-02.4**: Independent quality review of training records package before submittal

*Source: **ASSUMPTION** — typical verification process for training records*

**QR-03: Record Format and Legibility**

Training records shall be legible and compliant with format standards:

- **QR-03.1**: Handwritten entries (if any) shall be legible and in permanent ink
- **QR-03.2**: Electronic records shall be in non-editable format (PDF) for archival
- **QR-03.3**: Scanned records shall be high resolution and searchable (OCR)
- **QR-03.4**: All records shall include unique identifier (record number, document number, or equivalent)

*Source: **ASSUMPTION** — good practice for record management*

**QR-04: Retention and Archival**

Training records shall be archived for long-term retention:

- **QR-04.1**: Electronic copies retained in project document management system
- **QR-04.2**: Paper originals (if any) archived per project record retention schedule
- **QR-04.3**: Backup copies maintained per project data backup procedures
- **QR-04.4**: Training records transferred to Employer at handover with archival guidance

*Source: **ASSUMPTION** — typical record retention requirements*

## Standards

**Applicable Codes and Standards:**

**Quality Management:**
- ISO 9001:2015 — Quality Management Systems (Clause 7.2 Competence, Clause 7.3 Awareness)
  *Source: **ASSUMPTION** — ISO 9001 requires evidence of personnel competence*

**Health, Safety, and Environmental:**
- ISO 14001:2015 — Environmental Management Systems (Clause 7.2 Competence, Clause 7.3 Awareness)
- ISO 45001:2018 — Occupational Health and Safety Management Systems (Clause 7.2 Competence, Clause 7.3 Awareness, Clause 7.4 Communication)
  *Source: **ASSUMPTION** — training records demonstrate compliance with competence requirements*

**Training and Competency:**
- **TBD** — Canadian occupational health and safety training documentation requirements (federal and BC provincial)
- **TBD** — Industry-specific training record standards (e.g., marine terminal operations, bulk liquid handling)

**Record Management:**
- **TBD** — Project record management procedures
- **TBD** — Canadian privacy legislation (PIPEDA or BC PIPA) for personal information in training records

**Employer's Requirements:**
- Volume 2 Part 1: General Requirements — **TBD: Specific training record requirements (section number TBD)**
- Volume 2 Part 2: Civil & Process Mechanical Works — **TBD: Training record requirements (section number TBD)**
- Volume 2 Part 3: Building Works — **TBD: Training record requirements (section number TBD)**

*Source: Decomposition Section 3 (Reference Documents); specific sections TBD pending document access*

## Verification

**Verification Methods:**

**VM-01: Completeness Check**
- Review training record package against checklist of required records
- Verify 100% attendance for all personnel requiring training
- Verify 100% competency assessment completion
- Verify all forms are fully completed (no blank fields without justification)
- **Acceptance criteria**: All required records present and complete

**VM-02: Accuracy Verification**
- Spot-check training record data against source documents (training schedules, attendance sheets, test results)
- Verify signatures are authentic and authorized
- Verify dates and times are consistent and logical
- Verify training material revisions referenced are correct (cross-check with DEL-35.01 document control)
- **Acceptance criteria**: 100% accuracy in spot-check sample (minimum 10% of records)

**VM-03: Witness Signature Verification**
- Verify instructor/trainer signatures on attendance records
- Verify assessor signatures on competency records
- Verify Employer witness signatures (if witnessing was required)
- **Acceptance criteria**: All required signatures present and authenticated

**VM-04: Archival Format Compliance**
- Verify all records are in approved archival format (typically searchable PDF)
- Verify records are legible and properly scanned (if paper originals exist)
- Verify records are organized and indexed per project document control requirements
- **Acceptance criteria**: 100% of records meet archival format standards

**VM-05: Integration with Handover (cross-reference DEL-35.03)**
- Verify training records are included in handover documentation package
- Verify training record summary is prepared for handover certificate
- Verify all training-related handover acceptance criteria are met
- **Acceptance criteria**: Employer accepts training records as part of handover

*Source: **ASSUMPTION** — typical verification process for training records; cross-reference to DEL-35.03*

**VM-06: Regulatory Compliance Verification**
- Review training records against applicable regulatory requirements
- Verify training content meets regulatory training standards (where specified)
- Verify training record format meets regulatory documentation requirements (where specified)
- **Acceptance criteria**: Training records demonstrate full regulatory compliance
- **TBD** — Specific regulatory requirements to be confirmed

*Source: **ASSUMPTION** — regulatory compliance verification; specific requirements TBD*

## Documentation

**Required Documentation Outputs:**

**Output-01: Training Attendance Records**
- Record of each training session delivered
- Attendance lists with signatures
- Organized by training module/topic and by trainee
- Format: **TBD** — Paper forms with electronic archive (PDF), or electronic database with exported reports

*Source: _CONTEXT.md (Anticipated Artifacts)*

**Output-02: Competency Records**
- Record of each competency assessment conducted
- Assessment results and evidence (test scores, observation checklists, witness statements)
- Certificates of competency (if issued)
- Organized by trainee and by competency
- Format: **TBD** — Paper forms with electronic archive (PDF), or electronic database with exported reports

*Source: _CONTEXT.md (Anticipated Artifacts)*

**Output-03: Training Program Overview Document (ASSUMPTION)**
- Summary document describing training program structure, schedule, and outcomes
- Competency matrix
- Training material index (cross-reference DEL-35.01)
- Trainer qualifications summary
- Training program statistics

**Output-04: Training Record Index**
- Master index of all training records
- Organized by trainee, by training module, and by date
- Cross-references to training materials (DEL-35.01)

**Documentation Management:**

**DM-01: Record Numbering and Identification**
- Record numbering system: **TBD** — Per project record management procedures
- Unique identifier for each attendance record and each competency record
- Traceability to trainee, training session, and training material

**DM-02: Compilation and Packaging**
- Training records compiled into organized package for handover
- Electronic copies: Uploaded to project document management system
- Paper copies: **TBD** — Number and distribution (Employer, Contractor archive, regulatory submittal if required)
- Index provided for navigation

**DM-03: Retention and Archival**
- Retention period: **TBD** — Minimum facility operational life or per regulatory requirements (typically 7-10 years for training records)
- Archive location: Employer's document archive system (post-handover)
- Contractor retains copy for warranty/defects liability period
- **ASSUMPTION**: Electronic records in searchable PDF format for long-term retention

**DM-04: Privacy and Confidentiality**
- Training records contain personal information; managed per privacy legislation
- Access restricted during project (need-to-know basis)
- Confidentiality notice included when transferring to Employer
- **TBD** — Specific privacy requirements per Canadian legislation and Employer policies

**DM-05: Post-Handover Updates**
- Responsibility: **ASSUMPTION** — Employer/facility operator post-handover
- Ongoing training records for new hires or refresher training managed by Employer
- Contractor support: **ASSUMPTION** — Defects liability period support per DEL-35.05 (if training-related defects identified)

*Source: **ASSUMPTION** — typical record management practices; post-handover responsibilities TBD*
