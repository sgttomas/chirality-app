# Guidance — DEL-002-11 Foundation Design Package (Variable-Price)

---

## Purpose

This document provides directional guidance for the Structural Engineer producing the Foundation Design Package (DEL-002-11) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition.

DEL-002-11 exists to fulfil two linked project needs:

1. **Proposal-phase commercial need (OBJ-006):** The RFP requires Proponents to provide a separate, variable-price cost estimate for foundation design and construction, based on normal ground conditions, because final foundation scope and cost cannot be determined until geotechnical investigation results are available. This creates a special contractual mechanism within CCDC 14–2013 — the foundation is explicitly carved out from the stipulated-price total. (Source: RFP §4.8.2; Decomposition §5, OBJ-006)

2. **Technical design need (OBJ-003):** The foundation design must ultimately be developed to IFC standard — fully engineered, P.Eng.-stamped, and coordinated across all disciplines — to enable structural construction to proceed. (Source: RFP §3.3.2; Decomposition §5, OBJ-003)

The guidance below addresses both dimensions.

---

## Principles

### P-1 — Variable-Price Logic Must Be Preserved Throughout
The foundation scope occupies a special contractual position: it is estimated at proposal, re-priced post-geotech, and negotiated before finalization. All design documentation (design basis, drawings, calculations) must clearly distinguish what is assumed versus what is confirmed. This protects the Design-Builder's commercial position when the geotech report is received and the foundation price is renegotiated with the County.

**Practical implication:** Every assumed geotechnical parameter (bearing capacity, frost depth, soil classification, groundwater level) must be explicitly flagged in the Design Basis Document. The document should include a "Revision Register" listing each assumption and the trigger for revision (i.e., "revise upon receipt of DEL-008-01 geotech report").

**Contractual mechanism (re: E-005):** The variable-price re-negotiation is governed by CCDC 14–2013 and RFP §4.8.2. The specific CCDC 14–2013 clause governing the change/re-negotiation mechanism is TBD — the Project Manager and/or Contract Administrator should identify the applicable CCDC provision (e.g., GC 6.2 — Change Order, or GC 6.3 — Change Directive, or the supplementary conditions specific to the variable-price foundation scope as described in RFP §4.8.2). Without identifying the specific clause, the re-negotiation process lacks contractual grounding in the design documents. (Source: _SEMANTIC_LENSING.md E-005; RFP §4.8.2; CCDC 14–2013 — clause TBD)

### P-2 — Geotech-First for Confirmation, Normal Conditions for Proposal
The Structural Engineer should proceed using assumed normal-ground-condition parameters for the proposal-phase estimate. These assumptions should be reasonable and defensible for central Alberta, near Ferintosh, in similar landfill/agricultural terrain. However, the engineer must explicitly not treat these as confirmed values. When DEL-008-01 (Geotechnical Investigation and Report) is delivered, the Structural Engineer must review and update the foundation design as required, with the scope and cost delta forming the basis for re-negotiation.

**Source:** RFP §4.8.2; RFP §3.3.2 — "A full complete geotechnical report will be required by the successful proponent to use during the design process."

### P-3 — Heavy Loads Drive Foundation Sizing
The Addition is a heavy industrial facility. The foundation must be designed for loads significantly above a typical commercial building. Key load contributors:
- Two 5-tonne overhead cranes on trolleys (dynamic loads, rail reactions) — Appendix B (Shop), RFP §3.4
- Heavy tracked and packer equipment on the main floor (motor scraper class or heavier) — RFP §3.4, Appendix B (Shop)
- Steel plate embedments at strategic floor locations — Appendix B (Shop)
- Load-bearing mezzanine (oil totes, pumping equipment) — RFP §3.4
- 50,000 L water storage cistern — RFP §3.4, Appendix B (Shop)

The Structural Engineer should develop a comprehensive load schedule early, as it directly drives footing sizing, slab thickness, and reinforcement.

### P-4 — Below-Grade Elements Require Special Attention
The service pit/trench and the mud sump connection for the wash bay introduce below-grade structural elements that interact with the foundation. Consideration should be given to:
- Retained earth pressure on pit walls
- Groundwater levels (if any) affecting hydrostatic uplift on pit floor
- Proximity of pit/trench to footings — setback requirements to protect bearing
- Drainage and waterproofing of below-grade elements

**Source:** RFP §3.4 — "Ventilated and lighted service pit area." RFP §3.4, Appendix B (Shop) — wash bay mud sump.

### P-5 — Coordinate Early with Geotechnical and Architectural
Before finalizing footing layout, the Structural Engineer should confirm:
- Building footprint and column grid with the Architect (DEL-001-02)
- Geotech report findings (DEL-008-01) — or, if not yet available, confirm assumed parameters are aligned with what PKG-008 expects to report
- Cistern location and size with the Plumbing Engineer (DEL-006-04)

### P-6 — Alberta Safety Codes Act Compliance Pathway
The Alberta Safety Codes Act is listed in the Standards table (Specification.md) as an explicit requirement per RFP §3.3.2. The Structural Engineer and Project Manager should understand and plan for the Safety Codes compliance pathway applicable to foundation design. This typically includes:

- **Building permit review:** Foundation design documents are submitted as part of the building permit application to the local authority (Camrose County or its designated Safety Codes Officer).
- **Safety Codes Officer (SCO) involvement:** An accredited SCO reviews the structural design for compliance with the Alberta Building Code. For foundation design, this includes verification that the design meets structural safety requirements under the Safety Codes Act.
- **Inspection requirements:** The Safety Codes Act may require foundation inspections at specific construction stages (e.g., before concrete placement).

**Note:** The specific Safety Codes obligations applicable to this foundation design are TBD — the Project Manager should confirm with the County and/or the accredited SCO. The compliance pathway should be documented in the project management plan or permitting deliverables (PKG-009).

**Source:** _SEMANTIC_LENSING.md C-001; RFP §3.3.2 — "The proposed building must adhere to all Alberta Safety Codes"; Specification.md Standards table — Alberta Safety Codes Act row.

---

## Considerations

### Phasing: Proposal vs. IFC
The deliverable spans two time phases:

| Phase | Design State | Output |
|---|---|---|
| Proposal submission | Assumed normal ground conditions | Variable-price cost estimate (RFP §4.8.2) — included in Proposal section 3.2 |
| Post-award, pre-IFC | Geotech report received; design revised as needed | Full IFC foundation drawings, stamped by P.Eng. |

The Structural Engineer must plan workload and scheduling to accommodate the post-award revision cycle without compromising the December 31, 2026 completion deadline.

### Alberta Climatic and Seismic Context
The project is located in central Alberta (near Ferintosh, Camrose County). Climatic design values applicable to this region under NBC/ABC include:
- Ground snow load: TBD — verify from NBC climatic data tables for Ferintosh area
- Design frost depth: TBD — verify from NBC/ABC; ASSUMPTION: conservatively assume 2.0 m for design purposes (typical range 1.5–2.0 m for this region of Alberta)
- Seismic hazard: TBD — central Alberta is generally low seismic; verify from NBC seismic hazard maps

**Note:** The above are working ASSUMPTIONs only. The engineer of record must confirm all climatic and seismic design values from NBC climatic appendix and Alberta local data.

### Concrete Structure Type and Floor Loads
The RFP specifies a concrete structure with a 35-foot ceiling height. The floor slab must support very heavy equipment. ASSUMPTION: the floor will be a concrete slab-on-grade of sufficient thickness and reinforcement to support tracked equipment loads. Steel plate embedments at strategic locations (shown on Appendix B) must be detailed for constructability and durability.

### Cistern Placement
The 50,000 L water storage cistern is shown in the Appendix B (Shop) floor plan within the Addition footprint, adjacent to the stairs to the mezzanine. Its full weight when loaded is a significant point or area load on the slab/foundation. The Structural Engineer must confirm cistern dimensions and weight with the Plumbing Engineer and include this in the foundation load schedule.

### Mezzanine Load Path
The mezzanine is described as load-bearing capable of heavy items (oil totes, pumping equipment). The mezzanine structure is above the parts room, utility room, and wash bay. The mezzanine columns or walls transfer load down to the foundation slab or footings, and this load path must be fully traced in the structural calculations.

### Crane Support Interface
Crane rail beams and columns transfer significant dynamic loads to the foundation. The Structural Engineer must coordinate crane geometry (rail spacing, wheel loads, bridge span) — likely from the crane supplier or crane package deliverable (DEL-016-01, PKG-016) — and design the crane column bases and embedded anchor bolts accordingly.

**Crane data timing (re: F-003):** Crane technical data (wheel loads, rail spacing, bridge span) is listed as a prerequisite in Procedure.md but may not be available during the proposal phase. The Structural Engineer should clarify with the Project Manager and/or Procurement at what point crane data must be available. If crane data is unavailable at proposal time, the engineer should document assumed crane loads based on typical 5-tonne overhead crane specifications and flag these assumptions for revision upon receipt of supplier data. The proposal-phase cost estimate should note this assumption explicitly. (Source: _SEMANTIC_LENSING.md F-003; Procedure.md Prerequisites table — "Crane technical data" row)

### Foundation Type Rationale
The Trade-offs table below recommends spread footings as the baseline foundation type for the proposal-phase design on assumed normal conditions. The rationale for this assumption is:

- **Site conditions (assumed):** Central Alberta, near Ferintosh, is characterized by glacial till deposits with generally adequate bearing capacity for spread footings under normal conditions. The RFP's "normal ground conditions" language (§4.8.2) implies that the Owner anticipates foundation conditions amenable to conventional foundation types.
- **Structure type compatibility:** Spread footings are standard for single-storey industrial concrete structures with moderate to heavy column loads where adequate bearing capacity exists.
- **Cost and constructability:** Spread footings are lower cost and simpler to construct than alternatives (drilled piers, helical piles), which is consistent with the variable-price estimate approach — the proposal-phase estimate should reflect the most economical foundation assuming normal conditions.
- **Alternatives if conditions differ:** If the geotechnical report reveals poor bearing capacity, high groundwater, or deleterious material, alternatives such as drilled piers, driven piles, or helical piles would be evaluated. This scenario is the explicit trigger for variable-price re-negotiation under RFP §4.8.2.

This is an ASSUMPTION. The geotechnical report (DEL-008-01) is the authoritative basis for final foundation type selection. (Source: _SEMANTIC_LENSING.md F-004; RFP §4.8.2; Guidance.md Trade-offs table)

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Approach |
|---|---|---|---|
| Foundation type on assumed conditions | Spread footings (lower cost, simpler) | Continuous strip footings or mat (higher cost, more robust) | ASSUMPTION: Design for spread footings on assumed normal conditions; document sensitivity to poor subgrade in design basis. If geotech report indicates poor conditions, this becomes the post-award negotiation trigger. See "Foundation Type Rationale" above for justification. |
| Slab thickness for heavy equipment | Thinner slab (lower cost, adequate for lighter equipment) | Thicker reinforced slab (higher cost, better durability for motor scrapers) | ASSUMPTION: Heavy industrial floor should be designed for motor scraper-class equipment as minimum; slab thickness and reinforcement to be determined by structural calculation. Do not under-design for cost — poor floor performance in a landfill shop is operationally costly. |
| Frost protection depth | Footings at minimum code-required depth | Footings deeper than minimum | Footings must be at or below frost depth per ABC/NBC. Do not shallow-design for cost savings in this climate. |
| Timing of post-geotech revision | Revise immediately upon geotech receipt | Defer revision until later in design | Revise promptly. Foundation is on the critical path for construction. Delay in foundation finalization delays PKG-010 construction start. |

---

## Examples

TBD — No project-specific precedent examples are available from accessible sources. The engineer of record should reference comparable industrial concrete structures in central Alberta for basis-of-design context.

**Suggested reference points (ASSUMPTION — not verified from accessible sources):**
- Comparable heavy industrial maintenance shops or equipment storage facilities in central Alberta agricultural/landfill settings, designed on glacial till soils with spread footing foundations.
- NBC Part 4 structural design examples for buildings with overhead crane loading.
- CSA A23.3 design examples for reinforced concrete footings and slabs-on-grade supporting heavy equipment.

If no directly comparable precedent is available, the engineer should document why and proceed based on engineering first principles and applicable code provisions. (Source: _SEMANTIC_LENSING.md D-003)

---

## Artifact Production Rationale

The five anticipated artifacts listed in Specification.md, Documentation section, are all currently TBD. Their expected production sequence and rationale are:

1. **Foundation Design Basis Document** — produced first because it establishes all design parameters (assumptions, loads, codes, criteria) consumed by every subsequent artifact.
2. **Foundation Cost Estimate (Variable-Price)** — produced second (proposal phase) because it depends on the Design Basis Document and a preliminary foundation concept.
3. **Structural Calculation Package (Foundation Component)** — produced third (post-award, post-geotech or on assumed conditions) because it depends on confirmed or assumed geotechnical parameters from the Design Basis Document.
4. **Foundation Plan Drawing** — produced fourth because it depends on completed structural calculations to size and locate all foundation elements.
5. **Foundation Detail Drawings** — produced fifth because details depend on the plan layout and calculation results.

This sequence may overlap in practice (e.g., preliminary calculations may inform the cost estimate), but the dependency flow above governs the order in which each artifact can be considered complete.

**Source:** _SEMANTIC_LENSING.md E-004; Procedure.md Steps — phased approach (Phase 1 = proposal, Phase 2 = IFC).

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CFT-001 | The decomposition entry for DEL-002-11 lists it as supporting OBJ-003 and OBJ-006. The _CONTEXT.md description also states "Supports OBJ-003, OBJ-006." However, many other PKG-002 deliverables also support OBJ-001 (operational building) whereas DEL-002-11 does not list OBJ-001. It is unclear whether the foundation design package should also be linked to OBJ-001 — since a code-compliant foundation is intrinsic to OBJ-001. | Decomposition §7, PKG-002 row for DEL-002-11 (OBJ-003, OBJ-006 only) | Decomposition §5, OBJ-001 — "Deliver a code-compliant, fully functional maintenance shop addition" (implies foundation is in scope for OBJ-001) | Specification §Requirements, Datasheet §Identification | PROPOSAL: OBJ-001 may be implicitly served by DEL-002-11 but was intentionally excluded from the formal mapping, possibly because DEL-002-11 is the variable-price design package and OBJ-001 is tracked through construction deliverables. Accept current mapping (OBJ-003, OBJ-006) unless human confirms otherwise. | TBD |
