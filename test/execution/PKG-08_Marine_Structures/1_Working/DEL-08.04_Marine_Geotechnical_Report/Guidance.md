# Guidance: DEL-08.04 Marine Geotechnical Report

## Purpose

This document provides **engineering rationale and decision-making guidance** to support production of a Marine Geotechnical Report package that is complete, traceable, technically sound, and suitable for design verification and regulatory approvals.

**Deliverable intent (source-anchored):** Documents analysis and results for marine geotechnical report required for design verification and approvals. *(Source: Decomposition line 284 + `_CONTEXT.md`)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Principles (Engineering Intent, Non-Invented)

### Trace Data from Source to Design Conclusion
- **Intent:** Every geotechnical parameter and design recommendation must be traceable back to field/lab data or stated assumptions
- **Rationale:** Designers need confidence in geotechnical parameters; approvals require data substantiation; litigation risk if data/interpretations cannot be defended
- **Practice:** Reference specific boring numbers, depths, test results; show calculation methods for interpreted parameters; distinguish measured data from interpreted/correlated values

### Explicit Assumptions and Limitations
- **Intent:** State all assumptions about stratigraphy, groundwater, parameter selection, scour; clearly state investigation/survey limitations
- **Rationale:** Geotechnical investigations are site-specific and limited in extent; extrapolation between borings involves uncertainty; assumptions may need updating when design progresses or additional data obtained
- **Practice:** Label assumptions explicitly; discuss spatial variability and data gaps; state applicability limits (e.g., "recommendations apply to pile locations within surveyed area; additional investigation required if piles move outside this area")

### Design-Relevant Deliverables
- **Intent:** Report provides parameters and recommendations in a form directly usable for structural design
- **Rationale:** Geotechnical report is critical input to DEL-08.03 calculations; designers should not need to re-interpret raw data
- **Practice:** Provide design parameters in tables ready for use in calculations; provide pile capacity charts/tables for range of pile types/sizes; cross-reference to structural design codes (e.g., API RP 2A methods)

---

## Requirement Rationale Map

### R-001: Report Package Coverage (Minimum)

**What it requires:**
- Marine geotechnical investigation report and bathymetric survey report

**Rationale:**
- Decomposition specifies both investigation and bathymetry as required outputs (line 284)
- Geotechnical investigation provides subsurface conditions and pile capacity for structural design
- Bathymetric survey provides seabed elevations for design layout and pile penetration calculations
- Both are typically required for marine structures approvals

**Key Considerations:**
- **Combined vs separate reports:** Can geotechnical investigation and bathymetry be combined in one report? *(Typical: separate reports by specialist consultants; can be combined if same party performs both; ensure cross-references if separate)*
- **Report scope alignment:** Does investigation scope cover all pile locations? Does survey extend beyond pile footprint to show seabed context? *(Coordinate investigation/survey extents with preliminary design layout from DEL-08.01)*

**Sources:**
- Decomposition line 284 (anticipated artifacts)

---

### R-002: Traceable Data, Methods, and Assumptions

**What it requires:**
- Data traceability (investigation/survey scope, field/lab data, data custody)
- Methods documentation (investigation/survey/analysis methods)
- Assumptions and limitations explicitly labeled

**Rationale:**
- Data traceability enables verification, QA/QC audit, and design confidence
- Methods documentation enables independent review and demonstrates code compliance
- Assumptions/limitations manage expectations and enable design risk assessment

**Key Considerations:**
- **Data management:** How to organize field/lab/survey data for traceability? *(Recommend: appendices with boring logs, lab test summaries, survey data; cross-reference data in report body; maintain electronic data files with chain of custody)*
- **Soil parameter interpretation:** How to select design parameters when data shows variability? *(Conservative values for critical elements; representative/average values for less critical; discuss variability and sensitivity in report; consider characteristic values per code (e.g., cautious estimate per Eurocode) or LRFD approach)*
- **Scour assessment:** How to estimate scour depth when limited site-specific data? *(Use marine engineering scour equations (e.g., HEC-18, PIANC); consider vessel wash, current, wave action; conservative assumptions for design life; monitor during construction/operation if significant uncertainty)*

**Sources:**
- Standard geotechnical/survey reporting practice
- Project-specific requirements TBD from ER

---

### R-003: QA/QC and Review

**What it requires:**
- Field/lab/survey QA/QC procedures and documentation
- Technical review and sign-off
- Independent check (if required); professional seal (if required)

**Rationale:**
- QA/QC ensures data quality and reduces errors; required for approvals
- Technical review catches errors/omissions before issue; professional liability protection
- Professional seal (P.Eng./P.Geo.) is legal requirement for geotechnical work in BC; provides professional accountability

**Key Considerations:**
- **Laboratory accreditation:** Is laboratory accredited (e.g., CALA, A2LA)? *(Recommend: use accredited lab for approvals and design work; accreditation demonstrates competence and QA/QC)*
- **Survey accuracy requirements:** What accuracy is required for bathymetric survey? *(Typical: ±0.1m for structural design; confirm from ER or structural design needs; accuracy affects survey methods and cost)*
- **Professional seal requirement:** Is P.Eng. or P.Geo. seal required? *(Likely yes for geotechnical work in BC; confirm from ER or BC regulations (Professional Governance Act); geotechnical work may require P.Geo. (geoscience) rather than P.Eng. (engineering) depending on work scope)*

**Sources:**
- Standard geotechnical/survey practice
- Professional licensing requirements in BC (Engineers and Geoscientists BC)
- Project-specific requirements TBD from ER and QA plan

---

### R-004: ER Alignment and Approval Requirements

**What it requires:**
- Compliance with ER requirements and codes/standards
- Report suitable for Employer approval and regulatory submission

**Rationale:**
- ER defines contractual requirements; non-compliance causes rework and delays
- Regulatory approvals may require specific investigation scope, data, or certifications
- Report must provide all information required for approvals without follow-up requests

**Key Considerations:**
- **ER investigation scope:** Does ER specify minimum investigation scope (e.g., number of borings per structure, minimum boring depth)? *(TBD from ER clause extraction; ER may have prescriptive requirements)*
- **Regulatory approvals:** What regulatory approvals are required (e.g., Transport Canada, Canadian Coast Guard, local municipality)? *(TBD from ER; regulatory authority may have specific requirements for marine structures geotechnical/bathymetric work)*
- **Environmental considerations:** Are there environmental constraints on investigation/survey (e.g., fish windows, marine mammal protection, contaminated sediments)? *(TBD from ER environmental requirements; may affect investigation methods and timing)*

**Sources:**
- Decomposition line 284 ("required for design verification and approvals")
- ER requirements TBD from ER Vol 2 Parts 1-2

---

### R-005: Document Control and Packaging

**What it requires:**
- Report numbering, revision control, format compliance

**Rationale:**
- Document control enables version control and tracking
- Standard format improves usability and professionalism
- Approvals require controlled documents with clear revision status

**Key Considerations:**
- **Report format standards:** Does project or ER have report template or format requirements? *(TBD from ER or project procedures; geotechnical consultants may have own report format; ensure meets project requirements)*
- **Revision management:** How to revise report when additional investigation data obtained or design changes? *(Use revision numbers per project document control; revision table on cover page; highlight changes in revised sections; supersede previous revisions)*

**Sources:**
- Standard report practice
- Project-specific requirements TBD from ER and project document control procedures

---

## Report Content Guidance

### Geotechnical Investigation Report - Key Content

**Executive Summary:**
- Briefly summarize site conditions, key findings, and design recommendations in 1-2 pages for non-technical readers

**Subsurface Conditions:**
- Describe soil/rock stratigraphy clearly with engineering properties
- Use consistent terminology for soil layers (e.g., "Marine Clay" vs "Silty Clay" - be specific)
- Provide engineering properties in tables: unit weight, friction angle, cohesion, SPT N-value, CPT parameters, etc.
- Discuss spatial variability if significant

**Pile Capacity Analysis:**
- Provide capacity for range of pile types/sizes relevant to design (e.g., steel pipe piles, H-piles; various diameters and embedment depths)
- Show calculation methods (API RP 2A, CFEM, or equivalent)
- Provide capacity charts or tables for easy design reference
- State design approach (allowable stress vs LRFD; factors of safety or resistance factors used)
- Discuss axial capacity (compression and tension) and lateral capacity separately

**Scour Assessment:**
- Assess scour potential based on site conditions (current, waves, vessel wash)
- Estimate scour depth with method and assumptions stated
- Discuss effect of scour on pile capacity (reduced embedment) and structural design
- Recommend scour monitoring or mitigation if significant uncertainty

**Construction Considerations:**
- Discuss pile drivability (expected driving resistance, potential refusal on obstructions, soil setup/relaxation)
- Recommend pile installation procedures if non-standard conditions
- Identify construction risks (e.g., obstructions, hard driving, noise/vibration constraints)

### Bathymetric Survey Report - Key Content

**Survey Methods:**
- Describe survey equipment, calibration, and accuracy
- State positioning method (GPS/GNSS) and accuracy
- State datum and coordinate system used (critical for design integration)

**Survey Results:**
- Provide contour map of surveyed area at appropriate contour interval (e.g., 0.5m or 1m)
- Provide cross-sections along key lines (e.g., along trestle alignment)
- Identify seabed features (slopes, obstructions, debris, existing structures)
- Provide seabed elevations at proposed pile locations (or state that final pile locations TBD)

**Datum and Coordinates:**
- Clearly state vertical datum (Chart Datum, Geodetic Datum, etc.) and relationship to other datums if applicable
- Clearly state horizontal coordinate system and datum
- **Critical:** Datum must be coordinated with structural design datum (DEL-08.01); if different datums used, provide transformation parameters

---

## Trade-offs and Decisions

### Investigation Extent vs Cost and Schedule

**Trade-off:** More investigation (more borings, deeper borings, more testing) provides better subsurface characterization but increases cost and schedule; limited investigation reduces cost but increases design uncertainty.

**Considerations:**
- ER may specify minimum investigation scope (number of borings, depths); if not, balance data needs vs cost
- Critical areas (e.g., piles supporting heavy loads, areas with suspected poor soils) may warrant more investigation
- Phased approach: preliminary investigation for early design; supplemental investigation if design changes or critical areas identified

**Decision:** **TBD** *(Recommend: meet ER minimum requirements; additional investigation at critical locations; coordinate investigation scope with preliminary design from DEL-08.01 to optimize boring locations)*

### Conservative vs Representative Parameters

**Trade-off:** Conservative geotechnical parameters (low strength, high loads) provide safety margin but may result in uneconomical pile design; representative (average) parameters reduce conservatism but require higher confidence in data.

**Considerations:**
- Design codes (API RP 2A, CFEM) may specify parameter selection approach (e.g., characteristic values, lower bound, average)
- Limited data may warrant conservative parameters to account for uncertainty
- Sensitivity analysis: if pile design highly sensitive to geotechnical parameters, conservative approach or additional investigation may be warranted

**Decision:** **TBD** *(Recommend: follow code requirements for parameter selection; use conservative parameters for critical elements or when data limited; discuss parameter uncertainty and sensitivity in report; consider parametric design approach showing pile capacity for range of parameters)*

---

## Conflict Table (for human ruling)

No conflicts identified from sources currently present in this deliverable folder.

If conflicts arise during report development (e.g., contradictory ER requirements, conflicting test data), document them here for human ruling:

| Conflict ID | Conflict (short statement) | Source A (file + section) | Source B (file + section) | Impacted sections | Proposed authority (PROPOSAL) | Human ruling (TBD) |
|---|---|---|---|---|---|---|
| *(none)* | - | - | - | - | - | - |

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.04_Marine_Geotechnical_Report/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.04 at line 284)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard geotechnical and survey reporting practice (for data documentation, parameter selection, QA/QC, professional seal requirements)
