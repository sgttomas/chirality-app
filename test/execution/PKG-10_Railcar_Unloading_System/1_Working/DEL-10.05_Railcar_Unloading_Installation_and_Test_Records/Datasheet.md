# Datasheet: DEL-10.05 Railcar Unloading Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-10.05 |
| Name | Railcar Unloading Installation & Test Records |
| Package | PKG-10 Railcar Unloading System |
| Discipline | Process |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Number Series | **TBD** — per project document numbering procedure |
| Record Category | Construction / Completion Records |
| Retention Period | **TBD** — per Employer's Requirements / regulatory |
| Format | **TBD** — per project quality procedures |
| Revision | **TBD** — per project document control procedure |
| Classification | **TBD** — per project security/confidentiality requirements |

## Conditions

**Operating / Environmental Context:**

The Installation & Test Records provide evidence of completion, inspection, and testing for the railcar unloading system. The system comprises 32 unloading stations with associated equipment including unloading arms, quick-connects, gravity flow header, containment, and sump pumps. (**Source:** decomposition; README)

**Equipment Requiring Records:**

| Equipment | Quantity | Record Types Required |
|-----------|----------|----------------------|
| Unloading Arms | 32 | FAT, installation, functional test |
| Quick-Connect Couplers | 32 sets | Part of arm FAT/installation |
| Gravity Flow Header | 1 system | Installation, hydrostatic test |
| Spill Containment Pans | Multiple | Installation, leak test |
| Collection System | 1 system | Installation, drainage test |
| Sump Pumps | **TBD** | FAT, installation, functional test |
| Flow Indicators | 32 | Installation, calibration (PKG-20) |

**Test/Inspection Parameters:**

| Test Type | Applicable Equipment | Acceptance Criteria |
|-----------|---------------------|---------------------|
| Factory Acceptance Test (FAT) | Unloading arms, sump pumps | Vendor test per specification |
| Installation Inspection | All equipment | Per DEL-10.01 drawings |
| Hydrostatic Test | Header piping | Per DEL-10.02 specification (**TBD** pressure/duration) |
| Leak Test | Containment, connections | No visible leaks |
| Functional Test | Arms, pumps, controls | Per DEL-10.02 specification |

## Construction

**Record Package Structure (Anticipated Artifacts):**

| Record Type | Content | Quantity | Cross-Reference |
|-------------|---------|----------|-----------------|
| FAT Records | Factory acceptance test results for equipment | 32+ (arms) + pumps | DEL-10.02 (specification); DEL-10.04 (data sheets) |
| Installation Records | Installation inspection and completion records | All equipment | DEL-10.01 (drawings); DEL-10.02 (specification) |
| Hydrostatic Test Records | Pressure test results for header piping | Per test section | DEL-10.02 (specification) |

**Typical FAT Record Content:**

| Section | Content |
|---------|---------|
| Equipment identification | Tag, model, serial number |
| Test reference | Specification, test procedure |
| Test conditions | Date, location, witness |
| Test results | Measurements, observations |
| Pass/fail determination | Acceptance criteria compliance |
| Signatures | Vendor, contractor, employer witness |
| Attachments | Test certificates, calibration records |

**Typical Installation Record Content:**

| Section | Content |
|---------|---------|
| Equipment identification | Tag, location, drawing reference |
| Installation checklist | Alignment, supports, connections |
| Inspection results | Dimensional checks, visual inspection |
| As-built notes | Deviations from design |
| Signatures | Installer, inspector, QA/QC |
| Attachments | Photos, NCRs (if any) |

**Typical Hydrostatic Test Record Content:**

| Section | Content |
|---------|---------|
| System/section identification | Test boundary, drawing reference |
| Test parameters | Pressure, duration, medium |
| Test conditions | Date, ambient temperature |
| Test results | Pressure readings, hold time, observations |
| Pass/fail determination | Per specification criteria |
| Signatures | Test engineer, QA/QC, witness |
| Attachments | Pressure charts, calibration certificates |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-10 scope; DEL-10.05 definition; objectives (OBJ-1, OBJ-2, OBJ-4, OBJ-7) |
| Employer's Requirements Vol 2 Pt 1 | `test/Volume_2_Part_1_Employers_Requirements.pdf` | Record requirements (**TBD** clauses) |
| Employer's Requirements Vol 2 Pt 2 | `test/Volume_2_Part_2_Employers_Requirements.pdf` | Test requirements (**TBD** clauses) |
| Employer's Requirements Vol 2 Pt 3 | `test/Volume_2_Part_3_Employers_Requirements.pdf` | Quality requirements (**TBD** clauses) |
| DEL-10.01 | PKG-10 folder | Design Drawing Set (installation reference) |
| DEL-10.02 | PKG-10 folder | Technical Specification (test requirements) |
| DEL-10.03 | PKG-10 folder | Design Calculations (acceptance criteria basis) |
| DEL-10.04 | PKG-10 folder | Data Sheet Package (equipment identification) |
| Specification.md | This deliverable folder | Requirements for record package |
| Guidance.md | This deliverable folder | Record principles |
| Procedure.md | This deliverable folder | Record collection workflow |
| _DEPENDENCIES.md | This deliverable folder | NOT_TRACKED — dependencies coordinated externally |
