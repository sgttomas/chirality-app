# Electrical/IT Design Brief — Procedure

## Purpose

This procedure describes the **production process** for the Electrical/IT Design Brief (DEL-03-05), including prerequisites, key authoring steps, verification checkpoints, and records to be produced. The goal is a narrative document that satisfies all seven sub-topic requirements in RFP §7.1.2(5) and all OSR electrical/IT requirements (§§10.4, 10.5, 10.6) while aligning with Addendum 03 solar-readiness and generator requirements.

---

## Prerequisites

### Upstream Dependencies

| Dependency | Item | Responsible | Required Before |
|---|---|---|---|
| **Electrical/IT Concept Narrative** | DEL-02-05 (Electrical/IT Concept from PKG-002) | Electrical Engineer | Brief authoring (Step 2 onward); concept rationale is the foundation for brief justification |
| **Architectural Concept Package** | DEL-02-01 (Architectural Concept) | Architect | Step 8 (solar-readiness); needed to confirm roof orientation (flat/south/west/southwest per Addendum 03 §1.17) |
| **Mechanical Concept Narrative** | DEL-02-04 (Mechanical Concept) | Mechanical Engineer | Step 3 (power/generator); needed to confirm generator sizing, critical loads, and HVAC controls integration assumptions |
| **Functional Program** | RFP Appendix B | Available in RFP | Step 1 (context); source of zone-level program data for power and IT requirements |
| **Addendum 03** | All 21 Q&A items | Available in source folder | Step 1 (essential reading); §§1.6, 1.7, 1.15, 1.17 are directly binding on electrical/IT design |

### Accessible References

| Reference | Use | Location |
|---|---|---|
| **RFP Section 7.1.2(5)** | Defines Design Brief scope | Penhold PSB RFP 2024_004, p. 17 |
| **RFP OSR §10.4 — Electrical System** | Receptacles, grounding, future flexibility, door opener coordination | RFP 2024_004, p. 42 |
| **RFP OSR §10.5 — Lighting System** | IES standards, LED, emergency egress, weatherproof covers, fixture heights | RFP 2024_004, p. 42 |
| **RFP OSR §10.6 — IT/Telecommunications** | IT compatibility, 15-point meeting room, dispatch display, PA system | RFP 2024_004, p. 42 |
| **RFP OSR §10.3.9 — Roof and Door System** | Solar loading capability requirement | RFP 2024_004, p. 41 |
| **RFP OSR §12.3 — Access Control** | Multi-zone main structure; ancillary excluded; Additional Option pricing | RFP 2024_004, p. 44 |
| **RFP OSR §12.4 — Security and Camera** | Main structure; installation + monitoring priced separately; Additional Option | RFP 2024_004, p. 44 |
| **Addendum 03 §1.6** | Electrical service location (within a few feet of site) | Addendum 03, p. 3 |
| **Addendum 03 §1.7** | Site servicing cash allowance (electrical, water, wastewater, gas, comms) | Addendum 03, p. 3 |
| **Addendum 03 §1.15** | Backup generator critical loads; bay door secondary opening | Addendum 03, p. 4 |
| **Addendum 03 §1.17** | Solar-capable roofing required; flat/south/west/southwest orientation | Addendum 03, p. 4 |
| **Alberta Building Code** | Code compliance baseline | AHJ (specific sections TBD) |
| **Canadian Electrical Code (CEC), CSA C22.1** | National electrical standard (ASSUMPTION: applicable) | CSA (edition TBD) |
| **IES Lighting Standards** | Lighting level and fixture guidance (required by OSR §10.5) | IES (edition TBD) |

---

## Steps

### Step 1: Read Sources and Establish Design Context (Day 1)

**Owner:** Electrical Engineer

**Action:**
1. Read RFP §7.1.2(5) (p. 17) to confirm the exact seven sub-topic scope expected
2. Read RFP OSR §§10.4, 10.5, 10.6, 10.3.9, 12.3, 12.4 (pp. 41–44) — extract specific requirements by sub-topic
3. Read Addendum 03 §§1.6, 1.7, 1.15, 1.17 — record binding changes/requirements
4. Review DEL-02-05 (Electrical/IT Concept Narrative) for design decisions already made at concept stage
5. Confirm with Mechanical Engineer: generator sizing assumption, critical load list, bay door secondary opening strategy, HVAC controls integration approach (from DEL-02-04)
6. Confirm with Architect: roof orientation confirmed (flat/south/west/southwest per Addendum 03 §1.17)
7. Create a brief outline with one heading per sub-topic; list the specific RFP/Addendum requirements under each heading as a drafting checklist

**Verification Checkpoint:**
- Source checklist complete: all seven OSR sections read; Addendum 03 §§1.6/1.7/1.15/1.17 captured
- Dependencies confirmed: generator sizing assumption from DEL-02-04; roof orientation from DEL-02-01

**Record:** Brief outline with requirement checklist; coordination confirmation notes

---

### Step 2: Draft Power Distribution and Site Service Tie-In (Day 2)

**Owner:** Electrical Engineer

**Content to Address:**
- **Service connection:** Electrical service is within a few feet of the site per Addendum 03 §1.6; site servicing tie-in (electricity, communication) covered under cash allowance per Addendum 03 §1.7 — state this clearly
- **Main distribution:** Main service capacity, transformer sizing approach, distribution panel location (accessible for maintenance per OSR §10.4)
- **Receptacles:** Interior and exterior receptacle placement; coordination with mechanical (overhead door openers per OSR §10.4)
- **Future flexibility:** Service sized to accommodate future equipment additions and solar provisions (OSR §10.4 states "allow for future flexibility")
- **Grounding:** Grounding approach per code; note that design meets AHJ requirements

**Writing Guidance:** Anchor every statement to a source. "Service within a few feet of site (Addendum 03 §1.6); site tie-in under cash allowance (Addendum 03 §1.7)" is the correct format.

**Verification Checkpoint:**
- Site servicing cash allowance approach stated (not priced in proposal per Addendum 03 §1.7)
- Interior and exterior receptacles confirmed
- Mechanical coordination (door openers) noted

**Record:** Draft section; confirmation of mechanical coordination assumption for door openers

---

### Step 3: Draft Emergency Backup Power and Generator Strategy (Day 2–3)

**Owner:** Electrical Engineer (with Mechanical Engineer input)

**Content to Address:**
- **Critical loads (mandatory per Addendum 03 §1.15):** Kitchen; meeting room/ICP; two bathrooms; bay door secondary opening mechanism
- **Bay door secondary opening:** State choice — generator-powered OR manual (both acceptable per Addendum 03 §1.15). State rationale for choice.
- **Generator capacity:** Reference DEL-02-04 for generator sizing; state capacity assumption and label as ASSUMPTION if DEL-02-04 not yet finalized
- **Transfer switching:** Automatic transfer switching with appropriate transfer delay; load shedding of non-critical loads on generator start
- **Load shedding:** Which loads shed when generator activates (e.g., office lighting, non-essential HVAC zones)
- **Coordination:** Reference Mechanical Concept (DEL-02-04) explicitly; confirm no contradictions in critical load list

**Writing Guidance:** State the exact critical load list from Addendum 03 §1.15 verbatim, then explain the design approach for each load. Do not omit or reinterpret the Addendum 03 critical load list.

**Verification Checkpoint:**
- All four Addendum 03 §1.15 critical loads appear in draft
- Bay door secondary opening strategy (generator-powered or manual) is stated with rationale
- Generator capacity is either confirmed from DEL-02-04 or labeled ASSUMPTION
- No contradiction between this section and DEL-02-04 generator sizing

**Record:** Draft section; generator capacity assumption documented

---

### Step 4: Draft Lighting Design Approach (Day 3–4)

**Owner:** Electrical Engineer

**Content to Address:**
- **IES compliance:** State that lighting follows IES recommendations per RFP OSR §10.5
- **LED specification:** Energy-efficient LED throughout all buildings; state rationale (energy, lamp life, heat reduction in bays)
- **Emergency egress lighting:** Emergency exit lights above personal doors with internal batteries per code and RFP OSR §10.5
- **Weatherproof provisions:** Switches at person doors of ancillary buildings (cold storage) have weatherproof covers per RFP OSR §10.5
- **Fixture heights:** Heights adjusted to avoid interference with machinery per RFP OSR §10.5 (apparatus: type 1 engines/ladders; public works: graders, tandem trucks, loaders)
- **Lighting controls and zones:** Occupancy sensors in intermittent-use zones (apparatus bays, storage); scheduling in office/common areas; zone strategy for different operational profiles (fire, public works, shared)
- **Color temperature:** Recommend 3000–3500K range; explain rationale
- **Ancillary buildings:** Lighting for cold storage building includes weatherproof covers; fixture heights accommodate potential vehicle/equipment storage

**Writing Guidance:** Cite OSR §10.5 for each requirement. Distinguish between code-minimum compliance and beyond-code choices (e.g., occupancy controls, color temperature selection).

**Verification Checkpoint:**
- IES compliance stated; LED throughout confirmed
- Emergency exit light approach confirmed (above person doors, internal battery)
- Weatherproof switches confirmed for ancillary buildings
- Fixture heights for machinery clearance addressed
- LED energy efficiency narrative connects to DEL-04-03

**Record:** Draft section; lighting zone map assumption (may be sketch or table)

---

### Step 5: Draft Building Controls Strategy (Day 4–5)

**Owner:** Electrical Engineer (Mechanical Engineer input on HVAC integration)

**Content to Address:**
- **Controls architecture:** Choose centralized (BACnet/Modbus network) or distributed (independent controls); state rationale
- **Integration scope:** HVAC controls (heating, cooling, ventilation zones), lighting controls (occupancy sensors, scheduling), security system integration (door lock coordination with access control)
- **Overhead door openers:** Electrical coordination with mechanical (required by RFP OSR §10.4)
- **Dispatch display system coordination:** Building automation may integrate with or be separate from dispatch display
- **Monitoring and diagnostics:** What can facility manager observe/control remotely? Alert system for failures (generator alarm, exhaust fan failure)
- **Solar monitoring provision:** If centralized controls are chosen, note provision for future solar production monitoring (connects to solar-readiness narrative)

**Writing Guidance:** The choice of centralized vs. distributed must be stated explicitly — "we recommend [X] because [Y]" — not left open. The evaluator needs to assess the approach.

**Verification Checkpoint:**
- Controls architecture choice is stated with rationale
- HVAC integration confirmed with Mechanical Engineer
- Overhead door opener coordination addressed (per OSR §10.4)
- Fire alarm integration addressed (HVAC shutdown on alarm)

**Record:** Draft section; controls architecture decision documentation

---

### Step 6: Draft IT Infrastructure and Telecommunications (Day 5–6)

**Owner:** Electrical Engineer (IT Consultant input if available)

**Content to Address — all items from RFP OSR §10.6:**
1. **IT/data compatibility throughout main structure** — structured cabling approach; CAT6 (minimum) to all major spaces
2. **Meeting room/ICP: 15 concurrent internet access points for Emergency Management** — explicitly state this provision; explain WAP placement and network architecture
3. **Apparatus bay dispatch display system** — wall-mounted display in apparatus bay closest to office; designed for dispatch data connection (mounted TV with laptop/hardware as described in OSR §10.6); power and data cabling to location
4. **PA system** — throughout main structure only (not ancillary buildings per OSR §10.6)

**Additional content:**
- Network closet / IDF location and UPS backup for core networking equipment
- Cellular backup or redundant WAN connection (for emergency dispatch continuity)
- Video/CCTV cabling infrastructure (base scope; camera equipment is Additional Option 12.4)

**Writing Guidance:** Address all four OSR §10.6 requirements by item. These are specific, numbered requirements — missing one will be visible to the evaluator.

**Verification Checkpoint:**
- IT/data throughout main structure: confirmed
- 15 concurrent access points in meeting room: explicitly stated
- Dispatch display in apparatus bay (closest to office): confirmed; power and data provision noted
- PA system (main structure only): confirmed

**Record:** Draft section; IT infrastructure location assumptions

---

### Step 7: Draft Access Control and Security System Design Approach (Day 6–7)

**Owner:** Electrical Engineer (Access Control/Security Consultant input if available)

**Content to Address:**
- **Scope delineation (critical):**
  - Base scope: Power, data cabling, and conduit infrastructure to support access control and security systems
  - Additional Option 12.3: Access control equipment and installation (main structure, multiple zones, shared space use, interdepartmental access per OSR §12.3)
  - Additional Option 12.4: Security/camera equipment, installation, and monitoring costs (main structure interior and exterior per OSR §12.4)
- **Zones covered:** Multi-zone main structure (examples: main entrance, apparatus bay, meeting room/ICP, staff areas, shared zones); ancillary buildings explicitly excluded per OSR §12.3
- **Fail-safe/fail-secure strategy:** What happens to locks during power failure or fire alarm? Life safety override (fire alarm unlocks all doors for egress)
- **Monitoring cost separation:** OSR §12.4 requires installation costs and monitoring costs priced separately

**Writing Guidance:** The base/optional distinction must be unambiguous. Use a table if necessary. Do not conflate base electrical infrastructure (in base contract) with Additional Option equipment/installation.

**Verification Checkpoint:**
- Base vs. Optional 12.3/12.4 scope boundary is explicit
- Ancillary building exclusion from access control confirmed (OSR §12.3)
- Life safety override (fire alarm) addressed
- Monitoring costs priced separately confirmed (OSR §12.4)

**Record:** Draft section; scope delineation table

---

### Step 8: Draft Fire Alarm System Design Approach (Day 7–8)

**Owner:** Electrical Engineer (Fire Protection Consultant input if available)

**Content to Address:**
- **System type:** Addressable (point-by-point detection) vs. conventional (zone-based); state choice and rationale
- **Detection devices:** Smoke detectors, heat detectors, manual pull stations; locations per code
- **Notification:** Audible/visual notification devices in all areas including apparatus bays; connection to fire dispatch (appropriate for a fire station)
- **Backup power:** UPS/battery backup for fire alarm panel and notification devices (code-required)
- **Building integration:** Fire alarm triggers HVAC shutdown (smoke management); unlocks all doors (life safety override for access control)
- **Annual inspection and testing protocol:** Reference to code requirements

**Writing Guidance:** Fire alarm is a life safety system — non-negotiable. The brief should demonstrate the team understands the requirements and integrates fire alarm with the broader building controls strategy.

**Verification Checkpoint:**
- System type stated; backup power confirmed
- Integration with HVAC (shutdown) and access control (door unlock) stated
- Cross-consistency verified: fire alarm integration statements in this section (Step 8) are consistent with building controls content drafted in Step 5 (HVAC shutdown triggers) and access control content drafted in Step 7 (door unlock on alarm); any discrepancies in trigger logic, device references, or scope boundaries are reconciled before proceeding
- Life safety provisions are code-compliant (state compliance pathway)

**Record:** Draft section; life safety compliance statement

---

### Step 9: Draft Solar-Readiness Provisions (Day 8–9)

**Owner:** Electrical Engineer (with Architect confirmation of roof orientation)

**Content to Address — all items required by Addendum 03 §1.17 and OSR §10.3.9:**
- **Roof orientation:** Confirm flat/south/west/southwest per Addendum 03 §1.17; reference DEL-02-01 for Architect's confirmed orientation
- **Solar loading in roof structure:** OSR §10.3.9 requires solar loading capability; confirm structural provision (reference DEL-03-03 Structural Brief if relevant)
- **Electrical infrastructure (base contract):**
  - Conduit runs from roof to electrical room (sized for future solar inverter and disconnect wiring)
  - Reserved panel space for future solar breaker and metering
  - Disconnects and overcurrent protection sized to accommodate future solar capacity (TBD kW — state assumption if needed)
  - Sub-metering provision for solar production tracking (net metering with utility)
- **What is NOT in base contract:** Solar equipment (panels, inverter, racking) and installation — explicit statement required
- **Future Owner benefit:** Quantify or describe the cost advantage: pre-positioned infrastructure means future solar retrofit requires minimal new construction

**Writing Guidance:** This section answers a mandatory Addendum 03 §1.17 requirement. Use the four-part structure: roof orientation confirmed; structural provision referenced; electrical infrastructure listed; solar equipment excluded from base scope.

**Verification Checkpoint:**
- Addendum 03 §1.17 solar-ready requirement explicitly acknowledged
- Roof orientation confirmed with Architect (DEL-02-01)
- Four infrastructure elements (conduit, panel space, disconnects, sub-meter) stated
- Solar equipment exclusion from base contract explicitly stated

**Record:** Draft section; Owner phasing clarification statement

---

### Step 10: Integration Review and Cross-Reference Check (Day 9–10)

**Owner:** Electrical Engineer (peer review by Lead Architect/Design Manager)

**Action:**
1. **Cross-check with Concept (DEL-02-05):** Every design decision in the brief traces to concept narrative or expands on it; no contradictions
2. **Cross-check with Mechanical Brief (DEL-03-04):** Generator integration, overhead door openers, HVAC controls — confirm no conflicts
3. **Cross-check with Energy Efficiency (DEL-04-03):** LED lighting, controls, solar-ready infrastructure — confirm consistency
4. **Cross-check with Maintainability (DEL-05-04):** Panel access, fixture standardization, documentation — confirm consistency
5. **Review all seven sub-topic sections against RFP §7.1.2(5) and OSR §§10.4/10.5/10.6 checklist** — verify no requirement omitted
6. **Addendum 03 compliance check:** Verify §§1.6, 1.7, 1.15, 1.17 are each addressed in the brief
7. **Scope clarity check:** Base contract vs. Additional Option 12.3/12.4 distinctions are unambiguous throughout
8. **Internal document consistency check:** Verify that Datasheet attributes are consistent with Specification requirements — e.g., Datasheet "Backup Generator Capacity" attribute matches R-05 critical load list and generator capacity assumption; Datasheet "Solar Readiness" attribute matches R-06 provisions; Datasheet "Fire Alarm" attributes align with R-01 sub-topic coverage; Datasheet "Cold Storage Building Electrical Scope" matches Specification scope exclusions for ancillary buildings

**Verification Checkpoint:**
- No contradictions between brief and Concept narrative (DEL-02-05)
- Addendum 03 §§1.6/1.7/1.15/1.17 compliance verified
- All OSR §10.4/10.5/10.6 requirements addressed
- Internal consistency confirmed: Datasheet attributes match Specification requirements (generator capacity, solar readiness, fire alarm scope, cold storage electrical scope)
- Conflict Table populated for unresolved items; escalated to Lead Architect/PM if needed

**Record:** Cross-reference compliance matrix; Conflict Table (if conflicts exist)

---

### Step 11: Finalization and Approval (Day 10–11)

**Owner:** Electrical Engineer; Review Authority: Lead Architect / Design Manager

**Action:**
1. Incorporate feedback from Step 10 peer review
2. Confirm all seven sub-topic narrative sections are complete and professionally written
3. Confirm all ASSUMPTION labels are present where needed; all TBDs are documented in the Specification
4. Confirm scope delineation tables for Additional Option 12.3/12.4 are clear
5. Proofread for clarity, consistency, and professional tone appropriate for municipal proposal submission
6. Obtain Design Manager or Lead Architect sign-off
7. Package brief for inclusion in PKG-003 proposal submission

**Verification Checkpoint:**
- All seven sub-topics complete
- Addendum 03 compliance confirmed by checklist
- Additional Option 12.3/12.4 scope boundaries explicit
- Four-document structure (Datasheet, Specification, Guidance, Procedure) and narrative body all present
- No significant unresolved TBDs (minor location references acceptable)
- Narrative quality assessment: brief is persuasive to a non-specialist evaluation committee and demonstrates design team competence. Apply self-assessment criteria from Guidance Purpose section: (a) each section explains *why*, not just *what*; (b) a non-specialist evaluator would understand the operational benefit; (c) cross-discipline coordination is demonstrated, not just stated; (d) all seven sub-topics have source-anchored rationale, not generic statements. If any criterion is not met, the corresponding section requires strengthening before approval.

**Record:** Final brief document; approval sign-off with date; deferred decisions documented

---

## Verification Summary

| Step | Checkpoint | Evidence |
|---|---|---|
| 1 | Source reading complete; outline drafted; dependencies confirmed | Outline doc; coordination notes |
| 2 | Power distribution and site tie-in drafted; cash allowance approach stated | Draft section |
| 3 | Generator critical loads (Addendum 03 §1.15) confirmed; bay door strategy stated | Draft section; generator capacity assumption |
| 4 | Lighting: IES, LED, emergency egress, weatherproof, heights all addressed | Draft section |
| 5 | Building controls architecture stated; HVAC/door opener coordination confirmed | Draft section |
| 6 | IT/telecom: 4 OSR §10.6 requirements each addressed by item | Draft section |
| 7 | Access control/security: base vs. optional 12.3/12.4 scope explicit | Draft section; scope table |
| 8 | Fire alarm: system type stated; backup power and integrations confirmed; cross-consistency with Step 5 and Step 7 verified | Draft section |
| 9 | Solar-readiness: orientation confirmed; 4 infrastructure items listed; equipment excluded | Draft section |
| 10 | Cross-reference check complete; Addendum 03 compliance verified; internal Datasheet-Specification consistency confirmed | Compliance matrix; Conflict Table |
| 11 | Final brief complete; narrative quality assessed for persuasiveness; approved | Final document; sign-off |

---

## Records to Be Produced

| Record | Format | Owner | Timing |
|---|---|---|---|
| **Electrical/IT Design Brief (Full Narrative)** | Narrative document (7 sub-topics) | Electrical Engineer | Day 11 (final) |
| **Brief Outline with Requirement Checklist** | Document | Electrical Engineer | Day 1 |
| **Generator Critical Load Assumption** | Documented assumption (capacity + basis) | Electrical Engineer | Day 3 |
| **Controls Architecture Decision Record** | Paragraph or short memo | Electrical Engineer | Day 5 |
| **Solar-Readiness Scope Statement** | Paragraph embedded in brief | Electrical Engineer | Day 9 |
| **Base vs. Optional Scope Table (12.3/12.4)** | Table embedded in brief | Electrical Engineer | Day 7 |
| **Addendum 03 Compliance Checklist** | Table (§§1.6/1.7/1.15/1.17 vs. brief sections) | Electrical Engineer | Day 10 |
| **Cross-Reference Compliance Matrix** | Table | Electrical Engineer | Day 10 |
| **Conflict Table** | Table (if conflicts identified) | Electrical Engineer | Day 10 (only if needed) |
| **Approval Sign-Off** | Email or formal sign-off | Design Manager / Lead Architect | Day 11 |

---

## Notes

- **Addendum 03 §1.15 is critical.** The backup generator critical load list (kitchen, meeting room/ICP, 2 bathrooms, bay door secondary opening) is explicit and mandatory. Bay door secondary opening is explicitly flexible — both generator-powered and manual are acceptable. The brief must state the choice.
- **OSR §10.6 has four specific requirements** that must each be addressed: (1) IT/data throughout, (2) 15 concurrent access points for Emergency Management in meeting room, (3) dispatch display in apparatus bay closest to office, (4) PA system in main structure only.
- **Timeline:** Estimated 10–11 working days for Electrical Engineer with coordination from Mechanical, Architect. Actual duration depends on availability of DEL-02-04 (generator sizing) and DEL-02-05 (concept rationale).
- **ASSUMPTION:** Electrical Engineer is the author; peer review by Lead Architect/Design Manager. No dedicated fire alarm, access control, or IT specialist required unless team elects to engage one.
- **Location TBD:** IES edition, CEC (CSA C22.1) edition applicable in Alberta, and specific ABC sections require access to current standards for exact citation in final brief.
