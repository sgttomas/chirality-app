# Datasheet — DEL-004-02 Single-Line Diagram

**Document Type:** Datasheet (descriptive)
**Deliverable ID:** DEL-004-02
**Deliverable Name:** Single-Line Diagram
**Package:** PKG-004 Electrical Design
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Location:** SW 14–44–21–W4, near Ferintosh, Alberta
**Responsible Party:** Electrical Engineer
**Last Updated:** 2026-02-26

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-004-02 |
| Deliverable Name | Single-Line Diagram |
| Package | PKG-004 Electrical Design |
| Discipline | Electrical Engineering |
| Type | Drawing Set |
| Responsible Party | Electrical Engineer |
| SOW Coverage | SOW-0014 |
| Objectives Supported | OBJ-003, OBJ-005 |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| IFC Stamp Required | Yes — P.Eng. licensed in Alberta (SOW-0018) |

---

## Attributes

### Building Electrical Service

| Attribute | Value | Source |
|---|---|---|
| Service Type | Three-phase power supply | RFP §3.4, SOW-0051 |
| Service Voltage | TBD — ASSUMPTION: likely 120/208V or 347/600V three-phase; to be confirmed by service authority and load calculation | ASSUMPTION |
| Main Service Entry Point | TBD — to be located on final SLD per utility tie-in coordination (SOW-0081) | TBD |
| Service Authority Tie-In | Electrical service tie-in coordinated per SOW-0081 | RFP §3.3.2 |
| Building | New North Shop Addition — ~13,000 sq ft (130' × 100') | Decomposition §2, App B (Shop) |

### Identified Load Groups (from Conceptual Drawing)

| Load Group | Description | Circuit / Rating | Source |
|---|---|---|---|
| Main Shop High Bay Lighting | 5 rows × 4 fixtures = 20 fixtures, 150W LED, 22,000 lumens each | Shown as "L" symbols on conceptual drawing | App B (Electrical) |
| Wash Bay High Bay Lighting | 2 rows × 3 fixtures = 6 fixtures | Shown as "L" symbols on conceptual drawing | App B (Electrical) |
| Office Lighting | 1 × 8' LED fixture | 15A/120V (assumed) | App B (Electrical) |
| Utility Room Lighting | 2 × 8' LED fixtures | 15A/120V (assumed) | App B (Electrical) |
| Parts/Tool Room Lighting | 6 × 8' LED fixtures | 15A/120V (assumed) | App B (Electrical) |
| Exhaust Fan(s) | As shown on electrical drawing | "E" symbol on conceptual drawing — TBD: quantity and individual rating to be confirmed from equipment selection and mechanical coordination (DEL-003-05) | App B (Electrical) |
| 15A/120V Receptacles | General purpose duplex receptacles — multiple locations throughout | 15A/120V | App B (Electrical) |
| 20A/120V Receptacles | General purpose receptacles — multiple locations | 20A/120V | App B (Electrical) |
| 20A/240V Receptacles | 240V single-phase receptacles — multiple locations | 20A/240V | App B (Electrical) |
| 30A/240V Receptacles | Heavy-duty receptacles — multiple locations | 30A/240V | App B (Electrical) |
| 50A/240V Receptacles | Welding-grade receptacles — multiple locations including welding station area | 50A/240V | App B (Electrical); D-009 |
| Compressor Circuit | Dedicated circuit | 40A | App B (Electrical) |
| Fire Hose Pump Circuit | Dedicated circuit | 70A | App B (Electrical) |
| Pressure Washer Circuit | Dedicated circuit | 70A | App B (Electrical) |
| Crane Power (×2) | Power for two 5-tonne overhead cranes | TBD — size per crane manufacturer specification and structural design | App B (Electrical), SOW-0059 |
| Overhead Door Power | Power for all overhead doors | TBD — quantity of doors and motor ratings per architectural drawing | App B (Electrical), SOW-0060 |
| Ceiling Fans | 6 ceiling fans in main shop area | TBD — rating (watts or amps) per equipment selection; resolution source: equipment supplier or Electrical Engineer specification (SOW-0040) | App B (Electrical), SOW-0040 |
| Security Camera Wiring | Low-voltage wiring | TBD — system type and count not specified in source | App B (Electrical), SOW-0064 |
| Antenna Wire (2-Way Radios) | Low-voltage wiring for radio antenna | TBD — routing and termination per communications design | App B (Electrical), SOW-0065 |
| Forced-Air Makeup Air Unit (MUA) | Mechanical equipment electrical feed | TBD — rating per mechanical equipment schedule (DEL-003-05); coordinate with Mechanical Engineer | SOW-0037; Decomposition PKG-003 |
| High-Recovery Heating System | Mechanical equipment electrical feed | TBD — rating per mechanical equipment schedule (DEL-003-05); coordinate with Mechanical Engineer | SOW-0035; Decomposition PKG-003 |
| Mechanical Exhaust Systems | Mechanical equipment exhaust system electrical feed(s) | TBD — quantity and rating per mechanical equipment schedule (DEL-003-05); may overlap with exhaust fan(s) above — coordinate with Mechanical Engineer | SOW-0038, SOW-0039; Decomposition PKG-003 |

### Electrical Legend (from Conceptual Drawing)

| Symbol | Description |
|---|---|
| L (circle) | Lights |
| E (circle) | Exhaust Fan |
| 15 (circle) | 15 Amp 120V receptacle |
| 20 (circle) | 20 Amp 120V receptacle |
| 20 (solid circle) | 20 Amp 240V receptacle |
| 30 (solid circle) | 30 Amp 240V receptacle |
| 50 (solid circle) | 50 Amp 240V receptacle |

*Source: App B (Electrical) conceptual drawing legend*

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Project Location | SW 14–44–21–W4, near Ferintosh, Alberta | Decomposition §1 |
| Jurisdiction | Alberta — Safety Code permits required (SOW-0007, SOW-0009) | RFP §3.3.2 |
| Applicable Codes | Alberta Safety Codes Act; Alberta Building Code; applicable CSA/CEC standards — specific clauses TBD | RFP §3.3.2, SOW-0008, SOW-0009 |
| Building Occupancy / Use | Industrial maintenance shop — heavy equipment servicing, welding, crane operations | RFP §3.1, §3.4 |
| Environmental | Rural landfill site — outdoor utility tie-in required; specific exposure class TBD | App B, SOW-0081 |
| IFC Stamp Requirement | All drawings to be signed/stamped by a P.Eng. licensed in Alberta | RFP §3.3.2, SOW-0018 |
| County Approval Required | Preliminary electrical design requires County approval before IFC (SOW-0010d) | RFP §3.3.2 |

---

## Construction

| Item | Description | Source |
|---|---|---|
| Drawing Format | Single-Line Diagram (SLD) — schematic representation of power distribution hierarchy from service entrance to all branch circuits and equipment | Standard electrical engineering practice |
| Content Expected | Service entrance characteristics; main switchgear/distribution panel; feeder runs to sub-panels; branch circuit schedule references; dedicated equipment circuits (cranes, pumps, compressor); low-voltage system notation | App B (Electrical), SOW-0014 |
| Relationship to Other Deliverables | SLD is the primary power hierarchy document; informs DEL-004-03 (Power Distribution Plans), DEL-004-05 (Receptacle Layout Plans), DEL-004-06 (Panel Schedules), DEL-004-08 (Calculation Package) | Decomposition §7, PKG-004 |
| Conceptual Basis | Appendix B (Electrical) conceptual layout drawing — provides load locations, circuit ratings, and legend; SLD will formalize distribution hierarchy not yet shown at conceptual stage | App B (Electrical) |
| Preliminary Design Predecessor | DEL-004-01 (Preliminary Electrical Design) — County approval required before SLD is finalized for IFC | SOW-0010d, Decomposition §7 |

---

## References

| Ref # | Document | Relevance to This Deliverable |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.4 electrical design requirements; §3.3.2 IFC stamp and permit obligations; §1.0 scope overview |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Conceptual electrical layout, legend, circuit ratings, load locations — primary source for load inventory |
| Decomp | WDMLRL_Decomposition_Claude.md | SOW-0014, SOW-0051–SOW-0066, SOW-0081–SOW-0082; PKG-004 scope; OBJ-003, OBJ-005 |
