# Datasheet: DEL-30.01 Commissioning Procedures

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-30.01 |
| Name | Commissioning Procedures |
| Package | PKG-30 Commissioning |
| Discipline | T&C (Testing & Commissioning) |
| Type | Procedure |
| Responsible | D&B Contractor (Commissioning Team) |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

**Source:** `_CONTEXT.md`; Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md §5 PKG-30

## Attributes

| Attribute | Value |
|-----------|-------|
| Procedure Number | **TBD** — To be assigned per project document numbering system |
| Procedure Type | Method Procedure (defines execution methods for commissioning activities) |
| Applicable Phase | Pre-commissioning, Commissioning, Start-up |
| Revision | **TBD** — Initial issue to be assigned per project document control procedures |
| Classification | Project-Controlled Document |
| Scope Coverage | Canola oil transload facility systems: railcar unloading, storage tanks (3×15,000 MT), product transfer & metering, marine loading |

**Source:** Decomposition §1.1 (Key Parameters), §5 PKG-30 (Scope: Pre-commissioning, system commissioning, start-up, performance verification, defect rectification)

## Conditions

**Operating / Environmental Context:**

This deliverable defines the execution method and controls for commissioning to meet safety, quality, and operational requirements for a canola oil transload facility.

**Facility Parameters:**
- Product: CSD (Crude Super Degummed) grade canola oil
- Throughput capacity: 1,000,000 MT per annum (permitted)
- Storage capacity: 45,000 MT (3 × 15,000 MT tanks)
- Railcar unloading: 32 stations on 2 tracks
- Marine loading: Ship loading arms and metering

**Source:** Decomposition §1.1 (Key Parameters)

**Environmental Conditions:**
- Operating temperature range: **TBD** — To be confirmed from process design basis (typical canola oil handling: -10°C to +50°C ambient, product temp 15-40°C) — **ASSUMPTION**
- Environmental classification: Outdoor industrial facility, coastal marine environment
- Hazardous area classification: **TBD** — To be confirmed per facility hazardous area classification study; canola oil is combustible Class IIIA liquid (flash point > 93°C) — **ASSUMPTION**
- Seismic requirements: High seismic zone per NBC 2020 for Surrey, BC location — **ASSUMPTION: likely applicable**
- Design life: **TBD** — Typical industrial facility 25-30 years — **ASSUMPTION**

**Source:** Decomposition §1.1 (Location: Fraser Surrey Terminal, Surrey, BC); **location TBD** for specific environmental design parameters

## Construction

**Materials / Configuration:**

This deliverable produces the following anticipated artifacts:

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

**Source:** Decomposition §5 PKG-30, DEL-30.01 (Anticipated Artifacts)

**Procedure Format Elements:**
- Purpose and scope definition
- Safety precautions and permits required
- Prerequisites and dependencies
- Step-by-step execution instructions
- Hold points and witness points
- Verification and acceptance criteria
- Records and documentation requirements
- Sign-off and approval requirements

**Source:** **ASSUMPTION** — Standard commissioning procedure format per industry practice (IEC 62382, ASME PCC-1)

## References

**Primary References:**
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md — Project scope and deliverable definition
- `_CONTEXT.md` — Deliverable identity and description
- Employer's Requirements Volume 2 Parts 1-3 — **TBD: location** — Project-specific requirements
- DEL-30.02 Commissioning Plan — Planned approach and schedule for commissioning activities

**Source:** Decomposition §3 (Reference Documents); `_REFERENCES.md`

**Applicable Standards:**
- CSA Z662 — Oil and Gas Pipeline Systems
- IEC 62382 — Electrical and instrumentation loop check
- ASME PCC-1 — Guidelines for Pressure Boundary Bolted Flange Joint Assembly
- Employer's Requirements — Project-specific requirements

**Source:** **ASSUMPTION: likely applicable** based on deliverable type (Procedure) and discipline (T&C); **location TBD** for specific standard clauses

**Cross-references:**
- See `_DEPENDENCIES.md` — Dependencies coordinated externally (NOT_TRACKED mode)
- PKG-10 (Railcar Unloading System) — System-specific commissioning requirements
- PKG-11 (Marine Loading System) — System-specific commissioning requirements
- PKG-13 (Storage Tanks) — Tank commissioning requirements
- PKG-29 (Testing) — Interface with pre-commissioning testing activities

**Source:** Decomposition §5 (Package structure); **ASSUMPTION** — Interfaces required for commissioning execution

---

## Document Cross-References

This Datasheet connects to the other three documents as follows:

- **→ Specification.md:** Requirements are defined for each attribute and anticipated artifact identified in this Datasheet
  - Datasheet §Construction (Pre-commissioning procedures) → Specification §Requirements FR-2
  - Datasheet §Construction (Commissioning procedures) → Specification §Requirements FR-3
  - Datasheet §Construction (Start-up procedures) → Specification §Requirements FR-4
  - Datasheet §Conditions (Facility systems) → Specification §Requirements FR-6
  - Datasheet §References (Standards) → Specification §Standards

- **→ Guidance.md:** Engineering rationale and considerations are provided for commissioning approach
  - Datasheet §Construction (Phased approach) → Guidance §Principles P-1
  - Datasheet §Construction (Safety elements) → Guidance §Principles P-2
  - Datasheet §Conditions (Product: CSD canola oil) → Guidance §Principles P-5

- **→ Procedure.md:** Step-by-step process is defined for producing the anticipated artifacts
  - Datasheet §Construction (Pre-commissioning procedures) → Procedure §Steps Phase 2 (Development)
  - Datasheet §Construction (Procedure format elements) → Procedure §Steps 2.1, 2.4
  - Datasheet §References (Standards) → Procedure §Prerequisites (Applicable Codes and Standards)
