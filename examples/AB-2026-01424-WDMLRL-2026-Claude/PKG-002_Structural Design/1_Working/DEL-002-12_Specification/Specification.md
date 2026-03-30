# Specification — DEL-002-12 Structural Specification

**Document Type:** Specification (normative)
**Deliverable ID:** DEL-002-12
**Revision:** R1 — 2026-02-26
**Status:** SEMANTIC_READY (Pass 3 enrichment applied)

---

## Scope

### What This Specification Covers

This specification governs the preparation and content of the Structural Specification document for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition (New North Shop), Camrose County, Alberta.

The Structural Specification is a deliverable within PKG-002 (Structural Design) and covers the following SOW item:

- **SOW-0012:** Complete final structural design (concrete structure, 35 ft ceiling). [Source: RFP §3.4, App B; Decomposition §Scope Ledger]

The Structural Specification supports objectives:
- **OBJ-001:** Deliver a code-compliant, fully functional maintenance shop addition that satisfies the County's operational program and passes all applicable inspections. [Source: Decomposition §Objectives]
- **OBJ-003:** Produce complete, P.Eng.-stamped IFC design documentation across all disciplines before construction begins. [Source: Decomposition §Objectives]

### What This Specification Does Not Cover

- Foundation design (variable-price scope — covered by DEL-002-11, SOW-0019).
- Mechanical, electrical, plumbing, civil, or architectural design specifications.
- Construction execution (covered by PKG-010 — Foundation Construction; PKG-011 — Building Structure & Envelope).
- Geotechnical investigation (covered by PKG-008).

---

## Requirements

### REQ-001 — Structural System: Concrete Structure, 35 ft Ceiling

The structural system shall be designed as a concrete structure providing a minimum clear ceiling height of 35 ft.

- **Source:** RFP §3.4 ("Concrete structure 35' ceiling"), Appendix B notes.
- **Constraint:** The clear ceiling height of 35 ft is an explicit RFP requirement; no reduction is permissible without Owner approval.
- **Clarification required (TBD):** The RFP prescribes "concrete structure" as the material system. It does not prescribe the concrete construction method (tilt-up, cast-in-place, precast). The Structural Engineer shall confirm whether the construction method is open or constrained. ASSUMPTION: Construction method is open to Structural Engineer selection, subject to performance requirements. [Source: RFP §3.4; Guidance Consideration 1; Lensing: A-001]

### REQ-002 — Overhead Crane Support

The structural system shall incorporate supports for two (2) 5-tonne overhead cranes on a trolley system.

- **Source:** RFP §3.4 ("2 – 5-tonne overhead cranes on a trolley"), Appendix B.
- **Constraint:** Crane runway girder design loads, span, and runway geometry shall be established by the Structural Engineer based on selected crane equipment specifications. Crane specifications are TBD (to be provided by Owner or selected by Proponent).
- **Conditional hold:** Crane manufacturer specifications (wheel loads, runway gauge, bridge span, CMAA service class) are an **irrefutable prerequisite** for crane runway structural design. If crane specifications are not available at time of design, the Structural Engineer shall: (a) design the runway based on preliminary assumed parameters clearly documented as ASSUMPTION, and (b) include a contractual note requiring verification against final crane data and resubmission for engineering review if selection changes. The source and timeline for obtaining crane specifications must be established by the Owner / Proponent procurement. [Source: RFP §3.4; Procedure Step 3; Lensing: F-001]

### REQ-003 — Steel Plate Embedments in Concrete Floor

Steel plates shall be embedded in the concrete floor slab at strategic locations as indicated on the conceptual floor plan (Appendix B) to accommodate track and packer type heavy equipment.

- **Source:** RFP §3.4 ("Steel plating in concrete at strategic locations to accommodate track and packer type heavy equipment"), Appendix B (steel plate locations shown on floor plan).
- **Constraint:** Embedment locations and plate sizing shall be confirmed with the Owner / Architect. Plate design shall be coordinated with the floor slab structural design.
- **Corrosion protection (mandatory practice):** Steel embedment plates shall be provided with corrosion protection appropriate to the industrial environment, considering proximity to the wash bay and exposure to moisture, de-icing agents, and equipment fluids. The corrosion protection system (e.g., galvanizing, epoxy coating, or stainless steel) shall be specified by the Structural Engineer. ASSUMPTION: Corrosion protection is a mandatory practice gap identified by lensing; specific system TBD by Structural Engineer. [Source: Guidance Consideration 3; Lensing: A-002]

### REQ-004 — Service Pit / Trench

The structural design shall include a service pit (trench) for mechanics to perform servicing under equipment.

- **Source:** RFP §3.4 ("Ventilated and lighted service pit area for mechanics to perform servicing under equipment"), Appendix B (Service Pit shown on floor plan, 24 ft dimension).
- **Constraint:** The pit shall be structurally designed to carry applicable equipment loads at the edges. Ventilation and lighting penetrations through the pit structure shall be coordinated with the Mechanical and Electrical Engineers.
- **Performance criterion (TBD):** The specific edge load case (vehicle surcharge, equipment wheel loads, impact factors) and required factor of safety for the service pit structure must be established by the Structural Engineer. The verification approach shall include a quantitative pass/fail criterion, not merely dimensional confirmation on IFC drawings. [Source: RFP §3.4; Guidance Consideration 6; Lensing: E-003]

### REQ-005 — Mezzanine Structure (Load-Bearing)

A load-bearing mezzanine shall be provided over the Parts Room, Utility Room, and Wash Bay, capable of supporting heavy items including oil totes and oil pumping equipment.

- **Source:** RFP §3.4 ("Mezzanine storage above utility and parts room capable of handling heavy items such as several oil totes and oil pumping equipment"), Appendix B ("Load Bearing Over Parts Room + Utility For Storage", "Overhead Mezzanine over Parts Room/Utility Room/Wash Bay").
- **Material system clarification (TBD):** REQ-001 mandates a "concrete structure" overall, but this requirement does not explicitly state whether the mezzanine structural system must also be concrete or may be structural steel. If the mezzanine may use structural steel framing, the applicable design standard changes from CSA A23.3 to CSA S16. The Structural Engineer shall confirm the mezzanine material system. ASSUMPTION: Mezzanine material system is open to Structural Engineer selection within the context of a concrete building. [Source: Specification REQ-001; Lensing: D-001]
- **Constraint:** Design live load for the mezzanine shall be established by the Structural Engineer commensurate with the intended use. ASSUMPTION: A design live load of not less than 4.8 kPa (100 psf) is likely appropriate for this heavy storage application; this must be confirmed by the Structural Engineer against applicable code and Owner operational requirements. **Performance assessment of the mezzanine design cannot be completed without a confirmed live load value.** Owner confirmation of the design live load is a blocking prerequisite. [Source: RFP §3.4; Lensing: A-005]

### REQ-006 — Stair to Mezzanine

Structural stair access to the mezzanine shall be provided.

- **Source:** Appendix B ("Stairs to Mezzanine").
- **Constraint:** Stair design shall comply with applicable building code requirements for industrial occupancy. Covered by DEL-002-09 (Stair Details) but the Structural Specification shall include applicable material and performance requirements.

### REQ-007 — Wash Bay Mud Sump

A mud sump shall be provided on the exterior of the building at the wash bay for clean-out with an excavator.

- **Source:** RFP §3.4 ("Mud sump from wash bay on exterior of building for clean out with excavator"), Appendix B (Wash Bay Mud Sump label).
- **Constraint:** The sump structure shall be designed to withstand excavator loads and wash water hydrostatic conditions. Coordination with civil and plumbing designs is required.

### REQ-008 — Old North Shop Mezzanine Renovation

The existing Old North Shop mezzanine shall be renovated, and the washroom below shall be renovated with a new locker room.

- **Source:** Appendix B ("Old North Shop Mezzanine to be renovated and the washroom below renovated along with new locker room").
- **Constraint:** Structural assessment of the existing mezzanine structure is required prior to renovation design. Capacity of the existing structure is TBD pending assessment.

### REQ-009 — P.Eng. Stamp (Alberta)

All Issued for Construction (IFC) structural drawings and the Structural Specification shall be signed and stamped by a professional engineer (P.Eng.) licensed to practice in the Province of Alberta.

- **Source:** RFP §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta").

### REQ-010 — Code Compliance

The structural design shall adhere to all applicable Alberta Safety Codes, the National Building Code of Canada (NBC) as adopted in Alberta, and all applicable building regulations in force at time of permit application.

- **Source:** RFP §3.3.2 ("The building design must adhere to all applicable building codes and regulations"), §3.3.2 ("The proposed building must adhere to all Alberta Safety Codes").
- **Constraint:** Specific code edition shall be confirmed with the Authority Having Jurisdiction (AHJ) at time of permit application. ASSUMPTION: NBC 2019 as adopted by Alberta is likely the applicable edition; confirm with AHJ. **Compliance determination cannot proceed until the governing code edition is confirmed.** This is a blocking TBD that affects all structural design calculations and standards references. [Lensing: A-003]

### REQ-012 — Fire Resistance Rating (added by Pass 3 lensing)

The concrete structural system shall achieve the fire resistance rating required by the applicable building code for the building's occupancy classification and construction type.

- **Source:** Guidance Consideration 1 identifies fire rating as a performance requirement. NBC Part 3 (as adopted in Alberta) prescribes fire resistance ratings based on occupancy and building size. [Source: Guidance.md Consideration 1; Lensing: F-002]
- **Constraint:** The specific fire resistance rating (e.g., 1-hour, 2-hour) shall be determined by the Structural Engineer based on the confirmed NBC edition and occupancy classification. TBD -- fire resistance rating value to be confirmed.
- **Note:** This requirement was identified as a gap during semantic lensing. Guidance Consideration 1 references fire rating as a performance requirement, but no corresponding normative requirement existed in this specification prior to Pass 3. ASSUMPTION: Fire resistance rating is a code-mandated requirement that should be explicitly captured.

### REQ-011 — Coordination with Geotechnical Investigation

The structural foundation design shall incorporate findings from the geotechnical investigation report.

- **Source:** RFP §4.8.2 ("The Proponent will be conducting a geotechnical investigation. The Proponent shall provide a cost estimate based normal ground conditions, without any deleterious subgrade material. Final pricing for the design/construction of the foundation will be negotiated with the successful Proponent when the complete geotechnical report is available."); Decomposition SOW-0019, PKG-008.
- **Constraint:** Foundation design (DEL-002-11) is a variable-price deliverable and is separate from DEL-002-12. The Structural Specification (this deliverable) shall include general requirements for foundation materials and performance but shall cross-reference DEL-002-11 for foundation-specific details.
- **Scope change trigger:** If the geotechnical investigation (DEL-008-01) reveals deleterious subgrade material per RFP §4.8.2, the superstructure design may be affected (e.g., different foundation system changing load paths to superstructure). The Structural Engineer shall re-evaluate the Structural Specification requirements if the foundation system changes materially from the assumed normal ground conditions. The PM / Owner shall be notified of any scope impact to DEL-002-12 arising from the variable-price foundation scope. [Source: RFP §4.8.2; Procedure Step 2.4; Lensing: X-004]

---

## Standards

The following standards are expected to govern the Structural Specification. Where specific text has not been reviewed, the reference is noted as **location TBD**.

| Standard | Description | Status |
|---|---|---|
| National Building Code of Canada (NBC) — applicable Alberta edition | Primary structural design code for loads, structural integrity, occupancy requirements | ASSUMPTION: likely applicable; location TBD |
| CSA S16 — Design of Steel Structures | Applicable if structural steel elements are used (crane runway, mezzanine framing, embedments) | ASSUMPTION: likely applicable if steel used; location TBD |
| CSA A23.3 — Design of Concrete Structures | Applicable to concrete structural system, floor slab, pit walls, mezzanine supporting elements | ASSUMPTION: likely applicable; location TBD |
| Alberta Safety Codes Act and related regulations | Governing legislation for building safety compliance in Alberta | Source: RFP §3.3.2 |
| AISC / CMAA standards for crane runway design | Applicable if overhead crane runway is designed to AISC/CMAA criteria | ASSUMPTION: likely applicable; location TBD |
| CCDC 14–2013 | Design-Build Stipulated Price Contract — governs contractual obligations including design deliverables | Source: RFP §2.7 |

---

## Verification

**Provenance note:** Each verification approach should trace back to the source standard or code clause that dictates the verification method. This column is TBD -- the Structural Engineer shall add a "Source Standard / Clause" column when the governing code edition and applicable standard clauses are confirmed. [Lensing: E-004]

| Requirement | Verification Approach |
|---|---|
| REQ-001 — 35 ft clear ceiling | Confirm on IFC structural drawings; field measurement at substantial completion |
| REQ-002 — Crane support | Crane load calculations reviewed; runway girder design checked against crane manufacturer data |
| REQ-003 — Steel embedments | Embedment locations confirmed on IFC drawings; field inspection during pour. **Verification gap (TBD):** Quantified design load criteria for embedment plates (track/packer equipment loads, impact factors, load combination) must be established by the Structural Engineer before verification can confirm adequacy. Current verification confirms location only, not structural capacity. [Lensing: C-001] |
| REQ-004 — Service pit | Pit dimensions and structural capacity confirmed on IFC drawings; inspection during construction. **Acceptance threshold (TBD):** Quantitative pass/fail criteria must be established (e.g., minimum load case for pit edge, factor of safety). "Confirmed on IFC drawings" is a method, not a threshold. [Lensing: C-002] |
| REQ-005 — Mezzanine capacity | Mezzanine design live load stated in calculation package (DEL-002-10); confirmed on IFC drawings |
| REQ-006 — Stair | Stair design on IFC drawings; field inspection at installation |
| REQ-007 — Mud sump | Sump structural design confirmed on IFC drawings; field inspection. **Acceptance threshold (TBD):** Quantitative pass/fail criteria for excavator load capacity and hydrostatic design must be established. "Field inspection" is a method, not a threshold. [Lensing: C-002] |
| REQ-008 — Old North Shop renovation | Structural assessment report reviewed; renovation drawings on IFC set. **Verification baseline (TBD):** Acceptance criteria for the structural assessment must be defined (existing capacity vs. required capacity comparison, minimum factor of safety, acceptable deficiency remediation). "Assessment report reviewed" is a method, not a baseline. [Lensing: X-003] |
| REQ-009 — P.Eng. stamp | P.Eng. stamp and signature present on all IFC structural documents |
| REQ-010 — Code compliance | Code compliance review checklist; building permit issuance confirms AHJ acceptance |
| REQ-011 — Geotech coordination | Foundation design references geotech report; geotech report cited in calculation package |
| REQ-012 — Fire resistance rating | Fire resistance rating confirmed per applicable NBC edition and occupancy classification; documented in specification and calculation package. [Lensing: F-002] |

---

## Documentation

### Objective Traceability

This deliverable (DEL-002-12) contributes to **OBJ-003** ("Produce complete, P.Eng.-stamped IFC design documentation across all disciplines before construction begins") through the following documentation chain: the Structural Specification, combined with the PKG-002 drawing set (DEL-002-02 through DEL-002-09) and the Structural Calculation Package (DEL-002-10), forms the complete structural IFC documentation package. The P.Eng. stamp on the Structural Specification (per REQ-009) is a direct fulfillment artifact for OBJ-003. [Source: Decomposition Objectives; Lensing: D-003]

### Anticipated Artifacts

The following artifacts are anticipated as outputs of the Structural Specification deliverable (DEL-002-12) and the broader PKG-002 package:

| Artifact | Deliverable Reference | Status |
|---|---|---|
| Structural Specification document (this deliverable) | DEL-002-12 | This document |
| Foundation Plan (IFC drawing set) | DEL-002-02 | Separate deliverable |
| Structural Framing Plans (IFC drawing set) | DEL-002-03 | Separate deliverable |
| Structural Sections & Details (IFC drawing set) | DEL-002-04 | Separate deliverable |
| Mezzanine Framing Details (IFC drawing set) | DEL-002-05 | Separate deliverable |
| Service Pit / Trench Structural Details (IFC drawing set) | DEL-002-06 | Separate deliverable |
| Crane Support Structure Details (IFC drawing set) | DEL-002-07 | Separate deliverable |
| Steel Plate Embedment Plan (IFC drawing set) | DEL-002-08 | Separate deliverable |
| Stair Details (IFC drawing set) | DEL-002-09 | Separate deliverable |
| Structural Calculation Package | DEL-002-10 | Separate deliverable |
| Foundation Design Package (Variable-Price) | DEL-002-11 | Separate deliverable |

---

*This specification was enriched by Pass 3 (Semantic Lensing). Items tagged [Lensing: ...] trace to warranted items in _SEMANTIC_LENSING.md. Requirements labeled ASSUMPTION require confirmation by the Structural Engineer and/or human project authority. Values marked TBD require additional information.*
