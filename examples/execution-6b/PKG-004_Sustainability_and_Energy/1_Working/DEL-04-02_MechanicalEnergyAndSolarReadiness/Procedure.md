# Procedure — DEL-04-02: Mechanical Energy and Solar Readiness

---

## Purpose

This procedure documents the **workflow for producing the Mechanical Energy and Solar Readiness narrative** (DEL-04-02). The narrative is part of the RFP Design Brief (Section 7.1.2), scored under OBJ-004 (5 pts). It is authored by the Mechanical Engineer and coordinated with the Building Science consultant (DEL-04-01), Electrical Engineer (DEL-04-03), and Structural Engineer (DEL-02-03 — solar loading coordination).

The procedure covers production from initial scoping through final integration into the proposal package.

Source: Decomposition §6 OBJ-004; Decomposition §9 DEL-04-02 description; RFP SOW-0012.

---

## Prerequisites

The following must be in place or available before starting:

| Prerequisite | Resource | Notes |
|---|---|---|
| **RFP — Owner Statement of Requirements (OSR / Appendix A)** | Project source documents | Reference OSR energy/sustainability clauses |
| **Addendum 03 (Jul 31, 2024)** | Project source documents | Solar-capable roof; apparatus bay direct exhaust; PW bay ventilation; fill stations; sumps; 40 bunker gear lockers |
| **Functional Program (Appendix B)** | Project source documents | Room types, operational profile, DHW demand context |
| **Decomposition v2.3 FINAL** | Project repository | DEL-04-02 description; SOW-0012; PKG-004 scope |
| **DEL-04-01 (Building Envelope and Energy Strategy) — draft or concurrent** | PKG-004 sibling deliverable | Envelope U-value targets drive HVAC load and sizing assumptions |
| **DEL-02-04 (Mechanical Concept Narrative) — draft or concurrent** | PKG-002 deliverable | Baseline HVAC, plumbing, fire protection systems; energy narrative must align with and justify these |
| **DEL-04-03 (Electrical Energy Efficiency) — draft or concurrent** | PKG-004 sibling deliverable | Solar-ready electrical provisions (conduit, panel space, inverter location); coordinates with mechanical rough-in |
| **DEL-02-01/DEL-02-02 (Architectural/Civil Concept) — draft or concurrent** | PKG-002 deliverables | Building and roof orientation; solar-capable roof area location |
| **Geotechnical Investigation Report (2021)** | Appendix D (project source) | For ground-source heat pump feasibility assessment, if pursued; no additional investigation scope per DEC-013 |
| **NECB (applicable edition)** | Standards library | Energy code compliance pathway reference |

---

## Steps

### Step 1: Scope and Direction Confirmation

**Responsible:** Mechanical Engineer + Design Manager

**Actions:**
1. Read RFP Section 7.1.2 and understand the 5-point Design Brief scoring criteria — the narrative must explain rationale, not simply list systems.
2. Read Addendum 03, noting: solar-capable roof (flat/south/west/southwest orientation), apparatus bay direct exhaust (2 apparatus per bay), PW bay general ventilation (occasional idling + very occasional welding), bunker gear room ventilation, fill stations (2" × 2), bay sumps.
3. Review Functional Program (Appendix B) for operational profile — 24/7 operations, apparatus bay occupancy patterns, kitchen and residential DHW demand.
4. Confirm the design energy philosophy with Design Manager:
   - Is the goal NECB prescriptive compliance, performance-pathway enhancement, or net-zero ready?
   - Is the Owner interested in ground-source heat pump, or air-source/gas only?
   - Is solar-ready scope rough-in only (expected), or does the Owner want a full system designed?
5. Confirm that coordination meetings with DEL-04-01 and DEL-04-03 leads are scheduled.
6. Document scope assumptions in a brief memo or assumption list — these become the ASSUMPTION labels in the narrative.

**Outputs:** Scope confirmation memo; assumption list; coordination meeting schedule.

---

### Step 2: Cross-Discipline Coordination

**Responsible:** Mechanical Engineer + Architect/Building Science Lead + Electrical Engineer + Structural Engineer (as needed)

**Actions:**

**Coordination A — Envelope and HVAC Loads (with DEL-04-01 lead):**
- Obtain envelope U-value targets (walls, roof, glazing) from DEL-04-01 author.
- Confirm HVAC system sizing assumptions are consistent with those targets — if the envelope targets change, HVAC sizing claims must be updated.
- Align on overall energy performance target relative to NECB baseline (prescriptive vs. performance pathway).

**Coordination B — Solar Provisions (with DEL-04-03 lead and DEL-02-01/DEL-02-02 lead):**
- Determine roof orientation from architectural/civil concept: which face(s) of the roof are flat/south/west/southwest per Addendum 03 §1?
- Coordinate conduit routing from roof to mechanical room (solar thermal) and to electrical room (solar PV): single roof penetration strategy or separate routes?
- Confirm structural loading allowance required for future solar panels — coordinate with Structural Engineer to ensure load is captured in DEL-02-03.
- Define mechanical rough-in scope: pipe sleeves (solar thermal), conduit (PV wiring), space reservation in mechanical room, DHW tank port provision.

**Coordination C — Mechanical Concept Alignment (with DEL-02-04 lead):**
- Review HVAC system types and equipment selections documented in DEL-02-04.
- Confirm this energy narrative justifies those system choices from an energy angle — or flag if a different system type is preferred and reconcile the two documents.
- Ensure apparatus bay ventilation strategy in DEL-02-04 (direct exhaust) is consistent with energy narrative's heat recovery analysis.

**Output:** Coordination notes documenting resolved decisions and any open conflicts. At minimum, coordination notes must confirm:

- **(a) Confirmed envelope U-value targets from DEL-04-01** — wall, roof, and glazing U-values that drive HVAC load sizing assumptions in this narrative.
- **(b) Agreed solar conduit routing with DEL-04-03** — whether mechanical (solar thermal) and electrical (solar PV) conduit penetrations use a single shared roof penetration strategy or separate routes, and the confirmed routing path from roof to mechanical/electrical rooms.
- **(c) Confirmed HVAC system types from DEL-02-04** — equipment types and selections documented at the concept level that this energy narrative must justify from an energy perspective.

If any of these three outcomes are unresolved, the coordination notes must document the open item, assign a responsible party, and set a resolution deadline. Conflicts that cannot be resolved at this level are escalated to Design Manager and captured in Guidance.md Conflict Table.

Source: Semantic lensing item A-003.

---

### Step 3: Narrative Drafting

**Responsible:** Mechanical Engineer (lead drafter)

**Actions:**
1. Draft the narrative following the content structure defined in Specification.md (R-MEL-01 through R-MEL-13):
   - **Opening:** Purpose and facility energy context — why mechanical energy efficiency matters for this specific facility type.
   - **HVAC Zone Strategy:** Zone-by-zone approach (apparatus bays, PW bays, offices, residential quarters, shared spaces); equipment type and efficiency rationale.
   - **Heat Recovery:** Recovery opportunities by zone; constraints in apparatus bay exhaust; HRV/ERV scope.
   - **Ventilation Optimization:** DCV in PW bays; HRV in residential/office; apparatus bay exhaust strategy.
   - **Domestic Hot Water:** Water heater type, efficiency target, solar thermal rough-in provisions.
   - **Solar-Ready Roof Provisions:** Structural loading allowance (coordinated with DEL-02-03); mechanical rough-in (pipe sleeves, conduit); orientation rationale (Addendum 03 §1 cited explicitly).
   - **Energy Metering and Monitoring:** Whole-building metering; sub-metering strategy; controls/BEMS provisions.
   - **Energy Code Compliance:** NECB pathway; efficiency targets relative to code baseline.
   - **Maintainability Tie-In:** Key maintainability design decisions with energy efficiency implications (cross-reference DEL-05-03).
2. Tone: explain *why*, not just *what*. Address evaluators who include both technical and non-technical reviewers.
3. Label all assumptions explicitly as ASSUMPTION.
4. Include explicit cross-references to DEL-02-04, DEL-04-01, DEL-04-03 as required by R-MEL-09.
5. Target length: 2–4 pages (ASSUMPTION: appropriate for a Design Brief sub-brief).

**Output:** Draft narrative.

---

### Step 4: Internal Review and Revision

**Responsible:** Design Manager (primary reviewer) + Architect/Building Science Lead + Electrical Lead

**Checklist for reviewers:**

| Item | Check |
|---|---|
| All R-MEL-01 through R-MEL-13 requirements addressed | Yes / No / Partial |
| Addendum 03 requirements explicitly cited: solar-capable roof, apparatus bay direct exhaust, PW bay general ventilation, bunker gear room ventilation, fill station DHW interaction, bay sump energy implications | Yes / No |
| Cross-references to DEL-02-04, DEL-04-01, DEL-04-03 present | Yes / No |
| Assumptions labeled ASSUMPTION throughout | Yes / No |
| No contradictions with DEL-04-01 (envelope targets) or DEL-04-03 (solar electrical) | Yes / No |
| Language is clear and professional; no unexplained jargon | Yes / No |
| NECB compliance pathway credibly stated | Yes / No |
| Solar rough-in scope is explicit (structural loading, pipe sleeves, orientation, DHW port) | Yes / No |

Mechanical Engineer revises narrative based on feedback. Second review cycle if significant changes.

**Output:** Reviewed and revised draft narrative.

---

### Step 5: Cross-Document Consistency Check

**Responsible:** Mechanical Engineer + Design Manager

**Checks to perform:**

| Check | Verify | Action if Fail |
|---|---|---|
| Terminology consistent with Datasheet.md | Same terms used for system types, zones, solar provision elements | Update Datasheet or narrative to align |
| Requirements covered per Specification.md | R-MEL-01 through R-MEL-13 all addressed | Add missing content to narrative |
| Efficiency targets internally consistent | Same COP, SEER, AFUE values used across Datasheet, Specification, and narrative content | Reconcile values |
| Cross-references to DEL-04-01 and DEL-04-03 consistent | No contradictory efficiency claims or solar provision details | Update or escalate to Conflict Table |
| Conflict Table in Guidance.md updated | All unresolved conflicts captured with PROPOSAL column completed | Add any conflicts discovered during this check |
| ASSUMPTION labels consistent | All inferred content labeled in narrative and Specification | Add missing labels |
| Assumption register complete | Enumerate all ASSUMPTION labels across Datasheet, Specification, Guidance, and the draft narrative; verify each assumption is (a) still valid, (b) accurately stated, and (c) not contradicted by information obtained during coordination (Steps 1-2). Any new assumptions introduced during narrative drafting that are not already in the Datasheet or Specification must be captured in those documents as well. | Add missing assumptions to register; update or remove invalid assumptions |

**Output:** Consistency check pass/fail matrix; assumption register; Conflict Table updated if needed.

Source: Semantic lensing item X-004.

---

### Step 6: Proposal Manager Review and RFP Alignment Audit

**Responsible:** Proposal Manager

**Actions:**
1. Map RFP OSR energy/sustainability clauses to narrative sections — confirm coverage.
2. Verify Addendum 03 integration: solar-capable roof, apparatus bay direct exhaust, PW bay ventilation, fill stations, bay sumps — all addressed.
3. Confirm narrative is positioned correctly in the proposal document structure under RFP Section 7.1.2 (Design Brief, Mechanical sub-brief).
4. Flag any OSR clauses missed or any ambiguous compliance claims.

**Output:** RFP alignment audit checklist; any gaps flagged for revision.

---

### Step 7: Final Approval and Proposal Integration

**Responsible:** Mechanical Engineer + Design Manager + Proposal Manager

**Actions:**
1. Incorporate all feedback from Steps 4–6.
2. Final proofread for grammar, clarity, consistency.
3. Obtain sign-off from Mechanical Engineer (technical accuracy) and Design Manager (proposal quality).
4. Deliver finalized narrative to Proposal Manager for integration into the proposal PDF under Section 7.1.2.
5. Verify page count and formatting are consistent with rest of proposal.
6. Update proposal table of contents and cross-references.

**Output:** Final approved narrative; proposal PDF updated.

---

## Verification

| Verification Point | What to Check | Responsibility | Acceptance Criteria |
|---|---|---|---|
| **V-01: Requirements Coverage** | All R-MEL-01 through R-MEL-13 addressed in the narrative | Mechanical Lead + Design Manager | 13/13 requirements confirmed; checklist signed off |
| **V-02: Addendum 03 Integration** | Solar-capable roof orientation, apparatus bay direct exhaust strategy, PW bay demand-controlled ventilation, bunker gear room ventilation all explicitly addressed with Addendum 03 citation | Proposal Manager | Addendum 03 checklist items confirmed present |
| **V-03: Cross-Discipline Consistency** | Narrative consistent with DEL-04-01 (envelope thermal targets), DEL-04-03 (solar electrical rough-in), DEL-02-04 (mechanical concept systems) | Design Manager | No contradictions; or contradictions captured in Conflict Table |
| **V-04: Source Anchoring** | Non-trivial statements cite sources; inferred content labeled ASSUMPTION | Design Manager | Review: no unsupported assertions |
| **V-05: Code Compliance Credibility** | NECB compliance pathway is explicitly stated and credible | Mechanical Lead | NECB reference present; efficiency targets achievable |
| **V-06: Audience Appropriateness** | Narrative is clear, professional, readable for non-technical evaluators | Proposal Manager | Readability review: pass |

---

## Records

| Record | Format | Retention |
|---|---|---|
| Final approved narrative | Markdown / PDF (embedded in proposal) | Permanent (proposal archive) |
| Coordination meeting notes (Steps 1–2) | Email summary or minutes | 12 months |
| Internal review feedback (Step 4) | Tracked changes or comments | 12 months |
| Cross-document consistency check (Step 5) | Checklist | Permanent (design basis) |
| RFP alignment audit (Step 6) | Checklist | Permanent (compliance record) |
| Assumption log | Listed in narrative; archived separately | Permanent (design basis) |
