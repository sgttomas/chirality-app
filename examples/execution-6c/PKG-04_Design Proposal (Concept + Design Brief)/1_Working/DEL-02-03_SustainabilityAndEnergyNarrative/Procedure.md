# Procedure: DEL-02-03 SustainabilityAndEnergyNarrative

## Purpose

This procedure describes the process for **producing** the Sustainability and Energy Narrative deliverable for the Penhold Public Services Building Design-Build proposal response.

**What this procedure accomplishes:**
- Generation of a credible, code-aware energy efficiency and sustainability narrative
- Documentation of solar-ready provisions approach (Addendum 03 requirement)
- Integration of the narrative into the Design Brief section of the proposal (Section 7.1)
- Verification of alignment with concept design, design brief, and site conditions deliverables
- Quality assurance and compliance checking before proposal submission

**Audience for this procedure:**
- Lead Architect / Designer (narrative author)
- Sustainability Specialist / Energy Consultant (technical reviewer)
- Proposal Manager (coordination and compliance verification)
- Building Code Consultant (code compliance verification)

**Source:** _CONTEXT.md (Responsible: Lead Architect / Designer); Decomposition §8 (DEL-02-03 definition)

---

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED (per _DEPENDENCIES.md)

Dependencies are coordinated externally by humans (see `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Coordination/_COORDINATION.md`).

**Upstream deliverables (informative — not enforced by this agent):**
- **DEL-02-01 (Concept Design Package):** Provides building orientation, massing, roof configuration, and site layout context required for solar-ready strategy and energy narrative alignment
- **DEL-02-02 (Design Brief Narrative):** Provides materials, durability, and maintenance context; sustainability narrative must align and avoid duplication

**Note:** While dependencies are not tracked in this deliverable folder, the narrative author should coordinate with DEL-02-01 and DEL-02-02 authors to ensure consistency. Proceed with narrative production based on available information; flag any missing inputs as **TBD** in the narrative.

**Source:** _DEPENDENCIES.md; Decomposition §8 (PKG-04 deliverables)

### Reference Materials Required

The following reference materials must be available before beginning narrative production:

| Reference | Location | Purpose |
|-----------|----------|---------|
| **RFP Document** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf` | Section 7.1 (Design Brief requirements); Appendix A (OSR — energy/sustainability requirements); Appendix B (Functional Program — space/equipment loads) |
| **Addendum 01** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold_Public Services Building Addendum01.pdf` | Room dimension flexibility clarification |
| **Addendum 03** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf` | Solar-ready requirement; technical clarifications (doors, sumps, exhaust, generator); site clarifications |
| **Decomposition Document** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` | Deliverable definition, objectives, scope, evaluation criteria |
| **Site Grading** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold PSB_Site grading.pdf` | Site orientation, grading context for solar exposure and stormwater |
| **Flood Zone Mapping** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold PSB_parcel flood zone.pdf` | Flood fringe constraints; stormwater management context |
| **Geotechnical Report** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold PSB_Geotechnical Investigation Report.pdf` | Foundation design context (affects thermal envelope — slab insulation, below-grade walls) |
| **Wetland Assessment** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold PSB_Wetland Assessment.pdf` | Site environmental constraints; stormwater/water efficiency context |

**Availability confirmation:**
All reference materials are listed in `_REFERENCES.md` and are accessible in the `_Sources/` directory.

**If a reference is not accessible:** Mark the affected narrative content as **TBD** with a note indicating the missing reference (e.g., "**TBD:** Energy performance targets pending access to RFP Appendix A (OSR) Section X"). Do not guess or invent requirements.

**Source:** _REFERENCES.md

### Tools and Resources

| Tool/Resource | Purpose |
|---------------|---------|
| **Markdown editor** | Draft narrative in Markdown format (for version control and easy conversion to PDF) |
| **PDF reader** | Access reference materials (RFP, addenda, site reports) |
| **Code references** | Alberta Building Code (ABC), National Energy Code of Canada for Buildings (NECB) — online or print copies for verification |
| **Energy calculator (optional)** | Simple calculations for estimated savings, payback, EUI (e.g., spreadsheet or online tool) — for illustrative purposes only; not detailed energy model |
| **Diagram tool (optional)** | Create simple diagrams if beneficial (e.g., zoning schematic, solar-ready roof plan) — must be file-size optimized for 15 MB PDF limit |

**Source:** ASSUMPTION (typical tools for narrative document production)

### Skills and Knowledge Required

The narrative author should have:
- Understanding of building energy systems (envelope, HVAC, electrical, controls)
- Familiarity with Alberta Building Code (ABC) and National Energy Code of Canada for Buildings (NECB)
- Knowledge of solar-ready design principles (structural, electrical, orientation)
- Understanding of municipal building operations and life-cycle cost considerations
- Proposal writing skills (clear, persuasive, technically credible communication)

**If specialized expertise is needed** (e.g., detailed code interpretation, solar system sizing), coordinate with Sustainability Specialist, Building Code Consultant, or Electrical Engineer.

**Source:** ASSUMPTION (skills appropriate for deliverable scope)

---

## Steps

### Step 1: Review Context and Requirements

**Objective:** Understand the deliverable scope, acceptance criteria, and evaluation context before drafting narrative.

**Actions:**

1.1. **Read `_CONTEXT.md`:**
   - Confirm deliverable ID, name, package, discipline, responsible party
   - Review description: "Energy efficiency + sustainability narrative; solar-ready provisions approach"
   - Review acceptance criteria: "Credible, code-aware; aligns with 'solar capable roofing' requirement"
   - Note scope traceability: SOW-012, OBJ-004

1.2. **Read Decomposition Document (relevant sections):**
   - Section §1: Intake Summary (project context, submission deadline)
   - Section §4: Addendum 03 impacts (solar-ready requirement, technical clarifications)
   - Section §6: Objectives (OBJ-004 — Deliver strong Design Brief)
   - Section §8: DEL-02-03 definition
   - Section §9: SOW-012 (Provide energy efficiency and sustainability approach narrative including solar-ready considerations)
   - Section §15: Evaluation Criteria (Design Brief — 5 points; Durability/Maintenance — 15 points)

1.3. **Read `Specification.md` (this deliverable):**
   - Review all requirements (REQ-001 through REQ-008)
   - Note mandatory vs. recommended content ("shall" vs. "should")
   - Identify any **TBD** items that require follow-up

1.4. **Read `Guidance.md` (this deliverable):**
   - Understand principles, considerations, trade-offs, and examples
   - Identify key themes to emphasize (solar-ready, dual-function zoning, durability, life-cycle value)

**Deliverable:** Internal understanding of deliverable scope and requirements; notes on key themes and mandatory content.

**Verification:** Check that you can answer: "What is the purpose of this narrative? What must it include? How will it be evaluated?"

**Source:** AGENT_4_DOCUMENTS.md (Step 1 — Read Context); _CONTEXT.md; Decomposition document; `Specification.md`; `Guidance.md`

---

### Step 2: Extract Requirements from RFP and Addenda

**Objective:** Identify specific energy and sustainability requirements from the RFP Appendix A (OSR), Appendix B (Functional Program), Section 7.1 (Design Brief requirements), and Addenda.

**Actions:**

2.1. **Review RFP Appendix A (Owner Statement of Requirements — OSR):**
   - Search for energy performance targets (e.g., EUI, energy efficiency rating, renewable energy goals)
   - Search for sustainability requirements (e.g., LEED certification, green building standards, water efficiency targets)
   - Search for specific system requirements (e.g., HVAC type, insulation values, glazing specifications)
   - Note any requirements as **direct quotes** with section references for traceability

2.2. **Review RFP Appendix B (Functional Program):**
   - Identify spaces with high energy loads (apparatus bays, workshops, server rooms, kitchens)
   - Identify equipment loads that affect HVAC sizing (computers, kitchen appliances, specialty equipment)
   - Note any space-specific requirements (e.g., temperature/humidity control for specific rooms)

2.3. **Review RFP Section 7.1 (Design Brief Requirements):**
   - Identify required narrative topics and structure (headings, content expectations)
   - Note evaluation criteria language (what evaluators are looking for)
   - Identify any mandatory statements or commitments required in the narrative

2.4. **Review Addendum 03 (Solar-Ready and Technical Clarifications):**
   - Confirm "solar capable roofing" requirement language
   - Note technical clarifications: 16-ft overhead doors, bay sumps, fire apparatus exhaust, generator (supports ICP), fill stations
   - Note site clarifications: 12-acre developable area, pickled sand building removed

2.5. **Document extracted requirements in a checklist:**
   - Create a simple checklist (spreadsheet or Markdown table) mapping each requirement to its source (RFP section, addendum, page number)
   - Mark mandatory requirements ("shall") vs. recommended ("should")
   - Flag any ambiguous or conflicting requirements for clarification

**Deliverable:** Requirements checklist (internal working document; not for submission) with all energy/sustainability requirements extracted and source-referenced.

**Verification:** Cross-check checklist against `Specification.md` REQ-001 through REQ-008; all mandatory requirements should be captured.

**Source:** ASSUMPTION (standard requirements extraction process for proposal response)

**Note:** If RFP Appendix A or Section 7.1 cannot be accessed (e.g., PDF extraction issues), proceed using the requirements defined in `Specification.md` (which were generated based on typical Design Brief requirements and available decomposition information). Mark specific performance targets or detailed requirements as **TBD** with a note indicating missing RFP access.

---

### Step 3: Coordinate with Related Deliverables

**Objective:** Ensure sustainability narrative aligns with and does not duplicate content from related deliverables (Concept Design, Design Brief, Site Conditions).

**Actions:**

3.1. **Review DEL-02-01 (Concept Design Package) if available:**
   - Identify building orientation, massing, roof configuration (affects solar-ready strategy)
   - Identify site layout, parking, access (affects energy narrative site context)
   - Note any design features relevant to energy (e.g., daylighting strategy, thermal mass, natural ventilation)
   - If DEL-02-01 is not yet complete, proceed with narrative using **ASSUMPTION** labels and coordinate later

3.2. **Review DEL-02-02 (Design Brief Narrative) if available:**
   - Identify materials and durability content (avoid duplicating in energy narrative)
   - Identify operational workflow and maintenance content (coordinate with operational sustainability section)
   - Note any sustainability themes already addressed (avoid redundancy)
   - If DEL-02-02 is not yet complete, define clear boundary: DEL-02-02 covers **materials/construction/operations**, DEL-02-03 covers **energy systems/sustainability strategy**

3.3. **Review DEL-09-02 (Site Conditions Summary) if available:**
   - Identify site constraints relevant to energy/sustainability (flood fringe, wetlands, grading)
   - Note stormwater management approach (coordinate with water efficiency section)
   - If DEL-09-02 is not yet complete, extract relevant information from site reference reports (Site Grading, Flood Zone, Wetland Assessment)

3.4. **Identify cross-reference points:**
   - Where energy narrative refers to concept design features, use cross-reference language (e.g., "As shown in Concept Design, the building is oriented with south-facing roof slope to optimize solar potential...")
   - Where energy narrative touches on durability/maintenance, cross-reference DEL-02-02 (e.g., "Materials durability is addressed in Design Brief Narrative; energy implications of durable systems are discussed here...")

**Deliverable:** Cross-reference notes (internal working document) identifying alignment points and boundaries between deliverables.

**Verification:** Confirm that sustainability narrative does not duplicate content from other deliverables and that cross-references are noted for later inclusion in draft.

**Boundary Clarification (per Lensing C-005):**
- Confirm that operational discipline for BAS scheduling/seasonal adjustment is documented in commissioning/training plan (DEL-06-01) or Town operational manual scope
- Narrative describes strategy; long-term success depends on human discipline
- **Responsibility assignment:** Narrative describes what BAS can do; DEL-06-01 describes how Town staff will be trained to use it

**Source:** AGENT_4_DOCUMENTS.md (Step 5 — Cross-Reference Consistency Check protocol); Guidance.md (Consideration 5 — Avoid Duplication); Lensing C-005 (operational discipline documentation)

---

### Step 4: Draft Narrative Content

**Objective:** Produce the first draft of the Sustainability and Energy Narrative, addressing all mandatory requirements and incorporating key themes from Guidance.

**Actions:**

4.1. **Establish narrative structure:**

   Based on `Specification.md` requirements and `Guidance.md` principles, organize narrative into the following sections (adjust as needed to match RFP Section 7.1 structure if specified):

   - **Introduction:** Project context, sustainability goals, alignment with Town's objectives
   - **Building Envelope:** Thermal performance, insulation strategy, air tightness, overhead doors
   - **Mechanical Systems:** HVAC efficiency, zoning strategy (dual-function building), heat recovery, controls
   - **Electrical Systems:** Lighting efficiency, daylighting, plug load management
   - **Solar-Ready Provisions:** Structural capacity, electrical rough-in, roof orientation, future value
   - **Water Efficiency:** Plumbing fixtures, bay sumps, stormwater coordination
   - **Materials & Indoor Environment:** Low-emission materials, indoor air quality, daylighting (coordinate with DEL-02-02)
   - **Operational Sustainability:** Life-cycle considerations, maintenance, commissioning approach
   - **Emergency Systems:** Generator efficiency, integration with building energy management
   - **Performance Targets & Verification:** Code compliance, anticipated EUI, energy modeling and commissioning approach
   - **Conclusion:** Summary of key sustainability commitments and value proposition

4.2. **Draft each section:**

   For each section:
   - Address relevant requirements from `Specification.md` (check off requirements as addressed)
   - Apply principles and considerations from `Guidance.md`
   - Use specific technical strategies and terminology (avoid generic statements)
   - Cite codes, standards, and reference materials where applicable
   - Use examples from `Guidance.md` as templates (adapt to project specifics)
   - Maintain proposal-appropriate level of detail (conceptual; not detailed design)
   - Use clear, persuasive language suitable for municipal evaluators

   **Special focus areas (mandatory):**
   - **Solar-Ready Provisions (REQ-003):** This is an Addendum 03 requirement and must be addressed comprehensively. Use `Guidance.md` Example 1 as a template. Address structural, electrical, orientation, and access provisions. Frame in terms of future value and retrofit cost avoidance.
   - **Dual-Function Zoning (REQ-002.6):** Fire Hall 24/7 vs. Public Works business hours is a key operational reality. Use `Guidance.md` Example 2 as a template. Demonstrate understanding of energy profiles and zoning strategy.
   - **Overhead Door Thermal Strategy (REQ-002.2):** 16-ft doors (Addendum 03) are a thermal challenge. Address insulated doors, destratification, radiant heating options per `Guidance.md` Principle 4.
   - **Fire Apparatus Exhaust Integration (REQ-002.4):** Required per Addendum 03. Address make-up air, pressure balance, tempering per `Guidance.md` Principle 5.
   - **Code Compliance (REQ-001.2):** Use `Guidance.md` Example 3 as a template. State baseline compliance (ABC, NECB) with specific code references; identify performance enhancements; provide target EUI.

4.3. **Incorporate assumptions and TBD items:**
   - Where information is not available from reference materials (e.g., specific EUI targets from RFP OSR), use reasonable assumptions based on building type and label as **ASSUMPTION** (e.g., "Target EUI ≤250 kWh/m²/yr is typical for mixed-use municipal facilities in Alberta; specific Owner target is **TBD** pending RFP Appendix A confirmation")
   - Where requirements cannot be determined, mark as **TBD** with a note indicating missing information (e.g., "**TBD:** LEED certification level pending RFP Appendix A confirmation")
   - Do not invent requirements or commitments that are not supported by available information

4.4. **Add cross-references:**
   - Insert cross-references to related deliverables where noted in Step 3 (e.g., "As shown in Concept Design (Section X)...")
   - Use placeholders if section numbers are not yet known (e.g., "As shown in Concept Design [SECTION TBD]...")

4.5. **Write in Markdown format:**
   - Use headings, bullet points, tables for clarity and structure
   - Keep paragraphs concise (3-5 sentences)
   - Use bold for emphasis on key commitments or requirements
   - Include placeholders for diagrams if planned (e.g., "[INSERT: HVAC Zoning Diagram]")

**Deliverable:** First draft of Sustainability and Energy Narrative (Markdown file).

**Verification:**
- All mandatory requirements (REQ-001 through REQ-008 "shall" items) are addressed
- Solar-ready provisions section is comprehensive and aligns with Addendum 03
- Narrative is credible (uses specific strategies and code references)
- Narrative is appropriate length (target 4-6 pages; approximately 2,000-3,000 words)
- All assumptions and TBD items are labeled

**Source:** `Specification.md` (requirements); `Guidance.md` (principles, examples); ASSUMPTION (narrative structure and drafting process)

---

### Step 5: Technical Review and Code Compliance Check

**Objective:** Verify technical accuracy, code compliance, and credibility before finalizing narrative.

**Actions:**

5.1. **Self-review (narrative author):**
   - Read draft from evaluator perspective: Is it clear? Persuasive? Credible?
   - Check for consistency: Are technical terms used correctly and consistently?
   - Check for completeness: Are all mandatory requirements addressed?
   - Check for appropriate detail level: Is it conceptual (proposal stage) and not over-specified?

5.2. **Code compliance review (Building Code Consultant or experienced architect):**
   - Verify code references are accurate (ABC, NECB edition numbers and section references)
   - Verify code compliance statements are defensible (e.g., envelope R-values, mechanical system efficiencies)
   - **Verification method (per Lensing C-002):** Independently verify that envelope R-values and mechanical efficiencies cited in narrative match actual code requirements for the specified edition. Narrative author must not assume values from examples are correct without verification against current code.
   - Identify any code compliance risks or ambiguities
   - Recommend corrections or clarifications
   - **Pass/fail determination (per Lensing A-003, X-001):** Code compliance reviewer has authority to determine pass/fail for compliance matrix check (Step 8). Document ruling with rationale if narrative fails code compliance review.

5.3. **Sustainability/energy specialist review (if available):**
   - Verify energy strategies are technically sound and best practice
   - Verify solar-ready provisions are comprehensive and feasible
   - Verify performance targets (e.g., EUI) are realistic for building type and climate
   - Recommend enhancements or adjustments

5.4. **Cross-document consistency review (Proposal Manager or QA Lead):**
   - Compare sustainability narrative with related deliverables (DEL-02-01, DEL-02-02, DEL-09-02, DEL-06-01) if available
   - **Mandatory cross-deliverable verification (per Lensing X-002):** Explicitly verify alignment with:
     - DEL-02-01: Building orientation for solar strategy consistency
     - DEL-02-02: Design Brief boundaries to avoid duplication
     - DEL-09-02: Site conditions for stormwater/water efficiency
     - DEL-06-01: Commissioning scope for energy systems (avoid duplicating commissioning procedures)
   - Identify any conflicts or inconsistencies (e.g., energy narrative implies south-facing roof, but concept design shows east-west orientation)
   - Verify cross-references are accurate
   - Flag conflicts for resolution (see Step 6 if conflicts identified)

5.5. **Document review comments:**
   - Collect review comments in tracked changes (Word) or comment log (spreadsheet)
   - Prioritize comments: Critical (must fix for compliance), Important (improves credibility/scoring), Minor (nice to have)

**Deliverable:** Review comments log with prioritized action items.

**Verification:** All reviewers have provided input; critical comments are identified for resolution.

**Source:** `Specification.md` (Verification section); AGENT_4_DOCUMENTS.md (Step 5 — Cross-Reference Consistency Check)

---

### Step 6: Resolve Conflicts and Address Review Comments

**Objective:** Incorporate review feedback and resolve any conflicts or inconsistencies identified in Step 5.

**Actions:**

6.1. **Address critical comments:**
   - Correct any technical errors or code compliance issues
   - Resolve any conflicts with other deliverables (coordinate with other authors if needed)
   - Fill in any missing mandatory requirements

6.2. **Address important comments:**
   - Enhance credibility by incorporating reviewer suggestions (e.g., more specific strategies, better code references)
   - Improve clarity and persuasiveness based on feedback

6.3. **Address minor comments (as time/space allows):**
   - Incorporate editorial suggestions, formatting improvements

6.4. **Resolve cross-document conflicts (if identified):**
   - **If conflict can be resolved from available information:** Coordinate with other deliverable authors to align content (e.g., confirm building orientation with DEL-02-01 author; update energy narrative accordingly)
   - **If conflict cannot be resolved:** Document conflict in `Guidance.md` Conflict Table (see template in `Guidance.md`) and flag for human ruling. Do not guess or force a resolution that is unsupported by available information.

6.5. **Clarify authorship boundaries for detailed specifications (per Lensing F-004):**
   - Exhaust/HVAC interface specification: Clarify whether detailed exhaust system specification is narrative author responsibility (proposal deliverable) or deferred to detailed design (DEL-04-01 Construction Methodology)
   - **Recommendation:** Narrative describes design intent and integration strategy; detailed specifications are Design-Build detailed design responsibility
   - Document boundary decision in narrative (e.g., "Detailed exhaust system specifications will be developed during detailed design phase...")

**Conflict Table entry format (if needed):**

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------------------|--------------|
| CONF-001 | Energy narrative assumes south-facing roof for solar optimization, but Concept Design (DEL-02-01) shows east-west building orientation due to site access constraints | DEL-02-03 (Sustainability Narrative — Solar-Ready section) | DEL-02-01 (Concept Design — Site Plan) | Solar-ready provisions strategy; roof orientation rationale | Defer to DEL-02-01 (site access drives orientation); update DEL-02-03 to describe solar strategy for east-west roof (south-facing slope on one side; additional roof area to compensate) | TBD (human coordination) |

6.5. **Update draft to incorporate review comments:**
   - Revise narrative based on prioritized comments
   - Track changes or version control to document revisions
   - Update assumptions/TBD items if new information becomes available

**Deliverable:** Revised draft of Sustainability and Energy Narrative incorporating review feedback; Conflict Table updated (if conflicts identified).

**Verification:** All critical and important review comments are addressed; any unresolved conflicts are documented in Conflict Table.

**Source:** AGENT_4_DOCUMENTS.md (Step 5 — Cross-Reference Consistency Check; Conflict Table protocol); `Guidance.md` (Conflict Table template)

---

### Step 7: Prepare Diagrams (Optional)

**Objective:** Create illustrative diagrams to enhance narrative clarity and communication (if beneficial and file size permits).

**Actions:**

7.1. **Determine if diagrams are beneficial:**
   - Review narrative: Are there concepts that would be clearer with a visual (e.g., HVAC zoning, solar-ready roof plan, building envelope section)?
   - Assess value vs. file size: Will diagrams significantly improve evaluator understanding and differentiate the proposal, or are they redundant with text?
   - Coordinate with Proposal Manager to confirm file size budget (contribution to 15 MB total PDF limit)

7.2. **If diagrams are beneficial, create 1-3 key diagrams:**
   - **Suggested diagram 1: HVAC Zoning Schematic**
     - Simple floor plan showing Fire Hall zones (24/7) vs. Public Works zones (scheduled)
     - Color-coded or labeled to show zone types and control strategies
     - Supports dual-function zoning narrative (Guidance.md Principle 3, Example 2)
   - **Suggested diagram 2: Solar-Ready Roof Plan**
     - Annotated roof plan showing solar-ready zones, orientation, access points, HVAC equipment locations
     - Supports solar-ready provisions narrative (Guidance.md Principle 2, Example 1)
   - **Suggested diagram 3: Building Envelope Section**
     - Schematic wall/roof section showing insulation layers, air barrier, thermal bridge details, overhead door thermal strategy
     - Supports envelope thermal performance narrative (Guidance.md Principle 4)

7.3. **Optimize diagrams for file size:**
   - Use simple line drawings or schematics (not photo-realistic renderings)
   - Export as vector (PDF) or low-resolution raster (PNG, 150 dpi) to minimize file size
   - Compress images using image optimization tools if needed
   - Target <500 KB per diagram (total contribution ~1-1.5 MB for 3 diagrams)

7.4. **Insert diagrams into narrative:**
   - Place diagrams adjacent to relevant narrative sections
   - Add captions and figure numbers (e.g., "Figure 1: HVAC Zoning Strategy")
   - Reference diagrams in narrative text (e.g., "As shown in Figure 1, the HVAC system is zoned to...")

**Deliverable:** 1-3 diagrams (if created) in optimized format; diagrams inserted into narrative Markdown with captions.

**Verification:** Diagrams enhance clarity without adding excessive file size; diagrams are referenced in narrative text.

**Source:** `Guidance.md` (Consideration 4 — Proposal PDF size limit); ASSUMPTION (diagram best practices)

**Note:** If file size budget is tight or diagrams do not significantly add value, skip this step. Text-only narrative is acceptable if it is clear and credible.

---

### Step 8: Compliance Matrix Check

**Objective:** Verify that all mandatory compliance requirements are addressed in the narrative and documented for proposal compliance matrix (DEL-01-01).

**Actions:**

8.1. **Review `Specification.md` mandatory requirements:**
   - Go through all "shall" requirements (REQ-001.1, REQ-001.2, REQ-001.3, REQ-001.4, REQ-002.1–002.6, REQ-003.1–003.4, REQ-006.1, REQ-007.1, REQ-008.1–008.3)
   - For each requirement, identify where it is addressed in the narrative (section heading or paragraph)

8.2. **Create compliance mapping table (for internal use / DEL-01-01 input):**

   | Requirement ID | Requirement Summary | Narrative Section / Location | Status |
   |----------------|---------------------|------------------------------|--------|
   | REQ-001.1 | Address "solar capable roofing" | Solar-Ready Provisions section | ✓ Addressed |
   | REQ-001.2 | Credible and code-aware | Performance Targets & Verification section (code compliance statement) | ✓ Addressed |
   | REQ-002.2 | Address 16-ft overhead door thermal challenges | Building Envelope section (overhead door strategy) | ✓ Addressed |
   | ... | ... | ... | ... |

8.3. **Flag any gaps:**
   - If any mandatory requirement is not addressed, add to narrative immediately (critical for compliance)
   - If requirement cannot be addressed due to missing information, mark as **TBD** in narrative and flag in compliance table

8.4. **Provide compliance mapping to Proposal Manager:**
   - Share compliance table with Proposal Manager for integration into DEL-01-01 (Compliance Matrix and Checklist)
   - This supports overall proposal compliance verification

**Deliverable:** Compliance mapping table (for DEL-01-01 input); confirmation that all mandatory requirements are addressed in narrative.

**Verification:** No mandatory requirements are missing; all gaps are flagged and resolved.

**Source:** `Specification.md` (all requirements); Decomposition §8 (DEL-01-01 — Compliance Matrix)

---

### Step 9: Finalize and Format for Submission

**Objective:** Prepare the final version of the narrative for integration into the proposal PDF.

**Actions:**

9.1. **Final editorial review:**
   - Proofread for grammar, spelling, punctuation
   - Check formatting consistency (headings, bullet points, tables)
   - Verify all cross-references, citations, and figure numbers are correct
   - Verify all ASSUMPTION and TBD labels are in place where needed

9.2. **Convert to submission format:**
   - If proposal uses Word format: Convert Markdown to Word (.docx) with appropriate styles and formatting
   - If proposal uses PDF format: Convert Markdown to PDF or provide to Proposal Manager for integration into master proposal document
   - Ensure diagrams are embedded and display correctly

9.3. **Check page count and file size contribution:**
   - Verify narrative is within target length (4-6 pages)
   - Verify file size contribution is acceptable for 15 MB total PDF limit
   - If too long or too large, prioritize content (keep mandatory requirements; trim optional content or reduce diagram resolution)

9.4. **Deliver to Proposal Manager:**
   - Provide final narrative file (Word or PDF) to Proposal Manager for integration into proposal package (DEL-01-02)
   - Provide compliance mapping table (from Step 8) for DEL-01-01
   - Provide any notes or caveats (e.g., TBD items requiring follow-up, cross-references to finalize after other sections are complete)

9.5. **Archive draft versions:**
   - Save all draft versions, review comments, and working documents for record retention (30 days post-submission per `Specification.md`)
   - Ensure version control is clear (e.g., "DEL-02-03_Draft1.md", "DEL-02-03_Final.docx")

**Deliverable:** Final Sustainability and Energy Narrative (Word or PDF); compliance mapping table; delivery notes for Proposal Manager.

**Verification:** Narrative is complete, proofread, formatted, and ready for integration into proposal package.

**Source:** `Specification.md` (Documentation section); Decomposition §3 (C-01 — PDF ≤15 MB); ASSUMPTION (finalization process)

---

## Verification

### Process Verification (During Production)

| Step | Verification Checkpoint | Pass Criteria |
|------|-------------------------|---------------|
| **Step 1** | Context and requirements understood | Can articulate deliverable purpose, scope, and evaluation context |
| **Step 2** | Requirements extracted from RFP | Requirements checklist complete; all mandatory items captured |
| **Step 3** | Coordination with related deliverables | Cross-reference notes complete; boundaries defined |
| **Step 4** | Draft narrative complete | All mandatory requirements addressed; appropriate length and detail level |
| **Step 5** | Technical review complete | Review comments documented; critical issues identified |
| **Step 6** | Review comments addressed | All critical and important comments resolved; conflicts documented if unresolved |
| **Step 7** | Diagrams prepared (if applicable) | Diagrams enhance clarity and are file-size optimized |
| **Step 8** | Compliance check complete | Compliance mapping table complete; no mandatory gaps |
| **Step 9** | Final narrative delivered | Narrative finalized, formatted, and delivered to Proposal Manager |

**Source:** AGENT_4_DOCUMENTS.md (Procedure schema — Verification section)

### Deliverable Acceptance (Final Quality Gate)

The deliverable is accepted when:

1. **All mandatory requirements met:**
   - All `Specification.md` REQ-001 through REQ-008 "shall" requirements are addressed in narrative content
   - Compliance mapping table confirms all mandatory items are covered

2. **Solar-ready provisions comprehensively addressed:**
   - Structural, electrical, orientation, and access provisions are described with sufficient detail
   - Aligns with Addendum 03 "solar capable roofing" requirement

3. **Code-aware and credible:**
   - Narrative references applicable codes/standards (ABC, NECB)
   - Technical content is accurate and appropriate for proposal stage
   - No technical errors identified during code compliance review

4. **Cross-document consistency verified:**
   - Aligns with DEL-02-01 (Concept Design), DEL-02-02 (Design Brief), DEL-09-02 (Site Conditions) where applicable
   - Cross-references are accurate
   - No unresolved conflicts (or conflicts documented in Conflict Table with proposed resolution)

5. **Evaluation-ready:**
   - Content supports Design Brief evaluation criteria (5 points)
   - Narrative is clear, persuasive, and suitable for municipal evaluators
   - Appropriate length and formatting for proposal submission

6. **Ready for integration:**
   - Final narrative file delivered in required format (Word or PDF)
   - File size is within budget (contributes to 15 MB total PDF limit)
   - Proposal Manager confirms narrative is ready for integration into proposal package

**Source:** `Specification.md` (Acceptance Criteria section); _CONTEXT.md (acceptance criteria)

---

## Records

### Documentation to Retain

| Record | Format | Retention Period | Location |
|--------|--------|------------------|----------|
| **Final Sustainability and Energy Narrative** | Word/PDF | Project completion | Delivered to Proposal Manager for proposal package |
| **Draft Versions** | Markdown/Word | Submission + 30 days | Project working files folder |
| **Review Comments Log** | Spreadsheet/Word | Submission + 30 days | Project working files folder |
| **Requirements Checklist** | Spreadsheet/Markdown | Submission + 30 days | Project working files folder |
| **Cross-Reference Notes** | Markdown/Notes | Submission + 30 days | Project working files folder |
| **Compliance Mapping Table** | Spreadsheet | Project completion | Delivered to Proposal Manager for DEL-01-01 |
| **Diagrams (source files)** | CAD/Vector | Project completion | Project working files folder |

**Source:** `Specification.md` (Documentation — Record Retention section); ASSUMPTION (standard project records management)

**Additional Record (per Lensing A-004, X-004):**
- **Energy Commitment Traceability Log:** Retain until project completion. Design-Build flexibility allows refinement during detailed design; audit trail needed to verify how proposal energy commitments are maintained or modified post-award. Log should track: (1) original narrative commitments, (2) detailed design refinements, (3) rationale for changes, (4) Owner approval if commitments reduced.
- **Note:** Procedure defines proposal-stage verification (Steps 5-8) but does not define post-award verification of energy commitments during detailed design/construction. Coordinate with project management procedures to establish post-award traceability mechanism.

### Handoff Documentation

When delivering the final narrative to Proposal Manager, provide:

1. **Final narrative file** (Word or PDF)
2. **Compliance mapping table** (for DEL-01-01 integration)
3. **Delivery notes** including:
   - Any TBD items requiring follow-up or clarification
   - Any cross-references to finalize after other sections are complete (e.g., "[SECTION TBD]" placeholders)
   - Any assumptions made due to missing information (e.g., "Assumed NECB 2017 as code edition; confirm with RFP Appendix A")
   - File size and page count
   - Confirmation of all mandatory requirements addressed

**Source:** ASSUMPTION (standard deliverable handoff practice)

---

**Document History:**
- 2026-02-04 — INITIALIZED (4_DOCUMENTS agent — Pass 1)
- 2026-02-04 — SEMANTIC ENRICHED (4_DOCUMENTS agent — Pass 3, incorporated 7 warranted items: A-003, A-004, C-002, C-005, F-004, X-001, X-002, X-004)
