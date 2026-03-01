# Specification — DEL-001-08 Finish Schedule

**Document Type:** Specification (normative)
**Deliverable ID:** DEL-001-08
**Deliverable Name:** Finish Schedule
**Package:** PKG-001 Architectural Design
**Discipline:** Architect
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment by 4_DOCUMENTS)

---

## Scope

### In Scope

DEL-001-08 is a Schedule-type architectural deliverable that shall provide a comprehensive interior finish schedule for:

1. All rooms and functional areas within the New North Shop addition (~13,000 sq ft usable area), covering the full program of spaces as shown in Appendix B (App B, R-04) and described in RFP S3.1 and S3.4 (R-01).
2. All interior areas within the Old North Shop that are subject to renovation under SOW-0070 through SOW-0074 (kitchenette renovation, mezzanine/coffee room renovation, washroom renovation, new locker/change room, washroom expansion).

The Finish Schedule shall enumerate, for each room/area, the specified finish for:
- Floor (substrate, finish system, and any special embedments such as steel floor plates)
- Walls (including base and any partial-height treatments)
- Ceiling (including clear height where applicable)

The Finish Schedule forms part of the complete final architectural design package (SOW-0011) that must be produced under PKG-001 Architectural Design and shall be coordinated with all other PKG-001 drawing deliverables (DEL-001-02 through DEL-001-11).

### Out of Scope

- Structural design of floor slabs, walls, or roof (PKG-002 Structural)
- Mechanical system specifications (PKG-003 Mechanical)
- Electrical system specifications (PKG-004 Electrical)
- Plumbing system specifications (PKG-006 Plumbing)
- Exterior finishes (addressed by DEL-001-03 Exterior Elevations and DEL-001-11 Architectural Specification)
- Site finishes (gravel driving surface, civil grading — PKG-005 Civil)
- Door and window hardware/glazing (DEL-001-07 Door & Window Schedule)
- Construction-level product submittals and mock-ups (post-IFC phase)

---

## Requirements

### REQ-DS-001: Schedule Format
The Finish Schedule shall be presented in tabular format with at minimum the following columns: Room/Area ID, Room/Area Name, Floor Finish, Wall Finish (base and field), Ceiling Finish, and Remarks/Notes.
- **Source:** Industry standard architectural schedule practice; SOW-0011 (R-01 S1.0, S3.1)
- Room/Area IDs shall be consistent with those used in the Architectural Floor Plans (DEL-001-02) and Interior Elevations (DEL-001-05).

### REQ-DS-001a: Drawing Number and Sheet Identification
The Finish Schedule shall carry a drawing number and sheet number consistent with the PKG-001 drawing index, so that the document is traceable within the complete IFC drawing set.
- **Source:** Lensing item X-005; supported by REQ-DS-013 (IFC stamp requirement) and Procedure Step 7.4 (drawing number consistency check).
- The specific drawing number convention is TBD — to be established as part of the PKG-001 drawing index at design development.

### REQ-DS-002: Complete Room Coverage
The Finish Schedule shall include every enclosed room and functional area in the addition and in the Old North Shop renovation scope.
- **Source:** SOW-0011 (R-01 S1.0, S3.1); SOW-0070-SOW-0074 (Decomposition)
- No room or area identified in the architectural floor plans (DEL-001-02) shall be omitted.

### REQ-DS-003: Industrial Durability — Main Shop, Wash Bay, Service Pit
Finish selections for the Main Shop repair bays, Wash Bay, and Service Pit shall be appropriate for heavy industrial use, including resistance to vehicular traffic, oil, grease, and hydraulic fluid exposure, and impact from tracked and packer-type heavy equipment.
- **Source:** RFP S3.4 (steel plates for tracked/packer equipment, sump drains in repair bays); App B (steel plate locations, service trench)
- ASSUMPTION: The Architect shall select products with demonstrated performance in comparable industrial maintenance environments. Specific product requirements TBD at design development.

### REQ-DS-003a: Service Trench Cover — Type and Finish
The Finish Schedule shall specify the service trench (A-03) cover type (e.g., steel plate cover, grating, or concrete lid), its finish treatment, and its load rating classification. The trench cover is a walking and driving surface within the Main Shop floor plane and shall meet the same industrial durability requirements as the surrounding floor (REQ-DS-003). Cover type and finish shall be coordinated with the structural design (DEL-002).
- **Source:** Lensing item C-001; App B (service trench shown as linear element within Main Shop); Guidance C-02 (service trench cover detail identified as requiring specification).
- TBD: Specific cover type and load rating to be determined at design development in coordination with structural engineer.

### REQ-DS-004: Steel Floor Plates — Main Shop
The Finish Schedule shall note the locations and extent of embedded steel floor plates in the Main Shop concrete slab floor, consistent with App B conceptual layout. The schedule shall also state whether steel plates receive a finish coating or are left uncoated, and whether edge treatment or weld pattern requirements apply.
- **Source:** RFP S3.4 ("Steel plating in concrete at strategic locations to accommodate track and packer type heavy equipment"); App B
- Clarification (per lensing item A-002): The Specification requires an explicit statement on steel plate finish treatment. If no coating is applied, the schedule shall state "no floor coating over steel plates" with reference to structural engineer approval. If edge treatment or weld pattern requirements apply, these shall be noted or cross-referenced to DEL-002 structural details.

### REQ-DS-005: Wet Area Finishes — Wash Bay
Finish selections for the Wash Bay shall be appropriate for a high-moisture environment with drainage to a mud sump. Floor finish shall be compatible with floor drain installations and wash water discharge.
- **Source:** RFP S3.4 ("Single enclosed bay dedicated for washing large equipment"); App B (Wash Bay Mud Sump)

### REQ-DS-005a: Wash Bay Floor Slope
The Wash Bay floor shall be sloped at a minimum of 2% toward floor drains to ensure positive drainage. Slope direction and rate shall be noted on the Finish Schedule or cross-referenced to the Architectural Floor Plan (DEL-001-02).
- **Source:** Lensing item B-003; Procedure Step 3.3 (minimum 2% slope to drain for wash bays — promoted from procedural guidance to normative requirement). Industry standard drainage practice for enclosed equipment wash areas.
- Coordination: Slope and drain location to be coordinated with PKG-006 Plumbing.

### REQ-DS-006: Wet Area Finishes — Washroom / Locker-Change Room
Finish selections for the Washroom / Locker-Change Room (with laundry), and any other wet-area rooms shall be appropriate for wet/humid conditions and regular cleaning.
- **Source:** RFP S3.4 ("Expand washroom facilities to include urinal and locker change room, including laundry services"); App B
- **Terminology note:** Per the project terminology convention, "Washroom / Locker-Change Room" is the canonical name for the consolidated wet-area block encompassing washroom, urinal, locker room, change room, and laundry functions. See Datasheet A-07 and Guidance terminology note.

### REQ-DS-006a: Waterproofing Membrane — Wet Areas
Wet-area floor finishes in the Wash Bay (A-02), Washroom / Locker-Change Room (A-07), Old North Shop Washroom (B-03), and Locker / Change Room (B-04) shall include a waterproofing membrane under floor finishes where required by the Alberta Building Code. The membrane type and installation standard shall be noted in the Finish Schedule or cross-referenced to DEL-001-11 Architectural Specification.
- **Source:** Lensing item F-001; Procedure Step 4.1 (lists "waterproofing membrane" as a code compliance check item). Promoted from procedural check to normative requirement because membrane installation is a code-driven construction requirement, not merely a verification step.
- TBD: Specific membrane product and applicable ABC clause to be confirmed at design development after occupancy classification is determined (see REQ-DS-007a).

### REQ-DS-007: Code Compliance
All specified finish materials shall comply with the applicable edition of the Alberta Building Code (NBC 2019 Alberta Edition, or the edition in force at time of permit application) and all applicable Alberta Safety Codes.
- **Source:** RFP S3.3.2 ("The building design must adhere to all applicable building codes and regulations"); RFP S3.3.2 ("The proposed building must adhere to all Alberta Safety Codes")
- ASSUMPTION: The ABC (NBC 2019 Alberta Edition) is the applicable building code. Specific clause requirements (flame spread, smoke development, occupancy-specific finishes) shall be determined by the Architect based on occupancy classification and shall be noted in the Specification (DEL-001-11).

### REQ-DS-007a: Occupancy Classification Determination
The Architect shall determine and record the occupancy classification(s) under the Alberta Building Code for all areas of the building (e.g., Group F Division 2 or 3 for industrial areas; Group D for office — ASSUMPTION). The occupancy classification shall be documented in the Finish Schedule remarks or in DEL-001-11 and shall be the basis for determining applicable flame spread, smoke development, and finish material requirements under REQ-DS-008.
- **Source:** Lensing item A-001; REQ-DS-007 and REQ-DS-008 both reference ABC compliance but neither identifies the occupancy classification that drives which code clauses apply. Without occupancy classification, prescriptive direction for finish selection is incomplete.
- TBD: Occupancy classification to be determined by Architect during design development.

### REQ-DS-008: Fire and Flame-Spread Requirements
Finish materials in occupancies or locations where the Alberta Building Code imposes flame spread or smoke development limits shall be specified accordingly. The Finish Schedule shall include a notation column or remarks field for any regulated material classifications.
- **Source:** RFP S3.3.2 (code compliance); ASSUMPTION: ABC Part 3 occupancy classification will require flame spread ratings for wall and ceiling finishes in applicable areas. Exact ratings TBD by Architect at design development.
- **Acceptance criteria (per lensing item A-003):** Once occupancy classification is determined (REQ-DS-007a), specific numeric flame spread rating (FSR) and smoke development classification (SDC) limits shall be stated for each applicable area (e.g., FSR <= 25, SDC <= 50 for exits and corridors — ASSUMPTION based on typical NBC requirements; actual limits TBD per confirmed occupancy). The Verification table entry for this requirement shall include measurable acceptance thresholds, not only "Architect code check."

### REQ-DS-009: Welding Station — Non-Combustible Requirement
Finishes in the immediate vicinity of the Welding Station shall be non-combustible or shall meet the applicable fire-separation and flame-spread requirements of the Alberta Building Code for areas proximate to welding operations.
- **Source:** RFP S3.4 ("Ventilation at welding station"); App B (Welding Station shown in Main Shop)
- ASSUMPTION: Non-combustible finish requirements per ABC are anticipated; Architect to confirm at design development.

### REQ-DS-010: Mezzanine Finish — Load Compatibility
Floor finish on the Mezzanine shall be compatible with heavy storage loads (oil totes, pumping equipment) and shall not impair the structural capacity of the mezzanine deck.
- **Source:** RFP S3.4 ("Mezzanine storage above utility and parts room capable of handling heavy items such as several oil totes and oil pumping equipment"); App B
- **Verification criterion (per lensing item X-003):** Structural engineer shall provide written confirmation that the proposed finish dead load does not exceed the mezzanine deck design allowance. This coordination sign-off shall be documented before the finish selection is finalized. See Verification table.

### REQ-DS-011: Renovation Areas — Match or Complement Existing
Finish selections for the Old North Shop renovation areas (B-01 through B-04) shall be appropriate for their respective uses and shall be reviewed in the context of the existing building fabric. Where the renovation connects to existing finishes, the Finish Schedule shall note transition conditions.
- **Source:** RFP S3.4 ("Renovate 250 square foot kitchenette area located in the existing building"); App B (Old North Shop Mezzanine, washroom below)
- ASSUMPTION: Existing finish substrate conditions in Old North Shop are TBD pending site investigation (site meeting per RFP S3.2).
- **Acceptance criteria for site investigation (per lensing item X-002):** The site investigation shall produce documented evidence of existing substrate conditions sufficient to confirm finish compatibility. Minimum scope shall include: (1) visual inspection of existing floor, wall, and ceiling substrates; (2) moisture testing of concrete slabs where new floor finishes are proposed; (3) documentation of existing finish types, condition ratings, and remediation requirements. The evidence standard (visual only, destructive testing, or moisture testing) shall be defined by the Architect before the investigation and documented in the investigation scope. TBD: Architect to define minimum site investigation scope at post-award.

### REQ-DS-012: Ceiling Height Notation
The Finish Schedule shall include a notation for ceiling height (or "exposed to structure" at 35 ft) for the Main Shop to communicate the clear height requirement established in the RFP.
- **Source:** RFP S3.4 ("Concrete structure 35' ceiling"); App B

### REQ-DS-013: IFC Stamp Requirement
The Finish Schedule, as part of the IFC drawing set for PKG-001, shall be signed/stamped by a professional engineer (or architect, as applicable under Alberta regulations) licensed to practice in the Province of Alberta.
- **Source:** RFP S3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta")
- ASSUMPTION: In Alberta, architectural drawings are stamped by a registered Architect (AIAA member); the Architect of Record is responsible for the finish schedule stamp.

---

## Standards

| Standard / Code | Applicability | Access Status | Specific Clause References |
|---|---|---|---|
| Alberta Building Code (NBC 2019 Alberta Edition) | Governing building code — occupancy classification, flame spread, smoke development, wet area requirements | Referenced in RFP S3.3.2; text not directly accessible — location TBD | TBD — specific Part 3 clauses for occupancy classification, flame spread (Division B fire safety), and wet-area requirements to be populated after occupancy classification is determined (REQ-DS-007a). Per lensing item D-001. |
| Alberta Safety Codes Act | Overarching safety compliance requirement | Referenced in RFP S3.3.2; text not directly accessible — location TBD | General applicability |
| CCDC 14-2013 | Contract form governing design-build obligations including design deliverable requirements | Referenced in RFP S2.7; text not directly accessible — location TBD | General applicability |
| Alberta Architects Act / AIAA regulations | Professional stamp/seal requirements for architectural drawings | ASSUMPTION: applicable; text not directly accessible — location TBD | General applicability |

---

## Verification

| Requirement | Verification Approach | Acceptance Criteria |
|---|---|---|
| REQ-DS-001 (Schedule format) | Architect internal QC review: confirm all required columns present; cross-check room IDs against DEL-001-02 floor plans | All required columns present; room IDs match DEL-001-02 |
| REQ-DS-001a (Drawing number) | Drawing index cross-check: confirm drawing number and sheet number per PKG-001 convention | Drawing number assigned and consistent with PKG-001 drawing index |
| REQ-DS-002 (Complete room coverage) | Checklist comparison: every room/area on DEL-001-02 appears in the Finish Schedule | Room count in Finish Schedule equals room count on DEL-001-02; no omissions |
| REQ-DS-003 (Industrial durability — heavy areas) | Design review: product data sheets confirm performance ratings for heavy industrial use | Product data sheets on file demonstrating industrial-grade performance |
| REQ-DS-003a (Service trench cover) | Coordination review: trench cover type, finish, and load rating documented; structural sign-off from DEL-002 | Trench cover specified with load rating; structural engineer written confirmation on file |
| REQ-DS-004 (Steel floor plates noted) | Drawing/schedule cross-check: steel plate locations in App B and DEL-001-02 are noted in the Finish Schedule remarks; finish treatment statement present | Steel plate locations noted; explicit finish treatment statement (coated or uncoated) present |
| REQ-DS-005 (Wash Bay wet area) | Design review: confirm floor drain compatibility and moisture-resistant finish specification | Floor drain compatibility confirmed; moisture-resistant finish specified |
| REQ-DS-005a (Wash Bay floor slope) | Drawing/schedule review: slope notation present (minimum 2% to drain); coordination with PKG-006 documented | Slope >= 2% noted; plumbing coordination documented |
| REQ-DS-006 (Washroom / Locker-Change Room wet area) | Design review: confirm wet-area finish specifications for all relevant rooms | Wet-area specifications present for A-07, B-03, B-04 |
| REQ-DS-006a (Waterproofing membrane) | Code review: confirm membrane requirement per ABC; membrane type noted in schedule or DEL-001-11 | Membrane type specified where code-required; ABC clause reference documented |
| REQ-DS-007 (Code compliance) | Architect code review against applicable ABC edition; confirmed at building permit application | Code review documented; no non-compliant materials |
| REQ-DS-007a (Occupancy classification) | Architect determination: occupancy classification recorded in Finish Schedule remarks or DEL-001-11 | Occupancy classification documented with ABC Part 3 reference |
| REQ-DS-008 (Flame spread) | Architect code check: flame spread/smoke development ratings noted in schedule or DEL-001-11 Specification, with numeric FSR/SDC limits per occupancy | Numeric FSR and SDC limits stated for each regulated area; product certifications on file (TBD after occupancy classification) |
| REQ-DS-009 (Welding station non-combustible) | Architect fire review: confirm non-combustible finish requirements addressed | Non-combustible finish specified for welding zone; ABC compliance confirmed |
| REQ-DS-010 (Mezzanine load compatibility) | Coordination with DEL-002 (Structural): structural engineer written confirmation that finish dead load does not exceed mezzanine deck design allowance | Structural engineer written sign-off on file confirming finish dead load is within design allowance |
| REQ-DS-011 (Renovation areas — transitions) | Site investigation (post-award): documented evidence of existing substrate conditions per defined investigation scope; Finish Schedule updated as required | Site investigation report on file with visual inspection, moisture testing, and condition ratings per Architect-defined scope |
| REQ-DS-012 (Ceiling height notation) | Schedule review: 35 ft ceiling height or "exposed to structure" notation present for A-01 Main Shop | Notation present |
| REQ-DS-013 (IFC stamp) | Pre-issue check: Architect's stamp on issued drawings per AIAA requirements | Stamp present on IFC issue |

---

## Documentation

### Required Artifacts

| Artifact | Description | Source |
|---|---|---|
| Finish Schedule (tabular) | Primary deliverable — interior finish schedule by room/area covering floor, wall, ceiling for all areas in scope | _CONTEXT.md Anticipated Artifacts; SOW-0011 |
| Coordination notes | Remarks column in schedule noting special conditions (steel plates, wet areas, fire ratings, ceiling heights, renovation transitions, trench cover, slope) | REQ-DS-003a, -004, -005, -005a, -006, -006a, -008, -009, -011, -012 |

### Coordination with Other Deliverables

The Finish Schedule shall be coordinated with:
- DEL-001-02 Floor Plans — room IDs and layout (must match)
- DEL-001-05 Interior Elevations — wall finish extents and heights
- DEL-001-06 Reflected Ceiling Plans — ceiling finish types and heights
- DEL-001-11 Architectural Specification — product specifications, standards, and flame spread ratings
- DEL-002 Structural Design deliverables — mezzanine and slab structural requirements affecting finish selections; service trench cover coordination

### Lensing Items Incorporated at Pass 3

| Lensing Item | Incorporation |
|---|---|
| A-001 | Added REQ-DS-007a (occupancy classification determination) |
| A-002 | Strengthened REQ-DS-004 with explicit steel plate finish treatment requirement |
| A-003 | Added measurable acceptance criteria to REQ-DS-008 verification (numeric FSR/SDC) |
| B-003 | Added REQ-DS-005a (Wash Bay floor slope minimum 2%) |
| C-001 | Added REQ-DS-003a (service trench cover type and finish) |
| D-001 | Added specific clause reference column to Standards table (TBD pending occupancy) |
| F-001 | Added REQ-DS-006a (waterproofing membrane for wet areas) |
| F-002 | Normalized terminology in REQ-DS-006 to canonical "Washroom / Locker-Change Room" |
| X-002 | Added site investigation acceptance criteria to REQ-DS-011 |
| X-003 | Added structural engineer sign-off artifact to REQ-DS-010 verification |
| X-005 | Added REQ-DS-001a (drawing number and sheet identification) |
