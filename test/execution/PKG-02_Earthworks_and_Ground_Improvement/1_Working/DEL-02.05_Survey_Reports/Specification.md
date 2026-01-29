# Specification: DEL-02.05 Survey Reports

    ## Scope

    This deliverable defines the requirements for Survey Reports within PKG-02 Earthworks & Ground Improvement. Source: _CONTEXT.md; decomposition DEL-02 entry (location TBD).

    Package scope context includes Site grading, excavation, filling, ground improvements, geotechnical works, surveys. Source: decomposition PKG-02 scope (location TBD).

    Exclusions: This decomposition covers the Contractor's scope of work only. Employer-responsible items (permits obtained by Employer, nitrogen skid supply) are excluded except for interface connections. Source: decomposition Section 1.2 Scope Focus (location TBD).

    ## Requirements

    - R1: Topographic Survey Report shall document existing site conditions (topography, structures, features, vegetation, boundaries) for design verification and approvals. Source: decomposition DEL-02 entry and _CONTEXT.md (location TBD). Verified by V1, V3.
    - R2: Topographic Survey Report shall include survey methodology, control network, coordinate system/datum, site topography, existing features, accuracy statement, certification, and digital survey data in formats compatible with design software. Source: _CONTEXT.md; **ASSUMPTION**: Standard survey deliverables per industry practice. Verified by V1, V2.
    - R3: Utility Locate Report shall document existing utilities (type, location, depth, owner) and identify potential conflicts with proposed design. Source: _CONTEXT.md. Verified by V1, V3.
    - R4: Utility Locate Report shall include investigation methodology (records search, field locating), utility markings/coordinates, conflict assessment, limitations/disclaimers, and utility location plan sheets. Source: **ASSUMPTION**: Standard utility investigation deliverables. Verified by V1, V2.
    - R5: Surveys shall address site boundaries and existing conditions relevant to PKG-02 earthworks scope (grading, excavation, fill, ground improvement areas). Source: decomposition PKG-02 scope (location TBD). Verified by V2.
    - R6: Reports shall include document control fields (title, report number, revision, date, author/organization, approvals) per D&B Contractor standards. Source: **ASSUMPTION**: Standard D&B document control; details **TBD**. Verified by V1.
    - R7: Surveys shall be performed to accuracy standards specified in ER; horizontal and vertical accuracy shall be stated and certified. Source: **TBD**: ER will specify accuracy requirements; **ASSUMPTION**: Typical accuracy for engineering surveys (e.g., ±0.03 ft horizontal, ±0.05 ft vertical). Verified by V1, V3.
    - R8: Surveys shall be performed by licensed professional land surveyor as required by regulatory authority; reports shall include professional seal/certification. Source: **ASSUMPTION**: Professional surveying standards; **TBD**: ER will specify licensing jurisdiction. Verified by V1, V3.
    - R9: Survey coordinate system, datum, and projection shall be consistent with ER project requirements and compatible with design software. Source: **TBD**: ER will specify coordinate system; **ASSUMPTION**: Common system for all disciplines. Verified by V2, V3.
    - R10: Digital survey data shall be provided in formats specified by ER (e.g., AutoCAD DWG, Civil 3D surface, GIS shapefile, LandXML, point cloud). Source: **TBD**: ER will specify formats; **ASSUMPTION**: CAD/BIM compatibility required. Verified by V2.

    ## Related Datasheet Attributes

    - Report date, report number, revision, author/organization in `Datasheet.md` map to R6, R8.
    - Survey format, survey accuracy, coordinate system, survey control network in `Datasheet.md` map to R2, R7, R9, R10.
    - Topographic Survey Report content in `Datasheet.md` maps to R1, R2.
    - Utility Locate Report content in `Datasheet.md` maps to R3, R4.
    - Configuration notes track **TBDs** requiring ER input for R7, R8, R9, R10.

    ## Guidance & Procedure Alignment

    - Guidance principles (`Guidance.md`) describe how survey accuracy, data quality, coordination, and regulatory compliance influence report quality and usability.
    - Procedure steps (`Procedure.md`) describe the process for establishing survey control, performing field surveys, processing data, preparing reports, and verifying accuracy.
    - Verification approach in Procedure ensures requirements R1–R10 are satisfied before report issue.

    ## Standards

    - **TBD**: Applicable surveying standards (e.g., ALTA/NSPS Land Title Survey standards, state/provincial survey standards, ASPRS accuracy standards for aerial/LiDAR surveys) pending ER reference documents.
    - **TBD**: Coordinate system, datum, projection specifications (e.g., State Plane, UTM, local project coordinate system) per ER requirements.
    - **TBD**: Utility investigation standards (e.g., ASCE 38 standard for underground utility investigations, CI/ASCE 38-02 quality levels) pending ER specifications.
    - Employer's Requirements volumes are referenced in decomposition but not provided in _REFERENCES.md (**TBD**).
    - Professional surveying practice standards for report content and certification (**ASSUMPTION**: State/provincial licensing board requirements apply).

    ## Verification

    - V1 (maps to R1, R2, R3, R4, R6, R7, R8): Verify survey reports include all required content sections (methodology, control, coordinate system, topographic data, utility data, accuracy statement, certification) and document control elements per `Datasheet.md` Report Content and Specification requirements. Method: Technical review by qualified surveyor; accuracy checks against field data and control network; checklist against Specification R1–R10. Records: Review comments, accuracy verification calculations, professional seal documentation.
    - V2 (maps to R2, R4, R5, R9, R10): Verify surveys address PKG-02 site areas, digital data formats are compatible with design software, coordinate system is consistent across all survey deliverables, and utility conflicts are identified. Method: Cross-reference with DEL-02.01 (Earthworks Drawings) design limits; test import of survey data into design software; coordinate system consistency check; utility conflict matrix vs. proposed design. Records: Design software import log, coordinate system verification, utility conflict register.
    - V3 (maps to R1, R3, R7, R8, R9): Verify alignment with ER survey requirements (scope, accuracy, coordinate system, deliverable formats, regulatory approvals) once Employer's Requirements volumes are available. Method: ER compliance review against specified survey standards, accuracy tolerances, and approval authority. Records: ER compliance matrix, regulatory approval/certification documentation, Employer review comments and acceptance.

    ## Documentation

    - Controlled Survey Reports deliverable (issued revision).
    - Review comments and response log. ASSUMPTION: standard D&B document control workflow.

    ## References

    - _CONTEXT.md (deliverable identity, description, anticipated artifacts).
    - Decomposition file: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-02 scope, DEL-02 entries; location TBD).
    - `Datasheet.md`, `Guidance.md`, `Procedure.md` (cross-document alignment).
    - _REFERENCES.md indicates no references yet.
