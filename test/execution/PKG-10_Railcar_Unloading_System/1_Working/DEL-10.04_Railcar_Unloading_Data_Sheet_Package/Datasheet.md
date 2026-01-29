# Datasheet: DEL-10.04 Railcar Unloading Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-10.04 |
| Name | Railcar Unloading Data Sheet Package |
| Package | PKG-10 Railcar Unloading System |
| Discipline | Process |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Data Sheet Number Series | **TBD** — per project document numbering procedure |
| Total Data Sheet Count | 32+ (32 unloading arms + quick-connects + sump pump) |
| Equipment Tag Scheme | **TBD** — per project tagging standard |
| Format/Template | **TBD** — per Employer's Requirements / project standards |
| Revision | **TBD** — per project document control procedure |
| Classification | **TBD** — per project security/confidentiality requirements |

## Conditions

**Operating / Environmental Context:**

The Railcar Unloading Data Sheet Package defines and substantiates equipment for the railcar unloading system serving the Canola Oil Transload Facility. The facility has a permitted throughput of 1,000,000 MT/annum with 32 railcar unloading stations. (**Source:** decomposition; README)

**Equipment Covered:**

| Equipment | Quantity | Tag Range | Purpose |
|-----------|----------|-----------|---------|
| Unloading Arms | 32 | **TBD** (e.g., UA-1001 to UA-1032) | Railcar-to-header product transfer |
| Quick-Connect Couplers | 32 sets | Part of arm assembly | Railcar connection/disconnection |
| Sump Pumps | **TBD** (1 or more) | **TBD** (e.g., P-1001) | Containment drainage |

**Design Conditions (common to equipment):**

| Parameter | Value | Source |
|-----------|-------|--------|
| Product | Canola oil (food-grade vegetable oil) | Decomposition |
| Product density | **TBD** — ~920 kg/m³ at 15°C typical | Product data |
| Product viscosity | **TBD** — temperature dependent | Product data |
| Operating temperature range | **TBD** — per product and site conditions | ER clauses **TBD** |
| Design pressure | **TBD** — gravity flow (low pressure) | Design basis |
| Design temperature | **TBD** — per project design basis | ER clauses **TBD** |
| Hazardous area classification | **TBD** — per HAC study | ER clauses **TBD** |
| Ambient temperature range | **TBD** — Fraser Surrey climate | Site data |
| Seismic requirements | **TBD** — per BC Building Code | ER clauses **TBD** |
| Design life | **TBD** — per Employer's Requirements | ER clauses **TBD** |

## Construction

**Data Sheet Package Structure (Anticipated Artifacts):**

| Data Sheet Type | Quantity | Content | Cross-Reference |
|-----------------|----------|---------|-----------------|
| Unloading Arm Data Sheets | 32 | Individual arm specifications | DEL-10.01 Arm Arrangement; DEL-10.02 Arm Spec |
| Quick-Connect Coupler Data Sheets | 32 or combined | Coupler specifications | DEL-10.02 Containment Spec |
| Sump Pump Data Sheet | 1+ | Pump specifications | DEL-10.01 Containment Details; DEL-10.02 Containment Spec |

**Typical Unloading Arm Data Sheet Fields:**

| Field Category | Example Fields |
|----------------|----------------|
| Identification | Tag number, service, location, P&ID reference |
| Process conditions | Product, flow rate, temperature, pressure |
| Mechanical | Arm type, size, reach, materials, joints |
| Connection | Quick-connect type, railcar connection size |
| Controls | Limit switches, position indication |
| Materials | Wetted parts, seals, gaskets |
| Standards | Applicable codes, certifications |

**Typical Sump Pump Data Sheet Fields:**

| Field Category | Example Fields |
|----------------|----------------|
| Identification | Tag number, service, location |
| Process conditions | Fluid, flow rate, head, temperature |
| Mechanical | Pump type, size, driver, materials |
| Electrical | Motor data, area classification |
| Performance | Curve reference, NPSH, efficiency |
| Materials | Casing, impeller, shaft, seals |
| Standards | Applicable codes, certifications |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope; DEL-10.04 definition; objectives (OBJ-1, OBJ-2, OBJ-4, OBJ-7) |
| Employer's Requirements Vol 2 Pt 1 | `test/Volume_2_Part_1_Employers_Requirements.pdf` | Equipment requirements (**TBD** clauses) |
| Employer's Requirements Vol 2 Pt 2 | `test/Volume_2_Part_2_Employers_Requirements.pdf` | Technical requirements (**TBD** clauses) |
| Employer's Requirements Vol 2 Pt 3 | `test/Volume_2_Part_3_Employers_Requirements.pdf` | Quality requirements (**TBD** clauses) |
| DEL-10.01 | PKG-10 folder | Design Drawing Set (equipment locations, arrangements) |
| DEL-10.02 | PKG-10 folder | Technical Specification (performance/material requirements) |
| DEL-10.03 | PKG-10 folder | Design Calculations (sizing basis) |
| DEL-10.05 | PKG-10 folder | Installation & Test Records (FAT/site verification) |
| Specification.md | This deliverable folder | Requirements for data sheet package |
| Guidance.md | This deliverable folder | Data sheet principles |
| Procedure.md | This deliverable folder | Data sheet workflow |
| _DEPENDENCIES.md | This deliverable folder | NOT_TRACKED — dependencies coordinated externally |
