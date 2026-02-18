# Procedure: DEL-05-02 AppendixH ScheduleB CostBreakdown

## Purpose

This procedure describes the process to **produce** the Schedule B detailed cost breakdown for Appendix H of the Penhold Public Services Building Design-Build proposal.

**Target outcome:** A completed Schedule B form that meets all RFP requirements, reconciles to Schedule A, reflects addenda changes, and supports the 35-point Proposal Price evaluation.

**Responsible role:** Estimator / Commercial Lead (with input from technical leads for scope verification)

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED (dependencies coordinated externally by humans per _DEPENDENCIES.md)

**Upstream dependencies (coordinated externally):**
- **DEL-02-01 (Concept Design Package):** Required to understand building scope, area, and major systems for cost estimating
- **DEL-05-03 (Pricing Narrative and Assumptions):** Should be developed in parallel to ensure consistency of assumptions and exclusions
- **Technical input from discipline leads:** Required to validate scope inclusion/exclusion and technical requirements

**Downstream dependencies (coordinated externally):**
- **DEL-05-01 (Schedule A):** Schedule B totals flow to Schedule A summary pricing

**Source:** _DEPENDENCIES.md; ASSUMPTION (logical workflow dependencies)

### Reference Materials Required

**[Lensing C-004]** Before beginning, ensure access to all prerequisites. **Action Required:** Proposal Manager must obtain and provide file locations for RFP source files before Procedure Step 1 begins.

| # | Material | Location | Status | Responsible |
|---|----------|----------|--------|-------------|
| 1 | **RFP Appendix H template:** Blank Schedule B form (Excel or PDF format) | _Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf (Appendix H section) | **TBD — CRITICAL PATH BLOCKER** | Proposal Manager |
| 2 | **Decomposition document:** Section 4 (Addenda impacts), Section 5 (Vocabulary Map), Section 8 (DEL-05-02 definition) | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md | Available | N/A |
| 3 | **Addendum 03:** Scope changes (pickled sand removal, 12-acre site, technical clarifications) | _Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf | **TBD** | Proposal Manager |
| 4 | **DEL-02-01 (Concept Design):** Building area, massing, major systems | DEL-02-01 folder | **TBD** | Design Lead |
| 5 | **Reference project cost data:** Historical cost data for similar municipal facilities (fire hall + public works combination) | Firm internal database or external cost guides (e.g., RSMeans) | ASSUMPTION: Available to Estimator | Estimator |
| 6 | **Site reference reports:** Geotechnical, wetlands, grading plans (for sitework estimating) | _Sources/ (per _REFERENCES.md) | **TBD** | Civil Lead |

**Readiness Gate:** Procedure Step 1 cannot begin until items 1, 3 marked as Available. Items 4, 5, 6 required for Step 2.

**Source:** _REFERENCES.md; Specification.md (R-001 template requirement); ASSUMPTION (standard estimating inputs); _SEMANTIC_LENSING.md (C-004)

### Tools and Systems

- **Spreadsheet software:** Excel or equivalent (for cost calculations and template completion)
- **Estimating software (optional):** If firm uses dedicated estimating platform (e.g., On-Screen Takeoff, Bluebeam for quantities)
- **Version control:** Track Schedule B revisions if resubmitted (per RFP Section 4.2 revision protocol)

**Source:** ASSUMPTION (standard estimating tools)

## Steps

### Step 1: Review Scope and Template

**[Lensing A-003]** This step cannot proceed until Appendix H template is obtained. Template location is a critical path blocker per Prerequisites.

**Action:**
1. Read the decomposition document Section 8 (DEL-05-02) to confirm deliverable requirements
2. **Obtain and review the Appendix H Schedule B template** from:
   - **Primary source:** RFP Section 4.3 (Appendix H)
   - **File location:** _Sources/ directory — confirm with Proposal Manager
   - **Format:** Determine if Excel (enables linked formulas) or PDF (requires manual reconciliation)
3. Review template to understand:
   - Required cost categories (General Requirements, Building, Sitework)
   - Required line items (major systems, trades, or cost categories)
   - Format for Additional Options 1-6
   - Location of monitoring fee line (for Option 4)
   - Location of addenda acknowledgement line (if on Schedule B; may be on Schedule A)
4. Review Addendum 03 to confirm scope exclusions and clarifications:
   - Pickled sand storage building removed
   - 12-acre developable site (not full 20 acres)
   - Service tie-in allowance approach permitted
   - Technical requirements (overhead doors, sumps, exhaust, generator, fill stations, solar-ready)

**Verification:** Template obtained and structure understood; scope exclusions confirmed; addenda acknowledgement location determined.

**Output:** Annotated template with required line items identified; template file path documented.

**Source:** Specification.md (R-001, R-002, R-003); Decomposition Section 4, Section 8; _SEMANTIC_LENSING.md (A-003)

---

### Step 2: Gather Quantity and Scope Information

**Action:**
1. Review DEL-02-01 (Concept Design Package) to extract:
   - Building gross floor area (GFA) or net floor area (NFA)
   - Building height, massing, structural system
   - Major systems: foundation type, structural system, envelope materials, HVAC approach, electrical service size, fire protection approach
2. Perform preliminary quantity takeoff (or confirm quantities from design team):
   - Building area (SF) for area-based unit costs
   - Site earthwork quantities (CY) — note 12-acre developable area constraint
   - Linear quantities for utilities (LF of water, sanitary, storm, gas, electrical)
   - Paving area (SF or SY)
   - Overhead door quantities and sizes (per Addendum 03: 16 ft height requirement)
   - Apparatus bay sumps, fire apparatus exhaust systems, fill stations (per Addendum 03)
3. Identify Additional Options scope:
   - Option 1 (Built-in wash bay): Size, system requirements — **TBD: confirm design intent**
   - Option 2 (Yard lighting): Area coverage, fixture type/count — **TBD: confirm design intent**
   - Option 3 (Building access control): System type, door count — **TBD: confirm design intent**
   - Option 4 (Security/cameras): Camera count, monitoring service terms — **TBD: confirm design intent**
   - Option 5 (Exterior signage): Type, size, quantity — **TBD: confirm design intent**
   - Option 6 (Appliances): List of appliances, specifications — **TBD: confirm design intent**

**Verification:** Quantities reconcile to concept design; scope reflects addenda changes (no pickled sand building; 12-acre site).

**Output:** Quantity takeoff worksheet (internal working document).

**Source:** Procedure Step 1 prerequisite (DEL-02-01); Decomposition Section 4 (Addendum 03); Guidance.md (cost allocation considerations)

---

### Step 3: Apply Unit Costs and Calculate Line Items

**Action:**
1. For each cost category (General Requirements, Building, Sitework), apply appropriate unit costs:
   - **General Requirements:** Use percentage of construction cost (8-12% typical) or itemize (PM labor, superintendence, mobilization, temp facilities, closeout)
   - **Building:** Apply unit costs ($/SF of GFA or NFA) for major systems, or use detailed trade breakdowns:
     - Foundation: $/SF or $/CY
     - Structure: $/SF
     - Envelope: $/SF of wall/roof area
     - Interior finishes: $/SF of floor area
     - Mechanical: $/SF or lump sum per system
     - Electrical: $/SF or lump sum
     - Fire protection: $/SF or per sprinkler head + apparatus exhaust system
     - Specialties: Itemize (lockers, apparatus doors, fill stations, etc.)
   - **Sitework:** Apply unit costs:
     - Earthwork: $/CY
     - Utilities: $/LF for water, sanitary, storm, gas, electrical (or use allowance for service tie-ins per Addendum 03)
     - Paving: $/SF or $/SY
     - Landscaping: $/SF or lump sum
     - Site lighting (base scope): $/fixture or lump sum
2. For Additional Options 1-6, apply unit costs or lump sums:
   - Option 4 (Security/cameras): Separate capital cost (equipment + installation) from monitoring fee
   - Monitoring fee: Express as annual or monthly recurring cost (coordinate with DEL-05-03 for clarification)
3. Apply markups:
   - Overhead and profit (typical range: 15-25% on subtrades; 10-15% on own forces)
   - Contingency (if explicit line item in template; otherwise embed in line items) — coordinate with Guidance.md (Principle 5)
   - **TBD:** Confirm markup structure per firm policy and competitive strategy

**Verification:** Unit costs are reasonable and defensible; markups applied consistently.

**Output:** Draft Schedule B with all line items populated.

**Source:** Guidance.md (Principle 5: contingency; cost allocation considerations); Specification.md (R-004: monitoring fee separation)

---

### Step 4: Perform Internal QA and Reconciliation

**Action:**
1. **Completeness check:**
   - Verify all required cost categories present: General Requirements, Building, Sitework
   - Verify all six Additional Options have line items
   - Verify Option 4 monitoring fee is separated
   - Verify no pickled sand storage building line item in base costs
   - Verify sitework scope reflects 12-acre developable area
2. **Mathematical reconciliation:**
   - Sum Schedule B base scope line items → compare to Schedule A base total
   - Sum each Additional Option → compare to corresponding Schedule A option total
   - Check for arithmetic errors, formula breaks, or rounding discrepancies
3. **Consistency check with DEL-05-03 (Pricing Narrative):**
   - Confirm assumptions documented in pricing narrative match cost basis in Schedule B
   - Confirm exclusions (pickled sand, FF&E) are consistent
   - Confirm allowances (service tie-ins) are reflected consistently
4. **Cross-reference to Specification.md requirements:**
   - R-001 to R-010: Verify compliance with all requirements

**Verification:** All checks pass; reconciliation worksheet shows Schedule B = Schedule A.

**Output:** QA checklist completed; reconciliation worksheet documented (internal artifact).

**Source:** Specification.md (R-005: reconciliation; R-009: completeness); Guidance.md (Principle 2: consistency)

---

### Step 5: Technical Review and Approval

**Action:**
1. Circulate draft Schedule B to technical leads for scope verification:
   - **Architect / Design Lead:** Verify building systems and scope completeness
   - **Civil Lead:** Verify sitework scope and 12-acre site constraint
   - **MEP Lead:** Verify mechanical, electrical, plumbing, fire protection scope (including Addendum 03 technical requirements: generator, exhaust, fill stations, solar-ready)
   - **Commercial Lead:** Verify cost reasonableness and competitive positioning
2. Incorporate feedback and resolve discrepancies
3. Obtain Commercial Lead sign-off

**Verification:** Technical leads confirm scope accuracy; Commercial Lead approves for submission.

**Output:** Approved Schedule B ready for final assembly into Appendix H.

**Source:** ASSUMPTION (standard estimating QA workflow)

---

### Step 6: Finalize and Integrate into Appendix H

**Action:**
1. Complete addenda acknowledgement line (if on Schedule B; otherwise coordinate with DEL-05-01 Schedule A)
2. Export Schedule B in required format (PDF or Excel, per RFP instructions)
3. Integrate Schedule B into full Appendix H package (along with Schedule A from DEL-05-01)
4. Perform final visual QA:
   - Check for formatting errors, blank cells, or placeholder text
   - Verify page numbering and cross-references
   - Verify totals match Schedule A (final confirmation)
5. Deliver to Proposal Manager for integration into full proposal PDF (per DEL-01-02 submission package)

**Verification:** Schedule B formatted correctly; integrated into Appendix H; ready for submission.

**Output:** Final Schedule B delivered to Proposal Manager.

**Source:** Specification.md (R-001: template compliance; R-006: addenda acknowledgement); Decomposition Section 8 (DEL-01-02: proposal assembly)

---

## Verification

### Process Verification Checkpoints

**[Lensing X-001]** Added verification checkpoint for R-006 (Addenda Acknowledgement) to ensure governance alignment.

| Checkpoint | What to Verify | Responsible | Timing |
|------------|----------------|-------------|--------|
| **Step 1 completion** | Template structure understood; scope exclusions confirmed; template file path documented | Estimator | Before starting cost calculations |
| **Step 2 completion** | Quantities reconcile to concept design; no pickled sand building; 12-acre site reflected | Estimator + Design Lead | Before applying unit costs |
| **Step 3 completion** | All line items populated; unit costs reasonable; markups applied | Estimator | Before QA |
| **Step 4 completion** | All QA checks pass; Schedule B = Schedule A reconciliation confirmed | Estimator + QA reviewer | Before technical review |
| **Step 5 completion** | Technical leads approve scope; Commercial Lead signs off | Technical Leads + Commercial Lead | Before finalization |
| **Step 6 completion** | Final Schedule B formatted and integrated into Appendix H | Estimator + Proposal Manager | Before proposal submission |
| **R-006 Addenda Acknowledgement** | **[Lensing X-001]** Verify addenda acknowledgement line is completed at correct location (Schedule B, Schedule A, or Appendix H cover per RFP instructions); coordinate with DEL-05-01 if on Schedule A | Estimator + Proposal Manager | Before submission |

### Final Acceptance Criteria (from _CONTEXT.md)

1. **Completeness:** All required cost categories, line items, and Additional Options present
2. **Monitoring fee separated where required:** Option 4 monitoring fee is a separate line item
3. **Totals match Schedule A:** Mathematical reconciliation confirmed

**Pass condition:** All three acceptance criteria met AND all process verification checkpoints completed.

**Source:** _CONTEXT.md; Specification.md

---

## Records

### Documentation to Retain

| Record | Purpose | Retention |
|--------|---------|-----------|
| **Completed Schedule B (final submission version)** | Official deliverable | Permanent (proposal archive) |
| **Quantity takeoff worksheet** | Backup for cost derivation; audit trail | Retain through project delivery + warranty period |
| **Unit cost backup** | Justification for cost estimates; negotiation support | Retain through project delivery + warranty period |
| **Reconciliation worksheet** | Proof of Schedule A/B consistency | Retain through proposal evaluation period |
| **QA checklist** | Evidence of internal quality control | Retain through proposal evaluation period |
| **Technical review comments** | Scope verification trail | Retain through proposal evaluation period |
| **Version history** | Track revisions if proposal resubmitted (per RFP Section 4.2) | Retain through proposal evaluation period |

**Source:** ASSUMPTION (standard estimating records retention practice); Specification.md (Documentation section)

---

## Cross-References

| Related Document | Relationship | Key Links |
|------------------|--------------|-----------|
| **Datasheet.md** | Input facts and constraints | Cost categories, Additional Options, scope constraints inform Steps 1-2 (scope review and quantity gathering) |
| **Specification.md** | Requirements to verify | Step 4 (QA and reconciliation) verifies compliance with R-001 to R-010; verification checkpoints implement Specification verification methods |
| **Guidance.md** | Principles applied in execution | Step 3 (apply unit costs) implements Principle 5 (contingency); Step 4 implements Principle 2 (consistency); Step 1 implements Principle 3 (addenda compliance) |

---

**Document Status:** Pass 3 (Semantic Lensing Enrichment)
**Last Updated:** 2026-02-04
**Lensing Items Incorporated:** A-003, C-004, X-001
**Completeness:** Procedure steps defined; cross-references added; lensing enrichments added for prerequisites readiness gate, template location guidance, and addenda acknowledgement verification checkpoint. Detailed template structure and technical scope inputs are TBD pending access to Appendix H template and DEL-02-01 concept design.
