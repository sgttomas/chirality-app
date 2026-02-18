# Specification: DEL-08-01 DetailedProjectSchedule

## Scope

### Included in this Deliverable
This deliverable provides a detailed project schedule for the Town of Penhold Public Services Building Design-Build proposal response, covering:

- **Design-Build project phases:** Pre-construction, design development, permitting, procurement, construction, commissioning, and closeout
- **All major work streams:** Architectural, structural, mechanical, electrical, fire protection, site works, landscaping
- **Integrated facility scope:** Fire Hall + Public Works functions in single building
- **Site development:** 12-acre developable area (excludes 8-acre flood fringe area used for dog park/storm pond)
- **Scope alignment:** Reflects Addendum 03 clarifications (pickled sand storage building removed; survey files post-award)

**Source:** Decomposition Section 8 (DEL-08-01), Section 4 (Addendum 03 impacts)

### Excluded from this Deliverable
- **Pickled sand storage building:** Removed from RFP scope per Addendum 03 (separate future RFP)
- **FF&E procurement schedule:** May be treated as optional addition per Addendum 03 (**TBD** - pricing treatment not finalized per decomposition OI-004)
- **Post-occupancy operational schedule:** This deliverable covers project delivery only, not ongoing building operations
- **Detailed resource-loading:** Proposal-level schedule; detailed resource histograms are post-award refinements

**Source:** Decomposition Section 4 (Addendum 03), Section 12 (Open Issues)

### Boundaries and Interfaces
- **Upstream dependency:** All schedule-first coordination per `_DEPENDENCIES.md` (mode: NOT_TRACKED; external coordination)
- **Interface with pricing (DEL-05-01/02):** Schedule assumptions must align with cost basis and procurement strategies
- **Interface with risk register (DEL-09-01):** Schedule buffers and contingencies must reflect identified risks
- **Interface with methodology (DEL-04-01):** Schedule sequence must align with construction methodology narrative

**Source:** `_DEPENDENCIES.md`, decomposition Section 8 (cross-deliverable alignment)

---

## Requirements

### REQ-SCH-000: Compliance Foundation
**Requirement:** Schedule shall comply with RFP Section 7.1.9 (location per _REFERENCES.md), integrate Addenda 01-03 per Decomposition Section 4, and meet hard constraints (C-01/C-04/C-07). Any conflict: addenda governs.

**Source:** Semantic Lensing F-001 (authoritative compliance foundation); Decomposition C-07

**Rationale:** Missing overarching normative compliance requirement risks evaluator judgment that schedule did not follow RFP authority. Foundational compliance must be explicit.

**Verification:** Proposal Manager confirms RFP Section 7.1.9 compliance, addenda integration, and hard constraint adherence before submission.

---

### REQ-SCH-001: Schedule Format and Content
**Requirement:** The schedule shall be presented as a Gantt chart with milestone summary, critical path narrative, and schedule assumptions documented separately. Schedule shall be developed in scheduling software per RFP Section 7.1.9 (TBD); if unspecified, use firm standard. For submission, export PDF (≤5MB schedule section). Retain native file for post-award refinement.

**Source:** Decomposition Section 8 (DEL-08-01 anticipated artifacts), `_CONTEXT.md`, Semantic Lensing B-005 (software specification)

**Rationale:** RFP Section 7.1.9 requires detailed schedule presentation (**location TBD** - specific format requirements not accessible). Software clarity prevents compliance risk.

**Verification:** Visual inspection of Gantt chart; narrative presence check; milestone list completeness check; software compliance check per RFP.

---

### REQ-SCH-002: Duration Believability
**Requirement:** Activity durations shall be credible and defensible, based on typical industry practice for comparable municipal Design-Build projects. Durations shall be within ±20% of historical norms for comparable activities.

**Source:** Decomposition Section 8 (DEL-08-01 acceptance criteria: "Believable durations"), Semantic Lensing A-001 (acceptance tolerance), PMI PMBOK

**Rationale:** Schedule credibility impacts evaluation scoring per decomposition OBJ-009. Evaluators assess "believability" against industry norms; explicit tolerance provides verification standard.

**Verification:** Peer review by Primary Reviewer (Senior Scheduler or PM); comparison to historical project data (**ASSUMPTION**: firm has comparable project records). Duration Justification memo required as evidence documenting basis for each major activity duration. If reviewer opinions conflict, escalate to Proposal Manager.

**Source (Verification Enhancement):** Semantic Lensing A-003 (verification gap - reviewer designation and escalation)

---

### REQ-SCH-003: Permitting Inclusion
**Requirement:** The schedule shall include permitting activities, submission preparation time, authority review duration, and approval receipt milestones. Schedule shall include Permitting Assumptions section documenting: preparation duration (2-3 weeks), submission timing, authority review duration (8 weeks + 2-week buffer), follow-up/revision cycle, approval receipt milestone.

**Source:** Decomposition Section 8 (DEL-08-01 acceptance criteria: "includes permitting"), Semantic Lensing F-002 (substantiated execution proficiency)

**Rationale:** Permitting is on critical path for municipal projects; omission creates unrealistic schedule. Substantiated proficiency requires explicit permitting assumptions documentation.

**Verification:** Schedule includes permitting activities AND separate Permitting Assumptions section documenting: preparation duration, submission timing, authority review duration, follow-up/revision cycle, approval receipt milestone. Scheduler cites Alberta Building Code and Town of Penhold municipal norms where applicable.

**Source (Verification Enhancement):** Semantic Lensing F-002

---

### REQ-SCH-004: Procurement Lead Time Inclusion
**Requirement:** The schedule shall account for procurement lead times for long-lead equipment and materials, including vendor selection, shop drawing review, fabrication, and delivery. Procurement lead times shall include source documentation (vendor quotes, historical firm data, or industry benchmark source) for each item.

**Source:** Decomposition Section 8 (DEL-08-01 acceptance criteria: "includes procurement lead times"), Semantic Lensing B-002 (satisfactory reporting)

**Rationale:** Long-lead items (MEP equipment, overhead doors, fire apparatus systems - **ASSUMPTION**) drive construction sequencing. Source-documented lead times strengthen evaluator confidence.

**Verification:** Identification of long-lead items; lead time assumptions documented with source (vendor quote, firm historical data, or cited industry benchmark); sequencing logic review.

**Source (Verification Enhancement):** Semantic Lensing B-002

---

### REQ-SCH-005: Commissioning Inclusion
**Requirement:** The schedule shall include commissioning activities for all building systems (HVAC, electrical, fire alarm, fire suppression, building controls, generator, overhead doors).

**Source:** Decomposition Section 8 (DEL-08-01 acceptance criteria: "includes commissioning"); DEL-06-01 interface (commissioning narrative deliverable)

**Rationale:** Commissioning is required for functional building handover and impacts substantial completion date.

**Verification:** Commissioning tasks present in schedule; durations align with DEL-06-01 commissioning narrative (**cross-check in Pass 2**).

---

### REQ-SCH-006: Closeout Inclusion
**Requirement:** The schedule shall include closeout activities: deficiency correction, final inspections, as-built documentation, owner training, occupancy permit, and warranty period initiation.

**Source:** Decomposition Section 8 (DEL-08-01 acceptance criteria: "includes closeout"); DEL-06-01 interface

**Rationale:** Closeout activities must occur before final acceptance; 12-month warranty period baseline per decomposition.

**Verification:** Closeout tasks present; training and documentation handover milestones identified.

---

### REQ-SCH-007: Critical Path Identification
**Requirement:** The schedule shall identify and document the critical path, including a narrative explanation of key driving activities and float management approach.

**Source:** Decomposition Section 8 (DEL-08-01 anticipated artifacts: "Critical path narrative")

**Rationale:** Critical path transparency demonstrates schedule control competency; supports evaluation per OBJ-009.

**Verification:** Critical path visually highlighted in Gantt; narrative document present; logic explanation provided.

---

### REQ-SCH-008: Schedule Assumptions Documentation
**Requirement:** All schedule assumptions shall be documented, including weather constraints, procurement assumptions, permitting durations, site access assumptions, and any scope clarifications from addenda.

**Source:** Decomposition Section 8 (DEL-08-01 anticipated artifacts: "Schedule assumptions and basis")

**Rationale:** Assumption transparency supports schedule credibility and provides basis for post-award refinement.

**Verification:** Assumptions document present; covers weather, procurement, permitting, site, and addenda impacts.

---

### REQ-SCH-009: Addendum 03 Impacts Reflected
**Requirement:** The schedule shall reflect the following Addendum 03 impacts:
- Pickled sand storage building removed (scope reduction)
- Survey files availability post-award (constraint on early site work)
- Site servicing allowance approach (affects sitework phasing assumptions)

Schedule narrative and assumptions shall explicitly acknowledge Addendum 03 and document each impact: (a) Pickled sand building excluded; (b) Survey post-award constraint (3-week site survey gates site design); (c) Site servicing approach.

**Source:** Decomposition Section 4 (Addendum 03 Integration Summary), SOW-023, SOW-024, Semantic Lensing C-001 (binding foundational obligation)

**Rationale:** Addenda compliance is mandatory; failure to integrate addenda risks disqualification per decomposition C-07. Explicit citation in narrative is required per C-001.

**Verification:** Schedule narrative explicitly references Addendum 03 with documented impacts; removed scope not present; survey constraint documented with duration; Proposal Manager confirms addenda acknowledgment.

---

### REQ-SCH-010: Coordination with Pricing (Cross-Deliverable)
**Requirement:** Schedule assumptions (durations, sequencing, procurement) shall be consistent with pricing basis in DEL-05-01/02 (Appendix H).

**Source:** Decomposition Section 8 (deliverable interfaces); OBJ-007 (competitive price package)

**Rationale:** Schedule-cost misalignment undermines proposal credibility.

**Verification:** Cross-check between schedule narrative assumptions and pricing narrative (DEL-05-03); escalation/timing assumptions aligned (**cross-check in Pass 2**).

---

### REQ-SCH-011: Coordination with Risk Register (Cross-Deliverable)
**Requirement:** Schedule shall reflect risk mitigation strategies from DEL-09-01 (Risk Register), including schedule buffers or contingency activities for high-probability risks. If DEL-09-01 unavailable at development time, scheduler uses standard ASSUMPTION-based buffers (weather, permitting, procurement per Procedure). Schedule Assumptions shall note any TBD items pending Risk Register review.

**Source:** Decomposition Section 8 (deliverable interfaces); OBJ-008 (transparent risk management), Semantic Lensing C-005 (verification gap for DEL-09-01 dependency)

**Rationale:** Schedule must account for identified risks (e.g., weather delays, long-lead procurement, permitting unknowns). Parallel workstream acknowledgment prevents evaluator penalty for risk register unavailability.

**Verification:** Risk register review (if available); schedule buffers or float allocation aligned to risk mitigation plans. If DEL-09-01 not available, verify ASSUMPTION-based buffers per Procedure and note in Assumptions.

---

### REQ-SCH-012: Submission Deadline Compliance
**Requirement:** This deliverable (as part of the full proposal PDF) must be submitted by August 30, 2024 @ 2:00 PM MST via email, with the proposal PDF not exceeding 15 MB. Revision number must be clearly indicated if proposal is resubmitted before deadline.

**Source:** Decomposition Section 3 (Hard Constraints C-01, C-04), Semantic Lensing A-002 (revision numbering per Decomposition C-04)

**Rationale:** Late or non-compliant submission results in disqualification. Revision numbering prevents version confusion.

**Verification:** File size check; submission timestamp; revision numbering verified (if resubmitted).

---

## Evaluation Framework

### Evaluation Standard
**Source:** Semantic Lensing C-004 (consistent evaluative integrity)

Evaluators assess schedule using:
1. **Duration believability:** Align with 18-24 month benchmark for comparable municipal Design-Build projects
2. **Critical path transparency:** Critical path clearly identified with logic explanation and peer review
3. **Risk awareness:** Buffers reflect identified risks (weather, permitting, procurement, site conditions)

Schedule meeting all three criteria = "believable" per OBJ-009.

### Binding Compliance Assurance
**Source:** Semantic Lensing E-001 (binding compliance assurance)

Schedule evaluation has two phases:
1. **COMPLIANCE GATE:** Confirm responsive to RFP Section 7.1.9, integrates Addenda 01-03, includes all required artifacts (REQ-SCH-001). Failure = zero (0) points.
2. **EVALUATION:** If gate passes, score 0-10 points based on PRIMARY requirements (REQ-SCH-001/007/009/012) and SECONDARY (REQ-SCH-002 through REQ-SCH-006/010/011).

### Enforced Standard Practice
**Source:** Semantic Lensing D-001 (enforced standard practice)

Enforced Standard Practice per RFP Section 7.1.9 (location TBD):
1. **Critical Path Method (CPM) logic required:** All activities with predecessor/successor relationships; critical path highlighted
2. **Float transparency required:** Float allocation approach documented in Assumptions
3. **TBD:** Additional RFP-mandated standards pending RFP Section 7.1.9 review

Non-compliance may result in zero points in Schedule subcategory.

### Requirement Priority
**Source:** Semantic Lensing D-006 (justified benefit hierarchy)

| Priority | Requirements | Focus |
|----------|--------------|-------|
| **PRIMARY** (threshold-level) | REQ-SCH-000, REQ-SCH-001, REQ-SCH-007, REQ-SCH-009, REQ-SCH-012 | Format, critical path, addenda, submission |
| **SECONDARY** (differential) | REQ-SCH-002, REQ-SCH-003, REQ-SCH-004, REQ-SCH-005, REQ-SCH-006, REQ-SCH-010 | Durations, permitting, procurement, commissioning, closeout, pricing coordination |
| **TERTIARY** (enhancement) | REQ-SCH-008, REQ-SCH-011 | Assumptions documentation, risk register coordination |

Allocate effort proportional to priority.

### Milestone Definition
**Source:** Semantic Lensing C-006 (normalization of milestone definition)

A milestone represents a significant project event:
- **(a) Phase completions:** Design Development Complete, Permit Approval, Mobilization, Substantial Completion, Final Completion
- **(b) Critical path events:** Site Survey Complete, Permit Submission, Long-Lead Procurement Orders, Building Enclosure Complete, Commissioning Start
- **(c) External dependencies:** Contract Award, Warranty Period Start

Proposal shall include **12-15 milestones** with target date, predecessors, and float status.

---

## Standards

### Applicable Codes and Standards (ASSUMPTION)
The following standards are inferred as applicable to schedule development for this deliverable type; specific RFP requirements **location TBD**:

| Standard | Relevance | Source |
|----------|-----------|--------|
| **PMI PMBOK (6th or 7th Edition)** | Schedule management best practices; critical path method; float management | ASSUMPTION (industry standard for project scheduling) |
| **CSI MasterFormat 2020** | Construction phase breakdown and work packaging | ASSUMPTION (standard reference for construction sequencing) |
| **Alberta Building Code** | Permitting process and approval timelines | ASSUMPTION (provincial jurisdiction for building permits) |
| **Town of Penhold bylaws** | Municipal approval processes and timelines | ASSUMPTION (local jurisdiction context; **location TBD**) |

**Note:** RFP may specify scheduling software (e.g., MS Project, Primavera P6) or format requirements; not accessible in current references (**location TBD**).

---

## Verification

### Verification Methods

**Source Enhancement:** Semantic Lensing X-003 (mandatory performance proof - proof method column added)

| Requirement ID | Verification Method | Acceptance Criteria | Proof Method | Responsible |
|----------------|---------------------|---------------------|--------------|-------------|
| REQ-SCH-000 | Compliance review | RFP Section 7.1.9 addressed; Addenda integrated; hard constraints met | Proposal Manager sign-off on compliance checklist | Proposal Manager |
| REQ-SCH-001 | Document inspection | Gantt chart present; milestone summary present; critical path narrative present; assumptions document present | Proposal PDF includes section titled 'Schedule' with sub-sections per artifact list; evaluator confirms via PDF Table of Contents and section inspection | Scheduler / PM |
| REQ-SCH-002 | Peer review + historical comparison | Durations within ±20% of comparable project norms; no obvious duration outliers | Duration Justification memo with peer review sign-off | Senior Scheduler / Estimator |
| REQ-SCH-003 | Activity inspection | Permit activities present; durations documented; approval milestones identified | Permitting Assumptions section present in schedule narrative | Scheduler |
| REQ-SCH-004 | Procurement review | Long-lead items identified; lead times documented with source; procurement logic present | Lead time source documentation (vendor quotes, firm data, or cited benchmark) | Scheduler / Procurement Lead |
| REQ-SCH-005 | Commissioning alignment check | Commissioning activities present for all systems; durations align with DEL-06-01 | Cross-check memo between schedule and DEL-06-01 | Scheduler / Commissioning Lead |
| REQ-SCH-006 | Closeout alignment check | Closeout tasks present; training and documentation handover milestones identified | Closeout activities visible in Gantt; milestone table includes closeout items | Scheduler / PM |
| REQ-SCH-007 | Critical path analysis | Critical path identified and highlighted; narrative explains driving activities and float | Critical path highlighted in Gantt (color/bold); narrative document present | Scheduler |
| REQ-SCH-008 | Assumptions document review | Weather, procurement, permitting, site access, and addenda assumptions documented | Assumptions document present with categorized sections | Scheduler / PM |
| REQ-SCH-009 | Addendum compliance check | Pickled sand building absent; survey constraint noted; addenda explicitly referenced in narrative | Narrative includes explicit Addendum 03 acknowledgment with documented impacts | Proposal Manager |
| REQ-SCH-010 | Cross-deliverable consistency check | Schedule assumptions align with pricing basis (DEL-05-03); no duration-cost conflicts | Coordination checklist signed by Scheduler and Estimator | Scheduler + Estimator |
| REQ-SCH-011 | Risk alignment check | Schedule buffers or contingencies reflect risk register (DEL-09-01) high-priority items; or ASSUMPTION-based buffers if DEL-09-01 unavailable | Risk buffer documentation in Assumptions; coordination memo with Risk Manager | Scheduler + Risk Manager |
| REQ-SCH-012 | Submission compliance check | PDF ≤15 MB; submitted by deadline; revision numbering correct (if applicable) | File size verification; timestamp confirmation; revision number check | Proposal Manager |

---

## Documentation

### Required Documentation Outputs
Per `_CONTEXT.md` anticipated artifacts and decomposition acceptance criteria, the following documents shall be produced:

1. **Detailed Gantt Chart Schedule**
   - Format: TBD (MS Project, Primavera P6, or PDF export - **software not specified; location TBD**)
   - Detail level: Level 2 or 3 (50-150 activities typical for proposal stage - **ASSUMPTION**)
   - Content: All project phases from contract award through final completion and warranty initiation
   - Visual: Critical path highlighted; milestones marked; dependencies shown

2. **Milestone Summary**
   - Format: Table or timeline graphic
   - Content: Key project milestones (contract award, permit approval, substantial completion, final completion, etc.)
   - Source: Extracted from detailed Gantt chart

3. **Critical Path Narrative**
   - Format: Written narrative (1-2 pages recommended - **ASSUMPTION**)
   - Content: Explanation of critical path activities; float management approach; key driving constraints

4. **Schedule Assumptions and Basis**
   - Format: Written narrative or structured list
   - Content: Weather constraints, procurement lead times, permitting durations, site access assumptions, addenda impacts, coordination assumptions

### Supporting Documentation (Internal)
- **Schedule basis memo:** Internal justification for durations and sequencing (not necessarily submitted; used for QC)
- **Historical project data:** Reference schedules from comparable municipal Design-Build projects (**ASSUMPTION**: firm has records)

---

## Document Control

- **Version:** 1.1 (Pass 3 - Semantic Lensing Enrichment Complete)
- **Generated:** 2026-02-04
- **Agent:** 4_DOCUMENTS (Type 2)
- **Pass:** 3 of 3 (Semantic Lensing Complete)
- **Semantic Lensing Items Incorporated:** A-002, A-003, B-002, B-005, C-001, C-004, C-005, C-006, D-001, D-006, E-001, F-001, F-002, X-003
