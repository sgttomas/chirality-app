# Procedure — DEL-003-03 Ductwork & Distribution Plans

---

## Purpose

This procedure describes the steps to produce the Ductwork & Distribution Plans drawing set (DEL-003-03) as a complete, P.Eng.-stamped, IFC-ready deliverable. The procedure covers the Mechanical Engineer's design production workflow from preliminary inputs through IFC issuance, consistent with the design-build project requirements under CCDC 14–2013 and the RFP.

---

## Prerequisites

### Required Prior Deliverables

| Deliverable | Status Required | Reason |
|---|---|---|
| DEL-003-01 (Preliminary Mechanical Design) | County-approved | County approval of preliminary design is mandatory before IFC issuance (Source: RFP §3.3.2) |
| DEL-003-02 (HVAC Layout Plans) | Substantially complete (equipment locations fixed) | Ductwork routing originates from equipment locations; routing cannot be finalized without knowing equipment placement |
| DEL-003-06 (Mechanical Calculation Package) | Sufficiently advanced to provide design airflows | Duct sizing is driven by calculated airflow requirements |
| DEL-008-01 (Geotechnical Investigation & Report) | Complete | Foundation and slab conditions may affect below-grade mechanical penetrations (service pit ventilation) |
| DEL-001 set (Architectural Floor Plans, Sections) | Issued for coordination | Space geometry, ceiling heights, and room dimensions needed for duct routing |
| DEL-002 set (Structural Drawing Set) | Issued for coordination | Concrete structural member locations, crane rail positions, and permitted penetration zones required |

### Required References

| Reference | Purpose |
|---|---|
| AB-2026-01424-WDMLRL RFP.pdf — §3.4, §3.3.2 | RFP requirements for HVAC systems and IFC drawing standards |
| AB-2026-01424-Appendix B (Shop).pdf | Conceptual layout — spaces, equipment notes, mechanical room location |
| AB-2026-01424-Appendix B (Electrical).pdf | Ceiling fan locations for spatial coordination |
| Alberta Building Code (applicable edition) | Ventilation and HVAC design code compliance |
| Alberta Safety Codes (applicable regulations) | Safety code compliance for mechanical systems |
| ASHRAE standards (applicable editions) | Ventilation rates, duct design methodology (ASSUMPTION: applicable) |
| SMACNA HVAC Duct Construction Standards (applicable edition) | Duct fabrication standards (ASSUMPTION: applicable) |

### Personnel Prerequisites

| Role | Requirement |
|---|---|
| Mechanical Engineer of Record | P.Eng. licensed in the Province of Alberta; responsible for design, calculations, and stamp |
| Mechanical CAD/BIM Technologist | Proficiency in project's CAD/BIM platform; **specific platform and file format requirements TBD** — to be confirmed by Project Coordinator at project commencement (Lensing: C-003) |
| Project Coordinator | Facilitates interdisciplinary coordination reviews |

---

## Steps

### Step 1 — Confirm Scope Boundary with Project Team

1.1 Confirm the boundary between DEL-003-03 (Ductwork & Distribution Plans) and DEL-003-04 (Exhaust System Plans) with the Mechanical Engineer and Project Coordinator. Document the agreed boundary in writing. Refer to CON-003-03-01 in Guidance.md.

1.2 Confirm ceiling fan coordination responsibility. Determine whether fan locations are to be shown on mechanical ductwork drawings or electrical drawings only. Refer to CON-003-03-02 in Guidance.md.

1.3 Record agreed boundaries and confirm with all relevant discipline leads before beginning detailed drawing production.

- Source: ASSUMPTION — standard coordination step for design-build; no explicit step stated in RFP.

### Step 2 — Collect Design Inputs

2.1 Obtain approved architectural floor plans (DEL-001 set) and confirm room dimensions, wall locations, and ceiling heights for all spaces in the addition.

2.2 Obtain structural coordination drawings (DEL-002 set) and identify:
   - Concrete beam and column grid locations
   - Permitted penetration zones through floor, walls, and roof
   - Crane rail positions (two 5-tonne cranes on trolleys — Source: RFP §3.4; Appendix B)
   - Service pit structural details (DEL-002-06)
   - Mezzanine framing details (DEL-002-05)

2.3 Obtain equipment locations and airflow requirements from:
   - DEL-003-02 (HVAC Layout Plans) — equipment positions
   - DEL-003-06 (Mechanical Calculation Package) — design airflows per space and system

2.4 Confirm utility room location as the primary mechanical equipment room, consistent with Appendix B (Shop) conceptual drawing.

- Source: Appendix B (Shop); Decomposition §7 (DEL-002, DEL-003-02, DEL-003-06 cross-references).

### Step 3 — Develop Ductwork Routing

3.1 Lay out primary (main) duct runs from mechanical equipment in the utility room to each served zone. Coordinate main duct routing with crane clearance envelopes and structural member locations.

3.2 For the main shop (repair bays):
   - Route supply air for the forced-air makeup air (MUA) system to provide adequate distribution across both drive-through repair bays (each ~24 ft wide per Appendix B).
   - **Destratification strategy decision point (Lensing: A-004):** Select and document the destratification duct strategy for the 35 ft ceiling (Source: RFP §3.4). Options include mid-height distribution drops vs. high-level discharge relying on ceiling fans for mixing (see Guidance Trade-offs table). This decision affects duct routing geometry, structural penetration requirements, and coordination with the 6 ceiling fan positions (Source: Appendix B Electrical). Record the selected strategy and rationale before finalizing duct routing.

3.3 For the wash bay:
   - Route ventilation supply/exhaust ductwork appropriate for an enclosed industrial wash bay. Coordinate with wash bay enclosure structure (DEL-011-05).

3.4 For the service pit:
   - Route ventilation ductwork down to the service pit/trench. Identify and flag structural penetrations through the concrete floor slab.
   - Source: RFP §3.4 — "Ventilated and lighted service pit area."

3.5 For office, parts room, utility room, and mezzanine:
   - Route ductwork per calculated airflow requirements. Confirm mezzanine ventilation extent with Mechanical Engineer.

3.6 Branch duct runs from primary mains to terminal units (diffusers, grilles, registers) in each space. Show branch takeoff locations, duct sizes, and terminal locations.

- Source: ASSUMPTION — standard duct design procedure; no explicit routing steps stated in accessible sources.

### Step 4 — Size Ductwork

4.1 Apply duct sizing methodology (equal friction, velocity reduction, or other method per Mechanical Engineer's selection) to size all duct runs consistent with DEL-003-06 calculated airflows.

4.2 Record duct sizes, airflow quantities, and friction rates in a duct sizing schedule or on the drawings themselves.

4.3 Verify that duct velocities are appropriate for the application (e.g., main supply, branch, exhaust) consistent with applicable ASHRAE/SMACNA standards (ASSUMPTION: applicable; location TBD).

4.4 Confirm that sized ductwork physically fits within available ceiling/plenum space given structural constraints. Adjust routing or sizing as needed.

- Source: ASSUMPTION — standard duct design practice; Alberta Building Code requirements TBD.

### Step 5 — Structural Penetration Coordination

5.1 Compile a list of all required structural penetrations for ductwork through concrete walls, floors, and the roof.

5.2 Submit penetration list to the Structural Engineer (DEL-002 responsible party) for review and approval.

5.3 Incorporate structural engineer's requirements (size limits, reinforcement, sleeve specifications) into the ductwork drawings.

5.4 Ensure ductwork routing does not conflict with crane rail beams, crane travel paths, mezzanine framing, or service pit structure.

- Source: ASSUMPTION — mandatory coordination for concrete structure; RFP §3.4 (concrete structure, cranes).

### Step 6 — Interdisciplinary Coordination Review

6.1 Issue ductwork coordination drawings (or BIM model coordination views) to all discipline leads for clash review. At minimum, coordinate with:
   - Structural (clearances, penetrations)
   - Architectural (ceiling/plenum space, room heights)
   - Electrical (ceiling fan positions — CON-003-03-02; lighting — DEL-004-04)
   - Exhaust system (boundary interface with DEL-003-04)
   - Plumbing (wash bay drainage routing — DEL-006 set)

6.2 Document and resolve all coordination conflicts before proceeding to IFC.

6.3 Update drawings to reflect coordination outcomes.

- Source: ASSUMPTION — standard IFC coordination; RFP §3.3.2 (fully coordinated final design required).

### Step 7 — Prepare IFC Drawing Set

7.1 Finalize all ductwork routing, sizing, and annotation on the drawing set.

7.2 Ensure the drawing set includes:
   - Plan views showing ductwork routing at appropriate levels
   - Duct sizing schedule or annotated dimensions on all runs
   - Section/elevation views for areas with complex routing or height constraints (particularly at 35 ft ceiling)
   - Coordination notes and cross-references to DEL-003-02, DEL-003-04, and DEL-002 set
   - Structural penetration callouts or reference to penetration schedule
   - Equipment connection details (duct collars, transitions)
   - Legend and general notes consistent with PKG-003 drawing set standards

7.3 Complete internal QC review.

7.4 Submit drawing set to Mechanical Engineer of Record for final review and P.Eng. stamp.

- Source: RFP §3.3.2 (IFC drawings must be signed/stamped by P.Eng. licensed in Alberta).

### Step 8 — County Preliminary Approval (if not yet obtained)

> Note: County approval of the preliminary mechanical design (DEL-003-01) must be obtained before IFC issuance. If this approval has not been confirmed prior to beginning detailed ductwork drawing production, the IFC drawings shall be withheld from issuance until approval is documented.

8.1 Confirm County written approval of DEL-003-01 is on record.

8.2 If not approved, initiate the County approval process before issuing DEL-003-03 IFC.

- Source: RFP §3.3.2 — "Deliver Preliminary Design for the County project team to approve."

### Step 9 — Issue IFC Drawing Set

9.1 Issue DEL-003-03 as an IFC (Issued for Construction) drawing set with:
   - P.Eng. stamp and signature on all sheets
   - IFC revision designation per the project's drawing revision tracking convention (Lensing: E-001 — revision numbering and tracking convention TBD; to be specified by Project Coordinator; at minimum, each revision shall carry a unique revision number, date, and description of changes)
   - Issue date

9.2 Distribute to: Project Manager, General Contractor, Mechanical Contractor (PKG-013 responsible party), and County project representative.

9.3 File issued set in the project document control system. Ensure drawing revision history is recorded in the document control system per the project's revision tracking convention (Lensing: E-001).

- Source: RFP §3.3.2, §3.1 (weekly coordination; County project manager).

### Step 10 — Post-IFC Field Coordination (Lensing: F-004)

> **Note:** This step addresses field change management after IFC issuance. For a concrete structure where field modifications to ductwork routing are difficult and costly, the workflow should reference the project's change management process.

10.1 When field conditions require ductwork routing changes after IFC issuance (e.g., unforeseen structural conflicts, equipment changes, contractor-initiated modifications), initiate a Request for Information (RFI) or field change request per the project's change management protocol (TBD — to be established under the CCDC 14-2013 contract provisions).

10.2 All field changes affecting ductwork routing, sizing, or coordination shall be reviewed by the Mechanical Engineer of Record and documented.

10.3 As-built documentation: Upon construction completion, update the drawing set (or issue a separate as-built drawing set) reflecting all field changes. File in the project document control system.

- Source: ASSUMPTION — standard post-IFC field coordination process for design-build projects; CCDC 14-2013 governs change management; specific process TBD.

---

## Verification

| Check | What to Confirm | When |
|---|---|---|
| Space coverage | All served spaces shown on ductwork drawings | Before IFC issuance |
| Duct sizing schedule complete | All major duct runs have sizes shown or tabulated | Before IFC issuance |
| P.Eng. stamp present | All IFC sheets carry Mechanical Engineer's stamp and signature | At IFC issuance |
| County preliminary approval confirmed | DEL-003-01 approval documented | Before IFC issuance |
| Structural coordination complete | No unresolved duct/structure conflicts; penetrations approved | Before IFC issuance |
| Interdisciplinary coordination complete | No unresolved clashes with architectural, electrical, exhaust, plumbing | Before IFC issuance |
| Scope boundary confirmed | DEL-003-03 vs. DEL-003-04 boundary documented and consistently applied on drawings | Before detailed drawing production (Step 1) |
| Crane clearance confirmed | Ductwork routing does not conflict with crane travel envelope | Before IFC issuance |
| Service pit ventilation shown | Service pit ventilation ductwork shown and penetrations identified | Before IFC issuance |
| Code compliance | Mechanical Engineer certifies compliance with Alberta Building Code and Safety Codes | At IFC issuance |

---

## Records

| Record | Description | Responsible |
|---|---|---|
| Signed IFC drawing set | P.Eng.-stamped DEL-003-03 drawing set | Mechanical Engineer |
| Duct sizing schedule | Tabulated duct dimensions, airflows, and velocities | Mechanical Engineer |
| Coordination conflict log | Record of identified and resolved coordination conflicts (Steps 5, 6); **minimum fields: date, discipline, conflict description, resolution, responsible party, status** (Lensing: E-002 — standardized format to ensure consistent judgment record quality) | Project Coordinator |
| Structural penetration approval | Written confirmation from Structural Engineer of approved penetrations | Structural Engineer |
| County approval of DEL-003-01 | Written confirmation of preliminary mechanical design approval (Step 8) | Project Manager |
| Scope boundary agreement | Written record of DEL-003-03 vs. DEL-003-04 boundary (Step 1) | Project Coordinator / Mechanical Engineer |
| Safety Code inspection reports | Inspection results related to mechanical/HVAC systems | Project Manager (per RFP §3.3.2) |
| Drawing revision history | Revision tracking record per project convention — revision number, date, description of changes for each revision (Lensing: E-001) | Project Coordinator |
| Field change / RFI log | Record of post-IFC field changes to ductwork routing, reviewed by Mechanical Engineer (Lensing: F-004) | Project Coordinator |
| As-built drawing set | Updated drawing set (or separate as-built set) reflecting all field changes at construction completion (Lensing: F-004) | Mechanical Engineer |
