# Datasheet — DEL-015-02 Lighting Installation

**Deliverable ID:** DEL-015-02
**Title:** Lighting Installation
**Package:** PKG-015 — Electrical & Low-Voltage Installation
**Contractor:** Electrical Contractor
**Work Type:** Installation
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Document Status:** SEMANTIC_READY (Pass 3 enrichment applied)
**Prepared By:** 4_DOCUMENTS Agent
**Date:** 2026-02-26

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-015-02 |
| Deliverable Title | Lighting Installation |
| Package ID | PKG-015 |
| Package Title | Electrical & Low-Voltage Installation |
| Responsible Party | Electrical Contractor |
| Delivery Type | Installation |
| Project Contract Form | CCDC 14–2013 Design-Build Stipulated Price |
| Project Completion Deadline | December 31, 2026 |
| Governing Jurisdiction | Province of Alberta |
| Related SOWs | SOW-0052, SOW-0053, SOW-0054, SOW-0055, SOW-0056 |
| Objectives Addressed | OBJ-001, OBJ-005 |
| Upstream Dependency | DEL-015-01 (Three-Phase Power Service) |
| Downstream Dependency | None declared |

*Sources: _CONTEXT.md; Decomposition §7 PKG-015; _DEPENDENCIES.md*

---

## Attributes

### Lighting Zones and Fixture Schedule

| Zone | Room / Area | Fixture Type | Qty | Wattage | Lumen Output | SOW Ref | Source |
|---|---|---|---|---|---|---|---|
| Z-1 | Main Shop | High Bay LED | 20 (5 rows x 4) | 150 W each | 22,000 lm each | SOW-0052 | App B-Elec; Decomp §3 SOW-0052 |
| Z-2 | Wash Bay | High Bay LED | 6 (2 rows x 3) | TBD — pending IFC design by EOR | TBD — pending IFC design by EOR | SOW-0053 | App B-Elec; Decomp §3 SOW-0053 |
| Z-3 | Office | 8-foot LED linear fixture | 1 | TBD — pending IFC design by EOR | TBD — pending IFC design by EOR | SOW-0054 | App B-Elec; Decomp §3 SOW-0054 |
| Z-4 | Utility Room | 8-foot LED linear fixture | 2 | TBD — pending IFC design by EOR | TBD — pending IFC design by EOR | SOW-0055 | App B-Elec; Decomp §3 SOW-0055 |
| Z-5 | Parts / Tool Room | 8-foot LED linear fixture | 6 | TBD — pending IFC design by EOR | TBD — pending IFC design by EOR | SOW-0056 | App B-Elec; Decomp §3 SOW-0056 |

**Total fixture count:** 35 (20 + 6 + 1 + 2 + 6; arithmetic sum of zone quantities above)
**Total high-bay fixtures:** 26
**Total 8-foot LED linear fixtures:** 9

> **Resolution milestone for Z-2 through Z-5 performance data:** Wattage and lumen output for Z-2 through Z-5 are not explicitly stated in the source documents; Main Shop high bays are the only fixtures with explicit specifications (150 W, 22,000 lm) per App B-Elec Electrical Notes. These values shall be established by the Electrical Engineer of Record (EOR) in the IFC electrical drawings. *(Enrichment: B-001, B-004; sources: App B-Elec Electrical Notes; Decomp §3 SOW-0052 through SOW-0056)*

### Building Context (relevant to lighting)

| Attribute | Value | Source |
|---|---|---|
| Main Shop ceiling height | 35 feet (concrete structure) | RFP §3.4; App B-Elec |
| Building footprint | ~130' x 100' (New North Shop area) | App B-Elec drawing dimensions |
| Wash Bay width | 24' (as shown on drawing) | App B-Elec |
| Office location | South side of New North Shop | App B-Elec floor plan |
| Utility Room location | South side, adjacent to Parts Room | App B-Elec floor plan |
| Parts / Tool Room location | South side, 16' wide bay | App B-Elec floor plan |
| Main Shop crane clearance | 2 x 5-tonne overhead cranes on trolley | RFP §3.4; App B-Elec |
| Power supply | Three-phase (per DEL-015-01) | RFP §3.4 |

---

## Conditions

| Condition | Description | Source |
|---|---|---|
| Installation environment | Industrial maintenance shop — heavy equipment, overhead cranes, wash bay (wet area) | RFP §3.1; App B-Elec |
| Ceiling height (Main Shop) | 35 feet — requires high-bay fixtures with appropriate mounting hardware | RFP §3.4 |
| Crane interference | Overhead crane rails present in Main Shop — fixture layout must coordinate with crane travel path | App B-Elec; ASSUMPTION |
| Wash Bay moisture | Wash Bay is a wet/damp location — fixtures in Z-2 must be rated for wet or damp environments | ASSUMPTION (standard practice for wash bay installations) |
| Operating environment | Landfill maintenance facility — dust, vehicle exhaust, potential chemical exposure | RFP §3.1; ASSUMPTION |
| Electrical supply | Three-phase power service; individual lighting circuit voltages TBD per final electrical design | ASSUMPTION |
| Completion deadline | All work complete on or before December 31, 2026 | RFP §3.1 |
| Warranty period | 2 years following Construction Completion Certificate (CCC) | RFP §2.10 |

---

## Construction

| Attribute | Description | Source |
|---|---|---|
| Fixture type — Main Shop | LED high-bay, 150 W, 22,000 lumens minimum | App B-Elec Electrical Notes; SOW-0052 |
| Fixture type — Wash Bay | LED high-bay (wattage/lumens TBD — pending IFC design by EOR) | App B-Elec Electrical Notes; SOW-0053 |
| Fixture type — Office/Utility/Parts | 8-foot LED linear fixture (exact model TBD per final design) | App B-Elec Electrical Notes; SOW-0054, SOW-0055, SOW-0056 |
| Mounting method — Main Shop / Wash Bay | TBD — pendant, chain, or aircraft cable mount to be specified by EOR in IFC drawings. Selection depends on ceiling height, structural attachment points, and crane clearance requirements (Main Shop). *(Enrichment: D-001; source: ASSUMPTION; resolution milestone: IFC drawing issuance)* | ASSUMPTION |
| Mounting method — Office/Utility/Parts | TBD per IFC design (surface or suspended, per ceiling type in each room) | ASSUMPTION |
| Wiring | Branch circuit wiring per final electrical drawings — TBD | ASSUMPTION |
| Controls / switching | TBD — not explicitly specified in source documents. Decision owner: Owner (to select strategy); EOR (to implement in IFC drawings). Resolution milestone: IFC drawing issuance. Options may include manual switching, occupancy sensing, or daylight harvesting — see Guidance C-3. *(Enrichment: B-003; sources: App B-Elec conceptual drawing shows no switch locations; Specification REQ-L-14 TBD; Guidance C-3)* | TBD |
| Dimming / occupancy sensing | Not specified in source documents — see Controls/switching above | TBD |
| Emergency lighting | Not explicitly specified — TBD; likely required by Alberta Safety Codes. See Specification §Scope and Guidance CONF-L-02 for scope determination. | ASSUMPTION |
| Conduit type | TBD per final electrical design | TBD |
| Panel / circuit assignments | TBD per final electrical design | TBD |
| Circuit breaker sizes | TBD per final electrical design | TBD |

### Unresolved Design Parameters Register

The following design parameters are TBD and require resolution by the identified authority before the corresponding installation phase can proceed. *(Enrichment: B-002; source: compilation from Datasheet §Construction TBD entries)*

| Parameter | Current State | Resolution Authority | Resolution Milestone | Impacts |
|---|---|---|---|---|
| Wash Bay fixture wattage/lumens (Z-2) | TBD | EOR | IFC drawings | Spec REQ-L-04; Procurement |
| 8-foot fixture model selection (Z-3, Z-4, Z-5) | TBD | EOR | IFC drawings | Procurement |
| Mounting method (all zones) | TBD | EOR | IFC drawings | Procurement; installation |
| Controls / switching strategy | TBD | Owner decision; EOR implementation | IFC drawings | Spec REQ-L-14; Procedure Phase 2 Step 7 |
| Conduit type | TBD | EOR | IFC drawings | Procurement; rough-in |
| Panel / circuit assignments | TBD | EOR | IFC drawings | Rough-in; terminations |
| Circuit breaker sizes | TBD | EOR | IFC drawings | Panel capacity; procurement |
| Emergency lighting scope | TBD | Owner + AHJ | Permit application | Spec §Scope; procurement |

---

## References

| Ref ID | Document | Section / Notes |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.1 (Project Background), §3.4 (Design Requirements) |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Electrical layout drawing, Electrical Notes, fixture legend |
| Decomp | WDMLRL_Decomposition_Claude.md | §3 SSOW (SOW-0052–0056), §7 DEL-015-02, §5 OBJ-001 / OBJ-005 |
| _CONTEXT.md | DEL-015-02_Lighting Context | Deliverable overview and scope |
| _DEPENDENCIES.md | DEL-015-02_Lighting Dependencies | Upstream: DEL-015-01 |
