# Procedure — DEL-006-07 Plumbing Calculation Package

---

## Purpose

This procedure describes the steps to **produce** the Plumbing Calculation Package (DEL-006-07) for the New North Shop Addition at the West Dried Meat Lake Regional Landfill. It guides the Plumbing Engineer through the sequence of tasks required to generate a complete, P.Eng.-stamped calculation package that supports the IFC plumbing drawing set.

The calculation package is a pre-construction deliverable that provides engineered justification for all plumbing and water systems in the building. It must be completed before IFC drawings are issued for construction.

Source: WDMLRL_Decomposition_Claude.md (DEL-006-07 entry, OBJ-003); R-01 §3.3.2 (SOW-0016, SOW-0018).

---

## Prerequisites

### Upstream Deliverables and Information Required

The following items should be available or in progress before beginning the calculation package. These are best-effort dependencies; the Plumbing Engineer may proceed with reasonable assumptions where upstream information is pending, provided all assumptions are documented.

| Prerequisite | Source / Deliverable | Status |
|---|---|---|
| Conceptual plumbing layout (fixture locations, drain locations, cistern and septic positions) | R-06 — Appendix B (Plumbing) conceptual drawing | Available |
| RFP design requirements (cistern size, pump specs, septic size, fixture list) | R-01 §3.4 | Available |
| Preliminary architectural floor plan (room dimensions, occupancy) | DEL-001-01 or DEL-001-02 (Architectural Design) | TBD — may be needed for occupancy-based fixture counts |
| Geotechnical investigation report (for septic system siting if required by authority) | DEL-008-01 (Geotechnical Investigation) | TBD — required for septic authority submission; ASSUMPTION: holding tank installation may not require geotech if shallow excavation only |
| Plumbing fixture schedule (DEL-006-06) | DEL-006-06 | TBD — fixture schedule and calculation package are co-developed |
| Alberta Safety Code Plumbing permit requirements | Local Safety Codes Officer / Permit authority | TBD |
| Applicable plumbing code edition (NPC edition and Alberta amendments) | Safety Codes Officer confirmation | TBD |

### Required References

| Reference | Use |
|---|---|
| R-01 — AB-2026-01424-WDMLRL RFP.pdf | Design requirements (§3.4); scope of work (§3.3.2) |
| R-06 — AB-2026-01424-Appendix B (Plumbing).pdf | Conceptual fixture and drain layout |
| National Plumbing Code of Canada (applicable edition) — ASSUMPTION | Sizing tables and methods |
| Applicable Alberta Safety Code Plumbing Order — ASSUMPTION | Regulatory compliance requirements |
| ANSI Z358.1 (or applicable Alberta OHS standard) — ASSUMPTION | Emergency shower design criteria |

---

## Steps

### Step 1 — Scope Confirmation and Design Assumption List Initialization

1.1 Confirm the scope boundary of this calculation package: New North Shop addition vs. Old North Shop renovation plumbing. See Conflict Table CFT-001 in Guidance.md — obtain human ruling before proceeding if scope is ambiguous.

1.2 Confirm the applicable Alberta Plumbing Safety Code order and NPC edition with the Safety Codes Officer at the permit pre-application stage.

1.3 Initialize the Design Assumption Documentation sub-artifact. Each assumption entry shall include: assumption ID, description, source/basis, status (open / confirmed / invalidated), and confirmation date (when applicable). Record at minimum:
   - Building occupancy type (ASSUMPTION: Group F Division 2 or similar industrial — confirm with Architect)
   - Occupancy count / user count for fixture calculations (TBD)
   - Simultaneous demand factor adopted for system sizing
   - Oil/water separator requirement decision (see Conflict Table CFT-003 in Guidance.md)
   - Bulk water fill pump target flow rate (see Conflict Table CFT-002 in Guidance.md)
   - Cistern refill cycle frequency assumption
   - Unit convention adopted for the calculation package (see Datasheet.md Unit Convention Note)

Source for assumption record schema: _SEMANTIC_LENSING.md items A-004, X-006.

1.4 Cross-reference with the decomposition (SOW-0041 through SOW-0050) to confirm all plumbing scope items are captured.

---

### Step 2 — Water Demand Analysis

2.1 Determine occupancy-based fixture unit count per NPC (ASSUMPTION) for:
   - Washroom (toilet, urinal, lavatory)
   - Wash station (industrial sink)
   - Emergency shower
   - Water taps
   - Pressure washer reel(s)

2.2 Determine process water demand for:
   - Wash bay operations (motor-scraper class wash-down)
   - Pressure washer reel flow rate (TBD — specific model not identified in RFP; **resolution required:** Design-Builder to select or specify pressure washer reel model, or provide minimum performance parameters — flow rate and operating pressure — to enable supply sizing in Steps 3 and 4). Source: _SEMANTIC_LENSING.md item F-004.
   - Bulk water fill rate (TBD — see CFT-002)

2.3 Calculate peak simultaneous demand scenario (worst-case combination of fixtures and process loads operating concurrently). Document simultaneous demand factor and scenario adopted.

2.4 Calculate estimated daily and weekly water consumption to characterize cistern drawdown and fill frequency.

Output: Water Demand and Consumption Calculations sub-artifact.

**HOLD POINT 1:** Before proceeding to Step 3, review the Water Demand output for reasonableness. Confirm that: (a) the peak simultaneous demand scenario is documented and plausible; (b) the cistern drawdown rate does not indicate a fundamental sizing issue; (c) all fixture types from R-06 are accounted for. An error in demand analysis propagates through all subsequent sizing steps. Source: _SEMANTIC_LENSING.md item A-005.

---

### Step 3 — Water Supply Line Sizing

3.1 Using the peak simultaneous demand from Step 2, size the main supply line from the cistern to the building distribution header.

3.2 Size branch lines to each fixture group and point of use, including:
   - Emergency shower branch (priority — verify adequate pressure and flow; see REQ-007 and Consideration 3 in Guidance.md)
   - Pressure washer reel branch
   - Wash station branch
   - Washroom branch (toilet, urinal, lavatory)
   - Water tap branches

3.3 Size the cistern fill line and internal distribution pump supply/discharge connections (pump: 100 LPM minimum at 2.5" fill connection per REQ-002).

3.4 Size the bulk water fill line and pump (flow rate TBD per CFT-002).

Output: Water Supply Line Sizing Calculations sub-artifact.

---

### Step 4 — Pressure Drop and Pump Selection Calculations

4.1 Calculate system head loss for the critical (longest/highest) distribution circuit from cistern pump to most remote fixture.

4.2 Confirm the internal distribution pump operating point (flow ≥ 100 LPM at the calculated system head). Select pump or confirm Owner-specified pump meets requirements.

4.3 Calculate pressure available at emergency shower. Confirm it meets applicable standard minimum supply pressure (ASSUMPTION: ANSI Z358.1 or equivalent; specific value TBD).

4.4 Calculate pressure drop for pressure washer reel supply and confirm adequate pressure at point of use (TBD — depends on pressure washer reel model).

4.5 If a booster pump or pressure tank is required (ASSUMPTION: may be needed given cistern-fed system without municipal pressure), document pump selection and tank sizing.

4.6 Document the bulk water fill pump selection and system head calculation.

Output: Pressure Drop and Pump Selection Calculations sub-artifact; Equipment Performance Data Sheets sub-artifact (pump data sheets).

---

### Step 5 — Drainage System Sizing and Slope Calculations

5.1 Assign drainage fixture units (DFU) per NPC (ASSUMPTION) to each drain and fixture:
   - Floor drains in repair bays (left bay, centre/right bay)
   - Floor drain in wash bay
   - Floor drain in south interior area
   - Emergency shower drain
   - Wash station drain
   - Washroom fixtures (toilet, urinal, lavatory)

5.2 Size drain lines (diameter and slope) from each fixture/drain to the main building drain or holding tank connection, ensuring minimum slopes per NPC (ASSUMPTION: 1/8" per foot for 4" and larger, or per code table).

5.3 Calculate the wash bay floor drain line and sizing for connection to the exterior mud sump. Confirm pipe capacity is adequate for motor-scraper wash-down volumes.

5.4 Confirm the mud sump connection pipe sizing and verify gravity drainage is achievable given floor and sump elevations (elevations TBD from structural/civil drawings).

5.5 Address sump drain in repair bays — confirm whether oil/water separator is required and incorporated (see CFT-003 in Guidance.md).

5.6 Size the main sanitary drain from the building to the septic holding tank. Confirm minimum slope to holding tank inlet.

Output: Drainage System Sizing and Slope Calculations sub-artifact.

**HOLD POINT 2:** Before proceeding to Step 6, review the supply and drainage sizing outputs (Steps 3-5) for internal consistency. Confirm that: (a) supply pipe sizes are consistent with the demand analysis from Step 2; (b) drainage slopes meet minimum code requirements; (c) the mud sump connection is confirmed as gravity-drainable. Source: _SEMANTIC_LENSING.md item A-005.

---

### Step 6 — Vent Stack Sizing

6.1 Determine the venting system configuration (individual venting, wet venting, or common venting per NPC — ASSUMPTION).

6.2 Size vent stacks and branch vents for all fixture groups per NPC (ASSUMPTION).

6.3 Confirm vent termination location and clearances per code (ASSUMPTION: minimum 150 mm above roof and minimum horizontal clearance from air intakes — specific requirements TBD from NPC and Alberta amendments).

6.4 Verify vent termination clearances explicitly: (a) height above roof penetration meets NPC minimum; (b) horizontal clearance from air intakes, openable windows, and other openings meets NPC minimum; (c) clearance from building elements that could cause snow/ice blockage. Record pass/fail for each clearance criterion. Source: _SEMANTIC_LENSING.md item C-004.

Output: Vent Stack Sizing Calculations sub-artifact.

---

### Step 7 — Septic System Sizing

7.1 Calculate the daily sewage flow based on occupancy and fixture count (per Step 2 output and applicable Alberta regulation — ASSUMPTION).

7.2 Confirm that the 2,000 US gallon (approximately 7,571 L) holding tank has adequate capacity relative to estimated daily flow, and document estimated pump-out frequency for Owner operational awareness.

7.3 If regulatory authority requires additional information (e.g., site assessment, soil percolation — ASSUMPTION: holding tanks typically do not require perc test, but confirm), prepare supporting documentation.

7.4 Confirm that the tank meets Alberta Environment or applicable regulatory requirements for material, installation, and venting.

Output: Septic System Sizing Calculations sub-artifact.

---

### Step 8 — Code Compliance Matrix

8.1 Compile a code compliance matrix cross-referencing each applicable NPC (or Alberta Safety Code Plumbing) requirement against the design solution adopted.

8.2 Identify any areas requiring a variance or engineering judgement and document accordingly.

8.3 Confirm Safety Code permit application requirements are met.

Output: Code Compliance Matrices sub-artifact.

---

### Step 9 — Calculation Package Assembly and P.Eng. Review

9.1 Assemble all sub-artifacts into the final calculation package in a logical sequence (cover sheet → assumptions → water demand → supply sizing → pressure/pump → drainage → venting → septic → compliance).

9.2 The responsible Plumbing Engineer (P.Eng. licensed in Alberta) shall review all calculations for correctness, completeness, and code compliance.

9.3 P.Eng. signs and stamps the calculation package cover sheet.

9.4 Cross-reference the calculation package against the IFC plumbing drawing set (DEL-006-02 through DEL-006-05) to confirm consistency. The cross-reference check shall explicitly verify, at minimum:
   - Supply line diameters shown on drawings match calculated pipe sizes
   - Drain pipe diameters and slopes on drawings match drainage calculations
   - Fixture connection sizes on drawings match fixture unit sizing
   - Pump specifications on drawings match pump selection calculations
   - Vent pipe diameters on drawings match vent sizing calculations
   - Cistern, septic tank, and mud sump locations on drawings are consistent with calculation assumptions

Flag any discrepancies for resolution before drawings are issued for construction. Source: _SEMANTIC_LENSING.md item D-002.

9.5 Review the Design Assumption Documentation for completeness: confirm that each assumption has an ID, description, source/basis, status, and confirmation date (where resolved). Verify that assumptions confirmed or invalidated during design iterations are updated with the resolution and date. This step serves as the assumption audit trail for design progression. Source: _SEMANTIC_LENSING.md item A-004.

9.6 Submit the calculation package as part of the Safety Code permit application package (PKG-009 coordination).

Output: Final assembled Plumbing Calculation Package (DEL-006-07) — P.Eng.-stamped.

---

## Verification

The following checks shall be performed before the calculation package is considered complete:

| Check | Pass Criterion |
|---|---|
| All RFP-specified system parameters addressed | Cistern ≥ 50,000 L, pump ≥ 100 LPM, 2.5" fill connection, septic = 2,000 US gal confirmed in calculations |
| Peak demand scenario documented | Simultaneous demand scenario identified and flow rates calculated |
| Emergency shower supply confirmed | Minimum flow and pressure per applicable standard verified |
| All floor drain locations addressed | All drains shown on R-06 drawing have sizing calculations |
| Wash bay drainage to mud sump sized | Pipe sizing and sump connection documented |
| Vent stack sizing complete | All fixtures vented per NPC (ASSUMPTION); vent termination clearances (height above roof, clearance from air intakes, snow/ice blockage clearance) verified per NPC (specific values TBD once code edition confirmed). Source: _SEMANTIC_LENSING.md item C-004. |
| Septic sizing confirms 2,000 US gal adequacy | Estimated daily flow and pump-out frequency documented |
| Code compliance matrix complete | All applicable code requirements mapped to design |
| Assumptions documented | All engineering and Design-Builder assumptions listed in design assumption sub-artifact. Each assumption entry includes: assumption ID, description, source/basis, status (open / confirmed / invalidated), and confirmation date. Assumptions resolved during design iterations are updated with resolution and date. Source: _SEMANTIC_LENSING.md item X-006. |
| P.Eng. stamp present | Cover sheet signed and stamped by Alberta-licensed P.Eng. |
| Cross-reference to IFC drawings | Calculation values consistent with drawing dimensions and pipe sizes shown. Cross-reference checklist per Step 9.4: supply line diameters, drain pipe diameters and slopes, fixture connection sizes, pump specifications, vent pipe diameters, cistern/septic/sump locations. Source: _SEMANTIC_LENSING.md item D-002. |
| Hold Point 1 passed (after Step 2) | Peak demand scenario reviewed for reasonableness; cistern drawdown rate checked; all R-06 fixture types accounted for. Source: _SEMANTIC_LENSING.md item A-005. |
| Hold Point 2 passed (after Step 5) | Supply and drainage sizing internally consistent; drainage slopes meet minimum code requirements; mud sump gravity drainage confirmed. Source: _SEMANTIC_LENSING.md item A-005. |
| Assumption audit trail complete | Assumption documentation reviewed per Step 9.5; resolved assumptions updated with resolution and date. Source: _SEMANTIC_LENSING.md item A-004. |

---

## Records

The following evidence/documents shall result from executing this procedure and form the final DEL-006-07 calculation package:

| Record | Description |
|---|---|
| Design Assumption Documentation | All assumptions made during engineering, with rationale |
| Water Demand and Consumption Calculations | Fixture unit count, process demand, simultaneous demand, daily consumption |
| Water Supply Line Sizing Calculations | Pipe diameters for all supply branches |
| Pressure Drop and Pump Selection Calculations | System curve, pump operating point, pressure available at fixtures |
| Equipment Performance Data Sheets | Pump data sheets (internal distribution pump, bulk fill pump); must include manufacturer's pump performance curves as evidence for REQ-002 verification. Source: _SEMANTIC_LENSING.md item X-003. |
| Drainage System Sizing and Slope Calculations | Drain pipe diameters, slopes, DFU counts |
| Vent Stack Sizing Calculations | Vent pipe diameters and configuration |
| Septic System Sizing Calculations | Holding tank capacity confirmation, daily flow estimate, pump-out frequency |
| Code Compliance Matrices | NPC / Alberta Safety Code compliance cross-reference |
| P.Eng.-Stamped Cover Sheet | Signed and stamped by Alberta-licensed Plumbing Engineer |
| Calculation Package (assembled) | Complete DEL-006-07 as submitted for permit and retained in project record |
