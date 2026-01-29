# Procedure: DEL-30.02 Commissioning Plan

## Purpose

This procedure defines the process for developing, reviewing, approving, and maintaining the **Commissioning Plan** for the Canola Oil Transload Facility — Phase 1 Design & Build Contract.

**Deliverable Context:**

Defines the planned approach and controls for commissioning to meet Employer's Requirements.

**Source:** Decomposition §5 PKG-30, DEL-30.02 (Description)

**Deliverable Classification:**
- **Type:** Plan (strategic commissioning management document and integrated schedule)
- **Discipline:** T&C (Testing & Commissioning)
- **Responsible Party:** D&B Contractor (Commissioning Team)
- **Scope:** Pre-commissioning, system commissioning, integrated systems test, start-up, performance verification for canola oil transload facility

**Source:** `_CONTEXT.md`; Decomposition §5 PKG-30 (Scope)

## Prerequisites

**Dependencies:**
- **Dependency Tracking Mode:** NOT_TRACKED — Dependencies coordinated externally by humans
- See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`

**Source:** `_DEPENDENCIES.md`

**Upstream Deliverables (coordination required):**
- **PKG-27 (Engineering Design):** Design basis, system design documents define commissioning scope
- **PKG-10 through PKG-24:** System design packages provide commissioning scope detail
- **DEL-30.01 Commissioning Procedures:** Execution methods that this plan governs
- **Construction Schedule:** System handover dates are inputs to commissioning schedule
- **Project Execution Plan:** Overall project delivery framework — **ASSUMPTION: likely exists**

**Source:** Decomposition §4, §5; **ASSUMPTION** — Upstream information required for planning

**Reference Materials:**
- Employer's Requirements Volume 2 Parts 1-3 — **TBD: location** for commissioning requirements
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md — Project scope and objectives
- See `_REFERENCES.md` and `0_References/`
- IEC 62382, CSA Z662, API 653, ASME PCC-1 — **location TBD** for commissioning planning guidance

**Source:** Decomposition §3; Specification.md §Standards

**Personnel Requirements:**
- **Plan Author:** Commissioning Manager or Senior T&C Engineer
- **Technical Reviewers:** Discipline leads (mechanical, electrical, I&C, civil)
- **Operations Reviewer:** Operations Manager or delegate
- **HSE Reviewer:** HSE Manager
- **Schedule Reviewer:** Project planning / scheduling lead
- **Regulatory Reviewer:** Regulatory affairs / PKG-32 lead
- **Approver:** Project Manager or Commissioning Manager

**Source:** Specification.md §Verification; **ASSUMPTION** — Review roles for plan approval

**Tools and Resources:**
- Project-standard plan template — **TBD**
- Scheduling software (Primavera P6 or MS Project) — **TBD**
- Construction schedule for integration — **TBD**
- System design documents (drawings, P&IDs, specifications)
- Document management system

**Source:** **ASSUMPTION** — Tools required for plan development

## Steps

### Phase 1: Planning Foundation

**Step 1.1: Review Project Requirements and Constraints**

**Action:**
- Review Employer's Requirements Volumes 2 Parts 1-3 for commissioning requirements — **TBD: location**
- Review project objectives (OBJ-1 through OBJ-10) and commissioning's role in achieving them
- Review contract requirements for commissioning deliverables and milestones — **TBD: location**
- Identify regulatory requirements (TSB, Transport Canada, VFPA, environmental) affecting commissioning
- Identify terminal continuity constraints (OBJ-5: minimize disturbance to existing operations)
- Document requirements and constraints

**Verification:** Requirements documented with sources; constraints identified

**Source:** Decomposition §2 (Objectives), §2 OBJ-5; **location TBD** for ER commissioning requirements

**Step 1.2: Review Facility Scope and System Breakdown**

**Action:**
- Review facility key parameters: 32 railcar stations, 3×15,000 MT tanks, 1M MT/annum throughput, marine loading
- Review system design packages (PKG-10 through PKG-24) to understand commissioning scope
- Define system breakdown for commissioning planning:
  - Railcar unloading system
  - Storage tanks
  - Product transfer and metering
  - Marine loading system
  - Electrical and lighting
  - Control systems and instrumentation
  - Fire protection and security
  - Buildings and MEP (as applicable)
- Identify system boundaries, interfaces, and interdependencies
- Identify specialized commissioning requirements (metering proving, cathodic protection, etc.)

**Verification:** System breakdown complete and aligned with facility design

**Source:** Decomposition §1.1 (Key Parameters), §4 (Package Summary); Specification.md §Requirements FR-3

**Step 1.3: Review DEL-30.01 Commissioning Procedures Framework**

**Action:**
- Review DEL-30.01 to understand commissioning execution methods and procedures framework
- Understand procedure types: pre-commissioning, commissioning, start-up
- Understand procedure governance: development, review, approval process
- Align plan with procedures framework

**Verification:** Plan aligned with execution procedures

**Source:** DEL-30.01 Commissioning Procedures

### Phase 2: Plan Development

**Step 2.1: Define Commissioning Philosophy and Strategy**

**Action:**
- Define commissioning philosophy aligned with project objectives (safe, reliable operation)
- Define commissioning strategy: phased approach (pre-comm → individual systems → integrated → start-up → performance)
- Define commissioning principles: safety first, systematic verification, operational readiness focus
- Define success criteria for commissioning completion and operational readiness
- Document strategy in plan Section 2

**Verification:** Strategy clear, aligned with project objectives, phased approach defined

**Source:** Guidance.md §Principles P-1, P-4; Specification.md §Requirements FR-1

**Step 2.2: Define Commissioning Phases and Approach**

**Action:**
- Define pre-commissioning phase: scope, acceptance criteria, coordination with PKG-29 (Testing)
- Define individual system commissioning: mechanical, electrical, I&C sequences
- Define integrated systems commissioning: end-to-end testing approach
- Define start-up phase: initial fill, first product receipt (rail), first loading (ship)
- Define performance verification: capacity tests, custody transfer proving, reliability demonstration
- Define defect rectification and punch list closure process (DEL-30.07)
- Document in plan Sections 5 and 13

**Verification:** All phases defined with scope and acceptance criteria

**Source:** Specification.md §Requirements FR-5, FR-6, FR-7; Guidance.md §Principles P-1

**Step 2.3: Define Commissioning Organization and Responsibilities**

**Action:**
- Define commissioning organization structure
- Identify key roles: Commissioning Manager, discipline leads, QA/QC, HSE, ops liaison
- Define roles and responsibilities for each position
- Define decision-making authorities and escalation paths
- Define communication and reporting requirements
- Estimate commissioning team size and resource requirements
- Document in plan Section 3

**Verification:** Organization clear, roles defined, authorities assigned

**Source:** Specification.md §Requirements FR-2; Guidance.md §Considerations C-1

**Step 2.4: Define Commissioning Scope by System**

**Action:**
- For each system, define:
  - System description and boundaries
  - Pre-commissioning requirements
  - Commissioning sequence and activities
  - Acceptance criteria
  - Handover requirements from construction
  - Records requirements (DEL-30.03 through DEL-30.08)
  - Interface with other systems
- Document in plan Section 4 with system breakdown structure

**Verification:** All facility systems addressed; scope complete

**Source:** Specification.md §Requirements FR-3; Guidance.md §Considerations C-2

**Step 2.5: Develop Integrated Commissioning Schedule**

**Action:**
- Obtain construction schedule to identify system handover dates
- Define commissioning activities by system and phase
- Define activity durations based on system complexity and resource availability
- Define dependencies between activities:
  - Construction to commissioning handover
  - Pre-commissioning to commissioning
  - Individual systems to integrated systems
  - Commissioning to start-up to performance verification
- Identify critical path activities
- Define milestones: phase completions, first operations, performance acceptance
- Load resources (commissioning team personnel)
- Integrate with construction schedule
- Identify schedule risks and define contingency
- Use scheduling software (P6 or MS Project) — **TBD**
- Document schedule as plan Section 12 (integrated schedule document)

**Verification:** Schedule integrated, dependencies correct, critical path identified, resource loading realistic

**Source:** Specification.md §Requirements FR-9, FR-10, PR-2; Guidance.md §Considerations C-5

**Step 2.6: Define Safety and Permit Planning**

**Action:**
- Identify hazardous commissioning activities
- Define required work permits: hot work, confined space, LOTO, working at heights, excavation, hazardous area work
- Define PPE requirements
- Define emergency response provisions
- Integrate with PKG-33 HSE Management system
- Define terminal continuity measures (OBJ-5: minimize disturbance to existing operations)
- Document in plan Section 6

**Verification:** Safety requirements comprehensive; HSE integration defined

**Source:** Specification.md §Requirements FR-8; Guidance.md §Principles P-2

**Step 2.7: Define Interface Management**

**Action:**
- Define construction interface: handover process, punch-down, access, logistics
- Define operations interface: operational readiness criteria, training support, handover process (coordinate with PKG-35)
- Define regulatory interface: authority inspections, permit compliance, coordination (PKG-32)
- Define testing interface: pre-commissioning test coordination (PKG-29)
- Define documentation interface: as-builts, O&M manuals, vendor docs prerequisites (PKG-31)
- Document in plan Section 8

**Verification:** All interfaces identified and management approach defined

**Source:** Specification.md §Requirements IR-1 through IR-5; Guidance.md §Principles P-3

**Step 2.8: Define Quality Assurance, Verification, and Records Management**

**Action:**
- Define quality controls for commissioning activities
- Define hold points and witness points (authority inspections, Employer witness, QA/QC)
- Define verification methods and acceptance criteria for each commissioning phase
- Define records requirements: formats, retention, submittal process
- Map records to deliverables: DEL-30.03 (pre-comm), DEL-30.04 (comm), DEL-30.05 (IST), DEL-30.06 (performance), DEL-30.07 (punch lists), DEL-30.08 (cathodic protection)
- Document in plan Sections 7 and 11

**Verification:** QA approach defined; records management comprehensive

**Source:** Specification.md §Requirements QR-1, QR-2, QR-3

**Step 2.9: Define Risk Management and Contingency**

**Action:**
- Identify commissioning risks: technical, schedule, resource, interface, safety
- Assess risk likelihood and impact
- Define mitigation strategies for high-priority risks
- Define contingency plans for critical risks
- Define schedule contingency (float) and resource contingency
- Document in plan Section 10

**Verification:** Key risks identified and mitigation defined

**Source:** Guidance.md §Trade-offs; **ASSUMPTION** — Risk management required

**Step 2.10: Define Resource Requirements**

**Action:**
- Define personnel requirements by phase and system
- Define equipment requirements: test equipment, temporary utilities, tools
- Define consumables: nitrogen, air, water, flushing agents
- Define logistics requirements: site access, laydown areas, offices
- Identify resource constraints and procurement lead times
- Document in plan Section 9

**Verification:** Resources identified and realistic

**Source:** Specification.md §Requirements PR-3; Guidance.md §Considerations C-1

**Step 2.11: Define Handover and Closeout Process**

**Action:**
- Define operational readiness criteria (link to project objectives OBJ-1, OBJ-2, OBJ-3, OBJ-4, OBJ-10)
- Define handover documentation requirements
- Define handover process: phased handover or full facility handover
- Define closeout activities: punch list closure (DEL-30.07), final records submittal, lessons learned
- Define post-handover support period
- Document in plan Section 13

**Verification:** Handover process clear and aligned with operational readiness objectives

**Source:** Specification.md §Requirements PR-1; Guidance.md §Principles P-4

**Step 2.12: Compile Commissioning Plan Document**

**Action:**
- Compile all sections into integrated plan document
- Write executive summary (Section 1)
- Add table of contents, list of figures/tables, list of abbreviations
- Add appendices: system descriptions, organizational charts, interface agreements, risk register
- Attach integrated commissioning schedule (Section 12)
- Apply project formatting and numbering — **TBD**

**Verification:** Plan document complete and professional

**Source:** Datasheet.md §Construction (Plan content)

### Phase 3: Review and Approval

**Step 3.1: Technical Review**

**Action:**
- Distribute plan to discipline leads for technical review
- Reviewers verify: scope complete, technical approach sound, system breakdown correct, interfaces identified
- Address review comments and update plan

**Verification:** Technical review sign-offs obtained

**Source:** Specification.md §Verification VM-1

**Step 3.2: Operations Review**

**Action:**
- Distribute plan to operations representative
- Reviewer verifies: operational readiness criteria adequate, handover process defined, operations interface clear
- Address review comments and update plan

**Verification:** Operations review sign-off obtained

**Source:** Specification.md §Verification VM-2

**Step 3.3: HSE Review**

**Action:**
- Distribute plan to HSE representative
- Reviewer verifies: safety requirements comprehensive, permit planning adequate, HSE integration defined
- Address review comments and update plan

**Verification:** HSE review sign-off obtained

**Source:** Specification.md §Verification VM-3

**Step 3.4: Schedule Integration Review**

**Action:**
- Distribute schedule to project planning team
- Reviewer verifies: schedule integrated with construction, dependencies correct, critical path identified, resource loading realistic
- Address review comments and update schedule

**Verification:** Schedule review sign-off obtained

**Source:** Specification.md §Verification VM-4

**Step 3.5: Regulatory Review**

**Action:**
- Distribute plan to regulatory affairs / PKG-32 lead
- Reviewer verifies: regulatory milestones identified, authority inspections planned, permit compliance addressed
- Address review comments and update plan

**Verification:** Regulatory review sign-off obtained

**Source:** Specification.md §Verification VM-5

**Step 3.6: Final Approval**

**Action:**
- Submit plan with all review sign-offs to Project Manager or Commissioning Manager
- Approver verifies all reviews complete and plan ready for implementation
- Approver signs and dates approval
- Assign final document number and revision per project system — **TBD**
- Issue plan to controlled distribution

**Verification:** Approval obtained; plan issued

**Source:** **ASSUMPTION** — Final approval governance

### Phase 4: Plan Monitoring and Updates

**Step 4.1: Monitor Commissioning Progress**

**Action:**
- Track commissioning progress against plan and schedule
- Collect actual start/finish dates for commissioning activities
- Identify variances from plan (scope, schedule, resources)
- Identify emerging issues and risks
- Report progress to project management and Employer — **TBD: reporting frequency and format**

**Verification:** Progress monitoring active

**Source:** Specification.md §Requirements PR-2

**Step 4.2: Update Commissioning Plan and Schedule**

**Action:**
- Update plan and schedule per review cycle (monthly or per milestones) — **TBD**
- Update scope if changes occur
- Update schedule with actual progress and revised forecasts
- Update critical path analysis
- Update resource loading if changes occur
- Update risk register with new risks and closed risks
- Revise plan document and schedule
- Obtain approval for substantive changes
- Issue updated plan per revision control procedures — **TBD**

**Verification:** Plan kept current throughout commissioning

**Source:** Specification.md §Requirements QR-4; Datasheet.md §Attributes (Review Cycle)

**Step 4.3: Lessons Learned and Continuous Improvement**

**Action:**
- Capture lessons learned during commissioning execution
- Update plan based on lessons learned
- Share lessons learned with project team
- Incorporate lessons into future commissioning planning

**Verification:** Lessons learned captured and applied

**Source:** **ASSUMPTION** — Continuous improvement practice

## Verification

This commissioning plan shall undergo verification per Specification.md §Verification:

- **VM-1: Technical Review** — Discipline leads verify technical adequacy
- **VM-2: Operations Review** — Operations verifies operational readiness approach
- **VM-3: HSE Review** — HSE verifies safety and permit planning
- **VM-4: Schedule Integration Review** — Planning team verifies schedule integration
- **VM-5: Regulatory Review** — Regulatory affairs verifies compliance approach

**Acceptance Criteria:**
- Commissioning strategy complete and aligned with project objectives
- Organization and responsibilities clearly defined
- Commissioning scope covers all facility systems
- Schedule is integrated, realistic, and supports project milestones
- Safety and permit requirements identified
- Interface management defined
- Risk management and contingency planning adequate
- All required reviews complete and sign-offs obtained

**Source:** Specification.md §Verification

## Records

**Documentation Outputs:**

1. **Commissioning Plan Document:**
   - Executive summary
   - Commissioning strategy and philosophy
   - Organization and responsibilities
   - Scope definition and system breakdown
   - Commissioning phases and approach
   - Safety and permit planning
   - Quality assurance and verification
   - Interface management
   - Resource requirements
   - Risk management and contingency
   - Records management
   - Commissioning schedule (integrated schedule)
   - Handover and closeout process

2. **Commissioning Schedule:**
   - Integrated schedule (electronic format: P6 or MS Project — **TBD**)
   - PDF schedule for distribution

**Source:** Decomposition §5 PKG-30, DEL-30.02; Datasheet.md §Construction

**Record Management:**
- **Development Phase:** Working files in `1_Working/DEL-30.02_Commissioning_Plan/`
- **Review Phase:** Review package in `2_Checking/To/`
- **Issued Phase:** Approved plan and schedule in `3_Issued/`
- **Updates:** Revised versions per revision control — **TBD**
- **Retention:** **TBD** — Per project records management plan

**Source:** Specification.md §Documentation

---

## Document Cross-References

- **← Datasheet.md:** Procedure produces plan and schedule identified in Datasheet
  - Datasheet §Construction (Plan content) → This Procedure §Steps Phase 2
  - Datasheet §Construction (Schedule content) → This Procedure §Steps 2.5
  - Datasheet §Attributes (Review cycle) → This Procedure §Steps Phase 4

- **← Specification.md:** Procedure addresses all requirements
  - Specification §Requirements FR-1 through FR-10 → This Procedure §Steps Phase 2
  - Specification §Requirements PR-1 through PR-4 → This Procedure §Steps 2.1, 2.5, 2.10, 2.11
  - Specification §Requirements IR-1 through IR-6 → This Procedure §Steps 2.7
  - Specification §Requirements QR-1 through QR-4 → This Procedure §Steps 2.8, Phase 4
  - Specification §Verification → This Procedure §Steps Phase 3

- **← Guidance.md:** Procedure informed by principles and considerations
  - Guidance §Principles P-1 → This Procedure §Steps 2.1, 2.2
  - Guidance §Principles P-2 → This Procedure §Steps 2.6
  - Guidance §Principles P-3 → This Procedure §Steps 2.7
  - Guidance §Principles P-4 → This Procedure §Steps 2.11
  - Guidance §Considerations C-1 through C-7 → This Procedure §Steps Phase 2
