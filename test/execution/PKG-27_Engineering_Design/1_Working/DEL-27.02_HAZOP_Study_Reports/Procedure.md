# Procedure: DEL-27.02 HAZOP Study Reports

## Purpose

This procedure defines the process for conducting and documenting **HAZOP Study Reports** within **PKG-27 Engineering Design**.

**Scope:** Documents analysis and results for HAZOP study reports required for design verification and approvals (per _CONTEXT.md).

**Deliverable type:** Report (HAZOP Study Reports)

**Responsible party:** D&B Contractor

**Downstream use:** HAZOP findings inform detailed engineering design across all disciplines (PKG-01 through PKG-26, PKG-29 through PKG-36). HAZOP recommendations drive safeguard design (SIS, interlocks, alarms in PKG-19), hazardous area electrical classification (PKG-17), fire protection (PKG-23, PKG-24), containment (PKG-03), and operating procedures. HAZOP supports regulatory compliance (OBJ-6), safe and reliable operation (OBJ-1), and environmental protection (OBJ-7).

**Source:** _CONTEXT.md; Decomposition DEL-27.02; Specification.md

## Prerequisites

### Dependencies

**Dependency coordination:**
- Per `_DEPENDENCIES.md`: **NOT_TRACKED** — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Key upstream dependencies (coordination required):**
- DEL-27.01 (Design Basis Documents) — Design basis, operating philosophy, process description must be established before HAZOP can proceed
- P&IDs (Piping and Instrumentation Diagrams) — Must be available at appropriate maturity level for HAZOP stage (preliminary P&IDs for Preliminary HAZOP; near-final P&IDs for Detailed HAZOP)
- PFDs (Process Flow Diagrams) — **TBD** — If available, support HAZOP understanding of process
- Equipment datasheets — Sizes, capacities, materials, operating conditions
- Instrument lists and control philosophy — Alarms, interlocks, control loops
- Hazardous material data — Product properties (canola oil SDS, flash point, vapor pressure, etc.)
- Site and environmental data — Layout, environmental conditions, existing facilities
- **TBD** — Specific upstream deliverables and maturity requirements per HAZOP stage

**Key parallel dependencies (coordination during HAZOP):**
- All discipline engineering teams — Must participate in HAZOP and respond to recommendations
- DEL-27.04 (Design Submission Packages) — HAZOP timing aligned with submission milestones
- PKG-19 (Control Systems) — SIS and interlock design informed by HAZOP
- PKG-17 (Electrical) — Hazardous area classification informs electrical design
- **TBD** — Additional coordination per project organization

**Source:** _DEPENDENCIES.md; Specification.md (FR-3, Interface Requirements); Datasheet.md; **ASSUMPTION**: Typical HAZOP dependencies for Design & Build project

### Reference Materials

**Required reference materials:**

Per `_REFERENCES.md`, Datasheet.md, and Specification.md:
- DEL-27.01: Design Basis Documents (Design Basis Memorandum, Design Criteria)
- P&IDs for all major systems (railcar unloading, storage tanks, transfer piping, marine loading, pumps, valves, electrical, controls) — **TBD** — Maturity level depends on HAZOP stage
- PFDs (if available) — **TBD**
- Equipment datasheets (tanks, pumps, valves, loading arms, etc.) — **TBD**
- Instrument lists and control narratives — **TBD**
- Canola oil Safety Data Sheet (SDS) and product properties — **location TBD**
- Site layout drawings and plot plans — **TBD**
- Employer's Requirements Volume 2 (all parts) — **location TBD**
- Applicable HAZOP standards and guidelines:
  - IEC 61882: Hazard and operability studies (HAZOP studies) — Application guide — **location TBD**
  - CCPS Guidelines for Hazard Evaluation Procedures — **location TBD**
- Applicable hazardous area classification standards:
  - Canadian Electrical Code (CEC) Part I, Section 18 — **location TBD**
  - API RP 505 — **location TBD**
  - IEC 60079 series — **location TBD**
- Project Quality Management Plan and procedures — **location TBD**
- **TBD** — Additional references as needed during HAZOP

**Source:** _REFERENCES.md; Datasheet.md; Specification.md

### Personnel Requirements

**HAZOP Team Composition:**

Per Specification.md (FR-2) and industry best practice (IEC 61882):

1. **HAZOP Facilitator/Leader**
   - Qualifications: Experienced in HAZOP methodology (IEC 61882 or equivalent); facilitator training preferred; P.Eng. or equivalent; prior HAZOPs on similar facilities
   - Role: Leads HAZOP sessions; ensures methodology rigor; manages team discussions; guides guideword application; documents decisions
   - Independence: Should be independent of primary design (not lead designer); avoids bias

2. **HAZOP Scribe**
   - Qualifications: Technical background; able to document discussions accurately and rapidly; familiarity with HAZOP worksheets
   - Role: Records HAZOP discussions, deviations, causes, consequences, safeguards, recommendations in real-time; maintains action item register

3. **Process/Mechanical Engineer (Design Lead)**
   - Qualifications: P.Eng.; responsible for process design, P&IDs, equipment specifications
   - Role: Explains design intent; answers technical questions; evaluates consequences; proposes safeguards

4. **Electrical Engineer**
   - Qualifications: P.Eng.; responsible for electrical design (PKG-17)
   - Role: Addresses electrical hazards, hazardous area classification, motor/equipment failures

5. **Controls/Instrumentation Engineer**
   - Qualifications: P.Eng. or P.Tech; responsible for control system design (PKG-19)
   - Role: Addresses instrumentation failures, control logic, interlocks, alarms, SIS

6. **Safety Engineer/Specialist**
   - Qualifications: Safety engineering background; process safety or industrial safety experience
   - Role: Assesses safety consequences; proposes safety safeguards; ensures safety standards applied

7. **Operations Representative**
   - Qualifications: Operations experience in similar facilities (canola oil, liquid bulk, marine terminals, etc.); understanding of operating procedures
   - Role: Provides operability perspective; identifies practical operating issues; validates safeguards and procedures

8. **Maintenance Representative (optional but recommended)**
   - Qualifications: Maintenance experience in similar facilities
   - Role: Identifies maintenance-related hazards and operability issues; validates maintainability of safeguards

9. **Other Specialists as Needed:**
   - Civil/Structural Engineer (for tank foundation, containment, structural scenarios)
   - Fire Protection Engineer (for fire scenarios)
   - Environmental Specialist (for environmental release scenarios, spill response)
   - Employer Representative (optional but recommended for Design & Build; provides owner's perspective and approval authority)

**Team size:** Typically 6-10 people; larger teams become unwieldy; smaller teams may lack expertise

**Team availability:** HAZOP sessions require sustained participation; team members must commit to full session schedule (typically several days to weeks depending on scope)

**TBD** — Specific personnel assignments, qualifications matrix, independence verification per project

**Source:** Specification.md (FR-2); **ASSUMPTION**: Standard HAZOP team composition per IEC 61882 and industry practice

### Tools and Resources

**Software and tools:**
- HAZOP worksheet templates (Excel or specialized HAZOP software) — **TBD** — Project template or software selection
- P&ID viewing software (PDF viewer, CAD viewer, or engineering document management system)
- Projector or large screen for displaying P&IDs to HAZOP team
- Whiteboard or flipchart for capturing discussions
- Audio/video conferencing tools if remote participation required (not ideal; in-person preferred)

**Workspace:**
- Meeting room large enough for HAZOP team (8-12 people)
- Table configuration allowing all participants to see screen/P&IDs
- Adequate duration: HAZOP sessions typically 3-4 hours per day; avoid longer sessions (team fatigue reduces effectiveness)
- Schedule: Multiple consecutive days or weekly sessions depending on project schedule and team availability

**Reference materials access:**
- Electronic access to all reference documents (P&IDs, datasheets, design basis, standards)
- Physical or electronic copies of IEC 61882, guideword lists, risk matrix

**Source:** **ASSUMPTION**: Standard HAZOP facilitation tools and workspace requirements

## Steps

### Step 1: HAZOP Planning and Preparation

**1.1 Define HAZOP Scope and Objectives**
- Identify HAZOP stage: Preliminary (30-60% design) or Detailed (90% design) or Pre-commissioning review
- Define systems in scope per Datasheet.md: Railcar Unloading, Storage Tanks, Transfer Piping, Marine Loading, Pumps, Valves, Electrical, Controls, Safety Systems
- Define HAZOP objectives: hazard identification, operability assessment, hazardous area classification, recommendation generation
- **TBD** — Any specific Employer or regulatory requirements for HAZOP scope and objectives

**Outputs:**
- HAZOP scope statement documenting systems in scope, HAZOP stage, objectives
- HAZOP schedule and milestones aligned with design submission schedule (DEL-27.04)

**Verification:** Project Engineering Manager approves HAZOP scope and schedule

**Source:** Datasheet.md; Specification.md (FR-1); **ASSUMPTION**: Scoping aligned with project design maturity and submission stages

**1.2 Assemble HAZOP Team**
- Identify and assign HAZOP team members per Personnel Requirements (Prerequisites section)
- Confirm qualifications and availability
- Designate HAZOP facilitator/leader and scribe
- Notify team members of HAZOP schedule, scope, roles, responsibilities
- Provide pre-read materials: design basis (DEL-27.01), P&IDs, HAZOP methodology (IEC 61882), project-specific HAZOP procedure (if available)

**Outputs:**
- HAZOP team roster with names, roles, qualifications
- HAZOP schedule with session dates/times and team availability confirmed

**Verification:** All team members confirm participation and availability; Project Manager approves team composition

**Source:** Specification.md (FR-2); **ASSUMPTION**: Standard HAZOP team mobilization

**1.3 Prepare HAZOP Materials**
- Gather latest P&IDs for all systems in scope (verify revision/date; ensure P&IDs are approved and current)
- Mark up P&IDs with proposed HAZOP node boundaries (nodes = sections of process with similar conditions, analyzed separately)
- Prepare HAZOP worksheet templates with columns: Node, Guideword, Parameter, Deviation, Causes, Consequences, Safeguards, Risk Ranking, Recommendations, Action Items
- Prepare supporting documents: equipment datasheets, instrument lists, control narratives, design basis excerpts, product SDS
- Define risk ranking criteria (likelihood × consequence matrix; see Guidance.md Example for typical matrix structure) — **TBD** — Project-specific risk criteria
- **TBD** — Specific template and risk matrix from Employer or project procedures

**Outputs:**
- P&IDs with node boundaries marked (draft, to be finalized during HAZOP)
- HAZOP worksheet templates ready for use
- Risk ranking matrix defined and documented
- Supporting documents compiled and accessible

**Verification:** HAZOP facilitator reviews materials for completeness; identifies any gaps (TBD items to be resolved before HAZOP sessions)

**Source:** Specification.md (FR-1, FR-3, FR-5); **ASSUMPTION**: Standard HAZOP preparation per IEC 61882

**1.4 Conduct HAZOP Kickoff Meeting**
- Hold kickoff meeting with full HAZOP team before first working session
- Review HAZOP objectives, scope, schedule
- Review HAZOP methodology (IEC 61882): guidewords, parameters, deviation analysis, cause-consequence-safeguard structure
- Review risk ranking criteria and acceptance thresholds
- Review roles and responsibilities
- Walk through example HAZOP node (training/calibration exercise)
- Address team questions; clarify any ambiguities
- Finalize HAZOP node boundaries on P&IDs

**Kickoff agenda (typical):**
1. Introductions and team roles
2. Project overview and design basis review (30 min)
3. HAZOP methodology overview (30 min)
4. Risk ranking criteria and examples (15 min)
5. Node boundary review and finalization (30 min)
6. Example node walk-through (30 min)
7. Logistics, schedule, housekeeping (15 min)
8. Q&A

**Outputs:**
- HAZOP kickoff meeting minutes
- Finalized HAZOP node boundaries on P&IDs
- Team calibrated and ready for working sessions

**Verification:** All team members understand methodology and are ready to proceed

**Source:** **ASSUMPTION**: HAZOP kickoff meeting best practice for team alignment

### Step 2: Conduct HAZOP Study Sessions

**2.1 Execute HAZOP Node-by-Node Analysis**

For each HAZOP node (systematic process per IEC 61882):

**A. Introduce Node:**
- Facilitator describes node: boundaries, equipment included, process function, design intent
- Review relevant P&ID section (display on screen for team to view)
- Identify process parameters for this node: Flow, Pressure, Temperature, Level, Composition, Viscosity, Time, etc.
- **TBD** — Parameters depend on node type (typical liquid transfer node: Flow, Pressure, Temperature most relevant)

**B. Apply Guidewords Systematically:**
- For each parameter, apply guidewords to generate deviations:
  - **More** (e.g., More Flow, More Pressure, More Temperature)
  - **Less** (e.g., Less Flow, Less Pressure, Less Temperature)
  - **No** (e.g., No Flow, No Pressure, No Level signal)
  - **Reverse** (e.g., Reverse Flow)
  - **As Well As** (e.g., Contaminant as well as canola oil)
  - **Part Of** (e.g., Part of composition changed)
  - **Other Than** (e.g., Other fluid than canola oil)
  - **Early/Late** (e.g., Operation starts early, shuts down late)
  - **More/Less Time** (e.g., Longer or shorter than intended duration)
- Not all guideword-parameter combinations are credible; facilitator guides team to focus on meaningful deviations

**C. Analyze Each Credible Deviation:**
- **Deviation:** State the deviation clearly (e.g., "No flow of canola oil from pump P-101 to tank T-101 when pump is running")
- **Causes:** Brainstorm all credible causes (equipment failure, human error, instrument failure, external event, etc.)
  - Team discusses: "What could cause this deviation?"
  - Record all plausible causes
- **Consequences:** Identify consequences for each cause (or for deviation in general if consequences are similar across causes)
  - Team discusses: "What happens if this deviation occurs?"
  - Assess safety consequences (injury, fire, explosion, release), environmental consequences (spill, emission), equipment consequences (damage), operational consequences (downtime, off-spec product)
- **Existing Safeguards:** Identify safeguards already in design that prevent or mitigate this deviation
  - Preventive safeguards: Prevent deviation from occurring (e.g., interlock prevents wrong valve lineup)
  - Detective safeguards: Detect deviation (e.g., alarm alerts operator)
  - Mitigative safeguards: Reduce consequences if deviation occurs (e.g., relief valve prevents overpressure, containment prevents environmental release)
  - Record all relevant safeguards from P&IDs, design basis, procedures
- **Risk Ranking:** Assess residual risk (likelihood × consequence) considering existing safeguards
  - Use defined risk matrix from Step 1.3
  - Team discusses and reaches consensus on risk ranking
  - Likelihood: Rare, Unlikely, Possible, Likely, Almost Certain (or similar scale)
  - Consequence: Negligible, Minor, Moderate, Major, Catastrophic (or similar scale)
  - Risk = Likelihood × Consequence → Low, Medium, High (or color-coded: Green, Yellow, Red)
- **Recommendations:** If risk is unacceptable (High) or borderline (Medium), generate recommendations to reduce risk
  - Recommendations should be specific and actionable: "Add PAHH-101 interlock to shut down pump on high discharge pressure (SIL TBD)" NOT "Improve safety"
  - Assign responsibility (discipline lead or individual) and target date
  - Record as Action Item in action item register
  - If risk is acceptable (Low) with existing safeguards, no recommendation required; record "Risk acceptable, no action"

**D. Document in HAZOP Worksheet:**
- Scribe records all discussions in HAZOP worksheet in real-time
- Ensure all columns filled: Node, Guideword, Parameter, Deviation, Causes, Consequences, Safeguards, Risk Ranking, Recommendations
- Facilitator reviews worksheet entries for accuracy and completeness at end of each deviation

**E. Repeat for All Guidewords and Parameters:**
- Systematically work through all guideword-parameter combinations for the node
- Facilitator ensures completeness (all credible deviations addressed) and efficiency (avoid excessive discussion of low-value scenarios)

**F. Move to Next Node:**
- After completing all deviations for current node, move to next node
- Repeat process until all nodes in scope are analyzed

**Session Management:**
- HAZOP sessions typically 3-4 hours per day (morning or afternoon); longer sessions result in team fatigue and reduced effectiveness
- Schedule breaks every 60-90 minutes
- Facilitator manages time and keeps discussions focused; escalates complex issues for offline resolution if needed
- Scribe circulates draft worksheets to team after each session for review and corrections

**Outputs:**
- Completed HAZOP worksheets for all nodes (deviations, causes, consequences, safeguards, risk rankings, recommendations documented)
- Action item register populated with all recommendations

**Verification:** HAZOP facilitator and team leader review worksheets for completeness and accuracy after each session; team members concur

**Source:** Specification.md (FR-1); **ASSUMPTION**: Standard HAZOP node analysis process per IEC 61882; see Guidance.md Examples for scenario illustrations

**2.2 Hazardous Area Classification Analysis (Parallel Activity)**

During or after HAZOP sessions, conduct hazardous area classification analysis based on HAZOP-identified release scenarios:

**A. Identify Sources of Release:**
- Review HAZOP worksheets for all "Loss of Containment" scenarios (leaks, ruptures, spills, overflows)
- Identify specific locations: flanges, valve packing, pump seals, loading arm connections, tank vents, relief valve discharge, etc.
- For each source, characterize: release type (gas, vapor, liquid, mist), release rate (continuous, frequent, infrequent), release duration, product properties (flash point, vapor pressure, vapor density)

**B. Classify Zones per CEC/API RP 505/IEC 60079:**
- For each source of release, determine zone classification:
  - **Zone 0:** Hazardous atmosphere present continuously or for long periods (e.g., inside tank vapor space)
  - **Zone 1:** Hazardous atmosphere likely to occur in normal operation (e.g., near pump seal during operation, near loading arm during connection/disconnection)
  - **Zone 2:** Hazardous atmosphere not likely in normal operation; only under abnormal conditions (e.g., near piping flanges, valve packing)
  - **Non-classified:** No credible scenario for hazardous atmosphere
- Determine extent of classified zone (distance from source) based on:
  - Release rate and duration
  - Ventilation (natural or mechanical; indoor or outdoor)
  - Vapor density (heavier or lighter than air; affects dispersion)
  - Use dispersion modeling or empirical rules per API RP 505 / IEC 60079 guidance
  - **TBD** — Detailed classification calculations or modeling approach

**C. Document Hazardous Area Classification:**
- Prepare hazardous area classification drawings showing Zone 0, 1, 2 boundaries in plan and elevation views
- Prepare hazardous area classification report documenting methodology, assumptions, source analysis, zone determinations
- Include as section in HAZOP Study Report or as standalone appendix

**Outputs:**
- Hazardous area classification drawings (plan and elevation views)
- Hazardous area classification report or section in HAZOP report
- Source of release register

**Verification:** Electrical engineer (PKG-17 lead) reviews and concurs with hazardous area classification; classification used for electrical equipment selection

**Source:** Specification.md (FR-4); Datasheet.md; **ASSUMPTION**: Hazardous area classification per CEC, API RP 505, IEC 60079

### Step 3: HAZOP Report Preparation

**3.1 Compile HAZOP Study Report**

Prepare comprehensive HAZOP Study Report per structure in Datasheet.md:

**Report Sections (typical structure):**

1. **Executive Summary**
   - HAZOP objectives and scope
   - Key findings: number of deviations analyzed, high-risk scenarios identified, major recommendations
   - Hazardous area classification summary
   - Overall conclusions and path forward

2. **Introduction**
   - Project overview (canola oil transload facility, location, capacity, design basis reference)
   - HAZOP objectives
   - HAZOP methodology (IEC 61882) with guideword definitions

3. **Study Organization**
   - HAZOP team composition, roles, qualifications (include CV summaries or qualification statements in appendix)
   - HAZOP schedule: session dates, duration, attendance
   - Node definitions and boundaries (include marked-up P&IDs in appendix)

4. **Design Basis Review**
   - Summary of process description, operating philosophy, design intent (reference DEL-27.01)
   - Summary of P&IDs reviewed (list with revision dates)
   - Key design parameters: throughput, storage capacity, operating conditions, product properties
   - Assumptions and limitations

5. **HAZOP Worksheets**
   - Completed HAZOP worksheets for all nodes (typically in appendix due to length)
   - Summary tables in main body highlighting high-risk scenarios and key recommendations

6. **Hazardous Area Classification**
   - Methodology and standards (CEC, API RP 505, IEC 60079)
   - Source of release identification and characterization
   - Zone classification determinations (Zone 0, 1, 2)
   - Hazardous area classification drawings (include in appendix)

7. **Recommendations Summary**
   - Table of all HAZOP recommendations with: ID, recommendation description, system, risk ranking (before and after recommendation), responsible party, target date, priority
   - Cross-reference to HAZOP worksheet node/deviation
   - Categorize by priority: High (must implement for safety/regulatory compliance), Medium (should implement for risk reduction or operability), Low (nice to have, optional)

8. **Action Item Tracking**
   - Action item register: ID, description, assigned to, target date, status, closure evidence
   - Process for tracking and closing action items through design, construction, commissioning
   - Follow-up HAZOP review plan to verify closure before startup

9. **Conclusions**
   - Overall risk assessment: facility design is acceptable with implementation of HAZOP recommendations
   - Major findings and themes (e.g., overfill protection, SIS requirements, hazardous area classification, procedural controls)
   - Path forward: recommendation implementation, follow-up HAZOP review schedule

10. **Appendices**
    - A: HAZOP team qualifications
    - B: P&IDs with HAZOP node boundaries marked
    - C: HAZOP worksheets (full detail for all nodes)
    - D: Hazardous area classification drawings
    - E: Guideword definitions
    - F: Risk ranking matrix
    - G: Reference documents list
    - **TBD** — Additional appendices as needed

**Report Preparation Process:**
- HAZOP facilitator or designated engineer compiles report from workshop materials
- Scribe's HAZOP worksheets form core of report content
- Add narrative sections (introduction, design basis review, conclusions) for context and readability
- Format report per project document standards — **TBD**
- Generate PDF and native format (Word or equivalent)

**Outputs:**
- HAZOP Study Report (Draft 1 for internal review)

**Verification:** HAZOP facilitator reviews draft report for completeness, accuracy, and clarity

**Source:** Datasheet.md; Specification.md; **ASSUMPTION**: Standard HAZOP report structure per IEC 61882 and industry practice

**3.2 Internal Review of HAZOP Report**
- Distribute draft HAZOP report to HAZOP team members and discipline leads for review
- Review focuses on:
  - Technical accuracy (deviations, causes, consequences correctly characterized)
  - Completeness (all credible scenarios addressed)
  - Recommendations feasibility and appropriateness
  - Hazardous area classification reasonableness
  - Report clarity and usability

**Review checklist (minimum items):**
- All nodes in scope analyzed
- All guidewords systematically applied
- Risk rankings consistent with defined criteria
- Recommendations are specific and actionable
- Action items assigned with responsibility and target dates
- Hazardous area classification complete and documented
- Report structure complete per Datasheet.md template
- All TBDs and assumptions clearly flagged

**Outputs:**
- Review comments from HAZOP team and discipline leads
- Comment resolution log

**Verification:** HAZOP facilitator addresses all review comments; reviewers concur with resolutions

**Source:** Specification.md (QR-2, QR-3); **ASSUMPTION**: Standard engineering review per ISO 9001

**3.3 Revise HAZOP Report and Finalize**
- Incorporate review comments into HAZOP report
- Update action item register with any new or revised recommendations
- Perform final quality check: formatting, cross-references, appendices, page numbering, table of contents
- Generate final PDF for submission

**Outputs:**
- HAZOP Study Report (Final for submission to Employer)
- Action Item Register (living document for tracking)

**Verification:** HAZOP facilitator and Project Engineering Manager review and approve final report

**Source:** **ASSUMPTION**: Standard report finalization process

### Step 4: HAZOP Report Approval and Submission

**4.1 Internal Approval**
- Route final HAZOP report through internal approval workflow per project quality procedures
- Obtain required signatures:
  - HAZOP facilitator/leader (author)
  - HAZOP team leader or Project Engineering Manager (technical approval)
  - Project Quality Manager (quality approval)
  - **TBD** — Additional approvals per project approval matrix

**Outputs:**
- Internally approved HAZOP Study Report with signature page

**Verification:** All required signatures obtained; approval logged in document management system

**Source:** Specification.md (QR-3); **ASSUMPTION**: Internal approval per ISO 9001

**4.2 Submission to Employer**
- Submit approved HAZOP Study Report to Employer per DEL-27.04 (Design Submission Packages) requirements
- Include transmittal documenting HAZOP stage (Preliminary or Detailed), P&ID revisions analyzed, and any key notes
- Coordinate submission timing with design submission schedule (30-60% for Preliminary HAZOP; 90% for Detailed HAZOP)
- **TBD** — Specific submission procedures and Employer contact per project communication plan

**Outputs:**
- HAZOP Study Report submitted to Employer (in `2_Checking/To/` folder per deliverable lifecycle)
- Submission transmittal and acknowledgment

**Verification:** Project Manager confirms submission completed; submission logged in project tracking system

**Source:** Specification.md (VM-7); Datasheet.md; **ASSUMPTION**: Deliverable lifecycle per AGENTS.md

**4.3 Employer Review and Comment Resolution**
- Receive Employer review comments per Employer's review schedule
- Triage comments: editorial, technical clarifications, additional analysis requests, policy/contractual issues
- Develop comment responses; revise HAZOP report and/or action items as needed
- Submit comment response matrix and revised HAZOP report to Employer; iterate as needed

**Comment resolution process:**
- Assign comments to HAZOP facilitator or discipline leads for response
- Conduct internal coordination meeting to review responses and revisions
- Obtain HAZOP facilitator and Project Manager approval of responses
- Submit responses to Employer; resolve any disputed items through discussion or escalation

**Outputs:**
- Comment response matrix
- Revised HAZOP Study Report incorporating accepted comments

**Verification:** Employer concurs with comment responses; revised report accepted

**Source:** Specification.md (VM-7); **ASSUMPTION**: Standard design submission and review process

**4.4 Issuance**
- Upon Employer acceptance, issue final HAZOP Study Report for use in detailed engineering and action item implementation
- Update deliverable status to ISSUED in `_STATUS.md`
- Place issued report in `3_Issued/` folder per deliverable lifecycle
- Distribute issued report and action item register to all discipline engineering teams, operations, safety, and relevant stakeholders
- **TBD** — Distribution list and notification procedures

**Outputs:**
- Issued HAZOP Study Report and Action Item Register available for use
- Updated `_STATUS.md`: ISSUED with issuance date and notes
- Distribution confirmation

**Verification:** All stakeholders acknowledge receipt of issued HAZOP report

**Source:** **ASSUMPTION**: Deliverable issuance per AGENTS.md and README.md lifecycle model

### Step 5: HAZOP Action Item Implementation and Tracking

**5.1 Distribute Action Items to Responsible Parties**
- Distribute action item register to all assigned responsible parties (discipline leads, engineering teams, operations, etc.)
- Clarify action item requirements, priorities, target dates
- Establish tracking and reporting protocol: weekly or biweekly status updates; escalation for delays or issues

**Outputs:**
- Action item assignments distributed and acknowledged
- Tracking protocol established

**Verification:** All responsible parties acknowledge action items and commit to target dates

**Source:** Specification.md (FR-6); **ASSUMPTION**: Action item tracking process

**5.2 Implement HAZOP Recommendations**
- Responsible parties implement HAZOP recommendations in detailed engineering deliverables:
  - Design changes: Update P&IDs, equipment specs, datasheets, calculations
  - SIS design: Develop SIF specifications, SIL determinations, SIS logic (PKG-19)
  - Hazardous area classification: Select electrical equipment per classification (PKG-17)
  - Procedures: Develop or update operating procedures, maintenance procedures, emergency response procedures
  - Training: Incorporate HAZOP findings into operator and maintenance training
- Document implementation in respective deliverables
- Update action item register status as items are implemented

**Outputs:**
- Design deliverables updated with HAZOP recommendations
- Action item register status updated (Open → In Progress → Closed)

**Verification:** Discipline leads review and approve implementation; HAZOP facilitator or safety engineer reviews adequacy

**Source:** Specification.md (FR-6, IR-2); **ASSUMPTION**: Closed-loop recommendation implementation

**5.3 Verify Action Item Closure**
- For each completed action item, verify closure evidence:
  - Design changes: P&ID revision showing change, spec updated, calculation performed
  - SIS: SIF specification approved, SIS design documented
  - Procedures: Procedure issued and approved
  - Training: Training materials developed, training conducted (may be post-commissioning)
- HAZOP facilitator or designee reviews closure evidence and signs off
- Update action item register with closure evidence and sign-off

**Outputs:**
- Action item register updated with closure evidence and sign-off
- All High and Medium priority action items verified closed before commissioning

**Verification:** HAZOP facilitator or safety engineer signs off on action item closure; Project Manager monitors overall action item closure progress

**Source:** Specification.md (VM-5); **ASSUMPTION**: Action item closure verification before commissioning

### Step 6: Follow-Up HAZOP Review (Pre-Commissioning)

**6.1 Conduct Pre-Commissioning HAZOP Review**
- Timing: After detailed engineering substantially complete and before commissioning begins
- Purpose: Verify all HAZOP action items closed; review as-built P&IDs for any changes that affect HAZOP conclusions; identify any new hazards from as-built conditions

**Pre-Commissioning HAZOP Review Scope:**
- Review action item register: verify all High and Medium priority items closed with evidence
- Review as-built P&IDs: identify any changes from design P&IDs analyzed in Detailed HAZOP
- Assess impact of as-built changes: do changes introduce new hazards or invalidate HAZOP conclusions?
- Conduct targeted HAZOP analysis for any significant as-built changes
- Walk down facility (if accessible) to verify physical conditions match P&IDs and HAZOP assumptions

**HAZOP Team (subset of original team):**
- HAZOP facilitator or designated engineer
- Discipline leads (or representatives)
- Operations and maintenance representatives
- Safety engineer
- **TBD** — Team size and composition based on scope of as-built changes

**Outputs:**
- Pre-Commissioning HAZOP Review Report documenting action item closure verification, as-built review, and any new findings/recommendations
- Updated action item register if new items identified

**Verification:** All High and Medium priority action items verified closed; facility ready for commissioning from HAZOP perspective

**Source:** Specification.md (QR-4, VM-5); Datasheet.md; **ASSUMPTION**: Pre-commissioning HAZOP review before facility startup

**6.2 Resolve Any Outstanding Issues**
- If Pre-Commissioning HAZOP Review identifies unclosed action items or new hazards, resolve before commissioning proceeds
- Implement corrective actions; update action item register
- Obtain approval from HAZOP facilitator, Project Manager, and Employer before commissioning

**Outputs:**
- All action items resolved
- Approval to proceed with commissioning

**Verification:** HAZOP facilitator and Project Manager sign off that facility is safe to commission

**Source:** **ASSUMPTION**: HAZOP clearance required before commissioning

## Verification

### Verification Activities

**V-1: HAZOP Methodology Compliance Verification**
- Verify HAZOP methodology follows IEC 61882 or equivalent recognized standard
- Verify guidewords systematically applied to all nodes
- Verify all major systems in Datasheet.md scope are analyzed
- Verify HAZOP team composition and qualifications per Specification.md (FR-2)

**Acceptance criteria:**
- HAZOP methodology documented and compliant with IEC 61882
- All guidewords applied (or justification for omissions documented)
- All systems in scope covered by HAZOP nodes
- HAZOP team qualifications documented and adequate

**Source:** Specification.md (VM-1)

**V-2: HAZOP Technical Content Verification**
- Verify P&IDs and design basis used in HAZOP are current and correct revisions
- Verify deviations, causes, and consequences are technically sound
- Verify existing safeguards correctly identified
- Verify risk rankings consistent with defined risk matrix
- Verify recommendations are specific, actionable, technically feasible

**Acceptance criteria:**
- Reference documents are latest approved versions (documented in HAZOP report)
- Technical content reviewed by discipline leads and found accurate
- Risk rankings justified and consistent
- Recommendations clear and implementable

**Source:** Specification.md (VM-2)

**V-3: HAZOP Completeness Verification**
- Verify all nodes in scope analyzed
- Verify all credible deviations identified and documented
- Verify all high-risk scenarios have recommendations
- Verify HAZOP report includes all required sections per Datasheet.md structure

**Acceptance criteria:**
- No significant hazard scenarios omitted (based on review by experienced HAZOP practitioners)
- All high-risk and medium-risk scenarios addressed with recommendations or ALARP justification
- HAZOP report complete per template

**Source:** Specification.md (VM-3)

**V-4: Hazardous Area Classification Verification**
- Verify hazardous area classification methodology per CEC, API RP 505, IEC 60079
- Verify all potential release sources identified
- Verify zone classifications appropriate for release scenarios
- Verify hazardous area classification drawings complete

**Acceptance criteria:**
- Hazardous area classification methodology documented and compliant
- All release sources from HAZOP analysis included
- Hazardous area classification drawings approved by electrical engineer (PKG-17 lead)

**Source:** Specification.md (VM-4)

**V-5: Action Item Tracking Verification**
- Verify all HAZOP recommendations captured in action item register
- Verify action items assigned with responsibility and target dates
- Verify action item status tracked and current
- Verify completed action items have closure evidence

**Acceptance criteria:**
- All recommendations in action item register
- All High and Medium priority action items closed before commissioning (verified in Pre-Commissioning HAZOP Review)
- Action item register maintained and up-to-date

**Source:** Specification.md (VM-5)

**V-6: Independent Design Verification (IDV) (if applicable)**
- HAZOP study may undergo independent design verification per DEL-28.01
- IDV scope: HAZOP team qualifications, methodology rigor, technical content, recommendation adequacy
- IDV findings addressed and HAZOP report revised as needed
- **TBD** — Specific IDV requirements for HAZOP

**Source:** Specification.md (VM-6)

**V-7: Employer Approval**
- HAZOP report submitted to Employer at appropriate design stages (per DEL-27.04)
- Employer comments addressed satisfactorily
- Employer acceptance obtained before proceeding to next stage

**Acceptance criteria:**
- Employer approval issued for HAZOP report
- No outstanding Employer concerns

**Source:** Specification.md (VM-7)

### Sign-Off Requirements

**Internal Sign-Offs:**
- HAZOP facilitator/leader (technical originator)
- HAZOP team leader or Project Engineering Manager (overall technical approval)
- All discipline leads (discipline-specific concurrence with recommendations and action items)
- Project Safety Manager (safety compliance approval)
- Project Quality Manager (quality compliance approval)
- **TBD** — Additional internal sign-offs per project approval matrix

**External Sign-Offs:**
- Employer (approval of submitted HAZOP report at each stage)
- Independent design verifier (if IDV scope includes HAZOP review per DEL-28.01)
- **TBD** — Regulatory authority sign-offs if required

**Sign-off documentation:**
- Signature page in HAZOP Study Report
- Approval logs in document management system
- Transmittal acknowledgments for external approvals

**Source:** Specification.md; **ASSUMPTION**: Sign-off protocol per ISO 9001 and project-specific approval matrix

## Records

### Documentation Outputs

**Primary deliverable artifacts (per _CONTEXT.md):**
- **HAZOP Study Report** — Comprehensive documentation per Datasheet.md structure (Executive Summary, Introduction, Study Organization, Design Basis Review, HAZOP Worksheets, Hazardous Area Classification, Recommendations Summary, Action Item Tracking, Conclusions, Appendices)

**Supporting documentation:**
- HAZOP workshop attendance records and session notes
- P&IDs with HAZOP node boundaries marked
- HAZOP worksheets (detailed, typically in report appendix)
- Action item register (living document maintained throughout project)
- Hazardous area classification drawings
- HAZOP team qualifications documentation
- Risk ranking matrix
- Pre-Commissioning HAZOP Review Report
- Comment response matrices (internal review, Employer review, IDV review)
- Approval documentation and signature pages

**Source:** _CONTEXT.md; Datasheet.md; Specification.md

### Record Management

**Filing and storage:**
- **Working versions:** `1_Working/` folder in deliverable directory (DEL-27.02_HAZOP_Study_Reports/)
- **Review versions:** `2_Checking/To/` for submissions; `2_Checking/From/` for received comments
- **Issued versions:** `3_Issued/` folder with revision and date in filename
- Electronic copies in project document management system per project procedures — **TBD**
- Action item register maintained as shared file accessible to all responsible parties (e.g., SharePoint, project server)

**Retention requirements:**
- HAZOP Study Reports are critical safety documents; retain for facility lifecycle plus applicable regulatory retention period
- **TBD** — Specific retention requirements per project record retention schedule and regulatory requirements (WorkSafeBC, Environment Canada, etc.)

**Version control:**
- Use project document numbering system for HAZOP Study Reports — **TBD**
- Revision history documented in report header/footer and revision history page
- Previous revisions archived but accessible for traceability
- Action item register version-controlled; maintain history of changes

**Source:** Specification.md; **ASSUMPTION**: Document lifecycle per AGENTS.md and README.md; electronic records management per project DMS

### Traceability and Auditability

**Traceability provisions:**
- HAZOP worksheets link deviations to causes, consequences, safeguards, recommendations
- Action item register links recommendations to responsible parties, target dates, closure evidence
- Design deliverables reference HAZOP findings (e.g., P&ID notes "SIS per HAZOP Recommendation 010")
- Pre-Commissioning HAZOP Review links action items to closure evidence

**Audit trail:**
- HAZOP report revision history captures who, when, why for each revision
- Approval signatures and dates demonstrate review and approval
- Submission and acknowledgment records demonstrate Employer review and acceptance
- Action item register tracks status changes, closure dates, closure evidence

**Source:** Specification.md; **ASSUMPTION**: Traceability and audit trail per ISO 9001 quality management and process safety requirements

### Access and Distribution

**Access control:**
- Issued HAZOP reports are critical safety documents; available to all project engineering, operations, safety, and emergency response personnel
- Working drafts: restricted to HAZOP team and reviewers
- **TBD** — Specific access control per project information security and confidentiality requirements; consider sensitive nature of hazard information

**Distribution:**
- Issued HAZOP reports and action item register distributed to:
  - All discipline engineering leads and teams (implementation of recommendations)
  - Project management
  - Employer (per contract requirements)
  - Operations and maintenance (safety awareness, operating procedures development)
  - Safety and emergency response teams
  - Independent design verifier (DEL-28.01) if applicable
  - Regulatory authorities if required (WorkSafeBC, VFPA, etc.) — **TBD**
  - **TBD** — Additional distribution per project distribution matrix

**Distribution methods:**
- Electronic distribution via project document management system — **TBD**
- Physical copies if required per project or contractual requirements — **TBD**
- Action item register maintained as shared/collaborative document for real-time status tracking

**Source:** Specification.md; **ASSUMPTION**: Access control and distribution per project document management procedures and safety requirements

---

**Document Status:** This Procedure document is part of the DEL-27.02 deliverable working set. See `_STATUS.md` for current deliverable lifecycle state. This procedure will be updated as HAZOP studies are conducted and project-specific details (TBDs) are resolved.

**Source:** **ASSUMPTION**: Procedure document is living document aligned with deliverable lifecycle per AGENTS.md
