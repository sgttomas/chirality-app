# Electrical Maintainability — Procedure

## Purpose

This procedure describes the process for **producing** the electrical maintainability narrative (DEL-05-04) during the proposal phase, and after award, **operationalizing** the electrical maintenance strategy throughout the facility's design life (50 years main building; 20 years Cold Storage).

The narrative-production process (Steps 1–6) is the primary focus at the proposal stage. The post-occupancy maintenance phases (Steps A–E) give the proposal narrative credibility by showing the full operational lifecycle intent — demonstrating to the Evaluation Committee that the Design-Builder has thought through a 50-year operation, not just commissioning.

---

## Prerequisites

### For Narrative Production (Proposal Phase)

| Prerequisite | Source | Status at Proposal Stage |
|--------------|--------|--------------------------|
| RFP, Addenda 01, 02, 03 | AB-2024-07156-Penhold PSB RFP_2024_004.pdf; Addendum 03 | Available |
| Decomposition v2.3 FINAL | Penhold_PSB_Project_Decomposition_v2.md, §9 DEL-05-04 | Available |
| RFP OSR §10.4, §10.5, §10.6 (electrical, lighting, IT/telecom) | RFP Appendix A, pp. 42–43 | Available |
| RFP Optional Items §12.3, §12.4 (access control, security) | RFP p. 44 | Available |
| RFP Functional Program (App B, p. 46) | Room-level electrical/IT requirements | Available |
| Electrical/IT Concept Narrative (DEL-02-05) | PKG-002 — provides design baseline for system locations and types | Required before Step 5 |
| Electrical Energy Efficiency Narrative (DEL-04-03) | PKG-004 — LED controls, solar-ready provisions, metering coordination | Required before Step 5 |
| Mechanical Maintainability Narrative (DEL-05-03) | PKG-005 — generator location, bay exhaust fans, mechanical-electrical interfaces | Required before Step 5 |
| Electrical Engineer assigned as responsible party | Per Decomposition DEL-05-04 | Required |
| Access to IES standards, CEC, CAN/ULC codes | Expert knowledge or document access | Required |

### For Post-Occupancy Maintenance (Post-Award / Post-Construction)

| Prerequisite | Produced When |
|--------------|---------------|
| Electrical design drawings and panel schedules | Detailed design phase |
| One-line diagram and circuit schedule | 100% Detailed Design / IFC |
| Lighting fixture and equipment schedules (standardized by zone) | Detailed design phase |
| IT/Telecom cabling design and conduit layout | Detailed design phase |
| O&M manuals (all systems) | Commissioning phase |
| Facility staff training completion records | Commissioning / closeout |
| Preventive maintenance schedule | Commissioning (initial); updated Year 1 |

---

## Steps — Narrative Production (Proposal Phase)

### Step 1: Gather Requirements and Context

**Action:**
1. Read RFP §7.1.4 (p. 17) for the Owner's durability/maintenance narrative requirements and evaluation intent.
2. Read RFP OSR §10.4 (p. 42), §10.5 (p. 42), §10.6 (pp. 42–43) for electrical system, lighting, and IT/telecom requirements.
3. Read Addendum 03:
   - §1.8 (bay sumps — moisture environment implication)
   - §1.10 (16 ft minimum OH door height — fixture clearance implication)
   - §1.13 (40 bunker gear lockers — electrical provisions needed)
   - §1.14 (bunker gear room ventilation — electrical for fan motor)
   - §1.15 (generator minimum loads and bay door secondary opening)
   - §1.16 (water fill stations — 2" minimum; corrosion-resistant electrical in fill station areas)
   - §1.17 (solar-capable roofing — electrical rough-in required)
   - §1.19 (no Town preference on security/camera suppliers)
4. Read RFP Functional Program (App B, p. 46) to extract room-level electrical/IT requirements (apparatus bay power drops, IT room, meeting room/ICP, generator area, cold storage, etc.).
5. Review the decomposition entry for DEL-05-04 to confirm scope boundaries.
6. Confirm design life requirements: main building 50 years; Cold Storage 20 years.
7. Review OBJ-005 evaluation criteria (15 pts) and scoring matrix (RFP §8.3, p. 27) to calibrate narrative depth and specificity.

**Responsibility:** Electrical Engineer (lead); Proposal Manager (scope confirmation)

**Output:** Internal requirements summary (not submitted)

---

### Step 2: Establish Standardization and Lifecycle Strategy

**Action:**
1. Develop preliminary component standardization decisions for each system:

   | System | Standardization Decision | Lifecycle Target | Environment Notes |
   |--------|-------------------------|-----------------|-------------------|
   | Apparatus bay lighting | Single LED high-bay type (IP65, wet/damp rated, -40°C start) | 60,000+ hours (~20 yr) | Exhaust particulate; salt; moisture from sumps |
   | Office/shared space lighting | Single LED downlight or linear troffer type | 50,000+ hours (~15 yr) | Standard indoor |
   | Storage/ancillary lighting | Single utility LED type | 50,000+ hours | Cold Storage: cold-rated required |
   | Cold Storage lighting | Motion-activated LED, cold-rated (≥-40°C) | 50,000+ hours | Freeze-thaw cycles; unheated |
   | Fire alarm | Single ULCS527-certified manufacturer; addressable system | 15–20 yr panel lifecycle | Indoor; humidity |
   | Building controls | Single platform (lighting + integration capable) | 10–15 yr software cycle | — |
   | IT cabling | CAT6A throughout; single connector type | 30–40 yr cabling lifecycle | — |
   | Security/access control | Open-standard protocols; no Town supplier preference | 10–15 yr hardware lifecycle | Per Addendum 03 §1.19 |

   **ASSUMPTION:** Specific product selections TBD at detailed design. The above are framework targets for the narrative.

2. Document spare capacity targets:
   - Main panel: minimum 20% spare breaker positions at commissioning (**ASSUMPTION: typical practice; TBD at detailed design**)
   - Distribution boards: minimum 20% spare positions
   - IT conduit: spare stubs at each major junction for future cable addition without trenching
   - Solar-ready: conduit stubs from roof to electrical room; panel space reservation; inverter location designated per Addendum 03 §1.17

3. Identify key supplier criteria for each system:
   - Documented Canadian service network (Alberta at minimum)
   - Published product support lifecycle (minimum matching system design life)
   - Upgrade/replacement pathway for hardware without full system redesign

**Responsibility:** Electrical Engineer (lead); Procurement (supplier input)

**Output:** Standardization and Lifecycle Strategy Matrix (internal working note)

---

### Step 3: Coordinate with Discipline Leads

**Action:**

1. **Architectural coordination:**
   - Confirm electrical room (row 13.0) and IT room (row 17.0) locations, dimensions, and access clearances.
   - Confirm lighting fixture mounting heights in all zones (especially apparatus bays — clearance above 16 ft OH door minimum per Addendum 03 §1.10).
   - Confirm cable routing corridors and ceiling/wall access strategy for future maintenance.
   - Confirm bunker gear room size (40 lockers per Addendum 03 §1.13) and electrical provisions needed.

2. **Mechanical coordination (DEL-05-03):**
   - Confirm generator location and electrical interfaces (transfer switch location, essential load connections per Addendum 03 §1.15).
   - Confirm that IT room and electrical room HVAC is on the generator-backed essential load list.
   - Confirm bay exhaust fan electrical circuits and maintenance access.
   - Confirm bay sump pump electrical provisions (sump required per Addendum 03 §1.8).
   - Confirm water fill station locations (Addendum 03 §1.16) and electrical provisions (if powered fill station).
   - Confirm bunker gear room ventilation fan motor electrical circuit (Addendum 03 §1.14).

3. **Structural coordination:**
   - Confirm conduit support and cable tray integration with structural system.
   - Confirm solar-ready roof structural provisions align with electrical rough-in conduit locations (Addendum 03 §1.17).

4. Document coordination outcomes for integration into narrative and for consistency with DEL-02-05 (Electrical/IT Concept Narrative).

**Responsibility:** Electrical Engineer (lead); Discipline leads (input)

**Output:** Coordination meeting notes; updated design decisions table

---

### Step 4: Draft Narrative Structure and Outline

**Action:**
1. Prepare outline covering the following sections (aligned to decomposition scope and RFP §7.1.4):

   | Section | Key Sub-Topics |
   |---------|---------------|
   | 1. Electrical Panel & Distribution Accessibility | Main panel location; key fob access; spare capacity; sub-panels by zone; circuit labeling |
   | 2. Lighting Systems | Standardized LED types by zone category; IP ratings; Cold Storage cold-rated; fixture access; lifecycle intervals; control interface |
   | 3. Building Controls & Management | Platform selection; zone isolation capability; programming documentation; proprietary risk mitigation |
   | 4. IT / Telecom Infrastructure | Cabling standard; conduit/cable tray approach; 15-access-point ICP provision; dispatch display; PA system; cable labeling; spare capacity |
   | 5. Security & Access Control | Key Fob zones per Functional Program; hardware/software lifecycle; open-standards approach; Addendum 03 §1.19 compliance |
   | 6. Fire Alarm System | ULCS527-certified; addressable architecture; testing/maintenance access; code upgrade compatibility; service network |
   | 7. Emergency / Backup Power + Solar-Ready | Generator minimum load per Addendum 03 §1.15; transfer switch serviceability; load testing provisions; solar conduit rough-in per Addendum 03 §1.17 |

2. For each section, prepare talking points:
   - Component selection and standardization rationale
   - Typical lifecycle and replacement intervals
   - In-house vs. contracted maintenance split
   - Documentation and training approach specific to this system

**Responsibility:** Electrical Engineer (lead)

**Output:** Narrative outline (working document)

---

### Step 5: Incorporate Concept Design References

**Action:**
1. Obtain finalized conceptual design from DEL-02-05 showing:
   - Electrical room, IT room, and panel locations (floor plan)
   - Lighting fixture locations and zone types
   - Cable routing corridors
   - Generator location and transfer switch placement
   - Solar conduit rough-in pathway from roof to electrical room

2. Cross-reference narrative text to specific design features. Example:
   - "Main electrical panel is located in the electrical room (row 13.0, adjacent to [zone reference], Drawing E-101), providing key-fob-accessible maintenance access for authorized facilities staff..."

3. Verify that maintainability claims are grounded in actual design decisions, not aspirational statements.

4. Insert drawing references or excerpts as appendices to the narrative section.

**Responsibility:** Electrical Engineer (lead); Architect (drawing access)

**Output:** Narrative draft with embedded design references

---

### Step 6: Draft, Review, and Finalize Narrative

**Action:**
1. Write the full narrative (target 4–8 pages) incorporating:
   - Executive summary (1 paragraph) of overall electrical maintainability strategy
   - Detailed sections per Step 4 outline
   - Design-specific examples and drawing references from Step 5
   - Specific standardization/lifecycle commitments where determinable at proposal stage
   - Explicit acknowledgment of 50-year main building / 20-year Cold Storage design lives
   - Explicit Addendum 03 compliance statements (§1.8, §1.10, §1.15, §1.17, §1.19)

2. Internal review checklist:

   | Reviewer | Review Focus |
   |----------|-------------|
   | Proposal Manager | RFP §7.1.4 compliance; proposal section order |
   | Design Manager | Consistency with DEL-02-05, DEL-04-03, DEL-05-03 |
   | Estimator | Referenced service contracts, spare parts, training costs captured in pricing |
   | Mechanical Engineer | Mechanical-electrical interface statements consistent with DEL-05-03 |
   | Architectural Lead | Fixture locations, clearances, room sizing consistent with DEL-02-01 |

3. Revise based on review; confirm consistency with DEL-02-05, DEL-04-03, DEL-05-01, DEL-05-03.

4. Electrical Engineer provides final technical approval; Design Manager approves for proposal integration.

5. Complete OBJ-005 Final Checklist (see Verification section).

**Responsibility:** Electrical Engineer (lead); Proposal Manager (review); all discipline leads (consistency check)

**Output:** Approved electrical maintainability narrative, ready for proposal integration

---

## Steps — Operational Maintenance (Post-Award / Post-Occupancy)

### Step A: Detailed Design Phase (Year -1 to Occupancy)

**Action:**
1. Finalize electrical design drawings incorporating all maintainability principles from the proposal narrative:
   - Panel schedules with spare capacity documented
   - Lighting fixture schedules with zone standardization confirmed; cold-rating for Cold Storage confirmed
   - IT/telecom cabling layout with spare conduit stubs marked on drawings
   - Solar-ready conduit stubs installed per Addendum 03 §1.17; panel space documented
   - Generator load schedule and transfer switch location finalized (essential loads per Addendum 03 §1.15)
   - Bunker gear room electrical provisions confirmed (ventilation fan circuit per Addendum 03 §1.14)

2. Produce O&M manual outlines for each system (electrical, lighting, controls, IT, security, fire alarm, generator) during design development — do not wait until construction.

3. Confirm fire alarm zone isolation capability and AHJ pre-approval process for testing/maintenance impairment (24/7 operations requirement).

**Responsibility:** Electrical Engineer (design lead); Commissioning agent (O&M planning)

---

### Step B: Construction Phase

**Action:**
1. Verify all installations match design drawings before concealment or commissioning:
   - Panel locations and access clearances (minimum 1 m clear working space)
   - Circuit labeling installed and accurate before commissioning
   - LED fixture types per zone standardization schedule; cold-rated types in Cold Storage
   - Conduit/cabling with spare stubs at documented locations
   - Generator transfer switch and control panel placement (indoor, accessible)
   - Solar-ready conduit stubs pulled and ends capped

2. Document all field changes for as-built drawings — no undocumented deviations.

3. Test fire alarm per CAN/ULC-S527 certification process.

4. TIA certification test for structured IT cabling.

**Responsibility:** Electrical Engineer; Commissioning agent; General Contractor

---

### Step C: Commissioning & Closeout

**Action:**
1. Execute formal commissioning for all electrical systems per RFP §7.3.6 (p. 22):
   - Lighting: verify IES levels by zone; test emergency exit battery backup; test motion sensors (Cold Storage)
   - Controls: verify zone isolation capability; programming documentation archived
   - IT/telecom: connectivity test at all outlets; 15-access-point test in ICP room (R-EML-13)
   - PA system: coverage test throughout main structure (R-EML-15)
   - Dispatch display: functional test in apparatus bay (R-EML-14)
   - Security/access control: zone-by-zone test including all Key Fob zones per Functional Program
   - Fire alarm: full functional test per fire code requirements
   - Generator: load test under full simulated essential load (kitchen, ICP, 2 bathrooms, bay door secondary opening per Addendum 03 §1.15)

2. Verify that the O&M manual includes a **maintenance sequencing guide** showing which circuits and systems can be worked simultaneously vs. sequentially (required per Guidance C-002 for 24/7 operations). This guide is a critical deliverable for operational maintenance planning and must be reviewed for completeness and accuracy before Owner handover. (Source: Guidance C-002; Semantic Lensing D-001)

3. Produce completed O&M manuals (two hard copy + digital per RFP §7.5, p. 24):

   | Manual Section | Key Contents |
   |----------------|-------------|
   | Electrical Distribution | One-line diagram; panel schedule with spare capacity record; circuit labels list; vendor contact |
   | Lighting Systems | Fixture schedule with part numbers and zone map; driver replacement procedure; cold-rating confirmation for Cold Storage |
   | Building Controls | Zone map; programming documentation; setpoint schedules; adjustment procedure; backup files |
   | IT/Telecom | Cabling design; termination schedule; label convention; spare conduit record; network equipment list |
   | Security/Access Control | Zone architecture; component schedule; bypass/override procedure; vendor support contacts; upgrade pathway statement |
   | Fire Alarm | Riser diagram; component schedule; testing procedure; maintenance contractor contact; spare parts list |
   | Emergency Generator | Essential load schedule per Addendum 03 §1.15; transfer switch operation; monthly test procedure; fuel system details; annual service contact |

4. Conduct formal training for facility operations staff on:
   - Routine operation and daily/weekly checks for each system
   - Lamp and driver replacement procedure (by zone type)
   - Control system schedule adjustments
   - Generator monthly load test procedure
   - IT room UPS management
   - When to call a licensed service contractor vs. handle in-house
   - How to locate documentation and parts information

5. Resolve all electrical-related deficiencies before occupancy sign-off.

**Responsibility:** Commissioning agent (lead); Electrical Engineer; O&M manual contractor; Facility Manager

---

### Step D: Warranty Period and Early Operations (Year 1–2)

**Action:**
1. Implement preventive maintenance schedule:

   | Interval | System | Tasks |
   |----------|--------|-------|
   | Monthly | Emergency power | Generator load test per CSA C282 / manufacturer recommendation |
   | Monthly | Electrical panels | Visual check for heat/odor/tripped breakers; IT room temperature/humidity check |
   | Monthly | Emergency lighting | Battery function test (especially bay locations with salt/corrosion exposure) |
   | Quarterly | Apparatus bay lighting | Clean fixture lenses (exhaust particulate accumulation reduces light levels) |
   | Quarterly | Controls | Zone override test; confirm all zones responding correctly |
   | Quarterly | Spare parts review | Verify LED driver inventory; replenish as needed |
   | Annually | Fire alarm | Professional testing per fire code; AHJ notification/approval for maintenance outage |
   | Annually | All electrical | Load analysis review; panel schedule accuracy audit; conduit spare locations confirmed in records |
   | Annually | IT/telecom | Review cabling documentation accuracy against as-built; confirm spare conduit locations |
   | Annually | Generator | Full service by certified technician; transfer switch inspection |

2. **Reconcile preventive maintenance intervals with manufacturer-specific recommendations** after equipment procurement is complete. The intervals listed in the table above (e.g., "quarterly bay fixture cleaning," "monthly generator load test") are pre-procurement estimates based on general industry practice. After actual equipment is selected and manufacturer O&M documentation is received, the Commissioning Agent or Facility Manager shall:
   - Compare each scheduled interval against the manufacturer's recommended maintenance intervals
   - Adopt the more conservative (shorter) interval where manufacturer recommendations differ from the generic schedule
   - Update the O&M manual preventive maintenance schedule to reflect manufacturer-specific intervals
   - Document any deviations from manufacturer recommendations with justification

   **ASSUMPTION: manufacturer-specific intervals will be available at or before commissioning. If equipment is procured without O&M documentation, escalate to the Electrical Engineer.** (Source: Semantic Lensing D-002)

3. Document all warranty claims and service responses.

4. Conduct 12-month post-occupancy review with Owner, Commissioning agent, and key service vendors:
   - System performance feedback from staff
   - Documentation adequacy review
   - Maintenance schedule adjustments based on actual operations experience
   - O&M manual updates

**Responsibility:** Facility Manager (lead); Service contractors; Commissioning agent

---

### Step E: Long-Term Operations (Year 2–50)

**Action:**
1. Continue preventive maintenance schedule from Step D with adjustments from Year 1 review.

2. Component replacement planning (schedule at commissioning, update annually):

   | Component | Estimated Replacement Interval | Planning Notes |
   |-----------|-------------------------------|----------------|
   | LED drivers/modules (office/storage) | Year 15–20 | Zone-by-zone replacement; use standardized type from Step 2 |
   | LED drivers/modules (apparatus bay) | Year 18–22 | Higher operating hours if bays active 16+ hr/day |
   | Cold Storage motion-activated fixtures | Year 15–20 | Cold cycling may accelerate degradation — monitor |
   | Fire alarm panel | Year 15–20 | Addressable architecture enables phased upgrade |
   | Access control hardware | Year 10–15 | Software/firmware updates more frequent; hardware separate |
   | IT network active equipment | Every 8–10 years | CAT6A cabling should outlast 3–4 equipment cycles |
   | Generator transfer switch | Year 15–20 | Major service or replacement |
   | Generator engine | Per manufacturer (major overhaul ~Year 20) | **ASSUMPTION: TBD based on selected equipment** |

3. Maintain documentation accuracy:
   - Update O&M manuals when components are replaced
   - Maintain panel schedule accuracy when circuits are added
   - Keep programming archives version-controlled (fire alarm and controls)
   - Annual documentation audit

4. Monitor code changes and implement required upgrades:
   - CEC edition updates (every 3–5 years; AHJ direction on applicability)
   - Fire code testing requirement changes
   - AHJ-directed electrical safety upgrades

5. Train replacement operations staff as staff turnover occurs; update training materials as systems are upgraded.

**Responsibility:** Facility Manager and operations staff; Contracted service companies

---

## Verification

### Narrative Production Verification

| Step | Verification |
|------|-------------|
| Step 1 complete | Requirements summary reviewed by Proposal Manager; RFP §7.1.4 scope and all Addendum 03 items confirmed |
| Step 2 complete | Standardization Matrix reviewed by Estimator for cost/parts alignment; lifecycle targets confirmed |
| Step 3 complete | Coordination meeting notes documented; discipline leads confirm design consistency; Addendum 03 items explicitly addressed |
| Step 4 complete | Outline reviewed against Decomposition DEL-05-04 scope definition (7 system areas confirmed) |
| Step 5 complete | Narrative cross-references validated against finalized DEL-02-05 drawings |
| Step 6 complete | All review comments addressed; Electrical Engineer final approval; OBJ-005 checklist passed |

**OBJ-005 Final Checklist (Step 6):**
- [ ] All seven system areas addressed (electrical panels, lighting, controls, IT/telecom, security/access control, fire alarm, emergency power)
- [ ] Solar-ready provisions addressed (Addendum 03 §1.17)
- [ ] Generator minimum loads addressed (Addendum 03 §1.15)
- [ ] Bay door secondary opening mechanism addressed (Addendum 03 §1.15)
- [ ] Bay sump moisture implications addressed (Addendum 03 §1.8)
- [ ] Bunker gear room ventilation electrical provisions addressed (Addendum 03 §1.13, §1.14)
- [ ] Security/camera supplier flexibility addressed (Addendum 03 §1.19)
- [ ] Cold Storage freeze-thaw environment addressed (cold-rated fixtures, freeze-proof provisions)
- [ ] Design-specific details integrated (no generic-only language)
- [ ] 50-year main building / 20-year Cold Storage design lives explicitly referenced
- [ ] Component standardization documented with specific zone category rationale
- [ ] Lifecycle and replacement intervals stated for each system
- [ ] Spare capacity strategy documented (panels + conduit + IT)
- [ ] O&M manual and training commitment stated
- [ ] Consistency with DEL-02-05, DEL-04-03, DEL-05-01, DEL-05-03 verified

### Operational Phase Verification

| Phase | Verification Method |
|-------|---------------------|
| Step A | Design drawings reviewed; spare capacity in panel schedule confirmed; cold-rating on Cold Storage fixtures confirmed; O&M manual outlines approved |
| Step B | As-built documentation complete; all labels installed and accurate; certification tests (fire alarm ULC, IT cabling TIA) completed; field changes documented |
| Step C | Commissioning test results documented for all systems; O&M manuals reviewed by Facility Manager; maintenance sequencing guide present and reviewed (per Guidance C-002); training attendance records complete; all deficiencies resolved |
| Step D | Preventive maintenance logs active; manufacturer-specific PM intervals reconciled and documented; quarterly bay fixture cleaning records; 12-month review completed; O&M manuals updated |
| Step E | Annual maintenance audit reports; documentation version control active; staff training records maintained; code-change assessments documented |

---

## Records

### Narrative Production Records

- Requirements summary document (internal)
- Standardization and Lifecycle Strategy Matrix
- Coordination meeting notes (architectural, mechanical, structural)
- Narrative outline and talking points
- Draft narrative with review comments
- Final approved electrical maintainability narrative
- Proposal integration confirmation (PDF compliance check)

### Operational Records

- **Design Phase:** Electrical drawings; panel schedules (with spare capacity documented); fixture schedules by zone; IT cabling design; solar rough-in pathway record; design approval records
- **Construction Phase:** As-built drawings (CAD DWG + PDF); commissioning test reports; certification records (fire alarm ULC; IT cabling TIA); cold-start test record (Cold Storage); change order documentation; contractor warranties
- **Commissioning Phase:** Complete O&M manuals (hard copy x2 and digital); training attendance records; Owner sign-off; deficiency list and resolution confirmation
- **Operations Phase:** Preventive maintenance logs; spare parts inventory records; service contracts; component replacement records; code upgrade records; annual audit reports; staff training records

---

## Notes

- **Integration Note:** The narrative produced in Steps 1–6 is one section of the PKG-005 suite. Consistency with DEL-05-01 (architectural), DEL-05-02 (structural), and DEL-05-03 (mechanical) maintainability narratives is essential — use the same design life values (50-yr main / 20-yr Cold Storage), the same facility zone terminology, and consistent references to generator/solar/access-control scope.
- **Addendum 03 Reference Numbering:** The source Addendum 03 document uses the following section numbers (confirmed from source PDF): §1.8 = bay sumps; §1.10 = 16 ft door heights; §1.13 = 40 bunker gear lockers; §1.14 = bunker gear room ventilation; §1.15 = generator; §1.16 = water fill stations; §1.17 = solar-capable roofing; §1.19 = security supplier preference. The decomposition references §1.13 for solar and §1.14 for security — these appear to be numbering discrepancies that should be resolved in the Compliance Matrix (DEL-01-01).
- **OBJ-005 Scoring:** Per RFP §8.3 scoring matrix (p. 27), an "Exceptional" score (100%, 15 pts) requires exceeding expectations and demonstrating clear understanding with certainty of success and a level of innovation. The narrative must be specific, credible, and operations-aware — not generic. The examples in EX-001 through EX-004 (Guidance.md) demonstrate the level of specificity expected.
- **RFP §7.1.1 Owner Preference:** The RFP §7.1.1 (p. 16) states the Owner desires "to keep operations and maintenance costs low with an efficient, cost-effective design solution." This is the underlying evaluator motivation for OBJ-005. The narrative should frame all maintainability decisions in terms of cost avoidance for the Owner.
