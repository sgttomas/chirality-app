# Procedure: DEL-20.03 Instrumentation Design Calculations

## Purpose

This procedure defines the process for **producing** Instrumentation Design Calculations within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1 project.

**Deliverable Scope:** Provides the engineering basis and sizing/verification calculations for instrumentation.

**Source:** Decomposition document, DEL-20.03 (line 498)

## Prerequisites

**Dependencies:** See `_DEPENDENCIES.md` — **NOT_TRACKED** (coordinated externally by humans)

**Typical Upstream Inputs:**
- P&IDs and instrument list (instrument applications, tag numbers)
- Process data sheets (operating conditions, fluid properties)
- DEL-20.02 specification (requirements to be verified)
- Equipment specifications (tank dimensions, pump curves)
- Piping design basis (design pressures, temperatures)
- Environmental design criteria (ambient conditions, seismic)

**Reference Materials:**
- Applicable codes and standards (ISA, API, ASME)
- Employer's Requirements — **TBD**
- Vendor technical literature (performance curves, specifications)

**Personnel:** I&C Engineer (originator), Independent Checker (P.Eng. or senior engineer), I&C Lead (approver)

**Source:** **ASSUMPTION** based on typical calculation input requirements

## Steps

**Overview:** This procedure implements Specification.md requirements and produces calculations documented in Datasheet.md.

### Step 1: Input Data Collection

**Objective:** Gather all required design inputs and assumptions.

**Activities:**
- Review P&IDs for instrument applications and service descriptions
- Extract operating conditions from process data sheets (pressures, temperatures, flow rates, fluid properties)
- Review DEL-20.02 specification for requirements to be verified
- Identify calculation scope (which instruments require calculations)
- Document assumptions where inputs are unavailable (mark **TBD** for follow-up)

**Deliverable:** Design input register with sources documented

**Verification:** I&C Lead review of design basis

**Source:** **ASSUMPTION** based on typical calculation initiation

### Step 2: Methodology Selection

**Objective:** Select appropriate calculation methods and tools.

**Activities:**
- Select applicable codes and standards (ISA, API, ASME) for calculation methodology
- Select calculation software (Excel for tabular, MathCAD for analytical, specialty software for complex applications)
- Establish calculation format (objective, design basis, calculations, results, references)
- Establish design margins (range margin, overpressure factor, accuracy budget)

**Deliverable:** Calculation methodology document

**Source:** Specification PR-1, PR-2

### Step 3: Calculation Execution

**Objective:** Perform sizing and verification calculations.

**Activities:**

3.1. **Range Selection Calculations**
- Calculate normal/design/maximum operating points
- Select instrument range to position operating point at 30-70% of span
- Verify overpressure rating (≥2× range or piping MAWP)

3.2. **Accuracy Verification Calculations**
- Identify error components (sensor, transmitter, installation, calibration drift)
- Sum errors (RSS or worst-case method)
- Compare to measurement requirement (verify adequacy)

3.3. **Sizing Calculations (as applicable)**
- Orifice plate sizing per API 14.3 (if flow measurement via DP)
- Thermowell stress analysis per ASME PTC 19.3 (high-velocity applications)
- Impulse piping slope and support calculations per API 554

3.4. **Installation Calculations (as applicable)**
- Winterization requirements (heat loss, insulation)
- Seismic restraint loads per NBC 2015
- Mounting loads (weight, thermal expansion)

**Deliverable:** Completed calculations with results summary

**Verification:** Self-check by originator (completeness and arithmetic)

**Source:** Specification FR-2 to FR-5

### Step 4: Results Interpretation

**Objective:** Evaluate results against acceptance criteria.

**Activities:**
- Verify calculated ranges match data sheet specifications (DEL-20.04)
- Verify calculated accuracy meets specification requirements (DEL-20.02)
- Verify calculated parameters are constructible and practical
- Identify any non-conformances or design issues
- Document conclusions and recommendations

**Deliverable:** Results summary with conclusions

**Source:** **ASSUMPTION** based on typical calculation review

### Step 5: Independent Check

**Objective:** Verify calculations are correct and complete.

**Activities:**
- Independent checker (qualified engineer, not originator) reviews:
  - Input data traceability and accuracy
  - Methodology appropriateness
  - Calculation arithmetic and logic
  - Results reasonableness
- Checker documents findings on check sheet
- Originator addresses checker comments
- Checker signs off when satisfied

**Deliverable:** Signed check sheet

**Verification:** Check sheet includes checker name, date, sign-off

**Source:** Specification QR-1

### Step 6: Approval and Issuance

**Objective:** Approve calculations for use.

**Activities:**
- I&C Lead Engineer reviews and approves calculations
- Professional seal applied if required (**TBD**: P.Eng. seal requirements for BC)
- Calculations registered in document management system
- Calculations distributed to users (design team, procurement, construction)
- Calculation numbers cross-referenced in related deliverables (data sheets, drawings, specifications)

**Deliverable:** Approved calculations, distribution records

**Source:** Specification QR-4; **ASSUMPTION** based on typical approval process

## Verification

**Verification Activities:**
- Self-check (originator)
- Independent check (qualified engineer)
- Software output spot-check (if applicable)
- Design code compliance review
- Traceability verification (inputs to sources)

**Acceptance Criteria:**
- Methodology appropriate for application
- Inputs documented and traceable
- Calculations reproducible
- Results meet specification requirements
- Independent check complete with sign-off

**Source:** Specification Verification section

## Records

**Documentation Outputs:**
- Instrument sizing calculations (Excel, MathCAD, or PDF format)
- Calculation index (master list)
- Design basis summary
- Check sheets (signed)

**Record Management:**
- Working files in `1_Working/` during development
- Checking files in `2_Checking/` during review
- Issued files in `3_Issued/` upon approval
- Retention per project requirements — **TBD**

**Source:** README.md lifecycle folder structure

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** — Rigorous calculation process ensures instruments are correctly sized for safe and reliable operations.

**Source:** Decomposition Section 6 (line 780)
