# Procedure: DEL-33.03 Method Statements

## Purpose

This procedure defines how to **develop** and **manage** Safe Work Method Statements (SWMS) during the Design & Build execution phase.

**Deliverable Type:** Procedure
**Responsible Party:** D&B Contractor
**Source:** `_CONTEXT.md`, Decomposition line 731

## Prerequisites

**Dependency Tracking Mode:** NOT_TRACKED

**Upstream Dependencies:**
- DEL-33.01 (OHS Plan) — establishes SWMS requirements (Section 5, FR-5)
- DEL-33.02 (Risk Assessments) — approved risk assessment is basis for SWMS

**Reference Materials:**
- DEL-33.01 (OHS Plan)
- DEL-33.02 (Risk Assessments) — specific risk assessment for the activity
- Employer's Requirements (SWMS requirements — **TBD**)
- Contractor's SWMS templates
- Equipment manuals, SDS, design drawings

**Personnel Requirements:**
- SWMS Author: Supervisor or competent person familiar with the work
- Reviewer: HSE Coordinator or discipline lead
- Approver: HSE Coordinator (Medium risk), HSE Manager (High/Extreme risk)

**Source:** Specification QR-1; DEL-33.02 Procedure Prerequisites

## Steps

### Section 2: Developing SWMS

#### Step 2.1: Identify SWMS Requirement

**Trigger:** Risk assessment (DEL-33.02) identifies residual risk ≥10 (High or Extreme), OR permit-required work, OR Employer/regulatory requirement.

**Actions:**
1. Review weekly look-ahead schedule
2. Check risk assessments for upcoming activities
3. Determine if SWMS required (per Datasheet SWMS Triggers, Specification PR-1)
4. Check SWMS register for existing SWMS (may reuse generic SWMS or develop task-specific)

**Output:** Decision to develop new SWMS or use existing

**Source:** Specification PR-1; Datasheet SWMS Triggers

#### Step 2.2: Develop SWMS Content

**Actions:**

**2.2.1: Use Risk Assessment as Basis**
- Obtain approved risk assessment (DEL-33.02) for the activity
- Extract key hazards, risk ratings, control measures
- Reference risk assessment ID in SWMS header

**2.2.2: Define Scope and Roles**
- Describe activity scope (what, where, when, who, duration) — Specification FR-1
- Define roles and responsibilities — Specification FR-4
- Identify required plant and equipment — Specification FR-5

**2.2.3: Write Step-by-Step Procedure (Core Content)**
- Break work into sequential steps
- For each step, specify:
  - Action (what to do)
  - Controls (how to do it safely — from risk assessment)
  - Verification (how to confirm step is safe)
- Follow hierarchy of controls (eliminate > substitute > engineer > admin > PPE)
- Use clear, specific, active-voice language (see Guidance)

**2.2.4: Add Emergency Procedures**
- Identify emergency scenarios for this activity
- Specify emergency response (reference DEL-33.07 as needed)
- Define abort criteria

**2.2.5: Specify Training/Competency**
- List required training, certifications, competencies (cross-reference PKG-35)

**Output:** Draft SWMS

**Source:** Specification FR-1 through FR-8; Datasheet SWMS Structure; Guidance Writing Effective Procedures

#### Step 2.3: Review and Approval

**Actions:**

**2.3.1: Author Self-Check**
- Completeness (all sections populated)
- Consistency with risk assessment
- Clarity (worker can follow the steps)

**2.3.2: Independent Review**
- Reviewer (HSE Coordinator or discipline lead) checks:
  - Risk assessment integration (hazards and controls match)
  - Procedure clarity and feasibility
  - Regulatory compliance
  - Control adequacy
- Reviewer signs SWMS

**2.3.3: Approval**
- Medium risk activity: HSE Coordinator approves
- High/Extreme risk activity: HSE Manager approves
- Approver signs SWMS

**Output:** Approved SWMS

**Source:** Specification QR-1; Datasheet Approval Level

#### Step 2.4: Issue and Communicate

**Actions:**
1. Issue SWMS to:
   - Activity supervisor
   - HSE coordinator
   - Affected workers (via pre-task briefing)
2. Update SWMS register (ID, activity, risk rating, approval date, review date)
3. Distribute to site (controlled copy)

**Output:** SWMS issued and registered

**Source:** ASSUMPTION: SWMS distribution

### Section 3: Implementing SWMS

#### Step 3.1: Pre-Task Briefing

Before work commences, supervisor conducts briefing with crew:
- Review SWMS (step-by-step)
- Confirm controls are in place (equipment, PPE, permits)
- Answer questions
- Workers acknowledge understanding (sign briefing record)

**Output:** Pre-task briefing record

**Source:** Specification PR-3; DEL-33.01 Procedure Step 4.4; DEL-33.02 Procedure Section 3.4

#### Step 3.2: Work Execution

Workers follow SWMS step-by-step. Supervisor monitors compliance. Workers have stop-work authority if conditions change or SWMS inadequate.

**Source:** DEL-33.01 Guidance Principle 5 (stop-work authority)

#### Step 3.3: Permit Integration (if applicable)

For permit-required work, SWMS integrated into permit:
- Permit cannot be issued without approved SWMS
- SWMS ID referenced on permit
- Permit conditions aligned with SWMS controls

**Source:** Specification IR-2; DEL-33.02 Specification IR-3

### Section 4: Managing SWMS

#### Step 4.1: SWMS Register Maintenance

Maintain SWMS register (database or spreadsheet) with SWMS ID, activity, risk rating, approval date, review date, status.

**Source:** Specification Documentation

#### Step 4.2: SWMS Review and Update

**Review Triggers:**
- Scope/method changes
- Incident reveals SWMS inadequacy
- Periodic review (annually or per ER)

**Update Process:**
- Revise SWMS content
- Independent review and approval
- Increment revision number
- Reissue and brief workers on changes

**Source:** Specification QR-2; ASSUMPTION: SWMS revision control

## Verification

**Verification Checks:**
- SWMS completeness (all sections populated)
- Risk assessment integration (traceability)
- Control adequacy (hierarchy applied, specific controls)
- Approval signatures (appropriate authority)
- Pre-work briefing (workers understand SWMS)
- Compliance (workers following SWMS during work)

**Source:** Specification Verification

## Records

**Records:**
- Approved SWMS (activity-specific)
- SWMS register
- Pre-task briefing records (with worker acknowledgment)
- SWMS review/revision records

**Location:** SWMS database / `3_Issued/`; briefing records with supervisor

**Source:** Specification Documentation

---

**Document Status:** Pass 3/3 — Final reconciliation complete
**Generated:** 2026-01-28
**Cross-Document Consistency:** Verified against Datasheet, Specification, Guidance
**Ready for:** WORKING_ITEMS session (human review and refinement)
