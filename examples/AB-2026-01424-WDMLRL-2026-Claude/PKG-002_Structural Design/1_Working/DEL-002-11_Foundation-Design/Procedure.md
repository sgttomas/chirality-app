# Procedure — DEL-002-11 Foundation Design Package (Variable-Price)

---

## Purpose

This procedure describes the steps to produce the Foundation Design Package (DEL-002-11) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition, from initial design basis through IFC-ready deliverables. The procedure covers both the proposal-phase estimate and the post-award IFC design completion phases.

The procedure is intended for use by the Structural Engineer (responsible party) and the project team coordinating this deliverable within PKG-002 — Structural Design.

---

## Prerequisites

Before beginning this procedure, confirm the following inputs are available or in progress:

| Prerequisite | Source | Status at Procedure Start |
|---|---|---|
| RFP §4.8.2 — Foundation variable-price requirements | AB-2026-01424-WDMLRL RFP.pdf | Available — must be read |
| RFP §3.3.2, §3.4 — Scope of Work and Design Requirements | AB-2026-01424-WDMLRL RFP.pdf | Available — must be read |
| Appendix B (Shop) — Conceptual floor plan and structural notes | AB-2026-01424-Appendix B (Shop).pdf | Available — must be reviewed |
| Decomposition — DEL-002-11 entry, SOW-0019, OBJ-003, OBJ-006 | WDMLRL_Decomposition_Claude.md | Available — must be reviewed |
| Geotechnical Investigation Report (DEL-008-01) | PKG-008 output | REQUIRED for post-award IFC phase; NOT required for proposal-phase estimate (assumed normal conditions per RFP §4.8.2) |
| Preliminary Structural Design approval (DEL-002-01) | PKG-002 output | REQUIRED before IFC drawings are finalized; County project team approval needed |
| Architectural Floor Plans (DEL-001-02) | PKG-001 output | REQUIRED for column grid and building footprint confirmation |
| Cistern dimensions and weight (from Plumbing Engineer) | PKG-006 / DEL-006-04 | REQUIRED before final slab/foundation load schedule |
| Crane technical data (wheel loads, rail spacing) | PKG-016 / DEL-016-01 supplier data | REQUIRED for crane column base and foundation design. **Note (F-003):** If crane data is unavailable at proposal time, proceed using assumed crane loads based on typical 5-tonne overhead crane specifications; document assumptions explicitly and flag for revision upon receipt of supplier data. See Guidance.md, Crane Support Interface, for further direction. |
| Alberta Building Code (ABC) and NBC — current editions | Structural Engineer's reference library | Must be confirmed by engineer of record; specific governing edition (year) to be documented per Specification.md REQ-004 and Standards table |

---

## Steps

### Phase 1 — Proposal-Phase Foundation Cost Estimate

**Step 1.1 — Assemble Design Parameters (Assumed)**

1. Confirm building footprint: 130 ft x 100 ft (from Appendix B); confirm this with Architect (DEL-001-02 preliminary).
2. Confirm ceiling height: 35 feet (from RFP §3.4, Appendix B).
3. Establish assumed geotechnical parameters for "normal ground conditions":
   - Allowable bearing capacity: ASSUMPTION — use a conservative typical value for central Alberta glacial till or similar material (e.g., 100–150 kPa); document explicitly as assumed. Record in Datasheet.md Attributes table.
   - Frost depth: ASSUMPTION — conservatively assume 2.0 m below grade for design purposes (upper bound of typical 1.5–2.0 m range for central Alberta); confirm with NBC climatic appendix for Ferintosh, AB. Record in Datasheet.md Attributes table.
   - Groundwater: ASSUMPTION — groundwater assumed absent under normal conditions per RFP §4.8.2 ("without deleterious subgrade material"). Record in Datasheet.md Attributes table.
   - Record all assumptions in the Design Basis Document with the notation "ASSUMPTION — revise upon receipt of DEL-008-01."
4. Establish assumed crane loads if crane technical data is unavailable — document assumed values based on typical 5-tonne overhead crane specifications. (Source: Guidance.md, Crane Support Interface; _SEMANTIC_LENSING.md F-003)

> **QUALITY HOLD POINT 1 (A-004):** Before proceeding to Step 1.2, the Structural Engineer should confirm that all assumed design parameters (Step 1.1) have been documented in the Design Basis Document and reviewed by the Project Manager. This hold point ensures that the proposal-phase estimate is based on documented and defensible assumptions.

**Step 1.2 — Develop Preliminary Load Schedule**

1. Compile all loads acting on the foundation:
   - Structural dead loads: concrete frame weight, roof, mezzanine structure, slab.
   - Live loads: floor (heavy equipment, motor scraper class — document assumed design load value in kPa or kN per Specification REQ-006), mezzanine (heavy storage — oil totes, pumping equipment — document assumed mezzanine design live load in kPa per Specification REQ-008).
   - Equipment loads: two 5-tonne overhead cranes (dynamic load factors per NBC/CSA); 50,000 L cistern (full weight).
   - Lateral loads: wind and seismic per NBC/ABC for project location.
2. Apply load combinations per NBC/ABC.
3. Document load schedule in the Design Basis Document.

**Step 1.3 — Develop Foundation Concept (Normal Conditions)**

1. Based on assumed bearing capacity and load schedule, size preliminary footings or foundation system (e.g., spread footings under columns, continuous grade beams, slab-on-grade).
2. Identify below-grade elements: service pit/trench (below-grade retention), wash bay slab with drainage penetrations, cistern interface.
3. Confirm frost-depth compliance for all footings.
4. Sketch preliminary foundation plan — sufficient for cost estimating purposes.

> **QUALITY HOLD POINT 2 (A-004):** Before proceeding to Step 1.4, the foundation concept (Step 1.3) should be reviewed by a senior engineer or Project Manager to confirm that the concept is reasonable for cost estimating purposes and that all major load cases have been addressed.

**Step 1.4 — Prepare Variable-Price Cost Estimate**

1. Based on the preliminary foundation concept, prepare a cost estimate for foundation design and construction.
2. Clearly label: "Estimated cost — based on normal ground conditions per RFP §4.8.2 — subject to revision upon receipt of geotechnical report."
3. Structure the estimate to satisfy RFP Proposal Section 3.2 "Foundation Design & Construction" — separate from the firm-price total (RFP §4.8.1).
4. If crane technical data was unavailable and assumed loads were used, note this explicitly in the cost estimate. (Source: Guidance.md, Crane Support Interface)
5. Include the estimate in the Proposal submission package.

---

### Phase 2 — Post-Award Foundation Design to IFC

**Step 2.1 — Receive and Review Geotechnical Report (DEL-008-01)**

1. Upon receipt of the completed geotechnical investigation report (DEL-008-01), the Structural Engineer shall:
   - Compare actual geotechnical findings to all assumptions recorded in Step 1.1 and tracked in the assumption register (Specification REQ-018).
   - Identify any parameters that differ materially from assumptions.
   - Prepare a summary of differences and their structural implications.
2. If material differences exist (e.g., lower bearing capacity, unexpected groundwater, deleterious material), initiate the variable-price re-negotiation process with the County per CCDC 14–2013 and RFP §4.8.2. Identify the specific CCDC 14–2013 clause governing the re-negotiation (see Guidance.md, P-1 for contractual mechanism discussion).

**Step 2.2 — Update Design Basis Document**

1. Update the Design Basis Document to replace all assumptions with confirmed geotechnical parameters.
2. Record which assumptions were confirmed, which were revised, and by how much.
3. Update the assumption register (REQ-018) to mark each assumption as validated, revised, or flagged for re-design.
4. Issue Design Basis Document to the project team as the authoritative foundation design reference.

**Step 2.3 — Develop Structural Calculations**

1. Perform full structural calculations for:
   - Footing bearing: verify bearing capacity against allowable from geotech report.
   - Settlement analysis: confirm acceptable total and differential settlement for the structure type; document settlement limits and justify per Specification REQ-016.
   - Reinforcement design: footings, grade beams, slab-on-grade (per CSA A23.3).
   - Crane column bases: anchor bolt design for crane rail reactions (per CSA A23.3, CSA S16 for steel plate embedments).
   - Service pit/trench walls: retained earth pressure, concrete wall design.
   - Steel plate embedments: confirm adequate anchorage into slab (coordinate with DEL-002-08 Embedment Plan).
   - Cistern foundation: confirm slab/footing capacity under full cistern load.
   - Mezzanine column bases: load transfer from mezzanine columns to footings; document assumed mezzanine design live load per Specification REQ-008.
2. Confirm concrete materials specification per Specification REQ-017 (exposure class, minimum compressive strength, air entrainment requirements per CSA A23.1/A23.2).
3. Perform all calculations in accordance with NBC/ABC load combinations and CSA A23.3 (concrete) and CSA S16 (steel plate embedments). Confirm governing code editions per Specification Standards table.
4. Document calculations in the Structural Calculation Package (contributes to DEL-002-10).

> **QUALITY HOLD POINT 3 (A-004):** Before proceeding to Step 2.4, the structural calculation package should be peer-reviewed by a second engineer or senior reviewer (see also Step 2.7a below). This hold point ensures calculations are complete, internally consistent, and code-compliant before drawing production begins.

**Step 2.4 — Produce Foundation Drawing Set**

1. Produce the Foundation Plan drawing (feeds DEL-002-02):
   - Show all footing locations, sizes, and types.
   - Show slab-on-grade extents, thickness, and reinforcement callouts.
   - Show service pit/trench in plan, with reference to sections.
   - Show cistern location with foundation support detail.
   - Show crane column base locations.
   - Coordinate with Architectural floor plan (DEL-001-02) for column grid alignment.
2. Produce Foundation Detail drawings (feeds DEL-002-02 / DEL-002-04 as applicable):
   - Footing sections and reinforcement details.
   - Grade beam sections (if used).
   - Service pit/trench wall sections.
   - Crane column base anchor bolt details.
   - Steel plate embedment details (coordinate with DEL-002-08).
   - Slab joint and construction joint details.

**Step 2.5 — Coordinate with Other Disciplines**

1. Issue foundation plan to Architect — confirm alignment with architectural floor plan and any penetrations through slab.
2. Issue foundation plan to Mechanical Engineer — confirm any mechanical penetrations or equipment bases.
3. Issue foundation plan to Plumbing Engineer — confirm floor drain stub-ups, sump pits, and cistern interface.
4. Issue foundation plan to Civil Engineer — confirm interface with site grading and drainage (positive drainage away from building, as required by RFP §3.4 / SOW-0020).
5. Confirm crane base details with Crane Contractor (PKG-016) — anchor bolt layout must match crane supplier's requirements.
6. Resolve all inter-discipline conflicts before IFC stamp.
7. Retain evidence of coordination correspondence for each discipline (per Specification REQ-013).

**Step 2.6 — Preliminary Design Review (County Approval)**

1. Prior to finalizing IFC drawings, submit preliminary foundation design (as part of DEL-002-01 Preliminary Structural Design, or as a stand-alone preliminary package if required by project schedule) to the County project team for review and approval.
2. Incorporate County review comments.
3. Obtain written approval confirmation before proceeding to IFC stamp.
**Source:** RFP §3.3.2 — "Deliver Preliminary Design for the County project team to approve."

**Step 2.7 — Peer Review and Final IFC Stamp**

1. **Peer review (A-005):** Before P.Eng. stamp, the structural calculation package and foundation drawing set shall be formally peer-reviewed by a second qualified engineer or senior reviewer. The peer reviewer shall:
   - Confirm calculations are complete and internally consistent.
   - Confirm drawings accurately reflect the calculations.
   - Confirm code compliance (governing editions per Standards table).
   - Sign and date the peer review record.
2. Complete all revisions from Step 2.5 (coordination), Step 2.6 (County approval), and peer review findings.
3. Confirm all drawings comply with ABC/NBC and applicable CSA standards.
4. P.Eng. (licensed in Alberta) signs and stamps all IFC foundation drawings.
5. Issue IFC drawing set to:
   - General Contractor (PKG-010 — Foundation Construction)
   - Project Manager / PM
   - County (for records)
   - Other disciplines as required for coordination.

> **Enrichment note (A-005):** Peer review was previously mentioned only in the Verification table and not in the procedural steps. It is now a formal step (2.7 item 1) to ensure it is treated as mandatory rather than optional. (Source: _SEMANTIC_LENSING.md A-005; Procedure.md Verification table — peer review row)

**Step 2.8 — Update Variable-Price Cost Estimate (if applicable)**

1. If geotech findings resulted in changes to the foundation design scope or cost, prepare an updated cost estimate.
2. Present revised estimate to the County project manager for negotiation of final variable-price foundation scope per RFP §4.8.2. Reference the specific CCDC 14–2013 clause identified per Guidance.md P-1.
3. Record negotiated price in project cost register and CCDC 14–2013 contract documentation.

---

## Verification

After completing each phase, confirm the following:

| Check | Verification Method |
|---|---|
| All assumed geotechnical parameters documented | Review Design Basis Document — all assumptions labeled "ASSUMPTION"; assumption register (REQ-018) populated |
| Cost estimate labeled as variable-price, normal conditions | Review Proposal submission — cost estimate wording confirmed |
| Geotech report reviewed and compared to assumptions | Comparison summary on file; assumption register updated; re-negotiation initiated if warranted |
| Structural calculations complete and internally consistent | Calculation package peer-reviewed by second engineer or senior reviewer; peer review record signed and dated (per Step 2.7 item 1) |
| Foundation plan coordinates with architectural grid | Overlay check against DEL-001-02 architectural floor plan |
| Crane column bases match supplier anchor bolt layout | Confirmation received from crane contractor (PKG-016); if assumed loads were used, confirmation that assumptions are flagged for revision |
| Service pit/trench structurally designed for retained earth | Pit wall calculation included in DEL-002-10 |
| Cistern load included in foundation load schedule | Load schedule in Design Basis Document includes cistern full-weight case |
| Settlement analysis complete | Settlement analysis in calculation package; total and differential settlement within stated limits per REQ-016 |
| Concrete materials specified | Exposure class, minimum compressive strength, and special requirements per REQ-017 and CSA A23.1/A23.2 |
| All IFC drawings P.Eng. stamped | Physical review of stamped drawing set |
| County preliminary approval obtained | Written approval on file |
| IFC drawings issued to construction package (DEL-010-01) | Transmittal record on file |
| IFC drawing transmittal records created and retained | Transmittal record for each IFC drawing issue confirmed complete and filed per Records table (Source: _SEMANTIC_LENSING.md X-005) |
| Governing code editions confirmed | IFC drawing notes state the specific governing code edition (year) for each applicable standard per Specification Standards table and REQ-004 |
| Assumption register resolved post-geotech | All ASSUMPTION items in register either validated, revised, or flagged for re-design per REQ-018 |

---

## Records

The following records shall be created and retained as evidence of this deliverable:

| Record | Description |
|---|---|
| Design Basis Document | Geotechnical assumptions (proposal phase) and confirmed parameters (post-geotech), design criteria, load schedule, governing codes, assumption register (REQ-018) |
| Foundation Cost Estimate — Proposal Phase | Normal-conditions estimate; included in Proposal section 3.2 |
| Updated Foundation Cost Estimate (if applicable) | Revised estimate post-geotech; basis for County negotiation |
| Structural Calculation Package (Foundation Component) | Full calculations per CSA A23.3, CSA S16; contributes to DEL-002-10 |
| Peer Review Record | Signed and dated record of peer review per Step 2.7 item 1 |
| Foundation Plan Drawing (IFC) | Stamped drawing — feeds DEL-002-02 |
| Foundation Detail Drawings (IFC) | Stamped drawings — footing, slab, pit, crane base, steel plate embedment details |
| Coordination Correspondence | Records of inter-discipline coordination (architecture, mechanical, plumbing, civil, crane contractor) — per REQ-013 |
| County Preliminary Approval Record | Written approval from County project team |
| IFC Drawing Transmittal Record | Record of IFC drawing issue to General Contractor and other recipients |
| Variable-Price Negotiation Record | Documentation of post-geotech price negotiation with County per RFP §4.8.2 |
