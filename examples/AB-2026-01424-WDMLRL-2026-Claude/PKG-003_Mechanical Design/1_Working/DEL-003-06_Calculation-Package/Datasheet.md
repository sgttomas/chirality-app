# Datasheet — DEL-003-06 Mechanical Calculation Package

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-003-06 |
| **Deliverable Name** | Mechanical Calculation Package |
| **Package** | PKG-003 — Mechanical Design |
| **Discipline** | Mechanical Engineering |
| **Type** | Calculation Package |
| **Responsible Party** | Mechanical Engineer |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |
| **SOW Coverage** | SOW-0013 (Complete final mechanical design — HVAC, ventilation, exhaust systems) |
| **Objectives Supported** | OBJ-003 (IFC design documentation), OBJ-004 (mechanical/HVAC operational readiness) |
| **Status** | SEMANTIC_READY |

> **[Enrichment E-001]:** Status normalized to match _STATUS.md current state (was "INITIALIZED"; _STATUS.md records "SEMANTIC_READY" as of 2026-02-26). Source: _STATUS.md.

---

## Attributes

### Building — Physical Parameters

| Parameter | Value | Source |
|---|---|---|
| Building footprint (Addition) | ~13,000 sq ft useable area (conceptual: 130 ft x 100 ft) | R-01 S3.1; R-04 App B |
| Ceiling height (Addition — main shop) | 35 ft | R-01 S3.4; R-04 App B |
| Building type | Industrial maintenance shop (concrete structure) | R-01 S3.4 |
| Occupancy | Landfill maintenance operations; heavy equipment servicing, welding, vehicle washing | R-01 S3.1, S3.4 |
| Number of drive-through repair bays | 2 (each 24 ft wide per drawing) | R-01 S3.1; R-04 App B |
| Wash bay | 1 enclosed bay, motor-scraper sized (24 ft wide per drawing) | R-01 S3.1, S3.4; R-04 App B |
| Service pit/trench | 1, ventilated and lighted, for under-equipment servicing | R-01 S3.4; R-04 App B |
| Parts storage room | ~400 sq ft, secure, 6 ft roll-up door | R-01 S3.4; R-04 App B |
| Utility room | Present (dimensions TBD — not stated in accessible sources; **required input for zone-by-zone ventilation calculation per REQ-M-003**) | R-01 S3.1; R-04 App B; [Enrichment B-002] |
| Office space | Present (dimensions TBD — not stated in accessible sources; **required input for zone-by-zone ventilation calculation per REQ-M-003**) | R-01 S3.1; R-04 App B; [Enrichment B-002] |
| Mezzanine | Above parts room, utility room, and wash bay; load-bearing (oil totes, pump equipment) | R-01 S3.4; R-04 App B |
| Renovation area (Old North Shop) | 105 ft x 40 ft existing building (partial renovation) | R-04 App B |
| Site location | Camrose County, Alberta (~30 km south of Camrose) | R-01 S1.0 |

> **[Enrichment B-002]:** Office and utility room dimensions are flagged as required inputs for REQ-M-003 zone-by-zone ventilation. Source: Specification.md REQ-M-003; Datasheet.md Building Physical Parameters. PROPOSAL: Obtain from confirmed architectural drawings (PKG-001) or field measurement per App B.

### Mechanical Systems — Inventory

| System | Description | Source |
|---|---|---|
| High-Recovery Heating System | Space heating for the addition; type/capacity TBD pending design | R-01 S3.4; SOW-0035 |
| High-Volume Air Exchanger | Building air exchange/ventilation; capacity TBD. **Note: role delineation with MUA is unresolved (see Guidance CON-M-002)** | R-01 S3.4; SOW-0036; [Enrichment E-005] |
| Forced-Air Makeup Air Unit (MUA) | Tempered fresh air replacement; capacity TBD | R-04 App B; SOW-0037 |
| Heavy Equipment Exhaust System | Exhaust hose(s) and fan(s) serving repair bays; **number of exhaust drops per bay: TBD — not specified in RFP (required input: directly affects exhaust flow rate and MUA sizing; see REQ-M-005)** | R-01 S3.4; SOW-0038; [Enrichment F-003] |
| Welding Station Exhaust/Ventilation | Dedicated ventilation at welding station | R-01 S3.4; R-04 App B; SOW-0039 |
| Ceiling Fans | 6 ceiling fans in main shop area. **Basis for quantity of 6: TBD — not documented in accessible sources (see Guidance A-005 rationale gap)** | R-04 App B-Elec (per decomposition SOW-0040); SOW-0040; [Enrichment A-005] |
| Service Pit Ventilation | Integrated with service pit — ventilation required | R-01 S3.4; R-04 App B; SOW-0028 |

> **[Enrichment F-003]:** Exhaust drops per bay is an indispensable process input. If each bay has 2 drops rather than 1, exhaust flow doubles, affecting MUA sizing and system balance. Source: Specification.md REQ-M-005; Procedure.md Step 5.1. PROPOSAL: Design decision by Mechanical Engineer or RFI to Owner for operational requirements.

> **[Enrichment A-005]:** Ceiling fan quantity (6) is not traced to coverage area analysis, manufacturer recommendation, or Owner preference in accessible sources. Source: Guidance.md C-01; Datasheet.md Mechanical Systems Inventory. PROPOSAL: Mechanical Engineer to document basis for fan quantity in calculation package.

### Calculation Subjects

| Calculation Subject | Status | Target Range / Preliminary Estimate |
|---|---|---|
| Heating load (building heat loss) | TBD — requires building envelope U-values, climate data | TBD — **requires envelope U-values from PKG-001/PKG-002 before calculation can proceed** |
| Makeup air sizing (flow rate, tempered capacity) | TBD — requires infiltration and exhaust balancing | TBD |
| Air exchanger sizing (ACH, exhaust vs. supply balance) | TBD | TBD |
| Heavy equipment exhaust sizing (fan curves, duct routing) | TBD | TBD |
| Welding exhaust sizing (capture velocity, hood design) | TBD | TBD — **PRELIMINARY until County welding specs (SOW-0204) received** |
| Service pit ventilation sizing | TBD | TBD |
| Ceiling fan selection and layout | TBD | TBD |
| Energy balance / system coordination | TBD | TBD |

> **[Enrichment E-002]:** Target Range / Preliminary Estimate column added. All values remain TBD because no source provides order-of-magnitude estimates at this stage. PROPOSAL: Mechanical Engineer to add preliminary target ranges after initial design development. Source: Datasheet.md Calculation Subjects.

> **[Enrichment B-001]:** Building envelope U-values (wall, roof, slab, window, door assemblies) are essential input data not yet available. Heating load calculation (REQ-M-001) cannot proceed without these. Source: Datasheet.md Conditions; Specification.md REQ-M-001. PROPOSAL: Obtain from Architectural (PKG-001) and Structural (PKG-002) packages.

---

## Conditions

| Condition | Value / Status | Source |
|---|---|---|
| Climate zone | Alberta, Central region; **design heating temperature: TBD (ASSUMPTION: approximately -35C or colder per NBCC/Alberta practice for nearest station to Ferintosh, AB — specific value required for REQ-M-001; see Enrichment A-001)** | R-01 S1.0; ASSUMPTION; [Enrichment A-001] |
| Building envelope U-values | **TBD — wall, roof, slab, window, and door assembly U-values are essential inputs not yet available. Source: PKG-001 (Architectural) and PKG-002 (Structural)** | [Enrichment B-001] |
| Fuel/energy source | Natural gas (ASSUMPTION — natural gas tie-in is in scope; building runs on three-phase power) | R-01 S3.3.2, S3.4; ASSUMPTION |
| Welding equipment specifications | To be supplied by County (County responsibility per decomposition). **RFI timeline: TBD — no expected receipt date or escalation path recorded (see Enrichment B-003)** | R-01 S3.4; SOW-0204 (OUT of Design-Builder scope for supply); [Enrichment B-003] |
| Geotechnical influence on mechanical | Foundation type affects utility routing; geotech report (DEL-008-01) not yet available | Decomposition S7 PKG-008 |
| Three-phase power available | Yes — three-phase power distribution is in scope | R-01 S3.4; SOW-0051 |
| Ventilated service pit | Required; ventilation integrated with mechanical design | R-01 S3.4; SOW-0028 |

> **[Enrichment A-001]:** Design outdoor heating temperature requires commitment to a specific value from NBCC climate data tables. Multiple documents reference "approximately -35C or colder" as assumption, but no document commits to a specific value, which could change equipment sizing. Source: Specification.md REQ-M-001; Datasheet.md Conditions. PROPOSAL: Mechanical Engineer to confirm from NBCC climate data tables for nearest station to Ferintosh, AB.

> **[Enrichment B-003]:** County welding equipment specifications (SOW-0204) lack an expected receipt date or escalation path. Multiple documents note this dependency (Guidance P-03, Procedure Step 6, Specification REQ-M-006) but no document records the RFI timeline. Source: Specification.md REQ-M-006; Guidance.md P-03; Procedure.md Step 6. PROPOSAL: Project Manager to issue RFI and track response timeline.

---

## Construction (Package Context)

| Aspect | Detail | Source |
|---|---|---|
| Installed by | PKG-013 — Mechanical & HVAC Installation (Mechanical Contractor) | Decomposition S6 |
| Commissioning | PKG-020 — Building Systems Commissioning (post-installation) | Decomposition S6 |
| Drawing set relationship | This calculation package supports DEL-003-02 (HVAC Plans), DEL-003-03 (Ductwork Plans), DEL-003-04 (Exhaust Plans), DEL-003-05 (Equipment Schedule), DEL-003-07 (Mechanical Specification) | Decomposition S7 PKG-003 |
| IFC stamp requirement | All IFC drawings must be signed/stamped by a P.Eng. licensed in Alberta | R-01 S3.3.2; SOW-0018 |
| Preliminary design approval | Calculation package follows approval of DEL-003-01 (Preliminary Mechanical Design) | Decomposition S7 PKG-003 |

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Primary RFP — S1.0 (project overview), S3.1 (project background), S3.3.2 (scope), S3.4 (design requirements) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan — mechanical equipment locations, systems noted |
| Decomp | WDMLRL_Decomposition_Claude.md | SOW-0013, SOW-0035–0040, PKG-003, DEL-003-06 entry, OBJ-003, OBJ-004 |
| TBD | ASHRAE Handbook of Fundamentals (current edition) | Heating load calculations; design conditions (location TBD — ASSUMPTION: applicable) |
| TBD | ASHRAE 62.1 — Ventilation for Acceptable Indoor Air Quality | Ventilation rate determination (location TBD — ASSUMPTION: applicable) |
| TBD | Alberta Building Code (current edition) | Code-compliant ventilation, exhaust, and combustion air requirements (location TBD — ASSUMPTION: applicable) |
| TBD | SMACNA HVAC Duct Construction Standards | Ductwork design (location TBD — ASSUMPTION: applicable) |
| TBD | AMCA standards | Fan selection and performance (location TBD — ASSUMPTION: applicable) |
| TBD | ACGIH Industrial Ventilation Manual | Welding exhaust and industrial ventilation design (location TBD — ASSUMPTION: applicable) |
