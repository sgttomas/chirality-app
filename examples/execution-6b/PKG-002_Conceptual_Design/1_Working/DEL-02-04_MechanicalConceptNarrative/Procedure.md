# Mechanical Concept Narrative — Procedure

**Deliverable ID:** DEL-02-04
**Package:** PKG-002 — Conceptual Design
**Type:** Operational Procedure
**Last Updated:** 2026-02-17

---

## Purpose

This Procedure defines the workflow for developing and delivering the Mechanical Concept Narrative across two phases:

- **Phase A: Proposal Development** — Steps to research, draft, and finalize the mechanical concept narrative for inclusion in the RFP proposal response (deadline: August 30, 2024, 2:00 PM MST).
- **Phase B: Design Development Implementation** — Steps to transform the accepted concept narrative into detailed mechanical design post-award.

---

## Prerequisites

### Phase A Prerequisites (Proposal Development)

The following must be accessible before beginning:

| Prerequisite | Source | Status |
|---|---|---|
| RFP 2024_004 §7.1.1 (Proposed Conceptual Design) | RFP document | Accessible |
| RFP Appendix A (Owner Statement of Requirements / OSR) — §11 Mechanical Systems; §10.3.4 Design Requirements | RFP document | Accessible |
| RFP Appendix B (Functional Program) — equipment and power rows | RFP document | Accessible |
| OSR §12.6 (Appliances) — confirmed list: 2 refrigerators with freezers, 2 microwaves, stove + oven with range hoods, dishwasher, 2 laundry sets | RFP document page 45 | Accessible |
| Addendum 03 (Jul 31, 2024) — §1.8, §1.11, §1.12, §1.13, §1.14, §1.15, §1.16, §1.21 | Addendum 03 document | Accessible |
| Preliminary Architectural Concept (DEL-02-01) — floor plan, room layout, door heights, ceiling heights | Architectural team | Upstream dependency |
| Preliminary Structural Concept (DEL-02-03) — slab approach | Structural team | Upstream dependency |
| Civil/Site Concept (DEL-02-02) — site grading, utility entry | Civil team | Upstream dependency |
| 2021 Geotechnical Investigation Report (Appendix D) | RFP document | Accessible |
| Design team roster confirming Mechanical Engineer assignment | PM | Confirmed |

No critical upstream dependencies are declared in `_DEPENDENCIES.md`. All prerequisite information is either accessible from RFP/Addendum 03 documents or available from sibling deliverables within PKG-002.

---

## Steps

### Phase A: Proposal Development

#### Step A1 — Intake and Scope Extraction

**Action:**
1. Mechanical Engineer reads RFP §11 (Mechanical Systems: §11.1.1, §11.1.2, §11.2, §11.3), §10.3.4 (design requirements), Appendix A OSR, Appendix B Functional Program, OSR §12.6 (appliances), and all five pages of Addendum 03.
2. Extract all mechanical requirements into a checklist. Mandatory items from Addendum 03:
   - Bay sumps (§1.8)
   - PW bay ventilation (§1.11)
   - Fire apparatus direct exhaust, 2 per bay (§1.12)
   - Bunker gear room ventilation (§1.14)
   - Backup generator (§1.15)
   - Water fill stations (§1.16)
   - Room sizing table with mechanical implications (§1.21): apparatus bays (2000–2200 sf), workshop bays (2000–2200 sf), fire gear storage (200–350 sf), decontamination room (150–200 sf), decontamination shower/WR (50–60 sf x2), SCBA room (150–200 sf), compressor room (100–150 sf)
3. Extract all appliance loads from OSR §12.6: stove + oven with range hoods; 2 refrigerators with freezers; 2 microwaves; dishwasher; 2 laundry sets. Each has hot water and/or drainage requirements.
4. Note all spaces with mechanical loads from Functional Program (rows 1.0, 2.0 apparatus bays; row 12.0 mechanical/sprinkler room; row 16.0 kitchen; row 19.0 training/ICP; row 28.0 workshop; row 30.0 generator).
5. Identify cross-discipline interfaces: architectural (room layout, door heights, ceiling heights, decontamination drain locations), structural (slab for sumps and decon drains), civil (site drainage for sump discharge), electrical (generator ATS).

**Output:** Mechanical scope checklist including all Addendum 03 §1.21 rooms; cross-discipline interface list.

**Duration:** Day 1–2.

---

#### Step A2 — Preliminary System Selections

**Action:**
1. Select preliminary mechanical systems for each required scope element:
   - Main HVAC: high-efficiency condensing boiler or heat pump (TBD); ERV/HRV for office/residential zones; second-story zoning if architectural option adopted (Add 03 §1.5).
   - Fire apparatus bay exhaust: dedicated exhaust fan(s), 10,000–15,000 CFM per bay, damper control, tailpipe capture stubs.
   - PW bay ventilation: general roof or wall exhaust fan(s); sized for occasional idling.
   - Bunker gear room: local wall or roof exhaust fan.
   - Decontamination room/showers: hot/cold water branches, floor drains with traps, dedicated exhaust fan to exterior.
   - SCBA room: conditioned air supply from main HVAC; temperature-stabilized storage.
   - Compressor room: dedicated ventilation for heat rejection.
   - Cold Storage: passive or low-energy mechanical ventilation.
   - Water fill stations: 2" female coupling, ground level, one per fire bay and PW bay.
   - Bay sumps: submersible pump in sump pit; discharge routing TBD.
   - Domestic hot water: sizing must include kitchen, bathrooms, decontamination showers, dishwasher, and 2 laundry sets; storage tank + high-efficiency heat source (TBD); tankless point-of-use for remote fixtures.
   - Backup generator: diesel or natural gas standby; outdoor pad-mounted; ATS; 20–30 kW estimate.
   - Fire protection: wet or dry sprinkler system (TBD pending AHJ consultation and bay thermal design).
   - Kitchen exhaust: range hoods over stove/oven per code; makeup air.
2. Document all selections as ASSUMPTION. Mark all TBD items.
3. Review Guidance Considerations C-001 through C-006 and Trade-offs T-001 through T-004 to capture key decision points in narrative.

**Output:** Preliminary system selections table (for Datasheet Construction section); TBD items list.

**Duration:** Day 3–5.

---

#### Step A3 — Cross-Discipline Interface Documentation

**Action:**
1. Confirm apparatus bay ceiling/truss height from Architectural (DEL-02-01): must accommodate exhaust ductwork above 16 ft door clearance.
2. Confirm slab penetration feasibility with Structural (DEL-02-03): sump pit locations, decontamination drain locations, floor slope requirements, penetration sizing.
3. Confirm site drainage routing options with Civil (DEL-02-02): municipal sewer availability, percolation field feasibility.
4. Confirm generator electrical specs handoff to Electrical (DEL-02-05): capacity (kW), voltage, phase, fuel type, ATS requirements.
5. Confirm second-story adoption status with Architectural (DEL-02-01): if adopted, confirm HVAC zoning approach for upper floor.
6. Document all confirmed interfaces and all unresolved interfaces (TBD) in Datasheet section "Design Integration Points."

**Output:** Cross-discipline interface matrix; risk/constraint summary.

**Duration:** Day 6–8.

---

#### Step A4 — Draft Mechanical Concept Narrative

**Action:**
1. Draft the narrative document (the actual deliverable artifact) covering all mechanical systems in logical sequence: HVAC → fire apparatus exhaust → PW bay ventilation → bunker gear room ventilation → decontamination plumbing → SCBA room climate → compressor room → Cold Storage → plumbing (water supply + fill stations + hot water + appliances) → bay sumps → backup generator → fire protection → kitchen exhaust.
2. For each system section:
   - State the Owner requirement with Addendum 03 citation where applicable.
   - Describe the concept design approach.
   - Identify key design decisions or TBD items.
   - Note cross-discipline interfaces.
3. Embed all Addendum 03 requirements explicitly with section references (§1.8, §1.11, §1.12, §1.14, §1.15, §1.16, §1.21).
4. Embed OSR §12.6 appliance list plumbing scope (dishwasher, laundry sets, range hoods).
5. Include cross-discipline interface summary at end of narrative.
6. Label all ASSUMPTION items and TBD items clearly.
7. Target length: 3,000–6,000 words for concept-stage narrative (sufficient depth without over-engineering).

**Output:** Draft Mechanical Concept Narrative document.

**Duration:** Day 9–14.

---

#### Step A5 — Internal Multi-Discipline Review

**Action:**
1. Circulate draft narrative to Architectural, Structural, Civil, and Electrical leads with specific review focus areas:
   - Architectural: confirm door heights, ceiling clearances, room layout feasibility, decontamination room location relative to structure.
   - Structural: confirm sump pit feasibility, slab penetration approach for sumps and decon drains.
   - Civil: confirm sump discharge routing options.
   - Electrical: confirm generator handoff requirements, ATS coordination.
2. Incorporate review comments; resolve or document unresolved items.
3. Re-circulate for final acknowledgement from discipline leads (email sign-off acceptable at proposal stage).

**Output:** Reviewed and revised narrative; discipline acknowledgements.

**Duration:** Day 15–18.

---

#### Step A6 — Quality Check and Addendum 03 Compliance Verification

**QC Reviewer Identification (Lensing D-002):** The QC review must be performed by a qualified reviewer who is independent of the primary authoring Mechanical Engineer. The QC reviewer should be one of the following: (a) the Proposal Manager, (b) a designated QC lead with mechanical engineering background, or (c) a senior mechanical engineer not involved in drafting the concept narrative. The reviewer's name and role must be recorded in the QC review sign-off record (see Phase A Records). This ensures systematic process assurance and independent verification of the deliverable quality.

**Action:**
1. Assign QC reviewer per the identification criteria above before beginning the quality check.
2. Complete the Addendum 03 Compliance Verification Checklist (see Verification section below).
3. Confirm all 7 Addendum 03 mechanical requirements are addressed in the narrative (including §1.21 room sizing table).
4. Confirm OSR §12.6 full appliance list is addressed (range hoods, dishwasher, laundry sets — not just stove/oven).
5. Check cross-document consistency: narrative content matches Datasheet attributes, Specification requirements, and Guidance principles.
6. Confirm all ASSUMPTION and TBD items are labeled.
7. Confirm no invented facts (all statements either sourced or ASSUMPTION-labeled).

**Output:** Quality-checked Mechanical Concept Narrative; QC sign-off (including reviewer name, role, and date).

**Duration:** Day 19–20.

---

#### Step A7 — Finalization and Submission Handoff

**Action:**
1. Finalize formatting, page layout, and section headings per proposal document standards.
2. Export to PDF or final document format per Proposal Manager's instructions.
3. Deliver to Proposal Manager for inclusion in RFP proposal response under Section 7.1.1 (Proposed Conceptual Design).
4. Confirm final version is received and integrated into the proposal assembly (DEL-01-02 FormalSubmissionPackage coordination).

**Output:** Finalized Mechanical Concept Narrative; submitted as part of RFP proposal by August 30, 2024.

**Duration:** Day 21.

---

### Phase B: Design Development Implementation (Post-Award)

This phase transforms the accepted concept narrative into complete, code-compliant, buildable mechanical design.

#### Step B1 — Design Kickoff, Load Calculations, and Commissioning Agent Engagement

**Action:** Conduct heating/cooling/ventilation load calculations; establish design criteria; confirm design team and discipline coordination approach. Meetings with Owner to confirm generator scope, SCBA cylinder temperature requirements, and ATS requirements. Confirm second-story adoption with Architectural.

**Commissioning Agent Engagement (Lensing D-001):** Engage the commissioning agent no later than design kickoff (Week 1 post-award). The Specification Verification matrix references a "Commissioning Agent" for multiple system tests (apparatus bay exhaust, HVAC air balance, generator ATS test, fire protection, plumbing). Early engagement ensures the commissioning agent can review design intent, contribute to test procedure development, and identify commissioning access requirements before detailed design proceeds. If commissioning agent engagement is deferred beyond 60% design, risk of late-stage commissioning scope gaps increases.

**Outputs:** Design criteria report; load calculation summary; hot water peak demand calculation; kickoff meeting minutes; commissioning agent engagement confirmation and scope agreement.

**Timing:** Weeks 1–3 post-award.

---

#### Step B2 — Ventilation and HVAC System Design

**Action:** Design HVAC zone layout (including second story if adopted); apparatus bay exhaust system design (fan sizing, damper type, control strategy); PW bay ventilation sizing; bunker gear room fan sizing; decontamination area exhaust fan sizing; SCBA room conditioned air supply sizing; compressor room heat-rejection ventilation sizing; ERV/HRV integration for office/residential zones; Cold Storage ventilation opening design.

**Outputs:** HVAC schematic; ventilation system design drawings (preliminary); equipment selection.

**Timing:** Weeks 4–7 post-award.

---

#### Step B3 — Plumbing and Generator Design

**Action:** Design domestic water supply system (from municipal service through distribution); water fill station locations, sizing, and connections (2" minimum, ground level); sump pit sizing, locations, and pump selection; decontamination room and shower plumbing rough-in (hot/cold supply, floor drains, trap primer); laundry set and dishwasher connections; domestic hot water system design (peak demand sizing accounting for all confirmed OSR §12.6 loads + decon showers); kitchen exhaust hood sizing; generator capacity finalized (with Electrical load list); ATS specification; generator location and fuel system.

**Outputs:** Plumbing design drawings (preliminary); generator specification; ATS specification.

**Timing:** Weeks 8–11 post-award.

---

#### Step B4 — Fire Protection Preliminary Design

**Action:** Consult with AHJ to confirm fire sprinkler system type (wet vs. dry) for apparatus bay zones; design building-wide fire protection layout; hydraulic calculations preliminary; municipal water service connection design.

**Outputs:** Fire protection schematic; AHJ pre-consultation notes.

**Timing:** Weeks 10–13 post-award (overlaps with Step B3).

---

#### Step B5 — Multi-Discipline Coordination

**Action:** Consolidate mechanical design; conduct clash detection; resolve ductwork, piping, and structural conflicts; finalize sump pit locations with Structural; confirm decontamination drain locations with Structural and Architectural; confirm generator electrical handoff to Electrical; confirm sump discharge routing with Civil; confirm solar-ready roof clearances with Architectural.

**Outputs:** Coordination meeting minutes; clash detection report; resolved interface matrix.

**Timing:** Weeks 12–14 post-award.

---

#### Step B6 — 60% Design Submission and Code Review

**Action:** Complete 60% design drawings and specifications; conduct internal code compliance review (Alberta Building Code, NECB); AHJ pre-submission meeting for fire protection; Owner presentation.

**Outputs:** 60% design submission package; code compliance narrative; AHJ pre-submission meeting notes.

**Timing:** Weeks 14–16 post-award.

---

#### Step B7 — 100% IFC Design Package

**Action:** Incorporate 60% review comments; finalize all mechanical drawings (HVAC, plumbing, fire protection, generator/ATS); complete equipment schedules; final specifications; final AHJ submissions; Owner review and approval.

**Outputs:** 100% IFC mechanical design drawings and specifications; AHJ approvals; design completion sign-off.

**Timing:** Weeks 22–26 post-award.

---

## Verification

### Phase A — Addendum 03 Compliance Checklist

Verify all Addendum 03 mechanical requirements are addressed in the narrative before submission:

| Item | Addendum 03 Reference | Addressed in Narrative? |
|---|---|---|
| Bay sumps (snow melting + minor washing) in all bays | §1.8 | YES / NO |
| Fire apparatus bay: direct exhaust ventilation, 2 apparatus per bay | §1.12 | YES / NO |
| PW bay: general ventilation (occasional idling + very occasional welding) | §1.11 | YES / NO |
| Bunker gear room: room-level ventilation (not per-locker) | §1.14 | YES / NO |
| Backup generator: kitchen + ICP/meeting room + 2 bathrooms + bay door secondary opening | §1.15 | YES / NO |
| Water fill stations: 2" minimum, ground level, 1 fire bay + 1 PW bay | §1.16 | YES / NO |
| Room sizing table rooms with mechanical implications: decon room (150–200 sf), decon showers (50–60 sf x2), SCBA room (150–200 sf), compressor room (100–150 sf) | §1.21 | YES / NO |

**Pass threshold:** All 7 items = YES before submission.

### Phase A — OSR Appliance Plumbing Compliance Checklist

Verify all OSR §12.6 appliances with mechanical requirements are addressed:

| Appliance | Mechanical Requirement | Addressed? |
|---|---|---|
| Stove + oven with range hoods | Range hood, makeup air per code | YES / NO |
| 2 refrigerators with freezers | Power only (no plumbing); electrical coordination | N/A — electrical scope |
| 2 microwaves | Power only; no plumbing required | N/A — electrical scope |
| Dishwasher | Hot water supply + drain connection | YES / NO |
| 2 residential laundry sets | Hot + cold water supply + drain connection per laundry set | YES / NO |

**Pass threshold:** All mechanical-relevant items = YES before submission.

### Phase A — Document Quality Checklist

| Check | Criteria | Status |
|---|---|---|
| All systems covered | HVAC, exhaust, PW ventilation, bunker gear, decontamination, SCBA/compressor, Cold Storage, plumbing, fill stations, sumps, generator, fire protection, kitchen exhaust | YES / NO |
| Sources cited | Non-trivial statements cite RFP, Addendum 03, or OSR section | YES / NO |
| ASSUMPTION items labeled | All inferred content labeled ASSUMPTION | YES / NO |
| TBD items identified | Missing information labeled TBD (not invented) | YES / NO |
| Cross-discipline interfaces identified | Architectural, Structural, Civil, Electrical interfaces listed | YES / NO |
| Cross-document consistency | Narrative content consistent with Datasheet, Specification, Guidance | YES / NO |
| OBJ-003 alignment | Narrative demonstrates operational understanding; supports 20-pt evaluation criterion | YES / NO |

### Phase B — Design Completion Verification

| Check | Criteria | Status |
|---|---|---|
| All concept-phase TBD items resolved | HVAC selection, generator capacity, sump routing, sprinkler type, ventilation rates, SCBA temperature requirement, decon drain disposal method | YES / INCOMPLETE |
| Alberta Building Code compliance verified | All mechanical systems; code compliance narrative produced | YES / INCOMPLETE |
| NECB energy compliance verified | HVAC and ventilation energy modeling completed | YES / INCOMPLETE |
| AHJ approvals obtained | Fire protection AHJ plan approval; permit issued | YES / PENDING |
| 100% IFC drawings complete | All mechanical disciplines; equipment schedules; specifications | YES / INCOMPLETE |
| Cross-discipline clashes resolved | Clash detection completed; all conflicts resolved | YES / UNRESOLVED |
| Commissioning plan produced | Commissioning agent engaged; test procedures drafted | YES / INCOMPLETE |

---

## Records

### Phase A Records

| Record | Description |
|---|---|
| Mechanical scope checklist | Extracted from RFP/Addendum 03; all requirements listed including §1.21 room sizing |
| OSR §12.6 appliance plumbing scope summary | Identifies mechanical loads from each confirmed appliance |
| Cross-discipline interface matrix | Interface responsibilities and TBD items |
| Preliminary system selections summary | Concept-stage equipment selections with ASSUMPTION labels |
| Draft Mechanical Concept Narrative (all versions) | Working drafts with tracked changes |
| Discipline review comments | Emails or markup documents from Architectural, Structural, Civil, Electrical leads |
| Addendum 03 compliance checklist | Completed verification checklist (all 7 items = YES) |
| OSR §12.6 appliance plumbing checklist | Completed verification checklist |
| QC review sign-off | Proposal Manager or QC lead sign-off; must include reviewer name, role, and independence confirmation per Step A6 (Lensing D-002) |
| Final Mechanical Concept Narrative | Submitted version included in RFP proposal |

### Phase B Records

| Record | Description |
|---|---|
| Commissioning agent engagement confirmation | Scope agreement, engagement date, and commissioning agent contact information; confirmed at design kickoff per Step B1 (Lensing D-001) |
| Load calculation report | Heating, cooling, ventilation, hot water peak demand (all loads) electrical load calculations |
| Design coordination meeting minutes | Multi-discipline coordination session records |
| Equipment selection justification | Manufacturer/model selection rationale with cost comparison |
| AHJ review notes and approvals | Fire protection pre-submission meeting notes; permit |
| Code compliance narrative | Alberta Building Code and NECB compliance review |
| 60% and 100% design drawings | Mechanical drawings at each submission milestone |
| Clash detection report | Clash detection results and resolution documentation |
| 100% IFC specifications | Final mechanical specifications (NMS format recommended per RFP §7.2) |
| Commissioning plan | Test procedures for all mechanical systems |
| O&M manual mechanical section | Equipment data, maintenance schedules, contact lists |
| Design completion sign-off | All discipline leads and PM sign-off on 100% IFC package |

---

## Notes

### Key Authoring Guidance for the Concept Narrative

1. **Lead with Addendum 03 compliance.** Evaluators reviewing this narrative for OBJ-003 will check whether all Addendum 03 clarifications are embedded. State each requirement explicitly with the Addendum 03 section reference before describing the design response.

2. **Address every functional room from §1.21.** The Addendum 03 room sizing table is a direct signal of Owner expectations. Rooms with mechanical implications (decontamination, SCBA, compressor) must each receive at least a paragraph in the narrative.

3. **Use clear system headings.** Organize by mechanical system (HVAC, Apparatus Bay Exhaust, PW Bay Ventilation, etc.) so reviewers can locate each topic quickly. This is a design brief, not a textbook — lead with the "what and why," support with technical rationale.

4. **Quantify where possible.** Even at concept stage, rough estimates (exhaust fan CFM range, generator kW estimate, sump pit dimensions, hot water peak demand) demonstrate engineering competence and give evaluators confidence that the team has done substantive thinking.

5. **Name the coordination points.** Explicitly stating "mechanical exhaust ductwork must clear the 16 ft door height confirmed with architectural layout" shows integrated design thinking, which evaluators reward.

6. **Include the full appliance plumbing scope.** OSR §12.6 lists a dishwasher and two laundry sets in addition to the stove and range hoods. These require hot/cold water supply and drain connections. Missing these signals incomplete scope coverage.

7. **Label every ASSUMPTION and TBD.** Per protocol, all inferred content must be labeled ASSUMPTION; missing information must be TBD. Do not invent values or omit important gaps. TBD is credible; invented values are not.

### Common Pitfalls to Avoid

- Omitting the Cold Storage building ventilation requirement (RFP §11.1.2 is distinct from Main Building).
- Describing "bay door secondary opening" as a generator-only solution — Addendum 03 §1.15 explicitly allows manual override as an alternative.
- Specifying per-locker ventilation for bunker gear — Addendum 03 §1.14 explicitly states "direct ventilation to each locker is not required; the room itself should have ventilation."
- Failing to address the kitchen range hood requirement (implied by OSR §12.6 appliance list; easily missed if narrative focuses only on explicit RFP §11 content).
- Omitting the dishwasher and laundry set plumbing scope from OSR §12.6 — these are explicit appliances on the confirmed list.
- Omitting decontamination room and shower plumbing — Addendum 03 §1.21 sizes these rooms; mechanical scope must address them.
- Omitting SCBA room climate control and compressor room heat rejection ventilation.
- Using only RFP §11 without cross-referencing Addendum 03 — Addendum 03 adds and clarifies significant mechanical requirements not fully captured in the base RFP.

---

**End of Procedure**
