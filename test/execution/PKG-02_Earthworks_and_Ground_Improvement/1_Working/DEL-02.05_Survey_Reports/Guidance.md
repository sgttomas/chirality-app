# Guidance: DEL-02.05 Survey Reports

## Purpose

Provide guidance that keeps the Survey Reports aligned with PKG-02 earthworks objectives, Specification requirements, and Procedure realization. Source: _CONTEXT.md; decomposition (location TBD).

## Principles

- **Accuracy and Precision**: Survey data must meet specified accuracy tolerances to provide reliable foundation for design; errors in survey data propagate through entire design and construction process. **ASSUMPTION**: Aligns with professional surveying standards and engineering design requirements.
- **Data Quality and Usability**: Survey deliverables must be complete, clearly organized, and in formats compatible with design software to enable efficient design development without data translation errors. Source: **ASSUMPTION**: Standard digital design workflow.
- **Coordination and Consistency**: Coordinate system, datum, and control network must be consistent across all survey deliverables and compatible with design packages to avoid costly coordinate conflicts. Source: **ASSUMPTION**: Cross-package coordination requirement.
- **Regulatory Compliance**: Surveys shall satisfy jurisdictional requirements for professional land surveying practice, including licensing, certification, and professional seal where required. Source: **ASSUMPTION**: Professional surveying standards; **TBD**: ER will specify regulatory authority.
- **Completeness of Existing Conditions**: Thorough documentation of existing site features (topography, structures, utilities, vegetation, boundaries) reduces design risk and construction surprises. Source: **ASSUMPTION**: Standard due diligence for design.
- Interface-only connections to Employer responsibilities ensure the Contractor retains the defined scope. Source: decomposition Section 1.2 Scope Focus (location TBD).
- Align survey scope with PKG-02 earthworks areas and provide existing conditions baseline for all design packages. Source: decomposition PKG-02 scope (location TBD).

## Requirement Traceability

- R1, R2 (Topographic Survey Report): Guidance emphasizes importance of comprehensive existing conditions documentation to support grading design (DEL-02.01), drainage analysis, cut/fill calculations (DEL-02.03), and foundation design in other packages. Survey must capture all features that will influence design decisions.
- R3, R4 (Utility Locate Report): Guidance highlights that incomplete or inaccurate utility information is a leading cause of construction delays and cost overruns; utility conflicts must be identified early in design to allow reroutes or coordination with utility owners.
- R5 (PKG-02 scope coverage): Guidance emphasizes ensuring survey limits extend beyond design limits to provide context and avoid edge-of-survey issues during design development.
- R6 (Document control): Guidance highlights importance of clear revision tracking as survey data may be updated based on additional field work or design feedback.
- R7 (Survey accuracy): Guidance stresses that accuracy requirements should match design needs (e.g., foundation surveys require higher accuracy than general site topography); over-specifying accuracy increases cost without benefit.
- R8 (Professional qualifications): Guidance notes that professional land surveyor involvement ensures survey methodology, equipment calibration, and data processing meet professional standards and regulatory requirements.
- R9 (Coordinate system consistency): Guidance emphasizes early establishment of project coordinate system to avoid costly coordinate transformation errors; all disciplines must use same system.
- R10 (Digital data formats): Guidance highlights importance of compatible file formats to avoid data loss or errors during CAD/BIM import; test data transfer early in process.

## Considerations

- **Survey Control Network**: Establish robust control network (horizontal and vertical control points, benchmarks) early; control density and accuracy determine survey quality. **TBD**: ER may provide existing control monuments or require specific control approach. **ASSUMPTION**: Control network designed per professional surveying standards.
- **Survey Timing and Site Access**: Coordinate survey timing with site access availability, vegetation conditions (leaves-off for better ground visibility), and design schedule needs. Consider phased surveys if entire site not accessible initially. **ASSUMPTION**: Site access coordination with Employer or property owner.
- **Aerial vs. Ground Survey Methods**: Evaluate aerial survey (photogrammetry, LiDAR) vs. conventional ground survey based on site size, vegetation, required accuracy, and cost. Aerial methods efficient for large sites but may require ground survey supplement for utilities and obscured areas. **TBD**: ER may specify survey methods.
- **Utility Investigation Quality Levels**: Different utility investigation methods provide different confidence levels (e.g., ASCE 38 Quality Levels A through D); balance investigation rigor with risk and cost. Records search (low confidence) may suffice for preliminary design; test holes (high confidence) required for final design in critical areas. **TBD**: ER may specify utility investigation quality level.
- **Utility Ownership and Coordination**: Existing utilities may be owned by multiple entities (municipality, utility companies, private); coordination required for verification, relocation approvals, and protection during construction. **TBD**: ER will identify utility owners and coordination requirements.
- Tie Datasheet Attributes to Specification requirements (R1–R10) to ensure report content completeness. **ASSUMPTION**: Cross-document consistency ensures nothing falls through gaps.
- Environmental and regulatory constraints (e.g., surveying in environmentally sensitive areas, survey monumentation requirements) should be captured once references become available. **TBD** pending Employer's Requirements volumes.
- Contractor QA/QC procedures should confirm survey accuracy and data quality per Specification requirements and verification steps in `Procedure.md`. **ASSUMPTION**: Typical surveying QA/QC practice (equipment calibration, field checks, office calculations verification).

## Trade-offs

- **Survey Scope vs. Cost**: Comprehensive survey of entire site provides complete baseline but increases cost; focused survey of key areas reduces cost but may require supplemental surveys later. Guidance: Survey all areas within design limits plus reasonable buffer; prioritize detailed surveys in critical areas (structures, utilities, drainage).
- **Survey Accuracy vs. Cost**: Higher accuracy requires more time, sophisticated equipment, and rigorous field procedures; match accuracy to design needs. Guidance: Use Specification R7 and ER requirements as baseline; higher accuracy for structure locations and benchmarks, standard accuracy for general topography.
- **Survey Schedule vs. Design Schedule**: Early survey provides baseline for design but may not capture site changes; late survey delays design start. Guidance: Perform survey as early as feasible; update as needed if significant site changes occur before construction.
- **Detailed Analysis vs. Schedule**: Extensive utility investigation (test holes, vacuum excavation to verify depths) provides high confidence but takes time; records search and surface locating faster but lower confidence. Guidance: Use Specification requirements (R3, R4) and `Procedure.md` verification approach to balance investigation rigor with schedule and risk; higher rigor for conflict areas.

## Procedure Coordination

- Steps in `Procedure.md` implement the verification expectations outlined above and reference Specification requirements by ID.

## Conflict Table (for human ruling)

- None identified from available sources.

## References

- _CONTEXT.md (deliverable identity, description, anticipated artifacts).
- Decomposition file: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-02 scope, DEL-02 entries; location TBD).
- `Specification.md` and `Procedure.md` for alignment context.
- _REFERENCES.md indicates no references yet.
