# Datasheet — DEL-015-05 Low-Voltage Systems

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-015-05 |
| **Title** | Low-Voltage Systems |
| **Package** | PKG-015 — Electrical & Low-Voltage Installation |
| **Type** | Installation |
| **Responsible Party** | Electrical Contractor |
| **Work Classification** | Low-voltage wiring installation (120 V and below) |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Completion Deadline** | December 31, 2026 |
| **SOW Coverage** | SOW-0064, SOW-0065 |
| **Objectives Supported** | OBJ-001, OBJ-005 |

**Source:** _CONTEXT.md; Decomposition §7 PKG-015 table; R-01 (RFP) §1.1, §3.1

---

## Attributes

### Systems Covered

| System | Scope Statement | Source |
|---|---|---|
| Security Camera Wiring | Install wiring for security cameras | SOW-0064; App B-Elec (Electrical Notes) |
| 2-Way Radio Antenna Wiring | Install antenna wire for 2-way radios | SOW-0065; App B-Elec (Electrical Notes) |

### Voltage Classification

| Parameter | Value | Source |
|---|---|---|
| System voltage class | Low-voltage (120 V and below) | _CONTEXT.md (Scope of Work) |
| Power supply voltage (building) | Three-phase (exact voltage TBD per utility) | RFP §3.4; App B-Elec |

### Wiring Quantities and Routing

| Item | Quantity / Detail | Source |
|---|---|---|
| Security camera rough-in count | TBD — number of camera rough-in locations to be defined in DEL-004-07 Low-Voltage System Plans. Record count once confirmed by Owner/Electrical Engineer. [Lensing: B-001] | App B-Elec (legend: "Wiring for Security Cameras"); DEL-004-07 |
| Radio antenna rough-in locations | TBD — antenna termination location(s) to be defined in DEL-004-07 Low-Voltage System Plans. Record location once confirmed. [Lensing: B-001] | App B-Elec (legend: "Antenna Wire for 2 Way Radios"); DEL-004-07 |
| Cable types / specifications | TBD — to be specified in DEL-004-07 and/or electrical specification (DEL-004-09). Record cable type specifications once issued (e.g., Cat6/Cat6A for cameras, coaxial type for antenna, antenna cable grade). [Lensing: A-002] | location TBD |
| Conduit type and sizing | TBD — to be specified in IFC drawings | location TBD |

### Head-End / Termination Location

| Item | Value | Source |
|---|---|---|
| Head-end / termination location | TBD — identify where camera cables and antenna cable terminate (e.g., utility room, office, dedicated IDF closet). To be defined in DEL-004-07. [Lensing: B-002] | location TBD; Guidance.md §Considerations references "head-end or IDF location" and "equipment room" but no formal attribute defined |

> ASSUMPTION: The scope of DEL-015-05 is limited to rough-in wiring and conduit installation (pull wire/conduit to termination points). Supply and installation of cameras, radio equipment, and antenna hardware are not included in this deliverable unless confirmed otherwise by the Owner or Electrical Engineer. (No source explicitly states this boundary — inferred from the language "wiring for" and "antenna wire for" in App B-Elec.)

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Governing jurisdiction | Province of Alberta | RFP §2.22 |
| Applicable safety codes | Alberta Safety Codes (STANDATA and relevant Alberta Electrical Code adoptions) | RFP §3.3.2; §3.4 |
| IFC drawing requirement | All IFC drawings must be P.Eng.-stamped | RFP §3.3.2 |
| Guarantee period | 2 years post-Construction Completion Certificate (CCC) | RFP §2.10.2 |
| Defect rectification | Within 10 days of Owner written instruction during guarantee period | RFP §2.10.6 |
| Prime Contractor designation | Electrical Contractor works under Design-Builder as Prime Contractor | RFP §2.15 |
| Building completion deadline | December 31, 2026 | RFP §3.1 |

---

## Construction

| Element | Value | Source |
|---|---|---|
| Building type | New construction — concrete structure, 35' ceiling | RFP §3.4; App B-Elec |
| Building area (approx.) | 13,000 sq ft (New North Shop addition) | RFP §3.1 |
| Applicable rooms / areas | Main shop, wash bay, parts room, utility room, office — exact low-voltage locations per DEL-004-07 | App B-Elec (floor plan) |
| Interface with other packages | Upstream: DEL-015-04 (Equipment Power Circuits); Design: DEL-004-07 (Low-Voltage Plans); Electrical Spec: DEL-004-09 | _DEPENDENCIES.md; Decomposition §7 |

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Contract conditions, scope, design requirements |
| R-05 / App B-Elec | AB-2026-01424-Appendix B (Electrical).pdf | Conceptual electrical drawing — security camera and radio wiring noted |
| Decomposition | WDMLRL_Decomposition_Claude.md §7 PKG-015 | SOW-0064, SOW-0065 statements and objective mapping |
| DEL-004-07 | Low-Voltage System Plans (not yet issued) | Will define routing, quantities, and termination details |
| DEL-004-09 | Electrical Specification (not yet issued) | Will define material and workmanship standards |
