# Guidance: DEL-30.01 Commissioning Procedures

## Purpose

This guidance document supports the development of **Commissioning Procedures** for **PKG-30 Commissioning** in the Canola Oil Transload Facility — Phase 1 Design & Build Contract.

**Deliverable Context:**

Defines the execution method and controls for commissioning to meet safety, quality, and operational requirements.

**Source:** Decomposition §5 PKG-30, DEL-30.01 (Description)

**Deliverable Classification:**
- **Type:** Procedure
- **Discipline:** T&C (Testing & Commissioning)
- **Responsible Party:** D&B Contractor (Commissioning Team)
- **Project Objective Link:** OBJ-1 (Safe & Reliable Operation) — The facility is suitable for safe, efficient, reliable, and continuous use under actual operational conditions

**Source:** `_CONTEXT.md`; Decomposition §2 (Project Objectives), §6 (Objective-to-Deliverable Mapping: PKG-30 → OBJ-1)

**Facility Context:**

This is a CSD canola oil transload facility with:
- 32 railcar unloading stations on 2 tracks
- 3 storage tanks (15,000 MT each, 45,000 MT total)
- Marine loading system (ship loading arms)
- Product transfer, metering, and control systems
- Target throughput: 1,000,000 MT per annum

**Source:** Decomposition §1.1 (Key Parameters)

## Principles

**Engineering Rationale for Commissioning Procedures:**

**P-1: Phased Commissioning Approach**

Commissioning follows a staged progression:
1. **Pre-commissioning:** Prepare systems for commissioning (clean, test, inspect)
2. **Individual system commissioning:** Verify each system operates per design (mechanical, electrical, I&C)
3. **Integrated systems commissioning:** Verify systems work together as designed
4. **Start-up and performance testing:** Introduce product and verify performance under actual operating conditions

This phased approach reduces risk, enables early identification of issues, and supports systematic verification against design intent.

**Source:** **ASSUMPTION** — Industry standard commissioning philosophy; IEC 62382 (commissioning sequence); Decomposition §5 PKG-30 (Scope: Pre-commissioning, system commissioning, start-up, performance verification)

**P-2: Safety as the Foundation**

All commissioning activities must maintain personnel safety and equipment integrity. Commissioning procedures define:
- Required permits (hot work, confined space, lockout/tagout, excavation, working at heights)
- Hazard identification and controls
- Personal protective equipment requirements
- Emergency response provisions
- Safety hold points and witness points

Commissioning in an operating terminal (Fraser Surrey Terminal) requires additional vigilance to minimize disturbance to existing commercial activities (OBJ-5: Terminal Continuity).

**Source:** Decomposition §2 (OBJ-1: Safe & Reliable Operation, OBJ-5: Terminal Continuity); **ASSUMPTION** — Standard HSE requirements for commissioning work; **location TBD** in Employer's Requirements HSE section

**P-3: Systematic Verification Against Design**

Each commissioning procedure must define clear acceptance criteria linked to design requirements. Verification demonstrates:
- Equipment installed per design drawings and specifications
- Systems operate within design parameters
- Safety systems function as intended
- Performance meets design intent

This systematic approach supports regulatory compliance (OBJ-6) and provides documentary evidence of fitness for purpose.

**Source:** Decomposition §2 (OBJ-6: Regulatory Compliance); **ASSUMPTION** — Commissioning governance per IEC 62382; **location TBD** for project-specific verification requirements

**P-4: Integration with Project Delivery**

Commissioning procedures must integrate with:
- **Testing (PKG-29):** Pre-commissioning testing provides verified systems to commission
- **Documentation (PKG-31):** O&M manuals, vendor documentation, and as-built drawings inform commissioning execution
- **Training (PKG-35):** Commissioning procedures serve as training materials and operational readiness tools
- **Regulatory (PKG-32):** Commissioning demonstrates permit compliance and readiness for authority inspections

**Source:** Decomposition §4 (Package Summary: PKG-29, PKG-31, PKG-32, PKG-35); **ASSUMPTION** — Cross-package integration required for commissioning success

**P-5: Product-Specific Considerations**

CSD canola oil is a combustible Class IIIA liquid (flash point > 93°C) with specific handling requirements:
- Temperature control to maintain product quality and pumpability
- Inert gas blanketing to prevent oxidation and maintain product quality
- Clean systems to prevent contamination (food-grade product)
- Custody transfer metering accuracy for commercial operations (OBJ-10)

Commissioning procedures must address product-specific requirements to ensure operational readiness.

**Source:** Decomposition §1.1 (Product: CSD canola oil); §2 (OBJ-10: Custody Transfer Accuracy); **ASSUMPTION** — Canola oil handling characteristics; **location TBD** for product specification and handling requirements

**Applicable Standards Context:**

- **CSA Z662 (Oil and Gas Pipeline Systems):** Provides requirements for pipeline commissioning, hydrostatic testing, and operational readiness — **ASSUMPTION: likely applicable**; **location TBD**
- **IEC 62382 (Electrical and instrumentation loop check):** Defines systematic approach for I&C commissioning and loop checking — **ASSUMPTION: likely applicable**; **location TBD**
- **ASME PCC-1 (Bolted Flange Joint Assembly):** Provides guidelines for pressure boundary integrity during commissioning — **ASSUMPTION: likely applicable**; **location TBD**

**Source:** **ASSUMPTION** based on T&C discipline and facility type

## Considerations

**Factors to Consider During Commissioning Procedure Development:**

**C-1: Package Scope Context**

PKG-30 Commissioning scope includes:
- Pre-commissioning (flushing, cleaning, testing, drying, preservation)
- System commissioning (mechanical, electrical, I&C)
- Start-up (initial product introduction and operations)
- Performance verification (demonstrate design capacity and reliability)
- Defect rectification (punch list management)

Commissioning procedures must support all scope elements and define execution methods for each.

**Source:** Decomposition §5 PKG-30 (Scope)

**C-2: System Complexity and Interdependencies**

The facility comprises multiple interdependent systems:
- Railcar unloading system (PKG-10): 32 stations requiring coordinated commissioning
- Storage tanks (PKG-13): Tank commissioning, cleaning, certification
- Product transfer piping (PKG-14): Pressure testing, flushing, leak detection
- Metering systems (PKG-12): Calibration, proving, custody transfer certification
- Marine loading system (PKG-11): Loading arm commissioning, marine interface coordination
- Control systems (PKG-19): SCADA, interlocks, alarms, safety systems
- Electrical systems (PKG-17, PKG-18): Power-up sequence, motor commissioning, lighting
- Fire protection (PKG-23): Fire detection and suppression system commissioning
- Security systems (PKG-24): Access control, CCTV, intrusion detection

Commissioning procedures must define logical sequencing that respects system interdependencies.

**Source:** Decomposition §4 (Package Summary), §5 (Package Details for PKG-10 through PKG-24); **ASSUMPTION** — System interdependencies require coordinated commissioning approach

**C-3: Coordination with Operations**

Commissioning procedures must support transition from construction to operations:
- Define operational readiness criteria
- Identify operator training requirements
- Define operational handover requirements
- Support development of operating procedures
- Demonstrate operational flexibility (OBJ-4: support tank storage and direct rail-to-ship transfer)

**Source:** Decomposition §2 (OBJ-4: Operational Flexibility); **ASSUMPTION** — Operations involvement required for commissioning success; **location TBD** in Employer's Requirements for handover requirements

**C-4: Deliverable Type Specifics (Procedure)**

As a Procedure-type deliverable, this is inherently recursive:
- It is a procedure that defines how to create and execute other procedures
- It establishes the framework, format, and governance for commissioning execution procedures
- It defines roles, responsibilities, and approval requirements
- It establishes verification and records requirements

The procedure must be both prescriptive (define required elements) and flexible (allow system-specific adaptation).

**Source:** **ASSUMPTION** — Nature of meta-procedure deliverable; **location TBD** for project procedure governance requirements

**C-5: Employer's Requirements Compliance**

Commissioning procedures must demonstrate compliance with Employer's Requirements:
- Specific commissioning requirements — **TBD: location** in Volume 2 Part 1 (General Requirements)
- System-specific commissioning requirements — **TBD: location** in Volume 2 Part 2 (Civil & Process Mechanical Works)
- Building system commissioning requirements — **TBD: location** in Volume 2 Part 3 (Building Works, if applicable)

Review Employer's Requirements thoroughly before finalizing commissioning procedures.

**Source:** Decomposition §3 (Reference Documents: Employer's Requirements Volumes 2 Parts 1-3)

**C-6: Regulatory and Permitting Requirements**

Commissioning procedures must support regulatory compliance:
- Authority having jurisdiction (AHJ) inspection requirements
- Permit conditions and commissioning notifications
- Environmental protection requirements (OBJ-7: adequate containment, spill prevention)
- Transportation Safety Board (TSB) requirements for rail operations
- Transport Canada Marine Safety requirements for ship loading operations
- Vancouver Fraser Port Authority (VFPA) requirements

**Source:** Decomposition §2 (OBJ-6: Regulatory Compliance, OBJ-7: Environmental Protection); **ASSUMPTION** — Regulatory bodies likely involved; **location TBD** for specific requirements

**C-7: Constructability and Field Practicality**

Commissioning procedures must be field-executable:
- Define realistic hold points and witness points
- Allow for field adjustments within approved limits
- Provide clear guidance for non-conformance handling
- Consider construction site constraints (access, logistics, utilities)
- Consider operational terminal constraints (minimize disturbance to existing operations)

**Source:** Decomposition §2 (OBJ-5: Terminal Continuity); **ASSUMPTION** — Field practicality required for procedure effectiveness

**C-8: Operability and Maintainability**

Commissioning procedures should support long-term facility performance:
- Identify operational and maintenance requirements discovered during commissioning
- Feed lessons learned into O&M manuals
- Support lifecycle cost optimization (OBJ-9)
- Verify maintainability and accessibility during commissioning

**Source:** Decomposition §2 (OBJ-9: Lifecycle Cost Optimization); **ASSUMPTION** — Commissioning as opportunity for operability/maintainability verification

**C-9: Future Expandability**

Consider Phase 2 expansion (OBJ-8) when developing commissioning procedures:
- Define interface points that may be extended in future
- Identify systems that may require re-commissioning during expansion
- Document baseline performance for future comparison

**Source:** Decomposition §2 (OBJ-8: Future Expandability)

## Trade-offs

**Competing Concerns to Evaluate:**

**T-1: Prescriptive vs. Flexible Procedures**

**Trade-off:** Highly prescriptive procedures reduce risk of error but may be inflexible for field conditions; flexible procedures empower commissioning team but increase risk of inconsistency.

**Considerations:**
- Balance detailed steps for critical safety/quality activities with performance-based requirements for routine activities
- Define mandatory hold points/witness points while allowing field judgment for execution sequence details
- Provide decision trees for common scenarios while requiring engineering review for unusual conditions

**Recommendation:** Prescriptive for safety-critical and first-of-kind activities; performance-based for well-understood routine activities — **ASSUMPTION**

**T-2: Individual System vs. Integrated Systems Commissioning**

**Trade-off:** Individual system commissioning enables early identification of issues but delays integrated operations readiness; aggressive integrated commissioning reduces schedule but increases troubleshooting complexity.

**Considerations:**
- Individual system commissioning provides verified baseline before integration
- Integrated systems commissioning reveals interface issues and control system behavior
- Schedule pressure may drive early integration, increasing risk

**Recommendation:** Systematic progression from individual to integrated commissioning per IEC 62382; define clear acceptance criteria for each phase — **ASSUMPTION**

**T-3: Completion vs. Schedule Pressure**

**Trade-off:** Complete commissioning verification ensures operational readiness but may extend schedule; expedited commissioning to meet commercial deadlines increases operational risk.

**Considerations:**
- Define minimum acceptable commissioning scope for operational readiness
- Identify activities that can be deferred to post-startup (with appropriate risk assessment)
- Establish clear authority for scope reduction decisions

**Recommendation:** Define non-negotiable commissioning requirements (safety systems, regulatory compliance, custody transfer accuracy) vs. desirable activities that could be deferred — **ASSUMPTION**; **location TBD** for project-specific commissioning acceptance criteria

**T-4: Documentation Rigor vs. Execution Efficiency**

**Trade-off:** Comprehensive documentation provides evidence and traceability but consumes time and resources; streamlined documentation enables faster execution but reduces evidence quality.

**Considerations:**
- Regulatory and contractual requirements for records (PKG-32, Employer's Requirements)
- Quality management requirements for traceability
- Operational handover requirements for baseline documentation

**Recommendation:** Define minimum required documentation (safety, regulatory, warranty, custody transfer) vs. supplementary documentation; leverage digital tools for efficient record capture — **ASSUMPTION**

**T-5: Witness Points and Hold Points**

**Trade-off:** Extensive witness/hold points provide oversight and verification but extend schedule and require coordination; minimal witness/hold points improve efficiency but reduce oversight.

**Considerations:**
- Regulatory requirements for authority inspections
- Employer requirements for witness points — **TBD: location** in Employer's Requirements
- Contractor quality assurance requirements
- Risk level of activity (safety, environmental, quality impact)

**Recommendation:** Mandatory hold points for high-risk activities (pressure testing, first energization, first product introduction); witness points for activities requiring oversight but not requiring stop-work — **ASSUMPTION**; **location TBD** for project-specific witness/hold requirements

## Examples

**Reference Examples and Precedents:**

**E-1: Employer's Requirements**

Refer to Employer's Requirements Volume 2 Parts 1-3 for project-specific commissioning expectations and requirements — **TBD: location** for specific sections.

**Source:** Decomposition §3 (Reference Documents)

**E-2: Industry Standards and Guides**

- **IEC 62382:** Provides example commissioning procedures, loop check sheets, and verification methods for electrical and instrumentation systems
- **ASME PCC-1:** Provides example procedures for bolted flange joint assembly and pressure boundary verification
- **CSA Z662:** Provides requirements and example procedures for pipeline hydrostatic testing and commissioning

**Source:** **ASSUMPTION: likely applicable** standards; **location TBD** for specific example content

**E-3: Similar Facility Precedents**

- **TBD** — Precedent commissioning procedures from similar liquid bulk storage and transfer facilities
- **TBD** — Lessons learned from commissioning of canola oil or edible oil facilities
- **TBD** — Best practices from rail transload terminal commissioning

**Source:** **ASSUMPTION** — Industry precedent would inform procedure development; specific examples TBD

**E-4: Anticipated Artifacts for Reference**

This deliverable will produce the following anticipated artifacts that serve as examples:
1. **Pre-commissioning procedures:**
   - System flushing and cleaning procedures
   - Hydrostatic test procedures
   - Leak test procedures
   - Drying and preservation procedures
   - Pre-commissioning inspection procedures

2. **Commissioning procedures:**
   - Mechanical commissioning procedures (tanks, piping, pumps, valves)
   - Electrical commissioning procedures (power distribution, motors, transformers)
   - I&C commissioning procedures (control systems, instrumentation, safety systems)
   - Integrated systems commissioning procedures

3. **Start-up procedures:**
   - Initial fill and circulation procedures
   - First product receipt procedures (rail and ship)
   - System performance verification procedures
   - Operational readiness verification procedures

**Source:** Decomposition §5 PKG-30, DEL-30.01 (Anticipated Artifacts); **ASSUMPTION** — Expanded detail based on facility scope

**E-5: Cross-Package Reference Documents**

Commissioning procedures should reference:
- **PKG-10 through PKG-16:** System design documents (drawings, specifications, calculations) define what to verify during commissioning
- **PKG-19, PKG-20:** Control system and instrumentation documents define loop checking and functional testing requirements
- **PKG-23:** Fire protection system commissioning procedures
- **PKG-29:** Testing procedures and test records provide verified baseline for commissioning
- **PKG-31:** O&M manuals and vendor documentation provide operating parameters and commissioning guidance

**Source:** Decomposition §4, §5 (Package structure); **ASSUMPTION** — Cross-package integration required

## Conflict Table (for human ruling)

No conflicts identified during document enrichment. If conflicts arise during procedure development, they will be documented here using this format:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none) | | | | | | |

**Note:** Cross-deliverable conflicts are handled by RECONCILIATION agent when requested; this table captures only local conflicts within DEL-30.01 scope.

---

## Document Cross-References

This Guidance connects to the other three documents as follows:

- **← Datasheet.md:** Engineering rationale is provided for entities and attributes identified in Datasheet
  - Datasheet §Conditions (Facility parameters) → This Guidance §Purpose (Facility context)
  - Datasheet §Construction (Phased artifacts) → This Guidance §Principles P-1 (Phased commissioning approach)
  - Datasheet §Conditions (Product: CSD canola oil) → This Guidance §Principles P-5 (Product-specific considerations)
  - Datasheet §References (Standards) → This Guidance §Principles (Applicable standards context)

- **← Specification.md:** Engineering rationale is provided for each requirement category
  - Specification §Requirements FR-1 through FR-6 (Functional) → This Guidance §Principles P-1, P-3, P-4
  - Specification §Requirements FR-5 (Safety integration) → This Guidance §Principles P-2 (Safety as the foundation)
  - Specification §Requirements PR-1 through PR-3 (Performance) → This Guidance §Principles P-1, P-3, P-5
  - Specification §Requirements IR-1 through IR-6 (Interfaces) → This Guidance §Principles P-4 (Integration with project delivery), §Considerations C-2 (System interdependencies)
  - Specification §Requirements QR-1 through QR-4 (Quality) → This Guidance §Principles P-3 (Systematic verification)
  - Specification §Standards → This Guidance §Principles (Applicable standards context)

- **→ Procedure.md:** Considerations inform procedure development decisions and trade-offs
  - Guidance §Principles P-1 (Phased approach) → Procedure §Steps 1.1 (Scope definition by phase)
  - Guidance §Principles P-2 (Safety foundation) → Procedure §Steps 2.2 (Safety requirements)
  - Guidance §Principles P-3 (Systematic verification) → Procedure §Steps 2.5 (Verification criteria)
  - Guidance §Principles P-4 (Integration) → Procedure §Steps 2.3 (Prerequisites and dependencies)
  - Guidance §Considerations C-1 through C-9 → Procedure §Steps Phase 1 (Scope definition and planning)
  - Guidance §Trade-offs T-1 through T-5 → Procedure development decisions and risk-based approach
