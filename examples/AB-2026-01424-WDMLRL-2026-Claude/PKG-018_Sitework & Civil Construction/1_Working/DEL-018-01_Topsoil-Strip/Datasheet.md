# DEL-018-01 — Topsoil Stripping | Datasheet

---

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-018-01 |
| **Title** | Topsoil Stripping |
| **Package** | PKG-018 — Sitework & Civil Construction |
| **Deliverable Type** | Construction |
| **Responsible Party** | General Contractor |
| **SOW Reference** | SOW-0075 |
| **Objective(s)** | OBJ-001 |
| **Decomposition Reference** | WDMLRL_Decomposition_Claude.md, §PKG-018, §7 Deliverables by Package |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Critical Path** | Yes — foundational first step; upstream to all other PKG-018 deliverables |

---

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Work Description** | Strip topsoil from all driving surfaces | RFP §3.3.2, SOW-0075 |
| **Trigger Condition** | Required regardless of whether Owner has previously performed it | Decomposition D-010 |
| **Topsoil Depth** | TBD (to be determined by site survey — SURVEY-001). This is an essential data prerequisite: depth drives volume calculation, equipment selection, and stripping limit definition. Must be resolved before execution can proceed. | _DEPENDENCIES.md. **[B-001]** Resolution blocked on SURVEY-001 output. |
| **Area of Work** | All driving surfaces within the project lot — extent TBD pending site survey and IFC drawings. **Note:** "All driving surfaces" is interpreted by Specification REQ-018-01-01 as "the full extent of planned vehicle and equipment traffic areas" per IFC drawings. Whether this includes pedestrian paths, equipment staging areas, or building perimeter areas is TBD — see Guidance for normalization note. | ASSUMPTION: based on RFP §3.3.2 scope; exact limits per site maps (R-07). **[B-003]** Scope extent definition deferred to Specification as normative authority; see Conflict Table CFT-002 if ambiguity persists after IFC drawing review. |
| **Volume of Topsoil** | TBD — dependent on topsoil depth assessment and area determination. Calculation method: Volume = Stripping Area (m^2) x Average Topsoil Depth (m), to be computed once SURVEY-001 and IFC drawings (DEL-005-02) define both inputs. | _DEPENDENCIES.md. **[B-002]** Volume calculation formula placeholder added; actual value TBD pending depth and area resolution. |
| **Stockpile Location** | TBD — temporary on-site stockpile area to be identified in site layout | ASSUMPTION: stockpile required for later landscaping/restoration per context |
| **Topsoil Disposition** | Retained on site for reuse in future landscaping and site restoration | _CONTEXT.md (context summary) |
| **Equipment Type** | Mechanical excavation equipment — type TBD. Equipment selection criteria: must be suitable for topsoil depth and area determined by SURVEY-001; common categories include dozer, scraper, or excavator. Selection per contractor means and methods once depth/area are confirmed. | ASSUMPTION: standard earthworks practice. **[A-004]** Equipment category constraint TBD pending SURVEY-001 and contractor mobilization plan. |
| **Aggregate Supply** | Aggregate/gravel supply excluded — County/Landfill responsibility | RFP §3.3.1, Decomposition SOW-0203 |
| **Bulk Cut and Fill** | Excluded — County responsibility | RFP §3.3.1, Decomposition SOW-0201 |
| **Brushing and Clearing** | Excluded — County performs prior to Proponent mobilization | RFP §3.3.1, Decomposition SOW-0200 |

---

## Conditions

| Condition | Detail | Source |
|-----------|--------|--------|
| **Precondition: Site Access** | Site must be accessible and mobilization area prepared (SITE-ACCESS-001) before work begins | _DEPENDENCIES.md |
| **Precondition: Survey** | Site survey and topsoil depth assessment (SURVEY-001) must be complete to define excavation depth and volume | _DEPENDENCIES.md |
| **Precondition: Utility Locate** | Underground utilities must be located and marked (UTILITIES-001) before any excavation commences — safety-critical | _DEPENDENCIES.md |
| **Precondition: Brushing/Clearing** | County-performed brushing and clearing of project area must be complete before Proponent begins topsoil stripping | RFP §3.3.1, Decomposition SOW-0200 |
| **Site Environment** | Rural landfill site near Ferintosh, Alberta; site topography and existing conditions shown in Appendix C – Site Maps (R-07) | _REFERENCES.md |
| **County Coordination** | County project representative must be available for inspections; inspection requests to be submitted by Proponent | RFP §3.3.2 |
| **Completion Deadline** | December 31, 2026 (overall project deadline) | Decomposition — Project header |

---

## Construction

| Item | Detail | Source |
|------|--------|--------|
| **Execution Sequence** | First activity in PKG-018; must be completed before grading (DEL-018-02), driving surface (DEL-018-03), pads (DEL-018-04), drainage (DEL-018-05), and utility tie-ins (DEL-018-06) | _DEPENDENCIES.md, Decomposition §PKG-018 |
| **Execution Method** | Mechanical stripping and excavation of topsoil layer from all driving surface areas | ASSUMPTION: consistent with standard civil earthworks practice; specific method per contractor means and methods |
| **Stockpile Management** | Topsoil to be temporarily stockpiled on site for future reuse; stockpile area to be identified in site logistics plan | ASSUMPTION: required for site restoration and landscaping (DEL-018-02) |
| **Environmental Compliance** | Work to comply with applicable Alberta environmental regulations; erosion and sediment control required per Specification REQ-018-01-09; dust control per Guidance Considerations; specific measures TBD | ASSUMPTION: required by applicable codes; see Specification REQ-018-01-08 for regulatory detail and Standards table for applicable legislation |
| **IFC Drawing Dependency** | Exact limits of topsoil stripping area defined by IFC drawings (site grading plan — DEL-005-02); drawings must be issued before construction | ASSUMPTION: IFC drawings are condition precedent per RFP §3.3.2 |
| **Inspection** | County representative to be present for applicable inspections; inspection report copies to be provided to County | RFP §3.3.2 |

---

## References

| Ref Code | Document | Section | Relevance |
|----------|----------|---------|-----------|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.3.2 | Primary scope statement for topsoil stripping (SOW-0075) |
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.3.1 | Defines County-responsibility exclusions (clearing, bulk cut/fill, aggregate) |
| R-07 | AB-2026-01424-Appendix C - Site Maps.pdf | Overall site plans | Site topography, clearing limits, and expansion area — note: text content of maps not extractable; location TBD within document |
| DECOMP | WDMLRL_Decomposition_Claude.md | §J (SOW-0075), §D-010, §PKG-018, §DEL-018-01 | Scope assignment, decision rationale, deliverable identity |
| DECOMP | WDMLRL_Decomposition_Claude.md | §SOW-0200, SOW-0201, SOW-0203 | Out-of-scope County responsibilities |
