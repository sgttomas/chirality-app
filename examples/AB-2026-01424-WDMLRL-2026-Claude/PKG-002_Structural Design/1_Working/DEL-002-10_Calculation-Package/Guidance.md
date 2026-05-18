# Guidance: DEL-002-10 Structural Calculation Package

---

## Purpose

DEL-002-10 exists to provide the engineering justification record for the structural design of the West Dried Meat Lake Regional Landfill Maintenance Shop Addition (New North Shop). The Calculation Package serves three primary functions:

1. **Design authority** — It is the primary technical record establishing that the structural system is adequate for the building's loads, occupancy, and code requirements. All structural drawings within PKG-002 are subordinate to it.
2. **Regulatory compliance** — Alberta Safety Codes require that structural design be carried out by a licensed P.Eng. The stamped calculation package is the principal evidence of this compliance and is typically required for building permit issuance (PKG-009).
3. **Contract performance** — Under CCDC 14–2013 and the RFP, the Proponent bears responsibility for complete final structural design (SOW-0012) and foundation design (SOW-0019). The Calculation Package is the Design-Builder's primary evidence of meeting this obligation.

Within the project objectives, DEL-002-10 directly supports:
- **OBJ-001** — Code-compliant, fully functional maintenance shop addition that passes all inspections.
- **OBJ-003** — Complete, P.Eng.-stamped IFC design documentation across all disciplines.
- **OBJ-006** — Managing the variable-price foundation scope within the CCDC 14–2013 contractual framework.

> ASSUMPTION (PACKAGE_HEURISTIC): OBJ-001, OBJ-003, and OBJ-006 are associated with DEL-002-10 based on the decomposition's explicit PKG-002 deliverable table and Scope Ledger entries for SOW-0012 and SOW-0019.

---

## Principles

### Principle 1 — Calculations Lead Drawings
The Calculation Package is the governing document for structural dimensions, member sizes, reinforcement, and connection designs. The structural drawing set (DEL-002-02 through DEL-002-09) must be consistent with the calculations. Where discrepancies arise, the calculations govern unless formally superseded by a calculation revision.

### Principle 2 — Explicit Assumptions Must Be Flagged
Where design inputs are unavailable at the time of calculation (e.g., final crane specifications, confirmed geotechnical parameters, mezzanine live load not yet confirmed by Owner), the Structural Engineer of Record must document the assumed value, the basis for the assumption, and the trigger condition for revision. The foundation calculations using "normal ground conditions" (RFP §4.8.2) are the principal example — they must clearly state this basis.

### Principle 3 — Foundation Scope Is Variable-Price
The RFP explicitly states that foundation pricing is negotiated post-geotech (RFP §4.8.2). The Calculation Package must maintain a clear organizational boundary between foundation scope (DEL-002-11 / SOW-0019) and superstructure scope (SOW-0012) to allow independent cost segregation and post-geotech reconciliation without disrupting the broader document set.

### Principle 4 — Coordination Is Non-Optional
This is a design-build project with tight schedule to December 31, 2026. Structural loads and penetrations affect mechanical, electrical, and plumbing design, and vice versa. The Calculation Package should be developed in parallel with — not in isolation from — other discipline design efforts. Unresolved interface items create risk to schedule and to IFC drawing quality.

### Principle 5 — Stampable Quality from First Issue
Because Alberta requires a P.Eng. stamp on IFC documents, calculations should be produced at a quality that can be signed from the outset of the final design phase, rather than requiring a wholesale revision cycle prior to stamping.

---

## Considerations

### Building Type and Loads
The New North Shop is an industrial maintenance facility for heavy landfill equipment (tracked equipment, packer-class vehicles, motor scrapers). This drives structural design considerations well beyond a typical commercial building:

- **Floor slab and embedment loading:** Tracked and packer equipment impose high localized loads. Steel plate embedments at strategic locations (App B) are a direct response to this. The slab design must account for wheel/track loads at these locations.
- **Crane runway loading:** Two 5-tonne overhead cranes on trolley (RFP §3.4, App B) generate dynamic loads on the runway beams and brackets. The 35 ft ceiling height means crane rail elevation will be significant; column brackets or stepped columns are likely required. **ASSUMPTION:** Specific crane model/runway geometry is not stated in available sources; the Structural Engineer of Record must obtain crane specifications from the procurement package (DEL-016-01) or use conservative 5-tonne class parameters.
- **Mezzanine loading:** The mezzanine over the parts room, utility room, and wash bay is described as "capable of heavy items (oil totes, pumping equipment)" (RFP §3.4). Oil totes (typically 1,000 L each at ~1 tonne full) stacked on a mezzanine represent a significant design live load. The Structural Engineer should confirm the Owner's intended storage arrangement to set the design live load appropriately.
- **Service pit:** The below-grade service pit must resist lateral earth pressure and potentially hydrostatic pressure depending on the site water table (to be confirmed by DEL-008-01).

### Foundation Uncertainty
The geotechnical investigation (DEL-008-01) is an upstream dependency. Without it, the Structural Engineer must estimate foundation type, depth, and bearing capacity from regional norms for the Ferintosh/Camrose County area. Alberta prairie sites commonly exhibit bearing capacities in the 100–200 kPa range for shallow spread footings, but highly variable conditions (clay, till, organics) exist in the region. The "normal ground conditions" pricing basis (RFP §4.8.2) implies a shallow footing assumption. If the geotech reveals poor soils requiring deep foundations (piles, caissons), this is a contract-level event affecting OBJ-006. The calculations must be structured so this revision can be made efficiently.

### 35 ft Ceiling Height
A 35 ft clear ceiling in a concrete structure is a significant structural challenge. Concrete columns at this height must resist wind lateral loads and crane runway loads without excessive drift. Lateral bracing strategies (moment frames vs. shear walls vs. braced frames in concrete) will govern the structural system selection. The Structural Engineer of Record should confirm the lateral load resisting system early and document it in the Design Basis section of the calculations.

### Alberta Climate Loads
The Ferintosh area (Camrose County) is subject to significant snow and wind loads typical of Alberta's central prairie region. Ground snow load and wind pressure values should be taken from NBC climatic data for the nearest applicable weather station. These values are not stated in the RFP and must be sourced directly from the NBC Appendix C tables. **TBD:** Specific climatic values not available in accessible sources.

### Relationship to Preliminary Design
The RFP requires delivery of a Preliminary Structural Design (DEL-002-01) for County approval before final design proceeds (RFP §3.3.2). The Calculation Package development should be staged accordingly: a design-basis memo or preliminary sizing can serve as the calculation backbone supporting the Preliminary Design presentation, with final calculations completed as design is finalized.

### Regulatory Submission and AHJ Review
The Calculation Package is a key supporting document for the building permit application (PKG-009). The Authority Having Jurisdiction (AHJ) — Camrose County or the Alberta Safety Codes Officer — may require submission of the stamped calculation package (or a summary thereof) as part of the building permit review process. The Structural Engineer of Record should confirm the AHJ's specific submission requirements for structural calculations early in the design process, as these may affect the calculation package format, level of detail, and issuance timing. Neither the RFP nor the decomposition explicitly describe the AHJ submission requirements for structural calculations. **TBD:** Confirm municipal/AHJ structural calculation submission requirements for building permit. [Added per lensing item A-004]

### Quality Expectations Beyond Code Compliance
A code-compliant calculation package is a minimum threshold; a high-quality calculation package for a project of this scale and complexity should also demonstrate:
- **Clarity of presentation:** Calculations organized logically with a clear index (Procedure Step 2), each section self-contained with stated assumptions, applied loads, analysis, and pass/fail summary.
- **Depth of design basis documentation:** Not just stating the governing code, but documenting the rationale for key engineering judgments (e.g., lateral system selection, mezzanine load assumptions, crane load assumptions).
- **Peer review rigor:** Internal QA review (Procedure Step 5) should go beyond arithmetic checking to include independent verification of governing design assumptions and load paths.
- **Revision readiness:** The package should be structured so that foreseeable revisions (post-geotech foundation update, crane data reconciliation) can be made to isolated sections without disrupting the entire document.

These quality attributes are not code requirements but distinguish a package that supports efficient downstream use (permit review, construction, future modifications) from one that merely satisfies minimum compliance. **ASSUMPTION:** Based on standard Alberta structural engineering practice. [Added per lensing item A-006]

---

### Terminology Note — Foundation Scope Boundary

The variable-price foundation scope is referenced using varying terminology across the document set. For consistency, the canonical term is: **"variable-price foundation scope (SOW-0019)"**. Equivalent phrasings found in the current documents include:
- Datasheet: "Foundation Pricing Basis: Normal ground conditions (variable-price per geotech results)"
- Specification REQ-014: "foundation design scope (SOW-0019)"
- Guidance Principle 3: "foundation pricing is negotiated post-geotech"

All refer to the same concept: the foundation design and pricing element that is contractually segregated as a variable-price item under CCDC 14-2013, with final scope confirmed after delivery of the geotechnical investigation report (DEL-008-01). [Normalized per lensing item B-004]

---

## Trade-offs

| Trade-off | Option A | Option B | Consideration |
|---|---|---|---|
| Lateral load resisting system | Concrete shear walls (monolithic with building) | Moment frame system | Shear walls are typical for industrial concrete; moment frames provide more flexibility in bay layout. Choice affects column size, foundation design, and construction sequence. **Structural Engineer of Record decision.** |
| Foundation prior to geotech | Shallow spread footings (normal conditions assumed) | Defer foundation calculations | RFP requires pricing based on normal conditions (§4.8.2); assume shallow footings but clearly flag as preliminary. **Rationale for conservative approach:** Deferring foundation calculations until geotech delivery would delay the Preliminary Structural Design (DEL-002-01) and potentially the building permit application (PKG-009), creating schedule risk against the December 31, 2026 completion deadline. The contractual framework (CCDC 14-2013 variable-price) explicitly contemplates this approach — initial pricing on assumed conditions, with reconciliation post-geotech. [Expanded per lensing item C-004] |
| Mezzanine design live load | Use NBC minimum storage load (4.8 kPa per NBC Table 4.1.5.3) | Confirm with Owner for specific storage intent | NBC minimum provides a conservative code-compliant baseline; Owner confirmation allows optimization but requires coordination time. Given heavy-use intent (oil totes), higher load may be warranted. |
| Crane data availability | Use conservative 5-tonne class industry parameters | Wait for crane procurement package | Crane procurement (DEL-016-01) may not be finalized during design. Conservative industry parameters allow design to proceed; calculations must note the assumed data and trigger a reconciliation check when crane is specified. **Rationale for conservative approach:** Waiting for crane procurement data would delay crane runway and supporting column design, which in turn delays the structural framing plans (DEL-002-03) and crane support details (DEL-002-07). The 5-tonne capacity is contractually fixed (RFP §3.4); only the manufacturer-specific details (wheel spacing, bridge weight, end reactions) are unknown. Conservative industry parameters for 5-tonne class cranes are well-established and provide a defensible design basis. [Expanded per lensing item C-004] |
| Foundation scope segregation | Maintain separate Foundation Design Package (DEL-002-11) | Combine with main calculation package | Decomposition requires DEL-002-11 as a separate deliverable for variable-price contractual purposes. Calculations should be physically segregated (separate binder or clearly marked section) to facilitate this. |

---

## Examples

The following structural system characteristics are typical for industrial concrete buildings of similar scale and use. These are provided for orientation only and are not prescriptive — the Structural Engineer of Record will determine the appropriate system.

> **ASSUMPTION:** The following are based on general engineering practice for heavy industrial concrete buildings in Alberta and are not derived from a project-specific source. They are illustrative only.

- Concrete tilt-up or cast-in-place wall panels are common for industrial buildings with heavy overhead crane loads in Alberta.
- Crane runway beams in a 5-tonne, 35 ft clear height application would typically be W-shape steel sections mounted on column corbels or stepped columns.
- Service pit walls in a prairie Alberta context would typically be 200–250 mm reinforced concrete walls with waterproofing membrane at the exterior face if water table is above pit depth.
- Mezzanine structures in industrial shops are commonly composite steel deck / concrete topping over steel framing, separate from the main concrete superstructure — though this depends on the final structural system choice.

---

## Long-Term Considerations

The Calculation Package is not only a design-phase document — it serves as the structural record for the building's lifetime. The following long-term governance considerations should inform how the package is structured: [Added per lensing item E-001]

- **Future modifications:** If the Owner wishes to modify the building in the future (e.g., additional mezzanine areas, different crane capacity, wall openings), the Calculation Package is the starting point for any re-analysis. Structuring the package with clear, self-contained sections (per Procedure Step 2) supports efficient future use.
- **Guarantee period:** The RFP requires a 2-year guarantee period post-CCC (RFP §2.10.2). During this period, structural deficiencies discovered would be evaluated against the Calculation Package. The package should therefore document not only final design values but also the assumptions and load cases used, so that any future reviewer can verify the design basis.
- **Building code evolution:** Future building code editions may change load requirements or introduce new provisions (e.g., updated seismic hazard maps). A well-documented design basis section allows future engineers to identify which parameters may need re-evaluation under a new code cycle.
- **Records retention:** The Structural Engineer's professional obligations under the Alberta Engineering and Geoscience Professions Act may require retention of calculation records beyond the contractual guarantee period. See Procedure Records — Retention for further detail. **TBD:** Confirm APEGA retention requirements.

**ASSUMPTION:** These long-term considerations are based on standard Alberta structural engineering practice and general building lifecycle management principles, not on explicit RFP requirements.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| C-001 | The decomposition lists DEL-002-10 as covering SOW-0012 and SOW-0019 (foundation). DEL-002-11 is also listed as the "Foundation Design Package (Variable-Price)" covering SOW-0019. The boundary between what foundation calculation content belongs in DEL-002-10 vs. DEL-002-11 is not defined in the RFP or decomposition. | Decomposition §7 DEL-002-10 entry | Decomposition §7 DEL-002-11 entry | Specification REQ-014; Guidance Principle 3; Procedure Step 4 | PROPOSAL: DEL-002-10 includes all calculation work; DEL-002-11 is the separately packaged/priced subset for the variable-price foundation scope, drawing from the same calculations. | TBD |
| C-002 | The RFP Appendix B (Shop) drawing notes "Gantry" equipment adjacent to the wash bay, while the conceptual drawing also shows "5 TON CRANE" labels. The decomposition (D-001) resolves this as the same equipment. However, if the gantry label refers to a separate gantry crane (not overhead crane on runway), the structural support requirements would differ. | App B drawing (Gantry label) | Decomposition D-001 (same equipment) | Specification REQ-007; Datasheet Crane Support Structure row | PROPOSAL: Follow Decomposition D-001 resolution — treat as two 5-tonne overhead cranes on trolley. Flag for Structural Engineer of Record to confirm with Owner at design kickoff. | TBD |
| C-003 | The Specification Documentation section minimum content list was originally labeled as "ASSUMPTION" while REQ-001 requires the Calculation Package to "address all structural subsystems listed in the Scope section" — a normative requirement. The ASSUMPTION label has been removed and replaced with a clarifying note linking the minimum content to REQ-001's normative scope obligation. The underlying content items remain the same. | Specification — Documentation (formerly ASSUMPTION-labeled) | Specification — REQ-001 (normative) | Specification Documentation section | PROPOSAL: Resolved — ASSUMPTION label removed; minimum content now framed as consistent with REQ-001. Confirm this framing is acceptable. [Lensing item E-002] | TBD |
