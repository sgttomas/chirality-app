# Procedure: DEL-03-02 Detailed Design and Construction Docs Plan

## Purpose

### What This Procedure Accomplishes
This procedure describes two complementary workflows:

1. **Production workflow:** How to produce the DEL-03-02 plan document itself during the proposal phase (for submission with the RFP response)
2. **Operational workflow:** How the plan will be executed post-award to produce the actual detailed design and construction documents

**Context:** This is a "procedure for a plan document" — meaning the procedure is recursive. It describes both how to write the plan (proposal deliverable) and what the plan should describe (post-award design documentation process).

*Source: AGENT_4_DOCUMENTS instruction (Procedure.md is a typed structure that can be applied recursively to production and/or operation), _CONTEXT.md (deliverable type: Plan Document)*

---

## Prerequisites

### Before Starting Production of the Plan Document (Proposal Phase)

**Dependencies:**
- **Dependency tracking mode:** NOT_TRACKED (dependencies coordinated externally by humans per _DEPENDENCIES.md)
- **Coordination note:** This deliverable should be coordinated with DEL-03-01 (Design Methodology Narrative) to ensure consistency in process descriptions. Refer to execution/_Coordination/_COORDINATION.md for schedule-driven coordination.

**Reference materials that must be available:**
- **RFP Section 7.1.8:** Detailed design and construction documents plan requirements — *location: _Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf (TBD: specific page/section)*
- **Addendum 03:** Scope clarifications impacting design documentation — *location: _Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf*
- **Decomposition document:** Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md (Section 8: DEL-03-02 entry; Section 9: SOW-018)
- **_CONTEXT.md, _DEPENDENCIES.md, _REFERENCES.md:** Deliverable context files (created by PREPARATION)
- **Appendix I (Design-Build Team List):** To identify which disciplines/consultants are responsible for which scopes — *location: TBD (from DEL-07-03 or RFP appendix)*
- **Project schedule (DEL-08-01):** To align document production milestones with overall project timeline — *location: TBD (coordinated deliverable)*

**Team readiness:**
- **Proposal Manager / Design Manager:** Must be available to draft and review the plan document
- **Subject matter experts:** Input from discipline leads (architecture, structural, MEP, civil) on their typical deliverable scopes and QA/QC processes
- **Construction Manager:** Input on constructability review process

*Source: _DEPENDENCIES.md, _REFERENCES.md, decomposition Section 8 (related deliverables)*

---

### Before Executing the Plan (Post-Award Design Phase)

**Prerequisites for operational execution (after contract award):**
- **Contract executed:** Design-Build contract in place with Town of Penhold
- **Kick-off meeting complete:** Owner, Design-Builder, and key consultants aligned on process
- **Design team mobilized:** All disciplines from Appendix I are under contract and ready to proceed
- **Project schedule baselined:** DEL-08-01 (Detailed Project Schedule) approved by Owner; document production milestones established
- **Document management system (DMS) operational:** Software platform selected, access provisioned, protocols configured
- **BIM coordination platform established (if applicable):** Software selected, coordinate system defined, file exchange protocols agreed
- **Owner Statement of Requirements (OSR) and Functional Program confirmed:** Baseline requirements are clear and accepted by both parties
- **Site survey files available:** Per Addendum 03, survey files provided by Owner after award

> **[SL:E-001]** Prerequisites require a binding mobilization gate: all prerequisites must be certified complete in writing before commencing Step B-03 (Schematic Design). A "Design Mobilization Gate Checklist" artifact should be used to confirm readiness. *(SourcePath: Procedure.md § Part B / Prerequisites)*

**Mobilization Gate Requirement:**
All prerequisites must be verified and documented via a "Design Mobilization Gate Checklist" before design work commences. The checklist confirms:
- [ ] Contract fully executed
- [ ] Kick-off meeting held (minutes on file)
- [ ] All discipline leads confirmed and under contract
- [ ] Schedule baselined and Owner-approved
- [ ] DMS operational (test upload/download verified)
- [ ] BIM platform operational (if applicable)
- [ ] OSR and Functional Program confirmed
- [ ] Survey files received (or waiver documented if delayed)

**Gate authority:** Design Manager certifies mobilization complete; Project Manager approves commencement of design work.

*Source: Decomposition Section 4 (Addendum 03: survey files after award), SOW-024; ASSUMPTION on typical post-award mobilization requirements*

---

## Steps

### Part A: Steps to Produce the Plan Document (Proposal Phase)

#### Prerequisites for Part A (Proposal Phase)

> **[SL:F-002]** Part A requires a prerequisites section mirroring Part B structure. These foundational workflow prerequisites must be confirmed before proposal production begins. *(SourcePath: Procedure.md § Part A / Step A-01)*

**Prerequisites:**
- **RFP Section 7.1.8 accessible:** Confirm full RFP document is available and Section 7.1.8 has been read
- **Addenda integrated:** Confirm Addenda 01, 02, and 03 have been reviewed and requirements extracted
- **Team availability:** Proposal Manager and Design Manager available; discipline lead SMEs accessible for input
- **Decomposition document available:** Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md accessible
- **Context files in place:** _CONTEXT.md, _DEPENDENCIES.md, _REFERENCES.md created by PREPARATION

---

#### Step A-01: Gather Input from RFP and Team
**Action:** Review RFP Section 7.1.8 and extract requirements for the documentation plan. Interview or survey discipline leads to understand their typical deliverable scopes and QA/QC practices.

**Responsible:** Proposal Manager / Design Manager

**Output:** Notes on RFP requirements and team capabilities

**Verification:** Cross-check notes against RFP Section 7.1.8 checklist; confirm all required elements are captured

*Source: _CONTEXT.md (description: "describes discipline deliverables, QA checks, review cycles"), RFP Section 7.1.8 — location TBD*

---

#### Step A-02: Define Discipline Scopes
**Action:** For each design discipline (architecture, structural, mechanical, electrical, civil, landscape if applicable), list the deliverables they will produce at each phase (SD, DD, CD, IFC). Ensure Addendum 03 requirements are explicitly included (overhead doors, bay sumps, exhaust systems, generator, solar-ready provisions, etc.).

**Responsible:** Design Manager with input from discipline leads

**Output:** Discipline scope matrix (by phase)

**Verification:** Compare matrix to Addendum 03 checklist (decomposition Section 4) to confirm all addenda-driven requirements are assigned to a discipline

*Source: Decomposition Section 4 (Addendum 03 impacts), Specification RQ-06 (discipline scope definition), Guidance Example 1 (drawing index structure)*

---

#### Step A-03: Define QA/QC Checkpoints
**Action:** Identify QA/QC layers (self-check, Design Manager review, code review, constructability review, Owner review) and assign them to phases. Define what each checkpoint verifies and who is responsible.

**Responsible:** Design Manager / Proposal Manager

**Output:** QA/QC checkpoint table (by phase and layer)

**Verification:** Ensure at minimum: self-check at all phases, Design Manager review before Owner submittal, code review before permit submission, constructability review at DD and CD

*Source: Specification RQ-03 (QA/QC), Guidance P-04 (QA/QC is multi-layered)*

---

#### Step A-04: Define Coordination Process
**Action:** Describe how disciplines will coordinate (meeting frequency, BIM clash detection workflow, overlay reviews, interface management). Specify coordination tools and software platforms.

**Responsible:** Design Manager with input from BIM/CAD coordinator

**Output:** Coordination process description and tool list

**Verification:** Ensure coordination is described as continuous (not a single event per Guidance P-02); verify BIM coordination workflow is included if BIM approach is proposed

*Source: Specification RQ-02 (coordination), Guidance P-02 (coordination is continuous), Guidance Example 2 (BIM workflow)*

---

#### Step A-05: Define Document Control Protocols
**Action:** Establish drawing numbering system, revision tracking procedures, distribution protocols, and archival/retention requirements. Identify document management system (or state that it will be selected post-award).

**Responsible:** Design Manager / Document Controller

**Output:** Document control protocol description

**Verification:** Ensure numbering system, revision tracking, distribution, and retention are all addressed per Specification RQ-04

*Source: Specification RQ-04 (document control), Guidance P-05 (document control prevents chaos)*

---

#### Step A-06: Define Owner Review Process
**Action:** Describe how documents will be submitted to Owner for review at phase gates, expected review period duration, comment log format, response matrix process, and approval signoff requirements.

**Responsible:** Design Manager / Proposal Manager

**Output:** Owner review process description

**Verification:** Ensure submittal format, review period, comment incorporation, and approval signoff are all defined per Specification RQ-05

*Source: Specification RQ-05 (Owner review), Guidance P-03 (Owner engagement at key milestones), Guidance Example 3 (Owner review process)*

---

#### Step A-07: Integrate Code Compliance and Permitting Strategy
**Action:** Describe how construction documents will meet Alberta Building Code and local permitting requirements. State whether third-party code review will be used. Outline permit submission and comment incorporation process.

**Responsible:** Design Manager with input from code consultant (if applicable)

**Output:** Code compliance and permitting section of plan

**Verification:** Ensure code compliance checkpoints and permit coordination are addressed per Specification RQ-07 and Guidance considerations on permitting

*Source: Specification RQ-07 (code compliance), Guidance considerations (permit coordination with AHJ)*

---

#### Step A-08: Integrate Addenda Traceability
**Action:** Create a checklist or matrix showing which addenda requirements (Addendum 03: overhead doors, bay sumps, exhaust, generator, fill stations, solar-ready, room sizing) are assigned to which disciplines and will be verified in which QA/QC checkpoints.

**Responsible:** Design Manager / Proposal Manager

**Output:** Addenda integration checklist

**Verification:** Cross-check against decomposition Section 4 (Addendum 03 impacts summary) to ensure all items are traceable

*Source: Specification RQ-08 (addenda integration), Guidance P-06 (addenda requirements must be traceable)*

---

#### Step A-09: Align with Project Schedule
**Action:** Coordinate with DEL-08-01 (Detailed Project Schedule) to ensure document production milestones (SD review, DD review, CD review, permit submission, IFC issuance) are consistent with the overall schedule. Reference milestone dates or durations in the plan.

**Responsible:** Design Manager / Scheduler

**Output:** Milestone alignment table or narrative

**Verification:** Cross-check milestone dates/durations with DEL-08-01; resolve any conflicts

*Source: Decomposition Section 8 (DEL-08-01 relationship), Guidance considerations (design phase pacing and overlap)*

---

#### Step A-10: Draft and Review Plan Document
**Action:** Assemble all sections (discipline scopes, QA/QC, coordination, document control, Owner review, code compliance, addenda integration, schedule alignment) into a coherent narrative plan document. Conduct internal review with Proposal Manager and key discipline leads.

**Responsible:** Design Manager (author); Proposal Manager (reviewer); discipline leads (SME reviewers)

**Output:** Draft DEL-03-02 plan document

**Verification:** Internal review checklist: all sections present, no conflicts with other deliverables (esp. DEL-03-01, DEL-08-01), RFP Section 7.1.8 requirements addressed

*Source: _CONTEXT.md (acceptance criteria: "Describes completeness, coordination, and control of issued drawings/specs")*

---

#### Step A-11: Incorporate into Proposal Package
**Action:** Provide final DEL-03-02 plan document to Proposal Manager for inclusion in the full proposal PDF (PKG-01: DEL-01-02 Final Submission Package). Ensure document is placed in the correct RFP section order (Section 7.1.8 content).

**Responsible:** Proposal Manager

**Output:** DEL-03-02 integrated into proposal PDF

**Verification:** Confirm DEL-03-02 is in the correct section and under 15 MB total proposal size (constraint C-01)

*Source: Decomposition Section 3 (hard constraints: C-01 format, C-02 required structure/order), Section 7 (PKG-01 submission package)*

---

### Part B: Steps to Execute the Plan (Post-Award Design Phase)

#### Decision Authority and Escalation Path

> **[SL:A-004]** Post-award operational workflow requires clear definition of approval signoff authority and conflict escalation path when Owner and Design-Builder disagree on design or document adequacy. *(SourcePath: Procedure.md § Part B)*

**Decision Authority:**
- **Design Manager:** Approves design decisions within approved scope/budget; signs off on QA/QC checkpoints; submits documents to Owner
- **Project Manager:** Approves changes affecting scope, cost, or schedule; escalation point for disputes
- **Owner's Representative:** Provides design approvals at phase gates; final authority on Owner requirements interpretation

**Escalation Path (when Owner rejects or modifies design):**
1. **Level 1 (Design Manager):** Attempt resolution through clarification, revised approach, or additional documentation
2. **Level 2 (Project Manager):** If Level 1 fails, escalate to PM for negotiation with Owner on scope/cost/schedule trade-offs
3. **Level 3 (Contract Administration):** If Level 2 fails, invoke contract dispute resolution provisions (if applicable)

**Conflict Resolution Protocol:**
- Design Manager documents issue in "Design Decision Log" with: issue description, Owner position, Design-Builder position, proposed resolution
- If resolution requires scope/cost/schedule re-negotiation, change management process applies (see Guidance Example 5)

---

#### Risk Contingencies for Mobilization

> **[SL:C-003]** Procedure should acknowledge that mobilization risks and tool readiness risks may impact design start. These risks should be captured in DEL-09-01 (Risk Register) with mitigation plans. *(SourcePath: Procedure.md § Part B / Steps B-01, B-02)*

**Identified Mobilization Risks (cross-reference DEL-09-01):**
- **Discipline mobilization delay:** Key discipline (e.g., structural) not available at design start — *Mitigation: Identify backup resources; adjust phasing to start with available disciplines*
- **DMS platform delay:** Document management system not operational — *Mitigation: Use interim file-sharing with strict naming conventions; migrate to DMS when ready*
- **Survey file delay:** Site survey files not provided by Owner — *Mitigation: Proceed with available data; flag assumptions; plan resurvey coordination*

**Impact Management:** If prerequisites are not met by design start date, Design Manager escalates to Project Manager for schedule impact assessment and Owner notification.

---

#### Step B-01: Mobilize Design Team
**Action:** Convene kick-off meeting with all disciplines (per Appendix I). Review the approved DEL-03-02 plan and confirm roles, responsibilities, deliverable scopes, QA/QC checkpoints, and coordination procedures.

**Responsible:** Design Manager / Project Manager

**Output:** Kick-off meeting minutes with acknowledgments from all disciplines

**Verification:** All disciplines confirm understanding and acceptance of plan procedures

*Source: ASSUMPTION (standard post-award mobilization); contract terms — TBD*

---

#### Step B-02: Set Up Document Management and Coordination Tools
**Action:** Establish document management system (DMS) and BIM coordination platform (if applicable). Provision access for all team members. Configure folder structures, naming conventions, and revision tracking per plan protocols.

**Responsible:** Design Manager / IT/BIM Coordinator

**Output:** Operational DMS and BIM platform with access provisioned

**Verification:** Test upload, download, revision tracking, and clash detection functions; confirm all disciplines can access

*Source: Specification RQ-04 (document control), Guidance considerations (BIM vs. 2D CAD workflow)*

---

#### Coordination Meeting Protocol

> **[SL:X-002]** Coordination meetings require explicit protocol definition for systematic reassurance regularity. *(SourcePath: Procedure.md § Part B / Steps B-03, B-06, B-09)*

**Meeting Frequency:**
- **Minimum:** Weekly coordination meetings during active design phases (SD, DD, CD)
- **Increased frequency:** Daily or twice-weekly during final coordination push (2 weeks before permit submission)
- **Holiday/compressed schedule:** Meetings may be rescheduled but not skipped; minimum one meeting per week maintained

**Meeting Structure:**
- **Chair:** Design Manager (or designated BIM Coordinator)
- **Required attendees:** All discipline leads (or designated representatives)
- **Duration:** 60-90 minutes maximum

**Meeting Agenda (Standard):**
1. Review of action items from previous meeting
2. Coordination issues by discipline (round-robin)
3. BIM clash detection report review (if applicable)
4. Schedule status and upcoming milestones
5. Open discussion / new issues
6. Action item assignment and next meeting confirmation

**Minutes Requirements:**
- Minutes prepared within 24 hours of meeting
- Include: date, attendees, topics discussed, issues identified, action items with responsible party and due date
- Minutes archived in DMS (folder: /Coordination Reports/)
- Action items logged in project issue tracker with resolution target dates

**Issue Tracking:**
- All coordination issues logged with: issue ID, description, discipline(s) affected, priority (critical/major/minor), assigned party, due date, status
- Unresolved critical issues escalated to Project Manager

---

---

#### Step B-03: Commence Schematic Design (SD) Phase (if applicable to post-award scope)
**Action:** Each discipline develops SD-level deliverables per plan scope matrix. Conduct weekly coordination meetings. Perform initial BIM clash detection (if applicable). Design Manager reviews for completeness.

**Responsible:** Discipline leads (authors); Design Manager (coordinator/reviewer)

**Output:** SD submittal set (all disciplines)

> **[SL:D-002]** Outputs require detailed acceptance criteria to define "complete" for settled throughput deployment. *(SourcePath: Procedure.md § Part B / Steps B-03, B-06)*

**SD Output Acceptance Criteria:**
- Site plan showing building footprint, orientation, setbacks
- Conceptual floor plans for all areas (Fire Hall, Public Works)
- Preliminary massing model or key sections/elevations
- Discipline narratives describing systems approach (HVAC strategy, structural system, electrical distribution)
- Coordination meeting minutes (minimum 2 meetings during SD phase)
- Design Manager QA/QC sign-off memo (dated, signed)

**Verification:** Internal QA/QC checklist complete; coordination meeting minutes document issue resolution; Design Manager sign-off before Owner submittal

*Source: Guidance P-02 (continuous coordination), Specification RQ-01 (completeness)*

---

#### Step B-04: Submit SD to Owner for Review
**Action:** Assemble SD submittal per plan procedures (format, transmittal letter, review period). Submit to Owner. Track receipt and review period.

**Responsible:** Design Manager / Project Manager

**Output:** SD submittal transmitted to Owner

**Verification:** Owner confirms receipt and review period start date

*Source: Specification RQ-05 (Owner review), Guidance Example 3 (Owner review process)*

---

#### Step B-05: Incorporate Owner SD Comments
**Action:** Receive Owner comment log. Prepare response matrix (accept/revise/rebuttal). Incorporate accepted comments into design. Resubmit revised SD if major changes required.

**Responsible:** Design Manager with discipline leads

**Output:** SD response matrix and revised SD set (if applicable)

**Verification:** Owner accepts SD and authorizes proceeding to DD

*Source: Guidance Example 3 (comment incorporation process)*

---

#### Step B-06: Advance to Design Development (DD) Phase
**Action:** Each discipline develops DD-level deliverables per plan scope matrix (systems selections, major dimensions locked, cost estimate alignment). Conduct continuous coordination (weekly meetings, BIM clash detection, overlay reviews). Perform internal QA/QC (self-check, Design Manager review). Conduct constructability review with Construction Manager.

**Responsible:** Discipline leads (authors); Design Manager (coordinator); Construction Manager (constructability reviewer)

**Output:** DD submittal set (all disciplines)

**DD Output Acceptance Criteria:**
- Complete floor plans with dimensions and room labels
- Building elevations and key sections
- Systems selections documented (HVAC equipment, structural system, electrical panels)
- Preliminary specifications for major systems
- BIM coordination model (if BIM approach) with clash detection run complete
- Constructability review comments incorporated (Construction Manager sign-off)
- Cost estimate aligned with budget (±10% accuracy)
- Addenda checklist progress update (all Addendum 03 items addressed in DD scope)
- Coordination meeting minutes (weekly throughout DD phase)
- Design Manager QA/QC sign-off memo

**Verification:** Internal QA/QC checklist complete; coordination issues resolved; constructability review comments incorporated; Design Manager sign-off; cost estimate aligns with budget (DEL-05-01/02 baseline)

*Source: Specification RQ-03 (QA/QC), Guidance P-04 (multi-layered QA/QC), Guidance T-02 (detail level at each phase)*

---

#### Step B-07: Submit DD to Owner for Review
**Action:** Assemble DD submittal per plan procedures. Submit to Owner with transmittal and review period notice.

**Responsible:** Design Manager / Project Manager

**Output:** DD submittal transmitted to Owner

**Verification:** Owner confirms receipt

*Source: Specification RQ-05, Guidance Example 3*

---

#### Step B-08: Incorporate Owner DD Comments
**Action:** Receive Owner DD comment log. Prepare response matrix. Incorporate accepted comments. Resubmit revised DD if major changes required.

**Responsible:** Design Manager with discipline leads

**Output:** DD response matrix and revised DD set (if applicable)

**Verification:** Owner accepts DD and authorizes proceeding to CD

*Source: Guidance Example 3*

---

#### Step B-09: Advance to Construction Documents (CD) Phase
**Action:** Each discipline develops CD-level deliverables (100% construction detail, full specifications, all schedules complete). Conduct intensive coordination (increased meeting frequency, final BIM clash detection runs). Perform all QA/QC layers: self-check, Design Manager review, third-party code review (if included in plan), constructability review. Verify addenda integration checklist (all Addendum 03 requirements present and correct).

**Responsible:** Discipline leads (authors); Design Manager (coordinator); third-party code reviewer (if applicable); Construction Manager (constructability)

**Output:** CD submittal set (all disciplines)

**Verification:** Internal QA/QC complete; code review sign-off; coordination clash count zero or documented exceptions; addenda checklist 100% confirmed; Design Manager sign-off; cost estimate final (±5% accuracy target)

*Source: Specification RQ-01 (completeness), RQ-03 (QA/QC), RQ-08 (addenda integration), Guidance P-01 (completeness before issuance), Guidance P-04 (multi-layered QA/QC)*

---

#### Step B-10: Submit CD to Owner for Review
**Action:** Assemble CD submittal per plan procedures. Submit to Owner with transmittal and review period notice.

**Responsible:** Design Manager / Project Manager

**Output:** CD submittal transmitted to Owner

**Verification:** Owner confirms receipt

*Source: Specification RQ-05, Guidance Example 3*

---

#### Step B-11: Incorporate Owner CD Comments and Finalize for Permit
**Action:** Receive Owner CD comment log. Prepare response matrix. Incorporate accepted comments. Finalize CD set with professional seals/stamps as required by Alberta regulations.

**Responsible:** Design Manager with discipline leads; registered professionals (seal/stamp)

**Output:** Final CD set with Owner acceptance and professional seals

**Verification:** Owner acceptance letter received; all sheets sealed/stamped as required

*Source: Specification RQ-07 (code compliance: sealed drawings), Guidance Example 3 (Owner acceptance signoff)*

---

#### Step B-12: Submit for Building Permit
**Action:** Prepare permit application package (drawings, specifications, supporting documents per AHJ requirements). Submit to authority having jurisdiction (AHJ). Track permit review process.

**Responsible:** Design Manager / Project Manager

**Output:** Permit application submitted

**Verification:** AHJ confirms receipt and assigns permit review timeline

*Source: Specification RQ-07 (permitting alignment), Guidance considerations (permit coordination with AHJ)*

---

#### Step B-13: Incorporate Permit Review Comments
**Action:** Receive permit review comments from AHJ. Address comments (revisions, clarifications, additional documentation). Resubmit for permit approval.

**Responsible:** Design Manager with discipline leads

**Output:** Permit resubmittal package

**Verification:** Permit approved by AHJ

*Source: Guidance considerations (permit comment incorporation)*

---

#### Step B-14: Issue for Construction (IFC)
**Action:** Incorporate all permit comments and any final Owner-approved changes into the IFC set. Conduct final QA/QC review. Distribute IFC set to all stakeholders per plan distribution protocols (Owner, Design-Build team, subtrades per Appendix I, AHJ). Mark all sheets "Issued for Construction" with date and revision number.

**Responsible:** Design Manager / Document Controller

**Output:** IFC set distributed

**Verification:** Distribution log confirms all recipients received IFC set; no outstanding coordination issues; permit approved and on file

*Source: Specification RQ-10 (issuance protocols), Guidance P-01 (completeness before issuance), Guidance P-05 (document control)*

---

#### Step B-15: Maintain IFC Set During Construction
**Action:** Track field RFIs (requests for information) and required design changes. Issue addenda/bulletins as needed. Maintain IFC revision log. Provide updated drawings to field as changes are approved.

**Responsible:** Design Manager / Document Controller / Project Manager

**Output:** IFC addenda and updated drawings as needed

**Verification:** All changes logged and distributed per document control protocols; field confirms receipt

*Source: Specification RQ-04 (document control: revision tracking, distribution)*

---

#### Step B-16: Support As-Built Markup and Closeout
**Action:** Coordinate with field team to collect as-built markups (field changes, final conditions). Incorporate markups into record drawings. Issue final "Issued for Record" set per closeout procedures (see DEL-06-01 for full closeout process).

**Responsible:** Design Manager / Document Controller

**Output:** Record drawings (as-builts) issued to Owner

**Verification:** Owner accepts record drawings as part of project closeout

*Source: Guidance considerations (as-built documentation requirements), decomposition Section 8 (DEL-06-01 covers closeout)*

---

#### Step B-17: Post-Project Process Retrospective (OPTIONAL — Scope Question)

> **[SL:A-005 / SL:D-004]** Question: Should post-project process retrospection (lessons learned, process effectiveness review) be included as a post-project step for DEL-03-02? This step supports process maturity and future project replication but may be considered a project management function outside this deliverable's scope. *(SourcePath: Procedure.md § Part B / Records section)*

**If in scope:**
**Action:** Conduct post-project retrospective to evaluate effectiveness of the design documentation plan. Document lessons learned, process improvements, and recommendations for future projects.

**Responsible:** Design Manager / Project Manager

**Output:** Design Documentation Process Retrospective Report

**Content:**
- What worked well in the documentation process
- What challenges were encountered (delays, coordination issues, rework)
- How effectively were QA/QC checkpoints implemented
- Were Owner review periods adequate
- Were addenda requirements fully addressed
- Recommendations for process improvements on future projects

**Timing:** Within 30 days of substantial completion

**If out of scope:**
This step is deferred to broader project management protocols (project closeout lessons learned) rather than being part of DEL-03-02 specifically.

**TBD:** Human ruling required to determine whether Step B-17 is in scope for DEL-03-02 or deferred to project management.

---

## Verification

### Verification for Production Workflow (Proposal Phase)

| Step | Verification Checkpoint | Acceptance Criteria |
|------|-------------------------|---------------------|
| A-01 | RFP requirements captured | All RFP Section 7.1.8 requirements listed in notes |
| A-02 | Discipline scopes complete | All disciplines and all Addendum 03 items assigned |
| A-03 | QA/QC checkpoints defined | Minimum: self-check, Design Manager, code review, constructability, Owner |
| A-04 | Coordination process described | Continuous coordination (weekly meetings, BIM/overlays) specified |
| A-05 | Document control protocols established | Numbering, revision, distribution, retention all addressed |
| A-06 | Owner review process defined | Submittal format, review period, comment log, approval signoff |
| A-07 | Code compliance strategy included | Code checkpoints and permit process described |
| A-08 | Addenda traceability confirmed | All Addendum 03 items traceable to disciplines and QA/QC |
| A-09 | Schedule alignment verified | Milestones consistent with DEL-08-01 |
| A-10 | Plan document reviewed | Internal review complete; no conflicts with other deliverables |
| A-11 | Incorporated into proposal | DEL-03-02 in correct RFP section; proposal <15 MB |

---

### Verification for Operational Workflow (Post-Award Design Phase)

> **[SL:X-001]** Verification table expanded with "Evidence Format" column specifying the artifact that proves each checkpoint is satisfied. *(SourcePath: Procedure.md § Verification table / Part B)*

| Step | Verification Checkpoint | Acceptance Criteria | Evidence Format |
|------|-------------------------|---------------------|-----------------|
| B-01 | Design team mobilized | Kick-off meeting complete; all disciplines acknowledge plan | Kick-off meeting minutes with sign-in sheet; Mobilization Gate Checklist (signed by Design Manager) |
| B-02 | Tools operational | DMS and BIM platform functional; all team members have access | DMS access test log; BIM platform test report; access roster confirmation |
| B-03 | SD complete | SD QA/QC checklist complete; Design Manager sign-off | Signed QA/QC checklist (dated); Design Manager review memo with signature |
| B-04 | SD submitted to Owner | Owner confirms receipt | Transmittal letter (copy); Owner receipt confirmation (email/letter) |
| B-05 | SD accepted by Owner | Owner acceptance letter received; authorized to proceed to DD | Owner acceptance letter (dated, signed by Owner's Representative) |
| B-06 | DD complete | DD QA/QC checklist complete; constructability review done; Design Manager sign-off; cost aligned with budget | Signed QA/QC checklist; constructability review memo (CM signed); cost estimate reconciliation |
| B-07 | DD submitted to Owner | Owner confirms receipt | Transmittal letter; Owner receipt confirmation |
| B-08 | DD accepted by Owner | Owner acceptance letter received; authorized to proceed to CD | Owner acceptance letter |
| B-09 | CD complete | CD QA/QC complete; code review sign-off; addenda checklist 100%; Design Manager sign-off | QA/QC checklist; code review report (signed); addenda checklist (all items checked); Design Manager memo |
| B-10 | CD submitted to Owner | Owner confirms receipt | Transmittal letter; Owner receipt confirmation |
| B-11 | CD accepted and sealed | Owner acceptance letter; all sheets sealed by registered professionals | Owner acceptance letter; sealed drawing cover sheet (copy with seals visible) |
| B-12 | Permit application submitted | AHJ confirms receipt | Permit application receipt/acknowledgment from AHJ |
| B-13 | Permit approved | AHJ issues building permit | Building permit document (copy) |
| B-14 | IFC distributed | Distribution log confirms all recipients received IFC set; permit on file | IFC distribution log (signed receipts or email confirmations); permit on file confirmation |
| B-15 | IFC revisions controlled | All changes logged and distributed per document control protocols | Revision log (dated entries); distribution confirmations for each revision |
| B-16 | Record drawings issued | Owner accepts as-builts as part of closeout | Record drawing transmittal; Owner acceptance letter for closeout |

---

## Records

### Records Generated by Production Workflow (Proposal Phase)

> **[SL:E-002]** Records section expanded to include working/audit artifacts created during proposal drafting for exhaustive production documentation and traceability. *(SourcePath: Procedure.md § Records / Part A section)*

**Output Artifacts:**
- **Discipline scope matrix** (by phase)
- **QA/QC checkpoint table** (by phase and layer)
- **Coordination process description**
- **Document control protocol description**
- **Owner review process description**
- **Addenda integration checklist**
- **Milestone alignment table/narrative** (coordination with DEL-08-01)
- **DEL-03-02 Detailed Design and Construction Docs Plan** (final document for proposal submission)

**Working/Audit Artifacts (recommended for retention):**
- **Draft iterations with review comments:** Preserve intermediate drafts showing internal review feedback and revisions
- **Internal decision log:** Document key decisions made during plan drafting (e.g., design phase sequencing choices, tool selections, QA/QC layer definitions)
- **Assumption register:** List of flagged TBD items and rationale for assumptions made during proposal drafting (supports later enrichment and updates)

*Storage location:* Proposal assembly folder (per decomposition Section 16: artifact folder layout); final proposal PDF (PKG-01: DEL-01-02); working artifacts in 1_Working/DEL-03-02 folder

---

### Records Generated by Operational Workflow (Post-Award Design Phase)
- **Kick-off meeting minutes** (with discipline acknowledgments)
- **Coordination meeting minutes** (weekly throughout design phases)
- **BIM clash detection reports** (if BIM approach used)
- **QA/QC checklists** (completed at each phase and layer)
- **Design submittal packages** (SD, DD, CD sets)
- **Owner comment logs and response matrices** (for each phase)
- **Code review reports** (third-party or internal)
- **Constructability review reports** (Construction Manager input)
- **Owner acceptance letters** (SD, DD, CD approvals)
- **Permit application package** (drawings, specs, supporting docs)
- **Permit approval letter** (from AHJ)
- **IFC distribution log** (who received what, when)
- **IFC revision log** (addenda/bulletins during construction)
- **As-built markups and record drawings** (final closeout deliverable)

*Storage location:* Project document management system (DMS); archived per retention requirements (TBD: typically 10 years post-substantial completion — ASSUMPTION)

---

**Document Status:** DRAFT (Semantic Lensing Pass 3 complete — enrichment items incorporated)

**Semantic Lensing Items Incorporated:** A-004 (decision authority and escalation), A-005 (post-project retrospective question), C-003 (mobilization risk contingencies), D-002 (output acceptance criteria), D-004 (post-project review question), E-001 (mobilization gate requirement), E-002 (working/audit artifacts), F-002 (Part A prerequisites), X-001 (evidence format column), X-002 (coordination meeting protocol)

**TBD Items for resolution:**
- Specific RFP Section 7.1.8 requirements (will refine steps A-01 through A-08)
- Owner review period durations (will refine steps A-06, B-04, B-07, B-10)
- Third-party code review requirement confirmation (will refine step A-07 and B-09)
- Software platform selections for DMS and BIM (will refine step B-02)
- Retention period requirements (will refine Records section)
- **Landscape discipline scope confirmation (CONFLICT: will refine step A-02 and B-03/06/09)**
- Post-award phasing (whether SD phase occurs post-award or only DD/CD; proposal assumes SD = conceptual design from proposal)
- **Step B-17 scope (post-project retrospective): include in DEL-03-02 or defer to project management?**

**Assumptions flagged:**
- Standard Design-Build mobilization and phasing (SD, DD, CD, IFC)
- Typical QA/QC checkpoint structure with evidence standards
- Typical Owner review periods (2-3 weeks per milestone)
- BIM coordination workflow (if BIM approach is proposed)
- Third-party code review at CD phase
- Permit review timeline (4-8 weeks)
- Retention period (10 years post-substantial completion)
- Design team composition per Appendix I
- Mobilization gate requirement before design start
- Coordination meeting protocol (weekly minimum)
