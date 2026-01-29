# Datasheet: DEL-31.06 Asset Hierarchy

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-31.06 |
| Name | Asset Hierarchy |
| Package | PKG-31 Documentation & Deliverables |
| Discipline | Project Delivery |
| Type | Document |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Type | Asset Hierarchy Database/Document |
| Scope | All facility assets (equipment, systems, structures, buildings) |
| Structure | Hierarchical (Facility → Systems → Subsystems → Equipment → Components) |
| Content | Asset tags, descriptions, locations, parents/children relationships, criticality, attributes |
| Format | **TBD** — **ASSUMPTION**: Database (e.g., Excel, CMMS-compatible format) and/or document (PDF) |
| Asset Tagging Standard | Per project asset tagging standard; aligned with As-Built Drawings (DEL-31.02) |

**Source:** _CONTEXT.md; Decomposition DEL-31.06 (line 692)

## Conditions

**Purpose:** Asset Hierarchy provides structured asset information for operations, maintenance, asset management, and CMMS integration, supporting lifecycle cost optimization (OBJ-9).

**Key Functions:**
- Defines hierarchical relationships (Facility → Systems → Equipment)
- Provides consistent asset tagging across all documentation
- Enables CMMS data loading and maintenance management
- Supports asset criticality classification and risk-based maintenance
- Provides foundation for asset lifecycle management

**Source:** Decomposition line 692; **ASSUMPTION** per asset management purpose; OBJ-9 (line 67, line 788)

## Construction

**Asset Hierarchy Structure:**

1. **Level 1: Facility** — Canola Oil Transload Facility Phase 1
2. **Level 2: Systems** — Railcar Unloading, Marine Loading, Product Transfer & Metering, Storage Tanks, Process Piping, Pumps, Electrical, Control Systems, Fire Protection, Buildings, Marine Structures, etc.
3. **Level 3: Subsystems** — (as applicable, e.g., Unloading Pump System, Loading Arm System)
4. **Level 4: Equipment** — Individual equipment items (pumps, valves, instruments, electrical panels, etc.)
5. **Level 5: Components** — (optional, for critical equipment sub-components)

**Asset Attributes:**
- Asset Tag (unique identifier)
- Asset Description
- Parent Asset (hierarchical relationship)
- Location (physical location, drawing reference)
- Asset Type/Class
- Criticality (critical, important, routine)
- Manufacturer/Vendor
- Model/Serial Number
- Installation Date
- Warranty Expiration (cross-reference DEL-31.08)

**Source:** **ASSUMPTION** per typical asset hierarchy structure

## References

- Decomposition line 692
- DEL-31.02 As-Built Drawings — asset tagging baseline
- DEL-31.03 Operation Manuals — asset tags alignment
- DEL-31.04 Maintenance Manuals — asset tags alignment
- DEL-31.05 Vendor Documentation — manufacturer/model information
- DEL-31.08 Guarantees & Warranties Register — warranty information
- Employer's Requirements — **TBD**

**Supporting Project Objectives:**
- OBJ-9: Lifecycle Cost Optimization (line 788) — Asset Hierarchy enables effective asset management
