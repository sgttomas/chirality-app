# Specification: DEL-33.03 Method Statements

## Scope

This specification defines the requirements for **Method Statements** (Safe Work Method Statements - SWMS) within **PKG-33 HSE Management**.

### Purpose

Method Statements shall define the execution method and controls for high-risk construction activities to meet safety, quality, and operational requirements established in DEL-33.01 (OHS Plan) and informed by DEL-33.02 (Risk Assessments).

**Source:** `_CONTEXT.md`, Decomposition line 731; DEL-33.01 Specification FR-5; DEL-33.02 Specification IR-2

### Anticipated Deliverable Artifacts

- Safe Work Method Statements (SWMS) by activity
- SWMS register/database

**Source:** `_CONTEXT.md`, Decomposition line 731

## Requirements

### Functional Requirements

#### FR-1: Activity Scope Definition
SWMS shall clearly define the scope of work including what, where, when, who, and how.

**Source:** Datasheet SWMS Structure; ASSUMPTION: SWMS completeness
**Verification:** Scope review (Specification Section 5)
**Guidance Cross-Reference:** Guidance SWMS Content Requirements

#### FR-2: Risk Assessment Integration
SWMS shall be based on approved risk assessments (DEL-33.02), including summary of key hazards and residual risk ratings.

**Source:** DEL-33.02 Specification IR-2, PR-3; Datasheet Development Basis
**Verification:** Risk assessment cross-check (Specification Section 5)
**Guidance Cross-Reference:** Guidance Risk Assessment to SWMS Linkage

#### FR-3: Regulatory Compliance
SWMS shall address applicable WorkSafeBC requirements and project-specific regulations.

**Source:** DEL-33.01 Specification FR-3; Datasheet Conditions (Regulatory Framework)
**Verification:** Regulatory compliance review (Specification Section 5)

#### FR-4: Roles and Responsibilities
SWMS shall define roles and responsibilities for all personnel involved in the activity.

**Source:** DEL-33.01 Specification FR-2; Datasheet SWMS Structure
**Verification:** Role definition completeness (Specification Section 5)

#### FR-5: Plant and Equipment
SWMS shall list all required tools, equipment, and materials, including inspection/certification requirements.

**Source:** Datasheet SWMS Structure; ASSUMPTION: Equipment specification in SWMS
**Verification:** Equipment list completeness (Specification Section 5)

#### FR-6: Step-by-Step Procedure (Core Requirement)
SWMS shall provide sequential work steps with specific controls for each step following the hierarchy of controls.

**Source:** Datasheet SWMS Structure (core section); DEL-33.02 Datasheet Control Hierarchy
**Verification:** Procedure clarity and control adequacy (Specification Section 5)
**Guidance Cross-Reference:** Guidance Writing Effective Step-by-Step Procedures

#### FR-7: Emergency Procedures
SWMS shall include emergency response procedures specific to the activity's hazards.

**Source:** Cross-reference DEL-33.07 Emergency Response Plan; Datasheet SWMS Structure
**Verification:** Emergency procedure adequacy (Specification Section 5)

#### FR-8: Training and Competency
SWMS shall specify required training, certifications, and competency for personnel.

**Source:** DEL-33.01 Specification FR-7; Datasheet SWMS Structure; Cross-reference PKG-35
**Verification:** Training requirements completeness (Specification Section 5)

### Performance Requirements

#### PR-1: SWMS Requirement Trigger
SWMS required for:
- High-risk activities (residual risk ≥10 from DEL-33.02)
- Permit-required work (hot work, confined space, excavation, work at height, marine)
- Novel/non-routine activities
- Employer or regulatory requirements

**Source:** Datasheet SWMS Triggers; DEL-33.02 Specification IR-2; DEL-33.01 Specification FR-5

#### PR-2: Pre-Work Approval
SWMS must be approved before work commences. No work without approved SWMS for triggered activities.

**Source:** ASSUMPTION: SWMS as prerequisite for high-risk work
**Verification:** Pre-work SWMS verification (Specification Section 5)

#### PR-3: Worker Understanding
SWMS must be communicated to all workers via pre-task briefing; workers acknowledge understanding.

**Source:** DEL-33.01 Procedure Step 4.4 (pre-task briefing); ASSUMPTION: Worker engagement
**Verification:** Briefing records, worker acknowledgment (Specification Section 5)

### Interface Requirements

#### IR-1: Risk Assessment Interface
SWMS developed from approved risk assessments (DEL-33.02); risk assessment ID referenced in SWMS.

**Source:** DEL-33.02 Specification IR-2; DEL-33.02 Procedure Section 3.1
**Verification:** Risk assessment traceability (Specification Section 5)

#### IR-2: Permit-to-Work Interface
SWMS integrated into permit process; permit cannot be issued without approved SWMS (for permit-required activities).

**Source:** DEL-33.01 Specification FR-5; DEL-33.02 Specification IR-3; Datasheet SWMS Types (Permit-Integrated)
**Verification:** Permit-SWMS linkage audit (Specification Section 5)

#### IR-3: OHS Plan Interface
SWMS implement safe work procedures defined in DEL-33.01 (OHS Plan Section 5).

**Source:** DEL-33.01 Specification FR-5; DEL-33.01 Procedure Step 2.3 (Section 5)
**Verification:** Consistency with OHS Plan requirements (Specification Section 5)

### Quality Requirements

#### QR-1: SWMS Quality
SWMS prepared by competent personnel, independently reviewed, approved by appropriate authority.

**Source:** ASSUMPTION: Quality requirements for procedures
**Verification:** Competency records, review signatures (Specification Section 5)

#### QR-2: SWMS Revision Control
SWMS revision-controlled; updates when scope/method changes.

**Source:** ASSUMPTION: Document control requirements
**Verification:** Revision history, distribution records (Specification Section 5)

## Standards

**Applicable Standards:**
- WorkSafeBC OH&S Regulation (safe work procedures)
- ISO 45001 (OHSMS — safe work procedures)
- Employer's Requirements (SWMS requirements — **TBD**)

## Verification

See Procedure Verification section for detailed verification methods.

## Documentation

**Required Outputs:**
- Activity-specific SWMS
- SWMS register (ID, activity, risk rating, approval date, review date)

**Format:** TBD (ER requirements)

---

**Document Status:** Pass 3/3 — Final reconciliation complete
**Generated:** 2026-01-28
**Cross-Document Consistency:** Verified against Datasheet, Guidance, Procedure
**Ready for:** WORKING_ITEMS session (human review and refinement)
