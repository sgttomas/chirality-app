# Guidance — DEL-003-01 Preliminary Mechanical Design

---

## Purpose

DEL-003-01 exists to give Camrose County an early, approvable view of the mechanical engineering approach for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition before the design team commits to final engineering and IFC drawings.

Under the CCDC 14-2013 design-build delivery model, the County has a conceptual program (RFP §3.4 and Appendix B) but has explicitly reserved the right to approve or redirect preliminary designs before construction commences (RFP §3.3.2; SOW-0010c). The preliminary design presentation is the formal checkpoint that satisfies this requirement for the mechanical discipline.

**Objectives addressed:** OBJ-003 (complete, P.Eng.-stamped IFC design documentation across all disciplines -- preliminary approval is the gateway); OBJ-004 (install and commission all mechanical systems to operational readiness -- the preliminary design sets the system selection path).

Source: Decomposition §5 (OBJ-003, OBJ-004); RFP §3.3.2.

---

## Principles

### 1. Preliminary Approval is a Hard Gate

The County must approve the preliminary mechanical design before the design team proceeds to final engineering. This is not a courtesy review -- it is a contract requirement (SOW-0010c). The Mechanical Engineer should treat the Design Presentation as a binding checkpoint, not a rough sketch. Designs that receive approval provide the team with a mandate to proceed; those that do not must be revised.

Source: RFP §3.3.2; SOW-0010c.

### 2. Design-Build Responsibility for System Selection

The RFP states "The County only has a concept in mind; therefore, it will be a design/build project" (RFP §3.4). The County specifies systems by function and performance intent (e.g., "high-recovery heating system," "high-volume air exchanger"), not by brand, model, or exact specification. The Mechanical Engineer carries full responsibility for translating these functional requirements into compliant, appropriately-sized systems.

Source: RFP §3.4.

### 3. Industrial Occupancy Drives Mechanical Sizing

The Addition is a heavy-equipment maintenance shop -- not a light-industrial or commercial building. Mechanical design must account for:
- Very large internal volumes (35 ft ceiling, ~13,000 sq ft footprint) with high infiltration from large overhead doors
- Frequent door cycling for motor scraper-class equipment
- High exhaust loads (diesel engine exhaust, welding fumes)
- Alberta Central region climate (cold winters; heating load dominant)
- Wash bay humidity and thermal loads (if heated)

ASSUMPTION: The above factors are standard mechanical design considerations for this occupancy type in Alberta; they are not explicitly enumerated in the RFP but are implied by the program.

### 4. System Integration -- Makeup Air and Exhaust Must Be Balanced

A forced-air makeup air unit (MUA) and a high-volume air exchanger are specified alongside exhaust fans for heavy equipment and welding. These systems must be designed as an integrated air-handling strategy. The MUA must be sized to replace air exhausted by the exhaust systems while maintaining the selected pressure strategy in the main shop to prevent cold air infiltration.

> **Enrichment [X-001]:** Building pressure strategy (positive, neutral, or zoned) is a key design decision that should be determined at the preliminary stage. Positive pressure in the main shop area is the conventional approach for industrial shops with large overhead doors, as it resists cold air infiltration during door openings. However, zones with exhaust-dominant loads (wash bay, welding station) may require a different pressure approach. The Mechanical Engineer should document the selected pressure strategy and its rationale in the Design Presentation. See Procedure Step 2.4 for the action item. ASSUMPTION: Pressure strategy selection is a standard early-stage mechanical design decision for industrial buildings; this is not explicitly required by the RFP but is implied by the air-handling system scope. (Source: RFP §3.4; SOW-0035 through SOW-0039. Enriched per X-001.)

Source: RFP §3.4; SOW-0035, SOW-0036, SOW-0037, SOW-0038, SOW-0039.

### 5. Coordination with Electrical and Plumbing is Mandatory from Preliminary Stage

The mechanical systems have significant interfaces with other disciplines. The canonical interdisciplinary interface list (see Specification REQ-003-01-11) includes:

| Interface | Description | Counterpart | Source |
|---|---|---|---|
| (a) | Natural gas service tie-in | Civil/Utility (PKG-018, SOW-0080) | Decomposition §SSOW-K |
| (b) | Mechanical equipment structural supports | Structural (PKG-002) | App B (Shop); ASSUMPTION |
| (c) | Electrical power for mechanical equipment | Electrical (PKG-004 / PKG-015) | App B-Elec; Decomposition §6 |
| (d) | Utility room layout shared with plumbing | Plumbing (PKG-006) | App B (Shop); Decomposition §6 |
| (e) | Crane runway clearance for ductwork and equipment | Structural (PKG-002) / Crane supplier | App B (Shop); SOW-0067 |

The preliminary design should explicitly call out these interfaces to enable coordinated final design.

> **Enrichment [X-002]:** This interface list has been aligned with Specification REQ-003-01-11 and Procedure Step 4.2 to provide a single canonical reference. Interface (e) for crane clearance was previously noted only in Procedure Step 3.2 and is now formalized. PROPOSAL per X-002: Mechanical Engineer to confirm completeness of the interface list. (Source: Decomposition PKG-003 exclusions; App B (Shop); SOW-0080; SOW-0067. Enriched per X-002.)

### 6. Code Compliance Must Be Considered from the Outset

Although the P.Eng. stamp applies to final IFC drawings, the Mechanical Engineer is responsible for ensuring the preliminary design approach is code-compliant from the start. Designing to code from the preliminary stage avoids costly re-design after County approval has been granted.

> **Enrichment [D-001]:** A dedicated preliminary code compliance check step should be performed before County submission (see Procedure Step 6.1a). This provides an enforcement mechanism for REQ-003-01-09 at the preliminary stage, rather than deferring code verification entirely to the IFC stage. PROPOSAL per D-001: Mechanical Engineer to conduct an internal discipline review against applicable code requirements prior to County submission. (Source: RFP §3.3.2; SOW-0008, SOW-0009. Enriched per D-001.)

Source: RFP §3.3.2; SOW-0008, SOW-0009.

---

## Considerations

### Heating System Selection

**High-recovery heating system** is specified (RFP §3.4; SOW-0035). In Alberta industrial shop contexts, radiant tube heaters (gas-fired infrared) and unit heaters are common high-recovery options. The large ceiling height (35 ft) and high door infiltration typical of heavy-equipment shops often favour radiant systems for efficiency. However, system selection is the Mechanical Engineer's responsibility and must be justified in the design presentation.

ASSUMPTION: High-recovery likely refers to a high-efficiency system with heat recovery capability; final interpretation is the Mechanical Engineer's professional judgement.

### Wash Bay Heating and Ventilation

The wash bay (single bay, 24 ft wide, for motor scraper-class equipment) is shown on App B (Shop) with overhead door access. Heating and ventilation requirements for the wash bay are not explicitly differentiated from the main shop in the RFP. ASSUMPTION: The wash bay requires its own heating and ventilation consideration given the wet environment and potential for freezing in Alberta winters. The Mechanical Engineer should address this explicitly.

The wash bay heating status (heated / unheated / freeze-protection-only) is a key missing datum identified in Datasheet B-001. This determination affects heating system sizing, MUA zone design, and ventilation strategy. See Specification REQ-003-01-12 for the requirement to address this at the preliminary stage.

Source: RFP §3.1, §3.4; App B (Shop). (Enriched per B-001, X-003.)

### Service Pit Ventilation

RFP §3.4 states the service pit must be "ventilated and lighted." The ventilation strategy (forced mechanical exhaust, passive, or combined) must be determined by the Mechanical Engineer. Below-grade pits can accumulate heavier-than-air gases; dedicated exhaust is standard practice in Alberta shop environments.

ASSUMPTION: A dedicated mechanical exhaust system for the service pit is likely required under Alberta Safety Codes; final determination is the Mechanical Engineer's responsibility.

### Mezzanine HVAC

The mezzanine is shown over the parts room, utility room, and wash bay (App B; RFP §3.4). It is intended for heavy storage (oil totes, pumping equipment). Whether the mezzanine requires its own HVAC zone (heating, ventilation) is not specified. ASSUMPTION: Basic heating and freeze protection for stored equipment is likely required; extent TBD by Mechanical Engineer.

### Ceiling Fans -- Mechanical vs. Electrical Interface

The 6 ceiling fans in the main shop (SOW-0040) are installed by the Mechanical Contractor (PKG-013, DEL-013-06) and powered by the Electrical Contractor (PKG-015). The Mechanical Engineer should confirm fan specifications (diameter, CFM, motor size) so that the Electrical Engineer can design appropriate circuits. Preliminary design should include a fan schedule.

Source: Decomposition SOW-0040; PKG-013; PKG-015.

### Building Pressure Strategy

> **Added per X-001 enrichment.**

The building pressure strategy (positive, neutral, or zoned) is a fundamental design decision that affects all air-handling components. Key considerations:

- **Positive pressure** in the main shop area resists cold air infiltration through large overhead doors during equipment entry/exit. This is the conventional approach for Alberta industrial shops.
- **Exhaust-dominant zones** (welding station, service pit) will inherently operate at negative pressure relative to the main shop. The MUA must compensate for this.
- **Wash bay** may require its own pressure management depending on heating and humidity control strategy.
- **Zoned approach** may be necessary if the wash bay, main shop, and service areas have significantly different exhaust and conditioning requirements.

The Mechanical Engineer should document the selected pressure strategy and its rationale in the Design Presentation. This decision directly affects MUA sizing, air exchanger configuration, and exhaust system balancing. (Source: Procedure Step 2.4 references this decision; Specification REQ-003-01-03, REQ-003-01-04, REQ-003-01-05. Enriched per X-001.)

### Preliminary Design Presentation Format

The RFP does not prescribe a format for the preliminary design presentation beyond requiring County approval. ASSUMPTION: The Design Presentation should include at minimum: a narrative describing system selections and rationale, a conceptual layout drawing or sketch showing system locations, a preliminary equipment list, a statement of applicable codes, and a completeness checklist per Specification D-002. Format should be sufficient for the County to make an informed approval decision.

---

## Trade-offs

| Trade-off | Option A | Option B | Evaluation Criteria | Recommendation | Source |
|---|---|---|---|---|---|
| Heating system type | Radiant tube (high-efficiency, well-suited to large volumes, cold climate, high door cycling) | Unit heaters / forced air (simpler installation, more uniform air distribution) | Capital cost, operating cost (energy efficiency), maintenance complexity, suitability for 35 ft ceiling height, heating response time after door cycling | ASSUMPTION: Both are viable; Mechanical Engineer to evaluate against heat loss calculations and capital/operating cost. Radiant systems typically have lower operating cost in high-ceiling applications but higher capital cost. | RFP §3.4; ASSUMPTION |
| Air distribution strategy | Dedicated MUA with separate exhaust system | Combined air handling unit with heat recovery | Capital cost, energy recovery potential, system complexity, maintenance access, code compliance with separate exhaust requirements | ASSUMPTION: Design-build responsibility; RFP specifies MUA and high-volume exchanger as separate items. Combined units may offer energy savings but increase system complexity. | RFP §3.4; App B |
| Service pit ventilation | Integrated with general shop exhaust | Dedicated pit exhaust fan | Code compliance (Alberta Safety Codes for below-grade spaces), reliability, capital cost, operational flexibility, safety margin for heavier-than-air gas accumulation | ASSUMPTION: Dedicated is standard practice for below-grade pits in Alberta; to be confirmed by Mechanical Engineer against Alberta Safety Codes. Dedicated system provides higher safety margin. | RFP §3.4; ASSUMPTION |
| Wash bay HVAC treatment | Fully conditioned (heated and ventilated) | Minimal heat (freeze protection only) | Capital cost, operating cost, year-round usability, humidity management, equipment wash quality in winter, freeze protection for plumbing | ASSUMPTION: Full conditioning preferred for year-round use; cost trade-off to be evaluated by design-build team. Freeze-protection-only reduces capital and operating cost but limits winter functionality. | RFP §3.1, §3.4; ASSUMPTION |

> **Enrichment [A-005, F-004]:** Evaluation criteria column has been added to the trade-off table to provide a basis for comparing options. Capital cost, operating cost, maintenance complexity, and energy efficiency are included as standard evaluation dimensions. Schedule implications are noted: more complex systems (combined air handling, full wash bay conditioning) may extend design and procurement timelines. The Mechanical Engineer should quantify these criteria at the preliminary stage where possible, or at minimum establish the evaluation framework for final design. PROPOSAL per A-005: Mechanical Engineer to populate quantitative estimates where available. PROPOSAL per F-004: include cost/schedule context in the Design Presentation rationale. (Source: ASSUMPTION -- standard engineering evaluation criteria. Enriched per A-005, F-004.)

---

## Examples

No worked examples are available from accessible sources. The RFP does not provide example calculations or reference comparable projects.

TBD -- Mechanical Engineer to provide precedent examples at design stage if useful for County communication.

---

## Conflict Table (for human ruling)

The items below represent ambiguities requiring resolution. Items marked with a lensing enrichment reference have had their audit trail strengthened.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| C-003-01-01 | SOW-0040 attributes 6 ceiling fans to Mechanical scope (PKG-013), but App B-Elec (per decomposition SSOW-E) is the citation. Fans may be electrical-furnished, mechanically-installed, or fully electrical. | Decomposition SOW-0040 (PKG-013 -- Mechanical Installation) | Decomposition SOW-0040 citation: App B-Elec | Specification REQ-003-01-07; Datasheet (Ceiling Fans row) | PROPOSAL: Mechanical Engineer specifies and coordinates fan installation; Electrical Engineer provides power -- fan procurement scope to be confirmed at contract clarification | TBD |
| C-003-01-02 | Service pit ventilation: RFP §3.4 states "ventilated and lighted service pit" but SOW-0028 (structural) is the primary reference. It is not explicit whether mechanical design (PKG-003) or building ventilation design carries the service pit ventilation requirement. **Resolution path [E-002]:** PM to obtain ruling from project lead on whether PKG-003 or PKG-011 owns service pit ventilation design. Until resolved, PKG-003 (Mechanical) is proceeding on the assumption that it owns this scope per A-002 enrichment of REQ-003-01-08. | RFP §3.4 ("Ventilated and lighted service pit area for mechanics to perform servicing under equipment") | Decomposition SOW-0028 in PKG-011 (structural); no explicit PKG-003 assignment for pit ventilation | Specification REQ-003-01-08; Guidance (Service Pit Ventilation); Procedure Step 2.5 | PROPOSAL: PM to obtain ruling from project lead. Interim: Mechanical Engineer (PKG-003) takes responsibility for service pit ventilation system design as part of overall shop ventilation (enriched per E-002). | TBD |

> **Enrichment [B-004]:** Conflict C-003-01-01 has been cross-referenced in Datasheet (Ceiling Fans row) and Specification REQ-003-01-07 Notes to ensure the ambiguity is visible wherever the ceiling fans are discussed. Cross-document references have been added per B-004.

> **Enrichment [E-002]:** Conflict C-003-01-02 has been updated with a resolution path. The PM should obtain a ruling from the project lead on scope ownership. Until resolved, documents proceed on the assumption that PKG-003 owns service pit ventilation design. The Procedure (Step 2.5) and Specification (REQ-003-01-08) are aligned with this interim position.
