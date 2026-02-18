# Specification — DEL-04-03: Electrical Energy Efficiency

---

## Scope

### In Scope

- Electrical energy efficiency narrative for the Public Services Building (main building, 50-year design life) and Cold Storage building (20-year design life), as applicable per building type
- LED lighting design methodology and fixture selection per IES recommendations, by space type
- Lighting control strategy covering occupancy sensing, daylight harvesting, and time-of-day scheduling
- Motor efficiency standards application for all rotating electrical equipment (HVAC fans, pumps, exhaust fans, compressors)
- Solar-ready electrical provisions: conduit rough-in, panel space allocation, and inverter location per Addendum 03 requirements
- Electrical metering and sub-metering strategy for major operational zones
- Cross-discipline coordination documentation with DEL-02-05 (Electrical/IT Concept), DEL-04-01 (Building Envelope), and DEL-04-02 (Mechanical Energy)

### Out of Scope

- Detailed electrical design drawings (produced in DEL-02-05 Electrical/IT Concept)
- Mechanical energy efficiency narrative (DEL-04-02)
- Building envelope thermal performance (DEL-04-01)
- Actual photovoltaic (PV) system design or solar energy system specification (future Owner decision; this deliverable covers electrical rough-in only)
- Construction methodology or on-site electrical installation procedures (PKG-007)
- Electrical systems maintainability strategy (DEL-05-04, PKG-005)
- IT/telecommunications infrastructure (DEL-02-05 and DEL-03-05)

---

## Requirements

### R-EEE-01: LED Lighting Design per IES Recommendations

**Statement:** The narrative shall describe an LED lighting design strategy based on IES recommendations, covering all major space types in the Public Services Building.

**Rationale:** LED technology meets energy efficiency and lifecycle cost targets for a 24/7 municipal emergency services facility. IES provides recognized, defensible lighting level standards appropriate to space function.

**Source:** _CONTEXT.md (DEL-04-03 description: "LED lighting design per IES recommendations"); Decomposition DEL-04-03 entry; SOW-0012.

**Verification:** Narrative includes space-type lighting schedule with IES methodology documented; lux/illuminance targets stated for critical operational areas (apparatus bays, duty areas, offices); fixture efficacy (lm/W) confirmed for LED selections; NECB Lighting Power Density (LPD) limit targets (W/m2) stated for each major zone type to enable compliance verification (per Lensing item B-001; LPD values TBD — source from NECB 2020 or as confirmed by AHJ).

**Note (Cold Storage):** Cold Storage building lighting provisions shall be explicitly addressed in the narrative, including zone-specific verification that cold-rated LED fixtures and appropriate controls are specified for the 20-year unheated building. (Per Lensing item D-001; source: Guidance C-EEE-03, Procedure Step 2.1.)

---

### R-EEE-02: Occupancy-Based Lighting Controls

**Statement:** The narrative shall specify occupancy-based (motion or presence sensing) lighting controls for areas with variable or intermittent occupancy patterns.

**Rationale:** Reduces energy consumption in intermittently used spaces — conference rooms, storage areas, bathrooms, training rooms — which are common in combined fire hall and public works facilities.

**Source:** _CONTEXT.md (DEL-04-03 description: "lighting controls (occupancy, daylight harvesting, scheduling)"); Decomposition DEL-04-03 entry.

**Verification:** Narrative identifies which spaces receive occupancy controls, sensor technology selected with justification per zone characteristics (bay height, temperature range, occupancy pattern), placement strategy, and expected energy reduction.

---

### R-EEE-03: Daylight Harvesting Controls

**Statement:** The narrative shall integrate daylight harvesting controls in spaces where daylighting is available, coordinated with DEL-04-01 (Building Envelope and Energy Strategy).

**Rationale:** Maximizes use of natural light in perimeter and roof-lit spaces, reducing artificial lighting energy during daytime hours — particularly relevant for shared spaces and offices given Alberta's summer daylight hours.

**Source:** _CONTEXT.md (DEL-04-03 description: "daylight harvesting"); _REFERENCES.md (DEL-04-01 cross-reference for daylighting coordination).

**Verification:** Narrative describes daylight harvesting approach, identifies spaces with daylight potential, confirms coordination with DEL-04-01 for window and skylight locations and photosensor placement.

---

### R-EEE-04: Time-of-Day Scheduling Controls

**Statement:** The narrative shall specify scheduling-based lighting controls for areas with predictable occupancy or operational patterns.

**Rationale:** Emergency services operate 24/7 but with identifiable shift patterns; Public Works operates on business-hour schedules; scheduling avoids wasted energy in unoccupied periods without requiring manual intervention.

**Source:** _CONTEXT.md (DEL-04-03 description: "scheduling"); Decomposition §4 (operational profile: 24/7 fire operations, business-hour PW).

**Verification:** Narrative documents scheduling approach and identifies key operational time zones (fire apparatus bay 24/7, office/admin business hours, training room as-scheduled); explains how schedule accounts for shift-based operations.

---

### R-EEE-05: Motor Efficiency Standards

**Statement:** The narrative shall specify application of a recognized motor efficiency standard for all rotating electrical equipment, including HVAC fans, circulation pumps, exhaust fans, and compressors.

**Rationale:** Motors represent a significant fraction of building electrical load; premium efficiency motors deliver lower lifecycle energy cost with modest upfront premium, consistent with 50-year building design life.

**Source:** _CONTEXT.md (DEL-04-03 description: "motor efficiency standards"); Decomposition DEL-04-03 entry.

**Verification:** Narrative identifies motor categories and confirms efficiency standard applied (CSA C390 / NEMA Premium Efficiency, IE3 category minimum — see canonical terminology in Datasheet); coordination with DEL-04-02 documented for motor sizing and type inputs.

**Note:** Canonical motor efficiency reference is CSA C390 (IE3 category) as the Canadian-applicable standard, with NEMA Premium as procurement-equivalent designation — ASSUMPTION; confirm with Electrical Lead and align with DEL-04-02 mechanical equipment selections (per Lensing item C-002).

**VFD Application:** For motors serving variable-load applications (supply/return fans, circulation pumps), the narrative shall specify Variable Frequency Drive (VFD) application as the baseline approach. VFDs are standard mandatory practice for energy efficiency on variable-load rotating equipment in municipal facilities. Coordination with DEL-04-02 required for motor sizing confirmation. **ASSUMPTION** — VFD application is standard practice for variable-load motors; confirm mandatory framing with Electrical Lead (per Lensing item A-002). Source: Procedure Step 3.2 (VFD recommendations); Specification R-EEE-05 (motor efficiency standards).

---

### R-EEE-06: Solar-Ready Electrical Provisions (Addendum 03 Requirement)

**Statement:** The narrative shall describe solar-ready electrical infrastructure for potential future photovoltaic (PV) installation, specifically:
- (a) Conduit rough-in from roof to electrical room (or designated inverter location);
- (b) Dedicated panel space in main electrical panel(s) for future solar disconnect, inverter breaker, and interconnection equipment;
- (c) Pre-identified inverter location (roof-mounted, wall-mounted, or other, per design approach);
- (d) Documentation of solar conduit routing and panel space reservation for future integration.

**Rationale:** Addendum 03 explicitly requires solar-capable roofing with flat, south, west, or southwest orientation and solar-ready electrical provisions. Rough-in during initial construction avoids costly rework if Owner adds PV in the future; this is a compliance requirement, not an optional value-add.

**Source:** Addendum 03 (location TBD within Addendum 03 document); _CONTEXT.md ("solar-ready electrical provisions (conduit, panel space, inverter location for future PV per Addendum 03)"); _REFERENCES.md ("Addendum 03: Solar-capable roof provisions"); Decomposition §4 ("Solar-capable roofing required; orientation: flat, south, west, or southwest").

**Verification:**
- Narrative describes conduit routing path (roof to electrical room), conduit size assumption, and pull box locations;
- Panel space reservation is explicitly called out in main panel design (DEL-02-05);
- Inverter location identified with rationale;
- Coordination with DEL-04-02 (mechanical solar provisions) and DEL-02-05 (electrical one-line diagram) documented.

---

### R-EEE-07: Electrical Metering and Sub-Metering Strategy

**Statement:** The narrative shall define an electrical metering approach including sub-metering for major operational zones to support energy accountability and performance monitoring.

**Rationale:** A combined fire hall and public works facility has distinct operational zones with different energy profiles; sub-metering enables department-level cost allocation, equipment performance tracking, and anomaly detection — best practice for multi-tenant municipal facilities.

**Source:** _CONTEXT.md (DEL-04-03 description: "electrical metering and sub-metering strategy"); Decomposition DEL-04-03 entry.

**Verification:** Narrative describes metering architecture (main meter plus sub-meters), identifies major operational zones receiving sub-metering (minimum: fire apparatus bays, PW bays, office/administrative zone, shared mechanical spaces), specifies meter type or technology, and describes operational benefits and integration path for future building management system (BMS) connection.

---

### R-EEE-08: Canadian Electrical Code (CEC) Part I Compliance

**Statement:** The narrative shall address CEC Part I compliance as it relates to the energy efficiency narrative, including metering provisions, wiring methods for sub-metering circuits, and service entrance provisions that support the metering and solar-ready strategies described in R-EEE-06 and R-EEE-07.

**Rationale:** CEC Part I is listed in the Standards table and Procedure Prerequisites but had no corresponding Specification requirement. The regulatory imperative for wiring compliance applicable to metering, solar conduit, and service entrance provisions is a necessary part of the energy efficiency narrative's normative foundation.

**Source:** Specification Standards table (CEC Part I listed); Procedure Prerequisites (CEC Part I listed); Lensing item C-001.

**Verification:** Narrative confirms CEC Part I wiring methods are addressed for metering circuits and solar conduit provisions; service entrance provisions noted as applicable.

---

### R-EEE-09: Emergency/Egress Lighting Energy Efficiency

**Statement:** The narrative shall address the energy efficiency approach for emergency and egress lighting, including LED emergency fixtures and generator-backed lighting circuit design, as distinct from general area lighting.

**Rationale:** The Public Services Building is a 24/7 fire hall where emergency egress lighting reliability is a primary design constraint (Guidance P-EEE-01). Generator-backed sub-circuits are required for critical loads (Addendum 03). The energy efficiency approach for these always-on or standby circuits is a substantive design consideration distinct from general lighting and warrants explicit treatment in the narrative.

**Source:** Guidance P-EEE-01 (emergency egress lighting reliability); Datasheet Conditions (generator electrical interface, generator-backed sub-circuits); Lensing item D-002.

**Verification:** Narrative identifies emergency/egress lighting as a distinct category; LED emergency fixture approach described; energy efficiency of generator-backed lighting circuits addressed.

---

## Standards

| Standard / Code | Applicability | Status |
|---|---|---|
| IES Lighting Design Guidelines (current edition) | LED fixture selection; lux targets by space type; control system design | ASSUMPTION — applicable; specific edition TBD by Electrical Engineer |
| NECB (National Energy Code of Canada for Buildings) | Lighting Power Density (LPD) limits; energy performance compliance pathway; motor efficiency baseline | ASSUMPTION — applicable to Alberta new construction; edition TBD by AHJ |
| Alberta Building Code | Provincial modifications to national code; local electrical and energy requirements | ASSUMPTION — applicable; edition TBD |
| CSA C390 / NEMA Premium Efficiency (IE3 category) | Motor efficiency classification and procurement specification; canonical Canadian reference is CSA C390 (IE3 category); NEMA Premium is procurement-equivalent designation (per Lensing item C-002) | ASSUMPTION — applicable; confirm with Electrical Lead |
| Canadian Electrical Code (CEC) Part I | Electrical system design, wiring methods, service entrance, metering | ASSUMPTION — applicable; edition TBD |
| RFP Owner Statement of Requirements (Appendix A — OSR) | Owner's energy efficiency expectations; any Owner-specific standards or preferences | Per _REFERENCES.md; specific requirements TBD from OSR text |

---

## Verification

| Requirement | Verification Method | Timing |
|---|---|---|
| **R-EEE-01: LED Lighting Design** | Review lighting narrative for IES methodology; check lighting schedule for major space types; confirm fixture efficacy (lm/W) documented | Design Development phase; prior to proposal finalization |
| **R-EEE-02: Occupancy Controls** | Review control strategy narrative; confirm coverage of variable-occupancy spaces; validate against DEL-02-05 floor plan (sensor placement); **confirm sensor technology selection (PIR vs. ultrasonic vs. dual-technology) is justified per zone characteristics** (bay height, temperature range, occupancy pattern — per Lensing item X-002) | Design Development phase |
| **R-EEE-03: Daylight Harvesting** | Review narrative; confirm coordination with DEL-04-01 (daylighting zones confirmed); validate photosensor placement feasibility in concept drawings | Upon DEL-04-01 draft availability |
| **R-EEE-04: Scheduling Controls** | Review narrative; confirm alignment with operational schedule (24/7 fire; business-hour PW/admin); validate with Functional Program occupancy assumptions | Design Development phase |
| **R-EEE-05: Motor Efficiency** | Review motor category list from DEL-04-02; confirm efficiency standard applied and documented; verify procurement specification clarity | Upon DEL-04-02 motor schedule availability |
| **R-EEE-06: Solar-Ready Provisions** | Review narrative for conduit routing, panel space, and inverter location; confirm all three elements (conduit, space, location) addressed; check coordination with DEL-02-05 one-line diagram and DEL-04-02 solar strategy | Upon DEL-02-05 concept drawing availability |
| **R-EEE-07: Metering Strategy** | Review metering narrative for main meter plus sub-meter architecture; confirm major operational zones identified (minimum 4 zones — per Procedure Step 5.2 which specifies 5 zones); confirm meter communication protocol requirement stated (Modbus or equivalent — per Procedure Step 5.2); verify BMS integration path described (per Lensing item X-001) | Design Development phase |
| **R-EEE-08: CEC Part I Compliance** | Review narrative for CEC Part I wiring method references applicable to metering circuits and solar conduit; confirm service entrance provisions noted | Design Development phase |
| **R-EEE-09: Emergency/Egress Lighting** | Review narrative for distinct treatment of emergency/egress lighting; confirm LED emergency fixture approach described; verify generator-backed lighting circuit energy efficiency addressed | Design Development phase |
| **Cross-Discipline Sign-Off** | Confirm that DEL-02-05, DEL-04-01, and DEL-04-02 authors have provided written sign-off on cross-discipline coordination content within this narrative (per Lensing item X-004; currently described in Procedure Step 7.2 but owned here as a formal verification requirement) | Prior to proposal finalization |
| **Overall Energy Reduction Threshold** | Narrative shall include an estimated kWh reduction summary or demonstrate minimum percentage reduction vs. code baseline for electrical energy (quantitative or qualitative acceptance threshold TBD by Electrical Engineer / Design Manager — per Lensing item X-003) | Prior to proposal finalization |

---

## Documentation

**Anticipated Deliverable Artifacts:**

1. **Primary:** Electrical Energy Efficiency Narrative (6–10 pages) — prose narrative covering all nine requirements (R-EEE-01 through R-EEE-09), with supporting tables (lighting schedule, motor specifications, metering architecture) and schematic references to DEL-02-05.

2. **Supporting content embedded in or referenced from the narrative:**
   - Lighting schedule by space type (fixture type, lumen output, CCT, CRI, efficacy)
   - Lighting control strategy table (control type by space, rationale, expected savings)
   - Motor efficiency specification summary (equipment category, standard, cost delta)
   - Solar-ready provisions summary table (conduit, panel space, inverter location)
   - Metering architecture summary (main + sub-meter points and rationale)

3. **Cross-document references:**
   - DEL-02-05 (detailed lighting plan, control schematic, one-line diagram, solar conduit routing)
   - DEL-04-01 (daylighting zone confirmation, solar roof orientation)
   - DEL-04-02 (HVAC motor schedule, solar thermal/PV strategy coordination)
