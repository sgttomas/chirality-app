# Datasheet: DEL-12.01 Metering Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-12.01 |
| Name | Metering Design Drawing Set |
| Package | PKG-12 Product Transfer & Metering |
| Discipline | Process |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Number Series | To be issued per project numbering system (TBD; Source: ER Vol 2 Part 1, location TBD) |
| Sheet Size | Per project drawing standards (TBD; Source: ER Vol 2 Part 1, location TBD) |
| Scale | Per feature size and project drafting standards; typical scales: 1:50 for GAs, 1:10 or 1:5 for details (ASSUMPTION) |
| CAD Standard | Project CAD convention (TBD; Source: ER Vol 2 Part 1, location TBD) |
| Revision | 00 (initial issue) |
| Classification | Process — Custody Transfer Metering |
| Drawing Count (Anticipated) | Minimum 3 sheets (metering skid GA, flow meter installation details, proving connection details); actual count TBD based on complexity and service separation (ASSUMPTION) |

## Conditions

### Design Context

| Condition | Value / Description | Source |
|-----------|---------------------|--------|
| Service Application | Custody transfer metering for CSD canola oil at rail unloading and marine loading transfer points | Decomposition:350 |
| Product | CSD (Crude Super Degummed) canola oil | Decomposition:43 |
| Design Throughput | 1,000,000 MT per annum (permitted) | Decomposition:41 |
| Metering Points | Two primary locations: (1) Rail unloading custody transfer; (2) Marine loading custody transfer | Decomposition:350 |
| Operating Temperature Range | TBD (Source: ER Vol 2 Part 2, location TBD) |
| Design Pressure | TBD (Source: ER Vol 2 Part 2, location TBD) |
| Fluid Properties | Vegetable oil; density, viscosity, vapor pressure TBD (Source: ER Vol 2 Part 2, location TBD) |
| Hazardous Area Classification | TBD (Source: ER Vol 2 Part 2, location TBD) |
| Seismic Requirements | TBD (Source: ER Vol 2 Part 1, location TBD) |
| Design Life | TBD (Source: ER Vol 2 Part 1, location TBD) |
| Environmental Exposure | Outdoor installation at Fraser Surrey Terminal; temperature, wind, seismic per site conditions (TBD; ER Vol 2 Part 1) |

### Objective Alignment

| Objective | Relevance to This Deliverable |
|-----------|-------------------------------|
| OBJ-2 Throughput Capacity (1,000,000 MT/a) | Drawings must depict metering arrangements that do not constrain the 1,000,000 MT/a throughput; meter sizing and straight-run geometry per DEL-12.03 calculations must be accurately reflected (Source: Decomposition:781; Specification.md REQ-05) |
| OBJ-10 Custody Transfer Accuracy | Drawings must enable accurate custody transfer measurement; meter run geometry, straight-run requirements, flow conditioning (if any), instrument tap locations, and proving connections shall be clearly detailed to support measurement accuracy (Source: Decomposition:789; Specification.md REQ-06) |
| OBJ-6 Regulatory Compliance | Drawings must support compliance with Measurement Canada and applicable custody transfer regulations (ASSUMPTION based on Canadian location; TBD verification from ER) |

## Construction

### Anticipated Drawing Content

| Drawing Type | Description | Source |
|--------------|-------------|--------|
| Metering Skid GAs | General arrangement(s) for custody transfer metering skid(s) covering rail unloading and marine loading services; plan and elevation views showing meter runs, associated piping, instruments, structural supports, and access provisions | Decomposition:356; Specification.md REQ-16 |
| Flow Meter Installation Details | Installation details for custody transfer flow meters including meter orientation, upstream/downstream straight-run requirements, flow conditioning devices (if any), instrument tap positions, and mounting details | Decomposition:356; Specification.md REQ-17 |
| Proving Connection Details | Arrangement and connection details for meter proving including prover connection points, isolation valves, drainage provisions, and access for proving equipment (in-line prover, portable prover, or master meter per DEL-12.02) | Decomposition:356; Specification.md REQ-18 |

### Expected Drawing Features and Callouts

#### General Arrangement Features (per Specification.md REQ-16; Procedure.md Step 3.1)

- Tag numbers for flow meters, temperature transmitters, pressure transmitters, density transmitters (if applicable) — consistent with DEL-12.04 data sheets and PKG-14 P&IDs per Specification.md REQ-04
- Meter run orientations and elevations
- Straight-run piping upstream and downstream of meters (dimensions per manufacturer requirements and DEL-12.03) — per Specification.md REQ-07
- Flow conditioning devices (if specified in DEL-12.02)
- Piping tie-in points to upstream/downstream process piping (interface with PKG-14)
- Isolation and control valves
- Drain and vent points
- Structural supports and skid framing (interface with PKG-06)
- Access platforms and walkways for operation and maintenance
- Lifting provisions for equipment installation and removal

#### Electrical and Control Features (per Specification.md REQ-09)

- Electrical/controls interface points (interface with PKG-19, PKG-20)
- Junction boxes and cable routing
- Power supply connection points (interface with PKG-17)
- Conduit routing (if shown; coordinate with PKG-17)
- Hazardous area boundaries (if applicable; coordinate with PKG-17)

#### Installation and Maintenance Features (per Guidance.md constructability and maintainability principles; Procedure.md IC Step 5.3, 5.4)

- Access and maintenance clearances per manufacturer requirements
- Proving equipment access and connection points
- Calibration and inspection access
- Component removal clearances

### Materials and Configuration

- Primary materials (piping, structural, instrument materials) are specified in:
  - DEL-12.02 Metering Technical Specification
  - DEL-12.04 Metering Data Sheet Package
  - Vendor technical documentation (TBD)
- Drawing set shows physical arrangement, dimensions, and spatial relationships
- Material callouts on drawings reference specification sections and data sheets

## References

### Primary Sources

| Reference | Content | Location |
|-----------|---------|----------|
| Decomposition | PKG-12 scope definition, DEL-12.01 definition, objective mappings | Lines 41, 43, 350, 356, 781, 789 |
| ER Vol 2 Part 1 | General requirements, document control, drawing standards, CAD standards, seismic requirements, design life | TBD |
| ER Vol 2 Part 2 | Process mechanical requirements, metering requirements, fluid properties, operating conditions, hazardous area classification | TBD |

### Related Deliverables (PKG-12)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-12.02 Metering Technical Specification | Provides performance requirements, meter technology selection, materials, and workmanship standards that drawings must reflect; proving method specified in DEL-12.02 determines proving connection details shown in drawings (per Specification.md REQ-11) |
| DEL-12.03 Metering Design Calculations | Provides sizing basis (flow rates, pressure drops, straight-run lengths) that must be incorporated into drawing dimensions; straight-run dimensions on drawings shall comply with calculations per Specification.md REQ-07 |
| DEL-12.04 Metering Data Sheet Package | Provides specific instrument parameters, tag numbers, and dimensional data that drawings must accommodate; tag numbers on drawings shall be consistent with data sheets per Specification.md REQ-04 |
| DEL-12.05 Metering Installation & Test Records | Installation and testing are performed per drawings; test records verify compliance with drawing requirements |

### Interface Packages (Coordinated Externally)

Dependencies coordinated externally per dependency mode NOT_TRACKED (see `_DEPENDENCIES.md`):

- PKG-06 Structural Steelwork — skid support structures, platforms, access stairs
- PKG-14 Process Piping — piping tie-ins, supports, isolation valves
- PKG-17 Electrical Power Distribution — power supply to metering equipment
- PKG-19 Control Systems — control architecture, signal routing, HMI integration
- PKG-20 Field Instrumentation — transmitter integration, junction boxes, cable routing

## Cross-Document Traceability

| Document | Link Points |
|----------|-------------|
| Specification.md | Requirements section (REQ-01 through REQ-18) defines minimum drawing content, performance requirements, interface requirements, and quality requirements; Verification section defines review criteria and acceptance criteria that apply to drawing production (per Procedure.md Steps 4-6) |
| Guidance.md | Purpose section explains deliverable intent and downstream use; Principles section explains custody-transfer measurement intent (meter run geometry clarity, instrument tap locations, proving connection accessibility, installation precision) and drawing content principles (completeness, constructability, maintainability, interface clarity); Considerations section identifies design factors (meter technology, straight-run, proving method, environmental conditions, hazardous area classification, product characteristics) that affect drawing content |
| Procedure.md | Steps section defines production workflow (Step 1: Confirm scope and drawing list; Step 2: Collect inputs from DEL-12.02, DEL-12.03, DEL-12.04, PKG-14 P&IDs; Step 3: Draft drawings per anticipated content; Steps 4-6: Self-check, IC, IDC per Specification requirements; Step 7: Issue); Verification section aligns to Specification requirements; Records section identifies drawing outputs matching anticipated artifacts |
