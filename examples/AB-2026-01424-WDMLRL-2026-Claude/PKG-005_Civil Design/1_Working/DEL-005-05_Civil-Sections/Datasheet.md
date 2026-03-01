# Datasheet — DEL-005-05: Civil Sections & Details

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-005-05 |
| **Deliverable Name** | Civil Sections & Details |
| **Package** | PKG-005 — Civil Design |
| **Discipline** | Civil Engineering |
| **Delivery Type** | Drawing Set |
| **Responsible Party** | Civil Engineer (P.Eng., licensed in Alberta) |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Site Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |
| **SOW Coverage** | SOW-0015 |
| **Objectives Supported** | OBJ-001, OBJ-003 (ASSUMPTION: package-grouping heuristic; see note below) |

> **ASSUMPTION (best-effort mapping):** OBJ-001 and OBJ-003 are associated with all PKG-005 deliverables per the decomposition's Objective-to-Deliverable Mapping (WDMLRL_Decomposition_Claude.md, §8 Scope Ledger and §9 Coverage & Telemetry). This association is directionally relevant context; it has not been confirmed at the individual deliverable-ID level by the human.

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Drawing Set Content** | Cross-sectional views and construction details for civil infrastructure elements | _CONTEXT.md — Description |
| **Primary Detail Types** | Pavement sections, grading/fill sections, drainage structure sections, curb/gutter/edge conditions, driveway transitions/aprons, retaining wall sections (if applicable), utility crossings, standard construction details | _CONTEXT.md — Anticipated Artifacts |
| **Driving Surface Material** | Gravel | RFP §3.3.2 |
| **Driving Surface Design Criterion** | Accommodate weight and turning radius of large construction equipment, including motor scraper | RFP §3.3.2 |
| **Drainage Design Requirement** | Positive site drainage; account for future storm events | RFP §3.4 |
| **Off-Site Drainage Constraint** | Grading design shall not alter drainage conditions of neighbouring properties | RFP §3.4 |
| **Wash Bay Drainage Feature** | Exterior mud sump for wash bay drainage and excavator cleanout | RFP §3.4; App B (Shop) conceptual drawing |
| **Sump Drains** | Sump drains in repair bays | RFP §3.4 |
| **Topsoil Stripping** | Strip topsoil from all driving surfaces (if not already performed by Owner) | RFP §3.3.2 |
| **Stamp Requirement** | All IFC drawings signed/stamped by a P.Eng. licensed in the Province of Alberta | RFP §3.3.2 |
| **Building Footprint (New North Shop)** | Approximately 130 ft x 100 ft (from conceptual drawing dimensions) | App B (Shop) — conceptual floor plan |
| **Overall Site Width (reference)** | Approximately 235 ft (existing + new shop combined, from conceptual drawing) | App B (Shop) — conceptual floor plan |
| **Pad Types Shown on Conceptual Drawing** | Gravel Pad (north of new shop), Cement Pad (south of new shop), Cement Pad (east/wash bay side) | App B (Shop) — conceptual floor plan |
| **Expansion Area** | Identified north/northeast of existing Old North Shop building | App C (Site Maps) — Expansion Area aerial |
| **Geotechnical Input** | Geotechnical investigation and report required as input to civil design | RFP §3.3.2 (location TBD — geotech report not yet available at time of drafting) |
| **Existing Site Context** | Active regional landfill facility; site in open excavated/graded terrain adjacent tree line | App C (Site Maps) |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| **Climate / Region** | Central Alberta; semi-arid prairie; subject to freeze-thaw cycles and storm events | RFP §1.0 (location); ASSUMPTION: Alberta climate conditions apply |
| **Governing Jurisdiction** | Province of Alberta | RFP §2.22; §3.3.2 |
| **Site Ownership** | County-owned site, Camrose County | RFP §3.1 |
| **Bulk Cut/Fill** | Performed by County (OUT of Proponent scope) | RFP §3.3.1 |
| **Aggregate Supply** | Supplied by County (OUT of Proponent scope) | RFP §3.3.1 |
| **Brushing and Clearing** | Performed by County (OUT of Proponent scope) | RFP §3.3.1 |
| **Survey Input** | Preliminary, construction, and as-built surveys required (PKG-008 scope); survey data is upstream input to civil design | RFP §3.3.2; Decomposition — PKG-008 |
| **Geotechnical Input** | Full geotechnical report required before final civil design (PKG-008 scope) | RFP §3.3.2; Decomposition — PKG-008 |
| **Geotechnical Design Parameters (B-001)** | TBD — The following essential design parameters are required from the PKG-008 geotechnical report: CBR (California Bearing Ratio) or equivalent bearing value, frost depth for central Alberta at this site, subgrade soil classification, and groundwater depth. These values are essential facts for section design and cannot be assumed. **Proposed authority:** PKG-008 geotechnical consultant. | RFP §3.3.2 (geotech report required); *[lensing item B-001]* |

---

## Construction

| Item | Value | Source |
|---|---|---|
| **Sections Anticipated** | Pavement/gravel driving surface section (typical and at transitions); grading and fill section profiles; drainage structure sections (swales, culverts, or similar — type TBD); curb, gutter, edge condition details; driveway apron/transition details; retaining wall sections (if applicable — TBD based on grading design); utility crossing protection details; wash bay mud sump section/detail; standard notes and material specifications in detail format | _CONTEXT.md — Anticipated Artifacts |
| **Governing Codes/Standards** | Alberta Safety Codes (ASSUMPTION: applicable); municipal/county development permit requirements; applicable Alberta Infrastructure standards (TBD — specific standards not cited in RFP) | RFP §3.3.2; ASSUMPTION |
| **IFC Drawing Requirement** | All drawings issued for construction must be signed and stamped by a P.Eng. licensed in Alberta | RFP §3.3.2 |
| **Coordination** | Civil sections must coordinate with Site Grading Plan (DEL-005-02), Drainage Plan (DEL-005-03), Driving Surface & Pad Layout Plan (DEL-005-04), and Civil Specification (DEL-005-07) within PKG-005; also with structural (PKG-002) for any embedded or interface conditions | Decomposition — PKG-005; ASSUMPTION |

---

## References

> **Note (E-001):** Reference identifiers should use a single canonical format across all documents. The format used below (R-xx) should match _REFERENCES.md. **Action required:** R-04 (Appendix B — Shop) is cited in this Datasheet but is not listed in `_REFERENCES.md`, which currently lists only R-01 and R-07. The document controller should add R-04 to `_REFERENCES.md` to maintain a complete reference register. *[lensing items B-002, E-001]*

| Ref ID | Document | Relevance | Accessibility |
|---|---|---|---|
| R-01 | AB-2026-01424-WDMLRL_RFP.pdf | Main RFP — §3.3.2 (scope/IFC), §3.4 (grading/drainage requirements) | Accessed |
| R-04 | AB-2026-01424-Appendix_B__Shop_.pdf | Conceptual floor plan showing pad types, mud sump location, overall dimensions | Accessed |
| R-07 | AB-2026-01424-Appendix_C_-_Site_Maps.pdf | Site location, expansion area aerial | Accessed |
| — | WDMLRL_Decomposition_Claude.md | Project decomposition — PKG-005, DEL-005-05, SOW-0015 | Accessed |
| — | DEL-005-06_Calculation-Package | Civil calculation package (sibling deliverable — will contain design inputs for sections) | Not yet produced |
| — | DEL-005-07_Specification | Civil Specification (sibling deliverable — governs material requirements referenced in detail notes) | Not yet produced |
| — | PKG-008 Geotech Report | Geotechnical investigation report (upstream input) | Not yet available |
| — | Survey data (PKG-008) | Preliminary survey data (upstream input for grading sections) | Not yet available |
