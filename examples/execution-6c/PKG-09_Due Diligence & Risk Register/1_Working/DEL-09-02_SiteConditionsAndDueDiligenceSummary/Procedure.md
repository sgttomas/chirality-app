# Procedure: DEL-09-02 Site Conditions and Due Diligence Summary

## Purpose

**What this procedure accomplishes:**

This procedure describes the process to **produce** the Site Conditions and Due Diligence Summary deliverable (DEL-09-02) for the Penhold Public Services Building Design-Build proposal. The procedure guides the PM and technical leads through the steps of reviewing reference reports, extracting key findings, identifying site constraints, proposing mitigation strategies, and ensuring cross-deliverable consistency.

**Dual-use interpretation:** This procedure focuses on the **production** of the deliverable artifact (the summary document), not the operation/use of the artifact. The summary document itself is a proposal input, not an operational procedure.

**Source:** AGENT_4_DOCUMENTS protocol (Procedure Schema: "Purpose: What this procedure accomplishes — production and/or operation of this deliverable's artifact")

---

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies coordinated externally by humans (see `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`).

**Manual coordination requirements:**
- **Upstream coordination (inputs required):**
  - Access to all reference reports listed in `_REFERENCES.md` (geotechnical, wetland, environmental, grading, flood mapping, adjacent subdivision design).
  - Preliminary concept design direction (building size, program, site layout strategy) from PKG-04 team (DEL-02-01 lead).
  - Preliminary pricing strategy (allowance approach, cost estimation basis) from PKG-02 team (DEL-05-01/05-02 lead).
  - Preliminary schedule assumptions (survey timing, permitting activities) from PKG-08 team (DEL-08-01 lead).

- **Downstream coordination (outputs delivered to):**
  - **PKG-04 (Concept Design):** Site constraints inform building placement, site layout, grading strategy, access design.
  - **PKG-02 (Pricing):** Site conditions inform foundation cost, earthwork cost, servicing allowances, risk contingencies.
  - **PKG-09 (Risk Register):** Site constraints are captured as risks with mitigation strategies (DEL-09-01 lead).
  - **PKG-08 (Schedule):** Survey availability, permitting timelines, site preparation activities are reflected in schedule (DEL-08-01 lead).

**Source:** `_DEPENDENCIES.md` (NOT_TRACKED mode); Decomposition document Section 8 (DEL-09-02 downstream use)

### Reference Materials

The following reference materials must be available before starting this procedure:

| Reference Material | Location | Purpose |
|--------------------|----------|---------|
| **Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md** | `execution/_Decomposition/` | Project context, addenda integration, deliverable definition |
| **_CONTEXT.md** | Deliverable folder | Deliverable identity, discipline, acceptance criteria, anticipated artifacts |
| **_REFERENCES.md** | Deliverable folder | List of applicable reference reports and their locations |
| **AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf** | `execution/_Sources/` | Base RFP; Section 2.3 (site context), Section 7.4 (survey requirements) |
| **AB-2024-07156-Penhold_Public Services Building Addendum03.pdf** | `execution/_Sources/` | Addendum 03; 12-acre developable area, survey files after award, servicing allowance approach |
| **AB-2024-07156-Penhold PSB_Geotechnical Investigation Report.pdf** | `execution/_Sources/` | Geotechnical findings (soil, bearing capacity, groundwater, foundation recommendations) |
| **AB-2024-07156-Penhold PSB_Wetland Assessment.pdf** | `execution/_Sources/` | Wetland findings (presence, classification, setbacks, permitting) |
| **AB-2024-07156-Penhold PSB_Desktop_Field_Enviro_Assessment_2021 ghost Pine.pdf** | `execution/_Sources/` | Environmental findings (contamination screening, regulatory constraints) |
| **AB-2024-07156-Penhold PSB_Site grading.pdf** | `execution/_Sources/` | Site grading and drainage context |
| **AB-2024-07156-Penhold PSB_parcel  flood zone.pdf** | `execution/_Sources/` | Flood zone mapping and constraints |
| **AB-2024-07156-Penhold PSB_Adjacent Subdivision Design.pdf** | `execution/_Sources/` | Adjacent infrastructure and servicing context |

**Source:** `_REFERENCES.md`; AGENT_4_DOCUMENTS protocol Step 1 (Read Context)

### Prerequisite Criticality Classification (B-006)

**Not all prerequisites are equally blocking.** Classification by criticality:

| Criticality Tier | Documents | Impact of Absence | Proceed with TBD? |
|-----------------|-----------|-------------------|-------------------|
| **BLOCKING** (must have before concept design) | Geotechnical Report, Flood Zone Mapping, Wetland Assessment, Site Grading | Foundation design cannot proceed; site layout cannot be finalized; flood compliance cannot be verified | NO — Concept design on hold until obtained or explicit PM waiver with documented risk acceptance |
| **IMPORTANT** (should have) | Adjacent Subdivision Design, Environmental Assessment | Servicing coordination incomplete; environmental clearance status unknown | YES with ASSUMPTIONS — Document assumptions; include contingency; flag for post-award verification |
| **NICE-TO-HAVE** (can proceed with TBD) | Specific code section references, Town bylaws | Implementation details may require adjustment | YES — Proceed with standard code assumptions; verify during detailed design |

**Gate Protocol:** If BLOCKING documents are unavailable, PM must approve proceeding with ASSUMPTIONs and explicit risk acceptance documented in DEL-09-01 risk register.

**Source:** _SEMANTIC_LENSING.md Item B-006; prerequisite criticality classification

### Tools and Access

- **Document review tools:** PDF reader, markup tools for annotating reference reports.
- **Collaboration tools:** Communication channel with PKG-02 (estimator), PKG-04 (designer), PKG-08 (scheduler), PKG-09 (risk lead) for coordination.
- **Deliverable folder access:** Read/write access to `execution/PKG-09_Due Diligence & Risk Register/1_Working/DEL-09-02_SiteConditionsAndDueDiligenceSummary/`.
- **Subject matter expertise:** Access to geotechnical engineer, environmental consultant, civil engineer for technical review and interpretation of reference reports.

**Source:** ASSUMPTION based on deliverable production requirements

---

## Compliance Governance Structure (D-001)

**Roles and Responsibilities:**

| Role | Accountability | Authority |
|------|---------------|-----------|
| **PM** | Overall compliance framework; coordination across disciplines; documentation of compliance determinations | Final decision authority on compliance interpretation disputes; escalation to Proposal Manager for RFP clarification |
| **Geotechnical/Structural Technical Lead** | Interpreting geotechnical findings; determining foundation-related regulatory compliance | Signs off on geotechnical interpretation accuracy |
| **Environmental/Civil Technical Lead** | Interpreting wetland/environmental findings; determining environmental regulatory compliance | Signs off on environmental compliance status |
| **Civil Technical Lead** | Interpreting grading/flood/servicing findings; determining civil engineering regulatory compliance | Signs off on grading/drainage/flood compliance |

**Escalation Path for Compliance Disputes:**
1. If Technical Lead and PM disagree on compliance interpretation, escalate to external authority:
   - For wetland/environmental: Alberta Environment and Protected Areas
   - For geotechnical/grading: Professional Engineer peer review
   - For servicing: Municipal utility department (Town of Penhold)
2. PM documents all compliance determinations and disputes in the Assumption Register (ASSUM-XXX entries)
3. Unresolved compliance disputes are flagged as TBD and escalated to Proposal Manager for RFP clarification or PM decision with documented risk acceptance

**Source:** _SEMANTIC_LENSING.md Item D-001; compliance governance structure

---

## Steps

### Step 1: Review Deliverable Context and Scope

**Action:**
1. Read `_CONTEXT.md` in the deliverable folder to understand:
   - Deliverable ID, name, package, discipline, type, responsible party.
   - Description and acceptance criteria.
   - Anticipated artifacts.
   - Scope traceability (SOW-024, SOW-025; OBJ-008).
2. Read the deliverable's entry in the decomposition document (`Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`, Section 8, DEL-09-02) to understand:
   - Deliverable purpose and downstream use.
   - Relationship to other deliverables (DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01).
3. Confirm the current status in `_STATUS.md` (should be `OPEN` at the start of this procedure).

**Output:** Clear understanding of deliverable identity, scope, and success criteria.

**Verification:** Deliverable context matches the decomposition document entry; anticipated artifacts align with acceptance criteria.

**Source:** AGENT_4_DOCUMENTS protocol Step 1 (Read Context)

---

### Step 2: Review Reference Reports and Extract Key Findings

**Action:**
1. Access all reference reports listed in `_REFERENCES.md` (geotechnical, wetland, environmental, grading, flood mapping, adjacent subdivision design).
2. For each reference report, extract key findings relevant to site conditions and constraints:

   **Geotechnical Investigation Report:**
   - Soil stratigraphy and classification.
   - Bearing capacity values (allowable bearing pressure at foundation depth).
   - Groundwater depth and seasonal variation.
   - Foundation type recommendations (spread footings, piles, engineered fill requirements).
   - Seismic site class (if reported).
   - Frost depth and minimum foundation depth.
   - Implications for earthwork (cut/fill, compaction requirements).

   **Wetland Assessment Report:**
   - Wetland presence, location, and extent (map reference).
   - Wetland classification (permanent/seasonal; Class I–IV per Alberta Wetland Policy).
   - Required setback distances from wetland boundaries.
   - Regulatory permitting requirements (Alberta Water Act authorization trigger).
   - Implications for site layout and access design.

   **Desktop Environmental Assessment:**
   - Historical land use and potential contamination sources.
   - Phase I ESA screening results (presence/absence of environmental concerns).
   - Need for Phase II ESA (if contamination suspected).
   - Regulatory clearance status or further investigation requirements.
   - Implications for site development and construction safety.

   **Site Grading Document:**
   - Existing site topography and elevation range.
   - Natural drainage patterns and flow directions.
   - Cut-and-fill earthwork context for site development.
   - Grading implications for building placement and site servicing.

   **Flood Zone Mapping:**
   - Flood zone designation (flood fringe vs. floodway).
   - Extent of flood fringe area (cross-check against Addendum 03: 8 acres).
   - Developable area constraint (cross-check against Addendum 03: 12 acres).
   - Flood elevation and freeboard requirements (if reported).

   **Adjacent Subdivision Design:**
   - Adjacent infrastructure context (roads, utilities, drainage).
   - Service tie-in points (water, sanitary sewer, storm sewer) and routing constraints.
   - Coordination requirements with adjacent development.

3. Document findings in structured tables (see Datasheet.md and Guidance.md Example 2 for table templates).
4. Flag any missing information or unclear findings as **TBD** with a note to follow up with report authors or subject matter experts.

**Output:** Structured extraction of key findings from all reference reports, organized by discipline (geotechnical, wetland, environmental, grading, flood, servicing).

**Verification:** Extracted findings are accurately cited with report section references; all reference reports listed in `_REFERENCES.md` have been reviewed (or flagged as inaccessible).

**Source:** AGENT_4_DOCUMENTS protocol Step 4a (Datasheet: populate Attributes from reference materials); Specification R-01 through R-10 (requirements for findings extraction)

---

### Step 3: Identify Site Constraints and Implications

**Action:**
1. Review extracted findings (from Step 2) and identify site constraints that affect design, cost, schedule, or risk:

   **Design constraints:**
   - Building placement limitations (wetland setbacks, flood fringe exclusion, grading feasibility).
   - Foundation design requirements (bearing capacity, frost depth, groundwater management).
   - Site access and circulation constraints (grading, drainage, wetland avoidance).

   **Cost constraints:**
   - Foundation type and depth (affects foundation cost).
   - Earthwork quantities (cut/fill, engineered fill requirements).
   - Environmental mitigation (Phase II ESA, remediation if required).
   - Servicing tie-in costs (allowance for uncertain connection points).

   **Schedule constraints:**
   - Survey availability (after contract award per Addendum 03).
   - Permitting timelines (Alberta Water Act if wetland disturbance; environmental clearance).
   - Earthwork sequencing (frost protection, groundwater management).

   **Risk constraints:**
   - Uncertainty in geotechnical conditions (potential for unforeseen soil conditions).
   - Uncertainty in servicing costs (tie-in points TBD per Addendum 03).
   - Uncertainty in environmental clearance (Phase II ESA may identify contamination).

2. For each constraint, assess the impact on the four dimensions (design, cost, schedule, risk).
3. Document constraints in a structured constraint-to-mitigation matrix (see Guidance.md Example 1 for template).

**Output:** Comprehensive list of site constraints with impact assessment (design, cost, schedule, risk) for each constraint.

**Verification:** All material site constraints from reference reports are captured; impact assessment is credible and aligned with engineering judgment.

**Source:** Specification R-11 (Constraint-to-Mitigation Mapping); Decomposition document Section 8 (DEL-09-02 acceptance criteria: "identifies constraints and mitigation actions")

---

### Step 4: Propose Mitigation Strategies

**Action:**
1. For each constraint identified in Step 3, propose at least one mitigation strategy that addresses the constraint and reduces its impact:

   **Example mitigation strategies:**
   - **Wetland setback constraint:** Position building and access roads to maintain required setback distance; optimize site layout to avoid wetland buffer encroachment.
   - **Flood fringe constraint:** Confirm building placement within 12-acre developable area (outside 8-acre flood fringe per Addendum 03); allocate storm pond within flood fringe area.
   - **Low bearing capacity:** Design foundations per geotechnical recommendations (spread footings on engineered fill, piles if required); include cost allowance in pricing.
   - **Groundwater management:** Design perimeter drainage system; avoid dewatering if possible (schedule and cost savings).
   - **Survey data limitation:** Use available site grading and subdivision plan references for conceptual design; perform detailed survey post-award (schedule survey activity in DEL-08-01).
   - **Service tie-in uncertainty:** Use allowance approach for service tie-in costs per Addendum 03; coordinate with utility providers post-award for final connection points.
   - **Environmental contamination (if identified):** Include Phase II ESA in post-award schedule; include remediation cost allowance in pricing (if contamination suspected).

2. Assess residual risk after mitigation (low, medium, high) based on the effectiveness of the mitigation strategy and the likelihood of unforeseen issues.
3. Cross-reference each mitigation strategy to related deliverables:
   - **Design mitigations:** Reference DEL-02-01 (Concept Design Package).
   - **Cost mitigations:** Reference DEL-05-03 (Pricing Narrative and Assumptions).
   - **Schedule mitigations:** Reference DEL-08-01 (Detailed Project Schedule).
   - **Risk mitigations:** Reference DEL-09-01 (Risk Register and Mitigation Plan).
4. Document mitigation strategies in the constraint-to-mitigation matrix (see Guidance.md Example 1).

**Output:** Mitigation strategy for each identified constraint, with residual risk assessment and cross-references to related deliverables.

**Verification:** Mitigation strategies are credible, specific, and feasible; residual risks are transparently assessed; cross-references are accurate.

**Source:** Specification R-11 (Constraint-to-Mitigation Mapping); Guidance Principle 2 (Constraints Must Be Explicitly Linked to Mitigation)

---

### Step 4a: Evidence Extraction Protocol (F-004)

**Structured extraction ensures traceability and consistency.**

**Evidence Extraction Form (for each reference report):**

| Field | Content |
|-------|---------|
| **Report Title** | [Full title from report cover] |
| **Date + Author Credentials** | [Report date; Author name and professional designation (P.Eng., P.Geo., etc.)] |
| **Investigation Methodology** | [Brief summary: desk study, field investigation, laboratory testing, etc.] |
| **Key Findings Table:** | |
| - Finding Statement | [Specific finding from report] |
| - Report Citation | [Page number / Section reference] |
| - Key Data Values | [Numeric values: bearing capacity, depth, setback, etc.] |
| - Confidence Level | HIGH (direct measurement) / MEDIUM (interpreted) / LOW (inferred or assumed) |
| - Related Constraints | [Constraint ID from Constraint-to-Mitigation Matrix] |

**Protocol Application:** Use consistent format across all reports. Create extraction form template for team to populate during working sessions. Structured extraction ensures:
- Findings are traceable to source documents
- Confidence levels are explicit
- Cross-references to constraints are maintained

**Source:** _SEMANTIC_LENSING.md Item F-004; evidence extraction protocol

---

### Step 5: Integrate Addendum 03 Clarifications

**Action:**
1. Review Addendum 03 (or the Addendum 03 integration summary in the decomposition document, Section 4) and ensure the following clarifications are explicitly addressed in this deliverable:

   **12-acre developable area:**
   - Confirm that the site conditions summary reflects the 12-acre developable area constraint and the 8-acre flood fringe allocation (dog park/storm pond).
   - Ensure the flood zone context section (Datasheet, Specification R-08) cites Addendum 03.

   **Survey files available after award:**
   - Confirm that the survey approach and assumptions section (Datasheet, Specification R-10, Guidance Example 3) cites Addendum 03 and describes the interim basis for conceptual design.
   - Ensure the schedule mitigation strategy (Step 4) includes post-award survey activity.

   **Site servicing allowance approach:**
   - Confirm that the site servicing context section (Datasheet, Specification R-09) cites Addendum 03 and describes the allowance approach.
   - Ensure the cost mitigation strategy (Step 4) includes a servicing allowance cross-referenced to DEL-05-03.

2. Flag any inconsistencies between Addendum 03 and reference reports (e.g., if flood zone mapping shows a different developable area than stated in Addendum 03, flag this as a conflict for human ruling).

**Output:** Addendum 03 clarifications are explicitly integrated into the site conditions summary; any conflicts are flagged in the Guidance.md Conflict Table.

**Verification:** All Addendum 03 clarifications are cited and addressed; no conflicts with reference reports are unresolved.

**Source:** Decomposition document Section 4 (Addendum 03 integration summary); Guidance Principle 3 (Addenda Integration Is Critical to Compliance)

---

### Step 6: Coordinate with Related Deliverables

**Action:**
1. Share draft site conditions summary (Datasheet, Specification, Guidance, Procedure) with leads for related deliverables:
   - **PKG-04 (Concept Design, DEL-02-01):** Confirm that site constraints and mitigation strategies align with concept design assumptions (building placement, site layout, grading strategy).
   - **PKG-02 (Pricing, DEL-05-03):** Confirm that cost implications (foundation cost, earthwork cost, servicing allowances) are reflected in pricing assumptions.
   - **PKG-09 (Risk Register, DEL-09-01):** Confirm that site constraints are captured as risks in the risk register and that mitigation strategies are consistent.
   - **PKG-08 (Schedule, DEL-08-01):** Confirm that schedule implications (survey timing, permitting activities, earthwork sequencing) are reflected in the schedule.

2. Resolve any inconsistencies or coordination gaps identified during cross-deliverable review:
   - If terminology differs (e.g., "flood fringe" vs. "flood zone"), standardize terminology across all deliverables.
   - If values differ (e.g., bearing capacity, setback distance), verify against reference reports and correct as needed.
   - If mitigation strategies conflict (e.g., concept design shows building in wetland buffer; site conditions summary says setback required), flag the conflict and coordinate with the design lead to resolve.

3. Document cross-deliverable coordination in the Specification R-12 (Cross-Deliverable Consistency) verification notes.

**Output:** Site conditions summary is consistent with related deliverables (concept design, pricing, risk register, schedule); terminology and values are standardized.

**Verification:** No unresolved inconsistencies between this deliverable and related deliverables; coordination notes are documented.

**Source:** Specification R-12 (Cross-Deliverable Consistency); AGENT_4_DOCUMENTS protocol Step 5 (Cross-Reference Consistency Check)

---

### Step 6a: Site Conditions Propagation Protocol (D-005)

**Formalized mechanism for propagating site understanding to downstream deliverables.**

**Propagation Checklist Process:**
1. PM drafts Site Conditions Propagation Checklist listing all identified constraints from DEL-09-02
2. PM distributes checklist to leads of DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01
3. Each lead reviews checklist and responds with one of:
   - "Constraint [X] addressed in our deliverable at [section Y]"
   - "Constraint [X] not applicable to our deliverable; justification: [reason]"
   - "Constraint [X] TBD pending [information]"
4. PM consolidates responses
5. Any TBD or missing response triggers PM follow-up within 2 business days
6. PM maintains Propagation Record: who confirmed what, when

**Propagation Record Template:**

| Constraint ID | DEL-02-01 Confirmation | DEL-05-03 Confirmation | DEL-09-01 Confirmation | DEL-08-01 Confirmation | Status |
|---------------|------------------------|------------------------|------------------------|------------------------|--------|
| C-GEO-01 | [Lead name, date, section ref] | [Lead name, date, section ref] | [Lead name, date, section ref] | [Lead name, date, section ref] | COMPLETE / PENDING |

**Gate Requirement:** Step 7 (Finalize Documents) cannot be completed until Propagation Record shows all constraints either CONFIRMED or explicitly justified as N/A.

**Source:** _SEMANTIC_LENSING.md Item D-005; site conditions propagation protocol

---

### Step 7: Finalize Four Documents (Datasheet, Specification, Guidance, Procedure)

**Action:**
1. Compile the finalized content into the four deliverable documents:
   - **Datasheet.md:** Identification, Attributes (site context, geotechnical, wetland, environmental, grading, flood, servicing, survey), Conditions, Construction, References.
   - **Specification.md:** Scope, Requirements (R-01 through R-12), Standards, Verification, Documentation.
   - **Guidance.md:** Purpose, Principles, Considerations, Trade-offs, Examples, Conflict Table.
   - **Procedure.md:** Purpose, Prerequisites, Steps, Verification, Records (this document).

2. Ensure all sections are complete and all TBDs are flagged with justification (e.g., "TBD — Geotechnical Report PDF not accessible; requires human review").
3. Ensure all assumptions are labeled as **ASSUMPTION** with rationale.
4. Ensure all sources are cited (decomposition document, `_CONTEXT.md`, `_REFERENCES.md`, reference reports, Addendum 03).
5. Run a final cross-document consistency check (see Step 6 verification notes).

**Output:** Four finalized documents (Datasheet, Specification, Guidance, Procedure) ready for working sessions and proposal integration.

**Verification:** All four documents are complete; schema sections are populated; TBDs and assumptions are labeled; sources are cited; cross-document consistency is verified.

**Source:** AGENT_4_DOCUMENTS protocol Step 4 (Generate Four Documents); Step 5 (Cross-Reference Consistency Check)

---

### Step 7a: Discipline Coverage Verification Checklist (X-002)

**Before finalizing, confirm all disciplines have been adequately addressed:**

| Discipline | Coverage Check | Status |
|------------|---------------|--------|
| ☐ **Geotechnical** | Findings summarized with constraints identified | TBD / PARTIAL / COMPLETE |
| ☐ **Wetland** | Findings summarized with setback/permitting implications | TBD / PARTIAL / COMPLETE |
| ☐ **Environmental** | Findings summarized with clearance status | TBD / PARTIAL / COMPLETE |
| ☐ **Grading/Drainage** | Context summarized with earthwork implications | TBD / PARTIAL / COMPLETE |
| ☐ **Flood Zone** | Context summarized with building placement strategy | TBD / PARTIAL / COMPLETE |
| ☐ **Servicing** | Context summarized with allowance approach | TBD / PARTIAL / COMPLETE |
| ☐ **Survey** | Approach and assumptions documented | TBD / PARTIAL / COMPLETE |
| ☐ **Constraint-to-Mitigation** | Mapping addresses constraints from all disciplines | TBD / PARTIAL / COMPLETE |

**Gate Requirement:** If any discipline is marked TBD, loop back and add missing section or document explicit justification for deferral.

**Source:** _SEMANTIC_LENSING.md Item X-002; discipline coverage verification

---

### Step 7b: Synthesis Readiness Assessment (D-006)

**Before releasing for proposal integration, PM assesses:**

| Assessment Criterion | Question | Result |
|---------------------|----------|--------|
| **Synthesis Clarity** | Does the site characterization narrative (per R-15) clearly communicate key design drivers, cost drivers, and schedule drivers? | READY / REQUIRES REVISION |
| **Internal Consistency** | Are all 4 documents (Datasheet, Specification, Guidance, Procedure) internally consistent (terminology, values, cross-references)? | READY / REQUIRES REVISION |
| **External Consistency** | Are all 4 documents consistent with downstream deliverables (same constraints, same terminology, same cross-references)? | READY / REQUIRES REVISION |
| **TBD Justification** | Are all TBDs justified and flagged with escalation path? | READY / REQUIRES REVISION |
| **Assumption Labeling** | Are all assumptions labeled with rationale? | READY / REQUIRES REVISION |

**Assessment Result:** If all criteria = READY, proceed to proposal integration. If any criterion = REQUIRES REVISION, loop back to PM for targeted fixes.

**Source:** _SEMANTIC_LENSING.md Item D-006; synthesis readiness assessment

---

### Step 8: Proposal Readiness Gate (C-007)

**Before releasing DEL-09-02 for proposal integration, confirm:**

| Gate Criterion | Check | Status |
|----------------|-------|--------|
| ☐ All accessible reference reports reviewed | Inaccessible reports flagged with justification | PASS / FAIL |
| ☐ Constraint-to-Mitigation matrix populated | ≥5 material constraints with proposed mitigations | PASS / FAIL |
| ☐ Addendum 03 clarifications cited | 12-acre developable area, survey timing, servicing allowance explicitly cited | PASS / FAIL |
| ☐ No unresolved conflicts | CONF-001 type conflicts escalated to PM for ruling | PASS / FAIL |
| ☐ Cross-references reciprocated | Downstream documents (DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01) cite back to DEL-09-02 | PASS / FAIL |
| ☐ Terminology standardized | All four documents use consistent terminology | PASS / FAIL |
| ☐ TBDs justified; ASSUMPTIONs labeled | Every TBD has reason; every ASSUMPTION has rationale | PASS / FAIL |

**Gate Result:** If all checks = PASS: READY FOR PROPOSAL. If any check = FAIL: HOLD FOR REVISION — PM identifies specific remediation required.

**Source:** _SEMANTIC_LENSING.md Item C-007; proposal readiness gate

---

### Step 8a: Regulatory Compliance Sign-Off (A-003)

**Action:** PM obtains written confirmation from relevant authorities that site conditions summary accurately reflects regulatory requirements and constraints:

| Authority | Scope | Sign-Off Required |
|-----------|-------|------------------|
| **Environmental Consultant** | Wetland/environmental constraints per Wetland Assessment and Environmental Assessment | Confirmation that wetland setbacks and environmental clearance status are accurately represented |
| **Structural/Geotechnical Engineer** | Geotechnical constraints per Geotechnical Report | Confirmation that geotechnical findings and foundation implications are accurately represented |
| **Civil Engineer** | Grading/flood constraints per Site Grading and Flood Zone Mapping | Confirmation that grading context and flood zone constraints are accurately represented |

**Sign-Off Documentation:** Each authority provides brief written statement (email acceptable): "I have reviewed DEL-09-02 Site Conditions Summary dated [date] and confirm it accurately represents [discipline] constraints based on available reference reports."

**Gate Requirement:** Regulatory compliance sign-off must be obtained before proposal submission. If any authority withholds sign-off, PM escalates for resolution.

**Source:** _SEMANTIC_LENSING.md Item A-003; regulatory compliance sign-off

---

### Step 9: Cross-Deliverable Assumption Audit (D-007)

**Action:** After all five deliverables (DEL-09-02, DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01) have drafted content:

1. PM consolidates all assumptions from all documents into single Assumption Registry
2. For each assumption in DEL-09-02, verify:
   - Is the same assumption stated in downstream deliverables?
   - If yes, are the rationales and values consistent?
   - If no, is the absence justified (assumption not applicable to downstream deliverable)?
   - Are there contradictory assumptions? (e.g., DEL-09-02 assumes frost depth 1.8 m; DEL-05-03 assumes 2.2 m)

**Audit Result:**
- **CONSISTENT:** All assumptions aligned or justified as N/A
- **INCONSISTENT:** Contradictions found — resolve via PM decision and update all affected documents

**Audit Timing:** Perform 3-5 business days before proposal submission to allow time for corrections.

**Source:** _SEMANTIC_LENSING.md Item D-007; cross-deliverable assumption audit

---

### Step 10: Update Status (OPEN → INITIALIZED)

**Action:**
1. Read `_STATUS.md` and verify the current state is `OPEN`.
2. If the current state is `OPEN`, update the status to `INITIALIZED` and append a history entry:
   ```
   **Current State:** INITIALIZED
   **Last Updated:** [YYYY-MM-DD]

   ## History
   - [YYYY-MM-DD] — State set to OPEN (PREPARATION)
   - [YYYY-MM-DD] — State set to INITIALIZED (4_DOCUMENTS agent — enrichment pass completed)
   ```
3. If the current state is **not** `OPEN`, do not modify `_STATUS.md` and report the skip reason (e.g., "Status update skipped; current state = INITIALIZED").

**Output:** `_STATUS.md` updated to `INITIALIZED` (if starting state was `OPEN`).

**Verification:** `_STATUS.md` reflects the correct state transition; history entry is appended with date and agent note.

**Source:** AGENT_4_DOCUMENTS protocol Step 7 (Update Status)

---

## Verification

### Step Completion Checks

| Step | Verification Check | Pass Criteria |
|------|-------------------|---------------|
| **Step 1: Review Context** | Deliverable context understood | Deliverable ID, scope, acceptance criteria, and anticipated artifacts are clear |
| **Step 2: Extract Findings** | All reference reports reviewed | Key findings extracted from all accessible reports; inaccessible reports flagged as TBD |
| **Step 3: Identify Constraints** | Site constraints identified | All material constraints captured with impact assessment (design, cost, schedule, risk) |
| **Step 4: Propose Mitigations** | Mitigation strategies proposed | Each constraint has at least one mitigation strategy; residual risks assessed; cross-references provided |
| **Step 5: Integrate Addendum 03** | Addendum 03 clarifications integrated | 12-acre developable area, survey timing, servicing allowance approach are explicitly addressed |
| **Step 6: Coordinate Deliverables** | Cross-deliverable consistency verified | Terminology and values consistent with DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01 |
| **Step 7: Finalize Documents** | Four documents complete | Datasheet, Specification, Guidance, Procedure all complete with schema sections populated |
| **Step 8: Update Status** | Status updated to INITIALIZED | `_STATUS.md` updated if starting state was OPEN; history entry appended |

**Source:** AGENT_4_DOCUMENTS protocol (SPEC: Document Set Validity requirements)

---

### Quality Control Checkpoints (X-004 Enhanced)

**QC Tracking Log:**

| Checkpoint | Responsible Role | Due Date | Verification Criteria | Sign-off Authority | Status | Sign-off Date |
|------------|-----------------|----------|----------------------|-------------------|--------|---------------|
| **QC-01: Context Review** | PM | Working Session 1 | Deliverable context matches decomposition; acceptance criteria clear | PM | PENDING | — |
| **QC-02: Findings Extraction** | Technical Leads | Working Session 2 | Key findings from all accessible reports extracted with citations | Discipline Lead | PENDING | — |
| **QC-03: Constraint Identification** | Technical Leads | Working Session 2 | All material constraints captured with impact assessment | PM + Lead | PENDING | — |
| **QC-04: Mitigation Proposal** | Technical Leads | Working Session 3 | Each constraint has mitigation; residual risks assessed | PM + Lead | PENDING | — |
| **QC-05: Addendum 03 Integration** | PM | Working Session 3 | 12-acre area, survey timing, servicing allowance explicitly cited | PM | PENDING | — |
| **QC-06: Deliverable Coordination** | PM | Working Session 4 | Cross-references to DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01 verified | PM | PENDING | — |
| **QC-07: Documents Finalization** | PM | Working Session 5 | All four documents complete; TBDs/ASSUMPTIONs labeled; sources cited | PM | PENDING | — |
| **QC-08: Status Update** | PM | After Working Sessions | _STATUS.md reflects correct state; history appended | PM | PENDING | — |

**Escalation Path:** If any checkpoint results in FAIL, PM identifies corrective action and re-schedules checkpoint verification. Proceed to next step only after PASS achieved.

**Before finalizing the deliverable, verify:**
1. **Source fidelity:** All non-trivial statements cite sources (decomposition document, reference reports, Addendum 03, etc.); unsupported content is labeled **TBD** or **ASSUMPTION**.
2. **Completeness:** All four documents are present; all schema sections are populated (no missing sections).
3. **Cross-document consistency:** Terminology, values, and entity references are consistent across Datasheet, Specification, Guidance, and Procedure.
4. **TBD transparency:** Missing information is marked **TBD** with justification (e.g., "PDF not accessible," "pending utility coordination post-award").
5. **Assumption transparency:** Inferred content is labeled **ASSUMPTION** with rationale.
6. **Addenda compliance:** Addendum 03 clarifications are explicitly cited and integrated.
7. **Cross-deliverable alignment:** Site constraints and mitigation strategies align with DEL-02-01, DEL-05-03, DEL-09-01, DEL-08-01.

**Source:** AGENT_4_DOCUMENTS protocol (non-negotiable invariants); Guidance Value Hierarchy; _SEMANTIC_LENSING.md Item X-004

---

## Records

### Documentation Outputs from This Procedure

| Output | Description | Location | Status |
|--------|-------------|----------|--------|
| **Datasheet.md** | Site conditions datasheet (identification, attributes, conditions, construction, references) | Deliverable folder | Generated (Pass 1 complete) |
| **Specification.md** | Site conditions specification (scope, requirements, standards, verification, documentation) | Deliverable folder | Generated (Pass 1 complete) |
| **Guidance.md** | Site conditions guidance (purpose, principles, considerations, trade-offs, examples, conflict table) | Deliverable folder | Generated (Pass 1 complete) |
| **Procedure.md** | Site conditions procedure (purpose, prerequisites, steps, verification, records) | Deliverable folder | Generated (Pass 1 complete; this document) |
| **_STATUS.md** | Deliverable status file (state transition: OPEN → INITIALIZED) | Deliverable folder | To be updated (Step 8) |
| **Constraint-to-Mitigation Matrix** | Structured table mapping site constraints to mitigation strategies | Embedded in Guidance.md (Example 1) | Placeholder structure (to be populated during working sessions) |
| **Geotechnical Findings Table** | Tabular summary of key geotechnical parameters | Embedded in Datasheet.md and Guidance.md (Example 2) | Placeholder structure (to be populated during working sessions) |
| **Survey Assumptions Statement** | Statement of survey data limitations and conceptual design assumptions | Embedded in Guidance.md (Example 3) and Specification.md (R-10) | Draft complete (Addendum 03 compliant) |

**Source:** AGENT_4_DOCUMENTS protocol Step 4 (Generate Four Documents); `_CONTEXT.md` (Anticipated Artifacts)

---

### Handoff to Working Sessions

**After completing this procedure:**
- The four documents (Datasheet, Specification, Guidance, Procedure) are available in the deliverable folder as scaffolds for human review and enrichment.
- TBDs and assumptions are flagged for follow-up during working sessions (reference report review, subject matter expert input, cross-deliverable coordination).
- The deliverable status is updated to `INITIALIZED`, signaling readiness for WORKING_ITEMS sessions.

**Next steps for humans:**
1. Review all reference reports (geotechnical, wetland, environmental, grading, flood mapping, adjacent subdivision design) and populate TBD sections in Datasheet.md and Specification.md.
2. Validate mitigation strategies and residual risk assessments with subject matter experts (geotechnical engineer, environmental consultant, civil engineer).
3. Coordinate with PKG-02 (estimator), PKG-04 (designer), PKG-08 (scheduler), PKG-09 (risk lead) to ensure cross-deliverable consistency.
4. Finalize constraint-to-mitigation matrix and geotechnical findings table with specific values and cross-references.
5. Update `_STATUS.md` to `IN_PROGRESS` when working sessions begin; update to `COMPLETE` when deliverable is finalized and approved for proposal submission.

**Source:** AGENT_4_DOCUMENTS protocol (RATIONALE: "These drafts are scaffolds")

---

**Document Status:** SEMANTIC_READY — Pass 3 Semantic Lensing Enrichment complete. 9 warranted items incorporated (A-003, B-006, C-007, D-001, D-005, D-006, D-007, F-004, X-002, X-004). Ready for working sessions.
