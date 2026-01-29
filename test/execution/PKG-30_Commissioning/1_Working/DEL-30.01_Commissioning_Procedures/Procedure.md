# Procedure: DEL-30.01 Commissioning Procedures

## Purpose

This procedure defines the process for developing, reviewing, approving, and managing **Commissioning Procedures** for the Canola Oil Transload Facility — Phase 1 Design & Build Contract.

**Dual-Use Context:**

This procedure serves two purposes:
1. **Production:** Defines how to create commissioning execution procedures (pre-commissioning, commissioning, start-up)
2. **Governance:** Establishes the framework, format, and approval process for commissioning procedures

**Source:** Agent instructions (Procedure.md dual-use interpretation); Decomposition §5 PKG-30, DEL-30.01 (Deliverable type: Procedure)

**Deliverable Context:**

Defines the execution method and controls for commissioning to meet safety, quality, and operational requirements.

**Source:** Decomposition §5 PKG-30, DEL-30.01 (Description)

**Deliverable Classification:**
- **Type:** Procedure (meta-procedure / procedure framework)
- **Discipline:** T&C (Testing & Commissioning)
- **Responsible Party:** D&B Contractor (Commissioning Team)
- **Project Objective:** OBJ-1 (Safe & Reliable Operation)

**Source:** `_CONTEXT.md`; Decomposition §2, §6 (Objectives mapping: PKG-30 → OBJ-1)

**Scope of Commissioning:**
- Pre-commissioning, system commissioning, start-up, performance verification, defect rectification
- Systems: Railcar unloading (32 stations), storage tanks (3×15,000 MT), product transfer & metering, marine loading
- Product: CSD canola oil, 1,000,000 MT/annum throughput capacity

**Source:** Decomposition §1.1 (Key Parameters), §5 PKG-30 (Scope)

## Prerequisites

**Dependencies:**

- **Dependency Tracking Mode:** NOT_TRACKED — Dependencies are coordinated externally by humans
- See `_DEPENDENCIES.md` for coordination approach
- See `execution/_Coordination/_COORDINATION.md` for project-level coordination representation

**Source:** `_DEPENDENCIES.md`

**Upstream Deliverables (coordination required):**

The following deliverables should be available or in-progress before commissioning procedure development:
- **PKG-27 (Engineering Design):** Design basis, design drawings, specifications provide commissioning requirements
- **PKG-10 through PKG-24:** System design documents define what must be commissioned
- **PKG-29 (Testing):** Testing procedures and pre-commissioning test requirements
- **PKG-31 (Documentation):** O&M manuals and vendor documentation inform commissioning methods
- **PKG-32 (Regulatory & Permits):** Permit conditions and regulatory requirements affecting commissioning
- **PKG-33 (HSE Management):** HSE requirements and permit processes for commissioning work

**Source:** Decomposition §4, §5 (Package structure); **ASSUMPTION** — Upstream information required for commissioning procedure development

**Reference Materials:**

- Employer's Requirements Volume 2 Part 1 — General Requirements — **TBD: location** for commissioning requirements
- Employer's Requirements Volume 2 Part 2 — Civil & Process Mechanical Works — **TBD: location** for system commissioning requirements
- Employer's Requirements Volume 2 Part 3 — Building Works — **TBD: location** (if applicable)
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md — Project scope and deliverable definition
- DEL-30.02 Commissioning Plan — Overall commissioning strategy and schedule
- See `_REFERENCES.md` for additional applicable reference documents
- See `0_References/` in package directory for reference materials

**Source:** Decomposition §3 (Reference Documents); `_REFERENCES.md`; **ASSUMPTION** — DEL-30.02 provides commissioning strategy context

**Applicable Codes and Standards:**
- CSA Z662 — Oil and Gas Pipeline Systems — **location TBD** for commissioning requirements
- IEC 62382 — Electrical and instrumentation loop check — **location TBD** for commissioning methods
- ASME PCC-1 — Guidelines for Pressure Boundary Bolted Flange Joint Assembly — **location TBD**
- Employer's Requirements — Project-specific commissioning requirements

**Source:** Specification.md §Standards; **ASSUMPTION: likely applicable** based on facility type

**Personnel Requirements:**

- **Procedure Author:** Qualified T&C engineer or commissioning specialist with relevant facility experience
- **Technical Reviewer:** Senior T&C engineer or discipline lead(s) for systems being commissioned
- **Safety Reviewer:** HSE representative with commissioning risk assessment experience
- **Operations Reviewer:** Operations representative to verify operational readiness criteria
- **Approver:** Commissioning Manager or designated authority

**Source:** **ASSUMPTION** — Standard procedure development roles; **location TBD** for project-specific role definitions and qualification requirements

**Tools and Templates:**
- Project-standard procedure template — **TBD**
- Commissioning procedure checklist — **TBD**
- Safety review template (JSA / HAZOP) — **TBD**
- Document management system access for procedure version control — **TBD**

**Source:** **ASSUMPTION** — Project tools to be defined; **location TBD** in project quality/document control procedures

## Steps

This procedure follows a structured approach for commissioning procedure development, review, approval, and management.

### Phase 1: Scope Definition and Planning

**Step 1.1: Identify Commissioning Scope**

**Action:**
- Review system design documents (drawings, specifications, P&IDs, control narratives) to understand system configuration and requirements
- Identify systems requiring commissioning procedures within PKG-30 scope:
  - Railcar unloading system (PKG-10): 32 stations, product transfer pumps, valving
  - Storage tanks (PKG-13): 3×15,000 MT tanks, tank instrumentation, level gauging
  - Product transfer piping (PKG-14): Transfer lines, manifolds, isolation valves
  - Metering systems (PKG-12): Custody transfer meters, proving systems, flow computers
  - Marine loading system (PKG-11): Loading arms, marine hoses, gangway, manifold
  - Electrical systems (PKG-17, PKG-18): Power distribution, motor control, lighting
  - Control systems (PKG-19, PKG-20): SCADA, PLC, field instrumentation, interlocks, alarms
  - Fire protection (PKG-23): Detection, suppression, deluge, foam systems
  - Other systems as applicable
- Define commissioning phase applicability: pre-commissioning, commissioning, or start-up

**Verification:** System scope documented and confirmed with discipline leads

**Source:** Decomposition §4, §5 (Package structure); Specification.md §Requirements FR-6 (Systems Coverage); **ASSUMPTION** — System identification from design documents

**Step 1.2: Review Employer's Requirements and Regulatory Requirements**

**Action:**
- Review Employer's Requirements Volume 2 Parts 1-3 for commissioning requirements — **TBD: location**
- Identify authority requirements for inspections and witnessing
- Identify permit conditions affecting commissioning (hot work, confined space, environmental)
- Document regulatory compliance requirements

**Verification:** Requirements documented with source citations

**Source:** Decomposition §3 (Reference Documents); §2 OBJ-6 (Regulatory Compliance); **location TBD** for specific ER commissioning requirements

**Step 1.3: Define Procedure Objectives and Acceptance Criteria**

**Action:**
- Define what the commissioning procedure must accomplish (e.g., "Verify tank leak-tightness per API 653")
- Define clear, measurable acceptance criteria for commissioning completion
- Link acceptance criteria to design requirements and project objectives (especially OBJ-1: Safe & Reliable Operation)
- Identify required records and documentation outputs

**Verification:** Objectives and acceptance criteria documented and technically sound

**Source:** Guidance.md §Principles P-3 (Systematic Verification Against Design); **ASSUMPTION** — Objectives drive procedure content

### Phase 2: Procedure Development

**Step 2.1: Establish Procedure Framework**

**Action:**
- Use project-standard procedure template — **TBD**
- Populate procedure header information:
  - Procedure number and title
  - System/equipment identification
  - Applicable phase (pre-commissioning / commissioning / start-up)
  - Revision and date
  - Author, reviewers, approvers
- Define procedure scope and exclusions

**Verification:** Framework complete per template requirements

**Source:** **ASSUMPTION** — Standard procedure format; Datasheet.md §Construction (Procedure Format Elements)

**Step 2.2: Identify Safety Requirements and Permits**

**Action:**
- Conduct preliminary hazard identification for commissioning activities
- Identify required work permits:
  - Hot work permits (if welding, cutting, grinding)
  - Confined space entry permits (if tank entry, vessel entry)
  - Lockout/tagout (LOTO) requirements for energy isolation
  - Excavation permits (if accessing buried piping)
  - Working at heights permits (if elevated work)
  - Hazardous area work permits (if working in classified areas)
- Define personal protective equipment (PPE) requirements
- Define emergency response provisions
- Identify safety hold points and witness points

**Verification:** Safety requirements complete and consistent with project HSE procedures (PKG-33)

**Source:** Guidance.md §Principles P-2 (Safety as the Foundation); Specification.md §Requirements FR-5 (Safety Integration); **ASSUMPTION** — Standard permit types; **location TBD** for project-specific HSE requirements

**Step 2.3: Define Prerequisites and Dependencies**

**Action:**
- Identify upstream activities that must be complete before commissioning:
  - Construction completion and punch-down
  - Pre-commissioning testing complete (PKG-29: hydrostatic test, leak test, cleaning, drying)
  - As-built drawings available (PKG-31)
  - Vendor documentation and O&M manuals available (PKG-31)
  - Control system programming complete and factory-tested
  - Power available and verified
  - Temporary services available (air, water, nitrogen, etc.)
- Identify parallel activities requiring coordination
- Identify downstream activities dependent on this commissioning completion

**Verification:** Dependencies identified and coordination requirements documented

**Source:** Guidance.md §Considerations C-2 (System Complexity and Interdependencies); **ASSUMPTION** — Typical commissioning prerequisites

**Step 2.4: Develop Step-by-Step Execution Instructions**

**Action:**
- Define commissioning sequence in logical order:
  - Initial conditions and system configuration
  - Step-by-step execution instructions with sufficient detail for field execution
  - For each step: define action, responsible party, verification method, acceptance criterion
  - Identify hold points (must stop for inspection/approval before proceeding)
  - Identify witness points (inspection/verification required but not stop-work)
  - Define decision points and contingency actions (if acceptance criterion not met)
  - Define non-conformance handling and corrective action process
- Use clear, active voice instructions ("Verify...", "Open valve...", "Record...")
- Include reference to drawings, datasheets, and vendor documentation as needed

**Verification:** Steps are logical, complete, executable, and technically sound

**Source:** **ASSUMPTION** — Standard procedure development practice; IEC 62382 (commissioning procedures); Datasheet.md §Construction (Procedure Format Elements)

**Step 2.5: Define Verification and Acceptance Criteria**

**Action:**
- For each commissioning step, define how to verify successful completion:
  - Visual inspection criteria
  - Functional test criteria (e.g., valve strokes full open to full closed)
  - Performance test criteria (e.g., pump delivers rated flow at rated head)
  - Measurement requirements (pressure, temperature, flow, level, etc.)
  - Alarm and interlock verification (prove safety systems function)
- Define overall procedure acceptance criteria (what constitutes successful commissioning completion)
- Link acceptance criteria to design requirements and specifications

**Verification:** Acceptance criteria are measurable, achievable, and linked to design intent

**Source:** Guidance.md §Principles P-3 (Systematic Verification Against Design); Specification.md §Verification; **ASSUMPTION** — Verification methods from commissioning practice

**Step 2.6: Define Records and Documentation Requirements**

**Action:**
- Identify what records must be generated during procedure execution:
  - Commissioning record forms or checklists
  - Test data sheets (pressures, temperatures, flows, settings, measurements)
  - Photographs (initial condition, completion, any discrepancies)
  - Non-conformance reports (NCRs) if issues identified
  - Sign-off sheets (originator, checker, approver, witness signatures)
- Define record format (datasheets, forms, photos, etc.)
- Define record retention requirements — **TBD**
- Define record storage location (e.g., `2_Checking/` during execution, `3_Issued/` upon acceptance, DEL-30.04/05/06 for commissioning records)

**Verification:** Records requirements defined and consistent with project document control (DEL-30.03, DEL-30.04, DEL-30.05, DEL-30.06)

**Source:** Specification.md §Requirements QR-3 (Records Management); Decomposition §5 PKG-30 (DEL-30.03 through DEL-30.06: Installation & Test Records); **ASSUMPTION** — Records requirements standard practice

### Phase 3: Review and Approval

**Step 3.1: Technical Review**

**Action:**
- Submit procedure to technical reviewer (discipline lead or senior T&C engineer)
- Technical reviewer verifies:
  - Technical adequacy and completeness
  - Consistency with design requirements and specifications
  - Logical sequence and executability
  - Appropriate hold points and witness points
  - Achievable acceptance criteria
  - Adequate reference to design documents
- Technical reviewer documents review findings and approval

**Verification:** Technical review sign-off obtained; action items closed

**Source:** Specification.md §Verification VM-1 (Technical Review); **ASSUMPTION** — Standard procedure review practice

**Step 3.2: Safety Review**

**Action:**
- Submit procedure to HSE representative and operations representative for safety review
- Conduct Job Safety Analysis (JSA) or HAZOP review as appropriate
- Safety reviewers verify:
  - Hazards identified and controlled
  - Required permits identified
  - PPE requirements defined
  - Emergency response provisions adequate
  - Safety hold points appropriate
  - Compliance with project HSE procedures (PKG-33)
- Safety reviewers document review findings and approval

**Verification:** Safety review sign-off obtained; action items closed

**Source:** Specification.md §Verification VM-2 (Safety Review); Guidance.md §Principles P-2 (Safety as the Foundation); **ASSUMPTION** — Standard safety review practice

**Step 3.3: Walkthrough / Tabletop Review**

**Action:**
- Conduct tabletop or field walkthrough with commissioning team, operations, maintenance, and HSE
- Step through procedure to verify:
  - Procedure is executable with available resources and time
  - Field access and logistics are feasible
  - Equipment and tools required are available or obtainable
  - Personnel have necessary skills and training
  - Interfaces with other activities are clear
- Document walkthrough findings and incorporate lessons learned

**Verification:** Walkthrough complete; action items closed

**Source:** Specification.md §Verification VM-3 (Walkthrough / Tabletop Review); **ASSUMPTION** — Standard commissioning practice

**Step 3.4: Operations Review and Approval**

**Action:**
- Submit procedure to operations representative for review
- Operations reviewer verifies:
  - Operational readiness criteria are adequate
  - Handover requirements are defined
  - Operator training requirements are identified
  - Procedure supports operational flexibility (OBJ-4: tank storage and direct rail-to-ship transfer)
  - Long-term operability and maintainability considered (OBJ-9: lifecycle cost optimization)
- Operations reviewer documents review findings and approval

**Verification:** Operations review sign-off obtained; action items closed

**Source:** Guidance.md §Considerations C-3 (Coordination with Operations), C-8 (Operability and Maintainability); Decomposition §2 (OBJ-4: Operational Flexibility, OBJ-9: Lifecycle Cost Optimization)

**Step 3.5: Final Approval**

**Action:**
- Submit procedure with all review sign-offs to Commissioning Manager (or designated approver)
- Approver verifies:
  - All required reviews complete and action items closed
  - Procedure meets project quality standards
  - Procedure aligns with commissioning plan (DEL-30.02)
  - Procedure is ready for use
- Approver signs and dates procedure approval
- Procedure is assigned final document number and revision per project document numbering system — **TBD**

**Verification:** Approval sign-off obtained; procedure released for use

**Source:** **ASSUMPTION** — Standard procedure approval governance; **location TBD** for project-specific approval requirements and document numbering

### Phase 4: Execution and Management

**Step 4.1: Procedure Distribution and Training**

**Action:**
- Distribute approved procedure to commissioning team via project document management system
- Conduct procedure briefing or training session with commissioning personnel
- Verify personnel competency to execute procedure (training records, qualifications)
- Ensure personnel understand safety requirements, hold points, witness points, and acceptance criteria

**Verification:** Distribution recorded; briefing/training documented; competency verified

**Source:** Specification.md §Verification VM-4 (Competency Verification); **ASSUMPTION** — Personnel competency required before execution

**Step 4.2: Procedure Execution**

**Action:**
- Execute procedure per approved sequence and instructions
- Complete all required records and documentation during execution
- Obtain required signatures at hold points and witness points
- Handle non-conformances per project procedures (stop work, assess, correct, verify, document, resume)
- Coordinate with other activities and packages as required

**Verification:** Procedure executed per approved instructions; records complete; non-conformances documented and resolved

**Source:** **ASSUMPTION** — Procedure execution per approved instructions; non-conformance handling per project quality procedures

**Step 4.3: Procedure Completion and Records Submittal**

**Action:**
- Upon procedure completion, verify all steps complete and acceptance criteria met
- Compile all commissioning records (datasheets, test records, photos, sign-offs, NCRs)
- Submit commissioning records to designated location:
  - Pre-commissioning records → DEL-30.03
  - Commissioning records → DEL-30.04
  - Integrated systems test records → DEL-30.05
  - Performance test records → DEL-30.06
- Obtain final sign-offs (commissioning engineer, QC, operations)

**Verification:** Commissioning complete per acceptance criteria; records submitted and accepted

**Source:** Decomposition §5 PKG-30 (DEL-30.03 through DEL-30.06: Installation & Test Records); **ASSUMPTION** — Records submittal to appropriate deliverable

**Step 4.4: Lessons Learned and Continuous Improvement**

**Action:**
- Conduct post-commissioning debrief with commissioning team
- Identify lessons learned:
  - What went well
  - What could be improved
  - Issues encountered and resolutions
  - Recommendations for future procedures
- Update procedure if significant issues identified (revision process)
- Share lessons learned with other commissioning teams and feed into procedure templates

**Verification:** Lessons learned documented; improvement actions identified

**Source:** **ASSUMPTION** — Continuous improvement practice; Guidance.md §Considerations C-8 (feed lessons learned into O&M manuals)

### Phase 5: Procedure Revision and Change Management

**Step 5.1: Change Request and Evaluation**

**Action:**
- If procedure revision required (lessons learned, design change, field conditions):
  - Document change request with justification
  - Evaluate impact of change (safety, quality, schedule, cost)
  - Obtain approval from Commissioning Manager for change
- For minor editorial changes: may be handled expeditiously
- For substantive technical or safety changes: repeat review and approval process (Steps 3.1-3.5)

**Verification:** Change request documented and approved; revision justified

**Source:** **ASSUMPTION** — Standard change management practice; **location TBD** for project change control procedures

**Step 5.2: Revision, Review, and Re-Approval**

**Action:**
- Revise procedure per approved change request
- Conduct appropriate level of review (technical, safety, walkthrough as needed)
- Update revision number and revision history
- Re-approve per project document control procedures — **TBD**
- Supersede previous revision in document management system

**Verification:** Revision approved and current version identified

**Source:** Specification.md §Requirements QR-4 (Revision Control); **ASSUMPTION** — Revision control per project document management

**Step 5.3: Communicate Revision**

**Action:**
- Notify commissioning team of procedure revision
- Retrieve obsolete versions if hard copies in circulation
- Brief commissioning team on changes and implications
- Update training records if revision affects competency requirements

**Verification:** Revision communicated; obsolete versions retrieved; personnel briefed

**Source:** **ASSUMPTION** — Communication required for effective change implementation

## Verification

**Verification Activities:**

This procedure (DEL-30.01 Commissioning Procedures) itself shall undergo verification per the methods defined in Specification.md:

**V-1: Technical Review**
- Reviewer: Senior T&C Engineer or Commissioning Manager
- Criterion: Technical adequacy verified; sign-off obtained

**V-2: Safety Review**
- Reviewer: HSE representative
- Criterion: HSE requirements verified; sign-off obtained

**V-3: Walkthrough / Tabletop Review**
- Participants: Commissioning team, operations, HSE
- Criterion: Walkthrough complete; action items closed

**V-4: Competency Verification**
- Method: Commissioning team personnel qualifications verified
- Criterion: Personnel competency documented

**V-5: Trial Run (if practical)**
- Method: Test procedure framework on pilot system commissioning
- Criterion: Framework effective; lessons learned incorporated

**Source:** Specification.md §Verification (VM-1 through VM-5)

**Acceptance Criteria for This Procedure:**

- Procedure framework is complete and covers all commissioning phases (pre-commissioning, commissioning, start-up)
- Safety requirements are clearly defined
- Review and approval process is defined
- Records requirements are defined and linked to PKG-30 deliverables (DEL-30.03 through DEL-30.06)
- Procedure is technically sound and field-executable
- All required sign-offs obtained

**Source:** Specification.md §Verification (Acceptance Criteria); **ASSUMPTION** — Meta-procedure acceptance criteria

**Ongoing Verification:**

Commissioning procedures developed using this framework shall be verified per Steps 3.1-3.5 (Review and Approval phase).

## Records

**Documentation Outputs:**

This deliverable (DEL-30.01) produces the following anticipated artifacts:

**Primary Outputs:**

1. **Pre-commissioning Procedures:**
   - System flushing and cleaning procedures
   - Hydrostatic test procedures
   - Leak test procedures
   - Drying and preservation procedures
   - Pre-commissioning inspection procedures

2. **Commissioning Procedures:**
   - Mechanical commissioning procedures (by system: tanks, piping, pumps, valves, etc.)
   - Electrical commissioning procedures (by system: power distribution, motors, lighting, etc.)
   - I&C commissioning procedures (by system: control systems, instrumentation, safety systems, etc.)
   - Integrated systems commissioning procedures (end-to-end system verification)

3. **Start-up Procedures:**
   - Initial fill and circulation procedures
   - First product receipt procedures (railcar unloading)
   - First product loading procedures (ship loading)
   - System performance verification procedures
   - Operational readiness verification procedures

**Source:** Decomposition §5 PKG-30, DEL-30.01 (Anticipated Artifacts); Datasheet.md §Construction; Specification.md §Documentation; Guidance.md §Examples E-4

**Supporting Records:**

- Procedure development checklist (if used) — **TBD**
- Technical review records (reviewer comments, action item log, sign-offs)
- Safety review records (JSA / HAZOP worksheets, hazard register, sign-offs)
- Walkthrough records (attendees, findings, action items)
- Competency verification records (training logs, qualification certificates)
- Lessons learned register (post-commissioning feedback)
- Procedure revision history (change requests, revision log)

**Source:** **ASSUMPTION** — Supporting records for procedure development governance

**Record Management:**

- **Development Phase:** Working files in deliverable folder `1_Working/DEL-30.01_Commissioning_Procedures/`
- **Review Phase:** Review package in `2_Checking/To/` with distribution to reviewers
- **Issued Phase:** Approved procedures in `3_Issued/` with controlled distribution
- **Execution Phase:** Commissioning records generated from procedure execution submitted to:
  - Pre-commissioning records → `DEL-30.03/3_Issued/`
  - Commissioning records → `DEL-30.04/3_Issued/`
  - Integrated systems test records → `DEL-30.05/3_Issued/`
  - Performance test records → `DEL-30.06/3_Issued/`

**Source:** Specification.md §Documentation (Records Location); Decomposition §5 PKG-30 (DEL-30.03 through DEL-30.06)

**Retention Requirements:**
- **TBD** — To be defined per project records management plan and Employer's Requirements

**Source:** Specification.md §Documentation (Retention)

**Document Control:**
- All procedures shall be managed per project document control procedures — **TBD: location**
- Version control in project document management system — **ASSUMPTION**: Electronic EDMS or similar
- Controlled distribution to commissioning team and authorized personnel
- Obsolete versions retrieved and archived

**Source:** Specification.md §Requirements QR-4 (Revision Control); **ASSUMPTION** — Standard project document control practices

---

## Document Cross-References

This Procedure connects to the other three documents as follows:

- **← Datasheet.md:** Procedure produces the anticipated artifacts identified in Datasheet
  - Datasheet §Construction (Pre-commissioning procedures) → This Procedure §Steps Phase 2 (Development), §Records (Pre-commissioning outputs)
  - Datasheet §Construction (Commissioning procedures) → This Procedure §Steps Phase 2 (Development), §Records (Commissioning outputs)
  - Datasheet §Construction (Start-up procedures) → This Procedure §Steps Phase 2 (Development), §Records (Start-up outputs)
  - Datasheet §Construction (Procedure format elements) → This Procedure §Steps 2.1 (Framework), 2.4 (Execution instructions)
  - Datasheet §Conditions (Facility parameters) → This Procedure §Purpose (Scope context)

- **← Specification.md:** Procedure defines verification methods and execution steps for each requirement
  - Specification §Requirements FR-1 (Procedure structure) → This Procedure §Steps 2.1, 2.4
  - Specification §Requirements FR-2 through FR-4 (Coverage) → This Procedure §Steps 1.1 (Scope identification)
  - Specification §Requirements FR-5 (Safety) → This Procedure §Steps 2.2 (Safety requirements and permits)
  - Specification §Requirements FR-6 (Systems coverage) → This Procedure §Steps 1.1 (System scope)
  - Specification §Requirements PR-1 through PR-3 (Performance) → This Procedure §Steps 1.3, 2.5 (Objectives and acceptance criteria)
  - Specification §Requirements IR-1 through IR-6 (Interfaces) → This Procedure §Steps 1.2, 2.3 (ER review, prerequisites, dependencies)
  - Specification §Requirements QR-1, QR-2 (Quality) → This Procedure §Steps Phase 3 (Review and approval)
  - Specification §Requirements QR-3 (Records) → This Procedure §Steps 2.6 (Records requirements), §Records
  - Specification §Requirements QR-4 (Revision control) → This Procedure §Steps Phase 5 (Revision and change management)
  - Specification §Verification → This Procedure §Verification

- **← Guidance.md:** Procedure development informed by principles, considerations, and trade-offs
  - Guidance §Principles P-1 (Phased approach) → This Procedure §Steps 1.1 (Scope definition by phase)
  - Guidance §Principles P-2 (Safety foundation) → This Procedure §Steps 2.2 (Safety requirements identification)
  - Guidance §Principles P-3 (Systematic verification) → This Procedure §Steps 1.3, 2.5 (Objectives, acceptance criteria, verification)
  - Guidance §Principles P-4 (Integration) → This Procedure §Steps 1.2, 2.3 (Review ERs, prerequisites, dependencies)
  - Guidance §Principles P-5 (Product-specific) → This Procedure §Steps 1.2 (Review requirements including product handling)
  - Guidance §Considerations C-1 through C-9 → This Procedure §Steps Phase 1 (Scope definition and planning)
  - Guidance §Trade-offs T-1 through T-5 → This Procedure development decisions (prescriptive vs. flexible, witness/hold points, documentation rigor)
