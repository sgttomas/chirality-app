# Datasheet — DEL-004-05 Receptacle Layout Plans

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-004-05 |
| **Name** | Receptacle Layout Plans |
| **Package** | PKG-004 Electrical Design |
| **Discipline** | Electrical Engineering |
| **Type** | Drawing Set |
| **Responsible Party** | Electrical Engineer |
| **Covers SOW** | SOW-0014 |
| **Supports Objectives** | OBJ-001, OBJ-003, OBJ-005 |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14-2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |

### Revision History

| Rev | Date | Description | Author |
|---|---|---|---|
| — | TBD | Initial IFC issue | TBD — Electrical Engineer of Record |

> **Note (E-003):** Revision tracking is provided to support version control through the design process (preliminary through IFC). The Electrical Engineer shall update this table as revisions are issued.

---

## Attributes

### Building Context

| Attribute | Value | Source |
|---|---|---|
| Building name | New North Shop addition | R-01 S3.1 |
| Useable area (addition) | ~13,000 sq ft | R-01 S3.1 |
| Ceiling height | 35 ft (concrete structure) | R-01 S3.4, App B |
| Power supply | Three-phase | R-01 S3.4 |

### Receptacle Types Shown on Conceptual Drawing

| Symbol | Rating | Voltage | Notes | Source |
|---|---|---|---|---|
| 15 | 15 A | 120 V | General purpose; multiple locations per drawing | R-05 (App B-Elec legend) |
| 20 | 20 A | 120 V | General purpose; multiple locations per drawing | R-05 (App B-Elec legend) |
| 20 (bold circle) | 20 A | 240 V | Higher-demand locations | R-05 (App B-Elec legend) |
| 30 | 30 A | 240 V | Shown at welding station area | R-05 (App B-Elec legend) |
| 50 | 50 A | 240 V | Welding-grade; shown at welding station and distributed through main shop | R-05 (App B-Elec legend); D-009 |

### Receptacle Distribution by Zone (from Conceptual Drawing)

| Zone | Receptacle Types Indicated | Preliminary Count / Range | Notes | Source |
|---|---|---|---|---|
| Main Shop — Work Bench (north wall) | 20 A/120 V (multiple) | TBD — preliminary count per EE. Conceptual drawing shows ~6-8 symbols along bench. **ASSUMPTION** | Row of 20 A receptacles along work bench | R-05 (App B-Elec) |
| Main Shop — Welding Station (northeast) | 20 A/120 V, 50 A/240 V, 30 A/240 V (cluster) | TBD — preliminary count per EE. Conceptual drawing shows cluster of ~8-10 receptacle symbols. **ASSUMPTION** | High-density; also shows exhaust fan symbol | R-05 (App B-Elec) |
| Main Shop — general bays | 20 A/120 V, 50 A/240 V (distributed) | TBD — preliminary count per EE. Conceptual drawing shows multiple 20 A and 50 A symbols distributed across bays. **ASSUMPTION** | Multiple 20 A and 50 A symbols throughout bays | R-05 (App B-Elec) |
| Parts Room | 15 A/120 V (multiple) | TBD — preliminary count per EE | General purpose | R-05 (App B-Elec) |
| Office | 15 A/120 V (multiple) | TBD — preliminary count per EE | General purpose | R-05 (App B-Elec) |
| Utility Room | 15 A/120 V (multiple) | TBD — preliminary count per EE | General purpose | R-05 (App B-Elec) |
| Wash Bay | 15 A/120 V (limited) | TBD — preliminary count per EE | General purpose; wet-area GFCI requirements apply — ASSUMPTION | R-05 (App B-Elec) |
| Mezzanine | TBD | TBD — preliminary count per EE | Not explicitly depicted on conceptual drawing. Mezzanine is above parts room, utility room, and wash bay per R-01 S3.4. Area estimate TBD pending architectural design (DEL-001-02). | R-01 S3.4; R-05 (not shown) |
| Old North Shop renovation (washroom, locker room, kitchenette) | TBD | TBD — pending DEL-001-10 (renovation architectural plans) | Renovation receptacle scope not shown on conceptual electrical drawing. Whether included in DEL-004-05 or a separate drawing is TBD. | R-01 S3.1, S3.4; R-05 (not shown) |

> **Note (B-001):** The mezzanine zone entry has been expanded to include its location context from R-01 S3.4. Area estimate and receptacle coverage remain TBD pending architectural design confirmation.
>
> **Note (B-002):** Preliminary receptacle counts (or count ranges) have been added as TBD placeholders per zone. Counts from the conceptual drawing are approximate visual estimates marked as ASSUMPTION. Final counts are the Electrical Engineer's responsibility.
>
> **Note (B-003):** An Old North Shop renovation zone entry has been added. Receptacle scope for this zone is TBD pending DEL-001-10.

### Special Equipment Circuits (Shown on Conceptual Drawing — Not Receptacle Plans Scope per se, but coordinating context)

| Equipment | Circuit Rating | Source |
|---|---|---|
| Compressor | 40 A | R-05 (App B-Elec notes) |
| Fire Hose Pump | 70 A | R-05 (App B-Elec notes) |
| Pressure Washer | 70 A | R-05 (App B-Elec notes) |
| Overhead Cranes (x2) | TBD (power circuits — coordinated via DEL-004-03) | R-05 (App B-Elec notes) |
| Overhead Doors | TBD (power circuits — coordinated via DEL-004-03) | R-05 (App B-Elec notes) |

> **Note:** Equipment power circuits for compressor, pump, and washer are referenced on the conceptual electrical drawing. The Receptacle Layout Plans drawing set focuses on receptacle outlet placement. Coordination with DEL-004-03 (Power Distribution Plans) and DEL-004-06 (Panel Schedules) is required for circuit origination.

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Governing jurisdiction | Province of Alberta | R-01 S2.22 |
| Applicable code | Alberta Safety Codes (electrical) — ASSUMPTION: Alberta Electrical Utility Code / Canadian Electrical Code Part I applies | R-01 S3.3.2 (location TBD in code text) |
| Drawing stamp requirement | P.Eng. licensed to practice in Alberta | R-01 S3.3.2 |
| IFC status required before construction | Yes | R-01 S3.3.2; OBJ-003 |
| County approval required | Preliminary design approval by County before IFC issue | R-01 S3.3.2 |
| GFCI requirement (wet locations) | ASSUMPTION: required per CEC Part I for wash bay and utility wet areas | location TBD |
| Welding receptacle voltage assumption | 50 A/240 V — assumed; County to supply welder specs; treated as scope change if different. **TBD — County welder specifications not yet received; 50 A/240 V assumed per D-009; confirm before IFC.** | D-009 (Decomposition Decision Log); R-01 S3.4 |

> **Note (B-004):** The welding receptacle voltage condition has been expanded to highlight that this is the single most critical external input with no tracked receipt date. The Electrical Engineer should establish a target date for County confirmation and an escalation path if specifications are not received in time for IFC.

---

## Construction

| Item | Value | Source |
|---|---|---|
| Drawing format | TBD (IFC drawing set conventions apply) | — |
| CAD/BIM platform | TBD — Electrical Engineer's standard platform; file format TBD | — |
| Legend | Electrical legend to be reproduced and expanded per final design | R-05 (App B-Elec legend) |
| Scale | TBD — to be determined by Electrical Engineer; ensure consistency between Datasheet and actual drawing set | — |
| Zones covered | Main Shop, Welding Station, Work Bench area, Parts Room, Office, Utility Room, Wash Bay; Mezzanine TBD; Old North Shop renovation TBD | R-05 (App B-Elec) |
| Coordination drawings required | Power Distribution Plans (DEL-004-03), Panel Schedules (DEL-004-06), Architectural Floor Plans (DEL-001-02) | ASSUMPTION — standard drawing coordination |
| Note re Old North Shop renovation | Receptacle scope for renovation (washroom, locker room, kitchenette) is TBD — not explicitly shown on conceptual electrical drawing | R-01 S3.4; R-05 |

> **Note (X-002):** CAD/BIM platform and file format have been added as a tracked TBD. These must be determined before drawing production begins.
>
> **Note (X-003):** Drawing scale has been noted for tracking. The Electrical Engineer shall record the confirmed scale once determined and ensure it matches across the issued drawing set.

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | S1.0, S3.1, S3.3.2, S3.4 — project scope, room program, design requirements, three-phase power, code compliance |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Conceptual electrical layout and legend — primary source for receptacle types and zone placement |
| D-009 | Decomposition Decision Log | Welding receptacles assumed 50 A/240 V |
| WDMLRL_Decomposition_Claude.md | Project Decomposition R1 | SOW-0014, SOW-0057, SOW-0058, OBJ-001, OBJ-003, OBJ-005 |
