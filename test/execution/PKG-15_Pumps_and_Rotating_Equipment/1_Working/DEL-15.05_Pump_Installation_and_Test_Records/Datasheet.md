# Datasheet: DEL-15.05 Pump Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-15.05 |
| Name | Pump Installation & Test Records |
| Package | PKG-15 Pumps & Rotating Equipment |
| Discipline | Mechanical |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`, decomposition DEL-15.05

## Attributes

### Document Metadata

| Attribute | Value |
|-----------|-------|
| Document Type | Installation and commissioning test records (quality records) |
| Record Format | **TBD** — Test data sheets, inspection checklists, photos, signed forms |
| Revision | **TBD** — Typically single issue after test completion (not revised like design documents) |
| Classification | **TBD** — Quality records per project QA/QC procedures |
| Purpose | Provide evidence of proper installation, commissioning, and performance verification |

**Source:** Standard commissioning record types; API 610 Section 6 (installation and testing)

### Record Package Scope

| Attribute | Value |
|-----------|-------|
| Equipment Covered | All pumps for facility: Railcar unloading, marine loading, sump, transfer pumps |
| Quantity | One complete record set per pump unit |
| Record Types | Installation records, FAT records (if applicable), performance test records, vibration analysis, acceptance sign-offs |
| Service | CSD canola oil transfer and handling |

**Source:** `_CONTEXT.md` (anticipated artifacts), API 610 test requirements

### Anticipated Record Deliverables

The installation and test record package shall include:

| Record Type | Content | Timing |
|-------------|---------|--------|
| **FAT Records** | Factory acceptance test reports (if FAT performed) | Before shipment |
| **Installation Records** | Foundation inspection, equipment set and level, alignment records, grouting records | During installation |
| **Pre-Start Checks** | Rotation check, lubrication check, coupling alignment verification, system flush | Before commissioning |
| **Performance Test Records** | Flow, head, power, efficiency measurements; system curve verification | During commissioning |
| **Vibration Analysis Records** | Vibration measurements and acceptance per API 610 or ISO 10816 | During commissioning |
| **Acceptance Sign-Offs** | Contractor QA/QC sign-off, Employer acceptance (if required) | After successful testing |

**Source:** `_CONTEXT.md` (anticipated artifacts), API 610 Section 6 (installation and testing requirements)

## Conditions

### Operating Context

**Facility parameters:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Service:** CSD canola oil transload facility
- **Throughput:** 1,000,000 MT/annum (OBJ-2)
- **Operations:** Tank storage and direct rail-to-ship transfer (OBJ-4)

**Source:** Decomposition Section 1 (Project Overview), Section 2 (Objectives)

### Installation Requirements

Installation records shall document compliance with:

| Requirement | Record Evidence |
|-------------|-----------------|
| **Foundation quality** | Foundation inspection report (levelness, surface finish, anchor bolt embedment) |
| **Equipment setting** | Equipment set to correct elevation and location per DEL-15.01 drawings |
| **Alignment** | Shaft alignment within API 610 tolerances (dial indicator or laser alignment records) |
| **Grouting** | Grout pour records (non-shrink grout, proper thickness, curing time per API 610 Section 6.1.4) |
| **Piping connection** | Piping independence verified (no pipe loads on pump nozzles beyond allowable per API 610 Section 4.2.9) |
| **Electrical connection** | Motor wiring and termination inspection (coordinate with Electrical discipline) |
| **Lubrication** | Lubrication system filled and verified per manufacturer instructions |

**Source:** API 610 Section 6.1 (installation requirements)

### Performance Test Requirements

Performance test records shall document:

| Test Parameter | Measurement Method | Acceptance Criteria |
|----------------|-------------------|---------------------|
| **Flow Rate** | Flow meter or other approved method | Within ±7% of rated flow (ISO 9906 Grade 2) |
| **Discharge Head** | Pressure gauges at suction and discharge | Within ±5% of rated head (ISO 9906 Grade 2) |
| **Power Consumption** | Motor power meter or current/voltage measurement | Consistent with vendor data within tolerance |
| **Efficiency** | Calculated from flow, head, power | **TBD** — Not guaranteed below vendor-stated value |
| **NPSH Verification** | Suction pressure measurement | NPSHA > NPSHR with margin (from DEL-15.03 and vendor data) |
| **Vibration** | Vibration transducers or handheld analyzer | Per API 610 Figure 15 or ISO 10816 limits |
| **Noise Level** | Sound level meter (if specified) | Per WorkSafeBC limits (typically 85 dBA at 1m) |

**Source:** API 610 Section 6.9 (field performance test); ISO 9906 (acceptance tolerances)

### Vibration Acceptance Criteria

Per API 610 Figure 15 or ISO 10816:

**Typical acceptance criteria (API 610 Figure 15):**
- Zone A (Good): Vibration velocity < 2.8 mm/s RMS (for pumps 15–75 kW)
- Zone B (Acceptable): Vibration velocity 2.8–7.1 mm/s RMS
- Zone C (Marginal): Requires investigation
- Zone D (Unacceptable): Requires corrective action

**Measurement locations:**
- Pump bearing housing (horizontal, vertical, axial)
- Motor bearing housing (horizontal, vertical, axial)

**Source:** API 610 Figure 15, ISO 10816-3 (vibration severity for rotating machinery)

## Construction

### Installation Process Flow

**Phase 1: Pre-Installation**
- Foundation inspection
- Equipment receipt inspection
- Rigging plan review

**Phase 2: Installation**
- Equipment set and leveled
- Alignment (rough)
- Grouting
- Curing period (7 days minimum per ACI 318)
- Alignment (final)

**Phase 3: Pre-Commissioning**
- Piping tie-in and flush
- Electrical connections
- Lubrication fill
- Rotation check
- Pre-start inspection

**Phase 4: Commissioning**
- Initial startup (no-load or low-flow)
- Performance test (rated conditions)
- Vibration analysis
- Acceptance sign-off

**Source:** API 610 Section 6 (installation and testing sequence)

### Test Equipment Requirements

**For performance testing:**
- Flow meter (calibrated, traceable)
- Pressure gauges (suction and discharge, calibrated)
- Power meter or current/voltage meters (calibrated)
- Temperature sensors (if required)
- Data acquisition system or manual recording forms

**For vibration analysis:**
- Vibration analyzer (portable or installed transducers)
- Calibrated per ISO 10816 or manufacturer requirements

**Source:** API 610 Section 6.9 (test instrumentation); ISO 9906 (calibration requirements)

### Record Retention Requirements

Installation and test records are permanent quality records:

- **Retention period:** Facility life (25+ years typical)
- **Storage:** Project document management system (electronic)
- **Access:** Available for operations, maintenance, regulatory inspections, warranty claims

**Source:** Project quality management plan; regulatory requirements for permanent facilities

## References

### Primary References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (DEL-15.05 entry)
- **Context:** `_CONTEXT.md` (deliverable identity and anticipated artifacts)
- **Reference Index:** `PKG-15/0_References/_REFERENCE_INDEX.md`

### Applicable Standards

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (Section 6: Installation, operation, and testing)
- **API 682** — Shaft Sealing Systems for Centrifugal and Rotary Pumps (seal commissioning requirements)
- **ISO 9906** — Rotodynamic Pumps—Hydraulic Performance Acceptance Tests (Grade 2 acceptance criteria)
- **ISO 10816** — Mechanical Vibration—Evaluation of Machine Vibration (vibration acceptance)
- **ACI 318** / **CSA A23.3** — Structural Concrete (grouting and curing requirements)
- **WorkSafeBC** — Occupational Health and Safety Regulation (noise limits)

**Source:** Standards for pump installation and commissioning

### Cross-References

- **DEL-15.01** — Pump Design Drawing Set (installation arrangement and details per drawings)
- **DEL-15.02** — Pump Technical Specification (installation and testing requirements specified)
- **DEL-15.03** — Pump Design Calculations (calculated performance for comparison to test results)
- **DEL-15.04** — Pump Data Sheet Package (vendor data as baseline for performance comparison)
- **PKG-05** — Concrete Structures (foundation inspection and acceptance)
- **DEL-14** — Process Piping (piping independence verification, system flush)
- **PKG-19/20** — Electrical packages (motor electrical connections, power supply verification)

**Source:** Dependencies inferred from installation and commissioning activities

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle
