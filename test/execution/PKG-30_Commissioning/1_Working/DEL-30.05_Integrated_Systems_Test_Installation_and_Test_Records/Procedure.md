# Procedure: DEL-30.05 Integrated Systems Test Installation & Test Records

## Purpose

Defines the process for executing and documenting **Integrated Systems Test (IST)** for the Canola Oil Transload Facility.

**Context:** Provides evidence of completion, inspection, and testing for integrated systems test.

**Source:** Decomposition §5 PKG-30, DEL-30.05

## Prerequisites

**Dependencies:** NOT_TRACKED mode — See `_DEPENDENCIES.md`

**Upstream Requirements:**
- DEL-30.01 Commissioning Procedures — IST procedures
- DEL-30.02 Commissioning Plan — IST schedule
- DEL-30.04 Commissioning Records — All individual systems commissioned
- System design documents — End-to-end system design and operational scenarios
- O&M manuals — Operating procedures reference

**Personnel:**
- IST team: Commissioning engineers, control system specialists, operations representatives
- QA/QC Manager (sign-off)
- Commissioning Manager (sign-off)
- Operations Manager (sign-off)

**Tools:**
- IST test protocols and record forms — **TBD**
- Test medium (water, air) — **TBD**
- Instrumentation and data logging equipment

**Source:** DEL-30.01, DEL-30.02, DEL-30.04; **ASSUMPTION**

## Steps

**Step 1: Verify Prerequisites**
- Verify individual system commissioning complete (DEL-30.04)
- Verify control systems programmed and functional tested
- Verify safety systems commissioned
- Verify test medium available (water, air, nitrogen)

**Step 2: Prepare IST Protocols**
- Develop IST test protocols per DEL-30.01 procedures
- Define end-to-end scenarios:
  - Railcar → Tank transfer
  - Tank → Ship loading
  - Direct Railcar → Ship (operational flexibility demonstration)
- Define acceptance criteria for each scenario
- Obtain protocol approval

**Step 3: Conduct IST Briefing**
- Brief IST team on test objectives and protocols
- Assign roles and responsibilities
- Review safety requirements and emergency response
- Coordinate with operations representatives

**Step 4: Execute End-to-End Scenarios**

**Scenario 1: Railcar → Tank**
- Simulate railcar unloading to storage tank
- Verify: Pump operation, valve sequencing, level control, metering, interlocks, HMI operation
- Record: Flow rates, transfer time, volumes, system responses
- Document acceptance

**Scenario 2: Tank → Ship**
- Simulate tank to ship loading transfer
- Verify: Pump operation, metering, marine loading arm operation, interlocks, HMI operation
- Record: Flow rates, transfer time, volumes, custody transfer metering data
- Document acceptance

**Scenario 3: Direct Railcar → Ship (OBJ-4)**
- Simulate direct rail-to-ship transfer (operational flexibility)
- Verify: Valve lineup changes, routing, metering, control logic, HMI operation
- Record: Flow rates, transfer time, mode transition verification
- Document operational flexibility demonstrated

**Step 5: Verify Safety Systems Integration**
- Test emergency shutdown system (ESD) integration
- Test high-level protection interlocks across systems
- Test fire protection system integration
- Verify alarm management and response
- Document safety systems integrated and functional

**Step 6: Verify Control System Integration**
- Verify SCADA/PLC data integration across all systems
- Verify HMI displays and operator controls
- Verify data logging and trending
- Verify reporting functions
- Document control system integration complete

**Step 7: Document Non-Conformances and Resolutions**
- Document any integration issues discovered
- Track resolutions
- Re-test after resolution
- Close NCRs

**Step 8: Obtain Sign-offs**
- QA/QC Manager reviews IST records and signs
- Commissioning Manager reviews and signs
- Operations Manager reviews and signs (operational readiness acceptance)
- Employer witness signs — **TBD**

**Step 9: Submit IST Records**
- Compile all IST records and test results
- Submit to document control
- File in `3_Issued/DEL-30.05/`
- Notify start-up team IST complete (prerequisite for DEL-30.06)

**Source:** **ASSUMPTION** — IST execution process

## Verification

- IST protocols executed per plan
- All end-to-end scenarios complete
- Acceptance criteria met
- Safety systems integration verified
- NCRs closed
- Sign-offs obtained

**Source:** Specification.md

## Records

**Outputs:**
- IST test protocols
- End-to-end scenario test records
- Control system integration test records
- Safety interlock integration test records
- NCRs and resolutions

**Management:**
- Filed in `3_Issued/DEL-30.05/`
- Retention: **TBD** — Permanent project records

**Source:** Decomposition §5 DEL-30.05

---

## Document Cross-References

- **← Datasheet / Specification / Guidance:** Procedure implements IST requirements
- DEL-30.04 provides prerequisite individual system commissioning
- DEL-30.06 uses IST records as prerequisite for performance testing
