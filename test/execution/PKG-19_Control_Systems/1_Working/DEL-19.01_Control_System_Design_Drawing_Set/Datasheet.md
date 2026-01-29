# Datasheet: DEL-19.01 Control System Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-19.01 |
| Name | Control System Design Drawing Set |
| Package | PKG-19 Control Systems |
| Discipline | I&C |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md` and Decomposition Section PKG-19

## Attributes

### Drawing Set Characteristics

| Attribute | Value | Specification § | Procedure Step |
|-----------|-------|-----------------|----------------|
| Drawing Types | Control system architecture, network drawings, cabinet layouts, HMI arrangement | FR-01, Documentation | Steps 2–5 |
| Sheet Size | **TBD** — **ASSUMPTION**: Per project CAD standards (typically ISO A1 or ANSI D) | PR-02 | Step 8 |
| Scale | **TBD** — **ASSUMPTION**: As appropriate (NTS for schematics, to-scale for physical layouts) | PR-01 | Steps 2–5 |
| CAD Standard | **TBD** — Employer's Requirements **location TBD** | PR-02 | Step 8 |
| Drawing Numbering | **TBD** — Per project document numbering system | QR-02 | Step 9 |
| Revision Control | **TBD** — Per project revision procedure | QR-02 | Step 9 |
| File Format | **TBD** — **ASSUMPTION**: Native CAD + PDF | Documentation | Step 9 |

**Source:** Standard I&C drawing practice; project-specific requirements TBD pending Employer's Requirements

### Control System Scope

| Attribute | Value | Specification § | Guidance § |
|-----------|-------|-----------------|------------|
| Primary System Type | DCS/PLC system | FR-01, FR-02 | Trade-offs TO-01 |
| HMI Configuration | HMI workstations, remote HMIs | FR-01, Documentation | Trade-offs TO-04 |
| I/O Infrastructure | I/O racks | FR-01 | Considerations §5 |
| Data Management | Historian | FR-01 | Principles |
| Operator Interface | Operator graphics | FR-04 | Considerations §4 |

**Source:** Decomposition PKG-19 Scope

### System Capacity Parameters

| Parameter | Value | Specification § | Related Objective |
|-----------|-------|-----------------|-------------------|
| Throughput Support | 1,000,000 MT/annum canola oil (facility capacity) | FR-02 | OBJ-2 |
| Storage Support | 45,000 MT (3 × 15,000 MT tanks) | FR-04 | OBJ-3 |
| Unloading Stations | 32 railcar positions | FR-04, IR-05 | OBJ-2 |
| Loading Points | Marine loading arms **TBD** — count per DEL-11.xx | IR-05 | OBJ-2, OBJ-4 |
| Metering Points | Custody transfer metering stations **TBD** — count per DEL-12.xx | FR-05 | OBJ-10 |

**Source:** Decomposition Section 1 (Project Overview); OBJ-2 (Throughput Capacity), OBJ-3 (Storage Capacity)

## Conditions

### Operational Context

| Condition | Requirement | Specification § | Guidance § |
|-----------|-------------|-----------------|------------|
| Facility Type | Canola oil transload terminal (rail-to-storage-to-ship) | Scope | Purpose |
| Operating Mode | Both tank storage operations and direct rail-to-ship transfer | FR-04 | Considerations §1 |
| Operational Objective | Safe, efficient, reliable, and continuous use (OBJ-1) | FR-06 | Principles |
| Flexibility Objective | Operational flexibility per OBJ-4 | FR-04 | Trade-offs TO-04 |
| Custody Transfer | Accuracy per OBJ-10 | FR-05 | Principles |

**Source:** Decomposition Section 2 (Project Objectives); OBJ-1, OBJ-4, OBJ-10

### Environmental Context

| Condition | Value |
|-----------|-------|
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |
| Operating Temperature | **TBD** — Employer's Requirements **location TBD** |
| Environmental Classification | **TBD** — **ASSUMPTION**: Outdoor/industrial with marine exposure |
| Hazardous Area Classification | **TBD** — Per facility hazardous area study (see PKG-30 Area Classification deliverables) |
| Seismic Requirements | **TBD** — Employer's Requirements **location TBD** — **ASSUMPTION**: NBC seismic zone per BC location |
| Design Life | **TBD** — Employer's Requirements **location TBD** |

**Source:** Decomposition Section 1; environmental requirements TBD

## Construction

### Drawing Set Content

**Control System Architecture:**
- Overall system topology (DCS/PLC, HMI, historian, field networks)
- Control system hierarchy and functional zones
- System redundancy and fail-over architecture (supporting OBJ-1 reliability)
- Network segmentation (process control, safety, business)

**Network Drawings:**
- Industrial network topology (control network, safety network, field device networks)
- Network device locations and interconnections
- Communication protocols and data flow
- Cybersecurity zones and boundaries **ASSUMPTION**: Per ISA/IEC 62443 concepts

**Cabinet Layouts:**
- Control cabinet arrangements (DCS/PLC cabinets, I/O cabinets, junction boxes)
- Equipment mounting and spatial allocation
- Cable entry/exit provisions
- Cooling and power distribution within cabinets

**HMI Arrangement:**
- HMI workstation locations (control room, field operator stations)
- HMI hardware configuration (monitors, input devices)
- Remote HMI provisions
- Connection to control system and historian

**Source:** `_CONTEXT.md` anticipated artifacts; typical I&C drawing set content **ASSUMPTION**

### Physical Installation Context

| Aspect | Details |
|--------|---------|
| Primary Locations | Control building **TBD** — building location per PKG-21/PKG-22; field locations per process area layouts |
| Cabinet Locations | Control room, MCC building, field junction boxes **TBD** |
| Field Device Interfaces | To field instrumentation (PKG-20), motors/MCCs (PKG-17), safety systems (PKG-23) |
| Installation Environment | Indoor (control building) and outdoor (field enclosures) — environmental ratings **TBD** |

**Source:** Typical control system installation context; specific locations TBD pending site layout drawings

### Standards and Codes

| Standard/Code | Application |
|---------------|-------------|
| ISA 5.1 | Instrumentation symbols and identification |
| ISA 84 / IEC 61511 | Safety instrumented systems (if SIS included in scope) |
| CSA C22.1 | Canadian Electrical Code |
| API 554 | Process instrumentation and control |
| IEC 61131 | **ASSUMPTION**: Programmable controller standards (for PLC/DCS programming architecture) |
| ISA/IEC 62443 | **ASSUMPTION**: Cybersecurity for industrial automation (network security zones) |

**Source:** Typical I&C discipline standards for control system design; specific applicability TBD per Employer's Requirements

## References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Section PKG-19, DEL-19.01
- **Context:** `_CONTEXT.md`
- **Dependencies:** `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally by humans)
- **Reference materials:** See `_REFERENCES.md` and `0_References/` in package directory
- **Cross-references within DEL-19.01:**
  - See `Specification.md` for detailed requirements (FR-01 through FR-06, PR-01 through PR-04, IR-01 through IR-05)
  - See `Guidance.md` for design philosophy, trade-offs, and precedents
  - See `Procedure.md` for drawing production workflow
- **Related deliverables:**
  - DEL-19.02 (Control System Technical Specification) — requirements basis
  - DEL-19.03 (Control System Data Sheet Package) — equipment data
  - DEL-19.04 (Control System Software) — software architecture details
  - DEL-20.xx (Field Instrumentation) — I/O interface points
  - DEL-17.xx (Electrical Power Distribution) — power supply for control system
  - PKG-30 Area Classification — hazardous area boundaries affecting equipment selection
