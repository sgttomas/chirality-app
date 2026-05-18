# Guidance: DEL-004-09 Electrical Specification

---

## Purpose

DEL-004-09 is the written Electrical Specification for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It exists to give the electrical design team, reviewers, and construction team a normative document that defines what the electrical system must deliver — complementing the drawing deliverables (DEL-004-02 through DEL-004-07) which define where and how.

Within the project's design-build structure (CCDC 14–2013), the Electrical Specification is part of the IFC package and governs the electrical installation contractor (PKG-015). It supports two project objectives:
- **OBJ-003:** Produce complete, P.Eng.-stamped IFC design documentation across all disciplines before construction begins.
- **OBJ-005:** Install and commission all electrical and low-voltage systems to operational readiness.

The specification is not a standalone construction tender document. It is a design-build project document: the Electrical Engineer who produces this specification is also responsible for the design and the stamped drawings.

---

## Principles

### Principle 1: Follow the Conceptual Electrical Drawing as the Baseline
The Owner's intent is fully expressed in Appendix B (Electrical) of the RFP. That drawing contains the circuit types, fixture counts, dedicated equipment circuits, and low-voltage system requirements. The Electrical Engineer should treat App B as the floor — not the ceiling — and use professional judgment to ensure a compliant, safe, and functional installation. Do not downgrade any element shown on App B without Owner direction.
*(Source: App B (Electrical); RFP §3.4)*

### Principle 2: Three-Phase Power is Non-Negotiable
The RFP explicitly states the building shall run on three-phase power. The single-line diagram, panel design, and distribution architecture must all be three-phase throughout. Single-phase sub-panels may be acceptable in limited areas (e.g., office) but the main service shall be three-phase.
*(Source: RFP §3.4; Decomp SOW-0051)*

### Principle 3: Industrial Use Class — Size for Actual Loads
This is a heavy equipment maintenance shop. The electrical system must support simultaneous use of overhead cranes, welding equipment, compressors, high bay lighting, and exhaust systems. Demand factor assumptions should be conservative (i.e., assume high coincident load). The calculation package (DEL-004-08) must demonstrate adequate service capacity.
*(Source: RFP §3.4; App B (Electrical))*

### Principle 4: Welding Receptacle Density and Distribution
The RFP calls for "multiple" high-voltage welding-grade receptacles throughout the shop. The conceptual drawing shows 50 A / 240 V receptacles distributed along the shop walls and welding station area. The Electrical Engineer should ensure receptacle spacing allows welding operations throughout the full shop floor without extension cord runs that exceed safe practice.
*(Source: RFP §3.4; App B (Electrical); Decomp D-009)*

### Principle 5: Crane Power Requires Manufacturer Coordination
Crane circuit design (feeders, runway conductors, runway disconnects) is dependent on the crane equipment specification. The Electrical Engineer should either obtain the crane specification from the project team before finalizing the electrical design, or flag this as an outstanding input in the calculation package. Do not assume load.
*(Source: App B (Electrical); Decomp SOW-0059, Decomp SOW-0067)*

### Principle 6: Low-Voltage Systems are In Scope
Security camera wiring and 2-way radio antenna wire are explicitly required by App B (Electrical). These are often omitted when scope is ambiguous; they are not ambiguous here. The low-voltage plans (DEL-004-07) must address both systems. System specifications (camera counts, cable types, antenna routing) require Owner input.
*(Source: App B (Electrical); Decomp SOW-0064, Decomp SOW-0065)*

### Principle 7: Identify Governing Code Editions as a First Design Step
Before proceeding with detailed electrical design, the Electrical Engineer should identify and document the specific editions of all governing codes and standards currently in force in Alberta, including at minimum: (a) the Canadian Electrical Code (CEC) Part I edition adopted by Alberta, (b) the Alberta Safety Codes Act regulations applicable to electrical installations, (c) the Alberta Building Code edition (for emergency/egress lighting and occupancy classification), and (d) any applicable Alberta OH&S Code sections for industrial workspace illumination. This determination should be recorded in the Specification Standards table and referenced throughout the design. Without confirmed editions, compliance determination is incomplete.
*(Source: ASSUMPTION — standard practice for Alberta electrical design; no specific edition cited in RFP or App B. Lensing ref: D-001)*

---

## Considerations

### Consideration 1: Electrical Service Availability at Site
The site is at SW 14–44–21–W4, near Ferintosh, Alberta — a rural location. The Electrical Engineer should confirm early in design whether three-phase power is available at the site boundary, and if not, whether a transformer upgrade or new service entry is required. This is a design risk that could affect service sizing, utility coordination timelines, and cost.
*(Source: RFP §1.0; Decomp SOW-0081; ASSUMPTION — utility capacity not confirmed in available sources)*

### Consideration 2: Wash Bay Electrical Environment
The wash bay involves water use (washing large equipment), drainage to a mud sump, and high bay lighting. The electrical design for the wash bay must address wet/damp location requirements for fixtures, receptacles, and wiring methods. The Electrical Engineer shall apply the appropriate CEC ratings (ASSUMPTION: CEC Part I, current Alberta edition).
*(Source: App B (Electrical); RFP §3.4; Decomp SOW-0027a)*

### Consideration 3: Service Pit Lighting and Ventilation
The service pit/trench is described as ventilated and lighted (RFP §3.4; Decomp SOW-0028). The electrical drawing (App B) shows light symbols in the Service Pit area. The Electrical Engineer should consider the confined-space electrical classification of the service pit and apply appropriate wiring methods and fixture ratings.
*(Source: RFP §3.4; App B (Electrical); Decomp SOW-0028)*

### Consideration 4: Welding Station Ventilation — Electrical Interface
The welding station exhaust system (Decomp SOW-0039) is a mechanical scope item (PKG-003). However, the exhaust fan(s) will require electrical circuits (REQ-015). The Electrical Engineer and Mechanical Engineer must coordinate exhaust fan electrical load data before the electrical design is finalized.
*(Source: App B (Electrical); Decomp SOW-0039, Decomp SOW-0066)*

### Consideration 5: Coordination with Mechanical (Ceiling Fans and Forced Air)
Six ceiling fans (REQ-007) are in the main shop. The forced-air makeup air unit (Decomp SOW-0037) is also in the main shop. The Electrical Engineer should confirm that ceiling fan circuit design does not conflict with makeup air unit ductwork positioning.
*(Source: App B (Electrical); Decomp SOW-0037, Decomp SOW-0040)*

### Consideration 6: Panel Schedule Completeness
The conceptual drawing lists individual loads but does not show a panel layout or feeder arrangement. The Electrical Engineer is responsible for rationalizing all the individual loads shown on App B into a coherent panel schedule (DEL-004-06) with appropriate branch circuit protection, feeder sizing, and spare capacity.
*(Source: App B (Electrical))*

### Consideration 7: Energy Efficiency and Alberta Energy Code Requirements
The Electrical Engineer should assess whether the Alberta energy code or National Energy Code of Canada for Buildings (NECB) applies to this commercial/industrial building. If applicable, energy performance requirements may govern lighting power density (W/sq ft), lighting control requirements, and motor efficiency. The Guidance currently addresses industrial load sizing and lighting control (Trade-off 2) but does not address energy performance benchmarks or lifecycle cost considerations. Given the approximately 13,000 sq ft building area with high bay LED lighting and multiple motor loads, an energy code analysis may identify additional requirements or design optimization opportunities.
*(Source: ASSUMPTION — energy code applicability not confirmed in available sources; Electrical Engineer to determine. Lensing ref: A-005)*

### Consideration 8: Arc Flash Hazard Analysis and Short-Circuit Current Study
For an industrial three-phase electrical service with dedicated 70 A circuits (fire hose pump, pressure washer), overhead crane power, and multiple welding receptacles, an arc flash hazard analysis and short-circuit current study is standard practice and may be required by Alberta OH&S regulations. The Electrical Engineer should determine whether an arc flash study is required for this facility and, if so, include it in the scope of the Electrical Calculation Package (DEL-004-08). The study informs equipment ratings, labeling requirements, and personal protective equipment (PPE) requirements for maintenance personnel.
*(Source: ASSUMPTION — arc flash analysis is standard practice for industrial three-phase installations; not explicitly required in RFP or App B. Lensing ref: E-001)*

---

## Trade-offs

### Trade-off 1: Conduit System Selection
In a maintenance shop environment, exposed metallic conduit (EMT or rigid) is common for durability and repairability. However, in a concrete structure, some runs may be embedded. The Electrical Engineer should consider accessibility for future modifications given the industrial nature of the facility. The RFP does not specify conduit type; this is a design decision.
*(No direct source conflict; engineering judgment applies. ASSUMPTION: conduit type to be determined by Electrical Engineer.)*

### Trade-off 2: Lighting Control Strategy
The App B drawing shows lighting circuits but no switching or control strategy. For a 13,000 sq ft shop, zoned switching or occupancy-based control could reduce energy use. However, operational simplicity may be preferred for a maintenance facility. The Electrical Engineer should confirm the Owner's preference, as this affects panel schedule and code compliance under the Alberta Safety Codes.
*(Source: App B (Electrical); ASSUMPTION — no control strategy specified in sources)*

### Trade-off 3: Spare Capacity in Panels
The RFP/App B identify all known loads, but this is a design-build project where the County may have additional electrical needs not yet articulated. Building in spare panel capacity (e.g., 20% spare breaker spaces) is good practice for a facility of this type and operational profile. Cost of additional capacity at design time is low relative to future panel replacement.

**Rationale basis (TBD — Electrical Engineer to quantify):** The 20% spare breaker space recommendation is a common industry guideline for industrial/maintenance facilities where future load additions are likely (e.g., additional welding stations, compressed air tools, diagnostic equipment). The Electrical Engineer should provide a defensible basis for the spare capacity recommendation by considering: (a) projected load growth over the facility's expected service life, (b) cost differential between a panel with 20% spare capacity versus a minimal panel, and (c) cost of future panel replacement or addition if spare capacity proves insufficient. The Owner should be presented with options and cost implications to make an informed decision. *(Lensing ref: D-003)*
*(ASSUMPTION — no specific spare capacity requirement in sources; engineering judgment applies)*

---

## Examples

No worked examples from sources are available for this deliverable. Section reserved for future updates.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-004-09-01 | Wash bay high bay lighting wattage/lumens not stated. Main shop is explicitly 150 W / 22,000 lm. Wash bay may require different specification (wet location, potentially lower mounting height). | App B (Electrical) — wash bay note: "2 Rows of 3 High Bay Lights" (no wattage/lumen spec) | App B (Electrical) — main shop: "150 Watt LED 22,000 Lumens" | Specification REQ-005; Datasheet Lighting — Wash Bay | PROPOSAL: Electrical Engineer to specify consistent or equivalent fixture; confirm with Owner if lower lumen output acceptable for wash bay | TBD |
| CONF-004-09-02 | Security camera wiring scope: App B shows "Wiring for Security Cameras" but camera system specification (quantity, locations, cable type) is not provided in sources. Low-voltage design cannot be completed without this input. | App B (Electrical) — note: "Wiring for Security Cameras" | No camera specification in RFP or other accessible sources | Specification REQ-016; Procedure Prerequisites | PROPOSAL: Owner to provide camera system specification before low-voltage design (DEL-004-07) is finalized | TBD |
| CONF-004-09-03 | 2-way radio antenna wire scope: similarly, antenna system specification (frequency band, antenna type, routing termination) not in sources. | App B (Electrical) — note: "Antenna Wire for 2 Way Radios" | No radio system specification in RFP or other accessible sources | Specification REQ-017; Procedure Prerequisites | PROPOSAL: Owner to provide radio antenna specification before low-voltage design (DEL-004-07) is finalized | TBD |
| CONF-004-09-04 | Ceiling fan voltage assumption: Specification REQ-007 previously contained an unsourced ASSUMPTION ("120 V or 240 V single-phase") that was not present in Datasheet (which correctly recorded TBD). The ASSUMPTION has been removed from Specification for consistency; voltage is now TBD in both documents pending Electrical Engineer determination. *(Lensing ref: E-002)* | Specification REQ-007 Note (original: "ASSUMPTION: 120 V or 240 V single-phase per fan") | Datasheet Ceiling Fans table ("TBD — Not stated in sources") | Specification REQ-007; Datasheet Ceiling Fans | PROPOSAL: Resolved — ASSUMPTION removed from Specification; Electrical Engineer to confirm voltage during design | RESOLVED (Pass 3) |
