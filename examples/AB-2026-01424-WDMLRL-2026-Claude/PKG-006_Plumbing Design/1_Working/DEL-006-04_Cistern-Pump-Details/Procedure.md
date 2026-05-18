# Procedure — DEL-006-04: Cistern & Pump Details

---

## Purpose

This procedure describes the steps to produce the Cistern & Pump Details drawing set (DEL-006-04) — the engineered plumbing drawing set for the on-site cistern water storage system and associated pump systems for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. The drawing set must be produced by the Plumbing Engineer, coordinated with other disciplines, and issued as IFC (Issued for Construction) drawings stamped by a P.Eng. licensed in Alberta.

This procedure addresses the design and drawing production workflow. It does not cover physical installation (PKG-014).

---

## Prerequisites

### Upstream Information Required

| Prerequisite | Source Deliverable / Document | Status |
|---|---|---|
| Preliminary plumbing design approved by County | DEL-006-01 (Preliminary Plumbing Design) | Required before IFC issue |
| Architectural floor plans — utility room and building layout | DEL-001-02 (Architectural Floor Plans) | Required for spatial coordination |
| Structural design — slab, utility room, foundation details | DEL-002 (Structural Design package) | Required to confirm cistern installation type (in-slab, above-grade) and structural loads |
| Geotechnical investigation report | DEL-008-01 (Geotech Report) | Required if cistern is below-grade; informs material selection |
| Electrical design — available circuits, panel locations | DEL-004 (Electrical Design) | Required for pump electrical interface coordination |
| Civil / site grading plan | DEL-005-02 (Site Grading Plan) | Required for bulk fill point location and overflow drainage path |
| RFP §3.4 and Appendix B (Plumbing) | R-01, R-06 | Source performance requirements |

*Note: DEL-006-01 (Preliminary Design) is a formal prerequisite per the project workflow. The decomposition does not explicitly declare upstream dependencies for DEL-006-04 beyond SOW-0016 scope. The above are ASSUMPTION: standard design coordination prerequisites.*

### Required References

| Reference | Document |
|---|---|
| RFP §3.4 — Design Requirements | AB-2026-01424-WDMLRL RFP.pdf |
| Appendix B (Plumbing) — Conceptual Plumbing Layout | AB-2026-01424-Appendix B (Plumbing).pdf |
| Applicable edition of National Plumbing Code of Canada (as adopted in Alberta) | To be confirmed by Plumbing Engineer |
| Alberta Safety Codes Act and regulations | To be confirmed by Plumbing Engineer |
| CCDC 14–2013 (contract form) | For warranty / guarantee obligations |

### Personnel

| Role | Responsibility |
|---|---|
| Plumbing Engineer (P.Eng., Alberta) | Lead designer; stamps IFC drawings |
| Structural Engineer | Coordination on cistern type, slab penetrations, structural loads |
| Electrical Engineer | Coordination on pump electrical interface |
| Civil Engineer | Coordination on bulk fill point location; overflow drainage |
| Project Manager / Design-Builder | Drawing distribution, County approval coordination |

---

## Steps

### Step 1 — Confirm Scope and Performance Requirements

1.1 Review RFP §3.4 to confirm cistern minimum volume (50,000 L), pump minimum flow rate (100 LPM), and 2.5" filling connection requirement.

1.2 Review Appendix B (Plumbing) conceptual drawing to understand the intended location and configuration of the cistern, water taps, pressure washer reel, and bulk fill point.

1.3 Confirm with Project Manager which systems are to be included in this drawing set (DEL-006-04) versus other plumbing deliverables (DEL-006-02 distribution plans, DEL-006-03 drain/vent plans).

1.4 Review CONF-001 and CONF-002 in Guidance.md and flag for resolution before proceeding if impact on design direction is significant.

### Step 2 — Establish Design Basis

2.1 Determine final cistern volume:
- Minimum 50,000 L per RFP §3.4.
- Perform demand analysis (peak flow, fill truck frequency, operational reserve) — document in DEL-006-07 calculation package.

2.2 Determine cistern type and installation method:
- Consult with Structural Engineer regarding available space, slab details, and structural capacity.
- Confirm whether cistern is below-grade, in-slab, or above-grade in utility room.
- If below-grade: obtain geotech report (DEL-008-01) before finalizing design.

2.3 Determine distribution pump design:
- Calculate total dynamic head (TDH) for the distribution system at 100 LPM minimum flow.
- Select pump model meeting ≥ 100 LPM at design TDH.
- Determine pressurization approach (pressure tank or VFD pump) — document decision basis.

2.4 Determine bulk fill pump design:
- Establish required flow rate for external truck-fill operation — TBD based on Owner operational requirements.
- Select high-volume pump for external filling (SOW-0044).

2.5 Confirm electrical requirements for all pumps and provide interface data to Electrical Engineer (voltage, phase, amperage, motor kW) for circuit inclusion in PKG-004.

2.6 Confirm bulk fill connection point location with Civil Engineer for coordination with site access and drainage.

### Step 3 — Coordinate with Other Disciplines

3.1 Issue coordination requests to:
- Structural Engineer: cistern installation details, slab penetrations, structural loads from cistern (full and empty), pump pad requirements.
- Electrical Engineer: pump motor data for circuit sizing; confirm which pump corresponds to "fire hose pump" circuit in electrical drawing (see CONF-002, Guidance.md).
- Civil Engineer: bulk fill point location, overflow drainage path.
- Architect: utility room space confirmation, access opening locations.

3.2 Obtain written confirmation of coordination responses before finalizing drawings. **Minimum acceptable documentation forms [D-002]:** coordination confirmations must be in one of the following forms: (a) signed coordination drawing markup, (b) formal RFI response, (c) email from responsible discipline engineer with explicit confirmation statement, or (d) meeting minutes signed by both parties. Verbal confirmations are not sufficient for contract administration purposes in a design-build context. [D-002]
*Note: coordination is an ongoing process; do not defer all coordination to end of design.*

### Step 4 — Produce Drawing Set

4.1 Produce cistern plan view drawing:
- Show cistern location, plan dimensions, clearances, inlet/outlet piping connections, overflow connection, drain connection, vent connection, access opening, and isolation valve locations.
- Annotate all pipe sizes, materials, and slopes.

4.2 Produce cistern section view drawing:
- Show cistern depth, wall construction, inlet/outlet elevations, overflow elevation, internal baffling (if applicable), access hatch, and ladder (if required).

4.3 Produce pump equipment schedule:
- Include for each pump: tag number, type, manufacturer/model (or performance specification), rated flow (LPM), TDH (m or kPa), motor power (kW), voltage/phase/Hz, connection sizes, notes.

4.4 Produce piping and connection details:
- Detail the cistern filling connection (2.5 inch per RFP §3.4) with isolation valve, check valve, and union connections.
- Detail the distribution outlet from cistern to building distribution system.
- Detail the bulk fill connection point (external fill hose connection, backflow preventer, overflow).
- Detail any pressure tank connection (if included).

4.5 Produce control system diagram:
- Show level sensors/float switches for high-level alarm (overfill), low-level alarm, and pump enable/disable set points.
- Show pump control panel inputs/outputs (schematic).
- Coordinate with electrical discipline for control wiring.

4.6 Produce pressure tank detail (if included):
- Show pressure tank size, connection, pressure settings, and installation requirements.

4.7 Produce electrical connection diagram / interface table:
- List all motor loads with voltage, phase, amperage, and circuit designation.
- Cross-reference to electrical panel schedule (DEL-004-06).

4.8 Produce installation and maintenance access details:
- Show clearance envelopes for pump service, cistern access hatch, and bulk fill point.
- Note any special installation requirements (alignment, grouting, vibration isolation).

### Step 5 — Internal Review and Quality Check

5.1 Plumbing Engineer reviews all drawings against:
- RFP §3.4 requirements (checklist against R-001 through R-014 in Specification.md, including R-012 overflow protection, R-013 freeze protection, and R-014 pressure tank decision).
- Applicable plumbing code (NPC as adopted in Alberta — confirm edition per A-001).
- Coordination responses from other disciplines.
- Guarantee period compliance: confirm equipment warranty documentation covers construction period + 2 years post-CCC (RFP §2.10) [F-003].

5.2 Check cross-document consistency:
- Confirm pipe sizes, system pressures, and flow rates are consistent between this drawing set and DEL-006-02 (water distribution plans).
- Confirm pump electrical data matches what was provided to Electrical Engineer.
- Confirm cistern location is consistent with DEL-001-02 (architectural floor plans) and DEL-002 (structural drawings).

5.3 Resolve any inconsistencies before submitting for County approval.

### Step 6 — County Approval (Preliminary Design Stage)

*Note: Per RFP §3.3.2 and SOW-0010f, preliminary design must be delivered for County approval before final design proceeds. This step applies to the preliminary version of this drawing set.*

6.1 Package preliminary drawings for submission to County project manager.
6.2 Coordinate County review meeting if required.
6.3 Incorporate County comments and document responses.

### Step 7 — IFC Issue

7.1 Complete final drawings incorporating all discipline coordination and County approval comments.

7.2 Plumbing Engineer of Record signs and stamps all drawings per RFP §3.3.2 (P.Eng. licensed in Alberta).

7.3 Issue IFC drawing set to construction package.

7.4 Submit to applicable safety authority for plumbing permit as part of Safety Code permit application (SOW-0007; PKG-009).

---

## Verification

| Check | Method | Pass Criterion |
|---|---|---|
| Cistern volume shown on drawing | Measure/review drawing | Stated capacity ≥ 50,000 L |
| Pump flow rate on schedule | Review pump schedule | Rated flow ≥ 100 LPM at design TDH |
| 2.5" fill connection shown | Review connection detail | 2.5" annotated on drawing |
| Bulk fill system shown | Review drawing set | Bulk fill pump and fill point detailed |
| P.Eng. stamp present | Review IFC drawing title block | Stamp and signature of P.Eng. licensed in Alberta present |
| All connections coordinated | Review cross-discipline coordination log | No unresolved clashes or interface discrepancies |
| Code compliance notes present | Review drawing general notes | Reference to applicable Alberta Safety Codes and NPC edition noted |
| Safety Code permit submitted and accepted | Review permit application records (PKG-009) | Plumbing permit application submitted to safety authority and acceptance/permit number received prior to construction start [D-001] |
| County preliminary design approval obtained | Review County approval documentation (Step 6) | Written County acceptance of preliminary design on record before proceeding to IFC (per RFP §3.3.2) [X-004] |
| Equipment warranty meets guarantee period | Review manufacturer warranty documentation against RFP §2.10 | Pump equipment warranty covers construction period + 2 years post-CCC; warranty documentation on file [F-003] |

---

## Records

The following evidence documents should result from execution of this procedure:

| Record | Description |
|---|---|
| Issued-for-Construction (IFC) drawing set | Stamped drawings for DEL-006-04; filed in project drawing register |
| Pump equipment schedule | Final pump selection with manufacturer data sheets (filed in DEL-006-07 calculation package or attached to drawing) |
| Discipline coordination log | Written record of coordination exchanges with structural, electrical, and civil engineers |
| County approval record | Written County approval of preliminary design (email or formal letter) |
| Safety Code permit application reference | Cross-reference to plumbing permit application under PKG-009 |
| Design calculation reference | Cross-reference to DEL-006-07 (Plumbing Calculation Package) for cistern volume basis and pump TDH calculations |
