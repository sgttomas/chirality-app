# Specification: DEL-08.01 Marine Structures Design Drawing Set

## Scope

This document defines **minimum requirements for the deliverable artifact itself** (a marine structures drawing set): required contents, document-control expectations, interface coordination, and verification/acceptance criteria for issue.

**Deliverable description (source-anchored):** Defines the design arrangement and details for marine structures per Employer's Requirements (ER). *(Source: Decomposition line 281 + `_CONTEXT.md`; specific ER section/clause locations TBD)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

## Requirements (Deliverable Content)

### R-001 — Drawing Set Coverage (Minimum)

**Requirement:** The drawing set shall include, at minimum, the following anticipated artifacts as listed in the decomposition deliverables table (line 281):

- Piling layout
- Trestle general arrangement (GA)
- Platform GA
- Catwalk drawings
- Abutment drawings

**Additional scope coverage requirement:** All scope elements listed in PKG-08 scope (Decomposition line 275) shall be represented in the drawing set: piling, access trestle, loading platform structure, catwalk, and abutments. Any scope element not included shall be explicitly noted as out-of-scope or future phase.

**Source:** Decomposition line 281 (anticipated artifacts); Decomposition line 275 (PKG-08 scope)

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-001

**Verification:** See `Procedure.md` § Requirement Coverage, R-001

---

### R-002 — ER-Driven Requirements Capture

**Requirement:** The drawing set shall reflect all applicable ER requirements for marine structures.

**Applicable ER clauses:** **TBD** *(ER Vol 2 Parts 1-2 present as PDFs; clause extraction pending)*

**Required supporting documentation:** Any calculations, reports, or referenced documents required by ER to support the drawings shall be identified and cross-referenced on the drawings. **TBD** *(pending ER clause review)*

**Codes and standards:** The drawings shall comply with codes and standards required by ER. **TBD** *(pending ER clause review; likely: CSA S6, CSA S16, API, ISO standards for marine works)*

**Source:** Decomposition line 281 states "per ER requirements"; specific ER clause locations TBD

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-002

**Verification:** See `Procedure.md` § Requirement Coverage, R-002

---

### R-003 — Document Control / Metadata

**Requirement:** The drawing set shall comply with project document control requirements for numbering, revision control, and issue status.

**Drawing numbering scheme:** **TBD** *(pending project document control procedures from ER or project document control plan)*

**Revision and issue status scheme:** **TBD** *(typical: A/B/C for internal review; 0/1/2... for issued; confirm from project procedures)*

**Title block requirements:** All drawings shall include a compliant title block containing (at minimum): project name, drawing title, drawing number, scale, date, revision, approvals, and classification. Template and detailed requirements: **TBD** *(pending project CAD standard)*

**Drawing register/index:** A drawing register or index shall be maintained and issued with the drawing set, listing all drawing numbers, titles, revisions, and issue dates. Format: **TBD**

**ASSUMPTION:** Project document control procedures exist and are referenced in ER Vol 2 Part 1; clause/section location TBD.

**Source:** Standard EPC practice; project-specific requirements TBD from ER and project document control plan

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-003

**Verification:** See `Procedure.md` § Requirement Coverage, R-003

---

### R-004 — Interface Coordination

**Requirement:** Where interfaces affect drawing content (tie-ins, equipment envelopes, clearances, load paths, access provisions, utility penetrations), they shall be coordinated with relevant disciplines/packages and shown or noted on the drawings.

**Note on dependency tracking:** Per `_DEPENDENCIES.md`, dependency mode is NOT_TRACKED. Dependencies are coordinated externally by humans. The following interfaces are anticipated based on decomposition scope and shall be confirmed via design coordination:

#### Anticipated Interfaces (TBD):

- **PKG-09 Marine Outfitting:** Fender mounting points and reaction loads; bollard mounting points and pull-out loads; ladder and access provisions — **TBD**
- **PKG-11 Marine Loading System:** Marine loading arm mounting/support structure; operator shelter location and support; leak detection and nitrogen supply routing — **TBD**
- **Civil/Structural Works:** Abutment tie-in details (dimensions, elevations, connections); access provisions from landside; utilities penetrations and routing — **TBD**
- **DEL-08.04 Marine Geotechnical Report:** Marine geotechnical parameters (pile capacity, soil layering); bathymetric survey results (seabed levels, obstructions) — **TBD**

**Drawing requirements for interfaces:**
- Show interface points with dimensions, elevations, and coordinate references
- Include interface notes identifying interfacing discipline/package and drawing references (where known)
- Mark TBD interfaces explicitly on drawings with notes indicating coordination status

**Source:** Standard EPC practice for multi-discipline coordination; specific interface requirements TBD from ER and design coordination

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-004

**Verification:** See `Procedure.md` § Requirement Coverage, R-004

---

### R-005 — Technical Content and Notation (Best Practice)

**Requirement:** Drawings shall include sufficient technical content and notation to support construction and approval:

- **Coordinate system and datum:** All drawings shall reference the project coordinate system and vertical datum. Coordinate system and datum definition: **TBD** *(critical for marine structures; requires project survey control basis)*
- **Dimensions and elevations:** Key dimensions, clearances, and elevations shall be dimensioned. Dimensioning standard (metric/imperial): **TBD** *(ASSUMPTION: metric per Canadian practice; confirm from ER or project CAD standard)*
- **Materials and specifications:** Materials and specifications shall be noted on drawings or referenced to specification documents. Cross-references to DEL-08.02 Marine Structures Technical Specification: **TBD**
- **General notes:** Include general notes for codes/standards, tolerances, welding/fabrication standards, inspection requirements, and any deviations from standard practice
- **Legends and symbols:** Include legends for symbols, abbreviations, and drawing conventions used

**ASSUMPTION:** Standard marine engineering drawing practices apply unless otherwise specified by ER.

**Source:** Standard marine engineering practice; project-specific requirements TBD from ER and project CAD standard

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-005

**Verification:** See `Procedure.md` § Requirement Coverage, R-005

---

## Standards and References

### Codes and Standards (TBD)

Applicable codes and standards are **TBD** until the relevant ER clauses are extracted. Likely standards for Canadian marine structures (to be confirmed):

- CSA S6 — Canadian Highway Bridge Design Code (for structural design)
- CSA S16 — Design of Steel Structures (for steel structures)
- API standards (for marine piling and structures)
- ISO standards for marine structures (if specified by ER)
- Local building code and regulatory requirements (Transport Canada, Canadian Coast Guard, etc.)

**ASSUMPTION:** Canadian codes and standards apply unless otherwise specified by ER. Specific editions and clauses: **TBD**

### Reference Documents

Minimum reference set for drawing production:

- **Employer's Requirements:** Vol 2 Parts 1-2 (available in repo as PDFs; clause extraction pending)
- **DEL-08.02 Marine Structures Technical Specification** (defines materials, performance requirements)
- **DEL-08.03 Marine Structures Design Calculations** (provides engineering basis and sizing)
- **DEL-08.04 Marine Geotechnical Report** (provides geotechnical parameters and bathymetric data)
- **Project Document Control Procedures** — **TBD** *(location in ER or project procedures TBD)*
- **Project CAD/BIM Standard** — **TBD** *(location in ER or project procedures TBD)*

Reference index: `test/execution/PKG-08_Marine_Structures/0_References/_REFERENCE_INDEX.md` *(currently stub; to be populated)*

---

## Verification and Acceptance

### Verification Requirements

Verification requirements are not fully stated in accessible sources within this deliverable folder. The following verification approach is **PROPOSED** pending confirmation from ER and project QA/QC procedures:

1. **Originator self-check:** Engineer performing drawing work verifies compliance with R-001 through R-005 before submittal for review
2. **Discipline check:** Senior marine engineer or discipline lead reviews drawings for technical adequacy, completeness, and compliance with standards
3. **Interdisciplinary coordination (IDC) check:** Interfacing disciplines review drawings for interface coordination and compatibility
4. **Independent check:** Independent checker (if required by project) reviews drawings for compliance with ER, codes, and project procedures
5. **Approval for issue:** Authorized approver signs off on drawings for issue to Employer or construction

**Required reviews (to be confirmed):** Discipline check, IDC, independent check (if required), approval for issue — **TBD**

### Acceptance Criteria

Acceptance criteria for "issue" status are **TBD** pending ER and project procedures. Typical acceptance criteria (to be confirmed):

- All review comments resolved and dispositioned
- All requirements (R-001 through R-005) verified as met
- Drawing register/index complete and current
- Title blocks complete with all required approvals and signatures
- Issue status marked on drawings (e.g., "Issued for Construction")

### Requirement Verification Map

| Spec ID | Verification Method | Evidence / Record | Status |
|---|---|---|---|
| R-001 | Drawing list completeness check against decomposition artifacts list (line 281) and PKG-08 scope (line 275) | Drawing index/register showing all required artifacts included | **TBD** |
| R-002 | ER compliance review | Requirements/IDC matrix mapping drawings to ER clauses; supporting calculations/reports cross-referenced | **TBD** |
| R-003 | Document control compliance check | Drawing title blocks, numbering, revision status, drawing register reviewed against project document control procedures | **TBD** |
| R-004 | Interdisciplinary/interface review | IDC records and resolved interface comments; interface points shown/noted on drawings | **TBD** |
| R-005 | Technical content review | Peer/discipline check confirms adequate dimensions, notes, materials, symbols, general notes | **TBD** |

---

## Documentation / Deliverable Outputs

### Expected Drawing Set Outputs (Minimum)

Per decomposition line 281 and this Specification R-001:

- Piling layout
- Trestle general arrangement (GA)
- Platform GA
- Catwalk drawings
- Abutment drawings

### Associated Records (TBD)

Records to retain with the drawing set package:

- Drawing register / transmittal — **TBD** *(format and location TBD)*
- Review/IDC markups and dispositions — **TBD** *(format and location TBD)*
- Approval records and sign-offs — **TBD** *(format and location TBD)*

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.01_Marine_Structures_Design_Drawing_Set/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.01 at line 281)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard EPC/marine engineering practice (for document control, interface coordination, technical content requirements)
