# Procedure — DEL-002-03 Structural Framing Plans

---

## Purpose

This procedure describes the steps to produce the Structural Framing Plans (DEL-002-03) for the New North Shop Addition — from design inputs and preliminary drawing production through to the Issued for Construction (IFC) drawing set — in conformance with the RFP requirements (R-01, §3.3.2) and the CCDC 14–2013 Design-Build framework.

This procedure covers the **production** of the drawing set deliverable, not the construction activities performed from it.

---

## Prerequisites

### Information Inputs Required

| Input | Source / Deliverable | Status |
|---|---|---|
| Geotechnical investigation and report | DEL-008-01 (Geotechnical Investigation & Report) | Required before finalizing foundation/structural loads; impacts soil bearing, frost depth, and slab subgrade design |
| Preliminary site survey | DEL-008-02 (Preliminary Site Survey) | Required for site datum and existing building interface conditions |
| Preliminary architectural design (County-approved) | DEL-002-01 (Preliminary Structural Design) / DEL-001-01 (Preliminary Architectural Design) | Required — structural framing must coordinate with approved floor plan and room layout |
| County approval of preliminary structural design | County (via ORCHESTRATOR workflow) | Required before IFC drawing production per R-01, §3.3.2 |
| Crane manufacturer data | Crane supplier (for SOW-0067) | Required: wheel loads, wheel base, runway span, crane weight — needed to design crane runway framing (REQ-FP-04, REQ-FP-17) |
| NBC climatic data for site (snow, wind, seismic) | National Building Code of Canada — climatic data tables for SW 14–44–21–W4 area | Required to establish design loads for framing (REQ-FP-20) |
| Architectural floor plans (coordinated) | DEL-001-02 (Architectural Floor Plans) | Required for coordination of column grid with room layout, door openings, and drive-through bay clear widths |

### Reference Documents Required

| Reference | Purpose |
|---|---|
| R-01 — AB-2026-01424-WDMLRL RFP.pdf, §3.4 | Design requirements governing structural system |
| R-04 — AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan for spatial layout and structural notes |
| NBC (current Alberta edition) | Design loads and structural acceptance criteria |
| CSA S16 (if steel used) | Steel member design |
| CSA A23.3 (if concrete used) | Concrete member design |
| DEL-002-02 (Foundation Plan) | Column grid coordination |
| DEL-002-12 (Structural Specification) | Material and workmanship requirements for framing |

### Personnel and Credentials Required

| Role | Requirement |
|---|---|
| Structural Engineer of Record | P.Eng. licensed in the Province of Alberta (R-01, §3.3.2) |
| CAD/BIM Technician | ASSUMPTION: proficient in structural drawing production |
| Architectural Coordinator | ASSUMPTION: available for interdisciplinary coordination reviews |

---

## Steps

### Step 1 — Collect and Review Design Inputs

1.1 Obtain and review the geotechnical report (DEL-008-01). Extract: soil bearing capacity, frost depth, groundwater level, any special foundation recommendations affecting slab or pit design.

1.2 Obtain NBC climatic data for the site location (SW 14–44–21–W4, near Ferintosh, Alberta). Record: ground snow load (S_s, S_r), hourly wind pressure (q), seismic design data (S_a(T), site class).

1.3 Obtain crane data from the crane supplier (for two 5-tonne overhead cranes, SOW-0067): maximum wheel load, minimum wheel load, wheel base, crane bridge span, crane weight, trolley weight, hook approach dimensions.

**Acceptance criteria for crane data completeness (Lensing ref: A-004):** The following minimum data items must be received and confirmed before proceeding to Step 2 (structural system and column grid design):
- Maximum vertical wheel load (kN or lbs) — required for runway beam sizing
- Wheel base (mm or in) — required for runway beam local bending check
- Crane bridge span (mm or ft) — required for column grid spacing at crane aisle
- Crane weight and trolley weight — required for dead load calculation
- Hook approach dimensions (end approach + side approach) — required for crane clearance envelope verification against 35 ft clear height

If any of the above items are unavailable, the Structural Engineer shall document the missing items and either (a) use conservative ASSUMPTION values marked as TBD for preliminary design only, or (b) defer crane runway framing design until data is received. The choice between (a) and (b) shall be documented.

1.4 Review conceptual floor plan (R-04) and County-approved preliminary architectural drawings (DEL-001-02 or DEL-002-01) to understand room layout, repair bay widths (24 ft per R-04), wash bay width (24 ft per R-04), service trench location, mezzanine extents, and building overall dimensions (130 ft × 100 ft per R-04).

1.5 Review the Structural Specification (DEL-002-12) and Foundation Plan (DEL-002-02) for any constraints that affect framing member selection or column locations.

1.6 Confirm the mezzanine design live load with the County — the mezzanine must carry oil totes and pumping equipment (R-01, §3.4). Document the confirmed value or record as TBD if not yet confirmed.

### Step 2 — Establish Structural System and Column Grid

2.1 Select the structural framing system consistent with the RFP requirement for a "concrete structure" (R-01, §3.4). If a hybrid system (e.g., concrete columns with steel roof framing) is proposed, confirm acceptability with the County.

2.2 Develop the column grid layout. The grid must:
- Provide minimum 24 ft clear width in repair bays (per R-04 bay dimension annotation).
- Provide minimum 24 ft clear width in the wash bay (per R-04 annotation).
- Not obstruct the service trench opening or the drive-through access paths.
- Accommodate the crane runway beam spans without intermediate columns within the crane aisle.

2.3 Establish the crane runway beam elevation. Calculate the required bottom-of-rail elevation from:
- Required hook clearance above the tallest equipment (motor scraper class — ASSUMPTION: hook height TBD, to be confirmed with County)
- Crane rail height + runway beam depth + structure-to-rail clearance
- Confirm that the runway beam bottom elevation is at or below the clear ceiling height of 35 ft (R-01, §3.4)

2.4 Calculate the required building eave height (top of wall / top of frame) to achieve 35 ft clear height with roof framing depth and any suspended services.

2.5 Document the structural system selection and design load summary for inclusion in the general notes of the drawing set.

### Step 3 — Produce Preliminary Framing Plans

3.1 Produce schematic framing plans at each level (main floor, mezzanine, roof) showing:
- Column grid with dimensions
- Primary framing members (beams, girders, roof framing type) — without full connection details
- Crane runway beam location and elevation
- Mezzanine extents and framing direction
- Service pit/trench opening with header framing
- Wash bay boundary framing

3.2 Submit preliminary framing plans as part of DEL-002-01 (Preliminary Structural Design) for County approval (R-01, §3.3.2).

3.3 Incorporate County review comments and obtain written County approval before proceeding to IFC drawings.

### Step 4 — Produce IFC Framing Plans

4.1 Upon County approval of preliminary design, advance each framing plan to IFC level. IFC plans shall include:
- Fully dimensioned column grid
- All primary members designated with member marks (e.g., W-shapes, HSS designations, concrete column marks, beam marks)
- Crane runway beams designated and elevation noted
- Mezzanine framing plan with member designations and design live load stated
- Roof framing plan showing framing direction, member designations, roof slope (if applicable), and framing at openings
- Service pit header framing shown at ground level plan
- Section cut indicators referencing DEL-002-04 through DEL-002-09
- Detail bubble references for all major connections
- General notes block including: design loads, governing codes, material specifications summary, and reference to calculation package (DEL-002-10)

4.2 Coordinate with the architectural drawings (DEL-001-02) to confirm that structural column locations are compatible with room layouts, door openings, and finished floor elevations.

4.3 Coordinate with the electrical drawings (DEL-004 series) for crane power requirements and runway beam end-stop clearances.

4.4 Coordinate with the mechanical drawings (DEL-003 series) for any roof penetrations, equipment pads, or suspended equipment loads that affect roof framing.

4.5 Coordinate framing plan column locations with the foundation plan (DEL-002-02) to confirm consistency.

4.6 Coordinate slab framing (thickened slab, pit walls, embedment zones) with the steel plate embedment plan (DEL-002-08).

### Step 5 — Internal Quality Review

5.1 Structural Engineer of Record performs an internal quality review of all framing plan sheets, verifying:
- Column grid is consistent across all plan levels.
- All members are designated and no members are shown without a mark.
- All section cuts and detail bubbles correspond to sheets in DEL-002-04 through DEL-002-09.
- Design loads in general notes match the structural calculation package (DEL-002-10).
- 35 ft clear height dimension or note is shown.
- Crane runway elevation is shown.
- Mezzanine live load is stated.

5.2 Perform a cross-discipline coordination check against the most recent architectural, mechanical, and electrical drawings. Record any conflicts for resolution.

**Pass/fail criteria for cross-discipline coordination check (Lensing ref: D-002):**
- **Pass:** All of the following are confirmed:
  - Structural column locations do not conflict with architectural door openings, room boundaries, or required clear widths (24 ft repair bays, 24 ft wash bay).
  - Roof framing member depths and locations do not conflict with mechanical ductwork routing or equipment pads.
  - Crane runway end-stop locations and power connection points are coordinated with electrical drawings.
  - No unresolved spatial conflicts remain between structural and other discipline drawings.
- **Fail (blocking):** Any spatial conflict between structural framing and another discipline that cannot be resolved by the Structural Engineer alone (requires design change by another discipline). Document the conflict, notify the responsible party, and do not proceed to Step 6 (Stamp and Issue) until the conflict is resolved or an agreed-upon resolution path is documented.
- **Fail (non-blocking):** Minor annotation or reference discrepancies that can be corrected by the Structural Engineer without design impact. Correct and document before proceeding.

5.3 Resolve all internal conflicts and coordination issues before stamping.

### Step 6 — Stamp and Issue

6.1 Structural Engineer of Record reviews and stamps all IFC framing plan drawings with their P.Eng. seal and signature as required by R-01, §3.3.2.

6.2 Issue the framing plan drawing set as part of the IFC document package.

6.3 Transmit the IFC drawing set to the County for the building permit application (DEL-009-02) and to the General Contractor for construction (PKG-011).

6.4 Record the issue date and drawing revision on the title block of each sheet.

---

## Verification

The following checks confirm that the Structural Framing Plans (DEL-002-03) are complete and compliant prior to final issuance:

| Check | Criteria | Method |
|---|---|---|
| V-01 — All plan levels present | Ground floor, mezzanine, and roof framing plans all exist as separate sheets (or combined where justified) | Drawing index review |
| V-02 — Column grid dimensioned | All column grid lines are dimensioned in both directions on each plan level | Drawing review |
| V-03 — Member designations | All structural members have member mark designations | Drawing review |
| V-04 — 35 ft clear height noted | A clear height dimension or note of ≥35 ft is shown in the main shop area | Drawing review |
| V-05 — Crane runway shown | Crane runway beams are shown on the appropriate plan level with elevation notation | Drawing review |
| V-06 — Mezzanine load noted | Mezzanine design live load is stated on the mezzanine framing plan | Drawing review |
| V-07 — P.Eng. stamp | IFC drawings are signed and stamped by a P.Eng. licensed in Alberta | Stamp verification |
| V-08 — County preliminary approval | Written County approval of preliminary design on record before IFC issuance | Approval record review |
| V-09 — Column grid matches foundation plan | Column grid on DEL-002-03 is geometrically consistent with DEL-002-02 | Cross-document comparison |
| V-10 — Design loads stated | General notes block includes design loads (dead, live, snow, wind, seismic, crane) with values | Drawing review |
| V-11 — Cross-references present | Section cuts and detail bubbles reference correct sheets in DEL-002-04 through DEL-002-09 | Drawing review |

---

## Records

The following records shall result from execution of this procedure:

| Record | Purpose | Where Filed |
|---|---|---|
| County approval letter / email for preliminary framing plans | Evidence of County approval gate per R-01, §3.3.2 | Project correspondence file |
| Crane supplier data sheet | Input record for crane runway design | Structural design file |
| NBC climatic data extraction for site | Design load basis record | Structural calculation package (DEL-002-10) |
| Geotechnical report (DEL-008-01) | Foundation/slab design input record | Project file / PKG-008 folder |
| Internal QA review record | Evidence of engineer review before stamping. **Required format and content (Lensing ref: E-003):** The internal QA review record shall be a written document (checklist, memo, or structured form) containing at minimum: (1) Date of review, (2) Reviewer name and credential (P.Eng. number), (3) Drawing list reviewed (sheet numbers and revisions), (4) Checklist items corresponding to V-01 through V-11 with pass/fail status for each, (5) List of any deficiencies found and resolution status, (6) Reviewer signature or electronic approval. **ASSUMPTION:** The specific format (checklist vs. memo) is a project QA decision; the minimum content fields above are proposed to ensure the record is auditable. | Structural design file |
| Issued drawing set (IFC) | Primary deliverable — DEL-002-03 | PKG-002_Structural Design / 3_Issued (or equivalent) folder |
| Drawing transmittal record | Evidence of issue to County and Contractor. **Required format and content (Lensing ref: E-001):** The drawing transmittal record shall contain at minimum: (1) Transmittal date, (2) Recipient name and organization (County contact, General Contractor contact), (3) Drawing list with sheet numbers, titles, and revision numbers, (4) Number of copies or delivery method (electronic/hardcopy), (5) Transmittal purpose (e.g., "Issued for Construction", "Issued for Permit"), (6) Sender name and signature. **ASSUMPTION:** A standard project transmittal form may already exist; the minimum content fields above are proposed to ensure the record is standardized. | Project correspondence file |

---

*Procedure generated by 4_DOCUMENTS agent — Pass 1. Date: 2026-02-25.*
*Enriched by 4_DOCUMENTS agent — Pass 3 (Semantic Lensing). Date: 2026-02-26.*
*Lensing items applied: A-004, D-002, E-001, E-003.*
*ASSUMPTION labels indicate inferred content not explicitly stated in sources.*
*TBD entries require additional information before the relevant step can be completed.*
