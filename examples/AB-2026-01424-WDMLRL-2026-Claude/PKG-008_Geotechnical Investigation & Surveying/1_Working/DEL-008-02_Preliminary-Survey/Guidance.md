# Guidance — DEL-008-02 Preliminary Site Survey

---

## Purpose

The Preliminary Site Survey (DEL-008-02) establishes the foundational spatial dataset for the entire WDMLRL Maintenance Shop Addition project. It is the first field-based activity to produce measured, georeferenced data about the project area, and its outputs are consumed by every downstream design and construction activity.

Without reliable baseline topography, control points, boundary data, and existing conditions documentation, the design disciplines (civil grading, structural foundation, site servicing) cannot produce coordinated, constructible designs. Errors or gaps introduced at this stage propagate forward through the project.

Source: Decomposition OBJ-003, SOW-0002; _CONTEXT.md description; _DEPENDENCIES.md downstream list.

---

## Principles

### 1. Survey First, Design After
The preliminary survey should be completed and accepted before the detailed design phases proceed to avoid rework caused by conflicting or missing spatial data. The survey establishes the datum and coordinate system reference that all design drawings must share.

**Schedule risk foresight:** If the preliminary survey is delayed past the point at which design disciplines need to begin work, the project risks compressing the design-construction sequence against the December 31, 2026 hard deadline (RFP §3.1). In a delay scenario, the project team should identify the **minimum survey dataset** that would allow design to proceed in parallel — for example, preliminary control point coordinates and a rough topographic surface — while the full survey deliverable is completed. This contingency approach introduces coordination risk and should be treated as an exception, not normal practice. (Ref: Lensing E-001 — foresight guidance for delay scenario)

Source: ASSUMPTION — inferred from standard design-build practice and the downstream dependency chain (_DEPENDENCIES.md: PKG-002 Foundation Design, PKG-003+ all design packages require survey data).

### 2. Control Points Are a Long-Duration Asset
The control points established by this survey will be used throughout the project lifecycle — for construction layout (DEL-008-03) and for as-built verification (DEL-008-04). Control points should be:
- Located to survive construction activity (ASSUMPTION: outside immediate construction footprint where possible)
- Documented with sufficient redundancy to allow re-establishment if disturbed
- Referenced to a coordinated datum consistent with the design drawings

**Long-term preservation:** For a County-owned facility, the long-term value of a permanent control network may extend beyond this project. The project team should consider whether control points should be registered with a provincial survey control database or shared with Camrose County for future facility maintenance, expansion, or survey work. TBD — confirm with Owner whether post-project preservation or registration is desired. (Ref: Lensing E-003 — long-term control point preservation strategy)

Source: _DEPENDENCIES.md (DEL-008-03 uses control points from preliminary survey); _CONTEXT.md scope.

### 3. Coordinate Early with the Geotechnical Investigator
DEL-008-01 (Geotechnical Investigation) runs concurrently with DEL-008-02. Sharing control point data, site access arrangements, and field schedules between the Surveyor and the Geotechnical Engineer reduces redundant site mobilizations and ensures borehole locations are referenced in the same coordinate system used by the design team.

Source: _REFERENCES.md (DEL-008-01 described as complementary site investigation); Decomposition PKG-008 package scope.

### 4. Confirm Datum and Coordinate System Before Fieldwork
Once chosen and approved, the horizontal datum, vertical datum, and coordinate system must not change. Mid-project changes to the spatial reference system require transforming all previously produced data and drawings — a costly correction that can affect permitting, design, and construction.

Source: ASSUMPTION — standard surveying practice. Datum choice not specified in RFP.

### 5. Align Survey Coverage with Grading Design Needs
The RFP requires a site grading plan with drainage features (RFP §3.3.2, §3.4). The topographic survey coverage should extend beyond the immediate building footprint to capture sufficient context for the grading design — including offsite drainage patterns and neighboring conditions, since the grading design must not alter drainage conditions of neighboring properties (RFP §3.4).

Source: RFP §3.3.2 (grading plan required), §3.4 (grading design shall not alter drainage conditions of neighboring properties).

### 6. Prioritize Survey Scope Elements Under Constraint
If the survey schedule is compressed or resources are limited, the following priority ranking provides a basis for resource allocation decisions (Ref: Lensing A-005 — priority ranking for scope elements):

| Priority | Scope Element | Rationale |
|---|---|---|
| 1 | Control point network | All other survey data and all downstream work depend on the control network. Without it, no other survey data can be reliably georeferenced. |
| 2 | Topographic survey | Required for grading design (RFP §3.4), which is on the critical path to construction. |
| 3 | Existing conditions documentation | Required for design coordination; less time-sensitive than topography if partial data can support initial design. |
| 4 | Boundary survey | May require ALS involvement (longer lead time); less likely to be on the critical design path unless permitting requires it. TBD — confirm with Owner whether boundary work is time-critical. |

**ASSUMPTION (best-effort ranking):** This priority ranking is inferred from the downstream dependency structure and is not stated in any source document. The Project Manager and Surveyor should confirm or adjust this ranking during survey plan development.

---

## Considerations

### Site Context
- The site is an active regional landfill facility (WDMLRL). Site access for field survey crews must be coordinated with facility operations. Personal protective equipment and site safety protocols applicable to landfill environments should be observed. (Source: ASSUMPTION — RFP §3.2 references mandatory site meeting at the facility; site is an active landfill.)
- The expansion area is immediately east of the existing maintenance shop building (Appendix C aerial). The existing building and associated infrastructure will be present during the survey and must be documented.
- Camrose County is performing brushing/clearing and bulk cut and fill in the project area (RFP §3.3.1). Timing of County work relative to the survey should be confirmed; surveying after major clearing reduces obstructions but surveying before earthworks captures original conditions.

### Regulatory / Professional
- Boundary survey work in Alberta requires involvement of an Alberta Land Surveyor (ALS) licensed under the Alberta Land Surveyors Act (RSA 2000, c. A-31.5). The extent of boundary work required should be clarified with the Owner at survey plan stage. (Source: ASSUMPTION — applicable Alberta legislation; not cited in RFP.)
- All survey data and drawings should be stamped/certified as appropriate for the work performed. The broader project requirement for P.Eng. stamps on IFC drawings (RFP §3.3.2) does not apply to survey products, but the Surveyor's professional obligations apply.
- Existing survey monuments encountered during fieldwork are protected under the Alberta Surveys Act (RSA 2000, c. S-26). The Surveyor must identify, protect, and document any existing monuments (see R-013). (Ref: Lensing C-002)

### Seasonal / Weather
- The project is located in central Alberta. Field survey activities planned for early spring may encounter frozen ground, snow cover, or wet conditions that affect productivity and instrument performance. (Source: ASSUMPTION — _DEPENDENCIES.md identifies weather conditions as an external dependency.)
- Early completion of the preliminary survey is strongly preferable to allow design disciplines maximum time before the December 31, 2026 project deadline.

### Downstream Data Integration
- Digital survey data should be delivered in formats compatible with the civil/structural design software used by the design team. Format should be confirmed with the Prime Consultant before data delivery (see R-008). (Source: ASSUMPTION.)
- The coordinate system and elevation datum used in the survey must match what the design team uses in their CAD/BIM environment. This should be agreed upon before fieldwork.

### Data Backup and Security During Field Operations
Field survey data (raw observations, GPS/GNSS logs, field notes) represent irreplaceable evidence. Loss of raw field data before backup would require remobilization. The Surveyor should implement data protection protocols during the field campaign, including (Ref: Lensing X-001):
- Daily backup of raw field data to a separate storage device or secure cloud location
- Secure storage of digital field files (protection from weather, equipment failure, theft)
- Confirmation of data integrity before demobilizing from the site

Source: ASSUMPTION — standard survey field practice. No specific data security requirements in RFP.

### Budget / Cost Considerations
Survey scope decisions have cost implications that should be considered alongside technical factors (Ref: Lensing C-003):
- **Legal boundary survey vs. approximate boundary:** A full legal boundary survey (ALS required) carries higher professional fees and longer timelines than an approximate boundary delineation from title/maps. The cost-benefit assessment depends on whether permitting or design requires a legal survey.
- **Extended survey coverage:** Broader topographic coverage to support grading design (Principle 5) increases field time and data processing but reduces the risk of return visits for supplementary data.
- **Control point monumentation:** Permanent monuments (rebar, iron pipe) cost more to install but save cost if they avoid the need for re-establishment during construction.

TBD — Budget/cost decisions to be made by the Project Manager in consultation with the Surveyor during survey plan development.

---

## Trade-offs

| Trade-off | Options | Consideration |
|---|---|---|
| Survey timing vs. County earthworks | Survey before clearing: captures original ground but may have obstructions. Survey after clearing: easier fieldwork but original conditions may be lost. | Confirm sequence with County project manager. Early survey of undisturbed ground is generally preferable for establishing existing conditions baseline. **Decision mechanism:** Request written confirmation from County project manager on earthworks schedule before finalizing survey plan (Ref: Lensing B-004). |
| Legal boundary survey vs. approximate boundary delineation | Full legal survey (ALS required, higher cost, longer timeline) vs. approximate boundary from title/maps for design purposes. | Confirm with Owner whether legal boundary survey is required for permitting or design purposes. |
| Control point monumentation type | Permanent monuments (rebar, iron pipe) survive construction but may be disturbed. Temporary hubs are less durable but cheaper. | Install permanent or semi-permanent reference marks outside the construction zone, with tied temporary marks within it. |
| Survey coverage extent | Minimum: building footprint and immediate site only. Extended: broader site context for grading design. | Extended coverage is recommended to support the grading design's off-site drainage considerations (RFP §3.4). |

---

## Examples

TBD — No project-specific survey examples are available in the accessible sources. The Surveyor's similar-project references submitted with the proposal (RFP §4.6.3) may provide applicable precedents.

---

## Rationale for R-009 (Owner Approval of Survey Plan)

R-009 requires the survey plan to be submitted to Camrose County for review and approval before fieldwork. This approval gate exists because (Ref: Lensing F-002):

1. **Datum and accuracy decisions are irreversible once fieldwork begins.** If the chosen datum, coordinate system, or accuracy class does not meet the Owner's expectations or design team requirements, data collected under incorrect assumptions may need to be re-collected.
2. **The Owner bears project risk.** Under the CCDC 14–2013 contract form, the Owner retains responsibility for overall project completion. The survey plan approval gives the Owner visibility into the spatial reference framework that will govern all subsequent design and construction.
3. **Multiple TBDs require Owner input.** Several mandatory parameters (datum, accuracy class, mapping scale, boundary scope) are TBD and require Owner confirmation. The survey plan approval is the natural decision gate for resolving these TBDs.

Source: ASSUMPTION — rationale inferred from project governance structure and the number of TBD items requiring Owner input. No explicit source requires this approval, but it is consistent with the Owner approval pattern throughout the RFP (§3.3.2, §4.7.4).

---

## Conflict Table (for human ruling)

No conflicts identified at Pass 1+2+3. If conflicts are identified during design development, this table will be populated.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| — | No conflicts identified | — | — | — | — | TBD |

---

## Pass 3 Enrichment Log

The following semantic lensing items were incorporated into this document during Pass 3:

| Lensing Item | Action Taken |
|---|---|
| A-005 | Added Principle 6: explicit priority ranking for survey scope elements under constraint |
| B-004 | Added decision mechanism to survey timing vs. County earthworks trade-off |
| C-003 | Added Budget / Cost Considerations subsection under Considerations |
| E-001 | Added schedule risk foresight paragraph to Principle 1 (delay scenario and minimum data contingency) |
| E-003 | Added long-term control point preservation consideration to Principle 2 |
| F-002 | Added Rationale for R-009 section explaining why Owner approval gate matters |
| X-001 | Added Data Backup and Security During Field Operations subsection under Considerations |
| X-004 | Terminology normalized: "control points" used consistently throughout |
| E-002 | Standardized regulatory citations to formal format (RSA 2000, c. A-31.5; RSA 2000, c. S-26) |
