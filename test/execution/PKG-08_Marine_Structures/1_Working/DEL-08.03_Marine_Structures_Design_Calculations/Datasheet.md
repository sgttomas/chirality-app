# Datasheet: DEL-08.03 Marine Structures Design Calculations

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-08.03 |
| Name | Marine Structures Design Calculations |
| Package | PKG-08 Marine Structures |
| Discipline | Marine |
| Type | Calculation |
| Responsible | D&B Contractor |
| Lifecycle (from `_STATUS.md`) | INITIALIZED |

## What This Deliverable Is

**Description (source-anchored):** Provides the engineering basis and sizing/verification calculations for marine structures. *(Source: Decomposition line 283 + `_CONTEXT.md`)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

**Minimum anticipated calculation artifacts (per Decomposition line 283):**
- Pile capacity calculations
- Trestle structural calculations
- Mooring analysis

## Calculation Package Metadata (TBD)

| Attribute | Value |
|---|---|
| Calculation package number / register ID | **TBD** *(pending project document control procedures; likely: CALC-MAR-08-001 or similar)* |
| Revision / issue status format | **TBD** *(typical: Rev 0/1/2 for issued; Rev A/B/C for internal; confirm from project document control procedures)* |
| Calculation tools/software used | **TBD** *(likely: hand calculations + spreadsheets for simple elements; structural analysis software (e.g., SAP2000, STAAD.Pro, RISA) for complex frames; geotechnical software for pile capacity; specify versions)* |
| Calculation methods/standards referenced | **TBD** *(pending ER clause extraction; likely: CSA S6, CSA S16, API RP 2A for marine structures design; geotechnical standards for piles)* |
| Load cases / combinations | **TBD** *(pending design basis; likely: dead load, live load, vessel berthing, mooring, wind, current, wave, seismic per ER and codes)* |
| Professional stamp/seal requirements | **TBD** *(likely: Professional Engineer (P.Eng.) stamp required for structural calculations in British Columbia; confirm from ER or regulatory requirements)* |

## Anticipated Calculation Content Scope

The following calculation types are expected based on PKG-08 scope and decomposition anticipated artifacts. Specific content is **TBD** pending ER clause extraction, design basis inputs, and design development:

### Pile Capacity Calculations (Anticipated Content)

| Calculation Topic | Expected Content | Status |
|---|---|---|
| Geotechnical pile capacity | Axial capacity (compression and tension) based on soil parameters from DEL-08.04; pile type, size, embedment depth; calculation method per code (e.g., API RP 2A, Canadian Foundation Engineering Manual) | **TBD** *(requires DEL-08.04 Marine Geotechnical Report)* |
| Structural pile capacity | Structural capacity of pile (axial, bending, shear, combined loading); pile material properties; buckling check for unsupported lengths; structural design per CSA S6 or CSA S16 | **TBD** *(requires pile material grade and geometry; load cases from design basis)* |
| Lateral pile capacity | Lateral load capacity and deflection; p-y curve method or equivalent; soil-pile interaction | **TBD** *(requires DEL-08.04 geotechnical parameters; lateral loads from berthing/mooring analysis)* |
| Pile group effects | Group efficiency factors if piles are closely spaced; load distribution in pile groups | **TBD** *(requires final pile layout from DEL-08.01; geotechnical recommendations from DEL-08.04)* |
| Scour and erosion considerations | Scour depth assessment; effect on pile embedment and capacity | **TBD** *(requires marine environment data; scour assessment methodology per ER or marine codes)* |

### Trestle Structural Calculations (Anticipated Content)

| Calculation Topic | Expected Content | Status |
|---|---|---|
| Load analysis | Dead loads (self-weight of structure, decking, equipment); live loads (personnel, maintenance equipment, snow if applicable); environmental loads (wind, current if applicable); load combinations per CSA S6 or ER | **TBD** *(requires design basis; equipment loads; load factors and combinations per code/ER)* |
| Member sizing and design | Beam, column, brace design for trestle framing; material selection (steel grades); section properties; unity checks for axial, bending, shear, combined loading per CSA S16 or CSA S6 | **TBD** *(requires load analysis; preliminary layout from DEL-08.01; design criteria per ER)* |
| Connection design | Bolted and/or welded connection design; connection capacity for shear, tension, moment; bolt grades, weld sizes per CSA S16 or CSA S6 | **TBD** *(requires member forces from structural analysis; connection detailing from DEL-08.01)* |
| Deflection and serviceability checks | Deflection limits per code or ER; vibration considerations if applicable; serviceability criteria | **TBD** *(requires serviceability criteria from ER; load cases for serviceability limit states)* |
| Stability checks | Overall trestle stability (overturning, sliding); lateral bracing requirements; buckling checks for compression members | **TBD** *(requires foundation reactions; lateral load resistance; stability criteria per code)* |

### Mooring Analysis (Anticipated Content)

| Calculation Topic | Expected Content | Status |
|---|---|---|
| Vessel characteristics and assumptions | Design vessel dimensions, displacement, draft; mooring arrangement (line locations, angles); vessel type and class | **TBD** *(requires design vessel definition from ER or project basis; may reference DEL-08.09 Mooring Analysis Report if more detailed)* |
| Environmental loads on moored vessel | Wind loads on vessel; current loads on vessel; wave loads on vessel (if applicable); load calculation methods per OCIMF Mooring Equipment Guidelines or equivalent | **TBD** *(requires marine environment data; calculation methods per ER or industry standards)* |
| Mooring line loads | Mooring line tensions under environmental loading; line arrangement and angles; line material properties (MBL, elasticity); load sharing among mooring lines | **TBD** *(requires mooring arrangement; environmental loads; mooring line capacity; may be covered in DEL-08.09 Mooring Analysis Report)* |
| Berthing loads (if applicable) | Berthing energy and impact loads on fender system and structure; vessel approach velocity and angle; fender reaction forces; berthing energy calculation per PIANC or equivalent | **TBD** *(may be covered in DEL-08.06 Berthing Energy Calculation Report; check scope overlap)* |
| Structure loads from mooring/berthing | Loads transferred from mooring bollards and fenders to marine structure (platform, trestle); load path and distribution; bollard pull-out loads; fender reaction loads on structure | **TBD** *(requires bollard/fender locations from PKG-09; mooring/berthing loads; load transfer to structure)* |

**Note on scope overlap:** Some mooring and berthing topics may be covered in dedicated reports (DEL-08.06 Berthing Energy Calculation Report, DEL-08.09 Mooring Analysis Report). Coordination required to avoid duplication and ensure DEL-08.03 includes calculations needed for structural design.

### Platform Structural Calculations (If Applicable)

| Calculation Topic | Expected Content | Status |
|---|---|---|
| Platform framing design | Beam, column, brace design for loading platform structure; equipment support framing; design per CSA S16 or CSA S6 | **TBD** *(similar to trestle; requires platform layout from DEL-08.01; equipment loads from PKG-11 Marine Loading System)* |
| Platform connections | Connection design for platform framing; equipment mounting connection design | **TBD** *(requires connection detailing from DEL-08.01)* |
| Platform serviceability | Deflection, vibration, and dynamic considerations for equipment operation | **TBD** *(requires equipment operating criteria; serviceability limits per ER or equipment vendor)* |

### Catwalk and Abutment Structural Calculations (If Applicable)

| Calculation Topic | Expected Content | Status |
|---|---|---|
| Catwalk design | Beam, support, handrail design; live load and snow load (if applicable) per building code or ER | **TBD** *(requires catwalk layout from DEL-08.01; code requirements for personnel access structures)* |
| Abutment design | Abutment structural design for loads from trestle; bearing capacity of foundation; connection design to trestle and landside structures | **TBD** *(requires abutment configuration from DEL-08.01; geotechnical capacity; interface loads from civil/structural works)* |

## Design Inputs and Basis (Not Yet Captured)

The calculation package content depends on design inputs and basis documents not yet extracted into this deliverable folder:

- **ER clauses for marine structures design criteria and methods:** **TBD** *(ER Vol 2 Parts 1-2 present as PDFs; clause extraction pending)*
- **Codes and standards required by ER:** **TBD** *(likely: CSA S6, CSA S16, API RP 2A for marine structures; geotechnical codes for pile design; confirm from ER)*
- **Design loads and load combinations:** **TBD** *(dead, live, environmental loads; load factors and combinations per ER and codes)*
- **Geotechnical design parameters:** **TBD** *(from DEL-08.04 Marine Geotechnical Report; soil parameters, pile capacity, scour depth)*
- **Marine environment data:** **TBD** *(wind, current, wave, water levels, seismic; from ER or DEL-08.10 Current Assessment Basis Report)*
- **Vessel and mooring/berthing data:** **TBD** *(design vessel characteristics; mooring arrangement; berthing energy; from ER or DEL-08.06/DEL-08.09 reports)*
- **Equipment loads and envelopes:** **TBD** *(from PKG-11 Marine Loading System, PKG-09 Marine Outfitting; loading arm loads, fender reactions, bollard loads)*
- **Material properties:** **TBD** *(steel grades, yield/tensile strength; from DEL-08.02 Marine Structures Technical Specification)*
- **Geometry and layout:** **TBD** *(from DEL-08.01 Marine Structures Design Drawing Set; member sizes, spans, elevations, pile locations)*

## Interfaces (Advisory)

Dependencies are coordinated externally per `_DEPENDENCIES.md` (mode: NOT_TRACKED). The following interfaces are anticipated based on decomposition scope and should be confirmed via design coordination:

### Interface to DEL-08.01 Marine Structures Design Drawing Set
- Drawings provide geometry, layout, member sizes, pile locations used as calculation inputs — **TBD**
- Calculations provide design verification and member sizing that inform final drawing details — **TBD**
- **Coordination required:** Iterative design process; calculations verify/refine preliminary layout from drawings

### Interface to DEL-08.02 Marine Structures Technical Specification
- Specifications define material properties (steel grades, strengths) used in calculations — **TBD**
- Calculations verify that specified materials meet design requirements — **TBD**

### Interface to DEL-08.04 Marine Geotechnical Report
- Geotechnical report provides soil parameters, pile capacity recommendations, scour depth used in pile calculations — **TBD**
- **Coordination required:** Pile calculations must use geotechnical parameters from DEL-08.04

### Interface to DEL-08.06 Berthing Energy Calculation Report
- Berthing energy report provides berthing loads and fender reactions used in structural calculations — **TBD**
- **Coordination required:** Verify scope overlap; DEL-08.03 may reference DEL-08.06 for berthing loads rather than duplicating analysis

### Interface to DEL-08.09 Mooring Analysis Report
- Mooring analysis report provides mooring line loads and bollard loads used in structural calculations — **TBD**
- **Coordination required:** Verify scope overlap; DEL-08.03 may reference DEL-08.09 for mooring loads rather than duplicating analysis

### Interface to DEL-08.10 Current Assessment Basis Report
- Current assessment report provides current loads on structure used in structural calculations — **TBD**
- **Coordination required:** Current loads from DEL-08.10 used in load combinations for structural design

### Interface to PKG-09 Marine Outfitting and PKG-11 Marine Loading System
- Equipment loads (fenders, bollards, loading arm, operator shelter) used in structural calculations — **TBD**
- **Coordination required:** Equipment loads and mounting details must be obtained from equipment packages

## Cross-Document Links

- **Requirements basis:** `Specification.md` (R-001 through R-005) defines what must be included in the calculation package and verification criteria
- **Production workflow:** `Procedure.md` provides step-by-step process to produce calculations, aligned to Specification requirements
- **Engineering considerations:** `Guidance.md` provides rationale for each Specification requirement and guidance on calculation approach

## Key TBDs (Next Closure Items)

Priority items to resolve before calculation work can commence:

1. **ER clause extraction for design criteria, methods, and acceptance** (supports `Specification.md` R-003): **TBD**
2. **Design basis inputs** (loads, environmental data, vessel data, geotechnical parameters) (supports `Specification.md` R-002): **TBD**
3. **Calculation scope coordination** with DEL-08.06, DEL-08.09, DEL-08.10 to avoid duplication (supports `Specification.md` R-001): **TBD**
4. **Independent check and professional stamp requirements** (supports `Specification.md` R-004): **TBD**
5. **Calculation format and documentation standards** (hand calcs vs software; required documentation) (supports `Specification.md` R-002, R-005): **TBD**

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.03_Marine_Structures_Design_Calculations/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.03 at line 283)
- `test/execution/PKG-08_Marine_Structures/0_References/_REFERENCE_INDEX.md` *(stub; references not yet populated)*
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
