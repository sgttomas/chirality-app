# Datasheet: DEL-11.04 Marine Loading Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-11.04 |
| Name | Marine Loading Data Sheet Package |
| Package | PKG-11 Marine Loading System |
| Discipline | Process |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Objectives Mapping

This deliverable contributes to the following project objectives (per decomposition Section 6):
- **OBJ-1 Safe & Reliable Operation** — datasheets specify safety-critical parameters (ERC, leak detection, hazardous area ratings)
- **OBJ-2 Throughput Capacity (1,000,000 MT/annum)** — datasheets define equipment capacity supporting design throughput
- **OBJ-4 Operational Flexibility** — datasheets specify operating ranges for diverse operating conditions
- **OBJ-7 Environmental Protection** — datasheets specify leak detection and containment equipment parameters

## Attributes

| Attribute | Value |
|-----------|-------|
| Datasheet register/index | **TBD** — list of datasheets with tags, titles, revisions |
| Equipment tags | **TBD** — per project tag numbering convention |
| Service descriptions | **TBD** — per process descriptions |
| Operating conditions source | DEL-11.02 Technical Specification, DEL-11.03 Calculations |
| Revision | **TBD** |
| Classification | **TBD** (e.g., IFC/IFA per project conventions) |

## Conditions

**Operating / Environmental Context:**

Defines and substantiates marine loading equipment in accordance with Employer's Requirements (ER), providing procurement basis and technical evaluation criteria.

**Design basis (to be confirmed from DEL-11.02 and DEL-11.03):**

| Parameter | Value | Source |
|-----------|-------|--------|
| Product | Canola oil (refined vegetable oil) | DEL-11.02 §3 |
| Design loading rate | **TBD** m³/hr | DEL-11.02 §3 |
| Operating temperature | **TBD** (typical 20–60°C) | DEL-11.02 §3 |
| Design pressure | **TBD** barg | DEL-11.02 §3 |
| Ambient temperature range | **TBD** (approx. –10°C to +35°C) | Site data |
| Environmental classification | Marine/coastal (salt spray, humidity) | Site conditions |
| Hazardous area classification | **TBD** — Zone 2 at loading arm (**ASSUMPTION**) | PKG-27 |
| Design life | **TBD** — 25 years minimum (**ASSUMPTION**) | ER **TBD** |

## Construction

**Datasheet package contents (from decomposition):**

| Datasheet | Equipment/System | Key Parameters |
|-----------|-----------------|----------------|
| Marine loading arm data sheet | Powered loading arm with ERC | Reach, envelope, connections, materials, controls |
| Leak detection system data sheet | Annulus/drip tray/sump detection | Sensor type, zones, alarm outputs, hazardous area |
| Sump pump data sheet | Containment sump pump | Duty point, materials, motor, hazardous area |

**Datasheet field structure (typical — per equipment type):**

### Marine Loading Arm Data Sheet Fields

| Field Category | Required Fields |
|----------------|-----------------|
| Identification | Tag, service, location, P&ID reference |
| Design conditions | Design pressure, design temperature, product |
| Operating conditions | Operating pressure, operating temperature, flow rate |
| Mechanical | Arm type, reach (outboard/inboard), slew/luff range |
| ERC | Type, release force, spillage limit, reset method |
| Materials | Wetted parts, seals/gaskets, external coating |
| Connections | Vessel connection (size, rating, type), shore connection |
| Controls | Local/remote controls, position feedback, permissives |
| Electrical/I&C | Motor power, signal interfaces, ESD integration |
| Hazardous area | Zone classification, certification requirements |
| Vendor data | OEM, model, compliance statements |

### Leak Detection System Data Sheet Fields

| Field Category | Required Fields |
|----------------|-----------------|
| Identification | Tag, service, location |
| Detection philosophy | Annulus monitoring, drip tray, sump level |
| Sensor type | Technology (vacuum, pressure, liquid sensing) |
| Zones | Zone ID, coverage area, sensor count |
| Alarm outputs | Alarm setpoint, trip setpoint, signal type |
| I&C interfaces | Signal list, ESD integration, PLC I/O |
| Power | Voltage, power consumption |
| Hazardous area | Zone classification, certification |
| Testing | Functional test provisions, test interval |
| Vendor data | Manufacturer, model, compliance |

### Sump Pump Data Sheet Fields

| Field Category | Required Fields |
|----------------|-----------------|
| Identification | Tag, service, location |
| Design duty | Flow, head, fluid (canola oil + rainwater) |
| Operating range | Minimum/maximum flow, head curve |
| Construction | Pump type, materials (wetted/casing) |
| Motor | Power, voltage, enclosure, hazardous area rating |
| Connections | Suction size/rating, discharge size/rating |
| Controls | Level control, run/stop, alarms |
| Testing | Factory test, site test requirements |
| Vendor data | Manufacturer, model, compliance |

## Interfaces (Coordination Items)

Dependencies are coordinated externally (NOT_TRACKED). Datasheets shall identify interface requirements:

| Interface | Adjacent Package/Deliverable | Datasheet Affected |
|-----------|------------------------------|-------------------|
| Electrical power | DEL-20.xx (PKG-20 Electrical) | Loading arm, sump pump |
| I&C signals | DEL-19.xx (PKG-19 Instrumentation) | All datasheets |
| ESD integration | DEL-29.xx (PKG-29 SIS) | Loading arm, leak detection |
| Drainage connections | DEL-03.xx (PKG-03 Drainage) | Sump pump |
| Nitrogen supply | DEL-18.xx (PKG-18 Utilities) | Loading arm (purge) |
| OEM vendor data | DEL-11.06 OEM Qualification | Loading arm |

## Cross-Document Links

| Document | Link Point |
|----------|------------|
| Datasheet.md (this file) | Deliverable attributes and datasheet field structure |
| Specification.md (DEL-11.04) | Datasheet package requirements and acceptance criteria |
| Guidance.md (DEL-11.04) | Engineering rationale for datasheet development |
| Procedure.md (DEL-11.04) | Production workflow and verification checklist |
| DEL-11.01 Drawing Set | Tag numbers and equipment locations |
| DEL-11.02 Technical Specification | Design requirements governing datasheet values |
| DEL-11.03 Design Calculations | Calculated duty points and sizing |
| DEL-11.05 Installation & Test Records | Test records reference datasheet revisions |
| DEL-11.06 OEM Qualification | OEM data populates loading arm datasheet |

## Deliverable Acceptance (Minimum)

| Acceptance Criterion | Verification Method | Reference |
|---------------------|---------------------|-----------|
| Datasheet register provided with tags and revisions | Document review | Specification.md §Requirements |
| Each datasheet includes required fields or marked TBD | Completeness check | Specification.md §Requirements |
| Design basis values consistent with DEL-11.02/11.03 | Consistency check | Procedure.md §Steps |
| Vendor data referenced with revision/date | Traceability check | Specification.md §Requirements |
| Tags consistent with DEL-11.01 drawings | Cross-reference check | Procedure.md §Steps |
| Units and nomenclature per project standards | Standards check | Specification.md §Quality |

## References

- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Decomposition: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-11 / DEL-11.04)
- Employer's Requirements: **TBD** (clause references pending extraction)
- Applicable standards: **TBD** (confirm per ER and project code register)
- `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)
