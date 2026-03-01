# Datasheet — DEL-012-03: Office Space

**Document Type:** Datasheet (descriptive)
**Deliverable ID:** DEL-012-03
**Package:** PKG-012 — Interior Construction & Fit-Out
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Revision:** R2 — 2026-02-26 (Pass 3 — Semantic Lensing Enrichment)
**Status:** SEMANTIC_READY

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-012-03 |
| Deliverable Name | Office Space |
| Package | PKG-012 — Interior Construction & Fit-Out |
| Deliverable Type | Construction |
| SOW Reference | SOW-0031 |
| Objective Linkage | OBJ-001 |
| Responsible Party | General Contractor |
| Activity | Construction |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Project Location | SW 14–44–21–W4, near Ferintosh, Alberta |

**Source:** _CONTEXT.md; WDMLRL_Decomposition_Claude.md §7 PKG-012 deliverable table

---

## Attributes

### Spatial Attributes

| Attribute | Value | Source |
|---|---|---|
| Room Type | Administrative office space | RFP §3.1; App B (Shop) |
| Location in Building | Lower section of new north shop, adjacent to Parts Room (DEL-012-01) | App B (Shop) floor plan |
| Approximate Floor Area | TBD — **Resolution trigger:** IFC architectural drawings from PKG-001 (Architect). Floor area is a critical datum driving lighting adequacy (see CONF-002 in Guidance.md), HVAC zoning, accessibility layout, and fixture/outlet count decisions. [Lensing: B-001] | App B (Shop) — dimensions not explicitly labelled for office footprint |
| Overall Building Useable Area | ~13,000 sq ft (entire new north shop addition) | RFP §3.1 |
| Ceiling Height | TBD (building structural ceiling 35' per §3.4; office may have suspended ceiling at lower height — ASSUMPTION) | RFP §3.4; App B (Shop) |

**Note (ASSUMPTION):** The office footprint area is not dimensioned on the conceptual floor plan (App B Shop). The floor plan shows a desk symbol and the label "Office" within a partitioned area adjacent to the Parts Room. Exact dimensions are subject to IFC architectural design.

### Electrical Attributes

| Attribute | Value | Source |
|---|---|---|
| Lighting fixture | 1× 8' LED strip fixture. **Adequacy basis: TBD** — lux level target for office workspace not yet established; IFC Electrical Engineer to verify fixture count against workplace lighting standards and confirmed office floor area (see CONF-002 in Guidance.md). [Lensing: B-002] | SOW-0054; App B (Electrical) electrical notes |
| Receptacle circuits (15A/120V) | Multiple 15A/120V receptacles shown on electrical plan. **Note:** The "(15)" notation on App B (Electrical) is **ambiguous** — it may denote 15-amp circuit type symbol designation or a quantity of 15 receptacles. **Resolution trigger:** reconcile with IFC electrical drawing to confirm receptacle count and circuit type. [Lensing: X-002] | App B (Electrical) floor plan — office area shows "(15)" symbols |
| Power supply | Three-phase service to building; branch circuits for office TBD per IFC electrical design | RFP §3.4; SOW-0051 |

### HVAC / Environmental Attributes

| Attribute | Value | Source |
|---|---|---|
| HVAC supply | Office zone served by PKG-013 mechanical systems | _DEPENDENCIES.md; WDMLRL_Decomposition_Claude.md PKG-013 |
| Heating | Connected to building heating system (DEL-013-01) | _DEPENDENCIES.md |
| Fresh air / ventilation | Served by air exchanger (DEL-013-02) and makeup air system (DEL-013-03) | _DEPENDENCIES.md |
| HVAC zoning details | TBD — subject to IFC mechanical design | _CONTEXT.md |
| Temperature control | Comfortable environmental conditions for occupancy (ASSUMPTION: thermostat control per zone) | _CONTEXT.md Key Requirements |

### Fit-Out Attributes

| Attribute | Value | Source |
|---|---|---|
| Wall systems | Interior partitions as shown on App B (Shop) floor plan | App B (Shop) |
| Floor finish | TBD — to be defined in IFC architectural finish schedule | _CONTEXT.md; RFP §3.3.2 |
| Ceiling finish | TBD — to be defined in IFC architectural reflected ceiling plans | _CONTEXT.md; RFP §3.3.2 |
| Door(s) | TBD — quantity and type per IFC door/window schedule. **Conceptual baseline:** App B (Shop) floor plan shows 1 entry door to the office. Confirm quantity, type, and hardware via IFC door/window schedule. [Lensing: X-003] | App B (Shop) — 1 entry shown on floor plan; no spec detail available |
| Data/communications points | TBD — low-voltage wiring under PKG-015; **target quantity: TBD** (no baseline count or minimum established). **Resolution trigger:** County / IFC low-voltage designer (PKG-015) to specify minimum data point count based on intended office use. [Lensing: X-001] | _CONTEXT.md; WDMLRL_Decomposition_Claude.md PKG-015 |
| Security camera wiring | ASSUMPTION: camera wiring stub-out in office area per PKG-015 low-voltage scope | App B (Electrical) notes — "Wiring for Security Cameras" listed |
| Furniture | Not in scope (ASSUMPTION: County-supplied) | Not referenced in RFP or decomposition |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Occupancy type | Administrative / office — staff workspace for facility management and operations | _CONTEXT.md Description |
| Occupancy load | TBD — **Resolution trigger:** IFC Architect (PKG-001) to confirm as part of code analysis. Occupancy load affects HVAC sizing, egress width requirements, and fire code provisions. [Lensing: B-003] | — |
| Accessibility | Must meet accessibility standards (ADA/Alberta equivalent) | _CONTEXT.md Key Requirements |
| Environmental comfort | Professional workplace environment with comfortable environmental conditions | _CONTEXT.md Key Requirements |
| Completion deadline | On or before December 31, 2026 | RFP §3.1 (bold statement); OBJ-002 |
| Warranty period | 2 years post-Construction Completion Certificate (CCC) | RFP §2.10.2 |
| Jurisdiction | Province of Alberta | RFP §2.22 |

---

## Construction

| Element | Value | Source |
|---|---|---|
| Structural shell | Provided by PKG-011 (Building Structure & Envelope) — concrete superstructure, 35' ceiling | WDMLRL_Decomposition_Claude.md PKG-011; RFP §3.4 |
| Interior partitions | Non-structural partition walls per IFC architectural design | _CONTEXT.md Scope; PKG-012 inclusion criteria |
| Floor finish | TBD per IFC finish schedule | — |
| Ceiling finish | TBD per IFC reflected ceiling plans | — |
| Electrical rough-in | Scope boundary between PKG-012 and PKG-015 **to be confirmed** in IFC design and contractor scope documents (see Guidance.md CONF-001). _CONTEXT.md lists "Electrical outlets and data points" under PKG-012 scope; decomposition assigns "all lighting, all receptacles" to PKG-015. ASSUMPTION: PKG-012 provides physical accommodation (partitions, framing, rough openings); PKG-015 performs device installation. [Lensing: B-004] | _CONTEXT.md Scope; _DEPENDENCIES.md; WDMLRL_Decomposition_Claude.md PKG-015 |
| HVAC rough-in / ductwork | Installed by PKG-013; office construction must accommodate duct penetrations and registers (ASSUMPTION) | _DEPENDENCIES.md; WDMLRL_Decomposition_Claude.md PKG-013 |
| Lighting installation | 1× 8' LED fixture — installation under PKG-015 (ASSUMPTION) | SOW-0054; App B (Electrical) |
| Safety and accessibility features | Per IFC architectural design and applicable Alberta Safety Codes | _CONTEXT.md Scope; RFP §3.3.2 |

**ASSUMPTION:** The boundary between PKG-012 (interior fit-out) and PKG-015 (electrical installation) for rough-in work within the office is to be confirmed in the IFC design and contractor scope documents. This document treats the physical partitions, finishes, and framing as PKG-012 scope, and luminaire/receptacle installation as PKG-015 scope.

---

## References

| Ref ID | Document | Sections Used |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §1.0, §3.1, §3.3.2, §3.4, §2.10.2, §2.22 |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Floor plan — office location, desk, adjacencies |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Electrical plan — office lighting and receptacles |
| — | WDMLRL_Decomposition_Claude.md | §5 OBJ-001; §6 PKG-012; §7 DEL-012-03; §8 Scope Ledger |
| — | _CONTEXT.md | Deliverable identity, scope, key requirements |
| — | _DEPENDENCIES.md | Upstream/downstream dependencies |
| — | _REFERENCES.md | Reference list |

### Documentation Artifacts (cross-referenced from Procedure.md Records)

| Artifact | Notes | Source |
|---|---|---|
| Photo Record | Construction progress photographs of office fit-out (ASSUMPTION: standard practice). Tracked in Procedure.md Records table. [Lensing: E-002] | Procedure.md Records |

**Reference Register Alignment Note [Lensing: E-003]:** This Datasheet references R-05 (AB-2026-01424-Appendix B Electrical), which is also cited extensively in Specification.md. However, _REFERENCES.md (Primary References) lists only R-01 and R-04. R-05 should be added to _REFERENCES.md for a complete and consistent reference register. This agent cannot modify _REFERENCES.md; this note is recorded for human/ORCHESTRATOR action.
