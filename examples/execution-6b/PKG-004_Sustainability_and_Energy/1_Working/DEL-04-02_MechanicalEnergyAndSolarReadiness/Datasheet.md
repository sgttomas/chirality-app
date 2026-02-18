# Datasheet — DEL-04-02: Mechanical Energy and Solar Readiness

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-04-02 |
| **Deliverable Name** | Mechanical Energy and Solar Readiness |
| **Package** | PKG-004 — Sustainability & Energy |
| **Deliverable Type** | Sustainability / Narrative |
| **Responsible Party** | Mechanical Engineer |
| **Scope Item Coverage** | SOW-0012 (Sustainability/energy narrative) |
| **Objective Alignment** | OBJ-004 (Design Brief, 5 pts) — ASSUMPTION: best-effort mapping via PKG-004 package heuristic; confirmed by decomposition §9 DEL-04-02 entry |
| **RFP Section** | Section 7.1.2 (Design Brief — mechanical discipline sub-brief) |
| **Anticipated Artifact** | Mechanical energy efficiency and solar-readiness narrative |
| **Document Status** | INITIALIZED |
| **Date** | 2026-02-17 |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Building Type** | Combined Fire Hall + Public Works Operations facility (main building); Cold Storage (60'x100', unheated equipment storage) | Decomposition §1 |
| **Main Building Design Life** | 50 years | Decomposition §6 OBJ-005 |
| **Cold Storage Design Life** | 20 years | Decomposition §6 OBJ-005 |
| **Site Location** | Lot 1, Block 1, Plan 212 1668, Waskasoo Avenue North, Penhold, Alberta | Decomposition §1 |
| **Climate Zone** | Alberta, Canada — cold, heating-dominated climate; ASSUMPTION: Penhold is in NECB Climate Zone 7A or similar; ASSUMPTION: heating design temperature approximately -33 C (ASHRAE 99% heating design, central Alberta); ASSUMPTION: heating degree-days approximately 5500-6000 HDD (base 18 C) for Penhold/Red Deer area; cooling design temperature TBD at detailed design | ASSUMPTION based on project location; climate data values are ASSUMPTION pending confirmation from ASHRAE Fundamentals for Penhold/Red Deer station |
| **Energy Code Pathway** | NECB (National Energy Code of Canada for Buildings); ASSUMPTION: NECB 2020 as adopted by Alberta is the most likely applicable edition; specific provincial adoption and any Alberta-specific amendments TBD at detailed design | Decomposition SOW-0012; ASSUMPTION: NECB 2020 applicable for Alberta commercial buildings |
| **Solar-Ready Roof Requirement** | Required; orientation must be flat, south, west, or southwest | Addendum 03 §1 (solar-capable roofing); Decomposition §4 Addendum 03 summary |
| **Solar Technology (Future)** | Future solar PV or solar thermal — Owner decision deferred; base design provides rough-in only | Decomposition DEL-04-02 description |
| **Mechanical Energy Focus Areas** | High-efficiency HVAC equipment; heat recovery; ventilation energy optimization; domestic hot water efficiency; solar-ready provisions; energy metering and monitoring | Decomposition DEL-04-02 description |
| **Audience** | RFP evaluation committee — Section 7 scored criteria (Design Brief sub-criterion) | Decomposition §6 OBJ-004 |
| **Narrative Length (Target)** | 2–4 pages — ASSUMPTION: consistent with Design Brief sub-brief scope expectations | ASSUMPTION |

---

## Conditions

| Condition | Description | Source |
|---|---|---|
| **Fire Apparatus Bay Ventilation** | Direct exhaust ventilation required; 2 apparatus per bay; energy recovery is constrained by vehicle exhaust contamination | Addendum 03 §1; Decomposition §4 |
| **PW Bay Ventilation** | General dilution ventilation for occasional vehicle idling and very occasional welding; no dedicated welding ventilation required | Addendum 03 §1; Decomposition §4 |
| **Bunker Gear Room** | Room-level ventilation required (drying and odour control); 40 bunker gear lockers with ventilated storage | Addendum 03 §1; Decomposition §4 |
| **Cold Storage — Unheated (Scope Exclusion)** | Cold Storage building (60'x100') is intentionally unheated and is **excluded from the scope of this mechanical energy narrative**; no active mechanical energy systems apply; freeze-thaw cycling is the primary durability driver there. See Specification.md "What This Deliverable Excludes" for the formal scope boundary. | Decomposition DEL-05-01 description; Specification.md scope exclusion; ASSUMPTION: no active mechanical energy systems in Cold Storage |
| **Backup Generator** | Diesel standby generator required; minimum loads = kitchen, ICP/meeting room, 2 bathrooms, bay door secondary opening; generator fuel and energy interact with overall energy budget | Addendum 03 §1; Decomposition §4 and DEL-02-04 |
| **Fill Stations** | Two 2" water fill stations (1 fire apparatus bay, 1 PW bay); DHW system must be sized to support operational fill station demands if warm-water service required — TBD | Addendum 03 §1; Decomposition §4 |
| **Bay Sumps** | Required in all bays for snow melting and minor washing; sump heating energy is a design consideration if sumps are actively heated | Addendum 03 §1; Decomposition §4 |
| **Roof Orientation Constraint** | Roof orientation for solar-readiness must be flat, south, west, or southwest; actual building orientation is determined by site plan (DEL-02-01/DEL-02-02) | Addendum 03 §1 |
| **Envelope-HVAC Interdependence** | Mechanical heating/cooling loads are directly driven by envelope thermal performance (DEL-04-01); HVAC sizing and equipment selection must be consistent with envelope U-value targets | Decomposition DEL-04-01 and DEL-04-02 relationship |
| **Operational Profile** | 24/7 facility overall; zone-by-occupancy schedule below. See Guidance.md P-001 for zone-specific energy strategies aligned to these profiles. | Decomposition §4; Functional Program (Appendix B) — location TBD; Guidance.md P-001 |

**Zone-Occupancy Schedule (ASSUMPTION: to be confirmed from Functional Program, Appendix B)**

| Zone | Occupancy Schedule | Conditioning Requirement | Exhaust Type |
|---|---|---|---|
| Fire apparatus bays | 24/7 (standby + response events) | Intermittent high-demand; overhead door infiltration events | Direct exhaust (Addendum 03) |
| Public Works bays | Business hours; intermittent vehicle idling | Intermittent; DCV-controlled | General exhaust (Addendum 03) |
| Offices / administrative | Business hours (~8-10 hrs/day, weekdays) | Standard HVAC with setback scheduling | Standard return air |
| Residential quarters | 24/7 continuous | Continuous conditioning; ERV/HRV | Dedicated exhaust with heat recovery |
| Shared spaces (kitchen, ICP/meeting, training) | Variable; kitchen daily, training/meeting intermittent | Variable; kitchen requires dedicated makeup air | Kitchen: dedicated exhaust; others: standard |
| Bunker gear room | 24/7 continuous (drying/odour control) | Continuous ventilation | Dedicated exhaust (clean or contaminated TBD) |

---

## Construction (Narrative Content Elements)

| Content Element | Description | Status |
|---|---|---|
| **HVAC Zone Strategy** | Zone-specific approach for apparatus bays, PW bays, office/admin, residential quarters, shared spaces (kitchen, ICP/meeting room, training); equipment type and efficiency rationale per zone | TBD at narrative drafting; framework documented in Guidance.md |
| **High-Efficiency Equipment Selection** | Heating/cooling equipment with indicative efficiency targets: heating AFUE 95%+ (condensing boilers/furnaces) or COP 3.0-4.5 (air-source heat pumps); cooling SEER 16-18+; DHW EF 0.92 minimum (NECB) targeting 0.95+ or heat pump water heater COP 2.5-3.5. Selection rationale based on climate, occupancy, operational resilience. All targets are ASSUMPTION pending confirmation at detailed design per NECB edition in effect. See Guidance.md P-003 for rationale. | ASSUMPTION: indicative targets per Guidance.md P-003; to be confirmed at detailed design per NECB edition |
| **Heat Recovery — Ventilation** | HRV or ERV for conditioned occupied spaces (residential quarters, offices); not applicable to apparatus bay direct exhaust due to contamination; heat pipe or specialized HRV on PW bay general exhaust if feasible | TBD; applicability depends on final HVAC design |
| **Heat Recovery — DHW** | Solar thermal preheat rough-in or heat pump water heater for DHW efficiency | TBD; rough-in provisions are base-design scope |
| **Ventilation Energy Optimization** | Demand-controlled ventilation (DCV) via CO/CO2 sensors in PW bays; scheduled setback in office/administrative zones; HRV recovery in residential and shared zones | TBD; ASSUMPTION: DCV applicable in PW bays per Addendum 03 general ventilation requirement |
| **Domestic Hot Water** | High-efficiency DHW system (condensing gas water heater, heat pump water heater, or solar thermal preheat + efficient backup — TBD); insulated distribution piping; recirculation pump where justified | TBD at detailed design |
| **Solar Readiness — Structural** | Roof structure provisions for future PV or solar thermal panel dead load; coordinated with DEL-02-03 (structural concept) | TBD; load magnitude confirmed at detailed design |
| **Solar Readiness — Mechanical Rough-In** | Pipe sleeves, conduit pathways, or chase-ways from roof to mechanical room for future solar thermal loop piping; isolation provisions in mechanical room | Required per Addendum 03 (solar-capable); details TBD |
| **Solar Readiness — Orientation** | Flat/south/west/southwest per Addendum 03; rationale for chosen orientation relative to site plan | Required; orientation confirmed at architectural/civil concept (DEL-02-01, DEL-02-02) |
| **Energy Metering** | Utility-grade whole-building energy meter (electricity + gas); sub-metering provisions for major energy consumers (apparatus bay HVAC, DHW, office/residential HVAC) | TBD; scope of sub-metering TBD at detailed design |
| **Energy Monitoring / Controls** | Building energy management system (BEMS) or equivalent controls provisions for monitoring and operational optimization | TBD; ASSUMPTION: BEMS or equivalent controls are industry-standard for facility of this type |
| **Energy Code Compliance** | NECB compliance pathway (prescriptive or performance-based); efficiency target statement relative to NECB baseline | TBD; pathway selection at detailed design |

---

## References

| Reference | Description | Accessibility |
|---|---|---|
| RFP 2024_004 | Base RFP — SOW-0012 (sustainability/energy); Section 7.1.2 (Design Brief); OSR (Appendix A) energy requirements | Accessible |
| Addendum 03 (Jul 31, 2024) | Solar-capable roofing requirement; roof orientation (flat/south/west/southwest); apparatus bay direct exhaust; PW bay general ventilation; fill stations; sumps; generator | Accessible |
| Decomposition v2.3 FINAL | DEL-04-02 description; PKG-004 scope; SOW-0012; Addendum 03 integration summary; OBJ-004 | Accessible |
| OSR (Appendix A) | Owner Statement of Requirements — energy/sustainability clauses | Referenced; full text accessibility TBD |
| Functional Program (Appendix B) | Room sizing, equipment lists, operational profile | Referenced; full text accessibility TBD |
| DEL-02-04 (Mechanical Concept Narrative) | Upstream mechanical concept — HVAC, ventilation, generator, plumbing; energy narrative must align with and justify concept choices | Cross-reference (PKG-002) |
| DEL-04-01 (Building Envelope and Energy Strategy) | Envelope thermal performance targets; loads that drive mechanical sizing | Cross-reference (sibling in PKG-004) |
| DEL-04-03 (Electrical Energy Efficiency) | Solar-ready electrical provisions (conduit, panel space, inverter location); must be coordinated with mechanical solar rough-in | Cross-reference (sibling in PKG-004) |
| DEL-05-03 (Mechanical Maintainability) | Mechanical systems maintainability strategy; energy-efficient systems must be maintainable | Cross-reference (PKG-005) |
| NECB (National Energy Code of Canada) | Energy code compliance pathway; edition TBD | ASSUMPTION: applicable; specific edition TBD |
| ASHRAE 62.1 | Ventilation for acceptable indoor air quality — apparatus bay, PW bay, bunker gear room ventilation | ASSUMPTION: likely applicable; clause-level requirements TBD |
| ASHRAE 90.1 | Energy standard — reference for efficiency targets where NECB prescriptive is insufficient | ASSUMPTION: likely applicable as reference; clause-level requirements TBD |
