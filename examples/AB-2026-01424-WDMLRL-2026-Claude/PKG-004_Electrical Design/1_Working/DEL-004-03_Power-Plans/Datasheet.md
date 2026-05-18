# Datasheet — DEL-004-03 Power Distribution Plans

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-004-03 |
| Deliverable Name | Power Distribution Plans |
| Package | PKG-004 Electrical Design |
| Discipline | Electrical Engineering |
| Type | Drawing Set |
| Responsible Party | Electrical Engineer (P.Eng., Alberta-licensed) |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Completion Deadline | December 31, 2026 |
| Covers SOW | SOW-0014 (Complete final electrical design — three-phase power distribution, lighting, receptacles) |
| Supports Objectives | OBJ-001, OBJ-003, OBJ-005 |
| Status | SEMANTIC_READY (per _STATUS.md — authoritative source for state) |

---

## Attributes

### Building and Service Parameters

| Attribute | Value | Source |
|---|---|---|
| Building type | New maintenance shop addition (New North Shop) | RFP §3.1, App B (Electrical) |
| Useable area (approx.) | ~13,000 sq ft (130' × 100' per conceptual drawing) | RFP §3.1, App B (Electrical) |
| Power supply type | Three-phase | RFP §3.4 |
| Service voltage | TBD (ASSUMPTION: 120/208V or 347/600V three-phase; engineer to confirm based on utility availability) | RFP §3.4 (three-phase required); voltage level TBD |
| Service authority tie-in | Coordinated electrical service tie-in required | Decomposition SOW-0081 |
| IFC drawing requirement | All IFC drawings signed/stamped by P.Eng. licensed in Alberta | RFP §3.3.2, Decomposition SOW-0018 |

### Identified Loads — Power Distribution

| Load Description | Circuit / Rating | Quantity | Source |
|---|---|---|---|
| 5-tonne overhead cranes on trolley | Power for crane (circuit rating TBD by engineer) | 2 | RFP §3.4, App B (Electrical) |
| Overhead doors | Power for overhead doors (circuit rating TBD) | TBD — specific count to be confirmed from architectural door schedule (DEL-001-07); conceptual drawing shows multiple 24' doors in main shop and wash bay | App B (Electrical); door count **TBD** (Source: Architect / DEL-001-07) |
| Air compressor | 40A circuit | 1 | App B (Electrical) |
| Fire hose pump | 70A circuit | 1 | App B (Electrical) |
| Pressure washer | 70A circuit | 1 | App B (Electrical) |
| Welding-grade receptacles (high-voltage, shop area) | 50A/240V (ASSUMPTION per D-009) | Multiple, throughout shop area | RFP §3.4; ASSUMPTION: 50A/240V per Decomposition D-009 |
| 20A/240V receptacles | 20A/240V | Multiple per electrical drawing layout | App B (Electrical) |
| 30A/240V receptacles | 30A/240V | Multiple per electrical drawing layout | App B (Electrical) |
| 20A/120V receptacles | 20A/120V | Multiple per electrical drawing layout | App B (Electrical) |
| 15A/120V receptacles | 15A/120V | Multiple per electrical drawing layout | App B (Electrical) |
| Exhaust fans | Per electrical drawing layout | Multiple | App B (Electrical) |
| Forced-air makeup air unit | Power TBD by mechanical/electrical coordination | 1 | App B (Shop), Decomposition SOW-0037 |
| 6 ceiling fans (main shop area) | Power TBD | 6 | App B (Electrical) |
| Security camera wiring | Low-voltage / power TBD | Per drawing layout | App B (Electrical) |
| Antenna wire for 2-way radios | Low-voltage | Per drawing layout | App B (Electrical) |
| High bay lights (main shop) | 150W LED, 22,000 lumens each | 20 (5 rows × 4) | App B (Electrical) |
| High bay lights (wash bay) | Rating TBD — wattage to be confirmed by Electrical Engineer or lighting vendor; required for load calculation completeness (see DEL-004-08) | 6 (2 rows × 3) | App B (Electrical); wattage **TBD** (Source: Electrical Engineer / lighting vendor) |
| LED fixture (office) | 8' LED | 1 | App B (Electrical) |
| LED fixtures (utility room) | 8' LED | 2 | App B (Electrical) |
| LED fixtures (parts/tool room) | 8' LED | 6 | App B (Electrical) |

> Note: Lighting loads are shared with DEL-004-04 (Lighting Plans). Power distribution plans document the branch circuit feeds and panel schedule entries for all loads. Lighting circuit details are coordinated with DEL-004-04.

### Drawing Set Attributes

| Attribute | Value | Source |
|---|---|---|
| Drawing type | Issued for Construction (IFC) drawing set | RFP §3.3.2, SOW-0018 |
| Stamp requirement | P.Eng. licensed in Alberta | RFP §3.3.2 |
| Coordinating deliverables | DEL-004-02 Single-Line Diagram, DEL-004-04 Lighting Plans, DEL-004-05 Receptacle Layout Plans, DEL-004-06 Panel Schedules | Decomposition PKG-004 |
| Anticipated drawing content | Site/service entry plan, panel locations, branch circuit routing plan, load schedule cross-reference | ASSUMPTION: standard power distribution drawing set content |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Site location | SW 14–44–21–W4, near Ferintosh, Alberta | RFP §1.0 |
| Building occupancy type | Industrial maintenance shop (heavy equipment servicing) | RFP §3.1, §3.4 |
| Environment (general) | Indoor industrial; outdoor service tie-in | RFP §3.1, §3.4 |
| Applicable jurisdiction | Province of Alberta | RFP §2.22 |
| Regulatory framework | Alberta Safety Codes Act; Alberta Electrical Code (Canadian Electrical Code Part I, as adopted); CCDC 14–2013 | RFP §3.3.2; ASSUMPTION: likely applicable, location TBD in source text |
| Preliminary design approval | County (Owner) must approve preliminary electrical design before IFC | RFP §3.3.2, SOW-0010d |

---

## Construction

| Item | Description | Source |
|---|---|---|
| Anticipated artifact(s) | Power distribution drawing set (IFC), P.Eng.-stamped | RFP §3.3.2, _CONTEXT.md |
| Relationship to Single-Line Diagram | DEL-004-02 Single-Line Diagram provides top-level system overview; DEL-004-03 provides floor-plan-level branch circuit layout | Decomposition PKG-004 |
| Relationship to Panel Schedules | DEL-004-06 Panel Schedules tabulates circuit assignments; DEL-004-03 shows physical routing and load locations | Decomposition PKG-004 |
| Preliminary design milestone | DEL-004-01 Preliminary Electrical Design must precede IFC drawings | SOW-0010d, Decomposition PKG-004 |
| Construction execution package | PKG-015 Electrical & Low-Voltage Installation will use these drawings as the governing construction document | Decomposition PKG-015 |

---

## References

| Ref ID | Document | Relevance | Accessibility |
|---|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Main RFP — §3.4 electrical design requirements, §3.3.2 IFC and P.Eng. requirements | Accessed |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Conceptual electrical layout drawing — load schedule, receptacle layout, lighting layout, legend | Accessed |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Floor plan showing spatial layout, room locations, crane positions | Referenced in decomposition; not directly accessed for this deliverable |
| D-009 | Decomposition Decision Log | Welding receptacles assumed 50A/240V | Decomposition WDMLRL_Decomposition_Claude.md |
| D-001 | Decomposition Decision Log | Gantry/crane terminology reconciled — 5-tonne overhead cranes on trolley | Decomposition WDMLRL_Decomposition_Claude.md |
