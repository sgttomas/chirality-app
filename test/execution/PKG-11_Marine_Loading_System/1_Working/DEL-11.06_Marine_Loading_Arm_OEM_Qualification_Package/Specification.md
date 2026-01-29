# Specification: DEL-11.06 Marine Loading Arm OEM Qualification Package

## Scope

This specification defines the requirements for **Marine Loading Arm OEM Qualification Package** within **PKG-11 Marine Loading System**.

**Purpose:** Defines and substantiates marine loading arm OEM qualification in accordance with Employer's Requirements (ER), demonstrating OEM capability, product compliance, and suitability for the project prior to procurement commitment.

**Package scope (PKG-11):**
- Powered loading arm (articulated boom with powered slew/luff)
- Emergency release coupling (ERC)
- Associated controls and instrumentation

**Anticipated deliverable artifacts:**
- OEM qualification submission
- Comparable project references
- Compliance statements
- Supporting documentation

**Objectives served (per decomposition Section 6):**
- OBJ-1 Safe & Reliable Operation
- OBJ-2 Throughput Capacity (1,000,000 MT/annum)
- OBJ-4 Operational Flexibility
- OBJ-7 Environmental Protection

## Related Deliverables (PKG-11)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-11.01 Marine Loading Design Drawing Set | Receives OEM envelope data for layout |
| DEL-11.02 Marine Loading Technical Specification | Defines requirements for OEM compliance |
| DEL-11.03 Marine Loading Design Calculations | Uses OEM envelope data for verification |
| DEL-11.04 Marine Loading Data Sheet Package | Receives OEM-offered values |
| DEL-11.05 Marine Loading Installation & Test Records | FAT based on OEM procedures |

## Requirements

### General Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| OEM-001 | Provide a controlled OEM qualification submission package | Document review |
| OEM-002 | Package shall include contents index with document list and revisions | Document review |
| OEM-003 | All included documents shall be revision controlled and dated | Document review |
| OEM-004 | Package shall demonstrate OEM capability and product compliance | Technical review |
| OEM-005 | Package shall comply with project QA/QC procedures | QA review |

### OEM Qualification Submission Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| QUAL-001 | Provide company profile (history, ownership, organizational structure) | Completeness check |
| QUAL-002 | Provide manufacturing capability information (facilities, capacity, staff) | Completeness check |
| QUAL-003 | Provide quality management system evidence (ISO 9001 or equivalent) | Certificate review |
| QUAL-004 | Provide design capability information (engineering resources, tools) | Completeness check |
| QUAL-005 | Provide after-sales support information (spare parts, service, warranty) | Completeness check |
| QUAL-006 | Identify proposed product line/model for this application | Technical review |

### Comparable Project References Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| REF-001 | Provide minimum 3 comparable project references | Reference count |
| REF-002 | References shall include project name, location, client, dates | Completeness check |
| REF-003 | References shall include scope (arm type, size, ERC, product) | Relevance review |
| REF-004 | References shall include operational history where available | Reference review |
| REF-005 | References shall be relevant to marine loading arm application | Relevance review |
| REF-006 | Client contact information provided where authorized | Completeness check |

### Compliance Statement Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| COMP-001 | Provide ER compliance matrix (clause-by-clause if clauses available) | Compliance review |
| COMP-002 | Provide code/standards compliance statements (OCIMF, ASME, API, IEC) | Compliance review |
| COMP-003 | Provide deviation register listing all exceptions to requirements | Deviation review |
| COMP-004 | Each deviation shall include proposed disposition path | Deviation review |
| COMP-005 | Provide hazardous area certification evidence | Certificate review |
| COMP-006 | Provide type testing evidence where applicable | Technical review |

### Supporting Documentation Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| DOC-001 | Provide product brochure/catalog for proposed product line | Document review |
| DOC-002 | Provide GA drawings showing envelope and connection details | Technical review |
| DOC-003 | Provide standard product datasheets | Technical review |
| DOC-004 | Provide quality certificates (ISO, third-party) | Certificate review |
| DOC-005 | Provide FAT procedures (or outline) | Technical review |
| DOC-006 | Provide material certificates / welding qualifications as applicable | Technical review |

### Interface Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| INT-001 | OEM envelope data sufficient for DEL-11.01 layout drawings | Technical review |
| INT-002 | OEM connection details sufficient for piping coordination | Technical review |
| INT-003 | OEM control philosophy compatible with project I&C requirements | Interface review |
| INT-004 | OEM ERC performance data sufficient for DEL-11.02 requirements | Technical review |

**Note:** Dependency tracking is NOT_TRACKED; interfaces are coordinated externally per `_DEPENDENCIES.md`.

### Quality Requirements

| Req ID | Requirement | Verification |
|--------|-------------|--------------|
| QA-001 | Package shall be reviewed and approved per project QA/QC procedures | QA records |
| QA-002 | All included vendor documents clearly revision controlled and dated | Document review |
| QA-003 | Deviations shall be logged in project deviation register | Deviation tracking |
| QA-004 | Approval path for deviations shall be documented | Approval records |

## Standards

| Standard | Applicability | Status |
|----------|---------------|--------|
| Employer's Requirements (ER) | OEM qualification criteria | Clause references **TBD** |
| OCIMF Guidelines | Marine loading arm design | **TBD** |
| ISO 9001 | OEM quality management system | Required |
| IEC 60079 series | Hazardous area certification | **TBD** |
| API / ASME standards | Equipment design codes | **TBD** |

## Verification

**Verification methods for Document Package deliverables:**

| Method | Description | Applies To |
|--------|-------------|------------|
| Document review | Package completeness and revision control | OEM-001 to OEM-005 |
| Completeness check | All required sections present | QUAL, REF, DOC requirements |
| Technical review | OEM capability and product suitability | QUAL-006, DOC-002, INT requirements |
| Compliance review | ER and code compliance demonstrated | COMP-001 to COMP-006 |
| Reference review | Comparable references relevant and adequate | REF-001 to REF-006 |
| Deviation review | Exceptions documented with disposition | COMP-003, COMP-004 |
| Certificate review | Valid certifications provided | QUAL-003, COMP-005, DOC-004 |

**Acceptance criteria:**
- Package complete with all required sections
- Compliance statements with ER traceability (or TBD where clauses not available)
- Minimum 3 comparable project references provided
- Deviations explicitly documented with proposed disposition
- OEM capability demonstrated through certifications and references

## Documentation

**Required documentation outputs:**
- OEM qualification submission
- Comparable project references list
- Compliance statements and matrix
- Deviation register
- Supporting documentation package

**Documentation requirements:**
- All documents shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Format: **TBD** (project document management requirements)

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified all 37 requirements have unique IDs: OEM-001 to OEM-005 (5), QUAL-001 to QUAL-006 (6), REF-001 to REF-006 (6), COMP-001 to COMP-006 (6), DOC-001 to DOC-006 (6), INT-001 to INT-004 (4), QA-001 to QA-004 (4)
- Verified all requirements include verification method column
- Verified 4 document categories align with Datasheet §Construction and Procedure §Steps 2-6
- Verified QUAL requirements (6) trace to Datasheet §OEM Qualification Submission fields
- Verified REF requirements (6) trace to Datasheet §Comparable Project References fields
- Verified COMP requirements (6) trace to Datasheet §Compliance Statements documents
- Verified DOC requirements (6) trace to Datasheet §Supporting Documentation items
- Verified INT requirements (4) cover data flow to DEL-11.01, DEL-11.02, DEL-11.04, piping coordination
- Verified Related Deliverables table (5 deliverables) consistent with Datasheet §Cross-Document Links
- Verified Standards table (5 standards) and Verification methods (7 methods)
- Verified acceptance criteria (5 items) align with Datasheet §Deliverable Acceptance (6 criteria)
- Confirmed terminology consistent with DEL-11.02/11.04: envelope data, ERC performance, connection details
- All TBDs and ASSUMPTIONs retained with proper labeling
- Pass 3 complete — document ready for WORKING_ITEMS session
