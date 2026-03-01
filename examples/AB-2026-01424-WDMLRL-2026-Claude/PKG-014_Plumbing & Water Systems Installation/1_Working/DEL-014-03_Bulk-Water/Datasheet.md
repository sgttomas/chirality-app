# Datasheet — DEL-014-03 Bulk Water Fill System

**Document Type:** Datasheet (descriptive)
**Deliverable ID:** DEL-014-03
**Package:** PKG-014 — Plumbing & Water Systems Installation
**Revision:** R1 — 2026-02-26
**Status:** SEMANTIC_READY
**Enrichment Pass:** P3 (Semantic Lensing applied)

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-014-03 |
| Title | Bulk Water Fill System |
| Package | PKG-014 — Plumbing & Water Systems Installation |
| Contractor | Plumbing Contractor |
| Work Type | Installation |
| SOW Reference | SOW-0044 |
| Objectives Supported | OBJ-001, OBJ-004 |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Location | SW 14-44-21-W4, near Ferintosh, Alberta |
| Contract Form | CCDC 14-2013 Design-Build Stipulated Price Contract |
| Completion Deadline | December 31, 2026 |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| System Type | Bulk water fill with high-volume pump for external filling | RFP S3.4 |
| Primary Function | Provide a high-volume external fill point for bulk water delivery vehicles to replenish the 50,000L cistern. **Note:** RFP S3.4 states "bulk water fill... with high volume pump for external filling." The directional language ("filling") suggests the primary function is cistern replenishment from external delivery vehicles. Whether the system must also support *extraction* (pumping water from the cistern to vehicles) is unresolved -- see Conflict Table entry C-003 in Guidance.md. **TBD -- Owner/PM to confirm whether extraction (cistern-to-vehicle) is in scope for DEL-014-03.** | RFP S3.4; Guidance.md Conflict Table C-003 (E-004) |
| Pump Type | High-volume pump | RFP S3.4 |
| Pump Flow Rate | **TBD** — RFP requires "high volume" for external filling; specific LPM rating not stated for bulk fill (the 100 LPM / 2.5" connection stated in S3.4 is for the internal distribution pump, SOW-0042/DEL-014-01). **This is the most critical performance datum for this system; without it, pump selection, procurement, and acceptance testing cannot proceed. Plumbing engineer (PKG-006 IFC design) to confirm.** | RFP S3.4; Semantic Lensing B-001 |
| Fill Connection Size | **TBD** — not explicitly stated for the bulk fill point; design to confirm. To be resolved in PKG-006 IFC design and added to this Datasheet when available. | RFP S3.4; location TBD in plumbing design documents |
| Fill Point Location | Exterior of building — shown on Appendix B (Plumbing) conceptual drawing as "Bulk Water Fill" on the north/exterior face of the building. **Note:** This refers to the fill *connection point* location, not the pump location. Pump location (indoor vs. outdoor) is a separate design decision -- see Guidance.md T-1 and Conflict Table C-004. | R-06 (App B Plumbing); Specification REQ-014-03-03 |
| Integration Point | 50,000L cistern (DEL-014-01); fill line connects to cistern | _CONTEXT.md; R-06 |
| Power Supply Requirement | Electrical power required for pump motor — coordination with PKG-015 required | ASSUMPTION — standard for pump installations |
| Freeze Protection | **TBD** — Alberta climate requires consideration; design engineer to specify heat tracing or drainage provisions | ASSUMPTION — applicable to exterior Alberta installations |
| Backflow Prevention | **TBD** — required per Alberta Safety Codes (applicable plumbing code edition TBD -- see Specification Standards table); design to specify device type and location | ASSUMPTION — standard plumbing code requirement |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Project Location | Rural Alberta landfill site, near Ferintosh; off municipal water supply | RFP S3.1 |
| Climate Zone | Alberta Central region; subject to freeze-thaw cycles and sub-zero winter temperatures | RFP S1.0; ASSUMPTION |
| Water Supply Source | Bulk water delivered by tanker truck or similar vehicle to the external fill point | ASSUMPTION — consistent with cistern-based water supply system at rural site |
| Cistern Upstream Dependency | DEL-014-01 (50,000L Cistern & Distribution) must be installed prior to or concurrent with DEL-014-03 | _DEPENDENCIES.md; RFP S3.4 |
| Regulatory Environment | Province of Alberta; must adhere to Alberta Safety Codes and the Alberta Plumbing Code (National Plumbing Code as adopted in Alberta; specific edition TBD -- see Specification Standards table) | RFP S3.3.2; Semantic Lensing C-002 (terminology harmonized) |
| Guarantee Period | 2 years post-CCC | RFP S2.10 |
| Project Completion Deadline | December 31, 2026 | RFP S3.1 |

---

## Construction

| Element | Description | Source |
|---|---|---|
| Fill Line Pipe Material | **TBD** — to be specified by plumbing engineer in IFC drawings. To be added to Datasheet Attributes when resolved. | Design deliverable (PKG-006); Semantic Lensing B-002 |
| Pump Equipment | High-volume pump; manufacturer, model, and specifications **TBD** pending plumbing design. To be added to Datasheet Attributes when resolved. | RFP S3.4; Semantic Lensing B-002 |
| Fill Connection Hardware | Exterior fill point hardware (coupling type, cap, enclosure) **TBD**. To be added to Datasheet Attributes when resolved. | Design deliverable (PKG-006); Semantic Lensing B-002 |
| Electrical Connection | Motor power supply circuit; coordination required with DEL-015-04 (Equipment Power Circuits) | ASSUMPTION |
| Installation Drawings | To be produced under PKG-006 (Plumbing Design) — DEL-006-04 (Cistern & Pump Details) and associated plans | Decomposition S7 |
| Testing Requirement | Pressure and flow testing of completed fill line; pump performance verification | ASSUMPTION — standard installation practice |

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | S3.4 Design Requirements — explicit "bulk water fill with high volume pump for external filling" requirement |
| R-06 | AB-2026-01424-Appendix B (Plumbing).pdf | Conceptual plumbing layout showing "Bulk Water Fill" location on building exterior |
| SOW-0044 | Install bulk water fill system with high-volume pump for external filling | Decomposition SSOW SF, R-01 S3.4 |
| OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition... | Decomposition S5 |
| OBJ-004 | Install and commission all mechanical, plumbing, and water storage systems to operational readiness. Explicitly includes the bulk water fill. | Decomposition S5 |
| DEL-014-01 | Cistern & Distribution — upstream dependency (fill target) | _DEPENDENCIES.md |
| DEL-006-04 | Cistern & Pump Details — plumbing design deliverable governing this installation | Decomposition S7 |

---

## Semantic Lensing Enrichment Log (Pass 3)

| ItemID | Action Taken |
|---|---|
| B-001 | Pump Flow Rate attribute expanded with criticality note and plumbing engineer action required |
| B-002 | Construction table TBD entries annotated with note to update Datasheet Attributes when resolved in IFC design |
| E-004 | Primary Function attribute updated to flag bidirectional ambiguity; cross-referenced to Conflict Table C-003 in Guidance.md |
| C-002 | Regulatory Environment condition harmonized to use canonical plumbing code terminology; cross-references Specification Standards table |
