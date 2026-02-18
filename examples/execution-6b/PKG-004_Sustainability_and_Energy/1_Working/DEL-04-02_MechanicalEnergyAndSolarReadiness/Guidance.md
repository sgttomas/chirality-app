# Guidance — DEL-04-02: Mechanical Energy and Solar Readiness

---

## Purpose

DEL-04-02 exists to **articulate the mechanical engineer's energy efficiency philosophy and solar-readiness strategy** for the Penhold PSB in a way that:

1. Demonstrates that the design team understands the energy profile and operational demands of a combined Fire Hall + Public Works facility — including its unique high-exhaust, 24/7, mixed-occupancy character.
2. Directly addresses the Addendum 03 mandate for a "solar-capable roof" with a credible structural and mechanical rough-in strategy.
3. Provides the rationale behind mechanical system and equipment choices — explaining *why*, not just *what*.
4. Supports OBJ-004 (Design Brief, 5 pts) by fulfilling the mechanical discipline sub-brief required by RFP Section 7.1.2.
5. Enables cross-discipline coordination with the envelope strategy (DEL-04-01), electrical energy provisions (DEL-04-03), and the mechanical concept narrative (DEL-02-04).

Source: Decomposition §6 OBJ-004; Decomposition §9 DEL-04-02 description; Addendum 03 §1.

### Evaluator Scoring Calibration (OBJ-004)

OBJ-004 (Design Brief, 5 pts) is scored by a multi-disciplinary evaluation committee that may include non-technical members. The mechanical energy narrative is one sub-brief contributing to the overall Design Brief score. While the exact weighting within OBJ-004 is not disclosed, the following factors are likely to differentiate a high-scoring mechanical energy narrative from a low-scoring one (ASSUMPTION: based on typical design-build RFP evaluation criteria for municipal facilities):

- **Credibility of approach:** Does the narrative demonstrate that the proposed mechanical energy strategy is technically achievable for this climate, building type, and operational profile? Generic efficiency claims without facility-specific rationale are unlikely to score well.
- **Addendum 03 compliance:** Are all Addendum 03 energy-relevant requirements (solar-capable roof, apparatus bay direct exhaust, ventilation requirements) explicitly addressed and cited? Evaluators who issued the addendum will look for this.
- **Innovation balanced with practicality:** Does the narrative show awareness of advanced options (heat recovery, DCV, solar-ready provisions) while acknowledging practical constraints (contamination in apparatus bays, municipal operations staff capacity, Alberta cold-climate limitations)? Over-promising erodes credibility.
- **Life-cycle awareness:** Does the narrative consider operational cost, maintenance burden, and Owner flexibility alongside first cost? Evaluators value whole-cost thinking even if a formal lifecycle cost analysis is not required.
- **Cross-discipline coherence:** Does the narrative align with other Design Brief sub-briefs (envelope, electrical, structural)? Contradictions between sub-briefs undermine confidence in the team's coordination.

Source: ASSUMPTION based on OBJ-004 scoring context (Decomposition §6); Semantic lensing item D-002.

---

## Principles

### P-001: Zone-Specific Energy Thinking

The facility is not a monolithic building — it has zones with fundamentally different energy profiles, and each requires a tailored approach:

- **Fire apparatus bays:** Variable occupancy; frequent overhead door openings; direct exhaust ventilation required (2 apparatus per bay, per Addendum 03 §1). High air change rates and door infiltration drive heating demand. Energy strategy focuses on minimizing unnecessary conditioning during standby periods and offset via heat recovery where contamination constraints permit.
- **Public Works bays:** Occasional short-term vehicle idling + very occasional welding; general ventilation required (not direct exhaust, per Addendum 03 §1). Energy strategy focuses on demand-controlled ventilation (DCV) using CO/occupancy sensors to minimize exhaust when bays are unoccupied.
- **Offices / administrative:** Standard business-hours occupancy; conventional HVAC with scheduling setbacks.
- **Residential quarters (if included):** 24/7 occupancy; continuous conditioning required; ERV or HRV is a high-value investment in this zone.
- **Shared spaces (kitchen, ICP/meeting room, training spaces):** Variable occupancy; kitchen requires dedicated makeup air; DCV applicable in training and meeting spaces.
- **Bunker gear room:** Continuous ventilation for drying and odour control per Addendum 03 §1; 40 lockers with ventilated storage.

**Design principle:** A single-system approach wastes energy in intermittent-use zones and fails continuous-use zones. Zone-specific strategies optimize efficiency without sacrificing operational reliability.

Source: Addendum 03 §1; Decomposition §4 Addendum 03 summary.

### P-002: Heat Recovery Is a Primary Efficiency Lever

The facility generates significant conditioned exhaust from apparatus bays, kitchens, and occupied zones. Recovery of this heat directly reduces the primary heating load — a major cost driver in Alberta's cold climate.

Key recovery opportunities:
- HRV/ERV on residential quarters and offices: 75–85% sensible heat recovery is standard for residential-type spaces.
- Apparatus bay exhaust: direct exhaust per Addendum 03 limits full HRV integration (contamination from vehicle emissions), but partial heat recovery via heat pipe or a dedicated isolated HRV unit may be feasible depending on final air quality assessment.
- DHW: solar thermal preheat (rough-in provided) or heat pump water heater reduces gas/electric consumption for hot water.

**Design principle:** Maximize practical heat recovery without over-engineering. Payback must be realistic. Apparatus bay exhaust recovery is complex — if contamination prevents HRV use, document the constraint clearly and accept the energy loss as a design reality.

Source: Decomposition DEL-04-02 description (heat recovery opportunities); ASSUMPTION: HRV applicability to apparatus bay exhaust depends on air quality analysis at detailed design.

### P-003: Equipment Efficiency Targets Are Realistic and Widely Available

High-efficiency mechanical equipment is commercially standard in 2024–2025. Equipment selection should prioritize:
- Widespread availability from Alberta suppliers and contractors (avoid proprietary or exotic equipment requiring specialized service).
- NECB compliance or better as the efficiency floor, with cost-effective improvements above baseline where payback is justifiable.
- Consistency with Owner's operational capacity — a small municipal operations team can service standard equipment types (condensing boilers, packaged heat pumps, standard HRVs); they cannot service complex custom systems.

Indicative efficiency targets (ASSUMPTION: to be confirmed at detailed design per NECB edition in effect):
- Heating: AFUE 95%+ condensing boilers or gas furnaces, or COP 3.0–4.5 air-source heat pumps
- Cooling: SEER 16–18+ air conditioning
- DHW: EF 0.92 minimum per NECB; targeting 0.95+ or heat pump water heater (COP 2.5–3.5)

Source: ASSUMPTION based on current NECB efficiency requirements; specific targets confirmed at detailed design.

### P-004: Solar-Ready Means Rough-In, Not Full System

Addendum 03 §1 mandates "solar-capable roofing" — it does not require full solar PV or solar thermal installation in the base design. "Solar-ready" means:
- Structural loading allowance in the roof design for future panels (coordinated with DEL-02-03).
- Mechanical rough-in: pipe sleeves or conduit pathways from the roof to the mechanical room for future solar thermal loop piping; isolation valve provisions in the mechanical room.
- Space reservation on the roof plan for future solar panel area (coordinated with DEL-02-01 architectural concept).
- Orientation rationale: explain how the roof orientation (flat/south/west/southwest per Addendum 03) supports future solar efficiency.
- Coordination with electrical solar rough-in (DEL-04-03): conduit for PV wiring routed concurrently.

**Design principle:** Solar-ready provisions are a minor cost in the base design and give the Owner full flexibility to install solar PV or thermal within 5–15 years without major rework.

Source: Addendum 03 §1; Decomposition §4 Addendum 03 summary; Decomposition DEL-04-02 description.

### P-005: Energy Metering Serves Operations, Not Just Compliance

Energy metering and monitoring provisions serve multiple operational purposes beyond code compliance:
- Owner utilities tracking: validates actual energy consumption against design estimates; identifies variance early.
- Fault detection: unexpected energy spikes signal system problems (refrigerant leak, stuck damper, sensor failure).
- Operational learning: shows which zones and systems consume energy and when; supports future energy management decisions.

Metering scope should be appropriate but not excessive. Sub-metering at the major consumer level (apparatus bay HVAC, DHW, office/residential HVAC) is more useful than whole-building-only metering, while avoiding over-metering of minor loads.

Source: Decomposition DEL-04-02 description (energy metering and monitoring provisions).

### P-006: Maintainability Is Part of Energy Performance

A high-efficiency system that is difficult to maintain degrades over time. Energy-related design decisions must account for maintenance practicality:
- HRV filters: accessible location and standard replacement intervals (quarterly inspection typical in dusty operations environments).
- DHW system: adequate service aisle, accessible expansion tank and pressure relief connections.
- Demand-controlled ventilation sensors (CO, CO2, occupancy): accessible for calibration and replacement.
- Controls interface: simple and clearly labeled; local override options for operations staff.

This principle is coordinated with DEL-05-03 (Mechanical Maintainability), which addresses maintainability in detail. This narrative need only flag key maintainability design decisions that have energy efficiency implications.

Source: Decomposition DEL-05-03 description; ASSUMPTION: maintainability-energy interaction is an expected cross-document coordination point.

---

## Considerations

### C-001: Apparatus Bay Energy is the Dominant Challenge

The apparatus bay environment is the most energy-intensive and operationally constrained zone in the facility. Key considerations:

- Addendum 03 requires direct exhaust (not general exhaust) ventilation for fire apparatus bays; this means conditioned air is continuously or frequently purged from the bay.
- Overhead doors must be 16 ft minimum (Addendum 03 §1); each door opening is a major infiltration event in cold weather.
- Vehicle warm-up and idling produce combustion by-products that limit heat recovery options.
- The energy narrative must acknowledge these constraints honestly — do not overstate recovery potential in apparatus bays.

**Practical guidance:** Document the constraint, state the energy loss as accepted, and focus recovery efforts on adjacent zones (residential, offices) where HRV operates cleanly.

**NFPA ventilation vs. energy optimization interaction:** The Specification Standards table notes that NFPA 1/NFPA 13 "may impose ventilation requirements superseding energy optimization." The narrative author should be aware that fire station apparatus bay ventilation requirements under NFPA may mandate minimum air change rates or exhaust capacities that exceed what energy optimization alone would dictate. The recommended approach is:
- First, satisfy NFPA-mandated ventilation rates as the floor (life safety takes precedence over energy optimization).
- Then, apply energy optimization strategies (heat recovery, scheduling, DCV) only to the extent they do not compromise NFPA compliance.
- If NFPA ventilation requirements create a significant energy penalty relative to what NECB optimization would otherwise achieve, document this penalty explicitly in the narrative as a code-driven constraint, not a design deficiency.
- ASSUMPTION: NFPA apparatus bay ventilation requirements will be clarified at detailed design with input from the fire protection consultant; clause-level NFPA requirements are not accessible at this stage (location TBD).

Source: Specification.md Standards table (NFPA 1/NFPA 13 row); Addendum 03 §1; ASSUMPTION on NFPA interaction.

Source: Addendum 03 §1; Decomposition §4.

### C-002: Solar Orientation — Site Drives Building Orientation

Addendum 03 permits flat, south, west, or southwest orientation for the solar-ready roof. The actual building orientation on the 12-acre site is determined by the civil/architectural concept (DEL-02-01, DEL-02-02). This narrative should:
- State the preferred orientation (south is optimal for Alberta solar — ASSUMPTION based on Alberta latitude ~52°N and standard solar PV design principles).
- Confirm that the site plan supports the chosen orientation, or acknowledge a trade-off if site constraints dictate a less optimal orientation.
- Note that flat roofs with tilted racking systems can achieve near-optimal solar angles regardless of building orientation — this is a design flexibility point.

Source: Addendum 03 §1; ASSUMPTION on preferred orientation based on solar principles for Alberta latitude.

### C-003: Cross-Discipline Coordination Is Required Before Drafting

This narrative cannot be finalized independently. Three critical coordination points must be resolved with sibling deliverables:

1. **DEL-04-01 (Envelope):** What are the envelope U-value targets? These drive HVAC load sizing. If envelope targets change, HVAC sizing and efficiency claims may need revision.
2. **DEL-04-03 (Electrical):** What electrical provisions are being made for future solar PV? Conduit routing and roof penetrations should be coordinated between mechanical and electrical to avoid rework and conflict.
3. **DEL-02-04 (Mechanical Concept):** What HVAC systems and equipment were selected at the concept level? This energy narrative must justify those choices from an energy perspective — or flag where the energy analysis suggests a different approach.

**Risk:** If coordination is skipped, the three PKG-004 narratives may contradict each other on solar provisions, efficiency targets, or equipment types — undermining evaluator confidence.

Source: Decomposition _REFERENCES.md; Decomposition DEL-04-02 cross-references.

### C-004: Bunker Gear Room Ventilation Has an Energy Component

Addendum 03 §1 requires 40 bunker gear lockers with ventilated storage and room-level ventilation. This is primarily a health and durability requirement (moisture control, odour management, turnout gear maintenance), but it also has energy implications:
- Continuous exhaust from the bunker gear room is a heat loss.
- If the exhaust airstream is clean (no combustion contamination), heat recovery via a small dedicated HRV is feasible.
- If the bunker gear room exhausts to a common plenum with apparatus bay exhaust, contamination concerns may preclude HRV.

The narrative should note this as a design decision point with the energy implication stated.

**Preliminary recommendation (ASSUMPTION: to be confirmed at detailed design with fire protection consultant):** The bunker gear room exhaust should be **ducted separately** from the apparatus bay exhaust. Rationale:

- **Separate ducting preserves HRV eligibility.** If the bunker gear room exhaust is combined with apparatus bay exhaust (which carries vehicle combustion by-products), the contamination disqualifies the combined stream from standard HRV recovery. A separate duct keeps the bunker gear exhaust stream clean enough for a small dedicated HRV unit.
- **Energy implication of separate ducting with HRV:** A small dedicated HRV (60-75% sensible recovery) on the bunker gear exhaust stream recovers heat from what would otherwise be a continuous heat loss. Given 24/7 operation, the annual energy savings are meaningful relative to the modest HRV cost.
- **Energy implication of combined ducting (no HRV):** If combined with apparatus bay exhaust, the bunker gear room exhaust heat is lost entirely. The apparatus bay exhaust heat pipe recovery (if installed) may partially offset this, but the bunker gear airstream volume is small relative to apparatus bay exhaust and would contribute minimally to the heat pipe recovery.
- **ASSUMPTION:** The bunker gear room exhaust airstream, while carrying moisture and odour, does not carry combustion by-products and is therefore suitable for standard HRV recovery. This assumption must be validated with the fire protection consultant at detailed design.

Source: Addendum 03 §1; ASSUMPTION on HRV feasibility in bunker gear room; Semantic lensing item D-001.

### C-005: Ground-Source Heat Pump Feasibility Is TBD

The 2021 geotechnical investigation report (Appendix D) may provide information relevant to ground-source heat pump (GSHP) loop feasibility (soil thermal conductivity, groundwater depth, freeze risk). However:
- The decomposition confirms that no additional geotechnical investigation is included in this proposal (DEC-013).
- GSHP feasibility assessment is therefore constrained to information in the existing 2021 report.
- If GSHP is considered, it should be presented as a future value-add option, not a committed base design element, unless the existing report clearly supports it.

Source: Decomposition DEC-013; Decomposition DEL-10-02 description.

---

## Trade-Offs

### T-001: All-Electric Heat Pump vs. Hybrid Gas + Electric HVAC

| Aspect | All-Electric Heat Pump | Hybrid Gas + Electric |
|---|---|---|
| Efficiency | Higher — COP 3.0–4.5 in moderate temps | Lower — gas furnace AFUE 95%+ but still less efficient than heat pump |
| Cold-Climate Performance | Air-source heat pump efficiency drops at low ambient temps (below −15°C to −25°C); cold-climate heat pump models extend range | Gas backup handles cold-snaps reliably |
| Operating Cost | Higher if electricity cost/GJ > gas cost/GJ (Alberta context); lower if carbon pricing escalates | Lower in Alberta's current gas-dominant context |
| Operator Familiarity | Less familiar to typical municipal operations team | Gas systems are more familiar |
| Upfront Cost | Higher | Lower |
| Net-Zero Readiness | Better aligned if Owner has long-term electrification goals | Less aligned |
| **Recommendation** | Present both options; recommend based on Owner's energy goals and lifecycle cost analysis — ASSUMPTION: Owner preference TBD | Hybrid may be more practical for Alberta operations context given current electricity/gas price ratio |

Source: ASSUMPTION based on Alberta energy context; specific lifecycle cost comparison TBD at detailed design.

### T-002: HRV Coverage Scope — All Zones vs. Key Zones Only

| Aspect | HRV on All Exhaust Zones | HRV on Residential + Office Only |
|---|---|---|
| Energy Recovery | Higher total recovery | Lower but cleaner recovery |
| Apparatus Bay Applicability | Limited (contamination); specialized units required | Excluded — saves cost and complexity |
| Capital Cost | Higher | Lower |
| Maintenance | More filter surface area; more units to service | Simpler maintenance program |
| **Recommendation** | HRV on residential quarters and offices (clean exhaust, high occupancy hours, high value); evaluate apparatus bay heat pipe recovery separately; exclude PW bay from HRV if intermittent use makes payback poor | TBD at detailed design based on exhaust air quality assessment |

Source: ASSUMPTION based on apparatus bay contamination constraint per Addendum 03 §1.

### T-003: Solar Rough-In Scope — Minimal vs. Full Preparation

| Aspect | Minimal Rough-In (sleeves only) | Comprehensive Preparation |
|---|---|---|
| Base Design Cost | Very low | Low to moderate |
| Owner Flexibility | Adequate for future retrofit | Maximum flexibility |
| Future Retrofit Cost | Moderate (some disruption for routing) | Low (all provisions in place) |
| Design Effort Now | Minimal | Requires coordination between mech/elec/struct |
| **Recommendation** | Comprehensive preparation is the better value — the marginal cost is small, and it demonstrates solar readiness credibly to evaluators while maximizing Owner's future options | Source: Addendum 03 §1 intent |

Source: Addendum 03 §1; ASSUMPTION on cost-benefit of comprehensive vs. minimal rough-in.

### T-004: Sub-Metering Depth

| Aspect | Whole-Building Only | Key System Sub-Metering (4–6 points) | Comprehensive Sub-Metering |
|---|---|---|---|
| Cost | Low | Moderate | High |
| Operational Value | Limited fault detection | Good fault detection; actionable data for major consumers | High granularity but often unused by small municipal operations team |
| Owner Burden | Minimal | Manageable | May exceed operations team capacity to monitor and act |
| **Recommendation** | Key system sub-metering: apparatus bay HVAC, DHW, office/residential HVAC, PW bay ventilation (4 main points); whole-building utility meters as baseline | Source: ASSUMPTION on appropriate metering depth for facility type and Owner operations profile |

Source: Decomposition DEL-04-02 description; ASSUMPTION on metering scope.

---

## Examples

### EX-001: Apparatus Bay Exhaust Energy — Constraint and Partial Recovery Strategy

**Scenario:** Two fire apparatus bays, each with 2 apparatus positions and direct exhaust ventilation per Addendum 03. Conditioning loss from exhaust is significant in Alberta winter (heating season approximately October–April).

**Constraint:** Direct exhaust draws combustion by-products from vehicle engines; airstream is not clean enough for standard HRV recovery.

**Partial recovery approach (ASSUMPTION: feasibility subject to air quality assessment at detailed design):**
- Install a dedicated isolated exhaust heat exchanger (heat pipe type) on apparatus bay exhaust duct — no cross-contamination between exhaust and supply air streams.
- Recovered heat preheats fresh air makeup to the apparatus bay (not to other zones), reducing the heating load on the primary HVAC unit serving the bays.
- Expected sensible recovery: 40–60% of exhaust heat (heat pipe typically less efficient than full HRV, but safe for contaminated streams).
- Outcome: 10–15% reduction in apparatus bay heating energy compared to no recovery.

**Fallback if air quality prevents any recovery:** Accept energy loss; document the constraint in the narrative; compensate by optimizing envelope performance in apparatus bay walls and doors.

Source: ASSUMPTION on heat pipe applicability; Addendum 03 §1 (direct exhaust requirement).

### EX-002: Solar Thermal Rough-In — What "Mechanical Ready" Looks Like

**Scenario:** Owner wants the building to be solar-thermal ready for future DHW preheat system.

**Mechanical rough-in provisions (base design):**
1. Two 1.5" copper or CPVC sleeves through roof deck at a designated solar panel location (south or west-facing slope, or flat roof with racking area reserved).
2. Sleeves terminated with removable caps at roof level and rough-in couplings at mechanical room ceiling — labeled "FUTURE SOLAR THERMAL."
3. 6 ft² floor space reserved in mechanical room adjacent to DHW tank for future solar thermal storage tank and heat exchanger.
4. DHW tank selected with auxiliary inlet port to accept solar thermal preheat loop connection.
5. Isolation valves on DHW cold water inlet and hot water outlet for future solar loop integration.

**Cost:** Approximately $2,000–$5,000 in base design (ASSUMPTION: rough order-of-magnitude). Future solar thermal system installation enabled without roof or mechanical room reconstruction.

Source: ASSUMPTION on rough-in detail; Addendum 03 §1 (solar-capable roof); Decomposition DEL-04-02 description.

### EX-003: Demand-Controlled Ventilation in PW Bay — Practical Implementation

**Scenario:** PW bays are used intermittently — occasional vehicle idling for short periods and very occasional welding. Addendum 03 §1 specifies general ventilation (not direct exhaust), adequate for the use profile.

**DCV approach:**
- Install CO sensor at vehicle height in PW bay (mounted at 1.5 m to capture idling exhaust at source level) — ASSUMPTION: CO sensor triggers ventilation fan to high rate when CO concentration rises above threshold (e.g., 35 ppm — ASSUMPTION based on ASHRAE 62.1 CO limits).
- Occupancy sensor at bay entry/exit: ventilation system in low-rate (minimum outdoor air) mode when bay is unoccupied.
- Manual override switch at bay entry for operations staff to activate high-rate ventilation on demand (e.g., welding event).
- Fan control: two-speed or variable frequency drive (VFD) exhaust fan; low rate (approximately 10–15 ACH) during standby; high rate (approximately 25–30 ACH) during occupancy/CO event — ASSUMPTION on air change rates.

**Energy saving:** DCV reduces exhaust fan run-time and heating load significantly compared to constant high-rate ventilation. In an intermittently used bay, energy savings of 40–60% on ventilation energy vs. constant-on approach are typical — ASSUMPTION based on industry experience with DCV in vehicle maintenance garages.

Source: Addendum 03 §1; ASSUMPTION on DCV implementation details; ASHRAE 62.1 (location TBD for CO threshold).

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| TBD-001 | **Lifecycle cost analysis scope unclear:** Guidance T-001 references "lifecycle cost analysis" as a decision factor for heat pump vs. hybrid HVAC selection, but no R-MEL requirement mandates production of a lifecycle cost or payback period analysis. It is unclear whether the Owner or RFP requires lifecycle cost analysis as a narrative element, or whether the reference in T-001 is aspirational context only. If lifecycle cost analysis is required, it should be captured as a requirement in Specification.md. | Guidance.md T-001 ("lifecycle cost analysis" referenced as decision factor) | Specification.md Requirements (no R-MEL requirement mandates lifecycle cost analysis; scope exclusions do not mention it) | Specification.md Requirements; Guidance.md T-001; Procedure.md Step 3 | Design Manager + Proposal Manager | TBD |

If conflicts arise during cross-discipline coordination (e.g., envelope U-value target inconsistent with mechanical load assumptions, solar roof orientation not achievable on site, apparatus bay HRV technically infeasible), they shall be captured here and escalated to the Design Manager for resolution before narrative finalization.
