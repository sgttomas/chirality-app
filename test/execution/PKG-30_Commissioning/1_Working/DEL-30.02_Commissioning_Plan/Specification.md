# Specification: DEL-30.02 Commissioning Plan

## Scope

This specification defines the requirements for **Commissioning Plan** within **PKG-30 Commissioning** for the Canola Oil Transload Facility — Phase 1 Design & Build Contract.

**Project Context:**
- Employer: DP World Fraser Surrey Inc.
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- Contract Type: Design & Build
- Facility Type: CSD canola oil transload (rail-to-storage-to-ship)

**Source:** Decomposition §1 (Project Context)

**Deliverable Purpose:**

Defines the planned approach and controls for commissioning to meet Employer's Requirements.

**Source:** Decomposition §5 PKG-30, DEL-30.02 (Description)

**Anticipated Deliverable Artifacts:**
- Commissioning plan (document defining strategy, organization, scope, approach)
- Commissioning schedule (integrated schedule with activities, dependencies, resources, milestones)

**Source:** Decomposition §5 PKG-30, DEL-30.02 (Anticipated Artifacts)

**Scope Boundaries:**

**Included:**
- Overall commissioning strategy and philosophy
- Commissioning organization, roles, and responsibilities
- Commissioning scope breakdown by system and phase
- Integrated commissioning schedule with dependencies and milestones
- Resource planning (personnel, equipment, utilities)
- Safety and permit planning for commissioning work
- Interface management (construction, operations, regulatory)
- Risk management and contingency planning
- Quality assurance and verification approach
- Records and documentation governance
- Handover and closeout process

**Excluded:**
- Detailed execution procedures (covered in DEL-30.01 Commissioning Procedures)
- Actual commissioning records (captured in DEL-30.03 through DEL-30.08)
- System-specific design details (covered in PKG-10 through PKG-24 design packages)
- Construction schedule and methods (Contractor's separate deliverable)
- Operations procedures post-handover (covered in PKG-31 O&M Manuals)

**Source:** **ASSUMPTION** — Typical commissioning plan scope; DEL-30.01 provides execution detail; DEL-30.03-30.08 capture results

## Requirements

### Functional Requirements

**FR-1: Commissioning Strategy**
- The plan shall define the overall commissioning philosophy and approach
- The plan shall define commissioning phases: pre-commissioning, individual system commissioning, integrated systems commissioning, start-up, performance verification
- The plan shall define the logical sequence and dependencies between commissioning phases
- **Source:** **ASSUMPTION** — Standard commissioning phases per IEC 62382; Decomposition §5 PKG-30 (Scope: Pre-commissioning, system commissioning, start-up, performance verification)

**FR-2: Commissioning Organization**
- The plan shall define commissioning organization structure with clear roles and responsibilities
- The plan shall identify key personnel: Commissioning Manager, discipline leads, QA/QC, HSE, operations interface
- The plan shall define decision-making authority and escalation paths
- The plan shall define communication and reporting requirements
- **Source:** **ASSUMPTION: required** for commissioning governance; **location TBD** in Employer's Requirements for organizational requirements

**FR-3: Commissioning Scope Definition**
- The plan shall define commissioning scope for all facility systems:
  - Railcar unloading system (32 stations, 2 tracks)
  - Storage tanks (3 × 15,000 MT tanks)
  - Product transfer and metering systems
  - Marine loading system
  - Electrical power distribution and lighting
  - Control systems and instrumentation
  - Fire protection and safety systems
  - Security systems
  - Buildings and MEP systems (as applicable)
- The plan shall define system boundaries and interfaces
- The plan shall identify systems requiring specialized commissioning (e.g., custody transfer metering, fire protection, cathodic protection)
- **Source:** Decomposition §1.1 (Key Parameters), §4 (Package Summary: PKG-10 through PKG-24); Datasheet.md §Conditions (Facility parameters)

**FR-4: System Handover Process**
- The plan shall define the process for system handover from construction to commissioning
- The plan shall define handover criteria (construction complete, punch-down, pre-commissioning testing complete, as-builts available)
- The plan shall define handover documentation requirements (as-builts, vendor docs, test records, O&M manuals)
- **Source:** **ASSUMPTION: required** for construction-commissioning interface; **location TBD** for project-specific handover requirements

**FR-5: Pre-Commissioning Activities**
- The plan shall define pre-commissioning activities and acceptance criteria:
  - System flushing and cleaning
  - Hydrostatic testing and leak testing
  - Drying and preservation
  - Pre-commissioning inspections
- The plan shall define coordination with PKG-29 (Testing) for pre-commissioning test activities
- **Source:** Decomposition §5 PKG-30 (Scope: Pre-commissioning); PKG-29 (Testing); **ASSUMPTION** — Typical pre-commissioning scope

**FR-6: Individual System Commissioning**
- The plan shall define individual system commissioning by discipline:
  - Mechanical commissioning (tanks, piping, pumps, valves, pressure vessels)
  - Electrical commissioning (power distribution, motors, transformers, switchgear)
  - I&C commissioning (control systems, field instrumentation, safety interlocks, alarms)
- The plan shall define commissioning sequence to support integrated systems testing
- **Source:** Decomposition §5 PKG-30 (Scope: system commissioning); **ASSUMPTION** — Discipline-based commissioning approach

**FR-7: Integrated Systems Commissioning and Start-up**
- The plan shall define integrated systems commissioning approach to verify end-to-end system functionality
- The plan shall define start-up activities: initial fill, first product receipt (rail), first product transfer (ship)
- The plan shall define operational readiness criteria for transition to operations
- **Source:** Decomposition §5 PKG-30 (DEL-30.05: Integrated Systems Test); **ASSUMPTION** — Integrated testing required before operations

**FR-8: Safety and Permit Planning**
- The plan shall identify safety requirements for commissioning work:
  - Required work permits (hot work, confined space, LOTO, working at heights, excavation)
  - Hazardous area precautions
  - Emergency response provisions
  - PPE requirements
- The plan shall integrate with project HSE management system (PKG-33)
- The plan shall address terminal continuity and minimize disturbance to existing operations (OBJ-5)
- **Source:** Decomposition §2 OBJ-5 (Terminal Continuity); PKG-33 (HSE Management); **ASSUMPTION** — Safety planning required for commissioning work

**FR-9: Commissioning Schedule**
- The plan shall include an integrated commissioning schedule showing:
  - Pre-commissioning activities by system
  - Individual system commissioning by discipline
  - Integrated systems commissioning
  - Start-up and first operations
  - Performance verification
  - Defect rectification and punch list closure
- The schedule shall show dependencies, critical path, milestones, and resource loading
- The schedule shall be integrated with construction schedule (system handover dates)
- **Source:** Decomposition §5 PKG-30, DEL-30.02 (Anticipated Artifacts: commissioning schedule); **ASSUMPTION** — Integrated schedule required for coordination

**FR-10: Schedule Milestones**
- The schedule shall identify key commissioning milestones:
  - Pre-commissioning completion by system
  - Individual system commissioning completion by discipline
  - Integrated systems test completion
  - First product receipt (railcar unloading commissioning)
  - First product loading (ship loading commissioning)
  - Performance verification completion
  - Operational readiness and handover to operations
- **Source:** **ASSUMPTION** — Key milestones for commissioning governance and progress tracking

### Performance Requirements

**PR-1: Operational Readiness**
- The commissioning plan shall define activities and acceptance criteria to demonstrate operational readiness per project objectives:
  - OBJ-1: Safe & Reliable Operation — facility suitable for continuous use
  - OBJ-2: Throughput Capacity — 1,000,000 MT per annum confirmed
  - OBJ-3: Storage Capacity — 45,000 MT storage confirmed
  - OBJ-4: Operational Flexibility — tank storage and direct rail-to-ship transfer modes verified
  - OBJ-10: Custody Transfer Accuracy — metering system accuracy confirmed
- **Source:** Decomposition §2 (Project Objectives: OBJ-1, OBJ-2, OBJ-3, OBJ-4, OBJ-10)

**PR-2: Schedule Performance**
- The commissioning schedule shall support project delivery milestones — **TBD: location** for contractual milestones
- The commissioning plan shall identify critical path activities and schedule contingency
- The plan shall define schedule monitoring and update process
- **Source:** **ASSUMPTION** — Schedule performance required for project delivery; **location TBD** for contractual schedule requirements

**PR-3: Resource Efficiency**
- The plan shall define resource requirements and resource loading to optimize commissioning efficiency
- The plan shall identify resource constraints and mitigation strategies
- The plan shall support lifecycle cost optimization (OBJ-9) through efficient commissioning execution
- **Source:** Decomposition §2 OBJ-9 (Lifecycle Cost Optimization); **ASSUMPTION** — Resource planning required for execution efficiency

**PR-4: Performance Verification**
- The plan shall define performance verification activities to confirm facility achieves design parameters:
  - Throughput capacity verification
  - Storage capacity verification
  - System availability and reliability verification
  - Custody transfer metering accuracy verification
- The plan shall define acceptance criteria and testing methods for performance verification
- **Source:** Decomposition §5 PKG-30 (Scope: performance verification); §2 (Project Objectives)

### Interface Requirements

**IR-1: Construction Interface**
- The plan shall define interface with construction: system handover process, construction punch-down, access and logistics
- The plan shall coordinate commissioning activities with ongoing construction work
- **Source:** **ASSUMPTION** — Construction-commissioning interface required; **location TBD** for project interface management requirements

**IR-2: Operations Interface**
- The plan shall define interface with operations: operational readiness criteria, operator training, handover process
- The plan shall coordinate with PKG-35 (Training & Handover) for operational readiness and commissioning support
- **Source:** Decomposition §4 PKG-35 (Training & Handover); **ASSUMPTION** — Operations interface required for successful handover

**IR-3: Regulatory and Permitting Interface**
- The plan shall identify regulatory milestones and authority inspection requirements
- The plan shall coordinate with PKG-32 (Regulatory & Permits) for permit compliance and authority liaison
- The plan shall support regulatory compliance objective (OBJ-6)
- **Source:** Decomposition §2 OBJ-6 (Regulatory Compliance); §4 PKG-32 (Regulatory & Permits)

**IR-4: Testing Interface**
- The plan shall define interface with PKG-29 (Testing) for pre-commissioning testing coordination
- The plan shall identify testing milestones as prerequisites for commissioning
- **Source:** Decomposition §4 PKG-29 (Testing); **ASSUMPTION** — Testing-commissioning interface required

**IR-5: Documentation Interface**
- The plan shall require O&M manuals, vendor documentation, and as-built drawings from PKG-31 as prerequisites for commissioning
- The plan shall define commissioning records management and submittal to DEL-30.03 through DEL-30.08
- **Source:** Decomposition §4 PKG-31 (Documentation & Deliverables); §5 PKG-30 (DEL-30.03 through DEL-30.08: Installation & Test Records)

**IR-6: Dependencies Coordination**
- See `_DEPENDENCIES.md` — Dependencies coordinated externally by humans (NOT_TRACKED mode)
- **Source:** `_DEPENDENCIES.md`

### Quality Requirements

**QR-1: Quality Management Integration**
- The commissioning plan shall integrate with project Quality Management Plan
- The plan shall define quality controls, hold points, witness points for commissioning activities
- **Source:** **ASSUMPTION: standard requirement** for D&B contracts; **location TBD** in Employer's Requirements

**QR-2: Verification and Acceptance**
- The plan shall define verification methods and acceptance criteria for each commissioning phase
- The plan shall define roles and authorities for acceptance decisions
- **Source:** **ASSUMPTION** — Verification and acceptance governance required

**QR-3: Records Management**
- The plan shall define commissioning records requirements, formats, and retention
- The plan shall define records submittal process to DEL-30.03 through DEL-30.08
- **Source:** Decomposition §5 PKG-30 (DEL-30.03 through DEL-30.08: Installation & Test Records)

**QR-4: Plan Maintenance**
- The commissioning plan shall be maintained and updated throughout commissioning execution
- The plan shall define update frequency, revision control, and distribution
- **Source:** **ASSUMPTION** — Living document requires maintenance process; Datasheet.md §Attributes (Review Cycle)

## Standards

**Applicable Codes and Standards:**

**Primary Standards:**
- **IEC 62382** — Electrical and instrumentation loop check — **ASSUMPTION: likely applicable** for commissioning methodology and planning; **location TBD**
- **CSA Z662** — Oil and Gas Pipeline Systems — **ASSUMPTION: likely applicable** for pipeline commissioning requirements; **location TBD**
- **API 653** — Tank Inspection, Repair, Alteration, and Reconstruction — **ASSUMPTION: likely applicable** for tank commissioning; **location TBD**
- **ASME PCC-1** — Guidelines for Pressure Boundary Bolted Flange Joint Assembly — **ASSUMPTION: likely applicable** for mechanical commissioning; **location TBD**

**Source:** **ASSUMPTION** based on T&C discipline and facility systems

**Project-Specific Requirements:**
- Employer's Requirements Volume 2 Part 1 — General Requirements — **TBD: location** for commissioning planning requirements
- Employer's Requirements Volume 2 Part 2 — Civil & Process Mechanical Works — **TBD: location** for system commissioning requirements
- Employer's Requirements Volume 2 Part 3 — Building Works — **TBD: location** (if applicable)

**Source:** Decomposition §3 (Reference Documents)

**Additional Standards:**
- **TBD** — Additional applicable standards to be identified during plan development

## Verification

**Verification Methods for Commissioning Plan:**

**VM-1: Technical Review**
- Plan shall undergo technical review by discipline leads and commissioning team
- Reviewer: Senior T&C engineer or Commissioning Manager
- Acceptance criterion: Technical adequacy verified, scope complete, schedule realistic

**VM-2: Operations Review**
- Plan shall undergo review by operations representative
- Reviewer: Operations Manager or delegate
- Acceptance criterion: Operational readiness criteria adequate, handover process defined

**VM-3: HSE Review**
- Plan shall undergo safety review by HSE representative
- Reviewer: HSE Manager or delegate
- Acceptance criterion: Safety requirements integrated, permit planning adequate

**VM-4: Schedule Integration Review**
- Schedule shall be integrated with construction schedule and validated
- Reviewer: Project planning / scheduling team
- Acceptance criterion: Dependencies correct, critical path identified, resource loading realistic

**VM-5: Regulatory Review**
- Plan shall undergo review for regulatory compliance and permit conditions
- Reviewer: Regulatory affairs / PKG-32 lead
- Acceptance criterion: Regulatory milestones identified, authority inspection requirements defined

**Source:** **ASSUMPTION** — Standard plan verification methods; **location TBD** for project-specific review requirements

**Acceptance Criteria:**
- Commissioning strategy complete and aligned with project objectives
- Organization and responsibilities clearly defined
- Commissioning scope covers all facility systems
- Schedule is integrated, realistic, and supports project milestones
- Safety and permit requirements identified
- Interface management defined (construction, operations, regulatory)
- Risk management and contingency planning adequate
- All required reviews complete and sign-offs obtained

**Source:** **ASSUMPTION** — Standard commissioning plan acceptance criteria

## Documentation

**Required Documentation Outputs:**

1. **Commissioning Plan Document** containing:
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
   - Handover and closeout

2. **Commissioning Schedule** containing:
   - Integrated schedule (pre-commissioning through handover)
   - Dependencies and critical path
   - Milestones and hold points
   - Resource loading
   - Interface with construction schedule

**Source:** Decomposition §5 PKG-30, DEL-30.02 (Anticipated Artifacts); Datasheet.md §Construction

**Documentation Requirements:**

- **Format:** Project-standard plan format — **TBD**
- **Schedule Format:** Primavera P6 or MS Project — **TBD**; integrated with construction schedule
- **Numbering:** Per project document numbering system — **TBD**
- **Revision Control:** Per project document control procedures; living document with periodic updates — **TBD**
- **Distribution:** Controlled distribution to commissioning team, construction, operations, Employer — **TBD**
- **Records Location:** `2_Checking/` (during review) → `3_Issued/` (upon approval)
- **Update Frequency:** Monthly or per milestone — **TBD**
- **Retention:** **TBD** — To be defined per project records management plan

**Source:** **ASSUMPTION** — Standard project document control practices; **location TBD** in Employer's Requirements or project procedures

---

## Document Cross-References

This Specification connects to the other three documents as follows:

- **← Datasheet.md:** Requirements are defined for entities and attributes in Datasheet
  - Datasheet §Construction (Plan content) → This Specification §Requirements FR-1 through FR-8, QR-3
  - Datasheet §Construction (Schedule content) → This Specification §Requirements FR-9, FR-10
  - Datasheet §Conditions (Project objectives) → This Specification §Requirements PR-1
  - Datasheet §Conditions (Facility systems) → This Specification §Requirements FR-3

- **→ Guidance.md:** Engineering rationale provided for each requirement category
  - Specification §Requirements FR-1 (Strategy) → Guidance §Principles P-1
  - Specification §Requirements FR-2 (Organization) → Guidance §Considerations C-1, C-2
  - Specification §Requirements FR-5 through FR-7 (Phased commissioning) → Guidance §Principles P-1
  - Specification §Requirements FR-8 (Safety) → Guidance §Principles P-2
  - Specification §Requirements PR-1 (Operational readiness) → Guidance §Principles P-4
  - Specification §Requirements IR-1 through IR-5 (Interfaces) → Guidance §Considerations C-3, C-4, C-5

- **→ Procedure.md:** Execution steps defined for plan development and maintenance
  - Specification §Requirements FR-1 through FR-10 → Procedure §Steps Phase 2 (Plan development)
  - Specification §Requirements PR-2 (Schedule performance) → Procedure §Steps 2.5, 2.6 (Schedule development)
  - Specification §Requirements QR-4 (Plan maintenance) → Procedure §Steps Phase 4 (Plan monitoring and updates)
  - Specification §Verification → Procedure §Verification (verification of this plan)
