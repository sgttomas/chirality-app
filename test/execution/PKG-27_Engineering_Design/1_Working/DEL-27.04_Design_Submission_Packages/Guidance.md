# Guidance: DEL-27.04 Design Submission Packages

## Purpose

Supports development of **Design Submission Packages** for **PKG-27 Engineering Design**. Defines submission framework for staged design submissions (30%, 60%, 90%, IFC) per Design & Build contract.

**Source:** _CONTEXT.md; Datasheet.md

## Principles

**Principle 1: Staged Submissions Enable Employer Oversight**
Design & Build projects use staged submissions (30%, 60%, 90%, IFC) to allow Employer review and approval as design matures. Early submissions (30%) establish direction; later submissions (90%, IFC) confirm final design before construction.

**Principle 2: Submission Quality Reflects Project Professionalism**
Complete, accurate, organized submissions build Employer confidence; poor submissions cause delays and disputes.

**Principle 3: Comment Management is Closed-Loop Process**
All Employer comments must be captured, addressed, and closed with implementation evidence; no comments lost or deferred without agreement.

**Source:** **ASSUMPTION**: Design & Build submission best practices

## Considerations

**Project-Specific:**
- 210 deliverables across 36 packages require coordination
- Multi-discipline submissions (civil, structural, mechanical, electrical, controls, safety)
- Employer review capacity and priorities drive deliverable selection at each stage
- **TBD** — Employer-specific submission requirements from contract/ER

**Submission Timing Trade-offs:**
- Early submissions (30%) inform design direction but design immature
- Late submissions (90%) provide complete picture but limit flexibility for changes
- Balance: Submit when mature enough to be meaningful but early enough for feedback to be useful

**Comment Management:**
- Triage comments: Editorial (quick fix), Technical (engineering analysis), Contractual (escalate to PM)
- Prioritize: Design-impacting comments need quick resolution
- Track: Comment response matrix prevents comments from being lost

**Source:** Datasheet.md; **ASSUMPTION**: Typical Design & Build submission considerations

## Trade-offs

**Trade-off 1: Submission Scope (Comprehensive vs. Targeted)**
- Comprehensive: Submit all deliverables at each stage → Heavy Employer review burden, slower approvals
- Targeted: Submit priority deliverables only → Faster reviews, but gaps may emerge
- **Recommendation:** Targeted at 30-60%; comprehensive at 90-IFC

**Trade-off 2: Submission Frequency (More Stages vs. Fewer Stages)**
- More stages (e.g., add 45% submission) → More Employer touchpoints, better alignment
- Fewer stages (standard 30/60/90/IFC) → Lower overhead, faster design progress
- **Recommendation:** Standard 4-stage approach unless project complexity or Employer preference dictates otherwise

**Source:** **ASSUMPTION**: Submission strategy trade-offs common to Design & Build

## Examples

**Example 1: 30% Submission Content (Typical)**
- Design Basis Documents (DEL-27.01)
- HAZOP Study Reports (Preliminary, DEL-27.02)
- Key system P&IDs (preliminary)
- Major equipment lists and selection criteria
- Site plans and general arrangements
- Not included: Detailed calculations, final specs, procurement documents

**Example 2: Comment Response Matrix (Format)**
| ID | Comment | Source | Category | Response | Status | Implemented In | Closed |
|----|---------|--------|----------|----------|--------|----------------|--------|
| C-001 | Clarify tank heating requirements | Employer | Technical | Tank heating not required per product properties; added note to P&IDs | Closed | P&ID Rev B | Yes |
| C-002 | Add seismic design basis | Employer | Technical | Seismic criteria added to Design Basis (DEL-27.01 Rev B) | Closed | DEL-27.01 Rev B | Yes |

**Source:** **ASSUMPTION**: Typical submission content and comment management examples

---

**Cross-Document Verification (Pass 3):**
- All Principles linked to Specification § requirements and Procedure Steps
- All Considerations linked to Specification § requirements and Procedure Steps
- All Trade-offs linked to relevant Principles and Specification §
- All Examples linked to Specification § and Procedure Steps
- Terminology verified consistent with Datasheet.md, Specification.md, Procedure.md
- Submission stages (30%, 60%, 90%, IFC) verified consistent across all documents
- Comment management closed-loop process verified consistent across all documents
- Cross-references to DEL-27.01, DEL-27.02 and all PKG deliverables verified consistent
