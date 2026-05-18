# Guidance — DEL-003-07 Mechanical Specification

---

## Purpose

This Guidance document explains **why** DEL-003-07 (Mechanical Specification) exists, what design intent and principles should inform it, and what trade-offs and considerations the Mechanical Engineer and design-builder should be aware of when developing and finalizing the specification content.

DEL-003-07 is the normative written specification for all mechanical systems in the WDMLRL Maintenance Shop Addition. It translates RFP §3.4 design requirements and SOW-0013 scope into enforceable material, equipment, and installation standards. The specification is the primary contractual reference for mechanical installation under PKG-013 (Mechanical & HVAC Installation).

**Context:** This is a design-build project; the County has described intent, not a fully engineered solution. The Mechanical Engineer has significant design latitude within the stated requirements.

---

## Principles

### P-1: Occupant Safety Drives Ventilation Design

The shop houses diesel/gasoline heavy equipment, welding operations, and below-grade pit work — all generating toxic or asphyxiating gases. Ventilation system adequacy is a life-safety issue, not merely a comfort measure.

- Exhaust systems for equipment bays and the welding station must achieve adequate capture and dilution to meet occupational exposure limits (OELs).
- Below-grade pit ventilation must prevent CO and fuel vapour accumulation.
- Makeup air must be sufficient to replace exhausted air volumes and maintain positive pressure, preventing uncontrolled infiltration of cold air through doors and gaps.

**Source:** RFP §3.4 (service pit, exhaust hoses, welding ventilation); applicable Alberta OH&S Code and industrial ventilation standards (ASSUMPTION: applicable; specific references location TBD).

### P-2: The 35 ft Ceiling Height is Both an Asset and a Design Constraint

The concrete structure ceiling height of 35 ft provides crane clearance and operational flexibility. However, it creates significant thermal stratification — heated air rises and accumulates near the ceiling, while the occupied zone remains cold.

- Ceiling fans (6 units per Decomposition SOW-0040) serve the primary function of destratifying heat, making the heating system effective.
- Ductwork and exhaust drops must account for the long vertical runs and coordinate with crane travel paths.
- High-volume air exchange must be designed to circulate air through the full height of the space, not just at lower levels.

**Source:** RFP §3.4; App B (Shop); Decomposition SOW-0040.

### P-3: High-Recovery Heating is an Explicit Owner Requirement

The RFP specifically calls for a "high recovery heating system" (RFP §3.4). This phrasing indicates the Owner's preference for a system that recovers heat from exhaust gases or internal heat sources, rather than a simple direct-fired unit. The intent is operating cost efficiency for an industrial building that will have significant ventilation air turnover.

- The Specification should require that heating equipment efficiency ratings meet or exceed a defined threshold (TBD by the Mechanical Engineer based on system type selected).
- The Specification should address heat recovery from the air exchanger if technically and economically feasible.

**Rationale gap — heat recovery as normative vs. optional:** The RFP §3.4 uses the phrase "high recovery heating system," which indicates explicit Owner intent for heat recovery capability, not merely energy-efficient heating. However, Specification REQ-M-003 currently treats heat recovery as "encouraged" rather than required. The Mechanical Engineer should determine whether heat recovery should be elevated to a normative (mandatory) requirement based on:
- Owner's stated intent ("high recovery" language);
- Lifecycle cost analysis showing payback period for heat recovery equipment vs. standard equipment in an Alberta cold-climate industrial building with high ventilation air turnover;
- Whether the air exchanger type (e.g., ERV vs. simple exhaust-only) is within the design-builder's discretion or should be constrained by specification.

This is an open design decision that affects both Specification REQ-M-003 strength and the Trade-offs table (ERV vs. exhaust-only row). *(Lensing ref: F-005)*

**Source:** RFP §3.4.

### P-4: Design-Build Latitude Requires Specification to Define Minimum Performance, Not Prescriptive Products

Because this is a CCDC 14–2013 design-build contract, the Proponent selects the means and methods. The Mechanical Specification should define:
- Minimum performance criteria (heating capacity, air change rates, capture velocities, etc.) rather than specifying brand names.
- Acceptable equipment categories with performance thresholds.
- Coordination and interface requirements that constrain selection.

This approach preserves the design-builder's flexibility while protecting the Owner's functional outcome.

**Source:** RFP §2.7; CCDC 14–2013 design-build framework.

### P-5: Coordination Across Disciplines is Critical

Mechanical systems in a 13,000 sq ft industrial shop with 35 ft ceilings, two overhead cranes, a below-grade service pit, and a wash bay create extensive coordination requirements:

- **Structural:** Ductwork penetrations through the concrete structure; mechanical equipment curbs and supports on the roof/ceiling; crane girder clearance for hanging exhaust hoses.
- **Electrical:** Power supply to all mechanical units; control wiring for thermostats, VFDs, and interlock systems; ceiling fan circuits.
- **Plumbing:** Wash bay drainage and mud sump interface with floor drainage; condensate drainage from HVAC units.
- **Architectural:** Equipment room locations; louver and intake/exhaust wall penetrations; clearances in utility room.

The Specification should include explicit coordination requirements and assign interface responsibilities.

**Source:** RFP §3.3.2; Decomposition PKG-003 ("Dependencies: Plumbing, electrical, structural").

---

## Considerations

### C-1: Heating System Type Selection

The RFP does not prescribe a specific heating technology beyond "high recovery." Common options for large industrial shops in Alberta include:

| Option | Advantages | Disadvantages |
|---|---|---|
| High-efficiency infrared radiant tube heaters | Direct radiant heat to floor/equipment; high efficiency; works well with high ceilings | Requires adequate clearance; ceiling fans still needed for stratification at floor level |
| High-efficiency unit heaters (forced-air) | Familiar technology; integrates with makeup air | Less effective at 35 ft ceiling without destratification fans |
| In-floor radiant hydronic | Extremely comfortable; efficient for high-ceiling spaces | High capital cost; long lead time; incompatible with rapid heating after cold start |
| Combination systems | Flexibility; redundancy | Coordination complexity |

The Mechanical Engineer should select based on lifecycle cost analysis, Alberta climate load calculations, and interface with the makeup air unit.

**Note:** System selection is TBD by design. The Specification shall document the selected system and minimum performance requirements.

### C-2: Makeup Air and Exhaust Balancing

A shop with heavy equipment exhaust drops, welding exhaust, and a high-volume air exchanger will exhaust a significant volume of air. If makeup air supply is insufficient:
- Building will operate under negative pressure.
- Cold outside air infiltrates through large overhead doors.
- Heating system is overwhelmed.
- Combustion appliances (if any) may backdraft.

The Specification should require that makeup air volume be calculated to match or exceed total exhaust volumes, with a documented air balance calculation included in DEL-003-06.

**Source:** RFP §3.4; engineering best practice (ASSUMPTION).

### C-3: Welding Station Exhaust — Local vs. Dilution Ventilation

Dilution ventilation (general shop air change) alone is generally insufficient to control welding fume exposure at the source. The RFP specifically requires a welding station exhaust/ventilation system (RFP §3.4; App B (Shop)). The Specification should require local exhaust ventilation (LEV) at the welding station with:
- A capture device (fume arm, hood, or equivalent) positioned at the source.
- An exhaust fan sized for the required capture velocity.
- An exhaust duct routed to the building exterior.

The specification should not rely on general shop ventilation to meet welding fume OELs.

**Source:** RFP §3.4; ACGIH Industrial Ventilation (ASSUMPTION: applicable standard; location TBD).

### C-4: Service Pit Ventilation Code Requirements

Below-grade spaces in buildings where vehicles are operated are addressed by specific code provisions (typically under the Alberta Safety Codes / National Building Code and applicable fire/mechanical codes). The Mechanical Engineer should confirm:
- Whether the pit qualifies as a "repair garage" for code purposes.
- The required ventilation rate (volume per minute per floor area or per vehicle).
- Whether continuous mechanical ventilation is required during all occupancy periods.

**TBD (requires human ruling):** Confirm whether the service pit qualifies as a "repair garage" under Alberta Safety Codes and what ventilation rate applies. This classification directly affects REQ-M-006 ventilation rate requirements and may trigger additional fire/gas detection requirements. The AHJ and/or Mechanical Engineer must determine the code classification before the ventilation rate can be finalized. *(Lensing ref: A-003)*

**Source:** RFP §3.4; ASSUMPTION regarding applicable code provisions — specific code section TBD pending engineer's review.

### C-5: Crane Clearance and Ductwork Routing

The two 5-tonne overhead cranes on trolleys (App B (Shop)) operate on crane rails at high level within the main shop area. Mechanical ductwork, exhaust drops, and equipment suspended from structure must maintain adequate clearance from crane travel paths. The Mechanical Engineer must:
- Obtain structural crane girder heights and clearance envelopes from the Structural Engineer (PKG-002).
- Route all suspended mechanical elements outside crane clearance zones.
- Coordinate with the Structural Engineer on any penetrations required through crane girder framing.

**Source:** App B (Shop) — 5-tonne cranes shown; RFP §3.4 ("2 – 5-tonne overhead cranes on a trolley").

### C-6: Wash Bay Humidity and Freeze Protection

The enclosed wash bay will generate significant humidity and, if not properly ventilated, will promote condensation and potential freeze damage to building elements.
- Exhaust ventilation in the wash bay is required to remove moisture-laden air.
- Heating in the wash bay must maintain temperatures above freezing at all times when the bay is not in active use.
- Coordination required with the plumbing drain and mud sump systems.

**Source:** RFP §3.4 ("Single enclosed bay dedicated for washing large equipment"); App B (Shop).

### C-7: Cold-Start Heating Strategy

The building will experience cold-soak conditions during overnight and weekend shutdowns in Alberta winter. With a 35 ft ceiling, large thermal mass (concrete structure, steel plates in floor), and 13,000 sq ft footprint, bringing the building from cold-soak to operating temperature requires a deliberate heating strategy.

Considerations the Mechanical Engineer should address:
- **Thermal mass recovery time:** How long will it take to bring the building from cold-soak (potentially -30C or below) to comfortable working temperature? This affects work scheduling and energy consumption.
- **Staged heating:** Whether primary heating should run at reduced setback temperature overnight (continuous low-level) vs. full cold-start each morning.
- **Radiant vs. convective:** Radiant tube heaters heat occupants and equipment directly and may provide faster perceived comfort despite cold air temperatures, which may be advantageous for cold-start scenarios.
- **Ceiling fan integration:** During cold-start, ceiling fans must be coordinated with heating to push warm air down without creating uncomfortable drafts at floor level.
- **Energy cost implications:** Continuous setback heating may use more total energy than cold-start, but cold-start may require oversized equipment — this is a design trade-off.

**Source:** Guidance P-2, P-3 (ceiling height and high-recovery heating context); ASSUMPTION: cold-start strategy is a significant operational knowledge gap for Alberta industrial buildings with large thermal mass. *(Lensing ref: E-001)*

### C-8: Ductwork Material Standards and Insulation

Ductwork material selection is a significant design decision for a large industrial building with 35 ft ceilings and Alberta climate temperature differentials. The Mechanical Engineer should address:

- **Ductwork material:** Galvanized steel is standard for industrial HVAC; confirm gauge and construction standard (e.g., SMACNA HVAC Duct Construction Standards or equivalent).
- **Insulation requirements:** Ductwork carrying tempered air through unconditioned or high-ceiling spaces may require insulation to prevent condensation and reduce heat loss. Insulation type and thickness should be specified per applicable energy code and condensation analysis.
- **Fire rating:** Ductwork penetrating fire-rated assemblies (e.g., between wash bay and main shop, or through mezzanine floor) must comply with applicable fire code requirements for fire dampers and rated enclosures.
- **Energy efficiency:** Insulated ductwork reduces heating energy loss, supporting the "high recovery" intent of the RFP.

**Source:** ASSUMPTION: ductwork material and insulation standards are necessary specification content for industrial HVAC; specific standards TBD by Mechanical Engineer. *(Lensing ref: X-001)*

### C-9: Post-Occupancy Performance Validation

The current document set defines verification through the construction and commissioning phases (TAB report, Safety Code inspections, CCC). However, there is no mechanism for the Owner to evaluate long-term mechanical system performance after occupancy.

Considerations:
- **Warranty period performance review:** RFP §2.10 establishes a two-year guarantee period. The Owner could use this period to evaluate whether the mechanical systems achieve the intended comfort, safety, and efficiency outcomes during actual operational conditions (e.g., winter heating performance, exhaust system effectiveness during heavy equipment operations).
- **Seasonal commissioning:** Some mechanical systems (e.g., heating, air exchange) may perform differently in winter vs. summer. A seasonal commissioning check during the first winter of operation could validate design assumptions.
- **Operational feedback:** Maintenance shop operators (mechanics) are the end users. A structured feedback mechanism (e.g., post-occupancy survey at 6 and 12 months) could identify performance issues not captured during formal commissioning.

**Source:** RFP §2.10 (guarantee period); RFP §2.14 (completion and acceptance); ASSUMPTION: post-occupancy validation is good practice but not explicitly required by the RFP. *(Lensing ref: D-003)*

---

## Trade-offs

| Trade-off | Option A | Option B | Recommendation |
|---|---|---|---|
| Heating technology | Radiant tube (high capital, low operating cost) | High-efficiency unit heaters (lower capital, potentially higher operating cost) | TBD by Mechanical Engineer based on lifecycle cost analysis and ceiling height considerations |
| Makeup air tempering | Full heat (high comfort, higher energy use) | Partial heat/untempered (lower energy, risk of cold spots and condensation) | Full tempering recommended for Alberta climate (ASSUMPTION) |
| Exhaust fan control | Continuous operation | Demand-controlled (CO/VOC sensors) | Demand-controlled preferred for energy efficiency but adds complexity; TBD by design |
| Air exchanger type | ERV (energy recovery ventilator) | Simple exhaust-only | ERV preferred for energy recovery (aligns with "high recovery" intent of RFP §3.4); TBD |

---

## Examples

No directly applicable example projects were accessible in the source documents. The conceptual floor plan in App B (Shop) provides spatial layout information relevant to mechanical system placement.

**System layout notes from App B (Shop):**
- Welding station is shown at the northeast corner of the main shop area.
- The Service Pit runs along the east side of the main shop bays.
- The wash bay is at the southeast corner, separated by a partition.
- The utility room houses the 50,000L water storage cistern (plumbing system — coordination interface for the mechanical designer).
- Mezzanine is above parts room, utility room, and wash bay; mechanical equipment access and penetrations must account for this mezzanine level.

---

## Vocabulary Normalization Notes

The following terminology normalization has been applied across the four documents to ensure consistent usage. *(Lensing ref: B-003)*

| Term | Normalized Usage | Previous Variants | Notes |
|---|---|---|---|
| General building exhaust fan(s) | "General Building Exhaust Fan(s)" — used consistently in Datasheet (Mechanical Systems table), Procedure (Step 1 checklist), and this Guidance document | Datasheet previously used "Exhaust Fan(s)"; Procedure used "General building exhaust fan(s)" | This term refers to the exhaust fan(s) per Decomposition SOW-0066, distinct from the equipment exhaust (REQ-M-004) and welding exhaust (REQ-M-005). Scope boundary is discussed in CONF-M-02. |

---

## Conflict Table (for human ruling)

**NOTE:** All three conflicts below have Human Ruling = TBD. These must be resolved before the specification can be finalized, as they affect scope boundaries, equipment counts, and system classifications that directly drive specification content. Resolution requires County project representative and/or MEP coordination meeting input. *(Lensing ref: E-003)*

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-M-01 | Ceiling fan count: Decomposition cites SOW-0040 as "6 ceiling fans" referencing App B-Elec; App B (Shop) floor plan does not explicitly label ceiling fans or state a count. | Decomposition (SOW-0040, App B-Elec reference) | App B (Shop) — no explicit fan count on conceptual floor plan | Specification REQ-M-007; Datasheet Attributes | Decomposition SOW-0040 (derived from App B-Elec which was not independently accessible) | TBD |
| CONF-M-02 | Exhaust fan scope: REQ-M-004 (equipment exhaust hoses and fans) and REQ-M-007 (ceiling fans) are distinct; however, Decomposition SOW-0066 references "exhaust fan(s) as shown on electrical drawing" which may represent a separate general exhaust fan not covered under REQ-M-004 or REQ-M-005. Scope boundary between mechanical and electrical packages for this exhaust fan is unclear. | Decomposition SOW-0066 (electrical package — App B-Elec) | RFP §3.4 (mechanical scope); this Specification REQ-M-004/REQ-M-005 | Specification Scope exclusions; REQ-M-004, REQ-M-005 | Needs MEP coordination meeting to clarify; PROPOSAL: exhaust fan(s) per SOW-0066 are general building exhaust assigned to mechanical package with electrical supply from PKG-004 | TBD |
| CONF-M-03 | Service pit ventilation: RFP §3.4 states the pit is "ventilated and lighted." The lighting is clearly electrical. Whether the pit ventilation is a dedicated mechanical system or served by the general shop ventilation is not specified. | RFP §3.4 | No additional RFP clarification available | Specification REQ-M-006; Procedure Steps | PROPOSAL: Dedicated mechanical forced ventilation for pit per code; general shop air change is supplemental only | TBD |
