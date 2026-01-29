# Procedure: DEL-33.02 Risk Assessments

## Purpose

This procedure defines the process for **conducting** and **managing** **Risk Assessments** during the Design & Build execution phase of the Canola Oil Transload Facility.

**Deliverable Type:** Assessment
**Responsible Party:** D&B Contractor
**Source:** `_CONTEXT.md`, Decomposition line 730

### Dual-Use Application

This procedure serves two purposes:
1. **Production:** How to conduct risk assessments (Sections 2-3)
2. **Management:** How to maintain and update risk assessments during project execution (Section 4)

**Source:** 4_DOCUMENTS protocol — Procedure.md is dual-use

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED

Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`).

**Anticipated Upstream Dependencies:**
- DEL-33.01 (OHS Plan) — establishes risk assessment methodology (Section 4, FR-4)
- Project scope definition — understand activities to be assessed
- Work planning/scheduling — identify upcoming activities requiring assessment
- Design information — understand equipment, materials, methods

**Source:** `_DEPENDENCIES.md`; Specification IR-1 (OHS Plan Interface); DEL-33.01 Specification FR-4

### Reference Materials

**Required References:**
- DEL-33.01 (OHS Plan) — risk assessment methodology, risk matrix, acceptance criteria
- Employer's Requirements Volume 2 Part 1: General Requirements (risk assessment requirements) — **location TBD**
- WorkSafeBC OH&S Regulation — regulatory risk assessment obligations
- Project decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Contractor's corporate risk assessment templates and guidelines — **TBD**

**Supporting Information:**
- Work packages and scope descriptions (PKG-01 through PKG-26)
- Design drawings and specifications (understand equipment, layout, methods)
- Equipment manuals and data sheets (understand equipment hazards)
- Safety Data Sheets (SDS) for hazardous substances
- Incident/near-miss reports from similar projects (lessons learned)

**Source:** `_REFERENCES.md`; Specification Standards; DEL-33.01 Procedure Prerequisites

### Personnel Requirements

**Risk Assessment Team Roles:**

| Role | Responsibilities | Competency |
|------|-----------------|------------|
| Assessor (Originator) | Conducts risk assessment, identifies hazards, evaluates risks, proposes controls | Trained in risk assessment methodology; understands the work activity; preferably includes workers performing the task |
| Checker (Reviewer) | Independent review of assessment for completeness, accuracy, control adequacy | Trained in risk assessment; experience in the discipline; different person from assessor |
| Approver | Approves residual risk and authorizes work to proceed | Authority based on residual risk level: Low/Medium (HSE Coord), High (HSE Manager), Extreme (Project Manager) |

**Training Requirements:**
- Risk assessment methodology training (all assessors, checkers, approvers)
- Understanding of 5×5 risk matrix and hierarchy of controls
- Familiarity with project-specific hazards (per DEL-33.01)

**Source:** Specification QR-1 (competent personnel); Guidance Principle 1 (worker involvement); Datasheet Risk Matrix Parameters (approval authorities)

### Tools and Systems

**Required Tools:**
- Risk assessment template/form (Excel, database, or electronic form) — **TBD: ER format**
- Risk assessment register/database (track all assessments: ID, activity, risk rating, status, review date)
- Access to reference materials (SDS, equipment manuals, codes, DEL-33.01)
- Site inspection capability (camera for photos, measurement tools)

**Source:** Specification Documentation (format); ASSUMPTION: Risk assessment tools

## Steps

### Section 2: Conducting Risk Assessments

This section describes how to conduct a risk assessment (production).

#### Step 2.1: Determine Assessment Requirement

**Trigger Criteria for Risk Assessment:**

Risk assessment is required for:
- All new activities not previously performed on the project
- Changes to scope, design, or method affecting previously assessed activities
- Introduction of new equipment, materials, or subcontractors
- Incidents/near-misses revealing inadequate controls
- Simultaneous operations (SIMOPS) involving multiple packages in shared area
- Activity-specific assessments for permit-required work (hot work, confined space, excavation, working at height, marine operations)

**Source:** DEL-33.01 Guidance Example 3 (Risk Assessment Trigger Criteria); Specification PR-1 (Completeness); Datasheet Assessment Characteristics (Update Frequency)

**Actions:**
1. Review weekly look-ahead schedule to identify upcoming activities
2. Check risk assessment register to determine if assessment already exists
3. If no current assessment exists, initiate new assessment
4. If assessment exists but triggers apply (change, incident, periodic review), initiate assessment update (see Section 4)

**Output:** Decision to conduct new assessment or update existing assessment

**Verification:** Weekly look-ahead review documented, assessment requirement identified

#### Step 2.2: Conduct Risk Assessment

**Objective:** Systematically identify hazards, evaluate risks, and determine controls.

**Actions:**

**2.2.1: Activity Description**
- Describe the activity in detail (what, where, when, who, how)
- Break complex tasks into steps (for JHA-level assessments, use step-by-step analysis)
- Document assumptions and limitations (e.g., "assumes dry weather", "assumes utilities located")

**Source:** Guidance Task-Based Hazard Identification

**2.2.2: Hazard Identification**
- Involve workers who will perform the task (they know the work best)
- Use systematic prompts:
  - **Task-based:** What could go wrong at each step?
  - **Area-based:** Walk the work area, identify location-specific hazards
  - **SIMOPS:** Are other activities happening nearby? What interactions could occur?
- Refer to project-specific hazards in DEL-33.01 Datasheet (marine, rail, heavy lifting, confined space, hazardous substances, electrical, excavation)
- Review similar activities on this project or other projects (lessons learned)
- Consult references (SDS, equipment manuals, incident reports)

**Common Hazard Categories:**
- Physical (struck-by, caught-between, falls, electrical, fire/explosion)
- Health (noise, vibration, chemical exposure, ergonomic, heat/cold stress)
- Environmental (weather, marine conditions, unstable ground)
- Interface (Terminal operations, simultaneous activities, public/traffic)

**Output:** List of hazards for the activity

**Source:** Specification FR-1 (Hazard Identification); Guidance Hazard Identification Process; DEL-33.01 Datasheet Project-Specific Hazards

**2.2.3: Risk Evaluation (Initial Risk — Before Controls)**
- For each identified hazard, assess **Likelihood** (1-5: Rare to Almost Certain)
- For each hazard, assess **Consequence** (1-5: Insignificant to Catastrophic)
- Calculate **Initial Risk Rating** = Likelihood × Consequence
- Use definitions in Guidance (Risk Matrix Application) or DEL-33.01 OHS Plan

**Output:** Initial risk rating for each hazard (before controls)

**Source:** Specification FR-2 (Risk Evaluation); Datasheet Risk Matrix Parameters; Guidance Risk Matrix Application

**2.2.4: Control Identification**
- For each hazard, identify control measures using **hierarchy of controls**:
  1. **Elimination:** Can the hazard be removed entirely? (e.g., don't do the task, do it differently)
  2. **Substitution:** Can we use less hazardous materials/equipment/methods?
  3. **Engineering Controls:** Can we physically isolate or remove the hazard? (guards, barriers, ventilation)
  4. **Administrative Controls:** Procedures, training, permits, job rotation, signage
  5. **PPE:** Last line of defense (hard hats, gloves, respirators, harnesses)
- Controls must be **specific and actionable** (not generic "be careful" or "use PPE")
- Assign **responsibility** for each control (who implements/verifies)
- Consider **existing controls** (already in place) and **additional controls** (new measures required)

**Output:** List of control measures for each hazard (hierarchy applied)

**Source:** Specification FR-3 (Control Measures); Datasheet Control Hierarchy; Guidance Applying the Hierarchy of Controls

**2.2.5: Residual Risk Evaluation (After Controls)**
- Re-assess **Likelihood** and **Consequence** assuming controls are implemented and effective
- Calculate **Residual Risk Rating** = Likelihood × Consequence (after controls)
- Compare to risk tolerability:
  - Low (1-4): Acceptable
  - Medium (5-9): Tolerable with controls
  - High (10-16): Requires HSE Manager approval
  - Extreme (17-25): Requires Project Manager approval; must reduce to High or below

**ALARP Check:**
- For High and Extreme residual risks, document why additional controls are not reasonably practicable
- If Extreme risk cannot be reduced to High, escalate to Project Manager with justification

**Output:** Residual risk rating for each hazard (after controls)

**Source:** Specification FR-2, FR-4 (Residual Risk Acceptance); Guidance ALARP Principle; Datasheet Risk Matrix Parameters

**2.2.6: Risk Assessment Documentation**
- Complete risk assessment form/template with all sections:
  - Activity description, hazards, initial risk, controls, residual risk
  - Assessor name/signature/date
  - Review date or review trigger conditions
- Attach supporting information (photos, sketches, references)
- Assign unique risk assessment ID (e.g., RA-PKG##-###-Rev0)

**Output:** Completed risk assessment document

**Source:** Datasheet Risk Assessment Structure; Specification Documentation

**Verification:** All sections of risk assessment template populated, hazards match activity scope

#### Step 2.3: Review and Approval

**Objective:** Independent review and approval of risk assessment before work proceeds.

**Actions:**

**2.3.1: Independent Review (Checker)**
- **Checker** (different person from assessor) reviews risk assessment for:
  - **Completeness:** All hazards identified? All steps covered (if JHA)?
  - **Accuracy:** Risk ratings reasonable? Controls appropriate?
  - **Control Adequacy:** Hierarchy of controls applied? Controls specific and actionable?
  - **ALARP:** Residual risk reduced to ALARP? Extreme risks justified?
- Checker documents review (signature/date on form or separate review record)
- If deficiencies identified, return to assessor for revision

**2.3.2: Approval (Based on Residual Risk Level)**
- **Low/Medium Residual Risk (1-9):** HSE Coordinator approves
- **High Residual Risk (10-16):** HSE Manager approves
- **Extreme Residual Risk (17-25):** Project Manager approves (work may not proceed until risk reduced or PM accepts with documented justification)

**2.3.3: Issue Risk Assessment**
- Approved risk assessment issued to:
  - Assessor (for records)
  - Activity supervisor (for implementation)
  - HSE coordinator (for monitoring)
  - Affected workers (briefed via toolbox talk or pre-task meeting)
  - Risk assessment register updated (ID, activity, risk rating, approval date, review date)

**Output:** Approved and issued risk assessment

**Source:** Specification FR-4 (Residual Risk Acceptance); Specification QR-1 (independent review); Datasheet Risk Matrix Parameters (approval authorities)

**Verification:** Checker and approver signatures present, risk assessment distributed to affected personnel

### Section 3: Integrating Risk Assessments into Work Planning

**Objective:** Ensure risk assessments inform work execution (actionability).

**Actions:**

**3.1: Link to Safe Work Method Statements (SWMS)**
- High-risk activities (residual risk ≥10) require SWMS (DEL-33.03)
- SWMS developed based on risk assessment (hazards and controls from assessment inform SWMS content)
- Cross-reference risk assessment ID in SWMS

**Source:** Specification PR-3 (Actionability), IR-2 (Method Statements Interface); DEL-33.01 Specification FR-5

**3.2: Link to Permit-to-Work**
- Activity-specific risk assessments incorporated into permit forms:
  - Hot work permit: fire/explosion risk assessment
  - Confined space entry permit: atmospheric hazard assessment, rescue plan based on risks
  - Excavation permit: cave-in, striking utilities risk assessment
  - Work-at-height permit: fall risk assessment
  - Marine operations permit: marine hazard assessment
- Permit cannot be issued without approved risk assessment

**Source:** Specification IR-3 (Permit-to-Work Interface); DEL-33.01 Specification FR-5, Procedure Step 4.4

**3.3: Link to Training Requirements**
- Risk assessment identifies task-specific training needs (e.g., confined space, working at height, WHMIS)
- Training requirements communicated to training coordinator (DEL-33.01 / PKG-35)
- Workers cannot perform task without required training (verified in permit or pre-task briefing)

**Source:** Specification PR-3 (Actionability — training); DEL-33.01 Specification FR-7; Cross-reference PKG-35

**3.4: Pre-Task Briefing**
- Before work commences, supervisor conducts pre-task briefing with crew:
  - Review risk assessment (hazards, controls, residual risk)
  - Confirm controls are in place (equipment, PPE, permits)
  - Answer questions, address worker concerns
  - Emphasize stop-work authority if conditions change
- Document briefing (attendance, date, assessment reviewed)

**Source:** DEL-33.01 Procedure Step 4.2 (toolbox talks); ASSUMPTION: Pre-task briefing best practice

**Output:** Risk assessment integrated into SWMS, permits, training, pre-task briefings

**Verification:** Traceability from risk assessment to SWMS/permits, training records, briefing records

### Section 4: Managing Risk Assessments (Ongoing Maintenance)

**Objective:** Keep risk assessments current throughout project lifecycle.

#### Step 4.1: Risk Assessment Register Maintenance

**Actions:**
- Maintain risk assessment register (database or spreadsheet) with:
  - Risk Assessment ID
  - Activity description
  - Package / discipline
  - Initial risk rating (highest hazard)
  - Residual risk rating (highest hazard)
  - Status (Draft, Approved, Under Review, Superseded)
  - Approval date
  - Next review date
  - Revision number
- Update register weekly (new assessments, updates, status changes)
- Make register accessible to HSE team, supervisors, planners

**Output:** Current risk assessment register

**Source:** Specification Documentation (risk assessment register); ASSUMPTION: Register management best practice

**Verification:** Register reviewed in weekly HSE coordination meeting (DEL-33.01 Procedure Step 4.7)

#### Step 4.2: Periodic Review

**Actions:**
- **Quarterly Review:** All risk assessments reviewed quarterly (or per ER requirements)
  - Verify controls remain effective
  - Check for changes in scope, design, methods
  - Update if necessary
- **High-Risk Activity Monthly Review:** Risk assessments for high-risk activities (residual risk ≥10) reviewed monthly
- **Review Trigger:** If trigger condition occurs (see Step 2.1), review and update assessment immediately (do not wait for quarterly review)

**Output:** Risk assessment review records, updated assessments (if required)

**Source:** Specification PR-2 (Currency — periodic review); DEL-33.01 Guidance Example 3 (periodic review triggers)

**Verification:** Review dates tracked in register, reviews documented

#### Step 4.3: Update Risk Assessments

**Trigger Conditions for Update:**
- Scope, design, or method changes
- Incidents or near-misses revealing inadequate controls
- New equipment, materials, or subcontractors
- Periodic review identifies changes

**Update Process:**
- Assessor conducts update (may be different assessor if original assessor unavailable)
- Document changes (what changed, why update required)
- Re-evaluate risks and controls (Steps 2.2.3 through 2.2.5)
- Independent review and approval (Step 2.3)
- Increment revision number (e.g., Rev0 → Rev1)
- Supersede previous version (archive, update register status to "Superseded")
- Re-issue to affected personnel (briefing if significant changes)

**Output:** Updated risk assessment (new revision)

**Source:** Specification PR-2 (Currency — update triggers); Specification QR-2 (revision control)

**Verification:** Revision history documented, superseded versions archived, affected personnel notified

#### Step 4.4: Learning from Incidents

**Actions:**
- When incident or near-miss occurs:
  - Identify related risk assessment(s)
  - Review assessment to determine if hazard was identified and controls were adequate
  - If hazard not identified → update assessment to include hazard
  - If controls inadequate → update assessment with improved controls
  - If assessment was adequate but not followed → address compliance issue (not assessment issue)
- Document lessons learned in assessment update
- Share learning across similar activities (update generic assessments if applicable)

**Output:** Risk assessments updated based on incident investigation findings

**Source:** DEL-33.01 Specification FR-8 (Incident Management — lessons learned); DEL-33.01 Procedure Step 4.6 (CAPA)

**Verification:** Incident investigation reports reference risk assessment review, assessments updated as corrective actions

## Verification

### Risk Assessment Production Verification

| Verification Check | Method | Acceptance Criteria |
|--------------------|--------|---------------------|
| Hazard Identification Completeness | Hazard coverage audit | All credible hazards for activity identified; cross-check against DEL-33.01 project hazard list |
| Risk Evaluation Accuracy | Risk rating reasonableness review | Likelihood and consequence ratings justified; consistent with similar activities |
| Control Adequacy | Hierarchy of controls application check | Hierarchy applied; controls specific and actionable; not generic |
| Residual Risk Acceptance | Approval authority verification | Approval signature matches residual risk level (Low/Med: HSE Coord; High: HSE Mgr; Extreme: PM) |
| ALARP Justification | ALARP documentation review | High/Extreme risks have documented justification for residual risk level |
| Documentation Completeness | Template completeness check | All sections populated; assessor, checker, approver signatures present |

**Source:** Specification Verification (Methods); Specification Acceptance Criteria

### Risk Assessment Implementation Verification

| Verification Check | Method | Acceptance Criteria |
|--------------------|--------|---------------------|
| Assessment Availability | Pre-work verification | Approved risk assessment exists before work commences (no work without assessment) |
| SWMS Linkage | High-risk activity cross-check | All High/Extreme risk activities have corresponding SWMS (DEL-33.03) |
| Permit Linkage | Permit audit | All permit-required activities have risk assessment incorporated in permit |
| Training Linkage | Training records review | Task-specific training identified in risk assessment is completed (cross-reference PKG-35) |
| Pre-Task Briefing | Briefing record review | Pre-task briefings conducted; risk assessment reviewed with crew |
| Control Implementation | Site inspection | Controls identified in risk assessment are in place before work starts |
| Periodic Review Compliance | Review date tracking | Risk assessments reviewed per schedule (quarterly general, monthly high-risk) |

**Source:** Specification Verification (Implementation); Procedure Section 3 (Integration), Section 4 (Management)

## Records

### Risk Assessment Documents

| Record | Description | Location |
|--------|-------------|----------|
| Task Risk Assessments | Activity-based risk assessments (standard template) | Risk assessment database / `3_Issued/` |
| Job Hazard Analyses (JHA) | Step-by-step analyses for high-risk tasks | Risk assessment database / `3_Issued/` |
| Risk Assessment Register | Master log of all assessments (ID, activity, risk, status, review date) | Electronic database (accessible to HSE team, supervisors) |
| Review Records | Periodic review documentation (quarterly, monthly high-risk) | Risk assessment database |
| Revision History | Record of assessment updates (date, revision, reason for change) | Embedded in risk assessment document header |

**Source:** Specification Documentation; Datasheet Construction (Risk Assessment Structure)

### Supporting Records

| Record | Description | Location |
|--------|-------------|----------|
| Pre-Task Briefing Records | Attendance, risk assessment reviewed, date | Supervisor records (cross-reference DEL-33.01) |
| Checker Review Records | Independent review documentation | Risk assessment form or separate review log |
| Approval Records | Approval signatures on risk assessments | Risk assessment form |
| Incident-Driven Updates | Risk assessments updated due to incidents | Cross-reference incident investigation reports (DEL-33.01) |

**Source:** Procedure Steps 2.3, 3.4, 4.4

### Record Management

- **Retention:** Duration of project + regulatory retention period (TBD: ER requirements)
- **Accessibility:** Risk assessments accessible to all affected workers, supervisors, HSE personnel, Employer representatives, regulatory inspectors
- **Medium:** Electronic (risk assessment database — primary); printed copies for site use (permits, pre-task briefings)
- **Backup:** Electronic records backed up per IT disaster recovery plan
- **Superseded Versions:** Archived (not deleted) when new revision issued

**Source:** ASSUMPTION: D&B record management; DEL-33.01 Procedure Records section

---

**Document Status:** Pass 3/3 — Final reconciliation complete
**Generated:** 2026-01-28
**Cross-Document Consistency:** Verified against Datasheet, Specification, Guidance
**Ready for:** WORKING_ITEMS session (human review and refinement)
