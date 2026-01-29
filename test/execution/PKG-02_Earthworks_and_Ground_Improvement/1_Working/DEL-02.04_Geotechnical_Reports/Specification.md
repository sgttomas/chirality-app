# Specification: DEL-02.04 Geotechnical Reports

    ## Scope

    This deliverable defines the requirements for Geotechnical Reports within PKG-02 Earthworks & Ground Improvement. Source: _CONTEXT.md; decomposition DEL-02 entry (location TBD).

    Package scope context includes Site grading, excavation, filling, ground improvements, geotechnical works, surveys. Source: decomposition PKG-02 scope (location TBD).

    Exclusions: This decomposition covers the Contractor's scope of work only. Employer-responsible items (permits obtained by Employer, nitrogen skid supply) are excluded except for interface connections. Source: decomposition Section 1.2 Scope Focus (location TBD).

    ## Requirements

    - R1: Geotechnical Investigation Report shall document subsurface conditions, laboratory test results, and engineering analysis for design verification and approvals. Source: decomposition DEL-02 entry and _CONTEXT.md (location TBD). Verified by V1, V3.
    - R2: Geotechnical Investigation Report shall include site description, investigation program, subsurface stratigraphy, groundwater conditions, laboratory testing results, and design recommendations for foundations, earthworks, and pavements. Source: _CONTEXT.md; **ASSUMPTION**: standard geotechnical report content per industry practice. Verified by V1, V2.
    - R3: Ground Improvement Design Report (if required) shall document treatment objectives, method selection, design calculations, construction methodology, and performance criteria. Source: _CONTEXT.md; **TBD**: ER will specify if ground improvement is required. Verified by V1, V3.
    - R4: Reports shall address geotechnical aspects of grading, excavation, fill placement, ground improvement scope within PKG-02. Source: decomposition PKG-02 scope (location TBD). Verified by V2.
    - R5: Reports shall include document control fields (title, report number, revision, date, author/organization, approvals) per D&B Contractor standards. Source: **ASSUMPTION**: standard D&B document control; details **TBD**. Verified by V1.
    - R6: Reports shall be prepared by qualified geotechnical engineer(s) and sealed/stamped as required by regulatory authority. Source: **ASSUMPTION**: professional engineering standards; **TBD**: ER will specify licensing requirements. Verified by V1, V3.
    - R7: Reports shall provide geotechnical parameters required for design of structures in PKG-05 (Concrete Structures), PKG-06 (Structural Steelwork), PKG-04 (Pavements). Source: **ASSUMPTION**: cross-package coordination requirement. Verified by V2.
    - R8: Reports shall address excavation stability, dewatering requirements (if applicable), and earthworks compaction criteria. Source: **ASSUMPTION**: standard geotechnical report scope; **TBD**: ER site-specific requirements. Verified by V1, V2.

    ## Related Datasheet Attributes

    - Report date, report number, revision, author/organization in `Datasheet.md` map to R5, R6.
    - Investigation scope, ground improvement approach, report content sections in `Datasheet.md` map to R1, R2, R3, R4, R8.
    - Basis of report attribute ensures R1, R2 foundation data requirements are met.
    - Configuration notes track **TBDs** requiring ER input for R3, R6, R8.

    ## Guidance & Procedure Alignment

    - Guidance principles (`Guidance.md`) describe how technical rigor, regulatory compliance, and cross-package coordination influence report quality and acceptance.
    - Procedure steps (`Procedure.md`) describe the process for commissioning investigations, developing reports, performing technical reviews, and obtaining approvals.
    - Verification approach in Procedure ensures requirements R1–R8 are satisfied before report issue.

    ## Standards

    - **TBD**: Applicable geotechnical standards (e.g., ASTM D1586 for SPT, ASTM D2487 for soil classification, ASTM D698/D1557 for compaction testing) pending ER reference documents.
    - **TBD**: Foundation design codes (e.g., building code, bridge code if applicable) pending ER specifications.
    - **TBD**: Seismic design criteria and geotechnical seismic parameters per ER requirements.
    - Employer's Requirements volumes are referenced in decomposition but not provided in _REFERENCES.md (**TBD**).
    - Professional engineering practice standards for geotechnical reporting (**ASSUMPTION**: ASCE, CGS, or equivalent standards apply).

    ## Verification

    - V1 (maps to R1, R2, R3, R5, R6, R8): Verify geotechnical reports include all required content sections, technical analysis, design recommendations, and document control elements per `Datasheet.md` Report Content and Specification requirements. Method: Technical review by qualified geotechnical engineer; checklist against Specification R1–R8. Records: Review comments, approval signatures.
    - V2 (maps to R4, R7, R8): Verify reports address PKG-02 earthworks scope (grading, excavation, fill, ground improvement) and provide design parameters for coordinating packages (PKG-04, PKG-05, PKG-06). Method: Cross-reference with `Guidance.md` coordination notes and package interface requirements. Records: Coordination meeting minutes, transmittal logs.
    - V3 (maps to R1, R3, R6): Verify alignment with ER geotechnical requirements, regulatory standards, and professional engineering licensing requirements once Employer's Requirements volumes are available. Method: ER compliance review against specified investigation scope, design criteria, and approval authority. Records: ER compliance matrix; regulatory approval documentation.

    ## Documentation

    - Controlled Geotechnical Reports deliverable (issued revision).
    - Review comments and response log. ASSUMPTION: standard D&B document control workflow.

    ## References

    - _CONTEXT.md (deliverable identity, description, anticipated artifacts).
    - Decomposition file: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-02 scope, DEL-02 entries; location TBD).
    - `Datasheet.md`, `Guidance.md`, `Procedure.md` (cross-document alignment).
    - _REFERENCES.md indicates no references yet.
