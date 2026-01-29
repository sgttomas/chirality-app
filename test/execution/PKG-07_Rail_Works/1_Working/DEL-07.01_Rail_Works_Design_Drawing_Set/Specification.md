# Specification: DEL-07.01 Rail Works Design Drawing Set

**Enrichment Status:** Pass 3 Complete (3-pass enrichment: Initial draft, Cross-reference enrichment, Final reconciliation)

## Scope

### Deliverable Scope

This specification governs development of the **Rail Works Design Drawing Set** for **PKG-07 Rail Works** at the Canola Oil Transload Facility, Fraser Surrey Terminal.

**Physical scope:**
- New rail tracks 6 & 7 (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259)
- Track 5 restoration and modifications (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259)
- Associated ballast works (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259)
- End stops (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259)

**Deliverable purpose:**
Define the design arrangement and details for rail works per the Employer's Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265).

### Anticipated Artifacts

Minimum anticipated artifacts within this scope (per decomposition; see Datasheet.md: Content for detailed description):

| Artifact | Coverage | Cross-Reference |
|----------|----------|-----------------|
| Track layout plans | Plan view arrangement for Tracks 5, 6, 7 with limits of work | Datasheet.md: Content; Guidance.md: Examples; Procedure.md: Steps 4 |
| Rail profiles | Longitudinal profiles showing rail elevations and vertical geometry | Datasheet.md: Content; Guidance.md: Examples; Procedure.md: Steps 4 |
| Ballast sections | Cross-sections showing ballast depth, material zones, sub-base | Datasheet.md: Content; Guidance.md: Examples; Procedure.md: Steps 4 |
| End stop details | Detail drawings of end stop configuration and anchoring | Datasheet.md: Content; Guidance.md: Examples; Procedure.md: Steps 4 |

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265)

### Scope Exclusions

- Employer-provided items except at interface connections (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47)
- Rail works outside the defined package scope (other tracks, sidings not part of Phase 1)
- Adjacent package deliverables (civil works, process systems) except as required for interface coordination (coordination managed externally per NOT_TRACKED dependency mode)

## Requirements

### Functional Requirements

| Req ID | Requirement | Rationale | Verification | Cross-Reference |
|--------|-------------|-----------|--------------|-----------------|
| FR-01 | The drawing set shall cover all anticipated artifacts: track layout plans, rail profiles, ballast sections, end stop details | Completeness ensures design communicates arrangement and details for review and construction | Completeness check against artifact list | Datasheet.md: Content; Guidance.md: Purpose; Procedure.md: Verification (completeness check) |
| FR-02 | Drawings shall clearly differentiate new works (Tracks 6 & 7) versus restoration/modification (Track 5) with notes and boundaries | Clarity prevents construction scope ambiguity | Visual inspection of limits-of-work notation | Datasheet.md: Content (Additional Drawing Content Requirements); Guidance.md: Considerations |
| FR-03 | Drawings shall provide traceability to DEL-07.02 (technical specification) and DEL-07.03 (design calculations) | Ensures design coherence across deliverables | Cross-check consistency per Procedure.md: Steps 5 | Datasheet.md: References (Related Deliverables); Guidance.md: Considerations; Procedure.md: Steps 5 |
| FR-04 | Track layout plans shall show track arrangement, alignment, and interface points | Communicate spatial arrangement and coordination requirements | Plan review for completeness and clarity | Datasheet.md: Content; Guidance.md: Examples |
| FR-05 | Rail profiles shall show rail elevations, vertical geometry, and critical elevations | Communicate vertical design and construction requirements | Profile review for completeness and clarity | Datasheet.md: Content; Guidance.md: Examples |
| FR-06 | Ballast sections shall show depth, material zones, and sub-base details | Communicate ballast construction requirements | Section review for completeness and clarity | Datasheet.md: Content; Guidance.md: Examples |
| FR-07 | End stop details shall show configuration, anchoring, and clearances | Communicate end stop design and installation requirements | Detail review for completeness and clarity | Datasheet.md: Content; Guidance.md: Examples |

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259, :265)

### Performance Requirements

| Req ID | Requirement | Rationale | Verification | Cross-Reference |
|--------|-------------|-----------|--------------|-----------------|
| PR-01 | Rail/track performance criteria, tolerances, materials, and workmanship requirements shall be reflected in drawing notes/callouts where relevant | Ensures drawings communicate design intent aligned with ER | Cross-check against DEL-07.02 and ER requirements (clauses **TBD**) | Datasheet.md: Conditions (Design Criteria); Guidance.md: Considerations; Procedure.md: Steps 5 |
| PR-02 | Design loads and criteria shall be consistent with DEL-07.03 design calculations | Ensures design coherence | Cross-check against DEL-07.03 calculation basis | Datasheet.md: Attributes (Rail Works Scope Parameters); Procedure.md: Steps 5 |

(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:266)

### Interface Requirements

| Req ID | Requirement | Rationale | Verification | Cross-Reference |
|--------|-------------|-----------|--------------|-----------------|
| IR-01 | Drawings shall identify interface points with adjacent packages without asserting unsourced requirements | Facilitates coordination while maintaining scope boundaries | Interface callout review | Datasheet.md: Content (Additional Drawing Content Requirements); Guidance.md: Considerations |
| IR-02 | Interface details (tie-ins, limits, clearances, temporary works) shall be coordinated externally per NOT_TRACKED dependency mode | Coordination approach aligns with project framework | Coordination records per external workflow | Datasheet.md: Conditions (Interface boundaries); Procedure.md: Prerequisites |

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47; clauses **TBD**)

### Quality Requirements

| Req ID | Requirement | Rationale | Verification | Cross-Reference |
|--------|-------------|-----------|--------------|-----------------|
| QR-01 | Document control practices (numbering, revision, issue status) shall comply with ER general requirements | Ensures traceability and auditability | Document control compliance check | Datasheet.md: Attributes (Drawing Set Metadata); Procedure.md: Steps 6 |
| QR-02 | Drawing set shall be checked per Procedure.md verification workflow before issue | Ensures quality and completeness before submission | Procedure execution evidence | Procedure.md: Steps, Verification |
| QR-03 | Design assumptions visible in drawings shall be traceable to DEL-07.03 or explicitly tagged **ASSUMPTION** | Prevents implicit assumptions; maintains transparency | Assumption traceability check | Datasheet.md: Content (Additional Drawing Content Requirements); Guidance.md: Trade-offs; Procedure.md: Steps 3 |

(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, clauses TBD; Procedure.md)

## Standards

### Applicable Standards

| Standard Category | Standard/Code | Status | Application | Cross-Reference |
|-------------------|---------------|--------|-------------|-----------------|
| Drawing standards | **TBD** — per ER drawing/CAD requirements | Clauses TBD | Sheet formats, scales, title blocks, layer conventions | Datasheet.md: Attributes (Drawing Set Metadata); Guidance.md: Principles |
| Document control | **TBD** — per ER document control procedures | Clauses TBD | Numbering, revision tracking, issue practices | Datasheet.md: Attributes (Drawing Set Metadata); Procedure.md: Steps 6 |
| Rail/track design | **TBD** — per ER rail works requirements | Clauses TBD | Design loads, geometry, tolerances | Datasheet.md: Conditions (Design Criteria); cross-check with DEL-07.02, DEL-07.03 |
| QA/QC procedures | **TBD** — per ER general requirements | Clauses TBD | Checking, review, approval workflows | Procedure.md: Steps 6; Guidance.md: Principles |

(Source: test/Volume_2_Part_1_Employers_Requirements.pdf; test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD)

**ASSUMPTION:** Standard North American rail practices are likely applicable (AREMA, rail supplier standards); confirm with ER requirements once extracted.

## Verification

### Verification Methods

Verification is performed per Procedure.md workflow. Each requirement category maps to specific verification activities:

| Requirement Category | Verification Method | Acceptance Criterion | Procedure Reference |
|---------------------|---------------------|---------------------|---------------------|
| Functional (FR-01 to FR-07) | Completeness check against anticipated artifacts; visual review of content | All anticipated artifacts present and complete per decomposition | Procedure.md: Steps 1, 4; Verification |
| Performance (PR-01, PR-02) | Cross-check consistency with DEL-07.02 (specification) and DEL-07.03 (calculations) | No conflicts; design notes/callouts align with technical specification and calculation basis | Procedure.md: Steps 5; Verification |
| Interface (IR-01, IR-02) | Interface callout review; coordination records check | Interface points identified; coordination performed per external workflow | Procedure.md: Steps 2, 5; Verification |
| Quality (QR-01, QR-02, QR-03) | Document control compliance check; procedure execution evidence; assumption traceability check | Document control rules applied; procedure steps completed; assumptions traced or tagged | Procedure.md: Steps 3, 6; Verification |

### Acceptance Criteria

**General acceptance:**
- All requirements (FR, PR, IR, QR) verified per methods above
- All **TBD** items resolved or explicitly carried forward with approval
- All **ASSUMPTION** items traced to DEL-07.03 or explicitly tagged and approved
- No unresolved conflicts with DEL-07.02 or DEL-07.03

**Specific acceptance criteria:**
- **TBD** — will be refined once ER clauses and project QA procedures are identified (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, clauses TBD)

## Verification-to-Records Mapping

| Verification Item | Requirement Refs | Evidence / Record Produced | Where Defined | Cross-Reference |
|-------------------|------------------|----------------------------|---------------|-----------------|
| Completeness check | FR-01 to FR-07 | Drawing sheet index / sheet list covering all anticipated artifacts | Procedure.md: Steps 1, 4; Records | Datasheet.md: Content |
| Consistency check (DEL-07.02) | PR-01, FR-03 | Cross-check notes documenting alignment with technical specification; inputs/assumptions register updates | Procedure.md: Steps 5; Records | Datasheet.md: References (Related Deliverables) |
| Consistency check (DEL-07.03) | PR-02, FR-03, QR-03 | Cross-check notes documenting alignment with design calculations; assumption traceability matrix | Procedure.md: Steps 3, 5; Records | Datasheet.md: References (Related Deliverables) |
| Interface coordination check | IR-01, IR-02 | Coordination records per external workflow; interface callout review notes | Procedure.md: Steps 2, 5; Records | Guidance.md: Considerations |
| Constructability/clarity check | FR-02, FR-04 to FR-07 | IDC evidence, review comment logs/responses, limits-of-work notation verification | Procedure.md: Steps 6; Records | Guidance.md: Considerations, Trade-offs |
| Document control compliance | QR-01 | Issue transmittal / document control submission record with drawing metadata populated | Procedure.md: Steps 6; Records | Datasheet.md: Attributes (Drawing Set Metadata) |
| Assumption traceability | QR-03 | Inputs/assumptions register linking drawing assumptions to DEL-07.03 or **ASSUMPTION** tags | Procedure.md: Steps 3; Records | Guidance.md: Trade-offs |

## Documentation

### Deliverable Outputs

Primary outputs (anticipated artifacts per decomposition):
- Track layout plans (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265; Datasheet.md: Content)
- Rail profiles (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265; Datasheet.md: Content)
- Ballast sections (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265; Datasheet.md: Content)
- End stop details (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265; Datasheet.md: Content)

### Supporting Documentation

Per Procedure.md: Records, the following supporting documentation shall be maintained:
- Drawing sheet index (sheet list)
- Inputs/assumptions register (tracing design basis to DEL-07.03 and noting **ASSUMPTION** items)
- Drawing checklists (self-check, discipline check, IDC check)
- Review comments/responses logs
- Issue transmittals and document control submission records

### Metadata Requirements

Drawing metadata (numbering, revision, issue status, title block information) is **TBD** pending ER document control requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, clauses TBD; Datasheet.md: Attributes).

## Cross-Document Notes

### Specification ↔ Datasheet

- Requirements defined in this Specification are traceable to Datasheet entities (Attributes, Conditions, Content)
- Datasheet.md: Attributes defines metadata fields that must comply with QR-01 (document control requirements)
- Datasheet.md: Content lists anticipated artifacts that satisfy FR-01 (completeness requirement)

### Specification ↔ Guidance

- Requirements rationale is provided in Guidance.md: Principles and Considerations
- Guidance.md helps interpret requirements intent without inventing unsourced requirements
- Guidance.md: Trade-offs addresses QR-03 (assumption visibility and traceability)

### Specification ↔ Procedure

- Verification methods map to Procedure.md: Steps and Verification
- Procedure.md: Records defines evidence that demonstrates requirement compliance
- Procedure workflow operationalizes this Specification's requirements into actionable steps
