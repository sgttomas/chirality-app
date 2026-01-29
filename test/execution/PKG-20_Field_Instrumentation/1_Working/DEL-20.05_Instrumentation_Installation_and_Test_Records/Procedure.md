# Procedure: DEL-20.05 Instrumentation Installation & Test Records

## Purpose

Defines process for **producing** Instrumentation Installation & Test Records within **PKG-20 Field Instrumentation**.

**Deliverable Scope:** Provides evidence of completion, inspection, and testing for instrumentation.

**Source:** Decomposition document, DEL-20.05 (line 500)

## Prerequisites

**Dependencies:** See `_DEPENDENCIES.md` — **NOT_TRACKED**

**Typical Inputs:**
- DEL-20.01 (drawings — installation details)
- DEL-20.02 (specification — performance requirements)
- DEL-20.03 (calculations — verified parameters)
- DEL-20.04 (data sheets — equipment specifications)
- Project commissioning plan and test procedures
- Calibration equipment (traceable standards)

**Personnel:**
- Calibration technicians (certified)
- Instrument technicians (field installation and testing)
- Control systems technicians (loop checks)
- Commissioning engineers (functional tests, system integration)
- QA/QC inspectors (installation inspection)

**Source:** **ASSUMPTION** based on typical commissioning personnel requirements

## Steps

**Overview:** Implements Specification.md requirements through commissioning lifecycle (installation inspection → pre-commissioning testing → commissioning with product → performance verification).

### Step 1: Installation Inspection

**Objective:** Verify instruments are correctly installed per DEL-20.01 drawings and DEL-20.02 specifications.

**Activities:**
- Inspect mounting (secure, orientation correct, accessible for maintenance)
- Inspect wiring (connections per drawings, cable labels correct, grounding adequate)
- Inspect hazardous area compliance (conduit seals, cable glands, enclosure ratings per CSA C22.1)
- Verify nameplate data matches DEL-20.04 data sheets (manufacturer, model, serial number)
- Document deficiencies on punch list for correction
- QA/QC inspector sign-off

**Deliverable:** Installation inspection records

**Verification:** QA/QC inspector approval, punch list items closed before proceeding to testing

**Source:** Specification FR-4

### Step 2: Factory Acceptance Testing (if applicable)

**Objective:** Verify critical instruments at vendor factory before shipment.

**Activities:**
- Develop FAT procedures (approved by Contractor and Owner)
- Witness vendor testing (performance verification, accuracy verification)
- Document test results and non-conformances
- Approve equipment for shipment (or require corrective actions)

**Deliverable:** FAT records

**Applicability:** **TBD** — Major instruments (custody transfer meters, safety systems) may require FAT per Employer's Requirements

**Source:** Specification FR-5; **ASSUMPTION** based on typical FAT requirements for critical equipment

### Step 3: Pre-Commissioning Calibration and Loop Checks

**Objective:** Verify instrument calibration and loop functionality before process introduction.

**Activities:**

3.1. **Field Calibration:**
- Perform dry calibration using electronic simulators or calibrators
- Calibration equipment traceable to national standards (NIST, NRC Canada)
- Document calibration data (input/output, error at each point, as-found/as-left accuracy)
- Technician sign-off

3.2. **Loop Checks:**
- Simulate sensor input (level, pressure, temperature, flow)
- Verify control system reading matches simulated value
- Verify alarm and trip points (setpoints, time delays, reset functions)
- Verify signal integrity (4-20 mA span, HART communication if applicable)
- Document loop check results and sign-offs (instrument tech, control systems tech, commissioning engineer)

**Deliverable:** Calibration certificates, loop check records

**Verification:** Loops functional end-to-end, alarms and trips verified

**Source:** Specification FR-2, FR-3

### Step 4: Commissioning with Product (Wet Calibration)

**Objective:** Verify critical measurements under actual process conditions.

**Activities:**
- Introduce process fluid (canola oil) into systems
- Perform wet calibration for critical measurements:
  - **Tank level:** Measure with tape, verify transmitter reading (verify ±3 mm accuracy for tank gauging)
  - **Custody transfer flow:** Verify against master meter or prover (coordinate with PKG-12)
  - **Overfill protection:** Functional test of independent high level alarms and automatic shutdown (per API 2350)
- Document wet calibration results
- Adjust instruments if necessary (within specification tolerances)

**Deliverable:** Wet calibration records, functional test records

**Verification:** Critical measurements meet specification accuracy under actual conditions

**Source:** Specification FR-5; API 2350 reference for overfill protection testing

### Step 5: Functional and Performance Testing

**Objective:** Verify integrated system functionality and performance.

**Activities:**

5.1. **Functional Tests:**
- Alarm and interlock verification (setpoints correct, response correct, sequences correct)
- Control loop tuning (PID parameters, response testing, stability verification)
- Safety system verification (SIS functional testing per ISA 84 if applicable)

5.2. **Performance Tests:**
- System throughput verification (railcar unloading rate, ship loading rate)
- Measurement accuracy verification (inventory reconciliation, custody transfer accuracy)
- System integration verification (instrumentation + control + equipment operating together)

**Deliverable:** Functional test records, performance test records

**Verification:** Systems meet design performance requirements before operational handover

**Source:** Specification FR-5; **ASSUMPTION** based on typical commissioning functional/performance testing

### Step 6: Record Compilation and Turnover

**Objective:** Compile final test record package for facility turnover.

**Activities:**
- Compile all test records (calibration, loop checks, FAT, installation, functional, performance)
- Organize records (**TBD**: By tag, by system, by test type)
- Review records for completeness and quality (no missing sign-offs, no blank fields)
- Obtain final approvals (commissioning lead, QA/QC manager, Owner representative)
- Provide final record package to Owner (hard copy and/or electronic)
- Update DEL-20.04 data sheets with as-built calibration data

**Deliverable:** Final test record package delivered to Owner

**Source:** Specification Documentation section; **ASSUMPTION** based on typical facility turnover requirements

## Verification

**Verification Activities:**

- Test record review (completeness, accuracy, sign-offs)
- Spot-check verification (sample of records reviewed in detail)
- Field verification (random inspection of installations and re-test of samples)

**Acceptance Criteria:**

All required tests complete. All records signed by qualified personnel. All tests passed (or non-conformances resolved). Punch list items closed. Final approvals obtained. Package ready for Owner acceptance.

**Source:** Specification Verification section

## Records

**Documentation Outputs:**

- Calibration certificates (factory and field)
- Loop check records
- FAT records (if applicable)
- Installation inspection records
- Functional test records
- Performance test records
- Punch lists and corrective action records

**Organization:** **TBD** — By instrument tag, by system, or by test type

**Record Management:**

- Working records during commissioning (commissioning database or folder structure)
- Final compiled package in `3_Issued/` as permanent records
- Retention: **TBD** — Permanent facility records per contract and regulatory requirements
- Copies provided to Owner for operations and maintenance

**Source:** README.md lifecycle folder structure; **ASSUMPTION** on permanent record retention

**Integration with Operations:**

Test records establish operational baseline:
- Calibration baseline for recalibration intervals
- Alarm setpoints and control loop tuning parameters
- Equipment serial numbers and as-built configurations
- Foundation for computerized maintenance management system (CMMS) — **TBD**: System integration

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** — Test records provide evidence that instrumentation is correctly installed, calibrated, and functional for safe operations.

Supports **OBJ-9: Lifecycle Cost Optimization** — As-commissioned baseline supports efficient maintenance planning and calibration scheduling.

**Source:** Decomposition Section 6 (lines 780, 788)
