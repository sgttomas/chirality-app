# Guidance — DEL-012-03: Office Space

**Document Type:** Guidance (directional)
**Deliverable ID:** DEL-012-03
**Package:** PKG-012 — Interior Construction & Fit-Out
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Revision:** R2 — 2026-02-26 (Pass 3 — Semantic Lensing Enrichment)
**Status:** SEMANTIC_READY

---

## Purpose

DEL-012-03 exists to provide an administrative office space within the new north shop addition that supports facility management and operations at the West Dried Meat Lake Regional Landfill. The office is one of three interior spaces within PKG-012 (alongside the Parts Storage Room, DEL-012-01, and the Utility Room, DEL-012-02), and is part of the County's objective to deliver a fully functional maintenance shop addition that satisfies the County's operational program (OBJ-001).

The office space enables on-site administrative activities (scheduling, documentation, communications) that are essential to the daily operation of the landfill maintenance facility.

**Source:** _CONTEXT.md Description; WDMLRL_Decomposition_Claude.md OBJ-001; RFP §3.1

---

## Principles

### 1. Interior Fit-Out Serves Occupancy, Not Structure
PKG-012 is explicitly scoped as "all interior non-structural, non-MEP construction." The structural shell and envelope are provided by PKG-011. The office fit-out builds on that shell with partitions, finishes, and integrated services. Decisions about partition locations, finish selections, and service rough-ins must therefore be coordinated with and remain subordinate to the structural drawings from PKG-011 and the MEP designs from PKG-013 and PKG-015.

**Source:** WDMLRL_Decomposition_Claude.md PKG-012 Inclusion Criteria and Exclusions

### 2. Design-Build Context: Concept Only, IFC Required
The RFP explicitly states: "The County only has a concept in mind; therefore, it will be a design/build project." The App B drawings are conceptual only. All construction must follow the IFC drawings stamped by a P.Eng. licensed in Alberta. The office layout, dimensions, finishes, and service locations shown in the conceptual drawings are directional, not prescriptive.

**Source:** RFP §3.4 preamble; RFP §3.3.2

### 3. Workplace Standards Are Functional, Not Luxury
The office is intended to serve landfill maintenance facility management. Requirements emphasize functionality (professional environment, comfortable conditions, accessibility, integrated data/communications) rather than high-specification commercial finishes. Finish selections should be durable, easy to maintain, and appropriate for an industrial facility administrative context.

**Rationale for functional finish standard [Lensing: A-005]:** The "functional, not luxury" approach is driven by the operating context of a landfill maintenance facility, where:
- **Lifecycle cost:** Higher-grade commercial finishes carry premium material and installation costs with marginal durability benefit in a facility where foot traffic includes personnel transitioning from industrial shop environments. Durable mid-grade finishes (e.g., commercial-grade sheet vinyl or sealed concrete flooring, Level 4 drywall finish) provide adequate longevity at lower lifecycle cost. (ASSUMPTION: lifecycle cost reasoning inferred from facility type — no explicit cost guidance found in RFP or references.)
- **Maintenance burden:** An industrial facility administrative office experiences different wear patterns than a commercial office. Finishes that resist cleaning chemicals, tolerate minor impact damage, and do not require specialized maintenance reduce operational burden for County maintenance staff. (ASSUMPTION: maintenance context inferred from facility type.)
- **Calibration guidance for IFC Architect:** The IFC architect should calibrate finish selections to be appropriate for an industrial administrative context, not a corporate office standard. This principle should be communicated during the preliminary design review (Procedure.md Step 1.2).

**Source:** _CONTEXT.md Key Requirements; RFP §3.1

### 4. Scope Boundary Discipline is Critical
The office sits at the intersection of three packages (PKG-012 Interior, PKG-013 HVAC, PKG-015 Electrical). Clear scope boundaries must be established in the contractor scope documents to avoid gaps or duplication. The conceptual drawings do not resolve these boundaries explicitly.

**Source:** _DEPENDENCIES.md; WDMLRL_Decomposition_Claude.md PKG-012, PKG-013, PKG-015

---

## Considerations

### Coordination with Adjacent Spaces
- The office is adjacent to the Parts Storage Room (DEL-012-01). Access routes between these spaces and through the roll-up door area must be coordinated to avoid interference.
- The Utility Room (DEL-012-02) is nearby and shares HVAC and electrical distribution. Coordinate partition layouts and penetrations.
- The mezzanine structure (DEL-011-07, PKG-011) is located above the parts room and utility room zone. Verify whether any mezzanine structure element affects the office ceiling or overhead clearance. **Resolution status: UNRESOLVED (TBD).** [Lensing: E-001]
  - **Impact if mezzanine affects office zone:** Could constrain ceiling height below the 35' structural ceiling (RFP §3.4), affect HVAC duct routing above the office, and limit suspended ceiling height options.
  - **Resolution trigger:** IFC Architect / Structural Engineer to confirm the mezzanine-to-office spatial relationship during preliminary design. This finding should be documented and communicated to PKG-013 (HVAC) before finalizing office ceiling and duct routing design.

**Source:** _DEPENDENCIES.md Internal Package Dependencies; App B (Shop) floor plan; WDMLRL_Decomposition_Claude.md DEL-011-07

### HVAC Integration
The office requires comfortable environmental conditions and must be served by PKG-013 systems (heating via DEL-013-01, fresh air via DEL-013-02 Air Exchanger, makeup air via DEL-013-03). The IFC mechanical design must define the office's HVAC zone, supply/return register locations, and thermostat placement. PKG-012 construction must accommodate all duct and register penetrations without compromising partition structural integrity or fire separation requirements.

**Source:** _DEPENDENCIES.md PKG-013 Dependencies; _CONTEXT.md Scope — "HVAC zoning and controls"

### Lighting Adequacy
The conceptual electrical drawing specifies 1× 8' LED fixture for the office. Whether this is sufficient for the office's final floor area depends on the IFC architectural design. If the office footprint is confirmed to be larger than a small enclosed room, the IFC electrical design may need to increase fixture count. This should be reviewed during preliminary design.

**Source:** SOW-0054; App B (Electrical); ASSUMPTION

### Accessibility
The office must meet Alberta Building Code accessibility (barrier-free) requirements. This affects door width, threshold heights, maneuvering clearances, and potentially the floor finish (avoid trip hazards). These requirements should be incorporated into the IFC architectural design from the outset.

**Source:** _CONTEXT.md Key Requirements — "Accessibility standards compliance"; Alberta Building Code (barrier-free provisions)

### Data and Communication Infrastructure
The _CONTEXT.md scope includes "electrical outlets and data points" and "integrated communication and data systems." The RFP electrical notes reference "Wiring for Security Cameras" and "Antenna Wire for 2 Way Radios" as building-wide low-voltage work. The specific data/communications outlets within the office are TBD pending IFC low-voltage design (PKG-015).

**Intended operational purpose (TBD) [Lensing: D-003]:** The office location — adjacent to the parts room — suggests it may serve as a communications hub for the facility (ASSUMPTION). However, the intended use of the office data/communications infrastructure has not been confirmed by the County (Owner). The quality and quantity of data infrastructure depends on whether the office is:
- (a) a standalone administrative workspace with basic data connectivity, or
- (b) a facility communications hub requiring enhanced data infrastructure (e.g., network switch, multiple data drops, dedicated circuit for communications equipment), or
- (c) both.
**Resolution trigger:** County (Owner) to confirm intended use of office data/communications infrastructure during preliminary design review. This determination affects the minimum data point count tracked in Datasheet.md (see Lensing item X-001) and REQ-005 verification in Specification.md.

**Source:** _CONTEXT.md Scope and Key Requirements; App B (Electrical) notes

### Completion Schedule Pressure
The project completion deadline of December 31, 2026, is a hard contractual date. Interior fit-out (PKG-012) depends on the structural shell (PKG-011) being sufficiently complete. Construction scheduling should identify the critical path for office fit-out, particularly the sequencing of partition construction relative to MEP rough-in.

**Source:** RFP §3.1 completion deadline; _DEPENDENCIES.md External Dependencies

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Direction | Source |
|---|---|---|---|---|
| Office size vs. operational need | Smaller footprint = more shop floor area | Larger footprint = more administrative capacity | IFC architect should confirm with County's operational program; RFP is conceptual only | RFP §3.4 preamble; App B (Shop) |
| Finish level | Durable commercial-grade finishes (higher cost, longer life) | Basic industrial finishes (lower cost) | Match finish quality to durability needs of an industrial facility office | _CONTEXT.md Key Requirements |
| Lighting fixture count | 1× 8' LED as shown conceptually | Additional fixtures if final office area warrants | Review during IFC electrical design against final office dimensions | SOW-0054; App B (Electrical) |
| Scope boundary (PKG-012 vs PKG-015) for electrical rough-in | PKG-012 installs conduit/rough-in, PKG-015 pulls wire and devices | PKG-015 performs all electrical work including rough-in | Resolve explicitly in contractor scope documents to avoid gaps | _DEPENDENCIES.md; WDMLRL_Decomposition_Claude.md |

---

## Examples

No precedent examples are available from accessible sources. TBD.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-001 | Scope boundary for electrical outlet and lighting installation in the office: PKG-012 (Interior Fit-Out) vs. PKG-015 (Electrical Installation) is not explicitly resolved in the RFP or decomposition. PKG-012 includes "Electrical outlets and data points" per _CONTEXT.md, while PKG-015 includes "all lighting, all receptacles" per decomposition. | _CONTEXT.md Scope; Specification.md REQ-005, REQ-006, REQ-007 | WDMLRL_Decomposition_Claude.md PKG-015 description | Specification.md Requirements (REQ-005, REQ-006, REQ-007); Procedure.md Steps | PROPOSAL: Treat PKG-015 as the installing party for all electrical devices (outlets, lighting) in the office; PKG-012 is responsible for physical enclosure (partitions, finishes) and accommodation of PKG-015 work. Confirm in contractor scope documents. | TBD |
| CONF-002 | Lighting fixture adequacy: SOW-0054 and App B (Electrical) specify 1x 8' LED fixture for the office. If the IFC architectural design produces a larger office than implied by the conceptual drawing, 1 fixture may be insufficient for workplace lighting standards. | SOW-0054; App B (Electrical) — "1x 8' LED in Office" | General workplace lighting adequacy requirements (Alberta OH&S; Alberta Building Code) — location TBD | Specification.md REQ-006; Datasheet.md Electrical Attributes | PROPOSAL: IFC electrical design to verify fixture count against final office dimensions and Alberta workplace lighting requirements. SOW-0054 represents a conceptual minimum. | TBD |
| CONF-003 [Lensing: B-004] | Scope boundary interpretation for "Electrical outlets and data points" under PKG-012: _CONTEXT.md includes this in PKG-012 scope. Datasheet.md Construction previously stated "Included in PKG-012 scope" for electrical rough-in. Specification.md Scope hedges ("scope boundary with PKG-015 to be confirmed"). The three documents presented inconsistent positions on whether PKG-012 scope includes physical accommodation only or also installation. Now normalized in Datasheet.md to align with Specification.md hedging. | _CONTEXT.md Scope — "Electrical outlets and data points" | WDMLRL_Decomposition_Claude.md PKG-015 — "all lighting, all receptacles" | Datasheet.md Construction; Specification.md Scope; Procedure.md Steps 2.9, 2.10 | PROPOSAL: Resolve via contractor scope documents; CONF-001 remains the primary escalation. Datasheet, Specification, and Procedure now consistently treat this as TBD pending scope resolution. | TBD |
