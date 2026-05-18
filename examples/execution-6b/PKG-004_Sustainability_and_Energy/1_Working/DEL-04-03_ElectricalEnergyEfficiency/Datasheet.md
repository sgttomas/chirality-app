# Datasheet — DEL-04-03: Electrical Energy Efficiency

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-04-03 |
| **Deliverable Name** | Electrical Energy Efficiency |
| **Package** | PKG-004 — Sustainability & Energy |
| **Discipline** | Electrical Engineering |
| **Type** | Sustainability / Narrative |
| **Responsible Party** | Electrical Engineer |
| **Supports Objectives** | OBJ-004 (Design Brief, 5 pts) |
| **Covers Scope Items** | SOW-0012 |
| **RFP Reference** | RFP §7.1.2(5) (Electrical/IT sub-brief); energy narrative per SOW-0012 |
| **Version** | Pass 3 (Semantic Lensing Enrichment) |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Artifact type** | Narrative document — prose with supporting tables and diagrams | _CONTEXT.md |
| **Authoring discipline** | Electrical Engineer | _CONTEXT.md |
| **Primary submission section** | Section 7 (Technical Proposal) — Design Brief (electrical sub-brief content); PKG-004 sustainability narrative | RFP §7.1.2; Decomposition §8 (PKG-004 goal) |
| **Evaluation weight** | Contributes to Design Brief score (5 pts total for OBJ-004); sustainability content supports PKG-004 goal | Decomposition §6, §15 |
| **Project type** | Combined Fire Hall + Public Works Operations facility; main building 50-year design life; Cold Storage 20-year unheated | Decomposition §1, §9 (DEL-04-03 context) |
| **Solar-ready requirement** | Solar-capable roofing required; orientation flat, south, west, or southwest; electrical provisions required (conduit, panel space, inverter location) | Addendum 03 (location TBD within Addendum 03 document) |
| **Lighting standard** | LED per IES recommendations (specific edition TBD by Electrical Engineer; baseline assumption: IES Lighting Handbook, 10th Edition or current at time of design) | _CONTEXT.md; Decomposition DEL-04-03 description; edition clarification per Lensing item A-001 |
| **Motor efficiency standard** | NEMA Premium Efficiency / CSA C390 equivalent (IE3 category minimum) | ASSUMPTION — standard practice for municipal facilities; canonical reference: CSA C390 (IE3 category) as the Canadian-applicable standard, with NEMA Premium as the procurement-equivalent designation; confirm with Electrical Lead (see Lensing item C-002) |
| **Primary code framework** | NECB 2020 (National Energy Code of Canada for Buildings) or as confirmed by AHJ; Alberta Building Code (which adopts NECB with provincial amendments — relationship TBD; confirm whether ABC imposes energy-specific amendments beyond NECB) | ASSUMPTION — NECB 2020 assumed as baseline edition pending AHJ confirmation; Alberta Building Code relationship to NECB TBD (see Lensing items A-001, F-001) |
| **Cross-references** | DEL-02-05 (Electrical/IT Concept), DEL-04-01 (Building Envelope), DEL-04-02 (Mechanical Energy) | _REFERENCES.md |

---

## Conditions

| Condition | Description | Source |
|---|---|---|
| **Climate zone** | Penhold, Alberta — cold climate (high heating degree days); significant winter lighting demand due to short daylight hours; freeze-thaw cycles affect outdoor equipment | ASSUMPTION — Alberta cold climate, Penhold confirmed location |
| **Building operational profile** | Fire hall operates 24/7; Public Works operates typical business hours; shared spaces (ICP/meeting room, training, offices) mixed occupancy; occupancy profile drives lighting control strategy | Decomposition §4 (Addendum 03 clarifications); DEL-02-04 description |
| **Apparatus bay environment** | High-bay space; vehicle traffic; combustion residues; periodic wash-down; overhead doors (16 ft minimum per Addendum 03); bay sumps; requires robust sealed luminaires and appropriate control strategy | Addendum 03 (location TBD); Decomposition §4 |
| **Solar-ready provision trigger** | Addendum 03 explicitly requires solar-capable roofing; electrical rough-in for future PV is a direct baseline requirement, not an optional value-add | Addendum 03 (location TBD); Decomposition §4 |
| **Generator electrical interface** | Standby diesel generator required minimum: kitchen, ICP meeting room, 2 bathrooms, bay door secondary opening; electrical metering and circuit design must account for generator-backed sub-circuits | Addendum 03 §1.15 (location TBD); Decomposition DEL-02-04 |
| **Motor loads** | Public Works bay includes workshop equipment; HVAC fans and pumps throughout; direct apparatus bay exhaust fans (2 apparatus per bay); bunker gear room ventilation; motor efficiency standard applies to all rotating equipment | Addendum 03 (location TBD); Decomposition DEL-02-04 description |
| **Budget and value context** | Municipal owner (Town of Penhold); lifecycle cost efficiency valued; capital cost discipline expected; efficiency investments must be justifiable on TCO basis | Decomposition §1; OBJ-007 (price, 35 pts) |
| **Cold Storage exclusion** | Cold Storage building (60'×100') is unheated equipment storage; 20-year design life; electrical provisions are minimal — lighting and outlet circuits only | ASSUMPTION — unheated Cold Storage does not warrant advanced lighting controls; confirm with Electrical Lead |
| **Cold Storage electrical load summary** | Estimated connected load: TBD; number of circuits: TBD; lighting fixture count estimate: TBD; no advanced controls anticipated; cold-rated LED fixtures (-40C) required | ASSUMPTION — Cold Storage load data to be populated from DEL-02-05 electrical design; included for completeness per Lensing item B-002. Source: Guidance C-EEE-03; Procedure Step 2.1 |

---

## Construction (Scope of Document)

The electrical energy efficiency narrative encompasses five discrete content elements, each produced by the Electrical Engineer and integrated into the proposal:

| Element | Description | Coordination |
|---|---|---|
| **LED Lighting Design** | Zone-by-zone lighting selection per IES recommendations; lumen targets, color temperature, CRI, and efficacy by space type (apparatus bay, office, residential quarters, shared spaces, Cold Storage, exterior) | DEL-02-05 (detailed lighting schedule); DEL-04-01 (daylighting availability) |
| **Lighting Controls** | Occupancy sensing (PIR or ultrasonic), daylight harvesting (photosensor at perimeter/daylit zones), time-of-day scheduling, zone control logic by occupancy type; control system architecture | DEL-04-01 (daylight zones); DEL-02-05 (control schematic) |
| **Motor Efficiency Standards** | Selection criteria for HVAC fans, pumps, exhaust fans, and other rotating equipment; NEMA Premium or IE3 equivalent; Variable Frequency Drives (VFDs) where load varies | DEL-04-02 (motor sizes and types); DEL-02-05 (motor control centers) |
| **Solar-Ready Electrical Provisions** | Conduit pathways from roof to electrical room; panel space reserved for future inverter/combiner; dedicated breaker space; inverter location designated; orientation rationale (flat/south/west/southwest per Addendum 03); documentation for future integration | DEL-04-02 (solar thermal/PV strategy); DEL-02-05 (one-line diagram, conduit routing) |
| **Electrical Metering and Sub-Metering** | Main service metering; sub-metering for major operational zones (apparatus bay vs. PW bay vs. office/admin vs. shared mechanical); generator circuit accounting; integration path for future energy monitoring system | DEL-02-05 (distribution panel layout); DEL-04-02 (BMS/energy monitoring coordination) |

---

## References

| Reference | Role in this Deliverable | Accessibility |
|---|---|---|
| RFP 2024_004 (AB-2024-07156) — OSR (Appendix A) | Primary requirements document including Owner Statement of Requirements with energy efficiency expectations | Per _REFERENCES.md |
| Addendum 03 (Jul 31, 2024) | Solar-capable roof requirement; solar-ready electrical provisions (conduit, panel space, inverter location); 16 ft overhead doors (bay lighting implications) | Per _REFERENCES.md |
| DEL-02-05 (Electrical/IT Concept Narrative) | Upstream electrical concept — power distribution, lighting approach, conduit routing, one-line diagram alignment | Cross-reference per _REFERENCES.md |
| DEL-04-01 (Building Envelope and Energy Strategy) | Daylighting availability, window and skylight locations, solar roof orientation — inputs for daylight harvesting and solar conduit placement | Cross-reference per _REFERENCES.md |
| DEL-04-02 (Mechanical Energy and Solar Readiness) | HVAC motor types and sizes, solar thermal/PV strategy coordination, generator load confirmation | Cross-reference per _REFERENCES.md |
| IES (Illuminating Engineering Society) standards | Lighting level recommendations by space type (lux targets, fixture selection) | ASSUMPTION — accessible by Electrical Engineer; specific edition TBD |
| NECB 2020 (National Energy Code of Canada for Buildings) | Lighting power density limits, motor efficiency baseline requirements, energy performance framework | ASSUMPTION — NECB 2020 assumed pending AHJ confirmation; edition per Lensing item A-001 |
| Alberta Building Code | Provincial modifications to National Building Code including electrical provisions; relationship to NECB TBD (adoption pathway or separate code — see Lensing item F-001) | ASSUMPTION — applicable; edition TBD |
| CSA C390 / NEMA Premium Efficiency (IE3 category) | Motor efficiency classification and procurement specifications; canonical Canadian reference is CSA C390 (IE3); NEMA Premium is procurement-equivalent designation | ASSUMPTION — applicable; confirm with Electrical Lead per Lensing item C-002 |
