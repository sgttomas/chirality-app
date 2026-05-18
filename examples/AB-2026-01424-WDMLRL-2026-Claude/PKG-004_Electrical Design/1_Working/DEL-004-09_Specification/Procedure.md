# Procedure: DEL-004-09 Electrical Specification

---

## Purpose

This procedure describes the steps to produce the Electrical Specification (DEL-004-09) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It is intended for the Electrical Engineer responsible for PKG-004 Electrical Design.

The Electrical Specification is a written design document — not a field installation procedure. It governs what the electrical design must achieve and complements the PKG-004 drawing deliverables (DEL-004-02 through DEL-004-07).

---

## Prerequisites

### Required Inputs — Design

The following must be available or in progress before the Electrical Specification can be finalized:

| Input | Source | Status |
|---|---|---|
| RFP §3.4 Design Requirements (electrical content) | R-01 — AB-2026-01424-WDMLRL RFP.pdf | Available |
| Appendix B (Electrical) conceptual drawing | R-05 — AB-2026-01424-Appendix B (Electrical).pdf | Available |
| Project Decomposition (SOW, deliverable structure) | WDMLRL_Decomposition_Claude.md | Available |
| County preliminary design approval (DEL-004-01) | County project team | Required before IFC |
| Crane equipment specifications (make, model, kW rating) | Supplier / project team | TBD — needed for REQ-010 |
| Security camera system specification | Owner / IT advisor | TBD — needed for REQ-016 |
| 2-way radio antenna system specification | Owner | TBD — needed for REQ-017 |
| Mechanical/HVAC equipment electrical data (exhaust fans, MUA unit, ceiling fans) | Mechanical Engineer (PKG-003) | TBD — needed for REQ-007, REQ-015 |
| Utility confirmation of three-phase service availability at site | Electrical utility | TBD — **DESIGN-BLOCKING INPUT**: needed for REQ-001, REQ-002, REQ-022; service voltage and capacity cannot be designed without this confirmation (see HOLD-05) *(Lensing ref: B-004)* |

### Prerequisite Status Tracking *(Lensing ref: F-003)*

The following table tracks the resolution status of TBD prerequisite inputs. Each TBD input must be resolved (or explicitly deferred with documented rationale) before the corresponding procedure step can be finalized. The Electrical Engineer shall update the Status column as inputs are received.

| Prerequisite Input | Needed For | Status | Date Resolved | Resolution Notes |
|---|---|---|---|---|
| Crane equipment specifications | REQ-010 (Step 4.4, Step 5.5) | TBD | — | — |
| Security camera system specification | REQ-016 (Step 4.3) | TBD | — | — |
| 2-way radio antenna system specification | REQ-017 (Step 4.3) | TBD | — | — |
| Mechanical/HVAC equipment electrical data | REQ-007, REQ-015 (Step 4.1) | TBD | — | — |
| Utility confirmation of three-phase service | REQ-001, REQ-002, REQ-022 (Step 3.1) | TBD | — | — |
| County preliminary design approval (DEL-004-01) | Step 7 (gate before IFC) | TBD | — | — |
| Governing code editions (CEC, Safety Codes) | REQ-019, REQ-021–REQ-027, Standards table (Step 1) | TBD | — | — |

### Required Inputs — Regulatory / Standards

| Input | Notes |
|---|---|
| Current Alberta Safety Codes (Electrical) and adopted CEC edition | Electrical Engineer to confirm current edition in force |
| Alberta Electrical Utility Code | Applicable for service connection design |
| Safety Code permit application requirements | Obtained via PKG-009 permitting process |

### Required References

| Ref | Document |
|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf (§1.0, §3.1, §3.3.2, §3.4) |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf |

---

## Steps

### Step 1: Confirm Scope and Deliverable Boundaries
1.1 Review `_CONTEXT.md` and the Decomposition entry for DEL-004-09 to confirm deliverable ID, package, and SOW coverage (SOW-0014).
1.2 Confirm which drawing deliverables (DEL-004-02 through DEL-004-07) are being produced concurrently; establish cross-reference between specification sections and drawing deliverable IDs.
1.3 Confirm scope boundary: this specification covers the new Addition only unless the Owner directs electrical design for the Old North Shop renovation areas.

### Step 2: Extract and Tabulate All Electrical Requirements from Sources
2.1 Extract all explicit electrical requirements from RFP §3.4 (three-phase power, crane power, welding receptacles, equipment listed).
2.2 Extract all elements from App B (Electrical) drawing: fixture counts, circuit types, dedicated loads, low-voltage notes.
2.3 Cross-reference with Decomp SOW items (SOW-0051 through SOW-0066, SOW-0081, SOW-0082) to ensure all scope items are captured.
2.4 Flag any items where specification data is missing (e.g., wash bay light wattage, crane circuit rating, fan motor rating) and mark as TBD pending inputs from prerequisites.

### Step 3: Confirm Utility and Service Requirements
3.1 Contact the electrical utility to confirm three-phase service availability at site boundary (SW 14–44–21–W4).
3.2 Determine service voltage level (ASSUMPTION: 480Y/277V or 208Y/120V three-phase — TBD; confirm with utility).
3.3 Document utility requirements for service entry, metering, and any required utility-side upgrades.
3.4 Obtain preliminary load estimate to confirm service capacity.

### Step 4: Coordinate with Other Disciplines

**Interdisciplinary Hold Points** *(Lensing ref: A-004)*

The following hold points define gates that prevent advancement of the electrical design past the indicated step without confirmed inputs. The Electrical Engineer shall not finalize the associated design elements until the hold is released.

| Hold ID | Input Required | Responsible Party | Release Condition | Blocks Steps |
|---|---|---|---|---|
| HOLD-01 | Mechanical equipment electrical data (exhaust fans, MUA unit, ceiling fans) | Mechanical Engineer (PKG-003) | Written data sheet or email confirmation received | Step 5 (load schedule), Step 6 (REQ-007, REQ-015) |
| HOLD-02 | Crane electrical specifications (kW, voltage, FLA) | Crane supplier / Project team | Crane data sheet received | Step 5.5, Step 6 (REQ-010) |
| HOLD-03 | Security camera system specification | Owner / IT advisor | Written specification received | Step 6 (REQ-016), DEL-004-07 |
| HOLD-04 | 2-way radio antenna specification | Owner | Written specification received | Step 6 (REQ-017), DEL-004-07 |
| HOLD-05 | Utility three-phase service confirmation | Electrical utility | Utility confirmation letter or email | Step 3.2, Step 5.2, Step 6 (REQ-001, REQ-022) |

4.1 **Mechanical Engineer (PKG-003):** Obtain electrical load data for makeup air unit, exhaust fans (including welding station exhaust), and any other mechanically-driven equipment requiring electrical circuits. **(HOLD-01)**
4.2 **Structural Engineer (PKG-002):** Confirm routing constraints for electrical conduit in concrete structure (35' ceiling height); confirm embedded conduit requirements if any.
4.3 **Owner:** Obtain security camera system specification and 2-way radio antenna specification (Conflict Table CONF-004-09-02, CONF-004-09-03). **(HOLD-03, HOLD-04)**
4.4 **Crane supplier / project team:** Obtain 5-tonne crane electrical data (kW, voltage, full-load current) for crane circuit design (REQ-010). **(HOLD-02)**

### Step 5: Develop Electrical Design and Calculations
5.1 Produce load schedule from tabulated requirements (Step 2) and discipline coordination inputs (Step 4).
5.2 Size service entrance, main disconnect, and panelboard(s) based on calculated demand.
5.3 Design branch circuits per CEC requirements: wire sizing, conduit fill, circuit protection, voltage drop.
5.4 Perform lighting calculation for main shop (confirm 150 W / 22,000 lm high bay fixtures achieve required illumination levels) and other spaces.
5.5 Design crane runway conductors and disconnects per CEC and crane manufacturer requirements.
5.6 Size dedicated equipment circuits (40 A compressor, 70 A fire hose pump, 70 A pressure washer) per REQ-012 through REQ-014.
5.7 Document all calculations in the Electrical Calculation Package (DEL-004-08).

### Step 6: Draft the Specification Document (DEL-004-09)
6.1 Using this document as the working draft, confirm all TBD items from Step 2 are either resolved (update with confirmed values and source citations) or remain as TBD with explanation.
6.2 Verify each requirement (REQ-001 through REQ-027) is supported by a cited source or labeled ASSUMPTION.
6.3 Confirm that the Verification column in the Requirements section correctly references the drawing deliverable(s) that demonstrate compliance.
6.4 Add any requirements identified during design (Steps 3–5) that are not already in the draft specification.
6.5 Update the Conflict Table in Guidance.md with any new unresolved conflicts identified during design coordination.

### Step 7: Submit Preliminary Design for County Approval
7.1 Compile DEL-004-01 (Preliminary Electrical Design) from the draft drawing set.
7.2 Submit to County project team for review and approval per RFP §3.3.2 and Decomp SOW-0010d.
7.3 Receive written approval from County before proceeding to IFC.
7.4 Incorporate any County direction into the specification and drawings.

### Step 8: Finalize IFC Drawings and Specification
8.1 Finalize all drawing deliverables (DEL-004-02 through DEL-004-07) to IFC standard.
8.2 Update this specification (DEL-004-09) to reflect any changes made during County review (Step 7).
8.3 Ensure cross-document consistency: terminology, circuit ratings, and fixture counts must be identical between this specification and the drawing deliverables.
8.4 Obtain P.Eng. review and signature/stamp on all IFC drawings per REQ-018 (RFP §3.3.2).

### Step 9: Submit for Safety Code Permit
9.1 Coordinate with the permitting team (PKG-009) to submit the electrical design for Safety Code permit review.
9.2 Provide any supplemental information requested by the Safety Code Authority.
9.3 Obtain electrical Safety Code permit prior to construction commencement.

---

## Verification

The following checks shall be performed before the Electrical Specification is considered complete and ready for IFC issue:

| Check | What to Verify | Pass Condition |
|---|---|---|
| Completeness — requirement coverage | All SOW-0014 sub-items and App B notes have corresponding requirements (REQ-001 through REQ-027 at minimum) | No App B item or RFP §3.4 electrical item is unaddressed |
| TBD items logged | All TBDs are explicitly noted with reason and prerequisite | No unmarked gaps |
| Cross-document consistency | Fixture counts, circuit ratings, and system names match across Specification, Datasheet, Guidance, and drawing deliverables | No discrepancies |
| Source citations | Each requirement cites a source (RFP §, App B, Decomp SOW) or is labeled ASSUMPTION | All requirements traceable |
| Conflict Table | Unresolved items are in the Guidance.md Conflict Table | No silent gaps |
| Interdisciplinary coordination | All Step 4 hold-point inputs received and documented (HOLD-01 through HOLD-05); coordination records on file *(Lensing ref: X-005)* | All hold points released or explicitly deferred with documented rationale |
| P.Eng. stamp | All IFC drawings stamped by Alberta-licensed P.Eng. | Stamp and signature on all sheets |
| Safety Code permit | Permit obtained or in process before construction | Permit document on file |
| County approval | Written County approval of preliminary design documented | Approval record in project file |

---

## Records

The following records shall result from this procedure:

| Record | Type | Custodian |
|---|---|---|
| DEL-004-09 Electrical Specification (this document, final IFC version) | Design document | Electrical Engineer / Project records |
| DEL-004-08 Electrical Calculation Package | Calculation package | Electrical Engineer |
| Utility coordination correspondence | Correspondence | Electrical Engineer / Project Manager |
| County preliminary design approval | Written approval | Project Manager |
| Electrical Safety Code permit | Regulatory permit | Project Manager (PKG-009) |
| Completed inspection reports | Inspection records | Project Manager (per RFP §3.3.2; Decomp SOW-0084, Decomp SOW-0085) |
| Discipline coordination meeting notes / data exchanges | Coordination records | Project Manager / Electrical Engineer |
