# Datasheet — DEL-013-01: High-Recovery Heating System

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-013-01 |
| **Deliverable Name** | High-Recovery Heating System |
| **Package** | PKG-013 — Mechanical & HVAC Installation |
| **Type** | Installation |
| **Responsible Party** | Mechanical Contractor |
| **SOW Reference** | SOW-0035 |
| **Objective Linkage** | OBJ-001, OBJ-004 |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |
| **Document Date** | 2026-02-26 |

**Sources:** `_CONTEXT.md`; WDMLRL_Decomposition_Claude.md §7 (PKG-013 table); R-01 §3.4; R-01 §3.1

---

## Attributes

| Attribute | Value | Source / Notes |
|---|---|---|
| **System Type** | High-recovery heating system | R-01 §3.4 (explicit) |
| **Function** | Facility space heating with thermal energy recovery | R-01 §3.4; `_CONTEXT.md` Description |
| **Heat Recovery Mode** | High-recovery (energy recovery from exhaust or return air streams) | R-01 §3.4 (explicit term); mechanism TBD pending mechanical design (DEL-003-02/07) |
| **Integration — Air Exchanger** | Interfaces with DEL-013-02 (High-Volume Air Exchanger) for heat recovery loop | `_CONTEXT.md` Related Deliverables; `_DEPENDENCIES.md` |
| **Integration — Makeup Air** | Interfaces with DEL-013-03 (Forced-Air Makeup System) for conditioned fresh-air supply | `_CONTEXT.md`; `_DEPENDENCIES.md` |
| **Integration — Exhaust Systems** | Coordinates with DEL-013-04 (Equipment Exhaust) and DEL-013-05 (Welding Exhaust) for exhaust-stream management | `_DEPENDENCIES.md` |
| **Integration — Ceiling Fans** | Coordinates with DEL-013-06 (Ceiling Fans) for distributed air circulation | `_DEPENDENCIES.md` |
| **Building Area Served** | New North Shop addition; approx. 13,000 sq ft; 35 ft ceiling height | R-01 §3.1; Appendix B (Shop) floor plan |
| **Heating Capacity (BTU/h or kW)** | TBD — to be determined by Mechanical Engineer (DEL-003-06 Mechanical Calculation Package). **Note:** This is an essential data point required for procurement and installation; must be resolved before equipment selection. | Lensing ref: B-001 |
| **Fuel/Energy Source** | TBD — natural gas assumed given RFP reference to natural gas tie-in (R-01 §3.3.2). **Note:** Fuel source must be formally confirmed before procurement; see Guidance CONF-001 and Trade-off 3. | ASSUMPTION: natural gas; confirm with Mechanical Engineer (DEL-003-07). Lensing ref: B-001, B-004 |
| **Electrical Supply** | Three-phase power (building runs on three-phase per R-01 §3.4); circuit sizing TBD. **Note:** Circuit sizing is an essential data point required for coordination with PKG-015. | R-01 §3.4; circuit details via DEL-015-04. Lensing ref: B-001 |
| **Controls Interface** | Building management system (BMS) / controls integration required; BMS communication protocol TBD (e.g., BACnet, Modbus, LON — to be specified by design team in PKG-003/PKG-004) | `_DEPENDENCIES.md` Constraint Notes; Lensing ref: B-003 |
| **Equipment Location** | Utility Room (DEL-012-02); must fit with proper clearances | `_DEPENDENCIES.md`; Appendix B (Shop) floor plan |
| **Equipment Weight** | TBD — to be populated from equipment submittal after equipment selection | Lensing ref: B-002. Required for structural adequacy assessment of utility room. |
| **Equipment Dimensions (L x W x H)** | TBD — to be populated from equipment submittal after equipment selection | Lensing ref: B-002. Required for fit verification per REQ-005. |
| **Equipment Noise Rating** | TBD — to be populated from equipment submittal after equipment selection | Lensing ref: B-002. Required for acoustic assessment in industrial environment. |

---

## Conditions

| Condition | Value | Source / Notes |
|---|---|---|
| **Operating Environment** | Industrial maintenance shop; heavy equipment, dust, exhaust fumes present | R-01 §3.1; Appendix B (Shop) |
| **Ambient Temperature Range** | Alberta climate; design heating load driven by cold-climate requirements | ASSUMPTION: Alberta winter design conditions apply; specific design temperature TBD pending mechanical calculations |
| **Ceiling Height** | 35 ft (shop area) | R-01 §3.4; Appendix B (Shop) |
| **Ventilation Context** | High-volume air exchange required simultaneously with heating; makeup air system introduces cold outdoor air | `_CONTEXT.md`; `_DEPENDENCIES.md` |
| **Utility Room Constraints** | Equipment must fit within utility room with code-required clearances; ductwork routing must avoid structural conflicts | `_DEPENDENCIES.md` |
| **Utility Availability Pre-Condition** | Electrical, gas, and water connections must be available prior to installation | `_DEPENDENCIES.md` |

---

## Construction

| Element | Description | Source / Notes |
|---|---|---|
| **Equipment Procurement** | Mechanical Contractor procures and delivers heating equipment per approved mechanical design (DEL-003-07 specification) | `_CONTEXT.md` Scope |
| **System Assembly** | Equipment assembled and positioned in utility room per manufacturer requirements and mechanical drawings | `_CONTEXT.md` Scope |
| **Ductwork Connections** | Ductwork connected to building distribution system per mechanical drawings (DEL-003-03) | `_CONTEXT.md` Scope; R-01 §3.3 |
| **Controls & Monitoring** | Controls and monitoring system configured and integrated with building systems | `_CONTEXT.md` Scope; `_DEPENDENCIES.md` |
| **Performance Testing** | System commissioned and performance-tested before acceptance | `_CONTEXT.md` Scope |
| **IFC Drawing Requirement** | Installation must follow IFC drawings stamped by P.Eng. licensed in Alberta | R-01 §3.3.2 |
| **Upstream Dependency** | DEL-012-02 (Utility Room) must be substantially complete before heating system installation can proceed | `_DEPENDENCIES.md` |

---

## References

| Ref ID | Document | Relevant Sections |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.1 Project Background; §3.3 Scope of Work; §3.4 Design Requirements |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | New North Shop floor plan — equipment locations, utility room, dimensions |
| — | WDMLRL_Decomposition_Claude.md | §5 Objectives (OBJ-001, OBJ-004); §6 Packages (PKG-013); §7 Deliverables by Package (DEL-013-01) |
| — | `_CONTEXT.md` | Deliverable identity, scope, related deliverables |
| — | `_DEPENDENCIES.md` | Upstream/downstream dependency constraints |
| — | DEL-003-07 (not yet issued) | Mechanical Specification — will govern equipment selection |
| — | DEL-003-02 / DEL-003-03 (not yet issued) | HVAC Layout Plans / Ductwork Plans — will govern installation |
| — | DEL-003-06 (not yet issued) | Mechanical Calculation Package — will confirm heating capacity |

---

## Semantic Lensing Enrichment Log (Pass 3)

The following items from `_SEMANTIC_LENSING.md` were applied to this document:

| ItemID | Action Taken |
|---|---|
| B-001 | Annotated Heating Capacity, Fuel/Energy Source, and Electrical Supply TBD entries with notes emphasizing these are essential data points required for procurement |
| B-002 | Added Equipment Weight, Equipment Dimensions, and Equipment Noise Rating as new TBD attributes required for structural, fit, and acoustic assessments |
| B-003 | Enriched Controls Interface attribute with BMS protocol TBD note (BACnet, Modbus, LON) and reference to PKG-003/PKG-004 |
| B-004 | Added cross-reference to CONF-001 and Trade-off 3 on Fuel/Energy Source entry to surface fuel source ambiguity |
