# Datasheet — DEL-005-06: Civil Calculation Package

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-005-06 |
| Deliverable Name | Civil Calculation Package |
| Package | PKG-005 — Civil Design |
| Discipline | Civil Engineering |
| Delivery Type | Calculation Package |
| Responsible Role | Civil Engineer |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Site Legal Description | SW 14–44–21–W4, near Ferintosh, Alberta |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price Contract |
| Completion Deadline | December 31, 2026 (Source: R-01, §3.1) |
| Revision | 0 — Initial draft (Pass 1+2); enriched Pass 3 [2026-02-26] |

> **Revision Control Note** [enriched per E-001]: Multiple Datasheet attributes are currently TBD pending upstream deliverables (DEL-008-01, DEL-008-02). As these become available, update the affected attribute rows, increment the Revision field, and record the date, source, and nature of the change below.

| Rev | Date | Changed Attributes | Source | Author |
|---|---|---|---|---|
| 0 | 2026-02-26 | Initial draft | Pass 1+2 generation; Pass 3 enrichment | 4_DOCUMENTS agent |
| 1 | TBD | Site Area (total development area) | DEL-008-02 (Preliminary Site Survey) | TBD |
| 2 | TBD | Subgrade parameters, surface thickness | DEL-008-01 (Geotechnical Report) | TBD |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| Scope of Work References | SOW-0015, SOW-0020, SOW-0021 | Decomposition §7 / Scope Ledger |
| Objectives Served | OBJ-001, OBJ-003 | Decomposition §7, DEL-005-06 row |
| Governing SOW — Final Civil Design | Complete final civil design including site grading plan with drainage features and components | R-01 §3.3.2; Decomposition SOW-0015 |
| Governing SOW — Positive Drainage | Grading design shall account for positive site drainage and future storm events | R-01 §3.4; Decomposition SOW-0020 |
| Governing SOW — Neighbour Drainage | Grading design shall not alter drainage conditions of neighboring properties | R-01 §3.4; Decomposition SOW-0021 |
| Governing SOW — Driving Surface Construction | Construct gravel driving surface designed for weight and turning radius of heavy construction equipment (motor scraper class) | R-01 §3.3.2; Decomposition SOW-0077 [enriched per E-003: source reference aligned with Specification REQ-004] |
| Driving Surface Design Load | Weight and turning radius of motor-scraper-class equipment (minimum design load) | R-01 §3.3.2; Decomposition SOW-0077 [enriched per E-003, X-003: source and terminology normalized] |
| Driving Surface Material | Gravel | R-01 §3.3.2 |
| Site Area — Building Footprint | Approx. 13,000 sq ft useable building area (conceptual) | R-01 §3.1 (building useable area) |
| Site Area — Total Development Area | TBD — pending preliminary site survey (DEL-008-02). Required for drainage basin delineation and grading volume calculations. [enriched per B-001: distinguished from building footprint] | DEL-008-02 (not yet available) |
| Watershed / Drainage Context | Rural landfill site; existing drainage patterns must be preserved at property boundary | R-01 §3.4; Appendix C site maps |

---

## Conditions

| Condition | Statement | Source |
|---|---|---|
| Design Context | Design-build; County has concept only — civil engineer develops design to meet RFP performance requirements | R-01 §3.4 |
| County-Supplied Work (OUT of scope of calculations) | Bulk cut and fill, brushing/clearing, aggregate supply | R-01 §3.3.1; Decomposition §4 |
| Geotechnical Data | Full geotechnical investigation required before finalizing civil calculations; foundation pricing variable until geotech complete | R-01 §4.8.2; Decomposition SOW-0001 |
| IFC Drawing Requirement | All Issued-for-Construction drawings must be signed/stamped by a P.Eng. licensed in Alberta | R-01 §3.3.2 |
| Preliminary Design Approval | County must approve preliminary civil design before final design proceeds | R-01 §3.3.2 |
| Code Compliance | Building design (and associated civil works) must adhere to all applicable Alberta Safety Codes and building codes | R-01 §3.3.2 |
| Topsoil Stripping | Required for all driving surfaces (if not already performed by Owner) | R-01 §3.3.2; Decomposition SOW-0075 |

---

## Construction (Anticipated Artifacts / Calculation Coverage)

The Civil Calculation Package is expected to include the following calculation topics. Quantities, design parameters, and final coverage are TBD pending geotechnical investigation and site survey completion.

| Calculation Topic | Status | Notes |
|---|---|---|
| Drainage system sizing | TBD | Must address positive drainage for future storm events (SOW-0020) |
| Stormwater detention/retention | TBD | Must not alter downstream/neighbour drainage conditions (SOW-0021) |
| Hydrologic and hydraulic analysis | TBD | Return period(s) to be confirmed per applicable Alberta standards |
| Finish grading and cut/fill volume calculations | TBD | Bulk cut/fill is County scope; Proponent responsible for finish grading volumes [terminology normalized per F-003] |
| Pavement / driving surface design | TBD | Gravel surface; must accommodate motor-scraper-class equipment loads [terminology normalized per X-003] |
| Slope stability analysis | TBD | Applicable if site conditions require; to be determined after geotech report |
| Utility sizing calculations | TBD | Civil utility tie-ins in scope (gas, electrical, communications coordination per SOW-0080–SOW-0082 via PKG-018) |
| Design compliance verification | TBD | Against applicable Alberta codes and RFP requirements |
| Summary of design assumptions | TBD | To be documented within calculation package |
| References to design standards and codes | TBD | To be listed per applicable Alberta standards |

---

## References

| Ref ID | Document | Relevance | Location |
|---|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Primary civil scope: §3.3.2 (scope of work), §3.4 (grading/drainage design requirements) | _Sources/ |
| R-07 | AB-2026-01424-Appendix C - Site Maps.pdf | Site location map (SW 14-44-21-W4) and expansion area aerial showing construction location | _Sources/ |
| Decomposition | WDMLRL_Decomposition_Claude.md | SOW-0015, SOW-0020, SOW-0021, SOW-0077; PKG-005 package description; OBJ-001, OBJ-003 | _Decomposition/ |
| DEL-008-01 | Geotechnical Investigation & Report | Upstream dependency — civil calculations depend on geotech findings | PKG-008 |
| DEL-008-02 | Preliminary Site Survey | Upstream dependency — existing grades and site boundaries required for grading calculations | PKG-008 |
| App B (Shop) | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan — building footprint context for site grading layout | _Sources/ |
