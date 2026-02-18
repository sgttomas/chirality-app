# Procedure: Building Envelope and Energy Strategy

## Purpose

This procedure describes the steps required to **produce** the Building Envelope and Energy Strategy narrative document (DEL-04-01). It is intended for the Architect and Building Science Consultant responsible for developing the envelope strategy during the Design Brief phase of the Penhold PSB proposal.

The output of this procedure is a narrative section suitable for inclusion in the proposal Design Brief package, covering the building energy philosophy, thermal performance targets, air barrier approach, thermal bridging mitigation, energy code compliance pathway, and solar-ready provisions per Addendum 03.

---

## Prerequisites

### Required Inputs

| Input | Source | Status |
|-------|--------|--------|
| RFP 2024_004 (base document) | `test/execution-6b/_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf` | Available |
| Addendum 03 (Jul 31, 2024) | `test/execution-6b/_Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf` | Available |
| OSR (Appendix A of RFP) | Embedded in RFP document | Available via RFP; specific sections location TBD |
| NECB (current edition) | National Research Council Canada | Location TBD -- must be sourced by Building Science Consultant |
| Addendum 01 and 02 | Available in `_Sources/` | Available |
| Site orientation data for Penhold, AB | Climate data source; approximately 52.4°N, 113.9°W | ASSUMPTION: Building Science Consultant to obtain heating degree days, solar radiation, wind data |
| Architectural footprint / roof orientation | From DEL-02-01 (Architectural Concept Package) | In parallel production; coordinate with Architect |
| In-progress narratives: DEL-04-02, DEL-04-03 | PKG-004 sister deliverables | In parallel production |
| Decomposition v2.3 FINAL | `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | Available |

### Required Knowledge

- Building envelope design fundamentals: thermal resistance, air barriers, vapor management, moisture control
- Cold-climate building design: freeze-thaw cycling, infiltration, condensation risk, thermal bridging
- NECB compliance pathways: prescriptive and performance (at a sufficient level to select and document the approach)
- Thermal bridging concepts and mitigation strategies (continuous insulation, thermal breaks)
- Solar-ready design requirements: roof orientation, structural loading, mechanical/electrical rough-in
- Technical writing: clear, concise narrative for Design Brief evaluators (non-specialist audience)

### Upstream Dependencies (Declared)

None declared in `_DEPENDENCIES.md`. However, effective production of this narrative requires:
- Architectural roof orientation and building footprint from DEL-02-01 (to confirm solar-ready alignment per Addendum 03)
- Preliminary HVAC system approach from DEL-04-02 (to coordinate airtightness and load assumptions)

These are parallel coordination dependencies, not blocking upstream requirements.

---

## Steps

### Step 1: Establish Building Energy Philosophy

**Objective:** Define the overarching design intent that will frame all envelope strategy choices.

**Actions:**
1. Convene coordination meeting with Architect, Building Science Consultant, Mechanical Engineer, and Electrical Engineer (or leads for DEL-04-02 and DEL-04-03)
2. Agree on three foundational questions:
   - What is the primary energy goal? (e.g., "Achieve NECB + 20% with minimal lifecycle cost")
   - What is the climate adaptation strategy? (e.g., "Heating-dominated; exploit south solar gain; minimize infiltration")
   - What does the 50-year design life require from the envelope? (e.g., "Durable, maintainable, serviceable materials; no hidden moisture traps")
3. Document the philosophy in 2-4 sentences -- enough to orient all subsequent decisions
4. Flag any conflicts between philosophy and Addendum 03 requirements (e.g., flat roof vs. solar-ready orientation) for early resolution

**Output:** Philosophy statement (2-4 sentences) to open the narrative document

**Timing:** First week of Design Brief production

---

### Step 2: Confirm Thermal Performance Targets

**Objective:** Set R-value and U-value targets for walls, roof, and glazing that satisfy NECB minimum and align with the project energy philosophy.

**Actions:**
1. Obtain NECB prescriptive minimum R-values for Alberta Climate Zone (ASSUMPTION: Zone 6 or equivalent; confirm with Building Science Consultant using NECB tables)
2. Set project targets above NECB minimums, using Guidance T-001 trade-off analysis as a reference:
   - Walls: target NECB minimum + 20-30% (approximately R-40 to R-50 effective, depending on assembly)
   - Roof: target NECB minimum + 20-30% (approximately R-49 to R-60 above-deck, depending on assembly)
   - Glazing: differentiate by the standard four-category orientation classification -- **south, east, west, north** (south: high SHGC double low-E; north: low SHGC double low-E; east/west: consider triple low-E) [Ref: Semantic Lensing C-002]
3. Confirm feasibility of targets with Architect based on wall thickness and architectural intent
4. Document targets in a table with: assembly, NECB minimum, project target, assumed assembly approach, and justification

**Output -- Thermal Performance Target Table:**

| Assembly | NECB Minimum (ASSUMPTION) | Project Target | Assembly Approach | Justification |
|----------|--------------------------|----------------|------------------|---------------|
| Above-grade walls | Confirm from NECB | R-40 to R-50 effective | Cavity + continuous exterior insulation | Exceeds NECB; 50-yr life; cold climate |
| Roof (above-deck) | Confirm from NECB | R-49 to R-60 | Above-deck rigid foam + membrane | Solar-ready load provisions require above-deck |
| Glazing -- south | Confirm from NECB | U-0.22 to U-0.28; SHGC 0.50+ | Double low-E, high solar gain | Passive solar contribution |
| Glazing -- east | Confirm from NECB | U-0.22 to U-0.28; SHGC 0.25 to 0.35 | Double or triple low-E, low solar gain | Minimize unproductive heat loss; consider triple glazing |
| Glazing -- west | Confirm from NECB | U-0.22 to U-0.28; SHGC 0.25 to 0.35 | Double or triple low-E, low solar gain | Minimize unproductive heat loss; consider triple glazing |
| Glazing -- north | Confirm from NECB | U-0.22 to U-0.28; SHGC 0.25 to 0.35 | Double low-E, low solar gain | Minimize heat loss; minimal solar gain available |

**Timing:** First two weeks of Design Brief production

---

### Step 3: Define Air Barrier Strategy

**Objective:** Select and document the air barrier system location, material, airtightness target, and continuity approach.

**Actions:**
1. Evaluate the three air barrier options in Guidance C-002 (outer membrane, inner structural, hybrid)
2. For Penhold PSB with 50-year design life, assess trade-offs:
   - Inner structural air barrier (Option B) is recommended for long-term durability and public building context -- ASSUMPTION
   - Hybrid approach (Option C) provides redundancy; useful for complex envelope geometries
3. Set airtightness target:
   - NECB prescriptive minimum: confirm from NECB (location TBD); ASSUMPTION approximately ACH50 < 5.0
   - Project target: ACH50 < 3.5 (balancing performance and durability, per Guidance T-002)
4. Document continuity strategy at critical transitions:
   - Wall-to-foundation: inner air barrier membrane wrapped and lapped to foundation dampproofing
   - Wall-to-roof: inner air barrier extended to roof deck and sealed at plate
   - Window/door perimeters: pre-formed gaskets and polyurethane sealant at all frames
   - Mechanical/electrical penetrations: pre-insulated sleeve with gasket or wrap sealant
   - Cold Storage zone boundary: dedicated air barrier layer at conditioned/unconditioned transition
5. Coordinate airtightness target with Mechanical Engineer (DEL-04-02): confirm that HRV or ventilation system is sized assuming ACH50 < 3.5 infiltration baseline

**Output:** Air Barrier Strategy statement covering location, material, target, and continuity at all critical transitions

**Timing:** Second week of Design Brief production

---

### Step 4: Identify and Plan Thermal Bridging Mitigation

**Objective:** Map primary thermal bridge locations and commit to mitigation strategies.

**Actions:**
1. Walk through the building envelope systematically, using the Guidance C-003 table as a checklist
2. For each major bridge location, assign a severity rating and a mitigation approach:
   - Wall-to-foundation: continuous exterior insulation lapped below grade; thermal break at slab edge (HIGH severity)
   - Wall-to-roof eave: exterior insulation continuous past roof junction; minimize structural exposure (HIGH severity)
   - Window/door frames: thermally broken aluminum frames; insulated reveal at jamb and sill (MEDIUM-HIGH severity)
   - Mechanical roof penetrations: pre-insulated sleeves; conduit in conditioned space where possible (MEDIUM severity)
   - Cold Storage boundary wall: continuous insulation and vapor management at conditioned/unconditioned transition (HIGH severity)
3. State the overarching performance objective: "Thermal bridge impact to be limited to less than 10% additional heat loss versus ideal uniform wall assembly -- ASSUMPTION; to be verified by thermal modeling (THERM or equivalent) at Design Development phase"
4. Document which bridges will require detailed thermal modeling in Design Development (deferred action items)

**Output:** Thermal Bridge Mitigation table (key locations, severity, mitigation approach, verification plan) for inclusion in the narrative

**Timing:** Second to third week of Design Brief production

---

### Step 5: Establish Energy Code Compliance Pathway

**Objective:** Select and document the NECB compliance method and key assumptions.

**Actions:**
1. Confirm with Project Manager and AHJ which edition of NECB applies (ASSUMPTION: current edition; confirm edition year during Design Development)
2. Select compliance method:
   - **Prescriptive path (recommended for Design Brief stage):** Match NECB table minimums for wall, roof, and glazing; document table references; no energy modeling required
   - **Performance path (advanced):** Requires energy modeling tool and specialist time; provides trade-off flexibility
3. If prescriptive path selected:
   - Cross-check thermal targets from Step 2 against NECB prescriptive tables
   - Document the compliance claim: "Proposed envelope targets [wall R-xx, roof R-xx, glazing U-xx] equal or exceed NECB [edition] prescriptive minimums for Climate Zone [x]"
   - State the verification plan: "NECB compliance checklist to be completed during Design Development phase"
4. If performance path selected:
   - Identify modeling tool (HOT2000, EnerGuide, DOE-2, or equivalent)
   - Define baseline building per NECB requirements
   - Allocate energy modeling resource in Design Development schedule
5. State the quantified energy performance target (per R-ENV-006): even if precise modeling is deferred, provide a target range (e.g., "design targets 15-20% below NECB baseline energy consumption" -- ASSUMPTION based on proposed envelope performance increments)

**Output:** Compliance pathway statement covering: code identified, method selected, key assumptions, verification timeline, and quantified energy target

**Timing:** Third week of Design Brief production

---

### Step 6: Address Solar-Ready Provisions (Addendum 03)

**Objective:** Document building envelope contributions to Addendum 03 solar-ready requirements.

**Actions:**
1. Confirm roof orientation from Architectural concept (DEL-02-01): is roof oriented south, southwest, west, or flat per Addendum 03?
   - If yes: document as compliant with Addendum 03 orientation requirement
   - If not: identify alternative solar-ready surface and document rationale
2. Confirm or establish structural roof loading allowance for future solar array:
   - Target: TBD kPa superimposed dead load capacity at designated solar zones -- ASSUMPTION; previously stated as 1.0-1.5 kPa but inconsistent with Guidance P-005 (50-100 kg/m2) and EX-002 (1.5 kPa / ~150 kg/m2); see CONF-ENV-04 in Guidance Conflict Table; Structural Engineer to confirm a single design value [Ref: Semantic Lensing B-003]
   - Document as a design constraint for the structural brief (DEL-02-03 and DEL-03-03)
3. Coordinate with DEL-04-02 (Mechanical) on mechanical rough-in:
   - Conduit route from mechanical room to roof (minimum 25 mm, with pull string)
   - Connection points at roof (capped and protected by roof membrane)
   - Any drain or water routing for solar thermal application
4. Coordinate with DEL-04-03 (Electrical) on electrical rough-in:
   - Conduit route from electrical room to roof (minimum 38 mm, with pull string)
   - Spare breaker capacity in main electrical panel for future PV inverter
   - Inverter location designated in electrical room
5. Protect roof membrane at future solar racking attachment zones (pre-flash or protection pad detail)
6. Document all provisions in the narrative with explicit reference to Addendum 03

**Output:** Solar-ready provisions summary with: orientation confirmation, structural loading assumption, mechanical rough-in description (reference to DEL-04-02), electrical rough-in description (reference to DEL-04-03), and Addendum 03 compliance statement

**Timing:** Third to fourth week of Design Brief production; concurrent with Step 5

---

### Step 7: Coordinate with DEL-04-02 and DEL-04-03

**Objective:** Ensure envelope strategy is internally consistent with the mechanical and electrical narratives produced in parallel.

**Actions:**
1. Share the following with the DEL-04-02 (Mechanical) lead:
   - Confirmed airtightness target (ACH50)
   - Wall and roof R-values (heating/cooling load implications)
   - Glazing SHGC by orientation (solar heat gain assumptions)
   - Infiltration rate baseline (for mechanical ventilation and HRV sizing)
2. Receive from the DEL-04-02 (Mechanical) lead:
   - HRV efficiency assumption and any required infiltration baseline change
   - HVAC system type and sizing approach (validates envelope load reduction benefit)
   - Domestic hot water and heating system selection (may affect envelope targets)
3. Share the following with the DEL-04-03 (Electrical) lead:
   - Solar-ready roof area, structural loading assumption, and conduit routing strategy
   - Daylighting approach (windows and glazing area assumptions)
4. Receive from the DEL-04-03 (Electrical) lead:
   - LED lighting efficacy and approximate internal heat gain (affects cooling load)
   - Solar PV array capacity and panel layout assumption (confirms structural loading)
   - Any conflicts in solar-ready conduit routing or panel space allocation
5. Document coordination exchange in a **coordination memo** retained in project files. The memo must include the following minimum content: [Ref: Semantic Lensing A-003]
   - **Date** of coordination exchange
   - **Attendees** (names and roles/deliverable responsibilities)
   - **Assumptions shared** (list each assumption communicated, with value and units where applicable)
   - **Feedback received** (summary of responses, questions, or revisions requested by MEP leads)
   - **Action items** (specific follow-up tasks, responsible party, and due date for each)
   - **Agreed changes** (any modifications to envelope targets, airtightness assumptions, or solar-ready provisions resulting from feedback)
6. Update the envelope narrative to reflect any agreed changes from MEP feedback

**Output:** Coordination memo (per format above) documenting assumptions shared and feedback received; updated envelope narrative if changes result

**Timing:** Ongoing from Week 2 through Week 4 (concurrent with Steps 2-6)

---

### Step 7A: Draft Quality Review Gate [Ref: Semantic Lensing D-002]

**Objective:** Conduct a formal quality review of the draft narrative before final assembly to confirm completeness and consistency against the Specification verification checklists.

**Actions:**
1. Compile all draft outputs from Steps 1-7 into a preliminary draft narrative document
2. Conduct a structured review of the draft against:
   - **V-001 Completeness Check** (all required sections present and populated; TBD items identified)
   - **V-002 Cross-Document Consistency Check** (alignment with DEL-04-02, DEL-04-03, DEL-05-01 in-progress content)
   - **V-003 Specification Requirements Check** (each R-ENV requirement addressed)
3. Identify all gaps, inconsistencies, or unresolved TBDs and document them in a draft review findings list
4. Circulate the draft and findings list to:
   - Architect / Design Lead (for design intent and coordination review)
   - Building Science Consultant (for technical accuracy review)
5. Allow reviewers a minimum of 2 business days for review
6. Collect reviewer comments and resolve findings before proceeding to Step 8

**Output:** Reviewed draft narrative with all reviewer comments addressed or explicitly deferred to Design Development; draft review findings list with resolution status for each item

**Gate Criterion:** Draft may proceed to Step 8 (final assembly) only when:
- All V-003 Specification Requirements are either satisfied or have documented TBD items with a clear path to resolution
- No unresolved cross-document conflicts remain (or conflicts are captured in the Conflict Table with a resolution timeline per the Conflict Resolution Process)
- Both the Architect/Design Lead and Building Science Consultant have provided written acknowledgment that the draft is ready for final assembly

**Timing:** End of Week 3 / beginning of Week 4 (after coordination in Step 7, before final assembly in Step 8)

---

### Step 8: Write and Assemble Final Narrative

**Objective:** Produce the final, formatted narrative document ready for Design Brief submission.

**Actions:**
1. Consolidate outputs from Steps 1-7 into a structured narrative with these sections:
   - Building Energy Philosophy (from Step 1)
   - Climate Adaptation and Energy Performance Targets (from Steps 2 and 5)
   - Thermal Performance Strategy -- Walls, Roof, Glazing (from Step 2)
   - Air Barrier System Design (from Step 3)
   - Thermal Bridging Mitigation (from Step 4)
   - Energy Code Compliance Pathway (from Step 5)
   - Integration with Mechanical Systems (from Step 7, referencing DEL-04-02)
   - Solar-Ready Provisions and Electrical Integration (from Steps 6 and 7, referencing DEL-04-03 and Addendum 03)
   - Cold Storage Envelope Considerations (special section; document separately from main building)
   - Forward: Design Development Phase Requirements (what is deferred)
2. Apply house style: clear headings; tables for thermal targets, air barrier, and thermal bridge mitigation; concise prose; no jargon without definition
3. Mark all inferred or estimated content clearly (ASSUMPTION label, TBD for deferred items)
4. Verify all cross-references to sister deliverables (DEL-04-02, DEL-04-03, DEL-02-01, DEL-05-01) are consistent with those documents' content
5. Obtain review and sign-off from both the Architect/Design Lead **and** the Building Science Consultant before finalizing. Both sign-offs are required (not either/or). Sign-off authority is allocated as follows: [Ref: Semantic Lensing E-001]

   | Requirement | Primary Sign-off Authority | Secondary Sign-off Authority | Acceptance Criteria |
   |---|---|---|---|
   | R-ENV-001 (Philosophy) | Architect / Design Lead | Building Science Consultant | Philosophy is clear, addresses climate context, and aligns with 50-year design intent |
   | R-ENV-002 (Thermal targets) | Building Science Consultant | Architect / Design Lead | Targets stated with units, justified vs. NECB, and technically achievable |
   | R-ENV-003 (Air barrier) | Building Science Consultant | Architect / Design Lead | Strategy is technically sound, durable, and constructable |
   | R-ENV-003A (Vapor management) | Building Science Consultant | Architect / Design Lead | Vapor drive, retarder, and condensation risk properly addressed |
   | R-ENV-004 (Thermal bridging) | Building Science Consultant | Architect / Design Lead | Key locations identified; mitigation technically sound |
   | R-ENV-005 (Energy code) | Building Science Consultant | Architect / Design Lead | Code identified; compliance pathway viable |
   | R-ENV-006 (Quantified targets) | Building Science Consultant | Architect / Design Lead | Target is quantified, reasonable, and consistent with philosophy |
   | R-ENV-007 (Mechanical integration) | Architect / Design Lead | Building Science Consultant | Coordination assumptions documented and consistent with DEL-04-02 |
   | R-ENV-008 (Electrical/solar-ready) | Architect / Design Lead | Building Science Consultant | Addendum 03 compliance demonstrated; coordination with DEL-04-03 documented |

6. Incorporate reviewer comments; issue final version

**Output:** Final Building Envelope and Energy Strategy narrative, reviewed and approved

**Timing:** Week 4 of Design Brief production

---

## Verification

### V-001: Completeness Check

- [ ] Energy philosophy statement present (2-4 sentences)
- [ ] Thermal performance targets stated for walls, roof, and glazing with units and rationale
- [ ] Air barrier strategy documented: location, material, airtightness target (ACH50 < 3.5 or equivalent), continuity at critical transitions, and blower door test commitment
- [ ] Vapor management strategy documented: vapor drive direction, retarder placement and permeability class, condensation risk assessment approach
- [ ] Thermal bridging mitigation addressed for: wall-to-foundation, wall-to-roof, window/door frames, and major penetrations; pass/fail acceptance criterion stated or commitment to define in Design Development
- [ ] Energy code identified (NECB or equivalent); compliance method selected (prescriptive or performance); verification timeline stated
- [ ] At least one quantified energy performance target stated with units
- [ ] Mechanical coordination assumptions documented (ACH50, R-values, glazing SHGC, infiltration rate)
- [ ] Solar-ready roof provisions documented: orientation, structural loading, mechanical rough-in reference, electrical rough-in reference, Addendum 03 compliance statement
- [ ] Cold Storage zone envelope addressed separately from main building
- [ ] Design Development deferred items clearly listed

### V-002: Cross-Document Consistency Check

- [ ] Airtightness target (ACH50) consistent between DEL-04-01 and DEL-04-02
- [ ] Wall and roof R-values consistent between DEL-04-01 and any heating load assumptions in DEL-04-02
- [ ] Solar-ready roof orientation consistent across DEL-04-01, DEL-04-02, and DEL-04-03
- [ ] Structural loading allowance for solar array consistent between DEL-04-01 and structural narratives (DEL-02-03, DEL-03-03)
- [ ] Terminology consistent: "main building" (50-year), "Cold Storage" (20-year), "apparatus bay," "Public Works bay" aligned with Decomposition vocabulary map
- [ ] "NECB" referenced consistently (not "NBC," "Building Code," or "energy code" without qualification)
- [ ] ASSUMPTION labels applied consistently wherever content is inferred rather than sourced

### V-003: Specification Requirements Check

| Requirement | Satisfied? | Notes |
|-------------|-----------|-------|
| R-ENV-001: Energy philosophy statement | [ ] | 2-4 sentences; addresses climate, envelope role, 50-yr life |
| R-ENV-002: Thermal performance targets | [ ] | R-values/U-values with units and justification |
| R-ENV-003: Air barrier strategy | [ ] | Location, material, ACH50 target, continuity; blower door test commitment |
| R-ENV-003A: Vapor management strategy | [ ] | Vapor drive, retarder placement, permeability class, condensation risk |
| R-ENV-004: Thermal bridging mitigation | [ ] | Key locations + mitigation; performance objective; pass/fail criterion |
| R-ENV-005: Energy code compliance pathway | [ ] | Code, method, assumptions, verification timeline |
| R-ENV-006: Quantified energy performance targets | [ ] | At least one quantified target with units |
| R-ENV-007: Mechanical integration | [ ] | Key assumptions shared; coordination documented |
| R-ENV-008: Electrical integration and solar-ready | [ ] | Addendum 03; orientation, loading, rough-in reference |

---

## Records

| Record | Purpose | Retention |
|--------|---------|-----------|
| Thermal Performance Target Table | Committed R-values and U-values for Design Development | Design files |
| Air Barrier Strategy Statement | Airtightness target and continuity approach for Design Development detailing | Design files |
| Thermal Bridge Mitigation Table | Bridge locations and mitigation commitments for Design Development detailing | Design files |
| Energy Code Compliance Pathway Statement | Compliance method, assumptions, and verification timeline | Design files |
| Mechanical Coordination Memo | Assumptions shared with DEL-04-02 and responses received | Design files |
| Electrical/Solar Coordination Memo | Solar-ready provisions coordination with DEL-04-03 | Design files |
| Addendum 03 Compliance Checklist | Evidence of solar-ready requirement satisfaction across all three PKG-004 deliverables | Design files |
| Final Reviewed Narrative | Approved narrative for inclusion in Design Brief package | Proposal submission file |

---

## Notes

- **Thermal modeling tools:** Software such as THERM (Lawrence Berkeley National Lab) is useful for thermal bridge analysis at Design Development. Not required for Design Brief stage; narrative commitment is sufficient at this phase.
- **Energy modeling tools:** HOT2000, EnerGuide for Commercial Buildings, or equivalent are required only if performance path NECB compliance is selected. Flag resource requirement early if this path is chosen.
- **Cold Storage specifics:** Cold Storage is unheated; its primary envelope challenge is freeze-thaw management and moisture infiltration, not energy efficiency. The thermal boundary between the main building and Cold Storage is the critical zone requiring conditioned-side insulation and vapor management.
- **Addendum 03 cross-deliverable review:** Before submitting PKG-004 documents, all three narratives (DEL-04-01, DEL-04-02, DEL-04-03) must be reviewed side-by-side to confirm no solar-ready provisions are missed or contradicted across documents.
- **Design life consistency:** Always use "50-year design life" for the main building and "20-year design life" for the Cold Storage. These terms are defined in the Decomposition vocabulary map and must be applied consistently across all deliverables.
