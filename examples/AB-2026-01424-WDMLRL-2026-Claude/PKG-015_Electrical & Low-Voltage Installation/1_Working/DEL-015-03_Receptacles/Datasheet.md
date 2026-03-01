# Datasheet — DEL-015-03 Receptacle Installation

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-015-03 |
| Deliverable Title | Receptacle Installation |
| Package | PKG-015 — Electrical & Low-Voltage Installation |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Responsible Party | Electrical Contractor |
| Deliverable Type | Installation |
| Covers SOW Items | SOW-0057, SOW-0058 |
| Supports Objectives | OBJ-001, OBJ-005 |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Completion Deadline | December 31, 2026 |

Source: Decomposition §7 PKG-015 table (R1 2026-02-25); _CONTEXT.md

---

## Attributes

### Receptacle Types and Ratings

| Type Code | Rating | Voltage | NEMA Configuration | Notes |
|---|---|---|---|---|
| 15 | 15A | 120V | NEMA 5-15 (ASSUMPTION) | General-purpose; parts room, office, utility room, corridor areas |
| 20 (120V) | 20A | 120V | NEMA 5-20 (ASSUMPTION) | General-purpose higher-demand; main shop area |
| 20 (240V) | 20A | 240V | TBD — confirm NEMA configuration (e.g., NEMA 6-20) per DEL-004-09 | Industrial service; main shop area |
| 30 | 30A | 240V | TBD — confirm NEMA configuration (e.g., NEMA 6-30) per DEL-004-09 | Heavy-duty industrial; welding station area |
| 50 | 50A | 240V | TBD — confirm NEMA configuration (e.g., NEMA 6-50 vs. 14-50) per County welder specs and DEL-004-09 | Welding-grade; multiple locations throughout main shop (assumed; see note) |

Source: App B-Elec (Electrical Drawing legend and layout); SOW-0058 (Decomposition §3); SOW-0057 (Decomposition §3)

**NOTE — ASSUMPTION (D-009):** Welding receptacles are assumed to be 50A/240V industrial-grade, consistent with the electrical drawing legend. If County-supplied welder specifications differ, this is treated as a scope change per Decomposition Decision D-009.

**NOTE — NEMA Configuration (TBD) [Ref: A-002]:** NEMA receptacle configurations for 20A/240V, 30A/240V, and 50A/240V ratings are TBD. The correct NEMA designation determines device geometry and plug compatibility. Configuration must be confirmed against County welder specifications (for welding receptacles) and DEL-004-09 (IFC Electrical Specification) for all ratings. Source: _SEMANTIC_LENSING.md A-002; Procedure.md Step 1.1 (notes "NEMA 6-50 or 14-50 — TBD").

### Receptacle Quantities and Location Distribution

Per the conceptual electrical drawing (App B-Elec), the following distribution is indicated. Exact quantities are subject to IFC drawing confirmation (TBD at final design).

| Zone / Area | Receptacle Types Present | Quantity (TBD — per IFC drawings) |
|---|---|---|
| Main Shop — General | 20A/120V (multiple locations along perimeter and columns) | TBD — confirm against DEL-004-05 |
| Main Shop — Work Bench (north wall) | 20A/120V (multiple) | TBD — confirm against DEL-004-05 |
| Main Shop — Welding Station (northeast) | 50A/240V (×3), 30A/240V (×3), 20A/240V (×2), 20A/120V (×2); Exhaust Fan circuit | Approximate from drawing; confirm against DEL-004-05 |
| Main Shop — South perimeter | 20A/240V (multiple), 20A/120V (multiple), 50A/240V (scattered) | TBD — confirm against DEL-004-05 |
| Parts Room | 15A/120V (multiple) | TBD — confirm against DEL-004-05 |
| Office | 15A/120V (multiple) | TBD — confirm against DEL-004-05 |
| Utility Room | 15A/120V (multiple) | TBD — confirm against DEL-004-05 |
| Wash Bay | 20A/120V; 15A/120V; Exhaust Fan circuit | TBD — confirm against DEL-004-05 |

Source: App B-Elec (conceptual electrical layout, Appendix B drawing)

**ASSUMPTION:** Receptacle counts are approximate, read from the conceptual drawing. Final quantities shall be confirmed against the IFC electrical drawings prepared under DEL-004-05 (Receptacle Layout Plans) and DEL-004-06 (Panel Schedules). [Ref: B-001 — essential factual data (exact quantities per zone) is missing from the conceptual drawing and must be resolved at IFC stage.]

---

## Conditions

| Parameter | Value |
|---|---|
| Supply System | Three-phase power (source: RFP §3.4; Decomposition SOW-0051/DEL-015-01) |
| Upstream Dependency | DEL-015-01 Three-Phase Power Service must be energized before receptacle circuits are commissioned |
| Building Structure Dependency | Wall framing and rough-in must be complete before device installation |
| Jurisdiction | Province of Alberta |
| Applicable Code | Alberta Electrical Code (AEC) / Canadian Electrical Code (CEC) Part I — ASSUMPTION: specific edition TBD; confirm with IFC specification DEL-004-09 |
| Inspection Authority (AHJ) | Alberta Safety Codes Authority — TBD: identify the specific Safety Codes permit office for the project location (SW 14-44-21-W4, near Ferintosh, Alberta) before permitting [Ref: C-001] |
| Permit Responsibility | Electrical Contractor (building and safety code permits per RFP §3.3.2) |

---

## Construction

| Attribute | Value |
|---|---|
| Installation Method | TBD — subject to IFC electrical drawings and electrical specification (DEL-004-09) |
| Wiring System | TBD — conduit type, wire gauge, and panel assignment per IFC drawings (DEL-004-05, DEL-004-06) |
| Panel/Circuit Assignment | TBD — per panel schedules (DEL-004-06) |
| GFCI / AFCI Requirements | TBD — per AEC/CEC code requirements for applicable zones (e.g., wash bay for GFCI; office/other zones for AFCI if required by applicable CEC edition) [Ref: B-003] |
| Device Grade | ASSUMPTION: specification-grade or industrial-grade devices appropriate for a maintenance shop environment — TBD: confirm minimum device grade requirement in DEL-004-09 (IFC Electrical Specification) and establish as a normative requirement in Specification [Ref: C-002] |
| Cover Plates | ASSUMPTION: weatherproof/in-use covers required in wash bay zone; standard covers elsewhere unless otherwise specified in IFC drawings — TBD: confirm NEMA rating for weatherproof covers in wet/hazardous locations per CEC Part I and DEL-004-09 [Ref: F-004] |

**NOTE [Ref: B-002]:** The Construction section has 4 of 6 fields as TBD. These fields must be populated when IFC documents (DEL-004-05, DEL-004-06, DEL-004-09) become available. Source: _SEMANTIC_LENSING.md B-002.

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.4 Design Requirements (welding receptacles, three-phase power) |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Conceptual electrical layout, legend, receptacle type/location distribution |
| Decomp | WDMLRL_Decomposition_Claude.md (R1) | SOW-0057, SOW-0058, D-009, PKG-015 deliverable table, OBJ-001, OBJ-005 |
| DEL-004-05 | Receptacle Layout Plans (PKG-004) | IFC drawings — final receptacle layout authority |
| DEL-004-06 | Panel Schedules (PKG-004) | Circuit and panel assignment authority |
| DEL-004-09 | Electrical Specification (PKG-004) | Installation specification authority |
| DEL-015-01 | Three-Phase Power Service | Upstream power supply dependency |
