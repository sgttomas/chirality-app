# Datasheet: DEL-20.05 Instrumentation Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-20.05 |
| Name | Instrumentation Installation & Test Records |
| Package | PKG-20 Field Instrumentation |
| Discipline | I&C |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

**Source:** Decomposition document, DEL-20.05 (line 500)

## Attributes

**Record Package Characteristics:**

| Attribute | Value |
|-----------|-------|
| Record Type | Quality assurance and commissioning test records |
| Record Format | **TBD** — Forms, checklists, test sheets per project QA/commissioning procedures |
| Organization | By instrument tag number, by system, or by test type |
| Usage | QA verification, commissioning sign-off, regulatory compliance, facility turnover |
| Retention | **TBD** — Permanent facility records per contract and regulatory requirements |

**Anticipated Record Types:**

- **Calibration certificates:** Factory and field calibration of transmitters, gauges, switches
- **Loop check records:** End-to-end verification of instrument loops (sensor to control system)
- **FAT records:** Factory acceptance test documentation (if vendor testing required)
- **Installation inspection records:** Field installation verification (mounting, wiring, labeling)
- **Functional test records:** Operational verification (alarm points, trip functions, control loops)

**Source:** Decomposition DEL-20.05 Anticipated Artifacts (line 500); **ASSUMPTION** based on typical instrumentation commissioning records

## Conditions

**Project Context:**

Test records support commissioning and startup of the Canola Oil Transload Facility Phase 1 (1,000,000 MT/annum throughput, 3 × 15,000 MT storage tanks, 32 railcar unloading stations).

**Source:** Decomposition Section 1.1 Key Parameters

**Record Purpose:**

Installation and test records serve multiple purposes:
1. **Quality assurance:** Demonstrate compliance with specifications (DEL-20.02) and installation standards
2. **Commissioning:** Verify instrument and control loop functionality before operations
3. **Regulatory compliance:** Provide evidence for permitting and safety approvals
4. **Facility turnover:** Document as-built status and test results for Owner
5. **Operations baseline:** Establish calibration baseline for future maintenance

**Record Lifecycle:**

Records are created during:
- **Fabrication:** Factory calibration and testing (FAT records from vendors)
- **Installation:** Field installation inspection and verification
- **Pre-commissioning:** Individual instrument testing (calibration, functional checks)
- **Commissioning:** Loop testing and integrated system testing
- **Performance testing:** System performance verification before handover

**Source:** **ASSUMPTION** based on typical EPC commissioning workflow

**Instrumentation Testing Scope (Estimated):**

Based on facility scope:
- **Level instruments:** 30-60 devices (transmitters, switches) requiring calibration and loop checks
- **Pressure instruments:** 60-80 devices requiring calibration and loop checks
- **Temperature instruments:** 40-50 devices requiring calibration and loop checks
- **Flow instruments:** 15-30 devices requiring calibration and performance verification
- **Control loops:** 100+ loops requiring end-to-end verification

**Source:** **ASSUMPTION** based on Datasheet for DEL-20.04 (estimated instrument population) and typical commissioning scope

## Construction

**Record Types and Content:**

### Calibration Certificates

**Factory Calibration (from vendors):**
- Instrument tag number and serial number
- Calibration date and calibration technician
- Calibration equipment used (traceable standards)
- Calibration data (input vs. output, error at each point)
- As-found and as-left accuracy
- Certificate sign-off by qualified technician

**Field Calibration (site commissioning):**
- Same content as factory calibration
- Performed on-site after installation
- Includes ambient temperature and environmental conditions
- Documents calibration adjustments if required

**Calibration Standards:**
- Test equipment traceable to national standards (NIST, NRC Canada)
- Accuracy of calibration equipment superior to instrument being calibrated (typically 4:1 ratio)

**Source:** **ASSUMPTION** based on typical calibration certificate requirements and metrology standards

### Loop Check Records

**Loop Check Content:**
- Loop identification (tag number, P&ID reference, control system I/O point)
- Loop components (sensor, transmitter, cable, control system input)
- Functionality test (simulate sensor input, verify control system reading)
- Alarm and trip point verification (setpoints, response)
- Signal integrity (4-20 mA span check, HART communication if applicable)
- Sign-offs (instrument technician, control systems technician, commissioning engineer)

**Loop Check Methods:**
- **Level loops:** Simulate level (wet/dry calibration or electronic simulation), verify control room indication and alarms
- **Pressure loops:** Apply known pressure (calibrator), verify reading and alarms
- **Temperature loops:** Simulate temperature (RTD simulator or bath), verify reading and alarms

**Source:** **ASSUMPTION** based on typical loop check procedures for EPC commissioning

### Factory Acceptance Test (FAT) Records

**FAT Scope (if applicable):**
- Major or critical instruments may require factory testing before shipment
- Custody transfer meters (coordinate with PKG-12) typically require FAT
- Safety instrumented systems (SIS) may require FAT per ISA 84

**FAT Content:**
- Test procedure (approved by Contractor and Owner)
- Test results (performance verification, accuracy verification)
- Witnessed by Contractor/Owner representatives (witness signatures)
- Non-conformance reports and corrective actions
- Final approval and release for shipment

**Source:** **ASSUMPTION** based on typical FAT requirements for critical instrumentation; **TBD**: Specific FAT requirements per Employer's Requirements

### Installation Inspection Records

**Inspection Content:**
- Installation checklist (mounting secure, orientation correct, clearances adequate)
- Wiring verification (connections per wiring diagrams, cable labels correct, grounding adequate)
- Hazardous area compliance (conduit seals, cable glands, enclosure ratings per CSA C22.1)
- Material verification (nameplate data matches data sheets)
- Punch list (deficiencies identified for correction)
- Inspector sign-off (QA/QC inspector approval)

**Source:** **ASSUMPTION** based on typical field installation QA/QC procedures

### Functional Test Records

**Functional Test Content:**
- Operational verification (instrument responds correctly to process conditions)
- Alarm and interlock verification (setpoints, time delays, reset functions)
- Control loop tuning (PID parameters, response testing)
- Safety system verification (overfill protection, emergency shutdown per API 2350, ISA 84)
- Performance testing (system meets design throughput and accuracy requirements)

**Source:** **ASSUMPTION** based on typical commissioning functional test procedures; API 2350, ISA 84 references for safety systems

## References

**Primary References:**

- Decomposition document, Section PKG-20 (lines 486-501)
- DEL-20.02 Instrumentation Technical Specification (requirements being verified)
- DEL-20.03 Instrumentation Design Calculations (calculated performance being verified)
- DEL-20.04 Instrumentation Data Sheet Package (equipment specifications being verified)
- DEL-20.01 Instrumentation Design Drawing Set (installation details being verified)

**Commissioning Procedures:**

- Project commissioning plan — **TBD**
- Instrument calibration procedures — **TBD**
- Loop check procedures — **TBD**
- FAT procedures — **TBD** (if applicable)

**Applicable Standards:**

- ISA 84 / IEC 61511 (safety instrumented system verification)
- API 2350 (overfill protection testing)
- CSA C22.1 (hazardous area installation inspection)
- ISO/IEC 17025 (calibration laboratory accreditation — if required)

**Related Deliverables:**

All previous PKG-20 deliverables (DEL-20.01 through DEL-20.04) are inputs to test records. Test records demonstrate compliance with specifications, calculations, data sheets, and drawings.

**Dependencies:** See `_DEPENDENCIES.md` — **NOT_TRACKED** (coordinated externally)

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** — Installation and test records provide evidence that instrumentation is correctly installed, calibrated, and functional for safe and reliable facility operations.

**Source:** Decomposition Section 6 (line 780)

## Cross-Document Traceability

This Datasheet provides factual identification, attributes, conditions, and references for DEL-20.05. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Specification.md | Requirements and verification criteria | FR-1 to FR-5 define test record requirements; QR-1 to QR-3 define quality requirements |
| Guidance.md | Engineering rationale and decision context | Principles 1-3 explain commissioning philosophy; Trade-off addresses calibration methods |
| Procedure.md | Production workflow and verification steps | Steps 1-6 define commissioning lifecycle (inspection → testing → turnover) |

**Document Consistency Verification:**

- All record types in Datasheet Attributes § appear in Specification Documentation and Procedure Records
- All related deliverables in Datasheet References § are verified per Specification FR-1 and Procedure Prerequisites
- Test lifecycle in Datasheet Conditions § aligns with Procedure Steps 1-6
- Applicable standards in Datasheet References § appear in Specification Standards
