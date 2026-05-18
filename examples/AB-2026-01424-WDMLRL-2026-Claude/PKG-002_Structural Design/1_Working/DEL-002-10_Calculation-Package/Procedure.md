# Procedure: DEL-002-10 Structural Calculation Package

---

## Purpose

This procedure describes the steps required to produce, review, finalize, and deliver the Structural Calculation Package (DEL-002-10) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It covers both the production workflow (how to prepare the calculations) and the quality/verification gates that must be passed before the package is considered complete.

---

## Prerequisites

The following inputs and conditions must be satisfied or acknowledged before calculation work begins:

| Prerequisite | Status / Source | Blocking? |
|---|---|---|
| Conceptual floor plan and building dimensions confirmed | Available — App B (130 ft × 100 ft, 35 ft ceiling, room layout) | Partially satisfied; final architectural coordination required |
| Structural system selection (concrete type, lateral system) | TBD — Structural Engineer of Record decision at design kickoff. **Note:** This is an essential operational decision that gates all subsequent calculation logic (lateral system type governs column design, foundation design, and connection details). A formal go/no-go decision point is established between Steps 1 and 2 — see Decision Gate DG-1 below. [Strengthened per lensing item C-003] | Not blocking for starting preliminary work; **must be resolved before Step 2 (Calculation Structure)** |
| Governing codes confirmed | TBD — NBC edition, Alberta adoptions; to be confirmed by Engineer of Record | Not blocking for starting; must be documented in calculation cover sheet |
| Geotechnical report (DEL-008-01) | NOT YET AVAILABLE — upstream dependency | Not blocking for initial/preliminary calculations on normal ground conditions basis (RFP §4.8.2); blocking for final foundation calculations |
| Crane specifications (manufacturer data, model, wheel loads) | NOT YET AVAILABLE — dependent on procurement (DEL-016-01) | Not blocking; conservative 5-tonne class parameters may be assumed with documented flag |
| Preliminary Architectural Design input (DEL-002-01 / DEL-001-01) | Pending — required for floor plan coordination | Required before final calculations; preliminary dimensions from App B sufficient for early work |
| Mezzanine design live load confirmed by Owner | NOT YET CONFIRMED | ASSUMPTION: Use applicable NBC storage/industrial load pending Owner confirmation |
| Site climatic data (NBC Appendix C — snow, wind, seismicity for Ferintosh / Camrose County area) | Available from NBC Appendix C — not directly accessed in this package | Must be sourced by Structural Engineer of Record |

---

## Steps

### Step 1 — Design Kickoff and Basis of Design

**Action:** Convene a structural design kickoff meeting with the project team (minimum: Structural Engineer of Record, Architect, PM). Establish and document:

1a. Governing codes and standards (NBC edition, CSA A23.3, CSA S16, Alberta Safety Codes — see Specification §Standards).
1b. Structural system type (concrete wall type, lateral load resisting system).
1c. Site climatic parameters — extract from NBC Appendix C for Ferintosh / Camrose area: ground snow load (Ss, Sr), hourly wind pressure (q), seismic hazard values (Sa, F, etc.).
1d. Geotechnical assumption — confirm "normal ground conditions, shallow footing" as the pricing basis per RFP §4.8.2; document the trigger for revision upon geotech report receipt.
1e. Mezzanine design live load — document the assumed value and flag for Owner confirmation.
1f. Crane design loads — document the assumed 5-tonne class parameters used; flag for reconciliation against crane procurement.

**Output:** Design Basis Memorandum (may be the calculation cover section).

**Verification:** Design Basis reviewed by Senior/Reviewing Engineer before proceeding to Step 2.

---

### Decision Gate DG-1 — Structural System Selection Confirmation

**Purpose:** Confirm the structural system type before establishing the calculation structure. This decision gates the organization and content of all subsequent calculation sections. [Added per lensing item C-003]

**Go criteria:**
- Structural system type (concrete wall type, lateral load resisting system) has been selected and documented in the Design Basis Memorandum (Step 1 output).
- The selection is consistent with the building parameters (130 ft x 100 ft footprint, 35 ft clear ceiling, two 5-tonne overhead cranes).

**No-go action:** If the structural system cannot be confirmed at this point (e.g., pending architectural input), document the options under consideration and proceed to Step 2 with the most likely system as a working assumption, clearly flagged as PRELIMINARY. The assumption must be resolved before Step 4 (Final Calculations).

> **Relates to:** Specification REQ-002, REQ-010; Guidance Trade-offs (Lateral load resisting system); Datasheet Key Design Parameters (Lateral Load Resisting System — TBD).

---

### Step 2 — Establish Calculation Structure and Index

**Action:** Create the calculation package structure before populating it. Assign calculation section numbers to each structural subsystem:

| Section | Content | SOW Reference |
|---|---|---|
| DB — Design Basis | Codes, loads, assumptions, scope | SOW-0012, SOW-0019 |
| F — Foundation | Footing/foundation design (variable-price scope) | SOW-0019 |
| S — Superstructure | Columns, beams, roof, lateral system | SOW-0012 |
| M — Mezzanine | Mezzanine framing, connections | SOW-0012 |
| CR — Crane Runway | Runway beams, brackets, column loads | SOW-0012 |
| SP — Service Pit | Pit walls, floor slab at pit | SOW-0012 |
| EP — Steel Plate Embedments | Floor slab at steel plate zones | SOW-0012 |
| WB — Wash Bay Structure | Wash bay framing | SOW-0012 |
| ST — Stair Structure | Stair framing | SOW-0012 |

**Output:** Calculation index / table of contents with section assignments.

**Note:** Foundation section (F) must be clearly demarcated as the variable-price scope (SOW-0019) to support DEL-002-11 segregation (Guidance Principle 3, Specification REQ-014).

---

### Step 3 — Preliminary Calculations (Preliminary Design Support)

**Action:** Perform preliminary sizing calculations sufficient to support the Preliminary Structural Design (DEL-002-01) for County approval. At minimum:

3a. Gravity load take-down to establish preliminary column and foundation loads.
3b. Preliminary lateral system sizing (base shear, primary member sizing).
3c. Preliminary mezzanine beam and column sizing.
3d. Preliminary crane runway beam sizing.
3e. Preliminary foundation type and size (normal ground conditions).

**Output:** Preliminary calculation summary or early-draft sections DB, F (preliminary), S (preliminary), M (preliminary), CR (preliminary).

**Timing:** Must be complete prior to issuance of DEL-002-01 (Preliminary Structural Design presentation to County).

---

### Step 4 — Final Calculations — All Subsystems

**Action:** Develop full final calculations for each section in the calculation index. Each section shall include:

4a. **Loading:** All applicable load cases (dead, live, snow, wind, seismic, crane — as applicable). Load combinations per NBC. [Satisfies REQ-010]
4b. **Analysis:** Member forces, reactions, deflections as required. [Satisfies REQ-001 subsystem completeness]
4c. **Design:** Member sizing, reinforcement (for concrete), or section selection (for steel). Check all applicable limit states (ULS and SLS per NBC/CSA). [Satisfies REQ-002 (concrete superstructure), REQ-004 (foundation), REQ-006 (mezzanine), REQ-007 (crane), REQ-008 (embedments), REQ-009 (service pit), REQ-010 (code compliance)]
4d. **Connections:** Key connection design or reference to detail drawings; note any connections requiring separate calculation. [Satisfies REQ-012 coordination requirements where connections interface with other disciplines]
4e. **Summary:** Pass/fail summary for each check; governing load case identified. [Supports REQ-010 verification — all limit states checked, no element failing]

[REQ cross-references added per lensing item F-003]

**Sequence notes:**
- Section F (Foundation) may be issued as preliminary pending geotech report; mark clearly as PRELIMINARY. [Relates to REQ-004, REQ-005, REQ-014]
- Section CR (Crane Runway): If manufacturer data unavailable, document assumed wheel loads and dynamic factors. Flag for Step 8 reconciliation. [Relates to REQ-007]
- Section M (Mezzanine): Document assumed live load (NBC minimum or Owner-confirmed value). Flag if Owner confirmation is pending. [Relates to REQ-006]

**Output:** Completed calculation sections for all structural subsystems.

---

### Step 5 — Internal Quality Assurance Review

**Action:** Conduct internal QA review of completed calculations before stamp:

5a. **Completeness check:** Verify all sections in the calculation index are complete and indexed.
5b. **Arithmetic check:** Independent check of key calculations (at minimum: governing member designs, foundation, crane runway).
5c. **Code compliance check:** Confirm all code references are current; confirm load combinations are per NBC.
5d. **Assumption audit:** Review all documented assumptions; confirm each has a flag or a resolution status.
5e. **Drawing consistency check:** Cross-reference calculation outputs (member sizes, reinforcement, embedment locations) against draft drawing set (DEL-002-02 through DEL-002-09). Identify and resolve discrepancies.
5f. **Variable-price boundary check:** Confirm Section F is clearly segregated and quantifiable for independent pricing.

**Output:** Completed QA review record (checklist or review comments + resolution log).

---

### Step 6 — Discipline Coordination Check

**Action:** Cross-discipline interface review:

6a. Confirm structural penetrations and openings align with mechanical ductwork routing (PKG-003).
6b. Confirm structural member locations do not conflict with electrical equipment and cable tray routing (PKG-004).
6c. Confirm floor drain and pit locations align with plumbing design (PKG-006).
6d. Confirm crane runway clearances and column bay spacing align with final architectural layout (PKG-001).
6e. Confirm structural loads at foundation are documented for civil/geotechnical review (PKG-008 / DEL-008-01 coordination).

**Output:** Discipline interface checklist or coordination meeting notes. Any structural revisions required by coordination are incorporated into Step 4 calculations before proceeding.

---

### Step 7 — Foundation Reconciliation (Upon Receipt of Geotech Report)

**Action:** When DEL-008-01 (Geotechnical Investigation Report) is received:

7a. Review geotechnical report findings: soil profile, bearing capacity, groundwater, recommended foundation system.
7b. Compare to "normal ground conditions" assumption used in Section F.
7c. If the recommended foundation system is consistent with normal conditions: add a note to Section F confirming this; no revision to calculation required.
7d. If the recommended foundation system differs materially (e.g., pile foundation required): issue a revised Section F. Document as a formal design change; notify PM for contract-level coordination (OBJ-006 / variable-price reconciliation under CCDC 14–2013).
7e. If groundwater is present above pit depth: revise Section SP (Service Pit) to include hydrostatic load case.

**Output:** Revised or confirmed Section F with geotech report reference; any required revisions to Section SP.

---

### Step 8 — Crane Reconciliation (Upon Receipt of Crane Specifications)

**Action:** When crane procurement (DEL-016-01) specifications are confirmed:

8a. Obtain manufacturer's crane data: bridge weight, end-reaction loads, wheel loads, wheel spacing, minimum approach, electric supply.
8b. Compare to assumed loads in Section CR.
8c. If actual loads are within assumed values: note in Section CR — no revision required.
8d. If actual loads exceed assumed values: revise Section CR; check column and bracket adequacy; notify PM and drawing drafter for any required drawing revisions.

**Output:** Confirmed or revised Section CR with crane specification reference.

---

### Step 9 — P.Eng. Stamp and Issue

**Action:** After QA review (Step 5), coordination (Step 6), and reconciliation (Steps 7-8) are complete — or with appropriate PRELIMINARY flags where reconciliation is still pending — the Structural Engineer of Record:

9a. Reviews the complete calculation package.
9b. Confirms that the stamping engineer holds a current APEGA license in good standing and is authorized to practice structural engineering in the Province of Alberta. [Added per lensing item A-002]
9c. Signs and stamps (wet or digital) all calculation sheets per Alberta Engineering and Geoscience Professions Act requirements. [Satisfies REQ-011]
9d. Issues the package as the formal DEL-002-10 deliverable.

**Delivery format:** TBD — The physical/digital delivery format for the calculation package shall be confirmed (e.g., bound hard-copy binder, PDF with digital stamp, or both). If electronic delivery, a file naming convention consistent with the project document management system should be established. [Added per lensing item D-002]

**Output:** Signed and stamped Structural Calculation Package — DEL-002-10.

---

## Verification

After each step, the following conditions shall be confirmed before progressing:

| Gate | Condition | Step |
|---|---|---|
| G-1 | Design Basis documented and reviewed | After Step 1 |
| DG-1 | Structural system type selected and documented (or PRELIMINARY assumption flagged with resolution deadline). Go/no-go criteria: lateral load resisting system identified, consistent with building parameters. [Added per lensing item C-003] | Between Steps 1 and 2 |
| G-2 | Calculation index established; Foundation section clearly demarcated | After Step 2 |
| G-3 | Preliminary calculations complete to support DEL-002-01. **Minimum scope for this gate:** (a) gravity load take-down with preliminary column and foundation loads, (b) preliminary lateral system sizing with base shear calculation, (c) preliminary mezzanine beam/column sizing, (d) preliminary crane runway beam sizing, and (e) preliminary foundation type and size on normal ground conditions basis. [Strengthened per lensing item F-002] | After Step 3 |
| G-4 | All calculation sections complete; each includes loading, analysis, design, and summary | After Step 4 |
| G-5 | Internal QA review complete; no open arithmetic or code errors; assumptions flagged | After Step 5 |
| G-6 | Discipline coordination issues resolved; coordination log complete | After Step 6 |
| G-7 | Foundation reconciled against geotech report (or clearly marked PRELIMINARY with change trigger documented) | After Step 7 |
| G-8 | Crane loads reconciled against procurement data (or clearly marked PRELIMINARY with change trigger documented) | After Step 8 |
| G-9 | P.Eng. stamp present on all sheets; calculation index matches physical package | After Step 9 |

---

## Records

The following records shall exist upon completion of DEL-002-10:

| Record | Description | Owner |
|---|---|---|
| Calculation Package (signed/stamped) | Complete calculation set per Section Index, signed by P.Eng. | Structural Engineer |
| Design Basis Memorandum | Codes, loads, assumptions, system selection | Structural Engineer |
| QA Review Record | Internal review checklist or comments + resolutions | Senior/Reviewing Engineer |
| Discipline Coordination Log | Cross-discipline interface items and resolutions | Structural Engineer / PM |
| Foundation Reconciliation Record | Comparison of geotech findings to assumed conditions; revision log if applicable | Structural Engineer |
| Crane Reconciliation Record | Comparison of crane data to assumed loads; revision log if applicable | Structural Engineer |
| Calculation Revision Log | Record of all revisions to the calculation package. Each revision log entry shall contain at minimum: (a) revision date, (b) revision number, (c) description of change and reason, (d) calculation sections affected, (e) name of person making the revision, and (f) name of reviewer who checked the revision. [Schema defined per lensing item X-004] | Structural Engineer |

### Retention
All records associated with DEL-002-10 shall be retained for the duration of the Guarantee Period (construction period plus 2 years post-CCC per RFP §2.10.2) and per the Structural Engineer's professional obligations under the Alberta Engineering and Geoscience Professions Act.
> Source: RFP §2.10; SOW-0120, SOW-0121.

**TBD — APEGA Retention Requirements:** Verify whether the Alberta Engineering and Geoscience Professions Act and/or APEGA Practice Standards require retention of professional engineering records (including calculation packages) for a period longer than the contractual guarantee period (2 years post-CCC). If so, the longer retention period governs. The Structural Engineer of Record should confirm APEGA-specific retention obligations. [Added per lensing item E-003]
