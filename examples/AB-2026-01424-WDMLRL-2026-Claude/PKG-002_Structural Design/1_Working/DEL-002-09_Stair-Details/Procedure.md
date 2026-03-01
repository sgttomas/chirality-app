# Procedure — DEL-002-09 Stair Details

---

## Purpose

This procedure describes the steps for the Structural Engineer to produce the Stair Details drawing set (DEL-002-09) as part of the PKG-002 Structural Design deliverables for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. The procedure covers drawing set production from prerequisites through to IFC release and record-keeping.

---

## Prerequisites

### Required Inputs (before beginning DEL-002-09)

| Input | Source | Status |
|---|---|---|
| Geotechnical investigation report | PKG-008 — Geotechnical Investigation & Surveying | TBD — required for foundation and slab bearing conditions; stair base anchors depend on slab design |
| DEL-002-03 — Structural Framing Plans (or working draft) | PKG-002 | TBD — needed for overall structural grid and slab layout to locate stair base |
| DEL-002-05 — Mezzanine Framing Details (or working draft) | PKG-002 | TBD — needed for mezzanine top landing elevation, framing layout, and connection interface |
| DEL-002-08 — Steel Plate Embedment Plan | PKG-002 | TBD — confirm whether floor embedments exist at intended stair base location |
| Architectural Floor Plans (DEL-001-02) or working draft | PKG-001 | TBD — confirm stair location, stair clear width, and architectural intent |
| Confirmed mezzanine top-of-deck elevation | DEL-002-05 coordination | TBD |
| Alberta Building Code (current edition) | Regulatory — Proponent to obtain | Required for code-compliant stair geometry and structural load cases |
| RFP and Appendix B (Shop) conceptual drawing | R-01, R-04 (on file) | Available |

### Required Authorizations / Agreements
- County approval of Preliminary Structural Design (DEL-002-01) before proceeding to IFC details. (R-01 §3.3.2)
- Design team agreement on stair location, material, and scope boundary with DEL-002-05 (see Guidance CON-001).

---

## Steps

### Step 1 — Confirm Stair Location and Program

1.1 Review Appendix B (Shop) conceptual floor plan (R-04). Note the "Stairs to Mezzanine" label in the Utility Room / Water Storage area.

1.2 Coordinate with the Architect (PKG-001) and the mechanical/electrical engineers to confirm the final stair footprint does not conflict with equipment, plumbing, or electrical layout. Document the agreed stair location.

1.3 Confirm the mezzanine deck elevation from DEL-002-05 working drawings. Calculate the total stair rise.

1.4 Confirm total stair rise and plan area available to determine number of runs (straight-run vs. switchback/L-shape), subject to Alberta Building Code minimum tread and maximum riser constraints.

1.5 Document stair location, orientation, total rise, number of runs, and estimated landing dimensions. Record as a design basis note for the drawing set.

### Step 2 — Establish Structural Design Basis

2.1 Determine stair occupancy classification under the applicable Alberta Building Code (industrial/storage use is anticipated — ASSUMPTION).

2.2 Establish design live load for the stair (minimum per Alberta Building Code for the applicable occupancy class; given heavy-storage mezzanine context, confirm load is not reduced below industrial minimum). Record the design load value in the General Notes of the drawing set.

2.3 Select stair structural material (steel or concrete) in coordination with DEL-002-05 mezzanine framing material and overall PKG-002 structural strategy. Document selection rationale.

2.4 Verify with DEL-002-10 (Structural Calculation Package) that the stair structural calculations will be included in that deliverable. Confirm responsibility for calculation coverage.

2.5 Establish handrail and guardrail requirements (height, loading, post spacing) per Alberta Building Code and Safety Codes. Confirm scope boundary with DEL-002-05 (see Guidance CON-001).

### Step 3 — Produce Structural Drawings

3.1 Prepare a plan view of the stair at the mezzanine deck level, showing the stair footprint, landing dimensions, relationship to mezzanine framing members, and overall stair orientation.

3.2 Prepare elevation and section views showing:
- Overall stair height from finished floor to mezzanine deck
- Number of risers and treads
- Riser height and tread depth (confirm to Alberta Building Code limits)
- Stringer sizing and profile
- Intermediate landing (if required)

3.3 Prepare base connection details:
- Base plate or embedded anchor design at concrete slab
- Anchor bolt size, spacing, embedment depth
- Grout detail (if applicable)
- Cross-reference to DEL-002-08 (Embedment Plan): confirm whether a floor embedment is used at this location and coordinate accordingly. **[X-001] Note:** The status of DEL-002-08 as required vs. conditional input is subject to Conflict Table CON-002 in Guidance.md. Make a positive determination and record it.

3.4 Prepare top connection details:
- Connection of stair stringer or landing beam to mezzanine framing (per DEL-002-05)
- Confirm compatible detail type (bolted, welded, bearing)

3.5 Prepare handrail and guardrail details within the agreed scope (see Guidance CON-001):
- Stair handrail: post type, rail height, post spacing, attachment to stringer or wall
- Landing guardrail (if within this scope): post, rail, and toe plate details at stair opening
- Clearly cross-reference DEL-002-05 for mezzanine deck edge guardrail if that scope is assigned there

3.6 Prepare material and finish schedule (member sizes, material grade, surface treatment — e.g., galvanizing, paint primer).

3.7 Prepare General Notes:
- Applicable codes and edition (specify ABC edition year per [A-001])
- Design live load assumptions (record numeric value per [X-003])
- Fabrication and erection tolerances
- Welding/bolting standards: TBD -- confirm whether CSA W47.1 applies and remove "or equivalent" ambiguity before IFC. **[A-004] Enrichment:** The specific welding/bolting standard should be confirmed by the Structural Engineer based on the selected stair material (steel vs. concrete) and the applicable fabrication requirements. If steel is selected, CSA W47.1 (Certification of Companies for Fusion Welding of Steel) is the expected standard; confirm edition. If concrete is selected, welding standards may not apply to the stair itself. Do not leave as "or equivalent" in IFC documents. ASSUMPTION: CSA W47.1 applicability depends on steel material selection.
- Geotechnical bearing assumptions for anchor design (confirm receipt of geotechnical report per [C-001])

### Step 4 — Internal Quality Review

4.1 Structural Engineer reviews all drawings for internal consistency:
- Dimensions are consistent across plan, elevation, and detail sheets
- Load path is traceable from stair live load through stringers, connections, to concrete or mezzanine framing
- All required code dimensions (riser, tread, handrail height) are explicitly called out
- Material designations are consistent with DEL-002-12 (Structural Specification)

4.2 Cross-check with DEL-002-05 (Mezzanine Framing Details):
- Top landing connection detail matches mezzanine framing member location and depth
- Guardrail scope boundary is clearly delineated; no gaps or overlaps

4.3 Cross-check with DEL-002-08 (Steel Plate Embedment Plan):
- Confirm whether a floor embedment is used at the stair base. **[X-004] Enrichment:** Make a positive determination and record it: either (a) a floor embedment IS used -- confirm it is shown on the Embedment Plan (DEL-002-08) and cross-referenced in this drawing set, or (b) a floor embedment is NOT used -- record the alternative base connection method and confirm DEL-002-08 coordination is not required. Do not leave the embedment question as an implicit conditional. See also Conflict Table CON-002 in Guidance.md.

4.4 Verify drawing set title block is complete: project name, drawing title, number, revision, date, scale.

4.5 **[D-003] Independent Quality Assurance Review:**
TBD -- Confirm whether an independent P.Eng. review (separate from the engineer of record) is required or recommended before IFC issue. For IFC documents bearing a P.Eng. stamp, an independent check may be warranted per the firm's quality management system or applicable professional practice standards. If required, schedule the independent review before Step 6 (IFC Issue). If not required, document the rationale for self-review being sufficient.
- **Proposed authority:** Structural Engineer / Project Manager.

### Step 5 — Preliminary Design Submission (if not previously done)

5.1 If the stair structural concept has not been captured in DEL-002-01 (Preliminary Structural Design), prepare a preliminary stair concept for County approval before finalizing IFC details.

5.2 Incorporate any County review comments before proceeding to IFC issue.

5.3 **[D-001] Enrichment:** Record County approval of the preliminary stair design as a formal verification gate before proceeding to Step 6 (IFC Issue). Retain written confirmation of approval. This approval record is a precondition to conformance ruling for Specification REQ-008 (see Specification Verification table). Source: R-01 section 3.3.2.

### Step 6 — IFC Issue

6.1 Structural Engineer of Record applies P.Eng. stamp and signature to all sheets in the drawing set. Confirm the engineer is licensed to practice in the Province of Alberta (R-01 §3.3.2).

6.2 Assign IFC revision designation to all sheets. Record IFC issue date in revision table.

6.3 Issue drawing set to:
- Document controller / design-build team for distribution
- Building permit authority (as required)
- Construction team (PKG-011 DEL-011-07 — Mezzanine Structure & Stairs)
- County project manager (per R-01 §3.1)

---

## Verification

| Check | Method | Responsible |
|---|---|---|
| Stair provides access from main floor to mezzanine | Drawing review — confirm elevations and continuity | Structural Engineer |
| Stair geometry complies with Alberta Building Code | Explicit dimension callouts reviewed against code table | Structural Engineer / P.Eng. |
| Live load assumption is documented and appropriate | General Notes review | Structural Engineer |
| Base connections detailed and anchors sized | Drawing and calculation review (DEL-002-10) | Structural Engineer |
| Top connection coordinated with DEL-002-05 | Cross-document check | Structural Engineer |
| Handrail and guardrail details present within agreed scope | Drawing review | Structural Engineer |
| P.Eng. stamp present on all IFC sheets | Document check before release | Project Manager / Structural Engineer |
| IFC revision status and title block complete | Drawing review | Document Controller |
| County approval of preliminary design obtained | Written record on file | Project Manager |
| **[D-003] Independent QA review (if required)** | Confirm independent P.Eng. review completed and documented before IFC stamp (TBD -- see Step 4.5) | Structural Engineer / Project Manager |
| **[D-001] County approval recorded before IFC** | Confirm County preliminary design approval is on file before Step 6 IFC Issue proceeds (see Step 5.3) | Project Manager |

---

## Records

The following records shall be produced and retained as evidence of completion:

| Record | Description | Retained By |
|---|---|---|
| IFC Drawing Set — DEL-002-09 | Stamped and signed structural drawings for stair details | Design-build team document control |
| Design Basis Note | Record of stair location, material selection, live load, and design code edition | Structural Engineer's project file |
| Coordination Record | Written agreement with PKG-001 (stair location) and DEL-002-05 (connection interface, guardrail scope boundary) | Structural Engineer's project file |
| County Approval Record | Written confirmation of Preliminary Design approval (if stair concept required approval) | Project Manager |
| Building Permit Records | Copy of permit authority acknowledgement or approval | Project Manager |
| Structural Calculation Package reference | Confirm DEL-002-10 covers stair structural calculations | Structural Engineer's project file |
| **[E-002] Design Team Agreement Record** | TBD -- Confirm whether a formal record of the design team's agreement on stair location, material selection, and scope boundary (referenced in Required Authorizations) should be included in the Records table. This agreement is mentioned in Prerequisites but not currently tracked as a retained record. The verified audit archive should include all critical decision records. | Structural Engineer / Project Manager |

---

## Semantic Lensing Enrichment Trace (Pass 3)

| ItemID | Type | Action Taken |
|---|---|---|
| A-004 | WeakStatement | Clarified welding/bolting standard in Step 3.7; replaced "or equivalent" with material-dependent resolution guidance |
| D-001 | VerificationGap | Added Step 5.3 requiring formal County approval record before IFC; added Verification table row |
| D-003 | VerificationGap | Added Step 4.5 for independent QA review determination; added Verification table row |
| E-002 | TBD_Question | Added Design Team Agreement Record row to Records table |
| X-004 | Normalization | Normalized Step 4.3 conditional language to require positive determination on embedment use |
