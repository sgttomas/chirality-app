# Structural Design Brief -- Datasheet

## Identification

| Property | Value |
|----------|-------|
| **Deliverable ID** | DEL-03-03 |
| **Name** | Structural Design Brief |
| **Package** | PKG-003 -- Design Brief |
| **Type** | Design Brief / Narrative |
| **Discipline** | Structural Engineering |
| **Responsible Party** | Structural Engineer (Professional Engineer registered in Alberta) |
| **RFP References** | §7.1.2(3) (Structural Design Brief); §7.1.5 (Adaptability/Expansion); OSR §10.3.5 (Structural Objectives); OSR §10.3.6 (Foundations and Structure); OSR §10.3.8 (Flooring); OSR §10.3.9 (Roof and Door System); OSR §10.3.10 (Concrete Aprons) |
| **Scope Items Covered** | SOW-0011 (Design Brief, 5 sub-briefs), SOW-0014 (Adaptability/expansion narrative) |
| **Supporting Objectives** | OBJ-004 (strong Design Brief, 5 pts); supporting evidence for OBJ-005 (Durability, 15 pts) |
| **Status** | INITIALIZED |

---

## Attributes

| Attribute | Value |
|-----------|-------|
| **Primary Purpose** | Demonstrate to the evaluation committee that the Design-Builder has applied sound structural engineering judgment to system selection, understood site geotechnical constraints, planned a cost-effective and flexible structural approach, and provided credible provisions for future building expansion (RFP §7.1.2(3); §7.1.5) |
| **Document Format** | Written narrative by a Professional Structural Engineer; organized by topic area; proposal-stage communication tool (not a calculation package) |
| **Buildings Covered** | (1) Main Building (combined Fire Hall + Public Works); (2) Cold Storage Building (60' x 100', unheated) |
| **Design Life -- Main Building** | 50 years (RFP §2.2; Decomposition v2.3) |
| **Design Life -- Cold Storage** | 20 years (Decomposition v2.3) |
| **Structural Loads Classification** | Light to moderate (Geotech USG1123 §2.2) |
| **Post-Disaster Importance** | Not assigned; AHJ intends to exempt the PSB (OSR §10.3.5) |
| **Geotechnical Basis** | Union Street Geotechnical Ltd., File USG1123, 12 February 2021 -- sole basis; no additional investigation (Decision DEC-013). Prepared for Tagish Engineering Ltd.; Design-Builder uses as background information per limitations section. |
| **Seismic Site Classification** | Site Class C; average shear wave velocity 360 < Vs < 760 m/s (USG1123 §6, p.25) |
| **Frost Penetration Depth** | 2.0 m (estimated from historical temperature data for Penhold region; USG1123 §5.5.1, p.24) |

---

## Conditions

| Condition | Detail | Source |
|-----------|--------|--------|
| **Site Stratigraphy** | Topsoil (avg 72 mm) / Clayey Sand SC (to ~1.35 m below topsoil) / Clay CH (avg 1.35 m to 3.17 m in BH101-108; extends to full borehole depth in BH109-116) / Till (below clay in BH101-108, to max exploration depth) | USG1123 §4.1.3-4.1.6, pp.4-7 |
| **Sand Properties** | MUSC "SC" (Clayey Sand), medium plastic; moisture 8.3-15.7% avg 11.2%; poor to moderate bearing support for shallow foundations | USG1123 §4.1.4, Table 4.1, p.5; §5 intro, p.9 |
| **Clay Properties** | MUSC "CH" (high plasticity); undrained shear strength weighted avg 90 kPa (PP avg 124 kPa; SPT avg 10, K = 12.40); moisture content range 9.3-50.2%, avg 28.7%; frost-active; significant volume change with moisture fluctuation; NOT recommended as bearing stratum for shallow foundations | USG1123 §4.1.5, Table 4.2, p.6; §5 items 2-3, p.10 |
| **Till Properties** | Heterogeneous (clay, silt, sand, gravel); SPT N = 18-61, avg 32; PP avg 154 kPa; weighted average design undrained shear strength 184 kPa; moderate to good skin friction and end bearing for deep foundations; may contain cobbles and boulders | USG1123 §4.1.6, p.7 |
| **Groundwater Depth** | Approximately 3.0 m to 4.0 m below grade throughout majority of site (piezometer readings, 3 Feb 2021: BH101 = 3.88 m, BH104 = 3.44 m, BH106 = 3.26 m, BH108 = 5.98 m; avg 4.14 m). Depth varies approaching Waskasoo Creek. | USG1123 §4.2, Table 4.3, p.8 |
| **Sulphate Attack Risk** | Severe (Class S-2); concrete in contact with native or cohesive fill to use Type HS Portland cement; min 56-day compressive strength 32 MPa; max w/c ratio 0.45 (CAN/CSA A23.1-2014 Table 3). Calcium chloride admixtures must NOT be used -- reduces sulphate resistance. Type 10 cement + ~25% Type F or CI fly ash is acceptable equivalent. | USG1123 §4.3, pp.8-9 |
| **Freeze-Thaw Exposure** | All concrete exposed to freezing and thawing requires air entrainment per CAN/CSA A23.1-2014 Clause 4.3.3 and Table 4. Cold weather placement must comply with CAN/CSA-A23.1 cold weather provisions. | USG1123 §4.3, p.9 |
| **Shallow Foundation Constraint** | Clay is NOT recommended as bearing stratum for shallow foundations (high plasticity, frost active). Sand offers poor to moderate bearing. Shallow foundations must bear on undisturbed native sand or till; minimum depth 2.0 m if structure is not insulated and/or heated. Construction of unheated on-grade structures with movement-sensitive shallow foundations is not recommended. | USG1123 §5 items 2-3, p.10; §5.4, p.21 |
| **Deep Foundation Viability** | Driven steel pipe piles (open-end, bearing in till below 3.2 m) and screw piles are both recommended. Screw piles called "ideal" for this site. Cast-in-place concrete piles would likely require casing/pumping due to seepage/sloughing. | USG1123 §5 intro, p.9; §5.2, p.15; §5.3, p.18 |
| **Driven Pile Parameters** | Skin friction (clay, 2.0-3.2 m): 43 kPa. End bearing (till, below 3.2 m): 1,656 kPa. Minimum preliminary pile length: 5.3 m (for frost jacking resistance in unheated structures). Resistance factor phi = 0.4 compression, 0.3 tension. | USG1123 Table 5.1, p.15; §5.5.2, p.24 |
| **Screw Pile Parameters** | Helix must be fully below frost depth (2.0 m). Shaft diameter: 140 mm (5.5"); helix diameter: 508 mm (20") (example configuration). Su at helix (till) = 184 kPa; effective unit weight = 8.3 kN/m3. Resistance factor phi = 0.4 compression, 0.3 tension. Advantage over driven: smaller adfreezing stresses. | USG1123 §5.3, pp.18-20 |
| **Frost Heave Void Requirement** | Minimum 100 mm void between underside of pile-supported structure and sand subgrade (150 mm if subgrade is clay) to allow for frost heave movement without structural impact. | USG1123 §5.5.3, p.24 |
| **Single Foundation System Rule** | The use of several different foundation system types to support the same structure is not recommended -- systems mobilize support differently and mixing creates differential settlement risk. Choose one system type per structure. | USG1123 §5 item 5, p.10 |
| **Cold Storage Thermal Condition** | Unheated -- frost-active CH clay subgrade will experience seasonal freeze/thaw. Shallow foundations on frost-active subgrade not recommended for this condition. | USG1123 §5 item 2, p.10; Decomposition v2.3 |
| **Grade Supported Slab Requirements** | Subgrade: strip topsoil/organics to native sand; compact to 98% SPDD. Radon sump (100 mm min diameter collection pipe, sealed top) required near slab centre. Place minimum 150 mm of 20 mm screened/washed rock (radon rock, max 10% passing 4 mm sieve) on prepared subgrade. Install polyethylene sheeting (CAN/CGSB-51.34-M) between rock and slab. Provide separation boards between grade slab and any structurally supported elements. Use sleeves for all pipes passing through slab. | USG1123 §7.1, pp.25-27 |
| **Overhead Door Requirement** | 16 ft x 16 ft overhead doors with windows required for Main Building apparatus/equipment bays; Cold Storage Building also gets 16' x 16' doors; motorized openers with remote control; "car wash" grade hardware for Main Building; standard grade for Cold Storage Building. | OSR §10.3.9, p.41; Addendum 03 §1.10 |
| **Bay Sumps** | All apparatus bays and workshop bays require sumps for snow melting and minor washing -- penetrations in slab-on-grade require structural detailing | Addendum 03 §1.8 |
| **Concrete Aprons** | Aprons at all overhead door access points; designed to support weight and operation of service vehicles expected to use the facility. Design load class: TBD (e.g., AASHTO HS-20 or specific axle load per confirmed equipment list -- specific load class to be determined by Structural Engineer at detailed design). **ASSUMPTION: a load class commitment is needed to ensure consistent apron thickness design.** | OSR §10.3.10, p.42; Lensing item A-001 |
| **Solar-Capable Roof** | Roof must accommodate future solar panel installation; orientation: flat, south, west, or southwest; structural reserve for future dead loads required | Addendum 03 §1.17; OSR §10.3.9 |
| **NBCC Ground Snow Load (Ss, Sr)** | TBD -- ground snow load (Ss) and associated rain-on-snow load (Sr) for Penhold, Alberta per NBCC Appendix C. These are essential inputs for the load path narrative (R-STR-07) and roof structural design. Values to be confirmed from NBCC climatic data tables for the Penhold / Red Deer region. | NBCC Appendix C; location TBD |
| **NBCC Reference Wind Pressure (q)** | TBD -- hourly wind pressure (q) for Penhold, Alberta per NBCC Appendix C. Required for lateral load narrative (R-STR-07). Wind is likely the governing lateral load case for this central Alberta location (see Guidance C-007). Value to be confirmed from NBCC climatic data tables. | NBCC Appendix C; location TBD |
| **Code Compliance** | Alberta Building Code (ABC); National Building Code of Canada (NBCC); CAN/CSA A23.1-2014; Alberta OH&S Code Part 32 (excavations); CCDC 14-2013 | RFP §1; USG1123 §10 |

---

## Construction

| Element | Description |
|---------|-------------|
| **Primary Structural Artifact** | Structural Design Brief narrative authored and signed/committed by a Professional Structural Engineer registered in Alberta |
| **Relationship to DEL-02-03** | DEL-02-03 (Structural Concept Narrative, PKG-002) provides the concept-stage system selection; DEL-03-03 expands on rationale in greater depth for the Design Brief evaluation criterion. Both documents must be consistent and authored by the same Structural Engineer. |
| **Relationship to DEL-03-06** | DEL-03-06 (Accessibility and Adaptability Narrative) covers broader adaptability; DEL-03-03 provides the structural provisions for expansion that DEL-03-06 cross-references. Coordination required. |
| **Relationship to DEL-05-02** | DEL-05-02 (Structural Durability and Maintenance, PKG-005) addresses corrosion protection and long-term structural maintenance -- not duplicated here. Cross-reference only. |
| **Relationship to DEL-04-02** | DEL-04-02 (Mechanical Energy and Solar Readiness) defines solar roof orientation requirements that drive structural reserve load specifications. Structural engineer to coordinate solar dead load provision. |
| **Foundation Type Decision** | Design-Builder selects foundation type; cost-effective solution required; single system type per structure required (USG1123 §5 item 5). Design-Builder also responsible for retaining and paying for geotechnical services to certify subgrade (OSR §10.3.6). |
| **Cold Storage Foundation** | No owner preference; most cost-effective solution pursued; pole shed (post-and-frame) explicitly cited as acceptable approach (OSR §10.3.6). If pole shed, must address unheated condition and frost heave. |
| **Quality Checkpoint** | Brief must address: (1) structural system selection rationale with cost and flexibility considerations, (2) foundation approach based on geotechnical conditions, (3) load path narrative, (4) future expansion provisions per Section 7.1.5, (5) Addendum 03 items (sumps, door height, solar roof), (6) post-disaster importance exemption status, (7) USG1123 limitations acknowledgement, (8) eave height range, (9) OBJ-005 durability traceability, (10) Addendum 03 compliance summary. Specification contains 18 requirements (R-STR-01 through R-STR-18). |

---

## References

| Source | Purpose | Location |
|--------|---------|----------|
| RFP Section 7.1.2(3) | Structural Design Brief requirements | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`, p.16 |
| RFP Section 7.1.5 | Adaptability/expansion narrative requirements | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`, p.17 |
| RFP OSR §10.3.5 | Structural objectives; post-disaster exemption; equipment list | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`, p.40 |
| RFP OSR §10.3.6 | Foundation and structure requirements; geotechnical services responsibility | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`, p.40 |
| RFP OSR §10.3.8 | Flooring requirements (sealed concrete Main Building; Cold Storage Building options) | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`, p.41 |
| RFP OSR §10.3.9 | Roof, door system, solar loading, equipment clearance heights | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`, p.41 |
| RFP OSR §10.3.10 | Concrete aprons | `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`, p.42 |
| Addendum 03 (Jul 31, 2024) | Bay sumps (§1.8); 16 ft overhead doors (§1.10); solar roof (§1.17); 12-acre site (§1.1) | `_Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf` |
| Geotechnical Investigation Report, USG1123 | Foundation recommendations; soil stratigraphy; groundwater; sulphate/freeze-thaw; frost depth; seismic; slab | `_Sources/references/AB-2024-07156-Penhold PSB_Geotechnical Investigation Report.pdf` |
| Decomposition v2.3 FINAL | Project context, scope, design life, decisions (DEC-013) | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` |
