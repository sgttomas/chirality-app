# Specification: DEL-15.04 Pump Data Sheet Package

## Scope

This specification defines the requirements for the **Pump Data Sheet Package** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility at Fraser Surrey Terminal, Surrey, BC.

**Deliverable scope:** Defines and substantiates pumps in accordance with ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.04 entry

### Purpose

The Pump Data Sheet Package shall:

1. **Document as-purchased equipment** — Capture vendor-supplied pump and motor technical data
2. **Verify specification compliance** — Confirm vendor equipment meets DEL-15.02 specification requirements
3. **Support downstream design** — Provide data for DEL-15.01 (arrangement), PKG-05 (foundations), commissioning
4. **Enable O&M** — Provide baseline data for operations, maintenance, and troubleshooting

**Source:** Standard purpose of vendor data packages in EPC projects

### Equipment Covered

| Equipment Type | Data Sheet Required |
|----------------|---------------------|
| **Railcar Unloading Pumps** | Pump + motor data sheets |
| **Marine Loading Pumps** | Pump + motor data sheets |
| **Sump Pumps** | Pump + motor data sheets |
| **Transfer Pumps (if applicable)** | Pump + motor data sheets |

**Source:** `_CONTEXT.md` (anticipated artifacts)

### Included

- Pump performance data sheets (flow, head, NPSH, efficiency, power)
- Pump construction data sheets (materials, dimensions, weights)
- Motor data sheets (electrical ratings, dimensions, weights)
- Performance curves (head-flow-efficiency-power-NPSH)
- Outline drawings (general arrangement with dimensions)
- Foundation loads (static and dynamic)

**Source:** API 610 Section 8.2 (vendor data requirements)

### Excluded

- Vendor internal design calculations (proprietary)
- Detailed fabrication drawings (vendor internal use)
- Installation procedures (covered under DEL-15.05)
- Commissioning test procedures (covered under DEL-15.05)

**Source:** Standard vendor data scope

## Requirements

### Functional Requirements

#### FR-1: Document Required Pump Data

For each pump, data sheets shall include:

**Performance data:**
- Rated flow, head, power, speed, efficiency
- NPSH required at rated flow and other operating points
- Minimum continuous stable flow
- Performance curves showing head, efficiency, power, NPSH vs. flow

**Construction data:**
- Pump type (API 610 designation)
- Materials of construction (per API 610 Annex G)
- Mechanical seal type and support system (per API 682)
- Coupling type
- Dimensions and weights

**Source:** API 610 Section 8.2

#### FR-2: Document Required Motor Data

For each motor, data sheets shall include:

- Rated power (kW or HP)
- Voltage, frequency, phases
- Speed (RPM)
- Efficiency class (NEMA Premium or IEC IE3 minimum)
- Enclosure type (TEFC, ODP, explosion-proof)
- Dimensions and weight
- Terminal box location

**Source:** NEMA MG 1 / IEC 60034 motor data requirements; coordinate with Electrical discipline

### Performance Requirements

#### PR-1: Specification Compliance Verification

Vendor data shall be reviewed for compliance with DEL-15.02 specification:

| Requirement | Specification Value | Vendor Data Check |
|-------------|---------------------|-------------------|
| **Flow rate** | Per DEL-15.03 calculation | Vendor pump meets flow within API 610 tolerance (±7% per ISO 9906 Grade 2) |
| **Head** | Per DEL-15.03 calculation | Vendor pump meets head within API 610 tolerance (±5% per ISO 9906 Grade 2) |
| **NPSH** | NPSHR ≤ NPSHA - 0.5m (from DEL-15.03) | Vendor NPSHR satisfies margin requirement |
| **Efficiency** | Not guaranteed below specified value | Vendor efficiency meets or exceeds specified minimum |
| **Materials** | Per DEL-15.02 specification | Vendor materials comply with specification and API 610 Annex G |

**Source:** API 610 Section 3 (performance), ISO 9906 Grade 2 (tolerance)

#### PR-2: Operating Point Verification

Vendor pump curve shall be plotted against calculated system curve (from DEL-15.03):

- **Operating point** = Intersection of pump curve and system curve
- **Acceptance criteria:** Operating point within 70–120% of pump best efficiency point (BEP) per API 610

**Source:** API 610 Section 3 (preferred operating region)

### Interface Requirements

#### IF-1: Installation Design Interface

Vendor data shall provide information for DEL-15.01 (pump arrangement):

- Pump and motor outline dimensions
- Nozzle locations, sizes, orientations
- Baseplate dimensions
- Clearances for maintenance
- Lifting lug locations and capacities

**Source:** DEL-15.01 uses vendor data for arrangement drawings

#### IF-2: Foundation Design Interface

Vendor data shall provide information for PKG-05 (foundation design):

- Pump, motor, and baseplate weights (dry and operating)
- Static loads (vertical, horizontal)
- Dynamic loads (unbalanced forces, seismic)
- Anchor bolt requirements (number, size, pattern)

**Source:** PKG-05 uses vendor data for foundation design calculations

#### IF-3: Electrical Design Interface

Vendor motor data shall be provided to PKG-19/20 (Electrical discipline):

- Motor power rating
- Voltage and starting characteristics
- Terminal box location and conduit entry

**Source:** Electrical discipline uses motor data for power supply and control design

### Quality Requirements

#### QR-1: Data Submittal and Approval Process

Vendor data shall follow submittal process:

1. **Rev 0 (Initial Submittal):** Vendor submits after contract award
2. **Contractor Review:** Review for specification compliance and technical adequacy
3. **Comment Resolution:** Vendor addresses Contractor comments
4. **Rev A (Resubmittal):** Vendor resubmits with comments incorporated
5. **AFC (Approved for Construction):** Contractor approves for use in downstream design

**Source:** Standard EPC vendor data approval process

#### QR-2: Data Completeness

All required data sheets and drawings must be submitted:

- Pump performance data sheet ✓
- Pump construction data sheet ✓
- Motor data sheet ✓
- Performance curves ✓
- Outline drawings ✓
- Foundation loads ✓

Incomplete submittals will be returned for completion before review.

**Source:** API 610 Section 8.2 (complete data package requirement)

#### QR-3: Data Accuracy

Vendor data shall be:

- **Accurate:** Dimensions match drawings; performance data matches test results
- **Consistent:** Data sheets, curves, and drawings are internally consistent
- **Traceable:** Data is traceable to shop test results and approved drawings

**Source:** Quality requirements for vendor technical data

## Standards

### Primary Standards

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (Section 8.2: Technical data)
- **API 682** — Shaft Sealing Systems for Centrifugal and Rotary Pumps (seal data requirements)
- **ISO 9906** — Rotodynamic Pumps—Hydraulic Performance Acceptance Tests (Grade 2 tolerance)
- **NEMA MG 1** or **IEC 60034** — Rotating Electrical Machines (motor data)

**Source:** Standards governing pump and motor data requirements

## Verification

### Data Review Verification

| Review Item | Method | Acceptance Criteria |
|-------------|--------|---------------------|
| **Completeness** | Checklist review | All required data sheets and drawings provided |
| **Performance compliance** | Compare to DEL-15.02 specification | Flow, head, NPSH, efficiency within tolerance |
| **NPSH margin** | Compare to DEL-15.03 calculation | Vendor NPSHR ≤ Calculated NPSHA - 0.5m |
| **Operating point** | Plot pump curve vs. system curve | Operating point within 70–120% BEP |
| **Materials compliance** | Compare to DEL-15.02 specification | Materials match specification |
| **Dimensions accuracy** | Review outline drawings | Dimensions suitable for DEL-15.01 arrangement |

**Source:** Standard vendor data review process

### Approval Sign-Off

Data shall receive sign-offs:

1. **Reviewer:** Mechanical engineer reviews data for compliance
2. **Checker:** Independent check for critical items (NPSH, operating point)
3. **Approver:** Lead engineer approves for construction use (AFC)

**Source:** Standard vendor data approval process

## Documentation

### Data Sheet Package Deliverables

For each pump service:

1. **Pump Data Sheets** — Performance and construction data
2. **Motor Data Sheets** — Electrical and mechanical data
3. **Performance Curves** — Graphical performance data
4. **Outline Drawings** — Arrangement and dimensions
5. **Foundation Data** — Loads for foundation design

**Source:** `_CONTEXT.md` (anticipated artifacts), API 610 Section 8.2

### Record Management

- **Filing location:** `1_Working/DEL-15.04_Pump_Data_Sheet_Package/` with vendor data organized by pump tag number
- **Revision control:** Track vendor data revisions (Rev 0, Rev A, AFC)
- **Distribution:** Provide AFC data to DEL-15.01, PKG-05, PKG-19/20, DEL-15.05
- **Retention:** Per ER requirements — **TBD** — **ASSUMPTION**: Retain for facility life (25+ years)

**Source:** Project document control procedures

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Vendor data content and requirements
- Guidance.md — Data review principles and common issues
- Procedure.md — Data submittal and review process
- DEL-15.01 — Pump Design Drawing Set (uses vendor outline drawings)
- DEL-15.02 — Pump Technical Specification (vendor data verified against spec)
- DEL-15.03 — Pump Design Calculations (vendor data verified against calculations)
- DEL-15.05 — Pump Installation & Test Records (vendor data used for commissioning)
