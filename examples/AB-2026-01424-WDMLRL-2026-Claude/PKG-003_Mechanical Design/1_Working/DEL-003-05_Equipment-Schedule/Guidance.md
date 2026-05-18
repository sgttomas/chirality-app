# Guidance — DEL-003-05 Mechanical Equipment Schedule
**Deliverable ID:** DEL-003-05
**Name:** Mechanical Equipment Schedule
**Package:** PKG-003 Mechanical Design
**Discipline:** Mechanical Engineering
**Revision:** R1 (Pass 3 enrichment — 2026-02-26)
**Date:** 2026-02-25

---

## 1. Purpose

The Mechanical Equipment Schedule (DEL-003-05) exists to serve as the canonical, project-wide reference for all mechanical equipment to be installed in the New North Shop Addition. Its primary functions are:

1. **Procurement anchor** — Provides the performance specifications from which the mechanical contractor (PKG-013) can procure equipment consistent with the design intent.
2. **Drawing coordination hub** — Provides unique equipment tags that appear on all HVAC, ductwork, and exhaust plan drawings (DEL-003-02, DEL-003-03, DEL-003-04), ensuring a single point of truth for equipment identity.
3. **Commissioning baseline** — Establishes the design parameters against which commissioned performance is measured (DEL-020-01).
4. **County submission artifact** — Supports OBJ-003 (IFC design documentation) and OBJ-004 (mechanical systems to operational readiness), forming part of the design build submission to Camrose County.

The RFP (§3.4) specifies functional requirements for the shop's mechanical systems — heating, ventilation, exhaust — but leaves technology selection and performance engineering to the Design-Builder. This schedule is where those engineering decisions are formally recorded.

---

## 2. Principles

### 2.1 Industrial Context Governs Equipment Selection
This is a heavy equipment maintenance shop with 35-foot ceilings, diesel engine exhaust, welding fumes, and large overhead doors subject to frequent opening. ASSUMPTION: equipment selection must account for:
- High infiltration load when overhead doors are open (makeup air unit sizing is critical)
- Contaminant capture at source (exhaust hoses at tailpipes; welding capture hoods) rather than dilution-only strategies
- Destratification requirements at 35-foot ceiling height (ceiling fans serve to push warm air downward in heating mode)

These are principle-level considerations, not sourced from specific clauses of accessible documents. The Mechanical Engineer of record is responsible for confirming and applying them in the Calculation Package (DEL-003-06).

### 2.2 Schedule-Driven Design Build Workflow
Under CCDC 14-2013 (Design-Build Stipulated Price), the Design-Builder carries both design responsibility and cost risk. ASSUMPTION: equipment selections made in this schedule will be reflected in the stipulated price; the Mechanical Engineer should select equipment conservatively (proven product lines with known lead times) to manage procurement schedule risk against the December 31, 2026 completion deadline.

### 2.3 IFC Coordination Dependency
This schedule is not useful in isolation. Its value is realized only when:
- Equipment tags are applied consistently across all mechanical drawings
- Performance values are supported by calculations (DEL-003-06)
- The schedule is included in the IFC set stamped by a P.Eng.

The schedule should be developed concurrently with the HVAC and exhaust plan drawings — not as a downstream afterthought.

### 2.4 Preliminary Design Approval Gate
Per SOW-0010c and RFP §3.3.2, the Mechanical Engineer must obtain County approval of the preliminary design (DEL-003-01) before committing to IFC equipment selections. Equipment selections proposed in DEL-003-05 at the IFC stage should be consistent with the preliminary design approved by the County. If significant changes occur between preliminary and IFC, this should be flagged to the County for confirmation.

**Schedule impact if County approval is delayed (Pass 3 enrichment, F-001):** The County approval gate (REQ-012) is a hard prerequisite for IFC finalization. If County approval of DEL-003-01 is delayed or conditional, the following consequences should be anticipated:
- Equipment procurement cannot be committed (long-lead items at particular risk — see §4.1)
- Coordination data for Structural (PKG-002) and Electrical (PKG-004) engineers may be provisional, requiring rework if selections change after County review
- The IFC schedule milestone is directly gated by County approval timing; delays cascade to the December 31, 2026 project completion deadline (RFP §3.1, SOW-0091)
- ASSUMPTION: the Project Manager should establish a target date for County preliminary design submission early in the project and track it as a critical path item

> **Note:** The rationale for this gate is that the County, as Owner, must concur with the mechanical system approach before the Design-Builder commits to IFC-level detail and procurement. This is standard practice under CCDC 14-2013 design-build delivery. Source: RFP §3.3.2, SOW-0010c.

### 2.5 Definition of "High-Recovery Heating System" (Pass 3 enrichment, A-001)
The RFP phrase "high-recovery heating system" (SOW-0035, RFP §3.4) is undefined in the accessible source documents. This term governs a major equipment selection (HTG-001) and has no operational definition anywhere in the current document set. Different interpretations lead to materially different designs:
- "High recovery" as high-efficiency gas-fired equipment (e.g., condensing unit heater with 90%+ thermal efficiency)
- "High recovery" as waste-heat recovery from exhaust air streams (integrated with AEX-001 or MAU-001)
- "High recovery" as rapid temperature recovery after overhead door openings (emphasizing heating response time rather than steady-state efficiency)

**Decision framework:** The Mechanical Engineer should:
1. Document the chosen interpretation and its engineering basis in DEL-003-06
2. Present the interpretation to the County during preliminary design review (DEL-003-01)
3. Record the confirmed definition in this Guidance document or in DEL-003-06 for downstream reference

Until confirmed, this remains an open engineering decision. See Conflict Table CON-001.
Source: Guidance.md §3.1 (existing discussion); Datasheet.md §2.2 (HTG-001 row); semantic lensing item A-001.

---

## 3. Considerations

### 3.1 Heating System Technology Selection
The RFP requires a "high-recovery heating system" (SOW-0035; RFP §3.4). The phrase "high-recovery" is not further defined in the RFP. Potential technology options for industrial shops of this scale in Alberta include:

- **Infrared radiant tube heaters** — Common in high-bay shops; heat objects/people rather than air; compatible with high air change rates; do not integrate heat recovery from exhaust streams.
- **Unit heaters with heat exchanger** — Traditional forced-air heating; lower capital cost; less efficient.
- **Waste-heat recovery / make-up air combination unit** — Recovers heat from exhaust air streams; highest operating efficiency; typically higher capital cost.

**ASSUMPTION:** "High-recovery" in the RFP context most likely refers to a high-efficiency heating system (e.g., high-efficiency gas-fired unit heaters or radiant heaters coordinated with the makeup air unit). The specific technology is an engineering decision for the Mechanical Engineer of record. This selection has significant interaction with the makeup air unit (MAU-001) and air exchanger (AEX-001) sizing.

> This assumption should be confirmed or corrected by the Mechanical Engineer at preliminary design stage and during County preliminary design review.

### 3.2 Makeup Air Unit Sizing Criticality
The forced-air makeup air unit (MAU-001) is one of the most critical equipment selections for a shop of this size. With two 24-foot-wide drive-through repair bay doors and one 24-foot wash bay door at 35-foot ceiling height, the infiltration load when doors open is very large. ASSUMPTION: the MAU must be sized to maintain positive pressure and acceptable indoor temperature during door-open conditions, or a separate door vestibule/air curtain strategy must be adopted. This is a design judgment for the Mechanical Engineer.

**Air curtain / vestibule consideration (Pass 3 enrichment, C-002):** Standard industrial practice for high-bay shops with large overhead doors includes evaluation of air curtains as an alternative or complement to makeup air oversizing for infiltration control. Options to consider:
- **Air curtains at overhead doors** — Reduce infiltration load when doors are open; may allow a smaller MAU-001 sizing; require separate electrical connections and structural mounting
- **Vestibule / airlock design** — Physical separation reducing infiltration; requires additional floor space and structural framing; may conflict with drive-through bay geometry
- **MAU oversizing only** — Simpler mechanical design; higher operating cost during door-open events; larger equipment footprint

The RFP does not explicitly require or exclude air curtains. ASSUMPTION: the Mechanical Engineer should evaluate air curtain feasibility as part of the heating/ventilation system design and document the decision in DEL-003-06. If air curtains are selected, they should be added to this equipment schedule with their own tags.
Source: Guidance.md §3.2 (existing MAU discussion); standard industrial HVAC practice; semantic lensing item C-002.

### 3.3 Exhaust Hose System Design
RFP §3.4 (SOW-0038) requires "exhaust hoses and fans for heavy equipment in repair bays." Two bays are present (each 24' wide per App B). ASSUMPTION: this implies a direct-connect or proximity-capture vehicle exhaust extraction system (e.g., overhead reel-type hose drops or slide-rail systems), not dilution ventilation alone. The Mechanical Engineer should size the exhaust fans to achieve adequate tailpipe capture velocity per applicable industrial ventilation standards. Equipment brand and model are TBD pending design.

### 3.4 Welding Station Exhaust Relationship to Electrical Design
App B (Shop) shows a welding station at the north wall of the main shop area. RFP §3.4 and SOW-0039 require ventilation/exhaust at the welding station. The County is supplying welding equipment specifications (SOW-0204 — County responsibility). ASSUMPTION: the welding exhaust system design may depend on the type and number of welding stations the County ultimately specifies. If the County's welding equipment specification is not available at preliminary design stage, the Mechanical Engineer should design for a conservative scenario (e.g., one heavy-duty MIG/flux-core station) and flag the dependency.

### 3.5 Ceiling Fan Coordination with Structure and Overhead Cranes
Six ceiling fans are required in the main shop (SOW-0040) at 35-foot ceiling height. Mounting of high-bay ceiling fans at this height requires structural attachment points (PKG-002 structural design) and electrical drops (PKG-015). ASSUMPTION: the structural engineer must be made aware of the fan loads and positions during structural design. The Mechanical Engineer should coordinate fan locations with the overhead crane girder layout (two 5-tonne cranes per SOW-0067) to avoid interferences.

**Crane/fan interference coordination protocol (Pass 3 enrichment, X-001):** The two 5-tonne overhead cranes (SOW-0067) create a significant coordination constraint for ceiling fan placement. Crane girders, end trucks, and runway beams occupy zones at or near the ceiling level where fans would otherwise be positioned. The Mechanical Engineer should:
1. Obtain crane runway and girder layout from the Structural Engineer (PKG-002) early in design
2. Map proposed fan locations against the crane envelope (including travel path and hook height)
3. Confirm that fan blade sweep zones do not encroach on crane girder clearances or create obstruction hazards
4. If conflicts exist, adjust fan positions and document the revised layout in the HVAC Plans (DEL-003-02)
5. Coordinate with the Electrical Engineer (PKG-004/015) for revised electrical drop locations if fans are relocated

ASSUMPTION: this coordination should occur during Phase 2 (Preliminary Equipment Schedule) before fan positions are committed. Source: Guidance.md §3.5 (existing mention); SOW-0067 (overhead cranes); semantic lensing item X-001.

### 3.6 Service Pit Ventilation Gap
The RFP (SOW-0028) requires a "ventilated and lighted service pit" but does not enumerate a specific mechanical system in the SOW-0035-SOW-0040 list for this purpose. This is a potential scope gap. Options include: (a) a dedicated low-point exhaust fan discharging to exterior; (b) coverage by the main shop exhaust/makeup air system if air circulation geometry permits. ASSUMPTION: this requires engineering judgment and must be resolved in the Calculation Package (DEL-003-06). A placeholder tag (EXH-004) is reserved in the Datasheet.

### 3.7 Wash Bay Ventilation
The wash bay is an enclosed single bay (24' wide, motor-scraper sized per RFP §3.4). Ventilation for the wash bay is not explicitly itemized in SOW-0035-SOW-0040 beyond the general high-volume air exchanger (SOW-0036) and exhaust system scope. ASSUMPTION: the wash bay may require dedicated exhaust for moisture, cleaning chemicals, and drainage odors — this should be addressed in the Calculation Package and, if required, added to this schedule.

### 3.8 Indoor Design Temperature Basis (Pass 3 enrichment, E-001)
The Datasheet (§3.1) lists indoor design temperatures as ASSUMPTION values (18 C for Main Shop, 21 C for Office) without attribution to a specific source document. These values directly drive HTG-001 heating capacity sizing and MAU-001 discharge temperature calculations. The Guidance document does not currently confirm or reference these temperature assumptions.

**Resolution needed:** The Mechanical Engineer should:
1. Confirm indoor design temperatures from applicable standards (ASHRAE 55, Alberta Building Code, or project-specific requirements)
2. Record the confirmed values and their basis in DEL-003-06 or in this Guidance document
3. Update the Datasheet with confirmed values and source references

Until confirmed, these temperatures remain unattributed ASSUMPTION values. See Conflict Table CON-006.
Source: Datasheet.md §3.1; semantic lensing item E-001.

---

## 4. Trade-offs

### 4.1 Equipment Efficiency vs. First Cost vs. Lead Time
Higher-efficiency equipment (e.g., condensing unit heaters, HRV units with high effectiveness) reduces operating costs for the County but increases capital cost and may increase lead time. Given the December 31, 2026 completion deadline and the Alberta procurement environment, ASSUMPTION: the Mechanical Engineer should identify equipment with acceptable lead times at the time of design. Extended lead-time items (e.g., large custom makeup air units) should be identified early in the design phase and potentially procured on long-lead order.

**Long-lead procurement decision framework (Pass 3 enrichment, F-003):** The current guidance identifies lead time as a factor but does not provide actionable thresholds. The Mechanical Engineer should:
1. At equipment selection stage (Procedure Step 2.3), obtain lead time estimates from at least two suppliers for each major equipment item (HTG-001, AEX-001, MAU-001)
2. Compare quoted lead times against the available procurement window (time from County approval of DEL-003-01 to required site delivery, working backward from December 31, 2026 deadline)
3. If any equipment lead time exceeds the available procurement window, flag it to the Project Manager as a **long-lead item** requiring:
   - Early procurement authorization (potentially before all IFC details are finalized)
   - Specification flexibility to allow acceptable alternates with shorter lead times
   - Risk assessment of schedule impact if the item is not procured early
4. ASSUMPTION: the threshold for "long-lead" in this project context is TBD but should be defined early; a reasonable starting point is any item with a quoted lead time exceeding 60% of the available procurement window

Source: Guidance.md §4.1 (existing discussion); RFP §3.1, SOW-0091 (December 31, 2026 deadline); semantic lensing item F-003.

### 4.2 Centralized vs. Distributed Heating
A single large central heating system may be simpler to control but harder to maintain. Multiple unit heaters are more resilient (one fails, others continue) but require more electrical/gas connections. ASSUMPTION: the choice is an engineering judgment; the equipment schedule should reflect whatever system architecture the Mechanical Engineer selects, with rationale documented in DEL-003-06.

### 4.3 Capture-at-Source vs. Dilution Ventilation for Exhaust
The RFP explicitly requires exhaust hoses and fans at repair bays (SOW-0038) and welding station exhaust (SOW-0039), indicating capture-at-source strategies are required. The high-volume air exchanger (SOW-0036) provides general dilution ventilation. These are complementary, not alternatives. No trade-off exists on this point — both are required per the RFP.
**Source:** RFP §3.4, SOW-0036, SOW-0038, SOW-0039

---

## 5. Examples

### 5.1 Typical Equipment Schedule Row Format (ASSUMPTION — illustrative only; not sourced from project documents)

The following illustrates the expected row format. Actual values are TBD pending Mechanical Calculation Package (DEL-003-06):

| Tag | Description | Qty | Location | Airflow (CFM) | Heating Cap (kW) | Fuel | Electrical | Weight (kg) | Acoustics (dBA) | Mfr/Model Basis | Dwg Ref |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MAU-001 | Forced-Air Makeup Air Unit | 1 | Main shop — overhead | TBD | TBD | Natural Gas | 3-ph, TBD V | TBD | TBD | TBD | M-001 |
| EXH-001 | Equipment Exhaust Fan & Hose — Bay 1 | 1 | Repair Bay 1 | TBD | -- | -- | 1-ph/3-ph, TBD V | TBD | TBD | TBD | M-004 |

> This is a structural example only. Numeric values are placeholders; all real values require engineering calculation.
> **Note (Pass 3):** Weight and Acoustics columns added to align with Specification REQ-003 minimum data fields (per X-003 enrichment).

---

## Conflict Table (for human ruling)

The items below are flagged as open engineering decisions, scope ambiguities, or unresolved data conflicts requiring resolution by the Mechanical Engineer or County.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-001 | "High-recovery heating system" is undefined in the RFP. Interpretation determines equipment type and cost significantly. | RFP §3.4 ("high-recovery heating system") | No further definition in accessible sources | Datasheet §2.2 (HTG-001), Specification REQ-004, Guidance §3.1, §2.5 | PROPOSAL: Mechanical Engineer of record to define and document interpretation in Calculation Package (DEL-003-06); County to confirm at preliminary design review (DEL-003-01) | TBD |
| CON-002 | Service pit ventilation is required (SOW-0028) but not enumerated in the mechanical system list (SOW-0035-SOW-0040). Scope gap exists. | RFP §3.4, SOW-0028 ("ventilated and lighted service pit") | SOW-0035-SOW-0040 (mechanical equipment list — no pit exhaust item) | Datasheet §2.2 (EXH-004 row), Specification REQ-010 | PROPOSAL: Mechanical Engineer to resolve in Calculation Package; add pit exhaust fan to schedule if required; confirm scope inclusion with County | TBD |
| CON-003 | Wash bay ventilation system is implied by wash bay occupancy but not explicitly listed in SOW-0035-SOW-0040 or called out separately. | RFP §3.4 (wash bay described), App B (Shop) (wash bay shown) | SOW-0035-SOW-0040 (no explicit wash bay ventilation item beyond general exchanger) | Datasheet §2.2 (note), Guidance §3.7 | PROPOSAL: Mechanical Engineer to determine if wash bay is served by AEX-001 or requires dedicated exhaust; update schedule accordingly | TBD |
| CON-004 | Welding exhaust system design depends on County-supplied welding equipment specifications (SOW-0204), which are not yet available. | SOW-0039 (welding exhaust required), App B (welding station location shown) | SOW-0204 (County supplies welding equipment specs — timing unknown) | Datasheet §2.2 (EXH-003), Specification REQ-008, Guidance §3.4 | PROPOSAL: Mechanical Engineer to design for conservative scenario at preliminary stage; County to provide welding specs before IFC issue | TBD |
| CON-005 | Material change threshold for post-County-approval deviations (REQ-016) is undefined. Without a threshold, change management cannot be consistently applied. (Pass 3 enrichment, D-001) | Specification REQ-012 (County approval required) | Specification REQ-016 (material change threshold TBD) | Specification §2.3 (REQ-016), Guidance §2.4, Procedure Phase 3 | PROPOSAL: Mechanical Engineer to define material change threshold at project start; County to confirm acceptable threshold | TBD |
| CON-006 | Indoor design temperatures (18 C Main Shop, 21 C Office) are stated as unattributed ASSUMPTIONs in the Datasheet but not confirmed by any accessible source document. These values directly drive heating equipment sizing. (Pass 3 enrichment, E-001) | Datasheet §3.1 (18 C and 21 C assumptions) | No accessible source confirmation (Guidance silent on indoor design temperatures) | Datasheet §3.1, Specification REQ-004, Guidance §3.8 | PROPOSAL: Mechanical Engineer to confirm indoor design temperatures and record basis in DEL-003-06 or Guidance | TBD |

## Applicable Standards Reference (Pass 3 enrichment, B-005)

For ease of reference, the following is the canonical list of standards applicable to this deliverable, harmonized across all four documents. Individual documents may reference subsets of this list in context.

| Standard | Full Title | Applicability | Edition |
|---|---|---|---|
| Alberta Building Code | Provincial building code — mechanical provisions | Code compliance for all HVAC equipment | TBD — to be confirmed at design start |
| Alberta Safety Codes Act | Safety code compliance | All building systems | Current |
| ASHRAE 62.1 | Ventilation for Acceptable Indoor Air Quality | Minimum ventilation rates | TBD — to be confirmed |
| ASHRAE 90.1 | Energy Standard for Buildings | Equipment efficiency | TBD — to be confirmed |
| NFPA 91 | Exhaust Systems for Air Conveying of Vapors, Gases, Mists, and Particulate Solids | Equipment and welding exhaust | TBD — ASSUMPTION: applicable |
| ACGIH Industrial Ventilation Manual | Industrial Ventilation: A Manual of Recommended Practice | Welding exhaust capture design | TBD — ASSUMPTION: applicable |
| CSA B149.1 | Natural Gas and Propane Installation Code | Gas-fired equipment connections | TBD — ASSUMPTION: applicable |

> **Note (Pass 3, B-005):** This consolidated table addresses the inconsistent standards referencing across documents identified in semantic lensing. Each document continues to reference the standards relevant to its own content, but this table provides the single canonical list. Source: Specification.md §3; Procedure.md §2.2; Datasheet.md §5; semantic lensing item B-005.
