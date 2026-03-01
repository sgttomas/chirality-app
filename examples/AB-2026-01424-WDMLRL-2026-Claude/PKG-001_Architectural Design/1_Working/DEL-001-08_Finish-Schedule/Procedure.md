# Procedure — DEL-001-08 Finish Schedule

**Document Type:** Procedure (operational)
**Deliverable ID:** DEL-001-08
**Deliverable Name:** Finish Schedule
**Package:** PKG-001 Architectural Design
**Discipline:** Architect
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment by 4_DOCUMENTS)

---

## Purpose

This Procedure describes the steps the Architect and design team shall follow to **produce** the Finish Schedule (DEL-001-08) as an Issued For Construction (IFC) document. The procedure covers the production workflow from initial room list assembly through internal review, coordination, and final issue.

This procedure is written for the design-build context: the Architect has design latitude in finish selection, subject to County review at Preliminary Design and code compliance at IFC.

---

## Prerequisites

### P-PRE-01: Required Inputs
Before beginning the Finish Schedule, the following must be available or underway:

| Input | Source | Status | Sequencing Notes |
|---|---|---|---|
| Confirmed floor plan room layout and room IDs | DEL-001-02 Architectural Floor Plans (in progress or issued for coordination) | Must be at least sufficiently advanced to list all rooms with IDs | Gate for Step 1 |
| Conceptual drawing (Appendix B, Shop) | R-04 — available | Available | Available now |
| RFP S3.1 and S3.4 (program and design requirements) | R-01 — available | Available | Available now |
| Preliminary Design approval from County | RFP S3.3.2 | Required before IFC issue; Finish Schedule included in Preliminary Design submission | Gate for Step 7 (IFC issue) |
| Applicable Alberta Building Code edition | ASSUMPTION: NBC 2019 Alberta Edition | Must be confirmed at time of permit application | Required for Step 4 |
| Occupancy classification determination | Architect (REQ-DS-007a) | TBD — to be determined early in design development | Required before Step 4 can populate numeric flame spread thresholds |
| Site investigation results (for Old North Shop renovation areas) | Site meeting per RFP S3.2 (mandatory, March 3, 2026) and post-award investigation | Required to confirm existing substrate conditions for B-01 through B-04. **Sequencing (per lensing item X-001):** Site investigation is required before Step 3.6 (renovation finish selection) can be completed, but Steps 1-3.5 and Step 4 for New North Shop areas (A-series) may proceed in parallel while awaiting site investigation results. The Architect may advance to Step 4 (code review) and Step 5 (coordination) for all A-series areas without waiting for site investigation. B-series areas shall remain at preliminary category (Step 2) until site investigation is complete. | Gate for Step 3.6 (B-series only); A-series steps may proceed in parallel |
| Structural design input (mezzanine and slab) | DEL-002 Structural Design deliverables | Required for mezzanine floor finish dead load coordination (REQ-DS-010) and service trench cover coordination (REQ-DS-003a) | Gate for Step 3.5 and Step 3.7 |
| Plumbing coordination (floor drain locations, Wash Bay drain) | PKG-006 Plumbing deliverables | Required for Wash Bay and wet area floor finish slope/drain coordination | Gate for Step 3.3 |

### P-PRE-02: Required References
The following references must be accessible during production:

| Reference | Document |
|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf (S3.1, S3.4) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf — conceptual floor plan |
| Alberta Building Code (NBC 2019 Alberta Edition) | Architect's office reference (location TBD in project files) |
| DEL-001-02 Floor Plans | Issued for coordination |
| DEL-001-05 Interior Elevations | Issued for coordination (or developed concurrently) |
| DEL-001-06 Reflected Ceiling Plans | Issued for coordination (or developed concurrently) |
| DEL-001-11 Architectural Specification | Developed concurrently |

---

## Steps

### Step 1: Compile Room List from Floor Plans (DEL-001-02)

1.1 Extract every enclosed room and functional area from the Architectural Floor Plans (DEL-001-02), using the confirmed room IDs as they appear on the drawings.

1.2 Include both the New North Shop addition areas (A-01 series) and the Old North Shop renovation areas (B-01 series), consistent with the room area definitions in the Datasheet.

1.3 Add any interior functional zones shown in App B that are not yet named as discrete rooms on the floor plan (e.g., Welding Station, Wash Station — refer to Guidance CF-DS-001 for the Wash Station ambiguity). If the human ruling on CF-DS-001 has been made, apply it; otherwise, include the Wash Station as a provisional row with a note "pending CF-DS-001 resolution."

1.4 Confirm that the room list in the Finish Schedule is exhaustive — no room or area on DEL-001-02 shall be omitted (REQ-DS-002).

> **Output of Step 1:** Populated room list (column 1 of Finish Schedule table) with IDs matching DEL-001-02.

---

### Step 2: Assign Preliminary Finish Categories by Area Use

2.1 Using the use condition classifications in the Datasheet and the principles in the Guidance, assign a preliminary finish category to each room for floor, wall, and ceiling:

| Category | Typical Floor | Typical Wall | Typical Ceiling |
|---|---|---|---|
| Heavy Industrial (Main Shop, Wash Bay) | Concrete — sealed/epoxy / steel plates as noted | Concrete/masonry — painted or exposed | Exposed structure (or open-to-structure notation) |
| Wet Industrial (Service Pit, floor drains) | Concrete — sealed/epoxy, slope to drain | Concrete/masonry — sealed | Open-to-structure or sealed concrete above |
| Light Industrial / Storage (Parts Room, Utility Room, Mezzanine) | Concrete — sealed (ASSUMPTION) | Painted masonry or drywall (ASSUMPTION) | Exposed structure or painted (ASSUMPTION) |
| Office / Staff (Office) | VCT / LVT / carpet tile (ASSUMPTION) | Painted drywall (ASSUMPTION) | Suspended T-bar (ASSUMPTION; see Guidance T-02) |
| Wet / Hygiene (Washroom / Locker-Change Room, Laundry) | Ceramic tile or sealed concrete (ASSUMPTION) — with waterproofing membrane where code-required (REQ-DS-006a) | Ceramic tile or FRP panels (ASSUMPTION; see Guidance T-03) | Moisture-resistant painted drywall or FRP (ASSUMPTION) |
| Renovation (Old North Shop areas) | TBD pending site investigation | TBD pending site investigation | TBD pending site investigation |

2.2 Flag all finish category assignments as ASSUMPTION until confirmed with product data sheets and code review (Steps 3 and 4).

2.3 Consult Guidance Section Trade-offs (T-01, T-02, T-03) for areas where product category selection is not straightforward.

> **Output of Step 2:** Draft Finish Schedule table with preliminary finish category per area.

---

### Step 3: Select Specific Finish Products

3.1 For each preliminary finish category, select a specific finish product or system. Document:
- Generic system description (e.g., "Two-component water-based epoxy floor coating, 15-20 mil DFT")
- Acceptable manufacturer(s) or equal basis-of-design product
- Colour/pattern (or "County selection" for staff-occupied spaces where aesthetic preference applies)

3.2 For the Main Shop steel plate areas: note on the schedule whether steel plates receive a finish coating or are left uncoated, and state edge treatment or weld pattern requirements (or cross-reference to DEL-002 structural details). Default: "Embedded steel floor plates — see Structural drawings. No floor coating over steel plates unless specifically approved by Structural Engineer." (REQ-DS-004; see also Guidance CF-DS-003.)
- Source: REQ-DS-004; RFP S3.4; App B.

3.3 For the Wash Bay: confirm floor finish slope direction and rate (minimum 2% slope to drain per REQ-DS-005a), drain type, and connection to mud sump. Coordinate with PKG-006 Plumbing.
- Source: REQ-DS-005, REQ-DS-005a; RFP S3.4; App B (Wash Bay Mud Sump).

3.4 For wet hygiene areas (Washroom / Locker-Change Room, Laundry): confirm full wet-area treatment (floor to ceiling or to minimum required height) and grout joint specifications where tile is used. Confirm waterproofing membrane requirement per REQ-DS-006a and note membrane type in schedule or cross-reference to DEL-001-11.
- Source: REQ-DS-006, REQ-DS-006a.

3.5 For the Mezzanine: confirm dead load of proposed floor finish with structural engineer before finalizing specification. Obtain structural engineer written confirmation per REQ-DS-010 verification criteria.
- Source: REQ-DS-010.

3.6 For Old North Shop renovation areas: following site investigation (see Sequencing Notes in P-PRE-01), confirm substrate conditions and update finish selections. If existing substrate requires remediation (crack repair, leveling, moisture treatment) before new finishes can be applied, note remediation requirement in the Finish Schedule remarks column. The site investigation shall follow the defined evidence standard per REQ-DS-011 acceptance criteria (visual inspection, moisture testing, condition ratings).
- Source: REQ-DS-011; RFP S3.2.

3.7 For the Service Trench cover (A-03): select cover type (steel plate, grating, or concrete lid), finish treatment, and confirm load rating classification in coordination with the structural engineer (DEL-002). Note the trench cover specification in the Finish Schedule as a distinct element within the A-03 row or as a sub-row, consistent with REQ-DS-003a.
- Source: REQ-DS-003a; Guidance C-02; lensing item C-002.

> **Output of Step 3:** Draft Finish Schedule with specific product or system identified per area per element (floor/wall/ceiling), including trench cover specification.

---

### Step 4: Code Compliance Review

4.1 The Architect shall conduct a code compliance review of all specified finish materials against the applicable Alberta Building Code, specifically:
- **Occupancy classification** for each area (REQ-DS-007a — this must be determined before numeric flame spread and smoke development thresholds can be confirmed). If occupancy classification has not yet been determined, complete it before proceeding with the code compliance review.
- Flame spread rating (FSR) and smoke development classification (SDC) of wall and ceiling finish materials in all regulated spaces, with numeric limits per occupancy (e.g., FSR <= 25, SDC <= 50 for exits and corridors — ASSUMPTION; actual limits per confirmed occupancy classification).
- Wet area requirements (waterproofing membrane per REQ-DS-006a, floor slope per REQ-DS-005a, transition conditions).
- Non-combustible finish requirements in the welding area (REQ-DS-009) and any other areas where ABC requires it.

4.2 Add a "Code Rating" or "Remarks" column to the Finish Schedule table for any finish material where a code-governed performance rating must be declared (e.g., FSR 25 max, SDC 50 max — per REQ-DS-008 acceptance criteria; confirm after occupancy classification).

4.3 Update any non-compliant finish selections identified in 4.1 before proceeding.

> **Output of Step 4:** Code-reviewed Finish Schedule with flame spread / wet area / non-combustible notations as required.

---

### Step 5: Cross-Coordination with Other PKG-001 Deliverables

5.1 Compare the Finish Schedule against DEL-001-05 Interior Elevations:
- Wall finish type and height as shown on Interior Elevations must match the Finish Schedule.
- Partial-height tile or FRP wainscots must be dimensioned consistently.

5.2 Compare the Finish Schedule against DEL-001-06 Reflected Ceiling Plans:
- Ceiling finish type and ceiling height notation must match the Finish Schedule.
- The 35 ft exposed-structure notation in the Main Shop must appear consistently.

5.3 Compare the Finish Schedule against DEL-001-11 Architectural Specification:
- Each finish product specified in the Finish Schedule must have a corresponding specification section in DEL-001-11.
- Flame spread ratings noted in the Finish Schedule must match the product descriptions in DEL-001-11.

5.4 Confirm room IDs are identical across DEL-001-02, DEL-001-05, DEL-001-06, and DEL-001-08 (this Finish Schedule).

5.5 Document any discrepancies found and resolve before IFC issue. If a discrepancy cannot be resolved without a design decision, flag it in the Finish Schedule remarks column as "COORDINATION REQUIRED — see [reference]."

5.6 Complete the cross-coordination checklist (see below) and file the completed checklist as a coordination sign-off record.

#### Cross-Coordination Checklist Template (per lensing item X-004)

The following checklist shall be completed and signed off by the Architect before proceeding to Step 6. Minimum content:

| Coordination Point | Checked Against | Status (OK / Discrepancy / N-A) | Discrepancy Description | Resolution |
|---|---|---|---|---|
| Room IDs match | DEL-001-02 Floor Plans | | | |
| Wall finish types and heights match | DEL-001-05 Interior Elevations | | | |
| Ceiling finish types and heights match | DEL-001-06 Reflected Ceiling Plans | | | |
| Product specifications correspond | DEL-001-11 Architectural Specification | | | |
| Flame spread ratings consistent | DEL-001-11 Architectural Specification | | | |
| Mezzanine finish dead load confirmed | DEL-002 Structural (written sign-off) | | | |
| Service trench cover coordinated | DEL-002 Structural (written sign-off) | | | |
| Steel plate treatment coordinated | DEL-002 Structural | | | |
| Wash Bay slope and drain coordinated | PKG-006 Plumbing | | | |
| Wet area waterproofing coordinated | DEL-001-11 Architectural Specification | | | |
| Drawing number per PKG-001 index | PKG-001 Drawing Index | | | |

> **Output of Step 5:** Coordinated Finish Schedule consistent with all other PKG-001 drawing set deliverables. Completed cross-coordination checklist on file.

---

### Step 6: Preliminary Design Submission (County Approval Gate)

6.1 Include the draft Finish Schedule in the Preliminary Design submission to Camrose County for approval.
- Source: RFP S3.3.2 ("Deliver Preliminary Design for the County project team to approve").

6.2 For staff-occupied spaces (Office, Washroom / Locker-Change Room, Kitchenette), include colour palette options or County-selection callouts in the Finish Schedule to allow the County to make aesthetic selections within the Architect's specified system. Specifically identify the following aesthetic selection points (per lensing item D-002):

| Area | Finish Element | County Selection Type | Presentation Format |
|---|---|---|---|
| A-06 Office | Floor covering type and colour | County selects from Architect-curated options (e.g., 3 LVT colour options) | Colour/material sample board or digital palette |
| A-06 Office | Wall paint colour | County selects from Architect-curated options | Paint chip samples |
| A-07 Washroom / Locker-Change Room | Wall tile or FRP colour/pattern | County selects from Architect-curated options | Tile/FRP samples or digital images |
| A-07 Washroom / Locker-Change Room | Floor tile colour | County selects from Architect-curated options | Tile samples |
| B-01 Kitchenette | Countertop material and colour | County selects from Architect-curated options (TBD — ASSUMPTION that kitchenette includes countertop) | Material samples |
| B-01 Kitchenette | Wall finish colour | County selects from Architect-curated options | Paint chip or FRP samples |

> **Note:** The above list is an ASSUMPTION based on typical County aesthetic input points for staff-occupied spaces. The Architect shall confirm which finish selections require County aesthetic input during design development and update this list accordingly.

6.3 Document County feedback and incorporate revisions. If County requests a finish not consistent with industrial durability requirements or code compliance, the Architect shall advise the County in writing and propose an alternative.

> **Output of Step 6:** County-approved Finish Schedule (or marked with County comments for resolution).

---

### Step 7: Final IFC Issue

7.1 Incorporate all post-Preliminary-Design changes into the Finish Schedule.

7.2 Ensure the Finish Schedule is signed/stamped by the Architect of Record per Alberta Architects Act and AIAA requirements.
- Source: REQ-DS-013; RFP S3.3.2.

7.3 Issue the Finish Schedule as part of the complete IFC drawing set for PKG-001.

7.4 Confirm that the Finish Schedule issue date, revision number, and drawing number are consistent with the PKG-001 drawing index (REQ-DS-001a).

> **Output of Step 7:** IFC Finish Schedule — signed, stamped, and issued as part of PKG-001 IFC drawing set.

---

## Verification

| Step | Verification Check |
|---|---|
| Step 1 | Room list count in Finish Schedule equals room count on DEL-001-02; all room IDs match |
| Step 2 | All rooms have an assigned finish category; all ASSUMPTIONs flagged |
| Step 3 | Each area has a specific product/system identified for floor, wall, and ceiling; steel plate zones, trench cover, and drain slopes noted |
| Step 3.7 | Service trench cover type, finish, and load rating specified; structural coordination documented |
| Step 4 | Code review documented; occupancy classification determined (REQ-DS-007a); flame spread ratings with numeric thresholds noted where required; non-combustible zones confirmed; waterproofing membrane noted for wet areas |
| Step 5 | Cross-coordination checklist completed and signed off; no unresolved discrepancies |
| Step 6 | County approval obtained or outstanding comments documented and addressed |
| Step 7 | IFC issue confirmed; Architect's stamp present; drawing number and revision consistent with PKG-001 drawing index |

---

## Records

The following records shall be retained as evidence that this procedure was completed:

| Record | Description | Retention |
|---|---|---|
| Draft Finish Schedule (pre-County review) | Preliminary version submitted to County at Preliminary Design | Project file |
| County Preliminary Design approval documentation | Written County acknowledgment or meeting minutes confirming approval | Project file |
| Code compliance review notes | Architect's recorded code check against ABC for flame spread, wet areas, non-combustible requirements, including occupancy classification determination | Project file |
| Cross-coordination checklist (completed) | Signed-off checklist per Step 5.6 template, documenting all coordination points with DEL-001-02, -05, -06, -11, DEL-002, and PKG-006 | Project file |
| Structural engineer sign-off — mezzanine finish dead load | Written confirmation from structural engineer per REQ-DS-010 | Project file |
| Structural engineer sign-off — service trench cover | Written confirmation from structural engineer per REQ-DS-003a | Project file |
| IFC Finish Schedule (stamped) | Final issued-for-construction version, bearing Architect's stamp | Drawing record set; County submission; as-built file |
| Site investigation report (Old North Shop) | Documented evidence of existing substrate conditions for renovation areas, per defined investigation scope (REQ-DS-011 acceptance criteria) | Project file |

### Lensing Items Incorporated at Pass 3

| Lensing Item | Incorporation |
|---|---|
| X-001 | Added sequencing notes to P-PRE-01 clarifying parallel/serial relationship between A-series and B-series steps relative to site investigation |
| C-002 | Added Step 3.7 for service trench cover specification |
| D-002 | Added aesthetic selection points table to Step 6.2 |
| X-004 | Added cross-coordination checklist template to Step 5.6 |
| F-002 | Normalized terminology to canonical "Washroom / Locker-Change Room" throughout |
| A-002 | Strengthened Step 3.2 with explicit finish treatment and edge treatment requirement for steel plates |
| B-003 | Updated Step 3.3 with minimum 2% slope reference (REQ-DS-005a) |
| F-001 | Added waterproofing membrane reference to Step 3.4 and Step 4.1 |
| A-001 | Added occupancy classification as prerequisite for Step 4; updated Step 4.1 sequencing |
| A-003 | Updated Step 4.2 with numeric FSR/SDC threshold requirement |
| X-002 | Strengthened Step 3.6 with site investigation evidence standard reference |
| X-003 | Updated Step 3.5 with structural engineer sign-off requirement |
| X-005 | Updated Step 7.4 with REQ-DS-001a reference |
| E-002 | Implicit: revision convention established in Datasheet supports Step 7.4 |
