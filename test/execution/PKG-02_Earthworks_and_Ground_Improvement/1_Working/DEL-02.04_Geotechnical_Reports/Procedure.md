# Procedure: DEL-02.04 Geotechnical Reports

    ## Purpose

    Produce Geotechnical Reports (Investigation Report and Ground Improvement Design Report if required) for PKG-02 Earthworks & Ground Improvement while satisfying Specification requirements (R1–R8) and supporting Guidance principles. Source: _CONTEXT.md; decomposition (location TBD).

    ## Prerequisites

    - **Dependencies:** Dependencies coordinated externally by humans (see _DEPENDENCIES.md). Key interfaces: survey data for investigation locations; design loads from structural packages for foundation design.
    - **Reference materials:** Employer's Requirements volumes (geotechnical criteria, site data, regulatory requirements) are required but not provided in _REFERENCES.md (**TBD**).
    - **Inputs:** PKG-02 scope for earthworks and ground improvement; site access permissions; previous site investigations (if available); design criteria from ER. Source: decomposition PKG-02 scope (location TBD).
    - **Qualifications:** Qualified, licensed geotechnical engineer to lead investigation and report preparation (R6). **TBD**: ER will specify licensing jurisdiction requirements.

    ## Steps

### Phase 1: Investigation Planning

1. Review ER geotechnical requirements, site conditions, design criteria, and coordinate with DEL-02.01 (Earthworks Drawings), DEL-02.02 (Specifications), DEL-02.03 (Calculations) to understand investigation needs. **TBD** until ER references are provided. Maps to R1, R4, R7.
2. Develop investigation program (borehole/test pit locations, depths, sampling methods, laboratory testing scope) aligned with `Datasheet.md` Investigation Scope attribute and Specification R2, R8. Coordinate with survey team for accurate borehole positioning. Reference `Guidance.md` Investigation Program Adequacy considerations.
3. Obtain site access permissions, utility clearances, and environmental/safety approvals for field investigation work. **ASSUMPTION**: Contractor safety and permitting procedures apply.

### Phase 2: Field Investigation and Laboratory Testing

4. Execute field investigation (drilling, sampling, in-situ testing) per approved program under supervision of qualified geotechnical engineer. Document field conditions, groundwater levels, soil/rock descriptions per standard classification systems (e.g., ASTM D2487, D2488). Maps to R1, R2.
5. Conduct laboratory testing (classification, moisture-density, strength, consolidation as required) per investigation program and applicable standards. **TBD**: Standards reference from ER. Maps to R2, R8.
6. Compile field and laboratory data; perform quality control checks for data consistency and completeness. Reference `Guidance.md` considerations on investigation adequacy and testing scope.

### Phase 3: Engineering Analysis and Report Preparation

7. Perform engineering analysis: interpret subsurface conditions, determine soil/rock design parameters (bearing capacity, friction angle, cohesion, settlement characteristics), evaluate excavation stability, groundwater impacts, and earthworks compaction criteria. Maps to R1, R2, R8. Reference `Guidance.md` Design Parameter Conservatism.
8. If ground improvement is required (per ER or based on investigation findings), develop Ground Improvement Design Report content: treatment objectives, method selection (e.g., preloading, stone columns, soil mixing), design calculations, performance criteria, construction methodology, and quality control requirements. Maps to R3. Reference `Guidance.md` Ground Improvement Feasibility considerations. **TBD**: ER will specify if ground improvement is required.
9. Prepare Geotechnical Investigation Report per `Datasheet.md` Report Content structure: executive summary, site description, investigation program, subsurface conditions, laboratory results, engineering analysis, design recommendations (foundations, earthworks, pavements, excavation). Ensure clarity and completeness per `Guidance.md` Completeness and Clarity principle. Maps to R1, R2, R4, R7, R8.
10. Include document control elements (title, report number, revision, date, author/organization, professional seal/stamp) per R5, R6. Use `Datasheet.md` Attributes as template for required metadata.
11. Coordinate geotechnical design parameters with structural packages (PKG-05 Concrete Structures, PKG-06 Structural Steelwork, PKG-04 Pavements) to support their design schedules. Maps to R7. Reference `Guidance.md` Coordination and Consistency principle.

### Phase 4: Review and Approval

12. Perform internal technical review against Specification verification items (V1: content completeness per R1–R8; V2: PKG-02 scope coverage and cross-package coordination; V3: ER compliance). Reference `Guidance.md` Trade-offs for balancing detail vs. schedule. Update `Datasheet.md` Configuration Notes to document any **TBDs** or **ASSUMPTIONs** requiring resolution.
13. Address review comments; revise report as necessary. Update revision attribute in `Datasheet.md`.
14. Obtain professional engineer seal/stamp and approvals per regulatory requirements (R6). **TBD**: ER will specify approval authority and regulatory jurisdiction.
15. Issue controlled report per D&B Contractor document control procedures (R5). Capture issue date in `Datasheet.md` Report Date attribute. Distribute to design team, coordinating packages, and Employer as required. **ASSUMPTION**: Standard D&B document control workflow.

    ## Verification

    - **V1 Check (R1, R2, R3, R5, R6, R8 compliance)**: Verify geotechnical reports include all required content sections per `Datasheet.md` Report Content (executive summary, site description, investigation program, subsurface conditions, laboratory results, analysis, recommendations for foundations/earthworks/pavements/excavation/dewatering/compaction). Verify document control elements and professional seal/stamp are present. Method: Technical review checklist by qualified geotechnical engineer; compare report sections to Specification R1–R8. Records: Review checklist, approval signatures, professional seal documentation.
    - **V2 Check (R4, R7, R8 compliance)**: Verify reports address all geotechnical aspects of PKG-02 earthworks scope (grading, excavation, fill placement, ground improvement) and provide design parameters required by coordinating packages (PKG-04, PKG-05, PKG-06). Method: Cross-reference report recommendations with `Guidance.md` coordination notes and DEL-02.01, DEL-02.02, DEL-02.03 design requirements; confirm parameter transmittal to structural packages. Records: Coordination meeting minutes, parameter transmittal logs, interdisciplinary review comments.
    - **V3 Check (R1, R3, R6 compliance)**: Verify alignment with ER geotechnical requirements (investigation scope, design criteria, regulatory standards, approval authority) once Employer's Requirements volumes are available. Method: ER compliance matrix comparing report content to ER specifications; confirm regulatory approval/acceptance. Records: ER compliance matrix, regulatory approval letters/stamps, Employer review comments and acceptance documentation. **TBD**: Pending ER volumes.

    ## Records

    - Issued Geotechnical Reports (controlled revisions).
    - Review comments, approvals, and response log. ASSUMPTION: standard document control practice.

    ## References

    - _CONTEXT.md (deliverable identity, description, anticipated artifacts).
    - _DEPENDENCIES.md (NOT_TRACKED).
    - Decomposition file: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-02 scope, DEL-02 entries; location TBD).
    - `Datasheet.md`, `Specification.md`, `Guidance.md` for verification/context alignment.
    - _REFERENCES.md indicates no references yet.
