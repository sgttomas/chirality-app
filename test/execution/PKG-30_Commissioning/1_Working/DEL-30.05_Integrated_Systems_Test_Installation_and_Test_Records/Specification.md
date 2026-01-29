# Specification: DEL-30.05 Integrated Systems Test Installation & Test Records

## Scope

Defines requirements for **Integrated Systems Test Installation & Test Records** for the Canola Oil Transload Facility — Phase 1.

**Purpose:** Provides evidence of completion, inspection, and testing for integrated systems test.

**Artifacts:** IST records, end-to-end test records

**Source:** Decomposition §5 PKG-30, DEL-30.05

## Requirements

### Functional Requirements

**FR-1: End-to-End Scenario Testing**
- IST shall verify complete transfer paths: railcar → tank, tank → ship, direct rail → ship (OBJ-4)
- Test scenarios shall demonstrate systems work together per design
- **Source:** Decomposition §2 OBJ-4 (Operational Flexibility)

**FR-2: Control System Integration**
- IST shall verify SCADA/PLC integration across all facility systems
- HMI functionality, data logging, trending, alarm management verification
- **Source:** **ASSUMPTION** — Control system integration scope

**FR-3: Safety Systems Integration**
- IST shall verify safety interlocks across systems (emergency shutdown, high-level protection, fire protection interlocks)
- Safety system trip testing and fail-safe verification
- **Source:** Decomposition §2 OBJ-1 (Safe & Reliable Operation)

**FR-4: Metering System Integration**
- IST shall verify custody transfer metering integration in transfer paths
- Flow computer, totalizer, proving system integration verification (OBJ-10)
- **Source:** Decomposition §2 OBJ-10 (Custody Transfer Accuracy)

**FR-5: Operational Flexibility Demonstration**
- IST shall demonstrate tank storage mode and direct rail-to-ship mode (OBJ-4)
- Valve lineup changes, routing verification, operational transitions
- **Source:** Decomposition §2 OBJ-4

### Performance Requirements

**PR-1: Operational Readiness**
- IST shall demonstrate facility ready for start-up and product introduction
- Systems shall operate together reliably per design intent
- **Source:** Decomposition §2 OBJ-1; DEL-30.01 Commissioning Procedures

**PR-2: Throughput Capacity Indication**
- IST shall demonstrate system capacity trends toward design throughput (1,000,000 MT/annum - OBJ-2)
- Flow rates, pump performance, transfer times documented
- **Source:** Decomposition §2 OBJ-2 (Throughput Capacity)

### Interface Requirements

**IR-1: Individual System Commissioning Prerequisite**
- IST requires DEL-30.04 commissioning records complete for all systems
- **Source:** DEL-30.02 Commissioning Plan; DEL-30.04

**IR-2: Start-up and Performance Test Interface**
- IST records are prerequisite for start-up and performance testing (DEL-30.06)
- **Source:** DEL-30.02; DEL-30.06

**IR-3: Operations Interface**
- Operations representatives participate in IST and provide acceptance sign-off
- **Source:** **ASSUMPTION** — Operations involvement required

### Quality Requirements

**QR-1: Approval and Sign-off**
- IST records require QA/QC Manager, Commissioning Manager, Operations Manager sign-offs
- Employer witness sign-off — **TBD**
- **Source:** **ASSUMPTION** — IST governance

**QR-2: Record Quality**
- IST records shall be comprehensive, traceable, and provide objective evidence of integrated systems readiness
- **Source:** **ASSUMPTION**

## Standards

- IEC 62382 — Commissioning methodology — **location TBD**
- Employer's Requirements — **TBD: location** for IST requirements

**Source:** **ASSUMPTION: likely applicable**

## Verification

- Completeness check against IST test protocols
- End-to-end scenario completion verification
- Safety systems integration verification
- Sign-offs obtained

**Acceptance:** All IST scenarios complete, acceptance criteria met, systems operate together reliably, sign-offs obtained

## Documentation

**Outputs:** IST records, end-to-end test records for all facility transfer paths

**Format:** IST test protocols and results — **TBD**

**Submittal:** Upon IST completion; stored in `3_Issued/DEL-30.05/`

**Source:** Decomposition §5 DEL-30.05

---

## Document Cross-References

- **← Datasheet.md:** Requirements for IST scope
- **→ Guidance.md:** Rationale for integrated systems testing
- **→ Procedure.md:** IST execution process
