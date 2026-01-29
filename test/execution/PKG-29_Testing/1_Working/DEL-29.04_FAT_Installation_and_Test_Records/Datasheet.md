# Datasheet: DEL-29.04 FAT Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-29.04 |
| Name | FAT Installation & Test Records |
| Package | PKG-29 Testing |
| Discipline | T&C |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** _CONTEXT.md, Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md line 649

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Category | Factory Acceptance Test (FAT) Records |
| Record Scope | Major equipment factory testing and inspection |
| Test Location | Vendor/manufacturer facilities |
| Applicable Equipment | Pumps, loading arms, metering systems, control panels, major valves, specialty equipment |
| Test Phase | Procurement / Pre-delivery |
| Retention Period | Permanent (facility lifetime) **ASSUMPTION** |

**Source:** _CONTEXT.md; typical FAT scope **ASSUMPTION**

**ASSUMPTION:** FAT records are permanent quality records proving equipment met specifications prior to shipment and installation.

## Conditions

**Operating / Environmental Context:**

Provides evidence of completion, inspection, and testing for FAT. **Source:** Decomposition line 649

**FAT Purpose:**

Factory Acceptance Tests serve to:
1. Verify equipment meets purchase specifications before shipment
2. Identify defects early when correction is easier and less costly
3. Witness equipment operation in controlled factory environment
4. Train operations personnel on equipment operation and maintenance
5. Reduce site commissioning time and risk

**Project Objectives Supported:**
- OBJ-1: Safe & Reliable Operation (equipment proven functional before installation)
- OBJ-9: Lifecycle Cost Optimization (early defect detection reduces rework)

**Source:** Decomposition Section 2, Section 6 Objective Mapping; typical FAT benefits **ASSUMPTION**

**FAT Execution Context:**

FATs are typically conducted:
- At vendor/manufacturer facilities
- After equipment fabrication/assembly but before shipment
- Per ITP hold/witness points (DEL-29.02) for major equipment
- With Contractor, Employer, and/or third-party representatives present
- Per vendor-supplied FAT procedures or project-specified FAT requirements

## Construction

**FAT Record Types and Content:**

### Typical Equipment Requiring FATs:

**Mechanical Equipment:**
- **Transfer pumps** (P-201A/B): Performance testing (flow, head, NPSH), vibration, seal leakage, motor insulation
- **Loading arms** (marine loading): Articulation, emergency release, leak testing, controls
- **Specialty valves** (large actuated valves): Stroke testing, control signal response, position indication
- **Pressure relief valves**: Set pressure verification, leak testing

**Electrical Equipment:**
- **Motor Control Centers (MCCs)**: Insulation resistance, circuit breaker operation, metering accuracy
- **Switchgear**: High-potential (hi-pot) testing, protection relay settings, interlocks
- **Variable Frequency Drives (VFDs)**: Parameter programming, input/output verification, alarms

**I&C Equipment:**
- **Control panels / PLCs**: I/O verification, logic testing, HMI functionality
- **Metering systems** (custody transfer): Calibration verification, proving, accuracy testing per Measurement Canada requirements **ASSUMPTION**
- **Safety instrumented systems**: Logic solver testing, final element response, proof test

**Source:** Project scope (PKG-10, 11, 12, 15, 16, 19, 20) per Decomposition; typical EPC FAT scope **ASSUMPTION**

### FAT Report Content (per equipment):

**Equipment Identification:**
- Equipment tag, manufacturer, model, serial number
- Purchase order and specification reference
- FAT date and location

**FAT Procedure:**
- FAT procedure reference (vendor or project-specified)
- Test objectives and scope
- Test equipment used (with calibration status)

**Pre-FAT Inspection:**
- Dimensional verification (compare to drawings)
- Material verification (compare to material certs)
- Nameplate data verification
- Workmanship inspection (welds, coatings, assembly)

**Performance Testing:**
- Operational tests per specification (flow rates, pressures, speeds, accuracies)
- Functional tests (controls, interlocks, alarms, safety features)
- Endurance tests (run duration, cycling)
- Acceptance criteria and measured results

**Documentation:**
- Test data sheets with measured values
- Photographs (equipment, nameplates, test setup)
- Deviations/deficiencies noted and dispositioned
- Punch list items (to be completed before shipment or at site)

**Approvals and Witnesses:**
- Vendor test engineer sign-off
- Contractor QC witness signature
- Employer witness signature (if required per ITP)
- Final acceptance statement

**Source:** Typical FAT report structure per equipment procurement best practices **ASSUMPTION**

## References

**Decomposition & Context:**
- Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 5, PKG-29, line 649)
- _CONTEXT.md
- _REFERENCES.md

**Applicable Standards:**
- ISO 9001: Quality Management Systems (supplier quality)
- Equipment-specific standards (API, ASME, NFPA, IEC) per equipment type
- Manufacturer's test procedures
- Project equipment specifications
- Employer's Requirements: **location TBD**

**Cross-References:**

**Upstream (Input):**
- Procurement specifications (all equipment packages)
- Vendor drawings and manuals
- DEL-29.02: ITP (FAT witness requirements)
- Purchase orders with FAT requirements

**Downstream (Output):**
- DEL-29.05: SAT Records (FAT is prerequisite for SAT)
- PKG-30: Commissioning (FAT records support commissioning)
- O&M documentation (FAT reports provide baseline performance data)

See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
