# Guidance — DEL-04-03: Electrical Energy Efficiency

---

## Purpose

This deliverable articulates the Electrical Engineer's energy efficiency strategy for the Town of Penhold Public Services Building (combined Fire Hall and Public Works Operations facility). The narrative demonstrates how the electrical system will minimize energy consumption while maintaining operational reliability for a 24/7 emergency services environment.

The narrative supports **OBJ-004: Deliver a strong Design Brief (5 pts)** by providing discipline-specific technical justification for electrical design choices aligned with the sustainability goals of **SOW-0012** (energy efficiency and sustainability narrative). It is one of three discipline contributions within **PKG-004 — Sustainability & Energy**, alongside DEL-04-01 (Building Envelope) and DEL-04-02 (Mechanical Energy).

The narrative serves two audiences: (1) the Owner's evaluation committee assessing the proposal's technical quality, and (2) the design team using it as an authoritative scope and rationale document during design development.

---

## Principles

### P-EEE-01: Operational Reliability is the Primary Design Constraint

The Public Services Building is a 24/7 emergency services facility. Lighting design, controls, and electrical infrastructure must maintain continuous operational readiness. Energy efficiency is optimized within this constraint — never at the expense of:
- Lighting reliability in critical areas (apparatus bays, emergency egress, ICP/incident command post)
- Power quality and continuity (generator support for critical loads: kitchen, ICP room, 2 bathrooms, bay door secondary opening per Addendum 03)
- Equipment availability and response speed

**Implication for narrative:** Lead with operational reliability before discussing efficiency. Evaluators for a municipal fire hall will penalize any narrative that appears to trade safety for savings.

**Source:** Addendum 03 (generator minimum loads); Decomposition §4 (24/7 fire operations context); Decomposition DEL-02-04 description.

---

### P-EEE-02: Addendum 03 Solar-Ready Provisions Are Compliance, Not Value-Add

Addendum 03 (Jul 31, 2024) introduced solar-capable roofing and solar-ready electrical provisions as explicit baseline requirements. The narrative must treat these as mandatory compliance items:
- Conduit rough-in from roof to electrical room
- Panel space reservation for future inverter and disconnect equipment
- Pre-identified inverter location

**Implication for narrative:** Do not frame solar-ready provisions as an "optional enhancement." Present them as the compliance baseline, with optional commentary on future PV potential as supplementary context.

**Source:** Addendum 03 (location TBD); Decomposition §4 ("Solar-capable roofing required; orientation: flat, south, west, or southwest"); _CONTEXT.md; _REFERENCES.md.

---

### P-EEE-03: LED Lighting Requires Zone-Specific Design, Not a Single Standard

The facility contains zones with fundamentally different lighting requirements:

| Zone | Characteristics | Lighting Design Priority |
|---|---|---|
| Fire Apparatus Bay | High-bay, 24/7 operations, combustion environment, vehicle maintenance | High illuminance, robust sealed fixtures, limited downtime for maintenance |
| Public Works Bay | High-bay, business hours, workshop tasks, occasional welding | High illuminance, task-lighting provisions, robust fixtures |
| Office / Administrative | Standard office tasks, business hours, daylight available | IES office levels, daylight harvesting candidates |
| Residential / Duty Areas | Living/sleeping quarters, shift-based occupancy | Dimming, night-lighting, circadian-aware CCT if budget permits |
| Cold Storage | Unheated, 20-year building, minimal occupancy | Basic safety/task lighting; cold-rated LED fixtures required |
| Exterior / Site | Wayfinding, security, apparatus apron | Motion-triggered, dark-sky compliant; cold-start capable |

**Implication for narrative:** Address each zone explicitly. A generic "we will use LED" statement is insufficient for a 5-point evaluation criterion.

**Source:** Decomposition Functional Program references; Addendum 03 (room sizing and special requirements); _CONTEXT.md.

---

### P-EEE-04: Lifecycle Cost Justifies Efficiency Investment

Municipal owners evaluate sustainability investments through the lens of operating budget impact, not just capital cost. The narrative should frame LED, motor efficiency, and metering investments using:
- Energy cost reduction (kWh savings × utility rate)
- Maintenance cost reduction (LED fixture life vs. HPS/MH; motor reliability)
- Total Cost of Ownership (TCO) advantage over 50-year building life

**Implication for narrative:** Include at least a directional lifecycle cost argument (e.g., "LED fixtures at 50,000-hour rated life vs. 15,000-hour HPS; 3x fewer replacements over building life"). Exact numbers are estimates (mark as ASSUMPTION); the evaluator is looking for credible cost-awareness, not precision.

**Utility Rate Assumption (TBD):** Lifecycle cost arguments require an assumed electrical utility rate ($/kWh). This essential input is currently **TBD** -- source from local utility (Fortis Alberta or equivalent) or Owner. Until confirmed, lifecycle cost claims in the narrative should be expressed as relative percentages or directional statements rather than absolute dollar figures. (Per Lensing item B-003.)

**Source:** OBJ-005 (durability and ease of maintenance); typical industry practice for municipal facilities; 50-year design life from Decomposition S1.

---

### P-EEE-05: Coordination Across Disciplines Is Required for Consistency

Electrical energy efficiency is interdependent with:
- **DEL-04-01 (Building Envelope):** Daylighting availability and window locations drive daylight harvesting zone definitions; solar roof orientation impacts PV conduit placement
- **DEL-04-02 (Mechanical Energy):** HVAC motor types and sizes are inputs to motor efficiency narrative; future PV sizing depends on solar orientation and HVAC loads
- **DEL-02-05 (Electrical/IT Concept):** Lighting design, controls schematic, and solar conduit/panel planning must be internally consistent with this concept

**Implication for narrative:** Include an explicit coordination summary section. Reference all three deliverables with specific content handoffs described (e.g., "Daylighting zone locations confirmed by DEL-04-01; photosensor placement shown on DEL-02-05 control schematic").

**Source:** _REFERENCES.md cross-references; Decomposition PKG-004 description ("PKG-004 goal: demonstrate a credible energy efficiency and sustainability strategy with discipline-specific contributions").

---

### P-EEE-06: Control Sophistication Must Match Owner's Operational Capacity

Advanced controls (networked occupancy sensors, BMS-integrated daylight harvesting, automated scheduling dashboards) provide optimal energy performance but require:
- Commissioning expertise
- Staff O&M training
- Ongoing IT support capacity

The Town of Penhold is a small municipality with limited IT resources. Control system design must be appropriate to organizational capacity.

**Implication for narrative:** Specify simple, robust controls for most spaces; reserve advanced controls for areas with demonstrated Owner interest/capacity. Design for future upgradeability without major rework.

**Source:** ASSUMPTION — small municipal operator; confirm with Owner's operational profile (TBD). General principle from industry practice for comparable municipal facilities.

---

## Considerations

### C-EEE-01: IES Recommended Levels vs. Energy Code Minimum

**Issue:** IES lighting recommendations often target visual performance for occupant tasks (higher lux). Energy codes (NECB) set Lighting Power Density (LPD) limits that constrain total watts per square metre. A well-designed LED system can satisfy both, but trade-offs exist in high-bay industrial zones (apparatus bays, PW bays) where high lux targets demand high wattage.

**Resolution Approach:**
- In critical operational zones (apparatus bays, PW bays): specify IES-recommended levels, justified on safety grounds; demonstrate LPD compliance through fixture efficacy (high lm/W) and control strategy (dimming reduces average W)
- In secondary zones (storage, bathrooms, corridors): apply NECB LPD limit as ceiling; IES minimum is achievable within that ceiling with modern LEDs
- Document the zone-by-zone approach explicitly; show that IES performance and NECB compliance are achieved simultaneously

---

### C-EEE-02: Apparatus Bay Lighting — Sealed vs. Open Fixtures

**Issue:** Apparatus bays have combustion by-products, occasional washing, and potential chemical exposure (vehicle fluids). Standard LED fixtures may not be suitable without appropriate ingress protection (IP rating).

**Resolution Approach:**
- Specify IP-rated LED fixtures for apparatus bays:
  - **Minimum IP54** for general apparatus bay and workshop areas (protection against dust and water splash from all directions)
  - **Minimum IP65** for designated wet/wash-down zones where bay sumps are present and direct hose wash-down is anticipated (protection against low-pressure water jets from all directions)
- The distinction between IP54 and IP65 is material: apparatus bays with bay sumps (required per Addendum 03) will experience periodic wash-down conditions that exceed IP54 splash protection in the immediate sump/wash area. Confirm zone boundaries with Electrical Lead. (Per Lensing item E-002.)
- High-bay LED luminaires specifically rated for industrial garage/workshop environments
- Avoid surface-mounted fixtures with exposed wiring channels in wash-down areas

**Source:** Addendum 03 (bay sumps required); Decomposition §4 (bay sumps for snow melting, minor washing).

---

### C-EEE-03: Cold Storage Building — Cold-Temperature LED Selection

**Issue:** Cold Storage is an unheated building (20-year design life). Standard LED drivers lose efficacy and can fail at sustained low temperatures (-30°C or lower in Alberta winters). Fixture selection must address cold-start performance.

**Resolution Approach:**
- Specify LED fixtures rated for cold storage environments (typically rated to -40°C)
- Avoid occupancy sensors not rated for cold temperatures
- Occupancy or manual controls acceptable at this level (advanced scheduling not justified for minimal-occupancy unheated storage)

**Source:** Decomposition §1 (Cold Storage = unheated, 20-year design life); ASSUMPTION — Alberta climate minimum temperatures.

---

### C-EEE-04: Sub-Metering Granularity vs. Cost and Complexity

**Issue:** Fine-grained sub-metering (individual circuits or equipment) provides detailed energy tracking but increases meter count, wiring complexity, and data management burden (especially without BMS).

**Resolution Approach:**
- Specify sub-metering at **major operational zones** minimum (fire apparatus bays, PW bays, office/admin zone, shared mechanical/electrical rooms)
- Four to five sub-meters provides meaningful operational insight without excessive complexity
- Design infrastructure for future addition of circuit-level metering without major rework
- BMS integration is optional enhancement, not baseline requirement

---

### C-EEE-06: Exterior/Site Lighting Regulatory Requirements

**Issue:** Exterior and site lighting at the Public Services Building (apparatus apron, parking, wayfinding, security) is subject to regulatory requirements beyond general energy efficiency. Dark-sky compliance, municipal bylaw requirements for exterior lighting, and light trespass considerations all apply but are not addressed in a dedicated consideration section. The Guidance zone table (P-EEE-03) mentions "motion-triggered, dark-sky compliant; cold-start capable" for exterior lighting, and Procedure Step 2 includes exterior fixtures, but the regulatory rationale is absent.

**Resolution Approach:**
- Confirm whether the Town of Penhold or Red Deer County has exterior lighting or dark-sky bylaws applicable to the site (TBD -- confirm with municipality)
- Apply dark-sky compliance principles as good practice regardless of bylaw status: full cutoff fixtures, no uplight, warm CCT (3000K or below) for exterior, motion-triggered activation
- Address light trespass at property boundaries (12-acre site provides buffer, but confirm neighbouring land use)
- Document regulatory basis in narrative: municipal bylaw reference (TBD) or ASSUMPTION (dark-sky compliance as best practice)

**Source:** Guidance P-EEE-03 zone table (exterior lighting row); Procedure Step 2.1 fixture table (exterior fixtures); Lensing item E-001.

---

### C-EEE-05: Solar-Ready Conduit Routing and Sizing

**Issue:** Solar conduit must be sized for plausible future PV cables and routed to minimize wall and ceiling penetrations. Under-sizing forces conduit replacement if Owner installs a larger array; over-routing adds cost.

**Resolution Approach:**
- Assume 2-inch PVC conduit as standard for future solar wiring (accommodates #6 or #8 AWG PV cable for a mid-range array)
- Route via interior MEP chase where possible (protected, avoids exterior exposure)
- Include accessible pull boxes at direction changes
- Coordinate routing with DEL-02-05 one-line diagram and roof plan
- Document conduit route as ASSUMPTION pending final roof design and structural routing

---

## Trade-Offs

### T-EEE-01: Premium LED Fixtures vs. Standard LED Fixtures

| Factor | Premium LEDs (>140 lm/W, advanced controls) | Standard LEDs (~100 lm/W, basic controls) |
|---|---|---|
| Capital cost | +15–20% vs. incandescent/HPS baseline | +5–10% vs. baseline |
| Energy savings | 60–70% reduction in lighting energy | 40–50% reduction |
| Fixture lifespan | 75,000–100,000 hours | 50,000 hours |
| Maintenance frequency | Lower (fewer replacements) | Moderate |
| Control integration | Networked dimming, BMS-ready | Simple switch/sensor |
| Payback period (estimate) | ~8–10 years | ~12–15 years |

**Recommendation:** Premium LEDs and advanced controls in high-traffic operational areas (apparatus bays, duty rooms, training); standard LEDs in secondary spaces (storage, bathrooms). Hybrid approach optimizes capital and operating cost.

**Note:** Cost estimates are illustrative order-of-magnitude; mark as ASSUMPTION in narrative. Exact values depend on fixture quantities from DEL-02-05 lighting schedule.

**Methodology Disclosure (per Lensing item F-003):** Energy savings percentages (60-70%, 40-50%) and payback period estimates (8-10 years, 12-15 years) in this table are based on **engineering judgment and industry benchmarks** for LED vs. conventional lighting in municipal/institutional facilities. They are not derived from project-specific energy modeling or manufacturer-specific data. Actual values will vary based on fixture selection, operating hours, and utility rate (TBD -- see P-EEE-04 utility rate note). Mark as ASSUMPTION in narrative and disclose basis.

---

### T-EEE-02: Full Solar-Ready Provisions vs. No Provisions

| Factor | Full Solar-Ready Provisions (Addendum 03 required) | No Provisions |
|---|---|---|
| Upfront cost estimate | ~$5,000–$8,000 (conduit, pull boxes, panel space) | $0 |
| Future retrofit cost avoided | ~$10,000–$20,000 (wall/ceiling rework, panel upgrade) | N/A |
| Addendum 03 compliance | Compliant | Non-compliant — disqualification risk |
| Owner flexibility | Maximum (Owner can add PV anytime) | Minimal |

**Decision:** Full solar-ready provisions are mandatory per Addendum 03. No trade-off analysis needed — non-compliance is not an option. Cost estimates are ASSUMPTION; include in narrative as indicative figures.

**Source:** Addendum 03 (location TBD); Decomposition §4.

---

### T-EEE-03: Moderate Sub-Metering vs. Main Meter Only vs. Comprehensive BMS-Integrated Metering

| Factor | Main Meter Only | Moderate Sub-Metering (Recommended) | Comprehensive BMS-Integrated |
|---|---|---|---|
| Capital cost | ~$2,000–$3,000 | ~$6,000–$12,000 | ~$20,000–$35,000 |
| Operational insight | None (single monthly bill) | Zone-level cost allocation, performance trends | Real-time circuit-level monitoring, automated alerts |
| Owner IT burden | None | Low (manual meter reads) | High (BMS maintenance, software licensing) |
| Upgradeability | Limited | Can add BMS later | Fully operational now |
| Recommended | No — insufficient for multi-department facility | Yes — balances insight with simplicity | Optional — if Owner has existing BMS or confirmed interest |

**Recommendation:** Moderate sub-metering (4–5 meters covering major zones) as baseline. Comprehensive BMS-integrated approach presented as an optional enhancement with Owner confirmation required.

**Note:** Cost estimates are ASSUMPTION; mark accordingly in narrative. Confirm with Owner preferences during design development.

**Methodology Disclosure (per Lensing item F-003):** Capital cost estimates in this table are based on **engineering judgment and industry benchmarks** for sub-metering equipment in municipal/institutional facilities (meter hardware, wiring, installation, and commissioning). They are not derived from project-specific vendor quotes. Actual values will vary based on meter selection, wiring complexity, and local labor rates. Mark as ASSUMPTION in narrative and disclose basis.

---

## Examples

### EX-EEE-01: Apparatus Bay LED Lighting Design

**Context:** Fire apparatus bay must provide high visibility for vehicle preparation, maintenance, and emergency dispatch. Shift crews work at all hours. Bay includes sumps (Addendum 03) requiring floor wash-down capability.

**Design Approach:**
- Fixture selection: High-output LED high-bay luminaires, minimum IP54 rated (IP65 in designated wash-down zones adjacent to bay sumps — see C-EEE-02), 150W nominal
- IES target: ~120–150 lux at grade level (IES standard for vehicle maintenance areas — ASSUMPTION; confirm with IES reference)
- Color temperature: 4000K (neutral white, accurate color rendering for safety-critical inspection tasks)
- CRI: Minimum 80 (recommended 90 for inspection tasks)
- Control: Occupancy sensor at 70% base output for 24/7 standby; boosts to 100% on occupancy within 30 seconds
- Scheduling: Reduces to 50% from midnight to 0600 when apparatus is staged and bay is unoccupied (saves ~15–20% additional energy during standby hours)
- Coordination: DEL-02-05 provides fixture layout and sensor placement; DEL-04-01 confirms no daylighting available (interior bay)

**Outcome:** High-confidence visual environment for safety-critical tasks; energy-efficient operation through dimming; robust fixture selection handles wash-down and combustion environment.

---

### EX-EEE-02: Solar-Ready Electrical Provisions (Addendum 03 Compliance)

**Context:** Addendum 03 requires solar-capable roofing with flat/south/west/southwest orientation and solar-ready electrical infrastructure. Owner has not committed to PV installation but wants the option without major future rework.

**Design Approach:**
- Roof orientation: South-facing slope or flat roof area confirmed in DEL-02-05 site plan
- Conduit rough-in: 2" PVC conduit from main electrical room to roof, routed through interior MEP chase; pull boxes at each change in direction; labeled "FUTURE SOLAR PV — DO NOT DISTURB"
- Panel space: 2× 60A breaker spaces reserved in main distribution panel; label plate installed: "RESERVED FOR FUTURE SOLAR PV — DO NOT ASSIGN TO OTHER CIRCUITS"
- Inverter location: Roof equipment pad on south/southwest slope (coordinated with structural engineer for roof load capacity); interior wall alternative if Owner prefers easier maintenance access
- Documentation: One-line diagram (DEL-02-05) shows solar conduit schematic and inverter connection point
- Cost estimate: ~$6,000–$8,000 for conduit, pull boxes, and panel space (ASSUMPTION)
- Future PV benefit: Owner can install 25–50 kW PV array without major rework; estimated rework cost avoided: ~$12,000–$18,000 (ASSUMPTION)

**Source:** Addendum 03 (location TBD); _CONTEXT.md; Decomposition §4.

---

### EX-EEE-03: Office Zone Daylight Harvesting Integration

**Context:** Administrative offices and shared spaces (training room, duty room) have access to perimeter daylighting through windows. Alberta's long summer days provide meaningful daylight contributions.

**Design Approach (good practice):**
- Photosensors mounted at ceiling level, calibrated to measure horizontal workplane illuminance
- Dimming ballasts on all perimeter fixtures (within 3–4 m of windows)
- Control logic: Dims artificial lighting proportionally as daylight contribution increases; maintains constant target illuminance at workplane (~300–500 lux for office tasks — ASSUMPTION per IES office standards)
- Occupancy override: Sensor also activates lights when occupancy detected (daylight harvesting does not disable lights on occupancy)
- Coordination: DEL-04-01 (Building Envelope) confirms window-to-wall ratio and glazing specification; photosensor placement confirmed on DEL-02-05 lighting control schematic

**Outcome (good practice):** 20–40% reduction in artificial lighting energy during daylight hours (ASSUMPTION — depends on window-to-wall ratio and orientation); achievable with modest additional control system cost (~$200–$400 per fixture zone for dimming integration).

**Counter-example (what to avoid):** A system that relies entirely on daylighting without occupancy sensing or scheduled dimming would leave lights on in unoccupied spaces after dark — negating savings achieved during day.

---

## Conflict Table (for human ruling)

No conflicts identified during Pass 1 + Pass 2 generation. This table is retained for future use if contradictions emerge during design development or cross-document review.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| — | No conflicts identified | — | — | — | — | N/A |
