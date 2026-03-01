# Procedure — DEL-001-09 Old North Shop Demolition Plans

---

## Purpose

This procedure describes the steps to **produce** the Old North Shop Demolition Plans drawing set (DEL-001-09). It is directed at the Architect and the design-build project team. It covers the workflow from initial data gathering through IFC drawing issue, including key coordination checkpoints with other disciplines and the Owner.

---

## Prerequisites

### Information Prerequisites

| Item | Source | Status |
|---|---|---|
| RFP and all Appendices (R-01 through R-07) | `_Sources/` | Available |
| Appendix B — Shop conceptual floor plan (R-04) | `_Sources/AB-2026-01424-Appendix B (Shop).pdf` | Available |
| Project Decomposition (SOW-0070, SOW-0071, SOW-0072 scope entries) | `_Decomposition/WDMLRL_Decomposition_Claude.md` | Available |
| Existing as-built drawings of Old North Shop (if available) | Camrose County / Owner records | TBD — request from Owner at project award |
| Field survey / site measurement data for existing renovation areas | Field work | TBD — to be completed after project award and mandatory site visit |
| Hazardous materials assessment (if required) | Third-party assessor | TBD — confirm requirement with AHJ |
| Preliminary design scope confirmation from County | County project manager | TBD — confirmed at preliminary design stage |
| Coordination inputs from Structural Engineer (mezzanine structural elements) | PKG-002 | TBD |
| Coordination inputs from Mechanical / Electrical / Plumbing disciplines (MEP demolition in renovation areas) | PKG-003, PKG-004, PKG-006 | TBD |

### Approval Prerequisites

| Prerequisite | Notes |
|---|---|
| Project award and contract execution (CCDC 14–2013) | Required before design work commences |
| Mandatory site meeting attendance | RFP §3.2 — mandatory site meeting March 3, 2026 (or rescheduled date per addendum) |
| County project manager identification | RFP §3.1 — confirmed at project award |

---

## Steps

### Phase 1 — Project Initiation and Data Gathering

**Step 1.1 — Request existing building documentation from Owner**
Contact the Camrose County project manager to request any available as-built drawings, previous renovation records, or maintenance records for the existing Old North Shop. Document what is received vs. what is unavailable.
- **Output:** Existing building record file (or confirmed absence of records)
- **Source:** ASSUMPTION — standard renovation practice

**Step 1.2 — Conduct field survey of three renovation areas**
Arrange access to the existing Old North Shop. Measure and photograph the following areas:
- Kitchenette area (~250 sq ft per RFP §3.4)
- Mezzanine / 2nd-level coffee room (as labeled on Appendix B / R-04)
- Washroom below mezzanine (as labeled on Appendix B / R-04)

Document existing wall locations, door/window openings, fixture locations, ceiling heights, and any structural elements within the renovation extents.
- **Output:** Field notes, photographs, measured sketch plans
- **Source:** ASSUMPTION — standard practice; mandatory site meeting (RFP §3.2) provides initial site access

**Step 1.3 — Identify and flag hazardous materials risk**
Determine the approximate age of the existing Old North Shop. If the building predates applicable asbestos-abatement regulations (ASSUMPTION: general guidance — confirm date thresholds with AHJ), arrange for a hazardous materials assessment by a qualified assessor before finalizing demolition scope.
- **Output:** Hazardous materials assessment report or documented confirmation that assessment is not required
- **Source:** ASSUMPTION — Alberta OH&S obligations; specific requirements TBD

**Step 1.3a — HOLD POINT: Hazardous Materials Assessment Decision Gate (Enrichment: A-004)**
Before proceeding to Phase 2, confirm that the hazardous materials assessment decision has been resolved. Either: (a) the assessment has been completed and the report is available, or (b) a documented waiver exists confirming that assessment is not required (with rationale and responsible party sign-off). This hold point prevents Phase 2 from starting without the hazmat assessment result, which may affect demolition scope and regulatory compliance. If neither (a) nor (b) is satisfied, the project shall not proceed past Phase 1.
- **Output:** Hazardous materials assessment report OR documented waiver with rationale
- **Source:** Guidance C-004; Alberta OHS obligations (ASSUMPTION); Procedure Step 1.3
- **Gate owner:** Architect / Project Manager

**Step 1.4 — Establish base plan**
Using field survey data (and as-built records if available), produce a base floor plan of the Old North Shop at an appropriate scale, showing the three renovation areas in relation to the overall building footprint (105' x 40' per R-04 / Appendix B). **Note (Enrichment: B-003):** The 105' x 40' dimension from R-04 is a conceptual-plan dimension; actual dimensions may differ from field measurement. Base plan dimensions should be sourced from field survey data (Step 1.2) rather than relying solely on R-04.
- **Output:** Electronic base plan file (CAD or BIM)
- **Source:** R-04 (Appendix B — Shop) for overall dimensions; field survey data (Step 1.2) for verified dimensions

**Step 1.5 — GATE: Field verification sign-off (Enrichment: X-002, F-003)**
Before proceeding to Phase 2, the Architect shall formally confirm that field survey data (Step 1.2) has been incorporated into the base plan (Step 1.4). This sign-off ensures that demolition design is based on verified existing conditions rather than solely on R-04 conceptual plan data. TBD: define minimum field data adequacy criteria (e.g., minimum measurements required for each renovation area, photograph documentation standard, acceptable measurement tolerance). The sign-off shall be documented in the project file per REQ-010.
- **Output:** Documented field verification sign-off
- **Source:** Specification REQ-010; Procedure Steps 1.2 and 1.4
- **Gate condition:** Phase 2 shall not commence until field verification sign-off is documented.
- **Responsible:** Architect

---

### Phase 2 — Preliminary Demolition Design

**Step 2.0a — Consult AHJ regarding code edition and permit requirements (Enrichment: D-001)**
Contact the Authority Having Jurisdiction (AHJ) to confirm: (a) the exact edition of the Alberta Building Code applicable to this project (resolving Specification Standards table TBDs per A-003 and C-001), and (b) permit submission requirements for demolition drawings (supporting REQ-009 permit-readiness). Document the AHJ's responses in writing and update the Specification Standards table accordingly. This step should be completed before finalizing demolition design to ensure code compliance determinations are based on confirmed code editions.
- **Output:** Written AHJ confirmation of applicable code edition(s) and permit requirements
- **Source:** Specification.md Standards table (ABC and NBC entries); Guidance CONF-001; ASSUMPTION — standard pre-design coordination
- **Responsible:** Architect / Project Manager

**Step 2.0b — Establish drawing numbering convention (Enrichment: C-003)**
Establish the drawing numbering convention for the DEL-001-09 drawing set, consistent with PKG-001 drawing set conventions. Update the Specification Documentation section "Drawing Numbering Convention: TBD" entry with the confirmed convention. This should be done before producing preliminary drawings (Step 2.5) to ensure consistent sheet identification from the outset.
- **Output:** Documented drawing numbering convention
- **Source:** Specification.md Documentation section ("Drawing Numbering Convention: TBD — to be established by Architect")
- **Responsible:** Architect

**Step 2.1 — Define demolition extents for each area**
Working from the base plan and the renovation program (informed by SOW-0070, SOW-0071, SOW-0072 and the renovation design intent for DEL-001-10), define the demolition extent for each area:
- Kitchenette: identify all elements within the ~250 sq ft extent to be demolished (walls, fixtures, finishes, mechanical/plumbing rough-ins as applicable)
- Mezzanine: identify all elements to be demolished within the 2nd-level coffee room area
- Washroom: identify all elements to be demolished within the existing washroom

For each element, categorize as: (a) demolish/remove entirely, (b) remove and salvage (if any), or (c) remain.
- **Output:** Annotated demolition scope sketches per area
- **Source:** SOW-0070 (RFP §3.4), SOW-0071 (R-04/Appendix B), SOW-0072 (R-04/Appendix B)

**Step 2.2 — Coordinate with Structural Engineer (mezzanine)**
Share the proposed demolition scope for the mezzanine area with the Structural Engineer (PKG-002) to confirm which elements are structural vs. non-structural. Structural elements within demolition scope must be covered by structural demolition drawings (PKG-002 responsibility). Obtain confirmation that proposed non-structural demolition does not affect structural integrity.
- **Output:** Structural coordination memo or email confirmation
- **Source:** ASSUMPTION — standard multi-discipline coordination

**Step 2.3 — Coordinate with MEP disciplines**
Notify PKG-003 (Mechanical), PKG-004 (Electrical), and PKG-006 (Plumbing) of demolition extents. Confirm which MEP elements within the renovation areas appear on the architectural demolition drawings vs. on MEP-discipline demolition drawings. Agree on a division of scope to avoid gaps or duplication.
- **Output:** MEP coordination memo or agreed scope split document
- **Source:** ASSUMPTION — standard multi-discipline coordination

**Step 2.4 — GATE: Confirm scope interface with DEL-001-10 regarding SOW-0073/0074 (Enrichment: D-002)**
Confirm with the project team and Owner whether demolition associated with the new locker/change room (SOW-0073) and washroom expansion (SOW-0074) is to be shown in DEL-001-09 or DEL-001-10. (See Guidance Conflict Table CONF-002.) **This decision must be documented before proceeding to Step 2.5 (produce preliminary demolition drawings).** If this scope interface decision drifts past Step 2.5, the preliminary design submission may contain incorrect scope boundaries, undermining delivery competence and requiring rework.
- **Output:** Documented decision (with date, parties involved, and rationale)
- **Source:** Guidance.md CONF-002; Decomposition §7
- **Gate condition:** Step 2.5 shall not commence until Step 2.4 decision is documented.

**Step 2.5 — Produce preliminary demolition drawings**
Produce the preliminary demolition plan drawing set, incorporating:
- Demolition floor plan(s) at appropriate scale
- Demolition legend and general notes
- Identification of elements to demolish, elements to remain
- Reference to structural and MEP demolition drawings where applicable
- **Output:** Preliminary drawing set (PDF or equivalent)
- **Source:** ASSUMPTION — standard drawing production

**Step 2.6 — Submit preliminary design for County approval**
Submit the preliminary demolition drawings to the County project manager for review and approval per RFP §3.3.2. Record the submission date and await written approval.
- **Output:** Submission record; County written approval
- **Source:** RFP §3.3.2

---

### Phase 3 — IFC Drawing Production

**Step 3.1 — Incorporate County review comments**
Address all County comments from the preliminary design review. Document each comment and the response/resolution.
- **Output:** Comment-response log; revised drawings
- **Source:** RFP §3.3.2 (County approval obligation)

**Step 3.2 — Complete final demolition drawings**
Produce the IFC demolition drawing set, with all elements confirmed, legends complete, drawing titles, revision blocks, and stamp fields populated.
- **Output:** IFC drawing set (pre-stamp)
- **Source:** ASSUMPTION — standard practice; RFP §3.3.2

**Step 3.3 — Conduct internal Architect review**
Perform a final internal check of the drawings against:
- REQ-001: all three renovation areas addressed
- REQ-002: existing conditions documented (per X-004 strengthened verification method)
- REQ-003: demolition extent clearly delineated
- REQ-004: coordination with DEL-001-10 confirmed
- REQ-005: P.Eng. stamp arrangement confirmed (CONF-001 resolved)
- REQ-006: code compliance review documented (per F-001 strengthened verification method)
- REQ-008: kitchenette area corresponds to ~250 sq ft
- REQ-009: permit-readiness confirmed
- REQ-010: field verification sign-off on file
- REQ-011: revision control present on all sheets
- REQ-012: all required records created
- Overall drawing quality standard check (per A-005, criteria TBD)
- **Output:** Internal review sign-off (feeds into Step 3.3a acceptance gate)
- **Source:** Specification.md Requirements and Verification table

**Step 3.3a — GATE: Formal acceptance decision for IFC release (Enrichment: E-003)**
Following completion of the internal Architect review (Step 3.3), conduct a formal go/no-go acceptance decision for IFC issue. All verification checks in Step 3.3 must pass (no unresolved findings) before the drawing set is approved for P.Eng. stamping. The acceptance decision shall be documented with: (a) confirmation that all verification checks passed, (b) identification of the decision-maker(s), and (c) date of acceptance. If any verification check has an unresolved finding, document the finding, assign corrective action, and repeat Step 3.3 after resolution.
- **Output:** Formal acceptance record (go/no-go) with verification check results
- **Source:** Specification.md Verification table; Procedure Step 3.3
- **Gate condition:** Step 3.4 shall not commence until Step 3.3a acceptance is documented as "go."
- **Responsible:** Architect / Project Manager

**Step 3.4 — Obtain P.Eng. stamp**
Submit the completed drawing set to the designated P.Eng. for review and stamping per RFP §3.3.2. (See Guidance CONF-001 regarding whether Architect's seal alone is sufficient — confirm with AHJ before this step.)
- **Output:** Stamped IFC drawing set
- **Source:** RFP §3.3.2

**Step 3.5 — Issue IFC drawings**
Formally issue the stamped IFC demolition drawing set to the project team, including:
- General Contractor (PKG-017 construction team)
- Project Manager (for permit applications — DEL-009-02)
- County project manager

**Transmittal record requirements (Enrichment: E-004):** The transmittal record shall document: (a) drawing sheet numbers and revision levels issued, (b) date of issue, (c) recipient list, (d) method of delivery, and (e) confirmation of receipt (where practicable). TBD — identify whether the project uses a standard transmittal template (e.g., CCDC or firm-standard form) and cite it here. Without a defined standard, transmittal records may be inconsistent and difficult to audit.
- **Output:** Issued drawing set with transmittal record per standard identified above
- **Source:** ASSUMPTION — standard IFC issue procedure. **Proposed authority:** Project Manager.

---

## Verification

| Check | Method | Responsible |
|---|---|---|
| All three renovation areas addressed in drawings | Sheet-by-sheet review | Architect |
| Field survey data incorporated (REQ-010) | Compare drawings to field notes; confirm field verification sign-off (Step 1.5) documented | Architect |
| Hazardous materials assessment gate passed (Step 1.3a) | Confirm assessment report or documented waiver on file | Architect / Project Manager |
| Demolition vs. remain designation complete for all elements | Drawing review | Architect |
| Coordination with DEL-001-10 confirmed (no conflicts) | Cross-reference check | Architect |
| SOW-0073/0074 scope interface decision documented (Step 2.4) | Confirm decision record on file before preliminary design submission | Architect / Project Manager |
| AHJ code edition and permit requirements confirmed (Step 2.0a) | Confirm written AHJ response on file | Architect / Project Manager |
| Drawing numbering convention established (Step 2.0b) | Confirm convention documented and applied to drawing sheets | Architect |
| Structural coordination confirmed for mezzanine elements | Review coordination memo from PKG-002 | Architect / Structural Engineer |
| MEP demolition scope agreed | Review coordination memo from PKG-003/004/006 | Architect |
| Formal acceptance decision documented (Step 3.3a) | Confirm go/no-go record with verification check results | Architect / Project Manager |
| P.Eng. stamp present | Visual check on issued drawings | Project Manager |
| County preliminary design approval obtained | Review County approval letter/email | Project Manager |
| Drawing revision history current (REQ-011) | Title block review — confirm revision block populated on each sheet | Architect |
| Transmittal record complete (Step 3.5) | Confirm transmittal record meets documented standard | Project Manager |
| All required records created (REQ-012) | Audit project files against Records table below | Project Manager |

---

## Records

| Record | Description | Retained By |
|---|---|---|
| Field survey notes and photographs | Documentation of existing conditions for each renovation area | Architect's project file |
| As-built records received from Owner (or confirmed absence) | Owner-provided building documentation | Architect's project file |
| Hazardous materials assessment (if conducted) | Third-party assessment report | Project Manager / Architect |
| Preliminary design submission and County approval | Submission transmittal + County written approval | Project Manager |
| Structural coordination memo (mezzanine) | Written confirmation from Structural Engineer | Architect's project file |
| MEP scope split agreement | Written confirmation from MEP discipline leads | Architect's project file |
| CONF-002 decision record | Documented decision on SOW-0073/0074 demolition scope | Project Manager |
| Comment-response log | Record of County review comments and resolutions | Architect / Project Manager |
| AHJ code edition and permit requirements confirmation | Written response from AHJ confirming applicable codes and permit submission requirements (Step 2.0a) | Architect / Project Manager |
| Drawing numbering convention record | Documented convention established per Step 2.0b | Architect |
| Field verification sign-off | Documented confirmation that field data has been incorporated into base plan (Step 1.5) | Architect |
| Formal IFC acceptance record | Go/no-go decision with verification check results (Step 3.3a) | Architect / Project Manager |
| Issued IFC drawing set with transmittal | Final issued drawings and distribution record, with transmittal meeting documented standard (Step 3.5) | Project Manager |
