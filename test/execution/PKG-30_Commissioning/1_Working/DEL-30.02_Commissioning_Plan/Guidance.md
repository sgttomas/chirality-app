# Guidance: DEL-30.02 Commissioning Plan

## Purpose

This guidance document supports the development of **Commissioning Plan** for **PKG-30 Commissioning** in the Canola Oil Transload Facility — Phase 1 Design & Build Contract.

**Deliverable Context:**

Defines the planned approach and controls for commissioning to meet Employer's Requirements.

**Source:** Decomposition §5 PKG-30, DEL-30.02 (Description)

**Deliverable Classification:**
- **Type:** Plan (strategic commissioning management document)
- **Discipline:** T&C (Testing & Commissioning)
- **Responsible Party:** D&B Contractor (Commissioning Team)
- **Project Objective Link:** OBJ-1 (Safe & Reliable Operation), OBJ-2 (Throughput Capacity), OBJ-3 (Storage Capacity)

**Source:** `_CONTEXT.md`; Decomposition §2, §6 (PKG-30 → OBJ-1)

## Principles

**P-1: Phased Commissioning Strategy**

Commissioning plans follow a structured, phased approach to systematically build confidence in facility readiness:

1. **Pre-commissioning:** Clean, test, and prepare systems
2. **Individual system commissioning:** Verify each discipline (mechanical, electrical, I&C)
3. **Integrated systems commissioning:** Verify systems work together
4. **Start-up:** Introduce product and verify first operations
5. **Performance verification:** Confirm design capacity and acceptance criteria

This phased strategy reduces risk, enables early issue identification, and provides governance checkpoints. The plan defines the strategy, sequence, and acceptance criteria for each phase.

**Source:** IEC 62382 (commissioning methodology); Decomposition §5 PKG-30 (Scope: Pre-commissioning, system commissioning, start-up, performance verification, defect rectification)

**P-2: Safety and Risk Management**

The commissioning plan must prioritize personnel safety and equipment integrity. Safety planning includes:
- Identifying hazardous activities and required permits
- Defining safety precautions and emergency response
- Integrating with project HSE management (PKG-33)
- Minimizing disturbance to existing terminal operations (OBJ-5: Terminal Continuity)

Risk management identifies commissioning risks (technical, schedule, resource, interface) and defines mitigation strategies and contingencies.

**Source:** Decomposition §2 OBJ-1 (Safe & Reliable Operation), OBJ-5 (Terminal Continuity); PKG-33 (HSE Management)

**P-3: Interface Management**

Effective commissioning requires clear interface management:
- **Construction interface:** System handover criteria, access, logistics
- **Operations interface:** Operational readiness, training, handover process
- **Regulatory interface:** Authority inspections, permit compliance
- **Testing interface:** Pre-commissioning test coordination (PKG-29)
- **Documentation interface:** As-builts, O&M manuals, vendor docs (PKG-31)

The plan defines how these interfaces will be managed throughout commissioning.

**Source:** Decomposition §4 (PKG-29, PKG-31, PKG-32, PKG-33, PKG-35); **ASSUMPTION** — Interface management critical for commissioning success

**P-4: Operational Readiness Focus**

The commissioning plan's ultimate goal is demonstrating operational readiness:
- Facility suitable for safe, reliable, continuous operation (OBJ-1)
- Design capacity confirmed: 1,000,000 MT/annum throughput (OBJ-2), 45,000 MT storage (OBJ-3)
- Operational flexibility verified: tank storage and direct rail-to-ship modes (OBJ-4)
- Custody transfer accuracy confirmed (OBJ-10)

The plan defines acceptance criteria that link commissioning activities to these operational readiness objectives.

**Source:** Decomposition §2 (Project Objectives: OBJ-1, OBJ-2, OBJ-3, OBJ-4, OBJ-10)

## Considerations

**C-1: Commissioning Organization and Resources**

The plan must define:
- Organization structure: roles, responsibilities, authorities
- Key personnel: Commissioning Manager, discipline leads, QA/QC, HSE, operations liaison
- Resource requirements: commissioning team personnel, equipment (test equipment, temporary utilities), consumables
- Resource constraints: availability, cost, schedule impact
- Decision-making and escalation processes

Consider commissioning team size and skills required for facility complexity (32 railcar stations, 3 tanks, marine loading, extensive I&C systems).

**Source:** Decomposition §1.1 (Key Parameters: facility scale); **ASSUMPTION** — Resource planning critical for execution readiness

**C-2: Commissioning Scope and System Breakdown**

The plan must define commissioning scope for all facility systems:
- Railcar unloading system: 32 stations, product transfer pumps, valving
- Storage tanks: 3×15,000 MT tanks, instrumentation, level gauging
- Product transfer piping: Transfer lines, manifolds
- Metering systems: Custody transfer meters, proving systems (high criticality)
- Marine loading: Loading arms, gangway, manifold
- Electrical systems: Power distribution, motors, lighting
- I&C systems: SCADA, PLCs, field instruments, interlocks, alarms
- Fire protection: Detection, suppression systems
- Security systems: Access control, CCTV

Consider system complexity, interdependencies, and specialized commissioning requirements (e.g., metering proving requires specialized expertise).

**Source:** Decomposition §1.1 (Key Parameters), §4 (PKG-10 through PKG-24)

**C-3: Terminal Continuity (Active Operations)**

Fraser Surrey Terminal is an operating facility. The commissioning plan must:
- Minimize disturbance to existing commercial activities (OBJ-5)
- Coordinate work schedules to avoid conflicts with terminal operations
- Define access routes and logistics that don't impede existing operations
- Plan marine loading commissioning around existing terminal ship traffic
- Consider noise, dust, and safety impacts on adjacent operations

This constraint significantly affects commissioning schedule flexibility and work windows.

**Source:** Decomposition §1.1 (Location: Fraser Surrey Terminal), §2 OBJ-5 (Terminal Continuity)

**C-4: Regulatory and Permitting Considerations**

The plan must address:
- Authority inspection requirements and witness points
- Permit conditions affecting commissioning (environmental, marine, rail)
- Transportation Safety Board (TSB) requirements for rail operations
- Transport Canada Marine Safety requirements for ship loading
- Vancouver Fraser Port Authority (VFPA) requirements and coordination
- Environmental protection requirements (OBJ-7)

Regulatory milestones often drive critical path and must be integrated into commissioning schedule.

**Source:** Decomposition §2 (OBJ-6: Regulatory Compliance, OBJ-7: Environmental Protection); §4 PKG-32 (Regulatory & Permits)

**C-5: Schedule Integration and Critical Path**

The commissioning schedule must:
- Integrate with construction schedule (system handover dates as inputs)
- Show dependencies between commissioning activities
- Identify critical path activities
- Define milestones and schedule contingency
- Support contractual delivery milestones — **TBD: location**
- Consider seasonal factors (winter freeze protection, marine loading weather/tide windows)

Schedule performance is critical to project delivery success.

**Source:** **ASSUMPTION** — Schedule integration required for project coordination; **location TBD** for contractual milestones

**C-6: Performance Verification Planning**

Performance verification demonstrates facility achieves design intent:
- Throughput capacity: Verify 1,000,000 MT/annum capacity through run tests
- Storage capacity: Verify tank capacity and instrumentation accuracy
- Custody transfer metering: Prove meter accuracy per custody transfer requirements
- System reliability: Verify continuous operation capability
- Operational flexibility: Demonstrate tank storage and direct rail-to-ship modes

Define test methods, acceptance criteria, duration, and data collection requirements.

**Source:** Decomposition §2 (OBJ-2, OBJ-3, OBJ-4, OBJ-10); §5 PKG-30 (Scope: performance verification)

**C-7: Living Document Management**

The commissioning plan is a living document:
- Initial plan provides strategic framework and baseline schedule
- Plan must be updated as commissioning progresses (monthly or per milestones)
- Updates reflect actual progress, changes, lessons learned
- Version control and distribution critical for team alignment

Define update frequency, revision process, and distribution in the plan.

**Source:** Datasheet.md §Attributes (Review Cycle); **ASSUMPTION** — Plan maintenance required throughout commissioning

## Trade-offs

**T-1: Schedule Aggressiveness vs. Risk Mitigation**

**Trade-off:** Aggressive commissioning schedule reduces project duration but increases risk of rework and quality issues; conservative schedule provides margin but extends project delivery.

**Considerations:**
- Contractual delivery milestones and liquidated damages
- Resource availability and cost
- System complexity and likelihood of issues
- Interface constraints (terminal operations, seasonal factors)
- Employer's operational start-up requirements

**Recommendation:** Balanced approach with realistic schedule, identified critical path, and defined contingency (float); schedule risk analysis to quantify confidence — **ASSUMPTION**

**T-2: Resource Loading vs. Cost**

**Trade-off:** Large commissioning team enables faster execution but increases cost; smaller team reduces cost but extends schedule.

**Considerations:**
- Schedule criticality and contractual milestones
- Commissioning team accommodation and logistics in terminal environment
- Availability of skilled commissioning personnel (specialized roles like metering specialists)
- Lifecycle cost optimization (OBJ-9) — efficient commissioning reduces long-term costs

**Recommendation:** Right-size team for critical path activities; avoid over-resourcing non-critical activities; consider local hiring where feasible — **ASSUMPTION**

**T-3: Integration Testing Scope vs. Complexity**

**Trade-off:** Comprehensive integrated systems testing provides high confidence but is complex and time-consuming; limited integration testing enables faster start-up but increases operational risk.

**Considerations:**
- System complexity and interdependencies (extensive I&C, multiple transfer paths)
- Safety criticality (fire protection, emergency shutdown, interlocks)
- Operational readiness requirements (OBJ-1: Safe & Reliable Operation)
- Performance verification requirements (OBJ-2, OBJ-3, OBJ-10)
- Employer's acceptance criteria

**Recommendation:** Define risk-based integration testing scope; comprehensive testing for safety-critical systems; streamlined testing for well-understood standalone systems — **ASSUMPTION**

**T-4: Pre-commissioning Testing Rigor vs. Schedule**

**Trade-off:** Rigorous pre-commissioning testing ensures clean, tight systems but extends schedule; expedited pre-commissioning enables faster commissioning start but risks defects impacting commissioning quality.

**Considerations:**
- Product purity requirements (food-grade canola oil)
- Custody transfer metering accuracy requirements (contamination impacts accuracy)
- System complexity (extensive piping, 32 railcar stations, 3 tanks)
- Warranty and insurance implications of inadequate pre-commissioning
- Rework cost and schedule impact if defects found during commissioning

**Recommendation:** Do not compromise pre-commissioning testing quality; cost and schedule impact of rework far exceeds pre-commissioning effort — **ASSUMPTION**

## Examples

**E-1: Employer's Requirements**

Refer to Employer's Requirements Volume 2 Parts 1-3 for project-specific commissioning planning requirements — **TBD: location**

**Source:** Decomposition §3 (Reference Documents)

**E-2: Industry Standards and Guidance**

- **IEC 62382:** Provides commissioning methodology, organization models, and planning frameworks for electrical and I&C systems
- **API 653:** Provides tank commissioning requirements and acceptance criteria
- **CSA Z662:** Provides pipeline commissioning and startup requirements

**Source:** **ASSUMPTION: likely applicable**; **location TBD** for specific guidance content

**E-3: Anticipated Artifacts**

This deliverable produces:

1. **Commissioning Plan Document:** Comprehensive commissioning management document covering strategy, organization, scope, safety, interfaces, resources, risk management, handover

2. **Commissioning Schedule:** Integrated schedule showing pre-commissioning through performance verification with dependencies, critical path, milestones, resource loading

**Source:** Decomposition §5 PKG-30, DEL-30.02 (Anticipated Artifacts); Datasheet.md §Construction

**E-4: Key Plan Sections (Example Structure)**

- Section 1: Executive Summary
- Section 2: Commissioning Strategy and Philosophy
- Section 3: Organization and Responsibilities
- Section 4: Commissioning Scope and System Breakdown
- Section 5: Commissioning Phases and Approach
- Section 6: Safety and Permit Planning
- Section 7: Quality Assurance and Verification
- Section 8: Interface Management
- Section 9: Resource Requirements
- Section 10: Risk Management and Contingency
- Section 11: Records Management
- Section 12: Commissioning Schedule (integrated schedule document)
- Section 13: Handover and Closeout Process

**Source:** **ASSUMPTION** — Typical commissioning plan structure

---

## Document Cross-References

- **← Datasheet.md:** Rationale for plan attributes and scope
  - Datasheet §Conditions (Project objectives) → This Guidance §Principles P-4
  - Datasheet §Conditions (Phased commissioning) → This Guidance §Principles P-1
  - Datasheet §Construction (Plan content) → This Guidance §Considerations C-1, C-2

- **← Specification.md:** Rationale for requirements
  - Specification §Requirements FR-1 (Strategy) → This Guidance §Principles P-1
  - Specification §Requirements FR-2 (Organization) → This Guidance §Considerations C-1
  - Specification §Requirements FR-3 (Scope) → This Guidance §Considerations C-2
  - Specification §Requirements FR-8 (Safety) → This Guidance §Principles P-2
  - Specification §Requirements PR-1 (Operational readiness) → This Guidance §Principles P-4
  - Specification §Requirements IR-1 through IR-5 → This Guidance §Principles P-3

- **→ Procedure.md:** Considerations inform plan development decisions
  - Guidance §Principles P-1 → Procedure §Steps 2.2 (Strategy development)
  - Guidance §Considerations C-1, C-2 → Procedure §Steps 2.3, 2.4 (Organization, scope)
  - Guidance §Considerations C-5 → Procedure §Steps 2.5, 2.6 (Schedule development)
  - Guidance §Trade-offs → Procedure plan development decisions
