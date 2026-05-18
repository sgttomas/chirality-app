# Guidance — DEL-011-05 Wash Bay Enclosure

**Deliverable ID:** DEL-011-05
**Deliverable Name:** Wash Bay Enclosure
**Package:** PKG-011 Building Structure & Envelope
**Revision:** Draft P3 — 2026-02-26

---

## Purpose

The wash bay enclosure exists to provide a dedicated, weathertight, enclosed space for washing large-scale landfill equipment — up to and including motor scraper class — within the New North Shop addition. This function is distinct from the general shop repair bays: the wash bay is sized and configured to contain high-pressure wash-down of heavy equipment, with floor drains and an exterior mud sump managing wash effluent (see DEL-018-05 for drainage infrastructure).

The enclosure is a structural and envelope component of PKG-011, not a MEP or fitout component. Its primary purpose is to form the physical shell — walls, roof, overhead door, and reinforced floor — within which MEP systems are subsequently installed by other packages. Getting this shell right, early, and to IFC drawings is the primary driver.

Source: RFP §3.1, §3.4 (R-01); Decomposition SOW-0027a; _CONTEXT.md.

---

## Principles

**1. Shell-first, systems-follow sequencing.**
The wash bay enclosure is an upstream dependency for the drainage and plumbing work (DEL-018-05) and the electrical lighting and door power (DEL-015-02, DEL-015-04). The enclosure — including any floor penetrations and wall sleeves — must be completed and coordinated before those trades can finalize their work. This means the concrete floor pour with embedded drain sleeves and steel plates must be coordinated precisely with the plumbing and civil design (PKG-006, PKG-005) before the floor is poured. Once concrete is placed, penetrations cannot be easily added.

Source: _DEPENDENCIES.md (DEL-011-01 upstream, PKG-013 downstream); RFP §3.3.2 (IFC drawings required before construction).

**2. The 24 ft width is an equipment-driven constraint.**
The RFP specifies the wash bay for motor scraper-sized equipment. The 24 ft width shown in App B (R-04) is consistent with the two repair bays also shown at 24 ft. This width is a minimum clearance for the intended equipment class and should not be reduced. The Structural Engineer must confirm clear opening vs. structural framing dimensions.

Source: RFP §3.1, §3.4, App B (R-04).

**3. The mezzanine above creates a load interaction.**
The mezzanine above the wash bay is described as load-bearing for heavy items (oil totes, pumping equipment). The wash bay walls and roof structure must therefore be designed to transfer mezzanine loads as part of the overall structural system. The Structural Engineer (DEL-002 package) will govern this through IFC drawings; the General Contractor must build to those drawings without modification.

Source: RFP §3.4, App B (R-04).

**4. The steel plate embedment is a concrete-pour-time requirement.**
The steel plate(s) shown in the wash bay floor on App B (R-04) must be positioned and embedded during the concrete pour — they cannot be surface-applied after the fact. The embedment plan (DEL-002-08) must be available and confirmed before the floor pour proceeds.

Source: RFP §3.4, App B (R-04); Decomposition DEL-002-08.

**5. IFC dependency is pervasive — plan for contingencies.**
Multiple requirements and construction elements in this deliverable depend on IFC drawings that do not yet exist (door height, steel plate specifications, wall construction material, clear ceiling height, drainage slope). If IFC drawings are delayed or unavailable for specific elements, the General Contractor should have a clear protocol for how to proceed — whether that means a stop-work protocol for affected elements, an alternative approval path (e.g., preliminary engineering sketches with Architect/Engineer written approval), or an RFI process to obtain interim direction. Without such a protocol, the contractor cannot comply with requirements that reference nonexistent documents. [D-001]

Source: RFP §3.3.2 (IFC drawings requirement); Specification REQ-011-05-008; multiple REQ notes referencing "TBD pending IFC."

---

## Considerations

**Coordination with drainage (DEL-018-05 / SOW-0027b):**
The wash bay drainage infrastructure — floor drains, connection piping to the exterior mud sump — is scoped to DEL-018-05, not this deliverable. However, the concrete floor pour for the wash bay must include the drain sleeves and any embedded drain bodies. This creates a hard coordination dependency: the plumbing design (PKG-006) must be finalized and the drain locations confirmed before the floor is poured. Failure to pre-install sleeves will require saw-cutting or core-drilling through the structural floor, which is disruptive and may affect structural integrity and the steel plate embedments. **Cost/schedule consequence**: core-drilling a structural slab post-pour typically requires a structural assessment (additional engineering cost), causes schedule delays while the assessment is conducted and repairs are made, and risks compromising embedded steel plate anchorages if drill paths intersect plate embedments. For a project with a fixed December 31, 2026 deadline, this coordination failure could create a critical-path delay. The GC should treat the drain-sleeve/steel-plate coordination as a critical procurement and scheduling milestone. [F-003]

**Floor drainage slope:**
The wash bay floor must drain to floor drain locations shown on App B. This requires a drainage slope that must be coordinated with the plumbing design (PKG-006) and civil design (PKG-005) before formwork is set. The slope direction and minimum gradient affect the steel plate embedment elevations (plates must remain level while the surrounding slab slopes) and the formwork geometry. This coordination input must be resolved before the floor pour proceeds. [F-002]

**Overhead door height:**
The RFP and App B confirm a 24 ft wide overhead door but do not explicitly state a door height. For motor scraper-class equipment, door height is typically 16–20 ft (ASSUMPTION). The Architect and Structural Engineer must confirm the door height on IFC drawings. The door height affects the wall framing and structural header above the opening.

**Wash bay clear ceiling height:**
The building has a 35 ft ceiling (concrete structure), but the wash bay has a mezzanine above it. The clear ceiling height within the wash bay — the distance from the finished floor to the underside of the mezzanine floor structure — is not stated in the RFP or App B. This dimension is critical for motor scraper-class equipment access and must be confirmed on IFC drawings. If the clear height is insufficient for the intended equipment, the mezzanine floor elevation or structural depth may need adjustment. [C-001]

**Electrical rough-in provisions:**
While electrical installation is out of scope for this deliverable, the enclosure construction must include conduit stubs or sleeves at locations specified by the electrical IFC drawings (PKG-004) for overhead door operators and lighting mount points. The General Contractor should confirm these locations with the electrical subcontractor before wall and ceiling framing is completed. Note: electrical coordination is referenced in Procedure Steps 1.4, 2.5, 3.3, and 6.2 with varying levels of specificity. A single electrical coordination protocol or checklist (developed with the electrical subcontractor at project start) would reduce the risk of missed conduit locations and inconsistent coordination. [X-002]

**Mezzanine access (DEL-011-07 interface):**
The mezzanine above the wash bay is accessed via stairs located in the utility room / mezzanine area adjacent to the wash bay, as shown in App B. This deliverable does not include the stairs or mezzanine framing (those are DEL-011-07), but the wash bay structural walls must accommodate the mezzanine framing connections.

**Exterior mud sump location (interface only):**
App B (R-04) shows the mud sump exterior to the east wall of the building, labelled "Wash Bay Mud Sump." The enclosure east wall must include the penetration or opening for the drain pipe connection to the mud sump. This is a coordination item between DEL-011-05 (the wall) and DEL-018-05 (the drainage pipe and sump).

**Gantry provisions (conditional):**
App B shows a "Gantry" label at the south end of the wash bay. If the gantry is confirmed by the Owner/equipment design team, the enclosure walls and/or roof must accommodate structural provisions for the gantry (mounting points, load transfer, clearance). Currently, no requirement or verification exists for gantry provisions because the gantry itself is an ASSUMPTION requiring confirmation. If confirmed, a new requirement should be added to the Specification and verification approach defined. [B-002, X-003]

**As-built documentation expectations:**
The Specification Documentation section lists "As-built survey / drawings" (SOW-0004, DEL-008-04) as a required deliverable, but no specific guidance exists on what level of as-built detail is expected for the wash bay enclosure. As-built documentation should record all deviations from IFC drawings discovered during construction, including: (a) actual dimensions vs. IFC dimensions for key elements (bay width, door opening, steel plate locations, drain sleeve locations); (b) any field-directed changes via RFI or Architect/Engineer written direction; (c) format and submittal timing per the contract administrator's requirements. [X-001]

**Guarantee period — warranty-risk elements:**
REQ-011-05-010 establishes a 2-year guarantee period per RFP §2.10. For the wash bay enclosure specifically, the elements most likely to require warranty claims during the guarantee period include: (a) the overhead door mechanism and operator (motorized components subject to wear, especially in a high-moisture wash environment); (b) weatherseals at the door sill, jambs, and wall/roof junctions (exposure to water and temperature cycling); (c) steel plate embedment integrity (potential for plate shifting or debonding under repeated heavy equipment loading). The GC should ensure these elements receive particular attention during pre-CCC quality inspection (see Specification REQ-011-05-010 verification) and that manufacturer warranties for the overhead door operator are aligned with the contractual guarantee period. [D-002]

---

## Trade-offs

| Trade-off | Options | Preferred Direction | Source |
|---|---|---|---|
| Drain sleeve timing | Pre-install during floor pour vs. core-drill after | Pre-install during floor pour — avoids structural disruption, protects steel plate embedments, and avoids cost/schedule impact of post-pour remediation [F-003] | RFP §3.4, App B — steel plates and drains both in floor |
| Overhead door type | Manual chain-hoist vs. motorized | Motorized (ASSUMPTION) — consistent with repair bay doors and the scale of equipment being washed | App B (R-04); RFP SOW-0025 context |
| Wall construction material | Concrete tilt-up / CMU / steel-stud with cladding | TBD — to be determined by Architect and Structural Engineer on IFC drawings [B-003] | RFP §3.4 (concrete structure) |

---

## Examples

No worked examples are available from accessible sources for this specific deliverable. Guidance is derived from RFP requirements and App B conceptual drawings only.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| C-01 | **Steel plate scope ownership**: SOW-0027a scope statement includes "steel plate floor" as part of the wash bay enclosure, but the steel plate embedment plan and specification are governed by DEL-011-02 (Steel Plate Floor Embedments, SOW-0024). It is unclear whether the wash bay steel plate is captured under DEL-011-02 (building-wide steel plates) or is a distinct item under DEL-011-05, or both. Both deliverables reference steel plate installation, creating risk of double-counting or omission. [E-001] | Decomposition SOW-0027a / DEL-011-05 definition | Decomposition SOW-0024 / DEL-011-02 definition | Specification REQ-011-05-005; Datasheet Attributes (Steel plate floor, Steel plate dimensions); Procedure Step 2.4 (steel plate embedment installation) | PROPOSAL: The wash bay floor steel plate is part of the wash bay enclosure scope (SOW-0027a) but the embedment design is governed by DEL-002-08 (Structural). DEL-011-02 covers building-wide plates; DEL-011-05 is responsible for installing the wash bay plate(s) per the embedment plan. Confirm with GC and Structural Engineer. The verified execution documentation must identify a single responsible deliverable to avoid double-counting or omission. | TBD |
| C-02 | **Mezzanine boundary**: The mezzanine above the wash bay is referenced in SOW-0027a ("roof integration") and in SOW-0032/0033 (DEL-011-07 Mezzanine Structure & Stairs). The boundary between the wash bay roof/structural provision (DEL-011-05) and the mezzanine framing (DEL-011-07) is not precisely defined in the decomposition. The precise interface — which connection details belong to which deliverable — must be specified to determine completeness of each deliverable. [E-002] | Decomposition SOW-0027a | Decomposition SOW-0032, SOW-0033, DEL-011-07 | Specification REQ-011-05-006; Procedure coordination steps (Steps 4.1, 4.2) | PROPOSAL: DEL-011-05 provides the structural walls and support for the mezzanine level; DEL-011-07 provides the mezzanine floor framing, decking, and stairs. The interface (connection detail between wash bay walls and mezzanine framing) should be defined on IFC structural drawings. Verified audit documentation requires a clear scope boundary to determine completeness. | TBD |
