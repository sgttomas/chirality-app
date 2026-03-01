# Procedure — DEL-002-06: Service Pit / Trench Structural Details

---

## Purpose

This procedure describes the steps for the Structural Engineer to produce the Service Pit / Trench Structural Details drawing set (DEL-002-06) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. The procedure covers the production workflow from information gathering through IFC drawing issue.

This procedure governs production of the design drawing set artifact. The construction procedure for building the service pit is governed by DEL-011-06 (Service Pit/Trench construction package) and is outside the scope of this document.

---

## Prerequisites

### Information Prerequisites

| Item | Source | Status |
|---|---|---|
| Geotechnical Investigation Report (DEL-008-01) | PKG-008 — Geotechnical Engineer | Required before finalizing depth, wall thickness, waterproofing. If not available at design start, proceed with stated assumptions (see Step 3). |
| Conceptual floor plan (App B) | _Sources/AB-2026-01424-Appendix B (Shop).pdf | Available — conceptual dimensions 24' × 100' for service trench |
| RFP design requirements (§3.4, §3.3.2) | _Sources/AB-2026-01424-WDMLRL RFP.pdf | Available |
| Equipment load specification (governing axle load, track footprint, contact pressure) | Camrose County / Owner | TBD — must be obtained before cover system design (see CON-002 in Guidance.md) |
| Mechanical penetration requirements (ventilation duct routing, size, locations) | PKG-003 Mechanical Engineer | TBD — must be coordinated before structural drawings are issued IFC |
| Electrical penetration requirements (conduit, fixture mounting, lighting layout) | PKG-004 Electrical Engineer | TBD — must be coordinated before structural drawings are issued IFC |
| Plumbing drainage requirements within pit (drain location, sump, slope) | PKG-006 Plumbing Engineer | TBD — must be coordinated before structural drawings are issued IFC |
| Architectural floor plan (to confirm pit position relative to bays and building grid) | DEL-001-02 Architectural Floor Plans (PKG-001) | TBD — confirm when available |

### Personnel Prerequisites

| Requirement | Notes |
|---|---|
| Structural Engineer of Record | P.Eng. licensed to practice structural engineering in the Province of Alberta (required per RFP §3.3.2) |
| Structural drafting/BIM technician | As applicable to the firm's production workflow |
| Discipline coordinators | Mechanical, Electrical, Plumbing, Architectural — for penetration and interface coordination |

### Reference Documents (to have on hand)

| Document | Purpose |
|---|---|
| NBC 2019 (Alberta edition) — ASSUMPTION: applicable | Structural loads, occupancy requirements |
| CSA A23.3 — Design of Concrete Structures — ASSUMPTION: applicable | Reinforced concrete design |
| CSA S16 — Design of Steel Structures — ASSUMPTION: applicable | Steel cover system design |
| Alberta OH&S Code — ASSUMPTION: applicable | Below-grade working space requirements |
| DEL-002-10 Structural Calculation Package template / format | Supporting calculations companion |
| DEL-002-12 Structural Specification | Material specifications governing construction |

---

## Steps

### Step 1 — Confirm Pit Geometry and Program with Owner/Architect

1.1 Review the conceptual floor plan (App B) and note the service trench labeled dimensions (approximately 24' wide × 100' long).

1.2 Confirm with the Architect (PKG-001) and Camrose County whether:
- The 24' and 100' dimensions represent interior clear dimensions or overall dimensions.
- The pit's position relative to the building column grid is confirmed.
- The pit is intended to serve one or both repair bays, or is a dedicated service trench bay.
- There are any Owner preferences for pit depth or access configuration.

1.3 Document confirmed geometry in the project coordination log. If confirmation is not available, state the assumption in writing (see CON-001 in Guidance.md — treat App B dimensions as interior clear until confirmed).

**Verification:** Written record of confirmed pit geometry (or documented assumption).

---

### Step 2 — Obtain Equipment Load Specification

2.1 Contact Camrose County (Owner) to obtain the governing equipment load specification for the service pit cover system. Required data:
- Equipment type(s) to be serviced over the pit.
- Gross operating weight.
- Axle loads or track loads.
- Track or tire footprint dimensions / contact area.

2.2 If the Owner cannot provide a specific load specification, use a conservative load representative of a motor scraper (ASSUMPTION: in the range of 400–700 kN total operating weight — ASSUMPTION; to be confirmed). Document the assumption.

2.3 Use the governing load for design of the pit cover system and pit edge conditions.

**Verification:** Equipment load specification received and documented, or assumption stated in calculation package (DEL-002-10).

---

### Step 3 — Review Geotechnical Report and Establish Design Parameters

3.1 Upon receipt of the Geotechnical Investigation Report (DEL-008-01):
- Extract the allowable bearing capacity at the pit founding elevation.
- Note the design groundwater level (if any) relative to the pit floor elevation.
- Note the design frost depth.
- Note the soil lateral earth pressure parameters (Ka, Kp, unit weight) for pit wall design.
- Note any special soil conditions (expansive soils, organics, deleterious materials).

3.2 If the geotechnical report is not yet available at the time structural design must proceed, state the following design assumptions in the calculation package and on the drawings:
- Design groundwater level: TBD — assume no groundwater within pit depth (conservative check required once geotech available).
- Design frost depth: ASSUMPTION — use 1.5 m minimum (confirm from geotech and NBC/Alberta Building Code).
- Lateral earth pressure: ASSUMPTION — use Ka = 0.33 (loose granular) or as appropriate until geotech is received.
- Bearing capacity: ASSUMPTION — use 100 kPa allowable (confirm from geotech before finalization).

3.3 Establish the pit floor elevation consistent with:
- Required working headroom below the underside of equipment.
- Frost depth — pit floor should be below design frost depth, or insulation/heating must be provided.
- Confirmed with Owner's equipment clearance requirements (Step 2).

**Deviation Threshold Criteria (Lensing ref: X-002):** When actual geotechnical data is received (DEL-008-01), the Structural Engineer shall compare the actual parameters against the preliminary design assumptions (Step 3.2). Redesign or re-assessment is required if any of the following thresholds are exceeded:
- Bearing capacity is less than the assumed value (100 kPa) by more than TBD%.
- Groundwater table is found above the pit floor elevation (vs. the assumption of no groundwater within pit depth).
- Design frost depth exceeds the assumed 1.5 m by more than TBD m.
- Lateral earth pressure coefficient (Ka) exceeds the assumed 0.33 by more than TBD.
- Any special soil conditions are identified (expansive soils, organics, deleterious materials) that were not assumed.

> The specific percentage/magnitude thresholds are TBD and should be established by the Structural Engineer of Record at the time of preliminary design. The purpose of these thresholds is to provide a decisive assessment anchor for determining when actual conditions diverge sufficiently from assumptions to require redesign.

**Verification:** Geotechnical parameters documented in calculation package (DEL-002-10), or assumptions explicitly stated with reference to geotech TBD.

---

### Step 4 — Complete Structural Analysis and Design

4.1 Design pit walls for:
- Lateral earth pressure (active pressure from retained soil; surcharge from equipment loads at grade).
- Any hydrostatic pressure (if groundwater above pit floor).
- Temporary construction loading (when pit is open during construction).

4.2 Design pit floor slab for:
- Upward hydrostatic pressure (if applicable).
- Residual bearing — confirm the slab is in contact with competent subgrade.
- Drainage slope (coordinate with PKG-006 Plumbing Engineer — if a floor drain or sump is required, the structural floor slab must accommodate the slope and any sump blockout).

4.3 Design the pit cover system for:
- Governing equipment live load (Step 2).
- Impact factor appropriate to moving tracked equipment.
- Deflection limits appropriate for the application (cover must not deflect excessively under load as this could impair removal or damage edge conditions).

4.4 Design pit edge conditions at floor level for:
- Transition from the pit wall to the building floor slab.
- Protection of the concrete edge (embedded steel angle or plate at pit lip — coordinate with embedded floor steel plates per App B).
- Cover system bearing/support at the edge.

4.5 Design pit access (stairs or ladder) structural support/embedments.

4.6 Document all design assumptions, load derivations, and calculation results in the Structural Calculation Package (DEL-002-10). Reference applicable code clauses and standard sections.

**Verification:** Calculation package complete; independent check by a second P.Eng. or senior engineer (ASSUMPTION — required as standard practice for engineer-stamped design).

**Independent Check Clarification (Lensing ref: C-003):** The independent check shall be performed as follows:
- **Checker qualification:** TBD — a second P.Eng. or senior engineer with structural design competence. The specific qualification requirement (e.g., must be a P.Eng., years of experience) should be confirmed per the firm's QA standard.
- **Scope of check:** The independent check shall cover, at minimum: (a) load derivation and application, (b) wall and slab design adequacy, (c) cover system capacity, (d) code compliance of critical details, (e) consistency between calculations and drawings.
- **Output record:** The checker shall produce a written record (signed check set or review memo) documenting items checked, any deficiencies noted, and resolution of deficiencies. This record shall be retained in the project QA file.
- Source: ASSUMPTION -- standard structural engineering QA practice.

---

### Step 5 — Coordinate Penetrations and Interfaces with Other Disciplines

5.1 Circulate the preliminary pit structural plan and sections to:
- Mechanical Engineer (PKG-003): confirm ventilation duct penetration locations, sizes, and routing.
- Electrical Engineer (PKG-004): confirm conduit and lighting fixture locations, mounting details, penetrations.
- Plumbing Engineer (PKG-006): confirm floor drain locations, slope direction, sump location (if required), pit drainage connection point.
- Architect (PKG-001): confirm access location, headroom, interface with architectural floor plan.

5.2 Incorporate coordinated penetration locations into the structural drawings as blockouts, sleeves, or formed openings. Do not leave penetrations to be field-cored unless unavoidable (field coring in reinforced concrete walls risks cutting rebar).

5.3 Document coordination outcomes in the project coordination log. Note any unresolved items as TBD with expected resolution date.

**Verification:** Coordinated penetration schedule included on structural drawings; sign-off from discipline leads on penetration locations (or written acknowledgment of TBD items).

---

### Step 6 — Produce Drawing Set

6.1 Prepare the structural drawing set for DEL-002-06. Minimum expected sheets (ASSUMPTION — adjust to project drawing standards):

| Sheet | Content |
|---|---|
| S-[x].1 | Service Pit Plan — overall dimensions, wall thickness, column/grid reference, cover system extent, penetration locations |
| S-[x].2 | Service Pit — Transverse Sections (multiple cuts showing wall depth, rebar, slab, edge condition) |
| S-[x].3 | Service Pit — Longitudinal Section (full 100' length, construction joints, access location) |
| S-[x].4 | Wall Reinforcement Details (typical and end conditions, corner details) |
| S-[x].5 | Pit Floor Slab Detail and Waterproofing |
| S-[x].6 | Cover/Grating System Detail (plan and section, load rating noted) |
| S-[x].7 | Edge Condition and Embedded Plate Detail at Pit Lip |
| S-[x].8 | Access Detail (stair or ladder structure and embedments) |
| S-[x].9 | Penetration/Blockout Schedule and Notes |

6.2 Include a general notes sheet or general notes block on the first sheet with:
- Design standard references (NBC, CSA A23.3, CSA S16).
- Concrete compressive strength (f'c) specification.
- Reinforcement grade specification.
- Minimum cover to rebar.
- Geotechnical report reference (or stated design assumptions if geotech TBD).
- Waterproofing system reference.

6.3 Apply the project title block, deliverable ID (DEL-002-06), revision level, and date.

**Verification:** Drawing set reviewed internally by Structural Engineer for completeness against this Specification.

---

### Step 7 — Internal QA Review

7.1 The Structural Engineer of Record reviews all drawings for:
- Completeness against the Specification requirements (R-001 through R-012).
- Internal consistency (dimensions, details, cross-references).
- Coordination with other discipline drawings (penetrations, access, interfaces).
- Code compliance.

7.2 Resolve any deficiencies noted in the review before submission for stamp.

7.3 Confirm all requirements from the Specification are addressed or documented as TBD with a resolution plan.

**Verification:** Internal review checklist completed and signed by reviewer.

---

### Step 8 — P.Eng. Stamp and Issue IFC

8.1 The Structural Engineer of Record (P.Eng., Alberta-licensed) reviews the complete drawing set.

8.2 The P.Eng. stamps and signs each sheet of the IFC drawing set.

8.3 **HOLD POINT — Geotechnical Report Receipt (Lensing ref: X-003):** Before applying the P.Eng. stamp to the IFC drawing set, the Structural Engineer shall verify one of the following conditions is met:
- **(a)** The Geotechnical Investigation Report (DEL-008-01) has been received, reviewed, and its parameters incorporated into the design (preferred), OR
- **(b)** A formal written decision to proceed without the geotech report has been documented, signed by the Structural Engineer of Record and acknowledged by the Project Manager, listing: (i) the specific design assumptions used in lieu of geotech data, (ii) the risks accepted, and (iii) the commitment to revise drawings upon receipt of geotech data if parameters fall outside the deviation thresholds (see Step 3, Deviation Threshold Criteria).

> This hold point is intended to prevent IFC issue without either confirmed geotech data or a formal, documented decision to proceed on assumptions. The absence of this gate was identified as a verification gap. Source: ASSUMPTION -- standard structural engineering practice for geotech-dependent designs.

8.4 Confirm the following before stamping:
- Geotechnical parameters have been received and incorporated, or the formal decision to proceed on assumptions has been documented per 8.3(b).
- Penetration coordination has been completed with all disciplines (or TBD items are clearly noted).
- Calculations supporting the design are complete (DEL-002-10).

8.5 Issue the drawing set as IFC (Issued for Construction) to the General Contractor (PKG-011) and to the project coordinator for inclusion in the permit set (PKG-009 Building Permit, DEL-009-02).

**Verification:** Drawings bear P.Eng. stamp and signature. IFC issue record documented.

---

### Step 9 — Post-Issue Coordination and RFI Management

9.1 During construction of DEL-011-06 (Service Pit/Trench), the Structural Engineer responds to Requests for Information (RFIs) from the General Contractor within a timeframe consistent with the project schedule.

9.2 If field conditions differ from design assumptions (e.g., groundwater encountered, unexpected soil conditions), issue a Structural Engineer's Supplemental Instruction (SI) or revised drawing as required.

9.3 Revise drawings and re-issue if:
- Geotech report is received after preliminary IFC and design parameters require updating.
- Penetration coordination changes after IFC issue.
- County-requested design changes are received.

**Verification:** RFI log maintained. Revised drawings issued under a new revision level with revision description noted.

---

## Verification

### Final Checklist Before IFC Issue

| Item | Check |
|---|---|
| Pit geometry confirmed with Owner/Architect | Yes / TBD |
| Equipment load specification obtained or documented assumption | Yes / TBD |
| Geotechnical parameters incorporated or assumptions stated | Yes / TBD |
| Wall design complete (lateral earth, surcharge, hydrostatic) | Yes / TBD |
| Floor slab design complete | Yes / TBD |
| Cover system designed and load-rated | Yes / TBD |
| Edge condition detailed | Yes / TBD |
| Access detail shown | Yes / TBD |
| Penetrations coordinated with MEP disciplines | Yes / TBD |
| General notes complete (standards, materials, geotech reference) | Yes / TBD |
| Calculation package (DEL-002-10) complete and cross-referenced | Yes / TBD |
| Internal QA review complete | Yes / TBD |
| P.Eng. stamp applied to all sheets | Yes / TBD |
| Conflicts in Guidance.md (CON-001, CON-002, CON-003) resolved or documented | Yes / TBD |
| Geotech hold point (Step 8.3) satisfied — geotech received or formal proceed-on-assumptions decision documented | Yes / TBD |
| Independent check scope, checker qualification, and output record documented (Step 4) | Yes / TBD |
| Deviation threshold criteria established for preliminary design assumptions (Step 3) | Yes / TBD |

---

## Records

The following records shall be produced and retained as evidence that this procedure was completed:

| Record | Owner | Location |
|---|---|---|
| Structural Calculation Package (DEL-002-10) | Structural Engineer | PKG-002 deliverable folder |
| Coordinated penetration confirmation from MEP disciplines | Structural Engineer / Project Coordinator | Project coordination log |
| Equipment load specification (or documented assumption) | Structural Engineer | DEL-002-10 calculation package |
| Geotechnical design parameter extraction (or stated assumptions) | Structural Engineer | DEL-002-10 calculation package |
| Internal QA review record | Structural Engineer | Project QA file |
| IFC drawing issue record (transmittal) | Project Coordinator | Project correspondence file |
| RFI log (during construction) | Project Coordinator / Structural Engineer | Project coordination log |
| P.Eng.-stamped IFC drawing set | Structural Engineer / General Contractor | Permit set; Construction documents |
| Inspection records (DEL-009-04) | Authority Having Jurisdiction / Project Coordinator | Code compliance records for the constructed service pit (cross-ref: Specification R-006 verification). (Lensing ref: E-002) |
| Geotech hold point decision record (if 8.3(b) applies) | Structural Engineer / Project Manager | Project QA file. (Lensing ref: X-003) |
