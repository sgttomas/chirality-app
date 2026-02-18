# Procedure — Accessibility and Adaptability Narrative

## Purpose

This procedure documents the steps to **produce** the Accessibility and Adaptability Narrative (DEL-03-06) and **verify** that it meets RFP requirements per §7.1.3 and §7.1.5.

The narrative is a composition task, not a detailed technical design task. It requires research, cross-discipline coordination, drafting, consistency checking, and integration into the RFP Response. The Architect is the lead author; input from Structural, Mechanical, and Electrical engineers is required.

---

## Prerequisites

### Required Inputs

| Input | Description | Status | Location |
|-------|-------------|--------|----------|
| **RFP §7.1.3 and §7.1.5** | Scoring criteria, narrative expectations, and requirements for accessibility and adaptability sections | Available | `/test/execution-6b/_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf` (p. 17) |
| **Addendum 03** | Site area clarification (12 acres usable); pickled sand storage removal; second storey acceptable; flooring type; room sizing ranges | Available | `/test/execution-6b/_Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf` |
| **Decomposition v2.3** | SOW-0014, SOW-0015 scope definitions; OBJ-004, OBJ-005 objectives; PKG-003 package scope | Available | `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` |
| **Alberta Building Code** | Accessibility requirements governing this facility | Not provided in RFP sources — TBD | Design-Builder's architect/code consultant to procure applicable edition |
| **DEL-03-03 (Structural Design Brief)** | Structural expansion provisions for coordination. **Minimum-viable input:** structural grid decision (bay module dimensions, expansion direction, non-structural wall location) required before Step A3; full DEL-03-03 narrative not required -- verbal/written confirmation from Structural Engineer is acceptable at draft stage, with final consistency check when DEL-03-03 is complete. *(Enriched per E-002)* | TBD (to be generated) | `/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-03_StructuralDesignBrief/` |
| **DEL-02-01 (Architectural Concept)** | Floor plan showing accessibility features and building footprint. **Minimum-viable input:** preliminary floor plan with accessible washroom locations, primary circulation routes, and entrance locations required before Step A5; schematic-level layout is acceptable at draft stage. *(Enriched per E-002)* | TBD (to be generated) | `/test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-01_ArchitecturalConceptPackage/` |
| **DEL-02-02 (Civil Site Concept)** | Site plan showing expansion envelope, parking, access routes. **Minimum-viable input:** site plan showing building footprint location and feasible expansion direction(s) relative to flood fringe boundary required before Step A6; detailed grading not required at draft stage. *(Enriched per E-002)* | TBD (to be generated) | `/test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-02_CivilSiteConceptPlan/` |
| **Geotechnical Investigation Report** | Site soil conditions; foundation implications for expansion | Available | `/test/execution-6b/_Sources/references/AB-2024-07156-Penhold PSB_Geotechnical Investigation Report.pdf` |
| **Site Grading Plan** | Existing and proposed site layout; drainage; expansion footprint constraints | Available | `/test/execution-6b/_Sources/references/AB-2024-07156-Penhold PSB_Site grading.pdf` |
| **Wetland Assessment** | Environmental no-build constraints affecting expansion | Available | `/test/execution-6b/_Sources/references/AB-2024-07156-Penhold PSB_Wetland Assessment.pdf` |

### Required Resources

- **Architect** — lead author and coordinator
- **Structural Engineer** — input on structural expansion provisions (column grid, foundation, utility chases); also author of DEL-03-03
- **Mechanical Engineer** — input on HVAC/plumbing flexibility and MEP routing for future expansion
- **Electrical Engineer** — input on panel sizing, conduit routing, IT distribution for future loads
- **Building Code / Accessibility Consultant** — optional but recommended; assists with ABC interpretation and confirms accessible design features

---

## Steps

### Step A1: Confirm Governing Requirements

**Action:**
1. Read RFP §7.1.3 (p. 17): Extract exact accessibility narrative requirement — "Provide a narrative describing accommodation of key accessibility elements if/as required by the Alberta Building Code."
2. Read RFP §7.1.5 (p. 17): Extract exact adaptability narrative requirement — "Demonstrate how the site and building design are adaptable to changing needs and accommodate the potential for future building expansion. The structural design of the building should also consider these points (see Section 7.1.2.3 — Structural Design Brief)."
3. Confirm the Specification document (this deliverable folder) reflects current RFP language for all requirements ACC-001 through ACC-006 and ADAPT-001 through ADAPT-005.
4. Note: RFP §7.1.5 explicitly links to Structural Design Brief — confirm DEL-03-03 status and coordinate timing.

**Output:** Confirmed requirements baseline; scheduling of coordination with DEL-03-03 author.

**Effort:** 1 hour

---

### Step A2: Establish Site Constraints for Expansion Scenarios

**Action:**
1. Review Addendum 03 §1.1 (site map): Identify the 12-acre usable area boundary, flood fringe no-build zone (8 acres = storm pond + dog park), and indicative building locations (engineered fill area, ideal cold storage location, stockpile area).
2. Review Site Grading Plan (Appendix E): Confirm existing site grades, drainage direction, and which portions of the 12-acre area are developed/available.
3. Review Wetland Assessment (Appendix D): Identify no-build wetland zones and buffer areas that constrain expansion direction.
4. Review Geotechnical Investigation Report (Appendix D): Note soil conditions (bearing capacity, groundwater depth) relevant to future foundation expansion.
5. Compile a Site Constraint Summary (internal working document) that maps available expansion directions from the main building footprint.

**Output:** Site Constraint Summary — identifies feasible horizontal expansion directions and any site-specific constraints.

**Effort:** 2–3 hours

---

### Step A3: Coordinate with Structural Engineer (DEL-03-03)

**Action:**
1. Meet with Structural Engineer (author of DEL-03-03 Structural Design Brief):
   - Confirm the structural system proposed (e.g., steel frame, concrete frame, hybrid — TBD)
   - Confirm the structural grid / bay module (anticipated: 30-foot clear span bays)
   - Confirm which exterior walls are non-structural (enabling future bay extension)
   - Confirm foundation sizing approach and whether future bay column loads are accommodated
   - Confirm utility chase routing locations (mechanical, electrical, IT) and whether they support future zone extension
2. Document agreed expansion provisions with specific language (for cross-reference consistency in both DEL-03-03 and DEL-03-06)
3. Confirm that DEL-03-03 and DEL-03-06 will use identical terminology for: structural grid, bay expansion direction, foundation provisions, and utility routing

**Output:** Structural Coordination Summary (internal working document); agreed language for cross-referencing.

**Effort:** 2–4 hours (meeting + documentation)

---

### Step A4: Coordinate with Mechanical and Electrical Engineers

**Action:**
1. Meet with Mechanical Engineer (author of DEL-03-04 and DEL-02-04):
   - Confirm HVAC distribution approach (central vs. distributed; zone routing for future bays)
   - Confirm plumbing routing (supply/waste mains; extension points for future bays)
   - Confirm sump system can be extended per Addendum 03 §1.8 (all bays require sumps)
   - Confirm generator sizing (per Addendum 03 §1.15: minimum kitchen, ICP/meeting room, 2 bathrooms, bay door secondary opening) and whether future loads are accommodated
2. Meet with Electrical Engineer (author of DEL-03-05 and DEL-02-05):
   - Confirm main distribution panel spare capacity for future loads
   - Confirm IT/data conduit routing with spare capacity
   - Confirm lighting control system supports modular zone expansion
   - Confirm solar-ready electrical provisions (Addendum 03 §1.17) and whether future panel/inverter provisions are included
3. Document MEP future-readiness provisions in consistent terminology

**Output:** MEP Coordination Summary (internal working document).

**Effort:** 2–3 hours

---

### Step A5: Draft Accessibility Narrative Section (RFP §7.1.3)

**Action:**
1. Draft narrative covering these topics in order:
   - Universal design philosophy (1–2 paragraphs): position accessibility as foundational, not compliance-only; note that the facility serves diverse users
   - Barrier-free path of travel (1 paragraph): exterior approach (accessible parking → main entrance), interior circulation (minimum clear widths, level surface), emergency egress
   - Accessible washrooms (0.5–1 paragraph): count, floor locations, key features (turning radius, grab bars, accessible fixtures, door hardware)
   - Accessible signage strategy (0.5 paragraph): visual + tactile/Braille at room entries and corridor junctions; distinction from Optional Item 5 (building identification signage)
   - Operational area accessibility (0.5–1 paragraph): confirm that accessible paths are provided to all staff and publicly accessible spaces in apparatus bays and public works areas; note ABC applicability to industrial/operations areas as TBD
   - Code compliance statement (0.5 paragraph): reference Alberta Building Code by title; note that specific edition and clause numbers will be confirmed and cited in construction documents during detailed design and permitting
2. Incorporate the accessible flooring alignment note (Addendum 03 §1.3: sealed concrete = level, firm, cleanable surface compatible with accessibility when properly treated)
3. Target length: 350–500 words

**Quality Checks:**
- Addresses ACC-001 through ACC-006 from Specification
- References RFP §7.1.3 requirement
- Cites Alberta Building Code by title (specific clauses TBD)
- Does not claim specific ABC clause compliance that has not been confirmed
- Tone is professional, confident, and proposal-appropriate

**Output:** Draft Accessibility Narrative (350–500 words)

**Effort:** 2–3 hours

---

### Step A6: Draft Adaptability, Flexibility, and Expansion Narrative Section (RFP §7.1.5)

**Action:**
1. Draft narrative covering these topics in order:
   - Expansion philosophy (1 paragraph): 50-year design life; growing community; design provisions that protect the investment
   - Site expansion context (0.5–1 paragraph): 12-acre usable site; 8-acre flood fringe no-build; wetland and environmental constraints from site reports; feasible expansion direction(s) consistent with site plan
   - Structural provisions for expansion (1–1.5 paragraphs): cross-reference DEL-03-03; describe structural grid, non-structural exterior wall at expansion face, foundation sizing, utility chase routing; use language consistent with DEL-03-03
   - MEP future-readiness (0.5–1 paragraph): HVAC zone routing, electrical panel spare capacity, IT conduit provisions, generator sizing context
   - Flexible space planning (0.5–1 paragraph): non-load-bearing partitions in administrative/shared areas; modular equipment arrangements in operational areas; second storey option for shared spaces (Addendum 03 §1.5)
   - Operational adaptability (0.5 paragraph): how existing spaces can be reconfigured without expansion (layout changes, equipment upgrades, technology evolution)
   - Proposed growth scenarios (1 paragraph): Design-Builder proposes specific scenarios (e.g., +1 fire apparatus bay, +1 public works workshop bay, second-storey addition for shared spaces) with stated rationale and approximate timeline
2. Ensure all expansion direction, structural grid, and site references are consistent with DEL-03-03 and DEL-02-02
3. Target length: 400–600 words

**Quality Checks:**
- Addresses ADAPT-001 through ADAPT-005 from Specification
- Cross-references DEL-03-03 (Structural Design Brief) per RFP §7.1.5 mandate
- Acknowledges site constraints (flood fringe, wetlands) per Addendum 03 §1.1
- Proposes specific growth scenarios with rationale (not just principles)
- Consistent terminology with DEL-03-03 and DEL-02-01/02

**Output:** Draft Adaptability Narrative (400–600 words)

**Effort:** 3–4 hours

---

### Step A7: Cross-Document Consistency Review

**Action:**
1. Compare Accessibility Narrative with:
   - DEL-03-01 (Architectural Design Brief) — verify shared understanding of universal design approach and accessible floor plan features
   - DEL-02-01 (Architectural Concept) — verify that accessible path, accessible washroom locations, and accessible parking are reflected in floor plan and site plan
   - Specification.md (ACC requirements) — confirm all six requirements addressed in narrative
2. Compare Adaptability Narrative with:
   - DEL-03-03 (Structural Design Brief) — verify structural grid, expansion direction, foundation provisions, and utility routing language is exactly consistent
   - DEL-02-02 (Civil Site Concept) — verify site plan expansion envelope is consistent with narrative scenarios
   - Specification.md (ADAPT requirements) — confirm all five requirements addressed in narrative
3. Check terminology consistency across all deliverables:

| Term in DEL-03-06 | Must Match in |
|-------------------|--------------|
| "apparatus bay" | DEL-03-01, DEL-03-03, DEL-03-04 |
| "structural grid" / "bay module" | DEL-03-03 |
| "12-acre usable site" | DEL-03-02, DEL-10-02 |
| "Alberta Building Code" | DEL-03-01 |
| "accessible washroom" | DEL-03-01, DEL-02-01 |
| "second storey" | DEL-03-01, DEL-03-03, DEL-02-01 |

4. Check numeric consistency:
   - Number of accessible washrooms consistent with DEL-02-01 floor plan
   - Expansion bay count consistent with DEL-03-03 and site plan
   - 12-acre site area consistent with all other deliverables
5. Identify any unresolvable contradictions and add to Conflict Table in Guidance.md

**Output:** Consistency Review Checklist (completed)

**Effort:** 1–2 hours

---

### Step A8: Incorporate Feedback and Finalize

**Action:**
1. Circulate draft narrative to:
   - Structural Engineer (confirm expansion provisions language accuracy)
   - Mechanical / Electrical Engineers (confirm MEP language accuracy)
   - Proposal Manager (confirm alignment with broader RFP response and Design Brief)
2. Revise narrative based on feedback; document any changes to ASSUMPTION labeling
3. Final proofread: grammar, spelling, formatting consistency with other PKG-003 Design Brief sections
4. Confirm combined narrative length is approximately 800–1,100 words (both sections combined)
5. Remove any claims about specific ABC clauses that have not been confirmed; maintain TBD notation

**Output:** Final reviewed narrative (both sections)

**Effort:** 1–2 hours

---

### Step A9: Post-Submission Review and Assumption Closure Tracking

*(Enriched per A-003: post-submission review step for TBD/ASSUM resolution tracking)*

**Action:**
1. After the RFP response is submitted, review all TBD items and ASSUMPTION labels recorded in the Specification Unified Assumption and TBD Register (see E-001 register).
2. For each open item, confirm:
   - Whether the item was resolved prior to submission (update register status to RESOLVED with resolution date and outcome)
   - Whether the item was submitted as TBD (confirm that the TBD notation is clearly stated in the submitted narrative)
   - Whether any assumption was overtaken by new information during the drafting process (update register accordingly)
3. Record lessons learned:
   - Were any coordination inputs (DEL-03-03, DEL-02-01, DEL-02-02) not available when needed? If so, document the impact on narrative quality and recommend sequencing adjustments for future proposals.
   - Were any ABC-related assumptions challenged during drafting? Document for future code consultant engagement timing.
4. Close the Assumption/TBD register for this deliverable by marking all items as either RESOLVED, DEFERRED (to detailed design), or ACCEPTED (no resolution needed).

**Output:** Updated Unified Assumption and TBD Register (closed); Lessons Learned summary (internal record).

**Effort:** 1 hour

---

## Verification

| Verification Point | Success Criteria | How Verified | Responsible |
|-------------------|-----------------|-------------|-------------|
| **V-01: Accessibility Completeness** | ACC-001 through ACC-006 all addressed in narrative | Check each requirement against completed narrative | Architect + Accessibility Consultant |
| **V-02: Adaptability Completeness** | ADAPT-001 through ADAPT-005 all addressed in narrative | Check each requirement against completed narrative | Architect + Structural Engineer |
| **V-03: Structural Coordination** | DEL-03-06 expansion provisions language is consistent with DEL-03-03 | Side-by-side review of structural grid, expansion direction, foundation, and utility routing descriptions | Lead Architect + Structural Engineer |
| **V-04: Site Constraint Accuracy** | Proposed expansion scenarios are within 12-acre usable area; flood fringe and wetland no-build zones acknowledged | Cross-check with Addendum 03 §1.1, Site Grading Plan, Wetland Assessment | Lead Architect + Civil Engineer |
| **V-05: ABC Reference Accuracy** | Narrative references Alberta Building Code by title; no specific clause numbers claimed unless confirmed during design | Review all ABC references in narrative | Architect + Code Consultant |
| **V-06: Concept Alignment** | Accessible features described in narrative are reflected in DEL-02-01 floor plan and DEL-02-02 site plan | Cross-check drawings against narrative | Lead Architect |
| **V-07: Terminology Consistency** | All terms consistent with other PKG-003 Design Brief deliverables and PKG-002 Conceptual Design deliverables | Terminology cross-check (see Step A7 table) | Proposal Manager |
| **V-08: Proposal Quality** | Narrative is clear, well-organized, persuasive, and professional; appropriate for formal RFP submission | Review by Proposal Manager and Design-Builder leadership | Proposal Manager |

---

## Records

### Documents Produced

- **Accessibility and Adaptability Narrative** (final narrative for RFP Response §7.1.3 and §7.1.5)
  - Format: Markdown (working draft); Word or PDF (submission format)
  - Location: `/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-06_AccessibilityAndAdaptabilityNarrative/`
  - Owner: Architect (Lead Author)

### Supporting Records (Retained During Production)

*(Enriched per F-002: minimum content requirements and format guidance added for each supporting record)*

| Record | Produced In | Format | Minimum Content Requirements |
|--------|-------------|--------|------------------------------|
| **Site Constraint Summary** | Step A2 | Markdown or PDF; 1-2 pages | (1) Map/sketch showing 12-acre usable area boundary and flood fringe no-build zone; (2) Table of feasible expansion directions with constraints for each; (3) Geotechnical data summary (bearing capacity range, groundwater depth); (4) Wetland buffer distances if applicable |
| **Structural Coordination Summary** | Step A3 | Markdown or PDF; 1-2 pages | (1) Agreed structural system type; (2) Structural grid / bay module dimensions; (3) Non-structural exterior wall location(s); (4) Foundation approach for future bay loads; (5) Utility chase routing locations; (6) Verbatim agreed terminology for cross-reference consistency between DEL-03-03 and DEL-03-06 |
| **MEP Coordination Summary** | Step A4 | Markdown or PDF; 1-2 pages | (1) HVAC distribution approach and future zone capacity; (2) Plumbing routing and extension points; (3) Electrical panel spare capacity percentage or target; (4) IT/data conduit spare capacity; (5) Generator sizing and future load accommodation; (6) Solar-ready provisions status |
| **Consistency Review Checklist** | Step A7 | Markdown table or spreadsheet | (1) Terminology cross-check results (per Step A7 table); (2) Numeric value consistency results; (3) Identified contradictions with disposition (resolved/added to Conflict Table); (4) Sign-off by reviewer |
| **Feedback and Revision Log** | Step A8 | Markdown or text | (1) Reviewer name and role; (2) Date of review; (3) Changes requested; (4) Changes made; (5) Disposition of any rejected changes |
| **Lessons Learned and Register Closure** | Step A9 | Markdown | (1) Updated Unified Assumption and TBD Register with final status; (2) Coordination sequencing lessons; (3) Recommendations for future proposals |

### Hand-off Criteria

Before narrative is handed off to the Proposal Manager for RFP Response assembly:
- Narrative reviewed and confirmed by Architect, Structural Engineer, and Proposal Manager
- All open Conflict Table items reviewed and resolved or flagged for Owner input
- All TBD items reviewed: if not resolvable at proposal stage, TBD notation is appropriate and documented
- Narrative formatted for consistency with other PKG-003 sections and ready for PDF assembly
- Version label: "FINAL" applied in document header/footer

### Integration into RFP Response

The narrative is integrated into the RFP Response document under Section 7 — Project Delivery Plan, in the following order:

| RFP Section | Content | Source Deliverable |
|-------------|---------|-------------------|
| 7.1.2 | Design Brief (5 sub-briefs) | DEL-03-01 through DEL-03-05 |
| 7.1.3 | Accessibility Narrative | DEL-03-06, Part 1 |
| 7.1.4 | Building Durability / Ease of Repair and Maintenance | PKG-005 |
| 7.1.5 | Adaptability, Flexibility, Potential for Expansion | DEL-03-06, Part 2 |

---

**Procedure Status:** DRAFT (Pass 3 enriched)
**Last Updated:** 2026-02-17
**Pass 3 enrichments applied:** A-003 (post-submission review Step A9), E-002 (minimum-viable input requirements for dependent deliverables), F-002 (format and minimum content for supporting records)
