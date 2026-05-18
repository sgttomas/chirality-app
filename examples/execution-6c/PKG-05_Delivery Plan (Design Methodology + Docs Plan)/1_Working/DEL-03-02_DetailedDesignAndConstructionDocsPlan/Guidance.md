# Guidance: DEL-03-02 Detailed Design and Construction Docs Plan

## Purpose

### Why This Deliverable Exists
This plan document exists to demonstrate to the Town of Penhold that the Design-Build team has a credible, controlled approach to producing complete, coordinated, and code-compliant construction documents. In a Design-Build procurement, the Owner must evaluate whether the proponent can reliably translate conceptual design into executable construction documentation. This deliverable provides that assurance.

**Downstream use:**
- **Owner evaluation:** RFP evaluation criteria under "Project Delivery Plan" (10 points per decomposition Section 15) — clarity and credibility of the documentation plan contribute to scoring
- **Team alignment:** Serves as the internal roadmap for the design team during the post-award design phase
- **Risk mitigation:** Identifies quality control checkpoints and coordination procedures to reduce the risk of design errors, omissions, or conflicts that could delay permitting or construction

*Source: Decomposition Section 8 (DEL-03-02 description and downstream use), Section 15 (evaluation criteria), RFP Section 7.1.8 — location TBD*

---

## Principles

### P-01: Completeness Before Issuance
**Principle:** Documents should not be issued for construction until all disciplines are complete and coordinated.

**Rationale:** Incomplete or uncoordinated documents lead to:
- Construction delays (trades waiting for missing information)
- Change orders and cost overruns (conflicts discovered in the field)
- Quality issues (workarounds due to lack of design clarity)

A rigorous completeness check at each phase (especially CD and IFC) prevents these costly outcomes. The plan must define what "complete" means for each discipline and how completeness will be verified.

*Source: Industry best practice (ASSUMPTION); DBIA Design-Build quality guidelines*

---

### P-02: Coordination is Continuous, Not a Single Event
**Principle:** Interdisciplinary coordination must occur throughout the design process, not just at the end.

**Rationale:** Waiting until CD phase to coordinate disciplines results in:
- Major conflicts discovered too late to resolve efficiently
- Rework and wasted effort
- Compressed timelines and stress

Continuous coordination (weekly meetings, incremental BIM clash detection, overlay reviews during DD) catches issues early when they are easier and cheaper to fix. The plan must define coordination frequency, methods, and responsibilities.

*Source: Industry best practice (ASSUMPTION); BIM coordination standards (ISO 19650 or equivalent)*

---

### P-03: Owner Engagement at Key Milestones
**Principle:** The Owner must have formal opportunities to review and approve design at phase gates (SD, DD, CD).

**Rationale:** In a Design-Build model, the Owner retains design approval authority even though the Design-Builder has design responsibility. Formal review cycles ensure:
- Owner requirements (OSR, functional program) are met
- Design intent aligns with Owner expectations
- Owner has opportunity to course-correct before construction

The plan must define submittal formats, review periods, comment incorporation procedures, and approval signoffs.

*Source: Design-Build contract structure (ASSUMPTION); RFP Section 7.1.8 Owner review expectations — location TBD*

---

### P-04: QA/QC is Multi-Layered
**Principle:** Quality assurance requires checks at multiple levels: self-check (discipline), peer review (Design Manager), third-party review (code specialist, constructability), and Owner review.

**Rationale:** No single reviewer can catch all errors. Each layer targets different types of issues:
- **Self-check:** Discipline-specific completeness and accuracy
- **Design Manager review:** Cross-discipline consistency and coordination
- **Code review:** Building code and life safety compliance
- **Constructability review:** Buildability, sequencing, cost alignment
- **Owner review:** Owner requirements and operational suitability

The plan must define which QA/QC layers apply at which phases and who is responsible for each.

*Source: Industry best practice (ASSUMPTION); SOW-027 (quality management plan reference in decomposition)*

---

### P-05: Document Control Prevents Chaos
**Principle:** Without rigorous document control (numbering, revision tracking, distribution), projects devolve into confusion about which version is current.

**Rationale:** Poor document control leads to:
- Trades building to outdated drawings
- Conflicts between versions (field uses one revision, shop drawings reference another)
- Legal/warranty issues (no clear record of what was approved)

A robust document control system ensures everyone is working from the same information. The plan must define numbering conventions, revision protocols, and distribution/access controls.

*Source: Industry best practice (ASSUMPTION); ISO 9001 quality management principles*

---

### P-06: Addenda Requirements Must Be Traceable
**Principle:** Addendum 03 (and earlier addenda) introduced specific technical requirements that must be verifiable in the final documents.

**Rationale:** The RFP explicitly integrated addenda into the scope (decomposition Section 3, hard constraint C-07: addenda acknowledgment required). Failure to incorporate addenda requirements (e.g., 16 ft overhead doors, bay sumps, fire apparatus exhaust, generator, solar-ready provisions) could:
- Result in non-compliance with Owner requirements
- Trigger costly redesign during construction
- Undermine credibility with the Owner

The plan must explicitly call out addenda-driven requirements in each discipline's scope and include a verification checklist.

*Source: Decomposition Section 3 (hard constraint C-07), Section 4 (Addendum 03 impacts summary)*

---

## Considerations

### Design Phase Pacing and Overlap
**Consideration:** Should design phases be sequential (complete DD before starting CD) or overlapping (start CD on portions while DD is still in progress on others)?

**Factors to weigh:**
- **Sequential approach:** Reduces rework risk (full coordination before advancing); but may extend overall timeline
- **Overlapping approach (fast-track):** Compresses schedule; but increases risk of changes propagating into already-advanced work
- **Hybrid approach:** Advance low-risk or long-lead-time elements (e.g., foundations, structural steel procurement) while maintaining sequential approach for coordinated systems (MEP)

**Recommendation for plan:** Define which elements can safely advance and which must wait for full coordination. Tie to project schedule (DEL-08-01) and critical path.

*Source: ASSUMPTION based on Design-Build scheduling best practices; specific phasing strategy from RFP Section 7.1.8 — location TBD*

---

### BIM vs. 2D CAD Workflow
**Consideration:** Should the project use full BIM coordination (3D models) or traditional 2D CAD?

**Factors to weigh:**
- **BIM advantages:** Superior clash detection for MEP/structural; easier visualization for Owner; better as-built records
- **BIM challenges:** Requires compatible software across all disciplines; higher upfront modeling effort; may not be required by Owner
- **2D CAD advantages:** Familiar to all trades; faster for some disciplines (civil, site); lower software/training overhead
- **Hybrid approach:** BIM for building (structure + MEP); 2D for site/civil

> **[SL:B-005]** The plan should take a clear position on BIM vs. 2D rather than deferring entirely. For proposal credibility, recommend BIM if: (1) Owner has BIM requirement, (2) project complexity warrants 3D coordination, or (3) team has strong BIM capabilities. If BIM is not recommended, state rationale (e.g., "hybrid approach acceptable given building simplicity and team 2D expertise"). Decision criteria should be explicit. *(SourcePath: Guidance.md § Considerations / BIM vs. 2D CAD Workflow vs. Procedure assumption)*

**Recommendation for plan:** Take a position on BIM approach for the proposal. Recommended default: BIM-first for building (structure + MEP clash detection); 2D acceptable for site/civil. If BIM, specify coordination software platform and file exchange protocols. Justify the choice based on project complexity, team capabilities, and Owner preferences (if known).

*Source: ASSUMPTION (industry trend toward BIM for municipal facilities of this scale); RFP requirements for BIM — location TBD*

---

### Owner Review Period Duration
**Consideration:** How long should the Owner review period be at each phase gate?

**Factors to weigh:**
- **Shorter period (1-2 weeks):** Keeps project on schedule; reduces idle time for design team
- **Longer period (3-4 weeks):** Allows thorough Owner review; accommodates Owner's internal approvals (council, stakeholders)
- **RFP requirements:** May specify review period expectations

**Recommendation for plan:** Propose a reasonable period (e.g., 2-3 weeks for DD and CD; 1 week for minor revisions) and state that this is subject to Owner negotiation in the contract. Build this duration into DEL-08-01 (project schedule).

*Source: ASSUMPTION (typical municipal project review periods); RFP contract terms — location TBD*

---

### Code Review: Third-Party vs. Internal
**Consideration:** Should code compliance be reviewed by an independent third-party code consultant or by the Design-Builder's internal staff?

**Factors to weigh:**
- **Third-party advantages:** Independent verification; may be required by AHJ or Owner; reduces liability risk
- **Third-party challenges:** Adds cost; extends schedule; requires coordination with external reviewer
- **Internal review advantages:** Faster; lower cost; integrated into design workflow
- **Internal review risk:** Potential for bias or missed issues (lack of independence)

> **[SL:X-003]** The proposal must state the recommended code review approach (third-party vs. internal) with clear rationale substantiating the choice. Include: (1) team code expertise qualifications, (2) cost estimate impact (if third-party), (3) timeline impact, and (4) risk mitigation approach (if internal). This substantiates the ruling on which approach is recommended. *(SourcePath: Guidance.md § Considerations / Code Review: Third-Party vs. Internal)*

**Recommendation for plan:** Propose third-party code review at CD phase (before permit submission) as a best practice for Fire Hall facilities (life safety criticality). State that this is included in the base proposal cost (or as an allowance). The proposal must justify the choice with supporting rationale about team capacity, risk, and cost. Clarify if this is an Owner requirement or a proponent value-add.

*Source: ASSUMPTION (common for municipal facilities, especially Fire Halls with life safety criticality); RFP requirements or Owner preferences — location TBD*

---

### Permit Coordination with AHJ
**Consideration:** How will permit review comments from the authority having jurisdiction (AHJ) be incorporated?

**Factors to weigh:**
- **Permit review timeline:** Typically 4-8 weeks for municipal projects (ASSUMPTION)
- **Comment incorporation:** May require minor revisions (address and resubmit quickly) or major revisions (redesign and recirculate to Owner)
- **IFC issuance timing:** Should IFC set wait until permit is fully approved, or issue conditionally with permit comments tracked?

**Recommendation for plan:** State that permit comments will be incorporated into the IFC set before construction begins; define process for tracking and verifying permit comment closeout. Include permit review duration in DEL-08-01 (project schedule).

*Source: ASSUMPTION (typical permitting workflow); RFP contract terms or Appendix A (OSR) permitting expectations — location TBD*

---

### As-Built Documentation Requirements
**Consideration:** Should the plan address as-built (record drawing) requirements, or is that outside the scope of DEL-03-02?

**Factors to weigh:**
- **As-builts are part of closeout:** Typically covered in DEL-06-01 (Commissioning, Closeout, Warranty narrative)
- **But as-builts derive from construction documents:** The IFC set is the baseline; field changes are marked up during construction
- **Document control connection:** As-builts are a document issuance category ("Issued for Record")

**Recommendation for plan:** Briefly mention that IFC documents will serve as the baseline for as-built markups, and reference DEL-06-01 for full closeout/as-built procedures. Include "Issued for Record" as an issuance designation in document control protocols.

*Source: Decomposition Section 8 (DEL-06-01 covers closeout); industry practice (ASSUMPTION)*

---

## Trade-offs

### T-01: Speed vs. Thoroughness in QA/QC
**Competing concerns:**
- **Speed:** Minimize review cycles to meet aggressive schedule (faster to Owner review, faster to permit, faster to construction)
- **Thoroughness:** Ensure all checks are completed to prevent errors and omissions (reduces rework and change orders)

**Impact:** Cutting QA/QC checkpoints or review periods can compress the schedule but increases the risk of design errors escaping into construction, which typically costs 10x more to fix in the field than on paper.

**Guidance for plan:** Define minimum QA/QC checkpoints (self-check, Design Manager review, code review) as non-negotiable. If schedule pressure arises, accelerate by adding resources (more reviewers in parallel) rather than skipping checks.

*Source: Industry cost-of-quality studies (ASSUMPTION: 10x multiplier for field corrections); decomposition OBJ-008 (manage risk transparently)*

---

### T-02: Detail Level at Each Phase
**Competing concerns:**
- **More detail earlier (DD phase):** Provides better cost estimating accuracy; reduces unknowns; but requires more upfront effort
- **Less detail at DD, more at CD:** Faster DD phase; allows flexibility for value engineering; but risks scope creep and surprises

**Impact:** For Design-Build, cost certainty is critical (fixed-price contract context). Insufficient detail at DD can lead to budget overruns discovered at CD when it's too late to adjust.

**Guidance for plan:** Define detail expectations at each phase (e.g., DD = system selections finalized, major dimensions locked, cost estimate ±10%; CD = full construction detail, cost estimate ±5%). Tie to DEL-05-01/02 (pricing baseline from proposal) to ensure design stays within budget.

*Source: ASSUMPTION (Design-Build cost control best practices); decomposition OBJ-007 (competitive price package)*

---

### T-03: Flexibility vs. Control in Document Distribution
**Competing concerns:**
- **Broad distribution (everyone gets everything):** Ensures all stakeholders have access; transparency
- **Controlled distribution (need-to-know basis):** Reduces risk of outdated versions circulating; protects proprietary information; easier to manage

**Impact:** Too much openness can lead to confusion (subcontractors using superseded drawings); too much restriction can delay work (trades waiting for access).

**Guidance for plan:** Use a document management system (DMS) with role-based access controls. Issue formal sets at milestones to Owner and key stakeholders; provide controlled access to working documents for internal team. Clearly mark all distributed documents with issuance designation and date.

*Source: Industry best practice (ASSUMPTION); ISO 19650 information management principles*

---

### T-04: Proposal Detail vs. Post-Award Flexibility

> **[SL:F-003]** This trade-off addresses a gap in the original guidance: how detailed should the plan be in the proposal if the team will refine procedures post-award? *(SourcePath: Guidance.md § Trade-offs)*

**Competing concerns:**
- **High proposal detail:** Demonstrates thoroughness and credibility to evaluators; locks in commitments that Owner can rely on
- **Lower proposal detail:** Preserves flexibility for post-award refinement based on actual conditions, team composition, and Owner input

**Impact:** Over-specifying in the proposal constrains the team's ability to adapt; under-specifying risks appearing less credible or losing points in evaluation.

**Guidance for plan:**
- **Lock in proposal:** Document control schema (numbering system, revision protocols), QA/QC checkpoint structure (layers and responsible parties), Owner review milestones and general process, addenda integration checklist
- **Defer to post-award:** Specific software platform selection (DMS, BIM tools), detailed review period durations (subject to Owner negotiation), specific meeting schedules, detailed checklist templates

*Source: ASSUMPTION (Design-Build proposal strategy best practice)*

---

## Examples

### Example 1: Drawing Index and Completeness Checklist (ASSUMPTION: illustrative structure)

**Drawing Index Structure:**
```
COVER SHEET
  00-001  Cover Sheet and Drawing Index

ARCHITECTURAL
  A-000   Architectural General Notes, Legends, Symbols
  A-001   Site Plan (Architectural Context)
  A-100   Floor Plans (Fire Hall and Public Works areas)
  A-200   Roof Plan
  A-300   Building Elevations
  A-400   Building Sections
  A-500   Interior Elevations
  A-600   Details (Wall Sections, Stair Details, etc.)
  A-700   Door and Window Schedules
  A-800   Finish Schedule, Room Data Sheets

STRUCTURAL
  S-000   Structural General Notes
  S-100   Foundation Plan
  S-200   Framing Plans (Floor, Roof)
  S-300   Structural Details
  S-400   Structural Calculations (appendix or separate document)

MECHANICAL
  M-000   Mechanical General Notes
  M-100   HVAC Plans
  M-200   Plumbing Plans
  M-300   Fire Protection Plans
  M-400   Fire Apparatus Exhaust System (per Addendum 03)
  M-500   Equipment Schedules and Details

ELECTRICAL
  E-000   Electrical General Notes
  E-100   Power Distribution Plans
  E-200   Lighting Plans
  E-300   Fire Alarm Plans
  E-400   Communications/Data Plans
  E-500   Generator and Emergency Power (ICP support per decomposition)
  E-600   Panel Schedules and Details

CIVIL
  C-000   Civil General Notes
  C-100   Site Grading and Drainage Plan (12-acre developable area)
  C-200   Site Utility Plan (water, sanitary, storm, gas, electrical service)
  C-300   Paving and Surfacing Plan
  C-400   Civil Details
```

**Completeness Checklist (example items):**
- [ ] All sheets numbered per index; no gaps
- [ ] Cover sheet includes all disciplines
- [ ] General notes sheets present for each discipline
- [ ] All references between drawings verified (e.g., "See Detail 3/A-602" exists)
- [ ] All schedules complete (door/window, equipment, finishes, panels)
- [ ] Specifications cross-referenced to drawings
- [ ] All sheets dated and bear professional seal (where required)

*Source: ASSUMPTION (illustrative example for proposal credibility); actual index will vary based on project complexity*

---

### Example 2: BIM Coordination Workflow (ASSUMPTION)

**Workflow:**
1. **Model development:** Each discipline develops 3D model (Revit, AutoCAD MEP, or equivalent) in shared coordinate system
2. **Model aggregation:** Design Manager aggregates discipline models into federated model (Navisworks or equivalent)
3. **Clash detection run:** Automated clash detection identifies hard clashes (physical conflicts) and soft clashes (clearance violations)
4. **Clash report distribution:** Report sent to discipline leads with clash locations and severity ratings
5. **Clash resolution meeting:** Weekly coordination meeting to assign responsibility and resolve clashes
6. **Model updates:** Disciplines update models to resolve assigned clashes
7. **Re-run clash detection:** Verify clashes are resolved; iterate until clash count is zero or all remaining clashes are accepted (documented exceptions)
8. **Milestone coordination sign-off:** Design Manager confirms coordination is complete before advancing to next phase

**Frequency:** Weekly during active design (DD and CD); daily during final coordination push before permit submission.

*Source: ASSUMPTION (industry-standard BIM coordination workflow); specific software platforms and protocols — TBD based on team capabilities and Owner requirements*

---

### Example 3: Owner Review and Comment Incorporation Process (ASSUMPTION)

**Process:**
1. **Submittal preparation:** Design Manager assembles complete set (all disciplines) and confirms internal QA/QC is complete
2. **Submittal transmittal:** Issue to Owner with transmittal letter stating phase (e.g., "Design Development Submittal"), review period (e.g., "Please provide comments by [date]"), and format (PDF via email/portal)
3. **Owner review:** Owner and their consultants review documents for compliance with OSR, functional program, budget, and constructability
4. **Comment log:** Owner provides comments in structured format (drawing number, comment, priority level: critical/major/minor)
5. **Response matrix:** Design-Builder prepares response matrix for each comment (accepted/revised/rebuttal) with explanation
6. **Revision and resubmittal:** Incorporate accepted comments; revise drawings with revision clouds/deltas; resubmit revised set with response matrix
7. **Owner acceptance:** Owner provides written acceptance (email or letter) confirming phase approval; project proceeds to next phase

**Review period (ASSUMPTION):** 3 weeks for DD and CD; 1 week for minor resubmittals.

*Source: ASSUMPTION (typical Design-Build Owner review workflow); specific Owner review process from RFP Section 7.1.8 or contract terms — location TBD*

---

### Example 4: Document Control Implementation (ASSUMPTION)

> **[SL:B-003]** This example addresses a gap in the original guidance: no specific example of document control protocols (numbering system, revision tracking template) was provided despite P-05 (document control prevents chaos) emphasizing its importance. *(SourcePath: Guidance.md § Examples vs. Guidance.md § P-05)*

**Drawing Numbering System:**
```
Format: [Discipline]-[Sheet Type][Sheet Number]

Disciplines:
  G = General / Cover
  A = Architectural
  S = Structural
  M = Mechanical
  P = Plumbing
  E = Electrical
  C = Civil
  L = Landscape (if in scope)

Sheet Types (within discipline):
  0 = General notes, legends, symbols
  1 = Plans
  2 = Roof plans / upper level plans
  3 = Elevations
  4 = Sections
  5 = Interior elevations / details
  6 = Details
  7 = Schedules
  8 = Diagrams / schematics

Example: A-301 = Architectural, Elevations, Sheet 01
```

**Revision Tracking Protocol:**
- Revision designations: Use sequential numbers (1, 2, 3...) for pre-permit revisions; letters (A, B, C...) for post-permit revisions
- Revision clouds: Circle areas of change with revision triangle marker
- Revision history table: Located in title block or drawing border; includes: Rev #, Date, Description, Initials
- Superseded drawings: Mark "SUPERSEDED" with date; archive in DMS but remove from active set

**DMS Folder Structure:**
```
/[Project Number] - Penhold PSB/
  /01 - Design Development/
    /Architectural/
    /Structural/
    /Mechanical/
    /Electrical/
    /Civil/
    /Coordination Reports/
  /02 - Construction Documents/
    (same discipline subfolders)
  /03 - Permit Submittals/
  /04 - Issued for Construction/
  /05 - Addenda and Bulletins/
  /06 - Record Drawings/
  /Archive/
```

*Source: ASSUMPTION (industry-standard document control practice); specific Owner DMS preferences — TBD*

---

### Example 5: Design Change Management (ASSUMPTION)

> **[SL:F-005]** This example addresses integral adequacy transparency: how the team handles design changes (permit comments, Owner requests, cost constraints) should be visible to the Owner. *(SourcePath: Guidance.md § Examples)*

**Change Trigger Types:**
1. **Permit review comments:** AHJ requires design modifications for code compliance
2. **Owner-directed changes:** Owner requests scope additions, modifications, or value engineering
3. **Coordination discoveries:** Design team identifies conflicts or improvements during coordination
4. **Cost constraint responses:** Estimator identifies budget overrun; design adjustment needed

**Change Management Workflow:**
1. **Change identification:** Team member identifies potential change; logs in Change Request Register
2. **Impact assessment:** Design Manager evaluates: scope impact, cost impact, schedule impact, discipline(s) affected
3. **Owner notification:** For Owner-approval-required changes (scope/cost/schedule impact), submit Change Request Memo with: description, rationale, impact summary, recommendation
4. **Owner decision:** Owner approves, rejects, or modifies the change request
5. **Implementation:** If approved, incorporate change into design documents; update revision log; issue revised drawings
6. **Verification:** QA/QC checkpoint confirms change is correctly implemented; addenda checklist updated if Addendum 03 items affected

**Change Request Memo Template (ASSUMPTION):**
```
CHANGE REQUEST MEMO

CR Number: CR-[YYYY]-[###]
Date: [Date]
Project: Penhold PSB
Phase: [SD/DD/CD/IFC]

Change Description:
[Describe the change and affected scope]

Change Trigger:
[ ] Permit comment  [ ] Owner request  [ ] Coordination  [ ] Cost constraint

Impact Assessment:
- Scope: [Minor / Moderate / Major]
- Cost: [No impact / +$X / -$X]
- Schedule: [No impact / +X days / -X days]
- Disciplines Affected: [List]

Recommendation:
[Design Manager recommendation: approve / modify / alternative approach]

Owner Decision:
[ ] Approved  [ ] Rejected  [ ] Modified as follows: ___________
Owner Signature: ___________  Date: ___________
```

*Source: ASSUMPTION (typical Design-Build change management workflow); specific contract change order provisions — TBD*

---

## Evaluation Criteria Alignment

> **[SL:D-003]** The plan contributes to "Project Delivery Plan" evaluation criteria (10 points per decomposition Section 15). This section maps plan contents to probable Owner evaluation criteria to guide content emphasis. *(SourcePath: Guidance.md § Purpose)*

**Probable Evaluation Criteria (ASSUMPTION based on RFP evaluation structure):**

| Plan Content Area | Probable Evaluation Criteria | Emphasis Guidance |
|-------------------|------------------------------|-------------------|
| Completeness procedures | Thoroughness, clarity of process | Demonstrate structured approach with checklists and deliverable lists |
| Coordination processes | Feasibility, risk mitigation | Show continuous coordination (not one-time event); specify tools and frequency |
| QA/QC checkpoints | Quality assurance credibility | Multi-layered approach (self-check through Owner review); identify responsible parties |
| Document control | Professional practice | Numbering system, revision protocols, DMS; demonstrates project management maturity |
| Owner review process | Owner engagement, communication | Clear milestones, reasonable review periods, structured comment incorporation |
| Code compliance | Risk management, regulatory proficiency | Identify code review approach; demonstrate understanding of Alberta requirements |
| Addenda integration | Responsiveness to RFP requirements | Explicit checklist showing all Addendum 03 items addressed; traceability to disciplines |
| Schedule alignment | Feasibility, realistic planning | Consistency with DEL-08-01; reasonable phase durations |

**Scoring Maximization Guidance:**
- Prioritize clarity and specificity over generic statements
- Include sample artifacts (checklists, matrices, templates) to demonstrate capability
- Address all acceptance criteria from _CONTEXT.md explicitly
- Cross-reference related deliverables (DEL-03-01, DEL-08-01, DEL-09-01) to show integration

*Source: ASSUMPTION based on typical RFP evaluation methodology; decomposition Section 15 (evaluation criteria summary)*

---

## Conflict Table (for human ruling)

**Conflicts identified during Semantic Lensing Pass 3:**

| Conflict ID | Description | Contenders | Recommended Resolution | Human Ruling |
|-------------|-------------|------------|------------------------|--------------|
| CONFLICT-01 | Landscape discipline scope inconsistency | Datasheet/Specification flag as TBD; Procedure assumes inclusion | Decide: in scope (remove TBD) or out of scope (remove all references) | TBD |
| CONFLICT-02 | QA vs. QC terminology variation | Datasheet uses "Quality Assurance Checkpoints" for both QA and QC activities | Standardize to "QA/QC Checkpoints" with definitions across all documents | TBD |
| CONFLICT-03 | Third-party code review: mandatory vs. optional | Specification RQ-07 does not mandate; Guidance recommends as best practice | Clarify: mandatory for Fire Hall, or optional with rationale | TBD |

*See _SEMANTIC_LENSING.md Conflict Details section for full analysis of each conflict.*

---

**Document Status:** DRAFT (Semantic Lensing Pass 3 complete — enrichment items incorporated)

**Semantic Lensing Items Incorporated:** B-003 (document control example), B-005 (BIM decision criteria), D-003 (evaluation criteria alignment), F-003 (proposal detail vs. flexibility trade-off), F-005 (change management example), X-003 (code review substantiation)

**TBD Items for resolution:**
- Specific RFP Section 7.1.8 requirements for Owner review process, BIM requirements, code review mandates
- Owner preferences for review period duration and submittal format
- Software platform selections (BIM, document management system)
- **Landscape discipline scope (CONFLICT: requires decision)**
- **Third-party code review approach (CONFLICT: requires decision with rationale)**
- As-built documentation protocol details (defer to DEL-06-01 or include here)

**Assumptions flagged:**
- Design-Build contract structure and Owner approval authority
- DBIA best practices applicability
- BIM coordination approach and tools (recommend BIM-first position)
- QA/QC multi-layered structure
- Document control protocols (numbering, revision, DMS) — Example 4 provided
- Owner review periods (2-3 weeks)
- Third-party code review as best practice (with substantiation requirement)
- Permit review timeline (4-8 weeks)
- Cost-of-quality multiplier (10x for field corrections)
- Drawing index structure and completeness checklist
- BIM coordination workflow and frequency
- Owner review and comment incorporation process
- Change management workflow — Example 5 provided
- Evaluation criteria alignment — assumed criteria mapped
