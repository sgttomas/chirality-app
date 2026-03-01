# Datasheet — DEL-006-04: Cistern & Pump Details

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-006-04 |
| Deliverable Name | Cistern & Pump Details |
| Package | PKG-006 — Plumbing Design |
| Discipline | Plumbing Engineering |
| Artifact Type | Drawing Set |
| Responsible Party | Plumbing Engineer |
| SOW Reference | SOW-0016 (Complete final plumbing design — water supply, drainage, septic) |
| Objectives Supported | OBJ-001, OBJ-003, OBJ-004 (ASSUMPTION: package-grouping heuristic applied; PKG-006 maps to these objectives per decomposition §7 PKG-006 row) |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Completion Deadline | December 31, 2026 |

---

## Attributes

### Cistern System

| Attribute | Value | Source |
|---|---|---|
| Cistern minimum storage capacity | 50,000 L | RFP §3.4; App B-Plumb (noted on drawing as "50,000L Water Storage") |
| Cistern location | Utility Room / adjacent to utility room (as shown on plumbing drawing) | App B-Plumb (conceptual plan) |
| Cistern material / type | TBD — concrete, fiberglass, polyethylene, or steel; to be determined by Plumbing Engineer based on installation type, volume, climate, and structural coordination | ASSUMPTION — not specified in RFP; Guidance discusses options (see Guidance.md §Considerations > Cistern Material and Type) [B-002] |
| Cistern installation type | TBD — above-grade, in-slab, or below-grade; depends on structural and geotechnical coordination | ASSUMPTION — App B-Plumb shows conceptual location only; see CONF-001 in Guidance.md [X-002] |
| Cistern filling connection diameter | 2.5 inch | RFP §3.4; SOW-0042 |
| Cistern filling connection type | Bulk water fill connection | RFP §3.4; SOW-0044 |
| Cistern plumbing scope | "Minimum 50,000L cistern complete with the necessary plumbing" | RFP §3.4 |
| Geotechnical investigation status | TBD — confirm whether DEL-008-01 (Geotech Report) has been completed; required if cistern is below-grade | ASSUMPTION — geotech status unknown; see Procedure.md Step 2 (2.2) [X-002] |

### Distribution Pump System

| Attribute | Value | Source |
|---|---|---|
| Internal service distribution pump flow rate | 100 LPM (minimum) | RFP §3.4; SOW-0042 |
| Cistern filling connection size at pump | 2.5 inch | RFP §3.4; SOW-0042 [A-002: canonical term "cistern filling connection"] |
| Pump application | Internal service water distribution | RFP §3.4 |
| Pump quantity | TBD (minimum 1 assumed) | ASSUMPTION — RFP specifies "a pump" (singular); quantity per design |
| Pump type | TBD — centrifugal or pressure-booster type | ASSUMPTION — not specified in sources; engineer to determine |
| Pump head/pressure | TBD | Not stated in available sources |
| Pressure tank / hydropneumatic tank | TBD | ASSUMPTION — likely required for pressurized distribution; not explicitly stated |
| Pressure tank capacity | TBD | ASSUMPTION — to be determined by Plumbing Engineer if pressure tank approach is selected [B-001] |
| Pressure tank pre-charge pressure | TBD | ASSUMPTION — to be determined based on system operating pressure [B-001] |
| Pressure tank connection size | TBD | ASSUMPTION — to be determined based on system piping design [B-001] |

### Bulk Water Fill System

| Attribute | Value | Source |
|---|---|---|
| Bulk water fill purpose | External filling of cistern via high-volume pump | RFP §3.4; SOW-0044 |
| Bulk water fill pump | High volume pump for external filling | RFP §3.4; SOW-0044 |
| Bulk fill pump flow rate | TBD — to be determined based on Owner operational requirements (fill truck capacity, target fill time) | Not stated in available sources; see Procedure.md Step 2 (2.4) [A-004, B-003] |
| Bulk fill pump head | TBD | Not stated in available sources [B-003] |
| Bulk fill pump power | TBD | Not stated in available sources [B-003] |
| Bulk fill connection size | TBD | Not stated in available sources [B-003] |
| Bulk fill point location | TBD — shown conceptually on plumbing drawing | App B-Plumb (location TBD from IFC drawings) |

### Pressure Washer / Water Tap System

| Attribute | Value | Source |
|---|---|---|
| Water tap and pressure washer reel | As shown on plumbing drawing | RFP App B-Plumb; SOW-0049 |
| Water tap locations | Utility Room area and Wash Bay area (per conceptual plan) | App B-Plumb (conceptual drawing) |
| Pressure washer reel circuit | 70A circuit (electrical, by others) | Decomposition SOW-0063 / App B-Elec |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Site | Rural Alberta landfill; no municipal water service — all water from on-site cistern | RFP §1.0, §3.4; App B-Plumb |
| Water source | Bulk delivery (external truck fill to cistern) | RFP §3.4; SOW-0044; ASSUMPTION for source type |
| Operating environment | Industrial maintenance shop — heavy equipment servicing | RFP §3.1 |
| Governing codes | Alberta Safety Codes; all applicable Alberta building codes and regulations | RFP §3.3.2, §3.4 |
| IFC drawing stamp | All IFC drawings to be signed/stamped by a P.Eng. licensed in Alberta | RFP §3.3.2; SOW-0018 |
| Guarantee period | Construction period + 2 years post-CCC | RFP §2.10 |
| Pump electrical power | Three-phase power available to building | RFP §3.4; SOW-0051 |

---

## Construction

### Drawing Set Contents (Anticipated Artifacts)

| Sheet / Artifact | Description |
|---|---|
| Cistern system plan view | Plan showing cistern location, dimensions, connections, and clearances |
| Cistern section view | Section showing cistern depth, wall construction, inlet/outlet, access |
| Pump equipment schedule | Pump model, flow rate (min. 100 LPM), head, power requirements |
| Piping and connection details | Piping layout from cistern to distribution points; fill connection (2.5") detail |
| Control system diagram | Level controls, float switches, pump controls, alarms (as required) |
| Pressure tank details | TBD — if hydropneumatic tank is included in design |
| Electrical connection diagrams | Power connections to pump(s) — coordination with electrical discipline |
| Installation and maintenance access details | Clearance requirements, access hatches, service provisions |
| Bulk water fill detail | External fill connection point, hose connection, overflow provisions |

*Note: Artifact list is drawn from _CONTEXT.md anticipated artifacts and consistent with PKG-006 plumbing design scope. Final sheet list to be determined by Plumbing Engineer.*

### Interface Information

| Interface | Connected Deliverable | Notes |
|---|---|---|
| Water distribution (downstream) | DEL-006-02 Water Distribution Plans | Cistern feeds building water distribution system |
| Electrical connections | DEL-004 Electrical Design / DEL-015-04 Equipment Power | Pump power circuits; 70A for pressure washer |
| Drain and vent system | DEL-006-03 Drain & Vent Plans | Cistern overflow and drain connections |
| Bulk water fill (civil/sitework) | DEL-018 Sitework | Exterior fill connection access |
| Plumbing calculations (cistern sizing, pump TDH) | DEL-006-07 Plumbing Calculation Package | Cistern volume basis-of-design and pump TDH calculations documented here; referenced in Guidance.md §Principles > Cistern Sizing and Procedure.md Steps 2.1, 2.3 [E-001] |

---

## References

| Ref ID | Document | Sections Used |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §1.0, §3.1, §3.3.2, §3.4 |
| R-06 | AB-2026-01424-Appendix B (Plumbing).pdf | Conceptual plumbing plan — full sheet |
| DECOMP | WDMLRL_Decomposition_Claude.md | §3 (SOW-0041, SOW-0042, SOW-0044, SOW-0049), §5 (OBJ-001, OBJ-003, OBJ-004), §7 (PKG-006, DEL-006-04) |

*Note: No Canadian plumbing standards (e.g., NBC, Alberta Plumbing Code) are explicitly cited in the available source documents. Applicable codes are to be determined by the Plumbing Engineer of Record. ASSUMPTION: Alberta Safety Codes and the National Plumbing Code of Canada (as adopted in Alberta) govern this work.*

---

## Terminology and Notation Conventions

*The following conventions apply across this document and all four DEL-006-04 production documents (see also Guidance.md §Terminology Conventions):*

| Term / Notation | Canonical Form | Notes | Ref |
|---|---|---|---|
| Cistern filling connection | "cistern filling connection" | Preferred over "fill connection" or "filling connection" when referring to the 2.5 inch connection serving the distribution pump | [A-002] |
| Pipe size notation | Use "2.5 inch" in text; "2.5\"" in drawing annotations | Normalize across documents; avoid mixing "2.5 inch", "2.5\"", and "2.5'" | [X-003] |
