# Specification: DEL-30.01 Commissioning Procedures

## Scope

This specification defines the requirements for **Commissioning Procedures** within **PKG-30 Commissioning** for the Canola Oil Transload Facility — Phase 1 Design & Build Contract.

**Project Context:**
- Employer: DP World Fraser Surrey Inc.
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- Contract Type: Design & Build
- Facility Type: CSD canola oil transload (rail-to-storage-to-ship)

**Source:** Decomposition §1 (Project Context)

**Deliverable Purpose:**

Defines the execution method and controls for commissioning to meet safety, quality, and operational requirements.

**Source:** Decomposition §5 PKG-30, DEL-30.01 (Description)

**Anticipated Deliverable Artifacts:**
- Pre-commissioning procedures
- Commissioning procedures
- Start-up procedures

**Source:** Decomposition §5 PKG-30, DEL-30.01 (Anticipated Artifacts)

**Scope Boundaries:**

**Included:**
- Execution methods for pre-commissioning, commissioning, and start-up activities
- Safety controls and permit requirements for commissioning work
- Quality controls and acceptance criteria for commissioning verification
- Integration with project Quality Management Plan
- Coordination requirements with operations, testing, and other packages

**Excluded:**
- Employer-responsible commissioning activities — **TBD: location** in Employer's Requirements
- Specific system commissioning results (captured in DEL-30.04, DEL-30.05, DEL-30.06)
- Performance testing procedures (separate deliverable: DEL-30.06)
- Operation and maintenance procedures post-commissioning (covered in PKG-31 O&M Manuals)

**Source:** Decomposition §1.2 (Scope Focus: Contractor scope only, Employer items excluded); **ASSUMPTION** — Typical commissioning procedure scope boundaries

## Requirements

### Functional Requirements

**FR-1: Procedure Structure**
- Each commissioning procedure shall define: purpose, scope, safety requirements, prerequisites, step-by-step execution instructions, verification criteria, and records requirements
- **Source:** **ASSUMPTION** — Standard procedure format per IEC 62382 and industry practice; **location TBD**

**FR-2: Pre-commissioning Coverage**
- Pre-commissioning procedures shall address system flushing, cleaning, hydrostatic testing, leak testing, drying, and preservation
- **Source:** Decomposition §5 PKG-30 (Scope: Pre-commissioning); **ASSUMPTION** — Typical pre-commissioning activities for liquid product systems

**FR-3: Commissioning Coverage**
- Commissioning procedures shall address mechanical, electrical, and I&C systems commissioning in a logical sequence to support integrated systems testing
- **Source:** Decomposition §5 PKG-30 (Scope: system commissioning); DEL-30.04 (Mechanical, electrical, I&C commissioning records)

**FR-4: Start-up Coverage**
- Start-up procedures shall address initial product introduction, first operations (railcar unloading and ship loading), and performance verification
- **Source:** Decomposition §5 PKG-30 (Scope: start-up, performance verification); Project Objectives §2 OBJ-1 (Safe & Reliable Operation)

**FR-5: Safety Integration**
- All commissioning procedures shall identify required permits, lockout/tagout requirements, confined space entry requirements, hot work requirements, and hazardous area precautions as applicable
- **Source:** **ASSUMPTION: likely required** per project HSE requirements (PKG-33); **location TBD** in Employer's Requirements

**FR-6: Systems Coverage**
- Commissioning procedures shall cover all facility systems including:
  - Railcar unloading system (32 stations, 2 tracks)
  - Storage tanks (3 × 15,000 MT)
  - Product transfer and metering systems
  - Marine loading system (ship loading arms)
  - Electrical power distribution
  - Control systems and instrumentation
  - Fire protection and safety systems
- **Source:** Decomposition §1.1 (Key Parameters), §4 (Package Summary: PKG-10 through PKG-24)

### Performance Requirements

**PR-1: Operational Readiness**
- Commissioning procedures shall ensure the facility achieves operational readiness to support:
  - Throughput capacity: 1,000,000 MT per annum
  - Storage capacity: 45,000 MT (3 × 15,000 MT tanks)
  - Safe and reliable continuous operation
- **Source:** Decomposition §2 (Objectives: OBJ-1 Safe & Reliable Operation, OBJ-2 Throughput Capacity, OBJ-3 Storage Capacity)

**PR-2: Verification Criteria**
- Each procedure shall define clear acceptance criteria for commissioning completion and readiness for the next phase
- **Source:** **ASSUMPTION** — Required for commissioning governance; **location TBD** in Employer's Requirements

**PR-3: Integrated Systems Readiness**
- Commissioning procedures shall support progression from individual system commissioning to integrated systems testing per DEL-30.05
- **Source:** Decomposition §5 PKG-30 (DEL-30.05: Integrated Systems Test records); **ASSUMPTION** — Commissioning sequence logic

### Interface Requirements

**IR-1: Testing Package Interface**
- Pre-commissioning procedures shall coordinate with PKG-29 (Testing) deliverables for hydrostatic testing, leak testing, and other pre-commissioning test activities
- **Source:** Decomposition §4 (PKG-29: Testing); **ASSUMPTION** — Interface coordination required; **location TBD** for specific coordination requirements

**IR-2: Documentation Package Interface**
- Commissioning procedures shall reference and utilize O&M manuals, vendor documentation, and as-built drawings from PKG-31
- **Source:** Decomposition §5 PKG-31 (DEL-31.03 Operation Manuals, DEL-31.04 Maintenance Manuals, DEL-31.05 Vendor Documentation)

**IR-3: Training & Handover Interface**
- Commissioning procedures shall support training activities and operational handover per PKG-35
- **Source:** Decomposition §4 (PKG-35: Training & Handover); **ASSUMPTION** — Commissioning procedures used for training; **location TBD**

**IR-4: Permit & Regulatory Interface**
- Commissioning procedures shall comply with permit conditions and regulatory requirements per PKG-32
- **Source:** Decomposition §4 (PKG-32: Regulatory & Permits); §2 OBJ-6 (Regulatory Compliance)

**IR-5: HSE Management Interface**
- Commissioning procedures shall integrate with project HSE management system per PKG-33
- **Source:** Decomposition §4 (PKG-33: HSE Management); **ASSUMPTION** — HSE integration required for all commissioning work

**IR-6: Dependencies Coordination**
- See `_DEPENDENCIES.md` — Dependencies coordinated externally by humans (NOT_TRACKED mode)
- **Source:** `_DEPENDENCIES.md`

### Quality Requirements

**QR-1: Quality Management Plan Compliance**
- All commissioning procedures shall comply with the project Quality Management Plan
- **Source:** **ASSUMPTION: standard requirement** for D&B contracts; **location TBD** in Employer's Requirements

**QR-2: Procedure Verification**
- All commissioning procedures shall undergo technical review, safety review, and approval prior to use
- **Source:** **ASSUMPTION** — Standard procedure governance; **location TBD** in project quality procedures

**QR-3: Records Management**
- Commissioning procedures shall define what records must be generated, format requirements, and retention requirements
- **Source:** Decomposition §5 PKG-30 (DEL-30.03, DEL-30.04: Installation & Test Records); **ASSUMPTION** — Records defined in procedures

**QR-4: Revision Control**
- Commissioning procedures shall be maintained under project document control with revision tracking
- **Source:** **ASSUMPTION: standard requirement** for controlled project documents; **location TBD** in project document control procedures

## Standards

**Applicable Codes and Standards:**

**Primary Standards:**
- **CSA Z662** — Oil and Gas Pipeline Systems — **ASSUMPTION: likely applicable** for canola oil product piping commissioning; **location TBD** for specific clauses
- **IEC 62382** — Electrical and instrumentation loop check — **ASSUMPTION: likely applicable** for I&C commissioning procedures; **location TBD**
- **ASME PCC-1** — Guidelines for Pressure Boundary Bolted Flange Joint Assembly — **ASSUMPTION: likely applicable** for mechanical commissioning; **location TBD**

**Source:** **ASSUMPTION** based on T&C discipline and deliverable type (Procedure)

**Project-Specific Requirements:**
- Employer's Requirements Volume 2 Part 1 — General Requirements — **TBD: location** for commissioning requirements
- Employer's Requirements Volume 2 Part 2 — Civil & Process Mechanical Works — **TBD: location** for system-specific commissioning requirements
- Employer's Requirements Volume 2 Part 3 — Building Works — **TBD: location** (if applicable to commissioning)

**Source:** Decomposition §3 (Reference Documents)

**Additional Standards:**
- Vancouver Fraser Port Authority (VFPA) standards and requirements — **TBD: location** — **ASSUMPTION: likely applicable** given terminal location
- BC provincial regulations and WorkSafeBC requirements — **ASSUMPTION: likely applicable** for safety and permitting
- **TBD** — Additional applicable standards to be identified during procedure development

## Verification

**Verification Methods for Commissioning Procedures:**

**VM-1: Technical Review**
- Each procedure shall undergo technical review by discipline lead(s) to verify technical adequacy and completeness
- Reviewer: Qualified T&C / discipline engineer
- Acceptance criterion: Technical review sign-off

**VM-2: Safety Review**
- Each procedure shall undergo safety review (JSA / HAZOP as applicable) to identify hazards and verify safety controls
- Reviewer: HSE representative and operations representative
- Acceptance criterion: Safety review approval with identified hazards controlled

**VM-3: Walkthrough / Tabletop Review**
- Each procedure shall undergo tabletop or field walkthrough to verify executability and identify issues
- Participants: Commissioning team, operations, maintenance, HSE
- Acceptance criterion: Walkthrough completion with action items closed

**VM-4: Competency Verification**
- Personnel executing commissioning procedures shall have verified competency for the work scope
- Method: Training records, qualification records, competency assessment
- Acceptance criterion: Competency verification documented

**VM-5: Trial Run (where practical)**
- Complex or high-risk procedures should undergo trial run or simulation prior to actual execution
- Method: Dry run with equipment de-energized or isolated; simulation
- Acceptance criterion: Trial run successful with lessons learned incorporated

**Source:** **ASSUMPTION** — Standard verification methods for procedure deliverables; IEC 62382 (loop checking); **location TBD** for project-specific verification requirements

**Acceptance Criteria:**
- Procedure technically complete and accurate
- Safety hazards identified and controlled
- Prerequisites clearly defined
- Step sequence logical and executable
- Verification criteria measurable
- Records requirements defined
- Approval sign-offs obtained

**Source:** **ASSUMPTION** — Standard procedure acceptance criteria; **location TBD** in project quality procedures

## Documentation

**Required Documentation Outputs:**

1. **Pre-commissioning Procedures:**
   - System flushing and cleaning procedures
   - Hydrostatic test procedures
   - Leak test procedures
   - Drying and preservation procedures
   - Pre-commissioning inspection procedures

2. **Commissioning Procedures:**
   - Mechanical commissioning procedures (by system)
   - Electrical commissioning procedures (by system)
   - I&C commissioning procedures (by system)
   - Integrated systems commissioning procedures

3. **Start-up Procedures:**
   - Initial fill and circulation procedures
   - First product receipt procedures (rail and ship)
   - System performance verification procedures
   - Operational readiness verification procedures

**Source:** Decomposition §5 PKG-30, DEL-30.01 (Anticipated Artifacts); **ASSUMPTION** — Expanded detail based on facility scope

**Documentation Requirements:**

- **Format:** Project-standard procedure format — **TBD** — **ASSUMPTION**: Per project document management requirements
- **Numbering:** Per project document numbering system — **TBD**
- **Revision Control:** Per project document control procedures — **TBD**
- **Distribution:** Controlled distribution per project document control procedures — **TBD**
- **Records Storage:** Electronic records in project document management system — **ASSUMPTION**
- **Records Location:** `2_Checking/` (during review) → `3_Issued/` (upon approval)
- **Retention:** **TBD** — To be defined per project records management plan

**Source:** **ASSUMPTION** — Standard project document control practices; **location TBD** in Employer's Requirements or project procedures

---

## Document Cross-References

This Specification connects to the other three documents as follows:

- **← Datasheet.md:** Entities and attributes defined in Datasheet have requirements specified here
  - Datasheet §Construction (Anticipated artifacts) → This Specification §Requirements FR-2, FR-3, FR-4
  - Datasheet §Conditions (Facility parameters) → This Specification §Requirements FR-6
  - Datasheet §References (Standards) → This Specification §Standards

- **→ Guidance.md:** Engineering rationale is provided for each requirement category
  - Specification §Requirements (Functional) → Guidance §Principles P-1, P-3
  - Specification §Requirements (Safety: FR-5) → Guidance §Principles P-2
  - Specification §Requirements (Performance: PR-1) → Guidance §Principles P-5 (Product-specific considerations)
  - Specification §Requirements (Interface: IR-1 through IR-5) → Guidance §Principles P-4 (Integration with Project Delivery)
  - Specification §Requirements (Quality: QR-1 through QR-4) → Guidance §Principles P-3 (Systematic verification)

- **→ Procedure.md:** Verification methods and execution steps are defined for each requirement
  - Specification §Requirements FR-1 (Procedure structure) → Procedure §Steps 2.1 (Framework), 2.4 (Execution instructions)
  - Specification §Requirements FR-2 (Pre-commissioning) → Procedure §Steps 1.1 (Scope definition), §Records (Pre-commissioning outputs)
  - Specification §Requirements FR-3 (Commissioning) → Procedure §Steps 1.1 (System commissioning scope), §Records (Commissioning outputs)
  - Specification §Requirements FR-4 (Start-up) → Procedure §Steps 1.1 (Start-up scope), §Records (Start-up outputs)
  - Specification §Requirements FR-5 (Safety) → Procedure §Steps 2.2 (Safety requirements and permits)
  - Specification §Requirements FR-6 (Systems coverage) → Procedure §Steps 1.1 (Identify commissioning scope)
  - Specification §Requirements PR-1, PR-2, PR-3 (Performance) → Procedure §Steps 1.3 (Objectives and acceptance criteria), 2.5 (Verification criteria)
  - Specification §Requirements IR-1 through IR-6 (Interfaces) → Procedure §Steps 2.3 (Prerequisites and dependencies)
  - Specification §Requirements QR-1, QR-2 (Quality) → Procedure §Steps Phase 3 (Review and approval)
  - Specification §Requirements QR-3 (Records) → Procedure §Steps 2.6 (Records and documentation), §Records
  - Specification §Requirements QR-4 (Revision control) → Procedure §Steps Phase 5 (Revision and change management)
  - Specification §Verification → Procedure §Verification (verification of this procedure itself)
