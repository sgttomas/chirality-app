# Procedure — DEL-003-05 Mechanical Equipment Schedule
**Deliverable ID:** DEL-003-05
**Name:** Mechanical Equipment Schedule
**Package:** PKG-003 Mechanical Design
**Discipline:** Mechanical Engineering
**Revision:** R1 (Pass 3 enrichment — 2026-02-26)
**Date:** 2026-02-25

---

## 1. Purpose

This Procedure describes the steps required to **produce** the Mechanical Equipment Schedule (DEL-003-05) — from initial engineering inputs through IFC issue. It is intended for use by the Mechanical Engineer of record and the Design-Build project manager.

The schedule is a design artifact, not an operational document; this procedure governs its production workflow and quality control, not equipment operation.

---

## 2. Prerequisites

### 2.1 Required Upstream Inputs

| Input | Source | Required Before | Status |
|---|---|---|---|
| County-approved Preliminary Mechanical Design (DEL-003-01) | Mechanical Engineer + County approval | Equipment selections committed | TBD (requires DEL-003-01 completion and County sign-off) |
| Mechanical Calculation Package (DEL-003-06) | Mechanical Engineer | Performance values entered in schedule | TBD (calculations precede schedule finalization) |
| Geotechnical Report (DEL-008-01) | Geotechnical Engineer | Heating load calculations (ground conditions affect slab heating if applicable) | TBD (post-geotech, SOW-0001) |
| Structural Design inputs (PKG-002) | Structural Engineer | Fan and unit mounting loads confirmed; crane girder layout for ceiling fan coordination | TBD — coordination required |
| Electrical Design inputs (PKG-004) | Electrical Engineer | Electrical characteristics confirmed for each equipment item (phase, voltage, FLA) | TBD — coordination required |
| County welding equipment specifications (SOW-0204) | Camrose County | Welding exhaust system (EXH-003) sizing | TBD — County-supplied, timing unknown |
| RFP and all Addenda | Camrose County | Design start | Available (R-01, R-02) |
| Conceptual drawings (App B) | Camrose County | Equipment location planning | Available (R-04) |

### 2.2 Required References

| Reference | Use |
|---|---|
| RFP §3.4 (Design Requirements) | Equipment scope confirmation |
| App B (Shop) Conceptual Drawing | Equipment location context |
| Alberta Building Code (edition TBD) | Code compliance for equipment |
| ASHRAE 62.1 (edition TBD) | Ventilation rate calculations |
| ASHRAE 90.1 or Alberta energy code (edition TBD) | Equipment efficiency minimums |
| NFPA 91 (ASSUMPTION: applicable) | Exhaust system design |
| ACGIH Industrial Ventilation Manual (ASSUMPTION: applicable) | Welding and equipment exhaust design |
| CSA B149.1 (ASSUMPTION: applicable) | Gas-fired equipment connections |

> **Note:** All standard editions are TBD and must be confirmed by the Mechanical Engineer at design start (see Specification REQ-013 and Guidance §6 Applicable Standards Reference). See also semantic lensing item A-002.

### 2.3 Required Personnel

| Role | Responsibility |
|---|---|
| Mechanical Engineer of Record (P.Eng., Alberta) | Performs calculations, selects equipment, stamps IFC schedule |
| Project Manager (Design-Build) | Coordinates preliminary design County approval; manages schedule vs. project timeline |
| Structural Engineer | Confirms mounting loads for fans and units; provides crane girder layout for fan coordination (coordination) |
| Electrical Engineer | Confirms electrical characteristics and panel loads (coordination) |
| County Project Manager | Reviews and approves preliminary design (DEL-003-01) |

---

## 3. Steps

### Phase 1 — Scoping and Basis of Design

**Step 1.1 — Confirm Equipment Scope from RFP**
Review RFP §3.4 and Appendix B (Shop) to confirm all mechanical equipment categories required. Cross-reference against decomposition items SOW-0035 through SOW-0040. Identify any scope gaps (e.g., service pit ventilation, wash bay ventilation — see Guidance §3.6 and §3.7 and Conflict Table CON-002, CON-003).
- Deliverable: Equipment scope list with SOW references confirmed.

**Step 1.1a — Resolve Wash Bay Ventilation Scope (Pass 3 enrichment, A-004)**
Based on the scope review in Step 1.1, determine whether the wash bay requires dedicated ventilation/exhaust equipment or is adequately served by the main shop systems (AEX-001, MAU-001). Guidance §3.7 identifies this as a scope ambiguity. The resolution should be:
1. Assess wash bay ventilation load (moisture, cleaning chemicals, drainage odors) against main system capacity
2. Determine if a dedicated exhaust fan is required; if so, assign a tag and add to the equipment scope list
3. Document the decision and rationale in DEL-003-06 (Mechanical Calculation Package)
- Deliverable: Wash bay ventilation scope decision documented.
- Source: Guidance §3.7; Conflict Table CON-003; semantic lensing item A-004.

**Step 1.2 — Obtain County Welding Equipment Specifications**
Coordinate with Camrose County project manager to obtain welding equipment specifications (SOW-0204) needed for welding exhaust system sizing. If not available at preliminary design stage, document the assumption used (see Guidance §3.4, Conflict Table CON-004) and flag for resolution before IFC.
- Deliverable: Welding spec received and filed, or formal assumption documented.

**Step 1.3 — Establish Tag Convention**
Establish and document the equipment tag numbering convention for the project (see Specification REQ-002). Coordinate with the broader mechanical drawing set to ensure tags used in the schedule match tags on the drawings (DEL-003-02, DEL-003-03, DEL-003-04). **Note (Pass 3, F-002):** The tag convention must be confirmed and documented before schedule population begins; do not proceed with an assumed convention.
- Deliverable: Tag convention documented and shared with drawing team.

**Step 1.4 — Clarify "High-Recovery Heating System" Interpretation**
Determine what technology satisfies the RFP requirement for a "high-recovery heating system" (SOW-0035). Document the interpretation and rationale in the Calculation Package (DEL-003-06). Raise for County confirmation at preliminary design review. See Conflict Table CON-001 and Guidance §2.5.
- Deliverable: Engineering decision documented in DEL-003-06; position confirmed at preliminary design review.

**Step 1.5 — Confirm Standard Editions (Pass 3 enrichment, A-002)**
Before commencing design calculations, confirm the applicable editions of all governing standards (Alberta Building Code, ASHRAE 62.1, ASHRAE 90.1, NFPA 91, CSA B149.1, ACGIH Industrial Ventilation Manual). Record the confirmed editions in the project record and update the Standards table in Specification.md §3.
- Deliverable: List of confirmed standard editions filed in project record.
- Source: Specification REQ-013; semantic lensing item A-002.

### Phase 2 — Preliminary Equipment Schedule

**Step 2.1 — Develop Preliminary Equipment List**
Based on the scope confirmed in Step 1.1 and building layout from App B (Shop), develop a preliminary list of all equipment items with preliminary tags and candidate equipment categories. Do not commit to specific models or performance values at this stage.
- Deliverable: Preliminary equipment list (internal working document).

**Step 2.2 — Perform Mechanical Calculations (DEL-003-06)**
The Mechanical Engineer performs heating, cooling (if applicable), ventilation, and exhaust calculations per applicable standards (ASHRAE 62.1, ASHRAE 90.1, NFPA 91 as applicable). Calculations establish:
- Required heating output for HTG-001
- Required airflow for AEX-001, MAU-001
- Required exhaust flow and fan static pressure for EXH-001/002/003
- Confirmation of service pit and wash bay ventilation approach (see Conflict Table CON-002, CON-003)
- Fan sizing for CF-001 through CF-006
- Indoor design temperature confirmation (see Guidance §3.8 and Conflict Table CON-006)
- Source: This step is the responsibility of DEL-003-06, not DEL-003-05. The schedule cannot be finalized without calculation results.

**Step 2.3 — Select Equipment**
Based on calculation results (Step 2.2), the Mechanical Engineer selects equipment manufacturers and models (or establishes a performance specification basis if competitive tendering of equipment is desired). Consider:
- Alberta product availability and service network
- Lead times relative to December 31, 2026 project completion deadline (RFP §3.1, SOW-0091) — see Guidance §4.1 for long-lead procurement decision framework
- Energy efficiency compliance (ASHRAE 90.1 or Alberta equivalent)
- Three-phase power compatibility (RFP §3.4)
- Natural gas compatibility for heating/MUA (SOW-0080, CSA B149.1 ASSUMPTION)
- Equipment weight, vibration characteristics, and acoustical data (for structural coordination and occupant comfort — see Specification REQ-003)
- Deliverable: Equipment selection with manufacturer/model or performance basis documented.

**Step 2.4 — Populate Preliminary Schedule Table**
Populate the schedule table with all required fields per Specification REQ-003:
- Equipment tag, description, quantity, service area, performance parameters, connection requirements (including electrical characteristics — phase/voltage/FLA), equipment weight, vibration data, acoustical data, basis of design notes
- Mark all fields not yet confirmed as TBD
- Deliverable: Preliminary schedule table (internal working document).

**Step 2.5 — Include in Preliminary Mechanical Design Submission (DEL-003-01)**
The preliminary equipment schedule (or equipment list) shall be included as part of the Preliminary Mechanical Design submission to the County for approval (SOW-0010c; RFP §3.3.2).
- Deliverable: Preliminary design submitted to County with equipment list/schedule.

**Step 2.6 — County Review and Approval**
The County reviews the preliminary design. The Mechanical Engineer responds to any County comments on equipment selection or scope. County approval is required before IFC stage. **Note:** If County approval is delayed or conditional, see Guidance §2.4 for schedule impact assessment. Track County approval as a critical path milestone.
- Deliverable: Written County approval of preliminary mechanical design (DEL-003-01).
- Source: RFP §3.3.2, SOW-0010c.

**Step 2.7 — Quality Gate: Preliminary-to-IFC Baseline Confirmation (Pass 3 enrichment, D-003)**
Before proceeding to Phase 3, confirm that the County-approved equipment selections from the preliminary design form the baseline for the IFC schedule. Document the approved baseline as a hold point:
1. Record the list of County-approved equipment selections with key parameters
2. Identify any changes from the preliminary submission that occurred during County review
3. Confirm that the approved baseline is the starting point for IFC finalization
This hold point ensures that subsequent IFC work does not inadvertently deviate from the County-approved design without triggering the change management process (Specification REQ-016).
- Deliverable: Baseline confirmation record (brief memo or checklist).
- Source: Specification REQ-012, REQ-016; Guidance §2.4; semantic lensing item D-003.

### Phase 3 — IFC Equipment Schedule

**Step 3.1 — Incorporate County Feedback**
Update the equipment schedule based on any County direction received during preliminary design review. Update the basis-of-design notes as required. **If equipment selections change materially from the County-approved baseline (Step 2.7), document the deviation and notify the County per Specification REQ-016 and Conflict Table CON-005.**

**Step 3.2 — Coordinate with Structural and Electrical Engineers**
Provide the following coordination data to downstream engineers:

**To Structural Engineer (PKG-002):**
- Equipment weights and mounting requirements for all ceiling/roof-mounted units (HTG-001, AEX-001, MAU-001, CF-001-006)
- Vibration characteristics for rotating equipment
- Proposed ceiling fan locations (coordinated with crane girder layout per Guidance §3.5)

**To Electrical Engineer (PKG-004):**
- Electrical load data per equipment item: phase, voltage, FLA/RLA, motor power
- Equipment locations for circuit routing

Resolve any conflicts arising from coordination.
- Deliverable: Confirmed coordination records documenting at minimum: (a) confirmed equipment weights and mounting loads, (b) agreed electrical characteristics per equipment item, (c) confirmed fan locations relative to crane layout, and (d) identification of any unresolved conflicts. Records shall be filed as email, meeting minutes, or coordination log entries per project QC protocol.
- Source: Procedure Step 3.2 (original); semantic lensing items D-002 and X-002.
- **Note (Pass 3, D-002):** Minimum coordination record content specified per semantic lensing; "email or meeting minutes" alone was insufficient to ensure adequate evidence of coordination.

**Step 3.3 — Finalize Performance Values**
Confirm all TBD performance values are resolved and documented in the Calculation Package (DEL-003-06). The IFC schedule shall not contain TBD values in required performance fields (Specification REQ-017).
- Deliverable: All required schedule fields populated with confirmed values.

**Step 3.4 — Apply Drawing Cross-References**
Add the drawing sheet cross-reference column to the schedule, linking each equipment tag to the drawing sheet(s) where it appears (HVAC plans, ductwork plans, exhaust plans). **Verify bidirectional completeness:** confirm that all schedule tags appear on referenced drawings AND all equipment tags on drawings appear in the schedule (Specification REQ-015).
- Deliverable: Drawing cross-reference column populated; bidirectional reconciliation confirmed.

**Step 3.5 — QC Review**
A qualified reviewer performs a QC review of the schedule. **The reviewer shall be independent of the preparer** — either a qualified peer reviewer (P.Eng. or equivalent) or the design team lead, not the same individual who prepared the schedule. If the project team size does not permit independent review, the Mechanical Engineer of Record may perform self-review, but this shall be documented in the QC checklist with a notation that independent review was not available.

QC review shall verify:
- All required equipment categories present (check against SOW-0035-SOW-0040 and SOW-0028)
- Tags consistent with drawings (bidirectional per REQ-015)
- Performance values consistent with calculations (DEL-003-06) and mechanical specification (DEL-003-07)
- Electrical data consistent with Electrical Engineer's inputs
- Equipment weight and vibration data present for structural coordination items
- No TBD values in required fields (per REQ-017)
- All changes from County-approved baseline identified and documented (per REQ-016)
- Source: RFP §3.3.2; standard engineering QC. **Note (Pass 3, X-005):** Reviewer independence requirement clarified per semantic lensing.

**QC Review Checklist Minimum Content (Pass 3 enrichment, E-004):**
The QC review checklist referenced in Records §5 (row 7) shall include at minimum the following check items:

| Check # | Check Item | Pass/Fail | Notes |
|---|---|---|---|
| QC-01 | All SOW-0035-0040 and SOW-0028 equipment categories have assigned tags | | |
| QC-02 | Equipment tags are unique and follow documented convention (REQ-002) | | |
| QC-03 | All REQ-003 minimum data fields populated — no TBD in required fields | | |
| QC-04 | Performance values traceable to DEL-003-06 calculations | | |
| QC-05 | Electrical data consistent with PKG-004 coordination records | | |
| QC-06 | Equipment weights consistent with PKG-002 coordination records | | |
| QC-07 | Drawing cross-references complete — bidirectional reconciliation confirmed | | |
| QC-08 | No material deviations from County-approved baseline without documentation | | |
| QC-09 | Code compliance items addressed per REQ-013 (editions confirmed) | | |
| QC-10 | Service pit and wash bay ventilation approach confirmed and documented | | |
| QC-11 | Reviewer signature and date | | |

> This template may be expanded by the Mechanical Engineer. Source: Procedure Step 3.5; Records §5 (QC review checklist row); semantic lensing item E-004.

**Step 3.6 — P.Eng. Stamp and Sign**
The Mechanical Engineer of Record stamps and signs the finalized schedule as part of the IFC drawing set.
- Source: RFP §3.3.2; SOW-0018.

**Step 3.7 — Issue for Construction**
Issue the IFC schedule as part of the mechanical IFC drawing set. Distribute to:
- County project manager (RFP §3.3.2)
- Mechanical contractor (PKG-013)
- Electrical contractor (for electrical coordination — PKG-015)
- Project manager (for commissioning reference — DEL-020-01)

---

## 4. Verification

| Check | Method | Responsibility |
|---|---|---|
| All SOW-0035-0040 and SOW-0028 equipment categories present | Cross-check schedule tags against SOW list | Mechanical Engineer |
| Tags consistent with HVAC/exhaust plans | Bidirectional drawing review — tags on plans match schedule AND schedule tags appear on plans | Mechanical Engineer / Drafting lead |
| Performance values supported by DEL-003-06 | Calculation review — key values traceable to calc sheets | Mechanical Engineer |
| Electrical data consistent with PKG-004 | Coordination review with Electrical Engineer | Mechanical Engineer + Electrical Engineer |
| Equipment weight and vibration data consistent with PKG-002 coordination | Coordination review with Structural Engineer | Mechanical Engineer + Structural Engineer |
| IFC stamp applied | Document review | Project Manager |
| County preliminary approval obtained before IFC issue | Approval record on file | Project Manager |
| No material changes from County-approved baseline without documentation | Baseline comparison review (Step 2.7 vs. IFC) | Mechanical Engineer + Project Manager |
| Service pit and wash bay ventilation coverage confirmed | Design review / calculation | Mechanical Engineer |
| Welding exhaust design basis confirmed (or assumption documented) | Design review / County coordination | Mechanical Engineer + Project Manager |
| No TBD values in required performance fields at IFC | Document review (REQ-017) | Mechanical Engineer / QC Reviewer |
| QC review completed by independent reviewer (or self-review documented) | QC checklist on file | Project Manager |

---

## 5. Records

The following records shall result from or accompany the production of this deliverable:

| Record | Description | Filed By | Timing |
|---|---|---|---|
| Preliminary equipment list | Working document from Step 2.1 | Mechanical Engineer | Phase 2 |
| Calculation Package (DEL-003-06) | Supporting calculations for all performance values | Mechanical Engineer | Before IFC |
| County approval record for DEL-003-01 | Written County approval of preliminary design | Project Manager | Before IFC |
| Preliminary-to-IFC baseline confirmation | Baseline record from Step 2.7 confirming County-approved selections | Mechanical Engineer | After County approval, before Phase 3 |
| Coordination records with Structural and Electrical | Records documenting confirmed weights, electrical data, fan locations, and unresolved conflicts (Step 3.2 minimum content) | Project Manager | Phase 3 |
| County welding equipment specifications | Document received from County | Project Manager | Before IFC (EXH-003 design) |
| Confirmed standard editions | List of applicable code/standard editions from Step 1.5 | Mechanical Engineer | Phase 1 |
| IFC Mechanical Equipment Schedule (this deliverable) | Final stamped schedule | Mechanical Engineer | IFC issue |
| QC review checklist | Completed QC checklist from Step 3.5 (minimum content per E-004 template) | Mechanical Engineer / QC Reviewer | IFC issue |
| Long-lead equipment procurement records (if applicable) | Purchase orders for equipment with extended lead times | Project Manager / Procurement | As required, before construction |

---

## Notes

- All steps labeled TBD reference inputs or decisions that were not available in the accessible sources at the time this scaffold was generated.
- The Mechanical Engineer of record is the primary authority for all engineering judgments, equipment selections, and performance values. This procedure is a scaffold for that engineer's workflow, not a substitute for engineering judgment.
- Coordination with PKG-013 (Mechanical & HVAC Installation) should begin early to confirm that selected equipment is available from Alberta-based suppliers within the project timeline.
- Source for December 31, 2026 deadline: RFP §3.1, SOW-0091.
