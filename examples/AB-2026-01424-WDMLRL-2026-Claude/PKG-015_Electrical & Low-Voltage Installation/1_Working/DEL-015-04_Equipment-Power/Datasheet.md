# Datasheet — DEL-015-04 Equipment Power Circuits

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-015-04 |
| **Title** | Equipment Power Circuits |
| **Package** | PKG-015 — Electrical & Low-Voltage Installation |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Responsible Party** | Electrical Contractor |
| **Work Type** | Installation (Construction) |
| **Deliverable Type** | Installation |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |

**Sources:** _CONTEXT.md; Decomposition §7 PKG-015; RFP §1.0, §3.1

---

## Attributes

### Equipment Circuits Summary

The following dedicated power circuits are within scope for this deliverable. Values are drawn directly from App B (Electrical) and the decomposition SSOW.

| Circuit ID | Equipment / Load | Amperage | Voltage | SOW Ref | Source |
|---|---|---|---|---|---|
| C-01 | Overhead Crane #1 (5-tonne) | TBD — source: crane manufacturer via DEL-016-01 procurement | TBD (three-phase) — source: crane manufacturer via DEL-016-01 procurement | SOW-0059 | App B-Elec |
| C-02 | Overhead Crane #2 (5-tonne) | TBD — source: crane manufacturer via DEL-016-01 procurement | TBD (three-phase) — source: crane manufacturer via DEL-016-01 procurement | SOW-0059 | App B-Elec |
| C-03 | Overhead Doors — TBD: enumerate individual door circuits (count TBD per architectural drawings / DEL-004-02) | TBD | TBD | SOW-0060 | App B-Elec |
| C-04 | Air Compressor | 40 A | TBD — source: equipment nameplate / Electrical Engineer | SOW-0061 | App B-Elec |
| C-05 | Fire Hose Pump | 70 A | TBD — source: equipment nameplate / Electrical Engineer | SOW-0062 | App B-Elec |
| C-06 | Pressure Washer | 70 A | TBD — source: equipment nameplate / Electrical Engineer | SOW-0063 | App B-Elec |
| C-07 | Exhaust Fan(s) | TBD | TBD | SOW-0066 | App B-Elec |

**Notes:**
- **[B-001]** Crane circuit voltage and amperage (C-01, C-02) are TBD pending crane manufacturer specifications via DEL-016-01 procurement. Cannot proceed to IFC without this data. ASSUMPTION: three-phase supply consistent with the building three-phase service (SOW-0051).
- **[B-002]** Voltage for circuits C-04 (compressor 40 A), C-05 (fire hose pump 70 A), and C-06 (pressure washer 70 A) is TBD — required for conductor sizing and breaker selection. Source: equipment nameplates / Electrical Engineer. ASSUMPTION: likely 240 V single-phase or three-phase per equipment specifications.
- **[B-003]** Overhead door circuit entry C-03 currently aggregates "all" overhead doors as one entry. TBD: the number of overhead doors requiring power circuits must be confirmed and each circuit enumerated individually. Source: architectural drawings / DEL-004-02. App B-Elec indicates doors are powered; legend shows 20A 240V receptacles near door locations (ASSUMPTION: not confirmed as the dedicated circuit rating).
- Exhaust fan(s) quantity and circuit rating are TBD pending IFC electrical design. App B-Elec shows "E" (exhaust fan) symbol at the welding station area.

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| **Governing jurisdiction** | Alberta, Canada | RFP §2.22 |
| **Applicable codes** | Alberta Safety Codes Act; Canadian Electrical Code (CEC) Part I — ASSUMPTION: likely applicable; location TBD in IFC documents | RFP §3.3.2, §3.4 |
| **Building power supply** | Three-phase (voltage TBD) | RFP §3.4; SOW-0051 |
| **Upstream dependency** | DEL-015-01 (Three-Phase Power Service) must be complete before equipment circuits can be energized | _DEPENDENCIES.md |
| **Equipment specifications** | Owner / equipment suppliers to confirm load data for cranes, overhead doors, compressor, fire hose pump, pressure washer, exhaust fans | _DEPENDENCIES.md (external) |
| **IFC drawings required** | Final electrical design (DEL-004-02 through DEL-004-06) must be P.Eng.-stamped and Issued for Construction before installation proceeds | RFP §3.3.2; SOW-0018 |
| **Inspection requirement** | Safety Code inspections required; County project representative to be present at inspections; notification timeline and confirmation requirements TBD per RFP §3.3.2 / Project Manager. Copies of reports provided to Owner | RFP §3.3.2; SOW-0084, SOW-0085 |
| **Completion deadline** | December 31, 2026 | RFP §3.1 |
| **Warranty / Guarantee period** | Construction period + 2 years post-CCC | RFP §2.10 |

---

## Construction

| Item | Description | Source |
|---|---|---|
| **Circuit type** | Dedicated branch circuits for each equipment load | App B-Elec (implied); ASSUMPTION |
| **Wiring method** | TBD — to be determined per IFC electrical design and CEC requirements. Expected source: IFC Electrical Design (DEL-004-02) | TBD |
| **Conduit / raceway** | TBD — expected source: IFC Electrical Design (DEL-004-02) | TBD |
| **Overcurrent protection** | Per circuit amperage ratings listed under Attributes; exact breaker sizes per IFC panel schedules (DEL-004-06) | App B-Elec; TBD |
| **Disconnecting means** | TBD — required per CEC for motor loads (cranes, compressor, pumps, fans) — ASSUMPTION: individual disconnects required per CEC Part I rules for motors | ASSUMPTION based on CEC typical requirements |
| **Panel / distribution board** | TBD — which distribution panel(s) and whether single or multiple panels. Source: IFC panel schedules (DEL-004-06) | TBD |
| **Conductor sizing** | TBD — per IFC design based on load calculations (DEL-004-08) | TBD |
| **Grounding and bonding** | TBD — per CEC requirements — ASSUMPTION: required for all equipment circuits | ASSUMPTION |
| **Crane runway power supply** | TBD — typical methods include festoon cable, conductor bar, or bus duct; method to be specified in IFC design | ASSUMPTION: standard industrial practice |

---

## Materials and Equipment

**[X-002]** TBD — No materials/equipment list or bill of materials reference currently exists. A materials and equipment list identifying major components should be provided or referenced once the IFC electrical design is available. Expected content includes:

- Circuit breakers (types and ratings per IFC panel schedules)
- Motor disconnects (type, rating, and quantity per circuit count)
- Conduit / raceway (type, size, and quantity per IFC routing)
- Conductors (type, gauge, and length per IFC design and DEL-004-08 calculations)
- Crane runway power supply components (conductor bar, festoon cable, or bus duct per IFC design and crane manufacturer requirements)
- Terminal lugs, connectors, and associated hardware

**Source:** TBD — IFC Electrical Design (DEL-004-02, DEL-004-06); **location TBD**

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL_RFP.pdf | §3.4 design requirements; §3.3.2 scope of work |
| R-05 | AB-2026-01424-Appendix_B__Electrical_.pdf | Conceptual electrical layout showing equipment circuit callouts |
| Decomposition | WDMLRL_Decomposition_Claude.md | §3.G (SOW-0059–0066); §7 PKG-015; §5 OBJ-001, OBJ-005 |
| _CONTEXT.md | DEL-015-04 Context | Deliverable identity, scope, SOW references |
| _DEPENDENCIES.md | DEL-015-04 Dependencies | Upstream: DEL-015-01; Downstream: DEL-015-05 |
| DEL-004-02 | Electrical Power Distribution Plans (TBD — not yet issued) | Will specify wiring methods, conduit routing, and circuit layouts |
| DEL-004-06 | Panel Schedules (TBD — not yet issued) | Will specify circuit breaker ratings and panel assignments |
| DEL-004-08 | Electrical Calculation Package (TBD — not yet issued) | Will specify conductor sizing and load calculations |
| DEL-016-01 | Crane Procurement (TBD — not yet complete) | Will provide crane manufacturer electrical requirements (voltage, amperage, supply method) |
