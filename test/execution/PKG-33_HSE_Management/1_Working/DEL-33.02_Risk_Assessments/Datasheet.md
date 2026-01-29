# Datasheet: DEL-33.02 Risk Assessments

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-33.02 |
| Deliverable Name | Risk Assessments |
| Package | PKG-33 HSE Management |
| Discipline | Project Delivery |
| Type | Assessment |
| Responsible Party | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

### Assessment Characteristics

| Attribute | Value | Source |
|-----------|-------|--------|
| Assessment Type | Task Risk Assessments, Job Hazard Analyses | `_CONTEXT.md`; Decomposition line 730 |
| Applicable Phase | Construction (Design & Build execution) | Decomposition — project context (Section 1) |
| Risk Assessment Methodology | Likelihood × Consequence Matrix | ASSUMPTION: Standard risk assessment approach; Cross-reference DEL-33.01 (OHS Plan FR-4) |
| Assessment Scope | All project construction activities across 36 packages | Decomposition Package Summary (Section 4); DEL-33.01 Specification FR-4 |
| Assessment Format | Structured risk assessment forms/templates | TBD: Employer's Requirements risk assessment format |
| Update Frequency | As required by triggers (see Procedure) | DEL-33.01 Guidance Example 3 (Risk Assessment Trigger Criteria) |

### Risk Assessment Types

| Assessment Type | Description | Source |
|----------------|-------------|--------|
| Task-Based Risk Assessments | Risk assessment for specific work tasks or activities | Decomposition line 730; DEL-33.01 Specification FR-4 |
| Job Hazard Analysis (JHA) | Detailed step-by-step hazard analysis for high-risk tasks | Decomposition line 730; ASSUMPTION: JHA for critical activities |
| Area-Based Risk Assessments | Hazard assessment for specific work areas or zones | ASSUMPTION: Supplement to task-based assessments |
| SIMOPS Risk Assessments | Assessment of simultaneous operations risks | DEL-33.01 Guidance (Multi-Package Coordination) |
| Activity-Specific Assessments | Pre-task assessments for permit-required work | DEL-33.01 Specification FR-5 (permits include risk assessment) |

### Risk Matrix Parameters (Anticipated)

| Parameter | Scale | Description | Source |
|-----------|-------|-------------|--------|
| Likelihood | 1-5 | 1=Rare, 2=Unlikely, 3=Possible, 4=Likely, 5=Almost Certain | ASSUMPTION: Standard 5×5 risk matrix; TBD: ER risk criteria |
| Consequence | 1-5 | 1=Insignificant, 2=Minor, 3=Moderate, 4=Major, 5=Catastrophic | ASSUMPTION: Standard 5×5 matrix; TBD: ER consequence definitions |
| Risk Rating | 1-25 | Low (1-4), Medium (5-9), High (10-16), Extreme (17-25) | ASSUMPTION: Standard risk rating bands; TBD: ER risk tolerability |
| Residual Risk Acceptance | Varies by rating | Low/Medium: HSE Coord; High: HSE Manager; Extreme: Project Manager | ASSUMPTION: Risk acceptance authority levels; TBD: ER approval matrix |

## Conditions

### Operational Context

| Condition | Description | Source |
|-----------|-------------|--------|
| Project Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | Decomposition — Project Context (Section 1) |
| Contract Type | Design & Build | Decomposition — Project Context (Section 1) |
| Regulatory Framework | WorkSafeBC OH&S Regulation (risk assessment required) | DEL-33.01 Specification FR-3; Guidance Regulatory Environment |
| Active Terminal Environment | Risk assessments must consider Terminal operations interface | OBJ-5 Terminal Continuity; DEL-33.01 Specification PR-1 |
| Multi-Disciplinary Project | Risk assessments cover 36 packages across multiple disciplines | Decomposition Package Summary (Section 4) |

### Project-Specific Hazards Requiring Assessment

| Hazard Category | Risk Assessment Focus | Source |
|----------------|----------------------|--------|
| Marine Operations | Drowning, hypothermia, vessel collision, marine traffic, weather | DEL-33.01 Datasheet, Guidance Marine Hazards; PKG-08, PKG-09, PKG-11 |
| Rail Works | Train strike, railcar coupling, confined space (railcar interior), clearances | DEL-33.01 Guidance Rail Hazards; PKG-07, PKG-10 |
| Heavy Lifting | Crane tip-over, load drop, struck-by, rigging failure, ground failure | DEL-33.01 Guidance Heavy Lifting Hazards; PKG-05, PKG-06, PKG-13 |
| Confined Space | Oxygen deficiency, toxic atmosphere, engulfment, entrapment | DEL-33.01 Guidance Confined Space Hazards; PKG-03, PKG-13, PKG-14 |
| Hazardous Substances | Inhalation, skin contact, fire/explosion (canola oil, coatings, welding) | DEL-33.01 Guidance Hazardous Substances; PKG-26, product characteristics |
| Electrical Work | Electrocution, arc flash, fire | DEL-33.01 Datasheet; PKG-17, PKG-18 |
| Excavation | Cave-in, striking utilities, falls into excavation, mobile equipment | DEL-33.01 Datasheet; PKG-02, PKG-03 |
| Working at Height | Falls from height (scaffolding, ladders, elevated platforms) | ASSUMPTION: Common construction hazard; WorkSafeBC Part 11 |

## Construction

### Risk Assessment Structure (Anticipated)

| Section/Field | Content | Source |
|--------------|---------|--------|
| Assessment Header | Project, package, activity, date, assessor, approver | ASSUMPTION: Standard risk assessment template |
| Activity Description | Detailed description of task/activity being assessed | Specification FR-1 |
| Hazard Identification | List of hazards associated with the activity | Specification FR-1; DEL-33.01 FR-4 |
| Risk Evaluation | Likelihood, consequence, initial risk rating (before controls) | Specification FR-2; Attributes (Risk Matrix Parameters) |
| Control Measures | Existing and additional controls (hierarchy of controls) | Specification FR-3; DEL-33.01 FR-4 |
| Residual Risk | Likelihood, consequence, residual risk rating (after controls) | Specification FR-2; Attributes (Residual Risk Acceptance) |
| Approval | Signature/date of assessor, checker, approver | Specification Verification; Procedure Verification |
| Review Date | Next scheduled review date or review trigger conditions | Specification QR-2; DEL-33.01 Guidance Example 3 |

### Control Hierarchy Application

| Control Level | Description | Preference | Source |
|--------------|-------------|-----------|--------|
| Elimination | Remove the hazard entirely | 1st preference | DEL-33.01 Guidance Principle 1; Specification FR-3 |
| Substitution | Replace with less hazardous alternative | 2nd preference | DEL-33.01 Guidance Principle 1; Specification FR-3 |
| Engineering Controls | Physical barriers, ventilation, guarding | 3rd preference | DEL-33.01 Guidance Principle 1; Specification FR-3 |
| Administrative Controls | Procedures, training, permits, signage, rotation | 4th preference | DEL-33.01 Guidance Principle 1; Specification FR-3 |
| Personal Protective Equipment (PPE) | Last line of defense (hard hats, safety glasses, gloves, respirators) | 5th preference | DEL-33.01 Guidance Principle 1; Specification FR-3 |

## References

### Decomposition Document

- **Source:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- **Sections Referenced:**
  - Section 1: Project Context
  - Section 2: Project Objectives (OBJ-5, OBJ-6, OBJ-7)
  - Section 4: Package Summary (36 packages)
  - Section 5: PKG-33 HSE Management (line 730)
  - Section 6: Objective-to-Deliverable Mapping

### Internal Cross-References

- `_CONTEXT.md` — Deliverable identification
- **DEL-33.01 Occupational Health & Safety Plan** (primary interface):
  - Datasheet: Project-Specific Hazards
  - Specification FR-4 (Hazard Identification and Risk Assessment) — defines risk assessment process
  - Specification FR-5 (Safe Work Procedures) — risk assessments inform SWMS and permits
  - Guidance Principle 1 (Zero Harm), Principle 3 (Risk-Based Resource Allocation)
  - Guidance Project-Specific Hazard Considerations (all subsections)
  - Guidance Example 3 (Risk Assessment Trigger Criteria)
  - Procedure Step 2.2 (Hazard Identification and Risk Profiling)
  - Procedure Step 4.3 (Hazard Identification and Risk Assessment)
- DEL-33.03 — Method Statements (informed by risk assessments)
- DEL-33.07 — Emergency Response Plan (interface with emergency scenarios)
- PKG-32 — Regulatory & Permits (permit-related risk assessment requirements)
- All technical packages (PKG-01 through PKG-26) — discipline-specific hazards

### External References (TBD)

- Employer's Requirements Volume 2 Part 1: General Requirements (risk assessment requirements — **location TBD**)
- WorkSafeBC OH&S Regulation (risk assessment obligations)
- ISO 31000 Risk Management — Guidelines (ASSUMPTION: Industry standard reference)
- Contractor's Corporate Risk Assessment Methodology
- Project Hazard Register (summary in DEL-33.01 Annex C)

---

**Document Status:** Pass 3/3 — Final reconciliation complete
**Generated:** 2026-01-28
**Cross-Document Consistency:** Verified against Specification, Guidance, Procedure
**Ready for:** WORKING_ITEMS session (human review and refinement)
