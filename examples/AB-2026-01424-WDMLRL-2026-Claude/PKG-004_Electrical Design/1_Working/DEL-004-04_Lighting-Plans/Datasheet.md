# Datasheet — DEL-004-04 Lighting Plans

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-004-04 |
| **Name** | Lighting Plans |
| **Package** | PKG-004 — Electrical Design |
| **Discipline** | Electrical Engineering |
| **Type** | Drawing Set |
| **Responsible Party** | Electrical Engineer |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Covers SOW** | SOW-0014 (Complete final electrical design — three-phase power distribution, lighting, receptacles) |
| **Supports Objectives** | OBJ-001, OBJ-003, OBJ-005 |

---

## Attributes

### Lighting Zones and Fixture Counts

| Zone | Fixture Type | Quantity | Notes |
|---|---|---|---|
| Main Shop | High Bay LED | 20 (5 rows × 4 fixtures) | 150W LED, 22,000 lumens each |
| Wash Bay | High Bay LED | 6 (2 rows × 3 fixtures) | Type not separately specified beyond "High Bay" |
| Office | 8-foot LED strip | 1 | — |
| Utility Room | 8-foot LED strip | 2 | — |
| Parts/Tool Room | 8-foot LED strip | 6 | — |
| Service Pit/Trench | TBD | TBD | RFP §3.4 requires ventilated and lighted service pit; fixture type not specified in source. Fixture type, wattage, lumen output, enclosure rating (wet/damp location), and quantity to be determined by Electrical Engineer -- see CONF-LT-002 in Guidance.md. |

*Sources: App B-Elec (Electrical Notes and Layout); SOW-0052 through SOW-0056 (Decomposition §3 SSOW-G)*

**Note [B-001]:** Service pit fixture data rows (type, wattage, lumen output, quantity, enclosure rating) are absent from source documents. These fields must be populated once the Electrical Engineer resolves fixture selection at preliminary design. See CONF-LT-002 in Guidance.md.

### Key Electrical Attributes — Lighting System

| Attribute | Value | Source |
|---|---|---|
| High Bay wattage (main shop) | 150W per fixture | App B-Elec, Electrical Notes |
| High Bay lumen output (main shop) | 22,000 lumens per fixture | App B-Elec, Electrical Notes |
| High Bay type | LED | App B-Elec, Electrical Notes |
| Main shop total high bay fixtures | 20 | App B-Elec, SOW-0052 |
| Wash bay total high bay fixtures | 6 | App B-Elec, SOW-0053 |
| Office LED fixtures | 1 × 8-foot LED strip | App B-Elec, SOW-0054 |
| Office LED fixture wattage | TBD | Not specified in source — to be determined by Electrical Engineer during product selection |
| Office LED fixture lumen output | TBD | Not specified in source — to be determined by Electrical Engineer during product selection |
| Utility room LED fixtures | 2 × 8-foot LED strip | App B-Elec, SOW-0055 |
| Utility room LED fixture wattage | TBD | Not specified in source — to be determined by Electrical Engineer during product selection |
| Utility room LED fixture lumen output | TBD | Not specified in source — to be determined by Electrical Engineer during product selection |
| Parts/tool room LED fixtures | 6 × 8-foot LED strip | App B-Elec, SOW-0056 |
| Parts/tool room LED fixture wattage | TBD | Not specified in source — to be determined by Electrical Engineer during product selection |
| Parts/tool room LED fixture lumen output | TBD | Not specified in source — to be determined by Electrical Engineer during product selection |
| Building power supply | Three-phase | RFP §3.4; App B-Elec |
| IFC stamp requirement | P.Eng. licensed in Alberta | RFP §3.3.2 |

### Building Geometry (Reference — from Electrical Drawing)

| Dimension | Value | Source |
|---|---|---|
| New North Shop footprint | 130' × 100' (approx. 13,000 sq ft useable) | App B-Elec layout; RFP §3.1 |
| Ceiling height | 35 feet | RFP §3.4; App B-Elec notes |
| Wash Bay width | 24' | App B-Elec layout |

**Note [B-003]:** Building dimensions above are derived from conceptual-stage sources (App B-Elec layout and RFP). These values should be confirmed by cross-referencing architectural drawings (DEL-001-02) when available. Current source is App B-Elec layout only; treat as preliminary until architectural confirmation.

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Jurisdiction | Alberta, Canada | RFP §2.22; §3.3.2 |
| Applicable code regime | Alberta Safety Codes; Alberta Building Code | RFP §3.3.2; §3.4 |
| Governing electrical standard | ASSUMPTION: Canadian Electrical Code (CEC) Part I — location TBD in accessible sources |
| Environment | Industrial maintenance shop; high ceiling (35'); heavy equipment present | RFP §3.1; §3.4; App B-Elec |
| Service pit condition | Ventilated and lighted (requirements per RFP §3.4) | RFP §3.4 |
| Project deadline | On or before December 31, 2026 | RFP §3.1 |
| IFC drawings required | Yes — P.Eng. stamp required | RFP §3.3.2 |
| Preliminary design approval | County approval required prior to final design | RFP §3.3.2; SOW-0010d |

---

## Construction

### What This Deliverable Produces

The Lighting Plans drawing set is a design document (not a construction document in isolation). It provides:

- Plan-view lighting layout drawings showing fixture locations for all zones of the New North Shop addition.
- Fixture schedule identifying type, wattage, lumen output, and quantity for each zone.
- Sufficient detail to support IFC drawing set (Issued for Construction), P.Eng.-stamped.
- Coordination reference for related electrical deliverables: Single-Line Diagram (DEL-004-02), Power Distribution Plans (DEL-004-03), Panel Schedules (DEL-004-06).

### Anticipated Artifacts

- Drawing Set: Lighting layout plan(s) per RFP requirements (location/zone coverage per App B-Elec).
- Fixture Schedule — required fields per zone (aligned with Procedure Step 4.2):
  - Zone / area
  - Fixture type designation
  - Manufacturer and model (or performance specification)
  - Wattage (W)
  - Lumen output (lm)
  - Voltage / phase
  - Mounting type
  - Enclosure rating (IP / wet-location rating where applicable)
  - Quantity
  - TBD (to be populated during design).
- Notes and legend consistent with App B-Elec electrical legend symbols.

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Main RFP: §1.0, §3.1, §3.3.2, §3.4 electrical and design requirements |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Conceptual electrical layout, fixture counts, electrical legend, and notes — primary source for lighting layout |
| DECOMP | WDMLRL_Decomposition_Claude.md | SOW-0014, SOW-0052–0056; PKG-004; DEL-004-04; OBJ-001, OBJ-003, OBJ-005 |
