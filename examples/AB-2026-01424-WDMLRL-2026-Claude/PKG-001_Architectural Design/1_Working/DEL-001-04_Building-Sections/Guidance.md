# Guidance — DEL-001-04 Building Sections

**Document Type:** Guidance (directional)
**Deliverable ID:** DEL-001-04
**Deliverable Name:** Building Sections
**Package:** PKG-001 Architectural Design
**Revision:** R1 — 2026-02-26 (4_DOCUMENTS Pass 3 — Semantic Lensing Enrichment)

---

## Purpose

Building section drawings are vertical cut views that reveal what cannot be seen in plan: how height, structure, and layered levels relate to one another. For the New North Shop addition, the building sections serve three essential functions:

1. **Spatial verification** — They confirm that the 35' ceiling height is achieved and that the crane envelope, mezzanine, and service pit can all coexist without vertical conflicts.
2. **Structural interface documentation** — They show where the concrete structure (slab, walls, columns, roof) meets architectural elements, enabling the structural engineer to coordinate design without ambiguity.
3. **Construction communication** — They give the builder a clear understanding of vertical relationships that plan views alone cannot convey, particularly for the below-grade service pit, the elevated mezzanine, and the large overhead door openings.

This deliverable supports OBJ-001 (code-compliant, fully functional maintenance shop addition) and OBJ-003 (complete, P.Eng.-stamped IFC design documentation across all disciplines).

**Source:** Decomposition OBJ-001, OBJ-003; _CONTEXT.md.

---

## Principles

### P-01 — Section Cut Selection Is a Design Decision

The choice of where to cut sections is not mechanical — it reflects the Architect's judgment about what is difficult to understand from plan alone. For this building, the following conditions are the primary drivers of section cut placement:

- The 35' ceiling is an unusual height that must be explicitly documented for structural coordination.
- The mezzanine creates a two-level condition over a subset of the building; vertical clearances above and below must be confirmed.
- The service pit is below grade; its depth, wall construction, and slab interface are invisible in plan.
- The overhead crane runway is a large structural element that must fit within the ceiling envelope; its clearance to the mezzanine edge and to the roof structure must be checked.
- The wash bay requires its own section due to its separate height profile (full 35' or partial — TBD) and its exterior mud sump connection. **TBD (F-003):** The wash bay height profile has not been determined. The Architect must clarify whether the wash bay has the full 35' ceiling height (same as the main shop) or a reduced height (e.g., if the mezzanine extends over the wash bay and lowers the effective ceiling). The rationale for the determination should be documented, as it affects mezzanine extent, structural design, and section drawing content. Proposed authority: Architect. (Source: Guidance P-01; Specification REQ-002.)

**Source:** App B (Shop) floor plan; RFP §3.4; ASSUMPTION applied for section cut rationale.

### P-02 — Confirm the 35' Ceiling Envelope Before Detailing

The 35' concrete structure ceiling height (RFP §3.4; App B notes) is the dominant vertical constraint. All other elements — crane runway beams, mezzanine slab, ductwork, high bay light mounting — must fit beneath it. Sections should be drawn with this datum established first, and all other elements positioned relative to it.

**Source:** RFP §3.4; App B (Shop) notes; Decomposition SOW-0012, SOW-0022.

### P-03 — Coordinate with Structural Before Fixing Mezzanine Elevation

The mezzanine floor elevation is not yet defined in the RFP or conceptual drawings. It should be coordinated with the structural engineer (DEL-002-05 Mezzanine Framing Details) before the sections are finalized. Key considerations:

- Clearance required beneath the mezzanine for ground-floor operations (parts room, utility room, wash bay access).
- Structural depth of the mezzanine assembly (slab + beams) contributes to the overall height consumed.
- The mezzanine must accommodate heavy loads (oil totes, pumping equipment) — load bearing capacity is a structural determination.

**Source:** RFP §3.4; Decomposition SOW-0032, SOW-0033; ASSUMPTION applied for coordination sequence.

### P-04 — The Service Pit Requires Special Attention

The service pit is a below-grade element that is uncommon in most building section workflows. The section through the pit should document:

- Finished floor level (datum) vs. pit floor level (depth TBD).
- Pit wall construction and its relationship to the main slab.
- How the pit is covered when not in use (grating or flush plates — TBD).
- Ventilation and lighting provisions (coordination with mechanical and electrical packages).

This information is essential for both safety code compliance (ventilated pit area per RFP §3.4) and for structural design.

**Source:** RFP §3.4; Decomposition SOW-0028; ASSUMPTION applied for pit cover and ventilation coordination.

### P-05 — Crane Clearance Must Be Verified in Section

The two 5-tonne overhead cranes on trolley occupy significant vertical space. The section must show:

- Top of rail elevation (structural determination).
- Bottom of hook elevation (or bottom of crane bridge) at lowest travel.
- Headroom to underside of roof structure.
- Lateral clearance at mezzanine edge (if crane operates near mezzanine zone).

This is primarily a structural and crane-supplier coordination task, but the Architect is responsible for ensuring the section drawing reflects agreed-upon elevations.

**Source:** RFP §3.4; App B (Shop) notes; Decomposition SOW-0067; ASSUMPTION applied for clearance documentation rationale.

---

## Considerations

### C-01 — Design-Build Context and Evolving Information

This is a design-build project (CCDC 14-2013). The conceptual drawing (Appendix B) is the primary spatial reference, but it is not a dimensioned design document. The Architect must:

- Establish actual building dimensions in coordination with structural and civil (site constraints).
- Confirm ceiling height achievement in the final structural system.
- Update sections as the structural design develops.

The sections at preliminary design stage will be less detailed than IFC sections; both stages require documented vertical conditions, but IFC must be fully coordinated.

**Source:** RFP §3.3.2; CCDC 14-2013 (location TBD); Decomposition OBJ-003.

### C-02 — Relationship to Other PKG-001 Drawings

Building sections are most useful when cross-referenced to floor plans and reflected ceiling plans. Section cut marks on DEL-001-02 (Floor Plans) must correspond precisely to the sections in this deliverable. Interior elevations (DEL-001-05) may share cut geometry with sections at specific wall conditions.

**Source:** Decomposition PKG-001 deliverable list; ASSUMPTION applied for cross-reference coordination.

### C-03 — Alberta Code Implications for Section Content

The Alberta Building Code governs requirements for:

- Minimum headroom clearances in occupied spaces (office, parts room, utility room — ground floor under mezzanine).
- Means of egress — stair geometry from mezzanine must comply with code (tread/riser dimensions, handrail heights).
- Fire separation — if the mezzanine creates a separate fire compartment, this must be documented in sections.
- Service pit — occupational health and safety regulations may impose minimum depth and ventilation requirements.

Specific clause references are TBD (Alberta Building Code location TBD — not directly accessed).

> **TBD (B-004):** The fire separation question for the mezzanine remains unresolved. If the mezzanine creates a separate fire compartment (per Alberta Building Code requirements — specific clauses TBD), this must be documented in the building sections, including fire-rated assembly indications at the mezzanine floor and any separating walls. This determination should be tracked as a TBD and resolved by the Architect / code consultant before IFC. Proposed authority: Architect / code consultant. (Source: Guidance C-03; Specification REQ-009.)

**Source:** RFP §3.3.2; Alberta Safety Codes Act (location TBD); ASSUMPTION applied for specific code items.

### C-04 — Old North Shop Interface

The conceptual drawing (App B) shows the addition (130'×100') immediately adjacent to the Old North Shop (105'×40'). Building sections may need to show the interface condition at the shared wall or junction, particularly if a structural connection or fire separation is required at that boundary. This interface is TBD pending design development.

When documenting the Old North Shop interface in building sections, the Architect should address:

1. **Structural connection:** How the addition's concrete structure connects to or abuts the existing Old North Shop structure (expansion joint, structural tie, bearing condition).
2. **Fire separation:** Whether a fire separation is required at the shared boundary (per Alberta Building Code — clause TBD).
3. **Weatherproofing:** How the junction between new and existing rooflines and wall assemblies is weatherproofed.
4. **Trigger for determination:** The interface condition should be resolved no later than the Phase B structural coordination step (Procedure Step B-1), as it affects section content at that boundary.

> **TBD (X-001):** No directional guidance on when and how to document the Old North Shop interface condition in building sections was previously provided. The items above are ASSUMPTION-based. Proposed authority: Architect. (Source: Guidance C-04; App B floor plan.)

**Source:** App B (Shop) floor plan; ASSUMPTION applied for interface condition.

### C-05 — National Building Code of Canada Adoption Chain (ASSUMPTION)

The Specification Standards table lists the National Building Code of Canada (NBC) as "ASSUMPTION: likely applicable." For building sections, the relevant consideration is understanding how NBC provisions are adopted or amended by Alberta, and which specific NBC provisions affect section content (e.g., fire separation, means of egress, minimum headroom). The Alberta Building Code is the governing instrument, but it references or adopts provisions from the NBC. The Architect / code consultant should clarify:

1. Which NBC edition is currently adopted by Alberta for this project's permit cycle.
2. Whether any Alberta-specific amendments override NBC provisions relevant to section content (fire compartmentalization, stair geometry, headroom).
3. How this adoption chain should be documented in the Standards table and code compliance verification.

> **ASSUMPTION (C-002):** This consideration is inferred from the gap between listing NBC as likely applicable and providing no guidance on how it affects section content. Proposed authority: Architect / code consultant. (Source: Specification Standards table; Guidance C-03.)

### C-06 — Section Drawing Naming Convention (Normalization)

The deliverable title is "Building Sections" (the drawing set as a whole). Individual sections within the set are listed in Specification Documentation as "Section -- Longitudinal (primary)" etc. However, the naming convention for individual section drawings on sheets (e.g., "Section A-A" vs. "Building Section A-A") is not defined.

- **"Building Sections"** should refer to the drawing set (DEL-001-04) as a deliverable.
- **Individual section identifiers** (e.g., "Section A-A", "Section B-B") should follow a consistent convention across all drawings and all cross-references (floor plan section cut marks must match).
- The Architect should define and document this naming convention.

> **TBD (E-004):** Individual section naming convention is not defined. Proposed authority: Architect. (Source: Specification > Documentation > Expected Drawing Sheet Content; Datasheet > Identification.)

### C-07 — Measurement Unit Convention (Normalization)

Datasheet and Specification use imperial units throughout (35', 130'x100', 24'), while Procedure Step A-1 introduces metric equivalents (10,668 mm, 0.00 m) without noting a conversion convention. This inconsistency should be resolved with a project-level measurement unit convention:

- **Option A:** Imperial primary, with metric equivalents shown in parentheses where required by code or standards.
- **Option B:** Metric primary (Alberta Building Code is metric-based), with imperial equivalents shown where the RFP uses imperial.
- **Recommended:** Confirm with the Architect and apply consistently across all four documents and all drawing production.

> **TBD (B-003):** No project measurement unit convention has been established. The inconsistency between imperial (Datasheet) and metric (Procedure) should be resolved. Proposed authority: Architect / project convention. (Source: Datasheet > Attributes; Procedure Step A-1.)

### C-08 — Renovation Interface Scope Boundary (ASSUMPTION)

Specification Scope (Excluded) states that renovation drawings for the Old North Shop are excluded "except where renovation interfaces with the addition are shown for context." This exclusion boundary needs clarification for building sections:

- **What constitutes "interface context"?** At minimum, the shared wall/junction condition and any structural or fire separation at the boundary should be shown. The extent of existing building shown beyond the junction (e.g., 5' of existing structure, one structural bay, or the full Old North Shop width) should be defined.
- **How is the boundary marked on drawings?** A match line, dashed outline, or "existing" notation convention should be established.
- **What triggers inclusion?** If a section cut passes through or near the junction, the renovation interface is relevant. If the section is entirely within the new addition, the interface may not need to be shown.

> **ASSUMPTION (X-003):** This consideration is inferred from the ambiguity in the exclusion clause. Proposed authority: Architect. (Source: Specification > Scope > Excluded; Guidance C-04.)

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Direction | Source |
|---|---|---|---|---|
| Number of section cuts | Minimum (5 cuts per Specification) | Comprehensive (8–10 cuts) | Begin with minimum; add as design develops | ASSUMPTION |
| Mezzanine elevation determination | Set by Architect based on clearance assumptions | Set collaboratively with structural engineer | Collaborative — structural loads and beam depth drive the elevation | RFP §3.4; Decomposition SOW-0033 |
| Section drawing scale | 1:100 (overview) | 1:50 (detail-capable) | Both scales likely required: 1:100 for overall, 1:50 for pit and mezzanine details | ASSUMPTION |
| Service pit depth | Fixed early (Architect assumption) | Confirmed with structural and mechanical | Confirm with structural before fixing | Decomposition SOW-0028; ASSUMPTION |

---

## Examples

No project-specific section drawing examples are available from accessible sources. The Appendix B (Shop) conceptual floor plan provides spatial layout only and does not include section views.

**ASSUMPTION:** Standard industrial building section conventions apply — annotated vertical dimensions, assembly callouts, level datums, and grid references are expected on IFC drawings.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| C-001 | Building dimensions: RFP §3.1 states "approximately 13,000 sq ft useable area" while App B (Shop) floor plan shows 130'×100' = 13,000 sq ft nominal — consistent for gross area, but "useable" vs. gross area distinction may affect wall thickness assumptions and interior dimensions on sections. | RFP §3.1 (useable ~13,000 sq ft) | App B (Shop) (130'×100' plan dimensions) | Specification REQ-001; Datasheet Attributes | App B (Shop) dimensions govern for drawing production; Architect to confirm interior dimensions | TBD |
| C-002 | Ceiling height stated as 35' in both RFP §3.4 and App B (Shop) notes, but SOW-0012 in the Decomposition attributes the 35' ceiling to the structural design scope (not architectural). It is ambiguous whether 35' is the finished ceiling height or the structural frame height. **(X-005 confirms: this ambiguity affects every section drawing datum. "35' (concrete structure)" could mean structural frame height or finished interior ceiling height. All documents continue to use "35' ceiling height" without resolution.)** | RFP §3.4 ("Concrete structure 35' ceiling"); Datasheet > Attributes ("35' (concrete structure)") | Decomposition SOW-0012 ("concrete structure, 35' ceiling"); Specification REQ-002 | Specification REQ-002; Datasheet Attributes; all section drawings; Guidance P-02 | Human ruling required: Treat as finished interior ceiling height = 35' until structural confirms; ASSUMPTION | TBD |
