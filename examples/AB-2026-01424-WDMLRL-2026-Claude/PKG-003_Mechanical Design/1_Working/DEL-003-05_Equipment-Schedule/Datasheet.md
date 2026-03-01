# Datasheet — DEL-003-05 Mechanical Equipment Schedule
**Deliverable ID:** DEL-003-05
**Name:** Mechanical Equipment Schedule
**Package:** PKG-003 Mechanical Design
**Discipline:** Mechanical Engineering
**Type:** Schedule
**Responsible:** Mechanical Engineer
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Location:** SW 14–44–21–W4, near Ferintosh, Alberta
**Contract Form:** CCDC 14–2013 Design-Build Stipulated Price Contract
**Document Date:** 2026-02-25
**Revision:** R1 (Pass 3 enrichment — 2026-02-26)

---

## 1. Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-003-05 |
| Document Title | Mechanical Equipment Schedule |
| Package | PKG-003 — Mechanical Design |
| Parent Scope Item | SOW-0013 (Final mechanical design — HVAC, ventilation, exhaust systems) |
| Supports Objectives | OBJ-003 (IFC design documentation), OBJ-004 (Mechanical/plumbing systems to operational readiness) |
| Prepared By | Mechanical Engineer (role; individual TBD at project award) |
| Reviewed By | TBD |
| IFC Stamp Required | Yes — P.Eng. licensed in Alberta (per RFP §3.3.2, SOW-0018) |
| Status | Scaffold draft — SEMANTIC_READY |

---

## 2. Attributes

### 2.1 Building Parameters Governing Equipment Selection

| Parameter | Value | Source |
|---|---|---|
| Building Type | Industrial maintenance shop addition | RFP §3.1, App B (Shop) |
| Gross Floor Area (Addition) | ~13,000 sq ft (approximately 130' x 100') | RFP §3.1, Decomp Vocabulary Map |
| Ceiling Height (Main Shop) | 35 ft | RFP §3.4, App B (Shop) |
| Number of Repair Bays | 2 drive-through bays, each 24' wide | RFP §3.1, App B (Shop) |
| Wash Bay | 1 enclosed bay, 24' wide, motor-scraper sized | RFP §3.1, §3.4, App B (Shop) |
| Parts Room | ~400 sq ft | RFP §3.4, App B (Shop) |
| Utility Room | Present (dimensions TBD — not stated in RFP) | RFP §3.1, App B (Shop) |
| Office | Present (dimensions TBD — not stated in RFP) | RFP §3.1, App B (Shop) |
| Mezzanine | Above parts room, utility room, and wash bay; load-bearing | RFP §3.4, App B (Shop) |
| Power Supply | Three-phase (voltage/ampacity TBD — electrical design, SOW-0014) | RFP §3.4 |
| Climate Zone | Alberta Central region; near Ferintosh (design heating/cooling values TBD — geotech/climate data) | RFP §1.0 |
| Occupancy / Use | Heavy equipment maintenance; welding; parts storage; office | RFP §3.1, §3.4 |

### 2.2 Mechanical Equipment Register

The following equipment items are identified from RFP §3.4 and Appendix B (Shop). Performance values, model numbers, and manufacturers are TBD pending mechanical engineering design calculations (DEL-003-06 Mechanical Calculation Package).

#### Equipment Tag Scheme (ASSUMPTION: sequential tags by system; to be confirmed by Mechanical Engineer)

| Tag | Equipment Description | Qty | Serving | SOW Ref | Performance (Design Basis) | Electrical (Phase/Voltage/FLA) | Notes |
|---|---|---|---|---|---|---|---|
| HTG-001 | High-Recovery Heating System | 1 | Main shop — general heating | SOW-0035 | Heating capacity TBD (BTU/h or kW); recovery efficiency TBD | TBD — coordinate with PKG-004 | RFP §3.4 requires "high-recovery" type; specific technology (radiant tube, unit heater with heat recovery, etc.) TBD — ASSUMPTION: likely waste-heat recovery or high-efficiency gas unit heater given industrial context |
| AEX-001 | High-Volume Air Exchanger | 1 | Main shop — general ventilation | SOW-0036 | Airflow TBD (CFM or L/s); HRV/ERV effectiveness TBD | TBD — coordinate with PKG-004 | RFP §3.4 requires "high volume" exchanger; ASSUMPTION: heat recovery ventilator (HRV) given Alberta climate |
| MAU-001 | Forced-Air Makeup Air Unit (MUA) | 1 | Main shop — makeup air supply | SOW-0037 | Airflow TBD (CFM); heating capacity TBD; discharge temperature TBD | TBD — coordinate with PKG-004 | Confirmed in App B (Shop) note: "Forced Air Makeup"; tempered/heated supply ASSUMPTION |
| EXH-001 | Heavy Equipment Exhaust Hose and Fan — Repair Bay 1 | 1 | Repair Bay 1 (24' wide) | SOW-0038 | Exhaust flow TBD; fan static pressure TBD; hose length/diameter TBD | TBD — coordinate with PKG-004 | RFP §3.4: "exhaust hoses and fans for heavy equipment in repair bays" |
| EXH-002 | Heavy Equipment Exhaust Hose and Fan — Repair Bay 2 | 1 | Repair Bay 2 (24' wide) | SOW-0038 | Exhaust flow TBD; fan static pressure TBD; hose length/diameter TBD | TBD — coordinate with PKG-004 | Same as EXH-001 for second bay |
| EXH-003 | Welding Station Exhaust System | 1 | Welding station (north wall per App B) | SOW-0039 | Exhaust flow TBD; capture velocity TBD per ACGIH Industrial Ventilation guidelines (location TBD) | TBD — coordinate with PKG-004 | App B (Shop) shows welding station at north wall; RFP §3.4 and App B confirm exhaust requirement |
| EXH-004 | Service Pit Ventilation / Exhaust Fan | TBD | Service pit (ventilated per SOW-0028) | SOW-0028 | Exhaust flow TBD; fan size TBD; design approach TBD pending DEL-003-06 | TBD — coordinate with PKG-004 | RFP §3.4 requires "ventilated and lighted" service pit; not enumerated in SOW-0035–SOW-0040; scope inclusion to be confirmed — see Conflict Table CON-002 in Guidance.md. ASSUMPTION: dedicated low-point exhaust or served by main exhaust system |
| CF-001 thru CF-006 | Ceiling Fans — Main Shop | 6 | Main shop area | SOW-0040 | Fan diameter TBD; CFM TBD; motor power TBD | TBD — coordinate with PKG-004 | App B-Elec (R-05, location TBD in accessible sources) cited in decomp: "6 ceiling fans in main shop area"; 35' mounting height to be accommodated |

> **Quantities note (Pass 3 enrichment):** Per semantic lensing item E-002, quantities for discrete identified equipment items have been populated where inferable from the tag assignment (one tag = one unit). HTG-001, AEX-001, MAU-001, EXH-001, EXH-002, EXH-003 are each assigned quantity 1. EXH-004 remains TBD pending scope confirmation. CF-001 through CF-006 quantity remains 6 per decomposition source. Source: Datasheet tag assignments; Decomposition SOW-0035–SOW-0040.

> **Electrical characteristics note (Pass 3 enrichment):** Per semantic lensing item X-002, an "Electrical (Phase/Voltage/FLA)" column has been added to the Equipment Register to satisfy Specification REQ-003 ("connection requirements — electrical characteristics"). All electrical values are TBD pending coordination with PKG-004 (Electrical Design). Source: Specification.md REQ-003; Procedure.md Step 3.2.

> **Note:** Wash bay ventilation requirements are not explicitly called out as a separate HVAC item in RFP §3.4 or App B (Shop) beyond the general exhaust and makeup air systems. ASSUMPTION: wash bay ventilation is served by the high-volume air exchanger (AEX-001) and/or a dedicated exhaust fan. This is to be resolved in the Mechanical Calculation Package (DEL-003-06) and confirmed in the HVAC Plans (DEL-003-02).

> **R-05 evidence chain note (Pass 3 enrichment):** Per semantic lensing item B-002, R-05 (Appendix B Electrical) is cited as the source for the ceiling fan count (6x) but was not directly read; the citation relies on indirect reference in the decomposition. If R-05 contains additional constraints (fan locations, circuit assignments, electrical sizing), those constraints are not reflected here. ASSUMPTION: the decomposition's citation of 6 ceiling fans is accurate. This should be confirmed by directly reading R-05. Source: Datasheet #5 (References, R-05 row); Decomposition.

---

## 3. Conditions

### 3.1 Operating Conditions

| Parameter | Value | Source |
|---|---|---|
| Outdoor Design Temperature (Heating) | TBD — Alberta climate data for Ferintosh/Camrose County area to be confirmed by Mechanical Engineer (ASHRAE weather tables or Alberta-specific design data) | ASSUMPTION: approximately -35 C or colder per Alberta design practice. Per semantic lensing item B-001, this is essential data for equipment sizing and must be confirmed before HTG-001/MAU-001 capacity calculations. |
| Outdoor Design Temperature (Cooling) | TBD — cooling may not be required for shop occupancy; to be confirmed | ASSUMPTION |
| Indoor Design Temperature (Main Shop) | TBD — ASSUMPTION: minimum 18 C (heavy industrial) per ASHRAE/Alberta Safety Codes | ASSUMPTION — not confirmed by any accessible source document. Per semantic lensing item E-001, this value directly drives HTG-001 sizing. Mechanical Engineer to confirm and record basis in Guidance or DEL-003-06. |
| Indoor Design Temperature (Office) | TBD — ASSUMPTION: 21 C (light occupancy) | ASSUMPTION — not confirmed by any accessible source document. Per semantic lensing item E-001, Mechanical Engineer to confirm and record basis. |
| Relative Humidity (Indoor) | TBD | -- |
| Ventilation Rate | TBD — per ASHRAE 62.1 or NFPA 91 as applicable for industrial shop with diesel/exhaust contaminants | ASSUMPTION: applicable standard |
| Natural Gas Supply | Available (tie-in SOW-0080); pressure TBD | RFP §3.3.2, Decomp SOW-0080 |
| Electrical Supply | Three-phase (voltage TBD; coordinate with PKG-004) | RFP §3.4 |

### 3.2 Regulatory Conditions

| Requirement | Governing Authority | Source |
|---|---|---|
| Building code compliance | Alberta Building Code (edition TBD — see semantic lensing item A-002) | RFP §3.3.2, §3.4 |
| Safety code compliance | Alberta Safety Codes Act | RFP §3.3.2 |
| Gas installation code compliance | CSA B149.1 (edition TBD) — ASSUMPTION: applicable for gas-fired HTG-001 and MAU-001 | Specification.md #3; Procedure.md #2.2 |
| IFC drawings signed/stamped | P.Eng. licensed in Alberta | RFP §3.3.2, SOW-0018 |
| County preliminary design approval required | Camrose County | RFP §3.3.2, SOW-0010c |

---

## 4. Construction

### 4.1 Equipment Integration Notes

| System | Integration Requirement | Source |
|---|---|---|
| HTG-001 (Heating) | Natural gas connection (PKG-018 utility tie-in), three-phase electrical (PKG-015), structural supports (PKG-002/011) | SOW-0035, SOW-0080 |
| AEX-001 (Air Exchanger) | Ductwork penetrations through building envelope (coordinate with PKG-001/011), electrical (PKG-015) | SOW-0036 |
| MAU-001 (Makeup Air) | Ductwork distribution (DEL-003-03), structural supports for unit, electrical (PKG-015), gas (SOW-0080) | SOW-0037, App B (Shop) |
| EXH-001/002 (Equipment Exhaust) | Overhead hose reel systems or drop hoses in repair bays; exhaust fans with exterior discharge; electrical (PKG-015) | SOW-0038 |
| EXH-003 (Welding Exhaust) | Capture hood and fan at welding station; ductwork routed through roof/wall; electrical (PKG-015) | SOW-0039, App B (Shop) |
| EXH-004 (Service Pit Exhaust) | Low-point exhaust if dedicated fan required; ductwork routing TBD; electrical (PKG-015); scope inclusion to be confirmed — see Conflict Table CON-002 | SOW-0028, ASSUMPTION |
| CF-001-006 (Ceiling Fans) | Structural attachment to roof/ceiling structure at 35' height; electrical (PKG-015) per App B-Elec; coordinate fan locations with overhead crane girder layout (two 5-tonne cranes per SOW-0067) to avoid interferences | SOW-0040 |

### 4.2 Commissioning Interface

All mechanical equipment listed in this schedule is subject to commissioning per SOW-0090 (DEL-020-01 Building Systems Commissioning). Commissioning data sheets, startup checklists, and test records are anticipated outputs of commissioning, not of this schedule.

---

## 5. References

| Ref ID | Document | Relevance | Accessibility |
|---|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Main RFP; §3.4 HVAC/ventilation requirements, §3.1 building description | Accessible |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan; confirms forced air makeup, welding exhaust, ceiling fans, equipment layout | Accessible |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Electrical layout; ceiling fans (6x) and exhaust fans noted. **Note:** Not directly read; cited in decomposition — evidence chain is indirect (see B-002 enrichment note in §2.2) | Not directly read; cited in decomposition |
| Decomp | WDMLRL_Decomposition_Claude.md | SOW-0013, SOW-0035-SOW-0040, PKG-003 description, DEL-003-05 entry | Accessible |
| ASHRAE 62.1 | Ventilation for Acceptable Indoor Air Quality | Ventilation rates for occupied spaces | Not accessible — location TBD |
| ASHRAE 90.1 | Energy Standard for Buildings | Energy efficiency for HVAC equipment | Not accessible — location TBD |
| Alberta Building Code | Building code — Alberta (edition TBD — see A-002) | Applicable code for mechanical systems | Not accessible — location TBD |
| Alberta Safety Codes Act | Safety code requirements | Applicable to all building systems | Not accessible — location TBD |
| NFPA 91 | Standard for Exhaust Systems for Air Conveying of Vapors, Gases, Mists, and Particulate Solids | May apply to equipment exhaust and welding exhaust | Not accessible — ASSUMPTION: likely applicable |
| ACGIH Industrial Ventilation | Industrial Ventilation: A Manual of Recommended Practice | Welding exhaust capture velocities and design | Not accessible — ASSUMPTION: likely applicable |
| CSA B149.1 | Natural Gas and Propane Installation Code | Gas-fired equipment connections (HTG-001, MAU-001) — ASSUMPTION: applicable | Not accessible — ASSUMPTION: applicable |

> **Pass 3 enrichment note (B-004):** CSA B149.1 has been added to this References table to harmonize with Specification.md #3 (Standards) and Procedure.md #2.2, where it was already listed. Source: Specification.md Standards table; Procedure.md §2.2 Required References.
