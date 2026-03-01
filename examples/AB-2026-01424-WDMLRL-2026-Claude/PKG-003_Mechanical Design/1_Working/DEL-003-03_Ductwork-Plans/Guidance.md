# Guidance — DEL-003-03 Ductwork & Distribution Plans

---

## Purpose

DEL-003-03 (Ductwork & Distribution Plans) exists to provide the construction-ready, IFC-stamped drawing set that defines how conditioned and ventilated air is distributed throughout the New North Shop addition. This drawing set is the primary communication artifact between the Mechanical Engineer's design intent and the mechanical contractor's installation scope for all ductwork distribution systems (supply, return, general ventilation).

Within the decomposition, DEL-003-03 is one of six drawing/calculation deliverables within PKG-003 (Mechanical Design), all serving SOW-0013. The ductwork distribution drawings are subordinate to the HVAC layout (DEL-003-02, which establishes equipment placement) and are supported by the calculation package (DEL-003-06, which establishes airflow quantities that drive duct sizing).

ASSUMPTION (package-grouping heuristic): DEL-003-03 contributes to OBJ-001 (code-compliant functional shop), OBJ-003 (complete P.Eng.-stamped IFC documentation across all disciplines), and OBJ-004 (HVAC/ventilation systems commissioned to operational readiness). This association is confirmed by the decomposition's PKG-003 deliverable table (Decomposition §7).

**Link to OBJ-004 — Commissioning to Operational Readiness (Lensing: D-003):** The quality and accuracy of the ductwork distribution drawings directly affects commissioning success. During commissioning, the commissioning agent will verify that installed ductwork matches the design drawings, that airflow at terminal devices matches design quantities, and that the distribution system operates as intended. Drawing inaccuracies (e.g., incorrect duct sizes, missing branches, or uncoordinated routing) will result in commissioning deficiencies requiring field investigation and potential redesign. Therefore, drawing completeness and accuracy as verified through the requirements in Specification.md are a prerequisite for achieving OBJ-004.

---

## Principles

### 1. Design Sequence: Calculate Before You Route
Ductwork routing should not be finalized before airflow calculations (DEL-003-06) are complete or at least substantially advanced. Duct sizing is a direct output of airflow rates; routing ductwork at undersized or oversized dimensions and then retrofitting creates coordination conflicts with the structural frame. The Mechanical Engineer should sequence work so that the calculation package drives the duct sizing shown on this drawing set.
- Source: ASSUMPTION — standard mechanical design practice; no explicit sequencing stated in RFP or Appendix B sources.

### 2. The 35 ft Ceiling Is Both an Asset and a Challenge
The 35 ft concrete ceiling height (Source: RFP §3.4, Appendix B) provides significant plenum volume that simplifies main duct routing along the high ceiling. However, this height also means that heated air will stratify at ceiling level and must be actively destratified to maintain workable temperatures at floor level. Forced-air distribution, ceiling fan placement (6 fans per Appendix B Electrical), and destratification strategies should be coordinated in this ductwork drawing set.
- Source: RFP §3.4 (ceiling height, high-recovery heating, high-volume air exchanger); Appendix B (Electrical) for ceiling fans.

### 3. Dedicated Local Exhaust vs. General Ventilation — Maintain a Clear Boundary
The ductwork distribution system (this deliverable) and the exhaust system plans (DEL-003-04) serve different functions and different construction systems. The boundary must be clearly defined and consistently applied across both drawing sets. Mixing distribution and exhaust ductwork on the same sheet without clear differentiation will create installation errors. Recommend: use drawing layers, line weights, or legend symbols to distinguish supply, return, and exhaust duct types.
- Source: Decomposition §7 (DEL-003-03 vs. DEL-003-04 table entries); ASSUMPTION regarding representation convention.

### 4. Industrial Environment Requires Robust Duct Design
The New North Shop is an active heavy-equipment maintenance facility with sources of exhaust fumes, welding fumes, and particulate. Ductwork penetrations, material selection, and cleanout access provisions should reflect the industrial environment. Duct contamination paths (e.g., MUA intake location relative to exhaust discharge) require careful positioning.
- Source: RFP §3.1, §3.4 (nature of facility — exhaust hoses, welding station, heavy equipment); ASSUMPTION regarding design implications.

### 5. Coordination Must Be Explicit on the Drawings
Given the concrete structure (no easy field modifications), the 35 ft ceiling height, the two overhead 5-tonne crane rails (structural elements requiring clearance), and the service pit (below-grade penetration risk), every structural penetration for ductwork must be identified and coordinated before IFC. The ductwork drawing set must carry structural penetration callouts or cross-references to the structural penetration schedule.
- Source: RFP §3.4 (two 5-tonne overhead cranes on trolley; concrete structure; service pit); Decomposition §7 DEL-002 set; ASSUMPTION regarding coordination need.

---

## Considerations

### Space-by-Space Ventilation Considerations

**Main Shop (Repair Bays):**
The two drive-through repair bays (~24 ft wide each per Appendix B) are the primary work areas and the primary source of equipment exhaust. The MUA system supplies fresh, tempered replacement air. Ductwork distribution for MUA in the bays should account for the overhead crane paths (two 5-tonne cranes on trolleys) and avoid conflicting with crane travel. Distribution drops or destratification duct runs at mid-height may be required given the 35 ft ceiling.
- Source: RFP §3.4 (cranes, exhaust fans); Appendix B (Shop) (crane locations, bay widths).

**Wash Bay:**
The wash bay is a single enclosed bay (~24 ft wide) for washing large equipment such as a motor scraper (Source: RFP §3.1, §3.4; Appendix B). It is enclosed with its own overhead door and walls. Ventilation in the wash bay is required to manage moisture, temperature, and potential contaminants. The wash bay mud sump exterior connection (Source: RFP §3.4; Appendix B) is a plumbing interface, not a mechanical duct interface, but should be noted for coordination. Note (Lensing: B-004): The scope boundary between supply/general ventilation distribution (this deliverable) and dedicated local exhaust (DEL-003-04) applies to the wash bay per CON-003-03-01. This boundary is ASSUMPTION-dependent and TBD pending Mechanical Engineer confirmation. All documents (Datasheet, Specification, Guidance) now use consistent language to describe this assumption-qualified boundary.

**Service Pit / Trench:**
The service pit requires ventilation per RFP §3.4. The pit is below-grade; mechanical ventilation is required to address potential accumulation of fumes from vehicle maintenance below the equipment. Duct routing down to the pit level requires penetrations through the concrete floor or pit walls. This is a structural coordination point.
- Source: RFP §3.4 — "Ventilated and lighted service pit area."

**Office:**
The office is a small conditioned space per Appendix B. Standard comfort conditioning is expected. Area TBD — confirm from architectural drawings (DEL-001 set).

**Parts Room (~400 sq ft):**
Conditioned and ventilated space. Access controlled with 6 ft roll-up door (Source: RFP §3.4). ASSUMPTION: requires at least minimum ventilation per code.

**Utility Room:**
Likely the location of major mechanical equipment (forced-air MUA unit, heating unit, air exchanger). Ductwork connections will originate from or pass through this room. Coordinate with DEL-003-02 (HVAC Layout Plans) for equipment placement before routing ductwork from utility room.
- Source: Appendix B (Shop) — utility room shown adjacent to parts room and wash bay.

**Mezzanine:**
The mezzanine provides load-bearing storage over the parts room, utility room, and wash bay (Source: RFP §3.4; Appendix B). Whether the mezzanine receives conditioned air is TBD — to be determined by the Mechanical Engineer based on occupancy and code requirements. Ductwork routing through or around the mezzanine structure requires coordination with DEL-002-05 (Mezzanine Framing Details).

### Ceiling Fan Coordination
Six ceiling fans are specified in the main shop area (Source: Appendix B Electrical). These fans serve air destratification and do not appear to be duct-connected. However, their locations should be coordinated on the ductwork plans to ensure duct routing does not conflict with fan mounting positions or sweep radius. Fan locations are an electrical deliverable interface (DEL-004-04, DEL-015-04).

### Preliminary Design Dependency
The County must approve the preliminary mechanical design (DEL-003-01) before the ductwork plans can be issued for construction (RFP §3.3.2). The Mechanical Engineer should not commit ductwork routing at IFC level until system configurations, equipment selections, and airflow calculations are confirmed at the preliminary stage and approved.

### Safety Code Inspection and Drawing Detail (Lensing: E-003)

The Alberta Safety Code inspection process requires the Safety Code Officer to verify that installed mechanical systems comply with the applicable codes. The ductwork drawing set (DEL-003-03) must anticipate inspection hold points and provide sufficient detail for the Safety Code Officer to verify compliance. This means:

- Duct sizes, materials, and insulation (where specified) must be clearly annotated so the inspector can compare installed work against the design.
- Structural penetration fire/smoke ratings (if applicable) must be noted so the inspector can verify fire-stopping.
- The drawing set should identify which code sections govern the ductwork design (see REQ-003-03-06 in Specification.md) so the inspector has a clear compliance reference.

The rationale is that a drawing set that does not provide sufficient information for inspection will result in inspection delays, requests for additional information (RFIs), or conditional approvals. Source: ASSUMPTION — standard relationship between design drawings and safety code inspection in Alberta; specific inspection requirements are governed by the applicable Safety Codes (editions TBD).

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Approach | Source |
|---|---|---|---|---|
| Ductwork routing height | Route main ducts at high ceiling level (maximize clear height below) | Route main ducts at mid-height with distribution drops | Coordinate with crane clearance requirements; structural clearance governs | RFP §3.4 (cranes, ceiling height) |
| MUA distribution in bays | Perimeter slot diffusers at low level for destratification | High-level discharge with high-volume air movement | ASSUMPTION: engineer's judgment based on heat load calcs; TBD pending DEL-003-06 | RFP §3.4 (high volume air exchanger, high recovery heating) |
| Exhaust/ventilation boundary | Keep all exhaust in DEL-003-04 | Some combined systems on DEL-003-03 | Maintain clear boundary; confirm with Mechanical Engineer at preliminary design | Decomposition (DEL-003-03 vs. DEL-003-04) |
| Duct material (insulated vs. uninsulated) | Insulated sheet metal throughout | Bare sheet metal in conditioned heated space | TBD — depends on energy code requirements and system configuration | Alberta Building Code (location TBD) |

### Energy Performance Rationale (Lensing: F-005)

Energy performance considerations in duct design are relevant for this facility's long-term operating cost and lifecycle value:

- **Duct insulation:** In a heating-dominated cold climate (central Alberta), uninsulated ductwork routing through unconditioned or semi-conditioned spaces (e.g., high-ceiling plenum above the working zone) will lose heat to the surrounding air before reaching the occupied zone. Insulation reduces this loss and directly affects heating energy consumption and operating cost.
- **Air leakage class:** Duct air leakage (the amount of conditioned air lost through duct joints and seams) affects both energy efficiency and system capacity. SMACNA Seal Class and ASHRAE leakage class standards (editions TBD) provide benchmarks. For a large-volume industrial facility with significant heating loads, even modest leakage percentages represent meaningful energy waste over the building's lifecycle.
- **Energy code compliance:** The National Energy Code for Buildings (NECB), if applicable in Alberta for this building type, may prescribe minimum duct insulation R-values and maximum allowable air leakage rates. Compliance requirements are TBD pending confirmation of NECB applicability (see Specification Standards table and Lensing item C-002).
- **Lifecycle value context:** The facility is a County-owned public maintenance facility with an expected long service life. Operating cost savings from energy-efficient duct design accumulate over decades. The Mechanical Engineer should consider lifecycle cost implications when specifying duct material and insulation levels, even where energy code minimums may not strictly require insulation in heated spaces.

Source: ASSUMPTION — standard energy performance reasoning for heating-dominated industrial facilities; specific code requirements TBD.

---

## Examples

> No design examples from accessible sources. The Appendix B (Shop) conceptual drawing (R-04) shows the spatial layout of mechanical elements (forced air makeup notation, wash bay, service trench, welding station) but does not contain ductwork routing details. Ductwork routing examples and design methodology are TBD pending Mechanical Engineer's preliminary design work.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-003-03-01 | DEL-003-03 vs. DEL-003-04 scope boundary: the decomposition lists separate deliverables for ductwork distribution and exhaust systems, but the RFP (§3.4) lists exhaust hoses/fans, welding station ventilation, and air exchange as part of a single mechanical design scope (SOW-0013). The boundary between what belongs in DEL-003-03 vs. DEL-003-04 is not stated in the RFP. **Update (Lensing: F-003):** Boundary language has been normalized across all four documents to use consistent categorical terms: "supply, return, and general ventilation distribution" (DEL-003-03) vs. "dedicated local exhaust" (DEL-003-04). See Specification Boundary Note, Datasheet System Coverage table, and this Guidance entry. | Decomposition §7, PKG-003 table (two separate deliverables) | RFP §3.4 / SOW-0013 (single scope item covers all HVAC, ventilation, exhaust) | Specification.md (Scope section, Boundary Note), Datasheet.md (Ductwork System Coverage), Procedure.md (Step 1 and Step 5) | Mechanical Engineer to define the boundary at preliminary design stage and document in DEL-003-02 or DEL-003-07. | TBD |
| CON-003-03-02 | Ceiling fan designation: fans are listed in Appendix B (Electrical) and allocated to the electrical scope in the decomposition (SOW-0040 → PKG-013 installation; power from PKG-015). However, fans serve air distribution/circulation function and could be expected on a mechanical ductwork drawing set. Unclear which drawing set governs spatial layout coordination. **Update (Lensing: X-002):** REQ-003-03-15 has been added to Specification.md to provide a normative anchor for ceiling fan spatial coordination, requiring duct routing to be coordinated with fan locations. This conflict now has both procedural handling (Procedure Step 1.2) and a normative requirement. | Appendix B (Electrical); Decomposition §7 — SOW-0040 listed under PKG-013 (Mechanical & HVAC Installation) | Decomposition §7 — ceiling fan power under PKG-015; fan layout typically shown on electrical plans | Datasheet.md (Attributes — ceiling fans), Procedure.md (Step 5 — coordination), Specification.md (REQ-003-03-15) | ASSUMPTION: fan locations shown on electrical plans (DEL-004-04); mechanical drawing set includes coordination note only. Confirm with Mechanical and Electrical Engineers. | TBD |
