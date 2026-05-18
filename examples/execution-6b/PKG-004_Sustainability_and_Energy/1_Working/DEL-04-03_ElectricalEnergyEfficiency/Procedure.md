# Procedure — DEL-04-03: Electrical Energy Efficiency

---

## Purpose

This procedure describes the production process for the Electrical Energy Efficiency narrative — the primary artifact of DEL-04-03. The narrative articulates the Electrical Engineer's energy efficiency strategy for the Town of Penhold Public Services Building and supports proposal evaluation under OBJ-004 (Design Brief, 5 pts). The procedure covers: information gathering, discipline-specific section development, cross-discipline coordination, assembly, review, and records.

---

## Prerequisites

### Required Source Documents

| Document | Content Required | Source | Accessibility |
|---|---|---|---|
| Functional Program (Appendix B) | Space types, quantity, occupancy patterns, operational hours, power requirements | RFP appendix | TBD — obtain from Owner/RFP package |
| OSR (Appendix A) | Energy efficiency expectations; any Owner-specific lighting or motor standards; metering preferences | _REFERENCES.md | TBD — obtain from RFP package |
| Addendum 03 (Jul 31, 2024) | Solar-capable roofing requirement; electrical provisions (conduit, panel space, inverter); 16 ft overhead doors; bay sumps | _REFERENCES.md | Per project RFP package |
| DEL-02-05 draft (Electrical/IT Concept) | Lighting plan, conduit routing schematic, one-line diagram, generator connection | Cross-reference | In-progress; coordinate with Electrical team |
| DEL-04-01 draft (Building Envelope) | Daylighting availability, window/skylight locations, solar roof orientation confirmation | Cross-reference | In-progress; coordinate with Architecture/Building Science |
| DEL-04-02 draft (Mechanical Energy) | HVAC motor types and sizes; solar thermal/PV strategy; generator load confirmation | Cross-reference | In-progress; coordinate with Mechanical Engineer |

### Required Standards Access

| Standard | Use | Accessibility |
|---|---|---|
| IES Lighting Design Guidelines (current edition) | Lux targets by space type; lighting control design principles | ASSUMPTION — Electrical Engineer accesses through firm subscription or IES membership |
| CSA C390 / NEMA Premium Efficiency (IE3 category) | Motor efficiency class selection and procurement specification; canonical Canadian reference is CSA C390 (IE3); NEMA Premium is procurement-equivalent designation (per Lensing item C-002) | ASSUMPTION — accessible by Electrical Lead |
| NECB (National Energy Code of Canada for Buildings) | LPD limits; energy compliance pathway | ASSUMPTION — applicable; confirm edition with AHJ |
| Canadian Electrical Code (CEC) Part I | Wiring, metering, service entrance requirements | ASSUMPTION — applicable; standard practice |

### Internal Prerequisites

- Datasheet (this deliverable) reviewed and accepted as accurate
- Specification (this deliverable) requirements R-EEE-01 through R-EEE-09 confirmed with Electrical Lead
- Guidance document (this deliverable) circulated to Electrical Lead for design approach confirmation

### Owner/Commercial Prerequisites

- Owner's operational profile confirmed: 24/7 fire emergency services; Public Works business hours; shared spaces mixed occupancy (confirm with Owner — TBD)
- Preferences for control sophistication (basic vs. BMS-integrated) and metering granularity — TBD; obtain during Owner coordination if possible before narrative finalization

---

## Steps

### Step 1: Gather and Confirm Coordinating Information (2–3 business days)

**Objective:** Assemble all inputs needed before drafting narrative sections.

**Actions:**
1. Collect Functional Program (Appendix B) and extract: space types, occupancy patterns, operational hours, power requirements by zone
2. Review OSR (Appendix A) and extract: energy efficiency expectations, Owner lighting preferences, motor efficiency references, metering preferences
3. Confirm Addendum 03 solar-ready electrical requirements: conduit, panel space, inverter location, roof orientation options
4. Request current draft versions of DEL-02-05 (Electrical/IT Concept), DEL-04-01 (Building Envelope), and DEL-04-02 (Mechanical Energy)
5. Complete the Coordination Checklist:

| Input | Source | Status | Action if Missing |
|---|---|---|---|
| Space type list and occupancy patterns | Functional Program (Appendix B) | TBD | Request from Proposal Manager |
| Owner energy efficiency expectations | OSR (Appendix A) | TBD | Request from Proposal Manager; mark TBD if unavailable |
| Addendum 03 solar provisions | Addendum 03 | Available | Extract and confirm all three elements |
| Daylighting zones | DEL-04-01 draft | TBD | Request from Architecture/Building Science team |
| HVAC motor schedule | DEL-04-02 draft | TBD | Request from Mechanical Engineer |
| Lighting plan and conduit schematic | DEL-02-05 draft | TBD | Request from Electrical team |

6. **Dependency Readiness Gate Check (per Lensing item F-002):** Before proceeding to Steps 2-5, verify that upstream deliverables DEL-02-05 (Electrical/IT Concept), DEL-04-01 (Building Envelope), and DEL-04-02 (Mechanical Energy) have reached minimum "draft-available" status. Record readiness status:

| Upstream Deliverable | Minimum Required Status | Actual Status | Gate Decision |
|---|---|---|---|
| DEL-02-05 (Electrical/IT Concept) | Draft available for coordination | TBD | Proceed / Hold / Proceed with TBDs |
| DEL-04-01 (Building Envelope) | Draft available for coordination | TBD | Proceed / Hold / Proceed with TBDs |
| DEL-04-02 (Mechanical Energy) | Draft available for coordination | TBD | Proceed / Hold / Proceed with TBDs |

   - If all three are "Draft available": proceed to Steps 2-5.
   - If one or more are unavailable: proceed with TBDs in affected sections, but flag in Step 6 assembly that narrative sections dependent on missing upstream inputs require re-validation before finalization.
   - Document gate decision and rationale.

**Responsibility:** Electrical Engineer (author) or Electrical Lead
**Verification:** All inputs confirmed "Available" or "TBD with plan"; no unaddressed gaps; dependency readiness gate check completed and documented

---

### Step 2: Develop LED Lighting Design and Controls Narrative (3–4 business days)

**Objective:** Produce the lighting design section covering requirements R-EEE-01 through R-EEE-04.

**Actions:**

**2.1 — LED Fixture Selection:**
- Review Functional Program space types and develop a zone list
- For each zone, determine IES-recommended illuminance (lux) — reference specific IES guideline section for each space type
- Select LED fixture family appropriate to zone (high-bay industrial, recessed panel, strip, cold-rated, IP-rated as applicable per Guidance C-EEE-02 and C-EEE-03)
- Document fixture CCT, CRI, and efficacy (lm/W); confirm efficacy supports NECB LPD compliance
- Build Lighting Schedule Table:

| Zone | Quantity (est.) | Fixture Type | Lm Output | CCT (K) | CRI | Efficacy (lm/W) | IP Rating | IES Reference |
|---|---|---|---|---|---|---|---|---|
| Apparatus Bay | TBD | High-bay LED, IP54 (IP65 in wash-down zones per C-EEE-02) | TBD | 4000 | 80+ | 120+ | IP54 / IP65 | TBD — IES vehicle maintenance |
| PW Bay / Workshop | TBD | High-bay LED, IP54 (IP65 in wash-down zones if applicable) | TBD | 4000 | 80+ | 120+ | IP54 / IP65 | TBD — IES workshop |
| Office / Administrative | TBD | Recessed LED panel | TBD | 4000 | 90 | 100+ | Standard | TBD — IES office |
| Duty Room / Residential | TBD | Recessed LED, dimmable | TBD | 3000/4000 | 80 | 100+ | Standard | TBD — IES residential |
| Cold Storage | TBD | Cold-rated LED, -40°C | TBD | 4000 | 70+ | 100+ | IP65 | TBD — IES storage |
| Exterior / Apron | TBD | Exterior LED, cold-rated | TBD | 4000 | 70+ | 100+ | IP65 | TBD — IES exterior |

**2.2 — Lighting Control Strategy:**
- For each zone, determine control type per Guidance P-EEE-03 and P-EEE-06:
  - Occupancy sensing (PIR or ultrasonic): Variable/intermittent occupancy zones
  - Daylight harvesting (photosensor + dimming): Daylit perimeter zones (per DEL-04-01 input)
  - Scheduling (time-based): Zones with predictable operational patterns
  - 24/7 base + occupancy boost: Apparatus bay, emergency egress routes
- Build Control Strategy Table:

| Zone | Control Type | Sensor Technology | Rationale | Expected Energy Reduction |
|---|---|---|---|---|
| Apparatus Bay | 24/7 scheduled base + occupancy boost | PIR or ultrasonic high-bay | 24/7 operations; boost on crew presence | 15–25% vs. constant full output |
| PW Bay | Scheduled (business hours) + occupancy | PIR | Business-hour PW operations; off after hours | 40–50% |
| Office | Occupancy + daylight harvesting | PIR + photosensor | Intermittent occupancy; perimeter daylight | 35–50% |
| Duty Room | Occupancy + manual dimming | PIR + dimmer | Shift-based; circadian considerations | 30–40% |
| Storage / Utility | Occupancy | PIR | Intermittent access | 50–70% |
| Cold Storage | Manual or occupancy (cold-rated) | Manual switch or cold-rated PIR | Low occupancy; simplicity appropriate | 50%+ |
| Exterior / Apron | Motion-triggered + timer | Motion sensor | Security/safety; reduced overnight | 40–60% |

**2.3 — Coordinate Daylighting with DEL-04-01:**
- Obtain daylighting zone confirmation from DEL-04-01 author (which spaces have windows, skylights, or light shelves)
- For those spaces, propose daylight harvesting control
- Confirm photosensor placement feasibility with DEL-02-05 (avoid conflicts with structure, HVAC, etc.)

**2.4 — Draft Lighting Narrative Section:**
- Write 2–3 page section: "LED Lighting Design and Controls"
- Include: technology overview, zone-specific design approach, lighting schedule table, control strategy table, daylighting coordination, energy savings summary

**Responsibility:** Electrical Engineer (lighting specialist) with DEL-04-01 author input
**Verification:** All major zones covered; IES methodology cited; control types justified; daylighting coordination confirmed with DEL-04-01

---

### Step 3: Develop Motor Efficiency Narrative (2–3 business days)

**Objective:** Produce the motor efficiency section covering requirement R-EEE-05.

**Actions:**

**3.1 — Identify Motor Applications:**
- From DEL-04-02 (Mechanical Energy), extract motor-driven equipment:
  - HVAC supply and return fans
  - Heating circulation pumps
  - Apparatus bay direct exhaust fans (2 apparatus per bay, per Addendum 03)
  - Bunker gear room ventilation fan
  - PW bay general ventilation fans
  - Domestic hot water circulation pump (if applicable)
  - Air compressor motor (if in scope)
  - Any other rotating equipment confirmed by Mechanical Engineer

**3.2 — Define Efficiency Standard:**
- Baseline: CSA C390 / NEMA Premium Efficiency (IE3 category minimum) — use this canonical terminology consistently across all documents (per Lensing item C-002; CSA C390 is the Canadian-applicable standard; NEMA Premium is the procurement-equivalent designation)
- Confirm with Mechanical Engineer that standard is compatible with equipment selections
- For motors serving variable-load applications (supply/return fans, circulation pumps): specify Variable Frequency Drive (VFD) application as the baseline approach; VFDs are standard mandatory practice for energy efficiency on variable-load rotating equipment (per Lensing item A-002 and Specification R-EEE-05 VFD Application note)

**3.3 — Build Motor Efficiency Summary:**

| Equipment | Motor Type | Size (hp, est.) | Standard Applied | VFD | Delta Cost (est.) | Annual kWh Savings (est.) | Payback (est., yrs) |
|---|---|---|---|---|---|---|---|
| HVAC Supply Fan | Continuous | TBD | CSA C390 / NEMA Premium (IE3) | Recommended | TBD | TBD | TBD |
| HVAC Return Fan | Continuous | TBD | CSA C390 / NEMA Premium (IE3) | Recommended | TBD | TBD | TBD |
| Apparatus Bay Exhaust Fan | Duty-cycle | TBD | CSA C390 / NEMA Premium (IE3) | Optional | TBD | TBD | TBD |
| Bunker Gear Room Fan | Intermittent | TBD | CSA C390 (IE3 minimum) | No | TBD | TBD | TBD |
| PW Bay Ventilation Fan | Duty-cycle | TBD | CSA C390 / NEMA Premium (IE3) | Optional | TBD | TBD | TBD |
| Heating Circulation Pump | Continuous | TBD | CSA C390 / NEMA Premium (IE3) | Recommended | TBD | TBD | TBD |

Note: Motor sizes are TBD pending DEL-04-02 mechanical equipment schedule. Cost and savings estimates will be populated when motor schedule is available.

**3.4 — Draft Motor Efficiency Narrative Section:**
- Write 1–2 page section: "Motor Efficiency Standards"
- Include: motor load categories, standard selected with rationale, VFD application approach, summary of facility-wide energy savings (directional estimate), coordination with DEL-04-02

**Responsibility:** Electrical Engineer with Mechanical Engineer (motor schedule input from DEL-04-02)
**Verification:** All major motor categories identified; efficiency standard documented; VFD candidates confirmed; coordination with DEL-04-02 author completed

---

### Step 4: Develop Solar-Ready Electrical Provisions Narrative (3–4 business days)

**Objective:** Produce the solar-ready provisions section covering requirement R-EEE-06 (Addendum 03 compliance).

**Actions:**

**4.1 — Confirm Addendum 03 Requirements:**
- Extract all solar-related requirements from Addendum 03: solar-capable roof, orientation (flat/south/west/southwest), electrical provisions (conduit, panel space, inverter location)
- Confirm requirements are fully reflected in this deliverable's Specification (R-EEE-06)

**4.2 — Coordinate with DEL-02-05 and DEL-04-02:**
- Obtain roof plan and orientation confirmation from DEL-02-05 site plan (building orientation on 12-acre site)
- Obtain solar thermal or PV strategy direction from DEL-04-02 (if any future solar thermal included)
- Confirm roof structural capacity with Structural Engineer (DEL-03-03 cross-reference) for inverter equipment pad load

**4.3 — Design Solar-Ready Electrical Provisions:**

**Conduit Routing:**
- Path: Main electrical room → roof (routed via interior MEP chase to minimize exterior exposure)
- Size: 2" PVC conduit (sized for future #6 or #8 AWG solar cable)
- Fittings: Accessible pull boxes at direction changes (minimum every 15 m or at direction changes)
- Labeling: "FUTURE SOLAR PV CONDUIT — DO NOT DISTURB"
- Quantity: TBD based on roof area and estimated array layout (DEL-02-05 coordination)

**Panel Space Allocation:**
- Location: Main distribution panel (near service entrance)
- Reserved spaces: Minimum 2× 60A breaker positions (for future DC disconnect and AC inverter breaker)
- Labeling: "RESERVED FOR FUTURE SOLAR PV — DO NOT ASSIGN TO OTHER CIRCUITS"
- One-line diagram updated in DEL-02-05 to show reserved space

**Inverter Location:**
- Preferred: Interior electrical room wall (easier maintenance access; avoids outdoor exposure)
- Alternative: Roof equipment pad adjacent to solar array area (if interior space unavailable)
- Sizing assumption: Mid-range inverter capacity, 25–50 kW (ASSUMPTION — pending Owner confirmation of future PV scale and roof area from DEL-02-05)
- Structural coordination: Roof pad load communicated to Structural Engineer

**4.4 — Build Solar-Ready Provisions Summary:**

| Component | Description | Size / Capacity Assumption | Status |
|---|---|---|---|
| Roof Conduit | 2" PVC from electrical room to roof | Future #6/#8 AWG cable | Routing TBD pending DEL-02-05 |
| Pull Boxes | Accessible at direction changes | Standard conduit bodies | TBD — quantity per routing |
| Panel Space | 2× 60A breaker positions reserved | DC disconnect + AC inverter breaker | Main panel layout per DEL-02-05 |
| Inverter Location | Interior electrical room (preferred) or roof pad | 25–50 kW estimate | TBD — Owner preference |
| Documentation | One-line diagram schematic; conduit routing drawing | Per DEL-02-05 | Cross-reference confirmed |

**4.5 — Draft Solar-Ready Narrative Section:**
- Write 1–2 page section: "Solar-Ready Electrical Provisions (Addendum 03)"
- Include: Addendum 03 requirement summary, conduit design, panel space allocation, inverter location, cost estimate (~$5,000–$8,000 ASSUMPTION), future PV integration benefit, coordination with DEL-02-05 and DEL-04-02

**Responsibility:** Electrical Engineer with Structural Engineer input (roof load) and Mechanical Engineer input (DEL-04-02 solar strategy)
**Verification:** All three Addendum 03 provision elements addressed (conduit, panel space, inverter location); coordination confirmed with DEL-02-05 one-line diagram; panel space reservation labeled

---

### Step 5: Develop Metering and Sub-Metering Strategy Narrative (2–3 business days)

**Objective:** Produce the metering section covering requirement R-EEE-07.

**Actions:**

**5.1 — Define Metering Architecture:**
- Main utility meter: Single meter serving entire facility (ASSUMPTION — confirm with Owner and local utility provider)
- Sub-metering approach: Zone-level meters for major operational areas

**5.2 — Identify Sub-Meter Zones:**

| Zone | Meter Point Location | Rationale |
|---|---|---|
| Fire Apparatus Bays | Distribution panel serving bay circuits | Track fire operations energy; 24/7 baseline monitoring |
| Public Works Bays | Distribution panel serving PW circuits | Track PW operations and workshop equipment energy |
| Office / Administrative Zone | Distribution panel serving office/admin branch | Track administrative energy; occupancy-linked trends |
| Shared Mechanical / Electrical | Mechanical room panel | Baseline facility HVAC and service equipment loads |
| Generator-Backed Circuits | Sub-panel or circuit monitoring | Confirm generator load profile; track backed loads (kitchen, ICP, bathrooms) |

**5.3 — Specify Sub-Meter Equipment:**
- Type: Revenue-grade or pulse-output meters (compatible with future BMS if Owner chooses to integrate)
- Communication protocol: Modbus RTU or standard (enables future BMS integration without meter replacement)
- Installation cost estimate: ~$600–$1,000 per meter hardware plus wiring and installation labor (ASSUMPTION)
- Total estimated cost (4–5 meters, all-in including wiring and commissioning): ~$6,000–$12,000 (ASSUMPTION)

**5.4 — BMS Integration Option:**
- Baseline: Sub-meters provide manual readout (no automated BMS connection required at initial commissioning)
- Optional enhancement: Sub-meters integrated with Building Management System for real-time monitoring, automated alerts, and reporting dashboard
- BMS enhancement cost: +$8,000–$15,000 above moderate sub-metering baseline for integration and software (ASSUMPTION; total comprehensive BMS metering system ~$20,000–$35,000 all-in; recommend Owner confirm facility management strategy)
- Design for future BMS connection without meter replacement (Modbus protocol specification achieves this)

**5.5 — Draft Metering Narrative Section:**
- Write 1–2 page section: "Electrical Metering and Sub-Metering Strategy"
- Include: metering architecture overview, sub-meter zone table, equipment type, all-in cost estimate (~$6,000–$12,000 for 4–5 meters; ASSUMPTION), BMS integration option, operational benefits

**Responsibility:** Electrical Engineer (or BMS/Controls Specialist if available)
**Verification:** All major zones identified; equipment type specified; BMS integration path described; coordination with DEL-02-05 distribution panel layout confirmed

---

### Step 6: Assemble Integrated Narrative Document (2 business days)

**Objective:** Consolidate all sections into a single cohesive proposal document.

**Actions:**

**6.0 — Pre-Assembly Dependency Verification (per Lensing item F-002):**
Before consolidating narrative sections, verify that DEL-02-05, DEL-04-01, and DEL-04-02 have reached "draft-stable" status. If any upstream deliverable has not reached draft-stable since the Step 1 gate check:
- Re-validate all narrative sections that depend on that deliverable's inputs
- Update TBD items with any newly available information
- Document any sections that remain provisional due to upstream instability
- Escalate to Design Manager if draft-stable status cannot be confirmed before proposal deadline

**6.1 — Consolidate Sections:**
Integrate Steps 2–5 into one document with the following structure:
1. Executive Summary (1 page): Strategy overview, three key highlights (LED efficiency, solar-ready compliance, metering for accountability)
2. LED Lighting Design and Controls (2–3 pages): From Step 2; includes emergency/egress lighting approach (R-EEE-09) and CEC Part I wiring provisions for lighting circuits (R-EEE-08)
3. Motor Efficiency Standards (1–2 pages): From Step 3
4. Solar-Ready Electrical Provisions — Addendum 03 Compliance (1–2 pages): From Step 4; includes CEC Part I wiring provisions for solar conduit (R-EEE-08)
5. Electrical Metering and Sub-Metering Strategy (1–2 pages): From Step 5; includes CEC Part I wiring provisions for metering circuits (R-EEE-08)
6. Cross-Discipline Coordination Summary (0.5–1 page): Explicitly references DEL-02-05, DEL-04-01, DEL-04-02 with specific content handoffs described
7. Assumptions and TBD Items (0.5 page): All ASSUMPTION labels summarized; all TBD items listed with planned resolution path; code-edition ASSUMPTIONs resolution status documented (per Lensing item A-003)

**6.2 — Integrate Tables and Diagrams:**
- Lighting Schedule Table (Step 2.1)
- Control Strategy Table (Step 2.2)
- Motor Efficiency Summary Table (Step 3.3)
- Solar-Ready Provisions Summary Table (Step 4.4)
- Metering Architecture Table (Step 5.2)
- Cross-reference to DEL-02-05 for detailed diagrams (one-line diagram, solar conduit schematic, lighting control schematic)

**6.3 — Format for Proposal:**
- Target length: 6–10 pages (suitable for inclusion in Design Brief, PKG-004 section)
- Format: Consistent with proposal template (font, margins, section headings, figure captions)
- Compliance: Confirm Section 7.1.2 Design Brief formatting requirements are met
- Addendum 03 compliance: Solar-ready provisions section must be clearly identifiable by evaluator

**Responsibility:** Electrical Engineer (primary author); Electrical Lead (section review before Step 7)
**Verification:** All five content areas present; all tables integrated; references to DEL-02-05, DEL-04-01, DEL-04-02 are accurate; ASSUMPTION and TBD items clearly labeled

---

### Step 7: Review and Approval (2–3 business days)

**Objective:** Confirm technical accuracy, cross-discipline consistency, and proposal readiness.

**Actions:**

**7.1 — Internal Technical Review (Electrical Lead):**
- All nine Specification requirements addressed? (R-EEE-01 through R-EEE-09, including R-EEE-08 CEC Part I Compliance and R-EEE-09 Emergency/Egress Lighting)
- All coordinating deliverables referenced accurately? (DEL-02-05, DEL-04-01, DEL-04-02)
- IES, CSA C390 / NEMA Premium (IE3), NECB, and CEC Part I standards cited with proper attribution or ASSUMPTION label?
- All TBD items clearly marked; no invented data?
- All ASSUMPTION statements properly labeled?
- All code-edition ASSUMPTIONs (NECB, IES, CEC, Alberta Building Code) have been resolved to confirmed editions, or formally deferred with escalation path documented? (Per Lensing item A-003; unresolved code editions prevent regulatory audit of narrative claims.)

**7.2 — Cross-Discipline Coordination Review:**
Send draft to DEL-02-05 (Electrical Concept), DEL-04-01 (Building Envelope), and DEL-04-02 (Mechanical Energy) authors:
- Lighting strategy alignment with DEL-02-05 fixture and control schematic: Confirmed?
- Daylighting coordination accurate per DEL-04-01: Confirmed?
- Motor efficiency compatible with HVAC selections in DEL-04-02: Confirmed?
- Solar-ready provisions feasible per roof design (DEL-02-05) and structural (DEL-03-03): Confirmed?

**7.3 — Proposal Integration Review (Design Manager):**
- Narrative aligns with overall proposal strategy and tone?
- Page length and formatting match Design Brief template?
- Narrative supports OBJ-004 scoring (5 pts)?
- Cross-references to other deliverables are consistent throughout proposal?

**7.4 — Owner Coordination (as applicable, TBD):**
- BMS integration preference: Confirmed or deferred to design development?
- Metering granularity: Confirmed or deferred?
- Solar PV scale: Confirmed or deferred?
- Document Owner decisions for consistency with other design choices

**7.5 — Final Sign-Off:**
- Electrical Engineer: Narrative ready for proposal PDF
- Electrical Lead: Approved
- Design Manager: Integration confirmed; narrative locked for PDF assembly (SOW-0001)

**Responsibility:** Electrical Engineer (primary); Electrical Lead (review); Design Manager (proposal integration)
**Verification:** Review checklist complete; cross-discipline feedback incorporated; all TBD items resolved or escalated; sign-off documented

---

## Verification

| Criterion (post-completion) | Verification Method | Pass Condition |
|---|---|---|
| **V-EEE-01: Content completeness** | All five sections present (LED, motors, solar, metering, coordination) | All five sections in final document |
| **V-EEE-02: Requirement coverage** | All nine Specification requirements addressed (R-EEE-01 through R-EEE-09) | Each requirement cited or addressed in narrative |
| **V-EEE-03: Cross-discipline alignment** | DEL-02-05, DEL-04-01, DEL-04-02 authors confirm coordination | Written confirmation from each discipline author |
| **V-EEE-04: Standards citation** | IES, CSA C390 / NEMA Premium (IE3), NECB, CEC Part I cited with attribution or ASSUMPTION label | All standards labeled; no uncited claims |
| **V-EEE-05: Addendum 03 compliance** | All three solar-ready elements addressed (conduit, panel space, inverter) | Narrative explicitly covers all three elements |
| **V-EEE-06: Proposal format** | Page length, formatting, captions comply with RFP §7.1.2 | Design Manager sign-off |
| **V-EEE-07: Internal consistency** | Tables and narrative do not conflict; terminology consistent | Electrical Lead review sign-off |
| **V-EEE-08: No invented data** | All TBD items marked; all ASSUMPTION statements labeled | Technical review checklist pass |

---

## Records

**Primary Artifact:**
- `DEL-04-03_ElectricalEnergyEfficiency_Narrative.docx` — draft working document (6–10 pages)
- Final version merged into proposal PDF at Section 7 (Design Brief) upon completion of PKG-004 integration

**Supporting Tables and Diagrams (embedded in narrative or cross-referenced):**
- Lighting Schedule Table (Step 2.1) — detailed version in DEL-02-05
- Lighting Control Strategy Table (Step 2.2)
- Motor Efficiency Summary Table (Step 3.3)
- Solar-Ready Provisions Summary Table (Step 4.4)
- Metering Architecture Table (Step 5.2)
- Solar conduit schematic and one-line diagram — in DEL-02-05

**Review and Approval Records:**
- Internal Technical Review Checklist (Step 7.1) — completed by Electrical Lead
- Cross-Discipline Coordination Confirmation (Step 7.2) — written confirmation from DEL-02-05, DEL-04-01, DEL-04-02 authors
- Proposal Integration Memo (Step 7.3) — from Design Manager
- Owner Coordination Decision Log (Step 7.4 — if applicable)
- Sign-Off Documentation (Step 7.5) — Electrical Engineer + Electrical Lead + Design Manager

**Source Citations (embedded in narrative):**
- Addendum 03 — solar-ready requirements
- OSR (Appendix A) — Owner energy efficiency expectations
- Functional Program (Appendix B) — space types and occupancy
- DEL-02-05 (Electrical/IT Concept) — lighting plan, control schematic, one-line diagram, solar conduit routing
- DEL-04-01 (Building Envelope) — daylighting zones and window locations
- DEL-04-02 (Mechanical Energy) — HVAC motors, solar thermal/PV strategy

---

## Notes

- **Scheduling:** Steps 2–5 should begin as soon as DEL-02-05, DEL-04-01, and DEL-04-02 drafts are available. Step 6 assembly and Step 7 review require those deliverables to be at minimum draft-stable. Coordinate timing with Design Manager.
- **TBD priorities:** Owner preferences on BMS integration and metering granularity (Step 5.4) should be resolved early to avoid narrative rework. If Owner input is not available before proposal deadline, default to moderate sub-metering (4–5 zone meters, Modbus-ready) and document as ASSUMPTION.
- **Addendum 03 compliance:** Solar-ready provisions (Step 4) are the highest-priority non-negotiable element. This section must be complete and clearly written even if other narrative sections contain TBD items.
- **Cold Storage:** Cold Storage building electrical provisions are simple (safety/task lighting, minimal outlets). Motor efficiency standard applies to any Cold Storage HVAC or ventilation equipment (if any); confirm with Mechanical Engineer via DEL-04-02.
- **Code-edition resolution (per Lensing item A-003):** Multiple code editions are currently marked as ASSUMPTION (NECB 2020, IES current edition, CEC Part I, Alberta Building Code). These must be confirmed with AHJ or formally deferred with escalation path before narrative finalization. Step 7.1 includes a dedicated check for this.
- **IP rating clarification (per Lensing item E-002):** Apparatus bay IP ratings are differentiated: IP54 for general bay areas, IP65 for designated wash-down zones with bay sumps. Confirm zone boundaries with Electrical Lead during Step 2.1 fixture selection.
