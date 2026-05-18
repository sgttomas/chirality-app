# Specification — DEL-005-06: Civil Calculation Package

---

## Scope

### What This Deliverable Covers

DEL-005-06 is the Civil Calculation Package for the 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It provides the engineering calculation basis supporting all civil design decisions documented in PKG-005 drawings (DEL-005-02 through DEL-005-05) and the Civil Specification (DEL-005-07).

This package covers:
- Drainage system sizing calculations
- Stormwater management analysis (hydrologic and hydraulic)
- Finish grading and cut/fill volume calculations [terminology normalized per F-003]
- Driving surface (gravel) design calculations for motor-scraper-class equipment loads [terminology normalized per X-003]
- Slope stability assessment (if site conditions require — see REQ-010 for trigger criteria) [enriched per F-001]
- Utility sizing calculations within civil scope
- Design compliance verification summary
- Summary of design assumptions and governing references

### What This Deliverable Excludes

- Bulk earthworks (bulk cut and fill) — County responsibility per R-01 §3.3.1 and Decomposition §4
- Aggregate supply calculations — County-supplied per Decomposition SOW-0203
- Structural foundation calculations — covered by DEL-002-10 (Structural Calculation Package)
- Plumbing/drainage calculations for interior systems — covered by DEL-006 series
- Electrical or mechanical calculations — covered by respective discipline packages
- Brushing and clearing — County scope per R-01 §3.3.1

---

## Requirements

### REQ-001 — Positive Site Drainage
The grading design documented in this calculation package shall demonstrate that positive site drainage is achieved across the expansion area, accounting for future storm events.
- **Source:** R-01 §3.4 (SOW-0020); Decomposition Scope Ledger SOW-0020
- **Nature:** Explicit RFP requirement
- **Design Storm Return Period(s):** TBD — to be confirmed per applicable Alberta/Camrose County drainage standards. See Guidance Conflict Table CONF-001. The Civil Engineer shall confirm the governing design storm return period(s) with the County and/or applicable provincial drainage guidelines before finalizing this requirement's acceptance criteria. [enriched per A-001]

### REQ-002 — No Alteration of Neighbouring Drainage Conditions
The grading design shall demonstrate that proposed grades do not alter drainage conditions of neighbouring properties.
- **Source:** R-01 §3.4 (SOW-0021); Decomposition Scope Ledger SOW-0021
- **Nature:** Explicit RFP requirement

### REQ-003 — Site Grading Plan with Drainage Features
The calculation package shall support a complete site grading plan inclusive of drainage features and components.
- **Source:** R-01 §3.3.2 (SOW-0015); Decomposition Scope Ledger SOW-0015
- **Nature:** Explicit RFP requirement

### REQ-004 — Driving Surface Design for Heavy Equipment
The driving surface design calculations shall demonstrate that the gravel surface is adequate for the weight and turning radius of motor-scraper-class equipment (as minimum design load). [terminology normalized per X-003]
- **Source:** R-01 §3.3.2; Decomposition SOW-0077
- **Nature:** Explicit RFP requirement

### REQ-005 — P.Eng. Stamp (Alberta)
All Issued-for-Construction drawings supported by this calculation package must be signed and stamped by a professional engineer licensed to practise in the Province of Alberta. The calculation package itself must be prepared by or under the responsible supervision of a P.Eng. licensed in Alberta.
- **Source:** R-01 §3.3.2
- **Nature:** Explicit RFP requirement

### REQ-006 — Code and Regulatory Compliance
The civil design shall adhere to all applicable Alberta Safety Codes, applicable building codes, and municipal/county development requirements.
- **Source:** R-01 §3.3.2; Decomposition OBJ-001
- **Nature:** Explicit RFP requirement; specific codes are TBD pending design development (ASSUMPTION: Alberta Environment and Protected Areas drainage criteria apply; Camrose County land development standards apply — location TBD in specific bylaw/standard)
- **Note** [enriched per A-002, C-001]: The Civil Engineer shall identify specific applicable code clauses during project setup (Step 1 of Procedure) and populate the Standards table below with clause-level references. Until specific clauses are identified, compliance determination against this requirement cannot be fully verified (see A-003 enrichment in Verification table).

### REQ-007 — Geotechnical Data Integration
Civil calculations shall incorporate findings from the geotechnical investigation (DEL-008-01). Foundation-related pricing and design parameters are variable until the geotech report is available.
- **Source:** R-01 §4.8.2; Decomposition SOW-0001
- **Nature:** Explicit RFP requirement; upstream dependency

### REQ-008 — Preliminary Design Approval Gate
Preliminary civil design must receive County approval before final design calculations are completed.
- **Source:** R-01 §3.3.2; Decomposition SOW-0010e (preliminary civil design)
- **Nature:** Explicit RFP requirement; process constraint

### REQ-009 — Topsoil Stripping Design Support
Where topsoil stripping of driving surfaces is within Proponent scope, the calculation package shall include or reference the stripping volume and extent.
- **Source:** R-01 §3.3.2; Decomposition SOW-0075 / D-010 (assumed required)
- **Nature:** Explicit RFP requirement; extent of Proponent responsibility confirmed per Decision D-010 in decomposition

### REQ-010 — Slope Stability Trigger Criteria [enriched per F-001]
The calculation package shall include explicit trigger criteria for when slope stability analysis is required. The following criteria shall be evaluated based on site conditions and geotechnical recommendations from DEL-008-01:
- Cut or fill slope height exceeding TBD metres (to be confirmed per geotechnical recommendations and applicable standards)
- Slope angle exceeding TBD degrees (to be confirmed per geotechnical recommendations)
- Presence of retaining structures
- Adverse groundwater or soil conditions identified in the geotechnical investigation

Where slope stability analysis is not required, the calculation package shall include a documented determination citing the basis (e.g., all slopes below threshold height/angle; geotechnical engineer's recommendation).
- **Source:** R-01 §3.3.2 (civil design scope); Decomposition SOW-0015 (site grading plan)
- **Nature:** ASSUMPTION — inferred from standard civil engineering practice and the existing conditional scope statement. Specific thresholds are TBD pending DEL-008-01.

### REQ-011 — Septic System Drainage Interface [enriched per B-003]
The civil drainage design calculations shall account for the proposed septic system (DEL-006-05) drainage envelope as a design input. The calculation package shall document the drainage coordination interface between the civil site drainage system and the septic system outfall/drainage field.
- **Source:** Guidance — Coordination with PKG-006; Decomposition PKG-006 scope
- **Nature:** ASSUMPTION — inferred from interdisciplinary coordination requirements. Specific interface parameters are TBD pending DEL-006-05 design development.

### REQ-012 — Environmental Regulatory Compliance (Landfill Proximity) [enriched per C-002]
The civil drainage design shall comply with applicable environmental regulations governing surface drainage near an active landfill. The calculation package shall document the regulatory framework applied (e.g., Alberta Environmental Protection and Enhancement Act (EPEA) approvals, Alberta Environment and Protected Areas operating approval conditions, or equivalent) and demonstrate that proposed drainage does not compromise landfill environmental controls.
- **Source:** Guidance — Landfill Site Context consideration; R-01 §3.4 (site context)
- **Nature:** ASSUMPTION — inferred from the landfill site context. Specific regulatory requirements are TBD pending confirmation of the landfill's operating approval conditions and applicable EPEA provisions. The Civil Engineer should confirm with the County and/or Alberta Environment and Protected Areas.

### REQ-013 — Calculation Accuracy and Presentation Standards [enriched per F-005]
The calculation package shall be prepared to a standard of accuracy and presentation consistent with professional engineering practice for civil design calculations in Alberta. This includes:
- Appropriate significant figures for each calculation type (TBD — to be defined by the responsible P.Eng.)
- Consistent units throughout (SI or Imperial, as determined by project convention)
- Clear identification of input data, assumptions, calculation method, and results for each calculation section
- **Source:** ASSUMPTION — inferred from standard professional engineering practice requirements. No specific accuracy/precision standard is stated in accessible project sources.
- **Nature:** ASSUMPTION — quality criterion for calculation presentation.

### REQ-014 — Calculation Package Completeness [enriched per D-003]
The calculation package shall be considered complete when:
1. All calculation topics listed in the Datasheet Construction table have been addressed (either calculated or documented as not applicable with rationale),
2. All TBD items within the calculation package have been resolved or formally deferred with documented justification,
3. All records listed in the Procedure Records section have been produced, and
4. Cross-document consistency with the Civil Specification (DEL-005-07) and the PKG-005 drawing set (DEL-005-02 through DEL-005-05) has been verified.
- **Source:** Datasheet — Construction table; Procedure — Records section; Specification — Documentation artifacts
- **Nature:** ASSUMPTION — inferred from the existing document set as an overall completeness acceptance criterion not previously defined.

---

## Standards

The following standards are expected to govern civil design for this project. Full text of these standards has not been reviewed; applicability is noted as ASSUMPTION based on project location (Alberta, Canada) and project type. Specific clause requirements are TBD.

**Note** [enriched per A-002, C-001, D-001]: All clause-level entries below are TBD. The Civil Engineer shall research and populate specific clause references during project setup (Procedure Step 1). Until clause-level references are identified, verification of code compliance (REQ-006) will remain incomplete. This is a known gap requiring human action.

| Standard / Code | Applicability | Status |
|---|---|---|
| Alberta Safety Codes Act (and applicable Safety Codes) | Governing code for construction in Alberta | Explicit — R-01 §3.3.2; clause-level requirements TBD. Identify specific Safety Codes applicable to civil site works (e.g., Alberta Building Code Part 9 or Part 3 as applicable). |
| National Building Code of Canada (NBC) — applicable edition | Base building code | ASSUMPTION: likely applicable; edition TBD (confirm whether 2020 NBC or subsequent edition is adopted in Alberta at time of permit application); location TBD [enriched per D-001] |
| Alberta Drainage Design Guidelines (Alberta Environment and Protected Areas) | Drainage sizing and stormwater design | ASSUMPTION: likely applicable for rural municipal drainage; specific sections TBD. Confirm applicability of the Alberta Stormwater Management Guidelines (or equivalent current publication). |
| Camrose County Land Development / Subdivision and Development Regulations | Site grading, drainage, and setback requirements | ASSUMPTION: likely applicable; specific bylaw number TBD. Contact Camrose County Planning Department to obtain current bylaw and identify applicable sections. |
| CCDC 14–2013 Design-Build Stipulated Price Contract | Contract form governing design-builder obligations | Explicit — R-01 §2.7 |
| Alberta Environmental Protection and Enhancement Act (EPEA) | Environmental regulatory framework for drainage near active landfill | ASSUMPTION: likely applicable given landfill site context; specific approval conditions TBD [enriched per C-002, REQ-012] |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-001 (positive drainage) | Grading calculations demonstrate positive flow paths; drainage plan reviewed against topographic survey data. Design storm return period(s) verified against confirmed Alberta/County criteria (TBD per CONF-001). [enriched per A-001] |
| REQ-002 (no neighbour impact) | Pre- and post-development drainage comparison at property boundary; confirm no increase in offsite discharge rates or patterns. Pre-development baseline method and documentation standard per Guidance direction. [enriched per E-002] |
| REQ-003 (grading + drainage features) | Calculation package completeness review against drawing set (DEL-005-02, DEL-005-03) and Civil Specification (DEL-005-07). [enriched per F-002: added DEL-005-07 cross-reference to align with Procedure Step 7.3] |
| REQ-004 (driving surface capacity) | Pavement/surface design calculation against motor-scraper-class equipment load criteria; compare to standard design charts or geotechnical recommendations. [terminology normalized per X-003] |
| REQ-005 (P.Eng. stamp) | Stamp and signature on IFC drawings; calculation package sealed or supervised by stamping engineer |
| REQ-006 (code compliance) | Design compliance checklist referencing specific applicable Safety Code clauses and bylaw sections (TBD — to be populated once codes are identified per A-002/C-001); County inspection sign-offs. Verification cannot be fully completed until specific code clauses are identified. [enriched per A-003] |
| REQ-007 (geotech integration) | Calculation package cites geotech report (DEL-008-01) and incorporates subgrade recommendations |
| REQ-008 (approval gate) | County approval record documented for preliminary civil design before IFC calculations finalized |
| REQ-009 (topsoil stripping) | Stripping volumes and extents included or cross-referenced in calculations. Verification shall confirm accuracy of stripping volumes against surveyed stripping depth and/or reconciliation with County-performed work extents (where applicable). [enriched per X-004] |
| REQ-010 (slope stability triggers) | Trigger criteria documented; determination (required or not required) recorded with basis citing geotechnical recommendations and applicable standards. [enriched per F-001] |
| REQ-011 (septic interface) | Drainage calculations document the septic system drainage envelope as a design input; coordination record with DEL-006-05 exists. [enriched per B-003] |
| REQ-012 (environmental/landfill) | Environmental regulatory framework identified and documented; drainage design demonstrates no compromise of landfill environmental controls. [enriched per C-002] |
| REQ-013 (accuracy/presentation) | Checker review (Procedure Step 7) confirms appropriate significant figures, consistent units, and clear calculation structure per professional practice standards. [enriched per F-005] |
| REQ-014 (completeness) | All Datasheet Construction table topics addressed; all TBDs resolved or formally deferred; all Procedure records produced; cross-document consistency verified. [enriched per D-003] |

---

## Documentation

The following artifacts are anticipated outputs associated with this deliverable. Exact document list is TBD pending design development.

| Artifact | Description |
|---|---|
| Drainage sizing calculations | Hydrologic and hydraulic analysis for stormwater management |
| Stormwater detention/retention calculations | Where applicable per site conditions and regulatory requirements |
| Finish grading and cut/fill volume calculations | Finish grading balance; topsoil stripping volumes [terminology normalized per F-003] |
| Pavement/driving surface design | Gravel surface design for motor-scraper-class loading [terminology normalized per X-003] |
| Slope stability analysis | If required by site conditions per REQ-010 trigger criteria (TBD after geotech) |
| Utility sizing support calculations | Civil utility scope as applicable |
| Design assumptions summary | Documented list of all governing assumptions |
| Design standards and codes reference list | All governing codes cited in calculations |
| Calculation cover sheet with P.Eng. seal | Required for IFC submission |
| Design storm return period confirmation | Record documenting confirmed design storm criteria and basis [enriched per F-004] |
| Septic system drainage interface record | Coordination documentation with DEL-006-05 [enriched per B-003] |
