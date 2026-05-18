# Procedure — DEL-004-01 Preliminary Electrical Design

---

## Purpose

This procedure describes the steps to **produce** the Preliminary Electrical Design presentation deliverable (DEL-004-01) for the New North Shop Addition at the West Dried Meat Lake Regional Landfill (X-002). The output is a design presentation document suitable for County project team review and approval in accordance with RFP §3.3.2 (SOW-0010d).

---

## Prerequisites

### Reference Documents Required

| Document | Location | Required For |
|---|---|---|
| RFP — AB-2026-01424-WDMLRL RFP.pdf | _Sources/ | Design requirements (§1.0, §3.3.2, §3.4) |
| Appendix B (Electrical) — AB-2026-01424-Appendix B (Electrical).pdf | _Sources/ | Conceptual electrical layout, fixture counts, circuit types |
| WDMLRL_Decomposition_Claude.md | _Decomposition/ | SOW items, objectives, deliverable list for PKG-004 |
| Canadian Electrical Code (CEC), Part I | ASSUMPTION: Electrical Engineer's professional library — location TBD | Code compliance |
| Alberta Safety Codes Act (electrical) | ASSUMPTION: Electrical Engineer's professional library — location TBD | Code compliance |

### Upstream Dependencies

No human-declared upstream dependencies are recorded in `_DEPENDENCIES.md` (status: NOT_TRACKED). The following dependencies are identified from source review:

- **Architectural preliminary layout** (DEL-001-01 or working drawings): Needed to confirm room dimensions, panel space allocation, and overhead door locations for circuit planning. ASSUMPTION: Preliminary architectural information must be available before electrical layout can be finalized.
- **Mechanical preliminary design** (DEL-003-01): Needed to confirm exhaust fan quantities, locations, and motor sizes for circuit allocation.
- **Utility service information**: The existing electrical service infrastructure at the landfill site must be confirmed with the local utility provider to establish service voltage, available capacity, and tie-in requirements (SOW-0081). This information is not in the RFP.
- **Crane equipment specifications**: Needed to size crane power circuits (R-007). County to supply or confirm equipment specifications, or Electrical Engineer to obtain from anticipated crane supplier. **(F-002):** If crane specifications are unavailable, document the gap and note provisional assumptions for preliminary design. See Step 2.1 for fallback procedure.

### Responsible Party

Electrical Engineer (per _CONTEXT.md and Decomposition §7 PKG-004 deliverable table).

---

## Steps

### Step 1 — Review Source Documents

1.1 Read RFP §3.4 (Design Requirements) and §3.3.2 (Scope of Work) to confirm all electrical design requirements.

1.2 Study App B (Electrical) conceptual drawing in detail. Extract:
- Lighting fixture counts and types per room (see Datasheet — Lighting table).
- Receptacle types and approximate locations (see Datasheet — Receptacle table).
- Equipment circuit notes (compressor 40A, fire hose pump 70A, pressure washer 70A).
- Electrical legend (15A/120V, 20A/120V, 20A/240V, 30A/240V, 50A/240V, Lights, Exhaust Fan symbols).
- Low-voltage system notes (security camera wiring, antenna wire).

1.3 Review Decomposition §3G (SOW items G-series, SOW-0051 through SOW-0066) to confirm full scope of electrical and low-voltage systems to be addressed.

1.4 Confirm with the project team that no additional addenda or Owner clarifications have been issued that affect the electrical scope.

### Step 2 — Gather Preliminary Design Information

2.1 Obtain or confirm the following information (TBD items from Step 1 prerequisites):

- Architectural floor plan showing room locations, dimensions, and overhead door positions (including overhead door count — see Datasheet B-003).
- Mechanical preliminary layout showing exhaust fan locations and makeup air unit location.
- Utility provider information (A-004):
  - Identify the utility provider serving the West Dried Meat Lake Regional Landfill site.
  - Contact the utility provider (or request the project team to initiate contact) to obtain: existing service voltage at the site, available capacity, meter location requirements, and service connection/tie-in process and timeline.
  - Set a target date for obtaining utility information, aligned with the preliminary design submission schedule.
  - See Guidance — Considerations — Electrical service tie-in coordination (B-004) for additional context.
- Crane equipment specifications (or preliminary specification for budgeting purposes). **Note (F-002):** If crane specifications are unavailable at the preliminary design stage, document the gap explicitly and note provisional assumptions for crane circuit sizing. The gap should be carried forward as a TBD item in the design narrative and the Outstanding TBD Register.

2.2 If any prerequisite information cannot be obtained prior to preliminary design submission, document the gap and note it as TBD in the preliminary design presentation with an explanation.

### Step 2A — Readiness Gate (X-001, X-003)

Before proceeding to Step 3, verify that the prerequisite information from Step 2 has been obtained or that gaps are documented:

| Prerequisite | Status | Notes |
|---|---|---|
| Architectural floor plan (room layout, dimensions, overhead door positions and count) | Obtained / TBD | |
| Mechanical preliminary layout (exhaust fan locations, makeup air unit) | Obtained / TBD | |
| Utility provider information (service voltage, capacity, tie-in process) | Obtained / TBD | |
| Crane equipment specifications (motor ratings, power requirements) | Obtained / TBD | |

- If all four prerequisites are obtained: proceed to Step 3.
- If any prerequisite is TBD: confirm the gap is documented per Step 2.2, note the provisional assumption or TBD annotation that will be used in the layout, and proceed to Step 3 with the documented gap.
- **Do not proceed to Step 3 without completing this readiness check.** The purpose is to ensure that layout development does not begin without essential inputs being either available or explicitly flagged as missing.

### Step 3 — Develop Preliminary Electrical Layout

3.1 Prepare a preliminary electrical layout drawing at a scale appropriate for County review (TBD — drawing scale to be confirmed with the project team before layout development; F-003). The layout shall show:

- Building outline with room labels (Main Shop, Wash Bay, Office, Utility Room, Parts/Tool Room, Service Pit) consistent with App B (Electrical) and architectural layout.
- Lighting fixture locations and symbols consistent with the electrical legend, with fixture counts matching R-002 through R-005.
- Receptacle locations and symbols by type (15A/120V, 20A/120V, 20A/240V, 30A/240V, 50A/240V) consistent with App B (Electrical) layout and R-006.
- Overhead crane power feed locations (two crane bays as shown on App B).
- Overhead door operator power points.
- Equipment circuit symbols or annotations for compressor (40A), fire hose pump (70A), pressure washer (70A).
- Ceiling fan power points (6 locations in main shop).
- Exhaust fan power points (coordinated with mechanical).
- Low-voltage system rough-in locations (security camera conduit points, radio antenna wire routing).
- Proposed main panel/distribution board location.
- Service entry point (preliminary).
- Electrical legend on drawing.

3.2 For items where final information is not yet available, use TBD annotations on the drawing. Do not invent values.

3.3 Check that the layout is consistent with App B (Electrical) — do not reduce fixture counts or remove circuits shown on the conceptual drawing without County awareness.

### Step 4 — Prepare Design Narrative

4.1 Prepare a brief design narrative (1–3 pages) covering:

- System description: Three-phase distribution approach; anticipated service size (TBD — preliminary estimate by Electrical Engineer); panel location rationale.
- Lighting approach: High-bay LED in main shop and wash bay; 8' LED in ancillary rooms; service pit lighting provision.
- Receptacle strategy: Distribution of welding-grade 50A/240V receptacles throughout shop area; general 15A/120V and 20A/120V for shop and office use.
- Equipment circuits: Crane feed approach (ASSUMPTION: dedicated three-phase feeds per crane); specific ampacity circuits for compressor, fire hose pump, pressure washer.
- Low-voltage systems: Conduit/wiring provision for security cameras and 2-way radio antenna.
- Code compliance statement: Preliminary design intent is consistent with Alberta Safety Codes and applicable regulations; full code compliance to be confirmed at final design stage.
- Coordination notes: Outstanding items requiring resolution (crane specs, utility tie-in, mechanical coordination) with plan to resolve before final design.

4.2 Note any deviations from App B (Electrical) conceptual drawing and provide rationale.

### Step 5 — Internal Quality Review

5.1 Verify fixture counts against Specification requirements:
- Main shop: 20 high-bay fixtures (5 × 4) at 150W / 22,000 lm.
- Wash bay: 6 high-bay fixtures (2 × 3).
- Office: 1 × 8' LED.
- Utility Room: 2 × 8' LED.
- Parts/Tool Room: 6 × 8' LED.

5.2 Verify all equipment circuits are represented (40A compressor, 70A fire hose pump, 70A pressure washer, crane feeds, overhead door feeds).

5.3 Verify all receptacle types shown in electrical legend are present in layout (15A/120V, 20A/120V, 20A/240V, 30A/240V, 50A/240V).

5.4 Verify low-voltage items (security camera wiring, antenna wiring) are addressed.

5.5 Verify service entry point and three-phase supply intent are shown.

5.6 Verify all TBD items are explicitly labeled as TBD (not left blank or implied).

5.7 Confirm no values have been invented — all stated values must trace to RFP, App B (Electrical), or be labeled ASSUMPTION with a rationale.

### Step 6 — Interdisciplinary Coordination Review

6.1 Circulate preliminary electrical layout to:
- Architect — confirm panel space allocation, ceiling heights for fixture mounting, overhead door locations.
- Structural Engineer — confirm crane runway locations, slab penetration requirements for conduit.
- Mechanical Engineer — confirm exhaust fan locations and power requirements.

6.2 Record the coordination exchange in an **interdisciplinary coordination log** (D-002) that includes:
- Date of circulation and to whom (discipline, contact name).
- What was circulated (document version, drawing revision).
- Feedback received (comments, conflicts identified, approvals).
- Resolution status for each item (resolved, unresolved, deferred).

6.3 Resolve coordination conflicts before submitting to County.

6.4 **Go/no-go assessment (X-004):** Before proceeding to Step 7, assess whether unresolved coordination conflicts prevent County submission:
- **Go:** All coordination conflicts are resolved, or remaining conflicts are minor and can be documented with a resolution plan without affecting the County's ability to evaluate the design intent.
- **No-go / conditional:** Significant conflicts remain that would materially affect the design (e.g., crane location conflict with structural, panel location conflict with architectural). These must be resolved before submission, or the submission must include explicit caveats and a resolution timeline acceptable to the County.
- Document this assessment in the coordination log.

6.5 Document unresolved coordination items in the design narrative with resolution plan.

### Step 7 — Compile and Submit Preliminary Design Presentation

7.1 Compile the preliminary design presentation package including:
- Preliminary electrical layout drawing(s).
- Electrical legend.
- Design narrative.
- List of outstanding TBD items with resolution plan.

7.2 Submit to County project team for review and approval per RFP §3.3.2 (SOW-0010d).

7.3 Record submission date and County contact.

---

## Verification

| Check | Method |
|---|---|
| All required systems represented | Cross-check layout against Specification requirements R-001 through R-018 |
| Fixture counts correct | Count fixtures on layout per room; compare to Spec R-002 through R-005 |
| Equipment circuits present | Confirm 40A compressor, 70A fire hose pump, 70A pressure washer, crane feeds, door feeds all shown |
| Receptacle types complete | Verify legend and all five receptacle ampacity types are shown |
| Low-voltage systems addressed | Confirm security camera and antenna wiring noted on layout |
| No invented values | Review all numeric values against sources; confirm TBD used for unknowns |
| County submission format acceptable | Confirm with County project manager that format meets their review requirements |

---

## Records

The following records shall result from this procedure:

| Record | Description | File Format (E-002) | Naming Convention (E-002) | Location |
|---|---|---|---|---|
| Preliminary electrical layout drawing | Conceptual electrical floor plan with legend | TBD — confirm with project team (e.g., DWG/PDF) | TBD — e.g., `DEL-004-01_Electrical-Layout_Rev[X].[ext]` | DELIVERABLE_PATH |
| Design narrative | System description and TBD resolution plan | TBD — confirm with project team (e.g., DOCX/PDF) | TBD — e.g., `DEL-004-01_Design-Narrative_Rev[X].[ext]` | DELIVERABLE_PATH |
| Interdisciplinary coordination log | Record of coordination exchanges per Step 6.2 (D-002): dates, recipients, feedback, resolution status | TBD — e.g., spreadsheet or structured log | TBD — e.g., `DEL-004-01_Coordination-Log.[ext]` | DELIVERABLE_PATH or project coordination register |
| County submission record | Date submitted, submitted to whom, submission package contents | TBD | TBD | Project coordination log |
| County approval record | County written approval or approval-with-comments; comments log | TBD | TBD | Project coordination log |
| Outstanding TBD register | Tracked list of TBD items, responsible party, target resolution date | TBD — e.g., spreadsheet | TBD — e.g., `DEL-004-01_TBD-Register.[ext]` | DELIVERABLE_PATH or project coordination register |

**Note (E-002):** File format, naming convention, and storage location are placeholder values. The project team should establish file management conventions before production artifacts are created. The placeholder naming convention `DEL-004-01_[Description]_Rev[X].[ext]` is suggested for consistency but should be confirmed.
