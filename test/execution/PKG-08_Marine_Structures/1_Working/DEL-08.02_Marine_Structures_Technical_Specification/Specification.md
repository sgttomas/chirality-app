# Specification: DEL-08.02 Marine Structures Technical Specification

## Scope

This document defines **minimum requirements for the deliverable artifact itself** (the Marine Structures Technical Specification document): required specification content, document-control expectations, interface coordination, and verification/acceptance criteria for issue.

**Deliverable description (source-anchored):** Defines performance, materials, and workmanship requirements for marine structures per Employer's Requirements (ER). *(Source: Decomposition line 282 + `_CONTEXT.md`; specific ER section/clause locations TBD)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Requirements (Deliverable Content)

### R-001 — Specification Coverage (Minimum)

**Requirement:** The technical specification deliverable shall include, at minimum, the following anticipated specification artifacts as listed in the decomposition deliverables table (line 282):

- Marine piling specification
- Structural steel specification (marine)

**Additional scope coverage requirement:** All marine structures scope elements listed in PKG-08 scope (Decomposition line 275) — piling, access trestle, loading platform structure, catwalk, abutments — shall be addressed in the specifications. Materials, fabrication, installation, and inspection/testing requirements shall be specified for each scope element or explicitly noted as covered by another deliverable/specification.

**Source:** Decomposition line 282 (anticipated artifacts); Decomposition line 275 (PKG-08 scope)

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-001

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-001

---

### R-002 — ER-Driven Requirements Capture

**Requirement:** The technical specification(s) shall incorporate all applicable ER requirements for marine structures materials, performance, workmanship, inspection/testing, and documentation.

**Applicable ER clauses:** **TBD** *(ER Vol 2 Parts 1-2 present as PDFs; clause extraction pending)*

**Codes and standards:** The specifications shall reference and comply with codes and standards required by ER. **TBD** *(pending ER clause review; likely codes: CSA S6, CSA S16, CSA W59 for Canadian structures; API standards for marine piling; ASTM material standards; ISO marine standards if specified)*

**Requirements traceability:** Each "shall" requirement in the specification shall be traceable to an ER clause, code/standard clause, or design basis document. Requirements not traceable to a source shall be labeled as **ASSUMPTION** or **PROPOSAL** pending confirmation.

**Source:** Decomposition line 282 states "per ER requirements"; specific ER clause locations TBD

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-002

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-002

---

### R-003 — Technical Specification Structure and Content

**Requirement:** The technical specification(s) shall include the following minimum content sections to provide complete and usable requirements for fabrication and construction:

#### For Marine Piling Specification:

1. **Scope and Applicability** — Types of piling covered; exclusions; interface to other specifications
2. **Definitions and Abbreviations** — Terms and acronyms used in specification
3. **Referenced Standards and Codes** — Applicable codes for materials, fabrication, installation, testing (with edition/year)
4. **Materials** — Pile material grades and specifications; coatings/corrosion protection; fasteners; welding consumables; material testing and certification requirements
5. **Fabrication and Workmanship** — Pile fabrication tolerances; welding requirements (procedures, qualifications, inspection); surface preparation; coating application; shop inspection
6. **Installation Requirements** — Pile driving criteria and procedures; installation tolerances; minimum penetration; pile cut-off elevations; driving records and documentation
7. **Inspection and Testing** — Non-destructive testing (NDT) requirements; pile integrity testing; load testing (if required); acceptance criteria
8. **Submittals and Records** — Shop drawings; material certificates; welding documentation; test reports; as-built records

#### For Structural Steel Specification (Marine):

1. **Scope and Applicability** — Structural steel components covered (trestle, platform, catwalk, abutments); exclusions; interface to other specifications
2. **Definitions and Abbreviations** — Terms and acronyms used in specification
3. **Referenced Standards and Codes** — Applicable codes for materials, fabrication, welding, erection (with edition/year)
4. **Materials** — Steel grades and specifications; bolts/fasteners; welding consumables; coatings/corrosion protection; material testing and certification requirements
5. **Fabrication and Workmanship** — Fabrication tolerances; welding requirements (procedures, qualifications, inspection); bolting requirements; surface preparation; coating application; shop inspection
6. **Erection/Installation Requirements** — Erection tolerances; bolting/welding procedures; field welding; temporary bracing; erection sequence (if critical)
7. **Corrosion Protection** — Marine environment exposure classification; coating systems (primers, intermediate coats, finish coats); surface preparation standards; coating inspection; cathodic protection (if required)
8. **Inspection and Testing** — Weld inspection (visual, NDT); dimensional inspection; bolting inspection; coating inspection; acceptance criteria
9. **Submittals and Records** — Shop drawings; material certificates; welding procedure specifications (WPS); welder qualifications (WPQ); test reports; as-built records

**Content completeness requirement:** All sections listed above shall be included in the issued specifications. Sections for which requirements cannot yet be determined shall be marked **TBD** with a plan for resolution, rather than omitted.

**ASSUMPTION:** Standard technical specification structure applies unless ER or project template specifies otherwise. Specific template location: **TBD**

**Source:** Standard EPC/marine engineering practice for technical specifications; project-specific template TBD from ER or project procedures

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-003

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-003

---

### R-004 — Interface Coordination

**Requirement:** Where specifications affect or reference other deliverables (drawings, calculations, installation records), cross-references and coordination shall be ensured.

**Note on dependency tracking:** Per `_DEPENDENCIES.md`, dependency mode is NOT_TRACKED. Dependencies are coordinated externally by humans. The following interfaces are anticipated based on decomposition scope and shall be confirmed via design coordination:

#### Anticipated Interfaces (TBD):

- **DEL-08.01 Marine Structures Design Drawing Set:** Drawings reference materials and specifications from DEL-08.02; specifications provide detailed requirements for materials/workmanship shown on drawings — **TBD** *(coordination required to ensure consistency)*
- **DEL-08.03 Marine Structures Design Calculations:** Calculations establish design criteria (loads, stresses, member sizes, connection capacities) that inform specification requirements (material grades, connection details, inspection requirements) — **TBD**
- **DEL-08.04 Marine Geotechnical Report:** Geotechnical report provides pile capacity and installation criteria that inform piling specification requirements (minimum penetration, driving criteria, load testing) — **TBD**
- **DEL-08.05 Marine Structures Installation & Test Records:** Specifications define inspection and testing requirements that must be documented in installation/test records — **TBD** *(coordination required to ensure specification requirements align with records scope)*

**Specification requirements for interface coordination:**
- Include cross-references to related deliverables (e.g., "Refer to DEL-08.01 drawings for pile layout and member sizes")
- Note interface points where coordination is required (e.g., "Pile driving criteria shall be consistent with geotechnical recommendations in DEL-08.04")
- Mark TBD interfaces explicitly in specifications with notes indicating coordination status

**Source:** Standard EPC practice for multi-discipline coordination; specific interface requirements TBD from ER and design coordination

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-004

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-004

---

### R-005 — Document Control / Metadata

**Requirement:** The specification document(s) shall comply with project document control requirements for numbering, revision control, and issue status.

**Document numbering scheme:** **TBD** *(pending project document control procedures from ER or project document control plan; likely: discipline code + package code + sequence, e.g., SPEC-MAR-08-001)*

**Revision and issue status scheme:** **TBD** *(typical: Rev A/B/C for internal review; Rev 0/1/2 for issued; confirm from project procedures)*

**Document header/footer requirements:** All specification pages shall include (at minimum): document title, document number, revision, date, page number, project name, and classification. Template and detailed requirements: **TBD** *(pending project specification template)*

**ASSUMPTION:** Project document control procedures exist and are referenced in ER Vol 2 Part 1; clause/section location TBD.

**Source:** Standard EPC practice; project-specific requirements TBD from ER and project document control plan

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-005

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-005

---

## Standards and References

### Codes and Standards (TBD)

Applicable codes and standards are **TBD** until the relevant ER clauses are extracted. Likely standards for Canadian marine structures (to be confirmed from ER):

- **CSA S6** — Canadian Highway Bridge Design Code (for structural design)
- **CSA S16** — Design of Steel Structures (for steel design)
- **CSA W59** — Welded Steel Construction (for welding requirements)
- **API RP 2A** — Planning, Designing and Constructing Fixed Offshore Platforms (for piling and marine structures)
- **API Spec 2B** — Fabrication of Structural Steel Pipe (for pipe piles)
- **ASTM A252** — Welded and Seamless Steel Pipe Piles (for pile material)
- **ASTM A709** — Structural Steel for Bridges (for structural steel material)
- **SSPC/NACE coating standards** — Surface preparation and coating systems for marine environment
- **Transport Canada, Canadian Coast Guard regulations** — Regulatory requirements for marine structures (if applicable)

**ASSUMPTION:** Canadian codes and standards apply unless otherwise specified by ER. Specific editions and clauses: **TBD**

### Reference Documents

Minimum reference set for specification development:

- **Employer's Requirements:** Vol 2 Parts 1-2 (available in repo as PDFs; clause extraction pending)
- **DEL-08.01 Marine Structures Design Drawing Set** (provides design arrangement and details)
- **DEL-08.03 Marine Structures Design Calculations** (provides engineering basis and sizing)
- **DEL-08.04 Marine Geotechnical Report** (provides geotechnical parameters and pile capacity)
- **Project Document Control Procedures** — **TBD** *(location in ER or project procedures TBD)*
- **Project Specification Template** — **TBD** *(location in ER or project procedures TBD)*

Reference index: `test/execution/PKG-08_Marine_Structures/0_References/_REFERENCE_INDEX.md` *(currently stub; to be populated)*

---

## Verification and Acceptance

### Verification Requirements

Verification requirements are not fully stated in accessible sources within this deliverable folder. The following verification approach is **PROPOSED** pending confirmation from ER and project QA/QC procedures:

1. **Originator self-check:** Engineer drafting specification verifies compliance with R-001 through R-005 before submittal for review
2. **Discipline check:** Senior marine engineer or discipline lead reviews specification for technical adequacy, completeness, constructability, and compliance with standards
3. **Interdisciplinary coordination (IDC) check:** Interfacing disciplines review specification for interface coordination and compatibility with their deliverables
4. **Constructability review:** Fabricator/constructor input on specification clarity and constructability (if available at this stage)
5. **Independent check:** Independent checker (if required by project) reviews specification for compliance with ER, codes, and project procedures
6. **Approval for issue:** Authorized approver signs off on specification for issue to Employer or construction

**Required reviews (to be confirmed):** Discipline check, IDC, constructability review (if available), independent check (if required), approval for issue — **TBD**

### Acceptance Criteria

Acceptance criteria for "issue" status are **TBD** pending ER and project procedures. Typical acceptance criteria (to be confirmed):

- All review comments resolved and dispositioned
- All requirements (R-001 through R-005) verified as met
- ER requirements traceability matrix complete (all "shall" requirements traceable to source)
- All TBD items documented with resolution plan or acceptance by Employer
- Document control metadata complete (document number, revision, approvals, issue status)
- Document issued with required approvals and signatures

### Requirement Verification Map

| Spec ID | Verification Method | Evidence / Record | Status |
|---|---|---|---|
| R-001 | Specification completeness check against decomposition artifacts list (line 282) and PKG-08 scope (line 275) | Issued specification package includes both required specifications (piling + structural steel) covering all scope elements | **TBD** |
| R-002 | ER compliance review; requirements traceability check | Requirements traceability matrix mapping all "shall" requirements to ER clauses, codes/standards, or design basis documents | **TBD** |
| R-003 | Technical content review against required section structure | Section checklist showing all required sections present and populated (or marked TBD with resolution plan) | **TBD** |
| R-004 | Interdisciplinary/interface review | IDC records showing coordination with DEL-08.01, DEL-08.03, DEL-08.04, DEL-08.05; cross-references verified | **TBD** |
| R-005 | Document control compliance check | Document number, revision, header/footer compliance verified against project document control procedures | **TBD** |

---

## Documentation / Deliverable Outputs

### Expected Specification Outputs (Minimum)

Per Decomposition line 282 and this Specification R-001:

- Marine piling specification
- Structural steel specification (marine)

### Associated Records (TBD)

Records to retain with the specification package:

- Requirements traceability matrix (mapping specification requirements to ER clauses, codes/standards, design basis) — **TBD** *(format and location TBD)*
- Review/IDC markups and dispositions — **TBD** *(format and location TBD)*
- Approval records and sign-offs — **TBD** *(format and location TBD)*

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.02_Marine_Structures_Technical_Specification/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.02 at line 282)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard EPC/marine engineering practice (for specification structure, document control, interface coordination)
