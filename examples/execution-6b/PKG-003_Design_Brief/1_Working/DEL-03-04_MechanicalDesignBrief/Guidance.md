# Guidance — DEL-03-04: Mechanical Design Brief

---

## Purpose

The Mechanical Design Brief explains the Mechanical Engineer's rationale for all mechanical system selections for the Penhold Public Services Building. It is one of five discipline sub-briefs required by RFP §7.1.2, with the collective Design Brief evaluated at 5 points.

This brief serves three audiences simultaneously:

1. **Evaluation Committee** — must be convinced that the mechanical strategy is competent, RFP-compliant, and operations-fit for a Fire Hall + Public Works facility
2. **Owner (Town of Penhold)** — must trust that systems will be reliable, maintainable, and durable over a 50-year main building / 20-year Cold Storage lifespan
3. **Design-Build Team** — the brief documents mechanical design decisions that guide detailed design post-award

**Scope boundary (canonical phrasing used across all four documents):** This brief covers mechanical design rationale exclusively. Energy efficiency quantification and solar readiness are excluded (covered in DEL-04-02). Detailed lifecycle cost analysis and maintenance scheduling are excluded (covered in DEL-05-03). This brief introduces design life rationale for each system selection without duplicating those deliverables.

---

## Principles

**P-001 — Operations-Fit Design**

Mechanical systems must reflect the actual operational profile of a combined Fire Hall and Public Works facility:

- Apparatus bays: Frequent bay door cycling; cold air ingress; vehicle exhaust during apparatus operations; periodic washing
- Public Works bays: Maintenance environment; occasional vehicle idling; rare welding (not a dedicated welding space)
- Residential quarters: 24/7 occupancy by on-duty fire personnel; reliability and quiet operation paramount
- Bunker gear storage: High-value protective equipment sensitive to moisture and odor damage; 40 lockers per Addendum 03
- Shared spaces (ICP/kitchen): Must remain operational during power outages per generator scope

Principle: Select right-sized systems for actual use patterns. Oversizing wastes capital; undersizing compromises function and safety.

**P-002 — Simplicity and Reliability Over Novelty**

A straightforward, well-understood mechanical system maintained by local Alberta contractors over 50 years is preferable to a cutting-edge system that may lack service support by 2050+. Prioritize:

- Standardized equipment with proven track records in institutional and municipal buildings
- Redundancy for critical functions (generator for minimum loads; independent HVAC zones to isolate failures)
- Accessible mechanical rooms and clear service routes
- Equipment with Canadian parts availability and known local service contractors

Source: ASSUMPTION derived from standard municipal project procurement practice and 50-year design life requirement (RFP §7.1.4; Decomposition OBJ-005).

**P-003 — Explicit Interdisciplinary Coordination**

Mechanical systems are embedded in the whole facility structure. The brief must show awareness of interdependencies:

- Structural: Floor slab design for bay sumps; mechanical equipment support loads; penetrations through structure
- Civil: Sump drainage discharge routing to storm or sanitary system; utility service connections (gas, water)
- Electrical: Power distribution for HVAC, pumps, and controls; generator integration with automatic transfer switch
- Architectural: Mechanical room location and size; outdoor equipment placement (generator, condensers if any); ductwork routing within building envelope

Source: RFP §7.1.2(4) (design brief scope); DEL cross-references (DEL-03-02, DEL-03-03, DEL-03-05).

**P-004 — Life-Cycle Ownership**

The Town of Penhold will operate this facility for 50+ years with limited in-house mechanical expertise. System selections must balance:

- Capital cost (scope of build)
- Operating cost (fuel, electricity, filter and consumables, maintenance labor)
- Reliability (minimal downtime during fire or public works operations)
- Replacement cycles (boilers typically 20–25 years; unit heaters 15–20 years; sprinkler piping 30+ years)

Principle: Brief should justify selections on total life-cycle grounds and give the Owner confidence that systems will not require premature replacement or impose unmanageable maintenance burdens.

Source: RFP §7.1.4; Decomposition OBJ-005; ASSUMPTION (standard lifecycle guidance for institutional HVAC and plumbing; specific equipment lifecycle values location TBD in manufacturer data).

**P-005 — Write for Evaluator Scoring**

This deliverable contributes to OBJ-004 (Design Brief, 5 pts). The Evaluation Committee (Project Committee + Willis + Third Party evaluator per RFP §5.1) will score the brief based on demonstrated competence, RFP responsiveness, and Addendum 03 compliance. The brief should be written so that evaluators scanning for keyword compliance can quickly confirm that all required topics and addendum items are visibly addressed. Specifically:

- Use Addendum 03 language explicitly (e.g., "direct exhaust," "2 apparatus per bay," "40 bunker gear lockers," "2-inch minimum fill station") so that evaluators can locate compliance without interpretation
- Front-load key compliance statements in each section rather than burying them in technical detail
- Demonstrate responsiveness to the Owner's operational needs (fire hall + public works dual-use) in a way that signals understanding of the project context
- Avoid unnecessary jargon that might obscure compliance to non-technical evaluators on the committee

Source: RFP §5.1 (evaluation process); Decomposition §6 (OBJ-004 scoring); ASSUMPTION (evaluator scanning behavior is standard for scored proposals).

**P-006 — Addendum 03 Compliance is Non-Negotiable**

All seven Addendum 03 mechanical clarifications (M-001 through M-007 in Specification) must be explicitly visible in the brief narrative. Evaluators familiar with the addenda will check for this; omissions signal a non-compliant proposal. The brief must name each requirement (direct exhaust, fill stations, bay sumps, generator minimum loads, secondary door opening) explicitly and show how the proposed design addresses each.

Source: Addendum 03 §1 (Decomposition §4); Decomposition §2 Rule (addendum governs over RFP where conflicting).

---

## Terminology Note

**Bay door secondary opening mechanism** is the preferred term for the Addendum 03 M-007 requirement across all four documents. Alternative descriptions used in context include: manual hand-crank operator, hydraulic backup accumulator, and gravity-release mechanism (C-005 options list). These are subtypes of the standard term "bay door secondary opening mechanism" and should be referenced as such when discussing the requirement generically. Specific mechanism names should be used only when discussing selection options or trade-offs.

Source: Addendum 03 §1 (Decomposition §4) uses "secondary opening mechanism"; normalized here per B-004 (semantic lensing).

---

## Considerations

### C-001: Heating and Cooling Strategy

**Apparatus bays:**
- Heating load is significant because bay doors open frequently, admitting cold Alberta air (design temp approximately −33°C, ASSUMPTION: ASHRAE 99% for Red Deer region as proxy)
- System choices: Central hydronic (gas-fired boiler → unit heaters) vs. distributed gas-fired unit heaters vs. infrared radiant heaters
  - Hydronic: Efficient; good zone control; boiler maintenance required; superior lifecycle value for 50-year design life
  - Gas unit heaters: Simple; decentralized; fast response; higher operating cost; easier individual replacement
  - Infrared radiant: Efficient for intermittently occupied bays; less effective for continuous occupancy
- Cooling: Alberta climate makes full air conditioning of apparatus bays impractical and generally unnecessary; exhaust ventilation provides adequate heat removal during summer operations
- Zone control: Apparatus bays should be independently zoned from office, residential, and shared spaces to allow temperature control by area

**Office areas and residential quarters:**
- Standard occupant comfort (20–22°C); residential quarters require reliable heating for on-duty personnel
- May share a heating loop with apparatus bays or have a dedicated zone
- Cooling: Typically required in office/residential for summer comfort; split system or rooftop unit may be appropriate

**Public Works bays:**
- Lower comfort expectation than apparatus bays; intermittent occupancy for vehicle maintenance
- Heating may be by modest hydronic extension or dedicated space heaters (TBD in detailed design)

**Cold Storage building:**
- Unheated per Addendum 03; no mechanical heating or cooling scope
- Minimal ventilation may be warranted if motor-driven equipment is stored (ASSUMPTION: confirm with Owner); otherwise no active mechanical systems

**Trade-Off:** See T-001 (hydronic vs. gas unit heaters for apparatus bay heating).

### C-002: Ventilation Strategy by Zone

**Fire apparatus bays (Addendum 03 M-001 — direct exhaust):**
- Requirement: Non-recirculated exhaust; 2 apparatus per bay
- CO prevention rationale: Idling diesel/gasoline engines produce CO; direct exhaust removes contaminated air before it reaches occupant breathing zones
- Exhaust rate: TBD in detailed design. **Primary governing standard: ASHRAE 62.1 §6.2** (Ventilation Rate Procedure — vehicle service/repair occupancy category); supplemented by Alberta Building Code provisions. If ASHRAE 62.1 §6.2 does not apply to fire apparatus bay occupancy classification, the Mechanical Engineer shall identify the alternative governing standard — **resolution trigger: confirm applicable code clauses and occupancy classification at detailed design kickoff**
- Makeup air: Equal volume of outside air required to maintain neutral pressure; heated makeup air in winter to prevent discomfort and condensation on equipment
- Duct routing: Route exhaust to rooftop or exterior wall termination; termination must prevent re-entry into building air intakes
- Controls: Continuous during occupied periods; reduced rate unoccupied (occupancy sensor or CO sensor recommended)
- Note: Energy recovery is NOT applicable — Addendum 03 mandates direct (non-recirculated) exhaust; heat cannot be recovered from contaminated air

**Public Works bays (Addendum 03 M-002 — general ventilation):**
- General exhaust ventilation for odor, humidity, and occasional welding fumes (portable local exhaust provided by PW staff for welding; not building-installed)
- Exhaust rate: Lower than apparatus bays; rate TBD per code for industrial/workshop occupancy
- Not connected to apparatus bay exhaust; independent zone

**Bunker gear storage room (Addendum 03 M-003 — 40 lockers):**
- Dedicated room-level ventilation: Supply + exhaust or exhaust-only with fresh air inlets
- Purpose: Moisture removal (wet gear), odor control, drying to prevent mold growth on expensive protective equipment
- Rate: TBD; consult NFPA 1581 (Standard on Fire Department Infection Control Program) or equivalent fire service gear storage best practices (edition and specific clause location TBD). **Note:** NFPA 1581 is also listed in Specification Standards table and Datasheet References table for standards register consistency.

**Residential quarters:**
- Standard residential ventilation (ASHRAE 62.2 or equivalent; location TBD)
- Quiet operation required (sleeping quarters for on-duty personnel)
- Energy recovery ventilator (ERV) recommended for efficiency given Alberta climate (ASSUMPTION: standard best practice for residential in cold climates; location TBD)

**Office areas:**
- Standard office ventilation per ASHRAE 62.1; demand-controlled ventilation considered for cost savings
- May be part of central HVAC or dedicated rooftop unit

**Kitchen (ICP/meeting room — Addendum 03 generator scope):**
- Kitchen exhaust hood required (cooking exhaust); makeup air to balance hood
- Kitchen and ICP/meeting room are generator-backed loads (M-006); ventilation controls should be generator-compatible

**Bathrooms:**
- Standard exhaust per code (continuous or triggered by occupancy); two bathrooms are generator-backed loads (M-006)

**Mechanical room:**
- Fresh combustion air for gas-fired boiler (if applicable); mechanical ventilation may double as boiler combustion air per code provisions
- **Equipment heat rejection:** TBD — determine whether additional cooling ventilation is needed for equipment heat rejection (pumps, boiler jacket losses, electrical panels) beyond combustion air provision. If mechanical room is interior with limited natural ventilation, dedicated exhaust or supply cooling may be required to maintain acceptable ambient temperature for equipment longevity. Resolution: confirm during detailed design based on equipment selection and mechanical room layout.

### C-003: Plumbing Systems

**Domestic water supply:**
- Source: Municipal water from Waskasoo Avenue North (ASSUMPTION: based on site location described in Decomposition §1; service connection point location TBD in civil design)
- Pressure and flow: TBD based on utility confirmation; pressure reduction valve may be needed
- Water treatment: Not anticipated; TBD based on municipal water quality (ASSUMPTION)

**Hot water:**
- Required for kitchen, bathrooms, and apparatus bay hand-washing
- System options: Central gas-fired or electric storage tank vs. on-demand tankless
  - Central storage (gas-fired if gas utility available): Lower operating cost; suitable for high-occupancy periods; standard for institutional facilities; 15–20 year replacement cycle (ASSUMPTION: location TBD)
  - Tankless: Space savings; no standby losses; less common in high-demand institutional applications
- Thermostatic mixing valves required at accessible fixtures to prevent scalding

**Fill stations (Addendum 03 M-004):**
- Two stations: One in fire apparatus bay, one in Public Works bay
- Diameter: 2" minimum per Addendum 03
- Components: Isolation valve, backflow preventer, drain provision; connection standard (NPT, BSP, or Storz) to be confirmed with Owner based on actual fleet equipment (ASSUMPTION: connection type TBD)
- Protection from freezing: Stations should be located inside heated space or provided with freeze protection where exposed to exterior cold air during door operations

**Bay floor sumps (Addendum 03 M-005):**
- Purpose: Capture snow meltwater from apparatus and equipment; collect minor wash water
- Pump: Sump pumps with float switches; discharge routed to storm system (ASSUMPTION: civil drainage system accepts sump discharge; oil/water separator may be required per Alberta Environment regulations — location TBD). **TBD: Confirm whether Alberta Environment and Protected Areas requires oil/water separator for bay sump discharge; consult Authority Having Jurisdiction (AHJ) during detailed design. Resolution trigger: obtain AHJ determination before finalizing plumbing design. This regulatory requirement could significantly affect plumbing design scope and cost.**
- Structural coordination: Sump pit construction is part of slab-on-grade design (DEL-02-03); mechanical provides sump pump and piping only
- Capacity: TBD based on bay area and worst-case melt scenario

**Sanitary drainage:**
- Fixtures: Bathrooms, kitchen, laundry (if any), hand-wash sinks in apparatus bay and shop areas
- Grease trap: Required at kitchen if food service operations are significant (TBD per municipal authority having jurisdiction requirements; location TBD)

**Storm drainage:**
- Roof drains and exterior surfaces to storm system; coordinated with civil drainage design (DEL-03-02)
- Sump discharge: Separate from storm drains if oil/water separation required (ASSUMPTION; confirm with civil and environmental consultant)

### C-004: Fire Protection

**Sprinkler system:**
- Coverage: All occupied areas of main building — apparatus bays, PW bays, office, residential, shared spaces, storage
- System type:
  - Wet sprinkler (preferred for heated spaces): Simplest, lowest cost, most reliable; standard for Alberta institutional buildings
  - Dry sprinkler (applicable to unheated or potentially unheated spaces): Cold Storage building, if building is determined to be at freezing risk year-round; dry system adds cost and complexity
- Apparatus bays: High bay volumes (overhead doors at 16 ft per Addendum 03; ceiling height above); confirm sprinkler head coverage per NFPA 13 for high-bay occupancy (ASSUMPTION: in-rack and ceiling heads may be required — location TBD)
- Bunker gear room: Standard wet head coverage; small room

**Fire alarm:**
- Integrated smoke/heat detection system with manual pull stations per NFPA 72 (or Alberta equivalent)
- Control panel with UPS backup; fire alarm must remain functional during power outages
- Coordination: Generator does NOT need to power fire alarm directly (UPS backup is standard per code); brief should note UPS provision

**Fire pump:**
- TBD in detailed design; if municipal water supply pressure is insufficient for sprinkler demand, a fire pump (jockey + main) may be required; generator backup for fire pump if installed (ASSUMPTION: confirm with civil/fire review)

### C-005: Generator and Emergency Power Philosophy

**Minimum loads per Addendum 03 M-006:**
- Kitchen (food preparation continuity during outage)
- Incident Command Post / meeting room (ICP — Owner emergency operations center)
- Two bathrooms (occupant life safety)
- Bay door secondary opening mechanism (apparatus egress)

**Sizing:**
- Estimated generator load: TBD in detailed design (sum of kitchen appliance loads, ICP lighting and AV, bathroom exhaust and lighting, bay door operator motor)
- ASSUMPTION: Minimum generator likely in 20–50 kW range for these four loads; actual sizing TBD by mechanical/electrical engineer in detailed design

**Generator type:**
- Diesel (preferred): High power density; proven reliability in Alberta climate; simpler fuel storage; established service network
- Natural gas: Cleaner; avoids on-site fuel storage if gas utility available at site; lower power density for same footprint
- ASSUMPTION: Fuel selection TBD pending confirmation of natural gas utility availability at site (location TBD in civil/utility coordination)

**Operating mode:**
- Standby mode: Generator starts automatically on utility failure; automatic transfer switch (ATS) manages load transition; generator shuts down when utility restores
- Minimum 72-hour runtime per Functional Program (ASSUMPTION: noted as open item SOW-0222 per MEMORY; confirm in DEL-02-07 context — runtime duration should be verified against Addendum 03 and Functional Program for this deliverable). **Rationale for 72-hour assumption:** Standard emergency services practice for fire stations typically requires 48- to 72-hour generator runtime to cover extended utility outages during major events (ice storms, infrastructure failures). The 72-hour figure aligns with common municipal fire facility operational continuity requirements. However, the directive authority for this specific value is partially obscured (source: Functional Program row 30.0, per prior analysis in DEL-02-07 MEMORY entry); see CONF-01 in Conflict Table for resolution path.

**Fuel storage:**
- On-site tank: Sized for minimum 72-hour runtime at design load (TBD)
- Tank location: Outdoors (preferred for safety and ventilation); coordinated with architectural layout
- Secondary containment per Alberta Environmental Protection and Enhancement Act (ASSUMPTION; location TBD)

**Bay door secondary opening (Addendum 03 M-007):**
- Purpose: Apparatus egress when both utility and generator power are unavailable
- Options: Manual hand-crank operator; hydraulic backup accumulator; gravity-release mechanism
- Preferred approach: Manual hand-crank (simplest, no power dependency, code-compliant in most jurisdictions; ASSUMPTION: specific mechanism confirmed in detailed design with door supplier)
- Coordination: Mechanical/generator scope (power backup) + Architectural scope (door specification); joint coordination required

---

## Trade-Offs

**T-001 — Apparatus Bay Heating: Hydronic vs. Gas Unit Heaters**

| Factor | Central Hydronic (Gas Boiler + Unit Heaters) | Distributed Gas Unit Heaters |
|---|---|---|
| Capital cost | Higher (boiler, piping, controls) | Lower (simpler installation) |
| Operating efficiency | Better (central modulation, zoning) | Lower (per-unit cycling losses) |
| Maintenance | Central boiler maintenance (annual); unit heater fan service | Per-unit maintenance; no boiler |
| Zone control | Excellent (thermostatic per zone) | Moderate (per-heater thermostat) |
| 50-year fit | Good (piping long-lived; boilers replaceable mid-life at lower cost than full redesign) | Moderate (more frequent replacement of distributed units) |
| Recommended | Preferred for main building given 50-year lifespan | Appropriate for Cold Storage if any heating required (not applicable — unheated per Addendum 03) |

Source: ASSUMPTION (standard professional judgment for institutional HVAC; specific lifecycle cost modeling location TBD in DEL-04-02 and DEL-05-03).

**T-002 — Generator Fuel: Diesel vs. Natural Gas**

| Factor | Diesel | Natural Gas |
|---|---|---|
| Power density | Higher | Lower |
| Fuel storage | On-site tank required; secondary containment needed | No on-site tank if utility available |
| Reliability | Excellent (established diesel generator technology) | Dependent on natural gas utility continuity |
| Operating cost | Higher fuel cost per kWh | Lower fuel cost if gas utility available |
| Environmental | Higher NOx and particulate | Cleaner combustion |
| Recommendation | Preferred pending utility confirmation | Preferred if gas utility confirmed at site |

Source: ASSUMPTION (standard engineering judgment; utility confirmation from civil/site coordination — location TBD).

**T-003 — Ventilation Energy: Direct Exhaust vs. Heat Recovery**

This trade-off is resolved by Addendum 03: direct (non-recirculated) exhaust is mandated for fire apparatus bays. Heat recovery from contaminated apparatus bay exhaust air is not permissible. Energy mitigation must be addressed in other areas (e.g., heated makeup air efficiency, insulated building envelope, efficient lighting — see DEL-04-02 for energy narrative).

Source: Addendum 03 §1 (Decomposition §4); resolved — direct exhaust governs.

**T-004 — Sprinkler System Type: Wet vs. Dry**

| Factor | Wet Sprinkler | Dry Sprinkler |
|---|---|---|
| Applicability | All heated spaces | Spaces at risk of freezing (unheated or intermittently heated) |
| Cost | Lower (simpler system) | Higher (air compressor, more complex piping) |
| Response time | Faster (water immediately present) | Slower (air must exhaust before water flows) |
| Maintenance | Simpler | More complex |
| Recommendation | Main building (fully heated) → wet system | Cold Storage (unheated) → dry system if sprinkler coverage required (TBD) |

Source: ASSUMPTION (NFPA 13 standard guidance; specific Cold Storage sprinkler requirement TBD based on occupancy classification and provincial authority having jurisdiction confirmation).

---

## Examples

**EX-001 — Sample Brief Language: Apparatus Bay Heating and Ventilation**

*Illustrative excerpt (not final brief text):*

> "The fire apparatus bays are heated by a central hydronic system consisting of a natural gas-fired condensing boiler plant serving unit heaters mounted at high level in each bay. This approach delivers rapid warmth during cold Alberta winters while maintaining bay temperature above the minimum setpoint during unoccupied periods. Independent thermostatic zone control for each bay allows the Owner to optimize fuel consumption based on operational demand. The boiler plant serves both apparatus bay unit heaters and the residential quarters heating loop, providing economies of scale for plant maintenance. The system is designed for a replacement cycle of 20–25 years (boiler); unit heaters may be individually replaced without system redesign, supporting the 50-year building design life.
>
> Apparatus bay ventilation complies with Addendum 03's requirement for direct, non-recirculated exhaust, designed for 2 apparatus per bay. The exhaust system operates continuously during bay occupancy and at reduced rate during unoccupied periods, controlled by CO sensor and occupancy detection. Heated outside air is delivered as makeup air at low level to maintain neutral pressure, prevent cold drafts on personnel, and eliminate condensation on apparatus. Exhaust is discharged to rooftop via insulated ductwork and terminated above the roof parapet to prevent re-entry."

**EX-002 — Sample Brief Language: Generator and Emergency Power**

*Illustrative excerpt (not final brief text):*

> "A diesel standby generator, located outdoors in an acoustically rated enclosure, provides backup power for the critical loads identified in Addendum 03: the kitchen, the Incident Command Post / meeting room, two bathrooms, and the apparatus bay door secondary opening mechanism. The generator is sized to serve these loads simultaneously, with an on-site fuel tank providing a minimum [TBD]-hour runtime at design load. An automatic transfer switch (ATS) initiates generator startup within [TBD] seconds of utility failure and automatically returns loads to utility supply after power restoration. The generator and ATS are maintained under an annual service contract with load testing to confirm standby readiness. Apparatus bay doors are equipped with a manual hand-crank secondary opening operator that functions without any electrical power source, providing apparatus egress during complete power failure."

**EX-003 — What a Strong vs. Weak Brief Looks Like**

*Strong mechanical brief (achieves Design Brief evaluation score):*
- Names each zone explicitly and describes the mechanical approach for that zone
- States "direct exhaust" and "2 apparatus per bay" verbatim in the ventilation section
- Lists generator minimum loads verbatim from Addendum 03
- Provides explicit rationale for each system choice ("We selected hydronic heating because..." "We selected diesel over natural gas because...")
- Acknowledges interdependencies ("Sump discharge routing is coordinated with the Civil Design Brief; oil/water separation requirements will be confirmed with the AHJ during detailed design")
- Links system selections to 50-year design life explicitly

*Weak mechanical brief (risks low score or evaluator concern):*
- Generic HVAC description without zone-specific breakdown
- Does not mention direct exhaust, fill stations, sumps, or generator minimum loads
- Presents a list of systems without any rationale for why they were chosen
- Uses hedge language ("We would likely use..." "Probably gas heating...")
- Makes no reference to 50-year design life or maintenance strategy

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| **CONF-01** | Generator runtime duration: Functional Program implies 72-hour minimum; Addendum 03 does not specify runtime | Functional Program row 30.0 (ASSUMPTION: 72-hour runtime; source partially obscured per prior analysis in DEL-02-07 MEMORY entry) | Addendum 03 §1 (minimum load scope stated; duration not stated) | Generator philosophy section; fuel tank sizing | Addendum 03 governs scope (minimum loads); runtime is a design parameter. **PROPOSAL: Use 72-hour target as ASSUMPTION pending Owner confirmation.** State as "minimum 72-hour runtime at design load" and note as assumption to be confirmed post-award. | TBD |
| **CONF-02** | Bay door secondary opening mechanism: Addendum 03 says "secondary opening mechanism" but does not specify manual vs. mechanical backup | Addendum 03 §1.6 (secondary mechanism required; type not specified) | Design-Builder discretion | Generator section; architectural coordination | **PROPOSAL: State "either generator-powered secondary operator or manual hand-crank operator is acceptable per Addendum 03 §1; detailed mechanism selection to be coordinated with door supplier in detailed design."** | TBD |
| **CONF-03** | Cold Storage building ventilation: mechanical brief covers "all buildings" per RFP §7.1.2(4), but Cold Storage is unheated | RFP §7.1.2(4) (design brief for all mechanical systems) | Addendum 03 (Cold Storage is unheated equipment storage) | Scope coverage; mechanical brief opening statement | **PROPOSAL: Brief explicitly states Cold Storage is unheated per Addendum 03; mechanical scope for Cold Storage is limited to any equipment cooling ventilation if needed (ASSUMPTION: likely no active mechanical scope for Cold Storage).** | TBD |
