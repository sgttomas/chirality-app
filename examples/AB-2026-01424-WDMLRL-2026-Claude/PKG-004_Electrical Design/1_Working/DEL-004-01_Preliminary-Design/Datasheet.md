# Datasheet — DEL-004-01 Preliminary Electrical Design

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-004-01 |
| Name | Preliminary Electrical Design |
| Package | PKG-004 — Electrical Design |
| Discipline | Electrical Engineering |
| Type | Design Presentation |
| Responsible Party | Electrical Engineer |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Project Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Covers SOW | SOW-0010d |
| Supports Objectives | OBJ-003, OBJ-005 |
| Decomposition Reference | WDMLRL_Decomposition_Claude.md — §7 PKG-004 |

---

## Attributes

### Building Being Designed

| Attribute | Value | Source |
|---|---|---|
| Building | New North Shop Addition | RFP §3.1; App B (Electrical) |
| Gross Floor Area (approximate) | ~13,000 sq ft (usable) | RFP §3.1 |
| Building Footprint | 130' × 100' (per conceptual drawing) | App B (Electrical) drawing dimension |
| Ceiling Height | 35' (concrete structure) | RFP §3.4 |
| Primary Power Supply | Three-phase | RFP §3.4 |

### Power Distribution

| Circuit / Load | Ampacity / Voltage | Quantity | Source |
|---|---|---|---|
| Three-phase service — main breaker/service size | TBD — dependent on load calculation (DEL-004-08) | 1 | RFP §3.4; SOW-0051 |
| Two 5-tonne overhead crane power feeds | TBD per crane (crane motor ampacity TBD — crane specifications not provided in RFP) | 2 | App B (Electrical); SOW-0059 |
| Overhead door power | TBD per door | TBD (count to be confirmed from App B or architectural design) | App B (Electrical); SOW-0060 |
| Compressor circuit | 40A | 1 | App B (Electrical); SOW-0061 |
| Fire hose pump circuit | 70A | 1 | App B (Electrical); SOW-0062 |
| Pressure washer circuit | 70A | 1 | App B (Electrical); SOW-0063 |

**Note (B-001):** Service size (main breaker ampacity) is an essential design parameter listed as TBD pending load calculation (DEL-004-08). Cross-reference: Construction table below also records this dependency.
**Note (B-003):** Overhead door count is stated as "Multiple" without a specific count. Other equipment (cranes = 2, ceiling fans = 6) has specific counts. The door count is an essential input for circuit allocation; to be confirmed from App B or architectural design.
**Note (F-002):** Crane motor ampacity is TBD. Crane equipment specifications must be obtained before crane circuit sizing can proceed. If crane specifications are unavailable at preliminary design stage, document the gap and note provisional assumptions.

### Receptacle Layout

| Type | Ampacity / Voltage | Locations (as shown on electrical drawing) | Source |
|---|---|---|---|
| Standard duplex | 15A / 120V | Multiple — shop area, office, parts room, utility room, wash bay area | App B (Electrical) drawing |
| General purpose | 20A / 120V | Multiple — shop area and ancillary rooms | App B (Electrical) drawing |
| General purpose | 20A / 240V | Multiple — shop area, work bench area | App B (Electrical) drawing |
| Heavy duty | 30A / 240V | Multiple — shop area (work bench / welding station vicinity) | App B (Electrical) drawing |
| Welding-grade | 50A / 240V (**ASSUMPTION** — per App B symbols and Decomposition D-009; not confirmed by Owner) | Multiple — throughout shop area | App B (Electrical); RFP §3.4; SOW-0057, SOW-0058 |

**Note (D-001):** RFP §3.4 states "multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment" without specifying ampacity. App B (Electrical) shows 50A/240V symbols. Decomposition D-009 records the assumption that welding receptacles are 50A/240V. This value is assumption-dependent until the County confirms welding equipment specifications. See Guidance Conflict Table CF-004-001.

### Lighting

| Location | Fixture Type | Quantity | Specification | Source |
|---|---|---|---|---|
| Main Shop (New North Shop) | High-Bay LED | 20 (5 rows × 4) | 150W, 22,000 lumens each | App B (Electrical); SOW-0052 |
| Wash Bay | High-Bay LED | 6 (2 rows × 3) | TBD wattage/lumens (**ASSUMPTION:** same type as main shop assumed — 150W/22,000 lumens class — not confirmed in source; see Guidance CF-004-002) | App B (Electrical); SOW-0053 |
| Office | 8' LED fixture | 1 | TBD wattage/lumens | App B (Electrical); SOW-0054 |
| Utility Room | 8' LED fixture | 2 | TBD wattage/lumens | App B (Electrical); SOW-0055 |
| Parts/Tool Room | 8' LED fixture | 6 | TBD wattage/lumens | App B (Electrical); SOW-0056 |
| Service Pit/Trench | TBD | TBD | Per RFP §3.4: "ventilated and lighted service pit" | RFP §3.4; SOW-0028 |

**ASSUMPTION:** Wash Bay, Office, Utility Room, and Parts/Tool Room high-bay and 8' LED specifications (wattage/lumens) are not stated in sources for those rooms beyond fixture count and type; values marked TBD pending Electrical Engineer's selection.

### Mechanical Equipment with Electrical Connections

| Equipment | Electrical Requirement | Source |
|---|---|---|
| 6 ceiling fans (main shop) | Power feed — TBD circuit size | App B (Electrical); SOW-0040 (via App B-Elec) |
| Exhaust fan(s) | Power feed — TBD circuit size | App B (Electrical); SOW-0066 |
| Welding station exhaust system | Power feed — TBD circuit size | RFP §3.4; SOW-0039 |
| Forced-air makeup air unit | Power feed — TBD circuit size | App B (Shop notes); SOW-0037 |

### Low-Voltage Systems

| System | Description | Source |
|---|---|---|
| Security cameras | Wiring roughed in as shown on electrical drawing | App B (Electrical); SOW-0064 |
| 2-way radio antenna | Antenna wire as shown on electrical drawing | App B (Electrical); SOW-0065 |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Jurisdiction | Province of Alberta | RFP §2.22 |
| Code compliance | Must adhere to all Alberta Safety Codes and applicable Alberta building codes | RFP §3.3.2, §3.4 |
| Electrical service tie-in | Must be coordinated and executed | RFP §3.3.2; SOW-0081 |
| Communication lines tie-in | Must be coordinated and executed | RFP §3.3.2; SOW-0082 |
| IFC drawings | Must be signed/stamped by a P.Eng. licensed in Alberta | RFP §3.3.2; SOW-0018 |
| County approval required | Preliminary design must receive County approval before final design proceeds | RFP §3.3.2; SOW-0010d |
| Completion deadline | All Work on or before December 31, 2026 | RFP §3.1; SOW-0091 |

---

## Construction

| Item | Value | Source |
|---|---|---|
| Design-Build delivery | CCDC 14–2013 Stipulated Price Contract | RFP §2.7 |
| Preliminary design purpose | County project team approval | RFP §3.3.2; SOW-0010d |
| Final design requirement | IFC drawings — P.Eng. stamped | RFP §3.3.2; SOW-0018 |
| Coordinating disciplines | Architectural, Structural, Mechanical, Civil, Plumbing (all disciplines must be coordinated) | RFP §3.3.2; OBJ-003 |
| Panel schedules | Required as part of final electrical design (DEL-004-06); conceptual basis established in preliminary | Decomposition §7 PKG-004 |
| Service size | TBD — dependent on load calculation (DEL-004-08) | ASSUMPTION |

---

## References

| Ref ID | Document | Relevance to this Deliverable |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | RFP §1.0, §3.3.2, §3.4 — design requirements, scope of work, preliminary design obligation |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | App B (Electrical) — conceptual electrical layout, legend, fixture counts, circuit types, equipment circuits |
| Decomp | WDMLRL_Decomposition_Claude.md | Decomposition §3G, §5, §6, §7 — SOW items, objectives, package and deliverable context |

**Citation format note (E-004):** Source citations in this Datasheet use the pattern `[Document shorthand] [section]; [SOW-NNNN]` (e.g., "RFP §3.4; SOW-0051" or "App B (Electrical); SOW-0052"). Where multiple SOW items are relevant, they are listed comma-separated (e.g., "SOW-0057, SOW-0058").
