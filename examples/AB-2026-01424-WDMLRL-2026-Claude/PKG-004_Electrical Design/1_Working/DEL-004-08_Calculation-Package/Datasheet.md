# Datasheet — DEL-004-08 Electrical Calculation Package

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-004-08 |
| **Deliverable Name** | Electrical Calculation Package |
| **Package** | PKG-004 — Electrical Design |
| **Discipline** | Electrical Engineering |
| **Type** | Calculation Package |
| **Responsible Party** | Electrical Engineer |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition (New North Shop) |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |
| **Decomposition Reference** | WDMLRL_Decomposition_Claude.md — DEL-004-08 |
| **SOW Coverage** | SOW-0014 |
| **Objectives Supported** | OBJ-003, OBJ-005 |

**Canonical Building Name:** The building is formally referred to as the "West Dried Meat Lake Regional Landfill Maintenance Shop Addition." The term "New North Shop" appears in some project documentation as an informal reference. For the purposes of this calculation package, the formal name shall be used. (Lensing B-005 — terminology normalization)

---

## Attributes

### Building and Service Parameters

| Attribute | Value | Source |
|---|---|---|
| Building useable area | ~13,000 sq ft (approximately 130' × 100') | RFP §3.1; App B (Electrical) |
| Power supply type | Three-phase | RFP §3.4 |
| Service tie-in responsibility | Proponent to coordinate electrical service tie-in | RFP §3.3.2 (SOW-0081) |
| IFC drawings requirement | Signed/stamped by P.Eng. licensed in Alberta | RFP §3.3.2 (SOW-0018) |

### Lighting — Main Shop

| Attribute | Value | Source |
|---|---|---|
| Fixture type | High bay LED | App B (Electrical) |
| Wattage | 150 W per fixture | App B (Electrical) |
| Lumen output | 22,000 lumens per fixture | App B (Electrical) |
| Layout | 5 rows × 4 fixtures = 20 fixtures total | App B (Electrical) |

### Lighting — Wash Bay

| Attribute | Value | Source |
|---|---|---|
| Fixture type | High bay (type not specified beyond high bay) | App B (Electrical) |
| Layout | 2 rows × 3 fixtures = 6 fixtures total | App B (Electrical) |

### Lighting — Office, Utility Room, Parts/Tool Room

| Attribute | Value | Source |
|---|---|---|
| Office | 1 × 8' LED fixture (ASSUMPTION: 80 W conservative planning value — Electrical Engineer to confirm per selected product) | App B (Electrical); Lensing X-001 |
| Utility Room | 2 × 8' LED fixtures (ASSUMPTION: 80 W each conservative planning value — Electrical Engineer to confirm per selected product) | App B (Electrical); Lensing X-001 |
| Parts/Tool Room | 6 × 8' LED fixtures (ASSUMPTION: 80 W each conservative planning value — Electrical Engineer to confirm per selected product) | App B (Electrical); Lensing X-001 |

Note: Pass 1 documented the 8-foot LED fixture wattage as "~60-80 W each." Per lensing item X-001, the 33% range is too broad for load schedule purposes. The conservative upper value of 80 W is adopted as the planning assumption for connected load calculations. The Electrical Engineer shall confirm the actual wattage upon product selection.

### Receptacles (per electrical drawing layout)

| Circuit Type | Nominal Rating | Source |
|---|---|---|
| Standard general | 15 A / 120 V | App B (Electrical) |
| General power | 20 A / 120 V | App B (Electrical) |
| Medium power | 20 A / 240 V | App B (Electrical) |
| Heavy power | 30 A / 240 V | App B (Electrical) |
| Welding-grade | 50 A / 240 V | App B (Electrical); RFP §3.4 |

Note: The RFP §3.4 states "multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment." The specific assumption of 50 A / 240 V for welding receptacles is documented in Decomposition Decision D-009 (ASSUMPTION per decomposition). Quantity and exact placement per App B (Electrical) drawing layout.

### Dedicated Equipment Circuits

| Equipment | Circuit Rating | Source |
|---|---|---|
| 5-tonne overhead crane (×2) | Power supply required; ampacity TBD by Electrical Engineer | App B (Electrical); RFP §3.4 |
| Overhead doors | Power supply required; quantity TBD (coordinate with DEL-001-07); ampacity ASSUMPTION: ~15-20 A / 120 V per unit (typical practice) — Electrical Engineer to confirm per operator data | App B (Electrical); Lensing B-002 |
| Compressor | 40 A | App B (Electrical) |
| Fire hose pump | 70 A | App B (Electrical) |
| Pressure washer | 70 A | App B (Electrical) |

### Crane Electrical Data (placeholder — to be populated upon receipt of manufacturer data)

| Parameter | Value | Source |
|---|---|---|
| Motor full-load amperes (FLA) | TBD — obtain from crane manufacturer | Lensing B-001; PKG-016 coordination |
| Voltage | TBD — obtain from crane manufacturer | Lensing B-001; PKG-016 coordination |
| Phases | TBD — obtain from crane manufacturer | Lensing B-001; PKG-016 coordination |
| Duty cycle | TBD — obtain from crane manufacturer | Lensing B-001; PKG-016 coordination |

Note: Per lensing item B-001, crane electrical data is the single most critical missing data point for this calculation package. It affects service entrance sizing (REQ-004-08-01), dedicated circuit calculations (REQ-004-08-09), voltage drop (REQ-004-08-15), and panel schedules (DEL-004-06). The Electrical Engineer shall coordinate with PKG-016 to obtain this data before IFC.

### Exhaust Fans

| Attribute | Value | Source |
|---|---|---|
| Exhaust fan(s) | As shown on electrical drawing | App B (Electrical) |
| Quantity | TBD — coordinate with PKG-003 Mechanical Design to obtain count | App B (Electrical); Lensing B-003 |
| Motor wattage per unit | TBD — no assumed value available; coordinate with PKG-003 for motor data | Lensing B-003 |
| Placement | TBD — per final electrical drawing | App B (Electrical) |

Note: Per lensing item B-003, exhaust fans are the least-specified electrical load in the package. Unlike ceiling fans (which have a count of 6) or overhead doors (which have an assumed ampacity), exhaust fans currently have no count, no wattage, and no assumed value. The Electrical Engineer shall coordinate with PKG-003 Mechanical Design to obtain exhaust fan count and motor data and record planning assumptions here.

### Low-Voltage Systems

| System | Requirement | Source |
|---|---|---|
| Security cameras | Wiring to be installed | App B (Electrical) |
| 2-way radio antenna | Antenna wire to be installed | App B (Electrical) |

### Ceiling Fans (Main Shop)

| Attribute | Value | Source |
|---|---|---|
| Quantity | 6 | App B (Electrical); Decomposition SOW-0040 |
| Location | Main shop area | App B (Electrical) |

---

## Conditions

| Condition | Description | Source |
|---|---|---|
| Jurisdiction | Province of Alberta | RFP §2.22 |
| Code compliance | All applicable Alberta building codes and regulations; all Alberta Safety Codes | RFP §3.3.2 |
| Safety Code permits | Proponent to obtain all applicable Safety Code permits (fees paid by County) | RFP §3.3.2 |
| Stamped drawings | All IFC drawings signed/stamped by P.Eng. licensed in Alberta | RFP §3.3.2 |
| Welding equipment specifications | County to supply welding equipment specifications; Proponent sizes receptacles accordingly | RFP §3.4 |
| Project completion | All Work on or before December 31, 2026 | RFP §3.1 |
| Design-build form | Calculations must support design-build delivery; County has concept only | RFP §3.4 |

---

## Construction

| Aspect | Description | Source |
|---|---|---|
| Building structure | Concrete structure with 35' ceiling height | RFP §3.4; App B (Shop) |
| Service pit | Ventilated and lighted service pit/trench for under-equipment servicing (lighting to be designed by Electrical Engineer) | RFP §3.4; App B (Shop) |
| Mezzanine | Overhead mezzanine above parts room, utility room, and wash bay — electrical loads to be accounted for. Mezzanine-specific loads (lighting, receptacles, equipment) TBD — to be itemized separately in connected load schedule. ASSUMPTION: mezzanine area likely requires its own lighting circuit(s) and possibly receptacle circuits; scope TBD by Electrical Engineer. (Lensing E-001) | App B (Electrical) |
| Wash bay | Single enclosed bay, 24' wide — 6 high bay lights to be powered | App B (Electrical) |
| Welding station | Welding station in main shop area — welding-grade receptacles and ventilation exhaust power | App B (Electrical); RFP §3.4 |
| Crane supports | Two 5-tonne overhead cranes on trolley — power feeds sized by Electrical Engineer | App B (Electrical); RFP §3.4 |

---

## References

| Ref # | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §1.0, §3.3.2, §3.4 — project scope, design requirements, electrical requirements |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Conceptual electrical layout, legend, fixture counts, circuit ratings, equipment loads |
| Decomposition | WDMLRL_Decomposition_Claude.md | DEL-004-08 entry; SOW-0014, SOW-0051–SOW-0066; OBJ-003, OBJ-005; Decision D-009 |
