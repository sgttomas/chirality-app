# Datasheet — DEL-006-07 Plumbing Calculation Package

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-006-07 |
| Deliverable Name | Plumbing Calculation Package |
| Package | PKG-006 — Plumbing Design |
| Discipline | Plumbing Engineering |
| Artifact Type | Calculation Package |
| Responsible Party | Plumbing Engineer |
| SOW Reference | SOW-0016 |
| Objectives | OBJ-003 (P.Eng.-stamped IFC documentation), OBJ-004 (mechanical, plumbing, and water systems operational readiness) |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price |
| Completion Deadline | December 31, 2026 |
| Deliverable Status | SEMANTIC_READY (as of 2026-02-26) |

---

## Attributes

### Building Context

| Attribute | Value | Source |
|---|---|---|
| Building name | New North Shop Addition | R-01 §3.1; R-06 (Appendix B Plumbing drawing) |
| Building footprint (nominal) | 130 ft × 100 ft (~13,000 sq ft usable area) | R-01 §3.1; R-06 drawing dimensions |
| Ceiling height | 35 ft (concrete structure) | R-01 §3.4; R-06 drawing notes |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta | R-01 §1.0 |
| Water supply source | On-site cistern (no municipal water supply) | R-01 §3.4; R-06 |
| Sanitary disposal | On-site septic holding tank (no municipal sewer) | R-01 §3.4; R-06 |

### Plumbing Systems — Key Sizing Parameters

| System | Parameter | Value | Source |
|---|---|---|---|
| Water storage — cistern | Minimum volume | 50,000 L | R-01 §3.4 |
| Water distribution pump | Flow rate | 100 LPM | R-01 §3.4 |
| Cistern fill connection | Diameter | 2.5 inches | R-01 §3.4 |
| Septic holding tank | Capacity | 2,000 US gallons (approximately 7,571 L) | R-01 §3.4; R-06 drawing |
| Bulk water fill pump | Type | High-volume pump for external filling | R-01 §3.4 |
| Wash bay drainage | Discharge point | Exterior mud sump (cleanable by excavator) | R-01 §3.4; R-06 drawing |
| Wash bay mud sump | Volume | TBD — to be determined by Plumbing Engineer based on motor-scraper wash-down volumes (ASSUMPTION: industrial wash volumes; specific volume TBD) | R-01 §3.4; R-06 drawing |
| Building occupancy | User count / occupancy count | TBD — required for NPC fixture unit calculations; to be determined with Architect (ASSUMPTION: Group F Division 2 industrial or similar) | ASSUMPTION; Procedure Step 1.3, Step 2.1 |

**Unit Convention Note:** Source documents (R-01, R-06) use a mix of metric and imperial units: cistern volume in litres (50,000 L), pump flow in LPM (100 LPM), septic capacity in US gallons (2,000 US gal), fill connection diameter in inches (2.5"). To reduce conversion error risk during engineering, this Datasheet provides dual-unit values where both metric and imperial equivalents are available. The Plumbing Engineer should adopt a consistent unit convention for the calculation package and document it in the Design Assumption Documentation. Source: R-01 §3.4; _SEMANTIC_LENSING.md item B-003.

### Fixtures and Equipment Identified on Drawings

**Note:** The fixture list below is drawn from R-06 (Appendix B Plumbing drawing). The co-developed fixture schedule (DEL-006-06) should be cross-referenced when available to ensure comprehensive fixture coverage. Source: Procedure.md Prerequisites (DEL-006-06 listed as prerequisite); _SEMANTIC_LENSING.md item B-002.

| Item | Location (per drawing) | Source |
|---|---|---|
| Emergency shower | South wall area, near wash bay entrance | R-06 (Appendix B Plumbing) |
| Water tap and pressure washer reel | North repair bay area / wash bay boundary | R-06 (Appendix B Plumbing) |
| Water tap (additional) | South area near washroom | R-06 (Appendix B Plumbing) |
| Floor drain | North repair bay (left bay) | R-06 (Appendix B Plumbing) |
| Floor drain | North repair bay (right/centre bay) | R-06 (Appendix B Plumbing) |
| Floor drain | Wash bay | R-06 (Appendix B Plumbing) |
| Floor drain | South interior area (near washroom) | R-06 (Appendix B Plumbing) |
| Drain (emergency shower) | Adjacent to emergency shower | R-06 (Appendix B Plumbing) |
| Wash station (industrial wash sink) | South wall, adjacent to parts room / wash bay boundary | R-06 (Appendix B Plumbing) |
| Washroom | Interior — adjacent to utility room / office area | R-06 (Appendix B Plumbing) |
| 50,000 L water storage cistern | Exterior — east side of building (shown on drawing) | R-06 (Appendix B Plumbing) |
| Septic tank | Exterior — north side of building (shown on drawing) | R-06 (Appendix B Plumbing) |
| Mud sump (wash bay) | Exterior — east/right side of wash bay | R-06 (Appendix B Plumbing) |
| Sump drains in repair bays | Repair bays | R-01 §3.4 |

### Calculation Sub-Domains

| Sub-Domain | Status |
|---|---|
| Water demand analysis | TBD — to be determined during engineering |
| Water supply line sizing | TBD |
| Pressure drop and pump selection | Input data: 100 LPM @ TBD head (source: R-01 §3.4) |
| Drainage system sizing and slope | TBD |
| Vent stack sizing | TBD |
| Septic system sizing | Input: 2,000 US gallon (approximately 7,571 L) tank capacity (source: R-01 §3.4) |
| Code compliance matrix | TBD |
| Emergency shower flow/pressure verification | TBD (ASSUMPTION: ANSI Z358.1 or equivalent applies) |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Jurisdiction | Province of Alberta, Canada | R-01 §2.22 |
| Design authority | P.Eng. licensed in Alberta | R-01 §3.3.2 |
| Applicable codes | Alberta Safety Codes Act (Plumbing); National Plumbing Code of Canada (NPC) — ASSUMPTION: likely applicable; specific edition TBD | R-01 §3.3.2; ASSUMPTION |
| Septic regulation | Alberta Environment / AER requirements — ASSUMPTION: likely applicable for holding tank installation | ASSUMPTION |
| Water supply (no municipal) | Design assumes cistern as sole potable/service water source | R-01 §3.4; R-06 |
| Existing septic | Existing septic tank to be removed and replaced with 2,000 US gallon (approximately 7,571 L) holding tank | R-01 §3.4 |
| Sump drain type | Repair bay sumps — type (oil/water separator or simple sump) TBD | R-01 §3.4 (ASSUMPTION: industrial sump, separator sizing TBD) |
| Guarantee period | Construction period + 2 years post-CCC | R-01 §2.10 |

---

## Construction

| Artifact | Status | Notes |
|---|---|---|
| Water demand and consumption calculations | To be produced | Standard occupancy fixture-count method per NPC — ASSUMPTION |
| Water supply line sizing calculations | To be produced | Based on 100 LPM pump and distribution layout |
| Pressure drop and pump selection calculations | To be produced | Pump: 100 LPM @ 2.5" fill connection per R-01 §3.4 |
| Drainage system sizing and slope calculations | To be produced | Includes floor drains, wash bay drain to mud sump |
| Vent stack sizing calculations | To be produced | Per NPC or Alberta Safety Code — ASSUMPTION |
| Septic system sizing calculations | To be produced | 2,000 US gallon holding tank per R-01 §3.4 |
| Code compliance matrices | To be produced | Plumbing Safety Code compliance |
| Design assumption documentation | To be produced | Listing all engineering assumptions |
| Equipment performance data sheets | To be produced | Cistern pump, bulk water fill pump |

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §1.0 (project description), §3.4 (design requirements including cistern, pump, septic, drains, bulk water fill) |
| R-06 | AB-2026-01424-Appendix B (Plumbing).pdf | Conceptual plumbing layout drawing — New North Shop; shows fixture locations, drain locations, cistern, septic, mud sump |
| Decomposition | WDMLRL_Decomposition_Claude.md | PKG-006 scope, DEL-006-07 entry, OBJ-003, OBJ-004, SOW-0041–SOW-0050 |
| DEL-006-06 | Plumbing Fixture Schedule | Co-developed fixture schedule; cross-reference for fixture coverage (TBD — not yet available) |
| NPC | National Plumbing Code of Canada | ASSUMPTION: likely governing code; edition and applicability TBD pending Safety Code permit process |
| Alberta Safety Codes Act | Alberta Safety Codes (Plumbing) | ASSUMPTION: governing regulatory framework; specific safety code order TBD |

**SOW Traceability:** A consolidated SOW-to-REQ traceability matrix is provided in Specification.md (SOW Traceability section). Source: _SEMANTIC_LENSING.md item X-002.
