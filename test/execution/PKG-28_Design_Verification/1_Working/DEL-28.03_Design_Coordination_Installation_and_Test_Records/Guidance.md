# Guidance: DEL-28.03 Design Coordination Installation & Test Records

## Purpose

This guidance document supports the development of **Design Coordination Installation & Test Records** for **PKG-28 Design Verification**.

**Deliverable Purpose:** Provides evidence of completion, inspection, and testing for design coordination, supporting design quality, constructability, and **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.03 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6)

This deliverable is classified as a **Record** under the **Design** discipline, to be produced by **D&B Contractor (QA/QC)**.

**Source:** _CONTEXT.md (deliverable type, discipline, responsible party)

## Principles

**Engineering rationale (Design discipline):**

**P-1: Coordination as Quality Assurance**
- Design coordination is a quality assurance process that reduces design errors, conflicts, and rework
- Systematic inter-discipline coordination improves design quality, constructability, and operational performance
- Coordination records demonstrate that quality management practices were followed
- Effective coordination supports **OBJ-6: Regulatory Compliance** by ensuring designs are internally consistent and meet requirements
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6); Specification.md (QR-1: ISO 9001 Compliance); **ASSUMPTION**: Coordination as QA practice

**P-2: Early and Continuous Coordination**
- Early coordination (starting at conceptual/preliminary design) identifies and resolves interface issues before they become costly to fix
- Continuous coordination throughout design development maintains alignment as designs evolve
- Intensive coordination before design milestones (30%, 60%, 90%, IFC) ensures coordinated submissions
- "Coordinate early and often" principle reduces downstream rework and construction issues
- **Source:** Specification.md (FR-2: Coordination Meeting Frequency); Datasheet.md (coordination phases aligned with design stages); **ASSUMPTION**: Early coordination best practice

**P-3: Multi-Discipline Collaboration**
- Large multi-discipline projects require active collaboration and communication across disciplines
- No single discipline can design in isolation — interfaces affect all disciplines
- Coordination meetings and forums bring disciplines together to resolve interfaces collaboratively
- Respectful, collaborative coordination culture improves project outcomes
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary: 36 packages, multi-discipline project); **ASSUMPTION**: Collaboration principle for complex projects

**P-4: 3D Model-Based Coordination (BIM)**
- Building Information Modeling (BIM) and 3D model-based coordination enable spatial clash detection that is difficult to achieve with 2D drawings alone
- Clash detection identifies physical conflicts (pipes passing through beams, equipment colliding with structures, etc.) before construction
- Resolving clashes in the model is far less costly than resolving conflicts in the field during construction
- BIM coordination supports constructability and **OBJ-9: Lifecycle Cost Optimization** by reducing construction rework
- **Source:** Datasheet.md (BIM/3D modeling requirement, clash detection); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-9); **ASSUMPTION**: BIM coordination value proposition

**P-5: Documented Decisions and Traceability**
- Coordination decisions shall be documented in meeting minutes, interface agreements, and RFI responses
- Documentation provides traceability and prevents "he said, she said" disputes later in design or construction
- Clear documentation of responsibilities (who is responsible for what interface element) prevents coordination gaps
- Records demonstrate due diligence and professional practice
- **Source:** Specification.md (FR-1, FR-5, FR-6); **ASSUMPTION**: Documentation and traceability principles

**P-6: Issue Tracking to Closure**
- All coordination issues (clashes, RFIs, interface questions) shall be tracked until resolved
- Issue tracking ensures nothing "falls through the cracks"
- Critical and high-priority issues shall be escalated to ensure timely resolution
- Issue closure prior to design submission ensures submissions are coordinated and ready for review
- **Source:** Specification.md (FR-4, FR-5, FR-7, PR-2); **ASSUMPTION**: Issue management best practice

**Applicable standards context:**
- ISO 9001 — Quality Management Systems (design coordination as quality process)
- ISO 19650 — Building Information Modeling (BIM) standards (if BIM is used)
- **TBD**: Project-specific BIM standards and protocols
- Employer's Requirements — **TBD**: Specific ER sections governing design coordination requirements
- Professional practice standards (EGBC) — Coordination as part of professional design responsibility

**Source:** Specification.md (Standards section); Datasheet.md (applicable standards)

## Considerations

**Factors to consider during development:**

**C-1: Coordination Approach and Tools**
- Establish coordination approach early in project (coordination meetings, BIM coordination, RFI process)
- Select coordination tools (meeting platforms, BIM software, RFI tracking system, issue tracking system) — **TBD**: Specific tool selections
- Develop coordination procedures and protocols consistent with project QMP and BIM Execution Plan (if applicable)
- Train project team on coordination processes and tools
- **Source:** Specification.md (IR-5, IR-6); Datasheet.md (coordination methods); **ASSUMPTION**: Coordination approach planning

**C-2: Coordination Roles and Responsibilities**
- Assign coordination roles:
  - Design Coordination Lead (overall coordination responsibility)
  - Discipline Design Leads (represent their disciplines in coordination)
  - BIM Coordinator (if BIM is used) — manages models, performs clash detection
  - RFI Coordinator — manages RFI process and tracking
- Clarify coordination responsibilities in project kick-off and team charter
- **TBD**: Specific role assignments and authority levels
- **ASSUMPTION**: Clear roles improve coordination effectiveness

**C-3: Coordination Meeting Structure**
- Establish regular coordination meeting schedule (weekly or bi-weekly during active design) — **TBD**: Meeting frequency
- Develop coordination meeting agenda template:
  - Review action items from previous meeting
  - Review current design status by discipline
  - Identify and discuss interface issues
  - Review clash detection results (if available)
  - Assign action items for resolution
  - Schedule next meeting
- Keep meetings focused and productive — document decisions and action items clearly
- **Source:** Specification.md (FR-1, FR-2); Datasheet.md (coordination meeting minutes format); **ASSUMPTION**: Effective meeting management

**C-4: BIM Coordination Strategy** (if BIM is used)
- Develop BIM Execution Plan (BEP) defining BIM coordination requirements — **TBD**: BEP development and approval
- Establish model standards, Level of Development (LOD) requirements, coordination frequency
- Define clash detection protocol:
  - Clash detection software and settings
  - Clash classification criteria
  - Clash resolution workflow
  - Clash detection frequency (e.g., weekly during design development, before each design milestone)
- Coordinate model federation (combining discipline models for clash detection)
- **Source:** Specification.md (FR-3, FR-4, IR-5); Datasheet.md (BIM coordination); **ASSUMPTION**: BIM coordination planning if BIM is used

**C-5: RFI Process and Management**
- Establish RFI process including:
  - RFI submittal format and requirements
  - RFI numbering system
  - RFI distribution and routing (who receives RFIs, who responds)
  - RFI response timeframe requirements — **TBD**: Response timeframe
  - RFI tracking system (spreadsheet, database, project management software)
- Communicate RFI process to all project team members
- Monitor RFI response times and escalate overdue RFIs
- **Source:** Specification.md (FR-5); Datasheet.md (RFI logs); **ASSUMPTION**: RFI process management

**C-6: Interface Definition and Documentation**
- Identify critical interfaces between disciplines early in design
- Document interface agreements for complex or critical interfaces (elevations, locations, loads, connection details)
- Use interface registers or interface control documents to track interface status
- Verify interface agreements are reflected in design documents (drawings, specifications, calculations)
- **Source:** Specification.md (FR-6); Datasheet.md (interface registers); **ASSUMPTION**: Interface management for critical coordination points

**C-7: Coordination Issue Prioritization**
- Not all coordination issues are equal — prioritize based on impact and urgency
- Critical issues (safety, code compliance, major conflicts) require immediate resolution
- Major issues (functionality, constructability) should be resolved before design submission
- Minor issues (preferences, optimization) can be resolved during design development or construction
- Use priority classification to focus coordination effort where it matters most
- **Source:** Specification.md (FR-4, FR-7, PR-2); Datasheet.md (clash and issue classification); **ASSUMPTION**: Risk-based prioritization

**C-8: Coordination Status Tracking and Reporting**
- Track coordination status (meetings held, clashes detected/resolved, RFIs open/closed) throughout design
- Report coordination status at project meetings and design milestones
- Coordination status summary should be part of design submission readiness assessment
- Demonstrate to Employer and reviewers that coordination was performed systematically
- **Source:** Specification.md (IR-2: coordination supports design submissions); **ASSUMPTION**: Status tracking and reporting

**C-9: Record Management and Archiving**
- Maintain coordination records systematically throughout design (don't wait until end to compile)
- File meeting minutes, clash reports, and other records promptly in document management system
- Maintain living documents (RFI logs, issue logs) in accessible location with current status
- Export snapshots of living documents at design milestones for archival
- Plan for final coordination records compilation at project completion
- **Source:** Specification.md (QR-3, D-7); **ASSUMPTION**: Systematic record management

**Package scope:** PKG-28 Design Verification

**Deliverable type:** Record — documentation of coordination activities and decisions

**Coordination with adjacent packages:** See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally by humans); this deliverable coordinates with all discipline packages (PKG-01 through PKG-36)

**Source:** _CONTEXT.md (package, type); _DEPENDENCIES.md (dependency tracking mode); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary)

**Employer's Requirements:** Review ER for project-specific design coordination requirements — **TBD**: Specific ER sections

**Regulatory requirements:** Design coordination supports regulatory compliance by ensuring designs are internally consistent and meet all requirements — **OBJ-6**

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6)

**Constructability:** Effective design coordination improves constructability by resolving conflicts before construction — supports project success

**Operability and maintainability:** Coordination ensures operational and maintenance access requirements are addressed across disciplines

## Trade-offs

**Competing concerns to evaluate:**

**T-1: Coordination Effort vs. Schedule**
- **Trade-off**: Thorough coordination requires time for meetings, clash detection, issue resolution; aggressive schedule may limit coordination time
- **Consideration**: Inadequate coordination leads to construction rework and delays that exceed time saved during design
- **Guidance**: Allocate sufficient time for coordination, especially before design milestones; intensive coordination before submissions is critical
- **Source:** Specification.md (FR-2, IR-2); **ASSUMPTION**: Coordination investment prevents downstream delays

**T-2: Coordination Formality vs. Flexibility**
- **Trade-off**: Formal coordination processes (documented meetings, structured RFI system) provide traceability but require overhead; informal coordination (emails, phone calls) is faster but less traceable
- **Consideration**: Balance formality with project size, complexity, and risk
- **Guidance**: Use formal processes for decisions, critical interfaces, and complex coordination; informal communication acceptable for routine coordination; document significant decisions regardless of formality
- **Source:** Specification.md (FR-1, FR-5); Guidance.md (P-5: Documented Decisions)

**T-3: 2D vs. 3D Coordination**
- **Trade-off**: 3D model-based coordination (BIM) detects spatial clashes more effectively but requires BIM modeling effort and software; 2D drawing-based coordination is faster for simple projects but misses 3D conflicts
- **Consideration**: Project complexity, spatial congestion, and risk of conflicts
- **Guidance**: Use 3D/BIM coordination for complex, spatially congested projects (e.g., congested pipe racks, equipment areas, marine structures); 2D coordination may suffice for simpler, less congested projects
- **TBD**: BIM coordination requirement decision for this project
- **Source:** Specification.md (FR-3: BIM clash detection); Datasheet.md (BIM/3D modeling); Guidance.md (P-4: BIM coordination value)

**T-4: Coordination Frequency**
- **Trade-off**: Frequent coordination (weekly meetings, frequent clash detection) catches issues early but requires significant time investment; infrequent coordination (monthly meetings, milestone-based clash detection) requires less effort but may miss issues until late
- **Consideration**: Design pace, project complexity, and coordination risk
- **Guidance**: Frequent coordination (weekly/bi-weekly) during active design development; less frequent (monthly) during slow periods; always intensive coordination before design milestones
- **Source:** Specification.md (FR-2, FR-3); Datasheet.md (coordination frequency); Guidance.md (P-2: Early and Continuous Coordination)

**T-5: Clash Resolution Threshold**
- **Trade-off**: Resolving 100% of clashes before design submission ensures clean submissions but may require significant effort for minor clashes; resolving only critical/major clashes is more efficient but may defer minor issues to construction
- **Consideration**: Risk and impact of unresolved clashes
- **Guidance**: Resolve all critical and major clashes before design submission; minor clashes may be deferred if documented and have low risk
- **Source:** Specification.md (FR-4, PR-2); Datasheet.md (clash classification); Guidance.md (C-7: Prioritization)

**T-6: Coordination Record Detail**
- **Trade-off**: Detailed coordination records (verbatim meeting transcripts, comprehensive clash reports) provide complete traceability but require significant documentation effort; summary records (action items only, clash counts) are more efficient but less traceable
- **Consideration**: Professional liability, quality management, and regulatory requirements
- **Guidance**: Document decisions, action items, and critical discussions in meeting minutes; comprehensive clash reports at design milestones; summary updates during design development; balance detail with effort
- **Source:** Specification.md (FR-1: meeting minutes requirements, D-1 through D-5: record format); Guidance.md (P-5: Documentation and Traceability)

## Examples

**Reference examples and precedents:**

**E-1: Sample Coordination Meeting Agenda and Minutes** — **ASSUMPTION**: Standard format

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
- Sarah Lee (Electrical Lead)
- [etc.]

Action Items from Previous Meeting:
- AI-011-01: Civil to provide foundation elevations for Tank 1 — CLOSED (provided on Dwg C-201 Rev B)
- AI-011-02: Mechanical to review pipe routing conflict at Grid A5 — OPEN (in progress, update at next meeting)

Design Status Update:
- Civil: 60% design nearing completion, final grading plan issued
- Structural: Tank foundation design complete, wharf design in progress
- [etc.]

Interface Issues Discussed:
1. Tank foundation elevation vs. pipe support elevation — RESOLVED: Structural to raise foundation 100mm to provide clearance for pipe support
2. Electrical cable tray routing conflict with mechanical piping at Equipment Area — ASSIGNED: Electrical and Mechanical to coordinate routing offline and report back
   Action Item AI-012-01: Electrical/Mechanical coordinate cable tray vs. piping routing at Equipment Area (Due: 2026-02-22)

Next Meeting: 2026-02-22, 10:00 AM
```

**E-2: Sample Clash Detection Report Summary** — **ASSUMPTION**: Typical BIM clash report

```
Clash Detection Report
Report Date: 2026-03-01
Model Stage: 90% Design
Models Analyzed:
- Civil Model Rev 90%
- Structural Model Rev 90%
- Mechanical Model Rev 90%
- Electrical Model Rev 90%
Software: Autodesk Navisworks 2025

Clash Summary:
Total Clashes Detected: 127
- Critical: 3
- Major: 18
- Minor: 106

Clashes by Discipline Pair:
- Structural-Mechanical: 45 clashes (2 Critical, 8 Major, 35 Minor)
- Mechanical-Electrical: 32 clashes (0 Critical, 5 Major, 27 Minor)
- Civil-Structural: 18 clashes (1 Critical, 3 Major, 14 Minor)
- [etc.]

Critical Clashes (must be resolved before 90% submission):
1. Clash-90-001 [Critical]: Process pipe conflicts with main structural beam at Grid B3 (Structural-Mechanical) — ASSIGNED to Mechanical to reroute pipe
2. Clash-90-002 [Critical]: Foundation conflicts with underground drainage line (Civil-Structural) — ASSIGNED to Civil to relocate drainage
3. [etc.]

Status:
- Clashes from 60% review: 89 clashes, 87 resolved, 2 remain open (both Minor)
- New clashes at 90%: 127 clashes identified
- Target: Resolve all Critical and Major clashes before 90% submission (2026-03-15)
```

**E-3: Sample RFI Log Entry** — **ASSUMPTION**: Standard RFI tracking format

| RFI # | Originator | Addressee | Description | Date Submitted | Response | Date Responded | Status |
|-------|------------|-----------|-------------|----------------|----------|----------------|--------|
| RFI-045 | Mechanical | Civil | What is the elevation of the finished grade at Equipment Pad #2? Drawing C-101 shows 10.5m but Drawing C-102 shows 10.8m. Please clarify. | 2026-02-10 | Correct elevation is 10.8m. Drawing C-101 Rev B will be updated to match. | 2026-02-12 | Closed |
| RFI-046 | Electrical | Mechanical | Please provide motor nameplate data (HP, voltage, frame) for Pump P-101 so electrical can size motor starter. | 2026-02-11 | Motor data provided: 50 HP, 460V, 3-phase, NEMA Frame 326T. See updated Mechanical Datasheet DS-MECH-005 Rev A. | 2026-02-14 | Closed |
| RFI-047 | Structural | Marine | What is the design vessel berthing load for marine loading wharf? Fender datasheet required for structural design. | 2026-02-12 | Fender datasheet to be provided by Marine by 2026-02-20. Design vessel: Handymax 40,000 DWT, berthing energy per calculation CALC-MAR-003. | 2026-02-20 | Closed |

**E-4: Sample Interface Register Entry** — **ASSUMPTION**: Interface documentation format

| Interface ID | Discipline Pair | Interface Description | Responsible Discipline | Interface Criteria | Status | Notes |
|--------------|-----------------|----------------------|------------------------|-------------------|--------|-------|
| INT-CS-01 | Civil-Structural | Tank foundation embedment elevations | Civil provides grade, Structural provides foundation top elevation | Top of foundation: 10.8m, Finished grade: 11.0m (200mm cover over foundation) | Agreed | Verified on Dwgs C-101 Rev B and S-201 Rev A |
| INT-ME-02 | Mechanical-Electrical | Pump motor control interfaces | Mechanical provides motor data, Electrical provides motor control | Motor: 50 HP, 460V, 3-ph per DS-MECH-005; Starter: VFD per Spec E-001 | Agreed | VFD location shown on Dwg E-301 Rev A |

**Anticipated artifacts for reference:**
- Inter-discipline coordination records
- Clash detection reports
- RFI logs

**Source:** _CONTEXT.md (anticipated artifacts)

**Refer to Employer's Requirements for project-specific expectations** — **TBD**: Specific ER sections governing design coordination requirements

**Industry precedent and best practice examples** — **TBD**: Reference to BIM coordination guides, design coordination best practices, lessons learned from similar multi-discipline projects

**Lessons learned from similar facilities** — **TBD**: Applicable lessons learned regarding effective design coordination
