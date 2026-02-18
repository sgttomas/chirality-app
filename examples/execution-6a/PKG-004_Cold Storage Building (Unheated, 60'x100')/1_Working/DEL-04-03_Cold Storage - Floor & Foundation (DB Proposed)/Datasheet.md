# Datasheet: DEL-04-03 — Cold Storage Floor & Foundation (DB Proposed)

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-04-03 |
| **Name** | Cold Storage — Floor & Foundation (DB Proposed) |
| **Package** | PKG-004 Cold Storage Building (Unheated, 60'×100') |
| **Discipline** | Structural / Civil |
| **Type** | Building design package (4-doc bundle) |
| **Responsible Party** | Design-Builder (Structural/Civil) |
| **Scope Items Covered** | SOW-0303 (floor), SOW-0304 (foundation) |
| **Objective Supported** | OBJ-004 (unheated cold storage building) |
| **Decision References** | DEC-002 (DB proposes one floor solution); DEC-003 (DB proposes most cost-effective code-compliant foundation) |
| **Status** | OPEN |
| **Date** | 2026-02-17 |

---

## Attributes

### Building Context

| Attribute | Value | Source |
|---|---|---|
| Building type | Unheated cold storage (ancillary) | OSR §10.3.5; Decomposition §PKG-004 |
| Plan dimensions | 60' × 100' clear-span | SOW-0301; DEC-001 |
| Heated | No (unheated) | OSR §10.2; SOW-0300 |
| Use | Seasonal equipment/materials/supplies storage | OSR §10.2 |
| Design life (ancillary) | TBD (main building = 50 years; ancillary not explicitly stated in accessible sources). **TBD_QUESTION [A-001]:** Owner to confirm design life for ancillary cold storage building. This parameter governs foundation durability, material selection, and lifecycle cost assessment. | OSR §10.2 (main building reference only) |
| Floor live load design basis | TBD. **TBD_QUESTION [B-001]:** No floor live load (kPa or psf) stated in any accessible source. DB structural engineer to establish based on equipment types; Owner to confirm equipment inventory. | -- |
| Expected equipment/vehicle types and weights | TBD. **TBD_QUESTION [B-004]:** Multiple documents reference "equipment storage" and "service vehicle loads" (REQ-06) but no specific vehicle or equipment weights are provided. Owner to provide equipment inventory or load class. | OSR §10.2 (use described as "seasonal equipment/materials/supplies storage"); Specification REQ-06 |

### Site / Soil Conditions (from Geotechnical Investigation)

| Parameter | Value | Source |
|---|---|---|
| Geotechnical report | Union Street Geotechnical Ltd., File No. USG1123, 12 February 2021 | Geotech Report §1 |
| General stratigraphy (descending) | Topsoil → Sand (to ~1.35 m) → Clay (to ~3.17 m) → Till | Geotech Report §4.1 |
| Topsoil average thickness | ~72 mm | Geotech Report §4.1.3 |
| Sand depth | Surface to ~1.35 m below grade | Geotech Report §4.1.4 |
| Sand MUSC classification | SC (Clayey Sand), medium plastic | Geotech Report §4.1.4, Table 4.1 |
| Clay depth | ~1.35 m to ~3.17 m below grade | Geotech Report §4.1.5 |
| Clay MUSC classification | CH (high plasticity); undrained shear strength (weighted avg) = 90 kPa | Geotech Report §4.1.5, Table 4.2 |
| Till depth | ~3.17 m to maximum exploration depth | Geotech Report §4.1.6 |
| Till undrained shear strength (weighted avg) | 184 kPa | Geotech Report §4.1.6 |
| Groundwater depth (estimated) | ~3.0 m to ~4.0 m below grade | Geotech Report §4.2, Table 4.3 |
| Frost penetration depth (Penhold) | 2.0 m | Geotech Report §5.5.1 |
| Seismic site class | C (Avg Shear Wave Velocity 360 < Vs < 760 m/s) | Geotech Report §6 |
| Sulphate attack risk | Severe (Class S-2); Type HS cement required for concrete in contact with native/cohesive fill | Geotech Report §4.3 |

### Foundation System Options (Geotech-Identified)

| Foundation Type | Geotech Assessment | Key Parameter | Source |
|---|---|---|---|
| Shallow footings (on sand) | Possible; must bear on undisturbed native sand or till at min 2.0 m depth (unheated); clay NOT suitable as bearing stratum | ULS bearing capacity on sand (strip, >0.61 m depth): 300 kPa; SLS: 100 kPa | Geotech Report §5.4, items 2 & 6 |
| Shallow footings (on till) | Possible; must be deeper than 2.0 m; min 2.0 m depth for unheated structure | ULS bearing capacity on till (strip, >2.0 m depth): 360 kPa; SLS: 120 kPa | Geotech Report §5.4, items 2 & 8 |
| Driven steel pipe piles | Suitable; open-end piles recommended for till termination; min preliminary pile length 5.3 m to resist frost jacking | Ultimate skin friction in till: 72 kPa; end bearing: 1,656 kPa | Geotech Report §5.2, Table 5.1 |
| Screw piles | Described as "ideal" for this site; advantageous for frost-jacking resistance; upper helix must be below 2.0 m frost depth | φ = 0.4 (compression); Su (till) = 184 kPa for helix capacity calc | Geotech Report §5.3 |
| Cast-in-place concrete piles | Possible but likely requires casing/pumping due to seepage/sloughing | Not recommended as primary option | Geotech Report §5, intro |

**Critical Geotech Warning:** Construction of unheated, on-grade structures and/or shallow foundations where movement would be detrimental is NOT recommended at this site due to frost-active, high-plasticity clay subgrade. (Geotech Report §5, item 2.)

**Owner Preference (OSR §10.3.6):** Cold storage building has no foundation preference; most cost-effective solution preferred. Post and frame (pole shed) construction cited as an example. Optional solutions welcome.

### Floor System Options (OSR-Defined)

| Option | Description | Source |
|---|---|---|
| Option 1 (asphalt millings) | Floor capped with adequate layer of compacted asphalt millings; 4' (1,219 mm) wide concrete strips on inside for pallet racking installation | OSR §10.3.8 (Ancillary Buildings) |
| Option 2 (full concrete) | Concrete floor inside the building; concrete aprons in front of overhead and person doors | OSR §10.3.8 (Ancillary Buildings) |

**DEC-002 (Decomposition):** DB to propose a single floor solution; alternates are optional but not required.

### Concrete Specification Requirements (if concrete floor/aprons used)

| Requirement | Value | Source |
|---|---|---|
| Cement type (sulphate exposure) | Type HS (Portland), or Type 10 + ~25% Type F/CI fly ash | Geotech Report §4.3 |
| Minimum specified compressive strength (56-day) | 32 MPa | Geotech Report §4.3 (CAN/CSA A23.1-2014, Table 3) |
| Maximum water-cement ratio | 0.45 | Geotech Report §4.3 |
| Air entrainment | Required per CAN/CSA A23.1-2014 §4.3.3 and Table 4 | Geotech Report §4.3 |
| Cold weather placement | Must comply with CAN/CSA-A23.1 cold weather provisions | Geotech Report §4.3 |
| Calcium chloride admixtures | NOT permitted (reduces sulphate resistance) | Geotech Report §4.3 |

### Grade-Supported Slab Subgrade Preparation Requirements (if grade slab used)

| Requirement | Value | Source |
|---|---|---|
| Strip topsoil/organics/non-structural fill | Required prior to construction | Geotech Report §7.1, item 1 |
| Subgrade compaction | Min 98% SPDD (100% for fills >1.2 m); water content within +2% of OMC | Geotech Report §7.1, item 3 |
| Structural fill lifts | Max 200 mm compacted thickness; min 98% SPDD; water within ±2% OMC | Geotech Report §7.1, item 4 |
| Granular base (radon rock) | Min 150 mm of 20 mm screened/washed rock (≤10% passing 4 mm sieve) | Geotech Report §7.1, item 6 |
| Vapour barrier | Polyethylene sheeting conforming to CAN/CGSB-51.34-M between granular base and slab. **Note [E-002]:** Minimum thickness, lap width, and sealing method are TBD -- the referenced standard (CAN/CGSB-51.34-M) is not directly accessed. DB or Specification to confirm these parameters. | Geotech Report §7.1, item 7 |
| Separation from foundations | Do not tie grade slab reinforcing steel to edge/grade beam (risk of heave damage) | Geotech Report §7.1, item 11 |
| Drainage | **Two distinct requirements [E-003]:** (1) Slab surface drainage: min 2% slope away from slab; no ponding (Geotech Report §7.1, item 9). (2) Foundation perimeter drainage: min 3% slope over the first 3.0 m from the building perimeter (Geotech Report §5.1.2, per Specification REQ-12). Both apply in their respective contexts and are complementary, not conflicting. See Specification REQ-12 Normalization note for clarification. | Geotech Report §7.1, item 9 (slab); Geotech Report §5.1.2 (foundation perimeter) |

### Frost Design Summary

| Parameter | Value | Source |
|---|---|---|
| Frost penetration depth | 2.0 m | Geotech Report §5.5.1 |
| Frost jacking stress (adfreezing) | 100 kPa above 2.0 m depth (fine-grained soil to steel) | Geotech Report §5.5.2 |
| Driven piles (unheated structure) — min embedment | 5.3 m | Geotech Report §5.5.2; §5.2 |
| Screw piles — upper helix requirement | Must be below 2.0 m frost depth | Geotech Report §5.3 |
| Void under pile-supported structures | Min 100 mm (sand subgrade) or 150 mm (clay subgrade) between underside of structure and subgrade | Geotech Report §5.5.3 |
| Shallow footings (unheated) | Min 2.0 m depth | Geotech Report §5.4, item 2 |

---

## Conditions

| Condition | Description | Source |
|---|---|---|
| Unheated building | Frost design governs; on-grade unheated construction with shallow foundations requires careful assessment against geotech recommendations | Geotech Report §5, item 2; OSR §10.3.5 |
| High-plasticity clay subgrade | Clay (CH) present from ~1.35 m; significant frost heave and volume change expected; not suitable as shallow foundation bearing stratum | Geotech Report §4.1.5; §5, item 2 |
| Groundwater depth | ~3.0–4.0 m below grade; excavations beyond this depth may encounter seepage | Geotech Report §4.2; §5, item 7 |
| Sulphate attack | Severe sulphate environment (Class S-2); concrete mix design must account for this | Geotech Report §4.3 |
| No foundation type prescribed | DB proposes; post-and-frame / pole shed cited as acceptable example | OSR §10.3.6; DEC-003 |
| One floor solution | DB proposes one solution (alternates optional) | SOW-0303; DEC-002 |
| Drainage requirement | Positive drainage away from building required for foundation performance | Geotech Report §5 (intro) |

---

## Construction

| Element | DB Responsibility | Source |
|---|---|---|
| Foundation type selection and design | DB selects and designs; retain geotechnical services as required | OSR §10.3.6; RFP §7.1.2 |
| Geotechnical services during construction | DB responsible for retaining geotech to certify subgrade, certify imported material, and certify prepared granular base | OSR §10.3.6 |
| Floor system selection and design | DB selects one floor solution; structural engineer to specify slab | SOW-0303; DEC-002; Geotech Report §7.1, item 6 |
| Concrete aprons | Required at all overhead door access points (both overhead doors and person doors per floor option selected) | OSR §10.3.10; OSR §10.3.8 |
| Subgrade preparation | Strip topsoil/organics; proof roll; compact to specification | Geotech Report §5.1; §7.1 |
| Structural sealing of documents | Must be sealed by Alberta-registered professionals | RFP §7.1.2 |

---

## References

| Reference | Relevance | Location |
|---|---|---|
| Union Street Geotechnical Ltd., File No. USG1123, February 12, 2021 — *Geotechnical Investigation, Public Works Operations Centre, Penhold, Alberta* | Primary geotechnical data: stratigraphy, foundation options, floor recommendations, frost design | `_Sources/references/AB-2024-07156-Penhold PSB_Geotechnical Investigation Report.pdf` |
| Town of Penhold RFP 2024_004, Appendix A (OSR) §10.3.6, §10.3.8, §10.3.10 | Foundation preference, floor options, concrete aprons | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf` |
| RFP §7.1.2 | Structural sealing and design obligations | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf` |
| Penhold PSB Project Decomposition FINAL v1.0 PHASE7 | Deliverable scope, DEC-002, DEC-003, SOW-0303, SOW-0304 | `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` |
| CAN/CSA A23.1-2014 | Concrete specification (sulphate resistance, air entrainment) | Referenced in Geotech Report §4.3; not directly accessed |
| CAN/CGSB-51.34-M | Polyethylene sheeting specification for vapour barrier | Referenced in Geotech Report §7.1; not directly accessed |
| Alberta Building Code (ABC) | Governing building code | Referenced in Geotech Report §10 (location TBD); not directly accessed |
| Canadian Foundation Engineering Manual, 4th Edition (2006) | Foundation design methodology used in geotech analysis | Referenced in Geotech Report §5.2, §5.3; not directly accessed |
