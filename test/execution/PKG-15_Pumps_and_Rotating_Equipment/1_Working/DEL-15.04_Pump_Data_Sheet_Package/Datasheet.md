# Datasheet: DEL-15.04 Pump Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-15.04 |
| Name | Pump Data Sheet Package |
| Package | PKG-15 Pumps & Rotating Equipment |
| Discipline | Mechanical |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`, decomposition DEL-15.04

## Attributes

### Document Metadata

| Attribute | Value |
|-----------|-------|
| Document Type | Vendor-supplied equipment data sheets (pump and motor) |
| Data Sheet Format | **TBD** — Vendor format (typically standardized forms per API 610) |
| Revision | **TBD** — Tracks vendor data revisions (Rev 0 initial submittal, Rev A approved for construction, etc.) |
| Classification | **TBD** — Per project document classification system |
| Data Source | Pump equipment vendor (selected per DEL-15.02 specification) |

**Source:** Standard vendor data package content; API 610 Section 8.2 (technical data requirements)

### Data Sheet Package Scope

| Attribute | Value |
|-----------|-------|
| Equipment Covered | All pumps for facility: Railcar unloading, marine loading, sump, transfer pumps |
| Quantity | **TBD** — One data sheet per pump unit; one motor data sheet per motor |
| Purpose | Document as-purchased pump and motor specifications; support installation design (DEL-15.01), commissioning (DEL-15.05), and O&M |
| Service | CSD canola oil transfer and handling |

**Source:** `_CONTEXT.md` (anticipated artifacts), project pump requirements

### Anticipated Data Sheet Deliverables

The data sheet package shall include:

| Document Type | Content | Quantity |
|---------------|---------|----------|
| **Pump Data Sheets** | Performance, materials, dimensions, weights for each pump | One per pump unit (**TBD**: total quantity) |
| **Motor Data Sheets** | Electrical ratings, dimensions, weights for each motor | One per motor (**TBD**: total quantity) |
| **Performance Curves** | Head-flow-efficiency-power-NPSH curves | One set per pump model |
| **Outline Drawings** | General arrangement, nozzle schedule, dimensions | One per pump model |
| **Foundation Loads** | Static and dynamic loads for foundation design | One per pump model |

**Source:** `_CONTEXT.md` (anticipated artifacts), API 610 Section 8.2 (vendor data requirements)

## Conditions

### Operating Context

**Facility parameters:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Service:** CSD canola oil transload facility
- **Throughput:** 1,000,000 MT/annum (OBJ-2)
- **Operations:** Tank storage and direct rail-to-ship transfer (OBJ-4)

**Source:** Decomposition Section 1 (Project Overview), Section 2 (Objectives)

### Pump Performance Data

Each pump data sheet shall document:

| Parameter | Content |
|-----------|---------|
| **Rated Flow** | Normal operating flow rate (m³/hr or L/s) |
| **Rated Head** | Total dynamic head at rated flow (m) |
| **NPSH Required** | Vendor NPSHR at rated flow (m) — must be less than calculated NPSHA with margin per DEL-15.03 |
| **Efficiency** | Pump efficiency at rated flow (%) |
| **Power** | Pump brake horsepower at rated flow (kW or HP) |
| **Speed** | Operating speed (RPM) |
| **Impeller Diameter** | Impeller size (mm or inches) |
| **Minimum Flow** | Minimum continuous stable flow (m³/hr) |

**Source:** API 610 Section 8.2 (performance data requirements), DEL-15.03 (calculated requirements for comparison)

### Pump Construction Data

Each pump data sheet shall document:

| Parameter | Content |
|-----------|---------|
| **Pump Type** | API 610 designation (e.g., OH2, BB2, VS1) |
| **Materials** | Casing, impeller, shaft, wear rings, mechanical seal materials per API 610 Annex G |
| **Seal Type** | Mechanical seal per API 682 (Type 1, 2, or 3; single or dual) |
| **Seal Support System** | API 682 piping plan (Plan 11, 32, 53A, etc.) |
| **Coupling** | Coupling type and size |
| **Baseplate** | Baseplate type (fabricated steel, grouted) |
| **Weight** | Pump, motor, and baseplate weights (dry and operating) |

**Source:** API 610 Section 8.2 (construction data requirements)

### Motor Data

Each motor data sheet shall document:

| Parameter | Content |
|-----------|---------|
| **Motor Power** | Rated power (kW or HP) |
| **Voltage** | Rated voltage and phases (e.g., 460V 3-phase) |
| **Speed** | Synchronous speed (RPM) |
| **Efficiency** | Motor efficiency (NEMA Premium or IEC IE3 minimum per DEL-15.02) |
| **Enclosure** | Enclosure type (TEFC, ODP, explosion-proof) |
| **Mounting** | Foot-mounted or flange-mounted |
| **Weight** | Motor weight |
| **Terminal Box Location** | Orientation for conduit entry |

**Source:** Motor data requirements; coordinate with Electrical discipline (PKG-19/20)

## Construction

### Data Sheet Development Process

**Vendor data flow:**

1. **Specification issued** (DEL-15.02) → Vendor proposal → Contract award
2. **Vendor submits initial data** (Rev 0) → Contractor review
3. **Contractor reviews and comments** → Vendor incorporates comments
4. **Vendor resubmits revised data** (Rev A) → Contractor approves for construction (AFC)
5. **AFC data used for downstream design** (DEL-15.01 arrangement, PKG-05 foundations, DEL-15.05 commissioning)

**Source:** Standard EPC vendor data workflow

### Data Sheet Content Requirements

Per API 610 Section 8.2, vendor shall provide:

**Minimum data sheets:**
- Pump performance data sheet (flow, head, NPSH, efficiency, power)
- Pump construction data sheet (materials, dimensions, weights)
- Motor data sheet (electrical ratings, dimensions, weights)

**Supporting documents:**
- Performance curves (head-flow-efficiency-power-NPSH vs. flow)
- Outline drawings (general arrangement with dimensions)
- Cross-sectional drawing (pump internals for maintenance)
- Foundation loads (static and dynamic loads for foundation design)
- Nozzle schedule (size, rating, orientation, location)

**Source:** API 610 Section 8.2 (technical data requirements)

### Data Review and Verification

Contractor shall review vendor data for:

| Review Item | Verification Criteria |
|-------------|----------------------|
| **Performance compliance** | Flow, head, efficiency meet specification (DEL-15.02) within API 610 tolerances |
| **NPSH margin** | Vendor NPSHR ≤ Calculated NPSHA - 0.5m (from DEL-15.03) |
| **Operating point** | Pump operates within preferred operating region (70–120% BEP) when plotted against system curve |
| **Materials compliance** | Materials match specification and are suitable for CSD canola oil service |
| **Code compliance** | Pump design complies with API 610 and applicable codes |
| **Dimensions accuracy** | Dimensions match vendor outline drawings; suitable for installation design (DEL-15.01) |
| **Foundation loads** | Loads provided for foundation design (PKG-05) |

**Source:** Standard vendor data review process; API 610 compliance verification

## References

### Primary References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (DEL-15.04 entry)
- **Context:** `_CONTEXT.md` (deliverable identity and anticipated artifacts)
- **Reference Index:** `PKG-15/0_References/_REFERENCE_INDEX.md`

### Applicable Standards

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (Section 8.2: Technical data requirements)
- **API 682** — Shaft Sealing Systems for Centrifugal and Rotary Pumps (seal documentation requirements)
- **NEMA MG 1** or **IEC 60034** — Rotating Electrical Machines (motor data requirements)

**Source:** Standards for pump and motor data requirements

### Cross-References

- **DEL-15.01** — Pump Design Drawing Set (receives vendor outline drawings and dimensions)
- **DEL-15.02** — Pump Technical Specification (vendor data reviewed against specification requirements)
- **DEL-15.03** — Pump Design Calculations (vendor data verified against calculated requirements: NPSH, operating point)
- **DEL-15.05** — Pump Installation & Test Records (vendor data used for commissioning and performance testing)
- **PKG-05** — Concrete Structures (receives foundation loads for foundation design)
- **PKG-19/20** — Electrical packages (receives motor data for electrical design)

**Source:** Dependencies inferred from data sheet use in downstream deliverables

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle
