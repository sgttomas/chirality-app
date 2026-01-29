# Datasheet: DEL-11.06 Marine Loading Arm OEM Qualification Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-11.06 |
| Name | Marine Loading Arm OEM Qualification Package |
| Package | PKG-11 Marine Loading System |
| Discipline | Process |
| Type | Document Package |
| Responsible | D&B Contractor (with OEM/Supplier) |
| Status | INITIALIZED |

## Objectives Mapping

This deliverable contributes to the following project objectives (per decomposition Section 6):
- **OBJ-1 Safe & Reliable Operation** — OEM qualification ensures safety-critical equipment meets quality and performance standards
- **OBJ-2 Throughput Capacity (1,000,000 MT/annum)** — OEM capability verification ensures equipment can deliver design capacity
- **OBJ-4 Operational Flexibility** — OEM envelope data confirms operational requirements can be met
- **OBJ-7 Environmental Protection** — OEM compliance statements verify ERC and containment features meet requirements

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Number | **TBD** — per project document control |
| Document type | OEM qualification package (marine loading arm) |
| OEM/Supplier | **TBD** — to be confirmed during procurement |
| Product line | **TBD** — powered marine loading arm with ERC |
| Revision | **TBD** |
| Classification | **TBD** |

## Conditions

**Operating / Environmental Context:**

Defines and substantiates marine loading arm OEM qualification in accordance with Employer's Requirements (ER), demonstrating OEM capability and product compliance prior to procurement commitment.

**Application context:**

| Parameter | Value | Source |
|-----------|-------|--------|
| Product | Canola oil (refined vegetable oil) | DEL-11.02 §3 |
| Design loading rate | **TBD** m³/hr | DEL-11.02 §3 |
| Operating temperature | **TBD** (typical 20–60°C) | DEL-11.02 §3 |
| Ambient temperature range | **TBD** (approx. –10°C to +35°C) | Site data |
| Environmental classification | Marine/coastal (salt spray, humidity) | Site conditions |
| Hazardous area classification | **TBD** — Zone 2 at loading arm (**ASSUMPTION**) | PKG-27 |
| Design life | **TBD** — 25 years minimum (**ASSUMPTION**) | ER **TBD** |

## Construction

**Package contents (from decomposition):**

| Document Category | Content | Status |
|-------------------|---------|--------|
| OEM qualification submission | Company profile, manufacturing capability, quality system | **TBD** |
| Comparable project references | Similar installations, client contacts, performance history | **TBD** |
| Compliance statements | ER compliance, code compliance, deviation register | **TBD** |
| Supporting documentation | Product brochures, GA drawings, datasheets, certificates | **TBD** |

**Detailed package structure:**

### OEM Qualification Submission

| Item | Content |
|------|---------|
| Company profile | OEM history, ownership, financial stability |
| Manufacturing facilities | Factory locations, capacity, capabilities |
| Quality management system | ISO certification, QA procedures, inspection capabilities |
| Design capability | Engineering staff, design tools, type testing facilities |
| After-sales support | Spare parts, service, training, warranty |

### Comparable Project References

| Field | Content |
|-------|---------|
| Project name | Facility identification |
| Location | Country, region, site type |
| Client | Company name (and contact if authorized) |
| Scope | Arm type, size, ERC, product service |
| Date | Installation/commissioning date |
| Performance | Operational history, any issues |

### Compliance Statements

| Document | Content |
|----------|---------|
| ER compliance matrix | Clause-by-clause compliance (or TBD pending clause extraction) |
| Code/standards compliance | OCIMF, ASME, API, IEC compliance statements |
| Deviation register | List of deviations/exceptions with proposed disposition |
| Hazardous area certification | Equipment certification for Zone 2 (or applicable zone) |

### Supporting Documentation

| Document | Content |
|----------|---------|
| Product brochure | Standard product line information |
| GA drawings | Envelope drawings, connection details |
| Datasheets | Standard product specifications |
| Quality certificates | ISO 9001, third-party certifications |
| Test procedures | FAT procedures, type test reports |

## Interfaces (Coordination Items)

Dependencies are coordinated externally (NOT_TRACKED). OEM qualification affects:

| Interface | Adjacent Deliverable | Data Flow |
|-----------|---------------------|-----------|
| Loading arm envelope data | DEL-11.01 Drawing Set | OEM → drawings (envelope constraints) |
| Loading arm specification | DEL-11.02 Technical Specification | OEM → spec (extent of supply) |
| Loading arm datasheet | DEL-11.04 Data Sheet Package | OEM → datasheet (vendor-offered values) |
| FAT procedures | DEL-11.05 Installation & Test Records | OEM → ITR (test scope) |
| Envelope calculations | DEL-11.03 Design Calculations | OEM → calcs (reach/slew data) |

## Cross-Document Links

| Document | Link Point |
|----------|------------|
| Datasheet.md (this file) | Package attributes and content structure |
| Specification.md (DEL-11.06) | Package requirements and acceptance criteria |
| Guidance.md (DEL-11.06) | Engineering rationale for OEM qualification |
| Procedure.md (DEL-11.06) | Package development workflow |
| DEL-11.01 Drawing Set | Receives OEM envelope data for GA drawings |
| DEL-11.02 Technical Specification | Defines requirements OEM must comply with |
| DEL-11.03 Design Calculations | Uses OEM envelope data for verification |
| DEL-11.04 Data Sheet Package | Receives OEM-offered values |
| DEL-11.05 Installation & Test Records | FAT based on OEM procedures |

## Deliverable Acceptance (Minimum)

| Acceptance Criterion | Verification Method | Reference |
|---------------------|---------------------|-----------|
| Package index provided with document list and revisions | Document review | Specification.md §Requirements |
| OEM qualification submission complete | Completeness check | Specification.md §Requirements |
| Comparable project references provided (minimum 3) | Reference review | Specification.md §Requirements |
| Compliance statements with ER traceability | Compliance review | Specification.md §Requirements |
| Deviations explicitly listed with disposition | Deviation review | Specification.md §Quality |
| Supporting documentation complete and revision controlled | Document review | Specification.md §Quality |

## References

- `_REFERENCES.md` — applicable reference document list
- `0_References/` — package reference materials
- Decomposition: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-11 / DEL-11.06)
- Employer's Requirements: **TBD** (clause references pending extraction)
- Applicable standards: **TBD** (confirm per ER and project code register)
- `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)
