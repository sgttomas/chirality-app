# Guidance: DEL-02.01 Earthworks Design Drawing Set

## Purpose

Provide design principles and practical considerations to ensure the Earthworks Design Drawing Set achieves clarity, constructability, and regulatory compliance while satisfying PKG-02 objectives and Specification requirements R1-R7.

**Deliverable Role:** This drawing set translates earthworks design intent into constructible arrangements that enable field execution and verification per DEL-02.02 (Technical Specification) and DEL-02.07 (Method Statement).

Source: _CONTEXT.md; decomposition DEL-02.01 entry (location TBD).

## Principles

### P1: Clarity and Constructability
**Principle:** Drawing detail and presentation should prioritize field usability and construction sequencing.

**Rationale:** Design drawings are the primary field reference for earthworks contractors. Ambiguity in grading, cut/fill limits, or ground improvement zones creates rework risk and safety concerns.

**Application:**
- Use clear line weights, hatching, and annotation standards to distinguish existing vs. proposed conditions.
- Show construction limits, phasing, and access routes where applicable.
- Coordinate section locations with plan views for ease of reference.
- **ASSUMPTION**: Aligns with project safety and quality objectives.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1, R2, R3, R4, R5 |
| Datasheet mapping | Drawing content items 1-4, Scale attribute |
| Procedure Step | Steps 3.1-3.4, 4.5 |

### P2: Interface Management
**Principle:** Define Contractor scope boundaries and interface connections explicitly to prevent scope creep or gaps.

**Rationale:** Decomposition Section 1.2 Scope Focus clarifies that this decomposition covers Contractor scope only, with Employer-responsible items excluded except for interface connections.

**Application:**
- Clearly annotate earthworks limits where they interface with Employer-provided infrastructure or out-of-scope areas.
- Show connection details where Contractor earthworks meet existing terminal infrastructure.
- Note interfaces with other packages (e.g., underground utilities in PKG-03, pavements in PKG-04).

**Source:** Decomposition Section 1.2 Scope Focus (location TBD).

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1, R6 |
| Datasheet mapping | Context & Conditions, Drawing content coverage |
| Procedure Step | Step 2.2 |

### P3: Multi-Deliverable Coordination
**Principle:** Ensure earthworks drawings align with related deliverables in PKG-02 and adjacent packages.

**Rationale:** Earthworks design drawings must be consistent with calculations, specifications, geotechnical reports, and survey data to prevent construction conflicts.

**Application:**
- Coordinate cut/fill quantities with DEL-02.03 (Design Calculations).
- Coordinate ground improvement zones and methods with DEL-02.04 (Geotechnical Reports) and DEL-02.02 (Technical Specification).
- Coordinate finish grades and benchmarks with DEL-02.05 (Survey Reports).
- Coordinate drainage slopes with PKG-03 (Underground Utilities & Drainage).
- **ASSUMPTION**: Coordination typically managed through design review and issue cycle.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1, R2, R3, R4, R6 |
| Datasheet mapping | Drawing content items 1-4, Coordinate system attribute |
| Procedure Step | Steps 1.2-1.5, 3.1-3.4, 4.3 |

### P4: Design Basis Documentation
**Principle:** Reference design assumptions, criteria, and source documents clearly in drawing notes and title blocks.

**Rationale:** Drawings should be traceable to their design basis for verification and future modification.

**Application:**
- Include general notes referencing applicable standards, ER requirements, and design criteria.
- Reference geotechnical report recommendations in ground improvement details.
- Note survey datum and coordinate system per DEL-02.05.
- **TBD**: Specific ER requirements and design criteria pending reference materials.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1, R4, R5, R7 |
| Datasheet mapping | Attributes (drawing number, revision, classification) |
| Procedure Step | Steps 3.5, 3.6 |

## Requirement-Principle Traceability

| Requirement | Principles Applied | Key Considerations | Procedure Step |
|-------------|-------------------|-------------------|----------------|
| R1: Design definition per ER | P1, P2, P4 | Clarity, scope boundaries, design basis traceability | Steps 1-3 |
| R2: Grading plans | P1, P3 | Constructability, coordination with drainage (PKG-03) | Step 3.1 |
| R3: Cut/fill plans | P1, P3 | Constructability, coordination with DEL-02.03 quantities | Step 3.2 |
| R4: Ground improvement layout | P1, P3, P4 | Constructability, coordination with DEL-02.04, treatment methods per DEL-02.02 | Step 3.3 |
| R5: Sections | P1, P3, P4 | Clarity of existing/proposed conditions, layer details | Step 3.4 |
| R6: PKG-02 scope coverage | P2, P3 | Interface management, multi-deliverable coordination | Step 2.1 |
| R7: Document control | P4 | Traceability, revision management | Steps 2.4, 3.6, 5 |

## Considerations

### Design Phase Considerations

1. **Input Data Quality:**
   - Verify topographic survey accuracy and currency (DEL-02.05).
   - Confirm geotechnical investigation coverage and depth (DEL-02.04).
   - Identify design criteria and performance requirements from ER (**TBD** pending ER volumes).
   - **Procedure reference:** Step 1 (Compile and Validate Inputs).

2. **Regulatory and Environmental Constraints:**
   - Identify permit requirements affecting earthworks scope and limits.
   - Consider environmental protection measures (erosion control, sediment management).
   - Address terminal operational continuity constraints.
   - **TBD**: Specific constraints pending ER requirements and permit documentation.
   - **Procedure reference:** Step 1.1.

3. **Constructability and Sequencing:**
   - Consider equipment access and mobilization routes.
   - Identify phasing to maintain terminal operations during construction.
   - Coordinate temporary works requirements (haul roads, stockpile areas, dewatering).
   - **ASSUMPTION**: Contractor to develop detailed construction sequencing in DEL-02.07 (Method Statement).
   - **Procedure reference:** Step 3, Step 4.5.

### QA/QC Considerations

1. **Cross-Document Verification:**
   - Confirm drawing content matches Datasheet attributes and Specification requirements.
   - Verify quantities and dimensions align with DEL-02.03 (Design Calculations).
   - Check terminology consistency across all four documents (Datasheet, Specification, Guidance, Procedure).
   - **Procedure reference:** Step 4.3.

2. **Review Workflow:**
   - Internal design review against R1-R7 and V1-V3 (Specification verification items).
   - Coordination review with adjacent packages (PKG-03, PKG-04, etc.).
   - Employer review and approval per R7 document control requirements.
   - **ASSUMPTION**: Standard D&B QA/QC workflow applies.
   - **Procedure reference:** Step 4.

3. **Revision Management:**
   - Track drawing revisions per R7 document control.
   - Maintain revision history and response to review comments.
   - Coordinate revision impacts with dependent deliverables.
   - **Procedure reference:** Step 5.

## Trade-offs

### Detail Level vs. Schedule
**Trade-off:** More drawing detail improves constructability but increases production and revision effort.

**Guidance:** Use Specification requirements (R1-R7) and verification items (V1-V3) to define minimum necessary detail. Avoid unnecessary detail that doesn't support construction or verification. Balance is typically project-controls-driven.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1-R7, V1-V3 |
| Datasheet mapping | Sheet list, Scale attributes |
| Procedure Step | Step 3 |

### Prescriptive vs. Performance-Based
**Trade-off:** Prescriptive drawings provide more construction certainty but may limit Contractor means and methods flexibility. Performance-based drawings allow flexibility but require more robust quality verification.

**Guidance:**
- Use prescriptive details where design intent is critical (e.g., ground improvement zones, finish grades).
- Use performance-based details where Contractor means and methods flexibility is appropriate (e.g., compaction methods, sequencing).
- Align approach with DEL-02.02 (Technical Specification) and DEL-02.07 (Method Statement) expectations.
- **TBD**: ER may specify preferred approach.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R2-R5 |
| Procedure Step | Steps 2-3 |

### Drawing Format and Standards
**Trade-off:** Consistency with Contractor standards improves efficiency; consistency with Employer standards improves integration with existing terminal documentation.

**Guidance:**
- Confirm CAD standards, sheet sizes, and drawing numbering system requirements from ER.
- If ER does not specify, use Contractor standards and document choice in drawing general notes.
- **TBD**: Pending ER requirements.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R7 |
| Datasheet mapping | Sheet size, CAD standard, Drawing number attributes |
| Procedure Step | Step 2.4 |

## Examples

**Note:** Specific examples require ER requirements and design inputs. The following are typical examples for this deliverable type:

1. **Grading Plan Example (R2):**
   - Plan view showing existing and proposed contours, finish grade elevations at grid intersections, drainage slopes, and grading limits.
   - **TBD**: Specific grading arrangement pending design.
   - **Procedure reference:** Step 3.1.

2. **Ground Improvement Layout Example (R4):**
   - Plan view showing treatment zones (e.g., dynamic compaction areas, surcharge zones), grid spacing, and treatment depths.
   - Detail references to DEL-02.04 (Geotechnical Reports) and DEL-02.02 (Technical Specification) for methods and acceptance criteria.
   - **TBD**: Specific ground improvement design pending DEL-02.04.
   - **Procedure reference:** Step 3.3.

3. **Section Example (R5):**
   - Cross-section showing existing grade, proposed grade, cut/fill depths, ground improvement extents, fill layer thicknesses, and material specifications.
   - **TBD**: Specific section details pending design.
   - **Procedure reference:** Step 3.4.

## Procedure Coordination

| Procedure Step | Guidance Element | Key Focus |
|----------------|------------------|-----------|
| Step 1 | Considerations (Input Data Quality) | Validate inputs before design |
| Step 2 | P2 (Interface Management), R6 | Define scope and boundaries |
| Step 3 | P1 (Clarity), P3 (Coordination), P4 (Design Basis) | Develop drawing content |
| Step 4 | QA/QC Considerations, V1-V3 | Verify completeness and compliance |
| Step 5 | R7 (Document Control), Revision Management | Control and issue deliverable |

## Conflict Table (for human ruling)

No conflicts identified from available sources at this stage. If conflicts arise during production (e.g., between ER requirements and Contractor standards, or between design calculations and geotechnical recommendations), they should be documented here with:

| Column | Description |
|--------|-------------|
| Conflict ID | Unique identifier |
| Conflict | Short statement of conflict |
| Source A | File + section |
| Source B | File + section |
| Impacted requirements | R1-R7 affected |
| Proposed resolution | PROPOSAL |
| Human ruling | TBD |

## Cross-Document Traceability

| Document | Key Linkages |
|----------|--------------|
| Datasheet.md | Attributes mapped to principles; Drawing content items linked to R2-R5 |
| Specification.md | Requirements R1-R7 mapped to P1-P4; V1-V3 linked to QA/QC Considerations |
| Procedure.md | Steps 1-5 implement principles and verification expectations |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| Decomposition | PKG-02 scope, DEL-02.01 entry, Section 1.2 Scope Focus | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Specification.md | Requirements R1-R7, Verification V1-V3 | This folder |
| Datasheet.md | Drawing attributes and content | This folder |
| Procedure.md | Steps 1-5, Verification, Records | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
