# Datasheet: DEL-30.02 Commissioning Plan

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-30.02 |
| Name | Commissioning Plan |
| Package | PKG-30 Commissioning |
| Discipline | T&C (Testing & Commissioning) |
| Type | Plan |
| Responsible | D&B Contractor (Commissioning Team) |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

**Source:** `_CONTEXT.md`; Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md §5 PKG-30

## Attributes

| Attribute | Value |
|-----------|-------|
| Plan Number | **TBD** — To be assigned per project document numbering system |
| Plan Type | Commissioning Management Plan (strategic and scheduling document) |
| Applicable Phase | Pre-commissioning, Commissioning, Start-up, Performance Verification |
| Review Cycle | **TBD** — Periodic updates per commissioning progress milestones; recommend monthly review during active commissioning |
| Revision | **TBD** — Initial issue to be assigned per project document control procedures; living document during commissioning execution |
| Classification | Project-Controlled Document |
| Planning Horizon | From construction substantial completion through performance acceptance and handover to operations |
| Scope Coverage | Canola oil transload facility commissioning: railcar unloading (32 stations), storage tanks (3×15,000 MT), product transfer & metering, marine loading, electrical, I&C, fire protection, security |

**Source:** Decomposition §1.1 (Key Parameters), §5 PKG-30 (Scope: Pre-commissioning, system commissioning, start-up, performance verification, defect rectification); **ASSUMPTION** — Planning horizon and review cycle based on deliverable type (Plan)

## Conditions

**Operating / Environmental Context:**

This deliverable defines the planned approach and controls for commissioning to meet Employer's Requirements.

**Facility Parameters:**
- Product: CSD (Crude Super Degummed) grade canola oil
- Throughput capacity: 1,000,000 MT per annum (permitted)
- Storage capacity: 45,000 MT (3 × 15,000 MT tanks)
- Railcar unloading: 32 stations on 2 tracks
- Marine loading: Ship loading arms and metering
- Contract type: Design & Build
- Employer: DP World Fraser Surrey Inc.

**Source:** Decomposition §1.1 (Key Parameters, Project Context)

**Project Objectives Supported:**
- OBJ-1: Safe & Reliable Operation — commissioning demonstrates fitness for purpose
- OBJ-2: Throughput Capacity — performance verification confirms 1,000,000 MT/annum capacity
- OBJ-3: Storage Capacity — tank commissioning confirms 45,000 MT storage capacity
- OBJ-4: Operational Flexibility — commissioning verifies tank storage and direct rail-to-ship transfer modes
- OBJ-5: Terminal Continuity — commissioning plan minimizes disturbance to existing terminal operations
- OBJ-6: Regulatory Compliance — commissioning demonstrates compliance with permits and codes
- OBJ-10: Custody Transfer Accuracy — metering system commissioning and proving confirms accuracy

**Source:** Decomposition §2 (Project Objectives), §6 (Objective-to-Deliverable Mapping: PKG-30 → OBJ-1)

**Environmental Conditions:**
- Operating temperature range: **TBD** — Commissioning across multiple seasons likely (typical canola oil handling: -10°C to +50°C ambient)
- Environmental classification: Outdoor industrial facility, coastal marine environment, active terminal
- Hazardous area classification: **TBD** — Commissioning work in classified areas requires hot work permits and area monitoring
- Weather considerations: Marine loading commissioning requires suitable weather and tide conditions
- Seasonal considerations: Winter commissioning may require product heating and freeze protection
- Terminal operations: Commissioning must coordinate with existing terminal commercial activities (OBJ-5)

**Source:** Decomposition §1.1 (Location: Fraser Surrey Terminal); §2 OBJ-5 (Terminal Continuity); **ASSUMPTION** — Environmental factors affecting commissioning scheduling

## Construction

**Materials / Configuration:**

This deliverable produces the following anticipated artifacts:

1. **Commissioning Plan Document:**
   - Executive summary and plan purpose
   - Commissioning strategy and philosophy
   - Commissioning organization and responsibilities
   - Commissioning scope and systems breakdown
   - Commissioning phases and milestones
   - Commissioning procedures framework (reference to DEL-30.01)
   - Safety and permit requirements
   - Quality assurance and verification approach
   - Interface management (construction, operations, regulatory)
   - Resource requirements (personnel, equipment, utilities, consumables)
   - Risk management and contingency planning
   - Records management and documentation requirements
   - Handover and closeout process

2. **Commissioning Schedule:**
   - Integrated commissioning schedule showing:
     - Pre-commissioning activities by system
     - Individual system commissioning by discipline (mechanical, electrical, I&C)
     - Integrated systems commissioning
     - Start-up and first operations
     - Performance verification and acceptance testing
   - Critical path activities and dependencies
   - Resource loading (commissioning team personnel)
   - Milestones and hold points
   - Interface with construction schedule (substantial completion, system handovers)
   - Interface with operations (training, handover, operational readiness)
   - Contingency and float analysis

**Source:** Decomposition §5 PKG-30, DEL-30.02 (Anticipated Artifacts); **ASSUMPTION** — Standard commissioning plan content per IEC 62382 and commissioning management practice

**Plan Format and Structure:**
- Document structure: Per project standard for management plans — **TBD**
- Schedule format: Integrated with construction schedule; recommend Primavera P6 or MS Project format — **TBD**
- Level of detail: Summary level (system-based) for strategic planning; detailed level (activity-based) for near-term execution
- Update frequency: Monthly or per milestone achievement — **TBD**
- Reporting: Progress reporting against plan to project management and Employer — **TBD**

**Source:** **ASSUMPTION** — Plan characteristics based on deliverable type and EPC project management practice

## References

**Primary References:**
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md — Project scope and deliverable definition
- `_CONTEXT.md` — Deliverable identity and description
- Employer's Requirements Volume 2 Parts 1-3 — **TBD: location** — Project-specific commissioning requirements
- DEL-30.01 Commissioning Procedures — Execution methods that this plan governs
- DEL-27.02 Project Execution Plan — **ASSUMPTION: likely exists** — Overall project delivery framework
- Construction Schedule — Interface for commissioning planning and system handover
- DEL-35.01 through DEL-35.05 (Training & Handover) — Interface for operational readiness and handover

**Source:** Decomposition §3 (Reference Documents), §5 (PKG-27: Engineering Design, PKG-35: Training & Handover); `_REFERENCES.md`; **ASSUMPTION** — Interfaces required for commissioning planning

**Applicable Standards:**
- IEC 62382 — Electrical and instrumentation loop check (commissioning methodology)
- CSA Z662 — Oil and Gas Pipeline Systems (commissioning requirements for piping)
- ASME PCC-1 — Guidelines for Pressure Boundary Bolted Flange Joint Assembly
- API 653 — Tank Inspection, Repair, Alteration, and Reconstruction (tank commissioning requirements)
- Employer's Requirements — Project-specific commissioning planning requirements

**Source:** **ASSUMPTION: likely applicable** based on deliverable type (Plan) and discipline (T&C); **location TBD** for specific standard clauses

**Cross-references:**
- See `_DEPENDENCIES.md` — Dependencies coordinated externally (NOT_TRACKED mode)
- PKG-10 through PKG-24 — System design packages provide commissioning scope definition
- PKG-29 (Testing) — Pre-commissioning testing must be complete before system commissioning
- DEL-30.01 (Commissioning Procedures) — Execution methods governed by this plan
- DEL-30.03 through DEL-30.08 — Commissioning records produced during plan execution
- PKG-31 (Documentation & Deliverables) — O&M manuals and as-builts required for commissioning
- PKG-32 (Regulatory & Permits) — Permit conditions and regulatory milestones in commissioning schedule
- PKG-33 (HSE Management) — HSE requirements integrated into commissioning plan
- PKG-35 (Training & Handover) — Operational readiness and handover milestones

**Source:** Decomposition §4, §5 (Package structure); **ASSUMPTION** — Cross-package interfaces required for commissioning planning

---

## Document Cross-References

This Datasheet connects to the other three documents as follows:

- **→ Specification.md:** Requirements are defined for plan content, scheduling, and governance
  - Datasheet §Construction (Commissioning Plan content) → Specification §Requirements FR-1 through FR-8
  - Datasheet §Construction (Commissioning Schedule content) → Specification §Requirements FR-9, FR-10
  - Datasheet §Conditions (Project objectives) → Specification §Requirements PR-1 through PR-4
  - Datasheet §References (Standards) → Specification §Standards

- **→ Guidance.md:** Planning principles and considerations for commissioning strategy development
  - Datasheet §Conditions (Phased commissioning) → Guidance §Principles P-1
  - Datasheet §Conditions (Safety and regulatory objectives) → Guidance §Principles P-2
  - Datasheet §Conditions (Terminal continuity) → Guidance §Principles P-3, §Considerations C-3
  - Datasheet §Construction (Organization and resources) → Guidance §Considerations C-1, C-2

- **→ Procedure.md:** Process for developing, updating, and managing the commissioning plan
  - Datasheet §Construction (Plan content) → Procedure §Steps Phase 2 (Plan development)
  - Datasheet §Construction (Schedule development) → Procedure §Steps 2.5, 2.6
  - Datasheet §Attributes (Review cycle) → Procedure §Steps Phase 4 (Plan monitoring and updates)
