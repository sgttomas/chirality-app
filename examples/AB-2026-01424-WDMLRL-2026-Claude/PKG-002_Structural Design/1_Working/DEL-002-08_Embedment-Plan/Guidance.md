# Guidance — DEL-002-08 Steel Plate Embedment Plan

---

## Purpose

The Steel Plate Embedment Plan exists to translate the Owner's operational requirement for heavy equipment access on the shop floor into engineered, constructible design documentation. The Owner requires steel plates at strategic positions within the concrete floor slab to protect the slab surface and structural integrity when tracked and packer-type equipment (such as motor scrapers) traverse the floor.

This deliverable provides the construction team with the authoritative, P.Eng.-stamped plan and detail drawings needed to correctly locate, anchor, and finish the embedded steel plates before or during the concrete pour. Without this drawing set, the general contractor cannot correctly position the plates, and the concrete slab cannot be poured to final grade in the embedment zones.

This deliverable supports:
- **OBJ-001:** Code-compliant, fully functional shop that passes all applicable inspections
- **OBJ-003:** Complete, P.Eng.-stamped IFC design documentation before construction begins

Source: _CONTEXT.md; Decomposition §5 (Objectives), §7 (DEL-002-08 entry).

---

## Principles

### P-01: Design Leads Placement
Steel plate locations must be determined by engineering analysis (loading from tracked/packer equipment), not solely by the conceptual drawing. The Appendix B floor plan provides indicative locations; the Structural Engineer must validate these against actual equipment wheel/track loads and slab capacity.

Source: RFP §3.4 — "steel plating in concrete at strategic locations to accommodate track and packer type heavy equipment." The word "strategic" implies engineering judgment, not arbitrary placement.

### P-02: Coordinate Before Pour
Steel plate embedments are cast-in elements. Their location, anchoring, and surface height must be fully resolved before the concrete floor pour. Late changes after the pour require coring, demolition, or saw-cutting — all of which are costly and structurally undesirable. This drawing set must be issued IFC prior to slab construction.

Source: ASSUMPTION — standard construction sequencing for embedded elements in concrete slabs; consistent with OBJ-003 (IFC documentation before construction begins).

### P-03: Plate Surface Must Be Flush
Embedded plates in a heavy equipment maintenance shop floor must be flush with or marginally proud of the finished concrete surface to avoid creating trip hazards for maintenance personnel and to allow equipment to traverse without catching edges. Edge chamfers or radiused edges on the plate perimeter may be required.

Source: ASSUMPTION — industrial floor best practice for embedded plates in maintenance facilities. Specific tolerance to be specified by Structural Engineer.

### P-04: Anchor Design is Structural
The anchors connecting the steel plate to the concrete slab (headed studs, deformed bar anchors, or equivalent) are structural elements. They must be designed to resist the uplift, shear, and moment forces imposed by equipment operations. The anchor design must appear in the Structural Calculation Package (DEL-002-10).

Source: ASSUMPTION — structural engineering principle; consistent with REQ-009 in Specification.md. CSA A23.3 anchor design provisions are likely applicable (location TBD).

### P-05: Coordinate with All Floor Penetrations
The floor plan contains multiple competing elements: Service Pit, floor drains, sump connections, gantry crane runway column bases, and the 50,000 L water storage footprint. The Structural Engineer must confirm that plate positions do not conflict with any of these elements before issuing IFC drawings.

Source: R-04 (App B floor plan); consistent with Specification REQ-006.

---

## Considerations

### C-01: Wash Bay Steel Plates
The Appendix B conceptual drawing shows two steel plates in the wash bay zone. The wash bay is designed for washing large equipment (motor scraper-class), and this is the highest-intensity use case for steel plates. The wash bay also has a mud sump connection to the exterior. The Structural Engineer should confirm that the plate embedment details in the wash bay are compatible with the wash bay floor drain layout (DEL-006-03 / DEL-014-04) and that the slab slope toward drains is maintained at the plate edges.

Source: R-04 (App B — "Wash Bay Mud Sump," "Steel Plate" locations in wash bay); RFP §3.4 ("Single enclosed bay dedicated for washing large equipment such as a motor scraper").

### C-02: Main Repair Bay — Multiple Plates in Crane Zone
The conceptual drawing shows approximately four steel plate bands in the main repair bay area, which is also served by two 5-tonne overhead cranes. The gantry crane runway column base locations (DEL-002-07) must be confirmed before finalizing plate positions to avoid column base interference. Plates must also remain clear of the Service Pit structural walls (DEL-002-06).

Source: R-04 (App B — "5 Ton Crane," "Service Pit," multiple "Steel Plate" labels in main bay).

### C-03: Plate Dimensions Not Specified in Sources
The RFP and Appendix B do not specify steel plate dimensions (length, width, or thickness). The Structural Engineer must determine these based on equipment load analysis. Typical industrial shop floor embedded plates range from 10mm to 25mm thick, but this is provided as industry context only and must not be used as a design value without engineering justification.

Source: ASSUMPTION — industry context only. Actual dimensions: TBD by Structural Engineer.

### C-04: Geotech Dependency
The slab thickness and reinforcement design — which directly affect the embedment depth and anchor length for the steel plates — depend on subgrade conditions confirmed by the geotechnical investigation (DEL-008-01). If the geotech report is not yet available, the Structural Engineer may need to issue the Embedment Plan with assumed slab parameters, with a note that dimensions may be updated upon geotech completion.

**Enrichment (C-003) — Proceeding Without Geotech:** If DEL-008-01 is not available before embedment design must commence, the following directional guidance applies:
- The Structural Engineer should establish conservative assumed subgrade parameters based on regional soil data or preliminary site information (if available).
- The rationale for assumed values must be documented in DEL-002-10 (Structural Calculation Package), including the risk that actual conditions may differ.
- The risk threshold: if assumed bearing capacity is less than TBD kPa (to be set by Structural Engineer), the design should be flagged for mandatory re-verification post-geotech. **TBD:** Define the specific risk threshold value.
- A fallback strategy should be documented: either (a) design to worst-case regional parameters, accepting potential over-design, or (b) issue drawings with explicit assumption notes and a commitment to revise within a defined timeframe post-geotech.
- All drawings issued under assumed parameters must carry a prominent note per Procedure Prerequisites (see also Conflict Table CONF-004 regarding whether this note is mandatory or guidance).

Source: Decomposition — DEL-008-01 (Geotechnical Investigation); RFP §3.3.2 ("A full complete geotechnical report will be required by the successful proponent to use during the design process"). Enrichment via semantic lensing (C-003); ASSUMPTION — directional guidance for risk management.

### C-05: Motor Scraper Turning Loads
A motor scraper is an articulated piece of heavy equipment. When turning in a confined bay, it exerts high lateral (scrubbing) loads on the floor surface, in addition to vertical loads from its weight. The steel plate design and anchor design must account for lateral forces, not just vertical load — particularly for plates at entry zones to bays where turns may be executed.

Source: ASSUMPTION — structural engineering consideration for articulated heavy equipment in confined spaces. Specific load values: TBD by Structural Engineer.

### C-07: Lifecycle and Maintenance Implications of Embedded Steel Plates
**Enrichment (F-004):** The Structural Engineer should consider the following lifecycle and maintenance factors for embedded steel plates:
- **Replaceability:** Embedded plates cast into concrete are effectively permanent. If a plate is damaged by impact or excessive wear, replacement requires slab demolition in the affected zone. The design should consider whether plate thickness provides adequate service life for the expected equipment loading frequency.
- **Corrosion protection:** In a heated shop environment with potential exposure to road salts, de-icing chemicals, and wash water, the Structural Engineer should assess whether corrosion protection (e.g., galvanizing, epoxy coating on undersides, or sacrificial thickness allowance) is warranted.
- **Future re-surfacing:** If the concrete floor is re-surfaced in the future (e.g., overlay or grinding), the embedded plates create constraints. The design should document the minimum concrete cover around plate edges to preserve structural integrity after potential re-surfacing.

Source: ASSUMPTION — lifecycle considerations for industrial embedded elements. Proposed authority: Structural Engineer.

### C-06: IFC Timing
This deliverable must be issued IFC before the concrete floor slab is poured. Given the project's December 31, 2026 completion deadline (RFP §3.1), the embedment drawings must be available to the general contractor early enough to allow steel plate fabrication, delivery, and placement within the construction schedule.

Source: RFP §3.1 (completion deadline); ASSUMPTION — construction sequencing.

---

### Rationale for ASSUMPTION-Tagged Standards
**Enrichment (F-001):** The following standards are marked ASSUMPTION in the Specification Standards table. The rationale for why each is believed likely applicable is provided below to support defensible regulatory justification until formal confirmation:

| Standard | Rationale for Likely Applicability |
|---|---|
| Alberta Safety Codes (Building) | Alberta Safety Codes Act requires all building construction in the province to comply with the Alberta Building Code, which adopts the NBC with Alberta-specific amendments. This project is located in Camrose County, Alberta. Source: RFP §3.3.2. |
| National Building Code of Canada (NBC) | The NBC as adopted in Alberta governs structural design loads, including floor live loads and special equipment loads. An industrial maintenance shop floor with heavy equipment is subject to these provisions. Source: RFP §3.3.2 reference to "applicable building codes." |
| CSA S16 (Steel Structures) | CSA S16 is the Canadian standard for design of steel structures and is referenced by the NBC for structural steel elements. Embedded steel plates are structural steel elements. ASSUMPTION — standard Canadian structural engineering practice. |
| CSA A23.3 (Concrete Structures) | CSA A23.3 is the Canadian standard for concrete structural design, including Annex D for anchorage design. The plate-to-slab anchor connection falls under anchorage design. ASSUMPTION — standard Canadian structural engineering practice. |
| CSA G40.20/G40.21 (Structural Steel) | CSA G40.20/G40.21 is the Canadian material standard for structural steel. Steel plates specified for structural use in Canada are typically procured to this standard. ASSUMPTION — standard Canadian material specification practice. |

These rationales are directional only. Confirmation by the Structural Engineer is required to establish formal applicability.

---

## Trade-offs

### T-01: Larger Plates vs. More Plates
Larger continuous steel plate bands provide greater coverage and are more forgiving of vehicle path variability, but increase material cost and weight (affecting slab loading calculations). Smaller, precisely located plates reduce material cost but require the Structural Engineer to more precisely predict equipment paths. The Appendix B conceptual drawing implies band-style plates spanning the bay width.

**PROPOSAL:** Follow the band-style indicative layout from Appendix B as a starting point; adjust based on structural analysis. Human ruling: TBD.

### T-02: Plate Thickness vs. Slab Step
Thicker plates provide more durability under repeated heavy-equipment loads, but if too thick, create a step above the finished slab surface if not properly recessed. The Structural Engineer must balance plate durability against the requirement for flush or near-flush surface condition.

**PROPOSAL:** Structural Engineer to specify plate thickness based on load analysis, with embedment detail confirming flush surface. Human ruling: TBD.

---

## Examples

The Appendix B (Shop) conceptual floor plan (R-04) provides the primary reference example for steel plate placement. The following observations from that drawing are offered as context for the Structural Engineer:

- Steel plates appear as rectangular bands spanning the full width of the repair bay (approximately 24' bay widths per dimension callouts on drawing)
- Two gantry crane runway pairs are shown in the wash bay — the steel plates in that zone appear adjacent to the gantry positions
- The Service Pit is shown as a distinct element separate from the steel plate zones in the main bay

These observations are interpretations of the conceptual drawing only and should not be treated as final design dimensions.

Source: R-04 — AB-2026-01424-Appendix B (Shop).pdf.

---

## IFC Distribution Rationale
**Enrichment (E-001):** Procedure Step 8.4 lists three distribution targets for the IFC drawing set. The rationale for each is as follows:
- **General Contractor:** The GC is the primary consumer of IFC drawings for construction execution. DEL-011-02 (Steel Plate Floor Embedments — construction, PKG-011) depends on this drawing set. Source: Decomposition §7 (PKG-011), SOW-0024.
- **County Project Manager:** The RFP §3.3.2 requires submission of IFC drawings to the Owner. The County PM is the Owner's representative.
- **Project document control:** Standard design-build practice requires a controlled document register for all IFC-status drawings to support audit trail, coordination, and contract compliance under CCDC 14-2013.

**TBD:** Confirm whether additional parties require copies (e.g., building inspector for permit review, subtrades for steel plate fabrication/procurement). Proposed authority: Project team.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-001 | Plate count: Appendix B shows 6 steel plate locations; exact count for IFC drawings may differ after engineering load analysis. | R-04 (App B conceptual — 6 plates visible) | Engineering judgment (Structural Engineer, load analysis) | Datasheet §Attributes (plate count), Specification REQ-001 | Structural Engineer's engineering determination governs; Appendix B is conceptual only | TBD |
| CONF-002 | Plate dimensions (length, width, thickness) are not defined in any accessible source. Datasheet and Specification note TBD; actual dimensions must be set by Structural Engineer. | None (no source provides plate dimensions) | Standard practice assumption (10mm–25mm thickness range) | Datasheet §Attributes, Specification REQ-004 | Structural Engineer to determine based on load analysis; thickness assumption in Guidance §C-03 is illustrative only | TBD |
| CONF-003 | Geotech report not yet complete; slab parameters needed for anchor design may not be confirmed at time of Embedment Plan drafting. | DEL-008-01 (not yet run per Decomposition) | Structural design schedule requirement | Specification REQ-005, Guidance §C-04 | Structural Engineer to issue with assumed parameters and re-issue or confirm post-geotech | TBD |
| CONF-004 | Geotech assumption flag on drawings: Procedure Prerequisites Note says the Structural Engineer "must clearly note the assumption on drawings" if geotech is pending. However, Specification REQ-005 requires coordination with DEL-002-02 but does not mandate an assumption flag on drawings. Is the flag a requirement or guidance? | Procedure.md — Prerequisites Note on Geotech | Specification.md — REQ-005 | Procedure Prerequisites, Specification REQ-005, Drawing notes | Specification (normative document) should govern; if the flag is mandatory, add it to REQ-005 or create a new requirement (PROPOSAL) | TBD |
| CONF-005 | 50,000 L water storage coordination: Procedure Step 3.2 lists "50,000 L water storage footprint (confirm with DEL-001-02 and DEL-006-04)" as a coordination item, but Specification REQ-006 (conflict avoidance) and Datasheet Interface Conditions did not originally reference this element. Is it in scope? | Procedure.md — Step 3.2 | Specification.md — REQ-006; Datasheet Interface Conditions | Specification REQ-006, Datasheet Interface Conditions, Procedure Step 3.2 | Specification should be updated if this is a real coordination constraint (PROPOSAL) | TBD |
