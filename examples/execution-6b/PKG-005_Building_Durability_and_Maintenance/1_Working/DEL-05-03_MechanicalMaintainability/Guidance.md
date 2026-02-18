# Guidance — DEL-05-03: Mechanical Maintainability

---

## Purpose

This deliverable exists to demonstrate to the Town of Penhold that the mechanical systems of the Public Services Building will be designed and documented in a way that:

1. Minimizes operational disruption from routine maintenance tasks and emergency repairs.
2. Reduces lifecycle costs through standardized parts, modular design, and efficient equipment selection.
3. Supports the Fire Department and Public Works operations teams with practical access, clear procedures, and readily available spare parts.
4. Meets all applicable codes and standards for equipment safety and accessibility.

Mechanical maintainability is scored as part of the **Building Durability / Ease of Repair & Maintenance** evaluation criterion (OBJ-005, 15 evaluation points), the second-highest-weighted technical criterion after Conceptual Design (20 pts). The RFP states directly that all project design "must be practical, energy efficient, cost effective, and easy to maintain" (OSR §10.3.4) and that the proposal shall describe "the ease of repair and maintenance of the building and all systems and components" (RFP §7.1.4). This signals that the Town values a design the operations team can realistically maintain without constant contractor dependence.

**OBJ-005 scoring expectations and level of detail:** The 15-point evaluation weight is the second-highest technical criterion. While the RFP scoring rubric does not publish granular point breakdowns per sub-topic, the evaluation language ("describe the approach to building durability ... ease of repair and maintenance of the building and all systems and components") signals that a high-scoring submission should demonstrate: (a) system-by-system specificity rather than generic narrative -- i.e., each major mechanical system should have an identifiable maintainability strategy; (b) quantified lifecycle cost evidence where available (even if preliminary), not narrative-only summaries; and (c) operational credibility -- demonstrating that the proposed maintenance approach accounts for the Town's actual staffing model (combined Fire/PW team with limited in-house mechanical expertise). ASSUMPTION: The distinction between a high-scoring and a passing submission is the depth of system-specific evidence and operational realism; confirm with Design Committee or Town evaluation panel if available guidance exists on scoring rubric granularity (see _SEMANTIC_LENSING.md D-002).

Source: RFP §7.1.4 (verbatim); RFP OSR §10.3.4 (verbatim); Decomposition v2 §6 (OBJ-005); RFP §8.3 (Scoring Matrix).

---

## Principles

**P-001: Operations-First Design Philosophy**

Equipment layout shall prioritize the mechanical equipment owner's ability — typically the Public Works Superintendent or Fire Chief's designate — to troubleshoot and replace components without architectural redesign, invasive structural work, or contractor call-outs for routine tasks. Service routes, mechanical room aisles, and panel door clearances shall be dimensioned to accommodate a standard two-person equipment removal team with typical tools and a wheeled cart. Minimum 900 mm (3 ft) service aisle widths are the baseline standard.

The RFP explicitly intends the building to facilitate "safe and efficient … maintaining and operating equipment within the buildings" (OSR §10.3.4). Mechanical design must take this intent seriously at the layout stage, not as a post-design add-on.

Source: RFP §7.1.4; RFP OSR §10.3.4; Decomposition v2, DEL-05-03 definition ("equipment access provisions, service routes, mechanical room layout").

---

**P-002: Standardization Over Customization**

Selection of mechanical equipment shall favor industry-standard components: common refrigerant types, standard valve configurations, pump models with widely available impellers, and fan motors with off-the-shelf bearings. Proprietary or manufacturer-exclusive components require justification via lifecycle cost analysis that explicitly accounts for higher maintenance costs and longer procurement lead times.

Rationale: A small municipal team combining Fire Department and Public Works cannot maintain deep expertise in multiple proprietary platforms. Standardization reduces spare parts inventory, shortens procurement lead times, and enables cross-training of staff on similar equipment across both departments.

Source: RFP §7.1.4 ("serviceability" emphasis); RFP §11.3 ("durable, flexible materials for easy maintenance", verbatim); ASSUMPTION: municipal operations best practice consistent with OBJ-005 "operations-aware" framing.

---

**P-003: Preventive Maintenance as the Default Mode**

All mechanical systems shall be designed with routine maintenance as the normal operating posture — not as an afterthought. Degradation shall be visible or easily measurable: filter pressure-drop indicators, oil sight glasses on pump casings, refrigerant pressure gauges, low-fuel alarms on the generator. Silent failure modes shall be designed out wherever possible.

Rationale: Proactive maintenance prevents catastrophic failures during apparatus response or emergency operations. An apparatus bay exhaust system failure during a structure fire response is a health and safety incident — not merely a comfort issue. The Town operates a combined facility where systems failures can simultaneously impact two critical municipal services.

Source: NFPA 25 (fire pump maintenance philosophy); NFPA 110 (generator maintenance requirements); general best practice for public safety facilities.

---

**P-004: Lifecycle Cost Optimization**

Equipment selection trade-offs (higher capital cost for higher-efficiency unit vs. lower operating cost) shall be documented with a simple payback or 20-year NPV analysis. The planning horizon for major equipment replacement shall be 20 years — consistent with both the Cold Storage design life and a mid-cycle replacement point for the main building (50-year life).

**Rationale for the 20-year planning horizon (rather than 25 or 30 years):** The 20-year figure is selected because (a) it aligns with the Cold Storage building's full design life, enabling a single consistent analysis period across both structures; (b) it represents the approximate mid-cycle replacement point for the main building (50-year design life), at which most major mechanical equipment (boilers, chillers, air handling units, generators) will require either major overhaul or full replacement regardless of initial quality; and (c) economic assumptions (energy cost escalation, discount rates, maintenance cost escalation) become increasingly speculative beyond 20 years, reducing the reliability of longer-horizon analyses. If the Design Committee or Town evaluation panel requires a longer horizon (e.g., 30-year or full 50-year building life), the analysis methodology should be adjusted accordingly, but the 20-year mid-cycle basis provides the most defensible and actionable comparison for equipment selection decisions at this stage. ASSUMPTION: 20-year horizon is the appropriate default; confirm with Mechanical Engineer and Design Committee (see _SEMANTIC_LENSING.md D-001).

The RFP explicitly names "lifecycle cost considerations for major mechanical equipment" as a required component of this narrative (SOW-0013 scope; RFP §7.1.4). Documentation of these trade-offs is not optional.

Source: RFP §7.1.4 (lifecycle cost considerations explicit); RFP OSR §10.3.4 ("cost effective"); SOW-0013; Decomposition v2, DEL-05-03 definition.

---

**P-005: Filter Accessibility as a Priority**

Apparatus bay exhaust filters require quarterly inspection due to diesel combustion residue accumulation from fire apparatus start-up and warm-up cycles. All filter elements — HVAC, exhaust, sump discharge strainers, and fill station strainer baskets — shall be accessible without tools (or with only standard hand tools) and without depressurizing or fully shutting down the system they serve.

The RFP explicitly states that ventilation system filter access and maintenance — especially apparatus bay exhaust — is a named scope element of this deliverable (SOW-0013 scope description; Decomposition v2, DEL-05-03 entry).

Source: RFP §11.1.1; Addendum 03 §1.12 (direct exhaust per bay required, verbatim); SOW-0013 explicit scope language.

---

**P-006: Spare Parts Strategy as Built-in Operational Support**

Dedicated shelf or bin space in the mechanical room shall be allocated for a 1-year supply of consumables (filters, belts, seals) and 5-year replacement cycle major items (pump impellers, motor bearings). Supplier agreements should target 48-hour spare availability for non-stock critical items (ASSUMPTION: consistent with municipal operations standard practice).

The 150–300 sq ft storage allocation estimate assumes a mechanical room large enough to accommodate both equipment and a dedicated maintenance inventory area. This estimate shall be confirmed at the mechanical room layout stage.

Source: RFP §7.1.4 ("maintenance strategy"); ASSUMPTION: fire and PW facility standard practice.

---

## Considerations

**C-001: Apparatus Bay Environment Drives Higher Maintenance Frequency**

The apparatus bay is not a typical commercial HVAC environment. Diesel combustion residue from apparatus start-up and warm-up cycles accumulates on exhaust system filters at a rate significantly higher than in office or light commercial spaces. The direct exhaust system required by Addendum 03 §1.12 must be designed with quarterly filter inspection as the normal operating assumption, not the exception.

The apparatus bay also has bay sumps (Addendum 03 §1.8) introducing high-moisture conditions from snow melt. The combination of moisture, diesel soot, and de-icing chemical contamination in bay environments makes corrosion-resistant materials and accessible drainage provisions essential for any equipment located in or adjacent to apparatus bays.

Source: Addendum 03 §1.8, §1.12; RFP §11.1.1; RFP §11.3; ASSUMPTION: diesel combustion residue accumulation rate inference from operational environment.

---

**C-002: Bunker Gear Room — Moisture and Mold Risk**

Forty (40) bunker gear lockers in an enclosed room create a concentrated moisture load from damp gear after fire responses. Room ventilation required by Addendum 03 §1.14 must provide sufficient air changes to prevent mold and mildew accumulation on gear and locker surfaces. The ventilation design must also be maintainable by non-specialist operations staff: accessible filter changes and adjustable dampers are the minimum requirement.

Note that Addendum 03 §1.14 specifically states direct ventilation to each locker is NOT required; room-level ventilation IS required. The design must achieve moisture removal at the room level, not through individual locker ductwork.

Source: Addendum 03 §1.13 (40 lockers required), §1.14 (room ventilation required, verbatim); ASSUMPTION: moisture and mold risk inference from gear storage operational context.

---

**C-003: Cold Storage — Freeze-Thaw Is the Primary Mechanical Durability Driver**

The Cold Storage building is unheated (ASSUMPTION: inferred from "cold storage" classification and 20-year design life context). Any mechanical equipment installed there — ventilation fans, condensation drains, sump pumps — must be rated for freeze-thaw cycling. The RFP explicitly requires "adequate ventilation or alternate air circulation to prevent condensation and icing" (§11.1.2). Standard condensate drain pans and uninsulated drain lines will freeze and fail during Penhold winters; all Cold Storage mechanical installations must be specified for unheated enclosure temperature ranges.

Source: RFP §11.1.2 (condensation and icing prevention, verbatim); ASSUMPTION: unheated designation from "cold storage" classification and 20-year design life context.

---

**C-004: Generator Fuel Type — Site Utility Availability Is Determinative**

Natural gas availability at the site (Addendum 03 §1.6: gas services "within a few feet of the site") makes natural gas a viable generator fuel choice. Natural gas generators eliminate on-site fuel storage tank maintenance but introduce dependency on the utility supply line during an extended emergency (relevant if the 72-hour runtime target is ultimately confirmed — see Conflict Table below). Diesel generators require on-site fuel management but are independent of utility infrastructure.

The Design-Builder shall select fuel type and document the rationale in the Mechanical Concept Narrative (DEL-02-04), with maintainability implications — fuel storage access, oil service intervals, fuel system inspection — addressed in this narrative.

Source: Addendum 03 §1.6 (gas service proximity); Addendum 03 §1.15 (generator required); ASSUMPTION: fuel type selection deferred to Mechanical Design Brief.

---

**C-005: Bay Door Secondary Opening — Generator Power vs. Manual Override**

Addendum 03 §1.15 explicitly allows the bay door secondary opening mechanism to be either generator-powered or manually operated ("either by backup generation power or manually opening"). The choice has maintenance implications:

- Generator-powered secondary opening: requires the generator to reliably start and transfer load before occupants attempt to exit; increases annual generator load test complexity; introduces an additional electrical control circuit requiring periodic testing.
- Manual override: requires a simple, clearly labeled, physically accessible mechanism at each door; no power dependency; periodic mechanical inspection only.

Both options are maintainable without specialized contractors. The Design-Builder shall document the chosen approach and its maintenance requirements.

**Decision framework (ASSUMPTION — for Design-Builder consideration):** The manual override option is recommended as the default approach unless the generator-powered option provides a demonstrable operational advantage, based on the following criteria:

| Criterion | Manual Override | Generator-Powered |
|---|---|---|
| **Power dependency** | None — operates independently of all electrical systems | Requires generator start and ATS transfer before doors can open |
| **Maintenance burden** | Low — periodic mechanical inspection of release mechanism, lubrication of tracks/springs only | Higher — annual generator load test must include bay door circuit; additional electrical control circuit requires periodic testing and troubleshooting |
| **Reliability during extended outage** | High — functional regardless of fuel supply or generator failure | Dependent on generator fuel supply and reliability; if generator fails, doors cannot open electrically |
| **Training complexity** | Low — simple physical release mechanism demonstrated once | Moderate — operations staff must understand ATS sequence and generator circuit to troubleshoot door failures during outage |
| **Capital cost** | Lower — no additional electrical/control infrastructure | Higher — requires wiring, controls, and integration with ATS |

The manual override approach minimizes maintenance burden and eliminates a single point of failure (generator) from the emergency egress pathway. However, if the generator-powered approach is selected, the maintenance plan must include the bay door circuit in the annual generator load test and document the control circuit inspection as a separate maintenance task. The Design Committee should confirm the preferred approach during the Design Brief phase (see _SEMANTIC_LENSING.md E-002).

Source: Addendum 03 §1.15 (verbatim: "either by backup generation power or manually opening").

---

## Trade-offs

**T-001: Capital Cost vs. Operating Efficiency (HVAC)**

High-efficiency HVAC equipment (e.g., variable refrigerant flow, high HSPF heat pumps) carries higher capital cost but lower annual energy consumption. For a 50-year building life, lifecycle cost savings from efficiency can significantly exceed the capital premium at current energy prices.

- Trade-off: Higher capital in exchange for lower 20-year operating cost.
- Counterpoint: High-efficiency equipment often uses proprietary components (variable-speed compressors, advanced inverter boards) that conflict with the standardization principle (P-002). The lifecycle cost analysis must account for higher maintenance costs, not just energy savings.
- Decision authority: Mechanical Engineer with Design Committee input; detailed analysis in DEL-04-02 (Mechanical Energy and Solar Readiness).
- Source: RFP §7.1.4 ("lifecycle cost considerations"); RFP OSR §10.3.4 ("cost effective"); Decomposition v2, OBJ-004.

---

**T-002: Equipment Redundancy vs. Capital Cost**

Dual-unit designs for critical systems (apparatus bay exhaust fans, main HVAC units) provide built-in redundancy but increase capital cost. Single-unit designs are less expensive but create a single point of failure during the servicing cycle.

- Lower-cost alternative: A portable backup fan stored in the maintenance inventory, capable of bridging a primary apparatus bay exhaust fan failure during service, avoids the capital cost of permanent dual-unit installation. This option is viable only if the portable unit can be deployed quickly and safely in the bay environment.
- Decision authority: Mechanical Engineer; documented in Mechanical Concept Narrative (DEL-02-04).
- Source: ASSUMPTION (operations resilience principle); RFP §7.1.4 ("ease of maintenance" implies minimal single points of failure where feasible).

---

**T-003: Standard Parts vs. Optimized Performance**

Some high-efficiency equipment (variable-speed compressors, advanced economizer controls) uses proprietary components not available through general distributors. If such equipment is selected, the maintainability cost — longer lead times, manufacturer-only service, specialized technician call-out — may offset the operating efficiency benefit.

- Trade-off: Any non-standard equipment selection must be justified with a lifecycle cost analysis that explicitly accounts for higher maintenance costs. If proprietary equipment is selected, include an extended warranty or 24/7 service agreement to offset the operational risk.
- Decision authority: Mechanical Engineer with Design Committee sign-off.
- Source: RFP §11.3 ("durable, flexible materials for easy maintenance"); ASSUMPTION: municipal operations capability constraint.

---

**T-004: Filter Frequency vs. Filter Type**

MERV 13 (pleated, high-efficiency) filters provide better air quality and combustion particulate capture but require more frequent replacement (every 1–3 months in high-load apparatus bay zones) than lower-MERV filters. Washable pre-filters in high-load zones can extend the replacement interval for the primary filter but introduce a wash-and-dry cycle as a maintenance task with its own labor and disposal implications.

- Proposed approach: Specify filter banks sized for larger filter face area to extend change intervals; use washable metal mesh pre-filters in apparatus bay exhaust where combustion particulate is concentrated, paired with a replaceable primary filter.
- Decision authority: Mechanical Engineer based on zone air quality requirements, OEM filter recommendations, and Town operational feedback.
- Source: RFP §11.1.1; Addendum 03 §1.12; ASSUMPTION: MERV and filter interval inference from apparatus bay operational context.

---

## Examples

**EX-001: Apparatus Bay Exhaust — Quarterly Filter Inspection Procedure (Proposed)**

*Purpose:* Verify that the direct exhaust filter is not overloaded; schedule replacement before airflow restriction creates a health and safety risk.

*Steps:*
1. Confirm apparatus is parked outside or bay is unoccupied during inspection.
2. Rotate the exhaust isolation damper to "SERVICE" position (labeled, quarter-turn handle).
3. Confirm the airflow indicator (visual ball-in-tube or pressure-drop gauge) shows no flow.
4. Open the filter access door (recessed into duct soffit at approximately 7 ft height; 4 hand-captive bolts).
5. Visually inspect the filter cartridge: light gray = acceptable; medium gray = schedule replacement within 30 days; dark gray or black = replace immediately.
6. Return isolation damper to "NORMAL" position; confirm airflow indicator shows flow restored.
7. Log: date, inspector name, filter condition, date of next inspection (3 months).

*Annual Filter Replacement (additional steps):*
8. Follow steps 1–3 above.
9. Slide old cartridge out of frame (approximately 24" length, 5 lbs — one person can handle).
10. Insert new cartridge from shelf stock; bolt door closed.
11. Confirm airflow restored; log completion with filter part number and supplier date code.

Benefit: Operations staff complete this task without a contractor call-out. Total time: approximately 30 minutes. Spare filters kept in mechanical room stock.

Source: Addendum 03 §1.12 (direct exhaust per bay required); RFP §7.1.4 ("ease of maintenance"); RFP §11.1.1; procedure steps are ASSUMPTION based on standard apparatus bay exhaust system design.

---

**EX-002: Water Fill Station Annual Flushing Procedure (Proposed)**

*Purpose:* Confirm the 2" fill station is free of sediment and functioning correctly; verify strainer basket condition.

*Steps:*
1. Connect a hose-end cap to the 2" fill station coupling.
2. Open the isolation shutoff valve (labeled red ball valve at wall).
3. Open the fill station nozzle and run at full flow for 60 seconds. Note water colour.
4. If water is clear: close nozzle; close shutoff valve; log as "clear — OK."
5. If water is discoloured (rust, sediment): close isolation shutoff; open strainer bowl union; remove and rinse the basket in clean water; reinstall; reopen shutoff; repeat flush until clear. Additional time: approximately 15 minutes.
6. Log: date, inspector name, water clarity on first flush, strainer condition, date of next inspection (12 months).

Benefit: Simple, non-invasive procedure; sediment removal prevents fitting damage and corrosion; confirms fill station is ready for apparatus deployment.

Source: Addendum 03 §1.16 ("one fill station at ground level … both fill stations should be 2" minimum", verbatim); RFP §11.2; procedure steps are ASSUMPTION based on standard fill station maintenance practice.

---

**EX-003: Backup Generator Annual Load Test (Contractor-Supervised)**

*Purpose:* Verify the generator will start and carry full critical load in an emergency; exercise engine components to prevent fuel degradation and corrosion.

*Steps:*
1. Contractor technician brings portable load bank to exterior generator service pad.
2. Notify operations staff that the building will briefly transfer to generator power (non-emergency test; mains power available as backup).
3. Manually actuate the automatic transfer switch (ATS) to GENERATOR mode.
4. Increase load in steps: 25%, 50%, 75%, 100% of rated capacity.
5. Monitor at each step: voltage, frequency, engine oil temperature, coolant temperature, fuel consumption rate.
6. Hold at 50–75% load for 30 minutes minimum (exercises engine and charges battery).
7. Return ATS to NORMAL (utility power); confirm all critical loads restore correctly.
8. Document test report: date, load levels, voltages, temperatures, fuel consumption, battery state. File with O&M manuals.

Frequency: Annual (recommended spring, before summer cooling season when critical loads are highest).
Estimated cost: $500–800 per annual test (ASSUMPTION).

Minimum generator loads served (confirmed): kitchen, ICP/meeting room, 2 bathrooms, bay door secondary opening mechanism.

Benefit: Annual testing prevents silent failure; ensures generator is available when Fire or PW operations requires emergency power.

Source: Addendum 03 §1.15 (generator required; critical loads defined, verbatim); NFPA 110 (generator testing requirements; specific clause locations TBD); procedure steps are ASSUMPTION based on standard standby generator annual testing practice.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-01 | **Generator runtime target:** A 72-hour runtime target for the generator has been referenced in project context (Decomposition v2, noted as an open issue in prior work). This target is NOT confirmed in Addendum 03 §1.15, which specifies only minimum loads (kitchen, ICP/meeting room, 2 bathrooms; bay door secondary opening). If the 72-hour target is a real requirement, it significantly affects generator sizing, fuel tank size, and maintenance provisions (fuel consumption monitoring, tank inspection schedule, diesel fuel turnover if diesel is selected). | Decomposition v2 (prior open issue notation; not part of the v2.3 FINAL decomposition text) | Addendum 03 §1.15 (minimum loads stated; runtime not specified; Addendum governs) | Specification R-MEL-08; Datasheet Construction table (generator row); Procedure Step A1 (generator baseline); Guidance C-004 (fuel type selection) | PROPOSAL: Treat 72-hour runtime as an ASSUMPTION in this narrative pending confirmation. If confirmed by Town during Design Brief development, update generator sizing, fuel management provisions, and fuel tank inspection schedule in the Mechanical Maintainability narrative. | TBD |
| CONF-02 | **Fire sprinkler system type — main building vs. Cold Storage:** The Datasheet Construction table describes the fire protection system as "wet or dry pipe per detailed design (TBD)" without distinguishing between the main building and the Cold Storage building. In an unheated Cold Storage building, a wet pipe sprinkler system would freeze and fail; dry pipe would be mandatory. The main building (heated) could use either wet or dry pipe. The documents do not flag this as a coordination issue requiring separate system type decisions for each building. Additionally, whether Cold Storage requires fire protection at all is itself TBD (see Datasheet Attributes, "Cold Storage fire protection" row; _SEMANTIC_LENSING.md E-001). | Datasheet Construction table (fire protection row: "wet or dry pipe per detailed design (TBD)") | Guidance C-003 (Cold Storage freeze-thaw: "any mechanical equipment ... must be rated for freeze-thaw cycling") | Specification scope (Cold Storage in-scope); Datasheet Construction (fire protection row); Datasheet Attributes (Cold Storage fire protection TBD row) | PROPOSAL: If Cold Storage requires fire protection, the system type must be dry pipe (or pre-action) for the Cold Storage building, specified separately from the main building system. Mechanical Engineer and Fire Protection Engineer shall confirm during Design Brief phase. If Cold Storage does not require fire protection, document the exclusion explicitly and remove Cold Storage from the fire protection maintenance scope. | TBD |
