# Datasheet: DEL-08-01 DetailedProjectSchedule

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-08-01 |
| **Name** | DetailedProjectSchedule |
| **Type** | Schedule Document |
| **Package** | PKG-08 Schedule & Milestones |
| **Discipline** | Project Controls / Scheduling |
| **Responsible** | Scheduler / PM |
| **Status** | OPEN |

**Source:** `_CONTEXT.md`

---

## Attributes

### Schedule Scope
- **Project:** Town of Penhold Public Services Building (Design-Build)
- **Project Type:** Integrated Fire Hall + Public Works facility
- **Delivery Method:** Design-Build (single entity responsibility)
- **Submission Deadline:** August 30, 2024 @ 2:00 PM MST
- **Developable Site Area:** 12 acres (20 acres total; 8 acres dog park/storm pond in flood fringe)

**Source:** Decomposition document Section 1 (Intake Summary), Section 4 (Addendum 03 impacts)

### Schedule Duration Constraints
- **Total project duration:** TBD (not specified in accessible references; **location TBD** - RFP Section 7.1.9)
- **Substantial completion target:** TBD (not specified in accessible references; **location TBD** - RFP Section 7.1.9)
- **Final completion target:** TBD (not specified in accessible references; **location TBD** - RFP Section 7.1.9)

**Note:** RFP Section 7.1.9 requirements not accessible; constraints marked TBD. If RFP does not mandate specific duration, credibility will be assessed against industry benchmarks (18-24 months for comparable municipal Design-Build projects).

**Source:** Semantic Lensing B-001, F-005 (RFP duration targets required for credible schedule anchoring)

### Key Milestones (ASSUMPTION - typical Design-Build phasing)
- Proposal submission: August 30, 2024
- Contract award: TBD
- Design development: TBD
- Permitting submission: TBD
- Permit approval: TBD
- Construction mobilization: TBD
- Foundation completion: TBD
- Building enclosure: TBD
- MEP rough-in: TBD
- Interior finishes: TBD
- Commissioning start: TBD
- Substantial completion: TBD
- Owner training: TBD
- Final completion: TBD
- Warranty period start: TBD (12-month warranty baseline per decomposition)

**ASSUMPTION:** Milestone list derived from typical Design-Build project phasing; actual RFP requirements **location TBD**.

---

## Conditions

### Normal Operating Conditions
- **Schedule baseline:** Proposal-stage schedule (Level 2/3 detail; **ASSUMPTION**)
- **Update frequency (post-award):** TBD (not specified; typical is monthly)
- **Float management:** TBD (owner vs contractor float allocation not specified)

### Design Conditions
- **Critical path identification:** Required per decomposition (Section 8 DEL-08-01 acceptance criteria)
- **Procurement lead times:** Must be included (per decomposition acceptance criteria)
- **Permitting durations:** Must be included (per decomposition acceptance criteria)
- **Commissioning duration:** Must be included (per decomposition acceptance criteria)
- **Closeout duration:** Must be included (per decomposition acceptance criteria)

**Source:** Decomposition Section 8 (DEL-08-01 acceptance criteria)

### Limiting Conditions
- **Weather constraints (ASSUMPTION):** Alberta climate - limited winter concrete work; reduced productivity in extreme cold
- **Site access constraints:** TBD (not specified in accessible documents; **location TBD**)
- **Procurement risks:** Long-lead items TBD (MEP equipment, overhead doors, specialized fire apparatus systems - **ASSUMPTION**)
- **Survey availability:** Survey files provided after contract award (Addendum 03 impact; affects schedule assumptions)
- **Scope exclusion:** Pickled sand storage building removed from scope (Addendum 03; reduces overall schedule duration)

**Source:** Decomposition Section 4 (Addendum 03 impacts), SOW-024

---

## Construction

### Schedule Structure (ASSUMPTION - typical proposal-level detail)
- **WBS structure:** TBD (Work Breakdown Structure detail level not specified; **ASSUMPTION**: align to CSI divisions and project phases)
- **Activity detail level:** TBD (Level 2 or 3 detail typical for proposal; **ASSUMPTION**: 50-150 activities)
- **Sequencing logic:** Finish-to-Start relationships with identified critical path
- **Constraints:** TBD (start-no-earlier-than, milestone dates not specified in accessible documents)

### Schedule Format
- **Primary format:** Gantt chart (required per decomposition)
- **Supporting formats:**
  - Milestone summary (required per decomposition)
  - Critical path narrative (required per decomposition)
  - Schedule assumptions and basis (required per decomposition)
- **Schedule software:** TBD per RFP Section 7.1.9. If RFP unspecified, use firm standard (MS Project recommended). Both native file (for post-award refinement) and PDF export (for submission, ≤5MB) required.

**Source:** `_CONTEXT.md` anticipated artifacts, decomposition Section 8, Semantic Lensing B-005 (software specification clarification)

### Schedule Phases (ASSUMPTION - typical Design-Build sequence)
1. **Pre-Construction Phase**
   - Contract execution
   - Site survey (post-award)
   - Design development
   - Permit application preparation
   - Authority approvals

2. **Procurement Phase**
   - Long-lead equipment identification
   - Vendor selection
   - Shop drawing review cycles

3. **Construction Phase**
   - Site preparation and earthworks
   - Foundation and below-grade
   - Structural frame
   - Building enclosure
   - MEP rough-in
   - Interior finishes
   - Site works and paving

4. **Closeout Phase**
   - Commissioning
   - Owner training
   - Deficiency correction
   - Final inspections
   - Occupancy permit
   - Warranty period initiation

**ASSUMPTION:** Phasing structure derived from typical Design-Build workflow; RFP-specific requirements **location TBD**.

---

## References

### Primary Sources
- **Decomposition Document:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
  - Section 1 (Intake Summary)
  - Section 4 (Addendum 03 impacts)
  - Section 8 (Deliverable DEL-08-01 definition and acceptance criteria)
  - Section 9 (SOW-023: Detailed project schedule scope item)

- **Context File:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/_CONTEXT.md`

### Referenced But Not Accessible
- **RFP Section 7.1.9:** Schedule requirements (**location TBD** - PDF not accessible; specific milestone dates, duration requirements, and schedule format specifications unknown)
- **Addendum 01:** Timeline context regarding bidders meeting (**location TBD** - PDF not accessible)
- **Addendum 03:** Survey files and removed scope impacts on schedule (**location TBD** - PDF not accessible; impacts noted in decomposition only)

### Applicable Standards (ASSUMPTION)
- **PMI PMBOK 6th/7th Edition:** Schedule management standard practice (duration tolerance: ±10-20% vs comparable project norms)
- **CSI MasterFormat 2020:** Construction phase breakdown reference
- **Alberta Building Code:** Permitting process and timeline context

**Note:** Standards inferred from discipline; specific RFP requirements for schedule format/software not accessible.

### Schedule Credibility Definition
**Canonical Definition:** A schedule is credible if:
1. Durations are defensible against historical data (±20% of comparable project norms)
2. Critical path is transparent and peer-reviewed
3. Assumptions are explicit and documented
4. Risk buffers are proportional to identified risks
5. Internal consistency is maintained (schedule aligns with pricing, methodology, commissioning, risk register)

Schedule meeting all five criteria is considered "credible" for evaluation purposes.

**Source:** Semantic Lensing E-003, A-004 (normalization of credibility terminology across documents)

---

## Document Control

- **Version:** 1.1 (Pass 3 - Semantic Lensing Enrichment Complete)
- **Generated:** 2026-02-04
- **Agent:** 4_DOCUMENTS (Type 2)
- **Pass:** 3 of 3 (Semantic Lensing Complete)
- **Semantic Lensing Items Incorporated:** B-001, B-005, F-005, E-003, A-004
