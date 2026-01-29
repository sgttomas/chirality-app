# Specification: DEL-15.05 Pump Installation & Test Records

## Scope

This specification defines the requirements for **Pump Installation & Test Records** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility at Fraser Surrey Terminal, Surrey, BC.

**Deliverable scope:** Provides evidence of completion, inspection, and testing for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.05 entry

### Purpose

The Pump Installation & Test Records shall:

1. **Document proper installation** — Provide evidence that pumps are installed per drawings (DEL-15.01) and manufacturer instructions
2. **Verify performance** — Confirm pump performance meets specification (DEL-15.02) and design calculations (DEL-15.03)
3. **Support warranty** — Provide records for equipment warranty claims and troubleshooting
4. **Enable operations** — Provide baseline performance data for future comparison and maintenance planning
5. **Meet regulatory requirements** — Satisfy permit and code compliance requirements for inspections

**Source:** Standard purpose of installation and commissioning records in EPC projects

### Equipment Covered

Installation and test records shall be provided for all pumps:

- Railcar unloading pumps
- Marine loading pumps
- Sump pumps
- Transfer pumps (if applicable)

**Source:** `_CONTEXT.md`, project pump requirements

### Included

- Factory Acceptance Test (FAT) records (if FAT performed)
- Installation records (foundation, setting, alignment, grouting)
- Pre-commissioning inspection checklists
- Performance test records (flow, head, power, efficiency)
- Vibration analysis records
- Acceptance sign-offs and certifications

**Source:** `_CONTEXT.md` (anticipated artifacts), API 610 Section 6

### Excluded

- Vendor shop test records (covered under DEL-15.04 vendor data package)
- Detailed maintenance procedures (covered under O&M manuals, DEL-27.04)
- Ongoing operational records (covered under facility operations procedures)

**Source:** Standard scope boundaries for commissioning records

## Requirements

### Functional Requirements

#### FR-1: Document Installation Compliance

Installation records shall provide evidence of:

| Installation Activity | Record Required | Acceptance Criteria |
|----------------------|-----------------|---------------------|
| **Foundation preparation** | Foundation inspection checklist | Level, clean, proper finish per DEL-15.01 and API 610 Section 6.1 |
| **Equipment set** | Equipment setting record with elevations | Per DEL-15.01 drawings within tolerance (±3mm typical) |
| **Alignment (initial)** | Rough alignment record | Within temporary tolerance for grouting |
| **Grouting** | Grout pour record (mix, date, weather, curing) | Non-shrink grout, 25–75mm thickness per API 610 Section 6.1.4 |
| **Curing** | Curing time log | Minimum 7 days per ACI 318 before final alignment |
| **Alignment (final)** | Final alignment record (dial indicator or laser) | Per API 610 Section 6.3 and manufacturer tolerance (typically 0.05–0.10mm) |
| **Piping connection** | Piping strain check | No excessive loads on pump nozzles per API 610 Section 6.2 |

**Source:** API 610 Section 6.1 (installation requirements)

#### FR-2: Document Pre-Start Checks

Pre-commissioning records shall document:

- **Rotation check:** Motor rotation direction verified correct
- **Lubrication check:** Lubrication system filled and circulating
- **Coupling check:** Coupling guard installed and secure
- **System flush:** Piping system flushed and clean (coordinate with piping discipline)
- **Electrical check:** Motor electrical connections verified (coordinate with electrical discipline)
- **Safety check:** Safety equipment installed (guards, emergency stops)

**Source:** API 610 Section 6 (pre-start requirements)

#### FR-3: Document Performance Testing

Performance test records shall document:

**Test conditions:**
- Date, time, ambient conditions
- Fluid: CSD canola oil at measured temperature and density
- System configuration: Valves, instruments, piping as-tested

**Measurements:**
- Flow rate (m³/hr) — measured by calibrated flow meter
- Suction pressure (kPa gauge) — measured at pump suction flange
- Discharge pressure (kPa gauge) — measured at pump discharge flange
- Head (m) — calculated from pressure differential and elevation
- Motor power (kW) — measured by power meter or calculated from current/voltage
- Vibration (mm/s RMS) — measured at pump and motor bearings

**Calculated results:**
- Pump efficiency (%) — calculated from flow, head, power
- Comparison to vendor data (DEL-15.04) — verify within ISO 9906 Grade 2 tolerance

**Source:** API 610 Section 6.9 (field performance test); ISO 9906 (test methods and tolerances)

### Performance Requirements

#### PR-1: Performance Test Acceptance Criteria

| Parameter | Acceptance Criteria | Tolerance |
|-----------|---------------------|-----------|
| **Flow** | Per DEL-15.03 calculation and DEL-15.02 specification | ±7% (ISO 9906 Grade 2) |
| **Head** | Per DEL-15.03 calculation and DEL-15.02 specification | ±5% (ISO 9906 Grade 2) |
| **Power** | Consistent with vendor data (DEL-15.04) | +10% / -5% typical |
| **Efficiency** | Not guaranteed below vendor-stated value | N/A (information only) |
| **Vibration** | Per API 610 Figure 15 or ISO 10816 | Zone A or B acceptable |
| **Noise** | Per WorkSafeBC limits (if specified) | ≤85 dBA at 1m typical |

**Source:** API 610 Section 6.9, ISO 9906 Grade 2, ISO 10816

#### PR-2: Vibration Acceptance Criteria

Per API 610 Figure 15 (vibration velocity, mm/s RMS):

| Pump Size | Zone A (Good) | Zone B (Acceptable) | Zone C (Marginal) | Zone D (Unacceptable) |
|-----------|---------------|---------------------|-------------------|-----------------------|
| 15–75 kW | < 2.8 | 2.8–7.1 | 7.1–11.2 | > 11.2 |
| > 75 kW | < 4.5 | 4.5–11.2 | 11.2–18.0 | > 18.0 |

**Measurement:** Three axes (horizontal, vertical, axial) at pump and motor bearing housings

**Acceptance:** All measurements in Zone A or B

**Source:** API 610 Figure 15; ISO 10816-3

### Interface Requirements

#### IF-1: Installation Coordination

Installation records shall coordinate with:

- **DEL-15.01:** Installation per arrangement drawings
- **PKG-05:** Foundation acceptance before equipment set
- **DEL-14:** Piping system ready for connection and flush
- **PKG-19/20:** Electrical power available and motor connections verified

**Source:** Installation dependencies

#### IF-2: Testing Coordination

Performance testing shall coordinate with:

- **DEL-12:** Metering system operational for flow measurement
- **DEL-14:** Piping system commissioned and ready for pump operation
- **PKG-19/20:** Electrical power and controls operational
- **PKG-29/30:** Instrumentation calibrated and operational

**Source:** Commissioning dependencies

### Quality Requirements

#### QR-1: Record Documentation Standards

All records shall:

- Be legible and complete
- Include equipment identification (tag number, location)
- Include date, personnel, and witness signatures
- Include calibration certificates for test instruments (where applicable)
- Be reviewed and approved by QA/QC personnel

**Source:** Project quality management plan

#### QR-2: Test Instrumentation Requirements

Test instruments shall be:

- Calibrated and traceable to national standards
- Calibration certificates current (within 1 year typical)
- Appropriate accuracy for measurements (flow: ±2%, pressure: ±0.5% typical)

**Source:** ISO 9906 (test instrumentation requirements)

## Standards

### Primary Standards

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (Section 6: Installation, operation, and testing)
- **API 682** — Shaft Sealing Systems for Centrifugal and Rotary Pumps
- **ISO 9906** — Rotodynamic Pumps—Hydraulic Performance Acceptance Tests (Grade 2)
- **ISO 10816** — Mechanical Vibration—Evaluation of Machine Vibration
- **ACI 318** / **CSA A23.3** — Structural Concrete (grouting requirements)
- **WorkSafeBC** — Occupational Health and Safety Regulation (safety requirements)

**Source:** Standards for pump installation and commissioning

## Verification

### Installation Verification

| Activity | Verification Method | Acceptance |
|----------|---------------------|------------|
| **Foundation** | Visual inspection, levelness check | Level within tolerance, proper finish |
| **Equipment set** | Survey or laser level | Elevations per drawings |
| **Alignment** | Dial indicator or laser alignment | Within API 610 and manufacturer tolerance |
| **Grouting** | Visual inspection, curing time | Proper mix, no voids, adequate curing |
| **Piping** | Strain gauge or bolt torque check | No excessive loads on nozzles |

**Source:** API 610 Section 6.1 (installation verification)

### Performance Test Verification

| Parameter | Measurement | Verification |
|-----------|-------------|--------------|
| **Flow** | Calibrated flow meter | Compare to calculation (DEL-15.03) and spec (DEL-15.02) |
| **Head** | Pressure gauges + calculation | Compare to vendor curve (DEL-15.04) |
| **Vibration** | Vibration analyzer | Compare to API 610 Figure 15 limits |
| **Overall performance** | Test data analysis | Within ISO 9906 Grade 2 tolerance |

**Source:** API 610 Section 6.9 (performance test verification)

## Documentation

### Record Package Deliverables

For each pump:

1. **FAT Records** (if FAT performed) — Shop test reports from vendor
2. **Installation Records** — Foundation, setting, alignment, grouting documentation
3. **Pre-Start Records** — Pre-commissioning inspection checklists
4. **Performance Test Records** — Test data sheets with measurements and calculations
5. **Vibration Analysis Records** — Vibration test results and analysis
6. **Acceptance Certificates** — Final acceptance sign-off by QA/QC and Employer (if required)

**Source:** `_CONTEXT.md` (anticipated artifacts)

### Record Management

- **Filing location:** `1_Working/DEL-15.05_Pump_Installation_and_Test_Records/` organized by pump tag number
- **Record retention:** Permanent (facility life, 25+ years)
- **Distribution:** Provide to operations, maintenance, and Employer per contract requirements

**Source:** Project quality and document control procedures

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Record types and content requirements
- Guidance.md — Installation and testing best practices
- Procedure.md — Step-by-step installation and testing procedures
- DEL-15.01 — Pump Design Drawing Set (installation per drawings)
- DEL-15.02 — Pump Technical Specification (performance requirements)
- DEL-15.03 — Pump Design Calculations (calculated performance for comparison)
- DEL-15.04 — Pump Data Sheet Package (vendor data baseline)
