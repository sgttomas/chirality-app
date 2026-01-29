# Datasheet: DEL-08.04 Marine Geotechnical Report

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-08.04 |
| Name | Marine Geotechnical Report |
| Package | PKG-08 Marine Structures |
| Discipline | Marine |
| Type | Report |
| Responsible | D&B Contractor |
| Lifecycle (from `_STATUS.md`) | INITIALIZED |

## What This Deliverable Is

**Description (source-anchored):** Documents analysis and results for marine geotechnical report required for design verification and approvals. *(Source: Decomposition line 284 + `_CONTEXT.md`)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

**Minimum anticipated report artifacts (per Decomposition line 284):**
- Marine geotechnical investigation
- Bathymetric survey report

## Report Package Metadata (TBD)

| Attribute | Value |
|---|---|
| Report number / register ID | **TBD** *(pending project document control procedures; likely: RPT-MAR-08-001 for geotechnical, RPT-MAR-08-002 for bathymetry, or combined report)* |
| Revision / issue status format | **TBD** *(typical: Rev 0/1/2 for issued; Rev A/B/C for internal; confirm from project document control procedures)* |
| Investigation/survey contractor | **TBD** *(D&B Contractor may perform in-house or subcontract to specialist geotechnical/survey consultant)* |
| Investigation/survey dates | **TBD** *(field investigation and bathymetric survey dates)* |
| Scope of investigation/survey | **TBD** *(extent, number of borings/soundings, survey area)* |

## Anticipated Report Content

The following content is typical for marine geotechnical investigation and bathymetric survey reports. Specific content is **TBD** pending ER clause extraction and investigation/survey scope definition:

### Marine Geotechnical Investigation Report (Anticipated Content)

| Section | Expected Content | Status |
|---|---|---|
| Executive Summary | Summary of investigation scope, findings, and key recommendations for marine structures design | **TBD** |
| Introduction | Project description, site location, purpose of investigation | **TBD** |
| Site Description | Site location, access, existing conditions, marine environment (tidal range, currents, etc.) | **TBD** *(site visit observations; environmental data from ER or other sources)* |
| Investigation Program | Scope of investigation: number and locations of borings/soundings/samples; boring methods (e.g., marine borings from barge, CPT soundings); field testing (SPT, CPT, etc.); laboratory testing program | **TBD** *(investigation scope per ER requirements or design needs)* |
| Subsurface Conditions | Soil/rock stratigraphy: description of soil/rock layers encountered; depths and thicknesses; groundwater/seawater levels; engineering properties (strength, compressibility, permeability) | **TBD** *(from field logs and lab test results)* |
| Geotechnical Parameters | Design parameters for marine structures: soil unit weights, friction angles, cohesion, undrained shear strength, consolidation properties; parameters for pile capacity analysis | **TBD** *(interpreted from field/lab data; correlated to soil types)* |
| Pile Capacity Analysis | Axial pile capacity (compression and tension) for various pile types/sizes; lateral pile capacity; pile group effects; scour considerations; recommended pile penetration depths | **TBD** *(analysis per API RP 2A, CFEM, or other applicable codes; input to DEL-08.03 calculations)* |
| Scour Assessment | Scour potential and estimated scour depths; effect on pile capacity and structural design; scour mitigation measures (if required) | **TBD** *(scour analysis per marine engineering practice; depends on current/wave/vessel wash conditions)* |
| Construction Considerations | Drivability assessment (pile driving feasibility, potential obstructions); dewatering/excavation (if required); construction risks and mitigation | **TBD** *(practical construction guidance for contractor)* |
| Seismic Considerations | Site seismicity; seismic design parameters (if required by ER or code); liquefaction potential (if applicable) | **TBD** *(seismic hazard per NBCC or ER; liquefaction screening if cohesionless soils present)* |
| Conclusions and Recommendations | Summary of key findings; recommendations for foundation design (pile types, sizes, penetrations); construction recommendations; limitations of investigation | **TBD** |
| References | Standards, codes, and references cited in report | **TBD** |
| Appendices | Boring logs; laboratory test results; field test data; calculations; site photos; other supporting data | **TBD** |

### Bathymetric Survey Report (Anticipated Content)

| Section | Expected Content | Status |
|---|---|---|
| Executive Summary | Summary of survey scope, methods, and key findings | **TBD** |
| Introduction | Project description, survey purpose, survey area and extent | **TBD** |
| Survey Methods and Equipment | Survey methods (e.g., multibeam sonar, single-beam sonar, total station for nearshore); equipment specifications and calibration; positioning system (GPS/GNSS); datum and coordinate system used | **TBD** *(survey methods per ER requirements or industry practice)* |
| Survey Execution | Survey dates; environmental conditions during survey (weather, sea state, tides); survey crew and vessel (if applicable); quality control procedures | **TBD** |
| Survey Results | Bathymetric data: seabed elevations/depths; contour maps; cross-sections; existing seabed features (obstructions, debris, slopes); comparison to existing charts (if available) | **TBD** *(survey deliverables: contour map, point cloud data, sections)* |
| Datum and Coordinates | Vertical datum used (e.g., Chart Datum, Geodetic Datum); horizontal coordinate system (e.g., UTM, local grid); datum transformations (if applicable) | **TBD** *(critical for marine structures design; must be consistent with structural design datum)* |
| Accuracy and Quality Control | Survey accuracy assessment; quality control checks performed; comparison to checkpoints or previous surveys; uncertainty estimates | **TBD** *(accuracy per survey standards; typically ±0.1m or better for structural design)* |
| Conclusions and Recommendations | Summary of bathymetric findings; recommendations for design (seabed levels, slopes, obstructions); limitations of survey | **TBD** |
| References | Survey standards and references cited | **TBD** |
| Appendices | Bathymetric maps and contour plans; survey data files; calibration certificates; photos; other supporting data | **TBD** |

## Design Inputs and Basis (Not Yet Captured)

The report content depends on investigation/survey inputs and requirements not yet extracted into this deliverable folder:

- **ER clauses for geotechnical investigation and bathymetric survey requirements:** **TBD** *(ER Vol 2 Parts 1-2 present as PDFs; clause extraction pending; ER may specify investigation scope, boring depths, testing requirements, survey accuracy)*
- **Investigation/survey scope requirements:** **TBD** *(number and locations of borings/soundings; survey extent; ER or design-driven scope)*
- **Marine structures design needs:** **TBD** *(pile types/sizes being considered; loading conditions; required geotechnical parameters for design from DEL-08.03)*
- **Site-specific environmental data:** **TBD** *(tidal range, currents, wave climate, vessel traffic; for scour assessment and construction planning)*
- **Applicable codes and standards:** **TBD** *(likely: API RP 2A for pile capacity analysis; Canadian Foundation Engineering Manual (CFEM); survey standards (e.g., IHO S-44 for hydrographic surveys); confirm from ER)*
- **Quality assurance/quality control (QA/QC) requirements:** **TBD** *(ER or project QA plan may specify QA/QC procedures for investigation/survey; independent review requirements)*

## Interfaces (Advisory)

Dependencies are coordinated externally per `_DEPENDENCIES.md` (mode: NOT_TRACKED). The following interfaces are anticipated based on decomposition scope and should be confirmed via design coordination:

### Interface to DEL-08.03 Marine Structures Design Calculations
- Geotechnical report provides soil parameters and pile capacity recommendations used in DEL-08.03 structural calculations — **TBD**
- **Coordination required:** Geotechnical parameters and pile capacity from DEL-08.04 must be suitable for DEL-08.03 calculation methods; iterative coordination if pile sizes/types change during design

### Interface to DEL-08.01 Marine Structures Design Drawing Set
- Bathymetric survey provides seabed levels and elevations used in DEL-08.01 drawings (piling layout, sections) — **TBD**
- Geotechnical report provides pile penetration depths that affect drawing details — **TBD**
- **Coordination required:** Datum used in bathymetric survey must match datum used in structural drawings; coordinate system consistency

### Interface to DEL-08.02 Marine Structures Technical Specification
- Geotechnical report construction considerations may inform piling specification (drivability, installation procedures) — **TBD**

### Interface to Construction Planning
- Geotechnical report construction considerations inform contractor's construction methodology and sequencing — **TBD**
- Bathymetric survey identifies seabed obstructions/constraints affecting construction access and pile installation — **TBD**

## Cross-Document Links

- **Requirements basis:** `Specification.md` (R-001 through R-005) defines what must be included in the geotechnical/bathymetric report package and verification criteria
- **Production workflow:** `Procedure.md` provides step-by-step process to produce the report, aligned to Specification requirements
- **Engineering considerations:** `Guidance.md` provides rationale for each Specification requirement and guidance on report content

## Key TBDs (Next Closure Items)

Priority items to resolve before geotechnical investigation and bathymetric survey can be scoped and executed:

1. **ER clause extraction for geotechnical/bathymetric scope and requirements** (supports `Specification.md` R-004): **TBD**
2. **Investigation/survey scope definition** (number of borings, survey extent, testing program) (supports `Specification.md` R-001): **TBD**
3. **Design needs and required geotechnical parameters** (from DEL-08.03; defines what parameters investigation must provide) (supports `Specification.md` R-002): **TBD**
4. **Datum and coordinate system** (for bathymetric survey and design integration) (supports interface to DEL-08.01): **TBD**
5. **QA/QC requirements and acceptance criteria** (for investigation/survey data quality and report approval) (supports `Specification.md` R-003, R-004): **TBD**

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.04_Marine_Geotechnical_Report/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.04 at line 284)
- `test/execution/PKG-08_Marine_Structures/0_References/_REFERENCE_INDEX.md` *(stub; references not yet populated)*
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
