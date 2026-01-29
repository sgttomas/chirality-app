# Guidance: DEL-28.03 Design Coordination Installation & Test Records

## Purpose

This guidance document supports the development of **Design Coordination Installation & Test Records** for **PKG-28 Design Verification**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for design coordination, supporting design quality, constructability, and **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.03 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6)

This deliverable is classified as a **Record** under the **Design** discipline, to be produced by **D&B Contractor (QA/QC)**.

**Cross-Document References:**
- Datasheet.md — Identification, Attributes, Conditions, Construction, References
- Specification.md — Requirements FR-1 through FR-7, PR-1 through PR-3, IR-1 through IR-6, QR-1 through QR-4
- Procedure.md — Steps 1-8, Verification V-1 through V-5

**Source:** _CONTEXT.md (deliverable type, discipline, responsible party)

## Principles

**Engineering rationale (Design discipline):**

| Principle ID | Principle | Specification Req | Procedure Step |
|--------------|-----------|-------------------|----------------|
| P-1 | Coordination as Quality Assurance | QR-1 | Step 1.1 |
| P-2 | Early and Continuous Coordination | FR-2, IR-2 | Step 2, Step 5 |
| P-3 | Multi-Discipline Collaboration | IR-1 | Step 2, Step 4 |
| P-4 | 3D Model-Based Coordination (BIM) | FR-3, IR-5 | Step 3 |
| P-5 | Documented Decisions and Traceability | FR-1, FR-5, FR-6, QR-2 | Step 2.3, Step 6 |
| P-6 | Issue Tracking to Closure | FR-4, FR-7, PR-2 | Step 4, Step 5 |

**P-1: Coordination as Quality Assurance**
- Design coordination is a quality assurance process that reduces design errors, conflicts, and rework
- Systematic inter-discipline coordination improves design quality and constructability
- Coordination records demonstrate quality management practices
- **Requirement linkage:** Specification.md QR-1 (ISO 9001 Compliance)
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6)

**P-2: Early and Continuous Coordination**
- Early coordination identifies and resolves interface issues before they become costly
- Continuous coordination maintains alignment as designs evolve
- Intensive coordination before milestones (30%, 60%, 90%, IFC) ensures coordinated submissions
- **Requirement linkage:** Specification.md FR-2 (Meeting Frequency), IR-2 (Design Submissions)
- **Source:** Datasheet.md (Attributes: Coordination Phases)

**P-3: Multi-Discipline Collaboration**
- Large multi-discipline projects require active collaboration across disciplines
- No single discipline designs in isolation — interfaces affect all disciplines
- Coordination meetings bring disciplines together to resolve interfaces collaboratively
- **Requirement linkage:** Specification.md IR-1 (Discipline Packages)
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary: 36 packages)

**P-4: 3D Model-Based Coordination (BIM)**
- BIM and 3D coordination enable spatial clash detection difficult with 2D drawings alone
- Clash detection identifies physical conflicts before construction
- Resolving clashes in the model is far less costly than field resolution
- **Requirement linkage:** Specification.md FR-3 (Clash Detection), IR-5 (BIM Execution Plan)
- **Source:** Datasheet.md (Attributes: BIM/3D Coordination)

**P-5: Documented Decisions and Traceability**
- Coordination decisions shall be documented in meeting minutes, interface agreements, and RFI responses
- Documentation provides traceability and prevents disputes
- Clear documentation of responsibilities prevents coordination gaps
- **Requirement linkage:** Specification.md FR-1 (Meeting Documentation), FR-5 (RFI System), FR-6 (Interface Documentation), QR-2 (Record Quality)
- **Source:** Specification.md (FR-1, FR-5, FR-6)

**P-6: Issue Tracking to Closure**
- All coordination issues shall be tracked until resolved
- Issue tracking ensures nothing falls through the cracks
- Critical and high-priority issues shall be escalated
- **Requirement linkage:** Specification.md FR-4 (Clash Classification), FR-7 (Issue Tracking), PR-2 (Issue Resolution)
- **Source:** Specification.md (FR-4, FR-7, PR-2)

**Applicable standards context:**

| Standard | Application | Specification § |
|----------|-------------|-----------------|
| ISO 9001 | Quality Management — coordination as quality process | QR-1 |
| ISO 19650 | BIM standards (if BIM used) | IR-5 |
| Project BIM Standards | BIM coordination protocols | IR-5 |
| EGBC Practice Standards | Professional practice | Standards |

**Source:** Specification.md (Standards section)

## Considerations

**Factors to consider during development:**

| Consideration ID | Factor | Specification Req | Procedure Step |
|------------------|--------|-------------------|----------------|
| C-1 | Coordination Approach and Tools | IR-5, IR-6 | Step 1 |
| C-2 | Coordination Roles and Responsibilities | — | Step 1.2 |
| C-3 | Coordination Meeting Structure | FR-1, FR-2 | Step 2 |
| C-4 | BIM Coordination Strategy | FR-3, IR-5 | Step 3 |
| C-5 | RFI Process and Management | FR-5 | Step 4.2 |
| C-6 | Interface Definition and Documentation | FR-6 | Step 4.3 |
| C-7 | Coordination Issue Prioritization | FR-4, FR-7, PR-2 | Step 4.4, Step 5 |
| C-8 | Coordination Status Tracking and Reporting | IR-2 | Step 5 |
| C-9 | Record Management and Archiving | QR-3, QR-4 | Step 6, Step 7 |

**C-1: Coordination Approach and Tools**
- Establish coordination approach early (meetings, BIM, RFI process)
- Select coordination tools (meeting platforms, BIM software, RFI tracking) — **TBD**
- Develop coordination procedures consistent with QMP and BEP
- **Requirement linkage:** Specification.md IR-5 (BIM Execution Plan), IR-6 (QMS)
- **Source:** Specification.md (IR-5, IR-6)

**C-2: Coordination Roles and Responsibilities**
- Assign coordination roles: Coordination Lead, BIM Coordinator, RFI Coordinator
- Clarify roles in project kick-off
- **TBD**: Specific role assignments
- **Source:** Procedure.md (Personnel Requirements)

**C-3: Coordination Meeting Structure**
- Establish regular meeting schedule (weekly/bi-weekly during active design) — **TBD**
- Develop meeting agenda template
- Keep meetings focused; document decisions and action items
- **Requirement linkage:** Specification.md FR-1 (Meeting Documentation), FR-2 (Meeting Frequency)
- **Source:** Specification.md (FR-1, FR-2)

**C-4: BIM Coordination Strategy** (if BIM used)
- Develop BIM Execution Plan (BEP) — **TBD**
- Establish model standards, LOD requirements, coordination frequency
- Define clash detection protocol: software, classification, workflow, frequency
- **Requirement linkage:** Specification.md FR-3 (Clash Detection), IR-5 (BIM Execution Plan)
- **Source:** Specification.md (FR-3, IR-5)

**C-5: RFI Process and Management**
- Establish RFI process: format, numbering, routing, response timeframe — **TBD**
- Communicate RFI process to project team
- Monitor response times and escalate overdue RFIs
- **Requirement linkage:** Specification.md FR-5 (RFI System)
- **Source:** Specification.md (FR-5)

**C-6: Interface Definition and Documentation**
- Identify critical interfaces early in design
- Document interface agreements for complex/critical interfaces
- Verify interface agreements reflected in design documents
- **Requirement linkage:** Specification.md FR-6 (Interface Documentation)
- **Source:** Specification.md (FR-6)

**C-7: Coordination Issue Prioritization**
- Not all issues are equal — prioritize based on impact and urgency
- Critical issues (safety, code compliance, major conflicts) require immediate resolution
- Use priority classification to focus effort where it matters
- **Requirement linkage:** Specification.md FR-4 (Clash Classification), FR-7 (Issue Tracking), PR-2 (Issue Resolution)
- **Source:** Specification.md (FR-4, FR-7, PR-2)

**C-8: Coordination Status Tracking and Reporting**
- Track coordination status throughout design
- Report status at project meetings and design milestones
- Coordination status should be part of submission readiness assessment
- **Requirement linkage:** Specification.md IR-2 (Design Submissions)
- **Source:** Specification.md (IR-2)

**C-9: Record Management and Archiving**
- Maintain coordination records systematically throughout design
- File meeting minutes, clash reports promptly in document management system
- Export snapshots of living documents at milestones
- Plan for final records compilation
- **Requirement linkage:** Specification.md QR-3 (Document Control), QR-4 (Retention)
- **Source:** Specification.md (QR-3, QR-4, D-7)

**Package and Deliverable Context:**
- **Package scope:** PKG-28 Design Verification
- **Deliverable type:** Record — documentation of coordination activities
- **Coordination with adjacent packages:** See `_DEPENDENCIES.md` (NOT_TRACKED); coordinates with PKG-01 through PKG-36

**Source:** _CONTEXT.md; _DEPENDENCIES.md; Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4)

## Trade-offs

**Competing concerns to evaluate:**

| Trade-off ID | Trade-off | Considerations | Specification Req |
|--------------|-----------|----------------|-------------------|
| T-1 | Coordination Effort vs. Schedule | Thoroughness vs. time constraints | FR-2, IR-2 |
| T-2 | Coordination Formality vs. Flexibility | Traceability vs. overhead | FR-1, FR-5, QR-2 |
| T-3 | 2D vs. 3D Coordination | BIM effectiveness vs. effort | FR-3, IR-5 |
| T-4 | Coordination Frequency | Early issue detection vs. effort | FR-2, FR-3 |
| T-5 | Clash Resolution Threshold | Clean submissions vs. efficiency | FR-4, PR-2 |
| T-6 | Coordination Record Detail | Complete traceability vs. documentation effort | FR-1, QR-2 |

**T-1: Coordination Effort vs. Schedule**
- **Trade-off**: Thorough coordination requires time; aggressive schedule may limit coordination
- **Guidance**: Allocate sufficient time for coordination, especially before milestones; inadequate coordination leads to rework
- **Requirement linkage:** Specification.md FR-2 (Meeting Frequency), IR-2 (Design Submissions)

**T-2: Coordination Formality vs. Flexibility**
- **Trade-off**: Formal processes provide traceability but require overhead; informal is faster but less traceable
- **Guidance**: Use formal processes for decisions and critical interfaces; informal acceptable for routine coordination
- **Requirement linkage:** Specification.md FR-1 (Meeting Documentation), FR-5 (RFI System), QR-2 (Record Quality)

**T-3: 2D vs. 3D Coordination**
- **Trade-off**: 3D/BIM detects spatial clashes more effectively but requires BIM effort; 2D faster but misses 3D conflicts
- **Guidance**: Use 3D/BIM for complex, spatially congested projects; 2D may suffice for simpler projects
- **Requirement linkage:** Specification.md FR-3 (Clash Detection), IR-5 (BIM Execution Plan)
- **TBD**: BIM coordination requirement decision

**T-4: Coordination Frequency**
- **Trade-off**: Frequent coordination catches issues early but requires time; infrequent requires less effort but may miss issues
- **Guidance**: Frequent coordination (weekly/bi-weekly) during active development; always intensive before milestones
- **Requirement linkage:** Specification.md FR-2 (Meeting Frequency), FR-3 (Clash Detection)

**T-5: Clash Resolution Threshold**
- **Trade-off**: 100% clash resolution ensures clean submissions but may require significant effort; resolving only critical/major is more efficient
- **Guidance**: Resolve all critical and major clashes before submission; minor clashes may be deferred if documented
- **Requirement linkage:** Specification.md FR-4 (Clash Classification), PR-2 (Issue Resolution)

**T-6: Coordination Record Detail**
- **Trade-off**: Detailed records provide complete traceability but require significant effort; summary records more efficient but less traceable
- **Guidance**: Document decisions and critical discussions in minutes; comprehensive clash reports at milestones; balance detail with effort
- **Requirement linkage:** Specification.md FR-1 (Meeting Documentation), QR-2 (Record Quality)

## Examples

**Reference examples and precedents:**

**E-1: Sample Coordination Meeting Agenda and Minutes** — See Procedure.md Step 2.2, Step 2.3

**Agenda:**
1. Review action items from previous meeting
2. Design status update by discipline
3. Interface issues and coordination topics
4. Clash detection results review (if available)
5. RFI status and escalations
6. New action items
7. Next meeting scheduling

**Minutes (excerpt):**
```
Design Coordination Meeting Minutes
Meeting No: COORD-MTG-012
Date: 2026-02-15, 10:00-11:30 AM
Location: Project office / Teams

Attendees:
- John Smith (Civil Lead)
- Jane Doe (Structural Lead)
- Bob Johnson (Mechanical Lead)
- [etc.]

Action Items from Previous Meeting:
- AI-011-01: Civil to provide foundation elevations — CLOSED
- AI-011-02: Mechanical to review pipe routing conflict — OPEN

Interface Issues Discussed:
1. Tank foundation vs. pipe support elevation — RESOLVED
2. Electrical cable tray vs. mechanical piping — ASSIGNED
   Action Item AI-012-01: Coordinate routing (Due: 2026-02-22)

Next Meeting: 2026-02-22, 10:00 AM
```

**E-2: Sample Clash Detection Report Summary** — See Procedure.md Step 3.4

```
Clash Detection Report
Report Date: 2026-03-01
Model Stage: 90% Design
Software: Autodesk Navisworks 2025

Clash Summary:
Total: 127 | Critical: 3 | Major: 18 | Minor: 106

Clashes by Discipline Pair:
- Structural-Mechanical: 45 (2 Critical, 8 Major, 35 Minor)
- Mechanical-Electrical: 32 (0 Critical, 5 Major, 27 Minor)
- Civil-Structural: 18 (1 Critical, 3 Major, 14 Minor)

Critical Clashes (must resolve before submission):
1. Clash-90-001: Process pipe vs. structural beam at B3 — ASSIGNED
2. Clash-90-002: Foundation vs. drainage line — ASSIGNED
```

**E-3: Sample RFI Log Entry** — See Procedure.md Step 4.2

| RFI # | Originator | Addressee | Description | Submitted | Response | Responded | Status |
|-------|------------|-----------|-------------|-----------|----------|-----------|--------|
| RFI-045 | Mechanical | Civil | Equipment Pad #2 elevation clarification | 2026-02-10 | Correct: 10.8m. Dwg C-101 Rev B updated. | 2026-02-12 | Closed |
| RFI-046 | Electrical | Mechanical | Pump P-101 motor nameplate data | 2026-02-11 | 50 HP, 460V, 3-ph, NEMA 326T | 2026-02-14 | Closed |

**E-4: Sample Interface Register Entry** — See Procedure.md Step 4.3

| Interface ID | Discipline Pair | Description | Responsible | Criteria | Status |
|--------------|-----------------|-------------|-------------|----------|--------|
| INT-CS-01 | Civil-Structural | Tank foundation embedment | Civil: grade; Structural: foundation | TOF: 10.8m, FG: 11.0m (200mm cover) | Verified |
| INT-ME-02 | Mechanical-Electrical | Pump motor control | Mech: motor data; Elec: starter | 50 HP, 460V per DS-MECH-005; VFD per Spec E-001 | Agreed |

**Anticipated artifacts for reference:**
- Inter-discipline coordination records
- Clash detection reports
- RFI logs

**Source:** _CONTEXT.md (anticipated artifacts)

**TBD Items:**
- Employer's Requirements governing coordination — **TBD**: Specific ER sections
- Industry precedent examples — **TBD**: BIM coordination guides, best practices
- Lessons learned — **TBD**: Applicable lessons learned

## Cross-Document Consistency Notes

This guidance document has been verified for consistency with:
- **Datasheet.md**: Terminology, attribute values, and cross-references aligned
- **Specification.md**: All principles and considerations map to specific requirements
- **Procedure.md**: Considerations inform procedure steps; guidance supports procedural decisions

**Verification performed per:** AGENT_4_DOCUMENTS_REVISED_v3.md (Step 5, Cross-Reference and Iterate)
