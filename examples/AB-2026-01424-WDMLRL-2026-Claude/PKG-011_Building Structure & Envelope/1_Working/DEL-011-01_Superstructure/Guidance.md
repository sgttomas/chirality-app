# Guidance: DEL-011-01 Concrete Superstructure

---

## Purpose

DEL-011-01 is the primary structural deliverable of PKG-011. It produces the concrete structural frame and deck system of the New North Shop Addition -- the physical shell within which all other packages (mechanical, electrical, plumbing, crane installation, interior fit-out) will operate. Without a completed and inspected superstructure, no downstream construction can progress.

This deliverable directly supports:
- **OBJ-001**: Deliver a code-compliant, fully functional maintenance shop addition. The superstructure must enclose and structurally support all program elements described in RFP §3.1 and §3.4.
- **OBJ-002**: Complete all work on or before December 31, 2026. The superstructure is on the critical path; its timely completion gates all other construction packages.

Source: Decomposition §5 (OBJ-001, OBJ-002); RFP §3.1, §3.4.

---

## Principles

### P1 -- The superstructure is the critical-path item
The concrete superstructure gates virtually all other construction in PKG-011 through PKG-018. Delays to the structural frame directly compress time available for mechanical, electrical, plumbing, crane, and fit-out trades. Schedule risk to DEL-011-01 is schedule risk to OBJ-002. (Source: Decomposition OBJ-002; RFP §3.1 deadline)

### P2 -- IFC drawings must precede field work
The structural design (DEL-002 series, particularly DEL-002-02 through DEL-002-10) must be complete, P.Eng.-stamped, and issued before construction begins. Proceeding without IFC drawings is a code violation and an OH&S risk. (Source: RFP §3.3.2, SOW-0018)

### P3 -- Foundation interface must be confirmed before erection
The superstructure bears on the foundation (DEL-010-01). Foundation as-built dimensions, bearing capacity, and anchor bolt locations must be verified before the structural frame is erected. Discrepancies between design and as-built foundation conditions require engineer resolution before proceeding. (Source: _DEPENDENCIES.md upstream: PKG-010)

### P4 -- Embedded items cannot be installed retroactively
Steel plate embedments (SOW-0024, DEL-011-02), service pit/trench geometry (SOW-0028), plumbing rough-in sleeves, and electrical conduit sleeves are permanent items that must be positioned and inspected before concrete is placed. Errors discovered after pours are extremely costly or impossible to correct. The GC must coordinate with all trade packages before each pour. (Source: RFP §3.4; App B; ASSUMPTION: standard concrete construction coordination practice)

### P5 -- Crane runway geometry is precision-critical
The crane runway beams must be installed to the elevation and alignment tolerances specified by the crane manufacturer (DEL-016-01). If runway geometry is incorrect, crane installation cannot proceed and rectification after concrete has cured may be structurally difficult. Crane manufacturer requirements should be incorporated into the IFC drawing set before the structural frame is cast or erected. Specific alignment tolerances (span, elevation, levelness) must be obtained from the crane manufacturer and documented in the IFC drawings. (Source: RFP §3.4; App B "5 TON CRANE" x 2; SOW-0067; DEL-002-07; _SEMANTIC_LENSING.md F-001)

### P6 -- The 35 ft ceiling height is a program requirement, not a target
The 35 ft clear ceiling is explicitly stated in the RFP design requirements and shown on the conceptual drawing. It is required to accommodate the two 5-tonne overhead cranes on trolleys and large equipment (motor scraper class) operating in the bays. This dimension must be treated as a minimum design parameter by the Structural Engineer of Record. (Source: RFP §3.4 "Concrete structure 35' ceiling"; App B note; SOW-0022)

---

## Considerations

### C1 -- Structural system selection (concrete specifics TBD)
The RFP specifies "concrete structure" and the conceptual drawing confirms "Concrete Structure (35' Ceiling)." However, the specific concrete structural system -- cast-in-place, tilt-up panels, precast, or a hybrid -- is not prescribed in the RFP. This determination rests with the Structural Engineer of Record, subject to geotechnical conditions (DEL-008-01), local supply chain, and the December 31, 2026 schedule constraint.

Whether "concrete structure" prescriptively requires all-concrete or permits hybrid steel/concrete structural systems (e.g., steel roof deck on concrete walls) is ambiguous. The Structural Engineer of Record should confirm whether a hybrid system satisfies the RFP intent. (Source: _SEMANTIC_LENSING.md A-001; RFP §3.4)

- ASSUMPTION: Tilt-up or precast may offer schedule advantages in the Alberta market. The design team should evaluate early.
- Source: RFP §3.4; App B; Decomposition §3 SOW-0022

### C2 -- Geotechnical uncertainty affects superstructure design
The structural design (particularly column loads, floor slab thickness, and foundation-to-superstructure interface) depends on geotechnical investigation results (DEL-008-01). Until the geotech report is available, some structural design parameters will carry assumptions about normal ground conditions. The RFP explicitly acknowledges this for foundation pricing (RFP §4.8.2). The structural design team should flag any geotech-dependent assumptions in their calculation package (DEL-002-10). (Source: RFP §4.8.2; SOW-0019)

### C3 -- Mezzanine load classification requires early definition
The mezzanine must be "capable of handling heavy items such as several oil totes and oil pumping equipment" (RFP §3.4). Oil totes typically weigh approximately 1,000 kg (2,200 lb) each when full; pumping equipment adds additional point loads. The Structural Engineer of Record must establish a design live load (e.g., kPa or psf) early in design so the mezzanine structure and its supports can be sized accordingly. ASSUMPTION: The design load will likely exceed the minimum residential/light storage live load; a heavy storage or industrial live load classification is probable. (Source: RFP §3.4; App B "Load Bearing Over Parts Room + Utility For Storage")

### C4 -- Service pit ventilation and lighting are mechanical/electrical interfaces
REQ-011-01-07 requires the service pit to include provisions for ventilation and lighting. The structural scope creates the pit geometry; the installation of ventilation (PKG-013) and lighting (PKG-015) within the pit is a downstream trade scope. The GC must ensure that the structural design includes adequate conduit/duct sleeves and access provisions, coordinated with the mechanical and electrical IFC drawings before the pit is formed. Verification must confirm that ventilation duct openings/sleeves and lighting conduit sleeves are installed per MEP coordination drawings before concrete placement. (Source: RFP §3.4; SOW-0028; PKG-013, PKG-015; _SEMANTIC_LENSING.md X-004)

### C5 -- Wash bay structural scope boundary
Per the decomposition, the wash bay structural enclosure (walls, roof, overhead door opening, steel plate floor) is assigned to DEL-011-05 under SOW-0027a. DEL-018-05 covers the drainage infrastructure (floor drains, mud sump connection, exterior mud sump). The GC must ensure that drain sleeve and sump connection locations are incorporated into the structural concrete before the wash bay floor is poured.

Note: The previous version of this document attributed the wash bay structural enclosure to DEL-011-01. Per decomposition SOW-0027a mapping, DEL-011-05 is the correct reference. See CONF-011-01-003 below for the conflict record and proposed resolution. (Source: RFP §3.4; App B; SOW-0027a, SOW-0027b; Decomposition §7 PKG-011; _SEMANTIC_LENSING.md B-003)

### C6 -- County representative presence at all inspections
All structural inspections must be scheduled to accommodate the County project representative (RFP §3.3.2; SOW-0084). The GC is responsible for coordinating inspection scheduling with the County PM. Failure to have the County representative present may require repeat inspections. This has schedule implications that must be managed proactively. (Source: RFP §3.3.2; SOW-0084, SOW-0085)

### C7 -- Surety and insurance must be in place before construction begins
The Performance Bond, Labour and Material Payment Bond, and all insurance coverage must be in place before site work commences (RFP §2.12; SOW-0099 through SOW-0103). This is a commercial prerequisite to DEL-011-01 construction, managed under PKG-021. (Source: RFP §2.12; SOW-0099-SOW-0103)

### C8 -- Roof structure system selection
The roof structure is a major component of the superstructure but receives less analytical attention than the wall/column system. The specific roof system (concrete, steel deck on bar joists, pre-engineered metal, or other) is TBD per structural design. The roof system choice must be integrated with:
- The 35 ft minimum interior clear ceiling height requirement (REQ-011-01-01)
- The crane runway beam system (REQ-011-01-10), since roof structure interacts with column spacing and lateral bracing
- The building envelope and cladding system
The Structural Engineer of Record should evaluate roof system options as part of the overall structural system selection (C1). (Source: RFP §3.4; App B; _SEMANTIC_LENSING.md E-001)

### C9 -- Structural subcontractor qualification expectations
The Procedure addresses the General Contractor and their structural subcontractor(s), but no document currently specifies what qualifications the structural subcontractor must hold (e.g., COR certification, concrete work experience, specific trade certifications). ASSUMPTION: Structural subcontractor qualifications should be addressed during pre-construction coordination and documented as part of the GC's quality management program. The Owner/County may have specific prequalification requirements. (Source: _SEMANTIC_LENSING.md E-002; Procedure Purpose)

### C10 -- Cold-weather and hot-weather concreting provisions
Alberta's central region climate (cold winters, potential for hot summer days) requires specific provisions for concrete placement and curing. Cold-weather concreting (temperature monitoring, heated enclosures, curing protection) and hot-weather concreting (retarders, shading, accelerated curing) must be addressed in the construction plan. Specific provisions should reference CSA A23.1 cold/hot weather clauses once the standard is confirmed as applicable. (Source: _SEMANTIC_LENSING.md A-004; Datasheet Conditions -- Climate zone; ASSUMPTION: CSA A23.1 applicable)

---

## Trade-offs

| Trade-off | Option A | Option B | Consideration | Source |
|---|---|---|---|---|
| Structural system type | Cast-in-place concrete (slower, high site labour) | Tilt-up or precast panels (faster erection, more plant fabrication) | Schedule constraint (Dec 31, 2026) favours faster erection; geotech and local supply chain availability must be assessed | RFP §3.4; App B; ASSUMPTION |
| Roof structure system | Concrete roof (consistent with all-concrete system) | Steel deck on bar joists or pre-engineered (lighter, potentially faster, but "concrete structure" interpretation per A-001) | Must integrate with 35 ft ceiling and crane runway; structural engineer to evaluate alongside wall/column system; see C1 and C8 | RFP §3.4; _SEMANTIC_LENSING.md E-001; ASSUMPTION |
| Mezzanine framing | Concrete topping on steel joists/deck | Cast-in-place concrete slab on structural supports | Either viable; steel may be faster; concrete offers heavier load capacity; structural engineer to determine based on design loads | RFP §3.4; App B; ASSUMPTION |
| Service pit liner | Cast-in-place concrete walls and floor | Precast pit liner units | Local availability and geometry constraints will drive this; either must satisfy structural and chemical resistance requirements for shop drainage | RFP §3.4; App B; ASSUMPTION |
| Phasing | Construct superstructure as single phase | Phase pour (slab separately from walls/columns/roof) | Single phase may be faster; phased pours allow earlier access for embedded item inspection; structural engineer to advise based on system selected | ASSUMPTION |

---

## Examples

No precedent examples from accessible sources. The conceptual floor plan in Appendix B (R-04) is the primary spatial reference available at this stage. Full structural details will be established in the DEL-002 design package.

---

## Vocabulary Notes

### "Overhead doors" scope boundary
The term "overhead doors" is used across documents with varying scope implications. For clarity within DEL-011-01:
- **Structural rough openings and framing** (lintels, headers, jamb framing) for overhead doors are within DEL-011-01 scope (REQ-011-01-11).
- **Overhead door supply and installation** (door panels, tracks, operators, hardware) is under DEL-011-03 (repair bays) and DEL-011-05 (wash bay) per decomposition.
- The term "overhead doors" in Specification and Procedure refers to the structural rough openings unless explicitly noted otherwise.
- Preferred terminology in these documents: "structural rough openings for overhead doors" when referring to DEL-011-01 scope; "overhead door supply/install" when referring to DEL-011-03/DEL-011-05 scope.

(Source: _SEMANTIC_LENSING.md C-003; Decomposition §7 PKG-011)

### "Steel plate embedments" -- design vs. field tracking
- **DEL-002-08** is the design drawing (structural embedment plan) showing locations, sizes, and specifications.
- **DEL-011-02** is the field installation tracking/documentation deliverable covering the actual placement verification.
- References to "DEL-002-08" in Specification and Procedure refer to the design authority; references to "DEL-011-02" refer to field tracking records.

(Source: _SEMANTIC_LENSING.md X-005; Decomposition §7 PKG-011)

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-011-01-001 | Appendix B notes state "50,000L Water Storage" is located inside the New North Shop footprint (near stairs to mezzanine). The cistern is assigned to PKG-014 (plumbing). The structural concrete superstructure (DEL-011-01) must provide the structural enclosure and floor/wall penetrations for the cistern, but the scope boundary between structural (DEL-011-01) and plumbing (DEL-014-01) for cistern installation is not explicitly defined. | App B (cistern shown inside building footprint); Decomposition PKG-011 exclusions | Decomposition PKG-014 (cistern in plumbing) | Specification REQ-011-01-18 (cistern provisions); Specification Scope; Procedure Step 4 coordination; Datasheet Construction (cistern provisions) | PROPOSAL: Structural rough-in (slab penetration, structural support if required) falls under DEL-011-01; cistern supply and install falls under DEL-014-01. Confirm at pre-construction coordination meeting. | TBD |
| CONF-011-01-002 | RFP §3.4 lists "Concrete structure 35' ceiling" and Appendix B confirms this. The RFP §3.1 refers to "approximately 13000 square feet" useable area. The building footprint per App B scales to approximately 130' x 100' = 13,000 sq ft for the new addition. However, whether the 13,000 sq ft figure refers to the new addition only or includes the renovated Old North Shop area is ambiguous. REQ-011-01-02 should state unambiguously which area is measured. | RFP §3.1 ("approximately 13000 square feet"); App B (130' x 100' new shop) | RFP §3.1 overall project description including renovation reference | Specification REQ-011-01-02; Datasheet Attributes | PROPOSAL: 13,000 sq ft refers to the New North Shop addition only (130' x 100'), consistent with App B dimensions. Old North Shop renovation is separate scope (PKG-017). Confirm with County. Specification REQ-011-01-02 to state "New North Shop addition" explicitly upon confirmation. (Source: _SEMANTIC_LENSING.md E-003) | TBD |
| CONF-011-01-003 | Wash bay structural enclosure scope attribution is inconsistent between Specification and decomposition. Previous Specification REQ-011-01-06 listed the wash bay structural enclosure under DEL-011-01 scope. The decomposition assigns SOW-0027a (wash bay structural enclosure) to DEL-011-05. These are inconsistent. | Decomposition §7 PKG-011: SOW-0027a -> DEL-011-05 | Previous Specification DEL-011-01 REQ-011-01-06 (wash bay enclosure under DEL-011-01) | Specification REQ-011-01-06; Specification Scope; Datasheet Wash bay attribute; Guidance C5 | PROPOSAL: Per decomposition, wash bay structural enclosure is DEL-011-05. REQ-011-01-06 should be revised to cover only the DEL-011-01 coordination/integration points with DEL-011-05 (structural connections, roof integration, interface details). Confirm with decomposition owner. (Source: _SEMANTIC_LENSING.md B-003) | TBD |
