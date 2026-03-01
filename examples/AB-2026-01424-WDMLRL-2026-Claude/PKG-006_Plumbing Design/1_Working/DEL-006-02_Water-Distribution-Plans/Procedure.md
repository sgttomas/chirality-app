# Procedure — DEL-006-02: Water Distribution Plans

**Deliverable ID:** DEL-006-02
**Document Type:** Procedure (operational)
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## Purpose

This Procedure describes the steps to **produce** the Water Distribution Plans drawing set (DEL-006-02). It provides a sequence of tasks for the Plumbing Engineer and project team to progress from preliminary design through to the issue of Issued For Construction (IFC) drawings.

The procedure covers the drawing set production process only. Installation of the water distribution system is governed by PKG-014 (Plumbing & Water Systems Installation) and DEL-006-08 (Plumbing Specification).

---

## Prerequisites

Before beginning drawing set production, the following must be in place:

| # | Prerequisite | Source | Status |
|---|---|---|---|
| 1 | County-approved Preliminary Plumbing Design (DEL-006-01) | RFP §3.3.2; Decomp. DEL-006-01 | TBD — required before IFC drawings |
| 2 | Geotechnical Investigation Report (DEL-008-01) | Decomp. — required for foundation/slab design | TBD |
| 3 | Preliminary Site Survey (DEL-008-02) | Decomp. | TBD |
| 4 | Architectural Floor Plans (DEL-001-02) or approved preliminary architectural | Decomp. DEL-001-02; coordination requirement | TBD |
| 5 | Structural Foundation Plan (DEL-002-02) — or working draft | Required for slab penetration/sleeve coordination | TBD |
| 6 | Appendix B (Plumbing) conceptual drawing | R-06 — available in _Sources/ | Available |
| 7 | RFP §3.4 Design Requirements | R-01 — available in _Sources/ | Available |
| 8 | Project drawing standard / title block template | TBD — to be established by project team | TBD |
| 9 | Drawing numbering convention confirmed | TBD — ASSUMPTION: P-series prefix [D-002] | TBD |
| 10 | Plumbing Engineer assigned and under contract | Project management | TBD |
| 11 | Applicable Alberta Safety Codes and NPC edition confirmed | Plumbing Engineer professional determination | TBD |

---

## Steps

### Step 1: Confirm Scope Boundaries with PKG-006 Team

**Action:** Before beginning drawing production, the Plumbing Engineer shall confirm the internal scope boundaries between DEL-006-02 (Water Distribution Plans) and sibling deliverables:
- DEL-006-03 (Drain & Vent Plans) — confirm floor drain and waste connections are excluded from this drawing set and are shown in DEL-006-03
- DEL-006-04 (Cistern & Pump Details) — define the interface point between the pump discharge and the distribution system; agree on which drawing set shows the bulk fill piping interface (see CF-002 in Guidance.md Conflict Table)
- DEL-006-05 (Septic System Details) — confirm septic connections are excluded from this set

**Prerequisite Verification Gate [X-001]:** Before proceeding past this step, formally verify that all prerequisites in the Prerequisites table are satisfied or formally waived. Document the status of each prerequisite item. If any mandatory prerequisite (items 1, 6, 7, 10, 11) is not satisfied and cannot be waived, do not proceed to drawing production steps without Project Manager authorization.

**Output:** Agreed scope boundary memo or notes in MEMORY.md; completed prerequisite verification checklist.

### Step 2: Establish Drawing Set Structure

**Action:**
1. Confirm drawing numbering convention with the project team (ASSUMPTION: P-100 series for plumbing plans [D-002] — this assumption must be confirmed before drawing production begins).
2. Create a drawing register listing all anticipated sheets in DEL-006-02 (reference Datasheet.md — Drawing Sheet Anticipated Content). **[E-002] The drawing register shall use a defined template or format specifying at minimum: sheet number, sheet title, revision, date, scale, and status. Project Manager to confirm whether a project-wide drawing register template exists.**
3. Establish sheet sizes, title block format, and drawing standard consistent with the project IFC requirement.
4. Confirm CAD/BIM platform (TBD — coordinate with project team; ASSUMPTION: AutoCAD or Revit MEP standard for Alberta design-build of this scale [F-004]). **Note: platform choice affects file formats, coordination workflows (BIM clash detection per REQ-010 Verification Criteria), and deliverable format. Confirm before beginning Step 3.**

**Output:** Drawing register (using defined template); drawing standard confirmed; CAD/BIM platform confirmed.

### Step 3: Review and Interpret Source Documents

**Action:**
1. Review Appendix B (Plumbing) conceptual drawing (R-06) and extract all fixture and plumbing area locations.
2. Review RFP §3.4 design requirements and extract all water system parameters (50,000 L cistern, 100 LPM pump, 2.5 inch filling connection, bulk water fill, emergency shower, taps, pressure washer reel, wash station, washroom expansion).
3. Cross-reference with the decomposition (SOW-0041, SOW-0042, SOW-0044, SOW-0048, SOW-0049, SOW-0050) to confirm all scope items are captured.
4. Flag any gaps between the conceptual drawing and the RFP text requirements for resolution in preliminary design.

**Output:** Annotated source review notes; scope item coverage matrix.

### Step 4: Develop Preliminary Plumbing Distribution Layout

**Action** (performed as part of DEL-006-01, referenced here for continuity):
1. Develop a preliminary plan showing proposed pipe routing, fixture connection points, and major valving.
2. Submit preliminary layout as part of DEL-006-01 (Preliminary Plumbing Design) for County approval.
3. Incorporate County feedback before proceeding to IFC production.

**Note:** DEL-006-01 must be County-approved before IFC drawings are issued (RFP §3.3.2).

**Output:** County-approved preliminary distribution layout (DEL-006-01).

### Step 5: Perform Hydraulic Design and Calculations

**Action** (performed as part of DEL-006-07, referenced here for integration):
1. Size supply mains and branch lines based on fixture unit demand and the 100 LPM pump delivery (RFP §3.4).
2. Determine system pressure at each fixture under simultaneous demand conditions.
3. Confirm emergency shower supply meets applicable flow rate and tepid water requirements (ASSUMPTION: ANSI Z358.1 or equivalent; verify applicable standard). Verify against REQ-002 Acceptance Criteria in Specification.md [C-002].
4. Confirm pressure washer reel supply flow rate adequacy.
5. Document calculations in DEL-006-07 (Plumbing Calculation Package).

**Output:** Pipe sizing table; pressure analysis; confirmed fixture flow rates (DEL-006-07). **Update Datasheet.md — Fixture and Tap Locations flow rate column with confirmed values [B-001].**

### Step 5A: Freeze Protection Design [C-004]

**Action:** Determine freeze protection requirements for the water distribution piping:
1. Identify all piping runs in unheated areas, exterior walls, near overhead doors, or locations exposed to freezing temperatures.
2. Determine the applicable freeze protection strategy for each run:
   - Insulation type and R-value/thickness
   - Heat tracing (if applicable) — coordinate wattage/circuit requirements with PKG-004 (Electrical)
   - Drain-down provisions for seasonal or emergency isolation
3. Document the design outdoor temperature and insulation parameters.
4. If heat tracing is selected for any runs, coordinate with PKG-004 for electrical circuit requirements.
5. Record all freeze protection parameters in Datasheet.md — Freeze Protection Parameters [B-002].

**Note:** This step addresses REQ-012 (Freeze Protection) in Specification.md [F-001] and the Alberta climate considerations in Guidance.md. The freeze protection strategy is a trade-off between passive (insulation only) and active (insulation + heat tracing) approaches — see Guidance.md Trade-offs.

**Output:** Freeze protection design documentation; Datasheet.md freeze protection parameters populated; coordination request to PKG-004 (if heat tracing selected).

### Step 6: Produce IFC Drawing Set

**Action:**
1. Draw plan views of water distribution system at each floor level (ASSUMPTION: single storey + mezzanine where applicable), showing:
   - Supply mains from cistern/pump interface point
   - Branch lines to each fixture/tap location
   - Isolation valves at branches and fixtures
   - Pipe sizes labeled on all runs
   - Pipe material designations
   - Sleeve/penetration locations (coordinated with structural)
   - Freeze protection notations where applicable (insulation type, heat tracing — per Step 5A)
2. Produce isometric diagrams of the supply system.
3. Produce detail sheets for non-standard connections (emergency shower tempering valve — if applicable; pressure washer reel connection; bulk fill interface).
4. Produce pipe, fitting, and valve schedule.
5. Add construction notes covering: pressure testing requirements (test pressure, hold duration, and acceptable pressure drop TBD — to be established per applicable code [X-004]), disinfection/flushing, material specifications (cross-reference to DEL-006-08), freeze protection notes (per Step 5A and REQ-012), inspection requirements.
6. Include title block data: project name, drawing number (per confirmed convention [D-002]), revision block per REQ-013, scale, date, P.Eng. signature/stamp block.

**Output:** Draft drawing set (internal review stage).

### Step 6A: Internal Quality Review [F-005]

**Action:** Before issuing the draft drawing set for interdisciplinary coordination (Step 7), conduct a formal internal quality review:
1. Plumbing Engineer (or designated internal reviewer) reviews the draft drawing set against:
   - Specification.md requirements (REQ-001 through REQ-013)
   - SOW-to-Drawing Traceability matrix (Specification.md) — verify all SOW items are addressed [X-005]
   - Datasheet.md key parameters — verify consistency between drawing annotations and Datasheet values
   - Code review items identifiable at draft stage
2. Document all findings in an internal review log.
3. Resolve all internal findings before proceeding to Step 7.

**Note:** This internal quality gate ensures that the draft drawing set is reviewed for completeness and accuracy before being issued for external coordination. Without this gate, unchecked errors may propagate into the coordination process.

**Output:** Internal review log; corrected draft drawing set ready for coordination.

### Step 7: Interdisciplinary Coordination Review

**Action:**
1. Issue the draft drawing set for coordination review to:
   - Structural Engineer (slab penetrations, sleeve sizes, locations — DEL-002)
   - Mechanical Engineer (utility room layout, equipment clearances — PKG-003)
   - Electrical Engineer (pump power, heat tracing circuits if applicable — PKG-004)
   - Architect (room layouts, fixture rough-in heights — PKG-001)
2. Receive and document markups in a coordination review log. **[A-004] The coordination review log shall use a defined format or template specifying at minimum: item number, discipline, description, resolution, status, and responsible party.**
3. Resolve all coordination conflicts before IFC issue. Unresolved conflicts to be documented and escalated to project coordination meeting.

**Output:** Coordination review markup set; coordination review log (using defined template format).

### Step 8: Code and Regulatory Review

**Action:**
1. Plumbing Engineer performs a self-review of the drawing set against the applicable Alberta Safety Codes, NPC (and provincial amendments), and any applicable referenced standards.
2. Confirm all IFC drawings comply with code requirements or document deviations with variance applications (if applicable).
3. Prepare Safety Code permit application documents if required by the jurisdiction (ASSUMPTION: plumbing permit required; confirm with PKG-009 permitting lead).

**[A-004] Code Review Checklist:** The code review checklist shall use a defined format or template. At minimum, the checklist shall include:
- Standard/code reference (edition identified per Specification.md Standards table)
- Applicable clause or section
- Compliance status (compliant / non-compliant / not applicable)
- Drawing sheet reference
- Notes / variance application reference (if applicable)

**Output:** Code review checklist (using defined template format); permit application documents (if applicable).

### Step 8A: DEL-006-01 Approval Hold Point [X-002]

**Action:** Before proceeding to P.Eng. stamp and IFC issue (Step 9), formally verify:
1. County approval of DEL-006-01 (Preliminary Plumbing Design) has been received in writing.
2. All deviations from the approved DEL-006-01 submission have been documented and submitted for County review per REQ-011.

**This is a mandatory hold point.** If DEL-006-01 approval has not been received, do not proceed to Step 9. Escalate to the Project Manager.

**Note:** REQ-011 requires the IFC drawing set to be based on the County-approved preliminary design. Step 4 verification references this requirement, but no explicit procedural gate previously enforced it before IFC issue. This hold point formalizes that enforcement.

**Output:** Written confirmation of DEL-006-01 County approval; deviation log (if applicable).

### Step 9: P.Eng. Stamp and IFC Issue

**Action:**
1. Plumbing Engineer reviews final drawing set, confirms all coordination and code requirements are satisfied.
2. P.Eng. signs and stamps all IFC drawing sheets.
3. Issue IFC drawing set to the project team, County representative, and construction trades.
4. File signed originals per project document management protocol (TBD).

**Output:** Stamped IFC drawing set (DEL-006-02 complete).

---

## Verification

The following checks confirm that each step has been completed successfully:

| Step | Verification Check |
|---|---|
| Step 1 — Scope boundaries + prerequisite gate [X-001] | Scope boundary agreement documented; prerequisite verification checklist completed — all mandatory prerequisites satisfied or formally waived; no fixture or system appears on both DEL-006-02 and a sibling drawing set without cross-reference |
| Step 2 — Drawing set structure | Drawing register created using defined template [E-002]; title block template confirmed; CAD/BIM platform confirmed [F-004] |
| Step 3 — Source review | All SOW items (SOW-0041, 0042, 0044, 0048, 0049, 0050) traceable to drawing content or noted as TBD with reason |
| Step 4 — Preliminary layout | DEL-006-01 issued and County approval confirmed in writing before IFC production begins |
| Step 5 — Hydraulic design | DEL-006-07 calculation package complete; pipe sizes on drawings match calculation output; Datasheet.md fixture flow rates populated [B-001] |
| Step 5A — Freeze protection [C-004] | Freeze protection strategy documented for all applicable piping runs; Datasheet.md freeze protection parameters populated [B-002]; PKG-004 coordination request issued if heat tracing selected |
| Step 6 — IFC drawing set | All anticipated sheets per drawing register produced; pipe sizes, materials, valving, schedules, and notes complete; freeze protection notations included |
| Step 6A — Internal quality review [F-005] | Internal review log completed; all findings resolved; SOW traceability matrix verified [X-005] |
| Step 7 — Coordination review | Coordination review conducted with all disciplines using defined log format [A-004]; no outstanding unresolved conflicts at IFC issue |
| Step 8 — Code review | Code review checklist completed using defined template [A-004]; permit application submitted (if applicable) |
| Step 8A — DEL-006-01 hold point [X-002] | Written confirmation of DEL-006-01 County approval on file; deviation log complete (if applicable) |
| Step 9 — Stamp and issue | All IFC sheets bear P.Eng. stamp and signature per REQ-009; revision blocks per REQ-013; IFC transmittal issued and acknowledged |

---

## Records

The following records shall be created and retained as evidence of this procedure:

| Record | Description | Format / Template | Retained By |
|---|---|---|---|
| Prerequisite verification checklist [X-001] | Documented status of all prerequisites before drawing production | TBD — checklist format to be established by Project Manager | Project Manager |
| Scope boundary agreement | Notes or memo confirming DEL-006-02 scope limits vs. sibling deliverables | Memo or meeting minutes | Plumbing Engineer / Project Manager |
| Drawing register [E-002] | List of all sheets in the drawing set with revision history | TBD — defined template specifying sheet number, title, revision, date, scale, status | Plumbing Engineer |
| Preliminary design approval letter/email | County written approval of DEL-006-01 | Written correspondence | Project Manager |
| Hydraulic calculation package | DEL-006-07 — supports pipe sizing on IFC drawings | Per DEL-006-07 format | Plumbing Engineer |
| Freeze protection design documentation [C-004] | Parameters, strategy, and coordination requests for freeze protection | As documented in Datasheet.md and drawing notes | Plumbing Engineer |
| Internal quality review log [F-005] | Findings and resolutions from internal review before coordination | TBD — log format to be established by Plumbing Engineer | Plumbing Engineer |
| Coordination review log [A-004] | Record of markups received and resolutions | TBD — defined template specifying item number, discipline, description, resolution, status, responsible party | Plumbing Engineer / Project Manager |
| Code review checklist [A-004] | Self-certification of code compliance | TBD — defined template per Step 8 requirements | Plumbing Engineer |
| Safety Code permit application and approval | Plumbing permit for construction | Per jurisdiction requirements | Project Manager (PKG-009) |
| Signed IFC drawing set | Original stamped drawings or digital equivalent per project standard | Per project document management protocol | Project Manager / Owner |
| IFC transmittal record | Evidence of issue to construction trades and County | Per project transmittal format | Project Manager |
| Inspection reports [E-003] | Copies of all completed inspection reports (per RFP §3.3.2) | TBD — format and content requirements to be defined by Project Manager / PKG-009. At minimum: date, inspector, items inspected, pass/fail, deficiency notes, sign-off. | Project Manager |
