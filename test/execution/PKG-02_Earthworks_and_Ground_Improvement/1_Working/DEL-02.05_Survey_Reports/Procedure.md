# Procedure: DEL-02.05 Survey Reports

## Purpose

Produce Survey Reports (Topographic Survey Report and Utility Locate Report) for PKG-02 Earthworks & Ground Improvement while satisfying Specification requirements R1-R10 and supporting Guidance principles.

**Dual-Use Note:** This procedure describes how to **produce** the survey reports deliverable. Construction staking and as-built survey procedures are addressed separately.

Source: _CONTEXT.md; decomposition DEL-02.05 entry (location TBD).

## Prerequisites

### Dependencies
**Coordination status:** Dependencies coordinated externally by humans (see _DEPENDENCIES.md).

**Key coordination interfaces:**

| Interface | Relevance | Specification § |
|-----------|-----------|-----------------|
| Site access | Access permissions, safety approvals | — |
| Utility owners | Records, verification, coordination | R3, R4 |
| Coordinate system | ER-specified system for project | R9 |
| DEL-02.01 | Design limits for survey coverage | R5 |
| DEL-02.04 | Borehole locations for investigation | R5 |

### Reference Materials Required

| Reference | Status | Specification § |
|-----------|--------|-----------------|
| Employer's Requirements volumes | **TBD** — not yet provided | R7, R9, R10, V3 |
| Existing survey control monuments | **TBD** | R2 |
| Design limits from packages | **TBD** | R5 |

### Inputs
- PKG-02 scope and design limits for earthworks areas.
- Design limits from other packages requiring existing conditions survey.
- Existing survey control monuments (if available).

### Qualifications
- Licensed professional land surveyor to perform surveys and certify reports (R8).
- **TBD**: ER will specify licensing jurisdiction.

### Equipment
- Calibrated survey equipment (total station, GPS/GNSS, level, data collector) appropriate for specified accuracy (R7).

## Steps

### Phase 1: Survey Planning and Control Establishment

| Step | Action | Specification § | Guidance § | Status |
|------|--------|-----------------|------------|--------|
| 1 | Review ER survey requirements (scope, accuracy, coordinate system, formats); coordinate with DEL-02.01, DEL-02.04 to understand survey area limits | R1, R3, R5, R7, R9, R10 | All principles | **TBD** until ER provided |
| 2 | Establish or verify project coordinate system, datum, and projection per ER; document in Datasheet; coordinate with all design disciplines | R9 | Coordination | — |
| 3 | Establish survey control network (horizontal/vertical control, benchmarks) or verify existing monuments; perform control survey ties | R2 | Accuracy, Control Network | — |
| 4 | Obtain site access permissions; coordinate survey timing with site availability and vegetation conditions | — | Survey Timing | **ASSUMPTION**: Contractor procedures |

### Phase 2: Topographic Survey Execution

| Step | Action | Specification § | Guidance § | Datasheet § |
|------|--------|-----------------|------------|-------------|
| 5 | Perform field topographic survey of existing conditions (topography, structures, pavements, drainage, vegetation, boundaries); extend beyond design limits | R1, R2, R5 | Completeness | Site topography, Existing features |
| 6 | Collect survey data to accuracy specified in ER; document accuracy methodology | R7 | Accuracy | Survey accuracy attribute |
| 7 | Process survey data; create digital survey deliverables in formats specified by ER (CAD, GIS, etc.) | R2, R10 | Data Quality | Survey format, Digital data |
| 8 | Prepare topographic survey plan sheets showing existing conditions | R2 | Completeness | Survey plan sheets |

### Phase 3: Utility Investigation Execution

| Step | Action | Specification § | Guidance § | Datasheet § |
|------|--------|-----------------|------------|-------------|
| 9 | Perform utility records search with utility owners, municipalities, private entities; compile utility records | R3, R4 | Utility Ownership | Investigation methodology |
| 10 | Perform field utility locating (electromagnetic, GPR, one-call, test holes in critical areas); mark and survey utility locations | R3, R4 | Quality Levels | Existing utilities |
| 11 | Assess utility conflicts with proposed design from DEL-02.01; document in utility conflict register | R3, R4 | Completeness | Conflict assessment |
| 12 | Prepare utility location plan sheets showing utilities with type, location, depth, owner | R4 | Completeness | Utility location plans |

### Phase 4: Report Preparation and Quality Control

| Step | Action | Specification § | Guidance § | Records |
|------|--------|-----------------|------------|---------|
| 13 | Prepare Topographic Survey Report per Datasheet structure: methodology, control, coordinate system, data, accuracy statement, certification | R1, R2, R6, R7, R8 | Completeness, Accuracy | Topographic Report |
| 14 | Prepare Utility Locate Report per Datasheet structure: methodology, utilities, conflicts, limitations, plans | R3, R4, R6 | Completeness | Utility Report |
| 15 | Include document control elements (title, number, revision, date, author) | R6 | Data Quality | — |
| 16 | Perform survey data QC: verify control closure, check calculations, verify accuracy, test digital data import | R7, R10 | Accuracy, Data Quality | QC records |

### Phase 5: Review and Approval

| Step | Action | Specification § | Verification | Records |
|------|--------|-----------------|--------------|---------|
| 17 | Perform internal technical review against V1-V3; update Datasheet for TBDs/limitations | R1-R10 | V1, V2, V3 | Review checklist |
| 18 | Address review comments; revise reports and data as necessary; update revision | R6 | — | Comment log |
| 19 | Obtain professional land surveyor seal/certification per regulatory requirements | R8 | V3 | Seal documentation |
| 20 | Issue controlled reports and digital data per document control procedures; distribute to design team | R6 | — | Transmittal, distribution |

## Verification

### V1: Content Completeness

| Attribute | Value |
|-----------|-------|
| Check | Verify reports include all required content sections per Datasheet and R1-R10 |
| Method | Technical review checklist; accuracy verification calculations |
| Criteria | All sections present; accuracy meets requirements; professional seal present |
| Reference | Specification V1; Datasheet Report Content |
| Procedure Step | Step 17 |

### V2: Scope Coverage and Data Compatibility

| Attribute | Value |
|-----------|-------|
| Check | Verify surveys cover PKG-02 areas, digital formats import correctly, coordinate system consistent, utility conflicts identified |
| Method | Cross-reference with design limits; test data import; coordinate verification; conflict matrix |
| Criteria | All areas covered; data imports without errors; consistent coordinates; conflicts documented |
| Reference | Specification V2; Guidance Coordination, Data Quality |
| Procedure Step | Steps 11, 16, 17 |

### V3: ER Compliance

| Attribute | Value |
|-----------|-------|
| Check | Verify alignment with ER survey requirements |
| Method | ER compliance matrix; accuracy comparison |
| Criteria | **TBD** — pending ER volumes |
| Reference | Specification V3 |
| Status | Deferred pending ER volumes |
| Procedure Step | Steps 1, 19 |

## Records

### Primary Deliverable Records

| Record | Description | Specification § |
|--------|-------------|-----------------|
| Issued Topographic Survey Report | Controlled revision with professional seal | R1, R2, R6, R8 |
| Issued Utility Locate Report | Controlled revision | R3, R4, R6 |
| Digital survey data files | CAD, GIS, point cloud as specified | R10 |

### Production Records

| Record | Description | Procedure Step |
|--------|-------------|----------------|
| Survey control network documentation | Control points, benchmarks, ties | Step 3 |
| Field survey notes | Observations, conditions, methodology | Steps 5, 6, 10 |
| QC verification records | Accuracy calculations, data import tests | Step 16 |
| Technical review checklist | Record of verification against V1-V3 | Step 17 |
| Review comments and responses | Log of comments and resolutions | Step 18 |

### Approval and Distribution Records

| Record | Description | Procedure Step |
|--------|-------------|----------------|
| Professional seal documentation | Surveyor seal/certification | Step 19 |
| Transmittal records | Distribution list, issuance date | Step 20 |
| Utility conflict register | Conflicts with resolution tracking | Step 11 |

**Assumption:** Records management per standard D&B document control and QA/QC procedures.

## Cross-Document Traceability

| Procedure Phase | Specification § | Guidance § | Datasheet § | Verification |
|-----------------|-----------------|------------|-------------|--------------|
| Phase 1 (Planning) | R2, R5, R7, R9, R10 | Coordination, Accuracy | Control network, Coordinate system | — |
| Phase 2 (Topographic) | R1, R2, R5, R7, R10 | Accuracy, Completeness, Data Quality | Topographic sections | — |
| Phase 3 (Utility) | R3, R4 | Completeness | Utility sections | — |
| Phase 4 (QC/Report) | R1-R8, R10 | All principles | All sections | — |
| Phase 5 (Review/Approval) | R6, R8 | All principles | Attributes | V1, V2, V3 |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| _DEPENDENCIES.md | Dependency coordination mode (NOT_TRACKED) | This folder |
| Decomposition | PKG-02 scope, DEL-02.05 entry, Section 1.2 Scope Focus | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Datasheet.md | Report content and attributes | This folder |
| Specification.md | Requirements R1-R10, Verification V1-V3 | This folder |
| Guidance.md | Principles, Considerations, Trade-offs | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
| Related deliverables | DEL-02.01, DEL-02.04 | PKG-02 |
