# Datasheet — DEL-013-03: Forced-Air Makeup System

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-013-03 |
| Deliverable Title | Forced-Air Makeup System |
| Package | PKG-013 — Mechanical & HVAC Installation |
| Type | Mechanical & HVAC Installation |
| SOW Reference | SOW-0037 |
| Objective Linkage | OBJ-001, OBJ-004 |
| Responsible Party | Mechanical Contractor |
| Activity | Procurement + Installation + Commissioning |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Completion Deadline | December 31, 2026 (Source: RFP §3.1) |

### Terminology

The canonical term for this deliverable's principal equipment is **Makeup Air Unit (MUA)**. This term is used consistently throughout all four production documents. Other forms appearing in source documents — "forced-air makeup", "makeup air system", "forced-air makeup air system" — refer to the same system and should be understood as synonymous.

Source: Decomposition Vocabulary Map ("Forced Air Makeup | Makeup air unit, MUA"); _CONTEXT.md
Enrichment: B-003

---

## Attributes

### System Function

| Attribute | Value | Source |
|---|---|---|
| System type | Forced-air makeup air unit (MUA) | RFP App B; _CONTEXT.md |
| Primary function | Supply conditioned outside air to facility to supplement primary ventilation and replace exhaust air | _CONTEXT.md Description |
| Secondary function | Supplement primary air exchanger (DEL-013-02) operation | _CONTEXT.md Description |
| Air type supplied | Fresh outside air (conditioned / tempered) | _CONTEXT.md; _DEPENDENCIES.md |
| Served facility | New North Shop addition, ~13,000 sq ft useable area, 35' ceiling height | RFP §3.1, App B |

### Capacity & Performance

| Attribute | Value | Source |
|---|---|---|
| Required supply airflow rate | **TBD (BLOCKING)** — must balance total exhaust volumes from DEL-013-04 (heavy equipment exhaust) and DEL-013-05 (welding exhaust). Source to resolve: DEL-003-06 Mechanical Calculation Package. This is the essential design fact that drives equipment selection, duct sizing, and heating capacity. | _DEPENDENCIES.md Constraint Notes; Enrichment B-001 |
| Design outdoor air temperature | **TBD** — Alberta design conditions per ASHRAE climate data or DEL-003-06. Required for heating coil/burner sizing; without this value, heating capacity cannot be independently verified. | ASHRAE climate data (location TBD); Enrichment B-002 |
| Heating of makeup air | Required — coordinated with DEL-013-01 (High-Recovery Heating System) | _DEPENDENCIES.md Internal Package Dependencies |
| Air distribution coverage | All facility areas — ASSUMPTION: includes main shop, repair bays, welding area, wash bay (see REQ-013-03-06 note regarding wash bay confirmation — Enrichment X-001) | _DEPENDENCIES.md Constraint Notes; _CONTEXT.md Scope |
| Building pressurization control | Controls must prevent excessive pressurization | _DEPENDENCIES.md Constraint Notes |
| Air quality requirement | Fresh air quality critical for safety and comfort | _DEPENDENCIES.md Constraint Notes |

### Equipment

| Attribute | Value | Source |
|---|---|---|
| Unit designation | Makeup Air Unit (MUA) | Decomposition Vocabulary Map; _REFERENCES.md |
| Equipment location | TBD — anticipated in Utility Room (DEL-012-02) area or adjacent to fresh air intake | _DEPENDENCIES.md External Dependencies (ASSUMPTION) |
| Fresh air intake location | TBD — to be finalized; to coordinate with air exchanger intake (DEL-013-02) | _DEPENDENCIES.md External Dependencies; Critical Integration Points |
| Make / model | TBD — subject to mechanical design (DEL-003-07) and equipment schedule (DEL-003-05) | _REFERENCES.md Standard References |
| Electrical supply | TBD — three-phase power available (SOW-0051); circuit sizing per mechanical/electrical design | SOW-0051 (ASSUMPTION: three-phase supply consistent with other major equipment) |
| Electrical disconnect switch | **TBD** — required per Alberta Electrical Code; lockout/tagout provisions required per Alberta OHS. Disconnect type and location per electrical design. | ASSUMPTION: Alberta Electrical Code / Alberta OHS; Enrichment X-002 |
| Fuel / energy source | TBD — natural gas heating ASSUMPTION consistent with high-recovery heating system (DEL-013-01) | _DEPENDENCIES.md; SOW-0080 (ASSUMPTION) |
| Condensate management | **TBD** — determine whether MUA heating coil requires condensate drain pan and drain line, particularly for shoulder-season operation. Source to resolve: MUA manufacturer manual / DEL-003-07. | ASSUMPTION: standard element for MUA units with heating coils in cold climates; Enrichment F-004 |

### Ductwork & Distribution

| Attribute | Value | Source |
|---|---|---|
| Fresh air intake ductwork | Required — routing from exterior intake to MUA unit | _CONTEXT.md Scope |
| Supply ductwork | Required throughout facility | _CONTEXT.md Scope |
| Dampers and control valves | Required — installed as part of this deliverable | _CONTEXT.md Scope |
| Fire/smoke dampers | **TBD** — required at ductwork penetrations through fire-rated assemblies per Alberta Building Code. Quantity, locations, and ratings per mechanical design and fire separation drawings. | ASSUMPTION: standard code obligation; Enrichment C-002 |
| Supply ductwork routing | TBD — to be established in mechanical design (DEL-003-03); must avoid conflicts with structural and other systems | _DEPENDENCIES.md Critical Integration Points; _REFERENCES.md R-04 |
| Distribution point locations | TBD — per mechanical design drawings; reference R-04 (Shop Floor Plan) for layout intent | _REFERENCES.md R-04 |
| Control system integration | Required — dampers and control valves to coordinate with heating and air exchange systems | _CONTEXT.md Scope |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Climate / environment | Alberta Central region; cold climate conditions — makeup air requires heating in winter | RFP §1.0 (location); _DEPENDENCIES.md Constraint Notes (ASSUMPTION re: heating requirement) |
| Operating environment | Industrial maintenance shop; heavy equipment, diesel/gasoline fumes, welding fumes present | RFP §3.1, App B; _CONTEXT.md Related Deliverables |
| Acoustic environment | **TBD** — large MUA units can generate significant noise in the occupied shop space; acoustic impact on worker communication and comfort should be assessed. Source to resolve: Mechanical engineer / MUA manufacturer noise data / occupational health standards. | ASSUMPTION: standard consideration for industrial MUA installations; Enrichment E-001 |
| Pressure regime | Slight positive or neutral building pressure required; controls to prevent excessive pressurization | _DEPENDENCIES.md Constraint Notes |
| Coordination environment | Concurrent installation with DEL-013-01 (Heating), DEL-013-02 (Exchanger), DEL-013-04 (Equipment Exhaust), DEL-013-05 (Welding Exhaust), DEL-013-06 (Ceiling Fans) | _CONTEXT.md Related Deliverables |

---

## Construction

| Element | Description | Source |
|---|---|---|
| Equipment procurement | MUA unit(s) per mechanical engineer's equipment schedule (DEL-003-05) | _CONTEXT.md Scope |
| Equipment delivery | To site, coordinated with Utility Room readiness (DEL-012-02) | _DEPENDENCIES.md External Dependencies |
| Assembly and integration | System assembly including unit mounting, connection to fresh air intake ductwork, supply ductwork, and control wiring | _CONTEXT.md Scope |
| Fresh air intake ductwork | Installation from exterior wall penetration to MUA unit | _CONTEXT.md Scope |
| Intake filtration | Intake filter installation per MUA manufacturer specification — filter type, rating, and initial set TBD per DEL-003-07 / manufacturer manual | Enrichment C-003; ASSUMPTION |
| Supply ductwork | Main and branch supply ductwork throughout facility per design drawings | _CONTEXT.md Scope |
| Fire/smoke dampers | Installation at ductwork penetrations through fire-rated assemblies per code | Enrichment C-002; ASSUMPTION |
| Dampers and control valves | Installation at intake, supply terminals, and system junctions per design | _CONTEXT.md Scope |
| Ductwork insulation | Insulation of supply ductwork per DEL-003-07 specification and energy code — type, thickness, and vapor barrier TBD | Enrichment X-004; ASSUMPTION |
| Electrical disconnect | Installation of disconnect switch and lockout/tagout provisions per Alberta Electrical Code | Enrichment X-002; ASSUMPTION |
| Integration with heating | Physical and control integration with DEL-013-01 | _DEPENDENCIES.md Internal Package Dependencies |
| Integration with air exchanger | Coordination of intake locations and operating modes with DEL-013-02 | _DEPENDENCIES.md Critical Integration Points |
| Performance testing | System test and commissioning per mechanical engineer's requirements | _CONTEXT.md Scope; OBJ-004 |
| Code compliance | Installation to comply with Alberta Safety Codes and applicable mechanical codes | RFP §3.3.2; _CONTEXT.md Key Requirements |

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf — §3.4 Design Requirements | Lists high recovery heating, high volume air exchanger, exhaust systems as design requirements; Forced Air Makeup sourced from App B |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan; notes "Forced Air Makeup" as a building feature; shows equipment layout and space dimensions |
| Decomp | WDMLRL_Decomposition_Claude.md | SOW-0037: "Install forced-air makeup air system" (App B); PKG-013 narrative; Objectives OBJ-001, OBJ-004 |
| _CONTEXT.md | DEL-013-03 Context File | Deliverable identity, scope, key requirements, related deliverables |
| _DEPENDENCIES.md | DEL-013-03 Dependencies File | Upstream/downstream dependencies; constraint notes; critical integration points |
| _REFERENCES.md | DEL-013-03 References File | Standard references (ASHRAE, local code, equipment manufacturer specs — location TBD) |
| DEL-003-05 | Mechanical Equipment Schedule (design deliverable) | Will specify MUA unit make/model/capacity (not yet available) |
| DEL-003-06 | Mechanical Calculation Package (design deliverable) | Will establish required supply airflow rate, design temperatures (not yet available) |
| DEL-003-07 | Mechanical Specification (design deliverable) | Will specify installation standards and requirements (not yet available) |
