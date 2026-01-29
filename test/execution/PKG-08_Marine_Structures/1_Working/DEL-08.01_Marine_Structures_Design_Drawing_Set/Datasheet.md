# Datasheet: DEL-08.01 Marine Structures Design Drawing Set

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-08.01 |
| Name | Marine Structures Design Drawing Set |
| Package | PKG-08 Marine Structures |
| Discipline | Marine |
| Type | Drawing |
| Responsible | D&B Contractor |
| Lifecycle (from `_STATUS.md`) | INITIALIZED |

## What This Deliverable Is

**Description (source-anchored):** Defines the design arrangement and details for marine structures per Employer's Requirements (ER). *(Source: Decomposition line 281 + `_CONTEXT.md`; specific ER section/clause locations TBD)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275, PKG-08 scope statement)*

**Minimum anticipated drawing artifacts (per decomposition line 281):**
- Piling layout
- Trestle general arrangement (GA)
- Platform GA
- Catwalk drawings
- Abutment drawings

## Document / Drawing Set Metadata (TBD)

| Attribute | Value |
|---|---|
| Drawing / document numbering scheme | **TBD** *(pending project document control procedures from ER or project document control plan)* |
| Drawing list / index format | **TBD** *(standard practice: tabular register with drawing number, title, revision, date)* |
| Sheet sizes | **TBD** *(ASSUMPTION: typical marine drawings use ANSI D or ISO A1; confirm from project CAD standard)* |
| Scales | **TBD** *(typical: 1:50, 1:100, 1:200 for GAs; 1:10, 1:20 for details; confirm from project CAD standard)* |
| CAD/BIM standard and layer naming | **TBD** *(ASSUMPTION: project CAD standard exists; reference TBD from ER Vol 2 Part 1 or project procedures)* |
| Revision / issue status format | **TBD** *(typical: A/B/C for internal, 0/1/2... for issued; confirm from document control procedures)* |
| Title block requirements | **TBD** *(content: project name, drawing title, scale, date, revision, approvals; template location TBD)* |
| Classification / confidentiality marking | **TBD** *(ASSUMPTION: commercial-in-confidence unless otherwise specified by Employer)* |
| Coordinate system / survey datum | **TBD** *(critical for marine structures; requires project survey control basis)* |
| Elevation datum (e.g., chart datum, geodetic) | **TBD** *(critical for marine structures; requires project vertical datum basis)* |

## Marine Structures Scope Elements (from PKG-08)

The following scope elements (Decomposition line 275) require coverage in the drawing set. Each element listed below must appear on at least one drawing or be explicitly marked as out-of-scope/future phase:

| Scope Element | Typical Drawing Coverage | Status |
|---|---|---|
| Piling | Piling layout plan, pile details, pile schedule | **TBD** *(anticipated in drawing set per Decomposition line 281)* |
| Access trestle | Trestle GA (plan, elevation, sections), framing details | **TBD** *(anticipated in drawing set per Decomposition line 281)* |
| Loading platform structure | Platform GA (plan, elevation, sections), structural framing, equipment support details | **TBD** *(anticipated in drawing set per Decomposition line 281)* |
| Catwalk | Catwalk layout, support details, handrail/safety details | **TBD** *(anticipated in drawing set per Decomposition line 281)* |
| Abutments | Abutment drawings (plan, elevation, sections), tie-in details | **TBD** *(anticipated in drawing set per Decomposition line 281)* |

## Design Inputs (Not Yet Captured)

The drawing set content depends on project requirements not yet extracted into this deliverable folder. These inputs are **TBD** and must be resolved before drawing production can commence:

- Applicable ER clauses for marine structures drawing requirements: **TBD** *(ER Vol 2 Parts 1-2 present as PDFs; clause extraction pending)*
- Codes/standards required by ER for marine structures: **TBD** *(likely: CSA S6, CSA S16, API, ISO standards for marine works; confirm from ER)*
- Design basis data:
  - Vessel characteristics (dimensions, berthing loads, mooring loads): **TBD** *(may be in DEL-08.06 Berthing Energy Calculation Report or ER)*
  - Environmental loads (waves, current, wind, ice, seismic): **TBD** *(may be in DEL-08.10 Current Assessment Basis Report and ER)*
  - Geotechnical inputs (pile capacity, soil parameters): **TBD** *(from DEL-08.04 Marine Geotechnical Report)*
  - Design water levels and tidal range: **TBD** *(from ER or marine geotechnical report)*
  - Equipment loads and envelopes (loading arm, fenders, bollards, etc.): **TBD** *(from DEL-09.01, DEL-11.01, and related packages)*
  - Access and operational clearances: **TBD** *(from ER and operational requirements)*

## Interfaces (Advisory)

Dependencies are coordinated externally per `_DEPENDENCIES.md` (mode: NOT_TRACKED). The following interfaces are anticipated based on decomposition scope and should be confirmed via design coordination:

### Interface to PKG-09 Marine Outfitting
- Fender mounting points and reaction loads on structure *(affects platform/trestle structural design and drawing details)* — **TBD**
- Bollard mounting points and pull-out loads on structure *(affects platform structural design and drawing details)* — **TBD**
- Ladder and access provisions on structure *(affects GA layouts and detail drawings)* — **TBD**

### Interface to PKG-11 Marine Loading System
- Marine loading arm mounting/support structure *(affects platform structural design, equipment envelopes, loading path)* — **TBD**
- Operator shelter location and support structure *(affects platform GA and structural loading)* — **TBD**
- Leak detection and nitrogen supply routing/supports *(affects platform layout and penetrations)* — **TBD**

### Interface to Civil/Structural Works (abutments and landside connections)
- Abutment tie-in details (dimensions, elevations, connection details) *(affects abutment drawings and trestle end connections)* — **TBD**
- Access provisions from landside to marine structures *(affects trestle/platform access design)* — **TBD**
- Utilities penetrations and routing (power, control, water, etc.) *(affects platform/trestle layout and penetration details)* — **TBD**

### Interface to Geotechnical (DEL-08.04)
- Marine geotechnical parameters (pile capacity, soil layering) *(informs piling layout and pile selection)* — **TBD** *(from DEL-08.04 Marine Geotechnical Report)*
- Bathymetric survey results (seabed levels, existing obstructions) *(informs piling layout and elevation design)* — **TBD** *(from DEL-08.04 Marine Geotechnical Report)*

## Cross-Document Links

- **Requirements basis:** `Specification.md` (R-001 through R-005) defines what must be included in the drawing set and verification criteria
- **Production workflow:** `Procedure.md` provides step-by-step process to produce the drawing set, aligned to Specification requirements
- **Engineering considerations:** `Guidance.md` provides rationale for each Specification requirement and checklists for scope coverage

## Key TBDs (Next Closure Items)

Priority items to resolve before drawing production can commence:

1. **ER clause extraction for marine structures drawing requirements** (supports `Specification.md` R-002): **TBD**
2. **Project document control requirements** (numbering, revisioning, issue statuses) (supports `Specification.md` R-003): **TBD**
3. **Project CAD/BIM standards** (layer naming, sheet templates, coordinate system) (supports production workflow in `Procedure.md`): **TBD**
4. **Design basis inputs** (vessel data, environmental loads, geotechnical results) (required for drawing content): **TBD**
5. **Interface definition list** (equipment envelopes, tie-in points, clearances) (supports `Specification.md` R-004): **TBD**

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.01_Marine_Structures_Design_Drawing_Set/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope + deliverables table; DEL-08.01 at line 281)
- `test/execution/PKG-08_Marine_Structures/0_References/_REFERENCE_INDEX.md` *(stub; references not yet populated)*
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
