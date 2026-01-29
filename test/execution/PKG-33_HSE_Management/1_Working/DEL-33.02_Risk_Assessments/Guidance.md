# Guidance: DEL-33.02 Risk Assessments

## Purpose

This guidance document supports the development and management of **Risk Assessments** for **PKG-33 HSE Management** on the Canola Oil Transload Facility Design & Build project.

### Deliverable Context

- **Type:** Assessment
- **Discipline:** Project Delivery
- **Responsible Party:** D&B Contractor
- **Description:** Defines and substantiates risk assessments in accordance with ER requirements

**Source:** `_CONTEXT.md`, Decomposition line 730

### Strategic Alignment

Risk Assessments support the same project objectives as DEL-33.01 (OHS Plan):
- **OBJ-5: Terminal Continuity** — Risk assessments consider active Terminal operations interface
- **OBJ-6: Regulatory Compliance** — Fulfill WorkSafeBC general duty of care (risk assessment)
- **OBJ-7: Environmental Protection** — Environmental hazards captured in risk assessments

**Source:** Decomposition Section 2, Section 6; DEL-33.01 Guidance Strategic Alignment

### Deliverable Role

Risk Assessments implement the hazard identification and risk assessment processes established in DEL-33.01 (OHS Plan Section 4). They are the foundational tool for:
- Identifying what can go wrong (hazards)
- Evaluating how bad it could be and how likely (risk)
- Determining what to do about it (controls)
- Deciding if residual risk is acceptable (risk acceptance)

Risk Assessments feed into:
- **DEL-33.03 Method Statements** — SWMS developed for high-risk activities
- **DEL-33.01 Permit-to-Work** — Activity-specific assessments in permits
- **DEL-33.07 Emergency Response Plan** — Emergency scenarios based on credible risks
- **Training Requirements** — Task-specific training based on identified hazards

**Source:** Datasheet Internal Cross-References; Specification PR-3 (Actionability); DEL-33.01 Specification FR-4, FR-5

## Principles

### Principle 1: Risk Assessment is a Process, Not a Document

Risk assessment is a systematic thinking process to understand and control hazards. The documentation (risk assessment form) is evidence of that thinking, not the end goal itself.

**Key Practices:**
- Involve the people doing the work (workers, supervisors, trades) in hazard identification
- Use "what if" and "how could this go wrong" questioning
- Focus on credible hazards (not theoretical extremes)
- Document assumptions and limitations

**Source:** ASSUMPTION: Effective risk assessment practice; ISO 31000 principles
**Specification Cross-Reference:** Specification FR-1 (Hazard Identification)
**Procedure Cross-Reference:** Procedure Step 2 (Conduct Risk Assessment — worker involvement)

### Principle 2: ALARP (As Low As Reasonably Practicable)

Residual risk should be reduced to a level that is As Low As Reasonably Practicable (ALARP), balancing risk reduction against cost, effort, and practicality.

**ALARP Considerations:**
- **Intolerable Risk (Extreme):** Must be reduced, regardless of cost (unless physically impossible)
- **Tolerable Risk (High/Medium):** Reduce if reasonably practicable (cost-benefit considered)
- **Broadly Acceptable (Low):** No further action required (monitoring sufficient)

**Guidance:** For High and Extreme risks, document why additional controls are not reasonably practicable (if applicable). Extreme risks require Project Manager approval.

**Source:** ASSUMPTION: ALARP principle per UK HSE and WorkSafeBC philosophy; Specification FR-4 (Residual Risk Acceptance)
**Specification Cross-Reference:** Specification AC-2 (Risk Control Adequacy — ALARP)

### Principle 3: Hierarchy of Controls Over PPE

The hierarchy of controls reflects effectiveness: elimination/substitution are far more effective than relying on workers to use PPE correctly every time.

**Common Pitfalls to Avoid:**
- Jumping straight to PPE without considering elimination/engineering
- Generic controls ("wear PPE") without specifying what type or why
- Administrative controls (procedures, training) without verification of compliance

**Guidance:** Challenge each risk assessment to push up the hierarchy. If PPE is the primary control, document why higher-level controls are not feasible.

**Source:** DEL-33.01 Guidance Principle 1 (Zero Harm); Specification FR-3 (Control Measures); Datasheet Control Hierarchy
**Specification Cross-Reference:** Specification FR-3 (hierarchy application), AC-2 (hierarchy in acceptance criteria)

### Principle 4: Risk Assessment Informs, Does Not Replace, Judgment

Risk assessment provides structure to decision-making, but cannot replace competent supervision and worker judgment. Workers retain stop-work authority regardless of risk assessment approval.

**Source:** DEL-33.01 Guidance Principle 5 (Accountability — stop-work authority); ASSUMPTION: Risk assessment as decision support
**Specification Cross-Reference:** Specification QR-1 (competent personnel)

## Considerations

### Hazard Identification Process

Effective hazard identification requires systematic approaches:

#### Task-Based Hazard Identification

Break the task into steps and ask "what could go wrong?" at each step:
1. Mobilize equipment and materials
2. Set up work area (barriers, signage, equipment)
3. Perform work (main activity)
4. Clean up and demobilize

**Example (confined space tank entry):**
- Mobilize: transporting gas monitor, retrieval equipment → struck-by (mobile equipment)
- Setup: opening manway → oxygen deficiency, toxic gas release
- Entry: descending into tank → fall, slips/trips, engulfment
- Work inside: coating application → chemical exposure, fire/explosion (flammable vapors)
- Exit: ascending ladder → fatigue, heat stress
- Cleanup: disposing of waste → hazardous waste handling

**Source:** ASSUMPTION: Task-based hazard ID methodology; Datasheet Risk Assessment Types
**Specification Cross-Reference:** Specification FR-1 (systematic hazard identification)
**Procedure Cross-Reference:** Procedure Step 2 (task breakdown)

#### Area-Based Hazard Identification

Walk the work area and identify location-specific hazards:
- Overhead hazards (cranes, power lines, falling objects)
- Ground hazards (uneven surfaces, holes, underground utilities)
- Adjacent hazards (active operations, traffic, water/waterway)
- Environmental hazards (weather, noise, lighting)

**Source:** ASSUMPTION: Area-based methodology; Datasheet Risk Assessment Types

#### Change-Driven Hazard Identification

Re-assess when conditions change:
- Scope/design changes (new activities, different methods)
- New hazards introduced (different equipment, materials, subcontractors)
- Learning from incidents/near-misses (controls were inadequate)

**Source:** Specification PR-2 (Currency — change triggers); DEL-33.01 Guidance Example 3 (trigger criteria)

### Risk Matrix Application

The 5×5 risk matrix provides a semi-quantitative framework for prioritizing risks.

#### Likelihood Definitions (Anticipated)

| Rating | Term | Frequency | Description |
|--------|------|-----------|-------------|
| 1 | Rare | May occur in exceptional circumstances | Has never happened on similar projects; requires multiple failures |
| 2 | Unlikely | Could occur at some time | Has happened on similar projects occasionally |
| 3 | Possible | Might occur occasionally | Has happened on this type of work; not unexpected |
| 4 | Likely | Will probably occur | Happens regularly on this work; expected to occur |
| 5 | Almost Certain | Expected to occur frequently | Will occur multiple times unless controls applied |

**Source:** ASSUMPTION: Standard likelihood definitions; TBD: ER likelihood criteria; Datasheet Risk Matrix Parameters

#### Consequence Definitions (Anticipated)

| Rating | Term | People | Environment | Property | Schedule |
|--------|------|--------|-------------|----------|----------|
| 1 | Insignificant | First aid | Minor spill, no reporting | <$10k | <1 day |
| 2 | Minor | Medical treatment | Spill, regulatory reporting | $10-100k | 1-7 days |
| 3 | Moderate | Lost time injury (LTI) | Moderate spill, off-site impact | $100k-1M | 1-4 weeks |
| 4 | Major | Serious injury (permanent disability) | Major spill, significant off-site impact | $1-10M | 1-3 months |
| 5 | Catastrophic | Fatality or multiple serious injuries | Catastrophic spill, long-term environmental damage | >$10M | >3 months |

**Source:** ASSUMPTION: Standard consequence definitions; TBD: ER consequence criteria; Datasheet Risk Matrix Parameters

#### Risk Rating Bands

| Risk Rating | Band | Action |
|-------------|------|--------|
| 1-4 | Low | Acceptable; monitor; controls may be administrative/PPE |
| 5-9 | Medium | Tolerable with controls; engineering controls preferred |
| 10-16 | High | Requires HSE Manager approval; engineering controls mandatory; SWMS required |
| 17-25 | Extreme | Requires Project Manager approval; must reduce to High or below; work may not proceed until controls improved |

**Source:** ASSUMPTION: Risk rating bands and actions; TBD: ER risk tolerability; Datasheet Risk Matrix Parameters; Specification FR-4

### Applying the Hierarchy of Controls

The hierarchy guides selection of the most effective controls:

#### 1. Elimination

**Question:** Can we avoid the hazard entirely by not doing the task or doing it differently?

**Examples:**
- Eliminate work at height by assembling structures on the ground and lifting into place
- Eliminate confined space entry by designing tanks with large access or external monitoring
- Eliminate excavation near utilities by using trenchless methods

**Source:** DEL-33.01 Guidance Principle 1; Specification FR-3

#### 2. Substitution

**Question:** Can we replace the hazardous material, equipment, or method with a less hazardous alternative?

**Examples:**
- Substitute water-based coatings for solvent-based (reduce VOC exposure, fire risk)
- Substitute electric equipment for diesel (reduce exhaust fumes in confined areas)
- Substitute smaller/lighter components to reduce manual handling injury risk

**Source:** DEL-33.01 Guidance Principle 1; Specification FR-3

#### 3. Engineering Controls

**Question:** Can we physically isolate, contain, or remove the hazard through design or equipment?

**Examples:**
- Install guardrails and toe boards for fall protection (vs. relying on harnesses)
- Provide forced-air ventilation in confined spaces (vs. relying on respirators)
- Install machine guarding to prevent contact with moving parts
- Use ground mats or engineered pads to prevent crane tip-over

**Source:** DEL-33.01 Guidance Principle 1; Specification FR-3

#### 4. Administrative Controls

**Question:** Can we reduce risk through procedures, training, work practices, or job rotation?

**Examples:**
- Limit confined space entry time to 2 hours (reduce exposure to heat/fumes)
- Require buddy system for hazardous work (second person monitors)
- Implement permit-to-work to verify prerequisites (atmospheric testing, energy isolation)
- Provide task-specific training (confined space, working at height)

**Caution:** Administrative controls rely on people following the procedure every time. Verify compliance through inspections, audits, and supervision.

**Source:** DEL-33.01 Specification FR-5 (procedures), FR-7 (training); Specification FR-3

#### 5. Personal Protective Equipment (PPE)

**Question:** What PPE is required as the last line of defense?

**Examples:**
- Hard hats, safety glasses, steel-toe boots (basic site PPE)
- Respiratory protection (half-face or full-face respirator for chemical exposure, SCBA for confined space)
- Fall protection harness and lanyard (when fall hazard cannot be eliminated)
- Chemical-resistant gloves and suit (for hazardous substance contact)

**Caution:** PPE is the least effective control. It must be:
- Appropriate for the hazard (not generic "wear gloves")
- Properly fitted and maintained
- Used correctly every time (requires training and supervision)

**Source:** DEL-33.01 Specification FR-7; WorkSafeBC Part 8 (PPE); Specification FR-3

### SIMOPS (Simultaneous Operations) Risk Assessment

When multiple packages or activities occur in the same area simultaneously, risks can compound:

**SIMOPS Risk Factors:**
- **Physical interference:** Crane swing radius over active piping work, excavation near scaffolding
- **Communication breakdown:** Multiple supervisors, language barriers, radio congestion
- **Cumulative noise/distraction:** Reduces situational awareness
- **Shared resources:** Access routes, laydown areas, utilities

**SIMOPS Risk Assessment Process:**
1. Identify simultaneous activities (weekly look-ahead schedule)
2. Assess individual activity risks (standard risk assessments)
3. Assess interaction risks (combined effects, communication, coordination)
4. Identify additional SIMOPS controls (dedicated coordinators, exclusion zones, enhanced communication protocols, staggered work schedules)
5. Approve SIMOPS plan (HSE Manager minimum, Project Manager for complex SIMOPS)

**Source:** DEL-33.01 Guidance Multi-Package Coordination; Datasheet Risk Assessment Types; ASSUMPTION: SIMOPS methodology
**Specification Cross-Reference:** Specification IR-4 (Cross-Package Coordination)
**Procedure Cross-Reference:** Procedure Step 2 (SIMOPS assessment)

## Trade-offs

### Trade-off 1: Detailed vs. Streamlined Risk Assessments

**Tension:** Detailed risk assessments (multi-page, every sub-step analyzed) provide thorough coverage but are time-consuming and may not be read. Streamlined assessments (one-page, key hazards only) are faster and more accessible but may miss subtleties.

**Considerations:**
- **High-risk activities:** Detailed JHA (Job Hazard Analysis) warranted — break task into steps, analyze each step
- **Routine low-risk activities:** Streamlined assessment acceptable — focus on key hazards and controls
- **Balance:** Use tiered approach based on risk rating

**Guidance:**
- Risk rating ≥10 (High/Extreme): Detailed JHA required
- Risk rating 5-9 (Medium): Standard risk assessment (1-2 pages)
- Risk rating 1-4 (Low): Streamlined assessment or generic activity risk assessment

**Source:** ASSUMPTION: Tiered risk assessment approach; Datasheet Risk Assessment Types (JHA for high-risk)
**Specification Cross-Reference:** Specification FR-1, FR-2

### Trade-off 2: Generic vs. Task-Specific Assessments

**Tension:** Generic risk assessments (e.g., "all excavation work") are efficient to produce and maintain. Task-specific assessments (e.g., "excavate for tank foundation in northwest corner") are more accurate but create many documents.

**Considerations:**
- **Generic assessments:** Acceptable for routine, repetitive tasks with similar conditions (e.g., scaffold erection, concrete pouring)
- **Task-specific assessments:** Required when conditions vary significantly (e.g., excavation depth, proximity to utilities, soil conditions)

**Guidance:**
- Use generic assessments for routine work, supplemented by pre-task briefings to address site-specific conditions
- Use task-specific assessments for non-routine work or when significant variables exist

**Source:** ASSUMPTION: Generic vs. specific assessment trade-off
**Specification Cross-Reference:** Specification FR-1 (systematic hazard ID captures variations)

### Trade-off 3: Risk Assessment Timing (Upfront vs. Just-in-Time)

**Tension:** Upfront risk assessments (all activities assessed at project start) provide early visibility but may be based on incomplete information. Just-in-time assessments (assessed shortly before work) are more accurate but may delay mobilization.

**Considerations:**
- **D&B Context:** Design evolving during construction means upfront assessments may need revision
- **Long-lead controls:** Some controls (equipment procurement, training, permits) require advance planning
- **Agility:** Just-in-time allows learning from earlier work phases

**Guidance:**
- Conduct high-level risk assessments during project planning (identify major hazards, long-lead controls)
- Conduct detailed task risk assessments 1-2 weeks before activity (sufficient time for controls, training)
- Update assessments if conditions change

**Source:** DEL-33.01 Guidance D&B HSE Challenges (concurrent design and construction); Specification PR-2 (Currency)
**Specification Cross-Reference:** Specification PR-1 (Completeness — before work commences)

## Examples

### Example 1: Task Risk Assessment for Heavy Lift (Storage Tank Shell Course)

**Activity:** Lift and install 15,000 MT storage tank shell course #3 using mobile crane

**Hazards Identified:**
1. Crane tip-over (soft ground, overloading, wind)
2. Load drop (rigging failure, load shift, operator error)
3. Struck-by (personnel in lift zone, swinging load)
4. Structural failure (shell course damage, lifting lug failure)

**Risk Evaluation (Initial — Before Controls):**

| Hazard | Likelihood | Consequence | Risk Rating |
|--------|-----------|-------------|-------------|
| Crane tip-over | 2 (Unlikely) | 5 (Catastrophic — fatality, major property damage) | 10 (High) |
| Load drop | 3 (Possible) | 5 (Catastrophic) | 15 (High) |
| Struck-by | 3 (Possible) | 4 (Major — serious injury) | 12 (High) |
| Structural failure | 2 (Unlikely) | 4 (Major) | 8 (Medium) |

**Control Measures (Hierarchy Applied):**

**Elimination/Substitution:**
- Not feasible (tank must be erected in place)

**Engineering Controls:**
- Crane selection: 500-ton mobile crane with capacity margin (lift = 60% of rated capacity)
- Ground preparation: Engineered crane pads, ground bearing pressure calculation, proof rolling
- Rigging design: 4-point lift using certified lifting lugs, load equalizing spreader beam
- Load securing: Guide ropes (tag lines) to control load orientation
- Wind monitoring: Anemometer on crane boom, abort lift if wind >20 km/h

**Administrative Controls:**
- Engineered lift plan prepared and approved (third-party review by Professional Engineer)
- Pre-lift meeting (crane operator, riggers, lift supervisor, HSE coordinator)
- Trial lift (lift 300mm, hold, inspect rigging)
- Exclusion zone (2× lift radius, barriers and signage, spotter at barrier)
- Communication protocol (dedicated radio channel, hand signals for backup)
- Lift supervisor (competent person, dedicated to lift oversight)

**PPE:**
- Hard hat, safety glasses, high-visibility vest, steel-toe boots (all personnel)
- Fall protection harness (personnel on tank during fit-up)

**Residual Risk (After Controls):**

| Hazard | Likelihood | Consequence | Risk Rating | Approval |
|--------|-----------|-------------|-------------|----------|
| Crane tip-over | 1 (Rare) | 5 (Catastrophic) | 5 (Medium) | HSE Manager |
| Load drop | 1 (Rare) | 5 (Catastrophic) | 5 (Medium) | HSE Manager |
| Struck-by | 1 (Rare) | 4 (Major) | 4 (Low) | HSE Coordinator |
| Structural failure | 1 (Rare) | 4 (Major) | 4 (Low) | HSE Coordinator |

**Actionability:**
- SWMS required (DEL-33.03): Detailed safe work method statement for heavy lift
- Permits required: Crane permit, lift permit, work-at-height permit (for personnel on tank)
- Training required: Lift supervisor certification, rigger certification, crane operator certification

**Source:** ASSUMPTION: Example risk assessment based on typical heavy lift; DEL-33.01 Guidance Heavy Lifting Hazards
**Specification Cross-Reference:** Specification FR-1 through FR-4, PR-3 (actionability — SWMS, permits, training)

### Example 2: Job Hazard Analysis (JHA) for Confined Space Entry (Storage Tank Coating)

**Activity:** Enter 15,000 MT storage tank to apply internal protective coating

**JHA Step-by-Step:**

| Step | Hazards | Initial Risk | Controls | Residual Risk |
|------|---------|--------------|----------|---------------|
| 1. Prepare tank for entry (isolate, drain, clean) | Energy release (residual product, pressure), chemical exposure (canola oil residue), slip/trip (wet surfaces) | Medium (6) | LOTO procedure, drain and flush with water, hot work permit if steam cleaning, slip-resistant boots | Low (3) |
| 2. Open manway and ventilate | Oxygen deficiency (<19.5%), toxic gas (H₂S from decomposition, CO₂), flammable vapors | High (15) | Forced-air ventilation (blower rated for confined space, duct to tank bottom), atmospheric testing (O₂, LEL, H₂S, CO), continuous monitoring during entry | Medium (6) |
| 3. Set up entry equipment | Fall from height (accessing manway on tank roof), dropped tools (striking personnel below) | Medium (8) | Fall protection for roof access, tool lanyards, exclusion zone below manway | Low (4) |
| 4. Entry team descends ladder | Fall (ladder, fatigue), oxygen deficiency (ventilation failure), engulfment (if tank not fully drained) | High (12) | Ladder inspection, fall arrest system (tripod, winch, retrieval line), continuous atmospheric monitoring (abort if O₂ <19.5% or LEL >10%), standby person at manway, rescue equipment (harness connected to retrieval line) | Medium (6) |
| 5. Apply coating (spray application) | Chemical exposure (isocyanate vapors from polyurethane coating, skin contact), fire/explosion (flammable vapors from coating), oxygen deficiency (coating consumes O₂) | Extreme (20) | Forced-air ventilation increased (6+ air changes/hour), supplied-air respirator (airline from outside tank, not SCBA), chemical-resistant suit and gloves, continuous LEL and O₂ monitoring (abort if LEL >10% or O₂ <19.5%), bonding/grounding to prevent static ignition, explosion-proof lighting and tools | High (10 — Project Manager approval required) |
| 6. Exit tank | Fatigue, heat stress (coating work is physically demanding in confined space), oxygen deficiency | High (12) | Work rotation (max 2 hours in tank, rest breaks), hydration, medical monitoring (pre-entry and post-entry vitals), continuous atmospheric monitoring | Medium (6) |
| 7. Close manway and decontaminate equipment | Chemical exposure (contaminated equipment, waste disposal) | Low (4) | Decontamination procedure, hazardous waste disposal (used coating materials, contaminated PPE), PPE during decontamination | Low (2) |

**Additional Controls:**
- **Training:** Confined space entry competency (entry team, standby person, entry supervisor), respiratory protection fit-testing, chemical hazard training (SDS review)
- **Emergency Response:** Rescue plan (non-entry rescue using retrieval line preferred; entry rescue only if safe), rescue drill conducted before entry, emergency contact list posted at entry
- **Communication:** Continuous communication (radio or voice) between entry team and standby person
- **Permit:** Confined space entry permit (includes atmospheric test results, equipment checklist, entry team names, emergency contacts, approval signatures)

**Residual Risk Acceptance:**
- Overall activity residual risk: **High (10)** due to coating application step
- **Approval Required:** Project Manager (due to Extreme initial risk reduced to High residual risk)
- **Justification for ALARP:** Elimination/substitution not feasible (tank interior must be coated); engineering controls maximized (ventilation, supplied-air respirator, explosion-proof equipment); administrative controls in place (training, permit, communication, rotation); residual risk is unavoidable consequence of essential tank coating work

**Actionability:**
- **SWMS Required:** Detailed SWMS for confined space coating work (DEL-33.03)
- **Permits Required:** Confined space entry permit, hot work permit (if any welding/cutting required during setup)
- **Training Required:** Confined space entry, supplied-air respirator, chemical handling (polyurethane coatings)
- **Emergency Response:** Tank entry rescue scenario added to Emergency Response Plan (DEL-33.07)

**Source:** ASSUMPTION: Example JHA based on typical confined space coating; DEL-33.01 Guidance Confined Space Hazards
**Specification Cross-Reference:** Specification FR-1, FR-2, FR-3, FR-4, PR-3 (actionability)

---

**Document Status:** Pass 3/3 — Final reconciliation complete
**Generated:** 2026-01-28
**Cross-Document Consistency:** Verified against Datasheet, Specification, Procedure
**Ready for:** WORKING_ITEMS session (human review and refinement)
