# Specification: DEL-33.02 Risk Assessments

## Scope

This specification defines the requirements for **Risk Assessments** within **PKG-33 HSE Management**.

### Purpose

Risk Assessments shall define and substantiate project hazards and associated risks in accordance with Employer's Requirements and the risk assessment processes established in DEL-33.01 (OHS Plan).

**Source:** `_CONTEXT.md`, Decomposition line 730; DEL-33.01 Specification FR-4

### Scope Boundaries

**Inclusions:**
- Task-based risk assessments for all project construction activities
- Job Hazard Analyses (JHA) for high-risk tasks
- Area-based risk assessments for designated work zones
- SIMOPS risk assessments for simultaneous operations
- Activity-specific assessments for permit-required work (hot work, confined space, excavation, working at height, marine operations)
- Risk assessment updates based on trigger criteria

**Source:** Decomposition line 730; DEL-33.01 Specification FR-4, FR-5; Datasheet Risk Assessment Types

**Exclusions:**
- Design risk assessments (separate discipline-specific deliverables in technical packages)
- Project risk register (project management function, not HSE-specific)
- Employer operational risk assessments (post-construction, Employer responsibility)

**Source:** Decomposition Scope Focus (Section 1.2)

### Anticipated Deliverable Artifacts

- Task risk assessments (activity-based)
- Job Hazard Analyses (step-by-step for high-risk tasks)
- Risk assessment register/database

**Source:** `_CONTEXT.md`, Decomposition line 730

## Requirements

### Functional Requirements

#### FR-1: Hazard Identification

Risk Assessments shall systematically identify hazards for each assessed activity, including:
- Physical hazards (struck-by, caught-between, falls, electrical contact)
- Health hazards (noise, vibration, chemical exposure, ergonomic)
- Environmental hazards (weather, marine conditions, ground conditions)
- Interface hazards (Terminal operations, simultaneous activities, public/traffic)

**Source:** DEL-33.01 Specification FR-4; Datasheet Project-Specific Hazards; ASSUMPTION: Comprehensive hazard identification
**Verification:** Hazard coverage audit against project scope (Specification Section 5)
**Guidance Cross-Reference:** Guidance Hazard Identification Process

#### FR-2: Risk Evaluation

Risk Assessments shall evaluate risks using a structured methodology:
- **Likelihood:** Assess probability of hazard occurrence (5-point scale: Rare to Almost Certain)
- **Consequence:** Assess severity of potential outcome (5-point scale: Insignificant to Catastrophic)
- **Risk Rating:** Calculate initial risk (likelihood × consequence) before controls applied
- **Residual Risk:** Calculate residual risk after control measures applied

**Source:** DEL-33.01 Specification FR-4; Datasheet Risk Matrix Parameters; ASSUMPTION: 5×5 risk matrix; TBD: ER risk criteria
**Verification:** Risk evaluation methodology review (Specification Section 5)
**Guidance Cross-Reference:** Guidance Risk Matrix Application

#### FR-3: Control Measures

Risk Assessments shall identify control measures following the hierarchy of controls:
1. Elimination (remove hazard)
2. Substitution (replace with less hazardous)
3. Engineering controls (physical barriers, isolation)
4. Administrative controls (procedures, training, permits)
5. Personal Protective Equipment (PPE)

Control measures shall be:
- Specific and actionable (not generic "be careful")
- Assigned to responsible parties
- Verifiable and auditable

**Source:** DEL-33.01 Specification FR-4; Datasheet Control Hierarchy; ASSUMPTION: Standard hierarchy of controls per WorkSafeBC
**Verification:** Control measure adequacy review (Specification Section 5)
**Guidance Cross-Reference:** Guidance Applying the Hierarchy of Controls

#### FR-4: Residual Risk Acceptance

Risk Assessments shall define residual risk acceptance criteria and approval authorities:
- **Low Risk (1-4):** Accepted by HSE Coordinator
- **Medium Risk (5-9):** Accepted by HSE Coordinator (with HSE Manager awareness)
- **High Risk (10-16):** Requires HSE Manager approval
- **Extreme Risk (17-25):** Requires Project Manager approval; additional controls mandatory to reduce to High or below

**Source:** Datasheet Risk Matrix Parameters (Residual Risk Acceptance); ASSUMPTION: Risk acceptance authority levels; TBD: ER approval matrix
**Verification:** Approval signature verification (Specification Section 5)
**Guidance Cross-Reference:** Guidance Risk Tolerability and ALARP

### Performance Requirements

#### PR-1: Completeness

All project activities requiring risk assessment per DEL-33.01 (OHS Plan) trigger criteria shall have approved risk assessments before work commences.

**Source:** DEL-33.01 Guidance Example 3 (Risk Assessment Trigger Criteria); DEL-33.01 Procedure Step 4.3
**Verification:** Risk assessment register audit — no work without assessment (Specification Section 5)
**Guidance Cross-Reference:** Guidance Trigger Criteria for Risk Assessments

#### PR-2: Currency

Risk Assessments shall be reviewed and updated when:
- Scope, design, or method changes
- Incidents or near-misses reveal inadequate controls
- New equipment, materials, or subcontractors introduced
- Periodic review (quarterly minimum, or per ER requirements)
- High-risk activities reviewed monthly

**Source:** DEL-33.01 Guidance Example 3 (Periodic Review); Datasheet Assessment Characteristics (Update Frequency); ASSUMPTION: Review triggers
**Verification:** Review date tracking, update records (Specification Section 5)
**Guidance Cross-Reference:** Guidance Managing Risk Assessment Lifecycle

#### PR-3: Actionability

Risk Assessments shall inform:
- Safe Work Method Statements (SWMS) development (DEL-33.03)
- Permit-to-Work conditions (DEL-33.01 Procedure Step 4.4)
- Training requirements (DEL-33.01 Specification FR-7)
- Emergency response planning (DEL-33.07)
- HSE resource allocation (DEL-33.01 Guidance Principle 3)

**Source:** DEL-33.01 Specification FR-4, FR-5; Cross-reference DEL-33.03; Datasheet Construction (Risk Assessment Structure)
**Verification:** Traceability from risk assessment to SWMS/permits (Specification Section 5)
**Guidance Cross-Reference:** Guidance Integrating Risk Assessments into Work Planning

### Interface Requirements

#### IR-1: OHS Plan Interface

Risk Assessments shall implement the hazard identification and risk assessment processes defined in DEL-33.01 (OHS Plan Section 4).

**Source:** DEL-33.01 Specification FR-4; DEL-33.01 Procedure Step 2.3 (Section 4), Step 4.3; Datasheet Internal Cross-References
**Verification:** Consistency check with OHS Plan methodology (Specification Section 5)
**Guidance Cross-Reference:** Guidance Relationship to OHS Plan

#### IR-2: Method Statements Interface

Risk Assessments shall be the basis for developing Safe Work Method Statements (DEL-33.03). High-risk activities (risk rating ≥10) shall have corresponding SWMS.

**Source:** DEL-33.01 Specification FR-5; Cross-reference DEL-33.03; ASSUMPTION: Risk rating threshold for SWMS
**Verification:** SWMS coverage of high-risk assessments (Specification Section 5)
**Guidance Cross-Reference:** Guidance Risk Assessment to SWMS Workflow

#### IR-3: Permit-to-Work Interface

Activity-specific risk assessments shall be incorporated into Permit-to-Work forms for:
- Hot work
- Confined space entry
- Excavation
- Work at height
- Marine operations

**Source:** DEL-33.01 Specification FR-5; DEL-33.01 Procedure Step 4.4; Datasheet Risk Assessment Types (Activity-Specific Assessments)
**Verification:** Permit forms include risk assessment reference/summary (Specification Section 5)
**Guidance Cross-Reference:** Guidance Risk Assessment in Permit-to-Work System

#### IR-4: Cross-Package Coordination

Risk Assessments shall coordinate with all technical packages (PKG-01 through PKG-26) to capture discipline-specific hazards.

**Source:** `_DEPENDENCIES.md` (NOT_TRACKED); Decomposition Package Summary (36 packages); DEL-33.01 Specification IR-3
**Verification:** Cross-package coordination meeting records (Specification Section 5)
**Guidance Cross-Reference:** Guidance Multi-Discipline Hazard Identification

### Quality Requirements

#### QR-1: Assessment Quality

Risk Assessments shall:
- Be prepared by competent personnel (trained in risk assessment methodology)
- Be independently reviewed (checker different from originator)
- Be approved by appropriate authority based on residual risk level
- Comply with project document control procedures

**Source:** ASSUMPTION: Standard quality requirements for assessments; Procedure Prerequisites (Personnel Requirements)
**Verification:** Competency records, independent review signature (Specification Section 5)
**Guidance Cross-Reference:** Guidance Competency for Risk Assessment

#### QR-2: Assessment Revision Control

Risk Assessments shall:
- Have unique identification numbers (project-package-activity-sequence)
- Be revision-controlled (date, revision number, description of changes)
- Supersede earlier versions (archive previous revisions)
- Be redistributed to affected personnel upon revision

**Source:** Datasheet Assessment Characteristics (Assessment Format); ASSUMPTION: Document control requirements
**Verification:** Document control audit, distribution records (Specification Section 5)
**Guidance Cross-Reference:** Guidance Managing Assessment Revisions

## Standards

### Regulatory Standards

| Standard | Title | Applicability |
|----------|-------|---------------|
| WorkSafeBC OH&S Regulation | Occupational Health & Safety Regulation | Implied risk assessment obligation (general duty of care) |

**Source:** DEL-33.01 Specification Standards; ASSUMPTION: WorkSafeBC risk assessment requirements

### Industry Standards

| Standard | Title | Applicability |
|----------|-------|---------------|
| ISO 31000 | Risk Management — Guidelines | Risk assessment methodology framework |
| ISO 45001 | Occupational Health & Safety Management Systems | Context for risk assessment within OHSMS |
| CSA Z1000 | Occupational Health and Safety Management | Canadian HSE management (includes risk assessment) |

**Source:** ASSUMPTION: Industry best practice standards; DEL-33.01 Specification Standards

### Employer's Requirements

- Volume 2 Part 1: General Requirements (risk assessment requirements)

**Source:** Decomposition Section 3 (Reference Documents); **location TBD**

### Additional Standards (TBD)

- Contractor's corporate risk assessment methodology and templates
- Project-specific risk assessment forms and criteria

**Source:** TBD: Contractor's corporate documentation

## Verification

### Verification Methods

| Requirement Category | Verification Method | Cross-Reference |
|---------------------|---------------------|-----------------|
| FR-1: Hazard Identification | Hazard coverage audit against project scope | Procedure Step 2 (Conduct Risk Assessment) |
| FR-2: Risk Evaluation | Risk evaluation methodology review | Procedure Step 2 (Risk Evaluation), Guidance Risk Matrix |
| FR-3: Control Measures | Control measure adequacy review | Procedure Step 2 (Control Identification), Guidance Hierarchy |
| FR-4: Residual Risk Acceptance | Approval signature verification | Procedure Step 3 (Review and Approval) |
| PR-1: Completeness | Risk assessment register audit — no work without assessment | Procedure Step 4 (Implementation), DEL-33.01 Procedure Step 4.3 |
| PR-2: Currency | Review date tracking, update records | Procedure Step 5 (Review and Update) |
| PR-3: Actionability | Traceability to SWMS/permits | Cross-reference DEL-33.03, DEL-33.01 Procedure Step 4.4 |
| IR-1: OHS Plan Interface | Consistency check with OHS Plan methodology | DEL-33.01 Specification FR-4, Procedure Step 4.3 |
| IR-2: Method Statements Interface | SWMS coverage of high-risk assessments | DEL-33.03 verification |
| IR-3: Permit-to-Work Interface | Permit forms include risk assessment | DEL-33.01 Procedure Step 4.4 |
| IR-4: Cross-Package Coordination | Cross-package coordination meeting records | DEL-33.01 Specification IR-3 |
| QR-1: Assessment Quality | Competency records, independent review signature | Procedure Prerequisites, Step 3 |
| QR-2: Assessment Revision Control | Document control audit, distribution records | Procedure Step 5, Guidance Revision Management |

**Source:** Procedure verification sections

### Acceptance Criteria

#### AC-1: Assessment Completeness

- All sections of risk assessment template are populated
- All identified hazards have corresponding control measures
- Residual risk rating calculated and approved
- All signatures (originator, checker, approver) present

**Source:** Datasheet Risk Assessment Structure; Procedure Verification

#### AC-2: Risk Control Adequacy

- Control measures follow hierarchy of controls (elimination/substitution preferred)
- Controls are specific and actionable
- Residual risk reduced to ALARP (As Low As Reasonably Practicable)
- Extreme risks reduced to High or below (unless Project Manager approval with justification)

**Source:** FR-3 (Control Measures), FR-4 (Residual Risk Acceptance); Guidance ALARP Principle

#### AC-3: Integration with Work Planning

- High-risk activities (risk rating ≥10) have corresponding SWMS (DEL-33.03)
- Permit-required activities have risk assessment incorporated into permit
- Training requirements identified in risk assessment are actioned (DEL-33.01 FR-7)

**Source:** PR-3 (Actionability), IR-2, IR-3

## Documentation

### Required Documentation Outputs

| Document | Description | Cross-Reference |
|----------|-------------|-----------------|
| Task Risk Assessments | Activity-based risk assessments using standard template | Datasheet Risk Assessment Structure, Procedure Step 2 |
| Job Hazard Analyses (JHA) | Step-by-step hazard analysis for high-risk tasks | Datasheet Risk Assessment Types, Guidance JHA Methodology |
| Risk Assessment Register | Database or log of all risk assessments (ID, activity, risk rating, status, review date) | Procedure Records, Guidance Register Management |
| Risk Assessment Summary (for OHS Plan) | Summary of project hazards for inclusion in DEL-33.01 Annex C | DEL-33.01 Datasheet Plan Structure (Annex C) |

**Source:** `_CONTEXT.md`, Decomposition line 730; Datasheet Construction

### Documentation Requirements

- **Format:** Structured template (Excel, database, or similar) — **TBD: ER format requirements**
- **Identification:** Unique ID (e.g., RA-PKG##-###-RevX)
- **Revision Control:** Date, revision number, description of changes
- **Distribution:** Controlled distribution to assessor, supervisor, HSE coordinator, affected workers
- **Language:** English (ASSUMPTION)
- **Medium:** Electronic (primary), printed copy for site use

**Source:** Datasheet Assessment Characteristics (Assessment Format); ASSUMPTION: Document requirements

### Records Management

- **Location:** Risk assessment database (electronic); `2_Checking/To/` (during review); `3_Issued/` (approved assessments)
- **Retention:** Duration of project + regulatory retention period (TBD: ER requirements)
- **Accessibility:** Accessible to all affected workers, supervisors, HSE personnel, Employer representatives, regulatory inspectors

**Source:** ASSUMPTION: D&B record management; DEL-33.01 Procedure Records section

---

**Document Status:** Pass 3/3 — Final reconciliation complete
**Generated:** 2026-01-28
**Cross-Document Consistency:** Verified against Datasheet, Guidance, Procedure
**Ready for:** WORKING_ITEMS session (human review and refinement)
