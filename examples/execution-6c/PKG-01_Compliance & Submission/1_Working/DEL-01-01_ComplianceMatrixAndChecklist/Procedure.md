# Procedure: DEL-01-01 ComplianceMatrixAndChecklist

## Purpose

This procedure describes how to **produce** the Compliance Matrix and Addenda Checklist artifacts for the Penhold Public Services Building RFP response. It provides the Proposal Manager with a systematic process to:

1. Extract all requirements from RFP Sections 6-9 and all three addenda
2. Map requirements to proposal deliverables and response locations
3. Verify 100% coverage of mandatory items
4. Flag pass/fail risks with owners and resolution paths
5. Track addenda integration across all affected deliverables
6. Complete addenda acknowledgment in Appendix H

**Source:** _CONTEXT.md (Deliverable description); Specification.md (Requirements REQ-01 through REQ-10)

---

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED - Dependencies coordinated externally by humans (see `_DEPENDENCIES.md`).

**ASSUMPTION:** While dependency tracking is not formalized, this deliverable logically benefits from:
- Access to all RFP source documents (main RFP + 3 addenda) - **AVAILABLE** (confirmed in _REFERENCES.md and _Sources/)
- Understanding of proposal structure and deliverable assignments (PKG-01 through PKG-09) - **AVAILABLE** (from Decomposition Section 7)
- Initial proposal outline or section numbering scheme - **TBD** (may not exist at time of compliance matrix creation; can be populated later)

### Personnel Requirements (D-003)

**Extraction Personnel:** Extraction shall be performed by:
- Proposal Manager, OR
- Proposal Controls Specialist with RFP subject matter expertise and understanding of proposal structure

**Qualification:** Extractor must have read/reviewed RFP Sections 6-9 before commencing extraction. Familiarity with the Decomposition document is recommended.

*Source: _SEMANTIC_LENSING.md, ItemID D-003 (proficiency-confirmed execution lens)*

---

### Reference Materials

**Must be available before starting:**

1. **RFP_2024_004.pdf** (main RFP) - particularly Sections 6-9
   - Location: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`

2. **Addendum 01, 02, 03** (all three addenda)
   - Location: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/` (Addendum01.pdf, Addendum02.pdf, Addendum03.pdf)

3. **Decomposition Document** (for deliverable mappings and scope ledger)
   - Location: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`

4. **_CONTEXT.md** (deliverable metadata)
   - Location: Current deliverable folder

**Optional but helpful:**
- Proposal outline or section structure (if available)
- Deliverable assignment matrix (showing which team members own which DEL-IDs)

**Source:** _REFERENCES.md; AGENT_4_DOCUMENTS protocol Step 1 (Read Context)

---

### Tools and Templates

**ASSUMPTION:** Recommended tools:
- **Spreadsheet software** (Excel, Google Sheets) for compliance matrix and addenda checklist (enables sorting, filtering, status tracking)
- **Markdown or Word** for risk register narrative (if separate from matrix)

**Template Structure (PROPOSAL):**

**Compliance Matrix Template Columns:**
| RFP Section | Subsection | Requirement Description | Mandatory (Y/N) | Evaluation Points | Proposal Section Reference | Proposal Page(s) | Compliance Status | Risk Level | Assigned Owner | Notes |

**Addenda Checklist Template Columns:**
| Addendum No. | Item No. | Change Description | Impact Type | Affected Deliverable(s) | Integration Action | Status | Proposal Section Ref | Acknowledged in App H? |

**Source:** Inferred from Specification.md requirements and Guidance.md examples

---

## Steps

### Step 0: Create Extraction Log (F-003)

**Action:**
1. Before beginning requirement extraction, create an Extraction Log with the following columns:
   - Requirement ID (sequential, e.g., REQ-001, REQ-002)
   - RFP Reference (section number and page)
   - Requirement Text (verbatim or paraphrased)
   - Extracted By (person name/role)
   - Date Extracted
   - Verification Status (Pending/Verified)

2. Maintain this log throughout Steps 1-7
3. Finalize log before proceeding to Step 8

**Purpose:** Provide documented evidence that the extraction procedure was followed with clear audit trail.

*Source: _SEMANTIC_LENSING.md, ItemID F-003 (operational evidence foundation lens)*

---

### Extraction Method Preamble (C-004)

For all extraction steps (Steps 1-7), follow this consistent method:

1. **Open** the relevant RFP section in the PDF
2. **Identify** the subsection heading
3. **Extract** the requirement statement using consistent format:
   - Direct quote for mandatory requirements
   - Summary with source reference for evaluated requirements
4. **Record** in compliance matrix template row with all required columns populated
5. **Document** RFP reference (section number + page number) in Extraction Log

*Source: _SEMANTIC_LENSING.md, ItemID C-004 (verified procedural grounding lens)*

---

### Step 1: Extract RFP Section 6 Requirements

**Action:**
1. Open RFP_2024_004.pdf to Section 6 (Mandatory Requirements), page 15
2. Extract requirement: "Section 6.1 - Letter of Offer - Proponent is to submit Appendix G (Letter of Offer) completed in full"
3. Record in compliance matrix:
   - RFP Section: 6.1
   - Requirement: Complete and submit Letter of Offer (Appendix G)
   - Mandatory: YES
   - Points: PASS/FAIL
   - Cross-reference to execution requirements in Section 5.2 (signatures and seals)
4. Flag as HIGH RISK (disqualification if missing per Section 9.19)

**Source:** RFP Section 6, page 15

**Verification:** Confirm Section 6 has only one subsection (6.1); if additional subsections found, add them to matrix.

---

### Step 2: Extract RFP Section 7 Requirements

**Action:**
1. Open RFP Section 7 (Project Delivery Plan), pages 15-25
2. Systematically extract each subsection:
   - **7.1 Design Methodology** (parent heading)
     - 7.1.1 Proposed Conceptual Design
     - 7.1.2 Design Brief (with sub-items: .1 Architectural, .2 Civil, .3 Structural, .4 Mechanical, .5 Electrical/IT)
     - 7.1.3 Accessibility
     - 7.1.4 Building Durability / Ease of Repair and Maintenance
     - 7.1.5 Adaptability, Flexibility, Potential for Expansion
     - 7.1.6 Design-Build Firms
     - 7.1.7 Design-Build Key Members
     - 7.1.8 Detailed Design and Construction Documents
     - 7.1.9 Detailed Project Schedule
   - **7.2 Construction Methodology** (with bullets: Health & Safety, Staging, Permits, Budget Control, Schedule Control, Communications, Quality Management)
   - **7.3 Construction Phase and Administration** (parent heading)
     - 7.3.1 Cleaning
     - 7.3.2 Transportation and Storage
     - 7.3.3 New Site Services and Utilities
     - 7.3.4 Subconsultants
     - 7.3.5 Project Meetings and Reporting
     - 7.3.6 Commissioning, Training, and Closeout Procedures
     - 7.3.7 Deficiencies
   - **7.4 Legal Survey and Topographical Survey**
   - **7.5 Substantial Performance of the Work**
   - **7.6 Warranty Requirements**

3. For each subsection, record in compliance matrix:
   - RFP Section reference
   - Requirement description (brief summary)
   - Mandatory status (NO - these are evaluated, not pass/fail)
   - Evaluation points (from Section 8.3 scoring matrix)
   - Mapped proposal deliverable(s) (from Decomposition Section 10 - Scope Ledger)

4. Cross-reference with Decomposition Section 10 (Scope Ledger) to confirm deliverable mappings

**Source:** RFP Section 7, pages 15-25; Decomposition Section 10 (Scope Ledger, SOW items)

**Verification:** Count subsections extracted; compare against RFP Table of Contents (pages 2-3) to ensure no subsection missed.

---

### Step 3: Extract RFP Section 8 Requirements

**Action:**
1. Open RFP Section 8 (Evaluation of Proposals), pages 25-28
2. Extract evaluation criteria from Section 8.3 (Scoring Matrix), page 26:
   - Mandatory: Letter of Offer + Formal Submission Compliance (PASS/FAIL)
   - Project Delivery Plan: Design Methodology (3 pts), Construction Methodology (3 pts), Commissioning/Training/Closeout (2 pts), Detailed Project Schedule (2 pts)
   - Design Proposal: Proposed Conceptual Design (20 pts), Design Brief (5 pts), Building Durability (15 pts), Project Team and Firms (15 pts)
   - Proposal Price: Appendix H (35 pts)
3. Record in compliance matrix with point values
4. Note Section 8.5 (Pricing) requirement: use Appendix H template; propose alternatives separately
5. Note Section 8.6 (Selection Ranking) tie-breaker rule: if equal scores, lowest price wins

**Source:** RFP Section 8, pages 25-28

**Verification:** Verify total points = 100 (excluding PASS/FAIL mandatory item).

---

### Step 4: Extract RFP Section 9 Requirements

**Action:**
1. Open RFP Section 9 (General Terms and Conditions), pages 28-35
2. Extract all 22 subsections (9.1 through 9.22)
3. For each subsection, record in compliance matrix:
   - RFP Section reference
   - Requirement summary
   - Compliance action (typically: "Acknowledge" or "Comply")
   - Risk level (most are LOW; exceptions: 9.19 Acknowledgement = HIGH)
4. Identify any subsections requiring specific proposal content (vs. simple acknowledgment):
   - **9.14 Insurance:** Proponent must be willing to evaluate OCIP vs CCIP (may need to note in proposal)
   - **9.19 Acknowledgement:** Completed via Letter of Offer (Appendix G) - links to Section 6.1 mandatory requirement
   - **9.20 Conflict of Interest:** Must declare any conflicts - if conflicts exist, requires disclosure narrative

**Source:** RFP Section 9, pages 28-35

**Verification:** Confirm all subsections from 9.1 through 9.22 are captured (no gaps in sequence).

---

### Step 5: Extract Addendum 01 Changes

**Action:**
1. Open Addendum 01 (1 page), dated July 11, 2024
2. Extract changes:
   - **Item 1.1:** Bidders meeting date confirmed as July 25 (NOT July 15)
   - **Item 1.2:** Missing functional program dimensions are intentional (allow design innovation); spaces must meet building code minimum
3. Record in addenda checklist:
   - Addendum No.: 01
   - Item No.: 1.1, 1.2
   - Change description
   - Impact type: 1.1 = Schedule/Admin (no proposal impact); 1.2 = Design (affects DEL-02-01, DEL-02-02)
   - Integration action: 1.2 requires narrative in Design Brief explaining approach to sizing unlisted spaces
4. Mark Item 1.1 as low impact (informational only); Item 1.2 as requiring design deliverable integration

**Source:** Addendum 01, page 1

**Verification:** Confirm both items from Addendum 01 are captured.

---

### Step 6: Extract Addendum 02 Changes

**Action:**
1. Open Addendum 02 (1 page), dated July 15, 2024
2. Extract change:
   - **Item 1.1:** Missing pages 62-63 is formatting error; no missing information
3. Record in addenda checklist:
   - Addendum No.: 02
   - Item No.: 1.1
   - Change description: Formatting error clarification
   - Impact type: None (informational only)
   - Integration action: Acknowledge; no proposal content changes required
4. Mark as low impact (acknowledgment only)

**Source:** Addendum 02, page 1

**Verification:** Confirm this is the only item in Addendum 02.

---

### Step 7: Extract Addendum 03 Changes

**Action:**
1. Open Addendum 03 (5 pages), dated July 31, 2024
2. Extract all 21 items (sections 1.1 through 1.21):
   - **1.1:** 12-acre developable site (20 acres total; 8 acres dog park/storm pond in flood fringe)
   - **1.2:** Pickled sand storage building REMOVED from scope
   - **1.3:** Main building flooring: sealed concrete preferred
   - **1.4:** Functional program colors identify Fire, Public Works, and shared spaces
   - **1.5:** Second story acceptable for some program spaces
   - **1.6:** Services location confirmed (water/wastewater stubbed; elec/comm/gas nearby)
   - **1.7:** Cash allowance ALLOWED for service tie-ins (NOT required in base proposal price)
   - **1.8:** All bays require sumps
   - **1.9:** Wash bay as additional optional item
   - **1.10:** Overhead door height: 16 feet minimum
   - **1.11:** Public works bays: adequate ventilation (NOT dedicated welding ventilation)
   - **1.12:** Fire apparatus bays: direct exhaust ventilation required (2 apparatus per bay)
   - **1.13:** Bunker gear lockers: 40 required
   - **1.14:** Bunker gear locker room: room ventilation required
   - **1.15:** Backup generator REQUIRED (kitchen, meeting room/ICP, 2 bathrooms minimum)
   - **1.16:** Water fill stations REQUIRED (1 in fire bay, 1 in PW bay; 2" minimum; ground level)
   - **1.17:** Solar-capable roofing REQUIRED (flat, south, west, or southwest orientation)
   - **1.18:** FF&E as additional item (NOT in base costs)
   - **1.19:** No supplier preference for security/cameras
   - **1.20:** Survey files provided AFTER award
   - **1.21:** Sample room size ranges provided (table with 10 room types)

3. For EACH item, record in addenda checklist:
   - Impact type (Design, Pricing, Narrative, Schedule, or Informational)
   - Affected deliverable(s) (using DEL-ID references from Decomposition)
   - Integration action required
   - Status (to be tracked during proposal development)

4. Prioritize high-impact items:
   - **CRITICAL:** Items 1.2 (scope removal), 1.7 (pricing allowance), 1.8, 1.10, 1.12, 1.15, 1.16, 1.17 (design requirements affecting concept and cost)
   - **IMPORTANT:** Items 1.1, 1.3, 1.11, 1.13, 1.14, 1.18, 1.21 (design guidance and pricing structure)
   - **INFORMATIONAL:** Items 1.4, 1.5, 1.6, 1.9, 1.19, 1.20 (clarifications, confirmations, options)

**Source:** Addendum 03, pages 1-5; Specification.md REQ-05

**Verification:** Confirm all 21 items from Addendum 03 are captured (sections 1.1 through 1.21).

---

### Step 7.1: Verify Extraction Completeness (B-003, C-002)

**Action:**
1. After completing Steps 1-7, count extracted requirements against RFP Table of Contents (pages 2-3)
2. Document count reconciliation:
   - Section 6: Expected 1 subsection; Extracted: ____
   - Section 7: Expected 22 subsections; Extracted: ____
   - Section 8: Expected 6 evaluation criteria; Extracted: ____
   - Section 9: Expected 22 subsections; Extracted: ____
   - Addendum 01: Expected 2 items; Extracted: ____
   - Addendum 02: Expected 1 item; Extracted: ____
   - Addendum 03: Expected 21 items; Extracted: ____

3. If any count mismatch found, investigate and resolve before proceeding to Step 8
4. Record reconciliation results in Extraction Log

**Purpose:** Ensure 100% extraction completeness before proceeding to mapping.

*Source: _SEMANTIC_LENSING.md, ItemID B-003 (adequate evidence lens), C-002 (compulsory compliance assurance lens)*

---

### Step 8: Map Requirements to Deliverables

**Action:**
1. For each RFP requirement extracted in Steps 1-4, identify the responsible proposal deliverable(s) using:
   - Decomposition Section 10 (Scope Ledger) - maps SOW items to DEL-IDs
   - Decomposition Section 8 (Deliverables) - defines each DEL-ID output and acceptance criteria
   - Decomposition Section 15 (Evaluation Criteria Crosswalk) - maps evaluation categories to deliverables
2. Record deliverable mapping in compliance matrix "Proposal Section Reference" column (use DEL-ID format initially; convert to section names/numbers during proposal assembly)
3. Flag any requirements with no clear deliverable mapping as **GAP - NEEDS OWNER ASSIGNMENT**

**Source:** Decomposition Sections 8, 10, 15; Specification.md REQ-02 (Section 7 requirements table)

**Verification:**
- Every RFP requirement has at least one mapped deliverable
- No deliverable is mapped to requirements outside its defined scope
- Cross-check against Decomposition Section 11 (Coverage & Telemetry) showing 100% SOW coverage

---

### Step 9: Identify and Flag Pass/Fail Risks

**Action:**
1. Review all mandatory requirements (primarily Section 6, plus format/submission requirements from Sections 4-5)
2. For each mandatory requirement, assess:
   - **Disqualification risk if missing:** HIGH, MEDIUM, or LOW
   - **Current mitigation status:** What is being done to ensure compliance?
   - **Owner assignment:** Who is responsible for ensuring this requirement is met?
   - **Resolution path:** What are the specific steps to close this risk?
3. Create Pass/Fail Risk Register (can be embedded in compliance matrix or separate table)
4. Prioritize HIGH risk items for Proposal Manager review and tracking:
   - Letter of Offer (Appendix G) execution
   - Agreement to Bond inclusion
   - Addenda acknowledgment in Appendix H
   - Appendix H (Schedule A + B) completion
   - Appendix I (Subtrade List) completion
   - Proposal format compliance (PDF, <15 MB, correct section order)
   - Submission deadline compliance (Aug 30, 2024 @ 2:00 PM MST)

**Source:** Specification.md REQ-10 (Pass/Fail Risk Register); Datasheet.md (Conditions - Pass/Fail Compliance Gates); Decomposition Section 3 (Hard Constraints C-01 through C-07)

**Verification:**
- All items identified in Specification.md REQ-10 table are in risk register
- Each HIGH risk item has assigned owner and documented resolution path
- Risk register reviewed with Proposal Manager

---

### Step 10: Build Addenda Integration Checklist

**Action:**
1. Using extractions from Steps 5-7 (Addendum 01, 02, 03), populate addenda checklist table
2. For each addendum item:
   - Classify impact type:
     - **Design:** Affects concept, drawings, design brief, specifications
     - **Pricing:** Affects cost estimates, Appendix H schedules, assumptions
     - **Narrative:** Affects written responses, methodologies, plans
     - **Schedule:** Affects timeline, milestones, critical path
     - **Informational:** Acknowledgment only; no proposal changes
   - Identify affected deliverable(s) by DEL-ID
   - Document integration action required (what specifically must be done)
   - Initialize status as "Pending" (to be updated during proposal development)
3. Sort checklist by:
   - Primary sort: Impact type (Design, Pricing, Narrative, Schedule, Informational)
   - Secondary sort: Addendum number (01, 02, 03)
4. Highlight CRITICAL integration items (Addendum 03 items 1.2, 1.7, 1.8, 1.10, 1.12, 1.15, 1.16, 1.17)

**Source:** Addendum 01, 02, 03; Specification.md REQ-05; Guidance.md (Example 3 - Addenda Checklist Row)

**Verification:**
- All 2 items from Addendum 01 tracked
- 1 item from Addendum 02 tracked
- All 21 items from Addendum 03 tracked
- Total: 24 addendum items tracked
- Each item has identified affected deliverable(s)

---

### Step 11: Verify Addenda Acknowledgment Requirement

**Action:**
1. Open Appendix H (Financial Proposal), page 57, Schedule A
2. Locate addenda acknowledgment section: "The Proponent acknowledges that they have received the following Addenda and have accounted for their contents in their Total Stipulated Price above: Addenda ______ to ______"
3. Prepare completion instruction for Estimator: "Complete this line as: 'Addenda 01 to 03'"
4. Add to Pass/Fail Risk Register:
   - Risk Item: Addenda not acknowledged in Appendix H
   - Impact: Price proposal disqualification
   - Owner: Estimator / Proposal Manager
   - Resolution: Verify "Addenda 01 to 03" listed in Schedule A before final submission
5. Cross-reference addenda checklist to ensure all addendum changes have been integrated before acknowledgment completed (acknowledgment implies integration)

**Source:** Appendix H Schedule A, page 57; RFP Section 2.9, page 11

**Verification:** Confirm acknowledgment section exists in Appendix H template; confirm warning text: "Failure to acknowledge receipt and inclusion of all addenda may result in this Price Proposal being disqualified."

---

### Step 12: Cross-Reference with Decomposition Scope Ledger

**Action:**
1. Open Decomposition Document, Section 10 (Scope Ledger), scope items SOW-001 through SOW-028
2. For each SOW item, verify:
   - SOW item maps to at least one deliverable (DeliverableID column)
   - SOW item maps to at least one RFP requirement (SourceRef column)
3. Cross-check compliance matrix RFP requirements against Scope Ledger SourceRef column
4. Identify any mismatches:
   - RFP requirement in compliance matrix but not in Scope Ledger SourceRef
   - Scope Ledger SourceRef not captured in compliance matrix
5. If mismatches found, investigate using the following decision logic (D-002):
   - **Step 12a:** For each mismatch, determine: Is this a deliberate abstraction level difference (SOW item is parent of multiple RFP subsections)?
     - If YES: Document rationale and accept the mapping
     - If NO: Escalate as coverage gap requiring resolution
   - Is this a gap in the compliance matrix? (add requirement)
   - Is this a scope ledger interpretation difference? (document as note)

*Source: _SEMANTIC_LENSING.md, ItemID D-002 (evidence-based process governance lens)*

**Source:** Decomposition Section 10 (Scope Ledger); Decomposition Section 11 (Coverage & Telemetry showing 100% coverage)

**Verification:**
- All SOW items have RFP source references
- All RFP Section 6-9 requirements have corresponding SOW items (or are acknowledged as general terms not requiring specific deliverables)

**ASSUMPTION:** Scope Ledger may be at higher level of abstraction (SOW items) vs. compliance matrix (subsection level); perfect one-to-one mapping not expected, but major gaps should be investigated.

---

### Step 13: Populate Proposal Section References (Iterative)

**Action:**
1. **Initial Population (during proposal planning):** Use deliverable IDs (DEL-XX-XX format) as placeholders in "Proposal Section Reference" column
2. **Mid-Proposal Update (once proposal outline finalized):** Replace DEL-IDs with proposal section names/numbers (e.g., "Section 3.2 - Design Methodology")
3. **Final Population (during PDF assembly):** Add page number references in "Proposal Page(s)" column
4. Coordinate with DEL-01-02 (Formal Submission Package) owner to ensure page references are accurate in final PDF

**Source:** Specification.md REQ-01 through REQ-04 (mapping requirements to proposal sections/pages)

**Verification:**
- No "TBD" or blank entries in "Proposal Section Reference" column by final review milestone
- Page references added before final submission
- Cross-check page references against actual final PDF

**Note:** This step is iterative and spans the entire proposal development timeline.

**Conversion Method (B-008):** To convert DEL-ID to final section number:
1. For each DEL-ID in compliance matrix, consult Proposal Manager for final proposal section assignment
2. Record in "Proposal Section Reference" column using format: "Section X.X - [Title]"
3. If DEL-ID maps to multiple proposal sections, list all applicable sections

*Source: _SEMANTIC_LENSING.md, ItemID B-008 (satisfactory explanation lens)*

---

### Step 14: Mandatory Review and Sign-Off (X-002)

**IMPORTANT:** This step uses mandatory language. Proposal Manager SHALL PERFORM the following verification activities before allowing proposal assembly to proceed. This is not optional.

**Action:**
1. **Internal Review (Proposal Manager) - MANDATORY:**
   - SHALL verify 100% coverage of RFP Sections 6-9
   - SHALL verify all pass/fail risks flagged and assigned
   - SHALL verify addenda checklist complete (all 24 items tracked)
   - SHALL verify addenda acknowledgment in Appendix H flagged as required action

2. **Cross-Functional Review (Recommended):**
   - Share compliance matrix with deliverable owners (leads for PKG-01 through PKG-09)
   - Ask each lead to confirm their assigned requirements are correctly mapped
   - Collect feedback and resolve any discrepancies

3. **Final Sign-Off (Proposal Manager) - MANDATORY:**
   - SHALL mark compliance matrix as "VERIFIED - READY FOR PROPOSAL ASSEMBLY"
   - SHALL communicate any remaining HIGH risk items to proposal leadership
   - SHALL hand off to DEL-01-02 (Formal Submission Package) for final PDF assembly coordination
   - Proposal assembly SHALL NOT commence until Proposal Manager signs off on compliance matrix completion

*Source: _SEMANTIC_LENSING.md, ItemID X-002 (practiced compliance verification lens), A-003 (mandatory practice lens)*

**Source:** _CONTEXT.md (Acceptance Criteria: "100% mandatory items accounted for; pass/fail risks flagged with owner & resolution path")

**Verification:**
- Proposal Manager formal sign-off documented (email, meeting minutes, or matrix status field)
- All HIGH risk items have documented resolution status
- No unresolved gaps or missing mappings

---

### Step 15: Dispute Resolution (X-003)

**Action:**
If deliverable owners dispute a compliance mapping (e.g., one owner says "our section addresses RFP 7.1.1" but another says "it addresses 7.1.2"):

1. **Identify Dispute:** Record the disputed requirement and the conflicting interpretations
2. **Gather Evidence:** Request source references from each party (which proposal section addresses which RFP requirement?)
3. **Adjudicate:** Proposal Manager SHALL adjudicate the dispute based on:
   - RFP requirement text (authoritative)
   - Deliverable scope definitions (from Decomposition)
   - Proposal structure and organization
4. **Document Decision:** Record decision with rationale in the compliance matrix Notes column
5. **Communicate:** Notify affected deliverable owners of the ruling

*Source: _SEMANTIC_LENSING.md, ItemID X-003 (adjudicated compliance foundation lens)*

---

### Step 16: Verify Compliance Truth-Testing (A-007)

**Action:**
After initial matrix population (Steps 8-14), perform compliance truth-testing to confirm each mapped deliverable truly addresses its mapped requirement(s):

1. **For each HIGH-value requirement (top 5 by evaluation points):**
   - Read the actual deliverable content (draft or outline)
   - Confirm it substantively addresses the mapped RFP requirement
   - If content does not address requirement, flag as "CONTENT GAP" for deliverable owner

2. **For MANDATORY requirements:**
   - Verify not just presence but completeness (e.g., Appendix G not just present but fully completed)
   - Verify execution requirements (signatures, seals) have been addressed or flagged

3. **Record Results:** Update compliance matrix status from "Mapped" to "Verified" for each truth-tested item

**Purpose:** The "executed action" lens reveals that procedures describe setup and population but not the act of verifying compliance for real. This step closes that gap.

*Source: _SEMANTIC_LENSING.md, ItemID A-007 (executed action lens)*

---

### Step 17: Maintain During Proposal Development

**Action:**
1. **Establish Update Cadence:**
   - **ASSUMPTION:** Recommended: Update compliance matrix status weekly during active proposal development
   - Update addenda checklist integration status as deliverables are drafted/revised
   - Update risk register as risks are mitigated

2. **Trigger Updates:**
   - Whenever a deliverable is marked complete, update corresponding compliance matrix rows to "Complete"
   - Whenever an addendum item is integrated, update addenda checklist to "Integrated"
   - Whenever a risk is mitigated, update risk register status

3. **Milestone Reviews:**
   - **50% Draft Milestone:** Review matrix; identify any requirements not yet addressed; flag for owners
   - **90% Draft Milestone:** Review matrix; verify all "Pending" or "In Progress" items have clear completion plans
   - **Final Review Milestone (pre-submission):** Verify 100% "Complete" status; no open gaps

**Source:** Guidance.md Principle 5 (Living Document During Proposal Development); proposal management best practices

**Verification:**
- Matrix status reflects current reality (not stale)
- Any "Not Started" or "Pending" items at late milestones are escalated to Proposal Manager
- Final verification confirms 100% complete status before submission

---

## Verification

### Verification Checkpoint 0: Requirement Extraction Inventory Reconciliation (C-002)

**Check:** Confirm that all 46 RFP requirements (Sections 6-9) have been extracted and the extraction is complete per RFP Table of Contents.

**Method:**
1. Count all extracted requirements from Steps 1-4
2. Compare against RFP TOC (pages 2-3)
3. Document reconciliation in Extraction Log

**Acceptance:** All requirements accounted for; count matches expected values.

**Responsible Role:** Proposal Manager or designated extractor
**Timing:** Before Step 8 commences

*Source: _SEMANTIC_LENSING.md, ItemID C-002 (compulsory compliance assurance lens)*

---

### Verification Checkpoint 1: Requirement Extraction Completeness

**Check:**
- Section 6: 1 subsection (6.1) captured
- Section 7: 22 subsections (7.1, 7.1.1-7.1.9, 7.2, 7.3, 7.3.1-7.3.7, 7.4, 7.5, 7.6) captured
- Section 8: 6 evaluation criteria from scoring matrix captured
- Section 9: 22 subsections (9.1-9.22) captured
- Addendum 01: 2 items captured
- Addendum 02: 1 item captured
- Addendum 03: 21 items captured

**Method:** Compare extracted count against RFP Table of Contents and addenda page counts.

**Acceptance:** All subsections/items accounted for; no gaps in sequence numbering.

**Responsible Role:** Proposal Manager
**Timing:** After Step 7.1, before Step 8
**Verification Method:** Filter matrix for blank cells; count against RFP Table of Contents

*Source: _SEMANTIC_LENSING.md, ItemID E-002 (operationally governed verification lens)*

---

### Verification Checkpoint 2: 100% Requirement Coverage

**Check:**
- Every row in compliance matrix has a "Proposal Section Reference" value (not blank or "N/A")
- Every mandatory requirement (Section 6 + format/execution requirements) has "Compliance Status" = "Complete" before submission

**Method:** Filter compliance matrix for blank/null "Proposal Section Reference" cells; investigate and resolve any found.

**Acceptance:** Zero gaps; 100% of requirements mapped to proposal responses.

**Source:** _CONTEXT.md (Acceptance Criteria: "100% mandatory items accounted for")

---

### Verification Checkpoint 3: Addenda Integration Completeness

**Check:**
- All 24 addendum items (2 from Add 01, 1 from Add 02, 21 from Add 03) have "Integration Status" = "Complete"
- Addenda acknowledgment in Appendix H is marked "Complete"

**Method:** Filter addenda checklist for "Pending" or "In Progress" status; resolve any remaining before final submission.

**Acceptance:** All addendum changes integrated; acknowledgment completed.

**Source:** Specification.md REQ-05; Appendix H Schedule A requirement

---

### Verification Checkpoint 4: Pass/Fail Risk Mitigation

**Check:**
- All HIGH risk items in risk register have "Status" = "Mitigated" or "Resolved"
- Resolution paths documented and executed

**Method:** Review risk register; confirm actions completed for each HIGH risk item.

**Acceptance:** No open HIGH risks; any remaining risks documented with explicit acceptance from Proposal Manager.

**Source:** _CONTEXT.md (Acceptance Criteria: "pass/fail risks flagged with owner & resolution path"); Specification.md REQ-10

---

### Verification Checkpoint 5: Cross-Deliverable Consistency

**Check:**
- Compliance matrix deliverable mappings match Decomposition Section 10 (Scope Ledger) DeliverableID mappings
- No requirement is assigned to a deliverable outside its defined scope

**Method:** Compare compliance matrix "Proposal Section Reference" (deliverable assignments) against Decomposition Scope Ledger for consistency.

**Acceptance:** No conflicts; all mappings defensible based on deliverable definitions.

**Source:** Decomposition Sections 8 (Deliverables), 10 (Scope Ledger); AGENT_4_DOCUMENTS protocol requirement for cross-document consistency

---

## Records

### Record 1: Compliance Matrix (Final Version)

**Format:** Excel workbook (columns specified in Specification) - Excel preferred for sorting/filtering

**Content:**
- All RFP Sections 6-9 requirements mapped to proposal responses
- Mandatory items flagged
- Evaluation point values noted
- Proposal section and page references populated
- Status tracking (complete/pending)
- Risk flags

**Storage Location:** **TBD** - Proposal Manager to designate

**Retention:**
- Working version maintained during proposal development
- Final version archived with proposal submission package
- Retention period: Project duration plus contractual warranty period
- **TBD:** Confirm whether final compliance matrix is included in submitted proposal PDF or kept as internal record only

**Owner:** Proposal Manager

*Source: Specification.md (Documentation section - Required Artifacts); _CONTEXT.md (Anticipated Artifacts); _SEMANTIC_LENSING.md, ItemID F-004 (exhaustive process documentation lens)*

---

### Record 2: Addenda Integration Checklist (Final Version)

**Format:** Excel workbook or structured table

**Content:**
- All changes from Addendum 01, 02, 03
- Impact type and affected deliverables
- Integration status
- Proposal section references where changes are addressed
- Acknowledgment status (confirmed in Appendix H)

**Retention:**
- Working version maintained during proposal development
- Final version archived with proposal submission package
- **TBD:** Confirm whether addenda checklist is included in submitted proposal or internal only

**Owner:** Proposal Manager

**Source:** Specification.md (Documentation section - Required Artifacts); Decomposition Section 4 (Addenda Integration Summary)

---

### Record 3: Pass/Fail Risk Register (Final Version)

**Format:** Table (can be embedded in compliance matrix or separate)

**Content:**
- High-risk mandatory requirements
- Disqualification consequences if missed
- Assigned owners
- Resolution paths
- Final status (mitigated/resolved)

**Retention:**
- Updated throughout proposal development
- Final version shows all risks mitigated before submission
- Archived as part of proposal development record

**Owner:** Proposal Manager

**Source:** Specification.md REQ-10; _CONTEXT.md (Acceptance Criteria)

---

### Record 4: Compliance Review Meeting Notes (Optional but Recommended)

**Format:** Meeting minutes or email summaries

**Content:**
- Dates of compliance reviews (e.g., 50% draft, 90% draft, final review)
- Attendees
- Gaps identified and assignments to resolve
- Decisions made (e.g., whether to include Intent to Propose, whether to include compliance matrix in submitted proposal)
- Sign-off confirmations

**Retention:** Archived with proposal project files

**Owner:** Proposal Manager

**ASSUMPTION:** Best practice for proposal governance; not explicitly required but supports "owner & resolution path" acceptance criterion

---

## Acceptance Criteria

### Acceptance Criterion 1: 100% Coverage Verified

**Criterion:** All requirements from RFP Sections 6, 7, 8, 9 are mapped to proposal response locations with no gaps.

**Verification Method:** Compliance matrix filter/sort showing zero blank "Proposal Section Reference" cells.

**Sign-Off:** Proposal Manager confirms 100% coverage before final submission.

**Source:** _CONTEXT.md (Acceptance Criteria)

---

### Acceptance Criterion 2: All Addenda Integrated and Acknowledged

**Criterion:**
- All 24 addendum items (from Addendum 01, 02, 03) tracked in checklist
- All integration actions completed
- Addenda acknowledged in Appendix H Schedule A

**Verification Method:**
- Addenda checklist shows 100% "Integration Status" = "Complete"
- Appendix H Schedule A includes text: "Addenda 01 to 03" (or equivalent)

**Sign-Off:** Proposal Manager and Estimator confirm addenda acknowledgment completed.

**Source:** _CONTEXT.md (Acceptance Criteria); Specification.md REQ-05, REQ-09

---

### Acceptance Criterion 3: Pass/Fail Risks Flagged with Owners and Resolution Paths

**Criterion:** All high-risk mandatory requirements identified in risk register with:
- Clear statement of disqualification/rejection consequence
- Assigned owner (role/person responsible)
- Documented resolution path (steps to mitigate/close risk)
- Status tracked to resolution

**Verification Method:** Risk register review showing all HIGH risks have assigned owner and resolution path.

**Sign-Off:** Proposal Manager confirms all critical risks mitigated before submission.

**Source:** _CONTEXT.md (Acceptance Criteria: "pass/fail risks flagged with owner & resolution path")

---

### Acceptance Criterion 4: Cross-Deliverable Mapping Consistency

**Criterion:** Deliverable assignments in compliance matrix are consistent with Decomposition Scope Ledger (Section 10) and Deliverable definitions (Section 8).

**Verification Method:** Spot-check 10-20% of compliance matrix rows against Decomposition mappings; investigate and resolve any discrepancies.

**Sign-Off:** Proposal Manager confirms mappings are defensible and consistent.

**Source:** AGENT_4_DOCUMENTS protocol requirement for cross-document consistency; Decomposition as authoritative source for deliverable scope

---

### Acceptance Criterion 5: Final Compliance Matrix Reflects Final Proposal

**Criterion:** Proposal section references and page numbers in compliance matrix accurately reflect the final submitted proposal PDF.

**Verification Method:** Sample-check 10-20 compliance matrix entries against final PDF; verify section names and page numbers are correct.

**Sign-Off:** Proposal Manager confirms matrix matches final submission.

**Source:** Specification.md REQ-01 through REQ-04 (requirement mapping to proposal sections/pages)

**Note:** This verification occurs post-assembly, during final QA before submission.

---

**Document Status:** SEMANTIC LENSING ENRICHED (Pass 3)
**Last Updated:** 2026-02-04
**Agent:** 4_DOCUMENTS (Type 2 Specialist)
**Enrichment Source:** _SEMANTIC_LENSING.md - Items incorporated: A-003, A-007, B-003, B-008, C-002, C-004, D-002, D-003, E-002, F-003, F-004, X-002, X-003
