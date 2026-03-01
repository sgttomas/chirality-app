# Guidance — DEL-002-04 Structural Sections & Details

---

## Purpose

Structural Sections & Details drawings translate the structural framing plans (DEL-002-03) and design calculations (DEL-002-10) into construction-ready instructions. They exist because plan views alone cannot communicate the full three-dimensional geometry, connection conditions, reinforcing configurations, and interface conditions required to build a concrete structure safely and to code.

For this project, structural sections and details are particularly critical because:
1. The 35 ft clear ceiling height for a concrete structure is demanding — sections must fully communicate the wall-to-roof interface, column geometry, and lateral resistance strategy.
2. Multiple specialized structural elements coexist in a compact footprint: two 5-Tonne Overhead Crane runway beams, a below-grade service pit, a motor scraper-scale wash bay, a heavy-duty load-bearing mezzanine, and numerous steel plate floor embedments. Each requires purpose-engineered detailing.
3. The IFC drawing set must be complete before construction commences and must pass inspection by the Authority Having Jurisdiction (AHJ) in Alberta.

Source: R-01 §3.3.2, §3.4; decomposition OBJ-001, OBJ-003.

---

## Principles

### P-01 — Sections Are Derived from, Not Independent of, the Calculation Package
All member sizes, reinforcing bar sizes and spacings, embedment depths, and connection capacities shown on the detail drawings must be traceable to DEL-002-10 (Structural Calculation Package). Do not finalize sections before calculations are complete for the relevant structural elements.
Source: Standard structural engineering practice; R-01 §3.3.2 (IFC stamping requirement implies completed design).

### P-02 — Coordinate Section Cuts with Framing Plans Before Drawing
Section cut lines shown on DEL-002-03 (Structural Framing Plans) must correspond directly to sections in this deliverable. Establish the section cut schedule jointly with the framing plan set to avoid orphaned cuts or missing sections.
Source: ASSUMPTION — standard drawing coordination practice.

### P-03 — Concrete Construction Method Drives Detail Types
The RFP specifies a "concrete structure" but does not prescribe the construction method (tilt-up, cast-in-place, precast, hybrid). The detail types required differ substantially depending on the method chosen:
- Cast-in-place: form ties, construction joints, rebar splice details, pour sequence notes
- Tilt-up: panel lift inserts, temporary brace details, ledger connections
- Precast: bearing details, grout pockets, connection hardware
The Structural Engineer should resolve the construction method with the General Contractor early in design development, as this decision affects architectural sections (PKG-001), mechanical/plumbing sleeve coordination (PKG-003, PKG-006), and permit document content.
Source: ASSUMPTION — RFP §3.4 states "concrete structure" only; construction method TBD.

### P-04 — Service Pit Requires Special Attention for Waterproofing and Drainage Interface
The service pit is a below-grade structure in a cold Alberta climate. While the structural sections define the concrete elements, they must include provision for:
- Waterproofing membrane interface details (typically coordinated with architectural or civil)
- Floor drain or sump connection penetrations
- Ventilation and lighting penetration sleeves

**Waterproofing and Drainage Discipline Responsibility (lensing item C-003):**
The responsibility boundary for waterproofing design at the service pit is not explicitly assigned in accessible sources. The structural sections must accommodate the waterproofing membrane interface, but the waterproofing design itself (membrane selection, application method, drainage layer) is typically owned by either the architectural or civil discipline. The Design-Builder should assign discipline responsibility for:
- Waterproofing membrane specification and detailing
- Sub-slab drainage system design (if required by geotech conditions)
- Coordination of membrane termination details with the structural concrete elements

Until responsibility is assigned, this deliverable (Procedure Step 7) should show the structural provision for the membrane interface (e.g., keyway, waterstop, membrane turn-up detail) as TBD pending the responsible discipline's input. **Proposed authority: Design-Builder to assign discipline responsibility.**

Source: R-01 §3.4 (ventilated and lighted service pit); ASSUMPTION for waterproofing — cold climate/below-grade practice.

### P-05 — Crane Runway Beam Details Require Crane Supplier Input
The crane runway beam cross-section, connection to building columns or dedicated runway columns, and rail fastening details depend on the crane manufacturer's requirements (rail size, load distribution, end stop requirements). Final crane support details (this deliverable or DEL-002-07) should not be issued for construction until the crane supplier is confirmed.
Source: R-01 §3.4 (two 5-tonne overhead cranes); ASSUMPTION — standard crane runway design practice.

### P-06 — Mezzanine Design Load Must Be Explicitly Stated on Drawings
Because the RFP describes the mezzanine load requirement in functional rather than numerical terms ("heavy items such as oil totes and pumping equipment"), the Structural Engineer must establish and document the governing design live load on the drawings. This creates a clear record for the Owner, contractor, and future users of the mezzanine capacity limits.
Source: R-01 §3.4; ASSUMPTION — standard practice for owner communication.

### P-07 — Geotechnical Report Findings Must Inform Structural Section Details (ASSUMPTION)
The Procedure lists the geotechnical report (DEL-008-01) as a prerequisite and the Datasheet notes "normal ground conditions assumed" for estimation purposes. However, once the geotechnical investigation is complete, specific findings must be integrated into the structural sections:

- **Soil bearing capacity** affects service pit wall design, including lateral earth pressure on retaining walls and required wall thickness/reinforcing.
- **Groundwater level** affects the need for waterproofing, underdrain provisions, and hydrostatic load on the pit floor slab.
- **Frost depth** affects foundation interface details and the depth at which below-grade structural elements must be protected.
- **Soil classification** may affect backfill requirements around pit walls and any temporary shoring needed during construction.

The Structural Engineer should establish a checklist of geotechnical parameters required for this deliverable's structural sections and confirm these parameters are addressed in the geotechnical report before finalizing below-grade details (particularly Steps 7 and 5 in the Procedure).

Source: Datasheet Conditions (foundation pricing row); Procedure Prerequisites (Geotech row); ASSUMPTION — standard structural design practice (lensing item D-001).

---

## Considerations

### C-01 — Drawing Organization: Combined vs. Dedicated Detail Sheets
The PKG-002 deliverable list includes DEL-002-04 (Sections & Details) alongside five dedicated detail deliverables (DEL-002-05 through DEL-002-09). In practice, structural engineers often consolidate common details on generalized sheets and reserve dedicated sheets for complex elements. Either approach is acceptable provided:
- All elements required by SOW-0012 are detailed somewhere in the PKG-002 drawing set.
- Cross-references between sheets are clear and complete.
- The drawing index accounts for where each element is detailed.

### C-02 — Section Cut Selection Strategy
Priority section cuts for this building type and program:
- Transverse building section (cutting through repair bays) — establishes overall structure height, bay widths, wall/roof interface
- Section through wash bay — shows overhead door opening, wall/roof integration, steel plate floor
- Section through service pit — shows below-grade depth, wall thickness, floor slab, pit floor drain
- Longitudinal section — shows crane runway elevation, mezzanine level, interior clear height variation
- Mezzanine section — shows floor system, connection to supporting structure

### C-03 — Steel Plate Embedment Detail Complexity
The Appendix B floor plan shows multiple "Steel Plate" rows in the main shop and wash bay areas. The plates appear to be embedded in the floor slab at strategic positions to protect the concrete from tracked and packer equipment (e.g., compactor, motor grader tracks). Key design questions not resolved by available sources:
- Plate thickness and plan dimensions (TBD)
- Whether plates are flush, recessed, or raised (TBD)
- Anchoring mechanism to the slab (welded studs, rebar, drilled anchors — TBD)
- Whether plates are in the service pit floor as well (TBD)
These questions should be resolved with the Owner/County before detail drawings are finalized.

### C-04 — Gantry Annotation in App B (Terminology Normalization)
Appendix B shows two "Gantry" annotations (one in the main shop, one in the wash bay area). Per the decomposition Vocabulary Map (D-001), "Gantry" and "5-Tonne Overhead Crane" refer to the same equipment. **Canonical term for all deliverable documents: "5-Tonne Overhead Crane."** "Gantry" is the App B alias and should only appear when quoting source text directly. This normalization has been applied across all four documents in this deliverable (lensing item B-004).

### C-05 — Foundation Interface at Bottom of Structural Sections
Structural sections showing wall and column elements must clearly indicate the top-of-foundation reference elevation and the interface condition between the superstructure and foundation. Foundation details remain in DEL-002-02. The interface must be explicitly cross-referenced between the two deliverables to ensure the contractor has a complete picture.

### C-06 — Alberta Code Authority Having Jurisdiction (AHJ)
All structural IFC drawings must be suitable for submission to the AHJ as part of the building permit application (SOW-0006). The structural engineer should confirm the specific code editions required by the local AHJ (Camrose County / applicable Safety Codes authority) before finalizing drawing notes and code references on the sheets.

---

## Trade-offs

### T-01 — Drawing Count vs. Clarity
Consolidating sections and details onto fewer sheets reduces drawing volume and coordination risk but may compromise readability for complex elements (e.g., the crane runway bracket at a wall/column intersection). For a 13,000 sq ft industrial building of this complexity, a balance of approximately 8–15 structural detail sheets is typical (ASSUMPTION). The Structural Engineer should prioritize clarity for the elements with the greatest construction risk: crane runway, service pit, mezzanine connection, and steel plate embedment.

### T-02 — Early vs. Late Detail Finalization
Finalizing structural details early enables other disciplines (architectural sections, mechanical penetration layouts) to coordinate sooner. However, premature finalization of crane support details or mezzanine details before supplier information is available may require revision later. A two-stage approach (issue preliminary details for coordination, then final details for IFC) is common but requires careful revision management under the contract.

**Suggested Phasing Decision Framework (ASSUMPTION — lensing item D-003):**

The following categorization helps resolve which elements can proceed and which must wait for external inputs:

| Category | Elements | Can Proceed When | Must Wait For |
|---|---|---|---|
| **Proceed early** (geometry established from RFP/App B) | Building cross-sections (Steps 5-6), typical wall sections, wash bay enclosure (Step 9), stair framing (Step 12), miscellaneous typical details (Step 13) | DEL-002-03 draft framing plans + DEL-002-10 calculations for these elements are available | Construction method decision (Step 4) |
| **Proceed with provisional assumptions** | Service pit sections (Step 7), mezzanine sections (Step 8) | Preliminary geometry from App B; P.Eng. to establish conservative assumptions | County confirmation of pit depth and mezzanine load (Step 3); geotech report for pit wall design |
| **Must wait for external input** | Crane runway details (Step 10), steel plate embedment details (Step 11) | Crane supplier confirmed; County equipment types confirmed | Crane supplier data; County equipment loading data |

**Recommendation:** Issue Phase 2 "proceed early" elements for multi-discipline coordination review (Step 15) while awaiting external inputs for "must wait" elements. Track provisional assumptions using the revision management requirement (R-014) so that revisions are controlled when inputs arrive. This sequencing reduces coordination delay without committing to premature details on crane and plate elements.

### T-03 — Cast-in-Place vs. Tilt-Up
Both are common in Alberta industrial construction. Cast-in-place offers more flexibility for complex geometry (service pit walls, varied section depths) but has slower on-site cycle times. Tilt-up is faster for repetitive wall panels but requires a large casting area and may conflict with the service pit geometry. The General Contractor's preference and site conditions may drive this decision. The structural detail set must be developed in alignment with the selected method.

### T-04 — Crane Supplier Dependency Fallback Strategy (ASSUMPTION)
The crane supplier/manufacturer identity and runway requirements are an external dependency that blocks final detailing of the crane support structure (Step 10 / DEL-002-07). If the crane supplier is not confirmed before the drawing deadline (December 31, 2026), the project faces a risk of incomplete IFC documentation.

**No fallback or provisional design approach is documented in any accessible source.** The Structural Engineer should consider:
- Establishing a **provisional crane runway design** based on a representative 5-Tonne Overhead Crane specification (e.g., standard CMAA Class C crane with typical wheel loads and rail size) and issuing it as a "Preliminary -- Subject to Crane Supplier Confirmation" detail.
- Documenting the assumptions used for the provisional design so that the final crane supplier's data can be compared and revisions minimized.
- Coordinating with the Design-Builder's procurement team to establish a latest-date-by-which crane supplier data is required to maintain the December 2026 IFC deadline.

**Proposed authority: Design-Builder procurement to confirm crane supplier timeline; Structural Engineer to assess whether a provisional design is warranted.**

Source: Procedure Prerequisites (Crane supplier row); Guidance P-05; lensing item F-003.

---

## Examples

No example drawings are available in the accessible source documents for this deliverable. This is a known limitation (lensing item X-001).

**Recommended external resources for detail precedents (ASSUMPTION):**
The Structural Engineer should consult the following types of reference material when developing structural section details for this building type:
- **Comparable project types:** Municipal or county public works maintenance shops, heavy equipment maintenance facilities, regional landfill operations buildings — particularly those constructed in Alberta or similar cold-climate Canadian jurisdictions.
- **Overhead crane references:** CISC or AISC crane runway design guides for industrial buildings with 5-tonne bridge cranes; manufacturer installation manuals for overhead crane runway beam and rail sections.
- **Below-grade structure references:** Concrete pit and trench details from industrial flooring or automotive service pit design guides; relevant sections of CSA A23.3 for below-grade retaining wall design.
- **Tilt-up / cast-in-place references:** Tilt-Up Concrete Association (TCA) design guides if tilt-up is selected; ACI 318/CSA A23.3 for cast-in-place detailing.
- **Steel plate embedment references:** PCI (Precast/Prestressed Concrete Institute) Design Handbook for embedded plate connection details; or manufacturer data for abrasion-resistant floor plates.

Source: ASSUMPTION — standard structural engineering practice for referencing comparable precedents.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-001 | Mezzanine design live load is not quantified numerically. RFP states "heavy items (oil totes, pumping equipment)" without a kPa or psf value. | R-01 §3.4 (functional description only) | None — no numeric value provided anywhere | Specification.md R-006; Datasheet.md Attributes; Procedure.md Step 8 | Structural Engineer to establish minimum design live load per NBC/ABC storage provisions; Owner to confirm acceptability | TBD |
| CON-002 | Service pit depth is not stated in RFP or App B. App B labels it "Service Trench" with width/length annotations but no depth. | R-04 App B (width 24 ft, length 100 ft annotated) | R-01 §3.4 (ventilated and lighted; no depth) | Specification.md R-005; Datasheet.md Attributes; Procedure.md Step 7 | Structural Engineer to determine functional depth with Owner/operations team; depth drives soil retention, concrete volume, and waterproofing scope | TBD |
| CON-003 | Steel plate floor embedment dimensions (thickness, plan size, anchor type) are not specified in RFP or App B. | R-01 §3.4 (steel plating at strategic locations) | R-04 App B ("Steel Plate" labels only, no sizing) | Specification.md R-008; Datasheet.md Attributes | Structural Engineer to establish plate geometry based on equipment type and loading; County to confirm equipment types | TBD |
| CON-004 | Structural system construction method (tilt-up, cast-in-place, precast) is not prescribed by RFP. Choice significantly impacts detail types in this deliverable. | R-01 §3.4 ("concrete structure" only) | None | Guidance.md P-03; Specification.md R-002; Procedure.md Step 4 | Design-Builder to propose method; County approval not explicitly required for this decision per RFP (ASSUMPTION) | TBD |
