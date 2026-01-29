# Guidance: DEL-33.03 Method Statements

## Purpose

SWMS (Safe Work Method Statements) translate risk assessments into practical step-by-step procedures that workers can follow to control hazards.

**Source:** `_CONTEXT.md`; DEL-33.02 Specification IR-2

## Principles

### Principle 1: SWMS are Instructions, Not Descriptions
SWMS tell workers "how to do the work safely" (prescriptive), not "what the hazards are" (descriptive). Risk assessments identify hazards; SWMS provide the safe method.

**Source:** ASSUMPTION: Effective SWMS practice

### Principle 2: Worker-Centric Language
SWMS should be written for the workers performing the task, using clear language and avoiding jargon.

**Source:** ASSUMPTION: SWMS usability

## Considerations

### Risk Assessment to SWMS Linkage

**Process:**
1. Risk assessment (DEL-33.02) identifies hazards and controls
2. SWMS translates controls into step-by-step work instructions
3. Workers follow SWMS to implement controls

**Example:**
- **Risk Assessment:** "Confined space entry — oxygen deficiency hazard — control: forced-air ventilation"
- **SWMS Step:** "Step 3: Start forced-air blower (Model XYZ, rated 1000 CFM), position duct at tank bottom, verify airflow with anemometer >500 FPM before entry"

**Source:** DEL-33.02 Specification IR-2, PR-3

### Writing Effective Step-by-Step Procedures

**Best Practices:**
- One action per step (don't combine multiple actions)
- Active voice ("Position the ladder", not "The ladder should be positioned")
- Specific ("Attach fall arrest lanyard to anchor point #3", not "Use fall protection")
- Verifiable ("Confirm O₂ reading >19.5%", not "Ensure adequate oxygen")
- Sequence matters (steps in work order)

**Source:** ASSUMPTION: Procedure writing best practice

### SWMS for SIMOPS

When multiple activities occur simultaneously in the same area, SWMS must address coordination:
- Communication protocols (dedicated radio channel, hand signals)
- Exclusion zones (no-go areas for other crews)
- Coordination roles (SIMOPS coordinator)
- Abort criteria (stop work if coordination breaks down)

**Source:** DEL-33.02 Guidance SIMOPS; DEL-33.01 Guidance Multi-Package Coordination

## Trade-offs

### Trade-off 1: Detailed vs. Concise SWMS

**Detailed SWMS** (10+ pages, every sub-task) are thorough but workers may not read them.
**Concise SWMS** (2-3 pages, key steps only) are accessible but may lack detail.

**Guidance:** Use tiered approach:
- **High-risk activities:** Detailed SWMS warranted
- **Medium-risk routine work:** Concise SWMS acceptable
- **Low-risk work:** Generic SWMS or toolbox talk

**Source:** ASSUMPTION: SWMS length trade-off; Datasheet SWMS Types

### Trade-off 2: Generic vs. Task-Specific SWMS

**Generic SWMS** (e.g., "all scaffolding erection") are efficient to manage.
**Task-specific SWMS** (e.g., "scaffold at Tank #1, 15m height") are more accurate.

**Guidance:** Generic for routine repetitive work; task-specific for variable conditions.

**Source:** ASSUMPTION: Generic vs. specific SWMS trade-off

## Examples

### Example 1: SWMS for Confined Space Entry (Storage Tank Coating)

**(Abbreviated example — full SWMS would be more detailed)**

**Activity:** Apply protective coating to interior of 15,000 MT storage tank

**Risk Assessment Reference:** RA-PKG13-012-Rev1 (Residual Risk: High — approved by HSE Manager)

**Scope:** Tank #2, internal coating application (epoxy), 3-day duration, 2-person entry team + 1 standby

**Step-by-Step Procedure:**

1. **Tank Isolation:** Verify tank is drained, cleaned, isolated (LOTO procedure ER-TK-002 applied by Maintenance). Check isolation tag.

2. **Ventilation Setup:** Position forced-air blower at manway, run duct to tank bottom. Start blower, verify airflow >500 FPM at duct outlet.

3. **Atmospheric Testing (Initial):** Entry Supervisor performs atmospheric test at manway, mid-level, bottom:
   - O₂: 20.9% ±0.5% (acceptable range 19.5-23.5%)
   - LEL: 0% (max acceptable 10%)
   - H₂S: 0 ppm (max 10 ppm)
   - CO: 0 ppm (max 25 ppm)
   Record results on Confined Space Entry Permit (Form HSE-CS-01). If any parameter fails, DO NOT ENTER — troubleshoot and retest.

4. **Entry Equipment Setup:** Install fall arrest tripod over manway. Attach retrieval winch and harness. Test retrieval system (lift 100 kg test weight, lower, verify operation).

5. **Pre-Entry Briefing:** Entry Supervisor briefs entry team and standby person (review SWMS, emergency procedure, communication, abort criteria).

6. **Entry Team Don PPE:** Entry team dons supplied-air respirators, chemical-resistant suits, gloves, boots, hard hats. Attach retrieval harness.

7. **Continuous Monitoring:** Entry Supervisor starts continuous atmospheric monitoring (monitor suspended in tank, alarm set for O₂ <19.5%, LEL >10%).

8. **Entry:** Entry team descends ladder one at a time. Standby person maintains visual/radio contact.

9. **Coating Application:** Entry team applies epoxy coating per manufacturer instructions. Work rotation: 2 hours max in tank, 30 min break.

10. **Emergency Abort:** If alarm sounds or worker feels unwell, STOP WORK IMMEDIATELY. Entry team exits tank using retrieval harness/winch if needed.

11. **Exit:** Entry team exits tank, removes PPE. Entry Supervisor performs post-work atmospheric test. Close permit if work complete.

**Emergency Procedure:** See DEL-33.07 Emergency Response Plan, Scenario: Confined Space Rescue. Non-entry rescue using retrieval winch is primary response.

**Training Required:**
- Confined space entry
- Supplied-air respirator
- Rescue procedures
- WHMIS (epoxy coating hazards)

**Source:** ASSUMPTION: Example SWMS; DEL-33.01 Guidance Confined Space Hazards; DEL-33.02 Guidance Example 2

---

**Document Status:** Pass 3/3 — Final reconciliation complete
**Generated:** 2026-01-28
**Cross-Document Consistency:** Verified against Datasheet, Specification, Procedure
**Ready for:** WORKING_ITEMS session (human review and refinement)
