# Procedure: DEL-02.03 Earthworks Design Calculations

## Purpose

Define the calculation workflow for Earthworks Design Calculations to ensure the deliverable satisfies Specification requirements R1-R6, implements Guidance principles P1-P4, and supports PKG-02 Earthworks & Ground Improvement objectives.

**Dual-Use Note:** This procedure describes how to **produce** the design calculations deliverable. It does not describe field execution procedures (see DEL-02.07 for field procedures).

Source: _CONTEXT.md; decomposition DEL-02.03 entry (location TBD).

## Prerequisites

### Dependencies
**Coordination status:** Dependencies coordinated externally by humans (see _DEPENDENCIES.md).

**Key coordination interfaces:**

| Interface | Deliverable | Relevance | Specification § |
|-----------|-------------|-----------|-----------------|
| Geotechnical data | DEL-02.04 (Geotechnical Reports) | Soil parameters, bearing capacity recommendations | R3 |
| Survey data | DEL-02.05 (Survey Reports) | Topographic data for cut/fill calculations | R2 |
| Design drawings | DEL-02.01 (Design Drawing Set) | Uses calculation results; calculations must support design | R1, R2, R3 |
| Technical specification | DEL-02.02 (Technical Specification) | Uses calculation results for performance criteria | R1, R2, R3 |

**Note:** Maturity of upstream deliverables to be managed per project schedule and coordination plan.

### Reference Materials Required

**Primary References:**

| Reference | Status | Specification § |
|-----------|--------|-----------------|
| Employer's Requirements volumes (Vol 2 Parts 1-3) | **TBD** — not yet provided | R1, V3 |
| Project calculation template and format standards | **TBD** — per ER or Contractor standards | R5 |
| Project document numbering system | **TBD** | R6 |

**Design Inputs:**

| Input | Source | Specification § |
|-------|--------|-----------------|
| Geotechnical investigation and design | DEL-02.04 | R3 |
| Topographic survey | DEL-02.05 | R2 |
| Proposed finish grades | DEL-02.01 | R2 |
| Loading conditions | PKG-04, PKG-05, PKG-06 | R3 |
| Design criteria | ER | R1 |

**Technical Standards and Codes:**

| Standard Type | Examples | Status |
|---------------|----------|--------|
| Geotechnical design codes | Canadian Foundation Engineering Manual, CSA standards | **TBD** |
| Bearing capacity methods | Terzaghi, Meyerhof, code-specified | **TBD** |
| Civil design standards | Grading, earthwork measurement | **TBD** |

### Tools and Resources
- Calculation tools: Spreadsheets, Civil 3D (cut/fill), geotechnical analysis software.
- Access to referenced codes and standards.
- Project calculation template (if applicable).
- Document management system for revision control (R6).
- **ASSUMPTION**: Standard D&B engineering calculation tools and infrastructure.

## Steps

### Step 1: Compile and Validate Inputs
**Objective:** Gather all required reference materials and design inputs; confirm completeness and quality.

| Attribute | Value |
|-----------|-------|
| Specification § | R1, R2, R3 |
| Guidance § | P3, P4, Considerations (Input Data Quality) |
| Datasheet § | Design inputs attribute, Calculation Content inputs |

**Actions:**

| Step | Action | Verification | Status |
|------|--------|--------------|--------|
| 1.1 | Obtain and review ER volumes; extract earthworks design criteria | Confirm ER requirements applicable | **TBD** — ER volumes not yet provided |
| 1.2 | Obtain geotechnical reports (DEL-02.04); extract soil parameters, bearing capacity, ground improvement recommendations | Geotechnical data complete for bearing capacity calculations | Pending DEL-02.04 |
| 1.3 | Obtain survey reports (DEL-02.05); extract topographic data, datum, coordinate system | Survey data complete for cut/fill calculations | Pending DEL-02.05 |
| 1.4 | Obtain design drawings (DEL-02.01) or preliminary design; extract proposed finish grades, grading extents | Design data available for calculations | Pending DEL-02.01 |
| 1.5 | Identify loading conditions and design criteria | Loads and criteria identified | **TBD** |

**Outputs:**
- Validated input data package.
- Input data gaps documented as **TBD** or flagged for resolution.

### Step 2: Confirm Scope and Calculation Requirements
**Objective:** Define calculation scope, required calculation packages, and documentation requirements per Specification R1-R6.

| Attribute | Value |
|-----------|-------|
| Specification § | R4, R5, R6 |
| Guidance § | P4 (Coordination) |
| Datasheet § | Calculation format, Calculation package ID |
| Verification | V2 |

**Actions:**

| Step | Action | Reference | Output |
|------|--------|-----------|--------|
| 2.1 | Review PKG-02 scope and confirm calculation coverage | Decomposition PKG-02 scope, R4 | Scope coverage confirmation |
| 2.2 | Confirm required calculation packages | R2, R3 | Calculation package list |
| 2.3 | Establish calculation format and documentation requirements | R5 | Calculation format plan |
| 2.4 | Establish document control requirements | R6 | Document control plan |

**Outputs:**
- Scope definition and calculation package list.
- Calculation format and documentation plan.
- Document control plan (numbering, revision, checking, approvals).

### Step 3: Develop Calculations
**Objective:** Perform calculations per Specification R2-R3 and Guidance principles P1-P4.

| Attribute | Value |
|-----------|-------|
| Specification § | R2, R3, R5 |
| Guidance § | P1, P2, P3, P4, Trade-offs |
| Datasheet § | Calculation Content sections 1-2 |
| Verification | V1 |

**Actions:**

| Step | Calculation Type | Key Content | Guidance § |
|------|------------------|-------------|------------|
| 3.1 | Cut/Fill Quantity Calculations (R2) | Inputs, method, volumes, allowances, documentation | P1, P2, P4 |
| 3.2 | Bearing Capacity Calculations (R3) | Inputs, method, ultimate/allowable capacity, settlement, documentation | P1, P2, P3, P4 |
| 3.3 | General Documentation (R5) | Title page, design basis, assumptions, references, summary | P2 |

**Step 3.1 Detail — Cut/Fill Quantity Calculations (R2):**

| Element | Content | Source |
|---------|---------|--------|
| Inputs | Existing topography, proposed grades, limits | DEL-02.05, DEL-02.01 |
| Method | Cross-section, average end area, or DTM | Standards, P1 |
| Outputs | Total cut, total fill, net balance, breakdown by zone | — |
| Allowances | Compaction shrinkage (+5%), over-excavation (+2%); **ASSUMPTION** | P3 |

**Step 3.2 Detail — Bearing Capacity Calculations (R3):**

| Element | Content | Source |
|---------|---------|--------|
| Inputs | Soil parameters (c, φ, γ), groundwater, loads, depths | DEL-02.04, adjacent packages |
| Method | Terzaghi/Meyerhof or code-specified | Standards, P1 |
| Outputs | Ultimate capacity, factor of safety, allowable capacity, settlement | — |
| Conservatism | Code-required FS (typically 2.5-3.0); **ASSUMPTION** | P3 |

**Outputs:**
- Complete calculation packages for cut/fill (R2) and bearing capacity (R3).
- Calculations formatted per project template.
- All documentation requirements (R5) satisfied.

### Step 4: Perform Internal Verification and Checking
**Objective:** Verify calculation completeness, accuracy, and coordination with Specification R1-R6 and verification V1-V4.

| Attribute | Value |
|-----------|-------|
| Specification § | R1-R6, V1-V4 |
| Guidance § | P1 (Verification), QA/QC Considerations |
| Datasheet § | Check status attribute |

**Actions:**

| Step | Check | Method | Criteria | Specification § |
|------|-------|--------|----------|-----------------|
| 4.1 | Content Completeness (V1) | Verify all calculation packages and documentation present | All R2-R3 calculations with complete documentation | V1 |
| 4.2 | Scope Alignment (V2) | Verify coverage of PKG-02 scope | All scope items have design basis | V2, R4 |
| 4.3 | ER Compliance (V3) | Verify alignment with ER criteria | **TBD** — pending ER volumes | V3 |
| 4.4 | Independent Check (V4a) | Qualified checker verifies inputs, methods, calculations, results | Inputs accurate, assumptions reasonable, calculations verified | V4, R6 |
| 4.5 | Coordination Check (V4b) | Cross-reference with DEL-02.01, DEL-02.02, DEL-02.04, DEL-02.05 | No contradictions; outputs support design | V4, P4 |
| 4.6 | Cross-Document Consistency | Verify terminology and values across all four documents | Consistent terminology and values | QA/QC |

**Outputs:**
- Verification and check records.
- Nonconformances documented and resolved.
- Calculation package ready for issuance or flagged for revision.

### Step 5: Issue Controlled Deliverable
**Objective:** Issue calculation package per document control requirements (R6) and capture approval records.

| Attribute | Value |
|-----------|-------|
| Specification § | R6, Documentation |
| Guidance § | QA/QC Considerations |
| Datasheet § | Calculation package ID, Check status, Revision |

**Actions:**

| Step | Action | Records |
|------|--------|---------|
| 5.1 | Finalize calculation package with check comments addressed; update revision, obtain checker sign-off | Updated calculations |
| 5.2 | Obtain required approvals (preparer, checker, design lead, Employer if applicable) | Approval signatures or electronic records |
| 5.3 | Issue controlled calculation package through document management system | Transmittal, distribution list |
| 5.4 | Capture issuance records and maintain revision history | Revision log |

**Outputs:**
- Issued Earthworks Design Calculations (controlled revision).
- Approval and check records.
- Distribution records and transmittal.

## Verification

### Calculation Completeness

| Attribute | Value |
|-----------|-------|
| Check | All required calculation packages (R2-R3) and documentation (R5-R6) present and complete |
| Method | Compare delivered content against Datasheet and Specification R2-R6 |
| Criteria | All required calculations present with complete documentation; independent check signed |
| Reference | Specification V1; Datasheet Calculation Content sections |
| Procedure Step | Step 4.1 |

### Scope Coverage

| Attribute | Value |
|-----------|-------|
| Check | Calculations address all PKG-02 scope items relevant to earthworks design |
| Method | Review calculation content against PKG-02 scope |
| Criteria | All scope items have corresponding design basis |
| Reference | Specification V2; Guidance P4 |
| Procedure Step | Step 4.2 |

### Calculation Accuracy

| Attribute | Value |
|-----------|-------|
| Check | Calculations are accurate, verifiable, and based on valid inputs and methods |
| Method | Independent check by qualified engineer |
| Criteria | Inputs correct, assumptions reasonable, methods appropriate, calculations accurate |
| Reference | Specification V4; Guidance P1 |
| Procedure Step | Step 4.4 |

### Design and Construction Coordination

| Attribute | Value |
|-----------|-------|
| Check | Calculations consistent with design deliverables and support construction |
| Method | Cross-reference with DEL-02.01, DEL-02.02, DEL-02.04, DEL-02.05 |
| Criteria | No contradictions; calculation outputs used correctly in drawings and specifications |
| Reference | Specification V4; Guidance P4 |
| Procedure Step | Step 4.5 |

### ER Compliance

| Attribute | Value |
|-----------|-------|
| Check | Calculations align with ER design criteria and methods |
| Method | Review against ER requirements when available |
| Criteria | **TBD** — pending ER volumes |
| Reference | Specification V3 |
| Status | Deferred pending ER volumes |
| Procedure Step | Step 4.3 |

## Records

### Primary Deliverable Records

| Record | Description | Specification § |
|--------|-------------|-----------------|
| Issued Earthworks Design Calculations | Controlled revision with calculation package ID, preparer/checker sign-offs | R6 |

### Production Records

| Record | Description | Procedure Step |
|--------|-------------|----------------|
| Input Data Package | Documentation of reference materials used | Step 1 |
| Independent Check Records | Checker sign-off, check comments and resolutions | Step 4.4 |
| Calculation Review Checklist | Record of internal verification against V1-V4 | Step 4 |
| Review Comments and Responses | Log of review comments and resolutions | Step 4 |

### Approval and Distribution Records

| Record | Description | Procedure Step |
|--------|-------------|----------------|
| Approval Records | Preparer, checker, approver signatures | Step 5.2 |
| Transmittal Records | Distribution list, transmittal letter, issuance date | Step 5.3 |
| Revision History | Log of revisions, dates, and reasons | Step 5.4 |

### Coordination Records

| Record | Description | Guidance § |
|--------|-------------|------------|
| Coordination Notes | Documentation of coordination with related deliverables | P4 |
| Conflict Resolutions | Documentation of conflicts identified and resolved | Conflict Table |

**Assumption:** Records management per standard D&B engineering calculation and QA/QC procedures.

## Cross-Document Traceability

| Procedure Step | Specification § | Guidance § | Datasheet § | Verification |
|----------------|-----------------|------------|-------------|--------------|
| Step 1 | R1, R2, R3 | P3, P4, Considerations | Design inputs, Calculation inputs | — |
| Step 2 | R4, R5, R6 | P4 | Calculation format, ID | V2 |
| Step 3 | R2, R3, R5 | P1, P2, P3, P4, Trade-offs | Content sections 1-2 | V1 |
| Step 4 | R1-R6 | P1, QA/QC Considerations | Check status | V1, V2, V3, V4 |
| Step 5 | R6, Documentation | QA/QC | Attributes | — |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| _DEPENDENCIES.md | Dependency coordination mode (NOT_TRACKED) | This folder |
| Decomposition | PKG-02 scope, DEL-02.03 entry, Section 1.2 Scope Focus | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Datasheet.md | Calculation content and attributes | This folder |
| Specification.md | Requirements R1-R6, Verification V1-V4 | This folder |
| Guidance.md | Principles P1-P4, Considerations, Trade-offs | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
| Related deliverables | DEL-02.01, DEL-02.02, DEL-02.04, DEL-02.05 | PKG-02 |
