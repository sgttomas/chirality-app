# Datasheet: DEL-15.02 Pump Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-15.02 |
| Name | Pump Technical Specification |
| Package | PKG-15 Pumps & Rotating Equipment |
| Discipline | Mechanical |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`, decomposition DEL-15.02

## Attributes

### Document Metadata

| Attribute | Value |
|-----------|-------|
| Document Number | **TBD** — Per project document numbering system |
| Specification Type | Equipment Technical Specification (procurement specification) |
| Revision | **ASSUMPTION**: Rev 0 for initial issue |
| Applicable Standard | API 610 (Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries) |
| Classification | **TBD** — Per project document classification system |
| Format | **ASSUMPTION**: Text document (Word/PDF) with technical requirements |

**Source:** Specification type per deliverable classification; API 610 is primary standard for process pumps

### Specification Scope

| Attribute | Value |
|-----------|-------|
| Equipment Covered | Railcar unloading pumps, marine loading pumps, sump pumps, transfer pumps (if applicable) |
| Procurement Purpose | Equipment requisition and vendor quotation/proposal evaluation |
| Design Responsibility | Pump internal design by vendor per API 610; installation design by Contractor per DEL-15.01 |
| Service | CSD canola oil transfer and handling |
| Facility Throughput | 1,000,000 MT/annum (OBJ-2) |

**Source:** `_CONTEXT.md` (anticipated artifacts), decomposition Section 2 (OBJ-2), standard EPC procurement split (vendor equipment design, Contractor installation design)

### Pump Types and Anticipated Specifications

The specification shall address the following pump services:

| Pump Service | Specification Document | Typical Duty |
|-------------|------------------------|--------------|
| **Railcar Unloading Pumps** | Railcar unloading pump specification | Transfer canola oil from railcars to storage tanks or marine loading system |
| **Marine Loading Pumps** | Marine loading pump specification | Transfer canola oil from storage tanks to marine loading arms for ship loading |
| **Sump Pumps** | Sump pump specification | Spill recovery, rainwater drainage, leak collection from containment sumps |
| **Transfer Pumps (if applicable)** | **TBD** — Confirm if separate transfer pumps required for tank-to-tank service |

**Source:** `_CONTEXT.md` (anticipated artifacts); pump duties inferred from facility function and OBJ-4 (operational flexibility: tank storage and direct rail-to-ship transfer)

## Conditions

### Operating Context

**Facility parameters:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Service:** CSD canola oil transload facility
- **Throughput:** 1,000,000 MT/annum (OBJ-2)
- **Storage capacity:** 45,000 MT (3 × 15,000 MT tanks) (OBJ-3)
- **Operations:** Tank storage and direct rail-to-ship transfer (OBJ-4)
- **Railcar capacity:** 32 railcar unloading stations

**Source:** Decomposition Section 1 (Project Overview), Section 2 (Objectives)

### Fluid Properties (CSD Canola Oil)

| Property | Value | Notes |
|----------|-------|-------|
| **Product** | Crush Seed Distillate (CSD) canola oil | Refined vegetable oil |
| **Specific Gravity** | **TBD** — Typically 0.91–0.92 @ 15°C | **ASSUMPTION**: Typical for canola oil; confirm from ER Part 2 or process data |
| **Viscosity** | **TBD** — Typically 40–60 cP @ 20°C | Temperature-dependent; heating may be required for winter operations |
| **Vapor Pressure** | **TBD** — Low (vegetable oil) | NPSH considerations less critical than volatile hydrocarbons |
| **Operating Temperature Range** | **TBD** — Per ER Part 2 | **ASSUMPTION**: 10–50°C typical for vegetable oil handling |
| **Corrosiveness** | Low (non-corrosive, food-grade service) | Material selection less stringent than acid/caustic service |
| **Flammability** | Combustible (Class IIIB per NFPA) | Flash point >200°C typical; not volatile but can burn |

**Source:** **ASSUMPTION** — Typical canola oil properties; specific values TBD per ER Part 2 process data

**Note:** Canola oil viscosity increases significantly at low temperatures. Heating systems (tank heating, trace heating) may be required for winter operations to maintain pumpability. Coordinate with process design and DEL-13 (Storage Tanks).

### Environmental Conditions

| Condition | Value |
|-----------|-------|
| **Ambient Temperature Range** | **TBD** — Per ER Part 1 (site environmental data) — **ASSUMPTION**: -10°C to +35°C (BC coastal climate) |
| **Indoor/Outdoor Installation** | **TBD** — Likely outdoor (industrial terminal environment) |
| **Seismic Design** | **TBD** — Per ER Part 1 (seismic criteria) — **ASSUMPTION**: NBC 2015, Site Class per geotechnical |
| **Coastal/Marine Exposure** | Yes (Fraser River terminal location) — corrosion protection required |
| **Hazardous Area Classification** | **TBD** — Per facility hazardous area classification study (if applicable for canola oil combustible service) |

**Source:** Project location (decomposition Section 1); environmental/seismic criteria TBD pending ER Part 1

### Design Life and Reliability

| Parameter | Value |
|-----------|-------|
| **Design Life** | **TBD** — Per ER Part 1 — **ASSUMPTION**: 25 years typical for industrial equipment |
| **Availability Target** | **TBD** — To support OBJ-1 (safe & reliable operation) and OBJ-2 (throughput capacity) |
| **Redundancy** | **TBD** — Duty/standby configuration likely for critical services (railcar unloading, marine loading) |
| **Maintenance Philosophy** | **TBD** — To support OBJ-9 (lifecycle cost optimization) |

**Source:** OBJ-1, OBJ-2, OBJ-9 from decomposition Section 2; design life TBD per ER

## Construction

### Materials

#### Pump Materials (API 610 Designation)

| Component | Material | API 610 Material Code | Notes |
|-----------|----------|----------------------|-------|
| **Casing** | **TBD** — Cast iron, ductile iron, or carbon steel | **ASSUMPTION**: S-6 (cast iron) or S-1 (carbon steel) typical | Non-corrosive service; food-grade compatible |
| **Impeller** | **TBD** — Cast iron, ductile iron, bronze, or stainless steel | **ASSUMPTION**: Matched to casing material | Wear resistance; food-grade compatible |
| **Shaft** | **TBD** — Carbon steel or stainless steel | **ASSUMPTION**: S-1 (CS) or S-6 (316 SS) | API 610 requires adequate strength and corrosion resistance |
| **Wear Rings** | **TBD** — Bronze or stainless steel | Replaceable component | Minimize impeller/casing wear |
| **Mechanical Seal** | **TBD** — Per API 682 Type 2 or Type 3 | **ASSUMPTION**: Type 2 (externally mounted cartridge) typical | Single or dual seal per service criticality |
| **Seal Faces** | **TBD** — Silicon carbide, tungsten carbide | Hard faces for low-wear, long life | Food-grade compatible |
| **Baseplate** | **ASSUMPTION**: Structural steel ASTM A36 or CSA G40.21 350W | Standard fabricated baseplate | Common to pumps and drivers |

**Source:** API 610 material designations (Annex G); materials TBD per ER Part 2 and vendor proposal

**Food-grade consideration:** Canola oil is a food-grade product. Materials in contact with product should be compatible with food-grade service (typically stainless steel, cast iron, bronze; avoid leaded materials or materials that could contaminate product). **TBD**: Confirm food-grade requirements per ER Part 2.

### Configuration

| Feature | Requirement |
|---------|-------------|
| **Pump Type** | Horizontal or vertical centrifugal pump per API 610 (type selection by service and NPSH requirements) |
| **Stages** | **TBD** — Single-stage typical for low-head services; multi-stage if high head required |
| **Driver Type** | Electric motor (fixed-speed or variable-speed per electrical design) |
| **Coupling Type** | Flexible coupling per API 610 Section 5.4 (spacer type for seal maintenance without motor removal) |
| **Mounting** | Floor-mounted on fabricated baseplate or concrete sole plate |
| **Seal Type** | Mechanical seal per API 682 (single or dual seal per service criticality) |
| **Seal Support System** | **TBD** — API 682 Plan 11 (recirculation), Plan 32 (external flush), or Plan 53A/53B/54 (dual seal with barrier fluid) |

**Source:** API 610 (pump design requirements), API 682 (seal system requirements); specific configuration TBD per DEL-15.03 (calculations) and DEL-15.04 (data sheets)

### Installation Requirements

Installation requirements defined in:
- **DEL-15.01** — Pump Design Drawing Set (arrangement, foundation, piping interface)
- **DEL-15.05** — Pump Installation & Test Records (installation procedures and verification)

**Key installation requirements to be addressed in specification:**
- Foundation design loads (static, dynamic, seismic)
- Anchor bolt requirements
- Grouting requirements per API 610 Section 6.1.4
- Piping support requirements (independence from pump nozzles per API 610 Section 6.2)
- Alignment tolerances per API 610 Section 6.3

**Source:** API 610 Section 6 (installation requirements); cross-reference to DEL-15.01 and DEL-15.05

### Commissioning Requirements

Commissioning requirements defined in:
- **DEL-15.05** — Pump Installation & Test Records (performance testing, vibration analysis, acceptance criteria)

**Key commissioning requirements to be addressed in specification:**
- Factory Acceptance Test (FAT) per API 610 Section 7 (if applicable)
- Performance test requirements (flow, head, power, NPSH) per API 610 Section 6.9
- Vibration acceptance criteria per API 610 Figure 15 or ISO 10816
- Run-in period and initial operation requirements

**Source:** API 610 Section 6.9 (field performance test), Section 7 (shop test); cross-reference to DEL-15.05

## References

### Primary References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section 1: Project Overview, Section 2: Objectives, DEL-15.02 entry)
- **Context:** `_CONTEXT.md` (deliverable identity and anticipated artifacts)
- **Reference Index:** `PKG-15/0_References/_REFERENCE_INDEX.md`
- **Employer's Requirements:**
  - Volume 2 Part 1 (General Requirements) — **location TBD**: seismic, environmental, design life
  - Volume 2 Part 2 (Civil & Process Mechanical Works) — **location TBD**: pump performance requirements, materials, fluid properties
  - Volume 2 Part 3 (Building Works) — if applicable

### Applicable Standards

**Primary pump standards:**
- **API 610** (latest edition) — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
  - **ASSUMPTION**: 11th Edition (2010) or later
  - Covers design, materials, testing, and installation requirements
- **API 682** (latest edition) — Pumps—Shaft Sealing Systems for Centrifugal and Rotary Pumps
  - Covers mechanical seal design and seal support systems

**Piping and pressure equipment:**
- **ASME B31.3** — Process Piping (piping interface requirements)
- **ASME B16.5** — Pipe Flanges and Flanged Fittings
- **CSA B51** — Boiler, Pressure Vessel, and Pressure Piping Code (if applicable to specific services)

**Materials and welding:**
- **ASTM Standards** — Material specifications (e.g., ASTM A48 for cast iron, ASTM A216 for cast steel)
- **ASME Section IX** — Welding and Brazing Qualifications (if welded construction)

**Electrical (motors):**
- **NEMA MG 1** or **IEC 60034** — Rotating Electrical Machines (motor standards)
- **CSA C22.1** — Canadian Electrical Code (electrical installation requirements in BC)

**Testing and quality:**
- **ISO 9906** — Rotodynamic Pumps—Hydraulic Performance Acceptance Tests (Grade 2 typical)
- **ISO 10816** — Mechanical Vibration—Evaluation of Machine Vibration
- **ASME B31.3** — Hydrostatic testing requirements

**Canadian codes:**
- **NBC 2015** — National Building Code of Canada (seismic requirements)
- **WorkSafeBC** — Occupational Health and Safety Regulation (safety requirements)

**Source:** Standards typical for pump procurement specifications in Canadian industrial facilities; specific editions TBD per ER Part 1

### Cross-References

- **DEL-15.01** — Pump Design Drawing Set (installation arrangement, interfaces)
- **DEL-15.03** — Pump Design Calculations (sizing, NPSH, system curves)
- **DEL-15.04** — Pump Data Sheet Package (vendor equipment data)
- **DEL-15.05** — Pump Installation & Test Records (installation verification, commissioning)
- **DEL-10.01–10.05** — Railcar Unloading System (railcar unloading pump duty and interface)
- **DEL-11.01–11.06** — Marine Loading System (marine loading pump duty and interface)
- **DEL-12.01–12.05** — Product Transfer & Metering (transfer pump duties and metering interface)
- **DEL-13.01–13.06** — Storage Tanks (tank suction/discharge requirements)
- **DEL-14.01–14.08** — Process Piping (piping system design, nozzle loads)
- **PKG-19/20** — Electrical packages (motor specifications, power supply)

**Source:** Dependencies inferred from deliverable scope and typical pump system interfaces; formal dependency tracking per `_DEPENDENCIES.md` (NOT_TRACKED)

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle
