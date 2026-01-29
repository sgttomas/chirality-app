# Procedure: DEL-02.05 Survey Reports

    ## Purpose

    Produce Survey Reports (Topographic Survey Report and Utility Locate Report) for PKG-02 Earthworks & Ground Improvement while satisfying Specification requirements (R1–R10) and supporting Guidance principles. Source: _CONTEXT.md; decomposition (location TBD).

    ## Prerequisites

    - **Dependencies:** Dependencies coordinated externally by humans (see _DEPENDENCIES.md). Key interfaces: site access coordination; utility owner coordination for utility records/verification; coordinate system from ER.
    - **Reference materials:** Employer's Requirements volumes (survey scope, accuracy requirements, coordinate system, deliverable formats) are required but not provided in _REFERENCES.md (**TBD**).
    - **Inputs:** PKG-02 scope and design limits for earthworks areas; design limits from other packages requiring existing conditions survey; existing survey control monuments (if available). Source: decomposition PKG-02 scope (location TBD).
    - **Qualifications:** Licensed professional land surveyor to perform surveys and certify reports (R8). **TBD**: ER will specify licensing jurisdiction requirements.
    - **Equipment:** Calibrated survey equipment (total station, GPS/GNSS, level, data collector) appropriate for specified accuracy (R7).

    ## Steps

### Phase 1: Survey Planning and Control Establishment

1. Review ER survey requirements (scope, accuracy, coordinate system/datum, deliverable formats, regulatory approvals) and coordinate with DEL-02.01 (Earthworks Drawings), DEL-02.04 (Geotechnical Reports – for borehole locations), and other design packages to understand survey area limits and feature requirements. **TBD** until ER references are provided. Maps to R1, R3, R5, R7, R9, R10.
2. Establish or verify project coordinate system, datum, and projection per ER requirements; document in `Datasheet.md` Coordinate System attribute. Coordinate with all design disciplines to ensure consistency. Maps to R9. Reference `Guidance.md` Coordinate System Consistency considerations.
3. Establish survey control network (horizontal control points, vertical benchmarks) or verify existing control monuments; perform control survey ties to project datum. Document control network in `Datasheet.md` Survey Control Network attribute. Maps to R2. Reference `Guidance.md` Survey Control Network considerations. **ASSUMPTION**: Control network designed per professional surveying standards.
4. Obtain site access permissions and coordinate survey timing with site availability, vegetation conditions, and design schedule. **ASSUMPTION**: Contractor site access and safety procedures apply.

### Phase 2: Topographic Survey Execution

5. Perform field topographic survey (total station, GPS, or aerial survey/LiDAR if appropriate) of existing site conditions: topography, structures, pavements, drainage features, vegetation, property boundaries. Survey limits shall extend beyond design limits to provide context. Maps to R1, R2, R5. Reference `Guidance.md` Survey Scope considerations.
6. Collect survey data to accuracy specified in ER and document accuracy methodology in field notes. Maps to R7. Reference `Guidance.md` Survey Accuracy considerations. **TBD**: ER will specify horizontal/vertical accuracy tolerances.
7. Process survey data (coordinate calculations, error checks, CAD/GIS data preparation) and create digital survey deliverables in formats specified by ER (e.g., AutoCAD DWG, Civil 3D surface, GIS shapefile). Maps to R2, R10. Reference `Guidance.md` Digital Data Formats considerations. **TBD**: ER will specify file formats.
8. Prepare topographic survey plan sheets showing existing conditions with contours, elevations, and features clearly labeled. Maps to R2.

### Phase 3: Utility Investigation Execution

9. Perform utility records search with utility owners, municipalities, and private entities to identify existing utilities in project area. Compile utility record drawings and ownership information. Maps to R3, R4. Reference `Guidance.md` Utility Ownership and Coordination considerations. **TBD**: ER will identify utility owners and coordination requirements.
10. Perform field utility locating using appropriate methods (e.g., electromagnetic locating, ground-penetrating radar, one-call service, test holes/vacuum excavation in critical areas). Mark and survey utility locations. Maps to R3, R4. Reference `Guidance.md` Utility Investigation Quality Levels considerations. **TBD**: ER may specify utility investigation quality level (e.g., ASCE 38 Quality Level).
11. Assess utility conflicts with proposed design from DEL-02.01 (Earthworks Drawings) and other design packages; document conflicts in utility conflict register. Maps to R3, R4. Coordinate with design team on conflict resolution (design adjustments, utility relocations).
12. Prepare utility location plan sheets showing existing utilities with type, location, depth (where verified), and owner labeled. Maps to R4.

### Phase 4: Report Preparation and Quality Control

13. Prepare Topographic Survey Report per `Datasheet.md` Report Content structure: methodology, control network, coordinate system/datum, survey data, accuracy statement, professional certification. Maps to R1, R2, R6, R7, R8. Reference `Guidance.md` Completeness of Existing Conditions principle.
14. Prepare Utility Locate Report per `Datasheet.md` Report Content structure: investigation methodology, utilities identified, conflict assessment, limitations/disclaimers, utility location plans. Maps to R3, R4, R6. Reference `Guidance.md` considerations on utility investigation confidence levels.
15. Include document control elements (title, report number, revision, date, author/organization) per R6. Use `Datasheet.md` Attributes as template for required metadata.
16. Perform survey data quality control: verify control network closure, check coordinate calculations, verify accuracy compliance, test digital data import into design software. Maps to R7, R10. Reference `Guidance.md` Data Quality and Usability principle. **ASSUMPTION**: Surveying QA/QC procedures (equipment calibration, field checks, office calculations verification).

### Phase 5: Review and Approval

17. Perform internal technical review against Specification verification items (V1: content completeness per R1–R10; V2: scope coverage, data format compatibility, coordinate system consistency, utility conflicts identified; V3: ER compliance). Reference `Guidance.md` Trade-offs for balancing survey scope/accuracy/schedule. Update `Datasheet.md` Configuration Notes to document any **TBDs** or limitations.
18. Address review comments; revise reports and survey data as necessary. Update revision attribute in `Datasheet.md`.
19. Obtain professional land surveyor seal/certification per regulatory requirements (R8). **TBD**: ER will specify regulatory jurisdiction and approval authority.
20. Issue controlled reports and digital survey data per D&B Contractor document control procedures (R6). Capture issue date in `Datasheet.md` Report Date attribute. Distribute to design team, coordinating packages, and Employer as required. **ASSUMPTION**: Standard D&B document control workflow.

    ## Verification

    - **V1 Check (R1, R2, R3, R4, R6, R7, R8 compliance)**: Verify survey reports include all required content sections per `Datasheet.md` Report Content (topographic: methodology, control, coordinate system, survey data, accuracy statement, certification, digital files; utility: methodology, utilities identified, conflict assessment, limitations, plan sheets). Verify document control elements and professional seal/certification are present. Verify stated accuracy meets ER requirements. Method: Technical review checklist by qualified surveyor; accuracy verification calculations against control network and field data; compare report sections to Specification R1–R10. Records: Review checklist, accuracy verification calculations, professional seal documentation.
    - **V2 Check (R2, R4, R5, R9, R10 compliance)**: Verify surveys cover all PKG-02 earthworks areas plus buffer; verify digital data formats import correctly into design software without errors or data loss; verify coordinate system is consistent across all survey deliverables and compatible with design packages; verify utility conflicts with proposed design are identified in conflict register. Method: Cross-reference survey limits with DEL-02.01 design limits; test import of CAD/GIS files into design software (AutoCAD, Civil 3D, etc.); coordinate system consistency check across deliverables; utility conflict matrix comparing utility locations to proposed design features. Records: Design software import test log with screenshots, coordinate system verification memo, utility conflict register with resolution tracking.
    - **V3 Check (R1, R3, R7, R8, R9 compliance)**: Verify alignment with ER survey requirements (scope, accuracy tolerances, coordinate system/datum, deliverable formats, regulatory approvals, utility investigation quality level) once Employer's Requirements volumes are available. Method: ER compliance matrix comparing survey deliverables to ER specifications; confirm accuracy meets or exceeds ER tolerances; confirm regulatory approval/certification obtained. Records: ER compliance matrix, accuracy compliance calculations, regulatory approval letters/certifications, Employer review comments and acceptance documentation. **TBD**: Pending ER volumes.

    ## Records

    - Issued Survey Reports (controlled revisions).
    - Review comments, approvals, and response log. ASSUMPTION: standard document control practice.

    ## References

    - _CONTEXT.md (deliverable identity, description, anticipated artifacts).
    - _DEPENDENCIES.md (NOT_TRACKED).
    - Decomposition file: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-02 scope, DEL-02 entries; location TBD).
    - `Datasheet.md`, `Specification.md`, `Guidance.md` for verification/context alignment.
    - _REFERENCES.md indicates no references yet.
