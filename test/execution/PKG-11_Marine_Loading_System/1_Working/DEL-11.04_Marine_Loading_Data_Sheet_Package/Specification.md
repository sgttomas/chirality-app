# Specification: DEL-11.04 Marine Loading Data Sheet Package

## Scope

This specification defines the requirements for **Marine Loading Data Sheet Package** within **PKG-11 Marine Loading System**.

**Purpose:** Defines and substantiates marine loading equipment in accordance with Employer's Requirements (ER), providing the procurement basis and technical evaluation criteria for equipment selection and vendor qualification.

**Package scope (PKG-11):**
- Powered loading arm (articulated boom with powered slew/luff)
- Emergency release coupling (ERC)
- Double-walled export pipe
- Leak detection system
- Nitrogen supply provisions
- Operator shelter

**Anticipated deliverable artifacts:**
- Marine loading arm data sheet
- Leak detection system data sheet
- Sump pump data sheet

**Objectives served (per decomposition Section 6):**
- OBJ-1 Safe & Reliable Operation
- OBJ-2 Throughput Capacity (1,000,000 MT/annum)
- OBJ-4 Operational Flexibility
- OBJ-7 Environmental Protection

## Related Deliverables (PKG-11)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-11.01 Marine Loading Design Drawing Set | Provides tag numbers and equipment locations |
| DEL-11.02 Marine Loading Technical Specification | Provides design requirements governing datasheet values |
| DEL-11.03 Marine Loading Design Calculations | Provides calculated duty points and sizing |
| DEL-11.05 Marine Loading Installation & Test Records | References datasheet revisions for verification |
| DEL-11.06 Marine Loading Arm OEM Qualification Package | Provides OEM data for loading arm datasheet |

## Requirements

### General Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| DS-001 | Provide a datasheet register/index with tag numbers, titles, and revision status | Document review |
| DS-002 | Each datasheet shall be uniquely identified with equipment tag number | Document review |
| DS-003 | Datasheets shall be suitable for procurement and technical bid evaluation | Completeness check |
| DS-004 | Datasheets shall provide traceability to ER requirements where applicable | Traceability check |
| DS-005 | Each datasheet shall state input basis (design conditions, assumptions) | Completeness check |
| DS-006 | Vendor data shall be revision controlled and referenced | Traceability check |
| DS-007 | Design basis values shall be consistent with DEL-11.02 and DEL-11.03 | Consistency check |

### Marine Loading Arm Data Sheet Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| MLA-DS-001 | Include identification fields: tag, service, location, P&ID reference | Completeness check |
| MLA-DS-002 | Include design conditions: design pressure, temperature, product | Consistency with DEL-11.02 |
| MLA-DS-003 | Include mechanical data: arm type, reach (outboard/inboard), slew/luff range | Consistency with DEL-11.03 |
| MLA-DS-004 | Include ERC data: type, release force, spillage limit, reset method | Consistency with DEL-11.02 §4.6 |
| MLA-DS-005 | Include materials: wetted parts, seals/gaskets, external coating | Consistency with DEL-11.02 §4.4 |
| MLA-DS-006 | Include connection data: vessel connection (size, rating, type), shore connection | Consistency with DEL-11.02 §4.3 |
| MLA-DS-007 | Include controls data: local/remote controls, position feedback, permissives | Interface check (PKG-19/20) |
| MLA-DS-008 | Include electrical/I&C data: motor power, signal interfaces, ESD integration | Interface check (PKG-20/29) |
| MLA-DS-009 | Include hazardous area data: zone classification, certification requirements | Consistency with PKG-27 |
| MLA-DS-010 | Include vendor data: OEM, model, compliance statements | Vendor data review |

### Leak Detection System Data Sheet Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| LDS-DS-001 | Include identification fields: tag, service, location | Completeness check |
| LDS-DS-002 | Include detection philosophy: annulus monitoring, drip tray, sump level | Consistency with DEL-11.02 §6 |
| LDS-DS-003 | Include sensor data: technology, zones, coverage | Consistency with DEL-11.02 §6.1-6.2 |
| LDS-DS-004 | Include alarm outputs: alarm setpoint, trip setpoint, signal type | Consistency with DEL-11.02 §6.3 |
| LDS-DS-005 | Include I&C interface data: signal list, ESD integration, PLC I/O | Interface check (PKG-19/29) |
| LDS-DS-006 | Include power data: voltage, power consumption | Interface check (PKG-20) |
| LDS-DS-007 | Include hazardous area data: zone classification, certification | Consistency with PKG-27 |
| LDS-DS-008 | Include testing data: functional test provisions, test interval | Consistency with DEL-11.02 §6.4 |
| LDS-DS-009 | Include vendor data: manufacturer, model, compliance | Vendor data review |

### Sump Pump Data Sheet Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| SP-DS-001 | Include identification fields: tag, service, location | Completeness check |
| SP-DS-002 | Include design duty: flow, head, fluid properties | Consistency with DEL-11.03 |
| SP-DS-003 | Include operating range: minimum/maximum flow, head curve | Consistency with DEL-11.03 |
| SP-DS-004 | Include construction data: pump type, materials (wetted/casing) | Consistency with DEL-11.02 |
| SP-DS-005 | Include motor data: power, voltage, enclosure, hazardous area rating | Interface check (PKG-20/27) |
| SP-DS-006 | Include connection data: suction size/rating, discharge size/rating | Consistency with DEL-11.01 |
| SP-DS-007 | Include controls data: level control, run/stop, alarms | Interface check (PKG-19) |
| SP-DS-008 | Include testing data: factory test, site test requirements | Consistency with DEL-11.02 |
| SP-DS-009 | Include vendor data: manufacturer, model, compliance | Vendor data review |

### Interface Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| INT-001 | Datasheets shall identify electrical power requirements | Interface check (PKG-20) |
| INT-002 | Datasheets shall identify I&C signal interfaces | Interface check (PKG-19) |
| INT-003 | Datasheets shall identify ESD integration requirements | Interface check (PKG-29) |
| INT-004 | Datasheets shall identify hazardous area requirements | Consistency with PKG-27 |

**Note:** Dependency tracking is NOT_TRACKED; interfaces are coordinated externally per `_DEPENDENCIES.md`.

### Quality Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| QA-001 | Datasheets shall be checked and approved per project QA/QC procedures | Check records |
| QA-002 | Units shall be SI (or project-specified units) | Units check |
| QA-003 | Tag numbering shall match project conventions and DEL-11.01 | Cross-reference check |
| QA-004 | Nomenclature shall match project standards | Terminology check |

## Standards

| Standard | Applicability | Status |
|----------|---------------|--------|
| Employer's Requirements (ER) | Baseline requirements | Clause references **TBD** |
| Project datasheet templates | Format and content | **TBD** |
| Project tag numbering convention | Equipment identification | **TBD** |
| IEC 60079 series | Hazardous area equipment certification | **TBD** |
| API 610/682 | Pump specifications (if applicable) | **TBD** |

## Verification

**Verification methods for Data Sheet deliverables:**

| Method | Description | Applies To |
|--------|-------------|------------|
| Completeness check | All required fields populated or marked TBD | All datasheets |
| Consistency check | Values consistent with DEL-11.02/11.03 | Design basis fields |
| Cross-reference check | Tags consistent with DEL-11.01 | All datasheets |
| Vendor data review | Vendor data referenced with revision | Vendor-supplied fields |
| Interface check | Interface requirements coordinated with adjacent packages | Electrical, I&C, ESD |
| Units/terminology check | Units and nomenclature per project standards | All datasheets |

**Acceptance criteria:**
- Datasheet register present with tags and revisions
- Each datasheet complete with required fields or explicitly marked TBD
- Design basis values consistent with DEL-11.02 and DEL-11.03
- Vendor data referenced with revision and date
- Tags consistent with DEL-11.01 drawings

## Documentation

**Required documentation outputs:**
- Marine loading arm data sheet
- Leak detection system data sheet
- Sump pump data sheet
- Datasheet register/index

**Documentation requirements:**
- All documents shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Format: **TBD** (project document management requirements)

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified all 43 requirements have unique IDs: DS-001 to DS-007 (7), MLA-DS-001 to MLA-DS-010 (10), LDS-DS-001 to LDS-DS-009 (9), SP-DS-001 to SP-DS-009 (9), INT-001 to INT-004 (4), QA-001 to QA-004 (4)
- Verified all requirements include verification method column
- Verified 3 datasheets (loading arm, leak detection, sump pump) align with Datasheet §Construction and Procedure §Steps 3-5
- Verified MLA-DS requirements (10) trace to DEL-11.02 §3, §4.3-4.6 and DEL-11.06 OEM data
- Verified LDS-DS requirements (9) trace to DEL-11.02 §6 and PKG-19/29 interfaces
- Verified SP-DS requirements (9) trace to DEL-11.03 drainage calc and PKG-19/20 interfaces
- Verified Related Deliverables table (5 deliverables) consistent with Datasheet §Cross-Document Links
- Verified Standards table (5 standards) and Verification methods (6 methods)
- Verified acceptance criteria (5 items) align with Datasheet §Deliverable Acceptance (6 criteria)
- Confirmed terminology consistent with DEL-11.01/11.02: tag numbers, equipment tags, datasheet nomenclature
- All TBDs and ASSUMPTIONs retained with proper labeling
- Pass 3 complete — document ready for WORKING_ITEMS session
