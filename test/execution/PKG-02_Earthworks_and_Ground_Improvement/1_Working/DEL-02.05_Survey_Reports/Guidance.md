# Guidance: DEL-02.05 Survey Reports

## Purpose

Provide guidance that keeps the Survey Reports aligned with PKG-02 earthworks objectives, Specification requirements R1-R10, and Procedure realization.

**Deliverable Role:** Survey reports establish the existing conditions baseline that underpins all design work. Accurate topographic and utility data are critical inputs to DEL-02.01 (Drawings), DEL-02.03 (Calculations), DEL-02.04 (Geotechnical Reports), and all other design packages.

Source: _CONTEXT.md; decomposition DEL-02.05 entry (location TBD).

## Principles

### Accuracy and Precision
**Principle:** Survey data must meet specified accuracy tolerances to provide reliable foundation for design; errors in survey data propagate through entire design and construction process.

**Rationale:** Design calculations, grading plans, and cut/fill quantities all depend on accurate survey data. Survey errors directly translate into construction errors, cost overruns, and rework.

**Application:**
- Establish robust control network with appropriate accuracy.
- Use calibrated equipment and proper field procedures.
- Document accuracy achieved and compare to requirements.
- Verify results through independent checks.
- **ASSUMPTION**: Aligns with professional surveying standards.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R2, R7, R8 |
| Datasheet mapping | Survey accuracy attribute, Accuracy statement section |
| Procedure Step | Steps 3, 6, 16 |

### Data Quality and Usability
**Principle:** Survey deliverables must be complete, clearly organized, and in formats compatible with design software to enable efficient design development without data translation errors.

**Rationale:** Poorly formatted or incomplete survey data slows design development and risks data loss during CAD/BIM import. Design software compatibility is essential.

**Application:**
- Provide data in formats specified by ER or compatible with design software.
- Test data import before finalizing deliverables.
- Include complete metadata (coordinate system, datum, accuracy, date).
- Organize data logically with clear layer/file naming.
- **ASSUMPTION**: Standard digital design workflow.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R2, R6, R10 |
| Datasheet mapping | Survey format attribute, Digital survey data section |
| Procedure Step | Steps 7, 15, 16 |

### Coordination and Consistency
**Principle:** Coordinate system, datum, and control network must be consistent across all survey deliverables and compatible with design packages to avoid costly coordinate conflicts.

**Rationale:** Multiple design disciplines rely on survey data. Coordinate system inconsistencies create fundamental errors that are difficult and expensive to correct.

**Application:**
- Establish project coordinate system early with all disciplines.
- Document coordinate system, datum, and projection clearly.
- Verify consistency across all survey deliverables.
- Coordinate with DEL-02.01, DEL-02.04, and other packages.
- **ASSUMPTION**: Cross-package coordination requirement.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R9 |
| Datasheet mapping | Coordinate system attribute |
| Procedure Step | Step 2 |

### Regulatory Compliance
**Principle:** Surveys shall satisfy jurisdictional requirements for professional land surveying practice, including licensing, certification, and professional seal where required.

**Rationale:** Professional surveying requirements ensure competence and accountability. Non-compliant surveys may not be accepted by regulatory authorities.

**Application:**
- Verify licensing requirements for BC jurisdiction.
- Ensure survey performed under licensed surveyor supervision.
- Include professional seal/certification.
- **TBD**: ER will specify regulatory authority.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R8 |
| Datasheet mapping | Author/organization attribute |
| Procedure Step | Step 19 |

### Completeness of Existing Conditions
**Principle:** Thorough documentation of existing site features (topography, structures, utilities, vegetation, boundaries) reduces design risk and construction surprises.

**Rationale:** Incomplete existing conditions data leads to design gaps and unforeseen conditions during construction. Comprehensive survey is due diligence for design.

**Application:**
- Survey all features within and beyond design limits.
- Include sufficient detail for design decisions.
- Document limitations and areas not surveyed.
- **ASSUMPTION**: Standard due diligence for design.

| Attribute | Value |
|-----------|-------|
| Specification mapping | R1, R3, R5 |
| Datasheet mapping | Report Content sections |
| Procedure Step | Steps 5, 9-12 |

## Requirement-Principle Traceability

| Requirement | Principles Applied | Key Considerations | Procedure Step |
|-------------|-------------------|-------------------|----------------|
| R1: Topographic Survey Report | Completeness, Accuracy | Comprehensive existing conditions documentation | Steps 5-8, 13 |
| R2: Topographic content | Data Quality, Accuracy | All required sections, compatible formats | Steps 5-8, 13, 16 |
| R3: Utility Locate Report | Completeness | Thorough utility identification and conflict assessment | Steps 9-12, 14 |
| R4: Utility locate content | Completeness | Methodology, limitations, conflict register | Steps 9-12, 14 |
| R5: PKG-02 scope coverage | Completeness | Survey extends beyond design limits | Steps 1, 5 |
| R6: Document control | Data Quality | Revision tracking, clear metadata | Steps 15, 18, 20 |
| R7: Survey accuracy | Accuracy | Match accuracy to design needs | Steps 6, 16 |
| R8: Professional qualifications | Regulatory | Licensed surveyor, proper seals | Step 19 |
| R9: Coordinate system | Coordination | Consistent across all packages | Step 2 |
| R10: Digital data formats | Data Quality | Compatible with design software | Step 7 |

## Considerations

### Survey Control Network
- Establish robust control network (horizontal and vertical control points, benchmarks) early.
- Control density and accuracy determine survey quality.
- **TBD**: ER may provide existing control monuments or require specific control approach.
- **ASSUMPTION**: Control network designed per professional surveying standards.
- **Procedure reference:** Step 3.

### Survey Timing and Site Access
- Coordinate survey timing with site access availability and vegetation conditions.
- Consider leaves-off conditions for better ground visibility.
- Consider phased surveys if entire site not accessible initially.
- **ASSUMPTION**: Site access coordination with Employer.
- **Procedure reference:** Step 4.

### Aerial vs. Ground Survey Methods
- Evaluate aerial survey (photogrammetry, LiDAR) vs. conventional ground survey.
- Consider site size, vegetation, required accuracy, and cost.
- Aerial methods efficient for large sites but may require ground survey supplement.
- **TBD**: ER may specify survey methods.
- **Procedure reference:** Steps 5, 6.

### Utility Investigation Quality Levels
- Different utility investigation methods provide different confidence levels (ASCE 38 Quality Levels A-D).
- Records search (low confidence) may suffice for preliminary design.
- Test holes (high confidence) required for final design in critical areas.
- **TBD**: ER may specify utility investigation quality level.
- **Procedure reference:** Step 10.

### Utility Ownership and Coordination
- Existing utilities may be owned by multiple entities.
- Coordination required for verification, relocation approvals, and protection.
- **TBD**: ER will identify utility owners and coordination requirements.
- **Procedure reference:** Steps 9, 11.

## Trade-offs

### Survey Scope vs. Cost
**Trade-off:** Comprehensive survey of entire site provides complete baseline but increases cost; focused survey reduces cost but may require supplemental surveys later.

**Guidance:** Survey all areas within design limits plus reasonable buffer; prioritize detailed surveys in critical areas.

| Attribute | Value |
|-----------|-------|
| Principle reference | Completeness |
| Specification mapping | R1, R5 |
| Procedure Step | Step 5 |

### Survey Accuracy vs. Cost
**Trade-off:** Higher accuracy requires more time, sophisticated equipment, and rigorous procedures; match accuracy to design needs.

**Guidance:** Use R7 and ER requirements as baseline; higher accuracy for structure locations, standard for general topography.

| Attribute | Value |
|-----------|-------|
| Principle reference | Accuracy |
| Specification mapping | R7 |
| Procedure Step | Step 6 |

### Survey Schedule vs. Design Schedule
**Trade-off:** Early survey provides baseline for design but may not capture site changes; late survey delays design start.

**Guidance:** Perform survey as early as feasible; update if significant site changes occur.

| Attribute | Value |
|-----------|-------|
| Principle reference | Coordination |
| Procedure Step | Steps 4, 5 |

### Utility Investigation Rigor
**Trade-off:** Extensive utility investigation (test holes) provides high confidence but takes time; records search faster but lower confidence.

**Guidance:** Use R3, R4 and risk assessment to balance investigation rigor; higher rigor for conflict areas.

| Attribute | Value |
|-----------|-------|
| Principle reference | Completeness |
| Specification mapping | R3, R4 |
| Procedure Step | Step 10 |

## Procedure Coordination

| Procedure Phase | Guidance Element | Key Focus |
|-----------------|------------------|-----------|
| Phase 1 (Planning) | Coordination, Accuracy | Establish control and coordinate system |
| Phase 2 (Topographic) | Accuracy, Completeness | Execute quality field survey |
| Phase 3 (Utility) | Completeness | Thorough utility investigation |
| Phase 4 (QC/Report) | Data Quality, Accuracy | Verify and document |
| Phase 5 (Review/Approval) | Regulatory, All principles | Review, certify, issue |

## Conflict Table (for human ruling)

No conflicts identified from available sources at this stage. If conflicts arise during survey execution, document here with:

| Column | Description |
|--------|-------------|
| Conflict ID | Unique identifier |
| Conflict | Short statement of conflict |
| Source A | File + section |
| Source B | File + section |
| Impacted requirements | R1-R10 affected |
| Proposed resolution | PROPOSAL |
| Human ruling | TBD |

## Cross-Document Traceability

| Document | Key Linkages |
|----------|--------------|
| Datasheet.md | Attributes and Report Content mapped to principles |
| Specification.md | Requirements R1-R10 mapped to principles; V1-V3 linked to considerations |
| Procedure.md | Steps 1-20 implement principles and verification expectations |

## References

| Reference | Description | Location |
|-----------|-------------|----------|
| _CONTEXT.md | Deliverable identity, description, anticipated artifacts | This folder |
| Decomposition | PKG-02 scope, DEL-02.05 entry, Section 1.2 Scope Focus | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (location TBD) |
| Specification.md | Requirements R1-R10, Verification V1-V3 | This folder |
| Datasheet.md | Report content and attributes | This folder |
| Procedure.md | Steps 1-20, Verification, Records | This folder |
| _REFERENCES.md | ER volumes and reference materials | This folder (currently empty; pending) |
