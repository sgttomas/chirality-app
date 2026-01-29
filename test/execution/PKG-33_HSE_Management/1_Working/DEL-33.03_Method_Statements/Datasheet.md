# Datasheet: DEL-33.03 Method Statements

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-33.03 |
| Deliverable Name | Method Statements |
| Package | PKG-33 HSE Management |
| Discipline | Project Delivery |
| Type | Procedure |
| Responsible Party | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

### Method Statement Characteristics

| Attribute | Value | Source |
|-----------|-------|--------|
| Document Type | Safe Work Method Statements (SWMS) | `_CONTEXT.md`; Decomposition line 731 |
| Applicable Phase | Construction (Design & Build execution) | Decomposition — project context (Section 1) |
| Scope | High-risk activities across all project packages | DEL-33.01 Specification FR-5; DEL-33.02 Specification IR-2 (risk rating ≥10) |
| Development Basis | Risk assessments (DEL-33.02) | DEL-33.02 Specification IR-2, PR-3 |
| Format | Structured SWMS templates (step-by-step procedures) | TBD: Employer's Requirements SWMS format |
| Approval Level | Activity-dependent (based on risk rating) | ASSUMPTION: HSE Coordinator (Medium), HSE Manager (High/Extreme) |

### SWMS Types (Anticipated)

| SWMS Type | Description | Source |
|-----------|-------------|--------|
| Activity-Specific SWMS | Detailed procedures for specific high-risk tasks | Decomposition line 731; DEL-33.01 Specification FR-5 |
| Generic SWMS | Standard procedures for routine repetitive tasks | ASSUMPTION: Efficiency for common activities |
| Permit-Integrated SWMS | SWMS embedded in permit-to-work process | DEL-33.01 Specification FR-5; DEL-33.02 Specification IR-3 |
| Emergency SWMS | Procedures for emergency response activities | Cross-reference: DEL-33.07 Emergency Response Plan |

### High-Risk Activities Requiring SWMS

| Activity Category | SWMS Required For | Source |
|------------------|-------------------|--------|
| Marine Operations | Barge work, pile driving, fender installation, over-water work, vessel interface | DEL-33.01 Guidance Marine Hazards; PKG-08, PKG-09, PKG-11 |
| Rail Works | Track construction on active railway, railcar unloading operations, rail flagging | DEL-33.01 Guidance Rail Hazards; PKG-07, PKG-10 |
| Heavy Lifting | Critical lifts (tank shell courses, structural steel, major equipment) | DEL-33.01 Guidance Heavy Lifting Hazards; PKG-05, PKG-06, PKG-13 |
| Confined Space Entry | Tank entry, manhole entry, deep excavations (>1.2m), underground utilities | DEL-33.01 Guidance Confined Space Hazards; PKG-03, PKG-13, PKG-14 |
| Hot Work | Welding, cutting, grinding near flammables | DEL-33.01 Specification FR-5 (permits); ASSUMPTION: Hot work SWMS |
| Work at Height | Scaffolding, rope access, elevated platforms (>3m) | ASSUMPTION: Working at height hazards; WorkSafeBC Part 11 |
| Hazardous Substances | Coating application, chemical handling, asbestos/lead abatement | DEL-33.01 Guidance Hazardous Substances; PKG-26, PKG-01 |
| Excavation | Trenching, shoring, working near utilities | DEL-33.01 Datasheet Project-Specific Hazards; PKG-02, PKG-03 |

## Conditions

### Operational Context

| Condition | Description | Source |
|-----------|-------------|--------|
| Project Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | Decomposition — Project Context (Section 1) |
| Contract Type | Design & Build | Decomposition — Project Context (Section 1) |
| Regulatory Framework | WorkSafeBC OH&S Regulation (safe work procedures required) | DEL-33.01 Specification FR-3; ASSUMPTION: WorkSafeBC SWMS requirements |
| Active Terminal Environment | SWMS must consider Terminal operations interface | OBJ-5 Terminal Continuity; DEL-33.01 Specification PR-1 |
| Multi-Package Coordination | SWMS coordination for SIMOPS (simultaneous operations) | DEL-33.02 Guidance SIMOPS; DEL-33.01 Guidance Multi-Package Coordination |

### SWMS Triggers

| Trigger | Description | Source |
|---------|-------------|--------|
| High-Risk Activity | Risk assessment identifies residual risk ≥10 (High or Extreme) | DEL-33.02 Specification IR-2; DEL-33.02 Guidance Trade-off 1 (risk rating threshold) |
| Permit-Required Work | Hot work, confined space, excavation, work at height, marine operations | DEL-33.01 Specification FR-5; DEL-33.02 Specification IR-3 |
| Novel/Non-Routine Work | First-time activities or significantly different methods | ASSUMPTION: SWMS for non-routine work |
| Employer/Regulatory Requirement | ER or WorkSafeBC specifically requires SWMS | TBD: ER SWMS requirements |
| Client/Terminal Request | DP World Terminal requests SWMS for work in sensitive areas | OBJ-5 Terminal Continuity; ASSUMPTION: Terminal interface |

## Construction

### SWMS Structure (Anticipated)

| Section | Content | Source |
|---------|---------|--------|
| Header | Project, package, activity, SWMS ID, revision, date | ASSUMPTION: Standard SWMS template |
| Activity Description | What, where, when, who, duration | Specification FR-1 |
| Risk Assessment Summary | Key hazards and risk ratings (from DEL-33.02) | DEL-33.02 Specification IR-2; Specification FR-2 |
| Scope of Work | Detailed description of work to be performed | Specification FR-1 |
| Legislation & Standards | Applicable codes, regulations, standards | DEL-33.01 Specification FR-3; Specification FR-3 |
| Roles & Responsibilities | Who does what (supervisor, workers, HSE, others) | DEL-33.01 Specification FR-2; Specification FR-4 |
| Plant & Equipment | Tools, equipment, materials required | Specification FR-5 |
| Step-by-Step Procedure | Sequential work steps with controls for each step | Specification FR-6 (core section) |
| Emergency Procedures | What to do if something goes wrong | Cross-reference: DEL-33.07; Specification FR-7 |
| Training & Competency | Required training, certifications, competency | DEL-33.01 Specification FR-7; Specification FR-8 |
| Sign-Off | Prepared by, reviewed by, approved by (signatures/dates) | Specification Verification |

### Control Measures in SWMS

| Control Type | Implementation in SWMS | Source |
|-------------|----------------------|--------|
| Elimination | Document how hazard is eliminated (if applicable) | DEL-33.02 Datasheet Control Hierarchy |
| Substitution | Specify less hazardous alternatives being used | DEL-33.02 Datasheet Control Hierarchy |
| Engineering Controls | Detail physical controls (barriers, ventilation, guarding) | DEL-33.02 Datasheet Control Hierarchy |
| Administrative Controls | Reference procedures, permits, training, supervision requirements | DEL-33.02 Datasheet Control Hierarchy |
| PPE | Specify required PPE for each step | DEL-33.02 Datasheet Control Hierarchy |

## References

### Decomposition Document

- **Source:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- **Sections Referenced:**
  - Section 1: Project Context
  - Section 2: Project Objectives (OBJ-5, OBJ-6, OBJ-7)
  - Section 4: Package Summary (36 packages)
  - Section 5: PKG-33 HSE Management (line 731)

### Internal Cross-References

- `_CONTEXT.md` — Deliverable identification
- **DEL-33.01 Occupational Health & Safety Plan** (primary interface):
  - Specification FR-5 (Safe Work Procedures) — requires SWMS for high-risk activities
  - Datasheet Project-Specific Hazards
  - Guidance Project-Specific Hazard Considerations
  - Procedure Step 4.4 (Safe Work Procedures and Permits)
- **DEL-33.02 Risk Assessments** (primary basis):
  - Specification IR-2 (Method Statements Interface) — SWMS based on risk assessments
  - Specification PR-3 (Actionability) — risk assessments inform SWMS
  - Guidance Risk Assessment to SWMS Workflow
  - Procedure Section 3.1 (Link to SWMS)
- DEL-33.07 — Emergency Response Plan (emergency procedures in SWMS)
- PKG-35 — Training & Handover (training requirements in SWMS)
- All technical packages (PKG-01 through PKG-26) — activity-specific SWMS

### External References (TBD)

- Employer's Requirements Volume 2 Part 1: General Requirements (SWMS requirements — **location TBD**)
- WorkSafeBC OH&S Regulation (safe work procedures)
- Contractor's Corporate SWMS Templates and Guidelines
- Industry SWMS examples (precedents for similar work)

---

**Document Status:** Pass 3/3 — Final reconciliation complete
**Generated:** 2026-01-28
**Cross-Document Consistency:** Verified against Specification, Guidance, Procedure
**Ready for:** WORKING_ITEMS session (human review and refinement)
