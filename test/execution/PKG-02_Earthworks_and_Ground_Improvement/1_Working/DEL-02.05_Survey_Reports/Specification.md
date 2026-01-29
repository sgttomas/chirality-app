# Specification: DEL-02.05 Survey Reports

## Scope

This deliverable defines the requirements for Survey Reports within PKG-02 Earthworks & Ground Improvement. Source: _CONTEXT.md; decomposition DEL-02.05 entry (location TBD).

**Included:**
- Topographic survey report documenting existing site conditions
- Utility locate report documenting existing utilities and conflicts
- Digital survey data in design-compatible formats
- Professional certification and accuracy statements

**Package Context:**
Package scope includes Site grading, excavation, filling, ground improvements, geotechnical works, surveys. Source: decomposition PKG-02 scope (location TBD).

**Excluded:**
This decomposition covers the Contractor's scope of work only. Employer-responsible items excluded except for interface connections. Source: decomposition Section 1.2 Scope Focus (location TBD).

## Requirements

### R1: Topographic Survey Report
**Requirement:** Document existing site conditions (topography, structures, features, vegetation, boundaries) for design verification and approvals.

| Attribute | Value |
|-----------|-------|
| Source | Decomposition DEL-02.05 entry and _CONTEXT.md (location TBD) |
| Datasheet mapping | Report Content — Topographic Survey sections |
| Guidance § | Accuracy, Completeness |
| Procedure Step | Steps 5-8, 13 |
| Verification | V1, V3 |

### R2: Topographic Survey Content
**Requirement:** Include survey methodology, control network, coordinate system/datum, site topography, existing features, accuracy statement, certification, and digital survey data in formats compatible with design software.

| Attribute | Value |
|-----------|-------|
| Source | _CONTEXT.md; **ASSUMPTION**: Standard survey deliverables |
| Datasheet mapping | All Topographic Survey Report sections |
| Guidance § | Data Quality, Accuracy |
| Procedure Step | Steps 5-8, 13, 16 |
| Verification | V1, V2 |

### R3: Utility Locate Report
**Requirement:** Document existing utilities (type, location, depth, owner) and identify potential conflicts with proposed design.

| Attribute | Value |
|-----------|-------|
| Source | _CONTEXT.md |
| Datasheet mapping | Report Content — Utility Locate sections |
| Guidance § | Completeness |
| Procedure Step | Steps 9-12, 14 |
| Verification | V1, V3 |

### R4: Utility Locate Content
**Requirement:** Include investigation methodology (records search, field locating), utility markings/coordinates, conflict assessment, limitations/disclaimers, and utility location plan sheets.

| Attribute | Value |
|-----------|-------|
| Source | **ASSUMPTION**: Standard utility investigation deliverables |
| Datasheet mapping | All Utility Locate Report sections |
| Guidance § | Utility Investigation |
| Procedure Step | Steps 9-12, 14 |
| Verification | V1, V2 |

### R5: PKG-02 Scope Coverage
**Requirement:** Address site boundaries and existing conditions relevant to PKG-02 earthworks scope (grading, excavation, fill, ground improvement areas).

| Attribute | Value |
|-----------|-------|
| Source | Decomposition PKG-02 scope (location TBD) |
| Datasheet mapping | Context & Conditions |
| Guidance § | Completeness |
| Procedure Step | Steps 1, 5 |
| Verification | V2 |

### R6: Document Control
**Requirement:** Include document control fields (title, report number, revision, date, author/organization, approvals) per D&B Contractor standards.

| Attribute | Value |
|-----------|-------|
| Source | **ASSUMPTION**: Standard D&B document control |
| Datasheet mapping | Attributes (report date, number, revision) |
| Guidance § | Data Quality |
| Procedure Step | Steps 15, 18, 20 |
| Verification | V1 |

### R7: Survey Accuracy
**Requirement:** Surveys shall be performed to accuracy standards specified in ER; horizontal and vertical accuracy shall be stated and certified.

| Attribute | Value |
|-----------|-------|
| Source | **TBD**: ER will specify accuracy; **ASSUMPTION**: Typical engineering survey accuracy |
| Datasheet mapping | Survey accuracy attribute, Accuracy statement section |
| Guidance § | Accuracy |
| Procedure Step | Steps 6, 16 |
| Verification | V1, V3 |

### R8: Professional Qualifications
**Requirement:** Surveys shall be performed by licensed professional land surveyor; reports shall include professional seal/certification.

| Attribute | Value |
|-----------|-------|
| Source | **ASSUMPTION**: Professional surveying standards; **TBD**: ER licensing requirements |
| Datasheet mapping | Author/organization attribute |
| Guidance § | Regulatory Compliance |
| Procedure Step | Step 19 |
| Verification | V1, V3 |

### R9: Coordinate System Consistency
**Requirement:** Survey coordinate system, datum, and projection shall be consistent with ER project requirements and compatible with design software.

| Attribute | Value |
|-----------|-------|
| Source | **TBD**: ER will specify coordinate system |
| Datasheet mapping | Coordinate system attribute |
| Guidance § | Coordination |
| Procedure Step | Step 2 |
| Verification | V2, V3 |

### R10: Digital Data Formats
**Requirement:** Digital survey data shall be provided in formats specified by ER (e.g., AutoCAD DWG, Civil 3D surface, GIS shapefile, LandXML, point cloud).

| Attribute | Value |
|-----------|-------|
| Source | **TBD**: ER will specify formats |
| Datasheet mapping | Survey format attribute, Digital survey data section |
| Guidance § | Data Quality |
| Procedure Step | Step 7 |
| Verification | V2 |

## Standards

**Applicable Standards:**

| Standard Type | Examples | Status |
|---------------|----------|--------|
| Land title survey | ALTA/NSPS standards | **TBD** |
| Aerial survey accuracy | ASPRS accuracy standards | **TBD** |
| Utility investigation | ASCE 38 (CI/ASCE 38-02) quality levels | **TBD** |
| Coordinate systems | State Plane, UTM, local project system | **TBD** |
| Professional practice | State/provincial licensing board requirements | **ASSUMPTION** |

**Note:** Employer's Requirements volumes are referenced in decomposition but not provided. Standards identification is **TBD** until ER volumes are available.

## Verification

### V1: Content Completeness
**Method:** Verify survey reports include all required content sections per Datasheet and R1-R10.

| Attribute | Value |
|-----------|-------|
| Responsible | Qualified surveyor |
| Criteria | All sections present; accuracy statement compliant; professional seal present |
| Records | Review checklist, accuracy verification calculations, seal documentation |
| Guidance § | Accuracy, Data Quality |
| Procedure Step | Step 17 |

### V2: Scope Coverage and Data Compatibility
**Method:** Verify surveys cover PKG-02 areas, digital formats import correctly, coordinate system is consistent.

| Attribute | Value |
|-----------|-------|
| Responsible | Design lead and surveyor |
| Criteria | All areas covered; data imports without errors; coordinate system consistent; utility conflicts identified |
| Records | Design software import log, coordinate verification, utility conflict register |
| Guidance § | Coordination, Data Quality |
| Procedure Step | Steps 11, 16, 17 |

### V3: ER Compliance
**Method:** Verify alignment with ER survey requirements once available.

| Attribute | Value |
|-----------|-------|
| Responsible | Design lead and quality reviewer |
| Criteria | **TBD** — scope, accuracy, coordinate system per ER |
| Status | Requirements not yet available; verification deferred |
| Procedure Step | Steps 1, 19 |

## Documentation

**Primary Deliverables:**
- Controlled Topographic Survey Report (issued revision per R6).
- Controlled Utility Locate Report (issued revision per R6).
- Digital survey data files in specified formats (R10).

**Supporting Documentation:**
- Review comments and response log.
- Utility conflict register.
- Coordination transmittals.

**Assumptions:** Standard D&B document control workflow applies unless ER specifies otherwise.

## Cross-Document Traceability

| Requirement | Datasheet § | Guidance § | Procedure Step | Verification |
|-------------|-------------|------------|----------------|--------------|
| R1 | Topographic Report sections | Accuracy, Completeness | Steps 5-8, 13 | V1, V3 |
| R2 | Topographic Report sections | Data Quality, Accuracy | Steps 5-8, 13, 16 | V1, V2 |
| R3 | Utility Report sections | Completeness | Steps 9-12, 14 | V1, V3 |
| R4 | Utility Report sections | Utility Investigation | Steps 9-12, 14 | V1, V2 |
| R5 | Context & Conditions | Completeness | Steps 1, 5 | V2 |
| R6 | Attributes | Data Quality | Steps 15, 18, 20 | V1 |
| R7 | Survey accuracy, Accuracy statement | Accuracy | Steps 6, 16 | V1, V3 |
| R8 | Author/organization | Regulatory Compliance | Step 19 | V1, V3 |
| R9 | Coordinate system | Coordination | Step 2 | V2, V3 |
| R10 | Survey format, Digital data | Data Quality | Step 7 | V2 |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| Decomposition | PKG-02 scope, DEL-02.05 entry, Section 1.2 Scope Focus | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Datasheet.md | Report content and attributes mapped to R1-R10 | This folder |
| Guidance.md | Principles, Considerations, Trade-offs | This folder |
| Procedure.md | Steps 1-20 implementing requirements and V1-V3 | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
