# Guidance: DEL-08.01 Marine Structures Design Drawing Set

## Purpose

This document provides **engineering rationale and decision-making guidance** to support consistent production of the Marine Structures Design Drawing Set. It explains the "why" behind each Specification requirement, identifies key considerations and trade-offs, and highlights inputs still missing from the deliverable folder.

**Deliverable intent (source-anchored):** Defines the design arrangement and details for marine structures per ER requirements. *(Source: Decomposition line 281 + `_CONTEXT.md`; specific ER clause locations TBD)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Principles (Engineering Intent, Non-Invented)

Because the governing ER clauses and referenced standards are not yet extracted into this package, this guidance avoids asserting specific code/standard requirements. The following principles are based on standard marine engineering practice and the decomposition scope:

### Completeness and Traceability
- **Intent:** Every major marine structure element in scope (piling, trestle, platform, catwalk, abutments per Decomposition line 275) must appear on at least one drawing with clear cross-references to related drawings/details
- **Rationale:** Ensures constructors have complete information; supports approval process; reduces RFIs and construction errors
- **Practice:** Maintain a drawing index/register that maps each scope element to specific drawing numbers

### Coordination and Interface Management
- **Intent:** Interfaces to other disciplines/packages (outfitting, loading equipment, civil tie-ins) must be explicitly shown, dimensioned, or noted on drawings
- **Rationale:** Marine structures are an integration point for multiple packages (PKG-09 outfitting, PKG-11 loading system, civil works). Missing or unclear interface information causes construction delays and rework
- **Practice:** Even though dependencies are NOT_TRACKED, capture known interface points on drawings with notes identifying interfacing discipline/package and coordination status (TBD if not yet confirmed)

### Explicit Assumptions (Transparency)
- **Intent:** If a design basis input is not confirmed, mark it as TBD rather than embedding it implicitly in drawings
- **Rationale:** Undocumented assumptions become design defects when inputs change. Explicit TBDs enable systematic closure tracking
- **Practice:** Use drawing notes to call out TBD items (e.g., "Equipment envelope TBD — coordinate with PKG-11"; "Final elevation TBD — pending bathymetric survey")

---

## Requirement Rationale Map

This section links each Specification requirement to its engineering rationale and key considerations.

### R-001: Drawing Set Coverage (Minimum)

**What it requires:**
- Minimum drawing artifacts per Decomposition line 281: piling layout, trestle GA, platform GA, catwalk drawings, abutment drawings
- Coverage of all PKG-08 scope elements per Decomposition line 275: piling, access trestle, loading platform structure, catwalk, abutments

**Rationale:**
- Decomposition defines the minimum deliverable scope; R-001 ensures these minimum artifacts are produced
- Completeness check against scope ensures no scope element is omitted
- Drawing set must support construction and approval; incomplete sets delay project

**Key Considerations:**
- **Drawing breakdown strategy:** Should each scope element have a dedicated drawing, or can some be combined? *(Trade-off: fewer drawings vs clarity; TBD based on drawing complexity and project CAD standard)*
- **Level of detail:** What level of detail is required for each drawing type (GA vs detail)? *(TBD based on ER requirements and project practices)*
- **Phasing:** Are all scope elements in Phase 1, or are some future phase? *(TBD based on project phasing plan)*

**Sources:**
- Decomposition line 281 (anticipated artifacts list)
- Decomposition line 275 (PKG-08 scope statement)

---

### R-002: ER-Driven Requirements Capture

**What it requires:**
- Drawings shall reflect all applicable ER requirements for marine structures
- ER clauses, required supporting documentation, codes/standards: TBD

**Rationale:**
- ER is the contractual requirements document; compliance is mandatory
- Decomposition states deliverable is "per ER requirements" (line 281), so ER clauses must be identified and incorporated
- Failure to meet ER requirements results in non-conformance and rework

**Key Considerations:**
- **ER clause identification:** Which ER clauses apply to marine structures? *(TBD; requires systematic review of ER Vol 2 Parts 1-2)*
- **Code/standard compliance:** Which codes/standards are mandated by ER? *(TBD; likely CSA S6, CSA S16, API, ISO marine standards for Canadian marine structures)*
- **Supporting documentation:** What calculations/reports must be referenced on drawings? *(TBD; likely DEL-08.03 calculations, DEL-08.04 geotechnical report, DEL-08.06 berthing energy report)*

**ASSUMPTION:** ER Vol 2 Parts 1-2 contain marine structures requirements; specific clauses/sections TBD pending extraction.

**Sources:**
- Decomposition line 281 ("per ER requirements")
- ER Vol 2 Parts 1-2 PDFs (available in repo; content not yet extracted)

---

### R-003: Document Control / Metadata

**What it requires:**
- Compliance with project document control requirements (numbering, revision, issue status)
- Drawing register/index, title blocks, classification marking: TBD

**Rationale:**
- Document control enables traceability, version control, and approval tracking
- Construction and regulatory approvals require controlled documents with clear revision status
- Project-wide consistency in numbering/revisioning simplifies document management and reduces errors

**Key Considerations:**
- **Drawing numbering scheme:** How are marine structure drawings numbered? *(TBD; typical: discipline code + package code + sequential number, e.g., MAR-08-001)*
- **Revision scheme:** What revision codes are used (A/B/C for internal; 0/1/2 for issued)? *(TBD from project document control procedures)*
- **Title block template:** What information is required in title blocks? *(TBD from project CAD standard; typically: project name, drawing title, drawing number, scale, date, revision, originator, checker, approver, classification)*
- **Drawing register:** What format and content for drawing register/index? *(TBD; typical: spreadsheet or database with drawing number, title, revision, date, issue status)*

**ASSUMPTION:** Project document control procedures exist and are defined in ER or project document control plan; clause/section location TBD.

**Sources:**
- Standard EPC practice for document control
- Project-specific requirements TBD from ER and project document control plan

---

### R-004: Interface Coordination

**What it requires:**
- Show or note interfaces affecting drawing content (tie-ins, envelopes, clearances, load paths, access, penetrations)
- Coordinate with relevant disciplines/packages (even though dependencies are NOT_TRACKED)

**Rationale:**
- Marine structures are an integration point for multiple packages (outfitting, loading system, civil works)
- Uncoordinated interfaces cause construction conflicts, rework, and delays
- Clear interface notation on drawings enables systematic coordination tracking

**Key Considerations:**
- **PKG-09 Marine Outfitting interfaces:**
  - Fender mounting points and reaction loads *(affects platform/trestle structural design and drawing details)*
  - Bollard mounting points and pull-out loads *(affects platform structural design and drawing details)*
  - Ladder/access provisions *(affects GA layouts and detail drawings)*
  - **Coordination status:** TBD; requires interface meeting with PKG-09 lead
- **PKG-11 Marine Loading System interfaces:**
  - Loading arm mounting/support structure *(affects platform structural design, equipment envelopes, loading path)*
  - Operator shelter location and support *(affects platform GA and structural loading)*
  - Leak detection/nitrogen supply routing *(affects platform layout and penetrations)*
  - **Coordination status:** TBD; requires interface meeting with PKG-11 lead
- **Civil/Structural interfaces:**
  - Abutment tie-in details *(affects abutment drawings and trestle end connections)*
  - Access from landside *(affects trestle/platform access design)*
  - Utilities penetrations (power, control, water) *(affects platform/trestle layout and penetration details)*
  - **Coordination status:** TBD; requires interface meeting with civil/structural lead
- **DEL-08.04 Marine Geotechnical Report interface:**
  - Geotechnical parameters (pile capacity, soil layering) *(informs piling layout and pile selection)*
  - Bathymetric survey (seabed levels, obstructions) *(informs piling layout and elevation design)*
  - **Coordination status:** TBD; DEL-08.04 must be completed before final piling layout can be issued

**Practice — Interface Documentation:**
- Show interface points on drawings with dimensions, elevations, coordinate references
- Include interface notes identifying interfacing discipline/package and drawing references (where known)
- Mark TBD interfaces explicitly with notes indicating coordination status (e.g., "Fender mounting points TBD — coordinate with PKG-09 DEL-09.01")
- Track interface coordination status in IDC register or coordination log

**Sources:**
- Standard EPC practice for multi-discipline coordination
- Decomposition scope indicates interfaces to PKG-09 and PKG-11
- `_DEPENDENCIES.md` (mode: NOT_TRACKED; dependencies coordinated externally)

---

### R-005: Technical Content and Notation (Best Practice)

**What it requires:**
- Sufficient technical content for construction and approval: coordinate system/datum, dimensions/elevations, materials/specifications, general notes, legends/symbols

**Rationale:**
- Drawings must be self-sufficient (or clearly cross-referenced) for construction use
- Coordinate system/datum critical for marine structures (positioning, elevation control)
- Dimensions/elevations enable fabrication and construction layout
- Materials/specifications enable procurement and construction compliance
- General notes communicate code compliance, tolerances, welding/fabrication standards

**Key Considerations:**
- **Coordinate system and datum:**
  - What project coordinate system is used (e.g., UTM, local grid)? *(TBD from project survey control basis)*
  - What vertical datum (e.g., chart datum, geodetic datum)? *(TBD; critical for marine structures due to tidal range)*
  - **ASSUMPTION:** Project survey control basis exists; TBD from ER or project procedures
- **Dimensioning standard:**
  - Metric or imperial? *(TBD; ASSUMPTION: metric per Canadian practice)*
  - Tolerances for fabrication and construction? *(TBD from ER, codes, or project standards)*
- **Materials and specifications:**
  - How are materials noted on drawings? *(Typical: material grade/specification noted on drawings or in general notes; detailed specs in DEL-08.02)*
  - Cross-references to DEL-08.02 Marine Structures Technical Specification? *(TBD; recommended practice)*
- **General notes:**
  - What codes/standards govern? *(TBD from R-002 ER review)*
  - Welding/fabrication standards? *(TBD; likely CSA W59 or AWS D1.1; confirm from ER or DEL-08.02)*
  - Inspection requirements? *(TBD from ER or project QA/QC procedures)*
- **Legends and symbols:**
  - What symbols are used for materials, welds, connections, etc.? *(TBD from project CAD standard or CSA/API standard symbol libraries)*

**Sources:**
- Standard marine engineering drawing practice
- Project-specific requirements TBD from ER and project CAD standard

---

## Scope Coverage Checklist

Use this checklist to verify all PKG-08 scope elements (Decomposition line 275) are covered in the drawing set:

| Scope Element | Drawing Coverage Required | Drawing Number(s) | Status |
|---|---|---|---|
| Piling | Piling layout plan (locations, elevations, pile types); pile details; pile schedule | **TBD** | **TBD** |
| Access trestle | Trestle GA (plan, elevation, sections); framing details; support details | **TBD** | **TBD** |
| Loading platform structure | Platform GA (plan, elevation, sections); structural framing; equipment support details | **TBD** | **TBD** |
| Catwalk | Catwalk layout (plan, elevation); support details; handrail/safety details | **TBD** | **TBD** |
| Abutments | Abutment drawings (plan, elevation, sections); tie-in details to landside structures | **TBD** | **TBD** |

**Verification:** For each scope element, confirm that at least one drawing shows the element with adequate detail for construction. If any element is out-of-scope or future phase, document this explicitly.

---

## Interface Coordination Checklist

Use this checklist to track interface coordination for drawing production (even though dependencies are NOT_TRACKED, interfaces must still be managed):

| Interface | Interfacing Package/Deliverable | Information Needed from Interface | Coordination Status | Notes |
|---|---|---|---|---|
| Fender mounting points and loads | PKG-09 / DEL-09.01 Marine Outfitting Design Drawing Set | Fender locations, dimensions, reaction loads, mounting details | **TBD** | Required for platform structural design and drawing details |
| Bollard mounting points and loads | PKG-09 / DEL-09.01 Marine Outfitting Design Drawing Set | Bollard locations, dimensions, pull-out loads, mounting details | **TBD** | Required for platform structural design and drawing details |
| Ladder/access provisions | PKG-09 / DEL-09.01 Marine Outfitting Design Drawing Set | Ladder locations, dimensions, support details | **TBD** | Required for GA layouts and detail drawings |
| Loading arm mounting/support | PKG-11 / DEL-11.01 Marine Loading Design Drawing Set | Loading arm location, envelope, mounting details, loads | **TBD** | Required for platform structural design and equipment support details |
| Operator shelter support | PKG-11 / DEL-11.01 Marine Loading Design Drawing Set | Shelter location, dimensions, support loads | **TBD** | Required for platform GA and structural loading |
| Leak detection/nitrogen routing | PKG-11 / DEL-11.01 Marine Loading Design Drawing Set | Routing paths, penetration locations, support requirements | **TBD** | Required for platform layout and penetration details |
| Abutment tie-in details | Civil/Structural Works | Abutment dimensions, elevations, connection details | **TBD** | Required for abutment drawings and trestle end connections |
| Landside access provisions | Civil/Structural Works | Access path locations, dimensions, clearances | **TBD** | Required for trestle/platform access design |
| Utilities penetrations | Civil/Structural Works | Penetration locations, sizes, routing | **TBD** | Required for platform/trestle layout and penetration details |
| Geotechnical parameters | DEL-08.04 Marine Geotechnical Report | Pile capacity, soil layering, design parameters | **TBD** | Required for piling layout and pile selection |
| Bathymetric survey | DEL-08.04 Marine Geotechnical Report | Seabed levels, existing obstructions, survey datum | **TBD** | Required for piling layout and elevation design |

**Practice:** Use IDC meetings or coordination logs to track and resolve interfaces. Update this checklist as interfaces are confirmed.

---

## Trade-offs and Decisions (TBD)

Trade-off criteria and required documentation are **TBD** until ER clauses and project decision-capture practices are available in references. Typical trade-offs for marine structures drawings (to be confirmed):

### Drawing Detail Level vs Number of Drawings
- **Trade-off:** More detailed drawings provide better construction guidance but increase drawing count and maintenance effort
- **Consideration:** Balance detail level with drawing count; use typical details and standards notes to reduce repetition
- **Decision:** **TBD** (pending project CAD standard and ER requirements)

### Constructability vs Maintenance Access
- **Trade-off:** Optimal construction sequence may conflict with optimal maintenance access
- **Consideration:** Show access provisions, removable panels, lifting points for maintenance
- **Decision:** **TBD** (pending ER maintenance requirements and constructor input)

### Modular vs Stick-Built Construction
- **Trade-off:** Modular construction (pre-fabricated sections) can reduce on-site work but requires more detailed fabrication drawings and transportation planning
- **Consideration:** Show modular boundaries, connection details, lifting/rigging points if modular approach is used
- **Decision:** **TBD** (pending construction methodology and ER requirements)

---

## Conflict Table (for human ruling)

No conflicts identified from sources currently present in this deliverable folder.

If conflicts arise during drawing production (e.g., contradictory ER requirements, interface coordination issues), document them here for human ruling:

| Conflict ID | Conflict (short statement) | Source A (file + section) | Source B (file + section) | Impacted sections | Proposed authority (PROPOSAL) | Human ruling (TBD) |
|---|---|---|---|---|---|---|
| *(none)* | - | - | - | - | - | - |

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.01_Marine_Structures_Design_Drawing_Set/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.01 at line 281)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard marine engineering practice (for interface coordination, drawing content, technical notation)
