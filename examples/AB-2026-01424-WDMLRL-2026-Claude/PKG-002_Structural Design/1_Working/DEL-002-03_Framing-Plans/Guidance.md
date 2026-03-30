# Guidance — DEL-002-03 Structural Framing Plans

---

## Purpose

DEL-002-03 (Structural Framing Plans) exists because the New North Shop Addition is a structurally complex industrial building that requires fully coordinated framing drawings to govern construction. The framing plans are the primary structural document that communicates the building's load-path logic, member layout, and spatial coordination to the contractor. Without complete framing plans, the contractor cannot procure structural materials, sequence construction, or submit for building permit inspection at structural milestones.

This deliverable directly supports:
- **OBJ-001**: The addition must be code-compliant and fully functional — framing plans define the structural system that must achieve 35 ft clear height, carry two 5-tonne cranes, and support a heavy-duty mezzanine.
- **OBJ-003**: All IFC drawings must be P.Eng.-stamped and fully coordinated across disciplines; the structural framing plans are a mandatory component of the IFC set (R-01, §3.3.2).

---

## Principles

**1. Plan completeness before detail production.**
The framing plans establish the geometry and member layout from which all structural detail drawings (DEL-002-04 through DEL-002-09) are derived. Incomplete or inconsistent framing plans propagate errors into all downstream detail drawings. The Structural Engineer should finalize the primary framing grid, member spans, and crane runway elevations before producing connection details or mezzanine details.

**2. Crane loads govern framing system selection.**
The two 5-tonne overhead cranes on trolley impose dynamic loads (vertical, horizontal, and impact) on the crane runway structure. The crane runway framing (runway beams/girders and columns) typically drives the structural system size more than gravity-only loads in an industrial building of this scale. The Structural Engineer should obtain crane manufacturer data (wheel loads, wheel spacing, runway span) early and use these to set the runway framing before sizing roof structure. (R-01, §3.4; R-04)

**3. Mezzanine live load must be declared and conservative.**
The mezzanine is described as load-bearing for "heavy items such as several oil totes and oil pumping equipment" (R-01, §3.4). Oil totes (IBC 275-gallon / ~1,000 L) weigh approximately 900–1,000 kg each when full. Multiple totes plus pumping equipment can impose floor loads significantly higher than typical storage occupancy. The Structural Engineer should confirm the intended storage configuration with the County and select a mezzanine design live load that covers the worst-case arrangement. **ASSUMPTION:** A mezzanine design live load of at minimum 4.8 kPa (100 psf) is likely appropriate for heavy industrial storage, but the final value must be set by the Structural Engineer based on actual anticipated loads and code requirements.

**4. 35-foot clear height is a hard constraint.**
The RFP states "Concrete structure, 35' ceiling" (R-01, §3.4; R-04 notes). This clear height must be maintained through the full plan extent of the main shop area and is not a nominal dimension — it is the operational clearance required for equipment (motor-scraper class vehicles, overhead cranes). The Structural Engineer must account for the depth of the roof framing, crane runway beam depth, and any mechanical/HVAC hangers when establishing the structure-to-structure height. The building structure must be taller than 35 ft to achieve 35 ft of clear height.

**5. Coordinate with architectural floor plan early.**
The conceptual floor plan (R-04, Appendix B) shows the spatial layout of all rooms, the service pit, the wash bay, the parts room, and the mezzanine. The structural column grid must be developed in coordination with the architectural floor plan (DEL-001-02) to avoid columns conflicting with the wash bay, service pit, repair bay drive-through paths, and crane envelopes. Column placement in drive-through repair bays and the crane aisle is heavily constrained.

---

## Considerations

### Structural System Selection
Per SCA-001 (Addenda 2 and 4), the structural system has been confirmed as **precast concrete walls with a steel roof structure**. Interior walls are precast concrete (Add. 4, Q5). Crane support is via **corbels integrated into the precast side walls** with a maximum bay spacing of 25 ft (Add. 4, Q3). This resolves the original RFP ambiguity around "concrete structure" — the system is a hybrid precast/steel configuration, not cast-in-place concrete throughout. The framing plans must clearly indicate precast wall panels, steel roof members, and corbel locations for crane support.

### Crane Support Coordination (SCA-001 Updated)
Per Addendum 4, Q3, the two 5-tonne cranes are corbel-supported in the precast side walls with a maximum bay spacing of 25 ft. The Structural Engineer must:
- Coordinate corbel locations and capacity with the precast wall panel supplier/fabricator.
- Confirm crane rail elevation at corbel level is compatible with the 35 ft clear height requirement.
- Design corbel reinforcement and panel connection details for dynamic crane loads (vertical, horizontal, impact).
- Ensure corbel locations and crane framing are shown on DEL-002-03 and detailed on DEL-002-07.
- **New prerequisite (SCA-001):** Precast wall panel supplier/fabricator data (panel dimensions, connection details, corbel locations) is required as an upstream input — not yet formally listed as a dependency.

### Service Pit
The service pit (shown in R-04 as "SERVICE TRENCH") is approximately 24 ft × 100 ft per the conceptual plan (R-04 — ASSUMPTION based on plan notation). The below-grade walls of the pit are structural and must be designed for soil pressure and vehicle surcharge loads. The framing plan should show the pit extents, the header framing at the pit opening at floor level, and any structural cover framing. Details belong in DEL-002-06.

### Unit Convention Standardization

A unit convention inconsistency exists across the production documents: the Datasheet and Guidance use imperial units (ft, psf) for building dimensions and bay widths, while Guidance Principle 3 uses metric (kPa) for mezzanine loading, and Specification REQ-FP-11 acknowledges the unit convention is unconfirmed. This inconsistency must be resolved before drawing production.

- **Current state:** Dimensions are predominantly in feet (sourced from R-04 conceptual plan annotations which use imperial). Load values in Guidance reference kPa (metric), which is standard for NBC-based design in Canada.
- **Recommendation:** The project team (Architect + Structural Engineer) should establish a single unit convention for all drawings and document it as a project standard. In Alberta, structural engineering practice commonly uses metric (SI) units for design calculations (per NBC convention) and imperial for architectural dimensions — but the drawing set must be internally consistent per REQ-FP-11.
- **Action required:** Once the unit convention is decided, all four production documents should be updated to use consistent units.

**TBD:** Unit convention decision pending project team confirmation. (Lensing ref: B-004)

### Steel Plate Embedments
Steel plates are embedded in the concrete floor at strategic locations for heavy tracked and packer equipment (R-01, §3.4; R-04). These embedments are shown conceptually on R-04 at multiple locations in the main shop. The framing plans should coordinate with DEL-002-08 (Steel Plate Embedment Plan) to ensure slab thickness and reinforcing at embedment locations is compatible.

### Geotechnical Report Sequencing Dependency

The Procedure lists the geotechnical report (DEL-008-01) as a prerequisite "required before finalizing foundation/structural loads." However, the framing plans (DEL-002-03) primarily address the superstructure, not the foundations (which are covered by DEL-002-02). The relationship is as follows:

- **Framing plan production can begin before geotech completes.** The column grid layout, crane runway framing, mezzanine framing, and roof framing are driven by the building geometry, crane loads, and occupancy loads — none of which depend on soil conditions.
- **Framing plan finalization requires geotech indirectly.** Column base connection details (pinned vs. fixed base) may depend on foundation type, which depends on geotech. However, column base details are typically shown on DEL-002-04 (Structural Sections and Details), not on the framing plans themselves.
- **Recommended approach:** Proceed with framing plan preliminary design and County approval (Steps 2-3 of Procedure) in parallel with the geotechnical investigation. Finalize IFC framing plans after geotech confirms that no unusual foundation conditions require changes to the structural system.

**ASSUMPTION:** This sequencing rationale is inferred from standard structural engineering practice; the Structural Engineer of Record should confirm whether any site-specific condition requires geotech completion before superstructure framing design. (Lensing ref: X-001)

### Mezzanine Stair Integration
The conceptual plan (R-04) shows stairs to the mezzanine from the ground floor. The stair structural framing should be shown on the framing plans at the mezzanine level and detailed on DEL-002-09.

### County Approval Evidence Requirements

Procedure Step 3.3 and Verification V-08 require County preliminary approval before IFC production. However, neither the RFP (R-01) nor the current production documents specify what form this approval must take. The following guidance is provided to reduce ambiguity at the approval gate:

- **Acceptable forms of approval evidence (PROPOSAL):** Written letter from an authorized County representative, a formal email from the County project contact confirming design acceptance, or signed meeting minutes documenting County approval.
- **Minimum content of approval record:** Date of approval, identification of the documents reviewed (drawing list and revision), name and title of the County representative providing approval, and any conditions of approval.
- **Filing:** The approval evidence should be filed in the project correspondence file and referenced in the Procedure Records (Record: "County approval letter / email for preliminary framing plans").

**TBD:** Confirm with the County / project administration what form of approval evidence they will provide. (Lensing ref: C-003)

### Preliminary Design Gate
The County requires preliminary design approval before IFC production (R-01, §3.3.2). For framing plans, this means the Structural Engineer should produce schematic-level framing plans (showing structural system type, column grid, crane runway level, and mezzanine extents) for County review before committing to the full IFC drawing set. This is handled via DEL-002-01 (Preliminary Structural Design).

---

## Trade-offs

| Trade-off | Description | Recommendation |
|---|---|---|
| Precast wall + steel roof system (SCA-001 resolved) | Per Addenda 2 and 4, the structural system is confirmed as precast concrete walls with steel roof structure. This trade-off is resolved — County has accepted the precast/steel hybrid through the addendum process. Remaining design decisions: (1) precast panel connection type (wet vs. dry connections), (2) roof steel framing system (open web joists vs. wide-flange beams), (3) corbel detailing for crane loads. The Structural Engineer should coordinate with the precast supplier on panel dimensions and connection details. | Resolved by SCA-001 (Add. 2/4). |
| Column grid spacing | Wider column spacing reduces obstruction in the shop floor but increases beam/girder spans and member sizes. Narrower spacing reduces member sizes but adds columns that may conflict with crane envelopes, drive-through bays, and equipment access. | The crane envelope and drive-through bay widths (24 ft clear) set minimum column spacing in those areas; structural engineer should maximize bay sizes within cost constraints. |
| Mezzanine live load conservatism | A higher mezzanine design live load increases framing sizes and cost but avoids costly retrofits if the County's storage needs evolve. | Confirm actual storage loads with County; err on the side of a higher design live load for industrial mezzanines. |
| 35 ft clearance vs. structure depth | Meeting the 35 ft clear height constraint while accommodating roof framing depth, crane runway depth, and HVAC hangers may drive the overall building height. | Establish total structure height (eave height) early in design to close this constraint. |

---

## Examples

No specific precedent project framing plans are available in the accessible sources. The following are informational references drawn from R-04 (conceptual plan) that should inform the framing plan layout:

- **R-04 floor plan** shows two 5-ton crane runways running the full north-south depth of the main shop, confirming the crane runway spans the ~100 ft building depth.
- **R-04 notes** confirm: "Concrete Structure (35' Ceiling)", "(2) 5 Ton Cranes", "Steel Plates in Floor as indicated", "Overhead Mezzanine over Parts Room/Utility Room/Wash Bay", "Load Bearing Over Parts Room + Utility For Storage".
- **R-04 annotation** shows "Wash Bay Mud Sump" on the exterior east side of the building, confirming the wash bay is at the east end.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-FP-01 | Building plan dimensions: R-01 states "~13,000 sq ft useable area"; R-04 annotation shows 130 ft x 100 ft = 13,000 sq ft total, but also shows 105 ft wide Old North Shop abutting. It is unclear whether the 130 ft dimension is the new addition only or includes the Old North Shop. **Impact (Lensing ref: E-002):** This conflict directly affects the foundational data for framing plan correctness — column grid geometry, crane runway span, and all downstream framing depend on the confirmed building footprint. Resolution is required before column grid design (Procedure Step 2). | R-01, §3.1 ("approximately 13,000 square feet useable area") | R-04, Appendix B (floor plan annotation "130'" spanning the new shop only) | Datasheet (building footprint), Specification (REQ-FP-16, building geometry), Procedure (Step 2 — column grid) | R-04 annotation indicates 130 ft x 100 ft for the New North Shop addition only; the Old North Shop (105 ft x 40 ft) is existing and separate. This interpretation is consistent with R-01 §3.1. **ASSUMPTION** — confirm with County/Architect. | TBD |
| CONF-FP-02 | Service Pit dimensions: R-04 shows a "SERVICE TRENCH" annotation (canonical: service pit) with "24'" and "100'" markings, but the 100 ft dimension may refer to the building depth rather than the trench length. **Impact (Lensing ref: B-002):** Service Pit width (24 ft) and length propagate into framing design (pit header framing, floor slab openings). The 100 ft dimension is ambiguous — if it refers to building depth rather than trench length, the pit framing and Datasheet service pit attributes are incorrect. Resolution required before framing plan production at the pit area. | R-04, Appendix B (SERVICE TRENCH annotation — canonical: service pit) | R-04 overall building dimension annotation (100 ft building depth) | Datasheet (service pit dimensions), Specification (REQ-FP-08), Procedure (Step 3) | The 24 ft width annotation is likely the service pit width; the 100 ft likely refers to the building depth. Actual pit length is TBD and must be confirmed by the Structural Engineer from the architectural plans (DEL-001-02) or confirmed with County/Architect from R-04. | TBD |

---

*Guidance generated by 4_DOCUMENTS agent — Pass 1 + Pass 2. Date: 2026-02-25.*
*Enriched by 4_DOCUMENTS agent — Pass 3 (Semantic Lensing). Date: 2026-02-26.*
*SCA-001 cascade applied: 2026-03-29 (WORKING_ITEMS session — precast walls + steel roof + corbel cranes per Add. 2/4; terminology: "service pit" per Vocabulary Map).*
*Lensing items applied: B-002, B-004, C-003, E-002, F-003, X-001.*
*ASSUMPTION labels indicate inferred content not explicitly stated in sources.*
*Conflict Table entries require human ruling before IFC production.*
