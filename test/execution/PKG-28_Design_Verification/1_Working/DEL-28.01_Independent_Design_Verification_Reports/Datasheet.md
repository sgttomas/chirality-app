# Datasheet: DEL-28.01 Independent Design Verification Reports

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-28.01 |
| Name | Independent Design Verification Reports |
| Package | PKG-28 Design Verification |
| Discipline | Design |
| Type | Report |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Objective Mapping | OBJ-6: Regulatory Compliance |

**Source:** _CONTEXT.md (DEL-28.01); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 6, Objective-to-Deliverable Mapping)

## Attributes

| Attribute | Value | Specification § | Guidance § | Procedure Step |
|-----------|-------|-----------------|------------|----------------|
| Report Series | IDV-[Discipline]-[Stage] (e.g., IDV-CIVIL-30, IDV-STRUCT-60) | D-1, D-2 | E-1 | Step 4.3 |
| Review Stages | 30% Design, 60% Design, 90% Design, IFC (Issue for Construction) | FR-2 | P-3 | Step 7 |
| Disciplines Covered | Civil, Structural, Marine, Mechanical, Process, Electrical, I&C, Fire Protection | FR-3 | E-3 | Step 1.1 |
| Verification Scope | Compliance with codes, standards, Employer's Requirements, design criteria | FR-4 | P-4 | Step 3.1 |
| Review Method | Independent third-party technical review by qualified P.Eng. | FR-1, PR-3 | C-2 | Step 1.2 |
| Report Format | **TBD** — Per project document management system template | D-2 | C-8 | Step 4.1 |
| Classification | Project Controlled — Design Verification | QR-3 | C-8 | Step 5.1 |
| Typical Report Count | 8 disciplines × 4 stages = 32 reports — **ASSUMPTION** | FR-2, FR-3 | — | Records |

**Source:** _CONTEXT.md (DEL-28.01 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope, anticipated artifacts); Specification.md; Guidance.md; Procedure.md

## Conditions

**Operating / Environmental Context:**

Independent Design Verification (IDV) is a quality assurance process performed to verify that design deliverables comply with applicable codes, standards, and Employer's Requirements, supporting **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6; Section 6, Objective-to-Deliverable Mapping: DEL-28.01–DEL-28.03 associated with OBJ-6)

| Condition | Value | Specification § | Notes |
|-----------|-------|-----------------|-------|
| Design Submission Stages | 30%, 60%, 90%, IFC | FR-2 | **ASSUMPTION**: Typical D&B milestone sequence |
| Verification Timing | Prior to formal submission to authorities/Employer | IR-1, IR-2 | **TBD**: Specific submission gate requirements |
| Review Independence | Third-party verifiers independent of design team | FR-1, QR-1 | Per ISO 9001 quality requirements |
| Regulatory Context | VFPA, BC Building Code, CSA, ASME, API | FR-4 | **TBD**: Complete code list per discipline |
| Project Type | Design & Build — Contractor-led design | — | Per contract type |
| Review Duration | **TBD** days per submission | PR-2 | Per project schedule |

**Source:** _CONTEXT.md (DEL-28.01 responsible party: D&B Contractor); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 1.1, Contract Type: Design & Build)

## Construction

**Materials / Configuration:**

Anticipated artifacts:
- IDV reports (by discipline/submission stage)

**Typical IDV Report Structure** — See Specification.md (D-1), Guidance.md (E-1), Procedure.md (Step 4.1):

| Section | Content | Procedure Step |
|---------|---------|----------------|
| Executive Summary | Key findings, overall compliance status | Step 4.1 (1) |
| Introduction | Review scope, methodology, criteria | Step 4.1 (2) |
| Reviewer Qualifications | Credentials, certifications, independence statement | Step 4.1 (3) |
| Design Documents Reviewed | Document list with revision numbers | Step 4.1 (4) |
| Compliance Checklist | Code/standard verification by section | Step 4.1 (5) |
| Findings | NCRs with severity, description, code refs, recommendations | Step 4.1 (6) |
| Closure Verification | Status of previous stage findings | Step 4.1 (7) |
| Verification Statement | Compliance conclusion, Lead Reviewer signature | Step 4.1 (8) |
| Appendices | Detailed checklists, supporting docs | Step 4.1 (9) |

**Review Coverage by Discipline** — See Specification.md (FR-3), Guidance.md (E-3):

| Discipline | Typical Coverage | Related Packages |
|------------|------------------|------------------|
| Civil | Site grading, drainage, pavement, foundations | PKG-01, PKG-04 |
| Structural | Concrete, steel, marine structures, rail works | PKG-06, PKG-07, PKG-08 |
| Marine | Marine outfitting, fender systems, mooring | PKG-09 |
| Mechanical | Storage tanks, piping, pumps, valves | PKG-10, PKG-12, PKG-13 |
| Process | Railcar unloading, marine loading, metering | PKG-11, PKG-14, PKG-15 |
| Electrical | Power distribution, lighting, grounding | PKG-17, PKG-18 |
| I&C | Control systems, instrumentation, safety systems | PKG-19, PKG-20 |
| Fire Protection | Detection, suppression, sprinkler systems | PKG-22 |

**TBD**: Specific scope per discipline

**Source:** _CONTEXT.md (anticipated artifacts); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary)

## Cross-Deliverable Coordination

| Related Deliverable | Relationship | Specification § |
|--------------------|--------------|-----------------|
| DEL-27.04 Design Submission Packages | IDV reports submitted alongside design packages | IR-1, D-4 |
| DEL-28.02 VFPA IP Review Responses | IDV addresses issues raised during IP review | IR-2 |
| DEL-28.03 Design Coordination Records | IDV verifies resolution of coordination issues | IR-2 |
| DEL-32.xx Regulatory/Permits | IDV supports permit applications | IR-2, V-4 |

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope); Specification.md (Interface Requirements)

## References

| Reference | Status | Notes |
|-----------|--------|-------|
| _REFERENCES.md | See file | Applicable reference documents |
| 0_References/ | See folder | Package reference materials |
| ISO 9001 | Applicable | Quality Management Systems |
| Employer's Requirements | **TBD** | Specific ER sections governing IDV |
| BC Building Code | Applicable | **TBD**: Specific sections |
| CSA Standards | Applicable | **TBD**: Specific standards by discipline |
| ASME/API Standards | Applicable | **TBD**: Specific standards by discipline |
| _DEPENDENCIES.md | NOT_TRACKED | Dependencies coordinated externally |

**Cross-Document Traceability:**
- Specification.md — Requirements (FR-1 through FR-6, PR-1 through PR-3, IR-1 through IR-4, QR-1 through QR-3)
- Guidance.md — Principles (P-1 through P-5), Considerations (C-1 through C-8), Trade-offs (T-1 through T-6)
- Procedure.md — Steps 1-7, Verification V-1 through V-5

**Source:** Specification.md; Guidance.md; Procedure.md
