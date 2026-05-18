# Datasheet — DEL-013-02: High-Volume Air Exchanger

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-013-02 |
| **Title** | High-Volume Air Exchanger |
| **Package** | PKG-013 — Mechanical & HVAC Installation |
| **SOW Reference** | SOW-0036 |
| **Objective Linkage** | OBJ-001, OBJ-004 |
| **Type** | Mechanical & HVAC Installation |
| **Responsible Party** | Mechanical Contractor |
| **Activity** | Installation |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Equipment Type** | Heat Recovery Ventilator (HRV) / Energy Recovery Ventilator (ERV), high-volume commercial/industrial grade | ASSUMPTION — inferred from RFP §3.4 "high volume air exchanger" and _CONTEXT.md description |
| **Primary Function** | Exchange stale facility air with fresh outside air while recovering thermal energy | _CONTEXT.md — Description |
| **Air Exchange Capacity** | TBD — to be determined by Mechanical Engineer based on facility volume calculation | _CONTEXT.md — Key Requirements: "High-volume air exchange capability" |
| **Facility Floor Area** | Approximately 13,000 sq ft (130' × 100') | R-04 / Appendix B, shop floor plan |
| **Ceiling Height** | 35 ft | R-01 §3.4 (Design Requirements); R-04 / Appendix B |
| **Facility Volume (approximate)** | TBD — ASSUMPTION: approximately 455,000 cu ft based on ~13,000 sq ft × 35 ft ceiling. **Note:** Confirm whether interior partitions, mezzanine, or ceiling structure reduce the effective volume for ventilation calculation purposes. (Lensing item B-001) | Calculated from R-04 and RFP §3.4 — flagged as ASSUMPTION pending Mechanical Engineer confirmation in DEL-003-06 Calculation Package |
| **Heat Recovery Efficiency** | TBD — to be specified by Mechanical Engineer. A minimum numeric heat recovery efficiency target (percentage, sensible and/or total) is required for equipment selection and verification. No numeric target is stated in accessible sources. (Lensing item B-002) | ASSUMPTION — implied by RFP §3.4 "High recovery heating system" context and _CONTEXT.md; minimum efficiency to be specified in DEL-003-07 |
| **Fresh Air Intake** | Exterior wall penetration — location TBD (Mechanical Engineering design) | _DEPENDENCIES.md; R-04 (intake location shown on floor plan, specific coordinates TBD) |
| **Exhaust Outlet** | Exterior building envelope penetration — location TBD (Mechanical Engineering design) | _DEPENDENCIES.md |
| **Power Supply** | Three-phase power (building runs on three-phase per RFP §3.4) | R-01 §3.4: "The Proposed building shall run on three-phase power" |
| **Controls Integration** | Integrated with heating system controls (DEL-013-01) | _DEPENDENCIES.md — Critical Integration Points |
| **Installation Location** | Utility Room | _CONTEXT.md Scope; _DEPENDENCIES.md: DEL-012-02 Utility Room |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| **Climate / Location** | Rural Alberta — SW 14-44-21-W4, near Ferintosh, AB; cold continental climate with significant winter heating demand | R-01 §1.0 Introduction; R-07 (Site Maps) |
| **Indoor Environment** | Heavy-duty maintenance shop — diesel/gasoline equipment, welding fumes, exhaust gases, particulates | R-01 §3.4 (exhaust hoses and fans for heavy equipment, welding station exhaust); R-04 Appendix B |
| **Operating Temperature Range** | TBD — Alberta climate range (approximately −40°C to +35°C ambient); unit must be rated for cold-climate operation | ASSUMPTION — based on location; manufacturer specification TBD |
| **Ventilation Demand** | High — facility houses heavy equipment repair bays, wash bay, welding station; multiple exhaust and contaminant sources | R-01 §3.4; R-04 Appendix B |
| **Occupancy Type** | Industrial maintenance shop (heavy equipment maintenance, welding, vehicle repair) | R-01 §3.1 Project Background; R-04 Appendix B |
| **Code Jurisdiction** | Province of Alberta — Alberta Safety Codes Act, Alberta Building Code (ABC), National Building Code (NBC) | R-01 §3.3.2: "The proposed building must adhere to all Alberta Safety Codes" |

---

## Construction

| Item | Detail | Source |
|---|---|---|
| **Equipment Supply** | Mechanical Contractor responsible for procurement and delivery | _CONTEXT.md Scope |
| **Mounting / Housing** | Installed in Utility Room; structural support per manufacturer requirements — details TBD pending mechanical design | _CONTEXT.md Scope; _DEPENDENCIES.md |
| **Fresh Air Intake Ductwork** | From equipment to exterior wall penetration — sizing, material, and routing TBD | _CONTEXT.md Scope |
| **Exhaust Outlet Ductwork** | From equipment to exterior building envelope penetration — sizing, material, and routing TBD | _CONTEXT.md Scope |
| **Integration with Heating System** | Supply connection to DEL-013-01 (High-Recovery Heating System) — interface details TBD pending mechanical design | _CONTEXT.md Scope; _DEPENDENCIES.md |
| **Controls and Sensors** | Controls and sensor setup included in scope — type and configuration TBD | _CONTEXT.md Scope |
| **Coordination with Makeup Air** | Fresh air supply points coordinated with DEL-013-03 (Forced-Air Makeup System) | _DEPENDENCIES.md |
| **Coordination with Exhaust Systems** | Stale air collection coordinated with DEL-013-04 (Heavy Equipment Exhaust) and DEL-013-05 (Welding Station Exhaust) | _DEPENDENCIES.md |
| **Wall/Building Penetrations** | Facility exterior wall penetrations required for both intake and exhaust; location must avoid contamination re-entrainment | _DEPENDENCIES.md — Constraint Notes |
| **Commissioning** | Performance testing and commissioning included in scope | _CONTEXT.md Scope |
| **Warranty** | Two (2) year guarantee period post Construction Completion Certificate (CCC) | R-01 §2.10 Guarantee Period |

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL_RFP.pdf — §3.4 Design Requirements; §3.3.2 Scope of Work; §2.10 Guarantee Period | Primary project scope and contractual requirements |
| R-04 | AB-2026-01424-Appendix_B_(Shop).pdf — New North Shop floor plan | Facility dimensions, Utility Room location, equipment placement context |
| Decomposition | WDMLRL_Decomposition_Claude.md — PKG-013, DEL-013-02, SOW-0036, OBJ-001, OBJ-004 | Deliverable identity, objectives, and package context |
| _CONTEXT.md | DEL-013-02 — Deliverable identity, scope, key requirements | Deliverable definition |
| _DEPENDENCIES.md | DEL-013-02 — Upstream/downstream dependencies and integration constraints | Interface and coordination requirements |
| Standard (TBD) | ASHRAE 62.1 — Ventilation for Acceptable Indoor Air Quality | ASSUMPTION: likely applicable; location TBD — not confirmed against accessible source text |
| Standard (TBD) | ASHRAE 90.1 or NRCan energy efficiency requirements for HRV/ERV | ASSUMPTION: likely applicable; location TBD |
| Standard (TBD) | Alberta Mechanical Code / National Mechanical Code of Canada | ASSUMPTION: likely applicable; location TBD |
| Standard (TBD) | Manufacturer installation instructions and specifications | TBD — equipment not yet selected |
