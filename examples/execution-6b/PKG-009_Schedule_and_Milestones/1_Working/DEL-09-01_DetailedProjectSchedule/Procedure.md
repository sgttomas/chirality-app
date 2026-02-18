# Procedure: Detailed Project Schedule (DEL-09-01)

## Purpose

This procedure defines the steps to **produce** the Detailed Project Schedule deliverable for inclusion in the Penhold Public Services Building Design-Build proposal. The procedure covers: scope definition, work breakdown structure development, duration estimation, Gantt chart construction, critical path analysis, assumption documentation, quality review, and proposal packaging.

The produced deliverable must satisfy RFP Section 7.1.9 (Gantt chart format, key work packages, milestones, critical path, schedule assumptions) and support OBJ-009 ("Provide a believable, optimized schedule").

---

## Prerequisites

### Required Inputs

| Input | Source | Status |
|-------|--------|--------|
| RFP Section 7.1.9 -- Detailed Project Schedule requirements | RFP, p. 18-19 | Available |
| RFP Section 7.1.8 -- Five design submission milestones | RFP, p. 18 | Available |
| RFP Section 7.2 -- Schedule Control requirements (post-award baseline, monthly updates) | RFP, p. 19 | Available |
| RFP Section 2.6 -- RFP Schedule (contract award target: Sept 10, 2024) | RFP, p. 9 | Available |
| Decomposition v2.3 -- DEL-09-01 definition, SOW-0025, PKG-009 description | Decomposition v2.3, §9 | Available |
| Addendum 03 -- Site clarifications (12-acre developable area; specialty requirements) | Addendum 03 | Available |
| Site reference reports (geotech 2021, wetland, flood zone, grading) | Appendices D-F | Available |
| DEL-06-02 (Design Docs Plan) -- Design submission milestone dates | DEL-06-02 | Available when produced |
| DEL-07-01 (Construction Methodology) -- Construction phase approach | DEL-07-01 | Available when produced |
| DEL-08-01 (Commissioning/Closeout) -- Commissioning phase milestones | DEL-08-01 | Available when produced |
| DEL-10-02 (Site Conditions & Due Diligence Summary) -- Site constraint assumptions for duration estimation | DEL-10-02 | Available when produced; informs Step 3 duration estimation for site-related activities. Cross-referenced in Specification Documentation section. (Source: _SEMANTIC_LENSING.md B-003) |

### Required Resources

| Resource | Purpose |
|----------|---------|
| Scheduling software (MS Project, Smartsheet, Primavera P6, or equivalent) | Gantt chart construction and critical path analysis |
| Scheduler / PM with Design-Build project scheduling experience | Duration estimation, critical path, assumptions |
| Design Manager (discipline lead input) | Design phase duration validation |
| Construction Manager | Construction phase duration validation; site constraint input |
| Site reference reports | Site constraint assumption documentation |

---

## Steps

### Step 1: Establish Schedule Scope and Anchors

**Action:**
1. Confirm the schedule time span: from contract award through 12-month warranty review closeout (Phases 0-9 per Guidance C-001).
2. Set Day 0 anchor: Contract award target = September 10, 2024 (RFP §2.6, p. 9). Use this as the starting point for all relative durations.
3. Confirm Substantial Completion and Total Completion are "Design-Builder to Propose" (RFP §2.6); the schedule must propose these dates.
4. Note the post-award obligation: detailed baseline schedule due to Project Manager within 20 calendar days of contract award (RFP 7.2, p. 19). The proposal schedule is the basis for this baseline.
5. Confirm scope inclusions and exclusions:
   - Include: Main Building (PSB), Cold Storage (60' x 100'), all five design submission milestones, commissioning, closeout, 12-month warranty review.
   - Exclude: Pickled Sand Storage building (removed per Addendum 03 §1.2).

**Output:** Schedule scope summary (internal working document).

**Source:** RFP 7.1.9, p. 18-19; RFP 2.6, p. 9; Addendum 03 §1.2; Decomposition DEL-09-01.

---

### Step 2: Develop Work Breakdown Structure (WBS)

**Action:**
1. Organize project work into the following phases and sub-activities. Adjust activity granularity to target approximately 30-50 activities for a proposal-level Gantt chart.

| Phase | Activities (minimum) |
|-------|---------------------|
| **Phase 0: Kickoff and Mobilization** | Contract execution; team mobilization; site survey receipt (survey files provided post-award per Addendum 03 §1.16); existing geotech/wetland/grading report review; project management setup |
| **Phase 1: Design Development** | BDD development; BDD submission; Owner review BDD; 60% DD development; 60% DD submission; Owner review 60% DD; Foundation IFC preparation (if needed); Foundation IFC submission; Owner review Foundation IFC; 100% BDD development; 100% BDD submission; Owner review 100% BDD; 100% IFC package development; 100% IFC submission |
| **Phase 2: Permitting** | Permit application preparation; permit submission to AHJ; AHJ review; permit revisions (if required); permit issuance |
| **Phase 3: Pre-Construction** | Long-lead equipment ordering (overhead doors, generator, specialty items); contractor mobilization planning; bond and insurance documentation |
| **Phase 4: Site Work and Foundation** | Site mobilization; site grading and drainage; underground utilities (water, sewer, storm); foundation excavation; foundation construction; bay sumps installation; floor slab preparation |
| **Phase 5: Building Construction -- Main Building** | Structural frame erection; building envelope (roof, exterior cladding, glazing, doors); MEP rough-in (mechanical, electrical, plumbing); interior partitions and framing; MEP final connections; interior finishes (flooring, painting, fixtures) |
| **Phase 6: Building Construction -- Cold Storage** | Site prep; foundation; building shell; interior finishes |
| **Phase 7: Systems Commissioning** | HVAC commissioning; fire protection system commissioning; electrical systems commissioning; backup generator commissioning; fire apparatus bay direct exhaust system checkout; building controls and automation; systems performance verification |
| **Phase 8: Closeout and Handover** | Deficiency identification and resolution; staff training (all systems); O&M manual preparation and delivery; as-built drawing finalization; occupancy permit application and issuance; Substantial Performance certification; Total Completion certification |
| **Phase 9: Warranty Period** | 12-month warranty monitoring; deficiency calls and resolution; 12-month warranty review meeting; warranty closeout |

2. Check WBS coverage against Decomposition SOW-0025 and RFP 7.1.9 requirements.

**Note:** Phase naming and numbering in this WBS table is normalized to match Guidance C-001 exactly. Any changes to phase labels must be synchronized across both documents. (Source: _SEMANTIC_LENSING.md C-002)

**Output:** WBS outline (internal working document; not submitted in proposal, but informs the Gantt chart).

**Source:** RFP 7.1.9, 7.1.8, 7.2, 7.3.6, 7.6; Addendum 03 (sump, door, exhaust, generator, solar, lockers requirements); Decomposition SOW-0025.

---

### Step 3: Estimate Activity Durations

**Action:**
1. Estimate durations for each WBS activity using: comparable project benchmarks, team experience, site-specific constraint analysis, and the schedule assumptions developed in Step 5.

**Reference duration ranges (ASSUMPTION: based on comparable municipal Design-Build projects in Alberta; must be validated by Scheduler):**

| Activity Category | ASSUMPTION Duration Range |
|------------------|--------------------------|
| BDD development and Owner review | 3-5 weeks |
| 60% DD development and Owner review | 5-8 weeks |
| Foundation IFC (if needed) | 2-3 weeks |
| 100% BDD development and Owner review | 3-5 weeks |
| 100% IFC package | 2-4 weeks |
| AHJ building permit review | 6-10 weeks |
| Long-lead equipment order to delivery (overhead doors, generator) | 8-14 weeks |
| Site Work and Foundation (spring-fall favorable season) | 8-12 weeks |
| Main Building construction (superstructure + envelope) | 12-20 weeks |
| MEP rough-in and finishes (main building) | 10-16 weeks |
| Cold Storage construction | 6-10 weeks |
| Systems commissioning | 4-6 weeks |
| Closeout and handover | 3-5 weeks |
| 12-month warranty period | 52 weeks |

2. For each activity, note whether duration assumes: favorable season, no major change orders, no design revisions post-permit, standard permit review, etc. These become schedule assumptions (Step 5).

3. Apply site-specific adjustments:
   - **Geotechnical (2021 report; Appendix D):** If engineered fill or dewatering required, add 2-4 weeks to Phase 4. ASSUMPTION: existing geotech report (no additional investigation per DEC-013) indicates manageable soil conditions; specific adjustment TBD pending report review.
   - **Wetland/flood zone (Appendix D/flood zone map):** ASSUMPTION: seasonal wetland work restrictions do not fall within critical path window; TBD.
   - **Existing grading (Appendix E):** ASSUMPTION: Owner-completed grading reduces Phase 4 earthworks duration; adjustment TBD.

**Output:** Duration estimates for all WBS activities (working document; feeds directly into Gantt).

**Source:** RFP 7.1.9; Decomposition DEL-09-01; Reference reports (Appendices D-E); industry benchmarks (ASSUMPTION).

---

### Step 4: Build the Gantt Chart

**Action:**
1. Enter all WBS activities, durations, and dependencies into scheduling software (MS Project, Smartsheet, Primavera, or equivalent).
2. Define logical dependencies:
   - BDD -> Owner Review -> 60% DD start (Finish-to-Start with lag for Owner review)
   - 60% DD submission -> Permit submission (Start-to-Start; permitting begins at 60% DD)
   - Permit issuance -> Site work start (Finish-to-Start; permit must be in hand)
   - Foundation IFC -> Foundation construction start (Finish-to-Start; phased DB start)
   - 100% IFC -> Main building construction completion (design must be complete before MEP final connections)
   - Main building substantially complete -> Commissioning start (Finish-to-Start)
   - Commissioning complete -> Closeout/handover start (Finish-to-Start)
   - Occupancy permit issuance -> Warranty period start (Finish-to-Start)
3. Run critical path analysis; identify the critical path (zero-float activities).
4. Format the Gantt chart for legibility and proposal submission:
   - Horizontal bar chart with time scale (weeks from contract award, or calendar dates)
   - Milestone markers (diamond symbols) for: BDD, 60% DD, Foundation IFC, 100% BDD, 100% IFC, Permit Issued, Construction Start, Cold Storage Complete, Substantial Performance, Occupancy Permit, Warranty Review
   - Critical path highlighted in a distinct color (e.g., red)
   - Phase summary bars grouping related activities
   - Color-coding by phase (optional but recommended for evaluator readability)
   - Legend for milestone symbols, critical path color, and phase colors
   - Chart must be readable at proposal submission zoom level; export to PDF at high resolution

**Output:**
- Gantt chart PDF (primary proposal artifact): exported at 11x17 minimum page size for legibility; PDF resolution sufficient for clear reading of all activity labels, durations, and milestone dates.
- Editable schedule file retained internally: native format of the scheduling software used (e.g., .mpp for MS Project, .xls/.smartsheet for Smartsheet, .xer for Primavera P6). This editable file is required for the post-award 20-day baseline resubmission per RFP 7.2 and must be retained as a working record.

(Source: RFP 7.1.9, p. 18-19; RFP 7.2, p. 19; _SEMANTIC_LENSING.md A-003)

**Source:** RFP 7.1.9, p. 18-19 (Gantt format; milestones; critical path identification).

---

### Step 5: Document Schedule Assumptions

**Action:**
Create the Schedule Assumptions List. The list must cover at minimum the following categories:

**1. Contract and Procurement Assumptions**
- Day 0: Contract award target September 10, 2024 per RFP §2.6.
- Survey files provided by civil engineering firm after contract award per Addendum 03 §1.16; schedule does not depend on survey files before design start.
- No additional geotechnical investigation required; 2021 report is the basis (Decomposition DEC-013).
- Agreement to Bond and CCIP insurance (per DEL-01-03) in place at contract execution.

**2. Design Phase Assumptions**
- Design phase durations per Step 3 reference ranges.
- Owner design review cycles: 2-3 weeks per submission.
- Design revisions after Owner review: 1 week per review cycle.
- No major program changes after BDD; scope is fixed per Addendum 03 clarifications.
- Design team available and responsive per proposal commitment (DEL-01-08 key personnel).

**3. Permitting Assumptions**
- Building permit submitted at 60% DD phase (concurrent permitting strategy).
- ASSUMPTION: AHJ (Penhold or Red Deer County, as applicable) permit review time: **8 weeks** (default working value; TBD by Scheduler based on local AHJ knowledge; 6-10 weeks is a reasonable range per comparable Alberta municipal projects). Scheduler to override with jurisdiction-specific data if available. (Source: _SEMANTIC_LENSING.md A-002)
- Phased permit (Foundation IFC) available if AHJ supports phased permitting.
- No extraordinary permit modifications required after first submission.

**4. Site and Construction Assumptions**
- Outdoor site work (grading, foundation, underground utilities) scheduled during favorable season (approximate April-October in Alberta).
- Weather contingency: **2 weeks** (default working value for outdoor phases in Alberta; TBD -- Scheduler to adjust based on actual construction window alignment with favorable season April-October). (Source: _SEMANTIC_LENSING.md A-002)
- No Town-occupied operations on the construction site during construction.
- Main Building and Cold Storage construction can proceed in parallel; no site access conflicts.
- Long-lead items (overhead doors minimum 16 ft height per Addendum 03 §1.4; backup generator per Addendum 03 §1.15) ordered during 60% DD phase.
- ASSUMPTION: door lead time **10 weeks** (default working value; range 8-12 weeks per Guidance C-004); generator lead time **8 weeks** (default working value; range 6-10 weeks per Guidance C-004). Scheduler to override with vendor-confirmed lead times when available. (Source: _SEMANTIC_LENSING.md A-002)
- No significant unforeseen ground conditions (based on 2021 geotech report; risk accepted per DEC-013).
- Wetland setback and environmental buffer requirements do not constrain critical path activities (ASSUMPTION; TBD on review of Appendix D).

**5. Commissioning and Closeout Assumptions**
- Systems commissioning duration: 4-6 weeks.
- Staff training: 1-2 weeks (concurrent with commissioning; per DEL-08-01 requirements).
- O&M manual and as-built drawings prepared concurrently with commissioning.
- Occupancy permit issuance: **2 weeks** after substantial performance (ASSUMPTION; Scheduler to confirm with AHJ). (Source: _SEMANTIC_LENSING.md A-002)
- Warranty period: 12 calendar months from occupancy permit date (RFP 7.6).

**6. Schedule Philosophy**
- "This schedule is optimized for cost/value, not minimum duration, consistent with the Owner's stated 'not schedule-driven' philosophy (RFP 2.2). [Specific cost-optimization rationale to be stated by Scheduler, e.g., seasonal phasing, resource leveling, avoiding premium procurement.]"

**Output:** Schedule Assumptions List (formatted as bullet list or table; embedded in proposal Section 7.1.9 response or as labeled appendix to that section).

**Source:** RFP 7.1.9; Decomposition DEL-09-01; RFP 2.2; Addendum 03; Decomposition DEC-013.

---

### Step 6: Write Critical Path Narrative

**Action:**
Write a 1-2 page (or ~400-600 word) narrative covering:

1. **Critical Path Identification:**
   - "The critical path for this project runs through: [list critical activities in sequence, e.g., Design Development -> Permitting -> Site Work -> Building Construction -> Commissioning -> Substantial Performance]."
   - "Total critical path duration: approximately [X] weeks from contract award to Substantial Performance."

2. **Critical Path Logic:**
   - Why is each critical path activity on the critical path? (e.g., "Permitting is on the critical path because construction cannot begin without permit issuance, and permit review is estimated at [X] weeks.")
   - What design/construction overlap is included and how it reduces overall duration?

3. **Float Analysis:**
   - Identify 2-3 activities with significant float: "Cold Storage construction has approximately [X] weeks of float and can absorb minor delays without affecting Substantial Performance."
   - Explain how float will be managed.

4. **Schedule Risk Items:**
   - "If permit review exceeds [X] weeks, the critical path extends by the same duration; no mitigation within design schedule exists."
   - "Long-lead equipment (overhead doors, generator) is ordered at 60% DD; if delivery is delayed beyond [X] weeks, MEP commissioning could be affected."
   - "Weather delays on outdoor site work are the most likely non-critical path risk; [X] weeks of weather contingency is included in Phase 4 duration."

5. **Cost-Optimization Statement:**
   - Restate how the schedule demonstrates cost optimization (reference Guidance P-002 and T-001).

**Output:** Critical Path Narrative (1-2 pages; embedded in proposal Section 7.1.9 response).

**Source:** RFP 7.1.9 ("critical path identified and narrated"); Decomposition DEL-09-01.

---

### Step 7: Quality Review

**Action:**

**V-SCH-01: Format and Completeness Review (PM)**
- Gantt chart is in standard horizontal bar chart format.
- All key work package phases are present (Phases 0-9 per WBS).
- All required milestone dates are shown and dated.
- Critical path is visually identified.
- Chart is readable at proposal submission resolution.

**V-SCH-02: Design Milestone Integration (Design Manager)**
- Confirm all five design submission milestones from RFP 7.1.8 appear in the Gantt chart:
  - [ ] Building Design Development
  - [ ] 60% Detailed Design review
  - [ ] Foundation IFC (if needed)
  - [ ] 100% Building Detail Design
  - [ ] 100% IFC Detailed Design Package
- Confirm Owner review windows are included after each submission.

**V-SCH-03: Construction Phase Validation (Construction Manager)**
- Confirm construction phase durations are realistic for Main Building and Cold Storage of this type and size.
- Confirm site work sequencing reflects seasonal weather window.
- Confirm long-lead procurement timing is adequate.

**V-SCH-04: Assumptions Completeness (PM / Scheduler)**
- Confirm assumptions cover all required categories (permit, design, site, construction, commissioning, schedule philosophy).
- Confirm no assumption contradicts another deliverable (DEL-06-02, DEL-07-01, DEL-08-01).

**V-SCH-05: Critical Path Logic (Scheduler)**
- Confirm critical path is correctly identified (no logical errors; zero-float activities are correct).
- Confirm float analysis is accurate.
- Confirm narrative matches the Gantt chart.

**V-SCH-06: Cross-Deliverable Consistency (PM)**
- Confirm design submission milestone dates are consistent with DEL-06-02 (once produced).
- Confirm construction sequencing is consistent with DEL-07-01.
- Confirm commissioning timeline is consistent with DEL-08-01.

**V-SCH-07: Cost-Optimization Rationale (PM)**
- Confirm schedule narrative explicitly states how the proposed timeline leverages Owner's "not schedule-driven" flexibility.
- Confirm rationale is specific and credible (not generic boilerplate).

**Output:** Completed quality review checklist; any issues resolved before submission.

**Source:** RFP 7.1.9; Specification requirements R-SCH-01 through R-SCH-15.

---

### Step 8: Package for Proposal Submission

**Action:**
1. Export Gantt chart to PDF; confirm readability at typical screen zoom.
2. Assemble the DEL-09-01 submission package:
   - Gantt Chart (PDF)
   - Critical Path Narrative (text or PDF; 1-2 pages)
   - Schedule Assumptions List (text or PDF; 1 page)
3. Place within RFP Section 7.1.9 response in the proposal document, per RFP 4.3 ordering (C-02).
4. Retain editable schedule file (MS Project, Smartsheet, etc.) for post-award use (20-day baseline resubmission per RFP 7.2).
5. Confirm total PDF size contribution is within overall 15 MB proposal limit (C-01).

**Output:** DEL-09-01 package ready for proposal inclusion.

**Source:** RFP 4.2 (15 MB limit, C-01); RFP 4.3 (section ordering, C-02); RFP 7.1.9.

---

## Verification

| V-ID | Verification Check | Pass Criteria | Responsible |
|------|-------------------|---------------|-------------|
| **V-SCH-01** | Gantt chart format | Horizontal bar chart; time scale visible; activities labeled | PM |
| **V-SCH-02** | All phases present | Phases 0-9 represented; no major activity category omitted | PM |
| **V-SCH-03** | Milestone dates shown | All milestones listed in R-SCH-03 are dated in Gantt | PM / Scheduler |
| **V-SCH-04** | Critical path identified | Critical path visually distinct; zero-float activities correct | Scheduler |
| **V-SCH-05** | Five design milestones integrated | All five from RFP 7.1.8 present; Owner review windows included | Design Manager |
| **V-SCH-06** | Substantial Completion proposed | Date proposed and shown in Gantt | PM |
| **V-SCH-07** | Warranty review milestone | 12-month milestone present after occupancy permit date | PM |
| **V-SCH-08** | Assumptions list complete | All six assumption categories covered per Step 5 | Scheduler |
| **V-SCH-09** | Critical path narrative | Explains critical activities, float, and risk; 1-2 pages | PM |
| **V-SCH-10** | Cost-optimization rationale | Explicit statement of why schedule optimizes cost/value | PM |
| **V-SCH-11** | Cross-deliverable consistency | Design milestone dates consistent with DEL-06-02; construction consistent with DEL-07-01; commissioning consistent with DEL-08-01 | PM |
| **V-SCH-12** | PDF readability | Gantt chart readable at typical proposal zoom; high-resolution PDF | PM |
| **V-SCH-13** | Proposal size contribution | Gantt PDF size fits within 15 MB total proposal limit (C-01) | Proposal Manager |

---

## Records

### Proposal Artifacts (to be submitted)

| Record | Format | Retention |
|--------|--------|-----------|
| Gantt Chart (PDF) | PDF | Submitted in proposal; retained in project archive |
| Critical Path Narrative | Text/PDF | Submitted in proposal; retained |
| Schedule Assumptions List | Text/PDF | Submitted in proposal; retained |

### Working Documents (retained internally)

| Record | Format | Retention |
|--------|--------|-----------|
| Editable schedule file | MS Project / Smartsheet / Primavera file | Retained for post-award 20-day baseline resubmission |
| WBS outline and duration estimates | Internal document | Retained as basis for assumptions |
| Design Manager input on design durations | Email/notes | Retained |
| Construction Manager input on construction durations | Email/notes | Retained |
| QA/QC review sign-off | Checklist/email | Retained |

### Post-Award Schedule Obligations

| Obligation | Deadline | Source |
|-----------|---------|--------|
| Submit detailed project schedule to Project Manager | Within 20 calendar days of contract award | RFP 7.2, p. 19 |
| Project Committee review and acceptance of schedule | After submission; becomes Master Project Schedule | RFP 7.2, p. 19 |
| Monthly schedule updates with % complete per task | Monthly throughout construction | RFP 7.2, p. 19 |
| Report any schedule revisions to Project Manager | As revisions occur | RFP 7.2, p. 19 |
