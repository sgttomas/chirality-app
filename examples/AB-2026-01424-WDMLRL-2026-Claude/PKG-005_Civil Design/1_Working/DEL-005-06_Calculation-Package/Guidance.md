# Guidance — DEL-005-06: Civil Calculation Package

---

## Purpose

DEL-005-06 exists to provide the verified engineering calculation basis that justifies the civil design decisions for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition expansion area. The calculation package is the primary instrument by which the Civil Engineer demonstrates that:

1. The site grading plan achieves positive drainage and does not adversely affect neighbouring properties (RFP §3.4, SOW-0020, SOW-0021).
2. The driving surface is designed to safely carry heavy construction equipment (RFP §3.3.2).
3. The civil design is code-compliant and suitable for County approval, building permit, and construction.

The calculation package underpins the entire PKG-005 Civil Design drawing set and the Civil Specification (DEL-005-07). It is the technical record that survives inspections, warranty periods, and future operations.

Without this deliverable, the supporting drawings (DEL-005-02 through DEL-005-05) cannot be issued for construction under the signature of a P.Eng. licensed in Alberta (RFP §3.3.2).

**ASSUMPTION (best-effort objective mapping):** This deliverable serves OBJ-001 (code-compliant, functional shop addition) and OBJ-003 (complete, P.Eng.-stamped IFC documentation coordinated across disciplines) per the decomposition's objective-to-deliverable mapping for PKG-005 (Decomposition §7, DEL-005-06 row).

---

## Principles

### 1. Source-Anchored Calculations
All civil calculations shall reference the data sources used: survey data, geotechnical report, RFP requirements, and governing standards. This allows independent review and verification by the County's representatives and inspecting authorities.

### 2. Design-Build Context
The County has stated a performance concept, not a prescriptive design (RFP §3.4). The Civil Engineer is responsible for selecting appropriate methods and design approaches to meet RFP performance requirements. The calculation package shall clearly document the design basis, including all assumptions made where prescriptive direction was absent.

### 3. Upstream Data Dependency
Civil calculations depend critically on two upstream deliverables:
- **DEL-008-01 (Geotechnical Investigation & Report):** Subgrade bearing capacity, soil classification, and groundwater data are required for driving surface design and slope stability assessment.
- **DEL-008-02 (Preliminary Site Survey):** Existing grades, drainage patterns, and site boundaries are required before grading calculations can be meaningfully performed.

Calculation work should be staged accordingly: do not finalize grading or drainage calculations before survey data is available; do not finalize driving surface or foundation-related civil calculations before geotech data is available.

#### Interim Design Parameter Values [enriched per B-002]
Before DEL-008-01 is available, the Civil Engineer may need to proceed with preliminary design calculations (for County preliminary approval at Step 8). The following guidance applies to interim assumptions:
- **Subgrade CBR:** ASSUMPTION — adopt a conservative preliminary value (e.g., CBR 2-3 for heavy clay subgrade) pending confirmation from geotechnical testing. Document the assumed value and its basis explicitly. The actual value from DEL-008-01 may reduce or increase the required surface thickness.
- **Preliminary surface thickness:** ASSUMPTION — use a conservatively thick initial estimate based on the assumed low CBR and motor-scraper-class loading. This preliminary thickness is for approval-stage cost and layout purposes only, not for final design.
- **Soil classification:** ASSUMPTION — if site soils appear visually to be glacial till or lacustrine clay (common in this region of Alberta), assume conservative parameters accordingly. Confirm with DEL-008-01.

All interim values must be clearly labeled as PRELIMINARY/ASSUMPTION in calculation documents and must be updated when DEL-008-01 data becomes available. The revision control mechanism in the Datasheet should track these updates.

### 4. Separate County and Proponent Scopes
The County is responsible for bulk cut and fill and aggregate supply (RFP §3.3.1). The Proponent is responsible for detailed finish grading design, topsoil stripping (if County has not already performed it), and driving surface design. The calculation package should clearly delineate which quantities and works are within Proponent scope. Avoid performing or billing for County-scope work.

### 5. Neighbour Drainage Non-Alteration
RFP §3.4 (SOW-0021) is an explicit constraint: the grading design shall not alter drainage conditions of neighbouring properties. This is not a soft target. The calculation package must provide a defensible pre/post comparison at the property boundary demonstrating compliance.

#### Pre-Development Baseline Method [enriched per E-002]
To establish a defensible baseline for the "no alteration of neighbour drainage" requirement (REQ-002), the Civil Engineer should:
- **Data sources:** Use the preliminary site survey (DEL-008-02) as the primary data source for existing grades and drainage patterns. Supplement with historical aerial imagery (e.g., from Alberta Environment or municipal GIS) and any available County drainage records for the landfill property.
- **Analysis method:** Select a hydrologic analysis method appropriate for the contributing area size and available data. For a rural site of this scale, the Rational Method (for peak flow estimation) or SCS Curve Number method (for volume-based analysis) are typical approaches. Document the method selection rationale.
- **Documentation standard:** The pre-development baseline should be documented as a standalone calculation section (or sub-section within Step 2 of the Procedure) that includes: contributing area delineation map, land cover and soil classification assumptions, selected runoff coefficients or curve numbers with justification, and calculated pre-development peak flow rates and/or volumes at each property boundary discharge point.
- **Source:** ASSUMPTION — standard of practice guidance inferred from common Alberta civil engineering practice. No specific standard is cited in accessible project sources.

### 6. Future Storm Events
RFP §3.4 (SOW-0020) requires that grading account for "future storm events." The return period(s) to be designed for are not specified in the RFP. ASSUMPTION: applicable Alberta municipal drainage design standards will define minimum return periods (typically 1:5-year for minor drainage and 1:100-year for major drainage for rural municipal contexts — location TBD in specific provincial or county guidelines). The Civil Engineer must confirm the governing criteria with the County and document the selected design storms in the calculation package.

---

## Considerations

### Landfill Site Context
The site is an operating regional landfill (West Dried Meat Lake Regional Landfill, SW 14-44-21-W4, Camrose County). This has civil design implications:
1. Surface drainage from the expansion area must not direct runoff toward active landfill cells or compromise liner integrity. ASSUMPTION: this is a site-specific consideration that the Civil Engineer should confirm at the mandatory site meeting (RFP §3.2, March 3, 2026) and address in design assumptions.
2. The expansion area (identified in Appendix C aerial — yellow-bounded area east of existing shop building) appears to be on relatively flat, disturbed ground adjacent to the existing maintenance shop. This simplifies grading but requires attention to outfall directions.

#### Environmental Regulatory Framework [enriched per B-004]
Drainage near an active landfill may be subject to environmental regulatory requirements beyond standard municipal drainage codes. The Civil Engineer should investigate:
- **Alberta EPEA:** The Environmental Protection and Enhancement Act governs waste management facility approvals in Alberta. The landfill's operating approval may include conditions related to surface water management, drainage diversion, and runoff quality near active cells. The Civil Engineer should request a copy of the landfill's current operating approval from the County to identify any drainage-related conditions. ASSUMPTION: EPEA operating approval conditions likely exist but have not been accessed — location TBD.
- **Surface water quality:** If proposed drainage routes pass near active landfill cells or waste management areas, consideration of runoff quality (sediment, contact water) may be required. This is TBD pending review of the landfill's operating approval and site observations from the mandatory site meeting.
- **Source:** ASSUMPTION — inferred from Alberta regulatory framework for waste management facilities. Specific requirements are TBD pending access to the landfill operating approval document.

### Heavy Equipment Loading Context
The driving surface must accommodate motor-scraper-class equipment (R-01 §3.3.2). This is a high-load criterion for a gravel surface design. ASSUMPTION: the geotechnical investigation (DEL-008-01) will provide subgrade parameters needed for this design; until that report is available, surface thickness calculations cannot be finalized. An interim conservative estimate may be used for preliminary design approval purposes (see Principle 3 — Interim Design Parameter Values).

### Coordination with PKG-018 (Sitework & Civil Construction)
The civil design deliverables (PKG-005) inform construction scope in PKG-018. The calculation package and drawings must be complete and issued before PKG-018 construction can begin. Coordination between the Civil Engineer (design) and the General Contractor (construction) is required to ensure:
- Design grades match constructability given County-supplied bulk earthworks.
- Topsoil stripping extents are consistent between design documents and construction scope.

### Coordination with PKG-007 (Landscape Architectural Design)
The landscape design (DEL-007 series) is dependent on civil grading (PKG-005). The Civil Engineer should communicate proposed final grades and drainage outfall locations to the Landscape Architect to allow coordinated planting and restoration plans.

#### Specific Information Exchange Items [enriched per X-001]
To provide substantiated directive capacity for the PKG-007 coordination, the following specific information should be exchanged:
- **From Civil to Landscape:** Proposed finish grades at all landscape interface areas (perimeter of building, driving surfaces, drainage swale edges); drainage outfall locations with invert elevations and flow direction; any areas where slope protection or erosion control planting is required by the drainage design; topsoil stripping/replacement limits that affect planting areas.
- **From Landscape to Civil:** Proposed planting areas and irrigation requirements (if any) that may affect drainage basin delineation or surface runoff coefficients; any landscape grading requirements that differ from the civil grading plan.
- **Format/timing:** Exchange should occur after preliminary civil grading is established (after Step 3) and before final grading calculations are locked for IFC (before Step 9). Consider a coordination memo or shared markup of the site grading plan.

### Coordination with PKG-006 (Plumbing) — Septic and Drainage
The civil drainage design must account for the proposed septic system (DEL-006-05) and any related drainage infrastructure. The outfall or drainage envelope for the septic system is a coordination point between civil and plumbing discipline. The Civil Engineer should obtain the septic system drainage field location, sizing, and required setbacks from the Plumbing Engineer to incorporate as a constraint in the civil drainage calculations (see Specification REQ-011). [enriched per B-003]

---

## Trade-offs

| Trade-off | Options | Consideration |
|---|---|---|
| Stormwater management approach | Detention pond vs. infiltration vs. directed outfall | Site type (landfill), neighbour constraints (SOW-0021), and soil permeability (from geotech) will govern feasibility of each. TBD after geotech. The fundamental approach decision should be resolved before detailed drainage calculations begin (see Procedure Step 3 hold point). [enriched per X-002] |
| Driving surface design method | Empirical (CBR-based) vs. mechanistic-empirical | Geotech report will determine which method is appropriate and what subgrade support is available. |
| Grading strategy | Minimize earthworks vs. optimize drainage performance | Given County performs bulk cut/fill, the Proponent's grading design should work within the bulk grade envelope while achieving positive drainage. |
| Design storm return period | Conservative (100-year) vs. minimum required by code | Higher return period increases drainage infrastructure size and cost. Minimum required by applicable Alberta/County standards should be confirmed early. **Cost-engineering note** [enriched per A-005]: For this rural landfill context, the cost differential between designing for a 1:25-year and a 1:100-year major storm event may be significant in terms of drainage infrastructure sizing (swale cross-sections, culvert diameters, detention volumes). The Civil Engineer should document the cost implications of the selected return period as part of the design basis, particularly where the chosen return period exceeds minimum code requirements. This cost-risk trade-off should be presented to the County during preliminary design approval (Step 8) to support informed decision-making. |

---

## Terminology Notes [enriched per F-003, X-003]

To ensure cross-document consistency, the following normalized terms shall be used throughout the four production documents:

| Normalized Term | Replaces | Notes |
|---|---|---|
| Finish grading volumes | "finish cut/fill," "detailed finish grading volumes," "grading volumes: finish cut/fill" | Refers to Proponent-scope grading work only; bulk cut/fill is County scope |
| Motor-scraper-class equipment | "motor scraper class," "large construction equipment (motor scraper class as minimum)," "motor-scraper-class equipment" | The Specification (REQ-004) is the normative authority: the motor-scraper-class represents the minimum design load. Other heavier equipment may also need consideration per site conditions. |

---

## Examples

No examples from sources are available for this deliverable at this stage. TBD — to be developed as design progresses and comparable civil packages from similar rural Alberta industrial/maintenance facility projects are referenced.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-001 | Design storm return period(s) not specified in RFP. "Future storm events" language is ambiguous. | R-01 §3.4 (SOW-0020) — "account for positive site drainage and future storm events" | No specific return period stated in any accessible source | Specification REQ-001, REQ-006; Drainage sizing calculations | PROPOSAL: Civil Engineer to confirm with County/Camrose County development standards at project kickoff and document selected criteria in calculation package | TBD |
| CONF-002 | Extent of topsoil stripping responsibility between County and Proponent is conditionally stated ("if not already performed by Owner") | R-01 §3.3.2 — "Strip topsoil from all driving surfaces (if not already performed by Owner)" | Decomposition D-010 — "Resolved — topsoil stripping assumed required" | Specification REQ-009; Calculation scope | PROPOSAL: Treat as Proponent scope per D-010 decision; confirm with County at project kickoff | TBD |
| CONF-003 [enriched per E-003] | SOW-0077 source reference inconsistency between Specification and Datasheet. Specification REQ-004 cites "R-01 section 3.3.2; Decomposition SOW-0077" but original Datasheet Driving Surface Design Load row cited only "R-01 section 3.3.2" without SOW-0077. | Specification REQ-004 (cites R-01 §3.3.2 and SOW-0077) | Original Datasheet Attributes (cited R-01 §3.3.2 only) | Datasheet Attributes (Driving Surface Design Load); Specification REQ-004 | PROPOSAL: SOW-0077 confirmed in Decomposition Scope Ledger. Both documents now updated to cite SOW-0077. Conflict resolved in Pass 3 enrichment — confirm correctness. | RESOLVED (Pass 3) — verify |
